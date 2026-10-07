"""Unit tests for Stage-1 deterministic accounting (paper Sec. VII.A)."""
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ntn_eval import stage1


def test_gb_illustrative_eq11():
    # Paper eq (11): L_raw=200, L_sem=20, H=60, q=0.1 -> G_B = 32.5
    gb = stage1.gain_B(60, 200, 20, 0.1)
    assert abs(gb - 32.5) < 1e-9, gb


def test_gb_decomposition():
    # G_B = (1/q) * (H+L_raw)/(H+L_sem)
    gb = stage1.gain_B(60, 200, 20, 0.1)
    assert abs(gb - (10.0 * 260.0 / 80.0)) < 1e-9


def test_q_one_no_suppression():
    # q = 1: gain is purely the per-report payload ratio
    gb = stage1.gain_B(60, 200, 20, 1.0)
    assert abs(gb - 260.0 / 80.0) < 1e-9


def test_zero_overhead():
    # H = 0: gain reduces to (L_raw/L_sem)/q
    gb = stage1.gain_B(0, 200, 20, 0.1)
    assert abs(gb - (200.0 / 20.0) / 0.1) < 1e-9


def test_no_compression_equivalence():
    # L_x == L_raw and q == 1 -> no gain at all
    gb = stage1.gain_B(60, 200, 200, 1.0)
    assert abs(gb - 1.0) < 1e-9


def test_t_msg_eq2():
    # eq (2): T_msg = T_RA + K*8(H+L)/R
    t = stage1.t_msg(60, 200, 2.0, 1, 16000)
    assert abs(t - (2.0 + 8 * 260 / 16000)) < 1e-12


def test_airtime_gain_smaller_than_byte_gain():
    # With nonzero T_RA, eq (9) gain must be smaller than eq (8) gain
    T_RA, R, K, H = 2.0, 16000, 1, 60
    t_raw = stage1.t_msg(H, 200, T_RA, K, R)
    t_sem = stage1.t_msg(H, 20, T_RA, K, R)
    q = 0.1
    g_air = stage1.gain_air(t_raw, t_sem, q)
    g_b = stage1.gain_B(H, 200, 20, q)
    assert g_air < g_b, (g_air, g_b)
    assert g_air > 1.0


def test_gain_TO_eq10():
    # G_TO = (C_sem/C_raw) * G_air ; degraded task quality reduces the gain
    assert abs(stage1.gain_TO(100, 100, 8.0) - 8.0) < 1e-12
    assert stage1.gain_TO(90, 100, 8.0) < 8.0
    assert math.isnan(stage1.gain_TO(10, 0, 8.0))


def test_accounting_counts():
    import pandas as pd
    import numpy as np
    trace = pd.DataFrame({"t_h": np.arange(0, 24, 0.25)})  # 96 samples, 24 h
    reps = pd.DataFrame({"t_gen_h": np.arange(0, 24, 1.0),
                         "L_app": 200, "H": 60,
                         "kind": "periodic", "conf": np.nan})
    ntn = {"T_RA_s": 2.0, "K_rep": 1, "rate_bps": 16000, "rho": 1.0}
    acc = stage1.account(trace, reps, ntn, {}, "raw")
    assert acc["N_obs"] == 96
    assert acc["N_adm"] == 24
    assert acc["B_total"] == 24 * 260
    assert abs(acc["T_msg_mean_s"] - (2.0 + 8 * 260 / 16000)) < 1e-9
