# -*- coding: utf-8 -*-
"""Goertzel / DTMF visuals. Exact recurrence from the tool:
coeff=2cos(2 pi k/N), s=x+coeff*s1-s2, |X|^2=s1^2+s2^2-coeff*s1*s2."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "goertzel-algorithm"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; RED = "#ff6b6b"; BLUE = "#5b8def"; YEL = "#fcc419"
ROW = [697, 770, 852, 941]; COL = [1209, 1336, 1477, 1633]
KEYMAP = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D']
Fs, N = 8000, 256

def goertzel(x, tf):
    k = round(tf * len(x) / Fs); w = 2 * np.pi * k / len(x); c = 2 * np.cos(w)
    s1 = s2 = 0.0
    for v in x:
        s = v + c * s1 - s2; s2 = s1; s1 = s
    return np.sqrt(max(0.0, s1 * s1 + s2 * s2 - c * s1 * s2))

def dtmf_signal(key, noise=0.0, seed=1):
    rng = np.random.RandomState(seed)
    r, c = key // 4, key % 4
    n = np.arange(N)
    x = 0.5 * np.sin(2 * np.pi * ROW[r] * n / Fs) + 0.5 * np.sin(2 * np.pi * COL[c] * n / Fs)
    return x + noise * rng.randn(N), ROW[r], COL[c]

def mags(x):
    return [goertzel(x, f) for f in ROW + COL]

def draw(ax_sig, ax_bar, key, noise=0.0):
    x, rf, cf = dtmf_signal(key, noise); m = mags(x)
    ri = int(np.argmax(m[:4])); ci = 4 + int(np.argmax(m[4:]))
    ax_sig.set_facecolor(NAVY)
    ax_sig.plot(np.arange(160), x[:160], color=CYAN, lw=1.0)
    ax_sig.set_title(f"DTMF キー '{KEYMAP[key]}' の信号 x[n]（行{rf}+列{cf}Hz）", color="white", fontsize=9)
    ax_sig.set_xlim(0, 160); ax_sig.set_xticks([]); ax_sig.set_yticks([])
    for sp in ax_sig.spines.values(): sp.set_color("#3b4a6b")
    ax_bar.set_facecolor(NAVY)
    cols = [RED]*4 + [BLUE]*4
    cols[ri] = YEL; cols[ci] = YEL
    labels = [f"{f}" for f in ROW + COL]
    ax_bar.bar(range(8), m, color=cols)
    ax_bar.set_xticks(range(8)); ax_bar.set_xticklabels(labels, color="white", fontsize=7, rotation=40)
    ax_bar.set_title("Goertzel 8周波数の |X_k|（赤=行/青=列/黄=最強）", color="white", fontsize=9)
    ax_bar.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in ax_bar.spines.values(): sp.set_color("#3b4a6b")
    return KEYMAP[key], ROW[ri], COL[ci - 4]

# closeup
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.06, 0.58, 0.88, 0.32])
ax2 = fig.add_axes([0.30, 0.12, 0.42, 0.34])
det = draw(ax1, ax2, 5)
print(f"key 5 detected: {det}; ops N*M={N*8}")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axa = figc.add_axes([0.08, 0.56, 0.88, 0.36]); axb = figc.add_axes([0.20, 0.10, 0.62, 0.36])
draw(axa, axb, 5); axa.set_title(""); axb.set_title("")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "Goertzelアルゴリズム", "", "DTMF単一周波数検出を O(N) で可視化", cc)
os.remove(cc)

# gif: sweep through keys
frames = []
for key in list(range(16)) + list(range(14, 0, -1)):
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a1 = f2.add_axes([0.06, 0.58, 0.88, 0.30]); a2 = f2.add_axes([0.26, 0.12, 0.50, 0.34])
    kc, rr, cc2 = draw(a1, a2, key)
    a1.set_title(f"キー '{kc}'  検出: 行{rr}Hz / 列{cc2}Hz", color="white", fontsize=9)
    a2.set_title("Goertzel |X_k|", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
