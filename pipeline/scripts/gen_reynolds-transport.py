"""Matplotlib visuals for the Reynolds transport theorem article.

Faithful to tools/reynolds-transport.html physics:
  continuity:  V2 = V1*(D1/D2)^2
  Bernoulli:   P2 = P1 + 0.5*rho*(V1^2 - V2^2)
  nozzle force: Fx = mdot*(V2-V1) + P2*A2 - P1*A1
  bend force:   Fx = mdot*V1 + P1*A1 ; Fy = mdot*V2 + P2*A2 ; |F|=hypot

Outputs: images/reynolds-transport/{cover.png, charts-closeup.png, slider-anim.gif}
ASCII only in all drawn/printed text (use <v> not angle brackets).
"""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrow
import figlib

SLUG = "reynolds-transport"
ACCENT = "#007BFF"
ACCENT2 = "#00B4D8"
GREEN = "#28a745"
RED = "#dc3545"
NAVY = "#001F3F"


def solve(typ, D1mm, D2mm, V1, P1kPa, rho):
    D1 = D1mm / 1000.0
    D2 = D2mm / 1000.0
    P1 = P1kPa * 1000.0
    A1 = math.pi * D1 * D1 / 4
    A2 = math.pi * D2 * D2 / 4
    mdot = rho * A1 * V1
    V2 = mdot / (rho * A2)
    P2 = P1 + 0.5 * rho * (V1 * V1 - V2 * V2)
    if typ == "bend":
        Fx = mdot * V1 + P1 * A1
        Fy = mdot * V2 + P2 * A2
    else:
        Fx = mdot * (V2 - V1) + P2 * A2 - P1 * A1
        Fy = 0.0
    return dict(D1=D1, D2=D2, A1=A1, A2=A2, mdot=mdot, V1=V1, V2=V2,
                P1=P1, P2=P2, Fx=Fx, Fy=Fy, Ftot=math.hypot(Fx, Fy))


# ---------- charts-closeup: P/V bars + force bars (mirrors the two tool tabs) ----------
def charts_closeup():
    st = solve("nozzle", 100, 50, 5.0, 200, 1000)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.0))
    fig.patch.set_facecolor("white")

    # left: pressure + velocity at inlet/outlet (chartPV equivalent)
    pos = ["inlet", "outlet"]
    Pv = [st["P1"] / 1000, st["P2"] / 1000]
    Vv = [st["V1"], st["V2"]]
    x = [0, 1]
    b1 = ax1.bar([p - 0.18 for p in x], Pv, width=0.36, color=ACCENT, label="P [kPa]")
    ax1b = ax1.twinx()
    b2 = ax1b.bar([p + 0.18 for p in x], Vv, width=0.36, color=GREEN, label="V [m/s]")
    ax1.set_xticks(x); ax1.set_xticklabels(pos)
    ax1.set_ylabel("pressure P [kPa]", color=ACCENT)
    ax1b.set_ylabel("velocity V [m/s]", color=GREEN)
    ax1.set_title("Pressure & velocity (nozzle)", fontsize=11)
    for r, v in zip(b1, Pv):
        ax1.text(r.get_x() + r.get_width() / 2, v + 4, f"{v:.1f}", ha="center", fontsize=8, color=ACCENT)
    for r, v in zip(b2, Vv):
        ax1b.text(r.get_x() + r.get_width() / 2, v + 0.4, f"{v:.1f}", ha="center", fontsize=8, color=GREEN)
    ax1.set_ylim(0, 230)

    # right: force breakdown (chartForce equivalent) for bend
    sb = solve("bend", 100, 50, 5.0, 200, 1000)
    labels = ["Fx", "Fy", "|F|", "mdot*dV", "P*A"]
    vals = [sb["Fx"], sb["Fy"], sb["Ftot"],
            sb["mdot"] * (sb["V2"] - sb["V1"]),
            sb["P2"] * sb["A2"] - sb["P1"] * sb["A1"]]
    cols = [ACCENT, GREEN, "#fd7e14", "#0056b3", "#6c757d"]
    bars = ax2.bar(labels, vals, color=cols)
    ax2.axhline(0, color="#999", lw=0.8)
    ax2.set_ylabel("force [N]")
    ax2.set_title("Force components (90deg bend)", fontsize=11)
    for r, v in zip(bars, vals):
        ax2.text(r.get_x() + r.get_width() / 2,
                 v + (60 if v >= 0 else -120), f"{v:.0f}",
                 ha="center", fontsize=8)
    ax2.tick_params(axis="x", labelsize=8)

    fig.tight_layout()
    out = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
    figlib.save_fig(fig, out, dpi=130)
    print("  charts-closeup ->", out)
    return out


# ---------- control-volume diagram for a frame ----------
def draw_cv(ax, st, typ):
    ax.clear()
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_facecolor("white")
    maxD = max(st["D1"], st["D2"], 0.05)
    sc = 1.7 / maxD
    r1 = st["D1"] * sc
    r2 = st["D2"] * sc
    cy = 3.4
    # converging/diverging horizontal duct
    x1, x2, x3, x4 = 1.0, 4.3, 5.7, 9.0
    poly = Polygon([(x1, cy - r1), (x2, cy - r1), (x3, cy - r2), (x4, cy - r2),
                    (x4, cy + r2), (x3, cy + r2), (x2, cy + r1), (x1, cy + r1)],
                   closed=True, facecolor=(0, 0.48, 1, 0.15), edgecolor=ACCENT, lw=2)
    ax.add_patch(poly)
    # CV dashed box
    ax.add_patch(plt.Rectangle((x1 - 0.05, cy - r1 - 0.2), (x4 - x1) + 0.1,
                               2 * r1 + 0.4, fill=False, ls="--", ec="#888", lw=1))
    ax.text(x1 + 0.1, cy + r1 + 0.45, "control volume (CV)", fontsize=8, color="#666")
    # flow arrows
    ax.add_patch(FancyArrow(x1 + 0.3, cy, 1.9, 0, width=0.06, head_width=0.28,
                            head_length=0.35, color=GREEN, length_includes_head=True))
    ax.add_patch(FancyArrow(x3 + 0.3, cy, 2.4, 0, width=0.06, head_width=0.28,
                            head_length=0.35, color=GREEN, length_includes_head=True))
    # labels
    ax.text(x1, cy - r1 - 0.55, f"D1={st['D1']*1000:.0f}mm", fontsize=8.5, color="#333")
    ax.text(x1, cy + r1 + 0.05, f"V1={st['V1']:.1f} m/s", fontsize=8.5, color="#333")
    ax.text(x3 + 0.1, cy - r2 - 0.55, f"D2={st['D2']*1000:.0f}mm", fontsize=8.5, color="#333")
    ax.text(x3 + 0.1, cy + r2 + 0.05, f"V2={st['V2']:.1f} m/s", fontsize=8.5, color="#333")
    ax.text(5.0, 0.55, f"P1={st['P1']/1000:.0f} kPa  ->  P2={st['P2']/1000:.1f} kPa",
            fontsize=9, color=ACCENT, ha="center")
    ax.text(5.0, 5.55, "Reynolds transport theorem  |  continuity + Bernoulli",
            fontsize=10, color=NAVY, ha="center", weight="bold")


# ---------- slider-anim: sweep D2 (outlet diameter) ----------
def slider_anim():
    frames = []
    D2_vals = list(range(100, 29, -7)) + list(range(30, 101, 7))
    for D2 in D2_vals:
        st = solve("nozzle", 100, D2, 5.0, 200, 1000)
        fig, ax = plt.subplots(figsize=(7.4, 4.4))
        fig.patch.set_facecolor("white")
        draw_cv(ax, st, "nozzle")
        ax.text(5.0, 0.05, f"D2 slider = {D2} mm   (V2={st['V2']:.1f} m/s, P2={st['P2']/1000:.0f} kPa)",
                fontsize=9.5, color="#333", ha="center", weight="bold")
        frames.append(figlib.fig_to_pil(fig, dpi=95))
    figlib.save_gif(frames, SLUG, duration=160)


def cover():
    chart = charts_closeup()
    figlib.make_cover(
        SLUG,
        "Reynolds Transport",
        "Theorem",
        "Control volume: continuity + momentum + Bernoulli",
        chart,
    )


if __name__ == "__main__":
    cover()
    charts_closeup()
    slider_anim()
    print("done")
