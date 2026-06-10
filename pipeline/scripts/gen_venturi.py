# -*- coding: utf-8 -*-
"""Generate venturi-meter visuals (cover, charts-closeup, slider-anim).
Physics reproduced from tools/venturi-meter.html compute().
ASCII-only prints. No emoji.
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import figlib

SLUG = "venturi-meter"
NAVY = "#001F3F"
ACC = "#007BFF"
ACC2 = "#00B4D8"
GREEN = "#00b894"
ORANGE = "#e17055"


def Qh(D1, D2, dp_kPa, rho=998.0, Cd=0.980):
    A2 = math.pi * (D2 / 1000.0) ** 2 / 4.0
    beta = D2 / D1
    beta4 = beta ** 4
    V2 = math.sqrt(2 * (dp_kPa * 1000.0) / (rho * (1 - beta4)))
    return Cd * A2 * V2 * 3600.0


def pressure_profile(beta, recov_frac):
    """Normalized pressure p(x) along the tube, matching the canvas model."""
    rPipe = 1.0
    rTh = max(0.18, min(0.92, beta))

    def radius(u):
        if u < 0.28:
            return rPipe
        if u < 0.45:
            return rPipe + (rTh - rPipe) * ((u - 0.28) / 0.17)
        if u < 0.55:
            return rTh
        if u < 0.92:
            return rTh + (rPipe - rTh) * ((u - 0.55) / 0.37)
        return rPipe

    us = np.linspace(0, 1, 200)
    denom = (rPipe / max(rTh, 1e-6)) ** 4 - 1 + 1e-6
    ps = []
    for u in us:
        r = radius(u)
        drop = (rPipe / max(r, 1e-6)) ** 4 - 1
        dn = drop / denom
        if u <= 0.50:
            ps.append(1 - dn)
        else:
            back = (u - 0.50) / 0.50
            ps.append(back * recov_frac)
    return us, np.array(ps)


def fig_dp_curve(dp_now=20.0, D1=100, D2=50, save=None, dpi=110):
    fig, ax = plt.subplots(figsize=(6.0, 3.6), facecolor="white")
    dps = np.linspace(0.1, 250, 200)
    q = [Qh(D1, D2, d) for d in dps]
    ax.plot(dps, q, color=ACC, lw=2.6)
    ax.fill_between(dps, q, color=ACC, alpha=0.12)
    yn = Qh(D1, D2, dp_now)
    ax.plot([dp_now], [yn], "o", color=ORANGE, ms=10, zorder=5)
    ax.annotate(f"dp={dp_now:.0f} kPa\nQ={yn:.1f} m3/h",
                xy=(dp_now, yn), xytext=(dp_now + 35, yn - 22),
                color=NAVY, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.set_xlabel("differential pressure dp (kPa)")
    ax.set_ylabel("volume flow Q (m3/h)")
    ax.set_title("Q proportional to sqrt(dp)", color=NAVY, fontsize=12)
    ax.grid(alpha=0.25)
    ax.set_xlim(0, 250)
    ax.set_ylim(0, max(q) * 1.08)
    fig.tight_layout()
    if save:
        figlib.save_fig(fig, save, dpi=dpi)
    return fig


def fig_closeup():
    """Two-panel: sqrt curve + pressure profile through the tube."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0), facecolor="white")

    # left: Q vs dp
    D1, D2 = 100, 50
    dps = np.linspace(0.1, 250, 200)
    q = [Qh(D1, D2, d) for d in dps]
    ax1.plot(dps, q, color=ACC, lw=2.6)
    ax1.fill_between(dps, q, color=ACC, alpha=0.12)
    for d in (5, 20, 80, 180):
        ax1.plot([d], [Qh(D1, D2, d)], "o", color=ORANGE, ms=7)
    ax1.plot([20], [Qh(D1, D2, 20)], "o", color=ORANGE, ms=10)
    ax1.text(20, Qh(D1, D2, 20) - 14, "20 -> 45.3", color=NAVY, fontsize=9)
    ax1.text(80, Qh(D1, D2, 80) - 14, "80 -> 90.6", color=NAVY, fontsize=9)
    ax1.set_xlabel("differential pressure dp (kPa)")
    ax1.set_ylabel("volume flow Q (m3/h)")
    ax1.set_title("Flow vs dp  (beta=0.5)", color=NAVY, fontsize=12)
    ax1.grid(alpha=0.25)
    ax1.set_xlim(0, 250)
    ax1.set_ylim(0, max(q) * 1.08)

    # right: pressure profile
    us, ps = pressure_profile(0.5, 0.875)
    ax2.plot(us, ps, color=ACC2, lw=2.8)
    ax2.fill_between(us, ps, color=ACC2, alpha=0.12)
    ax2.axvline(0.18, color=ORANGE, ls="--", lw=1, alpha=0.7)
    ax2.axvline(0.50, color=ORANGE, ls="--", lw=1, alpha=0.7)
    ax2.text(0.18, 1.04, "upstream tap", color=NAVY, fontsize=9, ha="center")
    ax2.text(0.50, -0.13, "throat tap", color=NAVY, fontsize=9, ha="center")
    ax2.set_xlabel("axial position x (inlet -> throat -> diffuser)")
    ax2.set_ylabel("normalized pressure p(x)")
    ax2.set_title("Pressure dips at throat, recovers in diffuser",
                  color=NAVY, fontsize=11)
    ax2.grid(alpha=0.25)
    ax2.set_ylim(-0.18, 1.12)

    fig.tight_layout()
    out = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
    figlib.save_fig(fig, out, dpi=130)
    print("  charts-closeup ->", out)
    return out


def make_gif():
    """Animate the dp slider; the operating point sweeps the sqrt curve."""
    frames = []
    dp_vals = list(np.linspace(8, 200, 26))
    dp_vals = dp_vals + dp_vals[::-1]
    for dp in dp_vals:
        fig = fig_dp_curve(dp_now=dp)
        frames.append(figlib.fig_to_pil(fig, dpi=92))
    figlib.save_gif(frames, SLUG, duration=110)


def main():
    figlib.outdir(SLUG)
    closeup = fig_closeup()
    # cover uses the dp curve as preview chart
    prev = os.path.join(figlib.outdir(SLUG), "_cover_chart.png")
    fig_dp_curve(save=prev, dpi=110)
    figlib.make_cover(SLUG,
                      "ベンチュリ流量計",
                      "差圧から流量を測る",
                      "ベルヌーイの定理 x 連続の式",
                      prev)
    make_gif()
    if os.path.exists(prev):
        os.remove(prev)
    print("done")


if __name__ == "__main__":
    main()
