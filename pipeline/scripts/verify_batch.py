# -*- coding: utf-8 -*-
"""Numerical verification for batch: newtons-cradle, boids, karman, pipe-flow.
Reproduces each tool's exact JS logic and prints the numbers cited in articles.
No figures here -- just the measured values (RECIPE STEP 2)."""
import numpy as np

np.random.seed(7)

def hr(t): print("\n" + "=" * 60 + f"\n{t}\n" + "=" * 60)

# ===================================================================
hr("1) NEWTON'S CRADLE")
# Pendulum period T = 2*pi*sqrt(L/g)
for L, g in [(1.0, 9.81), (1.5, 9.8), (2.0, 9.81)]:
    T = 2 * np.pi * np.sqrt(L / g)
    print(f"  L={L} g={g} -> T = {T:.3f} s")

# Energy of one ball pulled to angle th0 (PE at release, m=1)
m, g, L = 1.0, 9.81, 1.0
for deg in [25, 40, 45 * 0.45 / 0.45]:
    th = np.radians(deg)
    pe = m * g * L * (1 - np.cos(th))
    v_bottom = np.sqrt(2 * g * L * (1 - np.cos(th)))  # energy conservation
    print(f"  pull {deg:.0f} deg: PE=mgL(1-cos)= {pe:.3f} J ; v at bottom={v_bottom:.3f} m/s")

# preset(2/3): angle = -pi*0.45
th = np.pi * 0.45
print(f"  preset angle 0.45*pi = {np.degrees(th):.1f} deg -> PE(1 ball)= {m*g*L*(1-np.cos(th)):.3f} J")

print("\n  -- COLLISION RULE CHECK (equal mass, restitution e) --")
def correct_collision(v1, v2, e):
    v1p = ((1 - e) / 2) * v1 + ((1 + e) / 2) * v2
    v2p = ((1 + e) / 2) * v1 + ((1 - e) / 2) * v2
    return v1p, v2p
def tool_collision(v1, v2, e):  # from drawFrame step(): balls[i].omega=(e*v2+(1-e)*v1/2)
    v1p = e * v2 + (1 - e) * v1 / 2
    v2p = e * v1 + (1 - e) * v2 / 2
    return v1p, v2p
def theory_box(v1, v2, e):  # theory-box claims v1'=e*v2, v2'=e*v1
    return e * v2, e * v1
v1, v2 = 1.0, 0.0
for e in [1.0, 0.98, 0.9, 0.8]:
    c1, c2 = correct_collision(v1, v2, e)
    t1, t2 = tool_collision(v1, v2, e)
    b1, b2 = theory_box(v1, v2, e)
    print(f"  e={e}: correct sum(p)={c1+c2:.3f} (should=1.000) | tool sum={t1+t2:.3f} | theorybox sum={b1+b2:.3f}")
print("  => tool & theory-box DO NOT conserve momentum for e<1 (sum p should stay 1.000)")
print(f"  e=0.9: tool gives v2'={tool_collision(1,0,0.9)[1]:.3f} vs correct {correct_collision(1,0,0.9)[1]:.3f}")

# ===================================================================
hr("2) BOIDS (replicate exact JS rules, deterministic)")
W, H = 600.0, 520.0
def run_boids(n, maxSpeed, visualRange, sw, aw, cw, steps=900, seed=7):
    rng = np.random.RandomState(seed)
    ang = rng.rand(n) * 2 * np.pi
    spd = (rng.rand(n) * 0.5 + 0.5) * maxSpeed
    x = rng.rand(n) * W; y = rng.rand(n) * H
    vx = np.cos(ang) * spd; vy = np.sin(ang) * spd
    sepRange = visualRange * 0.4
    r2 = visualRange ** 2; sr2 = sepRange ** 2; maxForce = 0.3
    for _ in range(steps):
        nx = np.zeros(n); ny = np.zeros(n)
        for i in range(n):
            sx = sy = ax = ay = cx = cy = 0.0; nc = 0
            for j in range(n):
                if i == j: continue
                dx = x[j] - x[i]; dy = y[j] - y[i]
                d2 = dx * dx + dy * dy
                if d2 > r2: continue
                if 0 < d2 < sr2:
                    d = np.sqrt(d2); sx -= dx / d * (sepRange / d); sy -= dy / d * (sepRange / d)
                ax += vx[j]; ay += vy[j]; cx += x[j]; cy += y[j]; nc += 1
            fx = fy = 0.0
            if nc > 0:
                fx += sx * sw; fy += sy * sw
                fx += (ax / nc - vx[i]) * aw * 0.1; fy += (ay / nc - vy[i]) * aw * 0.1
                fx += (cx / nc - x[i]) * cw * 0.002; fy += (cy / nc - y[i]) * cw * 0.002
            fm = np.hypot(fx, fy)
            if fm > maxForce: fx = fx / fm * maxForce; fy = fy / fm * maxForce
            nvx = vx[i] + fx; nvy = vy[i] + fy
            s = np.hypot(nvx, nvy)
            if s > maxSpeed: nvx = nvx / s * maxSpeed; nvy = nvy / s * maxSpeed
            if s < 0.3: nvx *= 1.05; nvy *= 1.05
            nx[i] = nvx; ny[i] = nvy
        vx, vy = nx, ny
        x = (x + vx) % W; y = (y + vy) % H
    # order parameter (alignment) phi = |sum v| / sum|v|
    phi = np.hypot(vx.sum(), vy.sum()) / np.hypot(vx, vy).sum()
    # clusters via connected components within visualRange
    visited = np.zeros(n, bool); clusters = 0
    for i in range(n):
        if visited[i]: continue
        clusters += 1; stack = [i]; visited[i] = True
        while stack:
            c = stack.pop()
            for j in range(n):
                if visited[j]: continue
                if (x[j] - x[c])**2 + (y[j] - y[c])**2 < r2:
                    visited[j] = True; stack.append(j)
    return phi, clusters

print(f"  O(n^2): n=100 -> {100*99} neighbour checks/frame; n=200 -> {200*199}")
for name, (n, ms, vr, sw, aw, cw) in {
    "default": (100, 2.5, 60, 1.5, 1.0, 1.0),
    "bird":    (80, 3.5, 80, 1.2, 1.5, 1.0),
    "chaos":   (150, 5.0, 30, 0.3, 0.2, 0.1),
    "tight":   (60, 1.5, 100, 0.8, 2.0, 2.5),
}.items():
    phi, cl = run_boids(n, ms, vr, sw, aw, cw, steps=600)
    print(f"  {name:8s}: order phi={phi:.3f}  clusters={cl}")

# ===================================================================
hr("3) KARMAN VORTEX (fs = St*V/D)")
NU_AIR = 1.5e-5
def karman(V, D_mm, St, fn):
    D = D_mm * 1e-3
    fs = St * V / D
    Re = V * D / NU_AIR
    ratio = fs / fn
    lockin = "yes" if 0.85 < ratio < 1.15 else "no"
    Vcr = fn * D / St
    return fs, Re, ratio, lockin, Vcr
for args in [(5.0, 50, 0.200, 25), (6.25, 50, 0.200, 25), (10, 50, 0.2, 25)]:
    fs, Re, r, lk, Vcr = karman(*args)
    print(f"  V={args[0]} D={args[1]}mm St={args[2]} fn={args[3]}: fs={fs:.1f}Hz Re={Re:.3e} fs/fn={r:.3f} lock={lk} Vcr={Vcr:.2f}m/s")
print("  onset of shedding (real physics): Re_crit ~ 47 (Benard-von Karman)")

# ===================================================================
hr("4) PIPE FLOW (Darcy-Weisbach / Colebrook)")
def colebrook_turb(Re, epsD):
    f = 0.02
    for _ in range(40):
        rhs = -2 * np.log10(epsD / 3.7 + 2.51 / (Re * np.sqrt(f)))
        f = 1 / (rhs * rhs)
    return f
def colebrook(Re, epsD):
    if Re < 2300: return 64 / Re
    if Re < 4000:
        fl = 64 / 2300; ft = colebrook_turb(4000, epsD)
        return fl + (ft - fl) * (Re - 2300) / 1700
    return colebrook_turb(Re, epsD)
def pipe(D_mm, L, Q, rho, mu, eps):
    D = D_mm * 1e-3; A = np.pi * D * D / 4; U = Q / A
    Re = rho * U * D / mu; epsD = eps / D
    f = colebrook(Re, epsD); dP = f * (L / D) * 0.5 * rho * U * U
    return U, Re, f, dP, epsD
# defaults: D=50, L=10, Q=0.01, water, steel eps=0.046mm
rho_w, mu_w = 998.2, 1.002e-3
U, Re, f, dP, epsD = pipe(50, 10, 0.01, rho_w, mu_w, 0.000046)
print(f"  default D=50 L=10 Q=0.01 water steel: U={U:.3f}m/s Re={Re:.3e} eps/D={epsD:.2e} f={f:.5f} dP={dP:.1f}Pa ({dP/1e5:.3e}bar)")
# reference: water 20C, D=25mm, U=1 m/s
D = 0.025; Re_ref = rho_w * 1.0 * D / mu_w
print(f"  ref water D=25mm U=1m/s: Re={Re_ref:.0f} (CLAUDE.md reynolds-number ~24,900)")
# laminar transition values
print(f"  Re=2000 (laminar) f=64/Re={64/2000:.4f}; Re=2300 crit f={64/2300:.4f}")
# Blasius smooth-turbulent check vs Colebrook smooth
for Re in [1e4, 1e5, 1e6]:
    fb = 0.3164 / Re**0.25
    fc = colebrook_turb(Re, 0.0)
    print(f"  Re={Re:.0e}: Blasius f={fb:.5f} vs Colebrook(smooth) f={fc:.5f}")
print("\nDONE.")
