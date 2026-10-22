# -*- coding: utf-8 -*-
"""Reproduce compton-scattering.html algorithm and cross-check vs closed form."""
import math

LAMBDA_C_PM = 2.4263102387   # electron Compton wavelength, pm
MEC2_KEV = 510.99895         # electron rest energy, keV
HC_KEV_PM = 1239.84193       # hc in keV*pm

def scatter(Ei, thetaDeg, mTarget=1):
    theta = math.radians(thetaDeg)
    lamC = LAMBDA_C_PM / mTarget
    dLam = lamC * (1 - math.cos(theta))
    lamIn = HC_KEV_PM / Ei
    lamF = lamIn + dLam
    Ef = HC_KEV_PM / lamF
    KE = Ei - Ef
    alpha = Ei / MEC2_KEV
    if thetaDeg <= 0.001:
        phiE = 90.0
    elif thetaDeg >= 179.999:
        phiE = 0.0
    else:
        cotHalf = 1/math.tan(theta/2)
        phiE = math.degrees(math.atan(cotHalf/(1+alpha)))
    return dict(lamIn=lamIn, lamF=lamF, dLam=dLam, Ef=Ef, KE=KE, alpha=alpha, phiE=phiE)

print("=== Default E_in=100 keV, theta=90 ===")
r = scatter(100, 90)
print(f"lambda_in={r['lamIn']:.3f} pm  dLambda={r['dLam']:.4f} pm  Ef={r['Ef']:.2f} keV")
print(f"KE_e={r['KE']:.2f} keV  alpha={r['alpha']:.4f}  phi_e={r['phiE']:.2f} deg")

print("\n=== dLambda vs theta (independent of E_in) ===")
for th in [0,45,90,135,180]:
    print(f"theta={th:4d}  dLambda={LAMBDA_C_PM*(1-math.cos(math.radians(th))):.4f} pm")
print("Max at 180:", round(2*LAMBDA_C_PM,4), "pm ; lambda_C at 90:", round(LAMBDA_C_PM,4), "pm")

print("\n=== Cross-check Compton wavelength h/(m_e c) ===")
h = 6.62607015e-34; me = 9.1093837015e-31; c = 2.99792458e8
lamC_SI = h/(me*c)
print("h/(m_e c) =", lamC_SI, "m =", lamC_SI*1e12, "pm")

print("\n=== Energy dependence: Ef and KE/Ein at theta=90 ===")
for Ei in [100, 200, 500, 1000]:
    rr = scatter(Ei, 90)
    print(f"E_in={Ei:5d} keV  Ef={rr['Ef']:7.2f} keV  KE/Ein={rr['KE']/Ei*100:5.1f}%  phi_e={rr['phiE']:.1f} deg")

print("\n=== Compton edge: Cs-137 662 keV, theta=180 ===")
r137 = scatter(662, 180)
print(f"E_in=662 keV theta=180 -> Ef={r137['Ef']:.1f} keV  KE_e(edge)={r137['KE']:.1f} keV")
# closed form compton edge KE = 2 alpha^2/(1+2alpha) * mec2
al = 662/MEC2_KEV
edge = 2*al*al/(1+2*al)*MEC2_KEV
print(f"closed-form Compton edge = {edge:.1f} keV")

print("\n=== Proton target (mTarget=1836) at 90 deg ===")
rp = scatter(100, 90, 1836)
print(f"dLambda={rp['dLam']:.6f} pm = {rp['dLam']*1000:.4f} fm")
