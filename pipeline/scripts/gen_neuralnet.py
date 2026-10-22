# -*- coding: utf-8 -*-
"""neural-network visuals: XOR decision boundary + loss curve + boundary-evolution gif.
Representative seeded training (tool itself is unseeded)."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="neural-network"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; RED="#fb7185"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
random.seed(7)
def sig(x): return 1/(1+math.exp(-max(-30,min(30,x))))
H=6
W1=[[random.uniform(-1,1) for _ in range(2)] for _ in range(H)]; b1=[random.uniform(-0.3,0.3) for _ in range(H)]
W2=[random.uniform(-1,1) for _ in range(H)]; b2=random.uniform(-0.3,0.3)
X=[[0,0],[0,1],[1,0],[1,1]]; Y=[0,1,1,0]
def fwd(x):
    h=[sig(sum(W1[i][j]*x[j] for j in range(2))+b1[i]) for i in range(H)]
    o=sig(sum(W2[i]*h[i] for i in range(H))+b2); return h,o
def loss():
    return sum(0.5*(fwd(x)[1]-y)**2 for x,y in zip(X,Y))/4
lr=0.6; losses=[loss()]; snap_epochs=[0]; W_snaps=[]
def snapshot(): return ([row[:] for row in W1],b1[:],W2[:],b2)
def setsnap(s):
    global b2
    for i in range(H):
        W1[i][:]=s[0][i]; b1[i]=s[1][i]; W2[i]=s[2][i]
    b2=s[3]
W_snaps.append(snapshot())
for ep in range(1,4001):
    for x,y in zip(X,Y):
        h,o=fwd(x); d2=(o-y)*o*(1-o)
        d1=[(W2[i]*d2)*h[i]*(1-h[i]) for i in range(H)]
        for i in range(H): W2[i]-=lr*d2*h[i]
        b2-=lr*d2
        for i in range(H):
            for j in range(2): W1[i][j]-=lr*d1[i]*x[j]
            b1[i]-=lr*d1[i]
    losses.append(loss())
    if ep in (40,120,400,1200,4000): W_snaps.append(snapshot()); snap_epochs.append(ep)
def boundary(ax,title):
    gx=np.linspace(-0.2,1.2,60); G=np.zeros((60,60))
    for ii,yy in enumerate(gx):
        for jj,xx in enumerate(gx): G[ii,jj]=fwd([xx,yy])[1]
    ax.imshow(G,extent=[-0.2,1.2,-0.2,1.2],origin="lower",cmap="coolwarm",alpha=0.85,vmin=0,vmax=1,aspect="auto")
    for (x1,x2),y in zip(X,Y):
        ax.plot(x1,x2,"o" if y else "X",color="white",ms=11,mew=2,mec="black")
    style(ax); ax.set_xlabel("x1",color="white",fontsize=9); ax.set_ylabel("x2",color="white",fontsize=9)
    ax.set_title(title,color="white",fontsize=10)
# closeup: decision boundary + loss curve
fig=plt.figure(figsize=(9.0,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.06,0.13,0.40,0.78]); boundary(ax,f"XORの決定境界 (精度100%)")
ax2=fig.add_axes([0.57,0.15,0.40,0.74]); style(ax2)
ax2.semilogy(losses,color=BLUE,lw=2)
ax2.set_xlabel("エポック",color="white",fontsize=9); ax2.set_ylabel("MSE損失 (対数)",color="white",fontsize=9)
ax2.set_title(f"損失 {losses[0]:.3f}→{losses[-1]:.4f}",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.12,0.84,0.80]); boundary(axc,"")
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ニューラルネットと","誤差逆伝播","XOR を隠れ層で解く、勾配で重みを学習",cc); os.remove(cc)
# gif: boundary evolving over epochs
frames=[]
for s,ep in zip(W_snaps,snap_epochs):
    setsnap(s)
    fr=plt.figure(figsize=(4.2,3.4)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.12,0.12,0.84,0.80]); boundary(g,f"エポック {ep}: 損失 {loss():.3f}")
    frames.append(figlib.fig_to_pil(fr,dpi=90))
frames+=[frames[-1]]*3
figlib.save_gif(frames,SLUG,duration=600); print("done")
