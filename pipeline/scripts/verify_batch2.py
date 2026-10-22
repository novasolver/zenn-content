# -*- coding: utf-8 -*-
"""Verify numbers for batch2: doppler, string-resonance, wave-interference,
heat-diffusion, game-of-life, random-walk-2d."""
import numpy as np
def hr(t): print("\n" + "=" * 56 + f"\n{t}\n" + "=" * 56)

hr("DOPPLER  f_obs = f0 (v+vo)/(v-vs)")
def dop(f0, vs, vo, v=340.0):
    return f0 * (v + vo) / (v - vs)
for f0, vs, vo in [(440, 170, 0), (800, 20, 0), (1000, 30, 0)]:
    a = dop(f0, vs, vo); r = dop(f0, -vs, -vo)
    print(f"  f0={f0} vs={vs} vo={vo}: approach={a:.1f}Hz recede={r:.1f}Hz Ma={vs/340:.3f} shift={(a/f0-1)*100:.1f}%")
# Mach cone angle
for Ma in [1.2, 1.5, 2.0]:
    print(f"  Ma={Ma}: cone half-angle theta=asin(1/Ma)={np.degrees(np.arcsin(1/Ma)):.1f} deg")

hr("STRING  f1 = (1/2L) sqrt(T/mu),  v=sqrt(T/mu)")
def fstr(T, mu, L): return 1/(2*L)*np.sqrt(T/mu)
for T, mu_gpm, L in [(60, 1.0, 1.0), (73, 0.85, 0.65)]:
    mu = mu_gpm * 1e-3
    f1 = fstr(T, mu, L); v = np.sqrt(T/mu)
    print(f"  T={T}N mu={mu_gpm}g/m L={L}m: v={v:.1f}m/s f1={f1:.1f}Hz  harmonics={[round(n*f1) for n in range(1,6)]}")
# pluck Fourier coeff for triangular pluck at frac p: A_n ∝ sin(n*pi*p)/(n^2)
print("  triangular pluck modal weights |An| (pluck at 1/2, 1/3, 1/4):")
for p in [0.5, 1/3, 0.25]:
    An = [abs(np.sin(n*np.pi*p))/(n*n) for n in range(1, 8)]
    An = np.array(An); An = An/An.max()
    print(f"    p={p:.3f}: " + " ".join(f"n{n}={a:.2f}" for n, a in enumerate(An, 1)))

hr("WAVE INTERFERENCE")
v, f1, f2 = 5.0, 5.0, 6.0
print(f"  beat=|f1-f2|={abs(f1-f2):.1f}Hz  lam1=v/f1={v/f1:.2f}m  lam2=v/f2={v/f2:.3f}m  Amax=A1+A2=2")
print(f"  beat period = 1/|f1-f2| = {1/abs(f1-f2):.2f}s ; standing: y=2A cos(kx) sin(wt)")
# audio beat example 440 vs 443
print(f"  audio 440 vs 443 Hz -> beat {abs(440-443)} Hz")

hr("HEAT DIFFUSION  FTCS a = alpha*dt/dx^2 (2D stable if a<=0.25)")
dt, dx = 0.02, 1.0
for name, al in [("木材", 0.13), ("ガラス", 0.34), ("鋼材", 1.2), ("アルミ", 8.4), ("銅", 11.6)]:
    a = al*dt/dx/dx
    print(f"  {name}: alpha={al} -> a={a:.3f}  {'STABLE' if a<=0.25 else 'UNSTABLE!'}")
print("  steady-state (Dirichlet both ends): T(x) linear = ax+b")

hr("GAME OF LIFE  B3/S23")
print("  glider: period 4, translates (1,1) every 4 gens -> speed c/4")
print("  pulsar period 3; pentadecathlon period 15; Gosper gun emits 1 glider/30 gens")
print("  random soup steady density ~0.0293 (ash)")
# simulate a glider to confirm period-4 translation
def life_step(g):
    from scipy.signal import convolve2d
    k = np.ones((3,3)); k[1,1]=0
    n = convolve2d(g, k, mode='same', boundary='wrap')
    return ((g==1)&((n==2)|(n==3))) | ((g==0)&(n==3))
try:
    g = np.zeros((20,20), int)
    for (x,y) in [[1,0],[2,1],[0,2],[1,2],[2,2]]: g[y+5, x+5]=1
    g0=g.copy()
    for _ in range(4): g = life_step(g).astype(int)
    # shift back by (1,1) and compare
    shifted = np.roll(np.roll(g, -1, axis=0), -1, axis=1)
    print(f"  glider period-4 translation check: matches={np.array_equal(shifted, g0)}")
except Exception as e:
    print("  (scipy not available, skip glider sim:", e, ")")

hr("RANDOM WALK 2D  <r^2> = 2*d*D*t ; tool sets D=a^2/4, plots 2*D*t")
a = 5.0; D = a*a/4
# Monte Carlo lattice4
rng = np.random.RandomState(1)
def mc(kind, N=400, W=4000, steps=400):
    x = np.zeros(W); y = np.zeros(W)
    for _ in range(steps):
        if kind == 'lattice4':
            d = rng.randint(0, 4, W)
            x += np.where(d==0, a, np.where(d==1, -a, 0.0))
            y += np.where(d==2, a, np.where(d==3, -a, 0.0))
        elif kind == 'gauss':
            x += rng.randn(W)*a; y += rng.randn(W)*a
    return np.mean(x*x+y*y), steps
for kind in ['lattice4', 'gauss']:
    msd, steps = mc(kind)
    print(f"  {kind}: measured <r^2>/t = {msd/steps:.2f} ; tool theory 2Dt/t = {2*D:.2f} ; correct 4Dt/t = {4*D:.2f}")
print("  => for lattice4 measured≈a^2=25; tool's 2Dt line = a^2/2 =12.5 (HALF). Correct 2D law is <r^2>=4Dt.")
print("DONE.")
