# -*- coding: utf-8 -*-
"""Elastic (spring) pendulum visuals. EOM as the tool:
r'' = r th'^2 - g cos th + (k/m)(L0 - r);  th'' = (-g sin th - 2 r' th')/r.
RK4. Demonstrates 2:1 autoparametric resonance (w_spring = 2 w_pendulum)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "spring-pendulum"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"
g = 9.81

def deriv(s, k, m, L0):
    r, dr, th, dth = s
    rs = max(r, 0.01)
    # physically correct hanging elastic pendulum (theta from downward vertical):
    # gravity is +g cos(theta) outward, so hanging (theta=0) is the stable equilibrium.
    ddr = rs * dth * dth + g * np.cos(th) - (k / m) * (rs - L0)
    ddth = (-g * np.sin(th) - 2 * dr * dth) / rs
    return np.array([dr, ddr, dth, ddth])

def energy(s, k, m, L0):
    r, dr, th, dth = s
    KE = 0.5 * m * (dr * dr + r * r * dth * dth)
    return KE - m * g * r * np.cos(th) + 0.5 * k * (r - L0) ** 2

def e_spring(s, k, m, L0):   # bounce(radial) energy
    r, dr, th, dth = s
    return 0.5 * m * dr * dr + 0.5 * k * (r - L0) ** 2

def e_swing(s, k, m, L0):    # swing(angular) energy incl. gravity (offset so >=0)
    r, dr, th, dth = s
    return 0.5 * m * r * r * dth * dth + m * g * r * (1 - np.cos(th))

def run(k, m, L0, r0, th0_deg, T=24, dt=0.0002):
    s = np.array([r0, 0.0, np.radians(th0_deg), 0.0]); E0 = energy(s, k, m, L0)
    nrec = int(T / dt); rec = max(1, nrec // 1400)
    ts, xs, ys, Es, Esp, Esw = [], [], [], [], [], []
    Emin = Emax = E0
    for i in range(nrec):
        k1 = deriv(s, k, m, L0); k2 = deriv(s + 0.5*dt*k1, k, m, L0)
        k3 = deriv(s + 0.5*dt*k2, k, m, L0); k4 = deriv(s + dt*k3, k, m, L0)
        s = s + dt/6*(k1 + 2*k2 + 2*k3 + k4)
        E = energy(s, k, m, L0); Emin = min(Emin, E); Emax = max(Emax, E)
        if i % rec == 0:
            r, dr, th, dth = s
            ts.append(i*dt); xs.append(r*np.sin(th)); ys.append(-r*np.cos(th))
            Es.append(E); Esp.append(e_spring(s,k,m,L0)); Esw.append(e_swing(s,k,m,L0))
    drift = (Emax - Emin) / abs(E0) * 100
    return map(np.array, (ts, xs, ys, Es, Esp, Esw)), drift

# 2:1 autoparametric resonance uses the STRETCHED equilibrium length r_eq=L0+mg/k:
# w_spring = sqrt(k/m) = 2*w_swing = 2*sqrt(g/r_eq). Sweep found k~28 (m=0.5,L0=0.5).
m, L0, k21 = 0.5, 0.5, 28.0
r_eq = L0 + m * g / k21
ws, wth = np.sqrt(k21 / m), np.sqrt(g / r_eq)
print(f"k={k21}: r_eq={r_eq:.3f} w_spring={ws:.2f} 2*w_swing={2*wth:.2f} ratio={ws/wth:.2f}")
# release from natural length (spring snaps & swings), small seed angle -> transfers to swing
(ts, xs, ys, Es, Esp, Esw), drift = run(k21, m, L0, L0, 3, T=60)
print(f"energy drift over 24s = {drift:.3f}%")

# closeup: trajectory + energy exchange
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.08, 0.40, 0.84]); ax1.set_facecolor(NAVY)
ax1.plot(xs, ys, color=CYAN, lw=0.7, alpha=0.85)
ax1.plot(0, 0, "s", color="#3b4a6b", ms=8); ax1.plot(xs[-1], ys[-1], "o", color=ORANGE, ms=8)
ax1.set_aspect("equal"); ax1.set_xticks([]); ax1.set_yticks([])
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title("おもりの軌跡（2:1 共振）", color="white", fontsize=10)
ax2 = fig.add_axes([0.55, 0.16, 0.42, 0.72]); ax2.set_facecolor(NAVY)
ax2.plot(ts, Esp, color=ORANGE, lw=1.4, label="バネ（上下）エネルギー")
ax2.plot(ts, Esw, color=CYAN, lw=1.4, label="振り子（振れ）エネルギー")
ax2.plot(ts, Es - Es.min(), color="white", lw=1.0, ls="--", alpha=0.7, label="合計（一定）")
ax2.set_xlabel("時間 t (s)", color="white", fontsize=9); ax2.set_ylabel("エネルギー (J)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
ax2.set_title("バネ ⇄ 振り子 のエネルギー授受", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.04, 0.92, 0.92]); axc.set_facecolor(NAVY)
axc.plot(xs, ys, color=CYAN, lw=0.7, alpha=0.85); axc.plot(0, 0, "s", color="#3b4a6b", ms=8)
axc.set_aspect("equal"); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "弾性振り子と", "パラメトリック共振", "バネと振れが2:1で連成しエネルギーが行き来", cc)
os.remove(cc)

# gif: the spring-pendulum moving (draw spring + bob)
(ts2, xs2, ys2, Es2, Esp2, Esw2), _ = run(k21, m, L0, L0, 3, T=20, dt=0.0002)
frames = []
step = max(1, len(xs2) // 60)
for idx in range(0, len(xs2), step):
    bx, by = xs2[idx], ys2[idx]
    f2 = plt.figure(figsize=(3.8, 4.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.0, 1.0, 0.93]); a.set_facecolor(NAVY)
    # zigzag spring from pivot(0,0) to bob
    n_coil = 14; tt = np.linspace(0, 1, n_coil * 2 + 2)
    px, py = np.array([0, bx]), np.array([0, by]); L = np.hypot(bx, by)
    ux, uy = bx / L, by / L; perp = np.array([-uy, ux])
    base = np.outer(tt, [bx, by])
    zig = np.where(np.arange(len(tt)) % 2 == 0, 0.03, -0.03)
    zig[0] = zig[-1] = 0
    sx = base[:, 0] + zig * perp[0] * L * 0.5
    sy = base[:, 1] + zig * perp[1] * L * 0.5
    a.plot(sx, sy, color="#9fb2d6", lw=1.2)
    a.plot(bx, by, "o", color=ORANGE, ms=16, mec="white")
    a.plot(0, 0, "s", color="#3b4a6b", ms=9)
    a.plot(xs2[max(0,idx-120):idx+1], ys2[max(0,idx-120):idx+1], color=CYAN, lw=0.6, alpha=0.5)
    a.set_xlim(-0.85, 0.85); a.set_ylim(-1.0, 0.15); a.set_aspect("equal"); a.axis("off")
    a.set_title(f"弾性振り子  t={ts2[idx]:.1f}s", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=70)
print("done.")
