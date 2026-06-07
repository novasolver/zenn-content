# -*- coding: utf-8 -*-
"""Pipe-flow visuals. Tool is analytical (Darcy-Weisbach / Colebrook-White /
Moody / velocity profile). Faithfully reproduces those with matplotlib.
Produces cover / charts-closeup / slider-anim.gif."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "pipe-flow"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"

def colebrook_turb(Re, epsD):
    f = 0.02
    for _ in range(40):
        rhs = -2 * np.log10(epsD / 3.7 + 2.51 / (Re * np.sqrt(f)))
        f = 1 / (rhs * rhs)
    return f
def colebrook(Re, epsD):
    if Re < 2300: return 64 / Re
    if Re < 4000:
        fl = 64 / 2300; ft = colebrook_turb(4000, epsD)
        return fl + (ft - fl) * (Re - 2300) / 1700
    return colebrook_turb(Re, epsD)

def moody_chart(ax, mark_Re=None, mark_f=None):
    ax.set_facecolor(NAVY)
    Re = np.logspace(2.8, 8, 240)
    eds = [0, 0.0001, 0.001, 0.01]
    cols = ["#00b894", CYAN, ORANGE, "#d63031"]
    labs = ["ε/D=0 (smooth)", "ε/D=0.0001", "ε/D=0.001", "ε/D=0.01"]
    # laminar branch
    Rl = np.linspace(600, 2300, 50)
    ax.plot(Rl, 64 / Rl, color="#9fb2d6", lw=1.6, ls="--", label="層流 64/Re")
    for ed, c, lb in zip(eds, cols, labs):
        f = [colebrook(r, ed) for r in Re]
        ax.plot(Re, f, color=c, lw=1.5, label=lb)
    ax.axvspan(2300, 4000, color="white", alpha=0.06)
    ax.text(2950, 0.075, "遷移", color="#9fb2d6", ha="center", fontsize=8, rotation=90)
    if mark_Re is not None:
        ax.scatter([mark_Re], [mark_f], s=90, color="#FFD166", ec="#001F3F", zorder=6, lw=1.5)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(600, 1e8); ax.set_ylim(0.008, 0.1)
    ax.set_xlabel("Reynolds 数 Re", color="white", fontsize=9)
    ax.set_ylabel("Darcy 摩擦係数 f", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7, loc="upper right")

def vprofile(ax, Re):
    ax.set_facecolor(NAVY)
    r = np.linspace(-1, 1, 200)
    if Re < 3000:
        u = np.maximum(0, 1 - r * r); kind = "層流 放物線"; col = CYAN
    else:
        u = np.power(np.maximum(0, 1 - np.abs(r)), 1 / 7); kind = "乱流 1/7乗則"; col = ORANGE
    ax.fill_betweenx(r, 0, u, color=col, alpha=0.25)
    ax.plot(u, r, color=col, lw=2.2)
    # arrows
    for ri in np.linspace(-0.92, 0.92, 11):
        ui = (np.maximum(0, 1 - ri * ri) if Re < 3000 else np.power(max(0, 1 - abs(ri)), 1 / 7))
        ax.annotate("", xy=(ui, ri), xytext=(0, ri),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1, alpha=0.8))
    ax.axhline(1, color="#3b4a6b", lw=2); ax.axhline(-1, color="#3b4a6b", lw=2)
    ax.set_xlim(0, 1.25); ax.set_ylim(-1.15, 1.15)
    ax.set_title(f"{kind}\nRe = {Re:.0f}", color="white", fontsize=9.5)
    ax.set_xlabel("u / u_max", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# default operating point: D=50mm, Q=0.01, water, steel
rho, mu = 998.2, 1.002e-3
D = 0.05; A = np.pi * D * D / 4; U = 0.01 / A
Re0 = rho * U * D / mu; epsD0 = 0.000046 / D; f0 = colebrook(Re0, epsD0)
dP0 = f0 * (10 / D) * 0.5 * rho * U * U
print(f"default: U={U:.3f} Re={Re0:.3e} f={f0:.5f} dP={dP0:.0f}Pa ({dP0/1e5:.3f}bar)")

# ---- closeup: Moody + velocity profiles (laminar & turbulent) ----
fig = plt.figure(figsize=(9.8, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.06, 0.14, 0.45, 0.78]); moody_chart(ax1, Re0, f0)
ax1.set_title("Moody チャート（黄=既定動作点）", color="white", fontsize=10)
ax2 = fig.add_axes([0.58, 0.16, 0.18, 0.66]); vprofile(ax2, 1500)
ax3 = fig.add_axes([0.80, 0.16, 0.18, 0.66]); vprofile(ax3, 100000)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover: Moody chart ----
figc = plt.figure(figsize=(5.2, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.15, 0.80, 0.80]); moody_chart(axc, Re0, f0)
cover_chart = os.path.join(figlib.outdir(SLUG), "_coverchart.png")
figlib.save_fig(figc, cover_chart, dpi=120)
figlib.make_cover(SLUG, "パイプ流れと", "層流・乱流遷移",
                  "Darcy-Weisbach・Moody・Reynolds 数を可視化", cover_chart)
os.remove(cover_chart)

# ---- gif: velocity profile morph + Moody point as Re sweeps ----
frames = []
Res = np.concatenate([np.logspace(np.log10(500), np.log10(3e5), 40),
                      np.logspace(np.log10(3e5), np.log10(500), 20)])
for Re in Res:
    fcur = colebrook(Re, epsD0)
    f2 = plt.figure(figsize=(6.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a1 = f2.add_axes([0.09, 0.17, 0.46, 0.74]); moody_chart(a1, Re, fcur)
    a1.get_legend().remove()
    a2 = f2.add_axes([0.64, 0.14, 0.32, 0.74]); vprofile(a2, Re)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
