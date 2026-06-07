# -*- coding: utf-8 -*-
"""orbital-mechanics visuals: ellipse + vis-viva curve + Kepler motion gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "orbital-mechanics"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"; RED="#fb7185"
MU=3.986e14; RE=6371e3
a_km, e = 20000.0, 0.30   # valid demo orbit (rp_alt ~ 7629 km)
a=a_km*1000

def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def solve_kepler(M,e):
    E=M
    for _ in range(50):
        dE=(M-E+e*math.sin(E))/(1-e*math.cos(E)); E+=dE
        if abs(dE)<1e-12: break
    return E

# closeup: orbit ellipse (left) + vis-viva (right)
fig=plt.figure(figsize=(9.4,4.3)); fig.patch.set_facecolor(NAVY)
axo=fig.add_axes([0.02,0.08,0.48,0.86]); style(axo); axo.set_aspect("equal"); axo.axis("off")
nu=np.linspace(0,2*np.pi,400); r=a*(1-e*e)/(1+e*np.cos(nu))
# focus at origin (Earth)
x=r*np.cos(nu); y=r*np.sin(nu)
axo.plot(x/1e6,y/1e6,color=BLUE,lw=1.8)
axo.add_patch(plt.Circle((0,0),RE/1e6,color="#2563eb"))
rp=a*(1-e); ra=a*(1+e)
axo.plot(rp/1e6,0,"o",color=RED); axo.text(rp/1e6,0.8,"近地点",color=RED,fontsize=8,ha="center")
axo.plot(-ra/1e6,0,"o",color=ORANGE); axo.text(-ra/1e6,0.8,"遠地点",color=ORANGE,fontsize=8,ha="center")
axo.set_title("楕円軌道 (a=20000km, e=0.30)",color="white",fontsize=10)
axr=fig.add_axes([0.60,0.16,0.37,0.72]); style(axr)
rr=np.linspace(rp,ra,300); v=np.sqrt(MU*(2/rr-1/a))/1000
axr.plot(rr/1e6,v,color=ORANGE,lw=2.2)
vp=math.sqrt(MU*(2/rp-1/a))/1000; va=math.sqrt(MU*(2/ra-1/a))/1000
axr.plot(rp/1e6,vp,"o",color=RED); axr.annotate(f"近地点 {vp:.2f}km/s",(rp/1e6,vp),(rp/1e6+1,vp-0.3),color="white",fontsize=8)
axr.plot(ra/1e6,va,"o",color=ORANGE); axr.annotate(f"遠地点 {va:.2f}km/s",(ra/1e6-9,va+0.2),color="white",fontsize=8)
axr.set_xlabel("中心からの距離 r [1000 km]",color="white",fontsize=9)
axr.set_ylabel("速度 v [km/s]",color="white",fontsize=9)
axr.set_title("vis-viva: v=sqrt(mu(2/r-1/a))",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0,0,1,1]); axc.set_facecolor(NAVY); axc.set_aspect("equal"); axc.axis("off")
axc.plot(x/1e6,y/1e6,color=BLUE,lw=2); axc.add_patch(plt.Circle((0,0),RE/1e6,color="#2563eb"))
axc.plot(rp/1e6,0,"o",color=RED); axc.plot(-ra/1e6,0,"o",color=ORANGE)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"軌道力学と","vis-viva方程式","ケプラー方程式 M=E-e sinE で軌道を解く",cc); os.remove(cc)

# gif: satellite along ellipse, faster at periapsis (equal area)
T=2*math.pi*math.sqrt(a**3/MU)
frames=[]
N=48
for kf in range(N):
    M=2*math.pi*kf/N; E=solve_kepler(M,e)
    nu_=2*math.atan2(math.sqrt(1+e)*math.sin(E/2),math.sqrt(1-e)*math.cos(E/2))
    rr=a*(1-e*e)/(1+e*math.cos(nu_)); px=rr*math.cos(nu_)/1e6; py=rr*math.sin(nu_)/1e6
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0,0,1,1]); aa.set_facecolor(NAVY); aa.set_aspect("equal"); aa.axis("off")
    aa.set_xlim(-2.7e1,1.5e1); aa.set_ylim(-1.6e1,1.6e1)
    aa.plot(x/1e6,y/1e6,color="#3b4a6b",lw=1.2)
    aa.add_patch(plt.Circle((0,0),RE/1e6,color="#2563eb"))
    aa.plot(px,py,"o",color=ORANGE,ms=9)
    aa.text(-26,14,"近地点で速く、遠地点で遅い",color="white",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=90)
print("done")
