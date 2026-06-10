# -*- coding: utf-8 -*-
"""image-convolution-kernel visuals (matplotlib + PIL only).
Faithfully replicates the tool's 3x3 convolution (border replication, [0,1] clamp,
seeded mulberry32 Gaussian noise). Produces cover / charts-closeup / slider-anim.gif.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "image-convolution-kernel"
NAVY = "#0b1020"; BLUE = "#3498db"; ORANGE = "#f59e0b"; GREEN = "#00b894"; RED = "#fb7185"

KERNELS = {
    "identity": [0, 0, 0, 0, 1, 0, 0, 0, 0],
    "boxblur":  [1/9]*9,
    "gaussian": [1/16, 2/16, 1/16, 2/16, 4/16, 2/16, 1/16, 2/16, 1/16],
    "sharpen":  [0, -1, 0, -1, 5, -1, 0, -1, 0],
    "edge":     [-1, -1, -1, -1, 8, -1, -1, -1, -1],
    "sobelx":   [-1, 0, 1, -2, 0, 2, -1, 0, 1],
}

def make_rng(seed):
    def imul(x, y): return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF
    def i32(x):
        x &= 0xFFFFFFFF
        return x - 0x100000000 if x >= 0x80000000 else x
    st = [seed & 0xFFFFFFFF]
    def rng():
        s = i32(st[0]); s = i32(s + 0x6D2B79F5); st[0] = s & 0xFFFFFFFF
        t = i32(imul(s ^ ((s & 0xFFFFFFFF) >> 15), 1 | s))
        t = i32(t + i32(imul(t ^ ((t & 0xFFFFFFFF) >> 7), 61 | t))) ^ t
        return ((t & 0xFFFFFFFF) ^ ((t & 0xFFFFFFFF) >> 14)) / 4294967296
    return rng

def gauss(rng):
    u = rng(); v = rng()
    if u < 1e-12: u = 1e-12
    return math.sqrt(-2*math.log(u)) * math.cos(2*math.pi*v)

def build(N, pattern="circle", noiseLv=0.0):
    img = np.zeros((N, N))
    for r in range(N):
        for c in range(N):
            x = c/(N-1); y = r/(N-1)
            if pattern == "circle":
                dx, dy = x-0.5, y-0.5
                img[r, c] = 0.9 if math.sqrt(dx*dx+dy*dy) < 0.32 else 0.12
            elif pattern == "checker":
                blk = N//4
                img[r, c] = 0.85 if ((r//blk)+(c//blk)) % 2 == 0 else 0.15
    if noiseLv > 0:
        rng = make_rng(987654321)
        for r in range(N):
            for c in range(N):
                img[r, c] = max(0.0, min(1.0, img[r, c] + noiseLv*gauss(rng)))
    return img

def keff(name, s):
    bk = KERNELS[name]; idk = KERNELS["identity"]
    return [idk[i] + s*(bk[i]-idk[i]) for i in range(9)]

def convolve(img, k):
    N = img.shape[0]
    out = np.zeros((N, N))
    for r in range(N):
        for c in range(N):
            acc = 0.0
            for m in (-1, 0, 1):
                for n in (-1, 0, 1):
                    rr = max(0, min(N-1, r+m)); cc = max(0, min(N-1, c+n))
                    acc += k[(m+1)*3+(n+1)] * img[rr, cc]
            out[r, c] = max(0.0, min(1.0, acc))
    return out

def gray(ax, im, title):
    ax.imshow(im, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    ax.set_title(title, color="white", fontsize=10, pad=6)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

N = 32
inp = build(N, "circle", 0.0)

# ---------- charts-closeup: input + 3 kernels ----------
fig = plt.figure(figsize=(9.6, 3.0)); fig.patch.set_facecolor(NAVY)
specs = [("入力画像（円）", inp),
         ("シャープ化 (sum=1)", convolve(inp, keff("sharpen", 1))),
         ("ガウシアンぼかし (sum=1)", convolve(inp, keff("gaussian", 1))),
         ("エッジ抽出 (sum=0)", convolve(inp, keff("edge", 1)))]
for i, (t, im) in enumerate(specs):
    ax = fig.add_axes([0.02 + i*0.245, 0.06, 0.225, 0.80]); gray(ax, im, t)
cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, cu, dpi=130); print(" closeup")

# ---------- cover chart (input -> sharpen) ----------
figc = plt.figure(figsize=(5.2, 2.7)); figc.patch.set_facecolor(NAVY)
a1 = figc.add_axes([0.03, 0.08, 0.44, 0.82]); gray(a1, inp, "入力")
a2 = figc.add_axes([0.53, 0.08, 0.44, 0.82]); gray(a2, convolve(inp, keff("sharpen", 1)), "出力(シャープ化)")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png")
figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "画像畳み込みカーネル", "(CNNの心臓部)",
                  "O(i,j)=sum K(m,n)*I(i+m,j+n)、3x3で全画像を走査", cc)
os.remove(cc)

# ---------- slider-anim.gif: strength sweep on sharpen ----------
frames = []
strengths = [round(x*0.1, 2) for x in range(0, 21)]  # 0.0 .. 2.0
for s in strengths:
    out = convolve(inp, keff("sharpen", s))
    fr = plt.figure(figsize=(4.2, 2.6)); fr.patch.set_facecolor(NAVY)
    a = fr.add_axes([0.05, 0.06, 0.9, 0.78])
    gray(a, out, f"シャープ化 強度 s = {s:.1f}")
    frames.append(figlib.fig_to_pil(fr, dpi=92))
frames = frames + frames[::-1]
frames += [frames[-1]]*2
figlib.save_gif(frames, SLUG, duration=140)
print("done")
