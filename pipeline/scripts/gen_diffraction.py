# -*- coding: utf-8 -*-
"""Diffraction grating visuals. d(sin th - sin thi)=m lam; I=[sin(N d)/(N sin d)]^2.
Faithful to the tool (d=1.67um ~600 lines/mm, lam=532nm, N=500)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "diffraction-grating"
NAVY = "#0b1020"; CYAN = "#7dd3fc"
d_um = 1.67; N = 500

def wl_rgb(wl):
    if wl < 440: r, g, b = -(wl-440)/60, 0, 1
    elif wl < 490: r, g, b = 0, (wl-440)/50, 1
    elif wl < 510: r, g, b = 0, 1, -(wl-510)/20
    elif wl < 580: r, g, b = (wl-510)/70, 1, 0
    elif wl < 645: r, g, b = 1, -(wl-645)/65, 0
    else: r, g, b = 1, 0, 0
    return (max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b)))

def intensity(thdeg, lam_nm, thi=0):
    th = np.radians(thdeg); lam = lam_nm/1000
    delta = np.pi*d_um*(np.sin(th) - np.sin(thi))/lam
    sd = np.sin(delta)
    return np.where(np.abs(sd) < 1e-9, 1.0, (np.sin(N*delta)/(N*sd))**2)

print("orders (lam=532nm):", [round(np.degrees(np.arcsin(m*0.532/d_um)), 1) for m in range(4)])

# closeup: intensity pattern + dispersion (angle vs wavelength)
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.52, 0.74]); ax1.set_facecolor(NAVY)
th = np.linspace(-80, 80, 4000)
I = np.minimum(intensity(th, 532), 1)
ax1.plot(th, I, color="#36e36b", lw=1)
for m in range(-3, 4):
    s = m*0.532/d_um
    if abs(s) <= 1:
        a = np.degrees(np.arcsin(s))
        ax1.text(a, 1.04, f"m={m}", color="white", ha="center", fontsize=7)
ax1.set_xlabel("回折角 θ (°)", color="white", fontsize=9); ax1.set_ylabel("相対強度", color="white", fontsize=9)
ax1.set_xlim(-80, 80); ax1.set_ylim(0, 1.15); ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title("多スリット干渉パターン（緑 532nm, N=500）", color="white", fontsize=10)
ax2 = fig.add_axes([0.66, 0.16, 0.31, 0.72]); ax2.set_facecolor(NAVY)
wls = np.linspace(380, 780, 200)
angs = np.degrees(np.arcsin(np.clip(wls/1000/d_um, 0, 1)))
for i in range(len(wls)-1):
    ax2.plot(wls[i:i+2], angs[i:i+2], color=wl_rgb(wls[i]), lw=3)
ax2.set_xlabel("波長 λ (nm)", color="white", fontsize=9); ax2.set_ylabel("1次回折角 θ₁ (°)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("白色光の分散（赤ほど大きく曲がる）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover: rainbow fan
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); axc.set_facecolor(NAVY)
for wl in range(380, 781, 3):
    a = np.arcsin(min(1, wl/1000/d_um))
    axc.plot([0, np.sin(a)], [0, -np.cos(a)], color=wl_rgb(wl), lw=2, alpha=0.85)
axc.plot([0, 0], [0, -1], color="#9fb2d6", lw=1.5, ls="--")   # m=0
axc.annotate("", xy=(-0.5, 0.6), xytext=(-0.8, 0.85), arrowprops=dict(arrowstyle="-|>", color="white", lw=2))
axc.set_xlim(-0.85, 1.0); axc.set_ylim(-1.05, 0.95); axc.set_aspect("equal"); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "回折格子", "", "d sinθ = mλ で白色光を虹に分ける", cc)
os.remove(cc)

# gif: sweep wavelength, peaks move
frames = []
for wl in list(range(400, 760, 18)) + list(range(742, 400, -18)):
    I = np.minimum(intensity(th, wl), 1)
    f2 = plt.figure(figsize=(5.4, 3.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.10, 0.16, 0.86, 0.74]); a.set_facecolor(NAVY)
    a.plot(th, I, color=wl_rgb(wl), lw=1.2)
    a.set_xlim(-80, 80); a.set_ylim(0, 1.1); a.tick_params(colors="#9fb2d6", labelsize=7)
    a.set_xlabel("回折角 θ (°)", color="white", fontsize=8)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"λ={wl}nm  1次回折角={np.degrees(np.arcsin(min(1,wl/1000/d_um))):.1f}°", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
