# -*- coding: utf-8 -*-
"""Verify three-body numbers + figures. Reproduces the tool's leapfrog
(velocity-Verlet KDK), dt=0.0005, softening eps=0.02, G=1, equal masses.
Figure-8 initial conditions (Chenciner-Montgomery)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "three-body"
G = 1.0
EPS = 0.02
DT = 0.0005
m = np.array([1.0, 1.0, 1.0])

# Figure-8 (verbatim from tool)
def figure8():
    x1, y1 = -0.97000436, 0.24308753
    x2, y2 = 0.0, 0.0
    x3, y3 = 0.97000436, -0.24308753
    vx2, vy2 = -0.93240737, -0.86473146
    vx1, vy1 = -vx2/2, -vy2/2
    vx3, vy3 = -vx2/2, -vy2/2
    pos = np.array([[x1, y1], [x2, y2], [x3, y3]])
    vel = np.array([[vx1, vy1], [vx2, vy2], [vx3, vy3]])
    return pos, vel


def accel(pos):
    a = np.zeros_like(pos)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            d = pos[j] - pos[i]
            r2 = d[0]*d[0] + d[1]*d[1] + EPS*EPS
            r3 = r2**1.5
            a[i] += G * m[j] * d / r3
    return a


def energy(pos, vel):
    ke = 0.5 * np.sum(m * np.sum(vel*vel, axis=1))
    pe = 0.0
    for i in range(3):
        for j in range(i+1, 3):
            d = pos[j] - pos[i]
            r = np.sqrt(d[0]*d[0] + d[1]*d[1] + EPS*EPS)
            pe -= G * m[i] * m[j] / r
    return ke + pe


def angmom(pos, vel):
    return np.sum(m * (pos[:, 0]*vel[:, 1] - pos[:, 1]*vel[:, 0]))


def step(pos, vel):
    a = accel(pos)
    vel = vel + 0.5 * a * DT
    pos = pos + vel * DT
    a2 = accel(pos)
    vel = vel + 0.5 * a2 * DT
    return pos, vel


def run(pos, vel, nsteps, record_every=20):
    traj = [[], [], []]
    E0 = energy(pos, vel)
    Emin, Emax = E0, E0
    for s in range(nsteps):
        pos, vel = step(pos, vel)
        E = energy(pos, vel)
        Emin = min(Emin, E); Emax = max(Emax, E)
        if s % record_every == 0:
            for i in range(3):
                traj[i].append(pos[i].copy())
    return pos, vel, np.array(traj), E0, Emin, Emax


print("=== three-body verification ===")
pos, vel = figure8()
E0 = energy(pos, vel)
L0 = angmom(pos, vel)
print(f"initial E = {E0:.6f}, L = {L0:.6f}")
# the standard figure-8 period
T8 = 6.3259
nsteps = int(round(T8 / DT))
pos2, vel2, traj, E0, Emin, Emax = run(pos.copy(), vel.copy(), nsteps)
drift = (Emax - Emin) / abs(E0) * 100
print(f"after one period T={T8}: steps={nsteps}")
print(f"E range [{Emin:.6f}, {Emax:.6f}], drift = {drift:.4f}%")
p0, v0 = figure8()
ret = np.max(np.abs(pos2 - p0))
print(f"max |pos(T) - pos(0)| = {ret:.4f} (periodicity check)")

# sensitivity: perturb body 1 x by 1e-3
pos_p, vel_p = figure8()
pos_p[0, 0] += 1e-3
posA, velA = figure8()
sep = []
pa, va = posA.copy(), velA.copy()
pb, vb = pos_p.copy(), vel_p.copy()
for s in range(int(6*T8/DT)):
    pa, va = step(pa, va)
    pb, vb = step(pb, vb)
    if s % 200 == 0:
        sep.append((s*DT, np.max(np.abs(pa-pb))))
sep = np.array(sep)
# time to reach separation ~1
idx = np.argmax(sep[:, 1] > 1.0)
print(f"perturbation 1e-3 grows to O(1) by t={sep[idx,0]:.2f} (~{sep[idx,0]/T8:.1f} periods)")

# ---- FIGURES ----
# charts-closeup: figure-8 traced over ~2 periods
pos, vel = figure8()
_, _, traj2, _, _, _ = run(pos.copy(), vel.copy(), int(2*T8/DT), record_every=8)
colors = ["#60a5fa", "#f472b6", "#43d47a"]
fig, ax = plt.subplots(figsize=(6.6, 4.4))
fig.patch.set_facecolor("#0b1020"); ax.set_facecolor("#0b1020")
for i in range(3):
    t = traj2[i]
    ax.plot(t[:, 0], t[:, 1], color=colors[i], lw=1.3, alpha=0.85)
    ax.scatter(t[-1, 0], t[-1, 1], color=colors[i], s=120, edgecolors="white", zorder=5)
    ax.text(t[-1, 0], t[-1, 1]+0.06, str(i+1), color="white", ha="center", fontsize=11)
ax.set_title("三体問題：figure-8 周期解（質量3つが1本の8字を共有）", color="white", fontsize=11)
ax.set_aspect("equal"); ax.tick_params(colors="white")
for s in ax.spines.values(): s.set_color("#445")
ax.set_xlabel("x", color="white"); ax.set_ylabel("y", color="white")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup)
print("  closeup ->", closeup)

figlib.make_cover(SLUG, "三体問題の", "カオスとfigure-8",
                  "Leapfrog法で解く重力多体系 — 唯一の安定周期解", closeup)

# gif: figure-8 choreography over time (bodies moving, trail)
pos, vel = figure8()
allpos = []
pp, vv = pos.copy(), vel.copy()
nrec = 60
total = int(T8 / DT)
for s in range(total):
    pp, vv = step(pp, vv)
    if s % (total // nrec) == 0:
        allpos.append(pp.copy())
allpos = np.array(allpos)  # (nrec, 3, 2)
# precompute full trail
full = []
pp, vv = figure8()
pp = pp.copy()
for s in range(int(2*T8/DT)):
    pp_arr = pp
    pp, vv = step(pp, vv)
    full.append(pp.copy())
full = np.array(full)
frames = []
nf = 48
for k in range(nf):
    fk = int((k+1)/nf * (len(full)-1))
    f2, a2 = plt.subplots(figsize=(4.4, 4.0))
    f2.patch.set_facecolor("#0b1020"); a2.set_facecolor("#0b1020")
    lo = max(0, fk-1400)
    for i in range(3):
        a2.plot(full[lo:fk, i, 0], full[lo:fk, i, 1], color=colors[i], lw=1.0, alpha=0.6)
        a2.scatter(full[fk, i, 0], full[fk, i, 1], color=colors[i], s=90, edgecolors="white", zorder=5)
    a2.set_xlim(-1.3, 1.3); a2.set_ylim(-0.55, 0.55)
    a2.set_aspect("equal"); a2.set_xticks([]); a2.set_yticks([])
    a2.set_title("figure-8 choreography", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
