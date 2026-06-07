# -*- coding: utf-8 -*-
"""taylor-series visuals: sin vs Taylor polynomials + error + add-terms gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="taylor-series"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"; YEL="#ffd24b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def fact(n):
    r=1
    for i in range(2,n+1): r*=i
    return r
def tsin(x,N):
    base=[0,1,0,-1]; s=np.zeros_like(x)
    for n in range(N+1): s=s+base[n%4]/fact(n)*x**n
    return s
x=np.linspace(-4,4,400)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
ax.plot(x,np.sin(x),color=YEL,lw=2.6,label="sin(x)")
for N,c in [(1,RED),(3,ORANGE),(5,GREEN),(7,BLUE)]:
    ax.plot(x,tsin(x,N),lw=1.6,color=c,ls="--",label=f"N={N}")
ax.set_ylim(-3,3); ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("y",color="white",fontsize=9)
ax.set_title("sin(x) のテイラー近似 (a=0)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.16,0.37,0.74]); style(ax2)
xt=0.5
Ns=range(1,10); errs=[abs(float(tsin(np.array([xt]),N)[0])-math.sin(xt)) for N in Ns]
ax2.semilogy(list(Ns),errs,"o-",color=ORANGE,lw=2,ms=5)
ax2.set_xlabel("次数 N",color="white",fontsize=9); ax2.set_ylabel("|sin(0.5)-T_N(0.5)| (対数)",color="white",fontsize=8)
ax2.set_title("項を増やすほど誤差は急減",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.plot(x,np.sin(x),color=YEL,lw=2.6)
for N,c in [(1,RED),(3,ORANGE),(5,GREEN),(7,BLUE)]: axc.plot(x,tsin(x,N),lw=1.6,color=c,ls="--")
axc.set_ylim(-3,3); axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("y",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"テイラー級数","による近似","多項式で関数を近似、次数を上げるほど一致",cc); os.remove(cc)
frames=[]
for N in [1,3,5,7,9,11,13]:
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.12,0.15,0.84,0.76]); style(g)
    g.plot(x,np.sin(x),color=YEL,lw=2.6); g.plot(x,tsin(x,N),color=BLUE,lw=2,ls="--")
    g.set_ylim(-3,3); g.set_xlabel("x",color="white",fontsize=9); g.set_ylabel("y",color="white",fontsize=9)
    g.set_title(f"N={N}: 近似範囲が広がる",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=420); print("done")
