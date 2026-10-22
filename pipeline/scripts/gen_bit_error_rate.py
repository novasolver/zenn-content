# -*- coding: utf-8 -*-
"""Bit Error Rate (BER) visuals. Faithful to the tool:
BER_BPSK=Q(sqrt(2*Eb/N0)), BER_16QAM=(3/8)Q(sqrt(4/5*Eb/N0)),
BER_64QAM=(7/24)Q(sqrt(2/7*Eb/N0)). Waterfall curves + constellation + bar of required Eb/N0."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bit-error-rate"
NAVY = "#0b1020"
BLUE, ORANGE, RED, GREEN = "#7dd3fc", "#f59e0b", "#ff6b6b", "#9be7a3"

def Q(x):
    return 0.5 * math.erfc(x / math.sqrt(2))

def ber(mod, lin):
    if lin <= 0: return 0.5
    if mod == "bpsk": return Q(math.sqrt(2*lin))
    if mod == "qam16": return (3/8)*Q(math.sqrt((4/5)*lin))
    if mod == "qam64": return (7/24)*Q(math.sqrt((2/7)*lin))

def req(mod):
    lo, hi = 0.0, 25.0
    for _ in range(80):
        mid = (lo+hi)/2
        if ber(mod, 10**(mid/10)) > 1e-6: lo = mid
        else: hi = mid
    return (lo+hi)/2

dbs = np.linspace(0, 20, 200)
def curve(mod):
    return [max(ber(mod, 10**(d/10)), 1e-12) for d in dbs]

def draw_waterfall(ax, title=None, marker_db=None):
    ax.set_facecolor(NAVY)
    ax.semilogy(dbs, curve("bpsk"), color=BLUE, lw=2.2, label="BPSK / QPSK")
    ax.semilogy(dbs, curve("qam16"), color=ORANGE, lw=2.2, label="16-QAM")
    ax.semilogy(dbs, curve("qam64"), color=RED, lw=2.2, label="64-QAM")
    if marker_db is not None:
        ax.semilogy([marker_db], [max(ber("bpsk", 10**(marker_db/10)), 1e-12)],
                    "o", color=GREEN, ms=9, zorder=5)
    ax.set_ylim(1e-9, 1)
    ax.set_xlim(0, 20)
    ax.set_xlabel("Eb/N0 (dB)", color="white", fontsize=9)
    ax.set_ylabel("ビット誤り率 BER", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    ax.grid(True, which="both", color="#26324d", lw=0.5)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower left")
    if title: ax.set_title(title, color="white", fontsize=10)

def constellation_pts(mod):
    if mod == "qam16": lv = [-1, -1/3, 1/3, 1]
    else: lv = [-1, -5/7, -3/7, -1/7, 1/7, 3/7, 5/7, 1]
    return [(i, j) for i in lv for j in lv]

def draw_const(ax, mod, ebn0_lin, k, title):
    ax.set_facecolor(NAVY)
    pts = constellation_pts(mod)
    rng = np.random.default_rng(7)
    sigma = min(0.22, 0.16/math.sqrt(ebn0_lin)*math.sqrt(k))
    for (ix, qx) in pts:
        n = 12
        ax.scatter(ix + sigma*rng.standard_normal(n), qx + sigma*rng.standard_normal(n),
                   s=5, color=ORANGE, alpha=0.5, edgecolors="none")
    px = [p[0] for p in pts]; py = [p[1] for p in pts]
    ax.scatter(px, py, s=22, facecolors="white", edgecolors=BLUE, linewidths=1.1, zorder=5)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    ax.axhline(0, color="#26324d", lw=0.8); ax.axvline(0, color="#26324d", lw=0.8)
    ax.set_xlabel("I", color="white", fontsize=9); ax.set_ylabel("Q", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.set_title(title, color="white", fontsize=10)

# console verification
for d in [4, 8, 10, 11, 12]:
    l = 10**(d/10)
    print(f"Eb/N0={d}dB BER_bpsk={ber('bpsk',l):.3e} 16={ber('qam16',l):.3e} 64={ber('qam64',l):.3e}")
print("required dB:", round(req("bpsk"),2), round(req("qam16"),2), round(req("qam64"),2))

# ---- closeup: waterfall + constellation ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.085, 0.15, 0.50, 0.74]); draw_waterfall(ax1, "BERウォーターフォール曲線", marker_db=8)
ax2 = fig.add_axes([0.66, 0.15, 0.31, 0.74]); draw_const(ax2, "qam16", 10**(12/10), 4, "16-QAM コンスタレーション")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.16, 0.80, 0.78]); draw_waterfall(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ビット誤り率 (BER)", "", "Eb/N0 と変調方式で決まる通信品質", cc)
os.remove(cc)

# ---- gif: sweep operating point along waterfall ----
frames = []
sweep = list(np.arange(2, 14.01, 1.0)) + list(np.arange(13, 1.99, -1.0))
for d in sweep:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.80, 0.72]); draw_waterfall(a, marker_db=d)
    b = max(ber("bpsk", 10**(d/10)), 1e-12)
    a.set_title(f"Eb/N0={d:.0f}dB  BPSK BER={b:.1e}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
