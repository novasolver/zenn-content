# -*- coding: utf-8 -*-
"""Half-wave dipole resonance visuals.
Faithful to the tool: lambda=c/f, L=VF*lambda/2, element=L/2,
Rr=73ohm, SWR=max(Rr,Z0)/min(Rr,Z0), gain=2.15dBi,
current standing wave I(x)=sin(pi*x) (zero at tips, max at centre)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "dipole-antenna-resonance"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"; PINK = "#f472b6"
C = 3e8
Rr = 73.0


def resonant_length(f_mhz, vf):
    lam = C / (f_mhz * 1e6)
    return lam, vf * lam / 2.0


def swr(z0):
    return max(Rr, z0) / min(Rr, z0)


# sanity print
lam144, L144 = resonant_length(144, 0.95)
print(f"144MHz vf0.95: lam={lam144:.3f}m L={L144:.3f}m elem={L144/2:.3f}m SWR50={swr(50):.2f} SWR75={swr(75):.3f}")

# ---------- charts-closeup: (a) L vs f  (b) current standing wave ----------
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72]); ax1.set_facecolor(NAVY)
fs = np.linspace(30, 1000, 400)
for vf, col in [(0.99, CYAN), (0.95, ORANGE), (0.90, PINK)]:
    Ls = np.array([resonant_length(f, vf)[1] for f in fs])
    ax1.plot(fs, Ls, color=col, lw=2, label=f"VF={vf}")
ax1.axvline(144, color=GREEN, lw=1, ls="--")
ax1.text(150, ax1.get_ylim()[1]*0.78, "144MHz\nL=0.99m", color=GREEN, fontsize=8)
ax1.set_xlabel("周波数 f (MHz)", color="white", fontsize=9)
ax1.set_ylabel("共振素子長 L (m)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax1.set_title("共振素子長 L = VF·λ/2 は周波数に反比例", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72]); ax2.set_facecolor(NAVY)
x = np.linspace(0, 1, 200)
I = np.sin(np.pi * x)
ax2.plot(x, I, color=ORANGE, lw=2.4)
ax2.fill_between(x, 0, I, color=ORANGE, alpha=0.18)
ax2.axvline(0.5, color=GREEN, lw=1, ls="--")
ax2.text(0.52, 0.1, "給電点\n(電流最大)", color=GREEN, fontsize=8)
ax2.text(0.02, 0.05, "左端\nI=0", color="#9fb2d6", fontsize=8)
ax2.text(0.86, 0.05, "右端\nI=0", color="#9fb2d6", fontsize=8)
ax2.set_xlabel("素子上の位置（左端→給電点→右端）", color="white", fontsize=9)
ax2.set_ylabel("電流振幅（規格化）", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
ax2.set_ylim(0, 1.15)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("電流定在波 I(x)=sin(πx)：中央で最大、両端でゼロ", color="white", fontsize=9.5)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---------- cover ----------
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
# draw dipole schematic + current envelope
xs = np.linspace(-1, 1, 200)
env = np.cos(np.pi/2 * xs)  # max at centre, zero at tips
axc.plot(xs, env*0.6, color=ORANGE, lw=2.6)
axc.plot(xs, -env*0.6, color=ORANGE, lw=1.2, alpha=0.4)
axc.plot([-1, -0.04], [0, 0], color=CYAN, lw=5, solid_capstyle="round")
axc.plot([0.04, 1], [0, 0], color=CYAN, lw=5, solid_capstyle="round")
axc.plot(0, 0, "o", color=PINK, ms=9)
axc.set_xlim(-1.15, 1.15); axc.set_ylim(-0.9, 0.9)
axc.set_xticks([]); axc.set_yticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "半波長ダイポール", "アンテナの共振", "L=VF·λ/2、放射抵抗73Ω、利得2.15dBi", cc)
os.remove(cc)

# ---------- gif: sweep frequency, dipole shrinks; standing wave oscillates ----------
frames = []
freqs = list(np.linspace(80, 500, 22)) + list(np.linspace(480, 90, 12))
for k, f_mhz in enumerate(freqs):
    lam, L = resonant_length(f_mhz, 0.95)
    half = L / 2.0
    osc = np.sin(k * 0.6)
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.06, 0.12, 0.90, 0.74]); a.set_facecolor(NAVY)
    xs = np.linspace(-half, half, 160)
    env = np.cos(np.pi/2 * (xs/half))   # zero at tips, max centre
    a.plot([-half, -0.005], [0, 0], color=CYAN, lw=6, solid_capstyle="round")
    a.plot([0.005, half], [0, 0], color=CYAN, lw=6, solid_capstyle="round")
    a.plot(xs, env*0.45*osc, color=ORANGE, lw=2.4)
    a.plot(xs, -env*0.45*osc, color=ORANGE, lw=1.2, alpha=0.35)
    a.plot(0, 0, "o", color=PINK, ms=8)
    a.set_xlim(-0.95, 0.95); a.set_ylim(-0.6, 0.6)
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"f={f_mhz:.0f}MHz  λ={lam:.3f}m  共振全長 L={L:.3f}m", color="white", fontsize=10.5)
    a.text(0, -0.52, "給電点", color=PINK, fontsize=8, ha="center")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
