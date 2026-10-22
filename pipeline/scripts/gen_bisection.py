# -*- coding: utf-8 -*-
"""bisection-method visuals: bracket shrinking + width convergence + gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="bisection-method"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"; YEL="#ffd24b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def f(x): return x**3-2*x-5
a,b=1.0,3.0; tol=1e-6; brackets=[(a,b)]; mids=[]; widths=[b-a]
while b-a>=tol and len(mids)<40:
    c=(a+b)/2; mids.append(c)
    if abs(f(c))<tol: break
    if f(a)*f(c)<0: b=c
    else: a=c
    brackets.append((a,b)); widths.append(b-a)
x=np.linspace(0.5,3.2,400)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.42,0.76]); style(ax)
ax.axhline(0,color="#3b4a6b",lw=1); ax.plot(x,f(x),color=BLUE,lw=2.2)
for i,(aa,bb) in enumerate(brackets[:6]):
    yv=2-i*2.0; ax.plot([aa,bb],[yv,yv],color=ORANGE,lw=2,alpha=0.85-0.1*i)
    ax.plot([aa,aa],[yv-0.4,yv+0.4],color=BLUE,lw=1); ax.plot([bb,bb],[yv-0.4,yv+0.4],color=RED,lw=1)
ax.plot(2.094551482,0,"o",color=GREEN,ms=8)
ax.set_ylim(-12,16); ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("f(x)=x^3-2x-5",color="white",fontsize=9)
ax.set_title("区間[a,b]を半分ずつ狭める",color="white",fontsize=10)
ax2=fig.add_axes([0.60,0.16,0.37,0.74]); style(ax2)
ax2.semilogy(range(len(widths)),widths,"o-",color=ORANGE,lw=2,ms=4)
ax2.axhline(tol,color=RED,ls="--",lw=1); ax2.text(2,tol*1.5,"許容差 1e-6",color=RED,fontsize=8)
ax2.set_xlabel("反復回数 n",color="white",fontsize=9); ax2.set_ylabel("区間幅 b-a (対数)",color="white",fontsize=9)
ax2.set_title("線形収束：幅は毎回半分(直線)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.axhline(0,color="#3b4a6b",lw=1); axc.plot(x,f(x),color=BLUE,lw=2.4)
for i,(aa,bb) in enumerate(brackets[:5]):
    yv=2-i*2.2; axc.plot([aa,bb],[yv,yv],color=ORANGE,lw=2)
axc.plot(2.094551482,0,"o",color=GREEN,ms=7); axc.set_ylim(-12,16)
axc.set_xlabel("x",color="white",fontsize=9); axc.set_ylabel("f(x)",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"二分法による求根","","符号が変わる区間を半分ずつ詰める",cc); os.remove(cc)
frames=[]
for i in range(min(12,len(brackets))):
    aa,bb=brackets[i]; c=(aa+bb)/2
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.15,0.83,0.76]); style(g)
    g.axhline(0,color="#3b4a6b",lw=1); g.plot(x,f(x),color=BLUE,lw=2.2)
    g.axvspan(aa,bb,color=ORANGE,alpha=0.18); g.axvline(c,color=YEL,ls="--",lw=1.4); g.plot(c,f(c),"o",color=RED,ms=6)
    g.set_ylim(-12,16); g.set_xlabel("x",color="white",fontsize=9); g.set_ylabel("f(x)",color="white",fontsize=9)
    g.set_title(f"反復{i}: 中点 c={c:.5f}, 幅={bb-aa:.1e}",color="white",fontsize=9)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=420); print("done")
