# -*- coding: utf-8 -*-
"""digital-pid-discretization visuals: discrete step response + Ts sweep + Ts-sweep gif.
ASCII labels only, faithful to the tool's discrete PID model.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "digital-pid-discretization"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"; RED = "#fb7185"; WHITE = "#e8eefc"

def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# Ideal discrete PID on a 1st-order ZOH-discretized plant G(s)=K/(tau s+1)
Kp, Ti, Td, K, tau = 2.5, 1.8, 0.25, 1.0, 1.0
Ki, Kd = Kp / Ti, Kp * Td

def step_response(Ts, Tend=12.0):
    ad = math.exp(-Ts / tau); bd = K * (1 - ad)
    y = 0.0; S = 0.0; e_prev = 0.0
    n = int(Tend / Ts)
    t = [0.0]; ys = [0.0]
    for k in range(n):
        e = 1.0 - y
        S += e
        u = Kp * e + Ki * Ts * S + Kd * (e - e_prev) / Ts
        y = ad * y + bd * u
        e_prev = e
        t.append((k + 1) * Ts); ys.append(y)
    return np.array(t), np.array(ys)

# ---------- charts-closeup: step responses for several Ts + kd/noise vs Ts ----------
fig = plt.figure(figsize=(9.2, 4.3)); fig.patch.set_facecolor(NAVY)
ax = fig.add_axes([0.08, 0.14, 0.44, 0.76]); style(ax)
ax.axhline(1.0, color="#3b4a6b", lw=1, ls="--")
for Ts, c, lab in [(0.05, BLUE, "Ts=0.05s (clean)"), (0.20, ORANGE, "Ts=0.20s"), (0.26, RED, "Ts=0.26s (oscillatory)")]:
    t, y = step_response(Ts)
    ax.step(t, y, where="post", color=c, lw=1.9, label=lab)
ax.set_ylim(-0.1, 1.6)
ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
ax.set_xlabel("time t [s]", color="white", fontsize=9)
ax.set_ylabel("output y[k]", color="white", fontsize=9)
ax.set_title("Discrete PID step response: coarse Ts degrades stability", color="white", fontsize=10)

ax2 = fig.add_axes([0.61, 0.16, 0.36, 0.74]); style(ax2)
tsg = np.linspace(0.005, 0.3, 200)
kd = Kp * Td / tsg
noise = 1 + (Kp * Td / tsg) / 12.0
ax2.plot(tsg, kd, color=GREEN, lw=2.2, label="kd = Kp*Td/Ts")
ax2.plot(tsg, noise, color=RED, lw=2.0, label="noise gain = 1+kd/N")
ax2.scatter([0.05], [Kp * Td / 0.05], color="white", zorder=5, s=28)
ax2.annotate("Ts=0.05 -> kd=12.5", (0.05, 12.5), color="white", fontsize=8,
             xytext=(0.09, 30), arrowprops=dict(color="white", arrowstyle="->", lw=0.8))
ax2.set_xlabel("sampling period Ts [s]", color="white", fontsize=9)
ax2.set_ylabel("discrete coefficient", color="white", fontsize=8)
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("kd blows up as Ts -> 0 (noise amplification)", color="white", fontsize=10)
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png"); figlib.save_fig(fig, cu, dpi=130); print(" closeup")

# ---------- cover ----------
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.16, 0.84, 0.78]); style(axc)
axc.axhline(1.0, color="#3b4a6b", lw=1, ls="--")
for Ts, c in [(0.05, BLUE), (0.20, ORANGE), (0.26, RED)]:
    t, y = step_response(Ts); axc.step(t, y, where="post", color=c, lw=1.9)
axc.set_ylim(-0.1, 1.6)
axc.set_xlabel("t [s]", color="white", fontsize=9); axc.set_ylabel("y[k]", color="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "デジタルPIDの", "離散化", "サンプリング周期Tsで応答・位相遅れ・ノイズが変わる", cc)
os.remove(cc)

# ---------- gif: sweep Ts and watch step response degrade ----------
frames = []
ts_seq = list(np.linspace(0.03, 0.27, 22)) + list(np.linspace(0.27, 0.03, 8))
for Ts in ts_seq:
    fr = plt.figure(figsize=(4.9, 3.0)); fr.patch.set_facecolor(NAVY)
    g = fr.add_axes([0.13, 0.16, 0.83, 0.74]); style(g)
    g.axhline(1.0, color="#3b4a6b", lw=1, ls="--")
    t, y = step_response(Ts)
    col = RED if Ts >= 0.24 else (ORANGE if Ts >= 0.15 else BLUE)
    g.step(t, y, where="post", color=col, lw=1.9)
    g.set_ylim(-0.1, 1.7); g.set_xlim(0, 12)
    g.set_xlabel("t [s]", color="white", fontsize=9); g.set_ylabel("y[k]", color="white", fontsize=9)
    g.set_title(f"Ts={Ts:.2f}s : kd={Kp*Td/Ts:.1f}, lag grows with Ts", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(fr, dpi=90))
figlib.save_gif(frames, SLUG, duration=120); print("done")
