# -*- coding: utf-8 -*-
"""organic-rankine-cycle visuals: T-s dome+cycle + eta-vs-Thot curve + slider gif.
Replicates the tool's own approximate ORC model (fluidProps + compute) so the
figures match the live simulator. ASCII-only prints; <v> not angle brackets."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "organic-rankine-cycle"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"
GREEN = "#2ecc71"; RED = "#e74c3c"; YEL = "#ffd24b"; GRY = "#8fb8e0"

FLUID = {  # matches tool fluidProps
    "r245fa":   dict(name="R245fa",   cp=1.32, hfg=200, Tcrit=154, Tmin=-25,  Tmax=140),
    "r134a":    dict(name="R134a",    cp=1.42, hfg=175, Tcrit=101, Tmin=-26,  Tmax=90),
    "npentane": dict(name="n-Pentane", cp=2.39, hfg=357, Tcrit=196, Tmin=-130, Tmax=180),
    "toluene":  dict(name="Toluene",  cp=2.05, hfg=412, Tcrit=319, Tmin=-95,  Tmax=300),
}

def compute(fl, Thot, Tcool, mdot=5.0, etaP=75, etaT=80, regen=True):
    f = FLUID[fl]
    Tevap = min(f["Tmax"], Thot - 10)
    Tcond = max(f["Tmin"] + 10, Tcool + 10)
    carnot = (Tevap + 273.15 - (Tcond + 273.15)) / (Tevap + 273.15)
    if not math.isfinite(carnot) or carnot < 0: carnot = 0
    eta = carnot * 0.55 * (etaT / 100)
    if regen: eta *= 1.12
    eta = min(0.5, max(0.01, eta))
    dT = max(0, Tevap - Tcond)
    Qin = mdot * (f["cp"] * dT + f["hfg"])
    Wnet = Qin * eta
    return dict(Tevap=Tevap, Tcond=Tcond, carnot=carnot, eta=eta, Qin=Qin, Wnet=Wnet)

def style(ax):
    ax.set_facecolor(NAVY); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

def ts_dome(ax, fl, Thot, Tcool):
    """Idealised dome around Tcrit + 1->2->3->4 cycle, mirroring the tool's chart."""
    f = FLUID[fl]; d = compute(fl, Thot, Tcool)
    Tc = f["Tcrit"]; Tlow = max(-50, d["Tcond"] - 30)
    Thigh = min(Tc - 1, max(d["Tevap"] + 20, Tc - 5))
    T = np.linspace(Tlow, Thigh, 60); u = (T - Tlow) / (Thigh - Tlow + 1e-6)
    half = 1.0 * (1 - 0.9 * u * u)
    liqx = 0.5 - half * 0.5; vapx = 0.5 + half * 0.5
    ax.plot(liqx, T, color=BLUE, lw=1.6)
    ax.plot(vapx, T, color=ORANGE, lw=1.6)
    def sx(Tt, side):
        w = 1 - 0.9 * ((Tt - Tlow) / (Thigh - Tlow + 1e-6)) ** 2
        return 0.5 + side * 0.5 * w
    sLiqE = sx(d["Tevap"], -1); sVapE = sx(d["Tevap"], +1)
    sLiqC = sx(d["Tcond"], -1); sVapC = sx(d["Tcond"], +1)
    sTurb = sVapC + 0.18
    cx = [sLiqC, sLiqE, sVapE, sTurb, sVapC, sLiqC]
    cy = [d["Tcond"], d["Tevap"], d["Tevap"], d["Tcond"] + 8, d["Tcond"], d["Tcond"]]
    ax.plot(cx, cy, color=YEL, lw=2.3)
    for x, y, n in [(sLiqC, d["Tcond"], "1"), (sVapE, d["Tevap"], "2"),
                    (sTurb, d["Tcond"] + 8, "3"), (sVapC, d["Tcond"], "4")]:
        ax.plot(x, y, "o", color="white", ms=5)
        ax.annotate(n, (x, y), (x + 0.04, y + 6), color="white", fontsize=9)
    ax.set_xlabel("比エントロピー s (相対値)", color="white", fontsize=9)
    ax.set_ylabel("温度 T [C]", color="white", fontsize=9)
    ax.set_title("T-s線図と飽和ドーム (%s)" % f["name"], color="white", fontsize=10)

def eff_curve(ax, fl, Thot, Tcool):
    f = FLUID[fl]
    Th = np.linspace(70, 400, 60)
    eta = [compute(fl, t, Tcool)["eta"] * 100 for t in Th]
    car = [compute(fl, t, Tcool)["carnot"] * 100 for t in Th]
    ax.plot(Th, car, "--", color=RED, lw=1.8, label="カルノー効率")
    ax.plot(Th, eta, color=BLUE, lw=2.4, label="ORC効率")
    d = compute(fl, Thot, Tcool)
    ax.plot(Thot, d["eta"] * 100, "o", color=ORANGE, ms=8, label="現在の設定")
    ax.annotate("%.1f%%" % (d["eta"] * 100), (Thot, d["eta"] * 100),
                (Thot + 8, d["eta"] * 100 - 4), color="white", fontsize=8)
    ax.set_xlabel("熱源温度 T_hot [C]", color="white", fontsize=9)
    ax.set_ylabel("効率 [%]", color="white", fontsize=9)
    ax.set_title("熱源温度に対する効率", color="white", fontsize=10)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7, loc="upper left")

# ---- charts-closeup: T-s dome + efficiency curve side by side ----
fig = plt.figure(figsize=(9.4, 4.2)); fig.patch.set_facecolor(NAVY)
a1 = fig.add_axes([0.08, 0.15, 0.40, 0.74]); style(a1); ts_dome(a1, "r245fa", 150, 25)
a2 = fig.add_axes([0.58, 0.15, 0.39, 0.74]); style(a2); eff_curve(a2, "r245fa", 150, 25)
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, cu, dpi=130); print("closeup done")

# ---- cover: small T-s panel pasted into branded cover ----
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.76]); style(axc); ts_dome(axc, "r245fa", 150, 25)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "有機ランキンサイクル", "(ORC)",
                  "低温廃熱を電気に変える熱力学サイクル", cc); os.remove(cc)
print("cover done")

# ---- gif: sweep heat-source temperature; show Wnet/Qin bars + eta point ----
frames = []
fl = "r245fa"
sweep = list(np.linspace(90, 250, 26)) + list(np.linspace(250, 90, 10))
for Th in sweep:
    d = compute(fl, Th, 25)
    f = plt.figure(figsize=(6.0, 3.2)); f.patch.set_facecolor(NAVY)
    # left: energy bars
    al = f.add_axes([0.09, 0.17, 0.36, 0.70]); style(al)
    al.bar(["熱入力\nQin", "正味出力\nWnet"], [d["Qin"], d["Wnet"]],
           color=[ORANGE, GREEN])
    al.set_ylim(0, 2600); al.set_ylabel("kW", color="white", fontsize=9)
    al.set_title("eta = %.1f%%" % (d["eta"] * 100), color="white", fontsize=10)
    # right: efficiency curve with moving point
    ar = f.add_axes([0.57, 0.17, 0.40, 0.70]); style(ar)
    Thx = np.linspace(70, 300, 50)
    ar.plot(Thx, [compute(fl, t, 25)["carnot"] * 100 for t in Thx], "--", color=RED, lw=1.4)
    ar.plot(Thx, [compute(fl, t, 25)["eta"] * 100 for t in Thx], color=BLUE, lw=2.0)
    ar.plot(Th, d["eta"] * 100, "o", color=ORANGE, ms=9)
    ar.set_xlabel("T_hot [C]", color="white", fontsize=9)
    ar.set_ylabel("効率 [%]", color="white", fontsize=9)
    ar.set_ylim(0, 45)
    ar.set_title("T_hot = %.0f C" % Th, color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f, dpi=85))
figlib.save_gif(frames, SLUG, duration=110)
print("done")
