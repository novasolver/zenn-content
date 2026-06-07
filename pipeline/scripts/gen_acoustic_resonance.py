# -*- coding: utf-8 -*-
"""acoustic-resonance visuals: standing waves in open/closed pipe + harmonic series + gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="acoustic-resonance"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
c=331.3*math.sqrt(293.15/273.15); L=0.6
x=np.linspace(0,1,300)
fig=plt.figure(figsize=(9.2,4.6)); fig.patch.set_facecolor(NAVY)
# open pipe modes
ax=fig.add_axes([0.07,0.57,0.42,0.36]); style(ax)
for n,col in [(1,BLUE),(2,ORANGE),(3,GREEN)]:
    ax.plot(x, np.sin(n*math.pi*x)+0, color=col, lw=2, label=f"n={n}: {n*c/(2*L):.0f}Hz")
    ax.plot(x,-np.sin(n*math.pi*x), color=col, lw=2, alpha=0.4)
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=7,loc="upper right")
ax.set_yticks([]); ax.set_title("開管: 両端が腹 f_n=n c/2L",color="white",fontsize=10); ax.set_xlabel("管に沿った位置",color="white",fontsize=8)
# closed pipe modes
axc=fig.add_axes([0.07,0.10,0.42,0.36]); style(axc)
for i,(col) in enumerate([BLUE,ORANGE,GREEN]):
    m=2*(i+1)-1
    axc.plot(x, np.sin(m*math.pi*x/2), color=col, lw=2, label=f"n={m}: {m*c/(4*L):.0f}Hz")
    axc.plot(x,-np.sin(m*math.pi*x/2), color=col, lw=2, alpha=0.4)
axc.axvline(1,color="#fb7185",lw=3)
axc.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=7,loc="upper left")
axc.set_yticks([]); axc.set_title("閉管: 一端閉(右,赤) 奇数倍音のみ f_n=(2n-1)c/4L",color="white",fontsize=9); axc.set_xlabel("位置",color="white",fontsize=8)
# harmonic frequencies bar
ax2=fig.add_axes([0.58,0.16,0.39,0.74]); style(ax2)
ns=np.arange(1,7)
ax2.bar(ns-0.18,[n*c/(2*L) for n in ns],width=0.36,color=BLUE,label="開管")
ax2.bar(ns+0.18,[(2*n-1)*c/(4*L) for n in ns],width=0.36,color=ORANGE,label="閉管")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("モード n",color="white",fontsize=9); ax2.set_ylabel("共鳴周波数 [Hz]",color="white",fontsize=9)
ax2.set_title("開管=全倍音, 閉管=奇数倍音",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc2=plt.figure(figsize=(5.2,3.0)); figc2.patch.set_facecolor(NAVY)
a=figc2.add_axes([0.05,0.1,0.9,0.82]); style(a); a.set_yticks([])
for n,col in [(1,BLUE),(2,ORANGE),(3,GREEN)]:
    a.plot(x,np.sin(n*math.pi*x),color=col,lw=2.2); a.plot(x,-np.sin(n*math.pi*x),color=col,lw=2.2,alpha=0.4)
a.set_xlabel("開管の定在波",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc2,cc,dpi=120)
figlib.make_cover(SLUG,"気柱の共鳴","","開管 n c/2L、閉管 (2n-1)c/4L で共鳴",cc); os.remove(cc)
# gif: standing wave oscillating + mode increasing
frames=[]
for n in [1,2,3,4]:
    for ph in np.linspace(0,2*math.pi,6,endpoint=False):
        fr=plt.figure(figsize=(5.0,2.6)); fr.patch.set_facecolor(NAVY)
        g=fr.add_axes([0.04,0.12,0.92,0.76]); style(g); g.set_yticks([]); g.set_ylim(-1.3,1.3)
        env=np.sin(n*math.pi*x); g.plot(x,env*math.cos(ph),color=BLUE,lw=2.4)
        g.plot(x,env,color="#3b4a6b",lw=1,ls="--"); g.plot(x,-env,color="#3b4a6b",lw=1,ls="--")
        g.set_title(f"開管 n={n}: {n*c/(2*L):.0f}Hz",color="white",fontsize=10)
        g.set_xlabel("位置",color="white",fontsize=8)
        frames.append(figlib.fig_to_pil(fr,dpi=88))
figlib.save_gif(frames,SLUG,duration=110); print("done")
