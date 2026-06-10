# -*- coding: utf-8 -*-
"""BJT amplifier (CE/CB/CC) AC analysis visuals.
Faithful to bjt-amplifier.html calcAC():
  gm = IC/VT (VT=26mV), rpi = beta/gm, ro = VA/IC
  CE: Av = -gm*(RC||RL||ro) [bypass ON] or /(1+gm*RE) [bypass OFF]
  CB: Av = +gm*(RC||RL||ro)
  CC: Av = gm*(RE||RL)/(1+gm*(RE||RL)) ~ +1
  Bode: first-order roll-off between fL and fH (matches tool's drawBode()).
ASCII labels only, no emoji.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bjt-amplifier"
NAVY = "#0b1020"
CYAN = "#7dd3fc"      # CE
ORANGE = "#f59e0b"    # CB
GREEN = "#9be7a3"     # CC
GRID = "#22304d"
VT = 0.026


def calc(ic_mA, beta, rc_k, rl_k, re_k, rb_k, va, config, bypass):
    ic = ic_mA * 1e-3; rc = rc_k * 1e3; rl = rl_k * 1e3
    re = re_k * 1e3; rb = rb_k * 1e3
    gm = ic / VT
    rpi = beta / gm
    ro = va / ic
    reEff = 0 if bypass else re
    if config == "CE":
        rcP = 1 / (1 / rc + 1 / rl + 1 / ro)
        av = -gm * rcP / (1 + gm * reEff) if reEff > 0 else -gm * rcP
        zin = 1 / (1 / rb + 1 / (rpi + (1 + beta) * reEff))
    elif config == "CB":
        rcP = 1 / (1 / rc + 1 / rl + 1 / ro)
        av = gm * rcP
        zin = 1 / (gm + 1 / rpi)
    else:  # CC
        reP = 1 / (1 / re + 1 / rl)
        av = gm * reP / (1 + gm * reP)
        zin = 1 / (1 / rb + 1 / (rpi + (1 + beta) * reP))
    C_couple = 10e-6
    fL = 1 / (2 * np.pi * C_couple * zin)
    Cpi = gm / (2 * np.pi * 5e8)
    fH = 1 / (2 * np.pi * Cpi * (1 / (1 / rc + 1 / rl)))
    return dict(gm=gm, av=av, av_db=20 * np.log10(abs(av)), zin=zin, fL=fL, fH=fH)


def bode_curve(av, fL, fH, fmin=10, fmax=1e8, n=400):
    f = np.logspace(np.log10(fmin), np.log10(fmax), n)
    magLow = np.where(f > fL, 1.0, f / fL)
    magHigh = np.where(f < fH, 1.0, fH / f)
    mag = abs(av) * magLow * magHigh
    db = np.where(mag > 1e-6, 20 * np.log10(mag), -60)
    return f, db


def style_ax(ax, logx=True):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8, which="both")
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")
    ax.grid(True, which="both", color=GRID, lw=0.5)
    if logx:
        ax.set_xscale("log")


# Default params, bypass ON (so CE shows full gain like the tool's compute() default? tool default OFF,
# but the Bode overlays all 3 with current bypass state. Use bypass ON to show meaningful CE gain.)
P = dict(ic_mA=1, beta=100, rc_k=3.3, rl_k=10, re_k=1, rb_k=20, va=100)

# ---- charts-closeup: Bode overlay (left) + IC->gain (right) ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.07, 0.16, 0.42, 0.70]); style_ax(ax1)
for cfg, col in [("CE", CYAN), ("CB", ORANGE), ("CC", GREEN)]:
    r = calc(config=cfg, bypass=True, **P)
    f, db = bode_curve(r["av"], r["fL"], r["fH"])
    ax1.plot(f, db, color=col, lw=2.2, label=f"{cfg}  ({r['av_db']:.0f} dB)")
ax1.set_xlim(10, 1e8); ax1.set_ylim(-20, 50)
ax1.set_xlabel("frequency [Hz]", color="white", fontsize=9)
ax1.set_ylabel("voltage gain |Av| [dB]", color="white", fontsize=9)
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower center")
ax1.set_title("Bode plot: CE / CB / CC", color="white", fontsize=10)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.70]); style_ax(ax2, logx=False)
ics = np.array([0.5, 1, 2, 5, 10])
dbs = [calc(ic_mA=ic, beta=100, rc_k=3.3, rl_k=10, re_k=1, rb_k=20, va=100,
            config="CE", bypass=True)["av_db"] for ic in ics]
ax2.plot(ics, dbs, "o-", color=CYAN, lw=2.2, ms=6)
for ic, db in zip(ics, dbs):
    ax2.annotate(f"{db:.0f} dB", (ic, db), color="white", fontsize=7.5,
                 xytext=(5, -10), textcoords="offset points")
ax2.set_xlabel("collector current IC [mA]", color="white", fontsize=9)
ax2.set_ylabel("CE gain Av [dB]", color="white", fontsize=9)
ax2.set_title("gm = IC/VT  ->  higher IC, higher gain", color="white", fontsize=10)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover chart preview ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13, 0.13, 0.83, 0.80]); style_ax(axc)
for cfg, col in [("CE", CYAN), ("CB", ORANGE), ("CC", GREEN)]:
    r = calc(config=cfg, bypass=True, **P)
    f, db = bode_curve(r["av"], r["fL"], r["fH"])
    axc.plot(f, db, color=col, lw=2.6)
axc.set_xlim(10, 1e8); axc.set_ylim(-20, 50)
axc.set_xticks([]); axc.set_yticks([])
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "BJTアンプの", "交流小信号解析",
                  "CE/CB/CC の電圧利得とボード線図を可視化", cc)
os.remove(cc)

# ---- gif: sweep IC -> CE Bode rises (gain grows with gm=IC/VT) ----
frames = []
ic_list = list(np.linspace(0.3, 10, 22)) + list(np.linspace(9, 0.5, 12))
for ic in ic_list:
    r = calc(ic_mA=ic, beta=100, rc_k=3.3, rl_k=10, re_k=1, rb_k=20, va=100,
             config="CE", bypass=True)
    f, db = bode_curve(r["av"], r["fL"], r["fH"])
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.14, 0.17, 0.82, 0.70]); style_ax(a)
    a.plot(f, db, color=CYAN, lw=2.4)
    a.set_xlim(10, 1e8); a.set_ylim(-20, 60)
    a.set_xlabel("frequency [Hz]", color="white", fontsize=8)
    a.set_ylabel("|Av| [dB]", color="white", fontsize=8)
    a.set_title(f"CE  IC={ic:.1f}mA  gm={r['gm']*1000:.0f}mA/V  Av={r['av_db']:.0f}dB",
                color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
