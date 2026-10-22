# -*- coding: utf-8 -*-
"""Verify belt-friction (capstan / Euler-Eytelwein).
Ratio = T_load/T_hold = exp(mu*beta); T_hold = T_load*exp(-mu*beta);
T(phi)=T_hold*exp(mu*phi). beta in radians."""
import math

def ratio(mu, beta): return math.exp(mu*beta)

# Tool default: mu=0.30, wrap=180deg, Tload=1000N, pos=50%
mu, wrapDeg, Tload, pos = 0.30, 180, 1000, 50
beta = math.radians(wrapDeg)
R = ratio(mu, beta)
Thold = Tload / R
phiObs = beta * pos/100
Tobs = Thold*math.exp(mu*phiObs)
reduce = (1 - Thold/Tload)*100
print(f"[default mu=0.30 wrap=180 Tload=1000 pos=50%]")
print(f"  beta={beta:.5f} rad  ratio=exp(mu*beta)={R:.4f}")
print(f"  Thold={Thold:.2f} N  Tobs={Tobs:.2f} N  reduce={reduce:.1f}%")

# Known textbook checks: mu=0.3, full turn (360deg=2pi)
print("\n[known: mu=0.3, wrap sweep] ratio=exp(mu*beta)")
for turns, deg in [(0.5,180),(1,360),(1.5,540),(2,720),(3,1080)]:
    b = math.radians(deg); r = ratio(mu, b)
    print(f"  {turns:>4} turn ({deg:>4}deg): ratio={r:8.2f}  Thold(1000N)={1000/r:8.2f}N")
# spot-check article claims: 360->~6.6, 540->~17, 3turns->~290
print(f"  check 360deg ~6.6: {ratio(0.3, 2*math.pi):.3f}")
print(f"  check 540deg ~17:  {ratio(0.3, 3*math.pi):.3f}")
print(f"  check 1080deg(3turn) ~290: {ratio(0.3, 6*math.pi):.3f}")

# Tool howto-example claim: mu=0.35, 2 turns (4pi), Tload=500 -> Thold~33.6, ratio~14.9
b = 4*math.pi; r = ratio(0.35, b)
print(f"\n[howto example mu=0.35 2turn Tload=500] ratio={r:.3f} Thold={500/r:.2f}N (claim 14.9x, 33.6N)")
b3 = 6*math.pi; r3 = ratio(0.35, b3)
print(f"  3turn(6pi): ratio={r3:.3f} Thold={500/r3:.2f}N (claim 57x, 8.7N)")

# radius independence demonstration (conceptual; ratio has no R)
print("\n[radius independence] ratio depends only on mu,beta -> no R term. Confirmed by formula.")
