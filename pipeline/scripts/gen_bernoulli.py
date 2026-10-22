# -*- coding: utf-8 -*-
"""Generate bernoulli-applications visuals (cover, charts-closeup, slider-anim).
Physics reproduced from tools/bernoulli-applications.html calcVenturi() and
the three chart tabs (pressure/velocity profile, ratio sensitivity, device comp).
ASCII-only prints. No emoji. Use <v> instead of angle brackets.
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bernoulli-applications"
NAVY = "#001F3F"
ACC = "#007BFF"
ACC2 = "#00B4D8"
RED = "#dc2626"
GREEN = "#16a34a"
ORANGE = "#f59e0b"


def calc_venturi(v1, D1mm, D2mm, rho):
    """Exact port of calcVenturi() in the tool."""
    D1 = D1mm / 1000.0
    D2 = D2mm / 1000.0
    A1 = math.pi * (D1 / 2) ** 2
    A2 = math.pi * (D2 / 2) ** 2
    v2 = v1 * A1 / A2
    dP = 0.5 * rho * (v2 ** 2 - v1 ** 2)
    return v2, dP, A1, A2


def velocity_pressure_profile(v1, D1mm, D2mm, rho, P1kPa, n=81):
    """Tab0 model: v(x) is constant/ramped along the venturi, P from Bernoulli."""
    v2, _, _, _ = calc_venturi(v1, D1mm, D2mm, rho)
    P1 = P1kPa * 1000.0
    xs = np.linspace(0, 1, n)
    v = np.zeros(n)
    for i, x in enumerate(xs):
        if x < 0.25:
            v[i] = v1
        elif x < 0.35:
            t = (x - 0.25) / 0.10
            v[i] = v1 + t * (v2 - v1)
        elif x < 0.60:
            v[i] = v2
        elif x < 0.70:
            t = (x - 0.60) / 0.10
            v[i] = v2 - t * (v2 - v1)
        else:
            v[i] = v1
    P = (P1 - 0.5 * rho * (v ** 2 - v1 ** 2)) / 1000.0  # kPa
    return xs, v, P


def fig_profile(v1=10, D1=100, D2=50, rho=1000, P1=200, save=None, dpi=110):
    xs, v, P = velocity_pressure_profile(v1, D1, D2, rho, P1)
    fig, ax = plt.subplots(figsize=(6.2, 3.7), facecolor="white")
    ax.plot(xs, v, color=ACC, lw=2.6, label="流速 v (m/s)")
    ax.set_xlabel("管軸方向の正規化位置 (0=入口, 1=出口)")
    ax.set_ylabel("流速 v (m/s)", color=ACC)
    ax.tick_params(axis="y", labelcolor=ACC)
    ax.set_ylim(0, max(v) * 1.15)
    ax.grid(alpha=0.25)
    ax2 = ax.twinx()
    ax2.plot(xs, P, color=RED, lw=2.6, label="静圧 P (kPa)")
    ax2.set_ylabel("静圧 P (kPa)", color=RED)
    ax2.tick_params(axis="y", labelcolor=RED)
    ax2.axhline(0, color="#888", ls=":", lw=1)
    ax.set_title("絞り部で流速が増し静圧が下がる", color=NAVY, fontsize=12)
    fig.tight_layout()
    if save:
        figlib.save_fig(fig, save, dpi=dpi)
    return fig


def fig_closeup():
    """Two-panel: pressure/velocity profile + ratio sensitivity (dP vs v1)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.1), facecolor="white")

    # left: profile (default preset)
    xs, v, P = velocity_pressure_profile(10, 100, 50, 1000, 200)
    ax1.plot(xs, v, color=ACC, lw=2.6)
    ax1.set_xlabel("正規化位置 x (入口->絞り->出口)")
    ax1.set_ylabel("流速 v (m/s)", color=ACC)
    ax1.tick_params(axis="y", labelcolor=ACC)
    ax1.set_ylim(0, max(v) * 1.15)
    ax1.grid(alpha=0.25)
    a1b = ax1.twinx()
    a1b.plot(xs, P, color=RED, lw=2.6)
    a1b.set_ylabel("静圧 P (kPa)", color=RED)
    a1b.tick_params(axis="y", labelcolor=RED)
    a1b.axhline(0, color="#888", ls=":", lw=1)
    ax1.set_title("管内 流速・静圧プロファイル (v1=10, D1/D2=2)",
                  color=NAVY, fontsize=11)

    # right: dP vs v1 for D1/D2 = 2,3,4 (rho=1000)
    v1s = np.linspace(1, 30, 120)
    for ratio, col in ((2, ACC), (3, RED), (4, GREEN)):
        v2 = v1s * ratio * ratio
        dP = 0.5 * 1000 * (v2 ** 2 - v1s ** 2) / 1000.0  # kPa
        ax2.plot(v1s, dP, color=col, lw=2.5, label=f"D1/D2 = {ratio}")
    ax2.plot([10], [0.5 * 1000 * ((10 * 4) ** 2 - 100) / 1000], "o",
             color=ORANGE, ms=11, zorder=5, label="現在の設定")
    ax2.text(10.5, 900, "v1=10, dP=750 kPa", color=NAVY, fontsize=9)
    ax2.set_xlabel("上流速度 v1 (m/s)")
    ax2.set_ylabel("圧力降下 dP (kPa)")
    ax2.set_title("径比の4乗で dP が急増する", color=NAVY, fontsize=11)
    ax2.grid(alpha=0.25)
    ax2.set_ylim(0, 4500)
    ax2.legend(fontsize=9, loc="upper left")

    fig.tight_layout()
    out = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
    figlib.save_fig(fig, out, dpi=130)
    print("  charts-closeup ->", out)
    return out


def make_gif():
    """Animate the D2 (throat diameter) slider; profile deepens as D2 shrinks."""
    frames = []
    d2_vals = list(np.linspace(80, 35, 22))
    d2_vals = d2_vals + d2_vals[::-1]
    for d2 in d2_vals:
        v2, dP, _, _ = calc_venturi(10, 100, d2, 1000)
        xs, v, P = velocity_pressure_profile(10, 100, d2, 1000, 200)
        fig, ax = plt.subplots(figsize=(6.2, 3.7), facecolor="white")
        ax.plot(xs, v, color=ACC, lw=2.6)
        ax.set_xlabel("正規化位置 x")
        ax.set_ylabel("流速 v (m/s)", color=ACC)
        ax.tick_params(axis="y", labelcolor=ACC)
        ax.set_ylim(0, 220)
        ax.grid(alpha=0.25)
        a2 = ax.twinx()
        a2.plot(xs, P, color=RED, lw=2.6)
        a2.set_ylabel("静圧 P (kPa)", color=RED)
        a2.tick_params(axis="y", labelcolor=RED)
        a2.set_ylim(-9000, 250)
        a2.axhline(0, color="#888", ls=":", lw=1)
        ax.set_title(f"D2={d2:.0f}mm  v2={v2:.0f} m/s  dP={dP/1000:.0f} kPa",
                     color=NAVY, fontsize=11)
        fig.tight_layout()
        frames.append(figlib.fig_to_pil(fig, dpi=90))
    figlib.save_gif(frames, SLUG, duration=120)


def main():
    figlib.outdir(SLUG)
    closeup = fig_closeup()
    prev = os.path.join(figlib.outdir(SLUG), "_cover_chart.png")
    fig_profile(save=prev, dpi=110)
    figlib.make_cover(SLUG,
                      "ベルヌーイの定理応用",
                      "ベンチュリ管で測る流量",
                      "連続の式 x ベルヌーイ = 差圧流量計",
                      prev)
    make_gif()
    if os.path.exists(prev):
        os.remove(prev)
    print("done")


if __name__ == "__main__":
    main()
