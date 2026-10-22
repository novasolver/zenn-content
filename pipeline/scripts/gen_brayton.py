# -*- coding: utf-8 -*-
"""brayton-cycle visuals: T-s diagram + eta(rp) + T-s marker gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="brayton-cycle"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#2ecc71"; YEL="#ffd24b"; GRY="#8fb8e0"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
cp=1.005; rp=12.0; g=1.4; T1=290.0; T3=1500.0
ex=(g-1)/g; rpex=rp**ex; T2=T1*rpex; T4=T3/rpex; eta=1-1/rpex
s3=cp*math.log(T3/T2)
# path points on T-s
def isobar(Tb,Te,soff,n=60):
    T=np.linspace(Tb,Te,n); s=soff+cp*np.log(T/Tb); return s,T
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.14,0.40,0.76]); style(ax)
# 1->2 vertical at s=0
ax.plot([0,0],[T1,T2],color=BLUE,lw=2.3)
s23,T23=isobar(T2,T3,0); ax.plot(s23,T23,color=ORANGE,lw=2.3)   # 2->3 heat at P2
ax.plot([s3,s3],[T3,T4],color=GREEN,lw=2.3)                     # 3->4
s41,T41=isobar(T4,T1,s3); ax.plot(s41,T41,color=GRY,lw=2.3)     # 4->1 cool at P1
for s,T,n in [(0,T1,"1"),(0,T2,"2"),(s3,T3,"3"),(s3,T4,"4")]:
    ax.plot(s,T,"o",color=YEL,ms=5); ax.annotate(n,(s,T),(s+0.02,T+20),color="white",fontsize=9)
ax.set_xlabel("エントロピー s [kJ/kg/K] (s1=0)",color="white",fontsize=9); ax.set_ylabel("温度 T [K]",color="white",fontsize=9)
ax.set_title("ブレイトンサイクルのT-s線図",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
rr=np.linspace(4,50,200); ax2.plot(rr,1-1/rr**ex,color=BLUE,lw=2.3)
ax2.plot(rp,eta,"o",color=ORANGE); ax2.annotate(f"rp=12: {eta*100:.1f}%",(rp,eta),(rp+2,0.35),color="white",fontsize=8)
ax2.set_xlabel("圧力比 rp",color="white",fontsize=9); ax2.set_ylabel("熱効率 eta",color="white",fontsize=9)
ax2.set_title("eta = 1 - 1/rp^((g-1)/g)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.16,0.80,0.78]); style(axc)
axc.plot([0,0],[T1,T2],color=BLUE,lw=2.4); axc.plot(s23,T23,color=ORANGE,lw=2.4)
axc.plot([s3,s3],[T3,T4],color=GREEN,lw=2.4); axc.plot(s41,T41,color=GRY,lw=2.4)
axc.set_xlabel("s",color="white",fontsize=9); axc.set_ylabel("T [K]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ブレイトンサイクル","","ガスタービンの基本、圧力比で効率が決まる",cc); os.remove(cc)
# gif: marker on T-s loop
sp=np.concatenate([[0,0],s23,[s3,s3],s41]); Tp=np.concatenate([[T1,T2],T23,[T3,T4],T41])
frames=[]; N=44; Ln=len(sp)
for kf in range(N):
    j=int(Ln*kf/N)
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.15,0.14,0.81,0.80]); style(a)
    a.plot([0,0],[T1,T2],color=BLUE,lw=1.8); a.plot(s23,T23,color=ORANGE,lw=1.8)
    a.plot([s3,s3],[T3,T4],color=GREEN,lw=1.8); a.plot(s41,T41,color=GRY,lw=1.8)
    a.plot(sp[j],Tp[j],"o",color="white",ms=9)
    a.set_xlabel("s",color="white",fontsize=9); a.set_ylabel("T [K]",color="white",fontsize=9)
    a.set_title("T-s上を一周",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=85); print("done")
