# -*- coding: utf-8 -*-
"""nyquist-sampling visuals: signal+samples+alias + folding chart + fs-sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="nyquist-sampling"; NAVY="#0b1020"; ORANGE="#ff8c50"; YEL="#FFD166"; BLUE="#4ac6ff"; WHITE="#ffffff"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def alias(f,fs): return abs(f-round(f/fs)*fs)
f,fs,dur=600,1000,50
fa=alias(f,fs)
t=np.linspace(0,dur/1000,800)
fig=plt.figure(figsize=(9.2,4.4)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.07,0.57,0.88,0.34]); style(ax)
ax.plot(t*1000,np.sin(2*np.pi*f*t),color=ORANGE,lw=1.1,label=f"原信号 {f}Hz")
ax.plot(t*1000,np.sin(2*np.pi*fa*t),color=YEL,lw=2.4,label=f"見かけ {fa:.0f}Hz")
ts=np.arange(0,dur/1000,1/fs); ax.plot(ts*1000,np.sin(2*np.pi*f*ts),"o",color=WHITE,ms=4)
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=7,loc="upper right")
ax.set_xlabel("時間 [ms]",color="white",fontsize=8); ax.set_ylabel("振幅",color="white",fontsize=8)
ax.set_title(f"f={f}Hz を fs={fs}Hz で標本化→見かけ {fa:.0f}Hz に化ける",color="white",fontsize=10)
ax2=fig.add_axes([0.07,0.10,0.88,0.34]); style(ax2)
ff=np.linspace(0,5000,800); fal=[alias(x,fs) for x in ff]
ax2.plot(ff,fal,color=BLUE,lw=2); ax2.axhline(fs/2,color="#fb7185",ls="--",lw=1); ax2.text(3500,fs/2+30,"ナイキスト fs/2",color="#fb7185",fontsize=8)
ax2.plot(f,fa,"o",color=YEL,ms=8)
ax2.set_xlabel("信号周波数 f [Hz]",color="white",fontsize=8); ax2.set_ylabel("見かけ周波数 [Hz]",color="white",fontsize=8)
ax2.set_title("折り返し: f>fs/2 で見かけ周波数が折り返す",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.4,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.08,0.16,0.88,0.76]); style(axc)
axc.plot(t*1000,np.sin(2*np.pi*f*t),color=ORANGE,lw=1.1); axc.plot(t*1000,np.sin(2*np.pi*fa*t),color=YEL,lw=2.4)
axc.plot(ts*1000,np.sin(2*np.pi*f*ts),"o",color=WHITE,ms=4); axc.set_xlabel("時間 [ms]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"標本化定理と","エイリアシング","fs<2f で高周波が低周波に化ける",cc); os.remove(cc)
frames=[]
for fsv in list(np.linspace(400,2000,22))+list(np.linspace(2000,400,8)):
    fav=alias(f,fsv); tsv=np.arange(0,dur/1000,1/fsv)
    fr=plt.figure(figsize=(5.2,2.7)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.07,0.16,0.9,0.74]); style(g)
    g.plot(t*1000,np.sin(2*np.pi*f*t),color=ORANGE,lw=1.0)
    if fsv<2*f: g.plot(t*1000,np.sin(2*np.pi*fav*t),color=YEL,lw=2.2)
    g.plot(tsv*1000,np.sin(2*np.pi*f*tsv),"o",color=WHITE,ms=4)
    g.set_ylim(-1.2,1.2); g.set_xlabel("時間 [ms]",color="white",fontsize=9)
    ok = fsv>=2*f
    g.set_title(f"fs={fsv:.0f}Hz: {'正常(fs≥2f)' if ok else f'エイリアシング→{fav:.0f}Hz'}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
