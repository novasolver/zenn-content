# -*- coding: utf-8 -*-
"""hohmann-transfer visuals: transfer geometry + efficiency curve + gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG="hohmann-transfer"
NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"
mu=398600.0; R=6378.0
r1=R+400; r2=R+35800
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# closeup left: geometry, right: efficiency curve
fig=plt.figure(figsize=(9.4,4.3)); fig.patch.set_facecolor(NAVY)
axg=fig.add_axes([0.02,0.06,0.46,0.88]); axg.set_facecolor(NAVY); axg.set_aspect("equal"); axg.axis("off")
th=np.linspace(0,2*np.pi,300)
axg.plot(r1*np.cos(th),r1*np.sin(th),color=BLUE,lw=1.6)       # LEO
axg.plot(r2*np.cos(th),r2*np.sin(th),color=GREEN,lw=1.6)      # GEO
a_tx=(r1+r2)/2; e_tx=(r2-r1)/(r2+r1); b_tx=a_tx*math.sqrt(1-e_tx**2)
# transfer ellipse: focus at origin; perigee at +x (r1), apogee at -x (r2)
phi=np.linspace(0,np.pi,200); rt=a_tx*(1-e_tx*e_tx)/(1+e_tx*np.cos(phi))
axg.plot(rt*np.cos(phi),rt*np.sin(phi),color=ORANGE,ls="--",lw=1.8)
axg.add_patch(plt.Circle((0,0),R,color="#2563eb"))
axg.plot(r1,0,"o",color=RED); axg.text(r1+1500,-2500,"dv1",color=RED,fontsize=9)
axg.plot(-r2,0,"o",color=ORANGE); axg.text(-r2,2500,"dv2",color=ORANGE,fontsize=9)
axg.set_title("LEO(400km)->GEO(35800km) ホーマン遷移",color="white",fontsize=10)
m=r2*1.15; axg.set_xlim(-m,m); axg.set_ylim(-m*0.8,m*0.8)
axe=fig.add_axes([0.60,0.16,0.37,0.72]); style(axe)
Rs=np.linspace(1.01,100,4000)
d=np.sqrt(2*Rs/(1+Rs))-1+np.sqrt(1/Rs)*(1-np.sqrt(2/(1+Rs)))
axe.semilogx(Rs,d,color=BLUE,lw=2.2)
ip=np.argmax(d); axe.plot(Rs[ip],d[ip],"o",color=RED); axe.annotate(f"ピーク R*={Rs[ip]:.1f}",(Rs[ip],d[ip]),(2,0.50),color="white",fontsize=8)
cur=r2/r1; dc=np.sqrt(2*cur/(1+cur))-1+np.sqrt(1/cur)*(1-np.sqrt(2/(1+cur)))
axe.plot(cur,dc,"o",color=ORANGE); axe.annotate(f"LEO->GEO R={cur:.1f}",(cur,dc),(cur-3,dc-0.12),color="white",fontsize=8)
axe.set_xlabel("半径比 r2/r1",color="white",fontsize=9); axe.set_ylabel("合計 dv / v1(円)",color="white",fontsize=9)
axe.set_title("無次元 dv は R~15.6 で最大",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")

# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0,0,1,1]); axc.set_facecolor(NAVY); axc.set_aspect("equal"); axc.axis("off")
axc.plot(r1*np.cos(th),r1*np.sin(th),color=BLUE,lw=1.6); axc.plot(r2*np.cos(th),r2*np.sin(th),color=GREEN,lw=1.6)
axc.plot(rt*np.cos(phi),rt*np.sin(phi),color=ORANGE,ls="--",lw=2); axc.add_patch(plt.Circle((0,0),R,color="#2563eb"))
axc.set_xlim(-m,m); axc.set_ylim(-m*0.85,m*0.85)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ホーマン遷移軌道","","2回の噴射 dv1+dv2 で円軌道を乗り換える",cc); os.remove(cc)

# gif: spacecraft riding transfer ellipse from LEO to GEO
def kep(M,e):
    E=M
    for _ in range(40):
        E-= (E-e*math.sin(E)-M)/(1-e*math.cos(E))
    return E
frames=[]; N=42
for kf in range(N):
    frac=kf/(N-1); M=math.pi*frac  # half orbit perigee->apogee
    E=kep(M,e_tx); nu=2*math.atan2(math.sqrt(1+e_tx)*math.sin(E/2),math.sqrt(1-e_tx)*math.cos(E/2))
    rr=a_tx*(1-e_tx*e_tx)/(1+e_tx*math.cos(nu)); px=rr*math.cos(nu); py=rr*math.sin(nu)
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0,0,1,1]); aa.set_facecolor(NAVY); aa.set_aspect("equal"); aa.axis("off")
    aa.set_xlim(-m,m); aa.set_ylim(-m*0.78,m*0.78)
    aa.plot(r1*np.cos(th),r1*np.sin(th),color=BLUE,lw=1.3); aa.plot(r2*np.cos(th),r2*np.sin(th),color=GREEN,lw=1.3)
    aa.plot(rt*np.cos(phi),rt*np.sin(phi),color="#6b5a2b",ls="--",lw=1.2)
    aa.add_patch(plt.Circle((0,0),R,color="#2563eb"))
    aa.plot(px,py,"o",color=ORANGE,ms=9)
    aa.text(-m*0.95,m*0.66,"遷移楕円で乗り換え中",color="white",fontsize=9)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=90)
print("done")
