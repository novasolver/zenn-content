# -*- coding: utf-8 -*-
"""stefan-boltzmann visuals: Planck curves + power vs T(log) + Planck-grow gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="stefan-boltzmann"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#ff6b6b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
SIG=5.670374419e-8; h=6.62607015e-34; c=2.99792458e8; kB=1.380649e-23
def planck(lam,T):  # lam in m
    x=h*c/(lam*kB*T); x=np.minimum(x,700)
    return (2*h*c*c)/(lam**5*(np.exp(x)-1))
lam=np.linspace(0.1e-6,8e-6,500)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.11,0.15,0.40,0.74]); style(ax)
for T,c_ in [(800,RED),(1000,ORANGE),(1500,GREEN)]:
    ax.plot(lam*1e6,planck(lam,T)/1e9,color=c_,lw=2.0,label=f"{T}K (lam_max={2898/T:.2f}um)")
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=7)
ax.set_xlabel("波長 lambda [um]",color="white",fontsize=9); ax.set_ylabel("分光放射輝度 [GW/m2/sr/m]",color="white",fontsize=8)
ax.set_title("プランク曲線：高温ほど短波長へ(Wien)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.15,0.37,0.74]); style(ax2)
T=np.linspace(100,6000,200); ax2.semilogy(T,SIG*T**4,color=BLUE,lw=2.3)
ax2.plot(1000,SIG*1000**4,"o",color=ORANGE); ax2.annotate("1000K: 56.7kW/m2",(1000,SIG*1000**4),(1300,1e3),color="white",fontsize=8)
ax2.set_xlabel("温度 T [K]",color="white",fontsize=9); ax2.set_ylabel("放射発散度 E [W/m2] (対数)",color="white",fontsize=8)
ax2.set_title("E = sigma T^4 (T2倍で16倍)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.14,0.16,0.82,0.78]); style(axc)
for T_,c_ in [(800,RED),(1000,ORANGE),(1500,GREEN)]: axc.plot(lam*1e6,planck(lam,T_)/1e9,color=c_,lw=2.2)
axc.set_xlabel("lambda [um]",color="white",fontsize=9); axc.set_ylabel("B_lambda",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"シュテファン","ボルツマンの法則","E=sigma T^4、温度の4乗で放射が増える",cc); os.remove(cc)
frames=[]; Ts=list(np.linspace(600,2000,30))+list(np.linspace(2000,600,12))
for T_ in Ts:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.15,0.15,0.81,0.78]); style(aa)
    aa.plot(lam*1e6,planck(lam,T_)/1e9,color=ORANGE,lw=2.3); aa.fill_between(lam*1e6,planck(lam,T_)/1e9,color=ORANGE,alpha=0.12)
    aa.axvline(2898/T_,color=BLUE,ls="--",lw=1.2)
    aa.set_ylim(0,planck(lam,2000).max()/1e9*1.05)
    aa.set_xlabel("lambda [um]",color="white",fontsize=9); aa.set_ylabel("B_lambda [GW]",color="white",fontsize=8)
    aa.set_title(f"T={T_:.0f}K, lam_max={2898/T_:.2f}um",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
