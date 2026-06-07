# -*- coding: utf-8 -*-
"""diesel-cycle visuals: P-V diagram + eta(r) diesel vs otto + PV marker gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="diesel-cycle"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#2ecc71"; YEL="#ffd24b"; PUR="#9b59b6"; RED="#e17055"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
r=18.0; rc=2.0; g=1.4
v1=1.0; v2=1.0/r; v3=v2*rc; P1=1.0; P2=P1*r**g; P3=P2; P4=P3*(v3/v1)**g
def pv():
    seg=[]
    vv=np.linspace(v1,v2,60); seg.append((vv,P1*(v1/vv)**g,BLUE))     # compression
    seg.append((np.array([v2,v3]),np.array([P2,P3]),RED))            # const pressure heat
    vv=np.linspace(v3,v1,60); seg.append((vv,P3*(v3/vv)**g,GREEN))   # expansion
    seg.append((np.array([v1,v1]),np.array([P4,P1]),PUR))            # const volume reject
    return seg
seg=pv()
def deta(r,rc,g): return 1-(1/r**(g-1))*((rc**g-1)/(g*(rc-1)))
def oeta(r,g): return 1-1/r**(g-1)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.14,0.40,0.76]); style(ax)
for vv,pp,c in seg: ax.plot(vv,pp,color=c,lw=2.3)
for v,p,n in [(v1,P1,"1"),(v2,P2,"2"),(v3,P3,"3"),(v1,P4,"4")]:
    ax.plot(v,p,"o",color=YEL,ms=5); ax.annotate(n,(v,p),(v+0.02,p*1.04+2),color="white",fontsize=9)
ax.set_xlabel("比体積 v (v1=1)",color="white",fontsize=9); ax.set_ylabel("圧力 P (P1=1)",color="white",fontsize=9)
ax.set_title("ディーゼル: 2->3は定圧加熱(赤)",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
rr=np.linspace(8,25,200); ax2.plot(rr,[deta(x,rc,g) for x in rr],color=BLUE,lw=2.3,label="ディーゼル(rc=2)")
ax2.plot(rr,[oeta(x,g) for x in rr],color=ORANGE,lw=2.0,ls="--",label="オットー")
ax2.plot(r,deta(r,rc,g),"o",color=ORANGE)
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("圧縮比 r",color="white",fontsize=9); ax2.set_ylabel("熱効率 eta",color="white",fontsize=9)
ax2.set_title("同じrならオットーが上",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.16,0.80,0.78]); style(axc)
for vv,pp,c in seg: axc.plot(vv,pp,color=c,lw=2.4)
axc.set_xlabel("v",color="white",fontsize=9); axc.set_ylabel("P",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ディーゼルサイクル","","圧縮着火・定圧加熱、締切り比 rc が効率を左右",cc); os.remove(cc)
allv=np.concatenate([s[0] for s in seg]); allp=np.concatenate([s[1] for s in seg])
frames=[]; N=44; Ln=len(allv)
for kf in range(N):
    j=int(Ln*kf/N)
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.14,0.14,0.82,0.80]); style(a)
    for vv,pp,c in seg: a.plot(vv,pp,color=c,lw=1.8)
    a.fill(allv,allp,color=YEL,alpha=0.12); a.plot(allv[j],allp[j],"o",color="white",ms=9)
    a.set_xlabel("v",color="white",fontsize=9); a.set_ylabel("P",color="white",fontsize=9)
    a.set_title("ディーゼルサイクル",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=80); print("done")
