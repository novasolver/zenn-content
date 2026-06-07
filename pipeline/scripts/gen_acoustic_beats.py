# -*- coding: utf-8 -*-
"""acoustic-beats visuals: composite waveform+envelope + spectrum + beat sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="acoustic-beats"; NAVY="#0b1020"; BLUE="#4ac6ff"; ORANGE="#ffaa50"; PINK="#ff8cc8"; YEL="#FFD166"; RED="#FF6B6B"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
# use lower freqs for visible carrier in plot, but state real 440/444 in article
f1,f2,A1,A2=20,24,0.5,0.5   # visualization freqs (beat=4Hz like 440/444 scaled)
t=np.linspace(0,1,4000)
y=A1*np.cos(2*np.pi*f1*t)+A2*np.cos(2*np.pi*f2*t)
env=np.sqrt(A1**2+A2**2+2*A1*A2*np.cos(2*np.pi*(f1-f2)*t))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.08,0.15,0.56,0.74]); style(ax)
ax.plot(t*1000,y,color=BLUE,lw=0.9); ax.plot(t*1000,env,color=ORANGE,ls="--",lw=1.6); ax.plot(t*1000,-env,color=ORANGE,ls="--",lw=1.6)
ax.set_xlabel("時間 [ms]",color="white",fontsize=9); ax.set_ylabel("合成波 y(t)",color="white",fontsize=9)
ax.set_title("うなり：包絡線が |f1-f2| で脈打つ (Tbeat=250ms)",color="white",fontsize=10)
ax2=fig.add_axes([0.71,0.15,0.26,0.74]); style(ax2)
ax2.vlines(440,0,A1,color=BLUE,lw=4); ax2.vlines(444,0,A2,color=PINK,lw=4)
ax2.set_xlim(435,449); ax2.set_ylim(0,0.65)
ax2.text(440,A1+0.03,"f1=440",color=BLUE,fontsize=8,ha="center"); ax2.text(444,A2+0.03,"f2=444",color=PINK,fontsize=8,ha="center")
ax2.set_xlabel("周波数 [Hz]",color="white",fontsize=9); ax2.set_title("スペクトル",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.4,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.06,0.16,0.9,0.76]); style(axc)
axc.plot(t*1000,y,color=BLUE,lw=0.9); axc.plot(t*1000,env,color=ORANGE,ls="--",lw=1.6); axc.plot(t*1000,-env,color=ORANGE,ls="--",lw=1.6)
axc.set_xlabel("時間 [ms]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"うなり(音のビート)","","2音の重ね合わせ、うなり周波数 = |f1-f2|",cc); os.remove(cc)
# gif: vary f2 -> beat rate changes
frames=[]; f2s=list(np.linspace(20,28,24))+list(np.linspace(28,20,12))
for f2v in f2s:
    yy=A1*np.cos(2*np.pi*f1*t)+A2*np.cos(2*np.pi*f2v*t)
    ev=np.sqrt(A1**2+A2**2+2*A1*A2*np.cos(2*np.pi*(f1-f2v)*t))
    f=plt.figure(figsize=(5.2,2.8)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.08,0.16,0.88,0.74]); style(aa)
    aa.plot(t*1000,yy,color=BLUE,lw=0.8); aa.plot(t*1000,ev,color=ORANGE,ls="--",lw=1.5); aa.plot(t*1000,-ev,color=ORANGE,ls="--",lw=1.5)
    beat=abs(f1-f2v)*22  # scaled label to 440-range analogue
    aa.set_xlabel("時間 [ms]",color="white",fontsize=9)
    aa.set_title(f"周波数差を変えるとうなりの速さが変化",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=95); print("done")
