# -*- coding: utf-8 -*-
"""Biot-Savart law (circular loop on-axis) visuals.
B(z)=mu0*N*I*R^2/(2(R^2+z^2)^1.5); B0=mu0*N*I/(2R); z_half=R*sqrt(2^(2/3)-1)~0.766R.
Faithful to the tool: default I1 R5cm z0 N1."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "biot-savart-law"
NAVY = "#0a1929"
CYAN, GOLD, ORANGE, RED, BLUE = "#00B4D8", "#FFD166", "#FF9F43", "#FF6B6B", "#4ac6ff"
MU0 = 4*np.pi*1e-7

def B(I, R_cm, z_cm, N):
    R = R_cm*0.01; z = z_cm*0.01
    return MU0*N*I*R*R/(2*(R*R+z*z)**1.5)

def draw_profile(ax, I=1, R_cm=5, z_cm=0, N=1, title=None):
    ax.set_facecolor(NAVY)
    Zmax = R_cm*3
    z = np.linspace(-Zmax, Zmax, 241)
    Bv = B(I, R_cm, z, N)*1e6  # uT
    B0 = B(I, R_cm, 0, N)*1e6
    ax.plot(z, Bv, color=CYAN, lw=2.6)
    ax.fill_between(z, Bv, 0, color=CYAN, alpha=0.10)
    zh = R_cm*np.sqrt(2**(2/3)-1)
    # half-width markers
    for s in (-1, 1):
        ax.plot([s*zh, s*zh], [0, B0/2], color=GOLD, ls="--", lw=1.2, alpha=0.7)
    ax.plot([-zh, zh], [B0/2, B0/2], color=GOLD, ls="--", lw=1.2, alpha=0.7)
    ax.text(0, B0/2+B0*0.04, f"±z(1/2)={zh:.2f}cm", color=GOLD, fontsize=8, ha="center")
    # center marker
    ax.plot([0], [B0], "o", color=GOLD, ms=8, zorder=5)
    # current marker
    Bz = B(I, R_cm, z_cm, N)*1e6
    if abs(z_cm) <= Zmax:
        ax.plot([z_cm], [Bz], "o", color=ORANGE, ms=8, mec="white", mew=1.0, zorder=6)
        ax.plot([z_cm, z_cm], [0, Bz], color=ORANGE, lw=1, alpha=0.6)
    ax.set_xlim(-Zmax, Zmax); ax.set_ylim(0, B0*1.15)
    ax.set_xlabel("軸上距離 z [cm]", color="white", fontsize=9)
    ax.set_ylabel("磁束密度 B [μT]", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_loop(ax, I=1, R_cm=5, z_cm=0, N=1, title=None):
    """Schematic 3D-perspective loop + observation point + B vector."""
    ax.set_facecolor(NAVY)
    viewHalf = max(R_cm*3, z_cm*1.2+R_cm, 10)
    # symmetry axis
    ax.annotate("", xy=(viewHalf, 0), xytext=(-viewHalf, 0),
                arrowprops=dict(arrowstyle="->", color="#8fb8e0", lw=1.2))
    ax.text(viewHalf*0.96, viewHalf*0.06, "z", color="#cfe3f7", fontsize=10)
    for k in (-2, -1, 1, 2):
        xx = k*R_cm
        if abs(xx) < viewHalf:
            ax.plot([xx, xx], [-viewHalf*0.03, viewHalf*0.03], color="#8fb8e0", lw=1, alpha=0.5)
            ax.text(xx, -viewHalf*0.13, f"{'+' if k>0 else ''}{k}R", color="#8fb8e0", fontsize=7.5, ha="center")
    # loop as ellipse (perspective: rx compressed)
    th = np.linspace(0, 2*np.pi, 120)
    ry = R_cm; rx = R_cm*0.32
    ax.plot(rx*np.cos(th), ry*np.sin(th), color=BLUE, lw=2.4)
    # current arrows
    for ang in [np.pi*0.5, np.pi, np.pi*1.5, 0]:
        px = rx*np.cos(ang); py = ry*np.sin(ang)
        tx = -rx*np.sin(ang); ty = ry*np.cos(ang)
        L = np.hypot(tx, ty); tx, ty = tx/L, ty/L
        ax.annotate("", xy=(px+tx*R_cm*0.18, py+ty*R_cm*0.18), xytext=(px, py),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    # observation point + B vector
    B0 = B(I, R_cm, 0, N); Bz = B(I, R_cm, z_cm, N)
    rel = max(0, min(1, Bz/B0 if B0 > 0 else 0))
    ax.plot([z_cm], [0], "o", color=GOLD, ms=9, zorder=6)
    arrowLen = R_cm*(0.25+rel*1.0)
    ax.annotate("", xy=(z_cm+arrowLen, 0), xytext=(z_cm, 0),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.4))
    ax.text(z_cm+arrowLen+viewHalf*0.02, viewHalf*0.08, "B", color=ORANGE, fontsize=10)
    ax.text(z_cm, -viewHalf*0.22, f"z={z_cm:.1f}cm", color=GOLD, fontsize=8, ha="center")
    ax.text(-viewHalf*0.95, viewHalf*0.82, f"I={I:.1f}A  R={R_cm:.1f}cm  N={int(N)}",
            color="#cfe3f7", fontsize=8.5, family="monospace")
    ax.set_xlim(-viewHalf, viewHalf); ax.set_ylim(-viewHalf*0.75, viewHalf*0.95)
    ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title(title, color="white", fontsize=10)

print(f"default I1 R5 z0 N1: B0={B(1,5,0,1)*1e6:.3f} uT  zhalf={5*np.sqrt(2**(2/3)-1):.3f} cm")

# ---- closeup: loop schematic + B(z) profile ----
fig = plt.figure(figsize=(9.8, 4.2)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.06, 0.46, 0.84]); draw_loop(ax1, 1, 5, 7.0, 1, "円電流ループと観測点（透視図）")
ax2 = fig.add_axes([0.57, 0.16, 0.40, 0.72]); draw_profile(ax2, 1, 5, 7.0, 1, "軸上磁場プロファイル B(z)")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.4, 3.3)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.17, 0.80, 0.74]); draw_profile(axc, 1, 5, 0, 1)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ビオ・サバールの法則", "", "円電流ループの軸上磁場 B(z)（ベル型）", cc)
os.remove(cc)

# ---- gif: sweep z, observation point rides the bell curve ----
frames = []
zs = list(np.linspace(0, 15, 14)) + list(np.linspace(15, 0, 14))
for zv in zs:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.81, 0.72]); draw_profile(a, 1, 5, zv, 1)
    ratio = B(1, 5, zv, 1)/B(1, 5, 0, 1)
    a.set_title(f"z={zv:.1f} cm  →  B(z)/B(0)={ratio:.3f}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
