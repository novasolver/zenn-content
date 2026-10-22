# -*- coding: utf-8 -*-
"""perceptron visuals: 2D points + decision boundary + learning gif.
Replicates tool's seeded LCG + Box-Muller dataset (seed=42)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="perceptron"; NAVY="#0b1020"; BLUE="#3498db"; ORANGE="#f59e0b"; GREEN="#00b894"; RED="#fb7185"; GRY="#c8c8d2"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def gen():
    s=[42&0xFFFFFFFF]
    def rng():
        s[0]=(s[0]*1664525+1013904223)&0xFFFFFFFF; return s[0]/4294967296
    sp=[None]
    def g():
        if sp[0] is not None:
            v=sp[0];sp[0]=None;return v
        u1=max(rng(),1e-12);u2=rng();mag=math.sqrt(-2*math.log(u1))
        sp[0]=mag*math.sin(2*math.pi*u2); return mag*math.cos(2*math.pi*u2)
    pts=[]
    for _ in range(10): pts.append((3+0.8*g(),3+0.8*g(),1))
    for _ in range(10): pts.append((-3+0.8*g(),-3+0.8*g(),-1))
    return pts
data=gen()
def sgn(v): return 1 if v>=0 else -1
def train_capture(eta,w1,w2,b,epochs):
    snaps=[(w1,w2,b)]
    for ep in range(epochs):
        for x1,x2,t in data:
            y=sgn(w1*x1+w2*x2+b)
            if y!=t:
                d=t-y; w1+=eta*d*x1; w2+=eta*d*x2; b+=eta*d
        snaps.append((w1,w2,b))
    return snaps
# start from a poor init (w1=-1.5) so learning is visible
snaps=train_capture(0.1,-1.5,0.5,0.0,8)
def draw(ax,w1,w2,b,title):
    style(ax); ax.set_xlim(-6,6); ax.set_ylim(-6,6); ax.set_aspect("equal")
    for x1,x2,t in data:
        if t==1: ax.plot(x1,x2,"o",color=BLUE,ms=7)
        else: ax.plot(x1,x2,"x",color=RED,ms=7,mew=2)
    xs=np.array([-6,6])
    ax.plot(xs,-xs,color=GRY,ls="--",lw=1.2)  # true boundary x1+x2=0
    if abs(w2)>1e-9: ax.plot(xs,-(w1*xs+b)/w2,color=GREEN,lw=2.4)
    ax.set_xlabel("x1",color="white",fontsize=9); ax.set_ylabel("x2",color="white",fontsize=9)
    ax.set_title(title,color="white",fontsize=10)
# closeup: before vs after
fig=plt.figure(figsize=(9.0,4.4)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.06,0.12,0.42,0.80]); draw(ax,*snaps[0],"学習前 (初期境界)")
w1,w2,b=snaps[-1]; acc=sum(1 for x1,x2,t in data if sgn(w1*x1+w2*x2+b)==t)/len(data)*100
ax2=fig.add_axes([0.55,0.12,0.42,0.80]); draw(ax2,*snaps[-1],f"学習後: 精度 {acc:.0f}%")
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.04,0.06,0.92,0.88]); draw(axc,*snaps[-1],"")
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"パーセプトロン","(線形分類器)","y=sign(w.x+b)、誤分類で重みを更新",cc); os.remove(cc)
frames=[]
for i,(w1,w2,b) in enumerate(snaps):
    acc=sum(1 for x1,x2,t in data if sgn(w1*x1+w2*x2+b)==t)/len(data)*100
    fr=plt.figure(figsize=(4.4,3.2)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.12,0.12,0.84,0.80]); draw(g,w1,w2,b,f"エポック {i}: 精度 {acc:.0f}%")
    frames.append(figlib.fig_to_pil(fr,dpi=90))
frames+=[frames[-1]]*3
figlib.save_gif(frames,SLUG,duration=500); print("done")
