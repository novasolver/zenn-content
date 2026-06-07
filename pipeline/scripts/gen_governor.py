# -*- coding: utf-8 -*-
"""centrifugal-governor visuals: angle&radius vs rpm + fly-ball gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="centrifugal-governor"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#e17055"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
m=1.5; M=4.0; L=0.20; g=9.81
def state(rpm):
    om=2*math.pi*rpm/60; h=((m+M)/m)*(g/om/om)
    th=0.0 if h>=L else math.acos(h/L); r=L*math.sin(th)
    return th, r
lift=math.sqrt((m+M)/m*g/L)*60/2/math.pi
# closeup: theta & radius vs rpm
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.15,0.40,0.74]); style(ax)
rp=np.linspace(50,600,300); ax.plot(rp,[math.degrees(state(x)[0]) for x in rp],color=BLUE,lw=2.2)
ax.plot(200,math.degrees(state(200)[0]),"o",color=ORANGE); ax.annotate("200rpm: 65.8deg",(200,65.8),(230,40),color="white",fontsize=8)
ax.axvline(lift,color=RED,ls="--",lw=1); ax.text(lift+5,5,f"動作開始 {lift:.0f}rpm",color=RED,fontsize=8)
ax.set_xlabel("回転数 [rpm]",color="white",fontsize=9); ax.set_ylabel("アーム角 theta [deg]",color="white",fontsize=9)
ax.set_title("回転が上がるとボールが開く",color="white",fontsize=10)
ax2=fig.add_axes([0.58,0.15,0.39,0.74]); style(ax2)
ax2.plot(rp,[state(x)[1]*1000 for x in rp],color=GREEN,lw=2.2)
ax2.plot(200,state(200)[1]*1000,"o",color=ORANGE)
ax2.set_xlabel("回転数 [rpm]",color="white",fontsize=9); ax2.set_ylabel("ボール回転半径 [mm]",color="white",fontsize=9)
ax2.set_title("半径も回転数とともに拡大",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
# cover: governor schematic
def draw_gov(ax,rpm):
    th,r=state(rpm); ax.set_facecolor(NAVY); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-0.3,0.3); ax.set_ylim(-0.32,0.12)
    ax.plot([0,0],[0.08,-0.30],color="#9fb2d6",lw=4)  # spindle
    for sgn in (-1,1):
        bx=sgn*L*math.sin(th); by=0.08-L*math.cos(th)
        ax.plot([0,bx],[0.08,by],color=BLUE,lw=3)
        ax.add_patch(plt.Circle((bx,by),0.028,color=RED))
        sy=0.08-2*L*math.cos(th)*0.5-0.02
        ax.plot([bx,0],[by,sy],color=ORANGE,lw=2)
    ax.add_patch(plt.matplotlib.patches.Rectangle((-0.05,sy-0.02),0.10,0.03,color="#9fb2d6"))
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0,0,1,1]); draw_gov(axc,260)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"遠心調速機","(ガバナー)","回転数で開くフライボール、cos theta = (m+M)/m * g/(L omega^2)",cc); os.remove(cc)
# gif: rpm sweep raising balls
frames=[]; rpms=list(np.linspace(130,500,30))+list(np.linspace(500,130,14))
for rpm in rpms:
    f=plt.figure(figsize=(4.4,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0,0,1,1]); draw_gov(a,rpm)
    a.text(0,0.10,f"{rpm:.0f} rpm",color="white",ha="center",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=80); print("done")
