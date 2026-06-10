# -*- coding: utf-8 -*-
"""Ultrasound Doppler flow visuals.
Tool computes:
  f_d = 2 f0 v cos(theta) / c          (Doppler shift)
  Nyquist = PRF/2 ; aliasing if f_d > PRF/2
  v_Nyquist = c*PRF / (4 f0 cos theta)
  d_max = c / (2 PRF)
  angle error sensitivity = |tan theta| * (1 deg in rad) * 100  [%/deg]
Charts faithfully reproduce the tool's spectrum waveform and the
Nyquist-velocity-vs-angle curve. matplotlib only (no Selenium)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "ultrasound-doppler-flow"
NAVY = "#0b1020"; BLUE = "#3b82f6"; CYAN = "#7dd3fc"; RED = "#ff6b6b"
GREEN = "#34d399"; ORANGE = "#f59e0b"
C = 1540.0  # m/s soft tissue


def fd_kHz(f0Hz, v_ms, theta_deg):
    return 2 * f0Hz * v_ms * np.cos(np.radians(theta_deg)) / C / 1000.0


def spectrum(ax, f0=5e6, v=1.0, theta=60.0, prf=5000.0, title=None):
    """Pulsatile spectral-Doppler waveform with Nyquist wrap (aliasing)."""
    ax.set_facecolor(NAVY)
    fdK = fd_kHz(f0, v, theta)
    fnyqK = prf / 2 / 1000.0
    t = np.linspace(0, 1, 240)
    s = np.where(t < 0.2,
                 fdK * 0.3 + (fdK * 1.6 - fdK * 0.3) * np.sin(np.pi * t / 0.2 / 2),
                 np.where(t < 0.5,
                          fdK * 1.6 - (fdK * 1.6 - fdK * 0.36) * (t - 0.2) / 0.3,
                          fdK * 0.36 - (fdK * 0.36 - fdK * 0.3) * (t - 0.5) / 0.5))
    sDisp = s.copy()
    for i in range(len(sDisp)):
        while sDisp[i] > fnyqK:  sDisp[i] -= 2 * fnyqK
        while sDisp[i] < -fnyqK: sDisp[i] += 2 * fnyqK
    aliased = np.any(s > fnyqK)
    ax.plot(t, sDisp, color=CYAN, lw=2.2, zorder=4)
    ax.axhline(fnyqK, color=RED, ls="--", lw=1.3)
    ax.axhline(-fnyqK, color=RED, ls="--", lw=1.3)
    ax.axhline(0, color="#5b6b8c", lw=0.8)
    ax.text(0.01, fnyqK, " +Nyquist", color=RED, fontsize=8, va="bottom")
    ax.text(0.01, -fnyqK, " -Nyquist", color=RED, fontsize=8, va="top")
    lim = max(fnyqK * 1.45, fdK * 0.6 + 0.5)
    ax.set_ylim(-lim, lim); ax.set_xlim(0, 1)
    ax.set_xlabel("時間 t（心拍周期 0〜1）", color="white", fontsize=9)
    ax.set_ylabel("ドップラー周波数 (kHz)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    tag = "ALIASING" if aliased else "OK"
    tc = RED if aliased else GREEN
    ax.text(0.98, 0.93, tag, transform=ax.transAxes, color="white", fontsize=9,
            ha="right", va="top", weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=tc, ec="none"))
    if title: ax.set_title(title, color="white", fontsize=10)


def vnyq_curve(ax, f0=5e6, prf=5000.0, v_cur=100.0, theta_cur=60.0, title=None):
    """Nyquist velocity vs beam angle, with current operating point."""
    ax.set_facecolor(NAVY)
    a = np.linspace(0, 80, 200)
    cA = np.maximum(np.abs(np.cos(np.radians(a))), 1e-6)
    vN = C * prf / (4 * f0 * cA) * 100.0  # cm/s
    ax.plot(a, vN, color=GREEN, lw=2.2, label="Nyquist 速度 v_nyq")
    ax.axhline(v_cur, color=ORANGE, ls="--", lw=1.8, label="現在の血流速度 v")
    cAc = max(abs(np.cos(np.radians(theta_cur))), 1e-6)
    vNc = C * prf / (4 * f0 * cAc) * 100.0
    ax.scatter([theta_cur], [vNc], s=80, color=BLUE, ec="white", zorder=6)
    ax.set_xlabel("ビーム角 θ (deg)", color="white", fontsize=9)
    ax.set_ylabel("速度 (cm/s)", color="white", fontsize=9)
    ax.set_xlim(0, 80); ax.set_ylim(0, min(vN.max(), v_cur * 4))
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white",
              fontsize=8, loc="upper left")
    if title: ax.set_title(title, color="white", fontsize=10)


# ---- closeup: spectrum (aliased default) + vnyq curve ----
fig = plt.figure(figsize=(9.6, 4.2)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.40, 0.72])
spectrum(ax1, f0=5e6, v=1.0, theta=60, prf=5000,
         title="スペクトル波形：f_d 3.25 kHz > Nyquist 2.5 kHz")
ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72])
vnyq_curve(ax2, f0=5e6, prf=5000, v_cur=100, theta_cur=60,
           title="Nyquist 速度 vs ビーム角")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.0, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13, 0.16, 0.82, 0.74])
spectrum(axc, f0=5e6, v=1.0, theta=60, prf=5000)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "超音波ドップラー", "血流計測",
                  "f_d = 2 f0 v cos θ / c とエイリアシング", cc)
os.remove(cc)

# ---- gif: sweep PRF from low (aliasing) to high (clears) ----
frames = []
prfs = list(np.linspace(3000, 12000, 24)) + list(np.linspace(12000, 3000, 24))
for prf in prfs:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.14, 0.17, 0.80, 0.74])
    spectrum(a2, f0=5e6, v=1.0, theta=60, prf=prf,
             title=f"PRF = {prf/1000:.1f} kHz  (Nyquist {prf/2000:.2f} kHz)")
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
