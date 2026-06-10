# -*- coding: utf-8 -*-
"""Bloom filter false-positive visuals. Faithful to the tool:
p=(1-e^(-kn/m))^k, k_opt=(m/n)ln2, occupancy=1-e^(-kn/m).
Charts: fpr vs k (sensitivity valley) + fpr vs m/n + bit-array fill."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bloom-filter-false-positive"
NAVY = "#0b1020"
BLUE, ORANGE, GREEN, PURPLE = "#7dd3fc", "#f59e0b", "#9be7a3", "#c084fc"

def fpr(n, m, k): return (1 - math.exp(-k*n/m))**k
def occ(n, m, k): return 1 - math.exp(-k*n/m)
def kopt(n, m): return (m/n)*math.log(2)

N, M = 50000, 800000  # m/n = 16

def draw_kcurve(ax, title=None):
    ax.set_facecolor(NAVY)
    ks = np.arange(1, 17)
    ys = [fpr(N, M, int(k))*100 for k in ks]
    ax.semilogy(ks, ys, "-o", color=BLUE, lw=2.0, ms=4)
    ko = kopt(N, M)
    ax.axvline(ko, color=ORANGE, ls="--", lw=1.4)
    ax.text(ko+0.2, ys[-1]*1.4, f"k_opt={ko:.1f}", color=ORANGE, fontsize=8)
    ax.set_xlabel("ハッシュ数 k", color="white", fontsize=9)
    ax.set_ylabel("偽陽性率 (%)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    ax.grid(True, which="both", color="#26324d", lw=0.5)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_ratio(ax, title=None):
    ax.set_facecolor(NAVY)
    ratios = np.arange(4, 24.01, 0.5)
    ys = []
    for r in ratios:
        mm = N*r
        ko = max(1, round(kopt(N, mm)))
        ys.append(fpr(N, mm, ko)*100)
    ax.semilogy(ratios, ys, color=PURPLE, lw=2.2)
    ax.fill_between(ratios, ys, 1e-4, color=PURPLE, alpha=0.12)
    ax.set_xlabel("1要素あたりのビット数 m/n", color="white", fontsize=9)
    ax.set_ylabel("偽陽性率（最適k, %)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    ax.grid(True, which="both", color="#26324d", lw=0.5)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

# console verification
print("defaults n=50000 m=800000 k=7:")
print("  fpr=", f"{fpr(N,M,7)*100:.3f}%", " occ=", f"{occ(N,M,7)*100:.1f}%",
      " kopt=", round(kopt(N,M),2))
for k in [1,3,7,11,14,16]:
    print(f"  k={k:2d} fpr={fpr(N,M,k)*100:.3f}%")

# ---- closeup: k-curve + ratio-curve ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.085, 0.15, 0.40, 0.74]); draw_kcurve(ax1, "ハッシュ数 k と偽陽性率（m/n=16）")
ax2 = fig.add_axes([0.585, 0.15, 0.39, 0.74]); draw_ratio(ax2, "メモリ m/n と偽陽性率（最適k）")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.17, 0.17, 0.79, 0.76]); draw_kcurve(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "Bloom フィルタ", "偽陽性率", "p=(1-e^-kn/m)^k と最適ハッシュ数", cc)
os.remove(cc)

# ---- gif: sweep m (memory), show bit fill + fpr ----
frames = []
sweep = list(range(200000, 1400001, 100000)) + list(range(1300000, 200000, -100000))
for mv in sweep:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.80, 0.70])
    a.set_facecolor(NAVY)
    ks = np.arange(1, 17)
    ys = [fpr(N, mv, int(k))*100 for k in ks]
    a.semilogy(ks, ys, "-o", color=BLUE, lw=2.0, ms=3.5)
    a.set_ylim(1e-4, 100)
    a.set_xlabel("ハッシュ数 k", color="white", fontsize=9)
    a.set_ylabel("偽陽性率 (%)", color="white", fontsize=9)
    a.tick_params(colors="#9fb2d6", labelsize=8)
    a.grid(True, which="both", color="#26324d", lw=0.5)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"m/n={mv/N:.0f}  最小偽陽性率={min(ys):.3f}%", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
