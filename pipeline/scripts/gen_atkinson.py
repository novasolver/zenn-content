# -*- coding: utf-8 -*-
"""Atkinson cycle visuals. Faithful to the tool: R_AIR=287, eta=1-cp(T4-T1)/qIn,
over-expansion to intake pressure P1. P-V diagram + efficiency-vs-r curve."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "atkinson-cycle"
NAVY = "#0b1020"
CYAN, ORANGE, BLUE, GREEN, YELLOW = "#00B4D8", "#e17055", "#7dd3fc", "#9be7a3", "#ffd24b"
R_AIR = 287.0

def cycle(r, g, T1, P1, qIn):
    cv = R_AIR/(g-1); cp = g*cv
    T2 = T1*r**(g-1); P2 = P1*r**g
    T3 = T2 + (qIn*1000)/cv; P3 = P2*T3/T2
    T4 = T3*(P1/P3)**((g-1)/g)
    rExp = (P3/P1)**(1/g)
    eta = 1 - cp*(T4-T1)/(qIn*1000)
    etaOtto = 1 - 1/r**(g-1)
    # relative volumes, V2=1
    V2 = 1.0; V1 = r; V4 = rExp
    return dict(V1=V1,V2=V2,V4=V4,P1=P1,P2=P2,P3=P3,eta=eta,etaOtto=etaOtto,rExp=rExp)

def pv_path(c, g):
    V1,V2,V4,P1,P2,P3 = c['V1'],c['V2'],c['V4'],c['P1'],c['P2'],c['P3']
    xs=[]; ys=[]
    # 1->2 compression
    V = np.linspace(V1,V2,40); xs += list(V); ys += list(P1*(V1/V)**g)
    # 2->3 const volume
    P = np.linspace(P2,P3,12); xs += [V2]*12; ys += list(P)
    # 3->4 expansion
    V = np.linspace(V2,V4,50); xs += list(V); ys += list(P3*(V2/V)**g)
    # 4->1 const pressure
    V = np.linspace(V4,V1,16); xs += list(V); ys += [P1]*16
    return np.array(xs), np.array(ys)

def draw_pv(ax, r, g, T1, P1, qIn, title=None, legend=True):
    ax.set_facecolor(NAVY)
    c = cycle(r,g,T1,P1,qIn)
    x,y = pv_path(c,g)
    ax.fill(x, y, color=CYAN, alpha=0.16)
    ax.plot(x, y, color=CYAN, lw=2.3)
    # highlight expansion stroke 3->4
    V = np.linspace(c['V2'],c['V4'],50)
    ax.plot(V, c['P3']*(c['V2']/V)**g, color=ORANGE, lw=3.2, label="3→4 完全膨張")
    # state points
    pts = [(c['V1'],c['P1'],'1'),(c['V2'],c['P2'],'2'),(c['V2'],c['P3'],'3'),(c['V4'],c['P1'],'4')]
    for vx,py,nm in pts:
        ax.plot(vx,py,'o',color=YELLOW,ms=6)
        ax.annotate(nm,(vx,py),textcoords="offset points",xytext=(6,4),color="white",fontsize=9,fontweight="bold")
    ax.set_xlabel("体積 V（相対値, V₂=1）", color="white", fontsize=9)
    ax.set_ylabel("圧力 P (kPa)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if legend: ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
    if title: ax.set_title(title, color="white", fontsize=10)
    return c

# defaults
r,g,T1,P1,qIn = 10,1.4,300,100,1800
c = cycle(r,g,T1,P1,qIn)
print(f"default eta={c['eta']*100:.1f}% etaOtto={c['etaOtto']*100:.1f}% rExp={c['rExp']:.2f}")

# closeup: P-V + efficiency vs r
fig = plt.figure(figsize=(9.6,4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08,0.15,0.50,0.74]); draw_pv(ax1,r,g,T1,P1,qIn,"P-V 線図（アトキンソンサイクル）")
ax2 = fig.add_axes([0.66,0.16,0.31,0.72]); ax2.set_facecolor(NAVY)
rs = np.linspace(8,16,40)
etaA = [cycle(rv,g,T1,P1,qIn)['eta']*100 for rv in rs]
etaO = [(1-1/rv**(g-1))*100 for rv in rs]
ax2.plot(rs,etaA,color=CYAN,lw=2.3,label="アトキンソン")
ax2.plot(rs,etaO,color=ORANGE,lw=2.0,ls="--",label="オットー")
ax2.plot(10, c['eta']*100,'o',color=GREEN,ms=8)
ax2.set_xlabel("圧縮比 r", color="white", fontsize=9)
ax2.set_ylabel("熱効率 η (%)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
ax2.set_title("熱効率 vs 圧縮比", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG),"charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13,0.13,0.83,0.81]); draw_pv(axc,r,g,T1,P1,qIn,legend=False)
cc = os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG,"アトキンソン","サイクル","膨張行程を長くして捨てる熱を回収する過膨張サイクル", cc)
os.remove(cc)

# gif: sweep compression ratio
frames=[]
rseq = list(range(8,17,1)) + list(range(15,8,-1))
for rv in rseq:
    cv2 = cycle(rv,g,T1,P1,qIn)
    f2 = plt.figure(figsize=(5.2,3.5)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13,0.16,0.83,0.74]); draw_pv(a,rv,g,T1,P1,qIn,legend=False)
    a.set_title(f"r={rv}  η_Atk={cv2['eta']*100:.1f}%  η_Otto={cv2['etaOtto']*100:.1f}%",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=140)
print("done.")
