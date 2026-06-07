# -*- coding: utf-8 -*-
"""quantum-tunneling visuals: barrier+wavefunction + T vs width + width-sweep gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="quantum-tunneling"; NAVY="#0b1020"; CY="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#9be7a3"; PUR="#c084fc"; RED="#fb7185"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
me=9.109e-31; eV=1.602e-19; hbar=1.055e-34; nm=1e-9
def kap(V0,E,m_rel=1): return math.sqrt(2*m_rel*me*(V0-E)*eV)/hbar
def Twkb(V0,E,d_nm,m_rel=1): return math.exp(-2*kap(V0,E,m_rel)*d_nm*nm)
V0,E,d=5,3,1.0; k=kap(V0,E); knm=k*nm; T=Twkb(V0,E,d)
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.07,0.14,0.46,0.78]); style(ax)
x=np.linspace(-3,5,500)
# barrier 0..d (scaled in nm visually)
ax.axvspan(0,d,color=PUR,alpha=0.2); ax.text(d/2,4.6,f"V0={V0}eV",color=PUR,ha="center",fontsize=9)
ax.axhline(E,color=ORANGE,ls="--",lw=1.4); ax.text(-2.8,E+0.15,f"E={E}eV",color=ORANGE,fontsize=8)
# wavefunctions (schematic)
xi=x[x<0]; ax.plot(xi,3+0.7*np.sin(2*np.pi*xi/0.8),color=CY,lw=1.6)
xb=x[(x>=0)&(x<=d)]; ax.plot(xb,3+0.7*np.exp(-k*nm/nm*xb*0)+0.6*np.exp(-knm*xb*3),color=PUR,lw=1.8)
amp=math.sqrt(T)*6
xt=x[x>d]; ax.plot(xt,3+max(amp,0.15)*np.sin(2*np.pi*(xt-d)/0.8),color=GREEN,lw=1.6)
ax.set_ylim(0,5.2); ax.set_xlabel("位置 x [nm]",color="white",fontsize=9); ax.set_ylabel("エネルギー / 波動関数",color="white",fontsize=8)
ax.set_title(f"E<V0 でも染み出して透過 (T={T:.1e})",color="white",fontsize=10)
ax2=fig.add_axes([0.62,0.16,0.35,0.74]); style(ax2)
ds=np.linspace(0.1,3,120); ax2.semilogy(ds,[Twkb(V0,E,dd) for dd in ds],color=CY,lw=2.2,label="電子")
ax2.semilogy(ds,[Twkb(V0,E,dd,1836) for dd in ds],color=RED,lw=2,label="陽子")
ax2.plot(d,T,"o",color=ORANGE)
ax2.legend(facecolor=NAVY,edgecolor="#3b4a6b",labelcolor="white",fontsize=8)
ax2.set_ylim(1e-30,1); ax2.set_xlabel("障壁の幅 d [nm]",color="white",fontsize=9); ax2.set_ylabel("透過確率 T (対数)",color="white",fontsize=8)
ax2.set_title("Tはdに対し指数的に減少",color="white",fontsize=10)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.1,0.14,0.86,0.78]); style(axc)
axc.axvspan(0,d,color=PUR,alpha=0.2); axc.axhline(E,color=ORANGE,ls="--",lw=1.2)
axc.plot(xi,3+0.7*np.sin(2*np.pi*xi/0.8),color=CY,lw=1.6); axc.plot(xb,3+0.6*np.exp(-knm*xb*3),color=PUR,lw=1.8)
axc.plot(xt,3+max(amp,0.15)*np.sin(2*np.pi*(xt-d)/0.8),color=GREEN,lw=1.6); axc.set_ylim(0,5.2); axc.axis("off")
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"量子トンネル効果","","E<V0 でも障壁を透過、T≈e^(-2κd)",cc); os.remove(cc)
frames=[]
for dd in list(np.linspace(0.2,2.5,20))+list(np.linspace(2.5,0.2,8)):
    Tv=Twkb(V0,E,dd); amp=math.sqrt(Tv)*6
    fr=plt.figure(figsize=(4.8,3.0)); fr.patch.set_facecolor(NAVY)
    g=fr.add_axes([0.06,0.1,0.9,0.82]); style(g); g.axis("off")
    g.axvspan(0,dd,color=PUR,alpha=0.2); g.axhline(3,color="#3b4a6b",lw=0.8)
    xi=x[x<0]; g.plot(xi,3+0.7*np.sin(2*np.pi*xi/0.8),color=CY,lw=1.6)
    xb=x[(x>=0)&(x<=dd)]; g.plot(xb,3+0.6*np.exp(-knm*xb*3),color=PUR,lw=1.8)
    xt=x[x>dd]; g.plot(xt,3+max(amp,0.1)*np.sin(2*np.pi*(xt-dd)/0.8),color=GREEN,lw=1.6)
    g.set_ylim(0.5,5); g.set_xlim(-3,5)
    g.set_title(f"障壁幅 d={dd:.1f}nm → T={Tv:.1e}",color="white",fontsize=10)
    frames.append(figlib.fig_to_pil(fr,dpi=90))
figlib.save_gif(frames,SLUG,duration=110); print("done")
