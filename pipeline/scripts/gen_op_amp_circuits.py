# -*- coding: utf-8 -*-
"""op-amp-circuits visuals: inverting amp waveform + clipping (closeup),
branded cover, and an amplitude-sweep gif showing clipping appear.
Faithful to the tool's JS: Vout = clip(-Rf/Rin * Vin, -Vcc, +Vcc).
Tool defaults: Rin=10k, Rf=47k -> Av=-4.7; Vcc=15V; f=1kHz; sine."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "op-amp-circuits"
NAVY = "#0b1020"; BLUE = "#60a5fa"; CYAN = "#22d3ee"; RED = "#fb7185"; GREY = "#3b4a6b"

def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GREY)

Rin, Rf, Vcc, freq = 10, 47, 15, 1000
gain = -(Rf / Rin)            # = -4.7
N = 600; T = 1.0 / freq
t = np.linspace(0, 3 * T, N)  # 3 periods, like the tool
tms = t * 1000

def waveform(amp):
    vin = amp * np.sin(2 * np.pi * freq * t)
    vout = np.clip(gain * vin, -Vcc, Vcc)
    return vin, vout

# ---------- charts-closeup ----------
amp = 5.0
vin, vout = waveform(amp)
clip_mask = np.abs(vout) >= Vcc - 0.01
vclip = np.where(clip_mask, vout, np.nan)

fig = plt.figure(figsize=(9.0, 4.2)); fig.patch.set_facecolor(NAVY)
ax = fig.add_axes([0.09, 0.15, 0.88, 0.74]); style(ax)
ax.axhline(Vcc, color=RED, ls="--", lw=1); ax.axhline(-Vcc, color=RED, ls="--", lw=1)
ax.text(tms[-1] * 0.60, Vcc + 0.6, "+Vcc = +15V (rail)", color=RED, fontsize=8)
ax.text(tms[-1] * 0.60, -Vcc - 2.4, "-Vcc = -15V (rail)", color=RED, fontsize=8)
ax.plot(tms, vin, color=BLUE, lw=1.6, label="Vin  (5Vp, 1kHz)")
ax.plot(tms, vout, color=CYAN, lw=2.4, label="Vout = -4.7 x Vin")
ax.plot(tms, vclip, color=RED, lw=3.0, label="clipped")
ax.set_xlabel("時間 t [ms]", color="white", fontsize=9)
ax.set_ylabel("電圧 [V]", color="white", fontsize=9)
ax.set_ylim(-20, 20)
ax.set_title("反転増幅 Av=-4.7：理想ピーク 23.5V が ±15V でクリップ（赤）",
             color="white", fontsize=10)
leg = ax.legend(loc="lower right", fontsize=7.5, facecolor=NAVY, edgecolor=GREY)
for txt in leg.get_texts(): txt.set_color("white")
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, cu, dpi=130); print("  closeup ->", cu)

# ---------- cover ----------
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13, 0.16, 0.83, 0.76]); style(axc)
axc.axhline(Vcc, color=RED, ls="--", lw=1); axc.axhline(-Vcc, color=RED, ls="--", lw=1)
axc.plot(tms, vin, color=BLUE, lw=1.6)
axc.plot(tms, vout, color=CYAN, lw=2.4)
axc.plot(tms, vclip, color=RED, lw=3.0)
axc.set_ylim(-20, 20)
axc.set_xlabel("t [ms]", color="white", fontsize=9)
axc.set_ylabel("V [V]", color="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "オペアンプ回路", "",
                  "Av=-Rf/Rin、出力は±Vccで頭打ち（クリッピング）", cc)
os.remove(cc)

# ---------- gif: amplitude sweep ----------
frames = []
amps = list(np.linspace(1.0, 6.0, 18)) + list(np.linspace(6.0, 1.0, 8))
for a in amps:
    vi, vo = waveform(a)
    cm = np.abs(vo) >= Vcc - 0.01
    vc = np.where(cm, vo, np.nan)
    fr = plt.figure(figsize=(4.9, 3.0)); fr.patch.set_facecolor(NAVY)
    g = fr.add_axes([0.14, 0.16, 0.82, 0.74]); style(g)
    g.axhline(Vcc, color=RED, ls="--", lw=1); g.axhline(-Vcc, color=RED, ls="--", lw=1)
    g.plot(tms, vi, color=BLUE, lw=1.4)
    g.plot(tms, vo, color=CYAN, lw=2.2)
    g.plot(tms, vc, color=RED, lw=2.8)
    g.set_ylim(-20, 20)
    g.set_xlabel("t [ms]", color="white", fontsize=9)
    g.set_ylabel("V [V]", color="white", fontsize=9)
    g.set_title(f"入力 {a:.1f}Vp → クリップ率 {cm.mean()*100:.0f}%",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(fr, dpi=92))
figlib.save_gif(frames, SLUG, duration=110); print("done.")
