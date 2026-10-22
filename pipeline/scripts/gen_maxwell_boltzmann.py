# -*- coding: utf-8 -*-
"""maxwell-boltzmann visuals: f(v) with characteristic speeds + T comparison + broadening gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="maxwell-boltzmann"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#5cd6a8"; RED="#ff6b6b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
kB=1.380649e-23; NA=6.02214076e23
def fMB(v,Mg,T):
    m=Mg*1e-3/NA; a=m/(2*math.pi*kB*T)
    return 4*math.pi*a**1.5*v*v*np.exp(-m*v*v/(2*kB*T))
def speeds(Mg,T):
    m=Mg*1e-3/NA; return math.sqrt(2*kB*T/m),math.sqrt(8*kB*T/(math.pi*m)),math.sqrt(3*kB*T/m)
v=np.linspace(1,1600,500); Mg=28; T=300
vp,vm,vr=speeds(Mg,T)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.15,0.42,0.74]); style(ax)
ax.plot(v,fMB(v,Mg,T),color=BLUE,lw=2.3)
pk=fMB(vp,Mg,T)
for val,c in [(vp,BLUE),(vm,GREEN),(vr,ORANGE)]:
    ax.axvline(val,color=c,ls="--",lw=1.4)
ax.text(680,pk*0.92,f"vp = {vp:.0f} m/s",color=BLUE,fontsize=9)
ax.text(680,pk*0.80,f"v_mean = {vm:.0f} m/s",color=GREEN,fontsize=9)
ax.text(680,pk*0.68,f"v_rms = {vr:.0f} m/s",color=ORANGE,fontsize=9)
ax.set_xlabel("速さ v [m/s]",color="white",fontsize=9); ax.set_ylabel("確率密度 f(v)",color="white",fontsize=9)
ax.set_title("N2 300K: vp<v_mean<v_rms (1:1.13:1.22)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.15,0.37,0.74]); style(ax2)
for Tt,c in [(150,GREEN),(300,BLUE),(600,RED)]:
    ax2.plot(v,fMB(v,Mg,Tt),color=c,lw=2.0,label=f"{Tt}K")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("速さ v [m/s]",color="white",fontsize=9); ax2.set_ylabel("f(v)",color="white",fontsize=9)
ax2.set_title("高温ほど分布は広く・低く",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.14,0.16,0.82,0.78]); style(axc)
for Tt,c in [(150,GREEN),(300,BLUE),(600,RED)]: axc.plot(v,fMB(v,Mg,Tt),color=c,lw=2.2)
axc.set_xlabel("v [m/s]",color="white",fontsize=9); axc.set_ylabel("f(v)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"マクスウェル","ボルツマン分布","気体分子の速さの分布、温度で広がる",cc); os.remove(cc)
frames=[]; Ts=list(np.linspace(100,800,30))+list(np.linspace(800,100,12))
for Tt in Ts:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.14,0.15,0.82,0.78]); style(aa)
    aa.plot(v,fMB(v,Mg,Tt),color=ORANGE,lw=2.3); aa.fill_between(v,fMB(v,Mg,Tt),color=ORANGE,alpha=0.12)
    aa.set_ylim(0,fMB(speeds(Mg,100)[0],Mg,100)*1.05)
    aa.set_xlabel("v [m/s]",color="white",fontsize=9); aa.set_ylabel("f(v)",color="white",fontsize=9)
    aa.set_title(f"N2 T={Tt:.0f}K",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
