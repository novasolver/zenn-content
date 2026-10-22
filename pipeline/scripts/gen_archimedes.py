# -*- coding: utf-8 -*-
"""Archimedes buoyancy visuals. Fb=rho_fluid*g*V_sub; floating fraction = rho_obj/rho_fluid.
Faithful to archimedes-buoyancy tool (density bar chart, float fraction)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "archimedes-buoyancy"
NAVY = "#0b1020"
BLUE, RED, CYAN, WATER = "#3b82f6", "#ef4444", "#67c7e8", "#1d3a6b"
G = 9.81

MATS = [("コルク",200),("木材",600),("氷",917),("淡水",1000),("海水",1025),
        ("アルミ",2700),("鉄/鋼",7800),("鉛",11340),("水銀",13600)]

# --- closeup: density bar chart + floating fraction diagram ---
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

# left: density bars
ax1 = fig.add_axes([0.09, 0.22, 0.48, 0.66]); ax1.set_facecolor(NAVY)
names = [m[0] for m in MATS]; rhos = [m[1] for m in MATS]
colors = [BLUE if r in (1000,1025) else RED if r==7800 else "#6aa9c9" for r in rhos]
ax1.bar(range(len(MATS)), rhos, color=colors)
for i,r in enumerate(rhos):
    ax1.text(i, r+200, f"{r/1000:.1f}k" if r>=1000 else str(r), color="white",
             ha="center", fontsize=7)
ax1.set_xticks(range(len(MATS))); ax1.set_xticklabels(names, rotation=40, ha="right", fontsize=7.5, color="white")
ax1.set_ylabel("密度 (kg/m³)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title("各材料の密度（青=流体, 赤=鉄）", color="white", fontsize=9.5)

# right: floating fraction (ice in seawater)
ax2 = fig.add_axes([0.63, 0.14, 0.33, 0.74]); ax2.set_facecolor(NAVY)
ax2.set_xlim(0,1); ax2.set_ylim(0,1.2)
frac = 917/1025  # submerged fraction
# water
ax2.add_patch(plt.Rectangle((0,0),1,0.62, color=WATER))
ax2.axhline(0.62, color=CYAN, lw=2)
# iceberg: total height block; submerged = frac of block sits below waterline
bh = 0.5  # block height in axis units
top = 0.62 + bh*(1-frac)
bot = 0.62 - bh*frac
ax2.add_patch(plt.Rectangle((0.3, bot), 0.4, bh, color="#cfe8f5", ec="white"))
ax2.text(0.5, top+0.05, "10.5% が水面上", color="white", ha="center", fontsize=8.5)
ax2.text(0.5, 0.62-bh*frac/2, "89.5%\n海面下", color=NAVY, ha="center", va="center", fontsize=8.5, weight="bold")
ax2.axis("off")
ax2.set_title("氷山: 水没率 = ρ_ice/ρ_sea\n= 917/1025 ≈ 89.5%", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# --- cover ---
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13, 0.20, 0.84, 0.72]); axc.set_facecolor(NAVY)
axc.bar(range(len(MATS)), rhos, color=colors)
axc.set_xticks(range(len(MATS))); axc.set_xticklabels(names, rotation=40, ha="right", fontsize=6.5, color="white")
axc.set_ylabel("密度 (kg/m³)", color="white", fontsize=8.5)
axc.tick_params(colors="#9fb2d6", labelsize=7)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "アルキメデスの原理", "", "Fb=ρ_fluid·g·V：水没率=ρ_obj/ρ_fluid", cc)
os.remove(cc)

# --- gif: sweep object density, show float fraction + sink ---
frames = []
rfluid = 1025
densities = list(range(200, 2200, 200)) + list(range(2000, 200, -200))
for robj in densities:
    f2 = plt.figure(figsize=(5.0, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.04, 0.04, 0.92, 0.80]); a.set_facecolor(NAVY)
    a.set_xlim(0,1); a.set_ylim(0,1.2); a.axis("off")
    a.add_patch(plt.Rectangle((0,0),1,0.62, color=WATER))
    a.axhline(0.62, color=CYAN, lw=2)
    floats = robj < rfluid
    if floats:
        frac = robj/rfluid
        bh=0.5
        bot=0.62-bh*frac
        a.add_patch(plt.Rectangle((0.35,bot),0.3,bh, color="#28a745", ec="white"))
        a.text(0.5, 0.62-bh*frac/2, f"水没\n{frac*100:.0f}%", color="white",
               ha="center", va="center", fontsize=8, weight="bold")
        title=f"ρ_obj={robj} < 海水1025 → 浮く（水没{frac*100:.0f}%）"
    else:
        a.add_patch(plt.Rectangle((0.35,0.06),0.3,0.30, color="#dc3545", ec="white"))
        a.text(0.5, 0.21, "沈降", color="white", ha="center", va="center", fontsize=9, weight="bold")
        title=f"ρ_obj={robj} > 海水1025 → 沈む"
    a.set_title(title, color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=170)
print("done.")
