# -*- coding: utf-8 -*-
"""Verify n-body-gravity numbers + figures. Velocity-Verlet (as the tool),
softening to avoid the Newtonian singularity, O(N^2) all-pairs force.
Demo: a dominant central mass + orbiting bodies -> bound, pretty trails."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "n-body-gravity"
NAVY = "#0b1020"
G = 1.0
EPS = 0.08          # softening (scaled)
DT = 0.002
rng = np.random.RandomState(7)   # deterministic (no Math.random at runtime)


def make_system():
    # central star + N light orbiters on near-circular, well-spaced orbits
    pos = [[0.0, 0.0]]; vel = [[0.0, 0.0]]; mass = [200.0]
    radii = [0.9, 1.25, 1.6, 2.0, 2.45, 2.9]
    for r in radii:
        ang = rng.uniform(0, 2*np.pi)
        x, y = r*np.cos(ang), r*np.sin(ang)
        vc = np.sqrt(G*200.0) * r / (r*r+EPS*EPS)**0.75   # softened circular speed
        vc *= rng.uniform(0.97, 1.03)                     # mild eccentricity
        pos.append([x, y]); vel.append([-vc*np.sin(ang), vc*np.cos(ang)])
        mass.append(rng.uniform(0.1, 0.5))                # light -> test-particle-like
    return np.array(pos), np.array(vel), np.array(mass)


def accel(pos, mass):
    n = len(mass); a = np.zeros_like(pos)
    for i in range(n):
        d = pos - pos[i]                       # (n,2)
        r2 = d[:, 0]**2 + d[:, 1]**2 + EPS*EPS
        inv = mass / (r2*np.sqrt(r2))
        inv[i] = 0.0
        a[i, 0] = G*np.sum(inv*d[:, 0]); a[i, 1] = G*np.sum(inv*d[:, 1])
    return a


def energy(pos, vel, mass):
    ke = 0.5*np.sum(mass*np.sum(vel*vel, axis=1))
    pe = 0.0; n = len(mass)
    for i in range(n):
        for j in range(i+1, n):
            d = pos[j]-pos[i]; r = np.sqrt(d[0]**2+d[1]**2+EPS*EPS)
            pe -= G*mass[i]*mass[j]/r
    return ke+pe


def run(pos, vel, mass, nsteps, rec=12):
    a = accel(pos, mass); traj = []
    E0 = energy(pos, vel, mass); Emin = Emax = E0
    for s in range(nsteps):
        vel = vel + 0.5*a*DT
        pos = pos + vel*DT
        a = accel(pos, mass)
        vel = vel + 0.5*a*DT
        E = energy(pos, vel, mass); Emin = min(Emin, E); Emax = max(Emax, E)
        if s % rec == 0:
            traj.append(pos.copy())
    return pos, vel, np.array(traj), E0, Emin, Emax


print("=== n-body verification ===")
pos, vel, mass = make_system()
n = len(mass)
print(f"bodies N={n}, pairwise forces per step = N(N-1)/2 = {n*(n-1)//2}")
pos2, vel2, traj, E0, Emin, Emax = run(pos.copy(), vel.copy(), mass, 13000)
print(f"velocity-Verlet energy: E0={E0:.3f}, drift={(Emax-Emin)/abs(E0)*100:.3f}%")
# without softening the central pass would blow up; show min separation handled
print(f"softening EPS={EPS} keeps force finite at r->0: a_max(r=0)= {G*200/EPS**2:.0f} (finite)")

colors = plt.cm.plasma(np.linspace(0.15, 0.95, n))

# closeup: orbital trails
fig, ax = plt.subplots(figsize=(6.4, 6.0)); fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
for i in range(n):
    t = traj[:, i, :]
    ax.plot(t[:, 0], t[:, 1], color=colors[i], lw=0.8, alpha=0.7)
    ax.scatter(t[-1, 0], t[-1, 1], color=colors[i],
               s=(120 if i == 0 else 30), edgecolors="white", zorder=5)
ax.set_aspect("equal"); ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("N体重力：中心星のまわりの軌道（O(N²)力計算）", color="white", fontsize=11)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup); print("  closeup ->", closeup)

figlib.make_cover(SLUG, "N体重力シミュレーション", "",
                  "velocity-Verlet と軟化長で解く重力多体系", closeup)

# gif: cluster evolving with fading trails
frames = []
nf = 40
total = traj.shape[0]
for k in range(nf):
    fk = int((k+1)/nf*(total-1))
    lo = max(0, fk-90)
    f2, a2 = plt.subplots(figsize=(4.6, 4.4)); f2.patch.set_facecolor(NAVY); a2.set_facecolor(NAVY)
    for i in range(n):
        t = traj[lo:fk+1, i, :]
        if len(t) > 1:
            a2.plot(t[:, 0], t[:, 1], color=colors[i], lw=0.8, alpha=0.6)
        a2.scatter(traj[fk, i, 0], traj[fk, i, 1], color=colors[i],
                   s=(90 if i == 0 else 22), edgecolors="white", zorder=5)
    a2.set_aspect("equal"); a2.set_xlim(-3.2, 3.2); a2.set_ylim(-3.2, 3.2)
    a2.set_xticks([]); a2.set_yticks([])
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
