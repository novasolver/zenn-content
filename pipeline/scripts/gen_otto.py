# -*- coding: utf-8 -*-
"""otto-cycle visuals: P-V diagram + efficiency(r) + PV marker gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="otto-cycle"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; YEL="#ffd24b"; PUR="#9b59b6"; RED="#e74c3c"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
r=9.0; g=1.4; T1=300.0; Qin=1500.0; R=0.287; cv=R/(g-1)
v1=1.0; v2=1.0/r; P1=1.0; P2=r**g
T2=T1*r**(g-1); T3=T2+Qin/cv; P3=P2*(T3/T2); P4=P3*(v2/v1)**g
def pv_curve():
    seg=[]
    vv=np.linspace(v1,v2,60); seg.append((vv,P1*(v1/vv)**g))      # 1->2 isentrope
    seg.append((np.array([v2,v2]),np.array([P2,P3])))             # 2->3 const V
    vv=np.linspace(v2,v1,60); seg.append((vv,P3*(v2/vv)**g))      # 3->4 isentrope
    seg.append((np.array([v1,v1]),np.array([P4,P1])))             # 4->1 const V
    return seg
seg=pv_curve()
# closeup: PV (left) + eta(r) (right)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.14,0.40,0.76]); style(ax)
cols=[BLUE,RED,GREEN,PUR]
for (vv,pp),c in zip(seg,cols): ax.plot(vv,pp,color=c,lw=2.3)
for v,p,n in [(v1,P1,"1"),(v2,P2,"2"),(v2,P3,"3"),(v1,P4,"4")]:
    ax.plot(v,p,"o",color=YEL,ms=5); ax.annotate(n,(v,p),(v+0.02,p*1.05),color="white",fontsize=9)
ax.set_xlabel("比体積 v (v1=1)",color="white",fontsize=9); ax.set_ylabel("圧力 P (P1=1)",color="white",fontsize=9)
ax.set_title("オットーサイクルのP-V線図",color="white",fontsize=10)
ax2=fig.add_axes([0.58,0.15,0.39,0.74]); style(ax2)
rr=np.linspace(4,20,200); ax2.plot(rr,1-1/rr**(g-1),color=BLUE,lw=2.3)
ax2.plot(r,1-1/r**(g-1),"o",color=ORANGE); ax2.annotate(f"r=9: {(1-1/r**(g-1))*100:.1f}%",(r,1-1/r**(g-1)),(r+0.5,0.45),color="white",fontsize=8)
ax2.set_xlabel("圧縮比 r",color="white",fontsize=9); ax2.set_ylabel("熱効率 eta",color="white",fontsize=9)
ax2.set_title("eta = 1 - 1/r^(gamma-1)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
# cover
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.16,0.80,0.78]); style(axc)
for (vv,pp),c in zip(seg,cols): axc.plot(vv,pp,color=c,lw=2.4)
axc.set_xlabel("v",color="white",fontsize=9); axc.set_ylabel("P",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"オットーサイクル","","ガソリン機関の熱効率 eta=1-1/r^(g-1)",cc); os.remove(cc)
# gif: marker around PV cycle
allv=np.concatenate([s[0] for s in seg]); allp=np.concatenate([s[1] for s in seg])
frames=[]; N=44; L=len(allv)
for kf in range(N):
    j=int(L*kf/N)
    f=plt.figure(figsize=(4.6,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.14,0.14,0.82,0.80]); style(a)
    for (vv,pp),c in zip(seg,cols): a.plot(vv,pp,color=c,lw=1.8)
    a.fill(allv,allp,color=YEL,alpha=0.12)
    a.plot(allv[j],allp[j],"o",color="white",ms=9)
    a.set_xlabel("v",color="white",fontsize=9); a.set_ylabel("P",color="white",fontsize=9)
    a.set_title("囲む面積 = 正味仕事",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=80); print("done")
