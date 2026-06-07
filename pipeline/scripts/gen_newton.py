# -*- coding: utf-8 -*-
"""newton-raphson visuals: f(x) curve + tangents + |f| convergence + tangent gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="newton-raphson"; NAVY="#0b1020"; BLUE="#7bb3ff"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"; YEL="#ffd24b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def f(x): return x**3-2*x-5
def fp(x): return 3*x*x-2
xs=[2.0]
for _ in range(6):
    x=xs[-1]; xs.append(x-f(x)/fp(x))
    if abs(f(xs[-1]))<1e-12: break
x=np.linspace(-0.5,3.2,400)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
ax.axhline(0,color="#3b4a6b",lw=1); ax.plot(x,f(x),color=BLUE,lw=2.2)
for i in range(min(3,len(xs)-1)):
    xn=xs[i]; ax.plot([xn,xn],[0,f(xn)],color="#3b4a6b",ls=":",lw=1)
    xt=np.array([xn-1.2,xn+1.2]); ax.plot(xt,f(xn)+fp(xn)*(xt-xn),color=YEL,ls="--",lw=1.2,alpha=0.8-0.2*i)
    ax.plot(xn,f(xn),"o",color=RED,ms=5)
ax.plot(2.094551482,0,"o",color=GREEN,ms=8)
ax.set_ylim(-12,18); ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("f(x)=x^3-2x-5",color="white",fontsize=9)
ax.set_title("接線で根へ近づく（緑=根 2.0946）",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.16,0.37,0.74]); style(ax2)
errs=[abs(f(xx)) for xx in xs]; ax2.semilogy(range(len(errs)),errs,"o-",color=ORANGE,lw=2,ms=5)
ax2.axhline(1e-6,color=RED,ls="--",lw=1); ax2.text(1.5,2e-6,"許容差 1e-6",color=RED,fontsize=8)
ax2.set_xlabel("反復回数 n",color="white",fontsize=9); ax2.set_ylabel("|f(x_n)| (対数)",color="white",fontsize=9)
ax2.set_title("2次収束：桁数が倍々で増える",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.axhline(0,color="#3b4a6b",lw=1); axc.plot(x,f(x),color=BLUE,lw=2.4)
for i in range(3):
    xn=xs[i]; xt=np.array([xn-1.2,xn+1.2]); axc.plot(xt,f(xn)+fp(xn)*(xt-xn),color=YEL,ls="--",lw=1.2)
axc.plot(2.094551482,0,"o",color=GREEN,ms=7); axc.set_ylim(-12,18)
axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("f(x)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ニュートン","ラフソン法","x <- x - f(x)/f'(x)、3反復で9桁一致",cc); os.remove(cc)
frames=[]
for i in range(min(4,len(xs))):
    f_=plt.figure(figsize=(4.8,3.0)); f_.patch.set_facecolor(NAVY)
    aa=f_.add_axes([0.13,0.15,0.83,0.76]); style(aa)
    aa.axhline(0,color="#3b4a6b",lw=1); aa.plot(x,f(x),color=BLUE,lw=2.2)
    xn=xs[i]; xt=np.array([xn-1.3,xn+1.3])
    aa.plot(xt,f(xn)+fp(xn)*(xt-xn),color=YEL,ls="--",lw=1.6); aa.plot(xn,f(xn),"o",color=RED,ms=7)
    aa.plot([xn,xn],[0,f(xn)],color="#3b4a6b",ls=":",lw=1)
    aa.set_ylim(-12,18); aa.set_xlabel("x",color="white",fontsize=9); aa.set_ylabel("f(x)",color="white",fontsize=9)
    aa.set_title(f"反復 {i}: x={xn:.6f}, |f|={abs(f(xn)):.1e}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f_,dpi=90))
frames+= [frames[-1]]*3
figlib.save_gif(frames,SLUG,duration=600); print("done")
