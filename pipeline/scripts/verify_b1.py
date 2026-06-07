# -*- coding: utf-8 -*-
"""Verify headline numbers for batch1 tools. ASCII-only prints (cp932-safe)."""
import math, numpy as np

def hr(t): print("="*8, t)

# 1) simple-pendulum: T=2pi sqrt(L/g); large-angle via RK4; energy conservation
hr("simple-pendulum")
def Tlin(L,g): return 2*math.pi*math.sqrt(L/g)
def pend_period_rk4(L,g,th0_deg,gamma=0):
    th=math.radians(th0_deg); om=0.0; dt=1e-4; t=0.0
    def deriv(th,om): return om, -(g/L)*math.sin(th)-gamma*om
    # integrate until theta crosses zero going same direction twice (one full period)
    prev=th; crossings=0; t_cross=[]
    while t<20:
        k1=deriv(th,om); th2=th+dt/2*k1[0]; om2=om+dt/2*k1[1]
        k2=deriv(th2,om2); th3=th+dt/2*k2[0]; om3=om+dt/2*k2[1]
        k3=deriv(th3,om3); th4=th+dt*k3[0]; om4=om+dt*k3[1]
        k4=deriv(th4,om4)
        thn=th+dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        omn=om+dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if th>0 and thn<=0:  # downward zero crossing
            t_cross.append(t);
            if len(t_cross)>=2: break
        th,om=thn,omn; t+=dt
    if len(t_cross)>=2: return t_cross[1]-t_cross[0]
    return float('nan')
for th0 in (10,30,120):
    print(f"  L=1 g=9.81 th0={th0}: Tlin={Tlin(1,9.81):.3f}s  Tactual={pend_period_rk4(1,9.81,th0):.3f}s")
# elliptic-integral exact for 30 and 120
def Texact(L,g,th0_deg):
    from scipy.special import ellipk
    k=math.sin(math.radians(th0_deg)/2)
    return 4*math.sqrt(L/g)*ellipk(k*k)
try:
    for th0 in (30,120): print(f"  exact(K) th0={th0}: {Texact(1,9.81,th0):.3f}s")
except Exception as e: print("  scipy ellipk NA", e)
print(f"  moon g=1.62 L=1: Tlin={Tlin(1,1.62):.3f}s")
# energy ratio over a period (gamma=0) should stay ~1
print(f"  ratio of large/small period (120 vs lin) = {pend_period_rk4(1,9.81,120)/Tlin(1,9.81):.3f}")

# 2) orbital-mechanics
hr("orbital-mechanics")
MU=3.986e14; RE=6371e3
def orbit(a_km,e):
    a=a_km*1000; T=2*math.pi*math.sqrt(a**3/MU)
    rp=a*(1-e); ra=a*(1+e)
    vp=math.sqrt(MU*(2/rp-1/a)); va=math.sqrt(MU*(2/ra-1/a))
    return T,rp,ra,vp,va
for name,a,e in [("default(BUG)",8000,0.30),("GPS",26560,0.01),("ISS",6778,0.001),("GEO",42164,0.0001),("Molniya",12000,0.72)]:
    T,rp,ra,vp,va=orbit(a,e)
    print(f"  {name:13} a={a} e={e}: T={T/3600:.3f}h rp_alt={(rp-RE)/1000:.0f}km ra_alt={(ra-RE)/1000:.0f}km vp={vp/1000:.3f} va={va/1000:.3f} km/s")

# 3) hohmann LEO400->GEO35800 (km units, mu=398600)
hr("hohmann-transfer")
def hohmann(h1,h2,mu=398600,R=6378):
    r1=R+h1; r2=R+h2; rs=min(r1,r2); rl=max(r1,r2)
    v1c=math.sqrt(mu/rs); v2c=math.sqrt(mu/rl)
    dv1=v1c*(math.sqrt(2*rl/(rs+rl))-1); dv2=v2c*(1-math.sqrt(2*rs/(rs+rl)))
    a_tx=(rs+rl)/2; t_tx=math.pi*math.sqrt(a_tx**3/mu)
    return dv1,dv2,dv1+dv2,t_tx
dv1,dv2,dvt,t=hohmann(400,35800)
print(f"  LEO400->GEO35800: dv1={dv1:.3f} dv2={dv2:.3f} total={dvt:.3f} km/s  t_tx={t/3600:.2f}h")
# peak of dv_total/v1c vs ratio R
Rs=np.linspace(1.01,100,20000)
d=np.sqrt(2*Rs/(1+Rs))-1 + np.sqrt(1/Rs)*(1-np.sqrt(2/(1+Rs)))
print(f"  peak ratio R*={Rs[np.argmax(d)]:.3f}  max dv/v1c={d.max():.4f}")

# 4) escape-velocity
hr("escape-velocity")
G=6.674e-11; c=2.998e8; Me=5.972e24; Re=6.371e6
def ve(mm,rm): M=mm*Me;R=rm*Re; return math.sqrt(2*G*M/R)/1000
def rs(mm): return 2*G*(mm*Me)/c**2
for n,mm,rm in [("moon",0.0123,0.2727),("mars",0.107,0.532),("earth",1,1),("jupiter",317.8,11.21),("sun",333000,109.2),("neutron",466200,0.00157)]:
    v=ve(mm,rm); print(f"  {n:8} ve={v:.2f} km/s vo={v/math.sqrt(2):.2f} ve/c={v*1000/c:.4f} rs={rs(mm):.3e}m")

# 5) coriolis: straight inertial line rotated -> deflection angle = Omega*t
hr("coriolis-effect")
def coriolis_deflect(omega,speed,angle_deg,sign,t):
    rad=math.radians(angle_deg); ivx=speed*math.cos(rad); ivy=-speed*math.sin(rad)
    dt=0.001; ix=iy=0; fa=0; pts=[]
    n=int(t/dt)
    for _ in range(n):
        ix+=ivx*dt; iy+=ivy*dt; fa+=omega*dt
        ct=math.cos(-sign*fa); st=math.sin(-sign*fa)
        rx=ix*ct-iy*st; ry=ix*st+iy*ct; pts.append((rx,ry))
    a0=math.atan2(iy,ix)  # inertial dir
    a1=math.atan2(pts[-1][1],pts[-1][0])
    d=math.degrees(a1-a0)
    while d>180:d-=360
    while d<-180:d+=360
    return d, math.degrees(omega*t)
d,exp=coriolis_deflect(1.0,80,0,1,2.0)
print(f"  omega=1,t=2s: rotating-frame deflection={d:.1f}deg  (=Omega*t={exp:.1f}deg, sign north=CW)")
d2,_=coriolis_deflect(1.0,80,0,-1,2.0); print(f"  south sign: deflection={d2:.1f}deg (opposite)")

# 6) foucault
hr("foucault-pendulum")
SID=86164.1; OE=2*math.pi/SID
def fou(lat,L=20,g=9.81,tH=6):
    Tosc=2*math.pi*math.sqrt(L/g); om=OE*math.sin(math.radians(abs(lat)))
    Tpre=2*math.pi/om if om>0 else float('inf')
    degph=math.degrees(om)*3600; dth=degph*tH
    return Tosc,Tpre,degph,dth
print(f"  OMEGA_earth={OE:.4e} rad/s")
for lat in (35,90,45,0):
    Tosc,Tpre,degph,dth=fou(lat)
    tp = f"{Tpre/3600:.2f}h" if math.isfinite(Tpre) else "inf"
    print(f"  lat={lat:3}: Tosc={Tosc:.3f}s Omega_pre={degph:.2f}deg/h Tpre={tp} dth(6h)={dth:.2f}deg")
print("done")
