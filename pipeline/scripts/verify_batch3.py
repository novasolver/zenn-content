# -*- coding: utf-8 -*-
"""Verify numbers for batch3: brachistochrone, spring-pendulum, lens, parseval,
goertzel, cepstrum, fourier-series, convection-cells."""
import numpy as np
def hr(t): print("\n" + "=" * 56 + f"\n{t}\n" + "=" * 56)

hr("BRACHISTOCHRONE")
def solve_thetaf(ratio):
    f = lambda th: (th - np.sin(th)) / (1 - np.cos(th)) - ratio
    lo, hi = 1e-3, 2 * np.pi - 1e-3
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
for D, H, g in [(5.0, 3.0, 9.81), (5.0, 5.0, 9.81)]:
    thf = solve_thetaf(D / H)
    a = H / (1 - np.cos(thf)); bt = thf * np.sqrt(a / g)
    L = np.hypot(D, H); st = np.sqrt(2 * L * L / (g * H))
    print(f"  D={D} H={H}: thetaF={thf:.3f} a={a:.3f} brach={bt:.3f}s straight={st:.3f}s saved={(st-bt)/st*100:.1f}% vend={np.sqrt(2*g*H):.2f}")

hr("SPRING-PENDULUM  2:1 parametric resonance (w_spring=2 w_pend)")
def w_spring(k, m): return np.sqrt(k / m)
def w_pend(g, L0): return np.sqrt(g / L0)
g = 9.81
print(f"  preset 'resonance' k=2,m=0.5,L0=0.5: w_s={w_spring(2,0.5):.2f} w_p={w_pend(g,0.5):.2f} ratio w_s/w_p={w_spring(2,0.5)/w_pend(g,0.5):.2f} (2:1 needs 2.0)")
# k for true 2:1 with m=0.5,L0=0.5
k21 = (2 * w_pend(g, 0.5))**2 * 0.5
print(f"  true 2:1 needs k = (2*w_p)^2*m = {k21:.1f} N/m (slider max 50)")
# RK4 elastic pendulum, measure energy exchange at 2:1 vs preset
def deriv(s, k, m, L0):
    r, dr, th, dth = s
    rs = max(r, 0.01)
    ddr = rs * dth * dth - g * np.cos(th) + (k / m) * (L0 - rs)
    ddth = (-g * np.sin(th) - 2 * dr * dth) / rs
    return np.array([dr, ddr, dth, ddth])
def energy(s, k, m, L0):
    r, dr, th, dth = s
    return 0.5*m*(dr*dr+r*r*dth*dth) - m*g*r*np.cos(th) + 0.5*k*(r-L0)**2
def run(k, m, L0, r0, th0_deg, T=40, dt=0.001):
    s = np.array([r0, 0.0, np.radians(th0_deg), 0.0]); E0 = energy(s, k, m, L0)
    Emin = Emax = E0; swing = []
    n = int(T/dt)
    for i in range(n):
        k1 = deriv(s,k,m,L0); k2 = deriv(s+0.5*dt*k1,k,m,L0)
        k3 = deriv(s+0.5*dt*k2,k,m,L0); k4 = deriv(s+dt*k3,k,m,L0)
        s = s + dt/6*(k1+2*k2+2*k3+k4)
        E = energy(s,k,m,L0); Emin=min(Emin,E); Emax=max(Emax,E)
        if i % 20 == 0: swing.append(abs(s[2]))
    return E0, (Emax-Emin)/abs(E0)*100, max(swing), np.degrees(min(swing))
for label, k in [("preset k=2", 2.0), ("tuned 2:1 k=39.2", 39.2)]:
    E0, drift, mxsw, mnsw = run(k, 0.5, 0.5, 0.55, 10)
    print(f"  {label}: E drift={drift:.4f}% over 40s; swing angle range min={mnsw:.1f}deg max={np.degrees(mxsw):.1f}deg")

hr("LENS  1/f=1/do+1/di, m=-di/do")
def lens(f, do): di = f*do/(do-f); return di, -di/do
for name, f, do, ho in [("default", 100, 200, 40), ("magnifier", 50, 40, 30),
                         ("camera", 50, 400, 40), ("diverging", -100, 150, 40)]:
    di, m = lens(f, do)
    typ = "real/inv" if di > 0 else "virtual/upright"
    print(f"  {name}: f={f} do={do} -> di={di:.1f}mm m={m:+.2f}x hi={m*ho:+.1f}mm ({typ})")

hr("PARSEVAL  sum|x|^2 = (1/N) sum|X|^2")
N, A, f0 = 512, 1.0, 10
n = np.arange(N); x = A*np.cos(2*np.pi*f0*n/N)
X = np.fft.fft(x)
Et = np.sum(x*x); Ef = np.sum(np.abs(X)**2)/N
print(f"  x=A cos: Et={Et:.3f} (=N*A^2/2={N*A*A/2}) Ef={Ef:.3f} relErr={abs(Et-Ef)/Et:.2e}")

hr("GOERTZEL  DTMF")
ROW = [697,770,852,941]; COL=[1209,1336,1477,1633]
key=5; Fs=8000; Nn=256
r,c = key//4, key%4
print(f"  key={key} -> row={ROW[r]}Hz col={COL[c]}Hz; bins k_row={round(ROW[r]*Nn/Fs)} k_col={round(COL[c]*Nn/Fs)}; ops N*M={Nn*8}")
def goertzel(x, N, Fs, tf):
    k = round(tf*N/Fs); w = 2*np.pi*k/N; cc = 2*np.cos(w); s1=s2=0.0
    for v in x: s=v+cc*s1-s2; s2=s1; s1=s
    return s1*s1+s2*s2-cc*s1*s2
nn = np.arange(Nn); sig = 0.5*np.sin(2*np.pi*ROW[r]*nn/Fs)+0.5*np.sin(2*np.pi*COL[c]*nn/Fs)
mags = [goertzel(sig, Nn, Fs, ff) for ff in ROW+COL]
print(f"  detected strongest row idx={int(np.argmax(mags[:4]))}(={ROW[int(np.argmax(mags[:4]))]}) col idx={int(np.argmax(mags[4:]))}(={COL[int(np.argmax(mags[4:]))]})")

hr("CEPSTRUM  F0 = Fs/quefrency")
f0c, Fsc = 200, 8000
print(f"  f0={f0c} Fs={Fsc}: quefrency peak={Fsc/f0c:.0f} samples, tau={1000/f0c:.2f}ms, f0est=Fs/q={Fsc/(Fsc/f0c):.0f}Hz")

hr("FOURIER SERIES  Gibbs overshoot")
def partial_square(N, A=1.0, npts=4000):
    t = np.linspace(0, 1, npts); s = np.zeros(npts)
    for nn in range(1, N+1):
        if nn % 2 == 1: s += 4*A/(nn*np.pi)*np.sin(2*np.pi*nn*t)
    return s.max()
for N in [10, 25, 50, 100]:
    mx = partial_square(N)
    print(f"  square N={N}: max={mx:.4f}, overshoot=(max-A)/A={(mx-1)*100:.2f}% (Gibbs ~8.95%)")

hr("CONVECTION  Ra")
for log in [3.1, 3.4, 4.5]:
    Ra = 10**log
    state = ("安定" if Ra<1708 else "定常対流セル" if Ra<5000 else "振動対流" if Ra<50000 else "乱流的")
    print(f"  log10Ra={log}: Ra={Ra:.0f} -> {state}  (Ra_crit=1708)")
print("DONE.")
