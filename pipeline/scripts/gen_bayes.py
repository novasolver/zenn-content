# -*- coding: utf-8 -*-
"""Bayes theorem visuals. P(A|B)=P(B|A)P(A)/P(B). Base-rate fallacy.
Faithful to bayes-theorem-visual tool (posterior, prior->posterior curve, 1000-person grid)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bayes-theorem-visual"
NAVY = "#0b1020"
GREEN, ORANGE, BLUE, GREY = "#27ae60", "#f59e0b", "#7dd3fc", "#9aa6bf"

def posterior(PA, PBA, PBNA):
    PB = PBA*PA + PBNA*(1-PA)
    return PBA*PA/PB

# --- closeup: prior->posterior curve + 1000-person grid for rare-disease ---
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

# left: prior -> posterior curves for two FPR values
ax1 = fig.add_axes([0.08, 0.15, 0.46, 0.74]); ax1.set_facecolor(NAVY)
priors = np.linspace(0.001, 0.999, 400)
for PBNA, col, lbl in [(0.05, GREEN, "偽陽性率 5%"), (0.20, ORANGE, "偽陽性率 20%")]:
    post = [posterior(p, 0.99, PBNA)*100 for p in priors]
    ax1.plot(priors*100, post, color=col, lw=2.4, label=lbl)
# mark rare-disease point
ax1.scatter([1], [posterior(0.01, 0.99, 0.05)*100], color="#fff", zorder=5, s=35)
ax1.annotate("有病率1% → 16.7%", (1, 16.7), (18, 14), color="white", fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color="white"))
ax1.plot([0,100],[0,100], color="#3b4a6b", lw=1, ls=":")
ax1.set_xlabel("事前確率 P(A) （%）", color="white", fontsize=9)
ax1.set_ylabel("事後確率 P(A|B) （%）", color="white", fontsize=9)
ax1.set_xlim(0,100); ax1.set_ylim(0,100)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower right")
ax1.set_title("感度99%・事前確率を動かすと（基準率の誤謬）", color="white", fontsize=9.5)

# right: 1000-person grid for rare-disease preset
ax2 = fig.add_axes([0.60, 0.10, 0.37, 0.80]); ax2.set_facecolor(NAVY)
PA, PBA, PBNA = 0.01, 0.99, 0.05
N=1000; cols=40; rows=25
tp=round(N*PA*PBA); fn=round(N*PA*(1-PBA)); fp=round(N*(1-PA)*PBNA); tn=N-tp-fn-fp
types = ['TP']*tp + ['FN']*fn + ['FP']*fp + ['TN']*tn
cmap = {'TP':GREEN, 'FN':GREY, 'FP':ORANGE, 'TN':"#33415c"}
for i in range(N):
    c = i % cols; r = i // cols
    ax2.scatter(c, rows-1-r, s=11, color=cmap[types[i]], marker='o')
ax2.set_xlim(-1, cols); ax2.set_ylim(-1, rows)
ax2.axis("off")
ax2.set_title(f"1000人: 真陽性{tp} / 偽陽性{fp}\n陽性的中率 = {tp}/{tp+fp} = 16.7%",
              color="white", fontsize=9.5)
# legend
from matplotlib.lines import Line2D
leg = [Line2D([0],[0], marker='o', color='none', markerfacecolor=cmap['TP'], label='真陽性', markersize=7),
       Line2D([0],[0], marker='o', color='none', markerfacecolor=cmap['FP'], label='偽陽性', markersize=7),
       Line2D([0],[0], marker='o', color='none', markerfacecolor=cmap['TN'], label='真陰性', markersize=7)]
ax2.legend(handles=leg, facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5,
           loc="lower center", ncol=3, bbox_to_anchor=(0.5,-0.10))
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# --- cover ---
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.78]); axc.set_facecolor(NAVY)
for PBNA, col in [(0.05, GREEN), (0.20, ORANGE)]:
    post = [posterior(p, 0.99, PBNA)*100 for p in priors]
    axc.plot(priors*100, post, color=col, lw=2.6)
axc.plot([0,100],[0,100], color="#3b4a6b", lw=1, ls=":")
axc.scatter([1],[16.7], color="#fff", s=30, zorder=5)
axc.set_xlim(0,100); axc.set_ylim(0,100)
axc.set_xlabel("事前確率 (%)", color="white", fontsize=9)
axc.set_ylabel("事後確率 (%)", color="white", fontsize=9)
axc.tick_params(colors="#9fb2d6", labelsize=8)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ベイズの定理", "と基準率の誤謬", "P(A|B)=P(B|A)P(A)/P(B)：感度99%でもPPV17%", cc)
os.remove(cc)

# --- gif: sweep prior P(A), grid + posterior bar ---
frames = []
PBA, PBNA = 0.99, 0.05
priors_g = list(np.linspace(0.005, 0.6, 9)) + list(np.linspace(0.6, 0.005, 6))
for pa in priors_g:
    post = posterior(pa, PBA, PBNA)
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.14, 0.17, 0.82, 0.66]); a.set_facecolor(NAVY)
    # posterior bar + prior bar
    a.barh([1], [pa*100], color="#5b6b8c", height=0.5)
    a.barh([0], [post*100], color=GREEN if post>0.5 else ORANGE, height=0.5)
    a.set_yticks([0,1]); a.set_yticklabels(["事後 P(A|B)","事前 P(A)"], color="white", fontsize=9)
    a.set_xlim(0,100); a.set_xlabel("確率 (%)", color="white", fontsize=9)
    a.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.text(post*100+2, 0, f"{post*100:.1f}%", color="white", va="center", fontsize=9)
    a.text(pa*100+2, 1, f"{pa*100:.1f}%", color="white", va="center", fontsize=9)
    a.set_title(f"感度99% / 偽陽性5% : 事前 {pa*100:.1f}% → 事後 {post*100:.1f}%",
                color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=160)
print("done.")
