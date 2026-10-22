# -*- coding: utf-8 -*-
"""numerical-integration visuals: trapezoids + error vs n + refine gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="numerical-integration"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
f=np.sin; a,b=0,1; ex=1-math.cos(1)
def trap(fn,a,b,n):
    h=(b-a)/n; s=(fn(a)+fn(b))/2
    for i in range(1,n): s+=fn(a+i*h)
    return h*s
def simp(fn,a,b,n):
    if n%2:n+=1
    h=(b-a)/n; s=fn(a)+fn(b)
    for i in range(1,n): s+=(2 if i%2==0 else 4)*fn(a+i*h)
    return h*s/3
x=np.linspace(0,1,300)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
ax.plot(x,np.sin(x),color=ORANGE,lw=2.3)
n=10; h=(b-a)/n; xn=np.linspace(a,b,n+1)
for i in range(n):
    ax.fill([xn[i],xn[i],xn[i+1],xn[i+1]],[0,math.sin(xn[i]),math.sin(xn[i+1]),0],color=BLUE,alpha=0.25,ec=BLUE,lw=0.6)
ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("f(x)=sin(x)",color="white",fontsize=9)
ax.set_title(f"台形則(n=10): 近似={trap(np.sin,0,1,10):.5f} (真値{ex:.5f})",color="white",fontsize=9)
ax2=fig.add_axes([0.60,0.16,0.37,0.74]); style(ax2)
ns=np.array([2,4,8,16,32,64,128])
et=[abs(trap(np.sin,0,1,n)-ex) for n in ns]; es=[abs(simp(np.sin,0,1,n)-ex) for n in ns]
ax2.loglog(ns,et,"o-",color=BLUE,lw=2,label="台形 O(h^2)"); ax2.loglog(ns,es,"s-",color=GREEN,lw=2,label="Simpson O(h^4)")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("分割数 n",color="white",fontsize=9); ax2.set_ylabel("絶対誤差 (対数)",color="white",fontsize=8)
ax2.set_title("Simpsonは収束が桁違いに速い",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.plot(x,np.sin(x),color=ORANGE,lw=2.4)
for i in range(n): axc.fill([xn[i],xn[i],xn[i+1],xn[i+1]],[0,math.sin(xn[i]),math.sin(xn[i+1]),0],color=BLUE,alpha=0.25,ec=BLUE,lw=0.6)
axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("sin(x)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"数値積分","(台形・シンプソン)","面積を短冊で近似、誤差は O(h^2) と O(h^4)",cc); os.remove(cc)
frames=[]
for n in [2,3,4,6,8,12,16,24,32]:
    h=(b-a)/n; xn=np.linspace(a,b,n+1)
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.15,0.83,0.76]); style(g)
    g.plot(x,np.sin(x),color=ORANGE,lw=2.3)
    for i in range(n): g.fill([xn[i],xn[i],xn[i+1],xn[i+1]],[0,math.sin(xn[i]),math.sin(xn[i+1]),0],color=BLUE,alpha=0.25,ec=BLUE,lw=0.6)
    g.set_xlabel("x",color="white",fontsize=9); g.set_ylabel("sin(x)",color="white",fontsize=9)
    g.set_title(f"n={n}: 誤差={abs(trap(np.sin,0,1,n)-ex):.1e}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=320); print("done")
