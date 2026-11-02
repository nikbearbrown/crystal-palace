#!/usr/bin/env python3
"""scan-fig01-frost-fair-thames — Muse version.
The 1683 frost fair on the frozen Thames (contemporary broadside print):
a street of booths on the ice, crowd rings and a whirligig horse on the
back ice, coaches/skaters/boats in the foreground, old London Bridge and
the City skyline as a flat backdrop. Elevated viewpoint as in the print.
Run: blender -b --python build_scan_fig01_frost_fair_thames.py
"""
import bpy, math, os, random
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig01-frost-fair-thames"
random.seed(11)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for coll in list(bpy.data.collections):
    if coll.name != "Collection":
        bpy.data.collections.remove(coll)
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

MATS = {}
def mat(name, rgb, rough=0.9):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    MATS[name] = m
    return m

def link(ob, coll=model_coll):
    for c in ob.users_collection: c.objects.unlink(ob)
    coll.objects.link(ob)

def prim(kind, name, mats, loc=(0,0,0), scale=(1,1,1), rot=(0,0,0), **kw):
    if kind == 'box': bpy.ops.mesh.primitive_cube_add()
    elif kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=kw.get('verts',11), radius=kw.get('r',0.5), depth=kw.get('d',1.0))
    elif kind == 'cone': bpy.ops.mesh.primitive_cone_add(vertices=kw.get('verts',11), radius1=kw.get('r1',0.5), radius2=kw.get('r2',0.0), depth=kw.get('d',1.0))
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=kw.get('seg',10), ring_count=kw.get('rings',7), radius=kw.get('r',0.5))
    elif kind == 'torus': bpy.ops.mesh.primitive_torus_add(major_segments=12, minor_segments=5, major_radius=kw.get('R',0.5), minor_radius=kw.get('r',0.08))
    ob = bpy.context.active_object
    ob.name = name
    ob.location = loc; ob.rotation_euler = rot; ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if isinstance(mats, (list, tuple)):
        for m in mats: ob.data.materials.append(m)
    elif mats: ob.data.materials.append(mats)
    link(ob)
    return ob

def root(name):
    return prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01))

def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name
    # rebase: objs[0] is a root at ~(0,0,0.01), so geometry keeps its authored frame
    loc = ob.location.copy()
    ob.data.transform(Matrix.Translation((-loc.x, -loc.y, -loc.z)))
    ob.location = (0, 0, 0)
    ob.rotation_euler = (0, 0, 0)
    return ob

def figure(name, h=1.66, dress='coat', coat=(0.2,0.17,0.15), lower=(0.3,0.26,0.22),
           skin=(0.85,0.65,0.52), hat='broad', hat_col=(0.1,0.09,0.09),
           arm_l=0.15, arm_r=0.15, arm_lz=0.12, arm_rz=-0.12, lean=0.0, leg_spread=0.0, shawl=None):
    parts = [root(name)]
    skin_m = mat('skin', skin); coat_m = mat('c_'+name, coat); low_m = mat('l_'+name, lower); hat_m = mat('h_'+name, hat_col)
    if dress == 'skirt':
        parts.append(prim('cone', name+'_skirt', coat_m, loc=(0,0,h*0.27), r1=h*0.185, r2=h*0.075, d=h*0.54))
        parts.append(prim('cyl', name+'_torso', coat_m, loc=(0,0,h*0.66), r=h*0.088, d=h*0.26))
        if shawl:
            parts.append(prim('cone', name+'_shawl', mat('s_'+name, shawl), loc=(0,0,h*0.70), r1=h*0.145, r2=h*0.06, d=h*0.24))
    else:
        for s in (-1,1):
            parts.append(prim('cyl', name+'_leg', low_m, loc=(s*h*0.055,0,h*0.24), r=h*0.036, d=h*0.48,
                              rot=(0, s*leg_spread, 0)))
        parts.append(prim('cyl', name+'_torso', coat_m, loc=(0,0,h*0.63), r=h*0.098, d=h*0.40))
        parts.append(prim('cone', name+'_coatsk', coat_m, loc=(0,0,h*0.44), r1=h*0.115, r2=h*0.095, d=h*0.14))
    for s, ang, angz in ((-1, arm_l, arm_lz), (1, arm_r, arm_rz)):
        parts.append(prim('cyl', name+'_arm', coat_m, loc=(s*h*0.125, 0, h*0.615), r=h*0.028, d=h*0.34,
                          rot=(ang, 0, angz + (0.10 if s<0 else -0.10))))
        parts.append(prim('sph', name+'_hand', skin_m, loc=(s*h*0.15, -math.sin(ang)*h*0.16, h*0.615-math.cos(ang)*h*0.17), r=h*0.028, seg=8, rings=6))
    parts.append(prim('sph', name+'_head', skin_m, loc=(0,0,h*0.905), scale=(0.92,0.98,1.06), r=h*0.068))
    hz = h*0.965
    if hat == 'top':
        parts.append(prim('cyl', name+'_brim', hat_m, loc=(0,0,hz), r=h*0.085, d=0.012))
        parts.append(prim('cyl', name+'_crown', hat_m, loc=(0,0,hz+h*0.05), r=h*0.058, d=h*0.10))
    elif hat == 'bonnet':
        parts.append(prim('sph', name+'_bonnet', hat_m, loc=(0,-h*0.018,h*0.925), scale=(1.0,1.05,0.95), r=h*0.075, seg=9, rings=7))
        parts.append(prim('cyl', name+'_bbrim', hat_m, loc=(0,h*0.045,h*0.955), r=h*0.07, d=0.01, rot=(0.5,0,0)))
    elif hat == 'cap':
        parts.append(prim('cone', name+'_cap', hat_m, loc=(0,0,h*0.965), r1=h*0.075, r2=h*0.045, d=h*0.05))
    elif hat == 'broad':
        parts.append(prim('cyl', name+'_brim', hat_m, loc=(0,0,hz), r=h*0.105, d=0.012))
        parts.append(prim('sph', name+'_crown', hat_m, loc=(0,0,hz+0.01), scale=(1,1,0.55), r=h*0.062, seg=9, rings=6))
    ob = join(parts, name)
    ob.rotation_euler = (lean, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return ob

def place(ob, x, y, rotz=0.0):
    ob.location = (x, y, 0)
    ob.rotation_euler = (0, 0, rotz)
    return ob

# ---------- materials ----------
ice_m   = mat('ice', (0.78,0.83,0.88), 0.5)
snow_m  = mat('snow', (0.92,0.93,0.95))
crack_m = mat('crack', (0.45,0.52,0.60), 0.6)
sil_m   = mat('silhouette', (0.34,0.38,0.46))
sil_d   = mat('silhouette_dark', (0.30,0.34,0.42))
wood_m  = mat('wood', (0.40,0.30,0.19))
wood_d  = mat('wood_dark', (0.27,0.20,0.13))
canvas_m= mat('canvas', (0.78,0.72,0.60))
red_m   = mat('awning_red', (0.55,0.22,0.18))
white_m = mat('awning_white', (0.85,0.82,0.75))
dark_m  = mat('dark', (0.12,0.11,0.12), 0.6)
coach_m = mat('coach', (0.16,0.13,0.12))
horse_m = mat('horse', (0.30,0.22,0.16))

COATS = [(0.25,0.19,0.14),(0.16,0.15,0.17),(0.35,0.24,0.16),(0.20,0.24,0.28),(0.40,0.28,0.18),(0.30,0.20,0.24)]
DRESSES = [(0.42,0.28,0.30),(0.30,0.34,0.40),(0.36,0.30,0.20),(0.28,0.38,0.30)]

# ---------- ice (30 x 20 m panorama) ----------
prim('box', 'Ice', ice_m, loc=(0,2,-0.15), scale=(15.0, 10.0, 0.15))
for i in range(8):
    prim('sph', 'SnowPatch', snow_m, loc=(random.uniform(-13,13), random.uniform(-6,10), 0.01),
         scale=(random.uniform(0.8,1.8), random.uniform(0.5,1.0), 0.03), r=0.5, seg=9, rings=6)
for i in range(7):
    prim('box', 'IceCrack', crack_m, loc=(random.uniform(-12,12), random.uniform(-6,9), 0.006),
         scale=(random.uniform(1.2,3.2), 0.035, 0.006), rot=(0,0,random.uniform(0,3.1)))

# ---------- backdrop: bridge + skyline (flat silhouette at y=11.5) ----------
BY = 11.5
prim('box', 'BridgeDeck', sil_m, loc=(0, BY, 3.0), scale=(14.0, 0.35, 0.5))
for i in range(13):
    x = -13.2 + i*2.2
    prim('box', 'BridgePier', sil_d, loc=(x, BY, 1.2), scale=(0.6, 0.35, 1.25))
for i in range(14):
    x = -13 + i*2.0
    prim('box', 'BridgeHouse', sil_m, loc=(x, BY, 3.95), scale=(0.8, 0.3, 0.5))
    prim('cone', 'BridgeRoof', sil_d, loc=(x, BY, 4.5), r1=0.9, r2=0.08, d=0.6, verts=4, rot=(0,0,math.pi/4))
# Tower of London: White Tower with four turrets (left-centre)
prim('box', 'WhiteTower', sil_m, loc=(-5.2, BY, 4.6), scale=(1.6, 0.35, 1.4))
for dx in (-1.35, 1.35):
    prim('cyl', 'Turret', sil_m, loc=(-5.2+dx, BY, 5.1), r=0.32, d=2.5)
    prim('cone', 'TurretCap', sil_d, loc=(-5.2+dx, BY, 6.7), r1=0.4, r2=0.02, d=0.75)
for dx in (-0.5, 0.5):
    prim('cyl', 'TurretIn', sil_m, loc=(-5.2+dx, BY, 4.9), r=0.26, d=2.1)
    prim('cone', 'TurretInCap', sil_d, loc=(-5.2+dx, BY, 6.3), r1=0.33, r2=0.02, d=0.65)
# church spire far left
prim('box', 'ChurchTower', sil_m, loc=(-12.6, BY, 4.0), scale=(0.55, 0.35, 2.5))
prim('cone', 'Spire', sil_d, loc=(-12.6, BY, 6.9), r1=0.5, r2=0.02, d=3.3)
# the Monument (column, left of centre)
prim('cyl', 'Monument', sil_m, loc=(1.2, BY, 4.9), r=0.28, d=4.8)
prim('box', 'MonumentCap', sil_d, loc=(1.2, BY, 7.5), scale=(0.42, 0.35, 0.25))
# Southwark tower right
prim('box', 'SouthwarkTower', sil_m, loc=(11.4, BY, 4.2), scale=(0.75, 0.35, 2.6))
prim('cone', 'SouthwarkSpire', sil_d, loc=(11.4, BY, 6.3), r1=0.48, r2=0.02, d=1.6)
prim('cone', 'SouthwarkSpire2', sil_d, loc=(11.4, BY, 7.5), r1=0.28, r2=0.02, d=1.2)
# rooftops behind bridge
for x, hh in ((-9.2,3.8),(-7.6,4.2),(3.6,3.9),(5.4,4.3),(7.6,3.7),(9.4,4.1),(13.2,3.8)):
    prim('box', 'RoofBlock', sil_m, loc=(x, BY+0.15, hh), scale=(0.85, 0.3, 0.65))
    prim('cone', 'RoofTop', sil_d, loc=(x, BY+0.15, hh+0.8), r1=0.95, r2=0.08, d=0.6, verts=4, rot=(0,0,math.pi/4))
# bare trees at both ends of the backdrop
for tx in (-14.3, 14.3):
    prim('cyl', 'TreeTrunk', sil_d, loc=(tx, BY, 1.5), r=0.15, d=3.0)
    for a in (-0.5, 0.0, 0.5):
        prim('cyl', 'TreeBranch', sil_d, loc=(tx + a*1.0, BY, 3.4), r=0.055, d=1.8, rot=(0, a, 0))
# sloped banks at both ends (embankments in the print)
for sx in (-1, 1):
    prim('box', 'Bank', sil_m, loc=(sx*14.6, 8.2, 0.9), scale=(0.9, 3.4, 0.9), rot=(0, sx*0.42, 0))
    prim('box', 'BankHouse', sil_d, loc=(sx*14.4, 10.6, 2.2), scale=(0.7, 0.5, 0.8))

# ---------- booths (two rows facing a street) ----------
def booth(name, x, y, rotz, stripe_a, stripe_b, curtain):
    parts = [root(name)]
    parts.append(prim('box', name+'_counter', wood_m, loc=(0,0,0.55), scale=(1.15, 0.55, 0.55)))
    parts.append(prim('box', name+'_back', wood_d, loc=(0,0.62,1.15), scale=(1.15, 0.05, 1.15)))
    for sx in (-1.08, 1.08):
        parts.append(prim('cyl', name+'_post', wood_d, loc=(sx,-0.5,1.25), r=0.045, d=2.5))
    for i in range(6):
        m = stripe_a if i % 2 == 0 else stripe_b
        parts.append(prim('box', name+'_awn', m, loc=(-0.96+i*0.385, -0.15, 2.45), scale=(0.20, 0.85, 0.035), rot=(0.62,0,0)))
    parts.append(prim('box', name+'_curtain', curtain, loc=(0, -0.28, 1.85), scale=(1.05, 0.03, 0.55), rot=(0.35,0,0)))
    for i in range(3):
        parts.append(prim('box', name+'_goods', mat('goods', (0.5,0.4,0.25)), loc=(-0.6+i*0.55, -0.25, 1.16), scale=(0.16,0.16,0.10)))
    parts.append(prim('cyl', name+'_pole', wood_d, loc=(1.08, 0.3, 3.15), r=0.025, d=1.5))
    parts.append(prim('box', name+'_flag', stripe_a, loc=(1.35, 0.3, 3.75), scale=(0.28, 0.015, 0.16)))
    ob = join(parts, name)
    ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rotz)
    return ob

for i, x in enumerate((-8.75, -5.25, -1.75, 1.75, 5.25, 8.75)):
    booth(f'BoothBack{i}', x, 3.2, 0.0, red_m if i%2 else white_m, white_m if i%2 else red_m, canvas_m)
for i, x in enumerate((-7.0, -3.5, 0.0, 3.5, 7.0)):
    booth(f'BoothFront{i}', x, 0.2, 0.0, white_m if i%2 else red_m, red_m if i%2 else white_m, mat('curtain2', (0.62,0.55,0.44)))
# people in the booth street
for i, (x, y, r) in enumerate(((-4.6,1.8,0.4),(2.9,1.6,-0.3),(-1.2,1.9,2.9),(6.1,1.7,-2.8),(-8.6,1.6,1.1))):
    f = figure(f'Street{i}', h=1.67, coat=COATS[i % len(COATS)], arm_l=0.4, arm_r=0.4)
    place(f, x, y, r)

# ---------- horse + coach ----------
def horse(name, x, y, rotz):
    parts = [root(name)]
    parts.append(prim('sph', name+'_body', horse_m, loc=(0,0,1.18), scale=(1.0,0.34,0.36), r=0.62))
    parts.append(prim('box', name+'_neck', horse_m, loc=(0.62,-0.02,1.48), scale=(0.16,0.11,0.30), rot=(0,0.6,0)))
    parts.append(prim('box', name+'_head', horse_m, loc=(0.86,-0.02,1.62), scale=(0.22,0.09,0.11), rot=(0,0.35,0)))
    for ex in (0.78, 0.92):
        parts.append(prim('cone', name+'_ear', horse_m, loc=(ex,-0.02,1.78), r1=0.03, r2=0.005, d=0.1))
    for lx in (-0.42, 0.42):
        for ly in (-0.16, 0.16):
            parts.append(prim('cyl', name+'_leg', horse_m, loc=(lx,ly,0.5), r=0.05, d=1.0))
    parts.append(prim('cone', name+'_tail', dark_m, loc=(-0.66,0,1.25), r1=0.09, r2=0.02, d=0.55, rot=(0,0.5,0)))
    ob = join(parts, name)
    ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rotz)
    return ob

def wheel(name, x, y, z, R):
    parts = [root(name)]
    parts.append(prim('torus', name+'_rim', wood_d, loc=(0,0,0), R=R, r=R*0.09, rot=(0, math.pi/2, 0)))
    for a in range(4):
        parts.append(prim('cyl', name+'_spoke', wood_m, loc=(0,0,0), r=R*0.06, d=R*1.85, rot=(a*math.pi/4, math.pi/2, 0)))
    parts.append(prim('cyl', name+'_hub', wood_d, loc=(0,0,0), r=R*0.16, d=0.1, rot=(0, math.pi/2, 0)))
    ob = join(parts, name)
    ob.location = (x, y, z)
    return ob

def coach(name, x, y, rotz, n_horses=2, with_horses=True):
    parts = [root(name)]
    parts.append(prim('box', name+'_body', coach_m, loc=(0,0,1.25), scale=(0.95, 0.55, 0.55)))
    parts.append(prim('box', name+'_roof', dark_m, loc=(0,0,1.92), scale=(0.85, 0.48, 0.10)))
    parts.append(prim('box', name+'_win', mat('coach_win', (0.55,0.58,0.55)), loc=(0.1,0.56,1.35), scale=(0.3,0.02,0.3)))
    parts.append(prim('box', name+'_win2', mat('coach_win', (0.55,0.58,0.55)), loc=(0.1,-0.56,1.35), scale=(0.3,0.02,0.3)))
    if with_horses:
        parts.append(prim('box', name+'_shaft', wood_d, loc=(1.45,0.25,0.85), scale=(0.65,0.035,0.035), rot=(0,0.15,0)))
        parts.append(prim('box', name+'_shaft2', wood_d, loc=(1.45,-0.25,0.85), scale=(0.65,0.035,0.035), rot=(0,0.15,0)))
    ob = join(parts, name)
    ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rotz)
    import mathutils
    m = mathutils.Matrix.Rotation(rotz, 4, 'Z')
    for (lx, ly, R) in ((0.75, 0.62, 0.42), (0.75, -0.62, 0.42), (-0.72, 0.62, 0.58), (-0.72, -0.62, 0.58)):
        wp = m @ mathutils.Vector((lx, ly, 0))
        w = wheel(name+f'_w{lx}{ly}', x+wp.x, y+wp.y, R, R)
        w.rotation_euler = (0, 0, rotz)
    if with_horses:
        offs = [(2.6, 0)] if n_horses == 1 else [(2.6, 0.44), (2.3, -0.44)]
        for i, (hx, hy) in enumerate(offs):
            hp = m @ mathutils.Vector((hx, hy, 0))
            horse(name+f'_horse{i}', x+hp.x, y+hp.y, rotz)
    return ob

# foreground coaches (as in the print: pair facing left, single facing right)
coach('CoachA', -2.5, -3.2, math.pi)
coach('CoachB', 5.2, -2.6, 0.30, n_horses=1)
# horseless coach standing on the far ice, upper right (print no. 28)
coach('CoachC', 11.6, 6.2, -0.5, with_horses=False)

# whirligig horse on the back ice (print no. 21): horse walking a circle by a fenced pit
horse('GigHorse', 0.2, 7.6, 2.6)
parts = [root('GigPit')]
for a in range(8):
    ang = a*math.pi/4
    parts.append(prim('cyl', 'GigPost', wood_d, loc=(math.cos(ang)*0.85, math.sin(ang)*0.85, 0.45), r=0.035, d=0.9))
parts.append(prim('cyl', 'GigBeam', wood_d, loc=(-0.75, 0, 1.15), r=0.04, d=1.6, rot=(0, math.pi/2, 0.5)))
g = join(parts, 'GigPit'); g.location = (-1.6, 7.6, 0); g.rotation_euler = (0,0,0.3)
f = figure('GigMan', h=1.7, coat=COATS[2], arm_l=1.2, arm_r=0.3)
place(f, 1.6, 8.1, -1.8)

# ---------- crowd rings on the back ice ----------
def ring(cx, cy, rx, ry, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        a = 2*math.pi*i/n
        x, y = cx + rx*math.cos(a), cy + ry*math.sin(a)
        f = figure(f'Ring{cx}_{i}', h=rnd.uniform(1.55,1.75),
                   dress='skirt' if i % 3 == 0 else 'coat',
                   coat=rnd.choice(DRESSES if i % 3 == 0 else COATS),
                   hat='bonnet' if i % 3 == 0 else 'broad',
                   arm_l=rnd.uniform(0,0.5), arm_r=rnd.uniform(0,0.5))
        place(f, x, y, -a + math.pi/2 + rnd.uniform(-0.2,0.2))
ring(-7.5, 8.3, 3.4, 1.7, 13, 5)
ring(7.8, 8.4, 3.6, 1.8, 15, 9)
# two performers at the right ring's centre
f = figure('PerfA', h=1.7, coat=(0.5,0.2,0.15), arm_l=1.4, arm_r=1.4); place(f, 7.5, 8.4, 2.8)
f = figure('PerfB', h=1.62, dress='skirt', coat=DRESSES[0], hat='bonnet', arm_l=1.1, arm_r=0.4); place(f, 8.3, 8.3, -2.4)

# ---------- skaters & walkers on the foreground ice ----------
rnd = random.Random(23)
for i in range(8):
    f = figure(f'Skater{i}', h=rnd.uniform(1.55,1.75), coat=rnd.choice(COATS),
               dress='skirt' if i % 4 == 0 else 'coat', hat='broad' if i%2 else 'cap',
               arm_l=rnd.uniform(0.4,1.1), arm_r=rnd.uniform(0.4,1.1),
               leg_spread=rnd.uniform(0.15,0.35), lean=rnd.uniform(-0.08,0.12))
    place(f, rnd.uniform(-12.5, 12.5), rnd.uniform(-6.8,-1.4), rnd.uniform(0, 6.28))
for i, (x, y, r) in enumerate(((-5.4,-5.4,0.9),(3.1,-5.9,2.8),(-9.8,-1.8,1.2),(10.4,-1.2,-1.0),(-0.6,-1.5,0.2))):
    f = figure(f'Walker{i}', h=1.68, coat=COATS[i % len(COATS)], arm_l=0.45, arm_r=0.45)
    place(f, x, y, r)

# ---------- sail-wheeled boat (lower left) & sailing barge (lower right) ----------
parts = [root('SailBoat')]
parts.append(prim('box', 'SB_Hull', wood_m, loc=(0,0,0.45), scale=(1.1, 0.42, 0.35)))
parts.append(prim('cyl', 'SB_Mast', wood_d, loc=(0,0,1.5), r=0.04, d=2.2))
parts.append(prim('box', 'SB_Sail', canvas_m, loc=(0.3,0,1.6), scale=(0.45,0.02,0.8)))
parts.append(prim('box', 'SB_Flag', red_m, loc=(0.3,0,2.68), scale=(0.26,0.015,0.15)))
for wx in (-0.8, 0.8):
    parts.append(prim('torus', 'SB_Wheel', wood_d, loc=(wx,-0.5,0.34), R=0.34, r=0.035, rot=(0, math.pi/2, 0)))
b = join(parts, 'SailBoat'); b.location = (-11.2, -5.4, 0); b.rotation_euler = (0,0,0.35)

parts = [root('Barge')]
parts.append(prim('box', 'B_Hull', wood_m, loc=(0,0,0.5), scale=(1.9, 0.55, 0.45)))
parts.append(prim('cone', 'B_Bow', wood_m, loc=(2.05,0,0.55), r1=0.55, r2=0.06, d=0.8, rot=(0,0,-math.pi/2)))
parts.append(prim('box', 'B_Cabin', wood_d, loc=(-0.6,0,1.05), scale=(0.9,0.45,0.35)))
parts.append(prim('cyl', 'B_Mast', wood_d, loc=(0.5,0,1.8), r=0.05, d=2.8))
parts.append(prim('box', 'B_Sail', canvas_m, loc=(0.85,0,1.9), scale=(0.55,0.02,1.0), rot=(0,0,0.12)))
parts.append(prim('box', 'B_Flag', red_m, loc=(0.85,0,3.35), scale=(0.32,0.015,0.18)))
b = join(parts, 'Barge'); b.location = (10.6, -5.9, 0); b.rotation_euler = (0,0,-0.2)
# crew hauling the barge on a rope line
for i in range(4):
    f = figure(f'Hauler{i}', h=1.66, coat=COATS[(i+1) % len(COATS)], arm_l=0.9, arm_r=0.9, lean=0.18)
    place(f, 5.9 + i*0.55, -6.6 + i*0.12, -1.35)

# horse-drawn covered sledge (foreground centre, print no. 13)
parts = [root('Sledge')]
parts.append(prim('box', 'S_Hull', wood_d, loc=(0,0,0.45), scale=(1.15, 0.45, 0.3)))
parts.append(prim('sph', 'S_Cover', canvas_m, loc=(0,0,0.92), scale=(1.05,0.42,0.5), r=0.55, seg=10, rings=6))
parts.append(prim('box', 'S_Run1', dark_m, loc=(0,-0.42,0.10), scale=(1.35,0.03,0.07)))
parts.append(prim('box', 'S_Run2', dark_m, loc=(0, 0.42,0.10), scale=(1.35,0.03,0.07)))
parts.append(prim('box', 'S_Flag', red_m, loc=(-1.0,0,1.35), scale=(0.24,0.015,0.14)))
s = join(parts, 'Sledge'); s.location = (1.8, -6.3, 0); s.rotation_euler = (0,0,0.15)
horse('SledgeHorse', 4.6, -6.0, 0.15)
f = figure('SledgeMan', h=1.68, coat=COATS[4], arm_l=0.8, arm_r=0.2); place(f, 5.9, -5.6, -1.2)

# ---------- render setup ----------
def look_at(ob, target):
    import mathutils
    d = mathutils.Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
setup_coll.objects.link(cam)
cam.location = (0, -22.5, 14.2)
look_at(cam, (0, 2.2, 0.4))
cam.data.lens = 32
bpy.context.scene.camera = cam
sun_d = bpy.data.lights.new('Sun', 'SUN'); sun_d.energy = 2.8; sun_d.angle = 0.5
sun = bpy.data.objects.new('Sun', sun_d); setup_coll.objects.link(sun)
sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(-30))
fill_d = bpy.data.lights.new('Fill', 'AREA'); fill_d.energy = 400; fill_d.shape = 'DISK'; fill_d.size = 6
fill = bpy.data.objects.new('Fill', fill_d); setup_coll.objects.link(fill)
fill.location = (-4, -8, 7); look_at(fill, (0, 1, 0.8))

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 1024; sc.render.resolution_y = 640
sc.world = bpy.data.worlds.new('W')
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.52, 0.52, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.75

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SLUG + ".blend"))
sc.render.filepath = os.path.join(HERE, "preview.png")
bpy.ops.render.render(write_still=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in model_coll.objects: ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, SLUG + ".glb"), export_format='GLB', use_selection=True)
tris = 0
for ob in model_coll.objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print("TRIANGLES:", tris)
print("DONE", SLUG)
