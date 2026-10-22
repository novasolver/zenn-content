# -*- coding: utf-8 -*-
"""Verify batch4: normal, binomial, markov, buffon, gradient-descent, newton-raphson."""
import math
def hr(t): print("="*8, t)

# 1) normal-distribution
hr("normal-distribution")
def erf(x):
    a1,a2,a3,a4,a5,p=0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429,0.3275911
    s=-1 if x<0 else 1; x=abs(x); t=1/(1+p*x)
    y=1-(((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*math.exp(-x*x); return s*y
def phi(x,mu,sig): return 0.5*(1+erf((x-mu)/(sig*math.sqrt(2))))
print(f"  mu=0 sig=1: P(X<-1)={phi(-1,0,1)*100:.3f}%  z(-1)={(-1-0)/1:.3f}")
print(f"  +-1sig={(phi(1,0,1)-phi(-1,0,1))*100:.2f}% +-2sig={(phi(2,0,1)-phi(-2,0,1))*100:.2f}% +-3sig={(phi(3,0,1)-phi(-3,0,1))*100:.2f}%")
print(f"  IQ mu=100 sig=15: P(115<X<130)={(phi(130,100,15)-phi(115,100,15))*100:.2f}%")

# 2) binomial
hr("binomial-distribution")
def logfact(n):
    s=0.0
    for i in range(2,n+1): s+=math.log(i)
    return s
def binpmf(n,k,p):
    if k<0 or k>n: return 0
    return math.exp(logfact(n)-logfact(k)-logfact(n-k)+k*math.log(p)+(n-k)*math.log(1-p))
n,p=20,0.30
mean=n*p; var=n*p*(1-p); sd=math.sqrt(var); skew=(1-2*p)/sd; mode=math.floor((n+1)*p)
print(f"  n=20 p=0.3: mean={mean:.3f} sd={sd:.3f} var={var:.3f} skew={skew:.4f} mode={mode}")
print(f"  P(X=6)={binpmf(20,6,0.3):.4f}  P(X<=6)={sum(binpmf(20,i,0.3) for i in range(7)):.4f}")
print(f"  coin n=20 p=0.5 P(X=10)={binpmf(20,10,0.5):.4f}")

# 3) markov
hr("markov-chain")
p,q=0.30,0.40
pi1=q/(p+q); pi2=p/(p+q); lam=1-p-q
def P1(t): return pi1+(1.0-pi1)*lam**t
tmix=math.log(0.01)/math.log(abs(lam))
print(f"  p=0.3 q=0.4: pi1={pi1:.4f} pi2={pi2:.4f} lambda={lam:.3f} P1(10)={P1(10):.4f} tmix(99%)={tmix:.2f}")
print(f"  P1(0..5): {[round(P1(t),4) for t in range(6)]}")

# 4) buffon-needle LCG exact
hr("buffon-needle")
def lcg(seed):
    st=seed&0xFFFFFFFF or 1
    while True:
        st=(st*1664525+1013904223)&0xFFFFFFFF; yield st/4294967296
def buffon(N,L,d,seed):
    g=lcg(seed); m=0
    for _ in range(N):
        y=next(g)*(d/2); th=next(g)*math.pi/2
        if y<=(L/2)*math.sin(th): m+=1
    pihat=2*L*N/(d*m) if m>0 else float('nan')
    return m,m/N,pihat,abs(pihat-math.pi)/math.pi*100
m,ph,pihat,err=buffon(5000,5.0,10.0,42)
print(f"  N=5000 L=5 d=10 seed=42: m={m} m/N={ph:.4f} pi_hat={pihat:.4f} err={err:.2f}% (theory P=2L/pid={2*5/(math.pi*10):.4f})")
m2,_,pi2,e2=buffon(100000,5.0,10.0,42); print(f"  N=100000: pi_hat={pi2:.4f} err={e2:.2f}%")

# 5) gradient-descent (bowl, adam)
hr("gradient-descent")
def loss(x,y): return x*x+y*y
def grad(x,y,eps=1e-5):
    return (loss(x+eps,y)-loss(x-eps,y))/(2*eps),(loss(x,y+eps)-loss(x,y-eps))/(2*eps)
def adam(steps,lr=0.01,b1=0.9,b2=0.999,eps=1e-8):
    px,py=-2.52,2.52; m1=m2=v1=v2=0.0
    for t in range(1,steps+1):
        gx,gy=grad(px,py)
        m1=b1*m1+(1-b1)*gx; m2=b1*m2+(1-b1)*gy
        v1=b2*v1+(1-b2)*gx*gx; v2=b2*v2+(1-b2)*gy*gy
        m1h=m1/(1-b1**t); m2h=m2/(1-b1**t); v1h=v1/(1-b2**t); v2h=v2/(1-b2**t)
        px-=lr*m1h/(math.sqrt(v1h)+eps); py-=lr*m2h/(math.sqrt(v2h)+eps)
    return px,py,loss(px,py)
for st in (100,300,500):
    px,py,l=adam(st); print(f"  adam bowl {st} steps: ({px:.4f},{py:.4f}) loss={l:.3e}")

# 6) newton-raphson
hr("newton-raphson")
def f(x): return x**3-2*x-5
def fp(x): return 3*x*x-2
x=2.0; tol=1e-6
for n in range(20):
    fn=f(x)
    if abs(fn)<tol: print(f"  converged n={n} x={x:.9f} |f|={abs(fn):.2e}"); break
    x=x-fn/fp(x); print(f"  n={n+1}: x={x:.9f} f={f(x):.2e}")
print("done")
