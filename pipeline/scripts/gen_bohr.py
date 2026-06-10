# -*- coding: utf-8 -*-
"""Bohr hydrogen model visuals. En=-13.6/n^2 eV, rn=n^2 a0, Balmer series.
Faithful to the tool (a0=0.0529 nm, lambda=1240/dE)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bohr-hydrogen-model"
NAVY = "#0b1020"
a0 = 0.0529

def E(n): return -13.6/(n*n)
def wl(n1, n2): return 1240/abs(E(n1)-E(n2))

def wl_to_rgb(w):
    # crude visible-spectrum colour map (380-700 nm)
    if w < 380 or w > 700: return (0.5,0.5,0.5)
    if w < 440: r,g,b = -(w-440)/60,0,1
    elif w < 490: r,g,b = 0,(w-440)/50,1
    elif w < 510: r,g,b = 0,1,-(w-510)/20
    elif w < 580: r,g,b = (w-510)/70,1,0
    elif w < 645: r,g,b = 1,-(w-645)/65,0
    else: r,g,b = 1,0,0
    return (max(0,min(1,r)), max(0,min(1,g)), max(0,min(1,b)))

def draw_orbits(ax, n1=4, n2=2, nmax=6):
    ax.set_facecolor(NAVY)
    rmax = (nmax*nmax*a0)
    for n in range(1, nmax+1):
        r = n*n*a0
        active = n in (n1, n2)
        c = "#e74c3c" if n==n1 else "#27ae60" if n==n2 else (1,1,1,0.18)
        circ = plt.Circle((0,0), r, fill=False, ec=c, lw=2 if active else 0.8)
        ax.add_patch(circ)
        ax.text(r*0.71, r*0.71, f"n={n}", color=(c if active else (1,1,1,0.5)),
                fontsize=8.5 if active else 7.5, ha="center")
    ax.plot(0,0, "o", color="#f39c12", ms=10)
    # transition arrow + photon colour
    w = wl(n1, n2); col = wl_to_rgb(w)
    ang = -np.pi/3.5
    r1, r2 = n1*n1*a0, n2*n2*a0
    ax.annotate("", xy=(r2*np.cos(ang), r2*np.sin(ang)),
                xytext=(r1*np.cos(ang), r1*np.sin(ang)),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
    ax.text(0.02, 0.96, f"{n1}→{n2}  λ={w:.0f} nm", transform=ax.transAxes,
            color=col, fontsize=10, va="top", fontweight="bold")
    ax.set_xlim(-rmax*1.05, rmax*1.05); ax.set_ylim(-rmax*1.05, rmax*1.05)
    ax.set_aspect("equal"); ax.axis("off")

# closeup: orbits + Balmer spectrum bar
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.06, 0.46, 0.88]); draw_orbits(ax1, 4, 2, 6)
ax1.set_title("ボーア軌道（n₁=4 → n₂=2, Hβ）", color="white", fontsize=10)

ax2 = fig.add_axes([0.58, 0.14, 0.38, 0.60]); ax2.set_facecolor(NAVY)
names = {3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ"}
for u in range(3,7):
    w = wl(u,2)
    ax2.axvline(w, color=wl_to_rgb(w), lw=3)
    ax2.text(w, 1.03, f"{names[u]}\n{w:.0f}", color=wl_to_rgb(w), ha="center",
             va="bottom", fontsize=8, fontweight="bold")
ax2.set_xlim(380, 700); ax2.set_ylim(0, 1.0)
ax2.set_xlabel("波長 λ (nm)", color="white", fontsize=9)
ax2.set_yticks([])
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("バルマー系列（n→2）の輝線", color="white", fontsize=9, pad=22)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.04, 0.92, 0.9]); draw_orbits(axc, 4, 2, 6)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ボーア水素原子モデル", "", "Eₙ = −13.6/n² eV とバルマー系列", cc)
os.remove(cc)

# gif: sweep n1 from 3..6 (and back), n2=2 fixed -> Balmer series
frames = []
seq = [3,4,5,6,6,5,4,3]
for n1 in seq:
    f2 = plt.figure(figsize=(5.0, 3.6)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.04, 0.04, 0.92, 0.86]); draw_orbits(a, n1, 2, 6)
    w = wl(n1, 2)
    a.set_title(f"n₁={n1} → n₂=2   λ={w:.0f} nm", color="white", fontsize=11)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=520)
print("done.")
