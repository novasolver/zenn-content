# -*- coding: utf-8 -*-
"""autocorrelation visuals: noisy signal + ACF with peak + noise-sweep gif.
Replicates tool's LCG (seed=42) for consistency."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="autocorrelation"; NAVY="#0b1020"; BLUE="#00B4D8"; ORANGE="#f59e0b"; RED="#E74C3C"; YEL="#FFD166"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def lcg(seed):
    s=[seed&0xFFFFFFFF]
    def r():
        s[0]=(s[0]*1103515245+12345)&0xFFFFFFFF; return s[0]/4294967296
    return r
def gen(A,f0,sigma,N,seed=42):
    rng=lcg(seed); sp=[None]
    def g():
        if sp[0] is not None:
            v=sp[0];sp[0]=None;return v
        u1=max(rng(),1e-12);u2=rng();mag=math.sqrt(-2*math.log(u1))
        sp[0]=mag*math.sin(2*math.pi*u2);return mag*math.cos(2*math.pi*u2)
    return np.array([A*math.sin(2*math.pi*f0*n)+sigma*g() for n in range(N)])
def acf(x):
    N=len(x); K=N//2; R=np.array([np.sum(x[:N-k]*x[k:])/N for k in range(K+1)])
    return R/R[0]
A,f0,sigma,N=1.0,0.05,0.5,512
x=gen(A,f0,sigma,N); rho=acf(x)
# peak
kStart=1
for k in range(1,len(rho)):
    if rho[k]<0: kStart=k;break
peakK=int(max(range(kStart,len(rho)-1),key=lambda k:rho[k]))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.08,0.58,0.88,0.34]); style(ax)
ax.plot(x[:200],color=BLUE,lw=0.9)
ax.set_xlabel("サンプル n (周期20が雑音に埋もれている)",color="white",fontsize=8); ax.set_ylabel("信号 x[n]",color="white",fontsize=8)
ax.set_title("ノイズまみれの信号 (σ=0.5, SNR=6dB)",color="white",fontsize=10)
ax2=fig.add_axes([0.08,0.12,0.88,0.34]); style(ax2)
ax2.plot(rho,color=RED,lw=1.4); ax2.axhline(0,color="#3b4a6b",lw=1)
ax2.axvline(peakK,color=YEL,lw=1.4); ax2.text(peakK+4,0.5,f"ピーク lag={peakK}\n=周期20",color=YEL,fontsize=8)
ax2.set_xlabel("ラグ k",color="white",fontsize=8); ax2.set_ylabel("正規化相関 ρ[k]",color="white",fontsize=8)
ax2.set_title("自己相関: ラグ20にピーク→周期検出",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.12,0.16,0.84,0.78]); style(axc); axc.plot(rho,color=RED,lw=1.6); axc.axhline(0,color="#3b4a6b",lw=1); axc.axvline(peakK,color=YEL,lw=1.4)
axc.set_xlabel("ラグ k",color="white",fontsize=9); axc.set_ylabel("ρ[k]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"自己相関と","周期性検出","R(τ)=Σx(t)x(t+τ)、雑音中の周期を見つける",cc); os.remove(cc)
frames=[]
for sg in list(np.linspace(0.1,2.0,18))+list(np.linspace(2.0,0.1,8)):
    xx=gen(A,f0,sg,N); rr=acf(xx)
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.15,0.83,0.76]); style(g)
    g.plot(rr,color=RED,lw=1.3); g.axhline(0,color="#3b4a6b",lw=1); g.axvline(20,color=YEL,ls="--",lw=1)
    g.set_ylim(-0.6,1.05); g.set_xlabel("ラグ k",color="white",fontsize=9); g.set_ylabel("ρ[k]",color="white",fontsize=9)
    g.set_title(f"ノイズ σ={sg:.1f}: 周期20のピークは残る",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
