# -*- coding: utf-8 -*-
"""Bias-variance visuals. Faithful to the tool: true f=sin(2pi x), poly fit with
ridge 1e-6, mulberry32 seeded PRNG, 60-pt test grid. Decompose for deg 1..12."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bias-variance-tradeoff"
NAVY = "#020d1a"
BLUE, ORANGE, GREEN, NAVYLINE = "#007BFF", "#e17055", "#00b894", "#7dd3fc"

BV_SEED = 0x9E3779B9
def make_rng(seed):
    state=[seed & 0xFFFFFFFF]
    def imul(x,y):
        x&=0xFFFFFFFF; y&=0xFFFFFFFF
        rx = x if x<0x80000000 else x-0x100000000
        ry = y if y<0x80000000 else y-0x100000000
        return (rx*ry)&0xFFFFFFFF
    def rng():
        state[0]=(state[0]+0x6D2B79F5)&0xFFFFFFFF
        a=state[0]
        t=imul(a^(a>>15), 1|a)
        t=((t+imul(t^(t>>7), 61|t))&0xFFFFFFFF) ^ t
        t&=0xFFFFFFFF
        return ((t ^ (t>>14))&0xFFFFFFFF)/4294967296.0
    return rng

def true_fn(kind,x):
    if kind=='cubic': return 2*x*x*x - x + 0.2
    return math.sin(2*math.pi*x)

def fit_poly(xs,ys,deg):
    m=deg+1; lam=1e-6
    X=np.vander(np.array(xs), m, increasing=True)
    XtX=X.T@X + lam*np.eye(m)
    return np.linalg.solve(XtX, X.T@np.array(ys))

def eval_poly(w,xg):
    V=np.vander(xg, len(w), increasing=True)
    return V@w

NTEST=60
TEST_X=np.array([i/(NTEST-1) for i in range(NTEST)])

def decompose(deg,nSamples,noiseLv,nDatasets,kind='sine'):
    rng=make_rng(BV_SEED)
    def gauss():
        u1=max(rng(),1e-12); u2=rng()
        return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)
    preds=[]; sets=[]
    for d in range(nDatasets):
        xs=[]; ys=[]
        for s in range(nSamples):
            x=rng(); xs.append(x); ys.append(true_fn(kind,x)+noiseLv*gauss())
        sets.append((xs,ys))
        w=fit_poly(xs,ys,deg)
        preds.append(eval_poly(w,TEST_X))
    preds=np.array(preds)
    mean=preds.mean(axis=0)
    f=np.array([true_fn(kind,x) for x in TEST_X])
    bias2=np.mean((mean-f)**2)
    variance=np.mean(preds.var(axis=0))
    std=preds.std(axis=0)
    return dict(preds=preds, mean=mean, std=std, f=f, sets=sets,
                bias2=bias2, variance=variance, noise=noiseLv**2,
                total=bias2+variance+noiseLv**2)

def style(ax, title=None):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

# ---- closeup: ensemble fit (left) + U-curve decomposition (right) ----
res = decompose(8, 25, 0.25, 20)   # high-degree to show variance spread
fig = plt.figure(figsize=(9.6,4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07,0.14,0.42,0.76]); style(ax1, "アンサンブルのばらつき（次数8）")
for p in res['preds']:
    ax1.plot(TEST_X, p, color=NAVYLINE, alpha=0.20, lw=0.9)
ax1.plot(TEST_X, res['f'], color=GREEN, lw=2.6, ls="--", label="真の関数 sin(2πx)")
ax1.plot(TEST_X, res['mean'], color="#ffd24b", lw=2.6, label="平均予測")
ax1.set_xlabel("x", color="white", fontsize=9); ax1.set_ylabel("y", color="white", fontsize=9)
ax1.set_ylim(-2.2,2.2)
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7, loc="upper right")

ax2 = fig.add_axes([0.58,0.14,0.39,0.76]); style(ax2, "バイアス・バリアンス分解 vs 次数")
degs=list(range(1,13)); bi=[]; va=[]; to=[]
for g in degs:
    r=decompose(g,25,0.25,20); bi.append(r['bias2']); va.append(r['variance']); to.append(r['total'])
ax2.plot(degs, bi, color=BLUE, lw=2.0, marker="o", ms=3, label="バイアス²")
ax2.plot(degs, va, color=ORANGE, lw=2.0, marker="o", ms=3, label="バリアンス")
ax2.plot(degs, to, color=GREEN, lw=2.6, marker="o", ms=3, label="期待総誤差")
imin=int(np.argmin(to))
ax2.scatter([degs[imin]],[to[imin]], s=90, facecolor="none", edgecolor="#d63031", lw=2, zorder=5)
ax2.annotate(f"U字の底\n次数{degs[imin]}", (degs[imin], to[imin]), color="white", fontsize=7.5,
             xytext=(degs[imin]+1.2, to[imin]+0.06), arrowprops=dict(color="#d63031", arrowstyle="->"))
ax2.axhline(0.0625, color="#888", lw=1, ls=":")
ax2.text(8.5, 0.072, "既約誤差 σ²=0.0625", color="#aaa", fontsize=7)
ax2.set_xlabel("多項式モデルの次数", color="white", fontsize=9); ax2.set_ylabel("誤差（平均二乗）", color="white", fontsize=9)
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)
ax2.grid(True, color="#1e2d44", lw=0.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup, "  min deg=",degs[imin])

# ---- cover ----
figc = plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13,0.14,0.83,0.80]); style(axc)
axc.plot(degs, bi, color=BLUE, lw=2.0, label="バイアス²")
axc.plot(degs, va, color=ORANGE, lw=2.0, label="バリアンス")
axc.plot(degs, to, color=GREEN, lw=2.6, label="総誤差(U字)")
axc.set_xlabel("次数", color="white", fontsize=9)
axc.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "バイアス・バリアンス", "トレードオフ", "汎化誤差 = バイアス² + バリアンス + ノイズ", cc)
os.remove(cc)

# ---- gif: sweep degree, show ensemble fit tightening then exploding ----
frames=[]
seq=[1,2,3,4,5,6,8,10,12]
seq=seq+seq[::-1]
for g in seq:
    r=decompose(g,25,0.25,20)
    f2=plt.figure(figsize=(5.3,3.4)); f2.patch.set_facecolor(NAVY)
    a=f2.add_axes([0.12,0.15,0.84,0.74]); style(a)
    for p in r['preds']:
        a.plot(TEST_X,p,color=NAVYLINE,alpha=0.18,lw=0.8)
    a.plot(TEST_X,r['f'],color=GREEN,lw=2.4,ls="--")
    a.plot(TEST_X,r['mean'],color="#ffd24b",lw=2.4)
    a.set_ylim(-2.4,2.4)
    a.set_title(f"次数={g}  bias²={r['bias2']:.3f}  var={r['variance']:.3f}", color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=160)
print("done.")
