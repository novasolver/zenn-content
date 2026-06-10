# -*- coding: utf-8 -*-
"""Visuals for fourier-series-vis (rotating-phasor waveform synthesizer).

Faithful to the tool's getHarmonics():
  square   : freq n=2k-1, amp=(4/pi)/n           (odd only)
  sawtooth : freq k,      amp=(2/pi)*(-1)^(k+1)/k (all)
  triangle : freq n=2k-1, amp=(8/pi^2)*(-1)^(k+1)/n^2 (odd only)
Phasor arms are drawn tip-to-tip; the final tip's y traces the waveform.
ASCII-only code; JP labels via figlib font. matplotlib only (no Selenium).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "fourier-series-vis"
NAVY = "#020d1a"; CYAN = "#00B4D8"; BLUE = "#007BFF"; GREY = "#9fb2d6"
COLORS = ['#007BFF', '#00B4D8', '#00f5d4', '#f72585', '#ffd166',
          '#06d6a0', '#ef476f', '#118ab2', '#ffd60a', '#80b918']


def harmonics(wave, N):
    terms = []
    if wave == "square":
        for k in range(1, N + 1):
            n = 2 * k - 1
            terms.append((n, (4 / np.pi) / n))
    elif wave == "sawtooth":
        for k in range(1, N + 1):
            sign = -1 if k % 2 == 0 else 1
            terms.append((k, (2 / np.pi) * sign / k))
    elif wave == "triangle":
        for k in range(1, N + 1):
            n = 2 * k - 1
            sign = -1 if k % 2 == 0 else 1
            terms.append((n, (8 / (np.pi * np.pi)) * sign / (n * n)))
    return terms


def synth(wave, N, tt):
    s = np.zeros_like(tt)
    for n, amp in harmonics(wave, N):
        s += amp * np.sin(2 * np.pi * n * tt)
    return s


def phasor_chain(wave, N, tau):
    """Return tip-to-tip vertices of the phasor arms at phase tau (cycles)."""
    px, py = 0.0, 0.0
    pts = [(px, py)]
    for n, amp in harmonics(wave, N):
        ang = n * tau * 2 * np.pi + (np.pi if amp < 0 else 0.0)
        r = abs(amp)
        px += r * np.cos(ang)
        py += r * np.sin(ang)
        pts.append((px, py))
    return np.array(pts)


# ---- charts-closeup: phasor chain + drawn waveform (the tool's core view) ----
tt = np.linspace(0, 1, 1600)
wave = "square"; N = 7
tau = 0.0
fig = plt.figure(figsize=(9.6, 4.2)); fig.patch.set_facecolor(NAVY)
axL = fig.add_axes([0.04, 0.10, 0.34, 0.82]); axL.set_facecolor(NAVY)
axR = fig.add_axes([0.45, 0.14, 0.52, 0.76]); axR.set_facecolor(NAVY)

pts = phasor_chain(wave, N, tau)
for i in range(len(pts) - 1):
    c = COLORS[i % len(pts)]
    r = np.hypot(*(pts[i + 1] - pts[i]))
    th = np.linspace(0, 2 * np.pi, 120)
    axL.plot(pts[i, 0] + r * np.cos(th), pts[i, 1] + r * np.sin(th), color=c, lw=0.8, alpha=0.5)
    axL.plot([pts[i, 0], pts[i + 1, 0]], [pts[i, 1], pts[i + 1, 1]], color=c, lw=2)
axL.plot(pts[-1, 0], pts[-1, 1], "o", color="white", ms=6)
tipy = pts[-1, 1]
axL.axhline(tipy, color="white", lw=0.6, ls=":", alpha=0.6)
axL.set_aspect("equal"); axL.set_xlim(-0.3, 2.0); axL.set_ylim(-1.3, 1.3)
axL.axis("off")
axL.set_title("回転フェーザー（腕を継いだ鎖）", color="white", fontsize=10)

# the waveform the chain has drawn so far (tip y vs phase)
wf = synth(wave, N, tt)
axR.plot(tt, wf, color=BLUE, lw=2, label="合成波形 N=7")
axR.plot(tt, synth(wave, 1, tt), color=GREY, lw=1, ls="--", label="基本波 (n=1)")
axR.plot([tau], [tipy], "o", color="#00f5d4", ms=7)
axR.axhline(tipy, color="white", lw=0.6, ls=":", alpha=0.6)
axR.set_xlim(0, 1); axR.set_ylim(-1.5, 1.5)
axR.set_xlabel("位相 t (周期)", color="white", fontsize=9)
axR.tick_params(colors=GREY, labelsize=8)
for sp in axR.spines.values(): sp.set_color("#3b4a6b")
axR.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
axR.set_title("鎖の先端の高さが波形を描く（方形波 N=7）", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.06, 0.44, 0.88]); axc.set_facecolor(NAVY)
pts = phasor_chain("square", 6, 0.12)
for i in range(len(pts) - 1):
    c = COLORS[i % len(pts)]
    r = np.hypot(*(pts[i + 1] - pts[i]))
    th = np.linspace(0, 2 * np.pi, 100)
    axc.plot(pts[i, 0] + r * np.cos(th), pts[i, 1] + r * np.sin(th), color=c, lw=0.8, alpha=0.5)
    axc.plot([pts[i, 0], pts[i + 1, 0]], [pts[i, 1], pts[i + 1, 1]], color=c, lw=2.2)
axc.plot(pts[-1, 0], pts[-1, 1], "o", color="white", ms=6)
axc.set_aspect("equal"); axc.set_xlim(-0.4, 2.0); axc.set_ylim(-1.4, 1.4); axc.axis("off")
axw = figc.add_axes([0.50, 0.10, 0.48, 0.80]); axw.set_facecolor(NAVY)
axw.plot(tt, synth("square", 7, tt), color=CYAN, lw=2)
axw.set_ylim(-1.5, 1.5); axw.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "フーリエ級数の", "フェーザー可視化",
                  "回転する円の重ね合わせが波形を描く", cc)
os.remove(cc)

# ---- gif: phasor chain rotating, tracing the waveform live ----
frames = []
wave = "square"; N = 7
hist_t = []; hist_y = []
taus = np.linspace(0, 1, 48, endpoint=False)
for tau in taus:
    pts = phasor_chain(wave, N, tau)
    tipy = pts[-1, 1]
    hist_t.append(tau); hist_y.append(tipy)
    f2 = plt.figure(figsize=(6.0, 3.0)); f2.patch.set_facecolor(NAVY)
    aL = f2.add_axes([0.01, 0.06, 0.36, 0.88]); aL.set_facecolor(NAVY)
    aR = f2.add_axes([0.43, 0.12, 0.55, 0.78]); aR.set_facecolor(NAVY)
    for i in range(len(pts) - 1):
        c = COLORS[i % len(pts)]
        r = np.hypot(*(pts[i + 1] - pts[i]))
        th = np.linspace(0, 2 * np.pi, 80)
        aL.plot(pts[i, 0] + r * np.cos(th), pts[i, 1] + r * np.sin(th), color=c, lw=0.7, alpha=0.45)
        aL.plot([pts[i, 0], pts[i + 1, 0]], [pts[i, 1], pts[i + 1, 1]], color=c, lw=2)
    aL.plot(pts[-1, 0], pts[-1, 1], "o", color="white", ms=5)
    aL.axhline(tipy, color="white", lw=0.5, ls=":", alpha=0.6)
    aL.set_aspect("equal"); aL.set_xlim(-0.3, 2.0); aL.set_ylim(-1.3, 1.3); aL.axis("off")
    aR.plot(tt, synth(wave, N, tt), color="#3b4a6b", lw=1, alpha=0.7)
    aR.plot(hist_t, hist_y, color=BLUE, lw=2)
    aR.plot([tau], [tipy], "o", color="#00f5d4", ms=6)
    aR.axhline(tipy, color="white", lw=0.5, ls=":", alpha=0.6)
    aR.set_xlim(0, 1); aR.set_ylim(-1.5, 1.5); aR.set_xticks([]); aR.set_yticks([])
    for sp in aR.spines.values(): sp.set_color("#3b4a6b")
    aR.set_title("方形波 N=7  先端のyが波形を描く", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
