# -*- coding: utf-8 -*-
"""kalman-filter visuals: true/measured/estimate (GPS preset) + K&P + tracking gif.
Replicates tool's seeded LCG + Box-Muller for consistency."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="kalman-filter"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; RED="#fb7185"; PUR="#c084fc"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def run(Q,R,P0,freq,noiseAmp,N=80,dt=0.1):
    s=[42]
    def rnd():
        s[0]=(s[0]*9301+49297)%233280; return s[0]/233280
    spare=[None]
    def gauss():
        if spare[0] is not None:
            v=spare[0];spare[0]=None;return v
        u1=max(rnd(),1e-12);u2=rnd();mag=math.sqrt(-2*math.log(u1))
        spare[0]=mag*math.sin(2*math.pi*u2); return mag*math.cos(2*math.pi*u2)
    xh=0.0;P=P0; T=[];TR=[];Z=[];KA=[];GA=[];CO=[]
    for i in range(N):
        t=i*dt;truth=math.sin(2*math.pi*freq*t);z=truth+gauss()*noiseAmp
        xp=xh;Pp=P+Q;K=Pp/(Pp+R);xh=xp+K*(z-xp);P=(1-K)*Pp
        T.append(t);TR.append(truth);Z.append(z);KA.append(xh);GA.append(K);CO.append(P)
    rr=math.sqrt(sum((Z[i]-TR[i])**2 for i in range(N))/N); rk=math.sqrt(sum((KA[i]-TR[i])**2 for i in range(N))/N)
    return map(np.array,(T,TR,Z,KA,GA,CO)),rr,rk
# GPS preset: Q=10^-2.5, R=10, P0=1, freq=0.5, noise=1.2
(arrs),rr,rk=run(10**-2.5,10.0,1.0,0.5,1.2)
T,TR,Z,KA,GA,CO=arrs
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.08,0.14,0.55,0.76]); style(ax)
ax.plot(T,Z,"o",color=RED,ms=3,alpha=0.6,label="観測値(ノイズ)")
ax.plot(T,TR,color=GREEN,lw=2.4,label="真値")
ax.plot(T,KA,color=BLUE,lw=2.2,label="カルマン推定")
ax.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax.set_xlabel("時刻 [s]",color="white",fontsize=9); ax.set_ylabel("位置",color="white",fontsize=9)
ax.set_title(f"GPSプリセット: RMSE {rr:.2f}→{rk:.2f} ({(1-rk/rr)*100:.0f}%改善)",color="white",fontsize=10)
ax2=fig.add_axes([0.70,0.16,0.27,0.74]); style(ax2)
ax2.plot(T,GA,color=ORANGE,lw=2,label="ゲイン K"); ax2.plot(T,CO,color=PUR,lw=2,label="共分散 P")
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_xlabel("時刻 [s]",color="white",fontsize=9); ax2.set_title("K・P は定常へ収束",color="white",fontsize=9)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.4,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.1,0.16,0.86,0.78]); style(axc)
axc.plot(T,Z,"o",color=RED,ms=3,alpha=0.6); axc.plot(T,TR,color=GREEN,lw=2.4); axc.plot(T,KA,color=BLUE,lw=2.2)
axc.set_xlabel("時刻 [s]",color="white",fontsize=9); axc.set_ylabel("位置",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"カルマンフィルタ","","予測と観測を最適に融合してノイズ除去",cc); os.remove(cc)
frames=[]; N=len(T)
for j in range(8,N+1,4):
    fr=plt.figure(figsize=(5.0,2.9)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.1,0.16,0.86,0.76]); style(g)
    g.plot(T[:j],Z[:j],"o",color=RED,ms=3,alpha=0.6); g.plot(T[:j],TR[:j],color=GREEN,lw=2.2); g.plot(T[:j],KA[:j],color=BLUE,lw=2)
    g.set_xlim(0,T[-1]); g.set_ylim(-3.5,3.5)
    g.set_xlabel("時刻 [s]",color="white",fontsize=9); g.set_ylabel("位置",color="white",fontsize=9)
    g.set_title("推定が真値を追従していく",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=90); print("done")
