# -*- coding: utf-8 -*-
"""markov-chain visuals: P1(t) convergence + state diagram + evolution gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="markov-chain"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
p,q=0.30,0.40; pi1=q/(p+q); lam=1-p-q
def P1(t): return pi1+(1-pi1)*lam**t
t=np.arange(0,21)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.15,0.46,0.74]); style(ax)
ax.plot(t,[P1(tt) for tt in t],"o-",color=BLUE,lw=2,ms=4)
ax.axhline(pi1,color=ORANGE,ls="--",lw=1.4); ax.text(12,pi1+0.02,f"定常 pi1={pi1:.4f}",color=ORANGE,fontsize=8)
ax.set_xlabel("ステップ t",color="white",fontsize=9); ax.set_ylabel("状態1の確率 P1(t)",color="white",fontsize=9)
ax.set_title("初期[1,0]から定常分布へ指数収束",color="white",fontsize=10)
# state diagram
ax2=fig.add_axes([0.60,0.10,0.38,0.82]); ax2.set_facecolor(NAVY); ax2.axis("off"); ax2.set_xlim(0,1); ax2.set_ylim(0,1)
ax2.add_patch(plt.Circle((0.28,0.5),0.14,color=BLUE,alpha=0.5,ec="white")); ax2.text(0.28,0.5,"状態1",color="white",ha="center",va="center",fontsize=9)
ax2.add_patch(plt.Circle((0.72,0.5),0.14,color=ORANGE,alpha=0.5,ec="white")); ax2.text(0.72,0.5,"状態2",color="white",ha="center",va="center",fontsize=9)
ax2.annotate("",xy=(0.58,0.58),xytext=(0.42,0.58),arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=2))
ax2.text(0.5,0.63,"p=0.30",color=GREEN,ha="center",fontsize=8)
ax2.annotate("",xy=(0.42,0.42),xytext=(0.58,0.42),arrowprops=dict(arrowstyle="-|>",color=RED,lw=2))
ax2.text(0.5,0.34,"q=0.40",color=RED,ha="center",fontsize=8)
ax2.set_title("2状態遷移図",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.14,0.16,0.82,0.78]); style(axc); axc.plot(t,[P1(tt) for tt in t],"o-",color=BLUE,lw=2,ms=4); axc.axhline(pi1,color=ORANGE,ls="--",lw=1.4)
axc.set_xlabel("t",color="white",fontsize=9); axc.set_ylabel("P1(t)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"マルコフ連鎖","と定常分布","pi=piP、初期状態を忘れて定常へ",cc); os.remove(cc)
frames=[]
for T in list(range(0,16))+[15]*4:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.14,0.16,0.82,0.74]); style(aa)
    p1=P1(T); aa.bar(["状態1","状態2"],[p1,1-p1],color=[BLUE,ORANGE])
    aa.axhline(pi1,color=GREEN,ls="--",lw=1); aa.set_ylim(0,1)
    aa.set_ylabel("確率",color="white",fontsize=9)
    aa.set_title(f"t={T}: P1={p1:.3f} (定常 {pi1:.3f})",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=130); print("done")
