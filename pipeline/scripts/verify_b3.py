# -*- coding: utf-8 -*-
"""Verify batch3: entropy-mixing, van-der-waals, maxwell-boltzmann, stefan-boltzmann, fin, acoustic-beats."""
import math
def hr(t): print("="*8, t)

# 1) entropy-mixing
hr("entropy-mixing")
R=8.314
def dSmix(n,xs,T):
    s=sum(x*math.log(x) for x in xs if x>0)
    dS=-n*R*s; return dS, -T*dS/1000, n*R*math.log(len(xs))
dS,dG,dSmax=dSmix(1.0,[0.5,0.3,0.2],298)
print(f"  n=1 x=[.5,.3,.2] T=298: dS={dS:.2f} J/K dG={dG:.2f} kJ dSmax(ln3)={dSmax:.2f} ratio={dS/dSmax*100:.1f}%")
print(f"  equimolar [1/3]*3: dS={dSmix(1,[1/3]*3,298)[0]:.2f} (=dSmax)")
print(f"  binary [.5,.5]: dS={dSmix(1,[0.5,0.5],298)[0]:.2f} J/K (=nR ln2={R*math.log(2):.2f})")

# 2) van-der-waals N2
hr("van-der-waals")
Rg=0.08206
def solveVm(P,T,a,b):
    V=Rg*T/P
    for _ in range(60):
        f=(P+a/V/V)*(V-b)-Rg*T; fp=(P+a/V/V)-(2*a/V**3)*(V-b)
        if abs(fp)<1e-14: break
        dV=f/fp; V-=dV
        if abs(dV)<1e-10: break
    return V
T,P,a,b=300,50.0,1.35,0.039
Vm=solveVm(P,T,a,b); Z=P*Vm/(Rg*T); Tc=8*a/(27*Rg*b); Pc=a/(27*b*b); Vc=3*b
print(f"  N2 T=300 P=50atm: Vm={Vm:.3f} L/mol Z={Z:.3f} Tc={Tc:.1f}K Pc={Pc:.1f}atm Vc={Vc:.3f}L/mol")
# ideal vs vdw molar volume
print(f"  ideal Vm=RT/P={Rg*T/P:.3f} L/mol (vdw {Vm:.3f}, Z={Z:.3f}<1 -> attraction dominates)")
for a_,b_,nm in [(0.034,0.024,"He"),(3.59,0.0427,"CO2")]:
    print(f"  {nm}: Tc={8*a_/(27*Rg*b_):.1f}K Pc={a_/(27*b_*b_):.1f}atm")

# 3) maxwell-boltzmann
hr("maxwell-boltzmann")
kB=1.380649e-23; NA=6.02214076e23
def speeds(T,Mg):
    m=Mg*1e-3/NA
    return math.sqrt(2*kB*T/m),math.sqrt(8*kB*T/(math.pi*m)),math.sqrt(3*kB*T/m)
vp,vm,vr=speeds(300,28)
print(f"  N2 T=300: vp={vp:.1f} vmean={vm:.1f} vrms={vr:.1f} m/s  ratio {vp/vp:.3f}:{vm/vp:.3f}:{vr/vp:.3f}")
for T in (600,):
    vp2=speeds(T,28)[0]; print(f"  T=600: vp={vp2:.1f} (=sqrt2 x 300K? {vp*math.sqrt(2):.1f})")
print(f"  H2 T=300: vp={speeds(300,2)[0]:.1f} m/s (light->fast)")

# 4) stefan-boltzmann
hr("stefan-boltzmann")
SIG=5.670374419e-8
def sb(T,eps=1.0,A=1.0,Tenv=300):
    E=eps*SIG*T**4; return E, E*A, 2898/T, eps*SIG*A*(T**4-Tenv**4)
E,Q,lam,Qnet=sb(1000)
print(f"  T=1000 eps=1 A=1: E={E:.1f} W/m2 ({E/1000:.1f}kW) lam_max={lam:.3f}um Qnet(Tenv=300)={Qnet:.1f}W")
print(f"  double T->2000: E={sb(2000)[0]:.0f} (x{sb(2000)[0]/E:.0f} = 2^4=16)")

# 5) fin-heat
hr("fin-heat-transfer")
def fin(L,t,W,k,h,Tb,Tinf,N):
    L*=1e-3;t*=1e-3;W*=1e-3; P=2*(W+t); A=W*t
    m=math.sqrt(h*P/(k*A)); mL=m*L; eta=math.tanh(mL)/mL
    th=Tb-Tinf; As=P*L; Qs=eta*h*As*th; Qnf=h*A*th
    return m,mL,eta,Qs,Qs/Qnf,Tinf+th/math.cosh(mL),N*Qs
m,mL,eta,Qs,enh,Ttip,Qtot=fin(50,3,50,200,25,80,25,10)
print(f"  Al default: m={m:.2f}/m mL={mL:.3f} eta={eta*100:.1f}% Qsingle={Qs:.2f}W Ttip={Ttip:.1f}C enhance={enh:.1f}x Qtot={Qtot:.1f}W")
print(f"  Cu(k=400): eta={fin(50,3,50,400,25,80,25,10)[2]*100:.1f}%  Steel(k=50): eta={fin(50,3,50,50,25,80,25,10)[2]*100:.1f}%")

# 6) acoustic-beats
hr("acoustic-beats")
def beats(f1,f2,A1,A2):
    fb=abs(f1-f2); fa=(f1+f2)/2; Tb=1000/fb if fb>0 else float('inf')
    return fb,fa,Tb,A1+A2,abs(A1-A2)
fb,fa,Tb,Amax,Amin=beats(440,444,0.5,0.5)
print(f"  440&444: fbeat={fb:.1f}Hz favg={fa:.0f}Hz Tbeat={Tb:.0f}ms Amax={Amax:.2f} Amin={Amin:.2f}")
print(f"  envelope cos arg uses Df/2={fb/2:.1f}Hz but |cos| period -> audible beat = Df = {fb:.1f}Hz")
print("done")
