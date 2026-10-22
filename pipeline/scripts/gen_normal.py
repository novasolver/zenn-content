# -*- coding: utf-8 -*-
"""normal-distribution visuals: PDF+shaded tail & CDF + empirical rule gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import erf
import figlib
SLUG="normal-distribution"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#00b894"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def pdf(x,mu=0,s=1): return np.exp(-0.5*((x-mu)/s)**2)/(s*math.sqrt(2*math.pi))
def cdf(x,mu=0,s=1): return 0.5*(1+erf((x-mu)/(s*math.sqrt(2))))
x=np.linspace(-4,4,400)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.15,0.42,0.74]); style(ax)
ax.plot(x,pdf(x),color=BLUE,lw=2.3)
xs=x[x<=-1]; ax.fill_between(xs,pdf(xs),color=ORANGE,alpha=0.45)
ax.text(-3.2,0.07,"P(X<-1)\n=15.87%",color=ORANGE,fontsize=9)
# empirical bands
for k,a in [(1,0.12),(2,0.08),(3,0.05)]:
    pass
ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("確率密度 f(x)",color="white",fontsize=9)
ax.set_title("標準正規分布 (mu=0, sigma=1)",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
ax2.plot(x,cdf(x),color=GREEN,lw=2.3); ax2.axhline(0.5,color="#3b4a6b",ls=":",lw=1)
ax2.plot(-1,cdf(-1),"o",color=ORANGE); ax2.annotate("Phi(-1)=0.159",(-1,cdf(-1)),(-0.5,0.25),color="white",fontsize=8)
ax2.set_xlabel("x",color="white",fontsize=9); ax2.set_ylabel("累積分布 Phi(x)",color="white",fontsize=9)
ax2.set_title("CDF: 68-95-99.7 ルール",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.plot(x,pdf(x),color=BLUE,lw=2.4)
for k,c in [(1,"#1e3a5f"),(2,"#16314f"),(3,"#0f263f")]:
    xs2=x[(x>=-k)&(x<=k)]; axc.fill_between(xs2,pdf(xs2),color=ORANGE,alpha=0.12)
axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("f(x)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"正規分布","(ガウス分布)","68-95-99.7 ルールと累積確率",cc); os.remove(cc)
# gif: shaded P(X<a) as a sweeps
frames=[]; avals=list(np.linspace(-3,3,30))+list(np.linspace(3,-3,12))
for a in avals:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.13,0.15,0.83,0.76]); style(aa)
    aa.plot(x,pdf(x),color=BLUE,lw=2.2); xs=x[x<=a]; aa.fill_between(xs,pdf(xs),color=ORANGE,alpha=0.45)
    aa.set_ylim(0,0.45); aa.set_xlabel("x",color="white",fontsize=9); aa.set_ylabel("f(x)",color="white",fontsize=9)
    aa.set_title(f"P(X < {a:+.1f}) = {cdf(a)*100:.1f}%",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=95); print("done")
