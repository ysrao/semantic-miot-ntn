"""Stage 1: deterministic accounting (paper Sec. VII.A).

No stochastic simulator. For each source trace and mode this records generated
observations, admitted reports, application/metadata bytes, overhead, the
repetition factor, and resulting airtime, then computes:

  eq (1):  B_x   = N_x (H + L_x)            offered information volume
  eq (2):  T_msg = T_RA + K 8(H+L)/R        airtime per admitted report
  eq (7):  q     = N_sem / N_raw            semantic report fraction
  eq (8):  G_B   = (H+L_raw) / [q (H+L_sem)]  offered-byte gain
  eq (9):  G_air = T_msg,raw / [q T_msg,sem]  airtime gain
  eq (10): G_TO  = (C_sem/C_raw) G_air        task-throughput-efficiency gain

C_x (correct, timely task outcomes) is filled in by Stage 3; Stage 1 reports
the resource side of eq (10).
"""
import numpy as np


def t_msg(H, L, T_RA, K, R):
    """Airtime of one admitted report, eq (2). All sizes in bytes."""
    return T_RA + K * 8.0 * (H + L) / R


def gain_B(H, L_raw, L_x, q):
    """Offered-byte gain of mode x vs raw, eq (8)."""
    return (H + L_raw) / (q * (H + L_x))


def gain_air(T_msg_raw, T_msg_x, q):
    """Airtime gain of mode x vs raw, eq (9)."""
    return T_msg_raw / (q * T_msg_x)


def gain_TO(C_x, C_raw, G_air):
    """Task-throughput-efficiency gain, eq (10)."""
    if C_raw == 0:
        return float("nan")
    return (C_x / C_raw) * G_air


def account(trace_df, reports, ntn, app, mode_name):
    """Deterministic accounting for one trace and one mode.

    Returns a dict of Stage-1 metrics. ``q`` and gains vs raw are computed by
    the caller via :func:`vs_raw` once the raw baseline is accounted.
    """
    T_RA, K, R = ntn["T_RA_s"], ntn["K_rep"], ntn["rate_bps"]
    n_obs = len(trace_df)
    T_obs_h = float(trace_df["t_h"].iloc[-1] - trace_df["t_h"].iloc[0])
    T_obs_s = T_obs_h * 3600.0

    sizes = (reports["H"] + reports["L_app"]).values
    N = len(reports)
    B_total = float(sizes.sum())                       # eq (1), bytes
    B_app = float(reports["L_app"].sum())
    B_oh = float(reports["H"].sum())
    # airtime: per-report T_msg depends on that report's own size
    T_rep = np.array([t_msg(h, l, T_RA, K, R)
                      for h, l in zip(reports["H"], reports["L_app"])])
    T_total = float(T_rep.sum())
    lam = N / T_obs_s if T_obs_s > 0 else 0.0          # reports/s per device
    # mean payload size (for the per-report gain decomposition)
    L_mean = float(reports["L_app"].mean()) if N else 0.0
    H_mean = float(reports["H"].mean()) if N else 0.0

    return {
        "mode": mode_name, "N_obs": n_obs, "N_adm": N,
        "T_obs_h": T_obs_h, "T_obs_s": T_obs_s,
        "B_total": B_total, "B_app": B_app, "B_oh": B_oh,
        "T_air_total_s": T_total,
        "T_msg_mean_s": float(T_rep.mean()) if N else 0.0,
        "lambda_per_s": lam,
        "reports_per_day": N / (T_obs_h / 24.0) if T_obs_h else 0.0,
        "L_mean": L_mean, "H_mean": H_mean,
        "goodput_bps": B_app * 8.0 / T_obs_s if T_obs_s else 0.0,
        # first-order supported devices per beam, eq (4):
        # Mmax <= rho*T_obs / (lambda_x*T_msg) with lambda_x = reports per
        # observation interval per device (N/T_obs), i.e. rho/(lam*T_msg)
        # with lam = reports/s per device.
        "Mmax_airtime": (ntn["rho"] / (lam * T_rep.mean())
                         if lam > 0 and N else float("inf")),
    }


def vs_raw(acc, acc_raw, ntn):
    """Add q and gain metrics of ``acc`` relative to the raw baseline ``acc_raw``.

    Uses eq (7) for q, eq (8) for G_B (with mean per-report sizes), eq (9) for
    G_air. Returns a new dict with the added keys.
    """
    out = dict(acc)
    q = acc["N_adm"] / acc_raw["N_adm"] if acc_raw["N_adm"] else float("nan")
    out["q"] = q
    out["G_B"] = gain_B(acc_raw["H_mean"], acc_raw["L_mean"],
                        acc["L_mean"], q)
    out["G_B_suppression"] = 1.0 / q                      # 1/q factor, eq (8)
    out["G_B_payload"] = ((acc_raw["H_mean"] + acc_raw["L_mean"])
                          / (acc["H_mean"] + acc["L_mean"]))
    out["G_air"] = gain_air(acc_raw["T_msg_mean_s"], acc["T_msg_mean_s"], q)
    out["S_bytes"] = 1.0 - 1.0 / out["G_B"]               # offered-byte reduction
    out["Mmax_gain"] = out["G_air"]  # eq (9): M_sem/M_raw approx G_air
    return out
