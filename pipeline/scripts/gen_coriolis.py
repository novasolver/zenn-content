# -*- coding: utf-8 -*-
"""coriolis-effect visuals: inertial vs rotating frame paths + gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG="coriolis-effect"
NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def sim(omega=1.4,speed=1.0,angle=0,sign=1,tmax=2.2,dt=0.002):
    rad=math.radians(angle); ivx=speed*math.cos(rad); ivy=speed*math.sin(rad)
    ix=iy=0; fa=0; I=[]; Rp=[]
    n=int(tmax/dt)
    for _ in range(n):
        ix+=ivx*dt; iy+=ivy*dt; fa+=omega*dt
        ct=math.cos(-sign*fa); st=math.sin(-sign*fa)
        I.append((ix,iy)); Rp.append((ix*ct-iy*st, ix*st+iy*ct))
    return np.array(I), np.array(Rp)

I,Rn=sim(sign=1); _,Rs=sim(sign=-1)

# closeup: 2 panels
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
axi=fig.add_axes([0.05,0.12,0.42,0.78]); style(axi); axi.set_aspect("equal")
axi.plot(I[:,0],I[:,1],color=GREEN,lw=2.2)
axi.plot(0,0,"o",color="white"); axi.set_title("慣性系：まっすぐ進む",color="white",fontsize=10)
axi.set_xlabel("x",color="white",fontsize=8)
axr=fig.add_axes([0.55,0.12,0.42,0.78]); style(axr); axr.set_aspect("equal")
axr.plot(Rn[:,0],Rn[:,1],color=ORANGE,lw=2.2,label="北半球(右へ)")
axr.plot(Rs[:,0],Rs[:,1],color=BLUE,lw=2.2,label="南半球(左へ)")
axr.plot(0,0,"o",color="white")
axr.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8,loc="lower left")
axr.set_title("回転系：見かけの力で曲がる",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0,0,1,1]); axc.set_facecolor(NAVY); axc.set_aspect("equal"); axc.axis("off")
axc.plot(Rn[:,0],Rn[:,1],color=ORANGE,lw=2.4); axc.plot(Rs[:,0],Rs[:,1],color=BLUE,lw=2.4); axc.plot(0,0,"o",color="white")
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"コリオリの力と","回転系","a_Cor = -2 Omega x v、北半球で右に偏向",cc); os.remove(cc)

# gif: particle moving, rotating-frame path drawing
frames=[]; N=44
for kf in range(1,N+1):
    j=int(len(Rn)*kf/N)
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.02,0.02,0.96,0.9]); a.set_facecolor(NAVY); a.set_aspect("equal"); a.axis("off")
    mx=max(np.abs(Rn).max(),0.1)*1.1; a.set_xlim(-mx,mx); a.set_ylim(-mx,mx)
    a.plot(Rn[:j,0],Rn[:j,1],color=ORANGE,lw=2.2)
    a.plot(Rn[j-1,0],Rn[j-1,1],"o",color="white",ms=8)
    a.plot(0,0,"o",color=BLUE)
    a.text(0,mx*0.86,"回転系で見た軌跡（北半球）",color="white",ha="center",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=80)
print("done")
