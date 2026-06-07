# -*- coding: utf-8 -*-
"""Verify batch5: diffraction-grating, blackbody, carnot, rlc, gear, collision-1d."""
import numpy as np
def hr(t): print("\n" + "=" * 56 + f"\n{t}\n" + "=" * 56)

hr("DIFFRACTION GRATING  d(sin th - sin thi)=m lam")
d = 1.67e-6; lam = 532e-9; thi = 0; N = 500
for m in range(0, 4):
    s = m*lam/d + np.sin(thi)
    th = np.degrees(np.arcsin(s)) if abs(s) <= 1 else None
    print(f"  m={m}: sin={s:.3f} theta={th if th is None else f'{th:.1f}deg'}  R=mN={m*N} dlam={lam*1e9/(m*N) if m else float('inf'):.2f}nm")
print(f"  d=1.67um -> {1/(1.67e-3):.0f} lines/mm")

hr("BLACKBODY  Planck/Wien/Stefan-Boltzmann")
sigma = 5.67e-8
for T, name in [(5778, "太陽"), (310, "人体"), (2700, "白熱灯"), (10000, "青色星")]:
    lpk = 2.898e-3 / T * 1e9
    P = sigma * T**4
    print(f"  {name} {T}K: lambda_peak={lpk:.0f}nm  P=sigma T^4={P:.2e} W/m2 ({P/1e6:.1f} MW/m2)")

hr("CARNOT  eta=1-Tc/Th")
for Th, Tc, QH in [(600, 300, 2000), (800, 300, 2000), (1200, 300, 2000)]:
    eta = 1 - Tc/Th; W = QH*eta; QC = QH - W; dS = QH/Th
    print(f"  Th={Th} Tc={Tc} QH={QH}: eta={eta:.3f} W={W:.0f}J QC={QC:.0f}J dS={dS:.2f}J/K  (QC/Tc={QC/Tc:.2f})")

hr("RLC RESONANCE  f0=1/(2pi sqrt(LC))")
def rlc(R, L, C, series=True):
    f0 = 1/(2*np.pi*np.sqrt(L*C)); w0 = 2*np.pi*f0
    Q = w0*L/R if series else R/(w0*L)
    BW = f0/Q
    Q_alt = (1/R)*np.sqrt(L/C) if series else R*np.sqrt(C/L)
    return f0, Q, BW, Q_alt
for name, R, L, C, s in [("default(series)", 31.6, 1.58e-3, 4.0e-6, True),
                          ("AMラジオ", 5, 270e-6, 100e-12, True),
                          ("音声", 100, 10e-3, 10e-6, True)]:
    f0, Q, BW, Qa = rlc(R, L, C, s)
    print(f"  {name}: f0={f0:.1f}Hz Q={Q:.1f} (=(1/R)sqrt(L/C)={Qa:.1f}) BW={BW:.1f}Hz")
# parallel Q identity check
R, L, C = 50, 1e-3, 1e-6; w0 = 1/np.sqrt(L*C)
print(f"  parallel Q identity: R/(w0 L)={R/(w0*L):.3f}  ==  w0 R C={w0*R*C:.3f}  (equal -> agent's 'bug' is false)")
print(f"  parallel Z_res: getZ gives R={R}; statZ0 shows Q^2 R={(R/(w0*L))**2*R:.0f} -> inconsistent for ideal parallel")

hr("GEAR RATIO  i=Z2/Z1")
for z1, z2, n1, t1, eta in [(20, 40, 1500, 10, 0.98)]:
    i = z2/z1; nout = n1/i; tout = t1*i*eta; P = t1*2*np.pi*n1/60
    print(f"  z1={z1} z2={z2} n1={n1}: i={i} nout={nout:.0f}rpm tout={tout:.1f}Nm P={P:.0f}W")
print(f"  planetary i=1+Zr/Zs, Zs=20 Zr=60 -> i={1+60/20}")

hr("COLLISION 1D  (momentum-conserving restitution)")
def coll(m1, m2, v1, v2, e):
    v1p = ((m1-e*m2)*v1 + (1+e)*m2*v2)/(m1+m2)
    v2p = ((m2-e*m1)*v2 + (1+e)*m1*v1)/(m1+m2)
    return v1p, v2p
for m1, m2, v1, v2, e in [(5, 5, 5, -3, 1.0), (5, 5, 5, -3, 0.0), (10, 2, 5, 0, 1.0)]:
    v1p, v2p = coll(m1, m2, v1, v2, e)
    pb, pa = m1*v1+m2*v2, m1*v1p+m2*v2p
    keb = 0.5*m1*v1*v1+0.5*m2*v2*v2; kea = 0.5*m1*v1p*v1p+0.5*m2*v2p*v2p
    print(f"  m=({m1},{m2}) v=({v1},{v2}) e={e}: v'=({v1p:.2f},{v2p:.2f}) p:{pb:.1f}->{pa:.1f} KE:{keb:.1f}->{kea:.1f} loss={keb-kea:.1f}")
print("  => momentum conserved for all e (p before == after). CORRECT (unlike newtons-cradle).")
print("DONE.")
