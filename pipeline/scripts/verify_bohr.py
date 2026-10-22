# -*- coding: utf-8 -*-
"""Reproduce bohr-hydrogen-model.html algorithm and cross-check vs closed form."""
import math

a0 = 0.0529  # nm (tool uses this; true Bohr radius 0.0529 nm = 0.529 Angstrom)

def E(n): return -13.6 / (n*n)          # eV
def r(n): return n*n*a0                  # nm
def wl(n1, n2):                          # nm, tool: 1240/|dE|
    dE = abs(E(n1) - E(n2))
    return 1240.0 / dE

# default tool state n1=4, n2=2
print("=== Default n1=4 -> n2=2 ===")
print("E1(n=4)=", round(E(4),3), "eV ; E2(n=2)=", round(E(2),3), "eV")
print("dE=", round(abs(E(4)-E(2)),3), "eV ; lambda=", round(wl(4,2),1), "nm")
print("r1(n=4)=", round(r(4),4), "nm ; r2(n=2)=", round(r(2),4), "nm")

# Balmer series: upper -> n=2
print("\n=== Balmer series (n->2) tool wavelengths ===")
names = {3:"Halpha",4:"Hbeta",5:"Hgamma",6:"Hdelta"}
for u in range(3,7):
    print(f"{u}->2  {names[u]:7s} lambda={wl(u,2):.1f} nm  dE={abs(E(u)-E(2)):.3f} eV")

# Lyman series (n->1)
print("\n=== Lyman series (n->1) ===")
for u in range(2,5):
    print(f"{u}->1  lambda={wl(u,1):.1f} nm  dE={abs(E(u)-E(1)):.3f} eV")

# Cross-check Rydberg closed form for Balmer
print("\n=== Cross-check vs Rydberg formula ===")
R_H = 1.0967757e7  # m^-1
for u in range(3,7):
    inv_lambda = R_H * (1/2**2 - 1/u**2)
    lam_nm = 1e9 / inv_lambda
    print(f"{u}->2 Rydberg lambda={lam_nm:.2f} nm  vs tool {wl(u,2):.1f} nm")

# ionization energy
print("\n=== Ionization (n=1) ===")
print("E1=", E(1), "eV  -> ionization energy = 13.6 eV")
print("Bohr radius r(1)=", r(1), "nm =", r(1)*10, "Angstrom")
