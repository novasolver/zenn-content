# -*- coding: utf-8 -*-
"""buffon-needle visuals: needles on lines + pi convergence + accumulation gif.
Replicates tool's deterministic LCG (seed=42) for consistency."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="buffon-needle"; NAVY="#0b1020"; BLUE="#007BFF"; ORANGE="#f59e0b"; RED="#e74c3c"; GRY="#6c757d"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def lcg(seed):
    st=seed&0xFFFFFFFF or 1
    while True:
        st=(st*1664525+1013904223)&0xFFFFFFFF; yield st/4294967296
L,d=5.0,10.0; seed=42
g=lcg(seed); N=20000
ys=[]; ths=[]; cross=[]; cum=[]; mc=0
for i in range(N):
    y=next(g)*(d/2); th=next(g)*math.pi/2; c=y<=(L/2)*math.sin(th)
    ys.append(y); ths.append(th); cross.append(c); mc+=c
    if i>=10: cum.append(2*L*(i+1)/(d*mc) if mc>0 else np.nan)
# closeup: needles (sample) + convergence
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
axn=fig.add_axes([0.03,0.08,0.46,0.84]); axn.set_facecolor(NAVY); axn.axis("off")
gv=lcg(seed+9973)
for j in range(160):
    yc=next(gv)*5; xc=next(gv)*9+0.5; th=ths[j]
    dx=(L/2)*math.cos(th)/3; dy=(L/2)*math.sin(th)/3
    axn.plot([xc-dx,xc+dx],[yc-dy,yc+dy],color=RED if cross[j] else BLUE,lw=1.3)
for ln in range(6): axn.axhline(ln,color=GRY,lw=1)
axn.set_xlim(0,10); axn.set_ylim(-0.3,5.3)
axn.set_title("針を投げる（赤=線と交差, 青=非交差）",color="white",fontsize=10)
axc=fig.add_axes([0.58,0.16,0.39,0.74]); style(axc)
xx=np.arange(11,N+1); axc.semilogx(xx,cum,color=BLUE,lw=1.4)
axc.axhline(math.pi,color=ORANGE,ls="--",lw=1.4); axc.text(2000,math.pi+0.05,"pi",color=ORANGE,fontsize=9)
axc.set_ylim(2.6,3.7); axc.set_xlabel("投げた本数 N",color="white",fontsize=9); axc.set_ylabel("pi 推定値",color="white",fontsize=9)
axc.set_title("N増加でpiに収束 (誤差~1/sqrt(N))",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
ax2=figc.add_axes([0.14,0.17,0.82,0.74]); style(ax2); ax2.semilogx(xx,cum,color=BLUE,lw=1.6); ax2.axhline(math.pi,color=ORANGE,ls="--",lw=1.6)
ax2.set_ylim(2.6,3.7); ax2.set_xlabel("N",color="white",fontsize=9); ax2.set_ylabel("pi 推定",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ビュフォンの針","と円周率","針を投げて pi を推定: pi=2LN/(dm)",cc); os.remove(cc)
# gif: convergence accumulation
frames=[]; pts=[20,50,100,300,1000,3000,10000,20000]
for npt in pts:
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    aa=f.add_axes([0.15,0.16,0.81,0.74]); style(aa)
    aa.semilogx(xx[:npt-10],cum[:npt-10],color=BLUE,lw=1.4); aa.axhline(math.pi,color=ORANGE,ls="--",lw=1.4)
    aa.set_ylim(2.6,3.7); aa.set_xlim(11,N)
    cur=cum[npt-11] if npt-11<len(cum) else cum[-1]
    aa.set_xlabel("N",color="white",fontsize=9); aa.set_ylabel("pi 推定",color="white",fontsize=9)
    aa.set_title(f"N={npt}: pi_hat={cur:.4f}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=130); print("done")
