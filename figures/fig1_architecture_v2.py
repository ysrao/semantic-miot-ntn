"""Redesigned architecture figure for the SPACOMM 2027 resubmission.

Deliberately different from the original Fig. 1 (which used six vertical pastel
columns): this version is a horizontal five-stage pipeline in a flat
navy/teal/amber palette, narrowed to the two evaluated applications
(agriculture + environmental monitoring) and annotated with the
measurement points of the new evaluation.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Arc
import matplotlib.patheffects as pe

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

# ---------------------------------------------------------------- palette
PALETTE = [
    ("#2E7D32", "#E8F5E9"),   # 1 sensing      - green
    ("#E65100", "#FFF3E0"),   # 2 semantic     - amber/orange
    ("#0D47A1", "#E3F2FD"),   # 3 NTN uplink   - blue
    ("#4527A0", "#EDE7F6"),   # 4 edge engine  - purple
    ("#00695C", "#E0F2F1"),   # 5 action       - teal
]

BLOCKS = [
    dict(x=0.25, title="1  FIELD SENSING",
         items=["Soil moisture probes", "Rain gauges", "Water-level sensors",
                "Temperature / humidity", "Pump & reservoir status"],
         note="5-15 min sampling"),
    dict(x=2.65, title="2  SEMANTIC AGENT",
         items=["Feature extraction", "Value & urgency scoring",
                "Admission control (q)", "Confidence estimate"],
         note="on device or village gateway"),
    dict(x=5.05, title="3  NTN UPLINK",
         items=[], note="LEO link  \u2022  contact windows",
         satellite=True),
    dict(x=7.45, title="4  EDGE TASK ENGINE",
         items=["Semantic decoder", "Irrigation decision", "Flood warning level",
                "Confidence calibration"],
         note="task inference, not bit recovery"),
    dict(x=9.85, title="5  ACTION & LEARNING",
         items=["Application action", "Task-accuracy feedback",
                "Threshold / model update", "Audit & rollback"],
         note="validated updates only"),
]
BW, BY, BH = 2.05, 2.1, 3.7

for i, b in enumerate(BLOCKS):
    dark, light = PALETTE[i]
    x = b["x"]
    box = FancyBboxPatch((x, BY), BW, BH, boxstyle="round,pad=0.02,rounding_size=0.12",
                         facecolor=light, edgecolor=dark, linewidth=1.6)
    ax.add_patch(box)
    # title bar
    bar = FancyBboxPatch((x, BY + BH - 0.55), BW, 0.55,
                         boxstyle="round,pad=0.02,rounding_size=0.12",
                         facecolor=dark, edgecolor=dark, linewidth=1.6)
    ax.add_patch(bar)
    ax.add_patch(Rectangle((x, BY + BH - 0.55), BW, 0.30, facecolor=dark,
                           edgecolor="none", zorder=2))
    ax.text(x + BW / 2, BY + BH - 0.27, b["title"], ha="center", va="center",
            fontsize=10, weight="bold", color="white", zorder=3)
    if b.get("satellite"):
        # --- stylised satellite, distinct from original iconography ---
        cx = x + BW / 2
        # solar panels
        ax.add_patch(Rectangle((cx - 0.85, 4.62), 0.55, 0.28, facecolor="#90CAF9",
                               edgecolor="#0D47A1", linewidth=1.2))
        ax.add_patch(Rectangle((cx + 0.30, 4.62), 0.55, 0.28, facecolor="#90CAF9",
                               edgecolor="#0D47A1", linewidth=1.2))
        for px in (cx - 0.575, cx + 0.575):
            ax.plot([px, px], [4.62, 4.90], color="#0D47A1", lw=1.0)
        # body
        ax.add_patch(FancyBboxPatch((cx - 0.30, 4.55), 0.60, 0.42,
                                    boxstyle="round,pad=0.01,rounding_size=0.06",
                                    facecolor="#0D47A1", edgecolor="#0D47A1"))
        # dish
        ax.add_patch(Arc((cx, 4.55), 0.34, 0.22, theta1=180, theta2=360,
                         color="white", lw=1.4))
        # signal arcs down to gateway
        for r in (0.25, 0.45, 0.65):
            ax.add_patch(Arc((cx, 4.30), 2 * r, 2 * r * 0.55, theta1=200,
                             theta2=340, color="#0D47A1", lw=1.1, ls=(0, (3, 2))))
        # ground gateway dish
        gx = cx
        ax.plot([gx - 0.28, gx + 0.28], [2.62, 2.62], color="#0D47A1", lw=2.2)
        ax.plot([gx, gx], [2.62, 2.95], color="#0D47A1", lw=1.6)
        ax.add_patch(Arc((gx, 3.02), 0.5, 0.3, theta1=200, theta2=340,
                         color="#0D47A1", lw=2.0))
        ax.text(cx, 2.52, "random access \u2022 repetitions\nstore-and-forward",
                ha="center", va="top", fontsize=8, color="#0D47A1", style="italic")
    else:
        yy = BY + BH - 0.85
        for it in b["items"]:
            ax.text(x + 0.14, yy, "\u2022  " + it, ha="left", va="top",
                    fontsize=8.6, color="#212121")
            yy -= 0.30
        ax.text(x + 0.14, BY + 0.28, b["note"], ha="left", va="bottom",
                fontsize=7.8, color="#616161", style="italic", wrap=True)

# ------------------------------------------------- pipeline arrows
for i in range(4):
    x0 = BLOCKS[i]["x"] + BW
    x1 = BLOCKS[i + 1]["x"]
    ax.add_patch(FancyArrowPatch((x0 + 0.02, BY + BH / 2 + 0.35),
                                 (x1 - 0.02, BY + BH / 2 + 0.35),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color="#37474F", linewidth=1.8,
                                 shrinkA=0, shrinkB=0))

# ------------------------------------------------- raw fallback path (under boxes)
ax.plot([BLOCKS[0]["x"] + 0.35, BLOCKS[4]["x"] + BW - 0.35], [1.72, 1.72],
        color="#9E9E9E", lw=1.4, ls=(0, (2, 2)))
ax.text(6.0, 1.52, "optional raw fallback: audit samples, drift, billing",
        ha="center", va="top", fontsize=8, color="#757575", style="italic")

# ------------------------------------------------- feedback loop (below fallback line)
fb = FancyArrowPatch((BLOCKS[4]["x"] + BW / 2, 1.30),
                     (BLOCKS[1]["x"] + BW / 2, 1.30),
                     arrowstyle="-|>", mutation_scale=14, color="#00695C",
                     linewidth=1.6, ls=(0, (5, 3)),
                     connectionstyle="arc3,rad=-0.14")
ax.add_patch(fb)
ax.text(6.3, 0.52, "task-accuracy feedback  \u2192  validated threshold / model update",
        ha="center", va="center", fontsize=8.6, color="#00695C",
        bbox=dict(facecolor="white", edgecolor="#00695C", boxstyle="round,pad=0.25"))

# ------------------------------------------------- measurement banner
ax.text(6.0, 6.55, "Every stage is measured: admitted reports, airtime, task outcomes, energy",
        ha="center", va="center", fontsize=10.5, weight="bold", color="#263238",
        bbox=dict(facecolor="#FFFDE7", edgecolor="#F9A825",
                  boxstyle="round,pad=0.35"))
ax.text(6.0, 6.18, "From illustrative to measured \u2014 trace-driven evaluation of two applications",
        ha="center", va="center", fontsize=9, color="#616161", style="italic")

# ------------------------------------------------- legend
ax.text(0.25, 0.18, "Figure 1.", ha="left", va="center", fontsize=9,
        weight="bold", color="#212121")
ax.text(1.05, 0.18, "Application-specific semantic / task-oriented mIoT over NTN: "
        "field sensing, on-device semantic agent, LEO uplink, edge task engine, "
        "and guarded learning loop.", ha="left", va="center", fontsize=8.4,
        color="#424242")

plt.tight_layout(pad=0.6)
plt.savefig("/home/hatch/workspace/ntn-eval/figures/fig1_architecture_v2.png",
            dpi=300, bbox_inches="tight")
plt.savefig("/home/hatch/workspace/ntn-eval/figures/fig1_architecture_v2.pdf",
            bbox_inches="tight")
print("saved fig1_architecture_v2.png / .pdf")
