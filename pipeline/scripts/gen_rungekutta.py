# -*- coding: utf-8 -*-
"""runge-kutta visuals: solution comparison + error + h-sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="runge-kutta"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; RED="#fb7185"; WHITE="#e8eefc"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
k,y0=0.5,10.0
def integ(h,xend=4.0):
    n=round(xend/h); xs=[0];yE=[y0];yR=[y0];ex=[y0]
    e=r=y0
    for i in range(n):
        e=e+h*(-k*e)
        k1=h*(-k*r);k2=h*(-k*(r+k1/2));k3=h*(-k*(r+k2/2));k4=h*(-k*(r+k3));r=r+(k1+2*k2+2*k3+k4)/6
        x=(i+1)*h; xs.append(x);yE.append(e);yR.append(r);ex.append(y0*math.exp(-k*x))
    return np.array(xs),np.array(yE),np.array(yR),np.array(ex)
xs,yE,yR,ex=integ(0.1)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
xf=np.linspace(0,4,200); ax.plot(xf,y0*np.exp(-k*xf),color=WHITE,lw=2.6,label="厳密解")
ax.plot(xs,yR,"o-",color=BLUE,lw=1.6,ms=3,label="RK4")
ax.plot(xs,yE,"s-",color=RED,lw=1.6,ms=3,label="Euler")
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("y(x)",color="white",fontsize=9)
ax.set_title("dy/dx=-ky の数値解 (h=0.1)",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.16,0.37,0.74]); style(ax2)
errR=np.maximum(np.abs(yR-ex),1e-16); errE=np.maximum(np.abs(yE-ex),1e-16)
ax2.semilogy(xs,errR,color=BLUE,lw=2,label="RK4 誤差"); ax2.semilogy(xs,errE,color=RED,lw=2,label="Euler 誤差")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("x",color="white",fontsize=9); ax2.set_ylabel("|y_num - y_exact| (対数)",color="white",fontsize=8)
ax2.set_title("RK4はEulerより桁違いに高精度",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc)
axc.plot(xf,y0*np.exp(-k*xf),color=WHITE,lw=2.6); axc.plot(xs,yR,"o-",color=BLUE,lw=1.6,ms=3); axc.plot(xs,yE,"s-",color=RED,lw=1.6,ms=3)
axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("y",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ルンゲ・クッタ法","(ODE解法)","4つの傾きの加重平均で高精度に積分",cc); os.remove(cc)
frames=[]; hs=list(np.linspace(0.05,1.0,24))+list(np.linspace(1.0,0.05,10))
for h in hs:
    xs,yE,yR,ex=integ(h)
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.15,0.83,0.76]); style(g)
    g.plot(xf,y0*np.exp(-k*xf),color=WHITE,lw=2.4)
    g.plot(xs,yR,"o-",color=BLUE,lw=1.4,ms=3); g.plot(xs,yE,"s-",color=RED,lw=1.4,ms=3)
    g.set_ylim(0,11); g.set_xlabel("x",color="white",fontsize=9); g.set_ylabel("y",color="white",fontsize=9)
    g.set_title(f"h={h:.2f}: Eulerはhが大きいと崩れる",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
