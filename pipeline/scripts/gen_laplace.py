# -*- coding: utf-8 -*-
"""laplace-transform visuals: s-plane poles + time response + pole-move gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="laplace-transform"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#e17055"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
a,w=1.0,2.0
fig=plt.figure(figsize=(9.0,4.4)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.06,0.10,0.42,0.82]); style(ax); ax.set_aspect("equal")
ax.axvspan(-4,0,color=GREEN,alpha=0.08)
ax.axhline(0,color="#3b4a6b",lw=1); ax.axvline(0,color="#3b4a6b",lw=1.5)
ax.plot([-a,-a],[w,-w],"x",color=RED,ms=12,mew=2.5)
ax.text(-a+0.15,w,"-a+jω",color=RED,fontsize=8); ax.text(-a+0.15,-w-0.3,"-a-jω",color=RED,fontsize=8)
ax.text(-3.5,3.2,"左半面=安定",color=GREEN,fontsize=9)
ax.set_xlim(-4,1.5); ax.set_ylim(-3.5,3.5)
ax.set_xlabel("Re(s)=σ",color="white",fontsize=9); ax.set_ylabel("Im(s)=jω",color="white",fontsize=9)
ax.set_title("s平面: 減衰振動 e^(-at)sin(ωt) の極",color="white",fontsize=10)
ax2=fig.add_axes([0.58,0.16,0.39,0.74]); style(ax2)
t=np.linspace(0,6,300)
ax2.plot(t,np.exp(-a*t),color=BLUE,lw=2.2,label="e^(-at) (a=1)")
ax2.plot(t,np.exp(-a*t)*np.sin(w*t),color=ORANGE,lw=2,label="e^(-at)sin(2t)")
ax2.plot(t,np.exp(-a*t),color="#3b4a6b",lw=1,ls="--"); ax2.plot(t,-np.exp(-a*t),color="#3b4a6b",lw=1,ls="--")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("時間 t [s]",color="white",fontsize=9); ax2.set_ylabel("f(t)",color="white",fontsize=9)
ax2.set_title("時間応答: 極の実部=減衰率",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.0,0.04,1.0,0.9]); axc.set_facecolor(NAVY); axc.set_aspect("equal"); axc.axis("off")
axc.axvspan(-4,0,color=GREEN,alpha=0.1); axc.axhline(0,color="#3b4a6b",lw=1); axc.axvline(0,color="#3b4a6b",lw=1.5)
axc.plot([-a,-a],[w,-w],"x",color=RED,ms=14,mew=3); axc.set_xlim(-4,1.5); axc.set_ylim(-3.5,3.5)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ラプラス変換","とs平面","F(s)=∫f(t)e^(-st)dt、極の位置で応答が決まる",cc); os.remove(cc)
# gif: pole moving (a sweep) showing decay rate
frames=[]
for av in list(np.linspace(0.2,2.5,20))+list(np.linspace(2.5,0.2,8)):
    fr=plt.figure(figsize=(4.8,2.9)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.16,0.83,0.74]); style(g)
    g.plot(t,np.exp(-av*t)*np.sin(w*t),color=ORANGE,lw=2)
    g.plot(t,np.exp(-av*t),color="#3b4a6b",lw=1,ls="--"); g.plot(t,-np.exp(-av*t),color="#3b4a6b",lw=1,ls="--")
    g.set_ylim(-1.05,1.05); g.set_xlabel("t [s]",color="white",fontsize=9); g.set_ylabel("f(t)",color="white",fontsize=9)
    g.set_title(f"a={av:.1f} (極が左ほど速く減衰)",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
