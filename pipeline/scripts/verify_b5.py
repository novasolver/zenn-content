# -*- coding: utf-8 -*-
"""Verify batch5: bisection, runge-kutta, numerical-integration, taylor, kalman, perceptron."""
import math
def hr(t): print("="*8, t)

# 1) bisection f=x^3-2x-5, [1,3], tol=1e-6
hr("bisection-method")
def f(x): return x**3-2*x-5
a,b=1.0,3.0; tol=1e-6; print(f"  f(1)={f(1)} f(3)={f(3)} (opposite signs)")
it=0
while b-a>=tol and it<50:
    c=(a+b)/2; it+=1
    if abs(f(c))<tol: break
    if f(a)*f(c)<0: b=c
    else: a=c
c=(a+b)/2
print(f"  root={c:.9f} iters={it} width={b-a:.2e} (theory N>=log2((b0-a0)/tol)={math.log2(2/tol):.1f})")

# 2) runge-kutta dy/dx=-ky
hr("runge-kutta")
k,h,xend,y0=0.5,0.1,4.0,10
n=round(xend/h)
yE=yR=y0
for i in range(n):
    yE=yE+h*(-k*yE)
    k1=h*(-k*yR);k2=h*(-k*(yR+k1/2));k3=h*(-k*(yR+k2/2));k4=h*(-k*(yR+k3))
    yR=yR+(k1+2*k2+2*k3+k4)/6
yex=y0*math.exp(-k*xend)
print(f"  k=0.5 h=0.1 xend=4 y0=10: exact={yex:.4f} Euler={yE:.4f}(err {(yE-yex)/yex*100:.2f}%) RK4={yR:.6f}(err {(yR-yex)/yex*100:.2e}%)")

# 3) numerical-integration sin on [0,1] n=10
hr("numerical-integration")
import math as m
def trap(fn,a,b,n):
    h=(b-a)/n; s=(fn(a)+fn(b))/2
    for i in range(1,n): s+=fn(a+i*h)
    return h*s
def simpson(fn,a,b,n):
    if n%2: n+=1
    h=(b-a)/n; s=fn(a)+fn(b)
    for i in range(1,n): s+=(2 if i%2==0 else 4)*fn(a+i*h)
    return h*s/3
ex=1-math.cos(1)
print(f"  sin [0,1] n=10: exact={ex:.6f} trap={trap(math.sin,0,1,10):.6f}(err {abs(trap(math.sin,0,1,10)-ex):.2e}) simpson={simpson(math.sin,0,1,10):.6f}(err {abs(simpson(math.sin,0,1,10)-ex):.2e})")
for n in (20,40): print(f"   n={n}: trap err={abs(trap(math.sin,0,1,n)-ex):.2e} simpson err={abs(simpson(math.sin,0,1,n)-ex):.2e}")

# 4) taylor sin a=0
hr("taylor-series")
def fact(n):
    r=1
    for i in range(2,n+1): r*=i
    return r
def taylor_sin(x,N):
    base=[0,1,0,-1]; s=0
    for n in range(N+1): s+=base[n%4]/fact(n)*x**n
    return s
x=0.5
for N in (3,5,7):
    ap=taylor_sin(x,N); print(f"  sin(0.5) N={N}: approx={ap:.7f} exact={math.sin(x):.7f} abserr={abs(ap-math.sin(x)):.2e}")

# 5) kalman replicate
hr("kalman-filter")
def seeded(seed):
    s=[seed]
    def r():
        s[0]=(s[0]*9301+49297)%233280; return s[0]/233280
    return r
def kalman(Q,R,P0,freq,noiseAmp,N=80,dt=0.1):
    rnd=seeded(42); xh=0.0; P=P0; trues=[];meas=[];kal=[];gains=[];covs=[]
    spare=[None]
    def gauss():
        if spare[0] is not None:
            v=spare[0];spare[0]=None;return v
        u1=max(rnd(),1e-12);u2=rnd();mag=math.sqrt(-2*math.log(u1))
        spare[0]=mag*math.sin(2*math.pi*u2); return mag*math.cos(2*math.pi*u2)
    for i in range(N):
        t=i*dt; truth=math.sin(2*math.pi*freq*t); z=truth+gauss()*noiseAmp
        xp=xh; Pp=P+Q; K=Pp/(Pp+R); xh=xp+K*(z-xp); P=(1-K)*Pp
        trues.append(truth);meas.append(z);kal.append(xh);gains.append(K);covs.append(P)
    rmseRaw=math.sqrt(sum((meas[i]-trues[i])**2 for i in range(N))/N)
    rmseKal=math.sqrt(sum((kal[i]-trues[i])**2 for i in range(N))/N)
    return rmseRaw,rmseKal,gains[-1],covs[-1]
rr,rk,K,P=kalman(0.01,1.0,1.0,1.0,0.5)
print(f"  Q=0.01 R=1 P0=1 freq=1 noise=0.5: RMSE_raw={rr:.4f} RMSE_filtered={rk:.4f} steadyK={K:.4f} Pfinal={P:.6f}")
print(f"  improvement: {(1-rk/rr)*100:.1f}% RMSE reduction")

# 6) perceptron replicate
hr("perceptron")
def lcg(seed):
    s=[seed&0xFFFFFFFF]
    def r():
        s[0]=(s[0]*1664525+1013904223)&0xFFFFFFFF; return s[0]/4294967296
    return r
def gen():
    rng=lcg(42); sp=[None]
    def g():
        if sp[0] is not None:
            v=sp[0];sp[0]=None;return v
        u1=max(rng(),1e-12);u2=rng();mag=math.sqrt(-2*math.log(u1))
        sp[0]=mag*math.sin(2*math.pi*u2); return mag*math.cos(2*math.pi*u2)
    pts=[]
    for _ in range(10): pts.append((3+0.8*g(),3+0.8*g(),1))
    for _ in range(10): pts.append((-3+0.8*g(),-3+0.8*g(),-1))
    return pts
def sgn(v): return 1 if v>=0 else -1
data=gen(); eta=0.1; w1,w2,b=0.5,0.5,0.0; conv=20
for ep in range(1,21):
    errs=0
    for x1,x2,t in data:
        y=sgn(w1*x1+w2*x2+b)
        if y!=t:
            d=t-y; w1+=eta*d*x1; w2+=eta*d*x2; b+=eta*d; errs+=1
    if errs==0: conv=ep; break
correct=sum(1 for x1,x2,t in data if sgn(w1*x1+w2*x2+b)==t)
print(f"  eta=0.1 w=(0.5,0.5) b=0: converged epoch {conv}, acc={correct/len(data)*100:.1f}%, w=({w1:.2f},{w2:.2f}) b={b:.2f}")
print("done")
