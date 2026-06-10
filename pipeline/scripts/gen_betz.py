# -*- coding: utf-8 -*-
"""Betz limit visuals. Faithful to the tool: C_P(a)=4a(1-a)^2, max 16/27 at a=1/3,
P=C_P*0.5*rho*A*V^3. C_P(a) curve + streamtube contraction."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "betz-limit"
NAVY = "#0a1929"
CYAN, YELLOW, BLUE, WHITE = "#00B4D8", "#FFD166", "#007BFF", "#cfe3f7"
BETZ = 16/27

def cp_of(a): return 4*a*(1-a)*(1-a)

def draw_cp(ax, a_now=1/3, title=None):
    ax.set_facecolor(NAVY)
    a = np.linspace(0,1,200)
    cp = np.clip(cp_of(a), 0, None)
    ax.plot(a, cp, color=CYAN, lw=2.6)
    ax.axhline(BETZ, color=YELLOW, ls="--", lw=1.3, alpha=0.7)
    ax.axvline(1/3, color=YELLOW, ls="--", lw=1.3, alpha=0.7)
    ax.text(0.55, BETZ+0.012, "Betz: 16/27 ≈ 0.593", color=YELLOW, fontsize=8.5)
    ax.text(1/3+0.02, 0.06, "a = 1/3", color=YELLOW, fontsize=8.5)
    cpn = max(0, cp_of(a_now))
    ax.plot(a_now, cpn, 'o', color=YELLOW, ms=9, markeredgecolor="#001F3F")
    ax.vlines(a_now, 0, cpn, color=YELLOW, ls=":", lw=1, alpha=0.6)
    ax.set_xlim(0,1); ax.set_ylim(0,0.7)
    ax.set_xlabel("軸方向誘導係数 a", color="white", fontsize=9)
    ax.set_ylabel("パワー係数 C_P", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_tube(ax, a, title=None):
    """Top view of the streamtube: contraction/expansion with a."""
    ax.set_facecolor(NAVY)
    aS = max(0.001, min(0.49, a))
    rR = 1.0                      # rotor radius (ref)
    r1 = rR*np.sqrt(1-aS)         # upstream
    r3 = rR*np.sqrt((1-aS)/max(0.02,1-2*aS))  # downstream
    r3 = min(r3, rR*3.0)
    xr = 0.0
    # boundaries via simple smooth interpolation
    xu = np.linspace(-3,0,50); xd = np.linspace(0,3,50)
    top_u = np.interp(xu, [-3,0], [r1,rR]);
    # use smoothstep for nicer taper
    t = (xu+3)/3; top_u = r1 + (rR-r1)*(3*t**2-2*t**3)
    t2 = xd/3; top_d = rR + (r3-rR)*(3*t2**2-2*t2**3)
    x = np.concatenate([xu,xd]); top = np.concatenate([top_u,top_d])
    ax.fill_between(x, -top, top, color=CYAN, alpha=0.22)
    ax.plot(x, top, color=CYAN, lw=1.6); ax.plot(x, -top, color=CYAN, lw=1.6)
    # rotor disk
    ax.plot([0,0], [-rR,rR], color=YELLOW, lw=3)
    # arrows (length ~ speed)
    for yy in [-r1*0.5, 0, r1*0.5]:
        ax.annotate("", xy=(-2.0,yy), xytext=(-2.7,yy), arrowprops=dict(arrowstyle="->",color=WHITE,lw=1.4))
    vW = max(0.1, 1-2*aS)
    for yy in [-r3*0.5, 0, r3*0.5]:
        ax.annotate("", xy=(2.7,yy), xytext=(2.7-0.7*vW,yy), arrowprops=dict(arrowstyle="->",color=WHITE,lw=1.4))
    ax.text(-2.7, r1+0.25, "V∞", color=WHITE, fontsize=8.5)
    ax.text(0.05, rR+0.25, "(1-a)V∞", color=WHITE, fontsize=8.5)
    ax.text(1.6, r3+0.25, "(1-2a)V∞", color=WHITE, fontsize=8.5)
    ax.text(-2.9, -3.4, f"a = {aS:.2f}", color=YELLOW, fontsize=9)
    ax.set_xlim(-3,3); ax.set_ylim(-3.8,3.8)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

print(f"Cp(1/3)={cp_of(1/3):.4f}  16/27={BETZ:.4f}")

# closeup: C_P curve + streamtube
fig = plt.figure(figsize=(9.6,4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07,0.15,0.50,0.74]); draw_cp(ax1, 1/3, "パワー係数 C_P(a) 曲線")
ax2 = fig.add_axes([0.62,0.10,0.36,0.80]); draw_tube(ax2, 1/3, "流管の収縮（a=1/3）")
closeup = os.path.join(figlib.outdir(SLUG),"charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14,0.15,0.82,0.80]); draw_cp(axc, 1/3)
cc = os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG,"ベッツ限界","","C_P,max = 16/27 ≈ 0.593 — 風車の理論最大効率", cc)
os.remove(cc)

# gif: sweep a along C_P curve
frames=[]
aseq = list(np.arange(0.0,0.51,0.04)) + list(np.arange(0.48,0.0,-0.04))
for av in aseq:
    f2 = plt.figure(figsize=(5.2,3.5)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.14,0.16,0.82,0.74]); draw_cp(a, av)
    a.set_title(f"a = {av:.2f}   C_P = {max(0,cp_of(av)):.3f}   ベッツ比 {max(0,cp_of(av))/BETZ*100:.0f}%",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
