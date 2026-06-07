# -*- coding: utf-8 -*-
"""escape-velocity visuals: bar chart (log) + launch trajectories gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG="escape-velocity"
NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
G=6.674e-11; c=2.998e8; Me=5.972e24; Re=6.371e6
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
bodies=[("月",0.0123,0.2727),("火星",0.107,0.532),("地球",1,1),("木星",317.8,11.21),("太陽",333000,109.2),("中性子星",466200,0.00157)]
ve=[math.sqrt(2*G*(m*Me)/(r*Re))/1000 for _,m,r in bodies]
names=[b[0] for b in bodies]

# closeup bar chart (log)
fig=plt.figure(figsize=(9.0,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.16,0.86,0.74]); style(ax)
cols=[BLUE]*5+[ORANGE]
ax.bar(names,ve,color=cols,edgecolor="white",linewidth=0.5)
ax.set_yscale("log"); ax.set_ylabel("脱出速度 [km/s] (対数)",color="white",fontsize=9)
for i,v in enumerate(ve):
    lab=f"{v:.1f}" if v<1000 else f"{v:.2e}"
    ax.text(i,v*1.15,lab,color="white",ha="center",fontsize=8)
ax.set_title("ve = sqrt(2GM/R) — 質量と半径で決まる",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.14,0.16,0.82,0.76]); style(axc)
axc.bar(names,ve,color=cols); axc.set_yscale("log"); axc.tick_params(labelsize=7)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"脱出速度と","重力井戸","地球 11.2 km/s、太陽 617 km/s",cc); os.remove(cc)

# gif: projectile launched at increasing speed from Earth surface (2D gravity)
GM=G*Me; R=Re
def traj(v0):
    # launch straight up; integrate r(t)
    r=R; vr=v0; dt=2.0; xs=[]; t=0
    for _ in range(900):
        a=-GM/r/r; vr+=a*dt; r+=vr*dt;
        if r<R: r=R; break
        xs.append(r/R); t+=dt
        if r/R>9: break
    return xs
vesc=math.sqrt(2*GM/R)
speeds=[0.6,0.8,0.95,1.0,1.05]
trajs=[traj(s*vesc) for s in speeds]
cols2=[BLUE,"#60a5fa",ORANGE,GREEN,"#f43f5e"]
maxlen=max(len(t) for t in trajs)
frames=[]
for k in range(0,maxlen,6):
    f=plt.figure(figsize=(5.0,2.9)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.12,0.14,0.84,0.78]); style(a)
    a.add_patch(plt.Rectangle((-0.5,0),len(speeds),1,color="#2563eb",alpha=0.5))
    for i,(tr,sp,c) in enumerate(zip(trajs,speeds,cols2)):
        h=tr[min(k,len(tr)-1)] if tr else 1
        a.plot(i,h,"o",color=c,ms=10)
        a.text(i,-0.6,f"{sp:.2f}ve",color=c,ha="center",fontsize=8)
    a.set_ylim(-1.0,9); a.set_xlim(-0.6,len(speeds)-0.4); a.set_xticks([])
    a.set_ylabel("高度 r / R_earth",color="white",fontsize=9)
    a.set_title("ve未満は落下、ve以上は脱出",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=80)
print("done")
