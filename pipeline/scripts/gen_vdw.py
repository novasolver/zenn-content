# -*- coding: utf-8 -*-
"""van-der-waals visuals: P-V isotherms + Z-P + isotherm sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="van-der-waals-gas"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; GRY="#8fb8e0"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
Rg=0.08206; a=1.35; b=0.039
Tc=8*a/(27*Rg*b); Pc=a/(27*b*b)
def vdwP(V,T): return Rg*T/(V-b)-a/V/V
def solveVm(P,T):
    V=Rg*T/P
    for _ in range(80):
        f=(P+a/V/V)*(V-b)-Rg*T; fp=(P+a/V/V)-(2*a/V**3)*(V-b)
        if abs(fp)<1e-14: break
        dV=f/fp; V-=dV
        if abs(dV)<1e-10: break
    return V
V=np.linspace(b*1.02,0.6,500)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.14,0.42,0.76]); style(ax)
for T,c in [(0.85*Tc,BLUE),(Tc,ORANGE),(1.3*Tc,GREEN)]:
    ax.plot(V,vdwP(V,T),color=c,lw=2.0,label=f"T={T:.0f}K")
ax.axhline(Pc,color="#3b4a6b",ls=":",lw=1); ax.plot(3*b,Pc,"o",color="white"); ax.annotate("臨界点",(3*b,Pc),(3*b+0.05,Pc+8),color="white",fontsize=8)
ax.set_ylim(-20,140); ax.set_xlabel("モル体積 V_m [L/mol]",color="white",fontsize=9); ax.set_ylabel("圧力 P [atm]",color="white",fontsize=9)
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax.set_title(f"P-V等温線 (N2: Tc={Tc:.0f}K, Pc={Pc:.0f}atm)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.15,0.37,0.74]); style(ax2)
Ps=np.linspace(1,200,120)
for T,c in [(300,BLUE),(150,ORANGE)]:
    Z=[P*solveVm(P,T)/(Rg*T) for P in Ps]; ax2.plot(Ps,Z,color=c,lw=2.0,label=f"T={T}K")
ax2.axhline(1,color=GRY,ls="--",lw=1)
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("圧力 P [atm]",color="white",fontsize=9); ax2.set_ylabel("圧縮率因子 Z=PV/RT",color="white",fontsize=9)
ax2.set_title("Z<1:引力支配 / Z>1:斥力支配",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.16,0.80,0.78]); style(axc)
for T,c in [(0.85*Tc,BLUE),(Tc,ORANGE),(1.3*Tc,GREEN)]: axc.plot(V,vdwP(V,T),color=c,lw=2.2)
axc.set_ylim(-20,140); axc.set_xlabel("V_m",color="white",fontsize=9); axc.set_ylabel("P [atm]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ファンデルワールス","実在気体","(P+a/V^2)(V-b)=RT、臨界点と液化",cc); os.remove(cc)
# gif: isotherm sweep over T
frames=[]; Ts=list(np.linspace(0.7*Tc,1.4*Tc,30))+list(np.linspace(1.4*Tc,0.7*Tc,12))
for T in Ts:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.15,0.15,0.81,0.78]); style(aa)
    aa.plot(V,vdwP(V,T),color=BLUE if T>=Tc else ORANGE,lw=2.2)
    aa.axhline(Pc,color="#3b4a6b",ls=":",lw=1)
    aa.set_ylim(-20,140); aa.set_xlabel("V_m [L/mol]",color="white",fontsize=9); aa.set_ylabel("P [atm]",color="white",fontsize=9)
    aa.set_title(f"T={T:.0f}K ({'>Tc' if T>=Tc else '<Tc: 不安定ループ'})",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
