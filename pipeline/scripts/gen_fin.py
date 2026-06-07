# -*- coding: utf-8 -*-
"""fin-heat-transfer visuals: T(x) profile + eta(mL) + fin temperature gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="fin-heat-transfer"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#ff6b6b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def finparams(L,t,W,k,h):
    L*=1e-3;t*=1e-3;W*=1e-3; P=2*(W+t); A=W*t; m=math.sqrt(h*P/(k*A)); return m,m*L,L
Tb,Tinf=80,25
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.15,0.42,0.74]); style(ax)
xrel=np.linspace(0,1,100)
for k,c,lab in [(400,GREEN,"銅 k=400"),(200,BLUE,"アルミ k=200"),(50,RED,"鋼 k=50")]:
    m,mL,L=finparams(50,3,50,k,25)
    T=Tinf+(Tb-Tinf)*np.cosh(mL*(1-xrel))/math.cosh(mL)
    ax.plot(xrel*50,T,color=c,lw=2.2,label=lab)
ax.axhline(Tinf,color="#3b4a6b",ls=":",lw=1); ax.text(2,Tinf+1.5,"環境温度 25C",color="#9fb2d6",fontsize=8)
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax.set_xlabel("根元からの位置 x [mm]",color="white",fontsize=9); ax.set_ylabel("温度 T [C]",color="white",fontsize=9)
ax.set_title("フィンの温度分布 cosh[m(L-x)]/cosh(mL)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.15,0.37,0.74]); style(ax2)
mLr=np.linspace(0.05,5,300); ax2.plot(mLr,np.tanh(mLr)/mLr,color=ORANGE,lw=2.3)
m,mL,_=finparams(50,3,50,200,25); ax2.plot(mL,math.tanh(mL)/mL,"o",color=BLUE); ax2.annotate(f"既定 mL={mL:.2f}: 93%",(mL,math.tanh(mL)/mL),(mL+0.6,0.85),color="white",fontsize=8)
ax2.set_xlabel("フィンパラメータ mL",color="white",fontsize=9); ax2.set_ylabel("フィン効率 eta=tanh(mL)/mL",color="white",fontsize=8)
ax2.set_title("mLが大きいほど効率は落ちる",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.15,0.16,0.81,0.78]); style(axc)
for k,c in [(400,GREEN),(200,BLUE),(50,RED)]:
    m,mL,L=finparams(50,3,50,k,25); axc.plot(xrel*50,Tinf+(Tb-Tinf)*np.cosh(mL*(1-xrel))/math.cosh(mL),color=c,lw=2.2)
axc.set_xlabel("x [mm]",color="white",fontsize=9); axc.set_ylabel("T [C]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"フィンの熱伝達","","放熱板の温度分布と効率 eta=tanh(mL)/mL",cc); os.remove(cc)
# gif: fin colored by temperature as h sweeps
frames=[]; hs=list(np.linspace(10,300,28))+list(np.linspace(300,10,12))
for hh in hs:
    m,mL,L=finparams(50,3,50,200,hh)
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.12,0.18,0.84,0.7]); aa.set_facecolor(NAVY); aa.set_xlim(0,50); aa.set_ylim(0,1); aa.set_yticks([])
    style(aa)
    for i in range(60):
        xr=i/60; T=Tinf+(Tb-Tinf)*math.cosh(mL*(1-xr))/math.cosh(mL); r=(T-Tinf)/(Tb-Tinf)
        aa.add_patch(plt.Rectangle((xr*50,0),50/60,1,color=(0.1+0.9*r,0.2+0.3*(1-abs(r-0.5)*2),0.9-0.8*r)))
    aa.set_xlabel("x [mm]  (赤=高温, 青=低温)",color="white",fontsize=9)
    aa.set_title(f"h={hh:.0f} W/m2K -> eta={math.tanh(mL)/mL*100:.0f}%",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
