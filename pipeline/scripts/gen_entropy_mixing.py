# -*- coding: utf-8 -*-
"""entropy-mixing visuals: dS vs composition + mixing gif."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib
SLUG="entropy-mixing"; NAVY="#0b1020"; BLUE="#7dd3fc"; ORANGE="#f59e0b"; GREEN="#63e6be"; RED="#ff6b6b"
def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
R=8.314
# binary dS curve
x=np.linspace(0.001,0.999,400); dS=-R*(x*np.log(x)+(1-x)*np.log(1-x))
fig=plt.figure(figsize=(9.2,4.3)); fig.patch.set_facecolor(NAVY)
ax=fig.add_axes([0.10,0.15,0.42,0.74]); style(ax)
ax.plot(x,dS,color=ORANGE,lw=2.3); ax.axvline(0.5,color="#3b4a6b",ls="--",lw=1)
ax.plot(0.5,R*math.log(2),"o",color=BLUE); ax.annotate(f"x=0.5: {R*math.log(2):.2f} J/K",(0.5,R*math.log(2)),(0.18,5.2),color="white",fontsize=8)
ax.set_xlabel("モル分率 x_1 (二成分)",color="white",fontsize=9); ax.set_ylabel("dS_mix [J/K] (n=1mol)",color="white",fontsize=9)
ax.set_title("等量混合(x=0.5)で混合エントロピー最大",color="white",fontsize=10)
# 3-component default bar
ax2=fig.add_axes([0.60,0.15,0.37,0.74]); style(ax2)
xs=[0.5,0.3,0.2]; comp=[-R*xi*math.log(xi) for xi in xs]
ax2.bar(["x1=0.5","x2=0.3","x3=0.2"],comp,color=[RED,GREEN,BLUE])
ax2.set_ylabel("-R x_i ln x_i への寄与",color="white",fontsize=9)
ax2.set_title(f"3成分 既定: dS=8.56 J/K (最大の93.7%)",color="white",fontsize=9)
cu=os.path.join(figlib.outdir(SLUG),"charts-closeup.png"); figlib.save_fig(fig,cu,dpi=130); print(" closeup")
figc=plt.figure(figsize=(5.2,3.0)); figc.patch.set_facecolor(NAVY)
axc=figc.add_axes([0.16,0.17,0.80,0.74]); style(axc); axc.plot(x,dS,color=ORANGE,lw=2.4); axc.axvline(0.5,color="#3b4a6b",ls="--",lw=1)
axc.set_xlabel("x_1",color="white",fontsize=9); axc.set_ylabel("dS_mix [J/K]",color="white",fontsize=9)
cc=os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc,cc,dpi=120)
figlib.make_cover(SLUG,"混合エントロピー","","dS_mix = -nR sum x_i ln x_i、混ざるほど増大",cc); os.remove(cc)
# gif: two gases mixing (particles spreading across a removed partition)
rng=np.random.default_rng(7)
NA=120; NB=80
ax_=rng.uniform(0,0.45,NA); ay=rng.uniform(0,1,NA); bx=rng.uniform(0.55,1,NB); by=rng.uniform(0,1,NB)
frames=[]; N=40
for kf in range(N):
    t=kf/(N-1)
    axp=ax_+(rng.uniform(0,1,NA)-ax_)*t; bxp=bx+(rng.uniform(0,1,NB)-bx)*t
    f=plt.figure(figsize=(4.8,3.0)); f.patch.set_facecolor(NAVY)
    a=f.add_axes([0.02,0.02,0.96,0.88]); a.set_facecolor(NAVY); a.set_xlim(0,1); a.set_ylim(0,1); a.axis("off")
    if t<0.05: a.axvline(0.5,color="#9fb2d6",lw=2)
    a.scatter(axp,ay,s=14,color=RED); a.scatter(bxp,by,s=14,color=BLUE)
    a.text(0.5,1.04,"仕切りを外すと2気体が混ざりエントロピー増大",color="white",ha="center",fontsize=8)
    frames.append(figlib.fig_to_pil(f,dpi=92))
figlib.save_gif(frames,SLUG,duration=110); print("done")
