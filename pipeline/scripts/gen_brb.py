# -*- coding: utf-8 -*-
"""Buckling-restrained brace (BRB) visuals. Faithful to the tool's compute():
P_y=A*Fy; k=A*E/L; dy=Fy*L/E; mu=drift/dy; E_cyc=4*P_y*(drift-dy); strain=drift/L*100.
The idealised elastoplastic hysteresis loop is symmetric (no buckling)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "buckling-restrained-brace"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#34d399"

# tool defaults
A, Fy, L, Egpa, drift = 2500.0, 235.0, 3500.0, 205.0, 40.0
E_MPa = Egpa * 1000.0

def calc(A, Fy, L, drift):
    Py = A * Fy                      # N
    k = A * E_MPa / L                # N/mm
    dy = Py / k                      # mm
    mu = drift / dy if dy > 0 else 0
    Ecyc = 4 * Py * max(0.0, drift - dy)  # N.mm
    strain = drift / L * 100.0       # %
    return Py / 1000, k / 1000, dy, mu, Ecyc / 1e6, strain  # kN, kN/mm, mm, -, kJ, %

Py, k, dy, mu, Ecyc, strain = calc(A, Fy, L, drift)
print(f"default: Py={Py:.1f}kN k={k:.1f}kN/mm dy={dy:.3f}mm mu={mu:.2f} Ecyc={Ecyc:.1f}kJ strain={strain:.2f}%")


def loop_points(Pyk, dy, dd):
    """Idealised symmetric elastoplastic loop, cycled to +/- design drift."""
    if dd > dy:
        xs = [-dd, -dy, dy, dd, dd, dy, -dy, -dd]
        ys = [-Pyk, -Pyk, Pyk, Pyk, Pyk, Pyk, -Pyk, -Pyk]
    else:
        xs = [-dd, dd]; ys = [-Pyk * dd / max(dy, 1e-6), Pyk * dd / max(dy, 1e-6)]
    return xs, ys


# ---------- closeup: hysteresis loop + energy-vs-drift ----------
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.14, 0.40, 0.74]); ax1.set_facecolor(NAVY)
xs, ys = loop_points(Py, dy, drift)
ax1.fill(xs, ys, color=CYAN, alpha=0.18)
ax1.plot(xs, ys, color=CYAN, lw=2.6)
ax1.axhline(0, color="#3b4a6b", lw=0.8); ax1.axvline(0, color="#3b4a6b", lw=0.8)
ax1.axhline(Py, color=ORANGE, ls="--", lw=1); ax1.axhline(-Py, color=ORANGE, ls="--", lw=1)
ax1.text(drift, Py + 18, "+P_y", color=ORANGE, fontsize=9, ha="right")
ax1.text(-drift, -Py - 28, "-P_y", color=ORANGE, fontsize=9, ha="left")
ax1.set_xlabel("軸方向変形 δ (mm)", color="white", fontsize=9)
ax1.set_ylabel("軸力 P (kN)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title(f"対称な履歴ループ（面積=E_cyc={Ecyc:.0f} kJ）", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.14, 0.39, 0.74]); ax2.set_facecolor(NAVY)
dv = np.linspace(5, 150, 60)
ev = np.array([calc(A, Fy, L, d)[4] for d in dv])
ax2.fill_between(dv, ev, color=GREEN, alpha=0.18); ax2.plot(dv, ev, color=GREEN, lw=2.4)
ax2.plot(drift, Ecyc, "o", color=ORANGE, ms=9)
ax2.annotate(f"設計層間変形 {drift:.0f}mm\n→ {Ecyc:.0f} kJ", (drift, Ecyc),
             textcoords="offset points", xytext=(14, -6), color=ORANGE, fontsize=8.5)
ax2.set_xlabel("設計層間変形 (mm)", color="white", fontsize=9)
ax2.set_ylabel("1サイクル消費エネルギー (kJ)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("E_cyc = 4 P_y (δ_design − δ_y)", color="white", fontsize=9.5)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---------- cover ----------
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.06, 0.12, 0.90, 0.80]); axc.set_facecolor(NAVY)
axc.fill(xs, ys, color=CYAN, alpha=0.20); axc.plot(xs, ys, color=CYAN, lw=3)
axc.axhline(0, color="#3b4a6b", lw=0.8); axc.axvline(0, color="#3b4a6b", lw=0.8)
axc.set_xlabel("δ (mm)", color="#9fb2d6", fontsize=9)
axc.set_ylabel("P (kN)", color="#9fb2d6", fontsize=9)
axc.tick_params(colors="#9fb2d6", labelsize=7)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "座屈拘束ブレース", "BRBの履歴吸収", "座屈しない芯材が描く対称な弾塑性ループ", cc)
os.remove(cc)

# ---------- gif: design drift sweep growing the loop + tracing the cycle ----------
frames = []
drifts = list(np.linspace(8, 120, 22)) + list(np.linspace(116, 12, 12))
xmax, ymax = 130, Py * 1.25
for dd in drifts:
    _, _, _dy, _mu, _Ecyc, _st = calc(A, Fy, L, dd)
    xs2, ys2 = loop_points(Py, _dy, dd)
    f2 = plt.figure(figsize=(5.4, 3.1)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.16, 0.84, 0.72]); a.set_facecolor(NAVY)
    a.fill(xs2, ys2, color=CYAN, alpha=0.18); a.plot(xs2, ys2, color=CYAN, lw=2.6)
    a.axhline(0, color="#3b4a6b", lw=0.8); a.axvline(0, color="#3b4a6b", lw=0.8)
    a.plot([dd], [Py], "o", color=ORANGE, ms=8)   # marker at peak tension
    a.set_xlim(-xmax, xmax); a.set_ylim(-ymax, ymax)
    a.set_xlabel("軸方向変形 δ (mm)", color="white", fontsize=8.5)
    a.set_ylabel("軸力 P (kN)", color="white", fontsize=8.5)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    col = "#ef4444" if _st > 3 else "white"
    a.set_title(f"δ_design={dd:.0f}mm  μ={_mu:.1f}  芯材ひずみ={_st:.2f}%  E_cyc={_Ecyc:.0f}kJ",
                color=col, fontsize=8.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
