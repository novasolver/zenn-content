# -*- coding: utf-8 -*-
"""gradient-descent visuals: contour + Adam path + loss curve + descent gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="gradient-descent"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def loss(x,y): return x*x+y*y
def grad(x,y,e=1e-5): return (loss(x+e,y)-loss(x-e,y))/(2*e),(loss(x,y+e)-loss(x,y-e))/(2*e)
def adam_path(steps,lr=0.01,b1=0.9,b2=0.999,eps=1e-8):
    px,py=-2.52,2.52; m1=m2=v1=v2=0.0; path=[(px,py)]; losses=[loss(px,py)]
    for t in range(1,steps+1):
        gx,gy=grad(px,py)
        m1=b1*m1+(1-b1)*gx; m2=b1*m2+(1-b1)*gy; v1=b2*v1+(1-b2)*gx*gx; v2=b2*v2+(1-b2)*gy*gy
        m1h=m1/(1-b1**t); m2h=m2/(1-b1**t); v1h=v1/(1-b2**t); v2h=v2/(1-b2**t)
        px-=lr*m1h/(math.sqrt(v1h)+eps); py-=lr*m2h/(math.sqrt(v2h)+eps)
        path.append((px,py)); losses.append(loss(px,py))
    return np.array(path),np.array(losses)
path,losses=adam_path(500)
gx=np.linspace(-3,3,200); X,Y=np.meshgrid(gx,gx); Z=X*X+Y*Y
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.06,0.12,0.44,0.80]); ax.set_facecolor(NAVY)
ax.contourf(X,Y,Z,levels=18,cmap="viridis",alpha=0.85); ax.contour(X,Y,Z,levels=10,colors="white",linewidths=0.4,alpha=0.4)
ax.plot(path[:,0],path[:,1],color=ORANGE,lw=2); ax.plot(path[0,0],path[0,1],"o",color="white",ms=7); ax.plot(path[-1,0],path[-1,1],"o",color=GREEN,ms=8)
ax.set_xlabel("x",color="white",fontsize=9); ax.set_ylabel("y",color="white",fontsize=9)
ax.tick_params(colors="#9fb2d6",labelsize=8)
ax.set_title("Adam の降下経路 (f=x^2+y^2)",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
ax2.semilogy(losses,color=BLUE,lw=2)
ax2.set_xlabel("ステップ",color="white",fontsize=9); ax2.set_ylabel("損失 f (対数)",color="white",fontsize=9)
ax2.set_title("損失は単調に減少 (500歩で~0.01)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0,0,1,1]); axc.set_facecolor(NAVY); axc.axis("off")
axc.contourf(X,Y,Z,levels=18,cmap="viridis"); axc.plot(path[:,0],path[:,1],color=ORANGE,lw=2.4); axc.plot(path[-1,0],path[-1,1],"o",color=GREEN,ms=8)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"勾配降下法","","x <- x - alpha grad f、最小へ降りる",cc); os.remove(cc)
frames=[]; idxs=list(range(0,501,16))
for j in idxs:
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.02,0.06,0.96,0.86]); aa.set_facecolor(NAVY); aa.axis("off")
    aa.contourf(X,Y,Z,levels=18,cmap="viridis",alpha=0.85)
    aa.plot(path[:j+1,0],path[:j+1,1],color=ORANGE,lw=2); aa.plot(path[j,0],path[j,1],"o",color="white",ms=8)
    aa.set_title(f"step {j}: loss={losses[j]:.3f}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=90); print("done")
