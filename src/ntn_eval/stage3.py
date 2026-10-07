"""Stage 3: application task evaluation (paper Sec. VII.C).

Task outcomes are scored against ground-truth events on held-out traces
(split by site/season via separate seeds, never random interleaving).

The device (semantic) and the receiver (raw/compressed/event-triggered) both
apply a threshold + persistence + hysteresis rule. The rule produces latch
EPISODES (start, end): the device transmits one compact decision at each
episode start. Scoring is episode-based:

  * hit:  an episode overlapping [onset, onset + D] whose trigger report was
          delivered no later than onset + D.  (A latch already held from a
          slightly early firing still covers the event -- operationally the
          receiver knows irrigation is needed.)
  * false alarm: an episode overlapping no event window
          [onset - early_h, onset + D].
  * detection delay / timing error are reported so early firing is visible
    instead of being hidden.

Comparison discipline (paper Sec. V.A): raw / compressed / event-triggered
modes use the SAME rule at the receiver applied to their delivered
observation series (forward-filled onto the sensing grid) -- the best
receiver-side task model under the same training information, so payload
modes are not handicapped with a weaker classifier.
"""
import numpy as np
import pandas as pd

INF = float("inf")


# ------------------------------------------------------------ decision rules

def _episodes_from_latch(t, cond, reset):
    """Generic latch: cond starts an episode after `persist` is handled by
    caller; reset ends it. Returns list of (start_idx, end_idx)."""
    episodes, start, in_ev = [], None, False
    for i in range(len(t)):
        if cond[i] and not in_ev:
            in_ev, start = True, i
        elif in_ev and reset[i]:
            episodes.append((start, i))
            in_ev = False
    if in_ev:
        episodes.append((start, len(t) - 1))
    return episodes


def _smooth_causal(x, w):
    """Causal moving average (uses samples up to and including i)."""
    x = np.asarray(x, float)
    w = int(w)
    if w <= 1 or len(x) == 0:
        return x
    w = min(w, len(x))
    c = np.cumsum(np.insert(x, 0, 0.0))
    head = c[1:w] / np.arange(1, w)
    tail = (c[w:] - c[:-w]) / w
    return np.concatenate([head, tail])


def rule_below(t, obs, thr, persist, hyst=0.0, smooth=1):
    """Episodes where (smoothed) obs stays < thr for >= persist samples.

    Rising edge fires after `persist` consecutive below-threshold samples;
    the latch resets only when obs clears thr + hyst (anti-chatter).
    A causal moving average of length `smooth` conditions the sensor noise
    before thresholding -- applied identically on device and receiver.
    Returns list of (start_idx, end_idx) into t.
    """
    obs = _smooth_causal(obs, smooth)
    thr = np.asarray(thr)
    below = obs < thr
    run = np.zeros(len(t), dtype=int)
    if len(t):
        run[0] = 1 if below[0] else 0
    for i in range(1, len(t)):
        run[i] = run[i - 1] + 1 if below[i] else 0
    fire = run >= persist
    reset = obs > thr + hyst
    episodes, start, in_ev = [], None, False
    for i in range(len(t)):
        if fire[i] and not in_ev:
            in_ev, start = True, i
        elif in_ev and reset[i]:
            episodes.append((start, i))
            in_ev = False
    if in_ev:
        episodes.append((start, len(t) - 1))
    return episodes


def rule_above(t, obs, thr, persist, hyst=0.0, smooth=1):
    """Episodes where (smoothed) obs stays > thr for >= persist samples."""
    obs = _smooth_causal(obs, smooth)
    thr = np.asarray(thr)
    above = obs > thr
    run = np.zeros(len(t), dtype=int)
    if len(t):
        run[0] = 1 if above[0] else 0
    for i in range(1, len(t)):
        run[i] = run[i - 1] + 1 if above[i] else 0
    fire = run >= persist
    reset = obs < thr - hyst
    episodes, start, in_ev = [], None, False
    for i in range(len(t)):
        if fire[i] and not in_ev:
            in_ev, start = True, i
        elif in_ev and reset[i]:
            episodes.append((start, i))
            in_ev = False
    if in_ev:
        episodes.append((start, len(t) - 1))
    return episodes


def ffill_to_grid(t_grid, t_rep, obs_rep):
    """Forward-fill irregular received observations onto the sensing grid."""
    order = np.argsort(t_rep)
    tr, obr = np.asarray(t_rep)[order], np.asarray(obs_rep)[order]
    idx = np.searchsorted(tr, t_grid, side="right") - 1
    idx = np.clip(idx, 0, len(tr) - 1)
    out = obr[idx]
    return out


# ------------------------------------------------------------ event scoring

def score_episodes(ep_starts, ep_ends, ep_delays, events, D_h, early_h,
                   T_obs_h):
    """Score latch episodes against ground-truth events.

    ep_starts/ends in hours, ep_delays in hours (inf = trigger lost).
    """
    events = events.reset_index(drop=True)
    n_ev = len(events)
    hits, det_delays, timing_err = 0, [], []
    used = np.zeros(len(ep_starts), dtype=bool)
    for _, ev in events.iterrows():
        o = ev["onset_h"]
        best = None
        for j in range(len(ep_starts)):
            if used[j] or np.isinf(ep_delays[j]):
                continue
            s, e = ep_starts[j], ep_ends[j]
            if not (s <= o + D_h and e >= o):
                continue
            tdel = s + ep_delays[j]
            if tdel <= o + D_h:
                if best is None or tdel < best[0]:
                    best = (tdel, j)
        if best is not None:
            hits += 1
            used[best[1]] = True
            det_delays.append(best[0] - o)
            timing_err.append(abs(ep_starts[best[1]] - o))
    fa = 0
    for j in range(len(ep_starts)):
        if used[j] or np.isinf(ep_delays[j]):
            continue
        s, e = ep_starts[j], ep_ends[j]
        matched = any((s <= ev["onset_h"] + D_h and e >= ev["onset_h"] - early_h)
                      for _, ev in events.iterrows())
        if not matched:
            fa += 1
    weeks = T_obs_h / (24.0 * 7.0)
    return {
        "n_events": n_ev, "n_hit": hits,
        "p_miss": (n_ev - hits) / n_ev if n_ev else float("nan"),
        "recall": hits / n_ev if n_ev else float("nan"),
        "fa_per_week": fa / weeks if weeks else 0.0,
        "n_fa": fa,
        "mean_det_delay_h": float(np.mean(det_delays)) if det_delays else float("nan"),
        "mean_timing_err_h": float(np.mean(timing_err)) if timing_err else float("nan"),
    }


# ------------------------------------------------------------ per-mode outputs

def _trigger_delays(ep_start_idx, t_rep, rep_delays):
    """Delivery delay of the received report triggering each episode."""
    tr = np.asarray(t_rep)
    out = np.empty(len(ep_start_idx))
    for k, i in enumerate(ep_start_idx):
        j = min(np.searchsorted(tr, i, side="right") - 1, len(tr) - 1)
        out[k] = rep_delays[j]
    return out


def task_outputs_agri(df, reports, delays, mode, offset, persist, hyst=0.0,
                      smooth=1):
    """Return (ep_starts_h, ep_ends_h, ep_delays_h) for one trace+mode."""
    t = df["t_h"].values
    thr = df["sm_thr"].values + offset
    if mode == "semantic":
        eps = rule_below(t, df["sm_obs"].values, thr, persist, hyst, smooth)
        dec = reports[reports["kind"] == "decision"]
        dmap = dict(zip(dec["t_gen_h"].values,
                        np.asarray(delays)[[reports.index.get_loc(i)
                                            for i in dec.index]]))
        starts = np.array([t[s] for s, _ in eps])
        ends = np.array([t[e] for _, e in eps])
        dls = np.array([dmap.get(ts, INF) for ts in starts])
        return starts, ends, dls
    rx = reports[np.isfinite(delays)].reset_index(drop=True)
    rdl = np.asarray(delays)[np.isfinite(delays)]
    if len(rx) == 0:
        return np.array([]), np.array([]), np.array([])
    grid_obs = ffill_to_grid(t, rx["t_gen_h"].values, rx["obs"].values)
    eps = rule_below(t, grid_obs, thr, persist, hyst, smooth)
    starts = np.array([t[s] for s, _ in eps])
    ends = np.array([t[e] for _, e in eps])
    # trigger = received sample at/before episode start (grid index -> time)
    trig_t = np.array([t[s] for s, _ in eps])
    dls = _trigger_delays(trig_t, rx["t_gen_h"].values, rdl)
    return starts, ends, dls


def task_outputs_env(df, reports, delays, mode, offset, persist, danger,
                     hyst=0.0, smooth=1):
    t = df["t_h"].values
    thr = danger + offset
    if mode == "semantic":
        eps = rule_above(t, df["level_obs"].values, thr, persist, hyst,
                         smooth)
        dec = reports[reports["kind"] == "warning"]
        dmap = dict(zip(dec["t_gen_h"].values,
                        np.asarray(delays)[[reports.index.get_loc(i)
                                            for i in dec.index]]))
        starts = np.array([t[s] for s, _ in eps])
        ends = np.array([t[e] for _, e in eps])
        dls = np.array([dmap.get(ts, INF) for ts in starts])
        return starts, ends, dls
    rx = reports[np.isfinite(delays)].reset_index(drop=True)
    rdl = np.asarray(delays)[np.isfinite(delays)]
    if len(rx) == 0:
        return np.array([]), np.array([]), np.array([])
    grid_obs = ffill_to_grid(t, rx["t_gen_h"].values, rx["obs"].values)
    eps = rule_above(t, grid_obs, thr, persist, hyst, smooth)
    starts = np.array([t[s] for s, _ in eps])
    ends = np.array([t[e] for _, e in eps])
    trig_t = np.array([t[s] for s, _ in eps])
    dls = _trigger_delays(trig_t, rx["t_gen_h"].values, rdl)
    return starts, ends, dls


# ------------------------------------------------------------ threshold tuning

def tune_offset_agri(tuning, modes, task, grid):
    """Pick sm threshold offset on tuning traces: meet miss target, min reports."""
    persist = task["persist_confirm"]
    hyst = task.get("hysteresis", 0.0)
    smooth = task.get("smooth", 1)
    D_h = task["deadline_h"]
    best = None
    for off in grid:
        tot_ev = tot_hit = tot_dec = 0
        for df, events in tuning:
            reps = _semantic_reports(df, modes, task, off)
            starts, ends, _ = task_outputs_agri(
                df, reps, np.zeros(len(reps)), "semantic", off, persist, hyst,
                smooth)
            s = score_episodes(starts, ends, np.zeros(len(starts)), events,
                               D_h, early_h=2.0,
                               T_obs_h=float(df["t_h"].iloc[-1]))
            tot_ev += s["n_events"]
            tot_hit += s["n_hit"]
            tot_dec += len(starts)
        p_miss = (tot_ev - tot_hit) / tot_ev if tot_ev else 1.0
        cand = (p_miss, tot_dec, off)
        if best is None or (p_miss <= task["miss_target"] and
                            (best[0] > task["miss_target"] or tot_dec < best[1])):
            best = cand
        elif best[0] > task["miss_target"] and p_miss < best[0]:
            best = cand
    return {"offset": best[2], "p_miss_tuning": best[0], "n_episodes": best[1]}


def _semantic_reports(df, modes, task, off):
    from . import schemes
    return schemes.run_semantic_agri(df, modes, task, thr_offset=off)


def tune_offset_env(tuning, modes, task, danger, grid):
    persist = task["persist_confirm"]
    hyst = task.get("hysteresis", 0.0)
    smooth = task.get("smooth", 1)
    D_h = task["deadline_min"] / 60.0
    best = None
    for off in grid:
        tot_ev = tot_hit = tot_warn = 0
        for df, events, _ in tuning:
            from . import schemes
            reps = schemes.run_semantic_env(df, modes, task, thr_offset=off,
                                            danger=danger)
            starts, ends, _ = task_outputs_env(
                df, reps, np.zeros(len(reps)), "semantic", off, persist,
                danger, hyst, smooth)
            s = score_episodes(starts, ends, np.zeros(len(starts)), events,
                               D_h, early_h=0.25,
                               T_obs_h=float(df["t_h"].iloc[-1]))
            tot_ev += s["n_events"]
            tot_hit += s["n_hit"]
            tot_warn += len(starts)
        p_miss = (tot_ev - tot_hit) / tot_ev if tot_ev else 1.0
        cand = (p_miss, tot_warn, off)
        if best is None or (p_miss <= task["miss_target"] and
                            (best[0] > task["miss_target"] or tot_warn < best[1])):
            best = cand
        elif best[0] > task["miss_target"] and p_miss < best[0]:
            best = cand
    return {"offset": best[2], "p_miss_tuning": best[0], "n_episodes": best[1]}


# ------------------------------------------------------------ drift experiment

def drift_detector_baseline(tuning_dry, obs_col):
    """Baseline daily-mean obs statistics from dry-season tuning traces."""
    vals = []
    for df, *_ in tuning_dry:
        d = df.copy()
        d["day"] = (d["t_h"] // 24).astype(int)
        vals.extend(d.groupby("day")[obs_col].mean().values)
    vals = np.array(vals)
    return float(vals.mean()), float(vals.std())


def _fallback_windows(df, obs_col, mu, sigma, win_h=24.0):
    d = df.copy()
    d["day"] = (d["t_h"] // 24).astype(int)
    daily = d.groupby("day")[obs_col].mean()
    roll = daily.rolling(7, min_periods=1).mean()
    trig_days = roll[np.abs(roll - mu) > 3 * sigma].index.values
    wins = []
    for day in trig_days:
        s = float(day * 24)
        if wins and s <= wins[-1][1] + 1e-9:
            wins[-1] = (wins[-1][0], s + win_h)
        else:
            wins.append((s, s + win_h))
    return wins


def fallback_windows_agri(df, mu, sigma, win_h=24.0):
    return _fallback_windows(df, "sm_obs", mu, sigma, win_h)


def fallback_windows_env(df, mu, sigma, win_h=24.0):
    return _fallback_windows(df, "level_obs", mu, sigma, win_h)
