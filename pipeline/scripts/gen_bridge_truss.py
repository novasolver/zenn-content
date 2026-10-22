# -*- coding: utf-8 -*-
"""Bridge truss FEM visuals. Faithful to bridge-truss.html:
bar-element K=EA/L, penalty BCs, Gaussian solve. 5-panel truss,
mid-span point load. Tension=red, Compression=blue.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import figlib

SLUG = "bridge-truss"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; RED = "#e74c3c"; BLUE = "#3498db"
GREY = "#95a5a6"; ORANGE = "#f39c12"

def build():
    panels = 5; Lp = 1.0; H = 1.0
    nodes = [[i*Lp, 0.0] for i in range(panels+1)]
    nodes += [[(i+0.5)*Lp, H] for i in range(panels)]
    nb = panels + 1
    el = [[i, i+1] for i in range(panels)]
    el += [[nb+i, nb+i+1] for i in range(panels-1)]
    for i in range(panels):
        el += [[i, nb+i], [i+1, nb+i]]
    for i in range(panels):
        el += [[i+1, nb+i]]
    seen = set(); out = []
    for e in el:
        key = (min(e), max(e))
        if key not in seen:
            seen.add(key); out.append(e)
    return np.array(nodes, float), out

def solve(F_kN=100, E_GPa=200, A_cm2=50):
    nodes, el = build()
    E = E_GPa*1e9; A = A_cm2*1e-4; F = F_kN*1e3
    n = len(nodes); ndof = 2*n
    K = np.zeros((ndof, ndof)); Fv = np.zeros(ndof)
    for (i, j) in el:
        dx, dy = nodes[j]-nodes[i]
        L = np.hypot(dx, dy); c = dx/L; s = dy/L; k = E*A/L
        d = [2*i, 2*i+1, 2*j, 2*j+1]
        T = np.array([[c*c, c*s, -c*c, -c*s],
                      [c*s, s*s, -c*s, -s*s],
                      [-c*c, -c*s, c*c, c*s],
                      [-c*s, -s*s, c*s, s*s]])
        for a in range(4):
            for b in range(4):
                K[d[a]][d[b]] += k*T[a][b]
    Fv[2*2+1] = -F  # mid node = floor(5/2)=2
    BIG = 1e20
    K[0][0] += BIG; K[1][1] += BIG; K[2*5+1][2*5+1] += BIG
    U = np.linalg.solve(K, Fv)
    forces = []
    for (i, j) in el:
        dx, dy = nodes[j]-nodes[i]
        L = np.hypot(dx, dy); c = dx/L; s = dy/L
        du = (U[2*j]-U[2*i])*c + (U[2*j+1]-U[2*i+1])*s
        forces.append(E*A/L*du/1e3)
    forces = np.array(forces)
    maxDisp = max(np.hypot(U[2*i], U[2*i+1]) for i in range(n))*1000
    return nodes, el, forces, U, maxDisp

def fcolor(f, maxF):
    if abs(f) < 0.01: return GREY
    return RED if f > 0 else BLUE

def draw_truss(ax, nodes, el, forces, U, scale, title):
    ax.set_facecolor("#020d1a")
    maxF = max(np.abs(forces).max(), 1e-3)
    # undeformed ghost
    for (i, j) in el:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]],
                color="#33405a", lw=1.0, ls="-", zorder=1)
    # deformed with force colors
    dn = nodes.copy()
    dn[:, 0] = nodes[:, 0] + U[0::2]*scale
    dn[:, 1] = nodes[:, 1] + U[1::2]*scale
    for idx, (i, j) in enumerate(el):
        f = forces[idx]; t = min(abs(f)/maxF, 1.0)
        ax.plot([dn[i][0], dn[j][0]], [dn[i][1], dn[j][1]],
                color=fcolor(f, maxF), lw=1.8+t*4.2, zorder=2,
                solid_capstyle="round")
    ax.scatter(dn[:, 0], dn[:, 1], s=30, c=CYAN, edgecolors="white",
               linewidths=1.0, zorder=3)
    # supports
    ax.plot(nodes[0][0], nodes[0][1]-0.02, marker="^", ms=13,
            color="#2ecc71", zorder=4)
    ax.plot(nodes[5][0], nodes[5][1]-0.02, marker="^", ms=13,
            color="#2ecc71", zorder=4)
    # load arrow at mid node (2)
    ax.annotate("", xy=(nodes[2][0], nodes[2][1]+0.03),
                xytext=(nodes[2][0], nodes[2][1]+0.45),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.2), zorder=5)
    ax.set_xlim(-0.4, 5.4); ax.set_ylim(-0.4, 1.7); ax.axis("off")
    ax.set_aspect("equal")
    ax.set_title(title, color="white", fontsize=10)

# ---- compute base case ----
nodes, el, forces, U, maxDisp = solve()
maxF = np.abs(forces).max()
maxIdx = int(np.argmax(np.abs(forces)))
print(f"base: maxDisp={maxDisp:.3f}mm maxF={maxF:.1f}kN member=#{maxIdx+1} "
      f"stress={maxF*1e3/(50e-4)/1e6:.1f}MPa")

# ===== charts-closeup: truss + bar chart =====
fig = plt.figure(figsize=(9.6, 5.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.50, 0.92, 0.44])
draw_truss(ax1, nodes, el, forces, U, 200,
           f"Pratt トラス 変形図（200x拡大）— 赤=引張 / 青=圧縮  最大軸力 {maxF:.0f}kN #{maxIdx+1}")
ax2 = fig.add_axes([0.09, 0.10, 0.86, 0.30]); ax2.set_facecolor(NAVY)
xs = np.arange(1, len(forces)+1)
cols = [RED if f >= 0 else BLUE for f in forces]
ax2.bar(xs, forces, color=cols, width=0.7)
ax2.axhline(0, color="#9fb2d6", lw=0.8)
ax2.set_xticks(xs); ax2.set_xticklabels([f"#{i}" for i in xs], fontsize=7, color="#9fb2d6")
ax2.set_ylabel("軸力 (kN)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("各部材の軸力 — 正=引張 負=圧縮（下弦材は引張・上弦材は圧縮）",
              color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ===== cover =====
figc = plt.figure(figsize=(5.4, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.04, 0.96, 0.92])
draw_truss(axc, nodes, el, forces, U, 200, "")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "トラス橋を", "FEMで解く",
                  "K·u=F で引張(赤)・圧縮(青)の地図を描く", cc)
os.remove(cc)

# ===== slider-anim.gif: increasing load =====
frames = []
loads = list(np.linspace(20, 500, 22)) + list(np.linspace(460, 60, 12))
for Ff in loads:
    nodes, el, forces, U, md = solve(F_kN=Ff)
    mf = np.abs(forces).max()
    f2 = plt.figure(figsize=(5.6, 3.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.02, 0.04, 0.96, 0.88])
    draw_truss(a, nodes, el, forces, U, 200,
               f"集中荷重 F={Ff:.0f}kN  →  最大変位 {md:.2f}mm / 最大軸力 {mf:.0f}kN")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
