# -*- coding: utf-8 -*-
"""Verify headline numbers for batch2: gyroscope, governor, otto, rankine, brayton, diesel."""
import math
def hr(t): print("="*8, t)

# 1) gyroscope: default rpm=3000,m=0.5,r=10cm,d=10cm,theta=90
hr("gyroscope")
def gyro(rpm,m,r_cm,d_cm,th_deg):
    r=r_cm/100; d=d_cm/100; th=math.radians(th_deg); g=9.81
    om=rpm*2*math.pi/60; I=0.5*m*r*r; L=I*om; tau=m*g*d*math.sin(th)
    omegaP_code=tau/L            # tool's code (theta-dependent)
    omegaP_correct=m*g*d/(I*om)  # standard steady precession (theta-independent)
    return om,I,L,tau,omegaP_code,omegaP_correct
om,I,L,tau,opc,opx=gyro(3000,0.5,10,10,90)
print(f"  default: omega={om:.2f} I={I:.5f} L={L:.4f} tau={tau:.4f} Omega_p(code)={opc:.4f} correct={opx:.4f} rad/s")
print(f"  precession period = {2*math.pi/opc:.3f} s")
for rpm in (1000,6000):
    print(f"  rpm={rpm}: Omega_p={gyro(rpm,0.5,10,10,90)[4]:.4f} rad/s")
print(f"  tilt 45deg(code)={gyro(3000,0.5,10,10,45)[4]:.4f} vs correct(const)={gyro(3000,0.5,10,10,45)[5]:.4f}")

# 2) centrifugal-governor: m=1.5,M=4.0,L=0.20,n=200rpm
hr("centrifugal-governor")
def gov(m,M,L,rpm,g=9.81):
    om=2*math.pi*rpm/60; h=((m+M)/m)*(g/om/om)
    if h>=L: th=0.0
    else: th=math.acos(h/L)
    r=L*math.sin(th); Fc=m*om*om*r
    om_min=math.sqrt((m+M)/m*g/L); rpm_lift=om_min*60/2/math.pi
    return om,h,math.degrees(th),r,Fc,rpm_lift
om,h,th,r,Fc,lift=gov(1.5,4.0,0.20,200)
print(f"  default 200rpm: omega={om:.2f} h={h*1000:.1f}mm theta={th:.1f}deg r={r*1000:.1f}mm Fc={Fc:.1f}N liftoff={lift:.1f}rpm")
for n in (100,150,300,400):
    o,hh,tt,rr,ff,ll=gov(1.5,4.0,0.20,n); print(f"   n={n}: h={hh*1000:.1f}mm theta={tt:.1f}deg r={rr*1000:.1f}mm")

# 3) otto: r=9,gamma=1.4,T1=300,Qin=1500
hr("otto-cycle")
def otto(r,g,T1,Qin,R=0.287):
    cv=R/(g-1); rgm1=r**(g-1); T2=T1*rgm1; T3=T2+Qin/cv; T4=T3/rgm1
    eta=1-1/rgm1; wnet=eta*Qin
    return eta,T2,T3,T4,wnet
eta,T2,T3,T4,w=otto(9,1.4,300,1500)
print(f"  default r=9: eta={eta*100:.2f}% T2={T2:.1f}K T3={T3:.1f}K T4={T4:.1f}K wnet={w:.1f}kJ/kg")
for r in (6,12,16): print(f"   r={r}: eta={otto(r,1.4,300,1500)[0]*100:.2f}%")

# 4) rankine: replicate tool's approximate model
hr("rankine-cycle")
def satWater(P):  # P in MPa
    Tsat=42.6776*P**0.2514+111.9*math.log(P+0.001)+15.0
    T=max(0,min(374,Tsat)); Tk=T+273.15
    hf=4.2*T-0.002*T*T; hfg=2500-2.36*T-0.002*T*T; hg=hf+hfg
    sf=4.2*math.log(Tk/273.15); sfg=hfg/Tk; sg=sf+sfg
    return dict(T=T,hf=hf,hg=hg,hfg=hfg,sf=sf,sg=sg,sfg=sfg)
def superheat(T_C,P):
    sat=satWater(P); dT=T_C-sat["T"]; cp=2.1+0.0025*(T_C+sat["T"])/2
    return dict(h=sat["hg"]+cp*dT, s=sat["sg"]+cp*math.log((T_C+273.15)/(sat["T"]+273.15)))
def isen_exp(s3,h3,Plow):
    sat=satWater(Plow)
    if s3>=sat["sg"]:
        cp=1.9; dh=-cp*(sat["T"]*(s3-sat["sg"])); return max(sat["hg"],h3+dh),1.0
    x=(s3-sat["sf"])/sat["sfg"]; return sat["hf"]+x*sat["hfg"], x
def rankine(Phigh,Plow_kPa,eta_t,eta_p):
    Plow=Plow_kPa/1000; sl=satWater(Plow); sh=satWater(Phigh)
    h1=sl["hf"]; v1=0.001; wp_s=v1*(Phigh-Plow)*1000; wp=wp_s/eta_p; h2=h1+wp
    T3=sh["T"]+20; s3=superheat(T3,Phigh)["s"]; h3=superheat(T3,Phigh)["h"]
    h4s,x4s=isen_exp(s3,h3,Plow); wt=(h3-h4s)*eta_t; h4=h3-wt
    wnet=wt-wp; qin=h3-h2; eta=wnet/qin; wr=wp/wt
    return eta,wnet,qin,wp,wt,wr
eta,wnet,qin,wp,wt,wr=rankine(3.0,10,0.85,0.80)
print(f"  default(3MPa/10kPa): eta={eta*100:.1f}% wnet={wnet:.0f} qin={qin:.0f} pump_w={wp:.2f} turb_w={wt:.0f} work_ratio={wr*100:.2f}%")
print(f"  robust: pump work v*dP = {0.001*(3.0-0.01)*1000:.2f} kJ/kg (tiny vs turbine ~{wt:.0f})")
for Ph in (8.0,15.0,22.0): print(f"   boiler {Ph}MPa: eta={rankine(Ph,10,0.85,0.80)[0]*100:.1f}%")

# 5) brayton: rp=12,gamma=1.4,T1=290,T3=1500
hr("brayton-cycle")
def brayton(rp,g,T1,T3,cp=1.005):
    ex=(g-1)/g; rpex=rp**ex; T2=T1*rpex; T4=T3/rpex; eta=1-1/rpex
    qin=cp*(T3-T2); wnet=qin*eta
    return eta,T2,T4,wnet,qin
eta,T2,T4,w,qin=brayton(12,1.4,290,1500)
print(f"  default rp=12: eta={eta*100:.2f}% T2={T2:.1f}K T4={T4:.1f}K wnet={w:.1f}kJ/kg qin={qin:.1f}")
for rp in (6,20,30): print(f"   rp={rp}: eta={brayton(rp,1.4,290,1500)[0]*100:.2f}%")

# 6) diesel: r=18,rc=2,gamma=1.4
hr("diesel-cycle")
def diesel(r,rc,g,T1=300,P1=100):
    cutoff=1.0 if abs(rc-1)<1e-6 else (rc**g-1)/(g*(rc-1))
    eta=1-(1/r**(g-1))*cutoff
    otto=1-1/r**(g-1)
    T2=T1*r**(g-1); T3=T2*rc; T4=T1*rc**g; P2=P1*r**g
    return eta,otto,T2,T3,T4,P2,cutoff
eta,otto,T2,T3,T4,P2,cf=diesel(18,2,1.4)
print(f"  default r=18,rc=2: eta={eta*100:.1f}% otto={otto*100:.1f}% (diff {(otto-eta)*100:.1f}pp) T2={T2:.0f} T3={T3:.0f} T4={T4:.0f} P2={P2:.0f}kPa cutoffF={cf:.3f}")
for rc in (1.5,3,4): print(f"   rc={rc}: eta={diesel(18,rc,1.4)[0]*100:.1f}%")
print("done")
