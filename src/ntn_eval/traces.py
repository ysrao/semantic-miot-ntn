"""Seeded synthetic traces for the two evaluation applications.

Both generators use numpy.random.Generator with a fixed integer seed, so every
trace is exactly reproducible. The generators model ground-truth state
(``*_true`` columns) separately from noisy device observations (``*_obs``
columns); task metrics in stage 3 are always scored against ground truth.

Application 1 — smart agriculture (India-oriented lens):
    90-day trace at 15-min sensing steps. A soil water-balance bucket is driven
    by monsoon-phase rainfall, temperature and humidity. Ground-truth
    irrigation-need events occur when true soil moisture stays below the
    crop-stage threshold for ``event_persist_h``.

Application 2 — environmental monitoring (India-oriented lens):
    90-day trace at 5-min sensing steps. River/reservoir level responds to
    catchment rainfall with a lag and recession constant. Ground-truth flood
    events occur when the true level exceeds ``danger_level_m`` for
    ``event_persist_min``. A few cloudburst episodes create sharp, rare events.
"""
import numpy as np
import pandas as pd

ROOT_DEPTH_MM = 500.0  # effective root-zone depth for the soil bucket


def _phase_at(t_days, phases):
    for p in phases:
        if p["start"] <= t_days < p["end"]:
            return p
    return phases[-1]


def _rain_events(rng, n_steps, dt_h, phases, t_days, rain_noise):
    """Poisson rain events; returns intensity series in mm/h."""
    rain = np.zeros(n_steps)
    # per-phase event rate -> homogeneous within each step via phase lookup
    for i in range(n_steps):
        p = _phase_at(t_days[i], phases)
        lam_step = p["rain_lambda"] / 24.0 * dt_h  # events per step
        if rng.random() < lam_step:
            dur_h = rng.exponential(2.0)
            inten = p["rain_mean"] * rng.lognormal(0.0, rain_noise)
            j_end = min(n_steps, i + max(1, int(dur_h / dt_h)))
            rain[i:j_end] = np.maximum(rain[i:j_end], inten)
    return rain


def gen_agri_trace(seed, cfg):
    """Generate one agriculture trace. Returns (DataFrame, events DataFrame)."""
    tr = cfg["trace"]
    rng = np.random.default_rng(seed)
    dt_h = tr["dt_min"] / 60.0
    n = int(tr["days"] * 24 * 60 / tr["dt_min"])
    t_h = np.arange(n) * dt_h
    t_days = t_h / 24.0

    phases = tr["phases"]
    rain = _rain_events(rng, n, dt_h, phases, t_days, tr["rain_noise"])

    temp, rh = np.zeros(n), np.zeros(n)
    for i in range(n):
        p = _phase_at(t_days[i], phases)
        hour = t_h[i] % 24
        temp[i] = (p["temp"] + tr["temp_diurnal_amp"] * np.sin(2 * np.pi * (hour - 14) / 24)
                   + rng.normal(0, tr["temp_noise"]))
        rh[i] = np.clip(p["rh"] + 0.12 * np.sin(2 * np.pi * (hour - 8) / 24)
                        + rng.normal(0, tr["rh_noise"]), 0.05, 1.0)

    # Crop stage and threshold per step (needed before the SM loop)
    stage_name = np.empty(n, dtype=object)
    sm_thr = np.zeros(n)
    for i in range(n):
        for s in tr["crop_stages"]:
            if s["start"] <= t_days[i] < s["end"]:
                stage_name[i] = s["name"]
                sm_thr[i] = s["sm_threshold"]
                break

    # Soil water-balance bucket (volumetric fraction) with reference
    # irrigation actuation: when true SM stays below the stage threshold for
    # event_persist_h, the reference farm controller irrigates (SM refilled).
    # Ground-truth events are these actuation onsets; the NTN task is for the
    # device/receiver to reproduce the irrigation decision remotely.
    sm = np.zeros(n)
    sm[0] = tr["sm_init"]
    fc, wp = tr["field_capacity"], tr["wilting_point"]
    persist_n = int(tr["event_persist_h"] / dt_h)
    need = np.zeros(n, dtype=bool)
    below_run, run_start = 0, 0
    for i in range(1, n):
        infil = tr["infiltration_frac"] * rain[i] * dt_h / ROOT_DEPTH_MM
        et = (tr["et0_mm_day"] / 24.0 * (1 + 0.05 * (temp[i] - 30.0))
              * (1.2 - rh[i]) * dt_h / ROOT_DEPTH_MM)
        sm[i] = sm[i - 1] + infil - et
        if sm[i] > fc:
            sm[i] -= (sm[i] - fc) * tr["drainage_rate"] * dt_h
        sm[i] = float(np.clip(sm[i], wp - 0.03, 0.55))
        if sm[i] < sm_thr[i]:
            if below_run == 0:
                run_start = i
            below_run += 1
        else:
            below_run = 0
        if below_run >= persist_n:
            # reference actuation: irrigate, marking the qualifying run
            need[run_start:i + 1] = True
            sm[i] = tr["irrig_refill_frac"] * fc
            below_run = 0

    # Noisy observations
    sm_obs = sm + rng.normal(0, tr["sensor_noise_sm"], n)
    temp_obs = temp + rng.normal(0, tr["sensor_noise_temp"], n)
    rh_obs = np.clip(rh + rng.normal(0, tr["sensor_noise_rh"], n), 0.05, 1.0)

    # (Ground-truth irrigation need was marked during the actuated SM loop.)

    # Strata labels (priority: irrigation > heavy_rain > monsoon > normal > dry)
    strata = np.empty(n, dtype=object)
    for i in range(n):
        p = _phase_at(t_days[i], phases)
        if need[i]:
            strata[i] = "irrigation"
        elif rain[i] > 10.0:
            strata[i] = "heavy_rain"
        elif p["name"] == "monsoon":
            strata[i] = "monsoon"
        elif rain[i] > 0.5:
            strata[i] = "normal_rainfall"
        else:
            strata[i] = "dry"

    df = pd.DataFrame({
        "t_h": t_h, "phase": [_phase_at(d, phases)["name"] for d in t_days],
        "rain_mm_h": rain, "temp_C": temp, "rh": rh,
        "sm_true": sm, "sm_obs": sm_obs, "temp_obs": temp_obs, "rh_obs": rh_obs,
        "crop_stage": stage_name, "sm_thr": sm_thr,
        "irrig_need": need, "stratum": strata,
    })
    events = _events_from_bool(t_h, need)
    return df, events


def _events_from_bool(t_h, flag):
    """Return DataFrame of [onset_h, end_h] for each contiguous True run."""
    events, onset = [], None
    for i, f in enumerate(flag):
        if f and onset is None:
            onset = t_h[i]
        elif not f and onset is not None:
            events.append((onset, t_h[i - 1]))
            onset = None
    if onset is not None:
        events.append((onset, t_h[-1]))
    return pd.DataFrame(events, columns=["onset_h", "end_h"])


def gen_env_trace(seed, cfg):
    """Generate one environment trace. Returns (DataFrame, events, bursts)."""
    tr = cfg["trace"]
    rng = np.random.default_rng(seed)
    dt_h = tr["dt_min"] / 60.0
    dt_min = tr["dt_min"]
    n = int(tr["days"] * 24 * 60 / dt_min)
    t_h = np.arange(n) * dt_h
    t_days = t_h / 24.0
    phases = tr["phases"]

    rain = _rain_events(rng, n, dt_h, phases, t_days, tr["rain_noise"])
    temp = np.zeros(n)
    for i in range(n):
        p = _phase_at(t_days[i], phases)
        hour = t_h[i] % 24
        temp[i] = (p["temp"] + tr["temp_diurnal_amp"] * np.sin(2 * np.pi * (hour - 14) / 24)
                   + rng.normal(0, tr["temp_noise"]))

    # Cloudburst episodes during monsoon -> sharp rare events
    bursts = []
    monsoon_days = [d for d in range(35, 70)]
    b = tr["burst"]
    for k in range(b["n_episodes"]):
        onset_day = float(rng.choice(monsoon_days)) + rng.random()
        onset_i = int(onset_day * 24 / dt_h)
        dur_i = int(2.0 / dt_h)  # 2-h cloudburst
        rain[onset_i:onset_i + dur_i] += b["extra_rain_mm_h"]
        bursts.append({"onset_h": onset_i * dt_h, "dur_h": 2.0})
    bursts = pd.DataFrame(bursts)

    # River level: lagged, smoothed response to catchment rainfall
    lag_i = int(tr["level_lag_h"] / dt_h)
    decay = np.exp(-dt_h / tr["level_decay_h"])
    s = np.zeros(n)
    for i in range(1, n):
        s[i] = s[i - 1] * decay + rain[i] * dt_h
    level_true = np.zeros(n)
    for i in range(n):
        j = max(0, i - lag_i)
        level_true[i] = tr["level_base_m"] + tr["level_gain"] * s[j]

    level_obs = level_true + rng.normal(0, tr["level_noise"], n)
    rain_obs = np.maximum(0, rain * rng.lognormal(0, tr["rain_noise_level"], n))

    persist_n = int(tr["event_persist_min"] / dt_min)
    danger = tr["danger_level_m"]
    fhyst = tr.get("flood_hyst_m", 0.3)
    above = level_true > danger
    flood = np.zeros(n, dtype=bool)
    run, in_flood = 0, False
    for i in range(n):
        # flood episode: starts after `persist_n` above danger, ends when the
        # level recedes below danger - hysteresis (same latch semantics as
        # the warning device, so a multi-peak flood is one ground-truth event)
        run = run + 1 if above[i] else 0
        if not in_flood and run >= persist_n:
            in_flood = True
            flood[i - persist_n + 1:i + 1] = True
        elif in_flood:
            if level_true[i] < danger - fhyst:
                in_flood = False
            else:
                flood[i] = True

    strata = np.empty(n, dtype=object)
    for i in range(n):
        p = _phase_at(t_days[i], phases)
        if flood[i]:
            strata[i] = "heavy_rain"
        elif rain[i] > 10.0:
            strata[i] = "heavy_rain"
        elif p["name"] == "monsoon":
            strata[i] = "monsoon"
        elif rain[i] > 0.5:
            strata[i] = "normal_rainfall"
        else:
            strata[i] = "dry"

    df = pd.DataFrame({
        "t_h": t_h, "phase": [_phase_at(d, phases)["name"] for d in t_days],
        "rain_mm_h": rain, "temp_C": temp,
        "level_true": level_true, "level_obs": level_obs, "rain_obs": rain_obs,
        "flood": flood, "stratum": strata,
    })
    events = _events_from_bool(t_h, flood)
    return df, events, bursts
