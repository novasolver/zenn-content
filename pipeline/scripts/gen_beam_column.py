# -*- coding: utf-8 -*-
"""Beam-column (P-M interaction) visuals, faithful to tools/beam-column.html.
EN1993-1-1 simplified interaction: N/Nb_Rd + kyy*My/Mb_Rd + kyz*Mz/Mbz_Rd <= 1.
Buckling curve b (alpha=0.34). Produces cover/charts-closeup/slider-anim.
ASCII-only prints; no emoji. Matplotlib only (no Selenium)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "beam-column"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; RED = "#f87171"; GREEN = "#34d399"

# HEA300 / S235 (the tool defaults)
SEC = dict(A=112.5, Iy=18260, Wy=1260, Wz=631)  # cm-based
MAT = dict(fy=235, E=210000)                      # MPa
ALPHA = 0.34                                       # curve b

def calc(L, K, N_Ed, My_Ed, Mz_Ed):
    E = MAT["E"]; fy = MAT["fy"]; EPa = E*1e6; fyPa = fy*1e6
    A = SEC["A"]*1e-4; Iy = SEC["Iy"]*1e-8; Wy = SEC["Wy"]*1e-6; Wz = SEC["Wz"]*1e-6
    KL = K*L
    Ncr = (math.pi**2*EPa*Iy)/(KL**2)/1e3
    lam = math.sqrt((A*fyPa)/(Ncr*1e3))
    Phi = 0.5*(1+ALPHA*(lam-0.2)+lam**2)
    chi = min(1.0, 1.0/(Phi+math.sqrt(max(0, Phi**2-lam**2))))
    Nb_Rd = chi*A*fyPa/1e3
    Mb_Rd = Wy*fyPa/1e3
    Mbz_Rd = Wz*fyPa/1e3
    mu = min(0.8, lam)
    kyy = 1+mu*(N_Ed/Nb_Rd); kyz = 0.6*kyy
    UN = N_Ed/Nb_Rd; UM = My_Ed/Mb_Rd; UMz = Mz_Ed/(Mbz_Rd if Mbz_Rd > 0 else 1)
    eta = UN+kyy*UM+kyz*UMz
    return dict(Ncr=Ncr, lam=lam, chi=chi, Nb_Rd=Nb_Rd, Mb_Rd=Mb_Rd, Mbz_Rd=Mbz_Rd,
                kyy=kyy, UMz=UMz, eta=eta)

def envelope(L, K, Mz_Ed):
    """P-M envelope at fixed Mz, reproducing the tool's loop."""
    r = calc(L, K, 0, 0, Mz_Ed)
    Nb_Rd, Mb_Rd, lam = r["Nb_Rd"], r["Mb_Rd"], r["lam"]
    mz_fixed = r["UMz"]
    xs, ys = [], []
    for i in range(101):
        n = i/100.0
        N_i = n*Nb_Rd
        kyy_i = 1+min(0.8, lam)*n
        kyz_i = 0.6*kyy_i
        my_max = max(0.0, (1.0-n-kyz_i*mz_fixed)/(kyy_i if kyy_i > 0 else 1))
        xs.append(my_max*Mb_Rd); ys.append(N_i)
    return np.array(xs), np.array(ys)

def chi_curve(lams):
    out = []
    for lam in lams:
        Phi = 0.5*(1+ALPHA*(lam-0.2)+lam**2)
        out.append(min(1.0, 1.0/(Phi+math.sqrt(max(0, Phi**2-lam**2)))))
    return np.array(out)

def style_ax(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# ---- charts-closeup: P-M diagram (PASS vs FAIL) + chi-vs-slenderness ----
fig = plt.figure(figsize=(9.8, 4.5)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.07, 0.15, 0.40, 0.72]); style_ax(ax1)
xs, ys = envelope(5.0, 1.0, 30)
ax1.fill_between(xs, ys, color=CYAN, alpha=0.10)
ax1.plot(xs, ys, color=CYAN, lw=2.2, label="P-M 包絡線 (Mz=30)")
# design points: default PASS, overload FAIL
ax1.plot(120, 800, "o", color=GREEN, ms=11, label="設計点 N=800 (eta=0.93 PASS)")
ax1.plot(120, 1500, "X", color=RED, ms=12, label="N=1500 (eta=1.28 FAIL)")
ax1.set_xlabel("My,Ed (kN.m)", color="white", fontsize=9)
ax1.set_ylabel("N (kN)", color="white", fontsize=9)
ax1.set_xlim(0, max(xs)*1.05); ax1.set_ylim(0, 2600)
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=6.8, loc="upper right")
ax1.set_title("P-M 相関図: 包絡線の内側=安全", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.15, 0.39, 0.72]); style_ax(ax2)
lams = np.linspace(0.1, 3.0, 200)
ax2.plot(lams, chi_curve(lams), color=CYAN, lw=2.2)
for L, c, lbl in [(5.0, GREEN, "L=5m"), (8.0, ORANGE, "L=8m"), (10.0, RED, "L=10m")]:
    r = calc(L, 1.0, 800, 120, 30)
    ax2.plot(r["lam"], r["chi"], "o", color=c, ms=10)
    ax2.annotate("%s lam=%.2f\nchi=%.2f" % (lbl, r["lam"], r["chi"]),
                 (r["lam"], r["chi"]), color=c, fontsize=7,
                 xytext=(8, -2), textcoords="offset points")
ax2.set_xlabel("無次元細長比 lam-bar", color="white", fontsize=9)
ax2.set_ylabel("座屈低減係数 chi", color="white", fontsize=9)
ax2.set_xlim(0, 3.0); ax2.set_ylim(0, 1.08)
ax2.set_title("細長いほど chi が下がり耐力が落ちる", color="white", fontsize=9.5)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=135); print("  closeup ->", closeup)

# ---- cover (small P-M panel reused) ----
figc = plt.figure(figsize=(5.6, 3.3)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.16, 0.80, 0.78]); style_ax(axc)
xs, ys = envelope(5.0, 1.0, 30)
axc.fill_between(xs, ys, color=CYAN, alpha=0.12)
axc.plot(xs, ys, color=CYAN, lw=2.6)
axc.plot(120, 800, "o", color=GREEN, ms=14)
axc.plot(120, 1500, "X", color=RED, ms=14)
axc.set_xlim(0, max(xs)*1.05); axc.set_ylim(0, 2600)
axc.set_xlabel("My (kN.m)", color="white", fontsize=9)
axc.set_ylabel("N (kN)", color="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "梁柱のP-M相関", "座屈と曲げの照査",
                  "N/Nb,Rd + kyy My/Mb,Rd <= 1  (EN1993-1-1)", cc)
os.remove(cc)

# ---- slider-anim.gif: sweep N (axial force), design point climbs across envelope ----
frames = []
xs0, ys0 = envelope(5.0, 1.0, 30)
N_seq = list(np.linspace(200, 2200, 26)) + list(np.linspace(2120, 280, 12))
for N in N_seq:
    r = calc(5.0, 1.0, N, 120, 30)
    eta = r["eta"]; passed = eta <= 1.0
    col = GREEN if passed else RED
    f2 = plt.figure(figsize=(4.6, 4.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.14, 0.80, 0.76]); style_ax(a)
    a.fill_between(xs0, ys0, color=CYAN, alpha=0.10)
    a.plot(xs0, ys0, color=CYAN, lw=2.2)
    a.plot(120, N, "o", color=col, ms=14)
    a.set_xlim(0, max(xs0)*1.05); a.set_ylim(0, 2600)
    a.set_xlabel("My,Ed (kN.m)", color="white", fontsize=9)
    a.set_ylabel("N (kN)", color="white", fontsize=9)
    a.set_title("N=%4.0f kN  eta=%.2f  %s" % (N, eta, "PASS" if passed else "FAIL"),
                color=col, fontsize=11)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)

# console verification (ASCII only)
d = calc(5.0, 1.0, 800, 120, 30)
print("VERIFY default: Ncr=%.0f lam=%.3f chi=%.3f Nb_Rd=%.0f Mb_Rd=%.1f eta=%.3f"
      % (d["Ncr"], d["lam"], d["chi"], d["Nb_Rd"], d["Mb_Rd"], d["eta"]))
print("done.")
