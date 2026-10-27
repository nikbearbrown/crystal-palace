# r15 SY-CLEARANCE (CP063): late-1930s clearance of the ruins — scrap gangs, cranes, lorries.
# Exec'd after states.py when STATE=='CLEARANCE'. Shares build namespace. Forms I/U (no clearance photo set in repo).
import math, random, bmesh
from mathutils import Vector, Matrix

RCL = random.Random(1938)
CL = coll('SY-CLEARANCE_scrap_gangs_cranes_lorries__late1930s')

def fmat(n, c, r=0.7, m=0.0):
    return bpy.data.materials.get(n) or mat(n, c, r, m)

rust = fmat('cl_scrap_rust', (0.28, 0.12, 0.05), 0.85, 0.4)
iron_d = fmat('cl_iron_dark', (0.08, 0.08, 0.09), 0.6, 0.35)
cab = fmat('cl_lorry_cab', (0.15, 0.18, 0.12), 0.7)
canvas = fmat('cl_canvas', (0.45, 0.40, 0.28), 0.9)
rubber = fmat('cl_rubber', (0.04, 0.04, 0.04), 0.9)
wood = fmat('cl_timber', (0.30, 0.22, 0.12), 0.85)
yellow = fmat('cl_crane_yellow', (0.72, 0.55, 0.08), 0.45, 0.2)  # r17 more readable crane body

# ---- scrap piles on the cleared plateau (footing pads already from RUINS) ----
SC = MB('clearance_scrap_piles', CL, rust)
IR = MB('clearance_iron_beams', CL, iron_d)
for i in range(90):
    x = RCL.uniform(-HALF + 30, HALF - 30); y = RCL.uniform(-140, 140)
    if (x + 336)**2 + y**2 < 50**2: continue   # keep CP072 eye clear
    z0 = gz(y) + 0.3
    # twisted beam
    L = RCL.uniform(8, 28); ang = RCL.uniform(0, math.pi)
    dx, dy = L * math.cos(ang), L * math.sin(ang)
    IR.strut((x, y, z0 + 0.5), (x + dx, y + dy, z0 + RCL.uniform(0.5, 4)), RCL.uniform(0.4, 0.9), RCL.uniform(0.3, 0.7))
    if RCL.random() < 0.5:
        SC.box(x - 3, x + 3, y - 3, y + 3, z0, z0 + RCL.uniform(2, 6))
SC.done(); IR.done()

# ---- mobile crane (block-out: lattice jib on a tracked chassis; form I) ----
def crane(name, x, y, z, yaw, jib_len=55):
    CR = MB(name + '_body', CL, yellow)
    CK = MB(name + '_tracks', CL, iron_d)
    CJ = MB(name + '_jib', CL, iron_d)
    # chassis
    CR.box(x - 6, x + 6, y - 4, y + 4, z, z + 5)
    CR.box(x - 4, x + 4, y - 3, y + 3, z + 5, z + 10)  # cab house
    # tracks
    for s in (-1, 1):
        CK.box(x - 7, x + 7, y + s * 4.5 - 1.2, y + s * 4.5 + 1.2, z - 0.5, z + 2.5)
    # jib (lattice approx as tapering box + bars)
    jx = x + jib_len * math.cos(yaw); jy = y + jib_len * math.sin(yaw)
    tip_z = z + 8 + jib_len * 0.55
    CJ.strut((x, y, z + 10), (jx, jy, tip_z), 1.2, 1.2)
    CJ.strut((x, y, z + 8), (jx, jy, tip_z - 2), 0.6, 0.6)
    # hook block
    CJ.cyl(jx, jy, tip_z - 10, tip_z - 2, 0.4, 0.35, 6)
    CR.done(); CK.done(); CJ.done()

crane('crane_central', -80, 40, gz(40), math.radians(40), 60)
crane('crane_south', -400, -60, gz(-60), math.radians(-20), 48)
crane('crane_north', 350, 20, gz(20), math.radians(120), 52)

# ---- lorries (1930s open-back tipper block-outs) ----
def lorry(name, x, y, z, yaw):
    LB = MB(name + '_body', CL, cab)
    LW = MB(name + '_wheels', CL, rubber)
    LC = MB(name + '_cargo', CL, rust)
    # local axes
    c, s = math.cos(yaw), math.sin(yaw)
    def lx(dx, dy): return x + dx * c - dy * s, y + dx * s + dy * c
    # cab
    (x0, y0) = lx(-8, -3); (x1, y1) = lx(2, 3)
    # approximate with axis-aligned for simplicity (I) — rotate by placing along yaw via strut boxes
    LB.box(x - 4, x + 10, y - 3.5, y + 3.5, z + 2.5, z + 8)   # chassis/cab envelope
    LB.box(x - 4, x + 1, y - 3.2, y + 3.2, z + 8, z + 12)      # cab roof
    LC.box(x + 1, x + 12, y - 3.2, y + 3.2, z + 3, z + 9)      # open cargo of scrap
    for dx in (-2, 8):
        for dy in (-3.8, 3.8):
            LW.cyl(x + dx, y + dy, z, z + 2.8, 1.3, 1.3, 8)
    LB.done(); LW.done(); LC.done()

for i, (xx, yy, yaw) in enumerate([(-120, 90, 0.3), (60, -100, 1.2), (-500, 30, -0.4),
                                    (200, 70, 2.0), (-250, -80, 0.8), (450, -40, -1.1)]):
    lorry(f'lorry_{i:02d}', xx, yy, gz(yy), yaw)

# ---- scrap gang workers (reuse dress36 lathe figures if available; else simple boxes) ----
# dress36 defines person()/lathe for 1930s — only loaded for 1936/FIRE/AFTER. Rebuild minimal workers here.
PM = [fmat('cl_coat', (0.08, 0.08, 0.09), 0.85), fmat('cl_skin', (0.55, 0.36, 0.27), 0.6),
      fmat('cl_hat', (0.05, 0.05, 0.05), 0.7), fmat('cl_trou', (0.12, 0.10, 0.08), 0.85)]

def worker_mesh(name, x, y, z, rot):
    bm = bmesh.new()
    # legs
    for s in (-0.25, 0.25):
        bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=f(0.2), radius2=f(0.18), depth=f(2.6),
                              matrix=Matrix.Translation(Vector((f(x + s*math.cos(rot)), f(y + s*math.sin(rot)), f(z + 1.3)))))
    # torso
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=f(0.65), radius2=f(0.45), depth=f(2.4),
                          matrix=Matrix.Translation(Vector((f(x), f(y), f(z + 3.7)))))
    # head
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=f(0.32),
                              matrix=Matrix.Translation(Vector((f(x), f(y), f(z + 5.2)))))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(PM[0]); me.materials.append(PM[1])
    o = bpy.data.objects.new(name, me); CL.objects.link(o)
    return o

WK = []
for i in range(48):
    x = RCL.uniform(-HALF + 40, HALF - 40); y = RCL.uniform(-130, 130)
    if (x + 336)**2 + y**2 < 55**2: continue
    WK.append(worker_mesh(f'worker_{i:02d}', x, y, gz(y), RCL.uniform(0, 6.28)))
# denser gang near central crane
for i in range(28):
    x = -80 + RCL.uniform(-30, 30); y = 40 + RCL.uniform(-25, 25)
    WK.append(worker_mesh(f'worker_crane_{i:02d}', x, y, gz(y), RCL.uniform(0, 6.28)))
# r17: scrap mound + beams in crane foreground (story: lift of wreckage)
SC2 = MB('clearance_crane_fg_scrap', CL, rust); IR2 = MB('clearance_crane_fg_beams', CL, iron_d)
for i in range(24):
    x = -55 + RCL.uniform(-18, 12); y = 55 + RCL.uniform(-12, 18); z0 = gz(y) + 0.3
    L = RCL.uniform(10, 26); ang = RCL.uniform(0, math.pi)
    IR2.strut((x, y, z0 + 0.5), (x + L*math.cos(ang), y + L*math.sin(ang), z0 + RCL.uniform(1, 5)), 0.6, 0.5)
    if RCL.random() < 0.6: SC2.box(x-4, x+4, y-3, y+3, z0, z0 + RCL.uniform(3, 8))
SC2.done(); IR2.done()

# ---- cameras CP063 ----
cam('CAM_CP063_clearance_perimeter_35mm', (-520, yU + 40, UT + EYE + 4), (0, 0, 20), 35)
cam('CAM_CP063_scrap_gang_35mm', (-200, 120, gz(120) + EYE), (-80, 40, gz(40) + 18), 35)
# r17c: among scrap looking at yellow crane body + workers (fill frame)
cam('CAM_CP063_crane_lift_50mm', (-20, 85, gz(85) + EYE + 2), (-80, 40, gz(40) + 10), 35)
cam('CAM_CP063_terrace_edge_35mm', (-100, yU + 20, UT + EYE), (100, -40, UT + 5), 35)  # intact terrace edge anchors

print('CLEARANCE OK', 'workers', len(WK), 'cranes 3 lorries 6')
