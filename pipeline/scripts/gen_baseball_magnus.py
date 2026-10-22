# -*- coding: utf-8 -*-
"""Baseball Magnus visuals. Faithful to baseball-pitch-magnus.html:
RHO=1.225, M=0.145, R=0.037, CD=0.35, G=9.81; S=r*omega/v, CL=0.1+0.4*min(S,0.5);
Fmag=0.5*rho*CL*A*v^2; trajectory drop/break = 0.5*a*t^2 (constant-accel approx)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "baseball-pitch-magnus"
NAVY = "#0a1929"
BLUE, CYAN, ORANGE, RED, GREEN = "#4ac6ff", "#00B4D8", "#f59e0b", "#ff6b6b", "#9be7a3"

RHO, M, R = 1.225, 0.145, 0.037
A = math.pi * R * R
CD, G = 0.35, 9.81

PRESETS = {
    "ストレート": (145, 2200, 90),
    "カーブ":     (120, 2800, 100),
    "スライダー": (135, 2400, 50),
    "シンカー":   (140, 1800, 115),
    "フォーク":   (130, 200, 90),
    "ナックル":   (105, 50, 0),
}


def pitch(speed_kmh, rpm, axis_deg, dist=18.4, N=60):
    v0 = speed_kmh / 3.6
    omega = rpm * 2 * math.pi / 60
    axis = math.radians(axis_deg)
    S = R * omega / v0
    CL = 0.1 + 0.4 * min(S, 0.5)
    Fmag = 0.5 * RHO * CL * A * v0 * v0
    Fdrag = 0.5 * RHO * CD * A * v0 * v0
    ay = -G + Fmag * math.cos(axis) / M
    ax = Fmag * math.sin(axis) / M
    adec = -Fdrag / M
    tF = dist / v0
    ts = np.linspace(0, tF, N)
    xs = v0 * ts + 0.5 * adec * ts * ts
    yside = 0.5 * ay * ts * ts * 100   # cm
    ytop = 0.5 * ax * ts * ts * 100    # cm
    return dict(xs=xs, yside=yside, ytop=ytop, Fmag=Fmag, Fdrag=Fdrag,
                drop=abs(yside[-1]), brk=abs(ytop[-1]), S=S, CL=CL)


def style_ax(ax, xl, yl, title=None):
    ax.set_facecolor(NAVY)
    ax.set_xlabel(xl, color="white", fontsize=9)
    ax.set_ylabel(yl, color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")
    ax.grid(True, color="#22324d", lw=0.6)
    if title:
        ax.set_title(title, color="white", fontsize=10)


# ---- closeup: bar comparison of drop/break per pitch ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.52, 0.72])
names = list(PRESETS.keys())
drops = [pitch(*PRESETS[n])["drop"] for n in names]
brks = [pitch(*PRESETS[n])["brk"] for n in names]
x = np.arange(len(names))
ax1.bar(x - 0.2, drops, 0.4, color=BLUE, label="落下量 (cm)")
ax1.bar(x + 0.2, brks, 0.4, color=CYAN, label="横変化量 (cm)")
ax1.set_xticks(x); ax1.set_xticklabels(names, fontsize=8)
style_ax(ax1, "", "変化量 (cm)", "球種別 変化量（投球距離 18.4 m）")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)

ax2 = fig.add_axes([0.67, 0.16, 0.30, 0.72])
for n, c in zip(["ストレート", "カーブ", "スライダー"], [GREEN, RED, ORANGE]):
    p = pitch(*PRESETS[n])
    ax2.plot(p["xs"], p["yside"], color=c, lw=2.2, label=n)
style_ax(ax2, "投球距離 (m)", "垂直変位 (cm)", "投球軌道（側面）")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.78])
for n, c in zip(["ストレート", "カーブ", "スライダー", "シンカー"], [GREEN, RED, ORANGE, CYAN]):
    p = pitch(*PRESETS[n])
    axc.plot(p["xs"], p["yside"], color=c, lw=2.4)
style_ax(axc, "投球距離 (m)", "垂直変位 (cm)")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "変化球とマグヌス力", "", "F = ½·ρ·CL·A·v² で曲がる投球軌道", cc)
os.remove(cc)

# ---- gif: sweep rpm, watch break/drop grow ----
frames = []
rpm_list = list(range(400, 3200, 280)) + list(range(3200, 400, -280))
for rpm in rpm_list:
    p = pitch(135, rpm, 50)  # slider-like, axis 50
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.81, 0.70])
    a.plot(p["xs"], p["yside"], color=BLUE, lw=2.4, label="縦（落下）")
    a.plot(p["xs"], p["ytop"], color=ORANGE, lw=2.4, label="横（変化）")
    style_ax(a, "投球距離 (m)", "変位 (cm)")
    a.set_ylim(-180, 90)
    a.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower left")
    a.set_title(f"球速135km/h, {rpm}rpm → Fmag={p['Fmag']:.2f}N", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
