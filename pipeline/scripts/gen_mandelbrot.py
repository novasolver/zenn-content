# -*- coding: utf-8 -*-
"""Verify mandelbrot numbers + figures. Reproduces tool's escape-time
iteration with smooth coloring nu = n+1 - log(log|z|)/log2, bailout |z|>2,
z0=0. Default center (-0.5,0), maxIter=200. scale = 3.5/(zoom*min(W,H))."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "mandelbrot"


def mandel(cx, cy, span, W, H, maxN):
    """Return smooth escape value array; <0 means in-set."""
    re = cx + (np.arange(W) - W/2) * span / W
    im = cy + (np.arange(H) - H/2) * span / H
    C = re[None, :] + 1j * im[:, None]
    Z = np.zeros_like(C)
    out = np.full(C.shape, -1.0)
    alive = np.ones(C.shape, bool)
    for n in range(maxN):
        Z[alive] = Z[alive]*Z[alive] + C[alive]
        mag2 = (Z.real*Z.real + Z.imag*Z.imag)
        esc = alive & (mag2 > 4.0)
        if esc.any():
            magesc = np.sqrt(mag2[esc])
            out[esc] = n + 1 - np.log(np.log(magesc))/np.log(2)
            alive[esc] = False
        if not alive.any():
            break
    return out


def scalar_iter(re, im, maxN):
    zr = zi = 0.0
    for n in range(maxN):
        zr, zi = zr*zr - zi*zi + re, 2*zr*zi + im
        if zr*zr + zi*zi > 4:
            return n + 1 - np.log(np.log(np.sqrt(zr*zr+zi*zi)))/np.log(2)
    return -1


print("=== mandelbrot verification ===")
# Known points
tests = {
    "(-0.5, 0) cardioid interior": (-0.5, 0.0),
    "(0.3, 0) elephant valley edge": (0.3, 0.0),
    "(-1.0, 0) period-2 bulb": (-1.0, 0.0),
    "(0.0, 1.0) escapes": (0.0, 1.0),
    "(0.30, 0) -> in/out?": (0.30, 0.0),
}
for name, (re, im) in tests.items():
    v = scalar_iter(re, im, 1000)
    status = "in set" if v < 0 else f"escapes nu={v:.2f}"
    print(f"  c={name}: {status}")

# default-view in-set fraction
out = mandel(-0.5, 0.0, 3.0, 600, 600, 200)
frac_in = np.mean(out < 0)
print(f"default view in-set fraction (maxIter=200): {frac_in:.3f}")
# boundary cell count scaling (fractal): vary maxIter
for mi in (50, 200, 1000):
    o = mandel(-0.5, 0.0, 3.0, 400, 400, mi)
    print(f"  maxIter={mi}: in-set frac={np.mean(o<0):.4f}")

# ---- FIGURES ----
def render(cx, cy, span, W, H, maxN, cmap="twilight_shifted"):
    o = mandel(cx, cy, span, W, H, maxN)
    img = np.zeros((H, W, 3))
    inset = o < 0
    t = np.where(inset, 0, (o % maxN) / maxN)
    cm = plt.get_cmap(cmap)
    rgb = cm(t)[..., :3]
    rgb[inset] = [0, 0, 0]
    return rgb

# charts-closeup: seahorse valley
closeup_rgb = render(-0.743643887, 0.131825904, 0.012, 760, 600, 1500, "twilight_shifted")
fig, ax = plt.subplots(figsize=(6.8, 5.4))
ax.imshow(closeup_rgb, origin="lower")
ax.set_title("マンデルブロ集合：シーホースの谷（ズーム ~290倍）", color="white", fontsize=11)
ax.set_xticks([]); ax.set_yticks([])
fig.patch.set_facecolor("#0b1020")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup)
print("  closeup ->", closeup)

figlib.make_cover(SLUG, "マンデルブロ集合", "z²+c が描く無限",
                  "エスケープ時間アルゴリズムとスムーズ着色", closeup)

# gif: zoom into seahorse valley
frames = []
cx0, cy0 = -0.743643887, 0.131825904
spans = np.geomspace(3.0, 0.0009, 26)
for sp in spans:
    mi = int(np.clip(120 + 90*np.log10(3.0/sp), 120, 1200))
    rgb = render(cx0, cy0, sp, 420, 360, mi, "twilight_shifted")
    f2, a2 = plt.subplots(figsize=(4.6, 3.9))
    a2.imshow(rgb, origin="lower")
    a2.set_xticks([]); a2.set_yticks([])
    a2.set_title(f"zoom ×{3.0/sp:,.0f}", color="white", fontsize=10)
    f2.patch.set_facecolor("#0b1020")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
