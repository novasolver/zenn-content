# -*- coding: utf-8 -*-
"""foucault-pendulum visuals: precession rosette + dtheta(t) curves + gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG="foucault-pendulum"
NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; CY="#00B4D8"
SID=86164.1; OE=2*math.pi/SID
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# closeup: rosette (left) + dtheta(t) curves (right)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
axp=fig.add_axes([0.03,0.06,0.42,0.88]); axp.set_facecolor(NAVY); axp.set_aspect("equal"); axp.axis("off")
axp.add_patch(plt.Circle((0,0),1,fill=False,ec="#3b4a6b"))
lat=35.0; om=OE*math.sin(math.radians(lat))
# show several swing axes precessing (compress time visually)
for i,frac in enumerate(np.linspace(0,1,9)):
    dth=-frac*math.radians(70)  # CW north
    x=math.sin(dth); y=math.cos(dth)
    c=plt.cm.autumn(frac*0.8)
    axp.plot([-x,x],[-y,y],color=c,lw=1.8,alpha=0.85)
axp.text(0,1.12,"N",color=CY,ha="center",fontsize=9); axp.text(0,-1.2,"S",color=CY,ha="center",fontsize=9)
axp.text(1.12,0,"E",color=CY,fontsize=9); axp.text(-1.2,0,"W",color=CY,fontsize=9)
axp.set_xlim(-1.3,1.3); axp.set_ylim(-1.35,1.3)
axp.set_title("振動面が時計回りに歳差(北半球)",color="white",fontsize=10)
axc=fig.add_axes([0.57,0.16,0.40,0.72]); style(axc)
t=np.linspace(0,36,200)
for la,c,lab in [(0,GREEN,"赤道 0deg"),(35,CY,"東京 35deg"),(90,ORANGE,"極 90deg")]:
    o=OE*math.sin(math.radians(la)); axc.plot(t,np.degrees(o)*3600*t,color=c,lw=2,label=lab)
axc.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
axc.set_xlabel("経過時間 [h]",color="white",fontsize=9); axc.set_ylabel("歳差角 dtheta [deg]",color="white",fontsize=9)
axc.set_title("緯度が高いほど速く回る",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
ax2=figc.add_axes([0,0,1,1]); ax2.set_facecolor(NAVY); ax2.set_aspect("equal"); ax2.axis("off")
ax2.add_patch(plt.Circle((0,0),1,fill=False,ec="#3b4a6b"))
for frac in np.linspace(0,1,11):
    dth=-frac*math.radians(80); x=math.sin(dth); y=math.cos(dth)
    ax2.plot([-x,x],[-y,y],color=plt.cm.autumn(frac*0.8),lw=1.6)
ax2.set_xlim(-1.2,1.2); ax2.set_ylim(-1.2,1.2)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"フーコーの振り子","","歳差 = Omega_earth sin(緯度)、東京で約41.7時間/回転",cc); os.remove(cc)

# gif: oscillation axis rotating (compass view)
frames=[]; N=44
for kf in range(N):
    dth=-2*math.pi*kf/N   # full visual rotation
    x=math.sin(dth); y=math.cos(dth)
    f=plt.figure(figsize=(4.4,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0,0,1,1]); a.set_facecolor(NAVY); a.set_aspect("equal"); a.axis("off")
    a.add_patch(plt.Circle((0,0),1,fill=False,ec="#3b4a6b"))
    a.plot([-x,x],[-y,y],color=CY,lw=2.6)
    a.add_patch(plt.Circle((x,y),0.07,color=ORANGE))
    a.set_xlim(-1.25,1.25); a.set_ylim(-1.25,1.3)
    a.text(0,1.12,"振動面の歳差（上から見た床）",color="white",ha="center",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=90)
print("done")
