# -*- coding: utf-8 -*-
"""Verify batch6b: z-transform, laplace, nyquist-sampling, quantum-tunneling, wheatstone."""
import math, cmath
def hr(t): print("="*8, t)

# 1) z-transform default LP IIR
hr("z-transform")
import numpy as np
b=np.array([0.0675,0.135,0.0675]); a=np.array([1,-1.143,0.4128])
poles=np.roots(a); zeros=np.roots(b)
print(f"  poles={['%.3f%+.3fj'%(p.real,p.imag) for p in poles]} |p|={[round(abs(p),3) for p in poles]}")
print(f"  zeros={['%.3f'%z.real for z in zeros]}  stable={all(abs(p)<1 for p in poles)} (全極が単位円内)")
w=np.linspace(0,np.pi,513); H=np.polyval(b,np.exp(-1j*w))/np.polyval(a,np.exp(-1j*w))
mag=20*np.log10(np.abs(H)); print(f"  DCgain={mag[0]:.1f}dB peak={mag.max():.1f}dB (低域通過)")

# 2) laplace default e^(-at)
hr("laplace-transform")
a_=1.0
print(f"  e^(-at) a=1: F(s)=1/(s+a), pole at s=-{a_:.0f} (左半面=安定), F(0)=1/a={1/a_:.1f}, f(inf)=0")
print(f"  damped sin e^(-at)sin(wt): poles at -a±jw (a=1,w=2 -> -1±2j)")

# 3) nyquist-sampling
hr("nyquist-sampling")
def alias(f,fs): return abs(f-round(f/fs)*fs)
f,fs,N=600,1000,8
print(f"  f={f} fs={fs}: fN=fs/2={fs/2:.0f}Hz f_alias=|{f}-{round(f/fs)}*{fs}|={alias(f,fs):.0f}Hz "
      f"{'エイリアシング(f>fN)' if f>fs/2 else '正常'} SNR={6.02*N+1.76:.2f}dB")
for ff in (400,600,900,1100): print(f"   f={ff}: f_alias={alias(ff,fs):.0f}Hz {'aliasing' if ff>500 else 'ok'}")

# 4) quantum-tunneling
hr("quantum-tunneling")
me=9.109e-31; eV=1.602e-19; hbar=1.055e-34; nm=1e-9
def tunnel(V0,E,d_nm,m_rel):
    dE=(V0-E)*eV; m=m_rel*me; kappa=math.sqrt(2*m*dE)/hbar; kappa_nm=kappa*nm
    a=d_nm*nm; Twkb=math.exp(-2*kappa*a)
    Texact=1/(1+(V0*V0)/(4*E*(V0-E))*math.sinh(kappa*a)**2)
    return kappa_nm,Twkb,Texact
k,Tw,Te=tunnel(5,3,1.0,1)
print(f"  電子 V0=5 E=3 d=1nm: kappa={k:.2f}/nm  T(WKB)={Tw:.2e}  T(exact)={Te:.2e}")
print(f"  d=0.5nm: T(WKB)={tunnel(5,3,0.5,1)[1]:.2e} (薄い障壁ほど透過大)")
print(f"  陽子(m=1836) d=1nm: T(WKB)={tunnel(5,3,1.0,1836)[1]:.2e} (重い粒子は透過しにくい)")

# 5) wheatstone-bridge
hr("wheatstone-bridge")
def bridge(R1,R2,R3,R4,Vin=5.0):
    Vout=Vin*(R2/(R1+R2)-R4/(R3+R4)); R4bal=R2*R3/R1
    return Vout*1000, Vout/Vin*1000, R4bal, R4-R4bal
vout,sens,bal,dR=bridge(1000,1000,1000,1010)
print(f"  R1=R2=R3=1000 R4=1010 Vin=5: Vout={vout:.2f}mV sens={sens:.2f}mV/V 平衡R4={bal:.0f}Ω dR4={dR:+.0f}Ω")
print(f"  平衡(R4=1000): Vout={bridge(1000,1000,1000,1000)[0]:.2f}mV (R1R4=R2R3で出力0)")
print("done")
