# -*- coding: utf-8 -*-
"""gyroscope visuals: precession-rate vs rpm + vector schematic + precession gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="gyroscope"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; YEL="#ffd24b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
m=0.5; r=0.10; d=0.10; g=9.81; I=0.5*m*r*r
def Op(rpm): return m*g*d/(I*(rpm*2*math.pi/60))
# closeup: left precession vs rpm, right vector schematic
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.15,0.42,0.74]); style(ax)
rp=np.linspace(500,10000,300); ax.plot(rp,[Op(x) for x in rp],color=ORANGE,lw=2.2)
ax.plot(3000,Op(3000),"o",color=BLUE); ax.annotate(f"3000rpm: {Op(3000):.3f} rad/s",(3000,Op(3000)),(3200,Op(3000)+0.5),color="white",fontsize=8)
ax.set_xlabel("スピン回転数 [rpm]",color="white",fontsize=9); ax.set_ylabel("歳差速度 Omega_p [rad/s]",color="white",fontsize=9)
ax.set_title("速く回すほど歳差は遅い (Op ~ 1/omega)",color="white",fontsize=10)
ax2=fig.add_axes([0.56,0.08,0.40,0.84]); style(ax2); ax2.set_aspect("equal"); ax2.axis("off")
ax2.set_xlim(-1.2,1.2); ax2.set_ylim(-1.1,1.2)
# spin axis (horizontal), L green, tau orange down, Omega_p yellow arc
ax2.annotate("",xy=(0.9,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=2.5))
ax2.text(0.95,0.05,"L",color=GREEN,fontsize=11)
ax2.annotate("",xy=(0.9,-0.5),xytext=(0.9,0),arrowprops=dict(arrowstyle="-|>",color=ORANGE,lw=2.5))
ax2.text(0.95,-0.4,"tau=mgd",color=ORANGE,fontsize=9)
ax2.add_patch(plt.matplotlib.patches.Arc((0,0),1.4,1.4,angle=0,theta1=-30,theta2=30,color=YEL,lw=2.2))
ax2.text(0.78,0.55,"Omega_p",color=YEL,fontsize=9)
ax2.add_patch(plt.Circle((0,0),0.06,color="#9fb2d6"))
from matplotlib.patches import Ellipse
ax2.add_patch(Ellipse((0.9,0),0.12,0.5,color=BLUE,alpha=0.85))
ax2.set_title("L・トルク・歳差の関係",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.18,0.80,0.74]); style(axc)
axc.plot(rp,[Op(x) for x in rp],color=ORANGE,lw=2.4); axc.plot(3000,Op(3000),"o",color=BLUE)
axc.set_xlabel("rpm",color="white",fontsize=9); axc.set_ylabel("Omega_p [rad/s]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ジャイロスコープの","歳差運動","Omega_p = mgd/(I omega)、速いほど遅く回る",cc); os.remove(cc)
# gif: spin axis precessing around vertical (top-down cone view)
frames=[]; N=44
for kf in range(N):
    ph=2*math.pi*kf/N
    f=plt.figure(figsize=(4.4,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0,0,1,1]); a.set_facecolor(NAVY); a.set_aspect("equal"); a.axis("off")
    a.set_xlim(-1.2,1.2); a.set_ylim(-1.2,1.3)
    a.add_patch(plt.Circle((0,0),0.95,fill=False,ec="#3b4a6b",ls="--"))
    x=0.8*math.cos(ph); y=0.8*math.sin(ph)
    a.annotate("",xy=(x,y),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=2.5))
    a.add_patch(Ellipse((x,y),0.16,0.4,angle=math.degrees(ph)+90,color=BLUE,alpha=0.85))
    a.plot(0,0,"o",color="#9fb2d6")
    a.text(0,1.12,"角運動量Lが鉛直軸まわりに歳差",color="white",ha="center",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=90); print("done")
