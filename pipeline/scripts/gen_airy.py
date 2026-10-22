# -*- coding: utf-8 -*-
"""Airy disk visuals. I=[2 J1(x)/x]^2; θ=1.22λ/D; r_focal=1.22λF#.
Faithful to the tool (λ=550nm, D=100mm, F#=8 default)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
from scipy.special import j1
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "airy-disk"
NAVY = "#0a1929"
CYAN, RED, YELLOW = "#00B4D8", "#ff8c8c", "#FFD166"
Z1 = 3.8317  # first zero of J1

def airy_I(x):
    x = np.asarray(x, dtype=float)
    out = np.where(np.abs(x) < 1e-9, 1.0, (2*j1(np.where(x==0,1e-12,x))/np.where(x==0,1e-12,x))**2)
    return out

def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def pattern2d(npx=260, xmax=12.0):
    g = np.linspace(-xmax, xmax, npx)
    X, Y = np.meshgrid(g, g)
    R = np.sqrt(X**2 + Y**2)
    I = airy_I(R)
    return np.power(np.clip(I,0,1), 0.42)  # gamma like the tool

# ---- closeup: 1D profile + resolution vs D ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72]); style(ax1)
x = np.linspace(-3*Z1, 3*Z1, 600)
r_over_rAiry = x / Z1
ax1.plot(r_over_rAiry, airy_I(x), color=CYAN, lw=2.4)
ax1.axvspan(-1, 1, color=YELLOW, alpha=0.12)
ax1.axvline(1, color=RED, ls="--", lw=1.3); ax1.axvline(-1, color=RED, ls="--", lw=1.3)
ax1.set_xlabel("半径 r / エアリー半径", color="white", fontsize=9)
ax1.set_ylabel("相対強度 I/I0", color="white", fontsize=9)
ax1.set_title("エアリー強度 [2 J₁(x)/x]²", color="white", fontsize=10)
ax1.text(0, 1.02, "中央 83.8%", color=YELLOW, ha="center", fontsize=8)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72]); style(ax2)
D = np.linspace(10, 1000, 100)  # mm
lam = 550e-9
theta = 1.22*lam/(D*1e-3)*1e6  # μrad
ax2.plot(D, theta, color=CYAN, lw=2.6)
for Dv in (10, 100, 1000):
    tv = 1.22*lam/(Dv*1e-3)*1e6
    ax2.plot(Dv, tv, "o", color=RED, ms=6)
ax2.set_xlabel("開口直径 D (mm)", color="white", fontsize=9)
ax2.set_ylabel("角分解能 θ (μrad)", color="white", fontsize=9)
ax2.set_yscale("log"); ax2.set_xscale("log")
ax2.set_title("θ = 1.22 λ/D（λ=550nm）", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover: 2D Airy pattern ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); axc.axis("off")
img = pattern2d()
# tint greenish (550nm)
rgb = np.zeros(img.shape + (3,))
rgb[...,0] = img*0.55; rgb[...,1] = img; rgb[...,2] = img*0.55
axc.imshow(rgb, origin="lower")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "エアリーディスク", "θ = 1.22 λ/D", "円形開口の回折限界", cc)
os.remove(cc)

# ---- gif: sweep D, pattern scales (smaller D -> wider pattern) ----
frames = []
D_seq = list(range(20, 320, 24)) + list(range(320, 20, -24))
base = pattern2d(npx=200, xmax=12.0)
for Dv in D_seq:
    # angular resolution scales as 1/D; visualize by scaling xmax (smaller D -> see fewer rings = pattern looks bigger)
    xmax = 12.0 * (100.0/Dv)  # at D=100 baseline xmax=12; smaller D -> larger xmax field shows wider central
    img = pattern2d(npx=200, xmax=max(4.0, min(40.0, xmax)))
    f2 = plt.figure(figsize=(4.6, 4.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.0, 1.0, 0.90]); a.axis("off")
    rgb = np.zeros(img.shape + (3,))
    rgb[...,0] = img*0.55; rgb[...,1] = img; rgb[...,2] = img*0.55
    a.imshow(rgb, origin="lower")
    th = 1.22*550e-9/(Dv*1e-3)*1e6
    f2.text(0.5, 0.94, f"D={Dv} mm  →  θ={th:.1f} μrad", color="white",
            ha="center", fontsize=12)
    frames.append(figlib.fig_to_pil(f2, dpi=66))
figlib.save_gif(frames, SLUG, duration=140)
print("done.")
