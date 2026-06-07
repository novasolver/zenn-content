# -*- coding: utf-8 -*-
"""Verify phase-space-portrait numbers + figures. Reproduces the tool's
systems (RK4, dt=0.01): harmonic, damped, van der Pol, duffing, lorenz(x-z).
Focus figure: van der Pol limit cycle + vector field."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "phase-space-portrait"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; BLUE = "#7dd3fc"; FAINT = "#33506e"
DT = 0.01


def rk4(f, s, dt):
    k1 = f(s); k2 = f(s + k1*dt/2); k3 = f(s + k2*dt/2); k4 = f(s + k3*dt)
    return s + (k1 + 2*k2 + 2*k3 + k4)*dt/6


def vdp(mu):
    return lambda s: np.array([s[1], mu*(1 - s[0]**2)*s[1] - s[0]])


def harmonic(w=1.0):
    return lambda s: np.array([s[1], -w*w*s[0]])


def damped(g=0.15, w=1.0):
    return lambda s: np.array([s[1], -2*g*s[1] - w*w*s[0]])


def traj(f, s0, n):
    s = np.array(s0, float); out = [s.copy()]
    for _ in range(n):
        s = rk4(f, s, DT); out.append(s.copy())
    return np.array(out)


# ---- VERIFICATION ----
print("=== phase-space verification ===")
# van der Pol limit-cycle amplitude (should approach ~2.0 in x)
for mu in (0.5, 1.0, 2.0):
    t = traj(vdp(mu), [0.1, 0.0], 20000)
    tail = t[-4000:]
    amp = np.max(np.abs(tail[:, 0]))
    # period: time between successive upward zero crossings of x
    x = tail[:, 0]
    cr = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    per = (cr[-1]-cr[0])/(len(cr)-1)*DT if len(cr) > 2 else float('nan')
    print(f"  vdP mu={mu}: limit-cycle x-amplitude={amp:.3f}, period={per:.2f}")
# harmonic energy conservation
t = traj(harmonic(1.0), [1.0, 0.0], 20000)
E = 0.5*t[:, 1]**2 + 0.5*t[:, 0]**2
print(f"  harmonic energy drift over 200s: {(E.max()-E.min())/E[0]*100:.4f}%")
# damped converges to origin
t = traj(damped(0.15, 1.0), [2.0, 0.0], 20000)
print(f"  damped final |state| after 200s: {np.hypot(*t[-1]):.2e}")


def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="white")
    for s in ax.spines.values(): s.set_color("#445")
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")


def vfield(ax, f, xr, yr, dens=22):
    xs = np.linspace(*xr, dens); ys = np.linspace(*yr, dens)
    X, Y = np.meshgrid(xs, ys)
    U = np.zeros_like(X); V = np.zeros_like(Y)
    for i in range(dens):
        for j in range(dens):
            d = f(np.array([X[i, j], Y[i, j]])); U[i, j], V[i, j] = d
    n = np.hypot(U, V) + 1e-9
    ax.quiver(X, Y, U/n, V/n, color=BLUE, alpha=0.35, width=0.0025, scale=42)


# ---- closeup: van der Pol mu=1 ----
mu = 1.0; f = vdp(mu)
fig, ax = plt.subplots(figsize=(6.6, 5.6)); fig.patch.set_facecolor(NAVY); style(ax)
vfield(ax, f, (-3, 3), (-3.5, 3.5))
for s0 in [[0.05, 0.0], [2.8, 2.8], [-2.8, -2.8], [0.1, 3.2], [-0.1, -3.2]]:
    t = traj(f, s0, 4000)
    ax.plot(t[:, 0], t[:, 1], color=ORANGE, lw=1.1, alpha=0.85)
# the limit cycle itself (heavy)
lc = traj(f, [2.0, 0.0], 20000)[-700:]
ax.plot(lc[:, 0], lc[:, 1], color="#ff7b00", lw=2.6)
ax.set_xlim(-3, 3); ax.set_ylim(-3.5, 3.5)
ax.set_xlabel("x （変位）"); ax.set_ylabel("dx/dt （速度）")
ax.set_title("ファン・デル・ポール振動子のリミットサイクル (μ=1)", color="white", fontsize=11)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup); print("  closeup ->", closeup)

figlib.make_cover(SLUG, "位相空間ポートレート", "で見る非線形振動",
                  "楕円・螺旋・リミットサイクル・カオス", closeup)

# ---- GIF: sweep mu, limit cycle morphs from circle to relaxation ----
frames = []
mus = list(np.linspace(0.2, 4.0, 10)); mus = mus + mus[::-1]
for mv in mus:
    f = vdp(mv)
    lc = traj(f, [2.0, 0.0], 24000)[-1200:]
    f2, a2 = plt.subplots(figsize=(4.8, 4.6)); f2.patch.set_facecolor(NAVY); style(a2)
    a2.plot(lc[:, 0], lc[:, 1], color=ORANGE, lw=2.2)
    a2.set_xlim(-3, 3); a2.set_ylim(-6, 6)
    a2.set_title(f"μ = {mv:.1f}", color="white"); a2.set_xticks([]); a2.set_yticks([])
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=180)
print("done.")
