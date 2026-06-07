# -*- coding: utf-8 -*-
"""wheatstone-bridge visuals: bridge diagram + Vout vs R4 + R4-sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="wheatstone-bridge"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#00b894"; RED="#e74c3c"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
Vin=5.0
def vout(R1,R2,R3,R4): return Vin*(R2/(R1+R2)-R4/(R3+R4))*1000
def draw_bridge(ax,R4):
    ax.set_facecolor(NAVY); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect("equal")
    T=(0.5,0.92); B=(0.5,0.08); L=(0.12,0.5); Rg=(0.88,0.5)
    for p,q,lab,c in [(T,L,"R1",BLUE),(T,Rg,"R2",BLUE),(L,B,"R3",ORANGE),(Rg,B,"R4",ORANGE)]:
        ax.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=2.5)
        ax.text((p[0]+q[0])/2+0.02,(p[1]+q[1])/2+0.03,lab,color="white",fontsize=10)
    for pt in (T,B,L,Rg): ax.add_patch(plt.Circle(pt,0.025,color="#9fb2d6"))
    ax.text(T[0],T[1]+0.05,"Vin=5V",color=GREEN,ha="center",fontsize=9)
    ax.text(B[0],B[1]-0.06,"GND",color="#9fb2d6",ha="center",fontsize=9)
    vo=vout(1000,1000,1000,R4)
    bal=abs(vo)<1
    ax.plot([L[0],Rg[0]],[L[1],Rg[1]],color=GREEN if bal else RED,lw=1.6,ls="--")
    ax.text(0.5,0.5,f"Vg={vo:.1f}mV",color=GREEN if bal else RED,ha="center",fontsize=10,
            bbox=dict(boxstyle="round",fc=NAVY,ec=GREEN if bal else RED))
fig=plt.figure(figsize=(9.0,4.3)); fig.patch.set_facecolor(NAVY)
axb=fig.add_axes([0.02,0.05,0.45,0.9]); draw_bridge(axb,1010)
axb.set_title("ブリッジ回路 (R4=1010Ω, 不平衡)",color="white",fontsize=10)
ax2=fig.add_axes([0.57,0.16,0.40,0.74]); style(ax2)
R4s=np.linspace(900,1100,200); ax2.plot(R4s,[vout(1000,1000,1000,r) for r in R4s],color=BLUE,lw=2.2)
ax2.axhline(0,color="#3b4a6b",lw=1); ax2.axvline(1000,color=GREEN,ls="--",lw=1.2); ax2.text(1002,8,"平衡 R4=1000Ω",color=GREEN,fontsize=8)
ax2.plot(1010,vout(1000,1000,1000,1010),"o",color=ORANGE); ax2.annotate("R4=1010: -12.4mV",(1010,vout(1000,1000,1000,1010)),(1015,-9),color="white",fontsize=8)
ax2.set_xlabel("R4 [Ω]",color="white",fontsize=9); ax2.set_ylabel("出力電圧 Vout [mV]",color="white",fontsize=9)
ax2.set_title("R4が平衡値から外れると出力が出る",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.0,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.0,0.0,1.0,1.0]); draw_bridge(axc,1010)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ホイートストン","ブリッジ","Vout=Vin(R2/(R1+R2)-R4/(R3+R4))、平衡で出力0",cc); os.remove(cc)
frames=[]
for R4 in list(np.linspace(950,1050,22))+list(np.linspace(1050,950,8)):
    fr=plt.figure(figsize=(4.0,3.6)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.0,0.04,1.0,0.88]); draw_bridge(g,R4)
    g.set_title(f"R4={R4:.0f}Ω",color="white",fontsize=11)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
