# -*- coding: utf-8 -*-
"""Verify catenary-cable numbers, faithful to the tool's JS.
Catenary: solve a*(cosh(L/2a)-1)=d by bisection; H=w*a; Tmax=H+w*d; S=2a*sinh(L/2a).
Parabola: H=wL^2/(8d); Tmax=sqrt(H^2+(wL/2)^2); S=L(1+(8/3)(d/L)^2).
"""
import math

def solve_a(L, d):
    f = lambda a: a*(math.cosh(L/(2*a))-1) - d
    lo, hi = 1e-6, L*1000
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: hi = mid
        else: lo = mid
        if hi-lo < 1e-9: break
    return (lo+hi)/2

def catenary(L, d, w):
    a = solve_a(L, d)
    H = w*a
    Tmax = H + w*d
    S = 2*a*math.sinh(L/(2*a))
    return a, H, Tmax, S

def parabola(L, d, w):
    H = w*L*L/(8*d)
    Tmax = math.sqrt(H*H + (w*L/2)**2)
    S = L*(1 + (8/3)*(d/L)**2)
    return H, Tmax, S

# Default tool case: L=100, d=10, w=50
L, d, w = 100, 10, 50
a, H, Tmax, S = catenary(L, d, w)
print(f"[catenary default] L={L} d={d} w={w}")
print(f"  a={a:.4f} m  H={H:.2f} N = {H/1000:.3f} kN")
print(f"  Tmax={Tmax:.2f} N = {Tmax/1000:.3f} kN  S={S:.4f} m")
Hp, Tmaxp, Sp = parabola(L, d, w)
print(f"[parabola default] H={Hp/1000:.3f} kN Tmax={Tmaxp/1000:.3f} kN S={Sp:.4f} m")
print(f"  H rel diff cat vs para = {(H-Hp)/Hp*100:.3f}%")
print(f"  S rel diff = {(S-Sp)/Sp*100:.4f}%")

# Cross check known analytic: y=a cosh(x/a). At d/L small, catenary->parabola.
print("\n[d/L sweep: catenary vs parabola H, % diff]")
for dd in (1, 2.5, 5, 10, 20, 40):
    a2,H2,_,S2 = catenary(L, dd, w)
    Hp2,_,Sp2 = parabola(L, dd, w)
    print(f"  d={dd:5.1f} (d/L={dd/L*100:4.1f}%)  Hcat={H2/1000:7.3f}kN Hpar={Hp2/1000:7.3f}kN  diff={ (H2-Hp2)/Hp2*100:6.2f}%  S diff={(S2-Sp2)/Sp2*100:6.3f}%")

# Known textbook: shallow cable d/L=1/8 (=12.5), classic parabola H=wL^2/(8d)
dd = L/8
Hp3,_,_ = parabola(L, dd, w)
print(f"\n[textbook shallow d=L/8={dd}] parabola H=wL^2/(8d)={Hp3:.2f} N (={w*L*L/(8*dd):.2f})")

# Stress + elastic elongation for default + steel A=100mm^2 E=200GPa
A_mm2, E_GPa = 100, 200
A_m2 = A_mm2*1e-6; E_Pa = E_GPa*1e9
sigma = Tmax/A_m2/1e6
dL = Tmax*S/(A_m2*E_Pa)*1000
print(f"\n[stress/elong default, A=100mm2 E=200GPa] sigma={sigma:.1f} MPa  dL={dL:.1f} mm")

# A bigger realistic transmission-line-ish case
L2,d2,w2 = 300, 9, 15
a4,H4,Tmax4,S4 = catenary(L2,d2,w2)
print(f"\n[transmission-ish] L={L2} d={d2} w={w2}: H={H4/1000:.3f}kN Tmax={Tmax4/1000:.3f}kN S={S4:.3f}m a={a4:.2f}m d/L={d2/L2*100:.2f}%")
