# -*- coding: utf-8 -*-
"""Decision-tree impurity visuals. Faithful to the tool: Gini=2p(1-p),
Entropy=-sum p log2 p, ME=min(p,1-p). Curves + split tree + IG."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figlib

SLUG = "decision-tree-impurity"
NAVY = "#0a1929"
CYAN, GREEN, RED, YELLOW = "#00B4D8", "#00b894", "#e74c3c", "#FFD166"

def gini(p): return 2*p*(1-p)
def entropy(p):
    p=np.asarray(p, dtype=float)
    out=np.zeros_like(p)
    m=(p>0)&(p<1)
    pp=p[m]; q=1-pp
    out[m]=-(pp*np.log2(pp)+q*np.log2(q))
    return out
def misclass(p): return np.minimum(p,1-p)

def style(ax, title=None):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

P = np.linspace(0,1,300)

def draw_curves(ax, p1=0.5):
    style(ax, "不純度カーブ（横軸 p1）")
    ax.plot(P, gini(P), color=CYAN, lw=2.4, label="Gini = 2p(1−p)")
    ax.plot(P, entropy(P), color=GREEN, lw=2.4, label="Entropy")
    ax.plot(P, misclass(P), color=RED, lw=2.4, label="誤分類率 min(p,1−p)")
    ax.axvline(p1, color=YELLOW, lw=1.2, ls="--", alpha=0.7)
    for fn,c in [(lambda x:gini(np.array([x]))[0],CYAN),
                 (lambda x:entropy(np.array([x]))[0],GREEN),
                 (lambda x:misclass(np.array([x]))[0],RED)]:
        ax.scatter([p1],[fn(p1)], s=30, color=c, zorder=5)
    ax.set_xlabel("p1（クラス1の比率）", color="white", fontsize=9)
    ax.set_ylabel("不純度 I", color="white", fontsize=9)
    ax.set_ylim(0,1.08)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper right")

def node(ax, x, y, title, l1, l2, color):
    box=FancyBboxPatch((x-0.16,y-0.085),0.32,0.17, boxstyle="round,pad=0.012",
                       fc="#1c2f47", ec=color, lw=2, zorder=3)
    ax.add_patch(box)
    ax.text(x,y+0.045,title,ha="center",va="center",color=color,fontsize=9,fontweight="bold",zorder=4)
    ax.text(x,y-0.005,l1,ha="center",va="center",color="#cfe3f7",fontsize=8,zorder=4)
    ax.text(x,y-0.05,l2,ha="center",va="center",color="#cfe3f7",fontsize=8,zorder=4)

def draw_tree(ax, p1, leftP1, rightP1, leftN, rightN, igG):
    ax.set_facecolor(NAVY); ax.axis("off")
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    total=leftN+rightN; lf=leftN/total; rf=rightN/total
    node(ax,0.5,0.82,"Parent",f"p1={p1:.2f}",f"Gini={gini(p1):.3f}",YELLOW)
    node(ax,0.25,0.25,f"Left ({lf:.2f})",f"p1={leftP1:.2f}",f"Gini={gini(leftP1):.3f}",CYAN)
    node(ax,0.75,0.25,f"Right ({rf:.2f})",f"p1={rightP1:.2f}",f"Gini={gini(rightP1):.3f}",GREEN)
    ax.plot([0.5,0.25],[0.73,0.34],color="#cfe3f7",lw=1.4,alpha=0.6)
    ax.plot([0.5,0.75],[0.73,0.34],color="#cfe3f7",lw=1.4,alpha=0.6)
    ax.text(0.5,0.50,f"IG_Gini = {igG:.3f}",ha="center",color="#ffd24b",fontsize=10,fontweight="bold")
    ax.set_title("親→左子・右子の分割と情報利得", color="white", fontsize=10)

# default params
p1,leftP1,rightP1,leftN,rightN=0.5,0.8,0.2,50,100
lf=leftN/(leftN+rightN); rf=rightN/(leftN+rightN)
igG=gini(p1)-(lf*gini(leftP1)+rf*gini(rightP1))
print(f"IG_Gini={igG:.3f}")

# ---- closeup: curves + tree ----
fig=plt.figure(figsize=(9.6,4.3)); fig.patch.set_facecolor(NAVY)
ax1=fig.add_axes([0.07,0.13,0.50,0.78]); draw_curves(ax1,p1)
ax2=fig.add_axes([0.60,0.05,0.38,0.90]); draw_tree(ax2,p1,leftP1,rightP1,leftN,rightN,igG)
closeup=os.path.join(figlib.outdir(SLUG),"charts-closeup.png")
figlib.save_fig(fig,closeup,dpi=130); print("  closeup ->",closeup)

# ---- cover ----
figc=plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.13,0.15,0.83,0.80]); draw_curves(axc,p1)
axc.set_title(None)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"決定木の不純度","Gini・Entropy・誤分類率","情報利得 IG で分割の良し悪しを測る",cc)
os.remove(cc)

# ---- gif: sweep parent p1, markers move along curves ----
frames=[]
ps=list(np.linspace(0.5,0.02,8))+list(np.linspace(0.02,0.98,14))+list(np.linspace(0.98,0.5,8))
for pv in ps:
    f2=plt.figure(figsize=(5.3,3.4)); f2.patch.set_facecolor(NAVY)
    a=f2.add_axes([0.13,0.15,0.83,0.76]); draw_curves(a,pv)
    a.set_title(f"p1={pv:.2f}   Gini={gini(pv):.3f}  Entropy={entropy(np.array([pv]))[0]:.3f}",
                color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2,dpi=88))
figlib.save_gif(frames,SLUG,duration=130)
print("done.")
