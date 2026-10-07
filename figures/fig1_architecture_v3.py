"""Figure 1 v3 for the SPACOMM 2027 resubmission.

Redrawn per author feedback:
- Every box sits inside an explicit LOCATION zone: CLIENT-TRANSMIT (field/village),
  SPACE SEGMENT (LEO), GATEWAY / CLIENT-TARGET (ground).
- Uplink and downlink are drawn as physical arrows between ground and satellite,
  each labeled with what it carries.
- The satellite artwork is taken from the author's earlier (IEEE) paper Fig. 1;
  its near-white background is keyed out (border-connected flood fill) and the
  cropped top edge trimmed, so no image rectangle shows on the dashed orbit path.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Rectangle,
                                Arc, Ellipse, Circle)
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]

fig, ax = plt.subplots(figsize=(12, 7.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.6)
ax.axis("off")

NAVY = "#0D47A1"

# ------------------------------------------------- measurement banner
ax.text(6.0, 7.32, "From illustrative to measured \u2014 every box is placed at its physical location",
        ha="center", va="center", fontsize=10.5, weight="bold", color="#263238",
        bbox=dict(facecolor="#FFFDE7", edgecolor="#F9A825", boxstyle="round,pad=0.3"))

# ------------------------------------------------- ground line
ax.plot([0.15, 11.85], [1.5, 1.5], color="#78909C", lw=3, solid_capstyle="round")
ax.text(0.18, 1.28, "GROUND", ha="left", va="top", fontsize=8, color="#78909C",
        weight="bold")

# ================================================= ZONE A: CLIENT-TRANSMIT
ax.add_patch(FancyBboxPatch((0.2, 1.68), 3.55, 5.15,
                            boxstyle="round,pad=0.02,rounding_size=0.15",
                            facecolor="#E8F5E9", edgecolor="#A5D6A7", linewidth=1.4))
ax.text(1.98, 6.62, "CLIENT \u2014 TRANSMIT", ha="center", va="center", fontsize=11,
        weight="bold", color="#1B5E20")
ax.text(1.98, 6.38, "field / village  \u00b7  where data originates", ha="center",
        va="center", fontsize=8, color="#616161", style="italic")


def titled_box(x, y, w, h, title, dark, light, bullets, note=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=light, edgecolor=dark, linewidth=1.6))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.5), w, 0.5,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=dark, edgecolor=dark, linewidth=1.6))
    ax.add_patch(Rectangle((x, y + h - 0.5), w, 0.28, facecolor=dark, edgecolor="none", zorder=2))
    ax.text(x + w / 2, y + h - 0.25, title, ha="center", va="center", fontsize=9.5,
            weight="bold", color="white", zorder=3)
    yy = y + h - 0.72
    for b in bullets:
        ax.text(x + 0.12, yy, "\u2022  " + b, ha="left", va="top", fontsize=8.4, color="#212121")
        yy -= 0.27
    if note:
        ax.text(x + 0.12, y + 0.16, note, ha="left", va="bottom", fontsize=7.6,
                color="#616161", style="italic")
    return x + w / 2, y  # bottom-center


# field sensing + semantic agent (zone A)
cx_a, _ = titled_box(0.45, 4.95, 2.8, 1.15, "FIELD SENSING", "#2E7D32", "#E8F5E9",
                     ["Soil moisture \u00b7 rain \u00b7 water level"])
cx_a2, _ = titled_box(0.45, 2.15, 2.8, 2.45, "SEMANTIC AGENT", "#E65100", "#FFF3E0",
                      ["Feature extraction", "Value & urgency scoring",
                       "Admission control (q)", "Confidence estimate"],
                      note="on device or village gateway")
ax.add_patch(FancyArrowPatch((1.85, 4.85), (1.85, 4.68), arrowstyle="-|>",
                             mutation_scale=13, color="#37474F", linewidth=1.6))

# client uplink dish (zone A, on the ground)
dx = 2.95
ax.plot([dx, dx], [1.5, 1.85], color="#2E7D32", lw=2.0)
ax.add_patch(Arc((dx, 1.92), 0.55, 0.32, theta1=195, theta2=345, color="#2E7D32", lw=2.2))
ax.text(dx, 1.18, "client terminal", ha="center", va="top", fontsize=7.5,
        color="#2E7D32", style="italic")

# ================================================= SPACE SEGMENT
ax.text(6.0, 6.62, "SPACE SEGMENT", ha="center", va="center", fontsize=11,
        weight="bold", color=NAVY)
ax.text(6.0, 6.38, "LEO satellite  \u00b7  bent-pipe relay", ha="center", va="center",
        fontsize=8, color="#616161", style="italic")

cx, cy = 6.0, 5.25
# orbit path
ax.add_patch(Ellipse((cx, cy), 4.9, 1.9, fill=False, color="#90A4AE", lw=1.2,
                     ls=(0, (4, 3))))
# --- satellite artwork taken from the author's earlier (IEEE) paper, Fig. 1 ---
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def _keyed_satellite(path):
    """Load the satellite PNG, key out the near-white background (only pixels
    connected to the image border, so light-gray dish parts are preserved),
    and trim the cropped blob at the top edge."""
    img = plt.imread(path).astype(float)
    if img.shape[2] == 3:
        rgba = np.zeros(img.shape[:2] + (4,))
        rgba[..., :3] = img
        rgba[..., 3] = 1.0
    else:
        rgba = img.copy()
    h, w = rgba.shape[:2]
    # trim the top ~10% where the artwork is cut off at the image edge
    top = int(0.10 * h)
    rgba = rgba[top:, :, :]
    h = rgba.shape[0]
    bright = rgba[..., :3].min(axis=-1) > 0.86
    # flood fill from the border through bright pixels (4-connected dilation)
    seed = np.zeros((h, w), bool)
    seed[0, :] = bright[0, :]
    seed[-1, :] = bright[-1, :]
    seed[:, 0] |= bright[:, 0]
    seed[:, -1] |= bright[:, -1]
    prev = np.zeros((h, w), bool)
    cur = seed
    while not np.array_equal(cur, prev):
        prev = cur
        grown = np.zeros((h, w), bool)
        grown[1:, :] |= cur[:-1, :]
        grown[:-1, :] |= cur[1:, :]
        grown[:, 1:] |= cur[:, :-1]
        grown[:, :-1] |= cur[:, 1:]
        cur = grown & bright
    # dilate the keyed region a few px to kill the 1-px halo fringe
    for _ in range(3):
        grown = np.zeros((h, w), bool)
        grown[1:, :] |= cur[:-1, :]
        grown[:-1, :] |= cur[1:, :]
        grown[:, 1:] |= cur[:, :-1]
        grown[:, :-1] |= cur[:, 1:]
        cur = cur | grown
    rgba[..., 3] = np.where(cur, 0.0, rgba[..., 3])
    return rgba


_sat_img = _keyed_satellite("/home/hatch/workspace/ntn-eval/figures/sat_from_original_hires.png")
_sat_box = AnnotationBbox(OffsetImage(_sat_img, zoom=0.38), (cx, cy + 0.10),
                          frameon=False)
ax.add_artist(_sat_box)
ax.text(cx, cy - 1.14, "LEO satellite", ha="center", va="top", fontsize=9,
        weight="bold", color=NAVY)

# ------------------------------------------------- UPLINK (client -> satellite)
ax.add_patch(FancyArrowPatch((3.02, 2.1), (4.55, 4.72), arrowstyle="-|>",
                             mutation_scale=18, color="#2E7D32", linewidth=2.4,
                             connectionstyle="arc3,rad=0.12", shrinkB=4))
ax.text(3.55, 3.62, "UPLINK", ha="center", va="center", fontsize=10, weight="bold",
        color="#1B5E20", bbox=dict(facecolor="white", edgecolor="#1B5E20",
                                   boxstyle="round,pad=0.2"))
ax.text(4.45, 2.72, "admitted semantic\nreports", ha="center", va="top", fontsize=7.8,
        color="#1B5E20", style="italic")

# ------------------------------------------------- DOWNLINK (satellite -> gateway)
ax.add_patch(FancyArrowPatch((7.45, 4.72), (8.72, 2.48), arrowstyle="-|>",
                             mutation_scale=18, color="#4527A0", linewidth=2.4,
                             connectionstyle="arc3,rad=-0.1", shrinkB=2))
ax.text(7.0, 3.55, "DOWNLINK", ha="center", va="center", fontsize=10, weight="bold",
        color="#311B92", bbox=dict(facecolor="white", edgecolor="#311B92",
                                    boxstyle="round,pad=0.2"))
ax.text(7.0, 3.18, "task decisions\nmodel updates", ha="center", va="top", fontsize=7.8,
        color="#311B92", style="italic")

# ================================================= ZONE C: GATEWAY + TARGET
ax.add_patch(FancyBboxPatch((8.45, 1.68), 3.35, 5.15,
                            boxstyle="round,pad=0.02,rounding_size=0.15",
                            facecolor="#EDE7F6", edgecolor="#B39DDB", linewidth=1.4))
ax.text(10.12, 6.62, "GATEWAY \u2014 CLIENT TARGET", ha="center", va="center", fontsize=11,
        weight="bold", color="#4527A0")
ax.text(10.12, 6.38, "ground  \u00b7  where decisions land", ha="center", va="center",
        fontsize=8, color="#616161", style="italic")

titled_box(8.7, 1.95, 2.5, 1.30, "NTN GATEWAY", "#1565C0", "#E3F2FD",
           ["Ground station (demod/decode)", "Raw-data audit fallback"])
titled_box(8.7, 3.35, 2.5, 1.50, "EDGE TASK ENGINE", "#4527A0", "#EDE7F6",
           ["Semantic decoder", "Irrigation decision", "Flood warning level"])
titled_box(8.7, 4.95, 2.5, 1.30, "CLIENT \u2014 TARGET", "#00695C", "#E0F2F1",
           ["Application action", "Actuators \u00b7 alerts"])
for y0, y1 in ((3.10, 3.28), (4.70, 4.88)):
    ax.add_patch(FancyArrowPatch((9.95, y0), (9.95, y1), arrowstyle="-|>",
                                 mutation_scale=13, color="#37474F", linewidth=1.6))
# gateway dish on the ground
gx = 9.0
ax.plot([gx, gx], [1.5, 1.82], color="#1565C0", lw=2.0)
ax.add_patch(Arc((gx, 1.90), 0.55, 0.32, theta1=195, theta2=345, color="#1565C0", lw=2.2))

# ------------------------------------------------- feedback (via downlink)
# routed in the clear channel right of the zone-C boxes: no box crossings
ax.plot([11.2, 11.48], [5.5, 5.5], color="#00695C", lw=1.6, ls=(0, (5, 3)))
ax.plot([11.48, 11.48], [5.5, 0.85], color="#00695C", lw=1.6, ls=(0, (5, 3)))
ax.add_patch(FancyArrowPatch((11.48, 0.85), (1.95, 0.85), arrowstyle="-|>",
                             mutation_scale=14, color="#00695C", linewidth=1.6,
                             ls=(0, (5, 3))))
ax.plot([1.95, 1.95], [0.85, 2.1], color="#00695C", lw=1.6, ls=(0, (5, 3)))
ax.text(6.7, 0.55, "task-accuracy feedback \u2192 validated threshold / model update (via downlink)",
        ha="center", va="center", fontsize=8.6, color="#00695C",
        bbox=dict(facecolor="white", edgecolor="#00695C", boxstyle="round,pad=0.25"))

# ------------------------------------------------- caption (short lines, no cutoff)
# label on its own line so it can never collide with the caption text
ax.set_ylim(-0.55, 7.6)
ax.text(0.2, 0.34, "Figure 1.", ha="left", va="top", fontsize=9, weight="bold",
        color="#212121")
cap = ["System architecture by physical location: the client-transmit side (field/village)",
       "sends admitted semantic reports over the NTN uplink; the LEO satellite relays task",
       "decisions over the downlink to the ground gateway; the edge task engine drives the",
       "client-target application, with task-accuracy feedback returning via downlink."]
for i, line in enumerate(cap):
    ax.text(0.2, 0.12 - 0.17 * i, line, ha="left", va="top",
            fontsize=8, color="#424242")

plt.savefig("/home/hatch/workspace/ntn-eval/figures/fig1_architecture_v3.png", dpi=300)
plt.savefig("/home/hatch/workspace/ntn-eval/figures/fig1_architecture_v3.pdf")
print("saved fig1_architecture_v3.png / .pdf")
