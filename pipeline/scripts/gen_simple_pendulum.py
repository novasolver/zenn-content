# -*- coding: utf-8 -*-
"""simple-pendulum visuals: amplitude-period curve + swinging gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import ellipk
import figlib

SLUG = "simple-pendulum"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"

def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# amplitude vs period ratio (exact / linear)
th = np.linspace(1, 170, 400)
k = np.sin(np.radians(th)/2)
ratio = (4/(2*np.pi))*ellipk(k*k)   # T/T0

# closeup
fig = plt.figure(figsize=(9.2, 4.2)); fig.patch.set_facecolor(NAVY)
ax = fig.add_axes([0.08, 0.14, 0.52, 0.76]); style(ax)
ax.plot(th, ratio, color=ORANGE, lw=2.2)
ax.axhline(1, color="#3b4a6b", ls="--", lw=1)
for a in (30,120):
    r=(4/(2*np.pi))*ellipk(np.sin(math.radians(a)/2)**2)
    ax.plot(a, r, "o", color=BLUE); ax.annotate(f"{a}deg: x{r:.3f}", (a,r), (a-55,r+0.04), color="white", fontsize=8)
ax.set_xlabel("初期角度 theta0 [deg]", color="white", fontsize=9)
ax.set_ylabel("周期比 T / T0", color="white", fontsize=9)
ax.set_title("振幅が大きいほど周期は伸びる（非線形）", color="white", fontsize=10)
# right: pendulum schematic at two angles
ax2 = fig.add_axes([0.66, 0.10, 0.31, 0.82]); style(ax2)
ax2.set_xlim(-1.2,1.2); ax2.set_ylim(-1.25,0.25); ax2.set_aspect("equal"); ax2.set_xticks([]); ax2.set_yticks([])
for a,c,lab in [(30,BLUE,"30deg"),(120,ORANGE,"120deg")]:
    x=math.sin(math.radians(a)); y=-math.cos(math.radians(a))
    ax2.plot([0,x],[0,y], color=c, lw=2)
    ax2.add_patch(plt.Circle((x,y),0.08,color=c))
ax2.plot(0,0,"o",color="white")
ax2.set_title("L=1m, g=9.81", color="white", fontsize=9)
cu = os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig, cu, dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.4,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.18,0.80,0.74]); style(axc)
axc.plot(th, ratio, color=ORANGE, lw=2.4); axc.axhline(1,color="#3b4a6b",ls="--",lw=1)
axc.set_xlabel("theta0 [deg]",color="white",fontsize=9); axc.set_ylabel("T/T0",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"単振り子と単振動","","周期 T=2pi sqrt(L/g)、大振幅で伸びる周期",cc); os.remove(cc)

# gif: two pendulums swinging (small vs large amplitude), RK4
def sim(th0,g=9.81,L=1.0,dt=0.01,n=240):
    th=math.radians(th0); om=0; out=[]
    for _ in range(n):
        def d(t,o): return o, -(g/L)*math.sin(t)
        k1=d(th,om); k2=d(th+dt/2*k1[0],om+dt/2*k1[1]); k3=d(th+dt/2*k2[0],om+dt/2*k2[1]); k4=d(th+dt*k3[0],om+dt*k3[1])
        th+=dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); om+=dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]); out.append(th)
    return out
A=sim(20); B=sim(120)
frames=[]
for i in range(0,240,4):
    f=plt.figure(figsize=(5.0,2.8)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0,0,1,1]); a.set_facecolor(NAVY); a.set_xlim(-1.3,1.3); a.set_ylim(-1.25,0.35); a.set_aspect("equal"); a.axis("off")
    for th,c,lab in [(A[i],BLUE,"20deg"),(B[i],ORANGE,"120deg")]:
        x=math.sin(th); y=-math.cos(th)
        a.plot([0,x],[0,y],color=c,lw=2.2); a.add_patch(plt.Circle((x,y),0.085,color=c))
    a.plot(0,0,"o",color="white")
    a.text(0,0.22,"小振幅(青)は周期が短い / 大振幅(橙)は遅い",color="white",ha="center",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=70)
print("done")
