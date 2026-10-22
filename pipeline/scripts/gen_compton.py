# -*- coding: utf-8 -*-
"""Compton scattering visuals. dLambda=lambda_C(1-cos theta), Ef=Ein/(1+alpha(1-cos)).
Faithful to the tool (lambda_C=2.4263 pm, mec2=511 keV, hc=1239.84 keV*pm)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "compton-scattering"
NAVY = "#0a1929"
LAMBDA_C = 2.4263102387
MEC2 = 510.99895
HC = 1239.84193

def dlam(thetaDeg): return LAMBDA_C*(1-np.cos(np.radians(thetaDeg)))
def Ef(Ein, thetaDeg):
    a = Ein/MEC2
    return Ein/(1+a*(1-np.cos(np.radians(thetaDeg))))

def draw_geometry(ax, Ein=100, thetaDeg=90):
    ax.set_facecolor(NAVY)
    th = np.radians(thetaDeg)
    a = Ein/MEC2
    phiE = np.degrees(np.arctan((1/np.tan(th/2))/(1+a))) if 0.01<thetaDeg<179.99 else (90 if thetaDeg<=0.01 else 0)
    L = 1.0
    # incoming photon (wave, from left)
    xs = np.linspace(-L, -0.06, 300)
    ax.plot(xs, 0.05*np.sin(2*np.pi*xs/0.10), color="#FFD166", lw=1.8)
    ax.annotate("", xy=(-0.04,0), xytext=(-0.12,0),
                arrowprops=dict(arrowstyle="-|>", color="#FFD166", lw=1.6))
    ax.text(-L, 0.16, f"λ_in, E_in={Ein:.0f} keV", color="#FFD166", fontsize=8.5)
    # scattered photon at +theta (up-right)
    sx, sy = L*np.cos(th), L*np.sin(th)
    t = np.linspace(0.06, L, 300)
    px, py = t*np.cos(th), t*np.sin(th)
    perp = np.array([-np.sin(th), np.cos(th)])
    ax.plot(px+perp[0]*0.05*np.sin(2*np.pi*t/0.12),
            py+perp[1]*0.05*np.sin(2*np.pi*t/0.12), color="#00B4D8", lw=1.8)
    ax.annotate("", xy=(sx,sy), xytext=(sx*0.92, sy*0.92),
                arrowprops=dict(arrowstyle="-|>", color="#00B4D8", lw=1.6))
    ax.text(sx*0.7+0.05, sy*0.7+0.10, f"λ_f, E_f={Ef(Ein,thetaDeg):.1f} keV",
            color="#00B4D8", fontsize=8.5)
    # recoil electron at -phiE
    pe = np.radians(-phiE)
    ex, ey = L*0.85*np.cos(pe), L*0.85*np.sin(pe)
    ax.annotate("", xy=(ex,ey), xytext=(0.05,0),
                arrowprops=dict(arrowstyle="-|>", color="#FF6B6B", lw=2.0))
    ax.text(ex*0.7, ey-0.12, f"e- φ_e={phiE:.1f}°", color="#FF6B6B", fontsize=8.5)
    # target
    ax.plot(0,0,"o", color="#5cd6a8", ms=9)
    ax.text(0.04,-0.10,"e-", color="#5cd6a8", fontsize=9)
    ax.text(-L, -0.95, f"Δλ={dlam(thetaDeg):.3f} pm  (θ={thetaDeg:.0f}°)",
            color="#cfe3f7", fontsize=9)
    ax.set_xlim(-1.15,1.15); ax.set_ylim(-1.05,1.05)
    ax.set_aspect("equal"); ax.axis("off")

def draw_shift_curve(ax, thetaDeg=90):
    ax.set_facecolor(NAVY)
    th = np.linspace(0,180,361)
    ax.plot(th, dlam(th), color="#00B4D8", lw=2.5)
    ax.axhline(2*LAMBDA_C, color="#5cd6a8", ls="--", lw=1)
    ax.text(5, 2*LAMBDA_C+0.06, f"2λ_C={2*LAMBDA_C:.3f} pm", color="#5cd6a8", fontsize=8)
    ax.axvline(thetaDeg, color="#FFD166", lw=1)
    ax.plot(thetaDeg, dlam(thetaDeg), "o", color="#FFD166", ms=7)
    ax.set_xlabel("散乱角 θ (deg)", color="white", fontsize=9)
    ax.set_ylabel("波長シフト Δλ (pm)", color="white", fontsize=9)
    ax.set_xlim(0,180); ax.set_ylim(0, 2.05*LAMBDA_C)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# closeup: geometry + shift curve
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.06, 0.50, 0.86]); draw_geometry(ax1, 100, 90)
ax1.set_title("散乱の幾何（E_in=100 keV, θ=90°）", color="white", fontsize=10)
ax2 = fig.add_axes([0.62, 0.16, 0.35, 0.70]); draw_shift_curve(ax2, 90)
ax2.set_title("Δλ(θ)=λ_C(1−cos θ)", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.04, 0.96, 0.9]); draw_geometry(axc, 100, 120)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "コンプトン散乱", "", "Δλ = λ_C (1 − cos θ) ≈ 2.43 pm", cc)
os.remove(cc)

# gif: sweep theta 0..180 and back
frames = []
for thv in list(range(0,181,15)) + list(range(165,0,-15)):
    f2 = plt.figure(figsize=(5.0, 3.6)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.02, 0.04, 0.96, 0.86]); draw_geometry(a, 100, max(0.5,thv))
    a.set_title(f"θ={thv}°   Δλ={dlam(thv):.2f} pm   E_f={Ef(100,max(0.5,thv)):.0f} keV",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=160)
print("done.")
