# -*- coding: utf-8 -*-
"""helmholtz-resonator visuals: geometry + f vs V (log-log) + volume sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="helmholtz-resonator"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
def helm(V_L,dn_mm=20,L_mm=50,c=343):
    V=V_L*1e-3; rn=(dn_mm/2)/1000; A=math.pi*rn*rn; Leff=L_mm/1000+1.7*rn
    return c/(2*math.pi)*math.sqrt(A/(V*Leff))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
# geometry (bottle)
axg=fig.add_axes([0.03,0.08,0.40,0.84]); axg.set_facecolor(NAVY); axg.axis("off"); axg.set_xlim(0,1); axg.set_ylim(0,1)
axg.add_patch(plt.Rectangle((0.25,0.1),0.5,0.45,color=BLUE,alpha=0.3,ec=BLUE,lw=2))   # cavity
axg.add_patch(plt.Rectangle((0.42,0.55),0.16,0.28,color=ORANGE,alpha=0.4,ec=ORANGE,lw=2)) # neck
axg.text(0.5,0.32,"空洞 V\n(バネ)",color="white",ha="center",fontsize=10)
axg.text(0.5,0.69,"首\nA, L",color="white",ha="center",fontsize=9)
axg.annotate("",xy=(0.5,0.95),xytext=(0.5,0.83),arrowprops=dict(arrowstyle="<->",color=GREEN,lw=2))
axg.text(0.62,0.89,"空気の出入り\n(おもり)",color=GREEN,fontsize=8)
axg.set_title("ヘルムホルツ共鳴器=バネ-質量系",color="white",fontsize=10)
# f vs V
ax2=fig.add_axes([0.55,0.16,0.42,0.74]); style(ax2)
Vs=np.logspace(np.log10(0.05),np.log10(20),120)
ax2.loglog(Vs,[helm(v) for v in Vs],color=BLUE,lw=2.3)
ax2.plot(1.0,helm(1.0),"o",color=ORANGE); ax2.annotate(f"V=1L: {helm(1.0):.0f}Hz",(1.0,helm(1.0)),(1.5,helm(1.0)+30),color="white",fontsize=8)
ax2.set_xlabel("空洞体積 V [L] (対数)",color="white",fontsize=9); ax2.set_ylabel("共鳴周波数 f [Hz] (対数)",color="white",fontsize=8)
ax2.set_title("f ∝ 1/√V (大きい容器ほど低い音)",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.14,0.17,0.82,0.74]); style(axc); axc.loglog(Vs,[helm(v) for v in Vs],color=BLUE,lw=2.4); axc.plot(1.0,helm(1.0),"o",color=ORANGE)
axc.set_xlabel("V [L]",color="white",fontsize=9); axc.set_ylabel("f [Hz]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ヘルムホルツ共鳴器","","f=(c/2π)√(A/(V·L_eff))、ビンが鳴る原理",cc); os.remove(cc)
frames=[]
for V in list(np.linspace(0.2,5,26))+list(np.linspace(5,0.2,12)):
    fr=plt.figure(figsize=(4.6,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.0,0.0,1,1]); g.set_facecolor(NAVY); g.axis("off"); g.set_xlim(0,1); g.set_ylim(0,1)
    s=0.3+0.5*(V/5)**0.5
    g.add_patch(plt.Rectangle((0.5-s/2,0.12),s,0.4*s/0.5,color=BLUE,alpha=0.3,ec=BLUE,lw=2))
    g.add_patch(plt.Rectangle((0.42,0.12+0.4*s/0.5),0.16,0.22,color=ORANGE,alpha=0.4,ec=ORANGE,lw=2))
    g.text(0.5,0.9,f"V={V:.1f}L → f={helm(V):.0f}Hz",color="white",ha="center",fontsize=11)
    frames.append(figlib.fig_to_pil(g.figure,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
