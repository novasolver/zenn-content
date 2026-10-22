# -*- coding: utf-8 -*-
"""Verify batch4: projectile, beam-deflection, mohr-circle, euler-buckling,
reynolds-number, snells-law."""
import numpy as np
def hr(t): print("\n" + "=" * 56 + f"\n{t}\n" + "=" * 56)

hr("PROJECTILE  R = v0^2 sin(2theta)/g")
def proj(v0, th, g=9.81, h0=0):
    thr = np.radians(th)
    if h0 == 0:
        R = v0*v0*np.sin(2*thr)/g; H = v0*v0*np.sin(thr)**2/(2*g); T = 2*v0*np.sin(thr)/g
    else:
        T = (v0*np.sin(thr)+np.sqrt((v0*np.sin(thr))**2+2*g*h0))/g
        R = v0*np.cos(thr)*T; H = h0 + v0*v0*np.sin(thr)**2/(2*g)
    return R, H, T
for v0, th, g in [(30,45,9.81),(30,45,1.62),(30,45,3.72),(50,30,9.81)]:
    R,H,T = proj(v0,th,g)
    print(f"  v0={v0} th={th} g={g}: R={R:.1f}m H={H:.1f}m T={T:.2f}s")
print(f"  optimal angle (h0=0) = 45deg; range max")

hr("BEAM DEFLECTION")
E=200e9; I=100e-8  # 100 cm^4 = 100e-8 m^4
L=2.0; q=10e3      # 10 kN/m
# ss UDL center: w=q*x*(L^3-2Lx^2+x^3)/(24EI), x=L/2
x=L/2; w_udl=q*x*(L**3-2*L*x*x+x**3)/(24*E*I)
print(f"  ss+UDL E=200GPa I=100cm^4 L=2 q=10kN/m: delta_center={w_udl*1000:.3f}mm (5qL^4/384EI={5*q*L**4/(384*E*I)*1000:.3f})")
P=10e3  # 10kN point load center
w_pt=P*L**3/(48*E*I)
print(f"  ss+point P=10kN center: delta=PL^3/48EI={w_pt*1000:.3f}mm")
w_cant=q*L**4/(8*E*I)
print(f"  cantilever+UDL: delta_tip=qL^4/8EI={w_cant*1000:.3f}mm; cant+point PL^3/3EI={P*L**3/(3*E*I)*1000:.3f}mm")

hr("MOHR CIRCLE")
sx,sy,txy = 80,-40,60
C=(sx+sy)/2; R=np.sqrt(((sx-sy)/2)**2+txy**2)
s1,s2=C+R,C-R; thp=0.5*np.degrees(np.arctan2(2*txy,sx-sy))
print(f"  sx={sx} sy={sy} txy={txy}: C={C} R={R:.2f} s1={s1:.2f} s2={s2:.2f} tmax={R:.2f} theta_p={thp:.1f}deg")

hr("EULER BUCKLING  Pcr = pi^2 EI/(KL)^2")
E=200e9
for d,L,K in [(0.05,2.0,1.0),(0.089,3.5,1.0)]:
    I=np.pi*d**4/64; A=np.pi*d*d/4; r=np.sqrt(I/A)
    Pcr=np.pi**2*E*I/(K*L)**2; slend=K*L/r
    print(f"  solid d={d*1000:.0f}mm L={L} K={K}: I={I:.3e} Pcr={Pcr/1000:.1f}kN slend KL/r={slend:.0f}")
# tube 89mm t=5.5
D,t=0.089,0.0055; di=D-2*t; I=np.pi*(D**4-di**4)/64; A=np.pi*(D*D-di*di)/4
Pcr=np.pi**2*E*I/(1*3.5)**2; r=np.sqrt(I/A)
print(f"  tube D=89 t=5.5 L=3.5 K=1: I={I:.3e} A={A:.3e} Pcr={Pcr/1000:.0f}kN KL/r={3.5/r:.0f} (FAQ ~238kN)")
print(f"  K factors: pinned-pinned 1.0, fixed-free 2.0, fixed-fixed 0.5, fixed-pinned 0.7")

hr("REYNOLDS NUMBER  Re = rho U L / mu")
fluids={'water':(998.2,1.002e-3),'air':(1.204,1.825e-5),'oil':(870,4.6e-2)}
for f,(rho,mu) in fluids.items():
    Re=rho*1.0*0.025/mu
    print(f"  {f}: U=1 D=25mm -> Re={Re:.0f} (nu={mu/rho:.2e})")
print(f"  pipe thresholds: laminar<2300, transition 2300-4000, turbulent>4000")
print(f"  water D=25mm U=1.5: Re={998.2*1.5*0.025/1.002e-3:.0f}")

hr("SNELL'S LAW  n1 sin th1 = n2 sin th2")
for n1,n2,th1 in [(1.0,1.5,40),(1.33,1.0,40),(2.42,1.0,30)]:
    s2=n1/n2*np.sin(np.radians(th1))
    if s2>1: th2='TIR';
    else: th2=f"{np.degrees(np.arcsin(s2)):.1f}deg"
    thc=np.degrees(np.arcsin(n2/n1)) if n1>n2 else None
    print(f"  n1={n1} n2={n2} th1={th1}: th2={th2}  crit={f'{thc:.1f}deg' if thc else '—'}")
print("DONE.")
