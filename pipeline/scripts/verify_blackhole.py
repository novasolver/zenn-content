# -*- coding: utf-8 -*-
"""Reproduce blackhole-event-horizon.html algorithm and cross-check vs closed form."""
import math

G = 6.674e-11; c = 2.998e8; hbar = 1.0546e-34; k_B = 1.381e-23; M_solar = 1.989e30

def compute(Msolar, aM=0.0):
    M = Msolar * M_solar
    r_s = 2*G*M/(c*c)            # m
    oneMinusA2 = max(0, 1 - aM*aM)
    r_outer = (1+math.sqrt(oneMinusA2)) * r_s/2
    r_inner = (1-math.sqrt(oneMinusA2)) * r_s/2
    if aM == 0:
        r_isco = 3*r_s
    else:
        Z1 = 1 + oneMinusA2**(1/3)*((1+aM)**(1/3)+(1-aM)**(1/3))
        Z2 = math.sqrt(3*aM*aM + Z1*Z1)
        r_isco = (r_s/2)*(3+Z2-math.sqrt(max(0,(3-Z1)*(3+Z1+2*Z2))))
    r_photon = 1.5*r_s
    T_H = (hbar*c**3)/(8*math.pi*G*M*k_B)
    life_sec = 5120*math.pi*G*G*M**3/(hbar*c**4)
    life_yr = life_sec/(365.25*86400)
    return dict(r_s=r_s, r_outer=r_outer, r_isco=r_isco, r_photon=r_photon,
                T_H=T_H, life_yr=life_yr, life_sec=life_sec)

print("=== Default: 10 M_sun, a/M=0 (Schwarzschild) ===")
r = compute(10, 0)
print(f"r_s={r['r_s']/1000:.3f} km  r+={r['r_outer']/1000:.3f} km  ISCO={r['r_isco']/1000:.3f} km")
print(f"photon={r['r_photon']/1000:.3f} km  T_H={r['T_H']:.3e} K  life={r['life_yr']:.3e} yr")

print("\n=== Cross-check r_s = 2GM/c^2 for 1 M_sun ===")
r1 = compute(1,0)
print(f"1 M_sun: r_s={r1['r_s']/1000:.4f} km (textbook ~2.95 km)")
print(f"T_H(1 M_sun)={r1['T_H']:.3e} K (textbook ~6.2e-8 K = 62 nK)")
print(f"life(1 M_sun)={r1['life_yr']:.3e} yr (textbook ~2e67 yr)")

print("\n=== Sgr A* 4.3e6 M_sun ===")
rs = compute(4.3e6, 0)
print(f"r_s={rs['r_s']/1000:.4e} km = {rs['r_s']/1e9:.3f} million km  T_H={rs['T_H']:.2e} K")

print("\n=== M87* 6.5e9 M_sun ===")
rm = compute(6.5e9, 0)
print(f"r_s={rm['r_s']/1e9:.3f} million km = {rm['r_s']/1.496e11:.2f} AU  life={rm['life_yr']:.2e} yr")

print("\n=== 10 M_sun a/M=0.8 (Kerr) ===")
rk = compute(10, 0.8)
print(f"r_s={rk['r_s']/1000:.2f} km  r+={rk['r_outer']/1000:.2f} km  ISCO={rk['r_isco']/1000:.2f} km")

print("\n=== Earth mass black hole ===")
M_earth = 5.972e24
r_s_earth = 2*G*M_earth/(c*c)
print(f"Earth r_s = {r_s_earth*1000:.2f} mm")

print("\n=== Primordial BH: lifetime = age of universe (1.38e10 yr) ===")
# solve M^3 = life_sec * hbar c^4 / (5120 pi G^2)
age_sec = 1.38e10*365.25*86400
M3 = age_sec * hbar * c**4 / (5120*math.pi*G*G)
M_pbh = M3**(1/3)
print(f"M_PBH = {M_pbh:.3e} kg = {M_pbh*1000:.2e} g")

print("\n=== max-spin Kerr a/M=0.998 ISCO and radiative efficiency ===")
rmax = compute(10, 0.998)
print(f"a/M=0.998: ISCO={rmax['r_isco']/1000:.2f} km  r+={rmax['r_outer']/1000:.2f} km")
print(f"ISCO/r_s ratio = {rmax['r_isco']/rmax['r_s']:.3f} (max spin ~0.5? approaches 1M=0.5 r_s)")
