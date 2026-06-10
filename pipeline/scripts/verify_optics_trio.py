# -*- coding: utf-8 -*-
"""Verify all numbers for bragg-diffraction, beer-lambert-law, airy-disk articles.
Reproduces each tool's JS algorithm exactly. Run in FOREGROUND."""
import math
from scipy.special import j1, jn_zeros
from scipy.integrate import quad

print("="*60)
print("1) BRAGG DIFFRACTION  (2 d sinθ = nλ; d_eff=d(1+ε); nmax=floor(2 d_eff/λ))")
print("="*60)
def bragg(d, lam, n, eps):
    dEff = d*(1+eps)
    sinT = (n*lam)/(2*dEff)
    nMax = math.floor((2*dEff)/lam)
    if sinT>1 or sinT<0:
        return dEff, sinT, None, None, nMax
    th = math.degrees(math.asin(sinT))
    return dEff, sinT, th, 2*th, nMax

# default: d=2.50, lam=1.54, n=1, eps=0
for (d,lam,n,eps) in [(2.50,1.54,1,0.0),(2.50,1.54,2,0.0),(2.50,1.54,3,0.0),
                       (2.50,0.71,1,0.0),(2.50,1.79,1,0.0),
                       (2.50,1.54,1,0.01),(2.50,1.54,1,-0.01),
                       (3.14,1.541,1,0.0)]:
    dEff,sinT,th,tt,nMax = bragg(d,lam,n,eps)
    th_s = f"{th:.2f}" if th is not None else "NaN(no reflection)"
    tt_s = f"{tt:.2f}" if tt is not None else "NaN"
    print(f"  d={d} λ={lam} n={n} ε={eps}: d_eff={dEff:.3f} sinθ={sinT:.4f} θ={th_s}° 2θ={tt_s}° nmax={nMax}")
# nmax check for Mo Kα 0.71
print(f"  Mo Kα 2d/λ = {2*2.5/0.71:.3f} -> nmax {math.floor(2*2.5/0.71)}")
print(f"  Cu Kα 2d/λ = {2*2.5/1.54:.3f} -> nmax {math.floor(2*2.5/1.54)}")

print()
print("="*60)
print("2) BEER-LAMBERT  (A=ε·l·(c·1e-3) where c in mmol/L; T=10^-A)")
print("="*60)
def beer(eps,l,c_mmol):
    A = eps*l*(c_mmol*1e-3)
    T = 10**(-A)
    absorbed = (1-T)*100
    halfLen = math.log10(2)/(eps*c_mmol*1e-3)
    return A,T*100,absorbed,halfLen
# default eps=5000, l=1.0, c=0.10 mmol/L
for (eps,l,c) in [(5000,1.0,0.10),(5000,1.0,0.20),(5000,1.0,0.30),
                   (5000,2.0,0.10),(1500,1.0,0.10),(120000,1.0,0.01)]:
    A,T,ab,hl = beer(eps,l,c)
    print(f"  ε={eps} l={l} c={c}mM: A={A:.3f} T={T:.1f}% absorbed={ab:.1f}% halfLen={hl:.3f}cm")
# A=1 -> T? ; A=2 -> T?
print(f"  A=1 -> T={10**-1*100:.1f}%   A=2 -> T={10**-2*100:.2f}%   A=0.1 -> T={10**-0.1*100:.1f}%")
print(f"  A=0.5 default -> T={10**-0.5*100:.2f}%")

print()
print("="*60)
print("3) AIRY DISK  (θ=1.22λ/D; r_focal=1.22λF#; rR=θ·R; energy 83.8%)")
print("="*60)
def airy(lam_nm,D_mm,Fnum,R_m):
    lam=lam_nm*1e-9; D=D_mm*1e-3
    theta=1.22*lam/D
    rFocal=1.22*lam*Fnum
    rDist=theta*R_m
    return theta, rFocal, rDist
for (lam,D,F,R) in [(550,100,8.0,1000),(550,2400,8.0,1000),(532,50,10,2.0),
                     (550,10,8.0,1000),(200,100,8.0,1000)]:
    th,rf,rd=airy(lam,D,F,R)
    arcsec=math.degrees(th)*3600
    print(f"  λ={lam}nm D={D}mm F#={F} R={R}m: θ={th*1e6:.2f}μrad ({arcsec:.3f}\") r_focal={rf*1e6:.2f}μm rR={rd*1e3:.2f}mm")
# first zero of J1
z1=jn_zeros(1,1)[0]
print(f"  First zero of J1 = {z1:.4f} (tool uses 3.8317)")
# energy in central disk = 1 - J0(z)^2 - J1(z)^2 ; for first dark ring
from scipy.special import j0
enc = 1 - j0(z1)**2 - j1(z1)**2
print(f"  Encircled energy in central disk = {enc*100:.2f}% (tool says 83.8%)")
# verify via integral of [2 J1(x)/x]^2 * x normalized
def airy_int(x):
    if x<1e-9: return 1.0*x
    return (2*j1(x)/x)**2 * x
num,_=quad(airy_int,0,z1)
den,_=quad(airy_int,0,500,limit=400)
print(f"  Integral ratio = {num/den*100:.2f}%")
# diffraction blur f#11 fullframe pixel 6um
rf11=1.22*550e-9*11*1e6
print(f"  F#=11 λ=550nm r_focal={rf11:.2f}μm (>6μm pixel -> diffraction limited)")
# lambda 200 vs 550 improvement
print(f"  λ improvement 550->200: factor {550/200:.2f}x")
