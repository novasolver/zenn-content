# -*- coding: utf-8 -*-
"""Adam optimizer visuals. Faithful to the tool: f=0.5(a x^2 + b y^2), a=1,b=20,
start (-9,4), lr=0.1, b1=0.9, b2=0.999. Contour + trajectory vs plain GD."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "adam-optimizer"
NAVY = "#020d1a"
CYAN, ORANGE, YELLOW, GREEN = "#00B4D8", "#e17055", "#ffd24b", "#00b894"
EPS = 1e-8
A, B = 1.0, 20.0
START = (-9.0, 4.0)

def run_adam(lr, b1, b2, steps, a=A, b=B):
    x, y = START
    mx=my=vx=vy=0.0
    traj=[(x,y)]
    for i in range(steps):
        t=i+1
        gx=a*x; gy=b*y
        mx=b1*mx+(1-b1)*gx; my=b1*my+(1-b1)*gy
        vx=b2*vx+(1-b2)*gx*gx; vy=b2*vy+(1-b2)*gy*gy
        mhx=mx/(1-b1**t); mhy=my/(1-b1**t)
        vhx=vx/(1-b2**t); vhy=vy/(1-b2**t)
        x-=lr*mhx/(np.sqrt(vhx)+EPS); y-=lr*mhy/(np.sqrt(vhy)+EPS)
        traj.append((x,y))
    return np.array(traj)

def run_gd(lr, steps, a=A, b=B):
    x,y=START; traj=[(x,y)]
    for i in range(steps):
        x-=lr*a*x; y-=lr*b*y
        if abs(x)>1e6 or abs(y)>1e6: break
        traj.append((x,y))
    return np.array(traj)

def loss(traj, a=A, b=B):
    return 0.5*(a*traj[:,0]**2 + b*traj[:,1]**2)

def draw_contour(ax, adam_tr, gd_tr=None, title=None, a=A, b=B):
    ax.set_facecolor(NAVY)
    xr=np.linspace(-11,11,250); yr=np.linspace(-6,6,200)
    X,Y=np.meshgrid(xr,yr); Z=0.5*(a*X**2+b*Y**2)
    levels=[0.5,2,6,15,35,70,130]
    ax.contour(X,Y,Z,levels=levels,colors="#00b4d8",alpha=0.30,linewidths=0.8)
    if gd_tr is not None:
        ax.plot(gd_tr[:,0],gd_tr[:,1],color=ORANGE,lw=1.6,ls="--",label="通常GD")
    # color gradient along adam path
    n=len(adam_tr)
    ax.plot(adam_tr[:,0],adam_tr[:,1],color=CYAN,lw=2.2,label="Adam")
    ax.scatter(adam_tr[::3,0],adam_tr[::3,1],s=8,color=CYAN,zorder=3)
    ax.scatter([START[0]],[START[1]],s=60,color=YELLOW,zorder=5,label="スタート (−9,4)")
    ax.scatter([0],[0],s=70,color=GREEN,marker="*",zorder=5,label="最小値 (0,0)")
    ax.set_xlabel("x", color="white", fontsize=9); ax.set_ylabel("y", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.set_xlim(-11,11); ax.set_ylim(-6,6)
    if title: ax.set_title(title, color="white", fontsize=10)

adam_tr = run_adam(0.1,0.9,0.999,150)
gd_marg = run_gd(0.1,150)        # marginal -> oscillates
print(f"Adam final loss={loss(adam_tr)[-1]:.4f}  GD(lr=0.1) final loss={loss(gd_marg)[-1]:.4f}")

# ---- closeup: contour+trajectory (left) + loss-vs-iteration log (right) ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07,0.14,0.52,0.76]); draw_contour(ax1, adam_tr, gd_marg, "損失曲面の等高線と最適化軌跡")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7, loc="upper right")
ax2 = fig.add_axes([0.67,0.16,0.30,0.72]); ax2.set_facecolor(NAVY)
La=loss(adam_tr); Lg=loss(gd_marg)
ax2.semilogy(range(len(La)), La, color=CYAN, lw=2.0, label="Adam")
ax2.semilogy(range(len(Lg)), Lg, color=ORANGE, lw=1.8, ls="--", label="通常GD (α=0.1)")
ax2.set_xlabel("反復回数", color="white", fontsize=9); ax2.set_ylabel("損失 f (log)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)
ax2.set_title("損失の収束（Adam は単調減少）", color="white", fontsize=9)
ax2.grid(True, color="#1e2d44", lw=0.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10,0.12,0.86,0.82]); draw_contour(axc, adam_tr, gd_marg)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "Adam オプティマイザ", "", "モメント + 適応的学習率で谷を降りる", cc)
os.remove(cc)

# ---- gif: sweep learning rate, show trajectory change ----
frames=[]
lrs = [0.02,0.05,0.1,0.2,0.35,0.5,0.7,0.9]
lrs = lrs + lrs[::-1]
for lr in lrs:
    tr = run_adam(lr,0.9,0.999,150)
    fl = loss(tr)[-1]
    diverged = (not np.all(np.isfinite(tr))) or np.max(np.abs(tr))>1e6
    f2 = plt.figure(figsize=(5.2,3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.10,0.15,0.86,0.76])
    # clip trajectory for display
    trc = tr[np.all(np.abs(tr)<1e3, axis=1)]
    draw_contour(a, trc if len(trc)>1 else tr[:2])
    tag = "発散" if diverged else f"最終損失 f={fl:.3f}"
    a.set_title(f"α={lr:.2f}  →  {tag}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=140)
print("done.")
