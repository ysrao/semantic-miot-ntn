"""Publication-quality figures for the NTN evaluation.

Six figures (paper Sec. VII, results):
  1. report-suppression and payload decomposition  (eq 8)
  2. beam airtime per day vs device population     (eq 4 bound)
  3. task-quality vs resource curves               (threshold sweep)
  4. deadline-success vs population -> supported devices per beam
  5. energy breakdown + AI break-even sensitivity  (eq 5)
  6. correlated-burst episode behaviour

Each function reads the results CSVs and writes a PNG into figures/.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150,
    "font.size": 9, "axes.grid": True, "grid.alpha": 0.3,
    "axes.titlesize": 10,
})
MODES = ["raw", "compressed", "event_triggered", "semantic"]
MODE_LABEL = {"raw": "Raw periodic", "compressed": "Compressed 2:1",
              "event_triggered": "Event-triggered", "semantic": "Semantic"}
COLORS = {"raw": "#1f77b4", "compressed": "#ff7f0e",
          "event_triggered": "#2ca02c", "semantic": "#d62728"}


def fig1_decomposition(s1_agri, s1_env, out):
    """G_B decomposition: report-suppression factor x per-report payload factor."""
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for a, (path, title) in enumerate([(s1_agri, "Agriculture"),
                                       (s1_env, "Environment")]):
        df = pd.read_csv(path)
        m = df[df["mode"] != "raw"].groupby("mode")[
            ["G_B_suppression", "G_B_payload", "G_B"]].mean()
        x = np.arange(len(m))
        ax[a].bar(x, m["G_B_suppression"], label="Report suppression (1/q)",
                  color="#4e79a7")
        ax[a].bar(x, m["G_B_payload"], bottom=m["G_B_suppression"],
                  label="Per-report payload", color="#f28e2b")
        for i, (_, r) in enumerate(m.iterrows()):
            ax[a].text(i, r["G_B"] * 1.04, f'{r["G_B"]:.1f}x',
                       ha="center", fontsize=8)
        ax[a].set_xticks(x)
        ax[a].set_xticklabels([MODE_LABEL[i] for i in m.index], rotation=15,
                              ha="right")
        ax[a].set_yscale("log")
        ax[a].set_ylabel("Offered-byte gain $G_B$ (log scale)")
        ax[a].set_title(title)
    ax[1].legend(fontsize=8)
    fig.suptitle("Gain decomposition: $G_B = (1/q)\\times(H+L_{raw})/(H+L_x)$  [eq 8]")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def fig2_airtime_vs_pop(s1_agri, s1_env, rho, out):
    """Beam airtime per day vs population; horizontal line = usable airtime."""
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    M = np.logspace(np.log10(50), np.log10(6400), 60)
    cap = rho * 86400
    for a, (path, title) in enumerate([(s1_agri, "Agriculture"),
                                       (s1_env, "Environment")]):
        df = pd.read_csv(path)
        per_dev = df.groupby("mode")["T_air_total_s"].mean() / 90.0  # s/day
        for md in MODES:
            ax[a].plot(M, M * per_dev[md], label=MODE_LABEL[md],
                       color=COLORS[md])
        ax[a].axhline(cap, color="k", ls="--", lw=1,
                      label=f"Usable airtime ($\\rho T_{{obs}}$)")
        ax[a].set_xscale("log")
        ax[a].set_yscale("log")
        ax[a].set_xlabel("Devices per beam")
        ax[a].set_ylabel("Beam airtime per day (s)")
        ax[a].set_title(title)
    ax[1].legend(fontsize=7)
    fig.suptitle("Occupied beam airtime vs population (Stage-1 accounting)")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def fig3_quality_vs_resource(sweep_csv, s1_csv, s3_csv, out, app_title):
    """Task quality (recall) vs resource (kB/device/day) across thresholds."""
    sw = pd.read_csv(sweep_csv)
    s1 = pd.read_csv(s1_csv).groupby("mode")[["B_total"]].mean() / 90.0 / 1000.0
    s3 = pd.read_csv(s3_csv)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(sw["kB_per_day"], sw["recall"], "o-", color=COLORS["semantic"],
            label="Semantic (threshold sweep)")
    for md in ["raw", "compressed", "event_triggered"]:
        q = s3[s3["mode"] == md]["recall"].mean()
        ax.plot(s1.loc[md, "B_total"], q, "s", color=COLORS[md], ms=8,
                label=f"{MODE_LABEL[md]}")
    ax.set_xlabel("Offered traffic (kB/device/day)")
    ax.set_ylabel("Event recall")
    ax.set_title(f"{app_title}: task quality vs resource")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def fig4_capacity(cap_csv, sup_csv, out, app_title):
    """Task capacity C(M) = ideal recall x Pr(delay <= D | M) per mode.

    Vertical lines mark the Stage-2 supported population per mode.
    """
    df = pd.read_csv(cap_csv)
    sup = pd.read_csv(sup_csv)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for md in MODES:
        d = df[df["mode"] == md].sort_values("M")
        ax.plot(d["M"], d["C"], "o-", color=COLORS[md], label=MODE_LABEL[md])
        ms = sup[(sup["mode"] == md) & (~sup["burst"])]["M_supported"]
        if len(ms):
            ax.axvline(ms.values[0], color=COLORS[md], ls=":", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel("Devices per beam")
    ax.set_ylabel("Task capacity C(M): event recall at load M")
    ax.set_title(f"{app_title}: task capacity vs population")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def fig5_energy(energy_csv, sens_csv, out):
    """(a) energy breakdown per mode; (b) net saving vs AI energy."""
    e = pd.read_csv(energy_csv)
    s = pd.read_csv(sens_csv)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    apps = e["app"].unique()
    ecols = ["E_sense_J", "E_AI_J", "E_access_J", "E_tx_J", "E_retx_J",
             "E_idle_J"]
    elabels = ["Sense", "AI", "Access", "TX", "ReTX", "Idle"]
    for a, app in enumerate(apps):
        d = e[e["app"] == app].groupby("mode")[ecols].mean()
        bottom = np.zeros(len(d))
        for c, lab in zip(ecols, elabels):
            ax[0].bar([f"{app}\n{MODE_LABEL[m]}" for m in d.index], d[c],
                      bottom=bottom, label=lab if a == 0 else None)
            bottom += d[c].values
    ax[0].set_ylabel("Energy per device / 90 days (J)")
    ax[0].set_title("(a) Eq (5) breakdown")
    ax[0].tick_params(axis="x", labelsize=7)
    ax[0].legend(fontsize=7, ncol=3)
    for app in s["app"].unique():
        d = s[s["app"] == app]
        ax[1].plot(d["ai_mJ"], d["S_E"], "o-", label=app)
    ax[1].axhline(0, color="k", lw=1)
    ax[1].set_xscale("log")
    ax[1].set_xlabel("AI energy per inference (mJ)")
    ax[1].set_ylabel("Net saving $S_E = 1 - E_{sem}/E_{raw}$")
    ax[1].set_title("(b) Break-even sensitivity")
    ax[1].legend(fontsize=8)
    fig.suptitle("Device energy [eq 5] — modeled NB-IoT-class values")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def fig6_burst(s2_csv, out):
    """Correlated-burst stress: deadline success, normal vs burst episode."""
    df = pd.read_csv(s2_csv)
    apps = df["app"].unique()
    fig, ax = plt.subplots(1, len(apps), figsize=(5 * len(apps), 3.8),
                           squeeze=False)
    for a, app in enumerate(apps):
        d = df[df["app"] == app]
        M_pick = 800
        sub = d[d["M"] == M_pick]
        x = np.arange(len(MODES))
        norm = [sub[(sub["mode"] == md) & (~sub["burst"])]["deadline_success"].mean()
                for md in MODES]
        burst = [sub[(sub["mode"] == md) & (sub["burst"])]["deadline_success"].mean()
                 for md in MODES]
        w = 0.35
        ax[0][a].bar(x - w / 2, norm, w, label="Normal load", color="#4e79a7")
        ax[0][a].bar(x + w / 2, burst, w, label="Burst episode", color="#e15759")
        ax[0][a].set_xticks(x)
        ax[0][a].set_xticklabels([MODE_LABEL[m] for m in MODES], rotation=15,
                                 ha="right", fontsize=8)
        ax[0][a].set_ylabel("Pr(delay <= D)")
        ax[0][a].set_title(f"{app}, M={M_pick}/beam")
        ax[0][a].legend(fontsize=8)
    fig.suptitle("Geographically correlated burst: deadline success")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
