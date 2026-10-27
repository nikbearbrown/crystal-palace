# r13 CP042 'the landscape performs': the waterworks RUNNING (first full display 18 June 1856, Queen present - R).
# Exec'd from build.py for SY_STATE=EARLY after the static basins (r05-r07), which stay as built. Adds, in a separate dated
# collection: vertical plumes with falling veils, rim jets arching inward, spray clouds, splash foam, the cascades running
# as white-water sheets over each step, the temple outfalls, and Victorian visitors on the terraces and walks.
# Grades: running display date R (Times 19 Jun 1856 / Grove 'Crystal Palace'); great-basin centre jets 'up to 250 ft' are
# a period claim (R as claim; modelled 200 ft, I); jet patterns after the 1886 photo 0120 (tall centre plume + ring jets on
# the terrace basins, many jets in the great basins - R for type, counts I); spray as mesh (form I); visitor numbers U.
import math, random, bmesh
from mathutils import Vector, Matrix
WWC = coll('SY56_waterworks_running__18Jun1856')
WSP = mat('water_spray_running', (0.93, 0.95, 0.98), 0.25)
_b = WSP.node_tree.nodes['Principled BSDF']
_b.inputs['Alpha'].default_value = 0.8; _b.inputs['Transmission Weight'].default_value = 0.3
_b.inputs['Emission Color'].default_value = (0.92, 0.96, 1.0, 1); _b.inputs['Emission Strength'].default_value = 0.25
FOAM = mat('water_foam_running', (0.86, 0.89, 0.90), 0.8)
SP = MB('waterworks_spray', WWC, WSP); FO = MB('waterworks_foam', WWC, FOAM); DR = MB('waterworks_drops', WWC, WSP)
R13 = random.Random(18061856)
def drop(x, y, z, s):
    bm = DR.bm; s = f(s)
    v = [bm.verts.new((f(x) + dx*s, f(y) + dy*s, f(z) + dz*s)) for dx, dy, dz in ((1, 0, -0.4), (-0.5, 0.87, -0.4), (-0.5, -0.87, -0.4), (0, 0, 1.4))]
    for t in ((0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)): bm.faces.new([v[i] for i in t])
def arc(p0, p1, H, w0, w1, n=12, mb=None):
    """parabolic jet from p0 to p1 rising H above the higher end; square-section bar chain tapering w0->w1"""
    mb = mb or SP; pts = []
    for i in range(n + 1):
        t = i/n; pts.append((p0[0] + (p1[0]-p0[0])*t, p0[1] + (p1[1]-p0[1])*t, p0[2] + (p1[2]-p0[2])*t + 4*H*t*(1-t)))
    for i in range(n):
        w = w0 + (w1 - w0)*(i + 0.5)/n; mb.strut(pts[i], pts[i+1], w, w)
    return pts
def plume(xc, yc, z0, H, r0=0.8, veils=20, drops=500, land=None, foam_r=None):
    """vertical display jet: tapering column, crown, falling umbrella veil, droplet cloud and splash foam"""
    n = 10
    for i in range(n):
        za, zb = z0 + H*i/n, z0 + H*(i+1)/n
        ra, rb = r0*(1 + 1.6*i/n), r0*(1 + 1.6*(i+1)/n)
        SP.cyl(xc, yc, za, zb, ra, rb, seg=12)
    SP.cyl(xc, yc, z0 + H, z0 + H*1.04, r0*2.6, r0*0.6, seg=12)
    land = land or H*0.28
    for k in range(veils):                                           # falling veil: from crown outwards and down
        t = 2*math.pi*k/veils + R13.uniform(-0.1, 0.1); L = land*R13.uniform(0.8, 1.1)
        arc((xc + r0*2*math.cos(t), yc + r0*2*math.sin(t), z0 + H*0.97), (xc + L*math.cos(t), yc + L*math.sin(t), z0), H*0.04, 0.95*r0, 0.45*r0, n=10)
    for i in range(drops):                                           # spray cloud, densest near the crown and the landing ring
        if i % 2:
            zz = z0 + H*(0.75 + 0.3*R13.random()); rr = R13.uniform(0, r0*5 + H*0.06)
        else:
            u = R13.random(); zz = z0 + H*(1 - u)*0.95; rr = land*(0.45 + 0.6*u)*R13.uniform(0.85, 1.12)
        t = R13.uniform(0, 2*math.pi); drop(xc + rr*math.cos(t), yc + rr*math.sin(t), zz, R13.uniform(0.2, 0.5) + H*0.003)
    fr = foam_r or land*1.15
    FO.cyl(xc, yc, z0 - 0.05, z0 + 0.12, fr, fr*0.7, seg=32)
def rim_jets(xc, yc, z, r, n, rise, reach, w=0.35):
    for k in range(n):
        t = 2*math.pi*k/n; p0 = (xc + r*math.cos(t), yc + r*math.sin(t), z); L = r - reach
        p1 = (xc + L*math.cos(t), yc + L*math.sin(t), z - 1.0)
        pts = arc(p0, p1, rise, w, w*0.6)
        for j in range(6): drop(p1[0] + R13.uniform(-1.5, 1.5), p1[1] + R13.uniform(-1.5, 1.5), z - 1 + R13.uniform(0, 1.6), 0.25)
        FO.cyl(p1[0], p1[1], z - 1.05, z - 0.9, 1.6, 1.2, seg=8)

# --- six terrace basins (z = LT, water at LT + 1.8; ornate centre bowl top ~ LT + 18*s) ---
for xs_ in (-720, -515, -231, 231, 515, 720):
    s_ = 1.0
    plume(xs_, YPC, LT + 18, 64, r0=0.6, veils=28, drops=700, land=13.0, foam_r=12.0)       # 0120: tall centre plume (height I)
    rim_jets(xs_, YPC, LT + 2.9, 42, 24, 9, 14)                                               # ring jets arching inward
    FO.cyl(xs_, YPC, LT + 1.75, LT + 1.86, 11.6, 10.5, seg=24)                                  # overflow from the lower bowl
# --- R fountains, H fountain ---
for dx in (447, 632):
    x_, y_ = mdx(dx), mdy(445); z_ = zs(y_)
    plume(x_, y_, z_ + 18*0.45, 40, r0=0.45, veils=14, drops=220, land=8); rim_jets(x_, y_, z_ + 2.9, 17, 12, 5, 8, 0.28)
yH = mdy(500); zH = zs(yH)
plume(0, yH, zH + 18*1.4, 120, r0=0.9, veils=24, drops=900, land=30); rim_jets(0, yH, zH + 2.9, 74, 32, 14, 24, 0.45)
# --- the two great lower basins (M): centre plume 200 ft (period claim 250 ft), ring of 24 jets, 40 rim jets ---
yM = mdy(700); zM = zs(yM)
for dx in (420, 662):
    x_ = mdx(dx); zw = zM + 3.5 - 0.6
    plume(x_, yM, zw, 200, r0=1.6, veils=30, drops=1600, land=48, foam_r=60)
    for k in range(24):                                                                     # inner ring on an ellipse
        t = 2*math.pi*k/24; px_, py_ = x_ + 210*math.cos(t), yM + 110*math.sin(t)
        plume(px_, py_, zw, 55 + 15*(k % 2), r0=0.5, veils=8, drops=80, land=11, foam_r=8)
    for k in range(40):                                                                     # rim jets on the super-ellipse
        t = 2*math.pi*k/40; ex = math.copysign(abs(math.cos(t))**0.5, math.cos(t)); ey = math.copysign(abs(math.sin(t))**0.5, math.sin(t))
        p0 = (x_ + 372*ex, yM + 202*ey, zM + 3.5); p1 = (x_ + 330*ex, yM + 170*ey, zw)
        arc(p0, p1, 16, 0.45, 0.3); FO.cyl(p1[0], p1[1], zw - 0.05, zw + 0.12, 3.0, 2.0, seg=8)
# --- cascades (L) running: white-water sheet falling off each step + foam where it lands; temple outfalls ---
for dx in (500, 582):
    x_ = mdx(dx); ya_, yb_ = mdy(560), mdy(690); nstep = 16
    for i in range(nstep):
        y0_ = ya_ + (yb_-ya_)*i/nstep; y1_ = ya_ + (yb_-ya_)*(i+1)/nstep; z_ = zs((y0_+y1_)/2)
        zn = zs((y1_ + (y1_ - y0_)/2)) if i < nstep - 1 else zM + 2.9
        # sheet over the lip (y1_ edge) falling to the next step's water level, slight forward curve
        bmv = FO.bm
        A = [(x_-11, y1_, z_ + 1.25), (x_+11, y1_, z_ + 1.25)]
        B = [(x_-11, y1_ - 1.6, zn + 1.2), (x_+11, y1_ - 1.6, zn + 1.2)]
        FO.poly([A[0], A[1], (x_+11, y1_ - 0.9, (z_ + zn)/2 + 1.3), (x_-11, y1_ - 0.9, (z_ + zn)/2 + 1.3)])
        FO.poly([(x_-11, y1_ - 0.9, (z_ + zn)/2 + 1.3), (x_+11, y1_ - 0.9, (z_ + zn)/2 + 1.3), B[1], B[0]])
        FO.box(x_-11, x_+11, y1_ - 4.5, y1_ - 1.2, zn + 1.2, zn + 1.45)                     # churned foam at the foot
        for j in range(20): drop(x_ + R13.uniform(-11, 11), y1_ - R13.uniform(0.5, 4), zn + 1.2 + R13.uniform(0, 2.2), 0.22)
    yJ = mdy(560); zJ = zs(yJ)
    for cx_ in (-8, 0, 8):                                                                 # outfall spouts at the temple front
        arc((x_ + cx_, yJ - 6, zJ + 3.6), (x_ + cx_, yJ - 14, zs(yJ - 14) + 1.3), 1.5, 1.2, 0.9, n=8)
        FO.cyl(x_ + cx_, yJ - 14, zs(yJ - 14) + 1.2, zs(yJ - 14) + 1.4, 3.0, 2.0, seg=10)
SP.done(); FO.done(); DR.done()
bpy.data.objects['waterworks_spray']['great_centres_ft'] = [mdx(420), yM, mdx(662), yM]   # r14: for the jet-height D-check

# --- visitors: terraces and walks, people(); figures face the water (U numbers) ---
VP = []
def crowd(x0, x1, y0, y1, z, n, look=None):
    for i in range(n):
        x, y = R13.uniform(x0, x1), R13.uniform(y0, y1)
        rot = face_rot(look[0] - x, look[1] - y) + R13.uniform(-0.7, 0.7) if look and R13.random() < 0.75 else R13.uniform(-math.pi, math.pi)
        VP.append((x, y, z, public(R13), rot))
for xs_ in (-720, -515, -231, 231, 515, 720):                                            # round each terrace basin
    for i in range(70):
        t = R13.uniform(0, 2*math.pi); rr = R13.uniform(53, 66); x, y = xs_ + rr*math.cos(t), YPC + rr*math.sin(t)
        VP.append((x, y, LT, public(R13), face_rot(xs_ - x, YPC - y) + R13.uniform(-0.4, 0.4)))
crowd(-40, 40, yL + 10, yU - 50, LT, 220)                                                  # central walk
crowd(-700, 700, yU - BANK - 14, yU - BANK - 4, LT, 380, look=(0, yL - 400))              # foot of the terrace bank
crowd(-700, 700, yU + 6, yU + 22, UT, 420, look=(0, yL - 400))                            # upper-terrace balustrade
crowd(-300, 300, yU + 30, -175, UT, 300)
for dx in (420, 662):                                                                     # round the great basins
    x_ = mdx(dx)
    for i in range(260):
        t = R13.uniform(0, 2*math.pi); ex = math.copysign(abs(math.cos(t))**0.5, math.cos(t)); ey = math.copysign(abs(math.sin(t))**0.5, math.sin(t))
        k = R13.uniform(1.04, 1.12); x, y = x_ + 380*k*ex, yM + 210*k*ey
        VP.append((x, y, zs(y), public(R13), face_rot(x_ - x, yM - y) + R13.uniform(-0.5, 0.5)))
for i in range(160):
    t = R13.uniform(0, 2*math.pi); rr = R13.uniform(84, 96); x, y = rr*math.cos(t), yH + rr*math.sin(t)
    VP.append((x, y, zs(y), public(R13), face_rot(-x, yH - y) + R13.uniform(-0.4, 0.4)))
cam('CAM_CP042_terrace_overlook_35mm', (20, yU - 2, UT + EYE), (300, yM, zM + 60), 35)   # head of the centre flight
cam('CAM_CP042_terrace_basin_35mm', (150, YPC + 40, LT + EYE), (231, YPC - 10, LT + 34), 35)
cam('CAM_CP042_great_basins_35mm', (150, yM + 420, zs(yM + 420) + EYE), (560, yM - 40, zM + 70), 35)
cam('CAM_CP042_cascade_50mm', (mdx(500) + 40, mdy(694), zs(mdy(694)) + EYE), (mdx(500), mdy(640), zs(mdy(640)) + 8), 50)
people('ppl57_waterworks_visitors', WWC, VP)
print('WATERWORKS visitors', len(VP))
