# -*- coding: utf-8 -*-
"""Mohr's circle visuals. sigma1,2=(sx+sy)/2 +- R, R=sqrt(((sx-sy)/2)^2+txy^2).
Faithful to the tool (default sx=80, sy=-40, txy=60)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "mohr-circle"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; RED = "#ff6b6b"; GREEN = "#9be7a3"
sx, sy, txy = 80.0, -40.0, 60.0
C = (sx + sy) / 2; R = np.sqrt(((sx - sy) / 2)**2 + txy**2)
s1, s2 = C + R, C - R; thp = 0.5 * np.degrees(np.arctan2(2*txy, sx - sy))
print(f"sx={sx} sy={sy} txy={txy}: C={C} R={R:.2f} s1={s1:.2f} s2={s2:.2f} tmax={R:.2f} theta_p={thp:.1f}deg")

def draw_circle(ax, mark2th=None):
    ax.set_facecolor(NAVY)
    th = np.linspace(0, 2*np.pi, 200)
    ax.plot(C + R*np.cos(th), R*np.sin(th), color=CYAN, lw=2)
    ax.axhline(0, color="#3b4a6b", lw=1); ax.axvline(0, color="#3b4a6b", lw=1)
    ax.plot(C, 0, "+", color="white", ms=10)
    # points A(sx,txy), B(sy,-txy)
    ax.plot(sx, txy, "o", color=RED, ms=7); ax.text(sx+3, txy+5, "A(σx,τxy)", color=RED, fontsize=8)
    ax.plot(sy, -txy, "o", color=GREEN, ms=7); ax.text(sy-6, -txy-9, "B(σy,−τxy)", color=GREEN, fontsize=8, ha="right")
    ax.plot([sx, sy], [txy, -txy], color="#9fb2d6", lw=1, ls="--")
    # principal stresses
    ax.plot(s1, 0, "v", color=ORANGE, ms=9); ax.text(s1, -12, f"σ₁={s1:.0f}", color=ORANGE, fontsize=8, ha="center")
    ax.plot(s2, 0, "v", color=ORANGE, ms=9); ax.text(s2, -12, f"σ₂={s2:.0f}", color=ORANGE, fontsize=8, ha="center")
    ax.plot(C, R, "^", color="#c084fc", ms=9); ax.text(C+4, R+3, f"τmax={R:.0f}", color="#c084fc", fontsize=8)
    if mark2th is not None:
        a = np.arctan2(txy, (sx-sy)/2)  # angle of A from center
        ang = a + np.radians(2*mark2th)
        px, py = C + R*np.cos(ang), R*np.sin(ang)
        ax.plot([C, px], [0, py], color="#FFD166", lw=1.5)
        ax.plot(px, py, "o", color="#FFD166", ms=8, mec="white")
    ax.set_xlabel("垂直応力 σ (MPa)", color="white", fontsize=9)
    ax.set_ylabel("せん断応力 τ (MPa)", color="white", fontsize=9)
    ax.set_aspect("equal"); ax.set_xlim(s2-25, s1+25); ax.set_ylim(-R-25, R+25)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def sig_tau(thdeg):
    t = np.radians(thdeg)
    sig = C + (sx-sy)/2*np.cos(2*t) + txy*np.sin(2*t)
    tau = -(sx-sy)/2*np.sin(2*t) + txy*np.cos(2*t)
    return sig, tau

# closeup: circle + transformation curves
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.06, 0.12, 0.44, 0.80]); draw_circle(ax1)
ax1.set_title("モールの応力円", color="white", fontsize=10)
ax2 = fig.add_axes([0.60, 0.16, 0.37, 0.72]); ax2.set_facecolor(NAVY)
ths = np.linspace(0, 180, 200); sig, tau = sig_tau(ths)
ax2.plot(ths, sig, color=ORANGE, lw=2, label="σ(θ)")
ax2.plot(ths, tau, color=CYAN, lw=2, label="τ(θ)")
ax2.axvline(thp % 180, color=GREEN, lw=1, ls="--")
ax2.text((thp % 180)+3, s1*0.9, f"θ_p={thp:.1f}°\n(τ=0, 主応力)", color=GREEN, fontsize=8)
ax2.axhline(0, color="#3b4a6b", lw=0.8)
ax2.set_xlabel("面の回転角 θ (°)", color="white", fontsize=9); ax2.set_ylabel("応力 (MPa)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
ax2.set_title("面を回すと σ・τ が変化（θ_p で主応力）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(4.8, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.12, 0.84, 0.84]); draw_circle(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "モールの応力円と", "主応力", "σ₁,₂=(σx+σy)/2±√(...) を可視化", cc)
os.remove(cc)

# gif: rotate plane, point moves around circle
frames = []
for thdeg in list(range(0, 180, 6)):
    f2 = plt.figure(figsize=(4.6, 4.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.10, 0.84, 0.82]); draw_circle(a, mark2th=thdeg)
    sig, tau = sig_tau(thdeg)
    a.set_title(f"面の回転 θ={thdeg}°  σ={sig:.0f}, τ={tau:.0f} MPa", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
