# -*- coding: utf-8 -*-
"""Verify reaction-diffusion (Gray-Scott) + figures. One simulation provides
both the GIF (pattern emerging) and the final closeup. 9-point Laplacian,
periodic boundaries. Du/Dv/F/k match the tool's ranges."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "reaction-diffusion"
NAVY = "#0b1020"
rng = np.random.RandomState(3)


def lap(A):
    # 9-point normalized Laplacian (Karl Sims kernel; stable at dt=1)
    return (np.roll(A, 1, 0)+np.roll(A, -1, 0)+np.roll(A, 1, 1)+np.roll(A, -1, 1))*0.2 \
        + (np.roll(np.roll(A, 1, 0), 1, 1)+np.roll(np.roll(A, 1, 0), -1, 1)
           + np.roll(np.roll(A, -1, 0), 1, 1)+np.roll(np.roll(A, -1, 0), -1, 1))*0.05 \
        - A


def simulate(N, Du, Dv, F, k, steps, snaps):
    u = np.ones((N, N)); v = np.zeros((N, N))
    # dense scattered seeds -> coral pattern grows to fill the frame
    for _ in range(120):
        cx, cy = rng.randint(5, N-5, 2)
        u[cx-3:cx+3, cy-3:cy+3] = 0.50
        v[cx-3:cx+3, cy-3:cy+3] = 0.25
    v += 0.01*rng.rand(N, N)
    frames = []
    snapset = set(int(s) for s in np.linspace(steps//12, steps-1, snaps))
    for t in range(steps):
        uvv = u*v*v
        u += (Du*lap(u) - uvv + F*(1-u))
        v += (Dv*lap(v) + uvv - (F+k)*v)
        if t in snapset:
            frames.append(v.copy())
    return u, v, frames


print("=== reaction-diffusion (Gray-Scott) verification ===")
Du, Dv, F, k = 0.30, 0.075, 0.0545, 0.062   # 'coral / worms' (wider patterns)
print(f"  Du={Du}, Dv={Dv} -> V は U の {Du/Dv:.0f} 倍ゆっくり拡散（チューリング不安定の条件）")
print(f"  F={F} (feed), k={k} (kill); trivial state (u,v)=(1,0)")
N = 200
u, v, frames = simulate(N, Du, Dv, F, k, steps=9000, snaps=36)
print(f"  grid {N}x{N}, dt=1, steps=9000, snapshots={len(frames)}")
print(f"  final v range [{v.min():.3f}, {v.max():.3f}], pattern coverage(v>0.2)={np.mean(v>0.2)*100:.1f}%")

cmap = "magma"
# closeup = final pattern
fig, ax = plt.subplots(figsize=(6.2, 6.0)); fig.patch.set_facecolor(NAVY)
ax.imshow(v, cmap=cmap, vmin=0, vmax=0.5, interpolation="bilinear"); ax.axis("off")
ax.set_title("Gray-Scott 反応拡散：チューリングパターン（珊瑚状）", color="white", fontsize=11)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup); print("  closeup ->", closeup)

figlib.make_cover(SLUG, "反応拡散と", "チューリングパターン",
                  "Gray-Scott モデルで自己組織化を解く", closeup)

# GIF from the snapshots (pattern emerging)
gframes = []
for vf in frames:
    f2, a2 = plt.subplots(figsize=(4.4, 4.4)); f2.patch.set_facecolor(NAVY)
    a2.imshow(vf, cmap=cmap, vmin=0, vmax=0.5, interpolation="bilinear"); a2.axis("off")
    gframes.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(gframes, SLUG, duration=110)
print("done.")
