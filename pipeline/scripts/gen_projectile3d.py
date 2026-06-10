# -*- coding: utf-8 -*-
"""3D projectile visuals (drag + Magnus + wind), faithful to projectile-3d.html.
RK4, dt=0.005, rho=1.225, g=9.81, Fd=0.5*Cd*rho*A*v*v, CL=min(0.5*omega*d/v,0.5),
Fm=0.5*CL*rho*A*v*v acting horizontally perpendicular to relative velocity."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "projectile-3d"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; RED = "#ef4444"; GREEN = "#22c55e"
RHO = 1.225; G = 9.81; DT = 0.005


def traj(v0, theta_deg, phi_deg, cd, area_cm2, mass, spin_rpm,
         wind_speed=0.0, wind_dir_deg=0.0, no_drag=False):
    theta = math.radians(theta_deg); phi = math.radians(phi_deg)
    wind_dir = math.radians(wind_dir_deg)
    area = area_cm2 * 1e-4
    x = y = z = 0.0
    vx = v0 * math.cos(theta) * math.cos(phi)
    vy = v0 * math.cos(theta) * math.sin(phi)
    vz = v0 * math.sin(theta)
    wx = wind_speed * math.cos(wind_dir); wy = wind_speed * math.sin(wind_dir)
    omega = spin_rpm * 2 * math.pi / 60
    d = 2 * math.sqrt(area / math.pi)
    xs = [x]; ys = [y]; zs = [z]

    def deriv(pvx, pvy, pvz):
        rx = pvx - wx; ry = pvy - wy; rz = pvz
        v = math.sqrt(rx*rx + ry*ry + rz*rz) or 1e-9
        if no_drag:
            return (0.0, 0.0, -G)
        Fd = 0.5 * cd * RHO * area * v * v
        ax = -Fd * rx / (v * mass); ay = -Fd * ry / (v * mass); az = -Fd * rz / (v * mass)
        CL = min(0.5 * omega * d / v, 0.5)
        Fm = 0.5 * CL * RHO * area * v * v
        vmh = math.sqrt(rx*rx + ry*ry) or 1e-9
        axm = Fm * (-ry / vmh) / mass; aym = Fm * (rx / vmh) / mass
        return (ax + axm, ay + aym, az - G)

    it = 50000
    while z >= 0 and it > 0:
        it -= 1
        k1 = deriv(vx, vy, vz)
        k2 = deriv(vx+0.5*DT*k1[0], vy+0.5*DT*k1[1], vz+0.5*DT*k1[2])
        k3 = deriv(vx+0.5*DT*k2[0], vy+0.5*DT*k2[1], vz+0.5*DT*k2[2])
        k4 = deriv(vx+DT*k3[0], vy+DT*k3[1], vz+DT*k3[2])
        vx += DT*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6
        vy += DT*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        vz += DT*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6
        x += vx*DT; y += vy*DT; z += vz*DT
        xs.append(x); ys.append(y); zs.append(z)
    # interpolate landing to z=0 (like the tool)
    if len(zs) > 1 and zs[-2] >= 0 and zs[-1] < 0:
        t = zs[-2] / (zs[-2] - zs[-1])
        xs[-1] = xs[-2] + t*(xs[-1]-xs[-2])
        ys[-1] = ys[-2] + t*(ys[-1]-ys[-2])
        zs[-1] = 0.0
    return np.array(xs), np.array(ys), np.array(zs)


def style(ax, xl, yl, title=None):
    ax.set_facecolor(NAVY)
    ax.set_xlabel(xl, color="white", fontsize=9)
    ax.set_ylabel(yl, color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")
    ax.grid(color="#1c2a44", lw=0.6)
    if title:
        ax.set_title(title, color="white", fontsize=10)


# Baseball preset for the side-view comparison (drag vs vacuum)
bx, by, bz = traj(42, 15, 0, 0.35, 29, 0.145, 2000)
vx_, vy_, vz_ = traj(42, 15, 0, 0.35, 29, 0.145, 2000, no_drag=True)
# spin on/off top view (sidespin: phi swept by Magnus). Use phi=0, look at lateral y.
sx, sy, sz = traj(42, 15, 0, 0.35, 29, 0.145, 2000)        # spin 2000
nx, ny, nz = traj(42, 15, 0, 0.35, 29, 0.145, 0)           # spin 0


def draw_side(ax, title=None):
    style(ax, "水平距離 X (m)", "高さ Z (m)", title)
    ax.plot(vx_, vz_, color="#9fb2d6", lw=1.4, ls="--", label="真空 (89.7m)")
    ax.plot(bx, bz, color=CYAN, lw=2.4, label="空気抵抗あり (71.9m)")
    pk = int(np.argmax(bz))
    ax.plot(bx[pk], bz[pk], "o", color=ORANGE, ms=7)
    ax.annotate("最高点 H=5.3m", (bx[pk], bz[pk]), color=ORANGE, fontsize=8,
                xytext=(bx[pk]-2, bz[pk]+0.9))
    ax.plot(bx[-1], 0, "o", color=RED, ms=7)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")


def draw_top(ax, title=None):
    style(ax, "飛距離 X (m)", "横方向 Y (m)", title)
    ax.plot(nx, ny, color="#9fb2d6", lw=1.6, ls="--", label="スピン 0 (偏向 0.0m)")
    ax.plot(sx, sy, color=GREEN, lw=2.4, label="スピン 2000rpm (偏向 5.6m)")
    ax.plot(sx[-1], sy[-1], "o", color=RED, ms=6)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower left")


# ---- charts-closeup: side view + top view ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.15, 0.42, 0.74]); draw_side(ax1, "側面図: 真空 vs 空気抵抗 (野球プリセット)")
ax2 = fig.add_axes([0.585, 0.15, 0.39, 0.74]); draw_top(ax2, "上面図: マグナス効果による横偏向")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.14, 0.85, 0.80]); draw_side(axc)
axc.get_legend().remove()
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "3次元飛翔体運動", "",
                  "空気抵抗・マグナス効果・風をRK4で積分", cc)
os.remove(cc)

# ---- gif: sweep spin 0 -> 4000 -> 0, show top-view deflection grow ----
frames = []
spins = list(range(0, 4001, 250)) + list(range(3750, -1, -250))
for sp in spins:
    txx, tyy, tzz = traj(42, 15, 0, 0.35, 29, 0.145, sp)
    defl = abs(tyy[-1])
    f2 = plt.figure(figsize=(5.6, 3.3)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.16, 0.83, 0.74]); style(a, "飛距離 X (m)", "横方向 Y (m)")
    a.plot(txx, tyy, color=GREEN, lw=2.4)
    a.plot(txx[-1], tyy[-1], "o", color=RED, ms=8)
    a.set_xlim(0, 78); a.set_ylim(-1, 13)
    a.set_title(f"スピン {sp} rpm   横偏向 {defl:.1f} m", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
