# -*- coding: utf-8 -*-
"""Verify batch6a: acoustic-resonance, helmholtz, neural-net, autocorrelation, high-pass, root-locus."""
import math, random
def hr(t): print("="*8, t)

# 1) acoustic-resonance
hr("acoustic-resonance")
def c_of(T): return 331.3*math.sqrt((T+273.15)/273.15)
c=c_of(20); L=0.60
print(f"  T=20C: c={c:.1f} m/s")
print(f"  open L=0.6: f_n =", [round(n*c/(2*L),1) for n in range(1,5)])
print(f"  closed L=0.6: f_n =", [round((2*n-1)*c/(4*L),1) for n in range(1,5)])
print(f"  open f1={c/(2*L):.1f}Hz closed f1={c/(4*L):.1f}Hz (closed=open/2)")

# 2) helmholtz
hr("helmholtz-resonator")
def helm(V_L,dn_mm,L_mm,c=343):
    V=V_L*1e-3; rn=(dn_mm/2)/1000; A=math.pi*rn*rn; Leff=L_mm/1000+1.7*rn
    return c/(2*math.pi)*math.sqrt(A/(V*Leff)), Leff
f,Leff=helm(1.0,20,50)
print(f"  V=1L dn=20mm L=50mm c=343: f={f:.1f}Hz Leff={Leff*1000:.1f}mm lambda={343/f:.2f}m")
print(f"  V=0.5L: f={helm(0.5,20,50)[0]:.1f}Hz (smaller V -> higher f)")

# 3) neural-net XOR (seeded representative run)
hr("neural-network")
random.seed(42)
def sig(x): return 1/(1+math.exp(-x))
# [2,4,1] single hidden for brevity representative
def init(rows,cols): return [[random.uniform(-0.5,0.5) for _ in range(cols)] for _ in range(rows)]
W1=init(4,2);b1=[random.uniform(-0.1,0.1) for _ in range(4)];W2=init(1,4);b2=[random.uniform(-0.1,0.1)]
X=[[0,0],[0,1],[1,0],[1,1]];Y=[0,1,1,0]
def fwd(x):
    h=[sig(sum(W1[i][j]*x[j] for j in range(2))+b1[i]) for i in range(4)]
    o=sig(sum(W2[0][i]*h[i] for i in range(4))+b2[0]); return h,o
def loss():
    return sum(0.5*(fwd(x)[1]-y)**2 for x,y in zip(X,Y))/4
lr=0.5
losses=[loss()]
for ep in range(3000):
    for x,y in zip(X,Y):
        h,o=fwd(x); d2=(o-y)*o*(1-o)
        d1=[ (W2[0][i]*d2)*h[i]*(1-h[i]) for i in range(4)]
        for i in range(4): W2[0][i]-=lr*d2*h[i]
        b2[0]-=lr*d2
        for i in range(4):
            for j in range(2): W1[i][j]-=lr*d1[i]*x[j]
            b1[i]-=lr*d1[i]
    if ep in (0,99,499,999,2999): losses.append(loss())
acc=sum(1 for x,y in zip(X,Y) if round(fwd(x)[1])==y)/4*100
print(f"  XOR [2,4,1] sigmoid lr=0.5: loss {losses[0]:.4f}->{loss():.4f}, acc={acc:.0f}% (XORは線形分離不可、隠れ層で解ける)")

# 4) autocorrelation replicate LCG
hr("autocorrelation")
def lcg(seed):
    s=[seed&0xFFFFFFFF]
    def r():
        s[0]=(s[0]*1103515245+12345)&0xFFFFFFFF; return s[0]/4294967296
    return r
def acf_test(A,f0,sigma,N,seed=42):
    rng=lcg(seed); sp=[None]
    def g():
        if sp[0] is not None:
            v=sp[0];sp[0]=None;return v
        u1=max(rng(),1e-12);u2=rng();mag=math.sqrt(-2*math.log(u1))
        sp[0]=mag*math.sin(2*math.pi*u2);return mag*math.cos(2*math.pi*u2)
    x=[A*math.sin(2*math.pi*f0*n)+sigma*g() for n in range(N)]
    K=N//2; R=[sum(x[n]*x[n+k] for n in range(N-k))/N for k in range(K+1)]
    rho=[R[k]/R[0] for k in range(K+1)]
    # find first peak after first negative crossing
    kStart=1
    for k in range(1,K+1):
        if rho[k]<0: kStart=k;break
    peakK=-1;peakV=-9
    for k in range(max(kStart,1),K):
        if rho[k]>rho[k-1] and rho[k]>=rho[k+1] and rho[k]>peakV: peakV=rho[k];peakK=k
    return peakK,R[0],(A/sigma)**2
pk,R0,snr=acf_test(1.0,0.05,0.5,512)
print(f"  A=1 f0=0.05 sigma=0.5 N=512: detected period={pk} samples (true 1/f0={1/0.05:.0f}) SNR={snr:.1f}={10*math.log10(snr):.1f}dB R(0)={R0:.3f}")

# 5) high-pass filter
hr("high-pass-filter")
def hp(R,C,f):
    tau=R*C; fc=1/(2*math.pi*tau); r=f/fc
    return fc,20*math.log10(r/math.sqrt(1+r*r)),90-math.degrees(math.atan(r)),tau
fc,g,ph,tau=hp(1000,100e-9,1592)
print(f"  R=1k C=100nF f=1592: fc={fc:.1f}Hz gain={g:.2f}dB phase={ph:.1f}deg tau={tau*1e6:.0f}us")
for f in (159,15920): print(f"   f={f}: gain={hp(1000,100e-9,f)[1]:.2f}dB (1decade={'低域-20dB/dec' if f<fc else '通過域'})")

# 6) root-locus p2 preset
hr("root-locus")
def cl2(p1,p2,K):
    a=p1+p2; b=p1*p2+K; disc=a*a-4*b
    if disc>=0: return (-a+math.sqrt(disc))/2,0,(-a-math.sqrt(disc))/2,0
    return -a/2,math.sqrt(-disc)/2,-a/2,-math.sqrt(-disc)/2
re,im,_,_=cl2(-1,-3,5)
wn=math.sqrt(re*re+im*im); zeta=-re/wn; os=math.exp(-math.pi*zeta/math.sqrt(1-zeta*zeta))*100; ts=4/(-re)
print(f"  p2 poles(-1,-3) K=5: closed pole={re:.2f}+{im:.2f}j wn={wn:.3f} zeta={zeta:.3f} OS={os:.2f}% Ts={ts:.2f}s")
# p3 Kcrit
p=[-1,-2,-4]; a1=-(sum(p)); a2=p[0]*p[1]+p[0]*p[2]+p[1]*p[2]; a3=-p[0]*p[1]*p[2]
print(f"  p3 poles(-1,-2,-4): Kcrit=a1*a2-a3={a1*a2-a3:.0f} (これ以上で不安定)")
print("done")
