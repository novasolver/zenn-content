# -*- coding: utf-8 -*-
"""Buckling-column visuals (Euler + Johnson, switched by slenderness).
Faithful to tool: Pcr = pi^2 EI/(KL)^2 (Euler) vs A*sy*[1 - sy*lam^2/(4 pi^2 E)]
(Johnson), boundary at lambda_c = pi*sqrt(2E/sy). Steel E=200GPa sy=250MPa,
circle d=50mm, K = 1.0/2.0/0.7/0.5. ASCII-only prints, no emoji."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "buckling-column"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; RED = "#f87171"

E = 200e9; sy = 250e6
d = 0.05
I = math.pi * d**4 / 64
A = math.pi * d**2 / 4
r = math.sqrt(I / A)
lamC = math.pi * math.sqrt(2 * E / sy)


def sigma_cr(lam):
    """sigma_cr (MPa) vs slenderness lam, with Euler/Johnson switch."""
    euler = math.pi**2 * E / lam**2 / 1e6
    john = sy * (1 - sy * lam**2 / (4 * math.pi**2 * E)) / 1e6
    return euler if lam > lamC else john


def Pcr_kN(K, L):
    lam = K * L / r
    if lam > lamC:
        return math.pi**2 * E * I / (K * L)**2 / 1e3
    return A * sy * (1 - sy * lam**2 / (4 * math.pi**2 * E)) / 1e3


# ---- closeup: sigma_cr vs lambda (Euler vs Johnson) + Pcr vs L by end cond ----
fig = plt.figure(figsize=(9.8, 4.4)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.07, 0.16, 0.40, 0.70]); ax1.set_facecolor(NAVY)
lam = np.linspace(10, 250, 300)
euler = math.pi**2 * E / lam**2 / 1e6
john = sy * (1 - sy * lam**2 / (4 * math.pi**2 * E)) / 1e6
ax1.plot(lam[lam >= lamC], euler[lam >= lamC], color=CYAN, lw=2.5, label="オイラー式")
ax1.plot(lam[lam <= lamC], john[lam <= lamC], color=RED, lw=2.5, label="ジョンソン式")
ax1.plot(lam[lam < lamC], euler[lam < lamC], color=CYAN, lw=1, ls=":", alpha=0.6)
ax1.axvline(lamC, color=ORANGE, lw=1.2, ls="--")
ax1.axhline(sy / 2 / 1e6, color="#3b4a6b", lw=0.8, ls=":")
ax1.text(lamC + 4, 230, f"λc={lamC:.0f}", color=ORANGE, fontsize=8.5)
ax1.set_xlabel("細長比 λ = KL/r", color="white", fontsize=9)
ax1.set_ylabel("座屈応力 σcr (MPa)", color="white", fontsize=9)
ax1.set_ylim(0, 260); ax1.set_xlim(10, 250)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax1.set_title("2式は λc で σy/2 で連続する", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.16, 0.38, 0.70]); ax2.set_facecolor(NAVY)
Ls = np.linspace(0.5, 6, 200)
for lbl, K, col in [("ピン-ピン K=1.0", 1.0, CYAN),
                    ("固定-固定 K=0.5", 0.5, ORANGE),
                    ("固定-自由 K=2.0", 2.0, RED)]:
    P = np.array([Pcr_kN(K, L) for L in Ls])
    ax2.plot(Ls, P, lw=2, label=lbl, color=col)
ax2.set_xlabel("柱の長さ L (m)", color="white", fontsize=9)
ax2.set_ylabel("座屈荷重 Pcr (kN)", color="white", fontsize=9)
ax2.set_ylim(0, 500); ax2.set_xlim(0.5, 6)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)
ax2.set_title("固定-固定はピン-ピンの4倍(長柱域)", color="white", fontsize=9.5)

print(f"check: lamC={lamC:.1f}  default(K=1,L=2) Pcr={Pcr_kN(1.0,2.0):.1f}kN  "
      f"K=0.5/L=4={Pcr_kN(0.5,4.0):.1f} vs K=1/L=4={Pcr_kN(1.0,4.0):.1f}")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover (small sigma-lambda chart) ----
figc = plt.figure(figsize=(5.4, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.78]); axc.set_facecolor(NAVY)
axc.plot(lam[lam >= lamC], euler[lam >= lamC], color=CYAN, lw=3, label="Euler")
axc.plot(lam[lam <= lamC], john[lam <= lamC], color=RED, lw=3, label="Johnson")
axc.axvline(lamC, color=ORANGE, lw=1.5, ls="--")
axc.set_xlabel("λ = KL/r", color="white", fontsize=10)
axc.set_ylabel("σcr (MPa)", color="white", fontsize=10)
axc.set_ylim(0, 260); axc.set_xlim(10, 250)
axc.tick_params(colors="#9fb2d6", labelsize=8)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
axc.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "柱の座屈", "Euler & Johnson",
                  "Pcr = π²EI/(KL)² を細長比 λ で切替", cc)
os.remove(cc)

# ---- gif: L sweep -> column buckles more, marker rides the curve, mode label ----
frames = []
y = np.linspace(0, 1, 100)
Lseq = list(np.linspace(0.8, 5.0, 24)) + list(np.linspace(4.8, 1.0, 12))
for L in Lseq:
    lam_v = 1.0 * L / r
    P = Pcr_kN(1.0, L)
    mode = "Euler" if lam_v > lamC else "Johnson"
    amp = min(0.46, 0.06 + (L - 0.8) / 4.2 * 0.4)
    f2 = plt.figure(figsize=(6.0, 3.6)); f2.patch.set_facecolor(NAVY)
    # left: buckled column
    a = f2.add_axes([0.02, 0.06, 0.34, 0.84]); a.set_facecolor(NAVY)
    a.plot(np.sin(np.pi * y) * amp, y, color=CYAN, lw=3)
    a.plot([0, 0], [0, 1], color="#3b4a6b", lw=1, ls=":")
    a.plot(0, 0, "^", color="white", ms=11); a.plot(0, 1, "v", color="white", ms=11)
    a.set_xlim(-0.6, 0.6); a.set_ylim(-0.05, 1.05); a.axis("off")
    a.set_title(f"L={L:.1f}m", color="white", fontsize=10)
    # right: sigma-lambda curve with current marker
    a2 = f2.add_axes([0.46, 0.18, 0.50, 0.66]); a2.set_facecolor(NAVY)
    a2.plot(lam[lam >= lamC], euler[lam >= lamC], color=CYAN, lw=2)
    a2.plot(lam[lam <= lamC], john[lam <= lamC], color=RED, lw=2)
    a2.axvline(lamC, color=ORANGE, lw=1, ls="--")
    a2.plot(lam_v, sigma_cr(lam_v), "o", color=ORANGE, ms=10)
    a2.set_xlim(10, 250); a2.set_ylim(0, 260)
    a2.set_xlabel("λ", color="white", fontsize=9)
    a2.set_ylabel("σcr (MPa)", color="white", fontsize=9)
    a2.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a2.spines.values(): sp.set_color("#3b4a6b")
    a2.set_title(f"Pcr={P:.0f}kN  [{mode}]", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=80))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
