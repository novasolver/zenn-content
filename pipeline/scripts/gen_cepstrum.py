# -*- coding: utf-8 -*-
"""Cepstrum pitch-detection visuals. Pipeline (as tool): signal (5 harmonics +
noise) -> log|FFT| -> real cepstrum -> quefrency peak -> F0 = Fs/quefrency."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "cepstrum"
NAVY = "#0b1020"; BLUE = "#5fb1ff"; GREEN = "#5fd49a"; RED = "#ff6b6b"; YEL = "#fcc419"
N = 1024; K = 5; EPS = 1e-10

def build(f0, Fs, alpha=0.30, sigma=0.05, seed=20260516):
    rng = np.random.RandomState(seed); n = np.arange(N); x = np.zeros(N)
    for k in range(1, K + 1):
        x += np.exp(-alpha * (k - 1)) * np.sin(2 * np.pi * k * f0 * n / Fs)
    return x + sigma * rng.randn(N)

def cepstrum(x, Fs):
    X = np.fft.fft(x); logmag = np.log(np.abs(X) + EPS)
    c = np.real(np.fft.ifft(logmag))
    nLo = max(2, int(0.002 * Fs)); nHi = min(N // 2 - 1, int(0.020 * Fs))
    pk = nLo + int(np.argmax(c[nLo:nHi]))
    return logmag, c, pk, Fs / pk

def panels(fig, x, Fs, f0, x0=0.07, w=0.88):
    logmag, c, pk, f0est = cepstrum(x, Fs)
    a1 = fig.add_axes([x0, 0.70, w, 0.22]); a1.set_facecolor(NAVY)
    a1.plot(np.arange(200), x[:200], color=BLUE, lw=1.0); a1.set_xlim(0, 200)
    a1.set_title("時系列 x[n]", color="white", fontsize=9); a1.set_xticks([]); a1.set_yticks([])
    a2 = fig.add_axes([x0, 0.40, w, 0.22]); a2.set_facecolor(NAVY)
    a2.plot(np.arange(N // 2), logmag[:N // 2], color=GREEN, lw=0.9); a2.set_xlim(0, N // 2)
    a2.set_title("対数振幅スペクトル log|X[k]|（高調波の櫛）", color="white", fontsize=9)
    a2.set_xticks([]); a2.set_yticks([])
    a3 = fig.add_axes([x0, 0.08, w, 0.24]); a3.set_facecolor(NAVY)
    q = N // 4
    a3.plot(np.arange(q), c[:q], color=RED, lw=1.0)
    a3.axvline(pk, color=YEL, lw=1.2, ls="--")
    a3.text(pk + 4, c[pk] * 0.9, f"ピーク quefrency={pk}\nf0={f0est:.0f}Hz", color=YEL, fontsize=8)
    a3.set_title("ケプストラム c[n]（黄=ピッチピーク）", color="white", fontsize=9)
    a3.set_xlabel("quefrency (サンプル)", color="white", fontsize=8)
    a3.set_xlim(0, q); a3.tick_params(colors="#9fb2d6", labelsize=7); a3.set_yticks([])
    for a in (a1, a2, a3):
        for sp in a.spines.values(): sp.set_color("#3b4a6b")
    return pk, f0est

x = build(200, 8000); _, _, pk, f0e = cepstrum(x, 8000)
print(f"f0=200 Fs=8000: quefrency peak={pk} (expect 40), f0est={f0e:.1f}Hz")

# closeup
fig = plt.figure(figsize=(8.6, 5.0)); fig.patch.set_facecolor(NAVY)
panels(fig, x, 8000, 200)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=125); print("  closeup ->", closeup)

# cover (use middle+bottom panels)
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
logmag, c, pk, f0e = cepstrum(x, 8000)
ac = figc.add_axes([0.06, 0.56, 0.9, 0.36]); ac.set_facecolor(NAVY)
ac.plot(np.arange(N // 2), logmag[:N // 2], color=GREEN, lw=0.9); ac.axis("off")
ac2 = figc.add_axes([0.06, 0.08, 0.9, 0.36]); ac2.set_facecolor(NAVY)
ac2.plot(np.arange(N // 4), c[:N // 4], color=RED, lw=1.0); ac2.axvline(pk, color=YEL, lw=1.2, ls="--"); ac2.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ケプストラム分析", "", "F0 = Fs/quefrency でピッチ検出", cc)
os.remove(cc)

# gif: sweep f0, quefrency peak moves
frames = []
for f0 in list(range(120, 320, 12)) + list(range(308, 120, -12)):
    x = build(f0, 8000)
    f2 = plt.figure(figsize=(5.6, 3.4)); f2.patch.set_facecolor(NAVY)
    pk, f0e = panels(f2, x, 8000, f0, x0=0.07, w=0.9)
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
