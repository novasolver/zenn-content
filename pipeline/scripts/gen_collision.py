# -*- coding: utf-8 -*-
"""1D collision visuals. Momentum-conserving restitution:
v1'=((m1-e m2)v1+(1+e)m2 v2)/(m1+m2). Blocks animation + before/after bars."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import figlib

SLUG = "collision-1d"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"

def collide(m1, m2, v1, v2, e):
    v1p = ((m1-e*m2)*v1 + (1+e)*m2*v2)/(m1+m2)
    v2p = ((m2-e*m1)*v2 + (1+e)*m1*v1)/(m1+m2)
    return v1p, v2p

m1, m2, v1, v2 = 5.0, 5.0, 5.0, -3.0
for e in [1.0, 0.0]:
    v1p, v2p = collide(m1, m2, v1, v2, e)
    keb = 0.5*m1*v1*v1+0.5*m2*v2*v2; kea = 0.5*m1*v1p*v1p+0.5*m2*v2p*v2p
    print(f"e={e}: v'=({v1p:.1f},{v2p:.1f}) p:{m1*v1+m2*v2:.0f}->{m1*v1p+m2*v2p:.0f} KEloss={keb-kea:.0f}")

def draw_blocks(ax, x1, x2, vel1, vel2, title=None):
    ax.set_facecolor(NAVY)
    ax.axhline(0, color="#3b4a6b", lw=1)
    w1, w2 = 0.6*np.sqrt(m1/5), 0.6*np.sqrt(m2/5)
    ax.add_patch(Rectangle((x1-w1/2, 0), w1, 0.5*np.sqrt(m1/5), color=BLUE, ec="white"))
    ax.add_patch(Rectangle((x2-w2/2, 0), w2, 0.5*np.sqrt(m2/5), color=ORANGE, ec="white"))
    for x, v, c in [(x1, vel1, BLUE), (x2, vel2, ORANGE)]:
        if abs(v) > 0.1:
            ax.annotate("", xy=(x+0.25*np.sign(v), 0.7), xytext=(x, 0.7),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2))
            ax.text(x, 0.85, f"{v:+.0f}", color=c, ha="center", fontsize=9)
    ax.set_xlim(-3, 3); ax.set_ylim(-0.2, 1.1); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

# closeup: before/after snapshots + conservation bars
fig = plt.figure(figsize=(9.4, 4.4)); fig.patch.set_facecolor(NAVY)
axa = fig.add_axes([0.03, 0.56, 0.50, 0.34]); draw_blocks(axa, -1.2, 1.2, v1, v2, "衝突前 (m₁=m₂=5kg)")
v1p, v2p = collide(m1, m2, v1, v2, 1.0)
axb = fig.add_axes([0.03, 0.10, 0.50, 0.34]); draw_blocks(axb, -1.2, 1.2, v1p, v2p, "衝突後 (e=1：速度を交換)")
ax2 = fig.add_axes([0.62, 0.16, 0.35, 0.72]); ax2.set_facecolor(NAVY)
cats = ["運動量 p", "運動E (e=1)", "運動E (e=0)"]
keb = 0.5*m1*v1*v1+0.5*m2*v2*v2
v1e0, v2e0 = collide(m1, m2, v1, v2, 0.0); ke0 = 0.5*m1*v1e0**2+0.5*m2*v2e0**2
before = [abs(m1*v1+m2*v2), keb, keb]
after = [abs(m1*v1p+m2*v2p), 0.5*m1*v1p**2+0.5*m2*v2p**2, ke0]
x = np.arange(3)
ax2.bar(x-0.2, before, width=0.4, color=BLUE, label="前")
ax2.bar(x+0.2, after, width=0.4, color=ORANGE, label="後")
ax2.set_xticks(x); ax2.set_xticklabels(cats, color="white", fontsize=8, rotation=12)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("運動量は常に保存、KEはe<1で損失", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.4, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.05, 1.0, 0.9]); draw_blocks(axc, -1.3, 1.3, v1, v2)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "1次元衝突", "", "運動量保存と反発係数 e、弾性・非弾性", cc)
os.remove(cc)

# gif: collision over time (elastic)
frames = []
x1, x2 = -2.5, 2.5; cv1, cv2 = v1, v2; dt = 0.04; collided = False
w = 0.5
for k in range(48):
    if not collided and (x2 - x1) <= w*1.2:
        cv1, cv2 = collide(m1, m2, cv1, cv2, 1.0); collided = True
    x1 += cv1*dt*0.5; x2 += cv2*dt*0.5
    f2 = plt.figure(figsize=(5.4, 2.6)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.06, 1.0, 0.84]); draw_blocks(a, x1, x2, cv1, cv2)
    a.set_xlim(-3.2, 3.2)
    a.set_title("弾性衝突 (e=1)：等質量は速度を交換", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=80)
print("done.")
