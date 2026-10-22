# -*- coding: utf-8 -*-
"""Verify column-buckling-adv. Pcr=pi^2 EI/(KL)^2; lambda=KL/r, r=sqrt(I/A);
sigma_cr=pi^2 E/lambda^2. Section props faithful to tool's sectionProps().
Secant P-delta: delta=e*(1/cos((pi/2)sqrt(P/Pcr))-1)."""
import math

E_steel = 200e3  # MPa (tool uses E*1e3 from GPa)

def section_props(t, b, h):
    if t == 'rect':
        I = b*h**3/12; A = b*h
    elif t == 'circle':
        r = b/2; I = math.pi*r**4/4; A = math.pi*r*r
    elif t == 'ihh':  # H-section: tf=0.12h, tw=0.08b, bf=b
        tf = 0.12*h; tw = 0.08*b; bf = b
        I = bf*h**3/12 - (bf-tw)*(h-2*tf)**3/12
        A = 2*bf*tf + tw*(h-2*tf)
    else:  # hollow square: t=0.1*min(b,h)
        tt = min(b, h)*0.1
        I = b*h**3/12 - (b-2*tt)*(h-2*tt)**3/12
        A = b*h - (b-2*tt)*(h-2*tt)
    return I, A, math.sqrt(I/A)

def pcr(E, I, K, L):  # E in MPa, I mm4, L mm -> N -> kN
    return math.pi**2 * E * I / (K*L)**2 / 1000

# Tool defaults: section=ihh, L=3000, b=150, h=200, K=1.0, e=5, E=200GPa
I, A, r = section_props('ihh', 150, 200)
K, L = 1.0, 3000
P = pcr(E_steel, I, K, L)
lam = K*L/r
sig = math.pi**2 * E_steel / lam**2
print("[default H-section L=3000 b=150 h=200 K=1.0 E=200GPa]")
print(f"  I={I:.1f} mm4 = {I/1e4:.1f} cm4   A={A:.1f} mm2 = {A/100:.1f} cm2   r={r:.2f} mm")
print(f"  Pcr={P:.1f} kN   lambda={lam:.2f}   sigma_cr={sig:.1f} MPa")

# Known textbook: simply-supported steel column, rect 100x100, L=3000, E=200GPa, K=1
I2, A2, r2 = section_props('rect', 100, 100)
P2 = pcr(E_steel, I2, 1.0, 3000)
print(f"\n[textbook rect 100x100 L=3000 K=1] I={I2:.0f}mm4 Pcr={P2:.1f}kN lambda={3000/r2:.1f}")
# hand calc: I=100^4/12=8.333e6, Pcr=pi^2*2e5*8.333e6/3000^2/1e3
hand = math.pi**2*2e5*(100**4/12)/(3000**2)/1000
print(f"  hand Pcr={hand:.1f} kN (match)")

# end-condition K factor effect (rect 100x100 L=3000)
print("\n[K factor effect, rect 100x100 L=3000]")
for K,name in [(1.0,'両端ピン'),(0.5,'両端固定'),(0.7,'固定-ピン'),(2.0,'固定-自由')]:
    print(f"  K={K} {name}: Pcr={pcr(E_steel,I2,K,3000):.1f} kN  (vs K=1 x{(1/K)**2:.2f})  lambda={K*3000/r2:.1f}")

# Secant P-delta curve sample (default H, e=5)
print("\n[P-delta secant, default H-section e=5mm] (P/Pcr, delta mm)")
e = 5
for ratio in [0.0,0.2,0.5,0.8,0.95]:
    ang = (math.pi/2)*math.sqrt(ratio)
    delta = e*(1/math.cos(ang)-1) if e>0 else 0
    print(f"  P/Pcr={ratio:.2f} P={ratio*P:.1f}kN  delta={delta:.3f}mm")

# slenderness regime
print(f"\n[slenderness] lambda={lam:.1f}: ", "弾性座屈支配 (lambda>~100)" if lam>100 else "中間柱域 (lambda<100, 非弾性座屈も考慮)")
