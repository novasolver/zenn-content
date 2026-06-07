# -*- coding: utf-8 -*-
"""rankine-cycle visuals: T-s dome+cycle + eta vs boiler P + energy split gif.
Replicates the tool's own approximate steam model for consistency with the simulator."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="rankine-cycle"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#2ecc71"; YEL="#ffd24b"; GRY="#8fb8e0"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def satWater(P):
    Tsat=42.6776*P**0.2514+111.9*math.log(P+0.001)+15.0
    T=max(0,min(374,Tsat)); Tk=T+273.15
    hf=4.2*T-0.002*T*T; hfg=2500-2.36*T-0.002*T*T; hg=hf+hfg
    sf=4.2*math.log(Tk/273.15); sfg=hfg/Tk; sg=sf+sfg
    return dict(T=T,hf=hf,hg=hg,hfg=hfg,sf=sf,sg=sg,sfg=sfg)
def superheat(T_C,P):
    sat=satWater(P); dT=T_C-sat["T"]; cp=2.1+0.0025*(T_C+sat["T"])/2
    return sat["hg"]+cp*dT, sat["sg"]+cp*math.log((T_C+273.15)/(sat["T"]+273.15))
def isen_exp(s3,h3,Plow):
    sat=satWater(Plow)
    if s3>=sat["sg"]:
        cp=1.9; return max(sat["hg"],h3-cp*(sat["T"]*(s3-sat["sg"]))),1.0
    x=(s3-sat["sf"])/sat["sfg"]; return sat["hf"]+x*sat["hfg"], x
def rankine(Phigh,Plow_kPa,eta_t=0.85,eta_p=0.80):
    Plow=Plow_kPa/1000; sl=satWater(Plow); sh=satWater(Phigh)
    h1=sl["hf"]; wp=0.001*(Phigh-Plow)*1000/eta_p; h2=h1+wp
    T3=sh["T"]+20; h3,s3=superheat(T3,Phigh); h4s,x4s=isen_exp(s3,h3,Plow)
    wt=(h3-h4s)*eta_t; h4=h3-wt; wnet=wt-wp; qin=h3-h2
    return wnet/qin, wnet, qin, wt, wp, x4s
# dome
Ts=np.linspace(2,360,80); domeS=[]; domeT=[]
for T in Ts:
    # invert satWater(P).T ~ T via bisection
    lo,hi=0.001,22.1
    for _ in range(40):
        mid=(lo+hi)/2
        if satWater(mid)["T"]<T: lo=mid
        else: hi=mid
    s=satWater((lo+hi)/2); domeS.append(s)
liqS=[d["sf"] for d in domeS]; vapS=[d["sg"] for d in domeS]; domT=list(Ts)
# cycle points (default)
Phigh=3.0; Plow=0.01; sl=satWater(Plow); sh=satWater(Phigh)
T3=sh["T"]+20; h3,s3=superheat(T3,Phigh); h4s,x4=isen_exp(s3,h3,Plow)
s1=sl["sf"]; s4=sl["sf"]+x4*sl["sfg"]
eta,wnet,qin,wt,wp,_=rankine(3.0,10)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.14,0.42,0.76]); style(ax)
ax.plot(liqS,domT,color=GRY,lw=1.4); ax.plot(vapS,domT,color=GRY,lw=1.4)
# cycle path approx: 1(sl.sf,sl.T)->2(~same)->3(s3,T3)->4(s4,sl.T)->1
cx=[s1,s1,s3,s4,s1]; cy=[sl["T"],sl["T"]+2,T3,sl["T"],sl["T"]]
ax.plot(cx,cy,color=BLUE,lw=2.2)
for s,T,n in [(s1,sl["T"],"1,2"),(s3,T3,"3"),(s4,sl["T"],"4")]:
    ax.plot(s,T,"o",color=YEL,ms=5); ax.annotate(n,(s,T),(s+0.1,T+12),color="white",fontsize=8)
ax.set_xlabel("エントロピー s [kJ/kg/K]",color="white",fontsize=9); ax.set_ylabel("温度 T [C]",color="white",fontsize=9)
ax.set_title("T-s線図と飽和ドーム(近似モデル)",color="white",fontsize=10)
ax2=fig.add_axes([0.61,0.15,0.36,0.74]); style(ax2)
Ps=np.linspace(1,22,120); ax2.plot(Ps,[rankine(P,10)[0]*100 for P in Ps],color=ORANGE,lw=2.3)
ax2.plot(3.0,eta*100,"o",color=BLUE); ax2.annotate(f"3MPa: {eta*100:.1f}%",(3,eta*100),(4,eta*100-3),color="white",fontsize=8)
ax2.set_xlabel("ボイラ圧力 [MPa]",color="white",fontsize=9); ax2.set_ylabel("熱効率 [%]",color="white",fontsize=9)
ax2.set_title("圧力を上げると効率が上がる",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.16,0.80,0.78]); style(axc)
axc.plot(liqS,domT,color=GRY,lw=1.4); axc.plot(vapS,domT,color=GRY,lw=1.4); axc.plot(cx,cy,color=BLUE,lw=2.4)
axc.set_xlabel("s",color="white",fontsize=9); axc.set_ylabel("T [C]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ランキンサイクル","(蒸気動力)","ポンプ仕事は微小、効率は圧力で決まる",cc); os.remove(cc)
# gif: energy bars (qin split into wnet + qout) sweeping boiler pressure
frames=[]
for P in list(np.linspace(2,20,28))+list(np.linspace(20,2,12)):
    e,wn,qi,wt_,wp_,_=rankine(P,10)
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.14,0.16,0.82,0.74]); style(a)
    a.bar(["投入熱 qin","正味仕事 wnet"],[qi,wn],color=[ORANGE,GREEN])
    a.set_ylim(0,3200); a.set_ylabel("kJ/kg",color="white",fontsize=9)
    a.set_title(f"ボイラ {P:.1f}MPa : eta={e*100:.1f}%",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(f,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
