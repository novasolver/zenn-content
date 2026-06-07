# -*- coding: utf-8 -*-
"""Parseval's theorem visuals: time-domain energy = (1/N) * freq-domain energy.
Reproduces the tool's signals (sine/rect/gauss) and DFT energy check."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "parsevals-theorem"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; RED = "#ff6b6b"; ORANGE = "#f59e0b"

def signal(kind, N=512, A=1.0, f0=10):
    n = np.arange(N)
    if kind == 0: return A * np.cos(2 * np.pi * f0 * n / N)
    if kind == 1:
        x = np.zeros(N); w = N // 8; c = N // 2; x[c - w // 2:c + w // 2] = A; return x
    s = N / 16; return A * np.exp(-((n - N / 2) ** 2) / (2 * s * s))

def energies(x):
    X = np.fft.fft(x); Et = np.sum(x * x); Ef = np.sum(np.abs(X) ** 2) / len(x)
    return Et, Ef, np.abs(X) ** 2 / len(x)

x = signal(0); Et, Ef, psd = energies(x)
print(f"sine: Et={Et:.3f} Ef={Ef:.3f} relErr={abs(Et-Ef)/Et:.2e}")

# closeup: time signal + PSD
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.58, 0.88, 0.32]); ax1.set_facecolor(NAVY)
ax1.plot(np.arange(200), x[:200], color=CYAN, lw=1.2)
ax1.set_title("時間領域 x[n]（先頭200サンプル）", color="white", fontsize=10)
ax1.set_xlim(0, 200); ax1.tick_params(colors="#9fb2d6", labelsize=8)
ax1.text(0.99, 0.92, f"E_t = Σ|x[n]|² = {Et:.0f}", transform=ax1.transAxes,
         ha="right", va="top", color=CYAN, fontsize=10)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax2 = fig.add_axes([0.07, 0.12, 0.88, 0.32]); ax2.set_facecolor(NAVY)
N = len(x); ax2.plot(np.arange(N // 2), psd[:N // 2], color=RED, lw=1.2)
pk = np.argmax(psd[:N // 2]); ax2.plot(pk, psd[pk], "o", color=ORANGE, ms=6)
ax2.set_title("周波数領域 PSD = |X[k]|²/N", color="white", fontsize=10)
ax2.set_xlabel("周波数ビン k", color="white", fontsize=9)
ax2.set_xlim(0, N // 2); ax2.tick_params(colors="#9fb2d6", labelsize=8)
ax2.text(0.99, 0.92, f"E_f = (1/N)Σ|X[k]|² = {Ef:.0f}  →  E_t = E_f ✓",
         transform=ax2.transAxes, ha="right", va="top", color=ORANGE, fontsize=10)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc1 = figc.add_axes([0.08, 0.56, 0.88, 0.36]); axc1.set_facecolor(NAVY)
axc1.plot(np.arange(200), x[:200], color=CYAN, lw=1.2); axc1.axis("off")
axc2 = figc.add_axes([0.08, 0.08, 0.88, 0.36]); axc2.set_facecolor(NAVY)
axc2.plot(np.arange(N // 2), psd[:N // 2], color=RED, lw=1.2); axc2.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "パーセバルの定理", "", "時間と周波数のエネルギー保存 Σ|x|²=(1/N)Σ|X|²", cc)
os.remove(cc)

# gif: sweep f0, peak moves, energies stay equal
frames = []
for f0 in list(range(4, 46, 2)) + list(range(44, 4, -2)):
    xx = signal(0, f0=f0); Et2, Ef2, psd2 = energies(xx)
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a1 = f2.add_axes([0.10, 0.56, 0.86, 0.34]); a1.set_facecolor(NAVY)
    a1.plot(np.arange(200), xx[:200], color=CYAN, lw=1.1); a1.set_xlim(0, 200)
    a1.set_xticks([]); a1.set_yticks([])
    a1.set_title(f"f0={f0} bin   E_t={Et2:.0f}", color="white", fontsize=9)
    a2 = f2.add_axes([0.10, 0.13, 0.86, 0.34]); a2.set_facecolor(NAVY)
    a2.plot(np.arange(N // 2), psd2[:N // 2], color=RED, lw=1.1); a2.set_xlim(0, N // 2)
    a2.set_xticks([]); a2.set_yticks([])
    a2.set_title(f"E_f={Ef2:.0f}  →  E_t=E_f", color="#f59e0b", fontsize=9)
    for ax in (a1, a2):
        for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
