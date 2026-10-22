# -*- coding: utf-8 -*-
"""contact-lens-oxygen-permeability visuals.
charts-closeup: Dk vs water-content curves + Dk/t requirement bars (24/87/125).
cover: branded.  gif: thickness sweep showing Dk/t crossing the 24/87/125 lines.
Faithful to the tool's JS (matProps, Holden 5.5*exp(0.072*WC), Dk/t = Dk/t*0.1).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "contact-lens-oxygen-permeability"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; GREEN = "#9be7a3"; ORANGE = "#f59e0b"; RED = "#ff6b6b"; CYAN = "#00b4d8"

def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def dk_sihy(WC, Dkmax=175, wf=0.5):
    return Dkmax * (1 - wf * (1 - WC / 100))

def dk_hema(WC):
    return 5.5 * math.exp(0.072 * WC)

# ---------- charts-closeup ----------
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax = fig.add_axes([0.09, 0.16, 0.42, 0.72]); style(ax)
wc = np.linspace(0, 80, 200)
ax.plot(wc, [dk_sihy(w) for w in wc], color=GREEN, lw=2.3, label="Si-Hy 等価モデル")
ax.plot(wc, [dk_hema(w) for w in wc], color=BLUE, lw=2.3, label="HEMA: 5.5e^(0.072WC)")
ax.plot(38, dk_sihy(38), "o", color=ORANGE, ms=8)
ax.annotate("既定 Si-Hy\nWC=38%, Dk=121", (38, dk_sihy(38)), (44, 35),
            color="white", fontsize=8, arrowprops=dict(color="white", arrowstyle="->"))
ax.set_ylim(0, 200)
ax.set_xlabel("含水率 WC [%]", color="white", fontsize=9)
ax.set_ylabel("酸素透過係数 Dk [x10^-11]", color="white", fontsize=9)
ax.set_title("Dk vs 含水率 (Holden 1984)", color="white", fontsize=10)
ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper left")

ax2 = fig.add_axes([0.60, 0.16, 0.37, 0.72]); style(ax2)
labels = ["デイリー\n(24)", "連続装用\n(87)", "無浮腫\n(125)", "既定設計点\n(121)"]
vals = [24, 87, 125, 121]
cols = ["#7aa9d6", "#5380b8", "#2d5a99", GREEN]
ax2.bar(range(4), vals, color=cols)
for i, v in enumerate(vals):
    ax2.text(i, v + 4, str(v), ha="center", color="white", fontsize=9)
ax2.set_xticks(range(4)); ax2.set_xticklabels(labels, fontsize=7.5)
ax2.set_ylim(0, 145)
ax2.set_ylabel("Dk/t [x10^-9]", color="white", fontsize=9)
ax2.set_title("装用モード別 Dk/t 要求", color="white", fontsize=10)
ax2.axhline(125, color=RED, ls=":", lw=1)
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, cu, dpi=130); print(" closeup")

# ---------- cover preview chart ----------
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.18, 0.80, 0.74]); style(axc)
axc.bar(range(4), vals, color=cols)
axc.set_xticks(range(4)); axc.set_xticklabels(["24", "87", "125", "121"], fontsize=9)
axc.set_ylabel("Dk/t", color="white", fontsize=9)
axc.set_title("Holden-Mertz 基準ライン", color="white", fontsize=10)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png")
figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "コンタクトレンズの", "酸素透過率 Dk/t",
                  "角膜が呼吸できる設計を数式で見る", cc)
os.remove(cc)

# ---------- gif: thickness sweep ----------
frames = []
ts = list(np.linspace(0.15, 0.05, 22)) + list(np.linspace(0.05, 0.15, 12))
Dk = dk_sihy(38)  # 120.75
for t in ts:
    Dk_t = Dk / t * 0.1
    EOP = min(21, 21 * (1 - math.exp(-Dk_t / 30)))
    f = plt.figure(figsize=(5.0, 3.2)); f.patch.set_facecolor(NAVY)
    a = f.add_axes([0.13, 0.20, 0.83, 0.64]); style(a)
    cur = GREEN if Dk_t > 125 else (BLUE if Dk_t > 87 else (ORANGE if Dk_t > 24 else RED))
    a.bar([0, 1, 2, 3], [24, 87, 125, Dk_t],
          color=["#7aa9d6", "#5380b8", "#2d5a99", cur])
    a.set_xticks([0, 1, 2, 3]); a.set_xticklabels(["24", "87", "125", "現在"], fontsize=9)
    a.set_ylim(0, 230); a.set_ylabel("Dk/t", color="white", fontsize=9)
    a.text(3, Dk_t + 6, f"{Dk_t:.0f}", ha="center", color="white", fontsize=10, fontweight="bold")
    verdict = "無浮腫OK" if Dk_t > 125 else ("連続装用OK" if Dk_t > 87 else "デイリーOK")
    a.set_title(f"Si-Hy  t={t*1000:.0f}um -> Dk/t={Dk_t:.0f}  EOP={EOP:.1f}%  [{verdict}]",
                color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done")
