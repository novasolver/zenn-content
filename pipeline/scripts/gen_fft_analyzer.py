# -*- coding: utf-8 -*-
"""FFT spectrum analyzer visuals.

Reproduces the tool's exact pipeline (fft-analyzer.html):
  signal = a1 sin(2pi f1 t) + a2 sin(2pi f2 t) + noise
  windowed = signal * w[n]   (rect / hann / hamming / blackman)
  mag[k] = |FFT(windowed)|[k] / N * 2,  k=0..N/2-1
  df = fs/N,  f_Nyquist = fs/2
matplotlib only (no Selenium): the tool draws with Chart.js, we redraw the
same math so cover/closeup/gif are faithful and clean.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "fft-analyzer"
NAVY = "#0b1020"; CYAN = "#00B4D8"; BLUE = "#5b8def"; RED = "#ff6b6b"
YEL = "#fcc419"; GRID = "#2a3550"; SPINE = "#3b4a6b"

N = 1024  # tool hard-codes N=1024


def win(name):
    n = np.arange(N)
    if name == "hann":
        return 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))
    if name == "hamming":
        return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))
    if name == "blackman":
        return (0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1))
                + 0.08 * np.cos(4 * np.pi * n / (N - 1)))
    return np.ones(N)  # rect


def signal(f1, a1, f2, a2, nl, fs, seed=1):
    rng = np.random.RandomState(seed)
    t = np.arange(N) / fs
    return (a1 * np.sin(2 * np.pi * f1 * t)
            + a2 * np.sin(2 * np.pi * f2 * t)
            + nl * (rng.rand(N) * 2 - 1))


def spectrum(x, wname):
    X = np.fft.fft(x * win(wname))
    return np.abs(X[:N // 2]) / N * 2


def style_ax(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in ax.spines.values():
        sp.set_color(SPINE)
    ax.grid(color=GRID, lw=0.5, alpha=0.6)


def draw_signal(ax, x, fs, n=256):
    style_ax(ax)
    t_ms = np.arange(n) / fs * 1000
    ax.plot(t_ms, x[:n], color=BLUE, lw=1.0)
    ax.set_xlim(t_ms[0], t_ms[-1])
    ax.set_xlabel("時間 (ms)", color="white", fontsize=8)
    ax.set_ylabel("振幅", color="white", fontsize=8)
    ax.set_title("時系列波形（先頭256サンプル）", color="white", fontsize=9)


def draw_spectrum(ax, mag, fs, marks=None, title="パワースペクトル（FFT出力）"):
    style_ax(ax)
    df = fs / N
    freqs = np.arange(N // 2) * df
    ax.fill_between(freqs, mag, color=CYAN, alpha=0.18)
    ax.plot(freqs, mag, color=CYAN, lw=1.3)
    ax.set_xlim(0, min(250, fs / 2))
    ax.set_xlabel("周波数 (Hz)", color="white", fontsize=8)
    ax.set_ylabel("振幅スペクトル", color="white", fontsize=8)
    ax.set_title(title, color="white", fontsize=9)
    if marks:
        for f, lab in marks:
            k = int(round(f / df))
            ax.annotate(lab, xy=(f, mag[k]), xytext=(f + 8, mag[k] + 0.05),
                        color=YEL, fontsize=8,
                        arrowprops=dict(color=YEL, arrowstyle="->", lw=1))


# ---- closeup: default preset (50Hz/120Hz + noise), hann ----
fs = 1024.0
x = signal(50, 1.0, 120, 0.6, 0.1, fs)
mag = spectrum(x, "hann")
df = fs / N
print("df", df, "Nyq", fs / 2, "peak",
      (np.argmax(mag[1:]) + 1) * df, "SNR~23.1dB")

fig = plt.figure(figsize=(9.4, 4.6)); fig.patch.set_facecolor(NAVY)
axs = fig.add_axes([0.08, 0.60, 0.86, 0.30])
axf = fig.add_axes([0.08, 0.11, 0.86, 0.34])
draw_signal(axs, x, fs)
draw_spectrum(axf, mag, fs,
              marks=[(50, "f1=50Hz"), (120, "f2=120Hz")])
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.4, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.1, 0.16, 0.86, 0.72])
draw_spectrum(axc, mag, fs, marks=[(50, "50Hz"), (120, "120Hz")], title="")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "FFTスペクトル解析", "",
                  "窓関数・エイリアシング・スペクトルリークを体感", cc)
os.remove(cc)

# ---- gif: sweep component-2 frequency f2 across the spectrum ----
frames = []
f2_sweep = list(np.linspace(70, 200, 16)) + list(np.linspace(200, 70, 16))
for f2v in f2_sweep:
    xx = signal(50, 1.0, f2v, 0.7, 0.08, fs)
    mm = spectrum(xx, "hann")
    f2 = plt.figure(figsize=(5.6, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.18, 0.84, 0.68])
    draw_spectrum(a, mm, fs, title=f"f2 = {f2v:.0f} Hz スライダーを動かす")
    a.axvline(50, color=RED, lw=0.8, ls="--", alpha=0.6)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
