# -*- coding: utf-8 -*-
"""kirchhoff-laws visuals: series-parallel circuit diagram + KCL bar chart + R3-sweep gif.

Matplotlib only (RECIPE STEP 5). Faithful to the real tool:
  V source -> R1 (series) -> node a -> R2 || R3 (parallel) -> GND.
  Rpar = R2 R3/(R2+R3), Rtot = R1 + Rpar, Itot = V/Rtot,
  Vpar = V - Itot*R1, I2 = Vpar/R2, I3 = Vpar/R3, KCL: Itot = I2 + I3.
Defaults V=12, R1=100, R2=200, R3=300 -> Itot=54.5mA, I2=32.7, I3=21.8, Vpar=6.55V.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow
import figlib

SLUG = "kirchhoff-laws"
NAVY = "#0a1929"; WIRE = "#cfe3f7"; BLUE = "#4dabff"
CYAN = "#00B4D8"; GOLD = "#FFD166"; GREEN = "#28d17c"; RED = "#e74c3c"
V0 = 12.0


def solve(V, R1, R2, R3):
    Rpar = R2 * R3 / (R2 + R3)
    Rtot = R1 + Rpar
    Itot = V / Rtot
    Vpar = V - Itot * R1
    return dict(Rpar=Rpar, Rtot=Rtot, Itot=Itot, Vpar=Vpar,
                Vr1=Itot * R1, I2=Vpar / R2, I3=Vpar / R3)


def fmtI(I):
    return "%.3f A" % I if abs(I) >= 1 else "%.1f mA" % (I * 1000)


def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")


def res_h(ax, x1, x2, y, color, lab, val):
    """Horizontal zig-zag resistor."""
    n = 6; dx = (x2 - x1) / (n * 2); xs = [x1]; ys = [y]
    for i in range(n):
        xs += [x1 + dx * (2 * i + 1), x1 + dx * (2 * i + 2)]
        ys += [y + 0.018, y - 0.018]
    xs.append(x2); ys.append(y)
    ax.plot(xs, ys, color=color, lw=2.2)
    ax.text((x1 + x2) / 2, y + 0.05, lab, color=color, ha="center", fontsize=10)
    ax.text((x1 + x2) / 2, y - 0.065, val, color=color, ha="center", fontsize=9)


def res_v(ax, x, y1, y2, color, lab, val, side):
    n = 6; dy = (y2 - y1) / (n * 2); xs = [x]; ys = [y1]
    for i in range(n):
        ys += [y1 + dy * (2 * i + 1), y1 + dy * (2 * i + 2)]
        xs += [x + 0.022, x - 0.022]
    xs.append(x); ys.append(y2)
    ax.plot(xs, ys, color=color, lw=2.2)
    ox = -0.05 if side == "left" else 0.05
    ha = "right" if side == "left" else "left"
    ax.text(x + ox, (y1 + y2) / 2 + 0.02, lab, color=color, ha=ha, fontsize=10)
    ax.text(x + ox, (y1 + y2) / 2 - 0.04, val, color=color, ha=ha, fontsize=9)


def draw_circuit(ax, V, R1, R2, R3):
    s = solve(V, R1, R2, R3)
    ax.set_facecolor(NAVY); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    L, R, T, B = 0.10, 0.92, 0.82, 0.16
    aX = 0.58; r2X = 0.70; r3X = 0.88
    # wires
    ax.plot([L, aX], [T, T], color=WIRE, lw=2)
    ax.plot([aX, r3X], [T, T], color=WIRE, lw=2)
    ax.plot([L, L], [T, B], color=WIRE, lw=2)
    ax.plot([L, r3X], [B, B], color=WIRE, lw=2)
    ax.plot([aX, r2X], [T, T], color=WIRE, lw=2)
    for x in (r2X, r3X):
        ax.plot([x, x], [T, 0.66], color=WIRE, lw=2)
        ax.plot([x, x], [0.32, B], color=WIRE, lw=2)
    # R1 series on top wire
    res_h(ax, L + 0.10, aX - 0.08, T, BLUE, "R_1", "%.0f Ω" % R1)
    ax.text((L + 0.10 + aX - 0.08) / 2, T + 0.10,
            "V_R1=%.2f V" % s["Vr1"], color="#9ad0ff", ha="center", fontsize=8)
    # I_total arrow
    ax.add_patch(FancyArrow(aX - 0.05, T, 0.03, 0, width=0.004,
                 head_width=0.02, head_length=0.018, color=GOLD, length_includes_head=True))
    ax.text(aX - 0.04, T + 0.045, "I_total=" + fmtI(s["Itot"]), color=GOLD, ha="center", fontsize=8)
    # parallel resistors
    res_v(ax, r2X, 0.32, 0.66, CYAN, "R_2", "%.0f Ω" % R2, "left")
    res_v(ax, r3X, 0.32, 0.66, GOLD, "R_3", "%.0f Ω" % R3, "right")
    for x, c, lab, I, ha, ox in [(r2X, CYAN, "I_2", s["I2"], "right", -0.018),
                                 (r3X, GOLD, "I_3", s["I3"], "left", 0.018)]:
        ax.add_patch(FancyArrow(x, 0.30, 0, -0.03, width=0.004,
                     head_width=0.02, head_length=0.018, color=c, length_includes_head=True))
        ax.text(x + ox, 0.245, lab + "=" + fmtI(I), color=c, ha=ha, fontsize=8)
    ax.text((r2X + r3X) / 2, T + 0.10, "V_par=%.2f V" % s["Vpar"],
            color="#9ad0ff", ha="center", fontsize=8)
    # source
    ax.add_patch(Circle((L, (T + B) / 2), 0.04, fill=False, color=GOLD, lw=2.2))
    ax.text(L, (T + B) / 2 + 0.012, "+", color=GOLD, ha="center", fontsize=12, weight="bold")
    ax.text(L, (T + B) / 2 - 0.04, "−", color=GOLD, ha="center", fontsize=12, weight="bold")
    ax.text(L - 0.055, (T + B) / 2, "V=%.0f V" % V, color=GOLD, ha="right", fontsize=9)
    ax.text(aX, T + 0.03, "a", color=WIRE, ha="center", fontsize=9)


def draw_bars(ax, V, R1, R2, R3):
    s = solve(V, R1, R2, R3)
    style(ax)
    vals = [("I_total", s["Itot"] * 1000, CYAN),
            ("I_2", s["I2"] * 1000, GREEN),
            ("I_3", s["I3"] * 1000, GOLD)]
    xs = np.arange(3)
    ax.bar(xs, [v[1] for v in vals], color=[v[2] for v in vals], width=0.55)
    for i, (lab, v, c) in enumerate(vals):
        ax.text(i, v + 1, "%.1f" % v, color="white", ha="center", fontsize=9)
    ssum = vals[1][1] + vals[2][1]
    ax.axhline(ssum, color=GOLD, ls="--", lw=1.3)
    ax.text(1.0, ssum * 1.06, "I_2+I_3=%.1f" % ssum, color=GOLD, ha="center", fontsize=8)
    ax.set_xticks(xs); ax.set_xticklabels([v[0] for v in vals], color="white", fontsize=9)
    ax.set_ylabel("電流 [mA]", color="white", fontsize=9)
    ax.set_ylim(0, max(vals[0][1], ssum) * 1.35)
    ax.set_title("KCL: I_total = I_2 + I_3", color="white", fontsize=10)


# ---- charts-closeup: circuit + bar chart side by side ----
fig = plt.figure(figsize=(9.2, 4.3)); fig.patch.set_facecolor(NAVY)
axc = fig.add_axes([0.01, 0.04, 0.52, 0.9]); draw_circuit(axc, V0, 100, 200, 300)
axc.set_title("直並列回路: V + R_1(直列) + R_2//R_3(並列)", color="white", fontsize=10)
axb = fig.add_axes([0.62, 0.14, 0.35, 0.76]); draw_bars(axb, V0, 100, 200, 300)
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png"); figlib.save_fig(fig, cu, dpi=130)
print(" closeup")

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.1)); figc.patch.set_facecolor(NAVY)
gg = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_circuit(gg, V0, 100, 200, 300)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "キルヒホッフ", "の法則",
                  "直並列回路でKVL/KCLを検証 — I_total=I_2+I_3", cc)
os.remove(cc)

# ---- slider-anim.gif: sweep R3 ----
frames = []
seq = list(np.linspace(300, 50, 16)) + list(np.linspace(50, 600, 18)) + list(np.linspace(600, 300, 8))
for R3 in seq:
    fr = plt.figure(figsize=(4.4, 3.6)); fr.patch.set_facecolor(NAVY)
    g = fr.add_axes([0.0, 0.02, 0.62, 0.9]); draw_circuit(g, V0, 100, 200, R3)
    h = fr.add_axes([0.66, 0.16, 0.32, 0.70]); draw_bars(h, V0, 100, 200, R3)
    g.set_title("R_3=%.0f Ω" % R3, color="white", fontsize=11)
    frames.append(figlib.fig_to_pil(fr, dpi=85))
figlib.save_gif(frames, SLUG, duration=110)
print("done")
