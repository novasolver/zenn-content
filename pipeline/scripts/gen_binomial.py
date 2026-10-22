# -*- coding: utf-8 -*-
"""binomial-distribution visuals: PMF bars + normal approx + p-sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="binomial-distribution"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
from math import comb
def pmf(n,k,p): return comb(n,k)*p**k*(1-p)**(n-k)
n,p=20,0.30; ks=np.arange(0,n+1); pm=[pmf(n,k,p) for k in ks]
mu=n*p; sd=math.sqrt(n*p*(1-p))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
cols=[RED if k==6 else BLUE for k in ks]
ax.bar(ks,pm,color=cols,edgecolor="white",linewidth=0.4)
xx=np.linspace(0,n,200); ax.plot(xx,np.exp(-0.5*((xx-mu)/sd)**2)/(sd*math.sqrt(2*math.pi)),color=ORANGE,lw=2)
ax.axvline(mu,color=GREEN,ls="--",lw=1.2); ax.text(mu+0.3,max(pm)*0.9,f"mu=np=6",color=GREEN,fontsize=8)
ax.text(6,pmf(n,6,p)+0.005,"P(X=6)\n=0.192",color=RED,fontsize=8,ha="center")
ax.set_xlabel("成功回数 k",color="white",fontsize=9); ax.set_ylabel("確率 P(X=k)",color="white",fontsize=9)
ax.set_title("二項分布 (n=20, p=0.3) と正規近似",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
cdf=np.cumsum(pm); ax2.step(ks,cdf,where="post",color=GREEN,lw=2)
ax2.plot(6,cdf[6],"o",color=ORANGE); ax2.annotate("P(X<=6)=0.608",(6,cdf[6]),(7,0.4),color="white",fontsize=8)
ax2.set_xlabel("k",color="white",fontsize=9); ax2.set_ylabel("累積 P(X<=k)",color="white",fontsize=9)
ax2.set_title("累積分布",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.bar(ks,pm,color=cols)
axc.plot(xx,np.exp(-0.5*((xx-mu)/sd)**2)/(sd*math.sqrt(2*math.pi)),color=ORANGE,lw=2)
axc.set_xlabel("k",color="white",fontsize=9); axc.set_ylabel("P(X=k)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"二項分布","","P(X=k)=C(n,k)p^k(1-p)^(n-k)、平均 np",cc); os.remove(cc)
frames=[]; ps=list(np.linspace(0.1,0.9,26))+list(np.linspace(0.9,0.1,12))
for pv in ps:
    pmv=[pmf(n,k,pv) for k in ks]
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.13,0.15,0.83,0.76]); style(aa)
    aa.bar(ks,pmv,color=BLUE,edgecolor="white",linewidth=0.3); aa.axvline(n*pv,color=GREEN,ls="--",lw=1.2)
    aa.set_ylim(0,0.30); aa.set_xlabel("k",color="white",fontsize=9); aa.set_ylabel("P(X=k)",color="white",fontsize=9)
    aa.set_title(f"n=20, p={pv:.2f} (mu=np={n*pv:.1f})",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=95); print("done")
