"""Main driver for the NTN 3-stage evaluation.

Runs, for two applications (agri, env) x 5 eval seeds x 4 modes:
  Stage 1: deterministic accounting  -> results/stage1.csv
  Stage 2: NTN access/channel sim    -> results/stage2.csv (+supported)
  Stage 3: task evaluation          -> results/stage3.csv
  Energy  (eq 5)                     -> results/energy.csv
  Sensitivity sweeps                 -> results/sensitivity.csv
  Threshold sweep (fig 3)            -> results/sweep_{agri,env}.csv
  Drift experiment                   -> results/drift.csv
Figures -> figures/fig1..fig6_*.png

Reproduce everything with:  python3 src/ntn_eval/run_all.py
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from ntn_eval import config, traces, schemes, stage1, stage2, stage3, energy, plots

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
RES = os.path.join(BASE, "results")
FIG = os.path.join(BASE, "figures")
MODES = ["raw", "compressed", "event_triggered", "semantic"]
TUNE_SEEDS = [101, 102, 103, 104, 105]
EVAL_SEEDS = [201, 202, 203, 204, 205]
AGRI_OFF_GRID = [-0.03, -0.02, -0.015, -0.01, -0.005, 0.0, 0.005, 0.01,
                 0.02, 0.03]
ENV_OFF_GRID = [-0.6, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4, 0.6]


def run_reports_agri(df, mode, modes_cfg, task_cfg, offset):
    if mode == "raw":
        return schemes.run_raw_agri(df, modes_cfg)
    if mode == "compressed":
        return schemes.run_compressed_agri(df, modes_cfg)
    if mode == "event_triggered":
        return schemes.run_event_agri(df, modes_cfg, task_cfg)
    return schemes.run_semantic_agri(df, modes_cfg, task_cfg, thr_offset=offset)


def run_reports_env(df, mode, modes_cfg, task_cfg, offset, danger):
    if mode == "raw":
        return schemes.run_raw_env(df, modes_cfg)
    if mode == "compressed":
        return schemes.run_compressed_env(df, modes_cfg)
    if mode == "event_triggered":
        return schemes.run_event_env(df, modes_cfg, danger=danger)
    return schemes.run_semantic_env(df, modes_cfg, task_cfg,
                                    thr_offset=offset, danger=danger)


def segment(df, events, d0, d1, extra=None):
    m = (df["t_h"] >= d0 * 24) & (df["t_h"] < d1 * 24)
    seg = df[m].reset_index(drop=True)
    ev = events[(events["onset_h"] >= d0 * 24)
                & (events["onset_h"] < d1 * 24)].reset_index(drop=True)
    if extra is None:
        return seg, ev
    return seg, ev, extra


def main():
    cfgs = config.load_all()
    modes_cfg, ntn, egy = cfgs["modes"]["modes"], cfgs["ntn"]["ntn"], cfgs["energy"]["energy"]
    agri_cfg, env_cfg = cfgs["agri"], cfgs["env"]
    agri_task, env_task = agri_cfg["task"], env_cfg["task"]
    danger = env_cfg["trace"]["danger_level_m"]
    D_agri_h, D_env_h = agri_task["deadline_h"], env_task["deadline_min"] / 60.0
    os.makedirs(RES, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)

    # ------------------------------------------------------- traces + tuning
    print("generating traces ...")
    tune_agri = [traces.gen_agri_trace(s, agri_cfg)[:2] for s in TUNE_SEEDS]
    tune_env = [traces.gen_env_trace(s, env_cfg) for s in TUNE_SEEDS]
    eval_agri = [(s,) + traces.gen_agri_trace(s, agri_cfg)[:2] for s in EVAL_SEEDS]
    eval_env = [(s,) + traces.gen_env_trace(s, env_cfg) for s in EVAL_SEEDS]

    print("tuning semantic thresholds (full season) ...")
    off_agri = stage3.tune_offset_agri(tune_agri, modes_cfg, agri_task, AGRI_OFF_GRID)
    off_env = stage3.tune_offset_env(tune_env, modes_cfg, env_task, danger, ENV_OFF_GRID)
    print("  agri offset:", off_agri)
    print("  env  offset:", off_env)
    # dry-season tuning for the drift experiment
    tune_agri_dry = [segment(df, ev, 0, 20) for df, ev in tune_agri]
    tune_env_dry = [(seg, ev, None)
                    for seg, ev in (segment(df, ev, 0, 20)
                                    for df, ev, _ in tune_env)]
    off_agri_dry = stage3.tune_offset_agri(tune_agri_dry, modes_cfg, agri_task, AGRI_OFF_GRID)
    off_env_dry = stage3.tune_offset_env(tune_env_dry, modes_cfg, env_task, danger, ENV_OFF_GRID)
    print("  agri dry offset:", off_agri_dry)
    print("  env  dry offset:", off_env_dry)
    pd.DataFrame([
        {"app": "agri", "offset_full": off_agri["offset"],
         "offset_dry": off_agri_dry["offset"],
         "p_miss_tuning_full": off_agri["p_miss_tuning"]},
        {"app": "env", "offset_full": off_env["offset"],
         "offset_dry": off_env_dry["offset"],
         "p_miss_tuning_full": off_env["p_miss_tuning"]},
    ]).to_csv(os.path.join(RES, "tuning.csv"), index=False)

    # ------------------------------------------------------- Stage 1
    print("Stage 1: deterministic accounting ...")
    s1_rows, store = [], {}
    for app, evals, tcfg in [("agri", eval_agri, agri_task),
                             ("env", eval_env, env_task)]:
        for seed, df, *rest in evals:
            events = rest[0]
            accs, reps = {}, {}
            for mode in MODES:
                off = off_agri["offset"] if app == "agri" and mode == "semantic" else 0.0
                if app == "agri":
                    reports = run_reports_agri(df, mode, modes_cfg, tcfg, off)
                else:
                    oe = off_env["offset"] if mode == "semantic" else 0.0
                    reports = run_reports_env(df, mode, modes_cfg, tcfg, oe, danger)
                reps[mode] = reports
                accs[mode] = stage1.account(df, reports, ntn, {}, mode)
            for mode in MODES:
                r = dict(accs[mode])
                if mode != "raw":
                    r = stage1.vs_raw(accs[mode], accs["raw"], ntn)
                else:
                    r.update({"q": 1.0, "G_B": 1.0, "G_B_suppression": 1.0,
                              "G_B_payload": 1.0, "G_air": 1.0, "S_bytes": 0.0,
                              "Mmax_gain": 1.0})
                r.update({"app": app, "seed": seed})
                s1_rows.append(r)
            store[(app, seed)] = (df, events, reps)
    s1 = pd.DataFrame(s1_rows)
    s1.to_csv(os.path.join(RES, "stage1.csv"), index=False)

    # ------------------------------------------------------- Stage 2
    print("Stage 2: NTN access/channel ...")
    s1m = s1.groupby(["app", "mode"])[["reports_per_day", "T_msg_mean_s"]].mean()
    delay_dist, s2_rows, sup_rows = {}, [], []
    M_task = ntn["M_task"]
    cluster_frac = env_cfg["trace"]["burst"]["cluster_frac"]
    for app in ["agri", "env"]:
        D_s = (D_agri_h if app == "agri" else D_env_h) * 3600.0
        for mi, mode in enumerate(MODES):
            rpd = s1m.loc[(app, mode), "reports_per_day"]
            tmm = s1m.loc[(app, mode), "T_msg_mean_s"]
            # operating-point delay distribution for Stage 3
            rng = np.random.default_rng(7000 + mi)
            ppd, dur = ntn["passes_per_day"], ntn["pass_duration_s"]
            slot_s = ntn["T_RA_s"] + tmm
            R_pass = M_task * rpd / ppd
            G = stage2._fixed_point_G(R_pass / max(1, int(dur / slot_s)),
                                      ntn["max_attempts"])
            sim = stage2.simulate_reports(rng, ntn["n_mc_reports"], G, ntn,
                                          tmm, D_s)
            delay_dist[(app, mode)] = (sim["delay_s"], sim["mean_attempts"], G)
            # population sweep, normal and burst
            for burst in [False, True]:
                rng2 = np.random.default_rng(8000 + mi * 10 + (1 if burst else 0)
                                             + (100 if app == "env" else 0))
                frac = cluster_frac if (burst and app == "env") else 0.0
                Msup, rows = stage2.supported_devices(
                    rng2, rpd, tmm, ntn, D_s, burst_extra_frac=frac)
                for r in rows:
                    r2 = {k: r[k] for k in
                          ["M", "G0", "G", "p_attempt", "mean_attempts",
                           "mean_delay_s", "deadline_success", "deliver_fail",
                           "R_pass", "n_slots"]}
                    r2.update({"app": app, "mode": mode, "burst": burst})
                    s2_rows.append(r2)
                sup_rows.append({"app": app, "mode": mode, "burst": burst,
                                 "M_supported": Msup})
    s2 = pd.DataFrame(s2_rows)
    s2.to_csv(os.path.join(RES, "stage2.csv"), index=False)
    pd.DataFrame(sup_rows).to_csv(os.path.join(RES, "stage2_supported.csv"),
                                  index=False)

    # deadline-success vs M grid for the task-capacity curve (Fig. 4)
    print("Stage 2b: deadline-success grid ...")
    dsucc_grid = {}
    pop_grid = list(ntn["pop_grid"])
    for app in ["agri", "env"]:
        D_s = (D_agri_h if app == "agri" else D_env_h) * 3600.0
        for mi, mode in enumerate(MODES):
            rpd = s1m.loc[(app, mode), "reports_per_day"]
            tmm = s1m.loc[(app, mode), "T_msg_mean_s"]
            for gi, M in enumerate(pop_grid):
                rng = np.random.default_rng(8100 + mi * 100 + gi
                                            + (1000 if app == "env" else 0))
                ppd, dur = ntn["passes_per_day"], ntn["pass_duration_s"]
                slot_s = ntn["T_RA_s"] + tmm
                R_pass = M * rpd / ppd
                G = stage2._fixed_point_G(R_pass / max(1, int(dur / slot_s)),
                                          ntn["max_attempts"])
                sim = stage2.simulate_reports(rng, 2000, G, ntn, tmm, D_s)
                dsucc_grid[(app, mode, M)] = sim["deadline_success"]

    # ------------------------------------------------------- Stage 3
    print("Stage 3: task evaluation ...")
    s3_rows = []
    for app in ["agri", "env"]:
        D_h = D_agri_h if app == "agri" else D_env_h
        early = 2.0 if app == "agri" else 0.25
        tcfg3 = agri_task if app == "agri" else env_task
        persist = tcfg3["persist_confirm"]
        hyst = tcfg3.get("hysteresis", 0.0)
        smooth = tcfg3.get("smooth", 1)
        for seed, df, *rest in (eval_agri if app == "agri" else eval_env):
            events = rest[0]
            _, _, reps = store[(app, seed)]
            T_obs_h = float(df["t_h"].iloc[-1])
            for mi, mode in enumerate(MODES):
                reports = reps[mode]
                ddist, _, _ = delay_dist[(app, mode)]
                rng = np.random.default_rng(9000 + seed + mi)
                dly = rng.choice(ddist, size=len(reports), replace=True) / 3600.0
                if app == "agri":
                    off = off_agri["offset"]
                    st, en, dl = stage3.task_outputs_agri(
                        df, reports, dly, mode, off, persist, hyst, smooth)
                else:
                    off = off_env["offset"]
                    st, en, dl = stage3.task_outputs_env(
                        df, reports, dly, mode, off, persist, danger, hyst,
                        smooth)
                s = stage3.score_episodes(st, en, dl, events, D_h, early,
                                          T_obs_h)
                si = stage3.score_episodes(st, en, np.zeros_like(dl), events,
                                           D_h, early, T_obs_h)
                g_air = s1[(s1.app == app) & (s1.seed == seed)
                           & (s1["mode"] == mode)]["G_air"].values[0]
                row = {"app": app, "seed": seed, "mode": mode,
                       "n_events": s["n_events"], "n_hit": s["n_hit"],
                       "C_raw0": si["recall"], "G_air": g_air,
                       "p_miss": s["p_miss"], "recall": s["recall"],
                       "fa_per_week": s["fa_per_week"],
                       "mean_det_delay_h": s["mean_det_delay_h"],
                       "mean_timing_err_h": s["mean_timing_err_h"],
                       "p_miss_ideal": si["p_miss"], "recall_ideal": si["recall"],
                       "G_air": g_air}
                s3_rows.append(row)
    s3 = pd.DataFrame(s3_rows)
    # G_TO needs C_raw per (app, seed)
    # task-throughput gain eq (10): G_TO = (recall_x / recall_raw) * G_air
    for (app, seed), g in s3.groupby(["app", "seed"]):
        c_raw = g[g["mode"] == "raw"]["recall"].values[0]
        for i in g.index:
            s3.loc[i, "G_TO"] = stage1.gain_TO(s3.loc[i, "recall"], c_raw,
                                              s3.loc[i, "G_air"])
    s3.to_csv(os.path.join(RES, "stage3.csv"), index=False)

    # task-capacity curve: C(M) = ideal recall x deadline_success(M)
    cap_rows = []
    for app in ["agri", "env"]:
        for mode in MODES:
            c0 = s3[(s3.app == app) & (s3["mode"] == mode)]["C_raw0"].mean()
            for M in pop_grid:
                ds = dsucc_grid[(app, mode, M)]
                cap_rows.append({"app": app, "mode": mode, "M": M,
                                 "C": float(c0 * ds),
                                 "deadline_success": ds})
    pd.DataFrame(cap_rows).to_csv(os.path.join(RES, "capacity.csv"),
                                  index=False)

    # ------------------------------------------------------- Energy
    print("energy ...")
    e_rows, sens_rows = [], []
    for app in ["agri", "env"]:
        for seed, df, *rest in (eval_agri if app == "agri" else eval_env):
            _, _, reps = store[(app, seed)]
            n_obs = len(df)
            T_obs_s = float(df["t_h"].iloc[-1]) * 3600.0
            tots = {}
            for mode in MODES:
                ai = modes_cfg[mode].get("ai_energy_mJ", 0.0)
                _, mean_att, _ = delay_dist[(app, mode)]
                br = energy.device_energy(n_obs, reps[mode], ai, egy, ntn,
                                          mean_attempts=mean_att)
                tot = energy.total_energy(br, T_obs_s, egy)
                tots[mode] = tot
            for mode in MODES:
                r = dict(tots[mode])
                r.update({"app": app, "seed": seed, "mode": mode,
                          "S_E": energy.net_saving(tots[mode]["E_total_J"],
                                                   tots["raw"]["E_total_J"])})
                e_rows.append(r)
    egy_df = pd.DataFrame(e_rows)
    egy_df.to_csv(os.path.join(RES, "energy.csv"), index=False)
    # break-even sensitivity on seed-averaged inputs
    for app in ["agri", "env"]:
        g = egy_df[egy_df.app == app].groupby("mode").mean(numeric_only=True)
        E_raw = g.loc["raw", "E_total_J"]
        base = g.loc["semantic"]
        E_noAI = (base["E_total_J"] - base["E_AI_J"])
        n_obs = base["n_obs"]
        for ai in egy["ai_sweep_mJ"]:
            E_sem = E_noAI + n_obs * ai / 1000.0
            sens_rows.append({"app": app, "ai_mJ": ai,
                              "S_E": energy.net_saving(E_sem, E_raw)})
    pd.DataFrame(sens_rows).to_csv(os.path.join(RES, "energy_sensitivity.csv"),
                                   index=False)

    # ------------------------------------------------------- sensitivity H, K
    print("sensitivity sweeps ...")
    sens2 = []
    seed0 = EVAL_SEEDS[0]
    for app in ["agri", "env"]:
        df, events, reps = store[(app, seed0)]
        for H in [20, 60, 120]:
            for K in [1, 2, 4]:
                ntn_v = dict(ntn, K_rep=K)
                reps_raw = reps["raw"].copy()
                reps_sem = reps["semantic"].copy()
                reps_raw["H"] = H
                reps_sem["H"] = H
                a_raw = stage1.account(df, reps_raw, ntn_v, {}, "raw")
                a_sem = stage1.account(df, reps_sem, ntn_v, {}, "semantic")
                v = stage1.vs_raw(a_sem, a_raw, ntn_v)
                sens2.append({"app": app, "H": H, "K": K, "q": v["q"],
                              "G_B": v["G_B"], "G_air": v["G_air"]})
    pd.DataFrame(sens2).to_csv(os.path.join(RES, "sensitivity.csv"), index=False)

    # ------------------------------------------------------- threshold sweep (fig 3)
    for app, grid, offkey in [("agri", AGRI_OFF_GRID, None), ("env", ENV_OFF_GRID, None)]:
        rows = []
        for off in grid:
            recs, kbs = [], []
            for seed, df, *rest in (eval_agri if app == "agri" else eval_env):
                events = rest[0]
                if app == "agri":
                    reps = schemes.run_semantic_agri(df, modes_cfg, agri_task,
                                                     thr_offset=off)
                    ddist, _, _ = delay_dist[(app, "semantic")]
                    rng = np.random.default_rng(9500 + seed)
                    dly = rng.choice(ddist, size=len(reps), replace=True) / 3600.0
                    st, en, dl = stage3.task_outputs_agri(
                        df, reps, dly, "semantic", off,
                        agri_task["persist_confirm"],
                        agri_task.get("hysteresis", 0.0),
                        agri_task.get("smooth", 1))
                    s = stage3.score_episodes(st, en, dl, events,
                                              D_agri_h, 2.0,
                                              float(df["t_h"].iloc[-1]))
                else:
                    reps = schemes.run_semantic_env(df, modes_cfg, env_task,
                                                    thr_offset=off, danger=danger)
                    ddist, _, _ = delay_dist[(app, "semantic")]
                    rng = np.random.default_rng(9500 + seed)
                    dly = rng.choice(ddist, size=len(reps), replace=True) / 3600.0
                    st, en, dl = stage3.task_outputs_env(
                        df, reps, dly, "semantic", off,
                        env_task["persist_confirm"], danger,
                        env_task.get("hysteresis", 0.0),
                        env_task.get("smooth", 1))
                    s = stage3.score_episodes(st, en, dl, events, D_env_h,
                                              0.25, float(df["t_h"].iloc[-1]))
                recs.append(s["recall"])
                kbs.append((reps["H"] + reps["L_app"]).sum() / 90.0 / 1000.0)
            rows.append({"offset": off, "recall": float(np.nanmean(recs)),
                         "kB_per_day": float(np.mean(kbs))})
        pd.DataFrame(rows).to_csv(os.path.join(RES, f"sweep_{app}.csv"), index=False)

    # ------------------------------------------------------- drift experiment
    print("drift experiment ...")
    d_rows = []
    for app in ["agri", "env"]:
        tcfg = agri_task if app == "agri" else env_task
        persist = tcfg["persist_confirm"]
        hyst = tcfg.get("hysteresis", 0.0)
        smooth = tcfg.get("smooth", 1)
        D_h = D_agri_h if app == "agri" else D_env_h
        early = 2.0 if app == "agri" else 0.25
        off_dry = off_agri_dry["offset"] if app == "agri" else off_env_dry["offset"]
        off_full = off_agri["offset"] if app == "agri" else off_env["offset"]
        obs_col = "sm_obs" if app == "agri" else "level_obs"
        mu, sigma = stage3.drift_detector_baseline(
            [segment(df, ev, 0, 20) for df, ev, *_ in
             (tune_agri if app == "agri" else tune_env)], obs_col)
        for seed, df, *rest in (eval_agri if app == "agri" else eval_env):
            events = rest[0]
            # drift evaluation segment: agri events occur in the dry phase
            # (days 0-35); env floods in monsoon (days 35-70)
            d0, d1 = (0, 35) if app == "agri" else (35, 70)
            seg_df, seg_ev = segment(df, events, d0, d1)
            T_seg = float(seg_df["t_h"].iloc[-1] - seg_df["t_h"].iloc[0])
            for variant, off in [("dry-tuned", off_dry), ("full-tuned", off_full)]:
                if app == "agri":
                    reps = schemes.run_semantic_agri(seg_df, modes_cfg, tcfg,
                                                     thr_offset=off)
                    st, en, dl = stage3.task_outputs_agri(
                        seg_df, reps, np.zeros(len(reps)), "semantic", off,
                        persist, hyst, smooth)
                else:
                    reps = schemes.run_semantic_env(seg_df, modes_cfg, tcfg,
                                                    thr_offset=off, danger=danger)
                    st, en, dl = stage3.task_outputs_env(
                        seg_df, reps, np.zeros(len(reps)), "semantic", off,
                        persist, danger, hyst, smooth)
                s = stage3.score_episodes(st, en, dl, seg_ev, D_h, early, T_seg)
                kb = (reps["H"] + reps["L_app"]).sum() / 35.0 / 1000.0
                d_rows.append({"app": app, "seed": seed, "variant": variant,
                               "p_miss": s["p_miss"], "recall": s["recall"],
                               "fa_per_week": s["fa_per_week"], "kB_per_day": kb})
            # adaptation variant: threshold update after drift detection
            wins = (stage3.fallback_windows_agri(seg_df, mu, sigma)
                    if app == "agri" else stage3.fallback_windows_env(seg_df, mu, sigma))
            st, en, dl, kb = _threshold_update_score(
                app, seg_df, seg_ev, modes_cfg, tcfg, off_dry, off_full,
                persist, D_h, early, wins, danger)
            s = stage3.score_episodes(st, en, dl, seg_ev, D_h, early, T_seg)
            d_rows.append({"app": app, "seed": seed, "variant": "dry-tuned+update",
                           "p_miss": s["p_miss"], "recall": s["recall"],
                           "fa_per_week": s["fa_per_week"], "kB_per_day": kb,
                           "n_fallback_windows": len(wins)})
    pd.DataFrame(d_rows).to_csv(os.path.join(RES, "drift.csv"), index=False)

    # ------------------------------------------------------- figures
    print("figures ...")
    R = RES
    s1a = s1[s1.app == "agri"]; s1e = s1[s1.app == "env"]
    s1a.to_csv(f"{R}/stage1_agri.csv", index=False)
    s1e.to_csv(f"{R}/stage1_env.csv", index=False)
    plots.fig1_decomposition(f"{R}/stage1_agri.csv", f"{R}/stage1_env.csv",
                             f"{FIG}/fig1_suppression_decomposition.png")
    plots.fig2_airtime_vs_pop(f"{R}/stage1_agri.csv", f"{R}/stage1_env.csv",
                              ntn["rho"], f"{FIG}/fig2_airtime_vs_load.png")
    s3e = s3[s3.app == "env"]
    s3e.to_csv(f"{R}/stage3_env.csv", index=False)
    s3a = s3[s3.app == "agri"]
    s3a.to_csv(f"{R}/stage3_agri.csv", index=False)
    plots.fig3_quality_vs_resource(f"{R}/sweep_agri.csv", f"{R}/stage1_agri.csv",
                                   f"{R}/stage3_agri.csv", f"{FIG}/fig3a_quality_vs_resource_agri.png",
                                   "Agriculture")
    plots.fig3_quality_vs_resource(f"{R}/sweep_env.csv", f"{R}/stage1_env.csv",
                                   f"{R}/stage3_env.csv", f"{FIG}/fig3b_quality_vs_resource_env.png",
                                   "Environment")
    s2a = s2[s2.app == "agri"]; s2e = s2[s2.app == "env"]
    s2a.to_csv(f"{R}/stage2_agri.csv", index=False)
    s2e.to_csv(f"{R}/stage2_env.csv", index=False)
    capa = pd.read_csv(f"{R}/capacity.csv")
    capa_a = capa[capa.app == "agri"]; capa_e = capa[capa.app == "env"]
    capa_a.to_csv(f"{R}/capacity_agri.csv", index=False)
    capa_e.to_csv(f"{R}/capacity_env.csv", index=False)
    sup = pd.read_csv(f"{R}/stage2_supported.csv")
    sup_a = sup[sup.app == "agri"]; sup_e = sup[sup.app == "env"]
    sup_a.to_csv(f"{R}/stage2_supported_agri.csv", index=False)
    sup_e.to_csv(f"{R}/stage2_supported_env.csv", index=False)
    plots.fig4_capacity(f"{R}/capacity_agri.csv", f"{R}/stage2_supported_agri.csv",
                        f"{FIG}/fig4a_task_capacity_agri.png", "Agriculture")
    plots.fig4_capacity(f"{R}/capacity_env.csv", f"{R}/stage2_supported_env.csv",
                        f"{FIG}/fig4b_task_capacity_env.png", "Environment")
    plots.fig5_energy(f"{R}/energy.csv", f"{R}/energy_sensitivity.csv",
                      f"{FIG}/fig5_energy.png")
    plots.fig6_burst(f"{R}/stage2.csv", f"{FIG}/fig6_burst.png")
    print("done.")


def _threshold_update_score(app, seg_df, seg_events, modes_cfg, task,
                            off_dry, off_full, persist, D_h, early,
                            windows, danger):
    """Drift adaptation by threshold update: the device runs its stale
    dry-tuned threshold until the network detects the baseline shift; from
    the first detection on it uses the up-to-date full-season threshold
    (pushed by downlink).  Ideal delivery.

    Returns (ep_starts, ep_ends, ep_delays, kB_per_day).
    """
    t = seg_df["t_h"].values
    hyst = task.get("hysteresis", 0.0)
    smooth = task.get("smooth", 1)
    t_upd = min([w[0] for w in windows]) if windows else np.inf

    if app == "agri":
        obs = seg_df["sm_obs"].values
        base_thr = seg_df["sm_thr"].values
        rule = stage3.rule_below
    else:
        obs = seg_df["level_obs"].values
        base_thr = np.full(len(seg_df), danger)
        rule = stage3.rule_above
    thr = base_thr + np.where(t < t_upd, off_dry, off_full)
    starts, ends = [], []
    for (a, b) in rule(t, obs, thr, persist, hyst, smooth):
        starts.append(t[a])
        ends.append(t[b])
    st = np.array(starts)
    en = np.array(ends)
    dl = np.zeros(len(st))
    # kB: semantic reports (dry- then full-tuned firing rates) + 1 downlink
    sem = (schemes.run_semantic_agri(seg_df, modes_cfg, task,
                                     thr_offset=off_dry)
           if app == "agri" else
           schemes.run_semantic_env(seg_df, modes_cfg, task,
                                    thr_offset=off_dry, danger=danger))
    kb = (sem["H"] + sem["L_app"]).sum() / 35.0 / 1000.0
    return st, en, dl, kb


if __name__ == "__main__":
    main()
