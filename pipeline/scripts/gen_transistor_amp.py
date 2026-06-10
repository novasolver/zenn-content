# -*- coding: utf-8 -*-
"""Transistor (BJT common-emitter) amplifier visuals.
Faithful to tool JS: VB=VCC*R2/(R1+R2); VE=VB-0.7; IC=VE/RE; VCE=VCC-IC*RC-VE;
gm=IC/VT (VT=0.026); Av=gm*(RC||RL); load line IC=(VCC-VCE)/(RC+RE).
Default: VCC=12 beta=150 R1=47k R2=10k RC=4.7k RE=1k RL=10k -> IC=1.41mA VCE=3.99V |Av|=172.8.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "transistor-amp"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"; RED = "#f47171"
VT = 0.026


def qpoint(VCC, beta, R1, R2, RC, RE, RL):
    R1 *= 1e3; R2 *= 1e3; RC *= 1e3; RE *= 1e3; RL *= 1e3
    VB = VCC * R2 / (R1 + R2)
    VE = max(0, VB - 0.7)
    IC = VE / RE if RE > 0 else 0
    VCE = VCC - IC * RC - VE
    gm = IC / VT if IC > 0 else 0
    Av = gm * (RC * RL) / (RC + RL)
    return IC, VCE, Av


def ic_curves(VCC, beta):
    """Tool's simplified output family: IC = beta*IB*(1-exp(-VCE/0.1))."""
    IB_vals = [5, 10, 20, 40, 80, 160]
    out = []
    for IB in IB_vals:
        vce = np.linspace(0, VCC, 200)
        ic = beta * IB * 1e-6 * (1 - np.exp(-vce / 0.1)) * 1e3  # mA
        out.append((IB, vce, ic))
    return out


# ---- charts-closeup: IC-VCE family + load line + Q-point (left), Av-vs-RE (right) ----
VCC, beta, R1, R2, RC, RE, RL = 12, 150, 47, 10, 4.7, 1.0, 10
IC, VCE, Av = qpoint(VCC, beta, R1, R2, RC, RE, RL)
print(f"DEFAULT  IC={IC*1e3:.3f}mA  VCE={VCE:.2f}V  |Av|={Av:.1f}  Av_dB={20*np.log10(Av):.2f}")

fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.15, 0.40, 0.72]); ax1.set_facecolor(NAVY)
greys = ["#5a6a8a", "#6f80a3", CYAN, "#5aa9e6", "#3b7fc4", "#2a5d9e"]
for (IB, vce, ic), col in zip(ic_curves(VCC, beta), greys):
    ax1.plot(vce, ic, color=col, lw=1.3)
# DC load line: IC = (VCC - VCE)/(RC+RE)
ax1.plot([0, VCC], [VCC / (RC + RE) * 1e3 * 1e-3 * 1e3, 0], color=RED, lw=2, ls="--", label="直流負荷線")
ax1.plot(VCE, IC * 1e3, "o", color=GREEN, ms=11, mec="#27ae60", mew=2, label="Qポイント", zorder=5)
ax1.annotate(f"Q ({VCE:.1f}V, {IC*1e3:.2f}mA)", (VCE, IC * 1e3),
             textcoords="offset points", xytext=(8, 10), color=GREEN, fontsize=8)
ax1.set_xlabel("VCE (V)", color="white", fontsize=9); ax1.set_ylabel("IC (mA)", color="white", fontsize=9)
ax1.set_xlim(0, VCC * 1.05); ax1.set_ylim(0, VCC / (RC + RE) * 1.05)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
ax1.set_title("IC-VCE特性・負荷線・Qポイント", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.15, 0.39, 0.72]); ax2.set_facecolor(NAVY)
RE_arr = np.linspace(0.3, 4.0, 80)
Avs = [qpoint(VCC, beta, R1, R2, RC, re, RL)[2] for re in RE_arr]
ICs = [qpoint(VCC, beta, R1, R2, RC, re, RL)[0] * 1e3 for re in RE_arr]
ax2.plot(RE_arr, Avs, color=ORANGE, lw=2.2, label="|Av| 電圧利得")
ax2.axvline(1.0, color=GREEN, lw=1, ls="--")
ax2.plot(1.0, Av, "o", color=GREEN, ms=8, zorder=5)
ax2.text(1.05, Av * 1.05, f"既定 RE=1kΩ\n|Av|={Av:.0f}", color=GREEN, fontsize=8)
ax2.set_xlabel("RE (kΩ)", color="white", fontsize=9); ax2.set_ylabel("|Av|", color=ORANGE, fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("RE を上げると IC↓ → 利得↓", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
for (IB, vce, ic), col in zip(ic_curves(VCC, beta), greys):
    axc.plot(vce, ic, color=col, lw=1.6)
axc.plot([0, VCC], [VCC / (RC + RE), 0], color=RED, lw=2.2, ls="--")
axc.plot(VCE, IC * 1e3, "o", color=GREEN, ms=12, mec="#27ae60", mew=2)
axc.set_xlim(0, VCC); axc.set_ylim(0, VCC / (RC + RE)); axc.set_xticks([]); axc.set_yticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "トランジスタ増幅回路と", "Qポイント設計",
                  "負荷線とIC-VCE特性の交点でVCE=4.0V・|Av|=173 を読む", cc)
os.remove(cc)

# ---- gif: sweep R2 -> Q-point slides along the load line ----
frames = []
R2_seq = list(np.linspace(4, 22, 22)) + list(np.linspace(21, 5, 12))
for r2 in R2_seq:
    icq, vceq, avq = qpoint(VCC, beta, R1, r2, RC, RE, RL)
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.16, 0.83, 0.70]); a.set_facecolor(NAVY)
    for (IB, vce, ic), col in zip(ic_curves(VCC, beta), greys):
        a.plot(vce, ic, color=col, lw=1.2)
    a.plot([0, VCC], [VCC / (RC + RE), 0], color=RED, lw=2, ls="--")
    if vceq > 0:
        a.plot(vceq, icq * 1e3, "o", color=GREEN, ms=11, mec="#27ae60", mew=2, zorder=5)
    a.set_xlim(0, VCC); a.set_ylim(0, VCC / (RC + RE))
    a.set_xlabel("VCE (V)", color="white", fontsize=8); a.set_ylabel("IC (mA)", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    st = "飽和" if vceq < 0.2 else ("カットオフ" if vceq > VCC - 0.2 else "能動域")
    a.set_title(f"R2={r2:.0f}kΩ  IC={icq*1e3:.2f}mA  VCE={vceq:.1f}V  {st}",
                color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
