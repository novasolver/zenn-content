# -*- coding: utf-8 -*-
"""z-transform visuals: z-plane poles/zeros + freq response + pole-radius gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="z-transform"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#00b894"; RED="#e17055"; CY="#00B4D8"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
b=np.array([0.0675,0.135,0.0675]); a=np.array([1,-1.143,0.4128])
poles=np.roots(a); zeros=np.roots(b)
fig=plt.figure(figsize=(9.0,4.4)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.06,0.10,0.42,0.82]); style(ax); ax.set_aspect("equal")
th=np.linspace(0,2*np.pi,200); ax.plot(np.cos(th),np.sin(th),color=CY,ls="--",lw=1.4)
ax.axhline(0,color="#3b4a6b",lw=1); ax.axvline(0,color="#3b4a6b",lw=1)
ax.plot(poles.real,poles.imag,"x",color=RED,ms=11,mew=2.5,label="極 (|p|=0.64)")
ax.plot(zeros.real,zeros.imag,"o",color=GREEN,ms=9,mfc="none",mew=2,label="零点")
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8,loc="upper left")
ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.4,1.4)
ax.set_xlabel("Re(z)",color="white",fontsize=9); ax.set_ylabel("Im(z)",color="white",fontsize=9)
ax.set_title("z平面: 全極が単位円内→安定",color="white",fontsize=10)
ax2=fig.add_axes([0.58,0.16,0.39,0.74]); style(ax2)
w=np.linspace(0,np.pi,512); H=np.polyval(b,np.exp(-1j*w))/np.polyval(a,np.exp(-1j*w))
ax2.plot(w/np.pi,20*np.log10(np.abs(H)),color=BLUE,lw=2.2)
ax2.set_xlabel("正規化周波数 ω/π",color="white",fontsize=9); ax2.set_ylabel("ゲイン [dB]",color="white",fontsize=9)
ax2.set_title("周波数応答 H(e^jω): 低域通過IIR",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.0,0.04,1.0,0.9]); axc.set_facecolor(NAVY); axc.set_aspect("equal"); axc.axis("off")
axc.plot(np.cos(th),np.sin(th),color=CY,ls="--",lw=1.6); axc.axhline(0,color="#3b4a6b",lw=1); axc.axvline(0,color="#3b4a6b",lw=1)
axc.plot(poles.real,poles.imag,"x",color=RED,ms=13,mew=3); axc.plot(zeros.real,zeros.imag,"o",color=GREEN,ms=10,mfc="none",mew=2)
axc.set_xlim(-1.4,1.4); axc.set_ylim(-1.4,1.4)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"Z変換と","極零配置","単位円内なら安定、極零でフィルタを設計",cc); os.remove(cc)
# gif: move pole radius toward unit circle
frames=[]
for radius in list(np.linspace(0.4,1.05,22))+list(np.linspace(1.05,0.4,8)):
    ang=0.474  # angle of default pole
    p=radius*np.exp(1j*ang); ps=[p,p.conjugate()]
    fr=plt.figure(figsize=(4.4,3.2)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.04,0.06,0.92,0.86]); g.set_facecolor(NAVY); g.set_aspect("equal")
    style(g); g.plot(np.cos(th),np.sin(th),color=CY,ls="--",lw=1.4)
    g.axhline(0,color="#3b4a6b",lw=1); g.axvline(0,color="#3b4a6b",lw=1)
    col=RED if radius<1 else "#ff2d55"
    g.plot([z.real for z in ps],[z.imag for z in ps],"x",color=col,ms=12,mew=2.5)
    g.set_xlim(-1.4,1.4); g.set_ylim(-1.4,1.4)
    g.set_title(f"|p|={radius:.2f} → {'安定' if radius<1 else '不安定!'}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
