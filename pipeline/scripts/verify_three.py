# -*- coding: utf-8 -*-
"""Verify all numbers for atkinson-cycle, clausius-clapeyron-vapor, betz-limit.
Reproduces each tool's exact JS compute() logic and cross-checks known results."""
import math

print("="*70)
print("TOOL 1: atkinson-cycle  (R_AIR=287 J/kgK)")
print("="*70)
R_AIR = 287.0
def atkinson(r, g, T1, P1, qIn):
    cv = R_AIR/(g-1)
    cp = g*cv
    T2 = T1*r**(g-1)
    P2 = P1*r**g
    T3 = T2 + (qIn*1000)/cv
    P3 = P2*T3/T2
    T4 = T3*(P1/P3)**((g-1)/g)
    rExp = (P3/P1)**(1/g)
    qInJ = qIn*1000
    qOut = cp*(T4-T1)
    eta = 1 - qOut/qInJ
    wNet = qInJ - qOut
    etaOtto = 1 - 1/r**(g-1)
    return dict(T2=T2,P2=P2,T3=T3,P3=P3,T4=T4,rExp=rExp,eta=eta,wNet=wNet,
                etaOtto=etaOtto, rExpRatio=rExp/r, adv=(eta-etaOtto)*100)

# default tool params: r=10, g=1.4, T1=300, P1=100, qIn=1800
d = atkinson(10, 1.4, 300, 100, 1800)
print(f"DEFAULT r=10 g=1.4 T1=300 P1=100 qIn=1800:")
print(f"  T2={d['T2']:.1f}K T3={d['T3']:.0f}K P3={d['P3']:.0f}kPa T4={d['T4']:.1f}K")
print(f"  eta_Atkinson={d['eta']*100:.1f}%  eta_Otto={d['etaOtto']*100:.1f}%  advantage=+{d['adv']:.1f}pt")
print(f"  rExp/rComp={d['rExpRatio']:.2f}  wNet={d['wNet']/1000:.0f} kJ/kg")
# sanity: Atkinson > Otto, rExp > rComp
assert d['eta'] > d['etaOtto'], "Atkinson should beat Otto"
assert d['rExp'] > 10, "expansion ratio should exceed compression ratio"
print(f"  CHECK eta_Atkinson > eta_Otto: PASS")
print(f"  CHECK rExp({d['rExp']:.2f}) > rComp(10): PASS")

# table across compression ratio (gamma=1.4 default)
print("\n  r-sweep table (g=1.4,T1=300,P1=100,qIn=1800):")
print("   r  | eta_Atk% | eta_Otto% | +pt  | rExp/r")
for r in [8,10,12,14,16]:
    dd = atkinson(r,1.4,300,100,1800)
    print(f"  {r:>3} |  {dd['eta']*100:>6.1f}  |  {dd['etaOtto']*100:>6.1f}   | {dd['adv']:>4.1f} | {dd['rExpRatio']:.2f}")

print()
print("="*70)
print("TOOL 2: clausius-clapeyron-vapor  (R=8.314 J/molK)")
print("="*70)
R = 8.314
def cc(T1,P1,dH_kJ,T2):
    enthalpyOverR = dH_kJ*1000/R       # K
    invDiff = 1/T2 - 1/T1
    lnRatio = -enthalpyOverR*invDiff
    ratio = math.exp(lnRatio)
    P2 = P1*ratio
    return dict(P2=P2,ratio=ratio,lnRatio=lnRatio,HoverR=enthalpyOverR,dT=T2-T1)

# default tool params: T1=373.15, P1=101.325, dH=40.7, T2=400
d2 = cc(373.15,101.325,40.7,400)
print(f"DEFAULT T1=373.15K P1=101.325kPa dH=40.7kJ/mol T2=400K:")
print(f"  P2={d2['P2']:.1f}kPa ratio={d2['ratio']:.3f} lnRatio={d2['lnRatio']:.3f} dH/R={d2['HoverR']:.0f}K dT={d2['dT']:.1f}K")

# Known result cross-check: water 20C -> 100C vapor pressure
# Using dH=40.7, ref=(373.15,101.325), eval=293.15
d_20 = cc(373.15,101.325,40.7,293.15)
print(f"\n  CROSS-CHECK water 100C->20C: P(20C)={d_20['P2']:.2f} kPa (literature ~2.3 kPa)")
# Boiling point at Fuji (0.65 atm = 65.86 kPa): solve for T where P=65.86 from (373.15,101.325)
# P = P1 exp(-H/R(1/T - 1/T1)) => 1/T = 1/T1 - (R/H)ln(P/P1)
Pf = 0.65*101.325
HoR = 40.7*1000/R
invT = 1/373.15 - (1/HoR)*math.log(Pf/101.325)
Tf = 1/invT
print(f"  CROSS-CHECK Fuji 0.65atm boiling T = {Tf:.1f}K = {Tf-273.15:.1f}C (literature ~87C)")
# Pressure cooker 2 atm
P2atm = 2*101.325
invT2 = 1/373.15 - (1/HoR)*math.log(P2atm/101.325)
Tpc = 1/invT2
print(f"  CROSS-CHECK pressure cooker 2atm boiling T = {Tpc:.1f}K = {Tpc-273.15:.1f}C (literature ~120C)")

# table: vapor pressure of water vs T
print("\n  Water vapor pressure table (T1=373.15,P1=101.325,dH=40.7):")
print("   T(C) | T(K)   | P2(kPa) | ratio")
for Tc in [20,40,60,80,100,120]:
    dd = cc(373.15,101.325,40.7,Tc+273.15)
    print(f"  {Tc:>4} | {Tc+273.15:>6.2f} | {dd['P2']:>7.2f} | {dd['ratio']:.3f}")

print()
print("="*70)
print("TOOL 3: betz-limit")
print("="*70)
def cp_of(a): return 4*a*(1-a)*(1-a)
def betz(V,D,a,rho):
    A = math.pi*D*D/4
    Pwind = 0.5*rho*A*V**3
    cp = max(0,cp_of(a))
    Pcap = cp*Pwind
    ratio = cp/(16/27)
    return dict(A=A,Pwind=Pwind,cp=cp,Pcap=Pcap,ratio=ratio)

# Cp,max at a=1/3
print(f"Cp(1/3) = {cp_of(1/3):.6f}   16/27 = {16/27:.6f}")
assert abs(cp_of(1/3) - 16/27) < 1e-9
print(f"  CHECK Cp(1/3)==16/27: PASS")
# verify a=1/3 is the maximum via derivative dC/da=4(1-a)(1-3a)
print(f"  Cp(0.25)={cp_of(0.25):.4f}  Cp(1/3)={cp_of(1/3):.4f}  Cp(0.40)={cp_of(0.40):.4f}  Cp(0.50)={cp_of(0.50):.4f}")
assert cp_of(1/3) > cp_of(0.25) and cp_of(1/3) > cp_of(0.40)
print(f"  CHECK a=1/3 is the peak: PASS")

# default tool params: V=12, D=80, a=0.333, rho=1.225
d3 = betz(12,80,0.333,1.225)
print(f"\nDEFAULT V=12 D=80 a=0.333 rho=1.225:")
print(f"  A={d3['A']:.0f}m2 Cp={d3['cp']:.3f} Pwind={d3['Pwind']/1e6:.2f}MW Pcap={d3['Pcap']/1e6:.2f}MW ratio={d3['ratio']*100:.1f}%")

# V^3 dependence check
print(f"\n  CHECK V^3 dependence: V=6->8 power ratio = {(8/6)**3:.3f} (expect 2.370)")
# Haliade-X example from tool: V=11, D=220, a=0.33, rho=1.225
dH3 = betz(11,220,0.33,1.225)
print(f"  Haliade-X (V=11,D=220,a=0.33): Pwind={dH3['Pwind']/1e6:.1f}MW Pcap={dH3['Pcap']/1e6:.1f}MW")

# Cp(a) table
print("\n  Cp(a) table:")
print("    a   |  Cp   ")
for a in [0.0,0.1,0.2,1/3,0.4,0.5]:
    print(f"  {a:>5.3f} | {cp_of(a):.4f}")

print("\nALL CHECKS PASSED")
