# -*- coding: utf-8 -*-
"""Drag terminal velocity visuals. Faithful to drag-terminal-velocity.html:
m dv/dt = mg - 0.5*rho*Cd*A*v^2; vt=sqrt(2mg/(rho Cd A)); forward-Euler integration.
Default rho=1.2, g=9.81."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "drag-terminal-velocity"
NAVY = "#020d1a"
BLUE, CYAN, ORANGE, RED, GREEN = "#007BFF", "#00B4D8", "#f59e0b", "#ff6b6b", "#9be7a3"
G, RHO = 9.81, 1.2

PRESETS = {
    "スカイダイバー": (75, 0.70, 1.00),
    "パラシュート":   (90, 28.0, 1.30),
    "野球ボール":     (0.145, 0.00427, 0.47),
    "雨滴":           (5e-5, 7.85e-5, 0.47),
    "雹":             (0.01, 7.07e-4, 0.47),
}


def vt(m, A, Cd, rho=RHO): return math.sqrt(2 * m * G / (rho * Cd * A))


def integrate(m, A, Cd, rho=RHO, tmax=None, dt=0.02):
    vterm = vt(m, A, Cd, rho)
    if tmax is None:
        tmax = 1.6 * 1.472 * vterm / G + 3
    ts, vs, accs = [], [], []
    v, t = 0.0, 0.0
    while t <= tmax:
        a = (m * G - 0.5 * rho * Cd * A * v * v) / m
        ts.append(t); vs.append(v); accs.append(a)
        v += a * dt; t += dt
    return np.array(ts), np.array(vs), np.array(accs), vterm


def style_ax(ax, xl, yl, title=None):
    ax.set_facecolor(NAVY)
    ax.set_xlabel(xl, color="white", fontsize=9)
    ax.set_ylabel(yl, color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")
    ax.grid(True, color="#13314d", lw=0.6)
    if title:
        ax.set_title(title, color="white", fontsize=10)


# ---- closeup: v(t) curves for several presets + terminal lines ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.52, 0.72])
colors = {"スカイダイバー": BLUE, "野球ボール": ORANGE, "雹": GREEN, "雨滴": CYAN, "パラシュート": RED}
for name in ["スカイダイバー", "雹", "野球ボール", "パラシュート", "雨滴"]:
    m, A, Cd = PRESETS[name]
    ts, vs, accs, vterm = integrate(m, A, Cd, tmax=14)
    ax1.plot(ts, vs, color=colors[name], lw=2.2, label=f"{name} (vt={vterm:.0f})")
    ax1.axhline(vterm, color=colors[name], lw=0.8, ls="--", alpha=0.4)
style_ax(ax1, "時間 t (s)", "速度 v (m/s)", "落下速度 v(t) の漸近（プリセット別）")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)

# right: a(t) for skydiver
ax2 = fig.add_axes([0.67, 0.16, 0.30, 0.72])
ts, vs, accs, vterm = integrate(75, 0.70, 1.0, tmax=12)
ax2.plot(ts, accs, color=CYAN, lw=2.4)
ax2.axhline(0, color="#6b8", lw=0.8, ls=":")
style_ax(ax2, "時間 t (s)", "加速度 a (m/s²)", "加速度は g→0 へ")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.15, 0.16, 0.81, 0.78])
for name in ["スカイダイバー", "野球ボール", "パラシュート"]:
    m, A, Cd = PRESETS[name]
    ts, vs, accs, vterm = integrate(m, A, Cd, tmax=12)
    axc.plot(ts, vs, color=colors[name], lw=2.6)
    axc.axhline(vterm, color=colors[name], lw=0.8, ls="--", alpha=0.4)
style_ax(axc, "時間 t (s)", "速度 v (m/s)")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "空気抵抗と終端速度", "", "vt = √(2mg / ρ·Cd·A)  と  v(t) = vt·tanh(gt/vt)", cc)
os.remove(cc)

# ---- gif: sweep mass (skydiver shape), watch vt and curve change ----
frames = []
mass_list = list(range(40, 130, 10)) + list(range(120, 40, -10))
for m in mass_list:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.81, 0.70])
    ts, vs, accs, vterm = integrate(m, 0.70, 1.0, tmax=14)
    a.plot(ts, vs, color=BLUE, lw=2.6)
    a.axhline(vterm, color=ORANGE, lw=1.2, ls="--", alpha=0.7)
    a.fill_between(ts, 0, vs, color=BLUE, alpha=0.10)
    style_ax(a, "時間 t (s)", "速度 v (m/s)")
    a.set_ylim(0, 60)
    a.set_title(f"質量 m={m}kg (A=0.70, Cd=1.0) → vt={vterm:.1f} m/s", color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
