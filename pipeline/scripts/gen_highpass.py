# -*- coding: utf-8 -*-
"""high-pass-filter visuals: Bode magnitude+phase + cutoff sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="high-pass-filter"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; RED="#fb7185"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
R,C=1000,100e-9; fc=1/(2*math.pi*R*C)
f=np.logspace(0,6,300); r=f/fc
gain=20*np.log10(r/np.sqrt(1+r*r)); phase=90-np.degrees(np.arctan(r))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.09,0.15,0.42,0.74]); style(ax)
ax.semilogx(f,gain,color=BLUE,lw=2.3); ax.axvline(fc,color="#3b4a6b",ls=":",lw=1); ax.axhline(-3.01,color=RED,ls="--",lw=1)
ax.plot(fc,-3.01,"o",color=ORANGE); ax.text(fc*1.2,-12,f"fc={fc:.0f}Hz\n-3dB",color=ORANGE,fontsize=8)
ax.set_ylim(-60,5); ax.set_xlabel("周波数 f [Hz]",color="white",fontsize=9); ax.set_ylabel("ゲイン [dB]",color="white",fontsize=9)
ax.set_title("ボード線図(ゲイン): 低域 -20dB/dec",color="white",fontsize=10)
ax2=fig.add_axes([0.59,0.15,0.38,0.74]); style(ax2)
ax2.semilogx(f,phase,color=ORANGE,lw=2.3); ax2.axvline(fc,color="#3b4a6b",ls=":",lw=1); ax2.plot(fc,45,"o",color=BLUE)
ax2.text(fc*1.2,50,"fcで +45°",color=BLUE,fontsize=8)
ax2.set_ylim(0,95); ax2.set_xlabel("周波数 f [Hz]",color="white",fontsize=9); ax2.set_ylabel("位相 [deg]",color="white",fontsize=9)
ax2.set_title("位相: 低域+90°→高域0°",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.13,0.16,0.83,0.78]); style(axc); axc.semilogx(f,gain,color=BLUE,lw=2.4); axc.axhline(-3.01,color=RED,ls="--",lw=1); axc.plot(fc,-3.01,"o",color=ORANGE)
axc.set_ylim(-60,5); axc.set_xlabel("f [Hz]",color="white",fontsize=9); axc.set_ylabel("ゲイン [dB]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"ハイパスフィルタ","","fc=1/(2πRC)、低周波を遮断し高周波を通す",cc); os.remove(cc)
frames=[]
for Cn in list(np.logspace(np.log10(10e-9),np.log10(1000e-9),20))+list(np.logspace(np.log10(1000e-9),np.log10(10e-9),8)):
    fcv=1/(2*math.pi*R*Cn); rr=f/fcv; gg=20*np.log10(rr/np.sqrt(1+rr*rr))
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.13,0.15,0.83,0.76]); style(g)
    g.semilogx(f,gg,color=BLUE,lw=2.2); g.axvline(fcv,color=ORANGE,ls="--",lw=1.4); g.axhline(-3.01,color=RED,ls=":",lw=1)
    g.set_ylim(-60,5); g.set_xlabel("f [Hz]",color="white",fontsize=9); g.set_ylabel("ゲイン [dB]",color="white",fontsize=9)
    g.set_title(f"C={Cn*1e9:.0f}nF → fc={fcv:.0f}Hz",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=100); print("done")
