"""Reporting schemes for the two applications.

Modes (paper Sec. V.A, Table II):
  raw             - conventional periodic payload reporting (baseline), 15-min period
  compressed      - conventional ~2:1 compression reference, 15-min period
  event_triggered - deterministic event-triggering reference (raw payload on trigger)
  semantic        - task-oriented: compact task output + admission control,
                    6-hourly heartbeat, one raw audit sample per day

Each ``run_*`` function takes a trace DataFrame and the configs and returns a
DataFrame of admitted reports with columns:
    t_gen_h   generation time (hours)
    L_app     application payload bytes
    H         overhead bytes
    kind      'periodic' | 'event' | 'decision' | 'warning' | 'heartbeat' | 'audit'
    conf      confidence in [0,1] for task outputs (NaN otherwise)

Semantic thresholds (margin / persistence) are tuned on held-out tuning traces
in stage3.tune_semantic(); the defaults below are the starting point.
"""
import numpy as np
import pandas as pd

from . import stage3 as _st3  # device uses the same rule as the receiver


# ---------------------------------------------------------------- agriculture

def run_raw_agri(df, modes):
    m = modes["raw"]
    step = int(m["period_min"] / 15)  # trace sensing step is 15 min
    idx = np.arange(0, len(df), step)
    return pd.DataFrame({
        "t_gen_h": df["t_h"].iloc[idx].values,
        "L_app": m["L_app"], "H": m["H"], "kind": "periodic", "conf": np.nan,
        "obs": df["sm_obs"].iloc[idx].values,  # transmitted observation (for receiver)
    })


def run_compressed_agri(df, modes):
    m = modes["compressed"]
    step = int(m["period_min"] / 15)
    idx = np.arange(0, len(df), step)
    return pd.DataFrame({
        "t_gen_h": df["t_h"].iloc[idx].values,
        "L_app": m["L_app"], "H": m["H"], "kind": "periodic", "conf": np.nan,
        "obs": df["sm_obs"].iloc[idx].values,
    })


def run_event_agri(df, modes, task):
    m = modes["event_triggered"]
    delta = task["et_delta_sm"]
    sm = df["sm_obs"].values
    thr = df["sm_thr"].values
    t = df["t_h"].values
    reps, last_tx = [], sm[0]
    prev_below = sm[0] < thr[0]
    for i in range(len(df)):
        below = sm[i] < thr[i]
        if abs(sm[i] - last_tx) > delta or (below != prev_below):
            reps.append(i)
            last_tx = sm[i]
        prev_below = below
    return pd.DataFrame({
        "t_gen_h": t[reps], "L_app": m["L_app"], "H": m["H"],
        "kind": "event", "conf": np.nan, "obs": sm[reps],
    })


def run_semantic_agri(df, modes, task, thr_offset=0.0):
    """Device-side irrigation decision.

    Emits a compact 'irrigate' decision when the observed soil moisture stays
    below (stage threshold + offset) for ``persist_confirm`` consecutive
    samples. Heartbeat every 6 h, one raw audit sample per day.
    """
    m = modes["semantic"]
    t = df["t_h"].values
    thr = df["sm_thr"].values + thr_offset
    persist = task["persist_confirm"]
    hyst = task.get("hysteresis", 0.0)
    smooth = task.get("smooth", 1)
    rows = []
    # the device applies exactly the same rule the receiver would
    for (s, e) in _st3.rule_below(t, df["sm_obs"].values, thr, persist, hyst,
                                  smooth):
        margin = float(np.clip((thr[s] - df["sm_obs"].values[s]) / 0.05, 0, 1))
        conf = 0.5 + 0.5 * margin
        rows.append((t[s], m["L_app"], m["H"], "decision", conf))
    # heartbeats
    hb_step_h = m["heartbeat_h"]
    for hh in np.arange(0, t[-1], hb_step_h):
        rows.append((hh, m["L_app"], m["H"], "heartbeat", np.nan))
    # daily raw audit samples
    for dd in np.arange(0, t[-1], 24.0):
        rows.append((dd, 200, m["H"], "audit", np.nan))
    rep = pd.DataFrame(rows, columns=["t_gen_h", "L_app", "H", "kind", "conf"])
    rep["obs"] = np.nan
    return rep.sort_values("t_gen_h").reset_index(drop=True)


# ---------------------------------------------------------------- environment

def _env_report_idx(df, period_min, dt_min=5):
    step = int(period_min / dt_min)
    return np.arange(0, len(df), step)


def run_raw_env(df, modes):
    m = modes["raw"]
    idx = _env_report_idx(df, m["period_min"])
    return pd.DataFrame({
        "t_gen_h": df["t_h"].iloc[idx].values,
        "L_app": m["L_app"], "H": m["H"], "kind": "periodic", "conf": np.nan,
        "obs": df["level_obs"].iloc[idx].values,
    })


def run_compressed_env(df, modes):
    m = modes["compressed"]
    idx = _env_report_idx(df, m["period_min"])
    return pd.DataFrame({
        "t_gen_h": df["t_h"].iloc[idx].values,
        "L_app": m["L_app"], "H": m["H"], "kind": "periodic", "conf": np.nan,
        "obs": df["level_obs"].iloc[idx].values,
    })


def run_event_env(df, modes, danger=4.5, delta_level=0.3):
    m = modes["event_triggered"]
    lv = df["level_obs"].values
    t = df["t_h"].values
    reps, last_tx = [], lv[0]
    prev_above = lv[0] > danger
    for i in range(len(df)):
        above = lv[i] > danger
        if abs(lv[i] - last_tx) > delta_level or (above != prev_above):
            reps.append(i)
            last_tx = lv[i]
        prev_above = above
    return pd.DataFrame({
        "t_gen_h": t[reps], "L_app": m["L_app"], "H": m["H"],
        "kind": "event", "conf": np.nan, "obs": lv[reps],
    })


def run_semantic_env(df, modes, task, thr_offset=0.0, danger=4.5):
    """Device-side flood warning.

    Emits a compact warning when the observed level stays above
    (danger + offset) for ``persist_confirm`` consecutive samples.
    Heartbeat every 6 h, one raw audit sample per day.
    """
    m = modes["semantic"]
    lv = df["level_obs"].values
    t = df["t_h"].values
    thr = danger + thr_offset
    persist = task["persist_confirm"]
    hyst = task.get("hysteresis", 0.0)
    smooth = task.get("smooth", 1)
    rows = []
    for (s, e) in _st3.rule_above(t, df["level_obs"].values, thr, persist,
                                  hyst, smooth):
        margin = float(np.clip((df["level_obs"].values[s] - thr) / 1.0, 0, 1))
        conf = 0.5 + 0.5 * margin
        rows.append((t[s], m["L_app"], m["H"], "warning", conf))
    hb_step_h = m["heartbeat_h"]
    for hh in np.arange(0, t[-1], hb_step_h):
        rows.append((hh, m["L_app"], m["H"], "heartbeat", np.nan))
    for dd in np.arange(0, t[-1], 24.0):
        rows.append((dd, 200, m["H"], "audit", np.nan))
    rep = pd.DataFrame(rows, columns=["t_gen_h", "L_app", "H", "kind", "conf"])
    rep["obs"] = np.nan
    return rep.sort_values("t_gen_h").reset_index(drop=True)


AGRI_RUNNERS = {
    "raw": run_raw_agri,
    "compressed": run_compressed_agri,
    "event_triggered": run_event_agri,
    "semantic": run_semantic_agri,
}
ENV_RUNNERS = {
    "raw": run_raw_env,
    "compressed": run_compressed_env,
    "event_triggered": run_event_env,
    "semantic": run_semantic_env,
}
