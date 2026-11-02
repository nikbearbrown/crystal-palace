#!/usr/bin/env python3
"""scan-fig41-london-1851 — Muse version.
Cruikshank 'London in 1851': Regent Circus crammed with exhibition
visitors — the crowded counterpart to the deserted Manchester street.
Banner across the circus, balconies full, street packed with figures
and cabs.
Run: blender -b --python build_scan_fig41_london_1851.py
"""
import bpy, math, os, random
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig41-london-1851"
random.seed(41)

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
    elif kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=kw.get('verts',14), radius=kw.get('r',0.5), depth=kw.get('d',1.0))
    elif kind == 'cone': bpy.ops.mesh.primitive_cone_add(vertices=kw.get('verts',14), radius1=kw.get('r1',0.5), radius2=kw.get('r2',0.0), depth=kw.get('d',1.0))
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=kw.get('seg',12), ring_count=kw.get('rings',9), radius=kw.get('r',0.5))
    elif kind == 'torus': bpy.ops.mesh.primitive_torus_add(major_segments=16, minor_segments=6, major_radius=kw.get('R',0.5), minor_radius=kw.get('r',0.08))
    ob = bpy.context.active_object
    ob.name = name
    ob.location = loc; ob.rotation_euler = rot; ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if isinstance(mats, (list, tuple)):
        for m in mats: ob.data.materials.append(m)
    elif mats: ob.data.materials.append(mats)
    link(ob)
    return ob

def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name
    loc = ob.location.copy()
    ob.data.transform(Matrix.Translation((-loc.x, -loc.y, -loc.z)))
    ob.location = (0, 0, 0)
    ob.rotation_euler = (0, 0, 0)
    return ob

def figure(name, h=1.68, dress='coat', coat=(0.16,0.15,0.17), lower=(0.25,0.22,0.2),
           skin=(0.85,0.65,0.52), hat='top', hat_col=(0.08,0.08,0.09),
           arm_l=0.15, arm_r=0.15, arm_lz=0.12, arm_rz=-0.12, lean=0.0, leg_spread=0.0, shawl=None):
    parts = []
    parts.append(prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    skin_m = mat('skin', skin); coat_m = mat('c_'+name, coat); low_m = mat('l_'+name, lower); hat_m = mat('h_'+name, hat_col)
    if dress == 'skirt':
        parts.append(prim('cone', name+'_skirt', coat_m, loc=(0,0,h*0.27), r1=h*0.185, r2=h*0.075, d=h*0.54, verts=10))
        parts.append(prim('cyl', name+'_torso', coat_m, loc=(0,0,h*0.66), r=h*0.088, d=h*0.26, verts=10))
        if shawl:
            parts.append(prim('cone', name+'_shawl', mat('s_'+name, shawl), loc=(0,0,h*0.70), r1=h*0.145, r2=h*0.06, d=h*0.24, verts=10))
    else:
        for s in (-1,1):
            parts.append(prim('cyl', name+'_leg', low_m, loc=(s*h*0.055,0,h*0.24), r=h*0.036, d=h*0.48, verts=8,
                              rot=(0, s*leg_spread, 0)))
        parts.append(prim('cyl', name+'_torso', coat_m, loc=(0,0,h*0.63), r=h*0.098, d=h*0.40, verts=10))
        parts.append(prim('cone', name+'_coatsk', coat_m, loc=(0,0,h*0.44), r1=h*0.115, r2=h*0.095, d=h*0.14, verts=10))
    for s, ang, angz in ((-1, arm_l, arm_lz), (1, arm_r, arm_rz)):
        parts.append(prim('cyl', name+'_arm', coat_m, loc=(s*h*0.125, 0, h*0.615), r=h*0.028, d=h*0.34, verts=8,
                          rot=(ang, 0, angz + (0.10 if s<0 else -0.10))))
    parts.append(prim('sph', name+'_head', skin_m, loc=(0,0,h*0.905), scale=(0.92,0.98,1.06), r=h*0.068))
    hz = h*0.965
    if hat == 'top':
        parts.append(prim('cyl', name+'_brim', hat_m, loc=(0,0,hz), r=h*0.085, d=0.012, verts=10))
        parts.append(prim('cyl', name+'_crown', hat_m, loc=(0,0,hz+h*0.05), r=h*0.058, d=h*0.10, verts=10))
    elif hat == 'bonnet':
        parts.append(prim('sph', name+'_bonnet', hat_m, loc=(0,-h*0.018,h*0.925), scale=(1.0,1.05,0.95), r=h*0.075))
    elif hat == 'cap':
        parts.append(prim('cone', name+'_cap', hat_m, loc=(0,0,h*0.965), r1=h*0.075, r2=h*0.045, d=h*0.05, verts=10))
    ob = join(parts, name)
    if lean:
        ob.rotation_euler = (lean, 0, 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return ob

def place(ob, x, y, rotz=0.0, z=0.0):
    ob.location = (x, y, z)
    ob.rotation_euler = (0, 0, rotz)
    return ob

# ---------- materials ----------
stucco  = mat('stucco', (0.62,0.58,0.52))
stucco2 = mat('stucco2', (0.55,0.52,0.47))
win_m   = mat('window', (0.15,0.17,0.20), 0.35)
win_p   = mat('window_pale', (0.5,0.52,0.5), 0.5)
road_m  = mat('road', (0.42,0.40,0.37))
pave_m  = mat('pavement', (0.55,0.53,0.49))
banner_m= mat('banner', (0.82,0.78,0.68))
roof_m  = mat('roof', (0.25,0.24,0.26))
sign_m  = mat('sign', (0.30,0.27,0.24))
wood_d  = mat('wood_dark', (0.27,0.20,0.13))
cab_m   = mat('cab', (0.14,0.12,0.11))
horse_m = mat('horse', (0.30,0.22,0.16))

COATS = [(0.14,0.13,0.15),(0.22,0.18,0.14),(0.30,0.22,0.15),(0.18,0.22,0.28),(0.35,0.26,0.17),(0.25,0.17,0.13)]
DRESSES = [(0.45,0.30,0.32),(0.32,0.38,0.44),(0.40,0.33,0.22),(0.30,0.42,0.34),(0.48,0.38,0.26),(0.38,0.30,0.42)]

# ---------- ground ----------
prim('box', 'CircusRoad', road_m, loc=(0, 1.0, -0.05), scale=(11.5, 10.5, 0.05))
prim('box', 'IslandPave', pave_m, loc=(0, -6.4, 0.01), scale=(11.5, 1.6, 0.06))

# ---------- curved frontages (3 angled segments per side) ----------
def frontage(name, side, seed):
    rnd = random.Random(seed)
    # quadrant arc: segments stand on a circle centred in front of the vista
    # (C=(0,-7), R=13.5) with facades pointing back toward the arc centre,
    # as the quadrant buildings of Regent Circus wrap around the viewer.
    C = (0.0, -7.0); R = 13.5
    segs = [(0.55, 6.0), (0.80, 7.0), (1.05, 6.6)]   # (arc angle, width) far -> near
    for k, (alpha, w) in enumerate(segs):
        cx = side * R * math.sin(alpha)
        cy = C[1] + R * math.cos(alpha)
        dirx, diry = -side * math.sin(alpha), -math.cos(alpha)   # facade direction (toward C)
        if side < 0:
            cz_rot = math.atan2(diry, dirx)          # facade is local +X
        else:
            cz_rot = math.atan2(diry, dirx) + math.pi  # facade is local -X
        parts = []
        h = 13.0
        parts.append(prim('box', f'{name}{k}_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
        parts.append(prim('box', f'{name}{k}_body', stucco if k % 2 == 0 else stucco2, loc=(0,0,h/2), scale=(0.95, w/2, h/2)))
        parts.append(prim('box', f'{name}{k}_cornice', stucco, loc=(side*-1.0, 0, h-0.4), scale=(0.18, w/2, 0.22)))
        parts.append(prim('box', f'{name}{k}_roof', roof_m, loc=(0.15*side, 0, h+0.5), scale=(1.15, w/2, 0.5)))
        fx = -side * 0.97  # local facade offset (toward street centre)
        # shopfront arcade at ground floor
        ncol = int(w / 1.15)
        for ci in range(ncol + 1):
            yy = -w/2 + ci * (w / ncol)
            parts.append(prim('cyl', f'{name}{k}_col', stucco, loc=(fx, yy, 1.7), r=0.11, d=3.4, verts=10))
        parts.append(prim('box', f'{name}{k}_shopdark', win_m, loc=(fx + side*0.35, 0, 1.7), scale=(0.5, w/2, 1.7)))
        parts.append(prim('box', f'{name}{k}_fascia', sign_m, loc=(fx - side*0.02, 0, 3.65), scale=(0.08, w/2, 0.3)))
        # balcony slab + railing at first floor
        parts.append(prim('box', f'{name}{k}_balc', stucco, loc=(fx - side*0.25, 0, 4.35), scale=(0.55, w/2, 0.10)))
        parts.append(prim('box', f'{name}{k}_rail', sign_m, loc=(fx - side*0.5, 0, 4.85), scale=(0.03, w/2, 0.45)))
        # window rows
        for f in range(3):
            z = 6.0 + f * 2.5
            cols = max(2, int(w / 1.3))
            for cix in range(cols):
                yy = -w/2 + (cix + 0.5) * (w / cols)
                parts.append(prim('box', f'{name}{k}_win', win_p if rnd.random() < 0.3 else win_m,
                                  loc=(fx - side*0.01, yy, z), scale=(0.03, 0.34, 0.66)))
        ob = join(parts, f'{name}{k}')
        ob.location = (cx, cy, 0)
        ob.rotation_euler = (0, 0, cz_rot)
        # balcony figures (world placed, approximated on the balcony line)
        import mathutils
        m = mathutils.Matrix.Rotation(cz_rot, 4, 'Z')
        nfig = 3 if k != 1 else 4
        for fi in range(nfig):
            yy = -w/2 + (fi + 0.7) * (w / (nfig + 0.4))
            lp = m @ mathutils.Vector((fx - side*0.28, yy, 0))
            f = figure(f'Balc{name}{k}_{fi}', h=rnd.uniform(1.55, 1.72),
                       dress='skirt' if fi % 2 else 'coat',
                       coat=rnd.choice(DRESSES if fi % 2 else COATS),
                       hat='bonnet' if fi % 2 else 'top', arm_l=0.35, arm_r=0.35)
            place(f, cx + lp.x, cy + lp.y, math.atan2(-dirx, diry), z=4.42)
frontage('FrontL', -1, 71)
frontage('FrontR', 1, 97)
# distant street vista behind (between the frontages, far +Y)
prim('box', 'VistaBlock', mat('vista', (0.48,0.46,0.44)), loc=(0, 12.5, 4.4), scale=(4.6, 1.0, 4.4))
prim('box', 'VistaBlock2', mat('vista', (0.44,0.42,0.40)), loc=(-3.6, 13.5, 4.2), scale=(1.8, 1.0, 4.2))
prim('box', 'VistaBlock3', mat('vista', (0.44,0.42,0.40)), loc=(3.8, 13.5, 4.4), scale=(1.7, 1.0, 4.4))

# ---------- banner across the circus (blank cloth, sagging) ----------
def banner_mesh():
    A = (-7.3, 4.6, 10.4); B = (7.3, 4.6, 10.4)
    nu, nv = 14, 2
    verts, faces = [], []
    for i in range(nu+1):
        s = i/nu
        x = A[0] + (B[0]-A[0])*s
        z = A[2] - math.sin(math.pi*s)*1.15
        for j in range(nv+1):
            zz = z - (j/nv)*1.35 + math.sin(math.pi*s)*0.15*(j/nv)
            verts.append((x, A[1] + math.sin(math.pi*s)*0.1, zz))
    for i in range(nu):
        for j in range(nv):
            a = i*(nv+1)+j; b = a+nv+1
            faces.append((a, b, a+1)); faces.append((b, b+1, a+1))
    me = bpy.data.meshes.new('BannerMesh')
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new('Banner', me)
    model_coll.objects.link(ob)
    me.materials.append(banner_m)
    return ob
banner_mesh()
# laurel festoons at banner ends (simple dark green swags)
for sx in (-7.3, 7.3):
    prim('sph', 'Festoon', mat('laurel', (0.22,0.30,0.18)), loc=(sx, 4.6, 10.1), scale=(0.5,0.25,0.7), r=0.5)
# flags hanging at the sides
for sx, sy in ((-7.2, 4.4), (7.2, 4.4), (-8.6, 1.8), (8.6, 1.8)):
    prim('cyl', 'FlagPole', wood_d, loc=(sx, sy, 9.4), r=0.03, d=2.6)
    prim('box', 'Flag', mat('flag', (0.55,0.3,0.28)), loc=(sx + (0.3 if sx < 0 else -0.3), sy, 10.3), scale=(0.3, 0.02, 0.45))

# ---------- hansom cabs hemmed in the crowd ----------
def cab(name, x, y, rotz):
    parts = []
    parts.append(prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    parts.append(prim('box', name+'_body', cab_m, loc=(0,0,1.30), scale=(0.85, 0.62, 0.62)))
    parts.append(prim('box', name+'_roof', cab_m, loc=(0,0,2.05), scale=(0.8, 0.55, 0.08)))
    parts.append(prim('box', name+'_win', win_p, loc=(0, 0.63, 1.45), scale=(0.3, 0.02, 0.3)))
    parts.append(prim('box', name+'_shaft', wood_d, loc=(1.35, 0.22, 0.9), scale=(0.55, 0.03, 0.03), rot=(0, 0.12, 0)))
    parts.append(prim('box', name+'_shaft2', wood_d, loc=(1.35, -0.22, 0.9), scale=(0.55, 0.03, 0.03), rot=(0, 0.12, 0)))
    # driver perched behind/above
    ob = join(parts, name)
    ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rotz)
    import mathutils
    m = mathutils.Matrix.Rotation(rotz, 4, 'Z')
    for (lx, ly, R) in ((0.55, 0.68, 0.52), (0.55, -0.68, 0.52), (-0.6, 0.68, 0.52), (-0.6, -0.68, 0.52)):
        wp = m @ mathutils.Vector((lx, ly, 0))
        parts2 = []
        parts2.append(prim('torus', name+'_rim', wood_d, loc=(0,0,0), R=R, r=0.045, rot=(0, math.pi/2, 0)))
        parts2.append(prim('cyl', name+'_hub', wood_d, loc=(0,0,0), r=0.07, d=0.09, rot=(0, math.pi/2, 0)))
        w = join(parts2, name+f'_wheel{lx}{ly}')
        w.location = (x + wp.x, y + wp.y, R); w.rotation_euler = (0, 0, rotz)
    # horse
    hp = m @ mathutils.Vector((2.45, 0, 0))
    parts3 = []
    parts3.append(prim('box', name+'_hroot', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    parts3.append(prim('sph', name+'_hbody', horse_m, loc=(0,0,1.15), scale=(1.0,0.33,0.35), r=0.6))
    parts3.append(prim('box', name+'_hneck', horse_m, loc=(0.6,-0.02,1.45), scale=(0.15,0.10,0.28), rot=(0,0.6,0)))
    parts3.append(prim('box', name+'_hhead', horse_m, loc=(0.83,-0.02,1.58), scale=(0.21,0.085,0.10), rot=(0,0.35,0)))
    for lx in (-0.4, 0.4):
        for ly in (-0.15, 0.15):
            parts3.append(prim('cyl', name+'_hleg', horse_m, loc=(lx,ly,0.48), r=0.045, d=0.96, verts=8))
    h = join(parts3, name+'_horse')
    h.location = (x + hp.x, y + hp.y, 0); h.rotation_euler = (0, 0, rotz)
    # driver figure on the box
    d = figure(name+'_driver', h=1.66, coat=(0.13,0.12,0.13), hat='top')
    dp = m @ mathutils.Vector((-0.7, 0, 0))
    place(d, x + dp.x, y + dp.y, rotz + math.pi/2, z=1.97)
cab('CabA', -3.1, -1.8, 2.75)
cab('CabB', 3.6, 1.2, -2.5)

# ---------- the crowd ----------
rnd = random.Random(1234)
spots = []
# dense foreground + mid street
for i in range(36):
    for _try in range(20):
        x = rnd.uniform(-6.2, 6.2); y = rnd.uniform(-7.4, 4.8)
        if any((x-sx)**2 + (y-sy)**2 < 0.55**2 for sx, sy in spots): continue
        if (-4.6 < x < -1.6 and -3.4 < y < -0.2) or (2.1 < x < 5.1 and -0.4 < y < 2.8): continue  # cab space
        spots.append((x, y)); break
for i, (x, y) in enumerate(spots):
    fem = rnd.random() < 0.45
    f = figure(f'Crowd{i}', h=rnd.uniform(1.5, 1.78),
               dress='skirt' if fem else 'coat',
               coat=rnd.choice(DRESSES if fem else COATS),
               hat='bonnet' if fem else rnd.choice(['top','top','cap']),
               shawl=rnd.choice([(0.4,0.35,0.3),(0.35,0.3,0.35)]) if fem and rnd.random() < 0.5 else None,
               arm_l=rnd.uniform(0, 0.9), arm_r=rnd.uniform(0, 0.9))
    place(f, x, y, rnd.uniform(0, 6.28))
# a few placard carriers ("TO THE EXHIBITION" boards left blank)
for i, (x, y) in enumerate(((-1.2, -3.4), (1.8, -4.6), (0.2, 2.8))):
    prim('cyl', f'PlacardPole{i}', wood_d, loc=(x, y, 1.5), r=0.018, d=1.9)
    prim('box', f'Placard{i}', banner_m, loc=(x, y, 2.6), scale=(0.42, 0.02, 0.3), rot=(0, 0, rnd.uniform(-0.1, 0.1)))
# crowd mass (fix round): the bare cylinder-and-ball blocks were replaced by
# instanced low-poly FIGURE variants in the batch house style — tapered
# coat/skirt body mass, head, and hat (top hat / cap / bonnet / shawl) —
# four types in three colourways each, placed as shared-mesh copies on
# staggered rows so the street reads as a packed sea of people.
def crowd_proto(name, kind, coat_rgb, hat_rgb=(0.09, 0.09, 0.10)):
    coat_m = mat('cp_' + name, coat_rgb)
    hat_m = mat('ch_' + name, hat_rgb)
    skin_m = mat('crowdskin', (0.82, 0.63, 0.50))
    parts = []
    parts.append(prim('box', name + '_root', None, loc=(0, 0, 0.01), scale=(0.01, 0.01, 0.01)))
    if kind in ('bonnet', 'shawl'):
        parts.append(prim('cone', name + '_skirt', coat_m, loc=(0, 0, 0.65), r1=0.215, r2=0.088, d=1.30, verts=6))
        if kind == 'shawl':
            parts.append(prim('cone', name + '_shawl', hat_m, loc=(0, 0, 1.17), r1=0.165, r2=0.07, d=0.34, verts=6))
    else:
        parts.append(prim('cone', name + '_coat', coat_m, loc=(0, 0, 0.65), r1=0.185, r2=0.10, d=1.30, verts=6))
    parts.append(prim('sph', name + '_head', skin_m, loc=(0, 0, 1.42), r=0.105, seg=6, rings=3))
    if kind == 'tophat':
        parts.append(prim('cyl', name + '_brim', hat_m, loc=(0, 0, 1.505), r=0.135, d=0.02, verts=6))
        parts.append(prim('cyl', name + '_crown', hat_m, loc=(0, 0, 1.585), r=0.088, d=0.15, verts=6))
    elif kind == 'cap':
        parts.append(prim('cone', name + '_cap', hat_m, loc=(0, 0, 1.51), r1=0.115, r2=0.05, d=0.07, verts=6))
    elif kind in ('bonnet', 'shawl'):
        parts.append(prim('sph', name + '_bonnet', hat_m, loc=(0, -0.02, 1.45), scale=(1.0, 1.05, 0.95), r=0.115, seg=6, rings=3))
    return join(parts, name)

CROWD_PROTOS = []
for ci, c in enumerate([(0.16, 0.14, 0.16), (0.24, 0.19, 0.14), (0.19, 0.23, 0.29)]):
    CROWD_PROTOS.append(crowd_proto(f'CPtop{ci}', 'tophat', c))
    CROWD_PROTOS.append(crowd_proto(f'CPcap{ci}', 'cap', c, hat_rgb=(0.20, 0.17, 0.14)))
for ci, c in enumerate([(0.44, 0.31, 0.33), (0.33, 0.38, 0.43), (0.41, 0.34, 0.23)]):
    CROWD_PROTOS.append(crowd_proto(f'CPbon{ci}', 'bonnet', c, hat_rgb=(0.30, 0.26, 0.24)))
    CROWD_PROTOS.append(crowd_proto(f'CPshw{ci}', 'shawl', c, hat_rgb=(0.38, 0.33, 0.28)))

def crowd_slots():
    slots = []
    # mid-ground: staggered rows, shoulder to shoulder across the street
    for ri in range(8):
        y = 1.05 + ri * 0.60
        x = -5.3 + (0.29 if ri % 2 else 0.0)
        while x <= 5.3:
            jx = x + rnd.uniform(-0.10, 0.10); jy = y + rnd.uniform(-0.09, 0.09)
            x += 0.58
            if 1.85 < jx < 5.35 and -0.7 < jy < 3.05: continue   # CabB space
            if -4.8 < jx < -1.4 and -3.6 < jy < 0.05: continue   # CabA space
            if abs(jx) > 4.55 and rnd.random() < 0.3: continue   # thin at frame edges
            if any((jx - sx) ** 2 + (jy - sy) ** 2 < 0.36 ** 2 for sx, sy in spots): continue
            if (jx - 0.2) ** 2 + (jy - 2.8) ** 2 < 0.32 ** 2: continue  # placard carrier
            slots.append((jx, jy))
    # distant crowd down the vista street: tighter rows between the vista blocks
    for ri in range(5):
        y = 6.2 + ri * 0.68
        x = -3.2 + (0.32 if ri % 2 else 0.0)
        while x <= 3.2:
            jx = x + rnd.uniform(-0.10, 0.10); jy = y + rnd.uniform(-0.09, 0.09)
            x += 0.64
            slots.append((jx, jy))
    return slots

_crowd = crowd_slots()
for i, (x, y) in enumerate(_crowd):
    if i < len(CROWD_PROTOS):
        ob = CROWD_PROTOS[i]
    else:
        ob = rnd.choice(CROWD_PROTOS).copy()
        model_coll.objects.link(ob)
    s = rnd.uniform(0.93, 1.05)
    ob.scale = (s, s, s * rnd.uniform(0.96, 1.06))
    ob.location = (x, y, 0)
    ob.rotation_euler = (0, 0, rnd.uniform(-0.7, 0.7) + (math.pi if rnd.random() < 0.25 else 0))
print("CROWD:", len(_crowd))

# ---------- lamps ----------
for (lx, ly) in ((-6.2, -5.5), (6.2, -5.5)):
    prim('cyl', f'Lamp{lx}', mat('iron', (0.12,0.12,0.13), 0.5), loc=(lx, ly, 1.9), r=0.05, d=3.8)
    prim('box', f'LampHead{lx}', mat('iron', (0.12,0.12,0.13), 0.5), loc=(lx, ly, 3.95), scale=(0.15, 0.15, 0.24))

# ---------- render setup ----------
def look_at(ob, target):
    import mathutils
    d = mathutils.Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
setup_coll.objects.link(cam)
cam.location = (0, -13.5, 8.5)
look_at(cam, (0, 3.5, 3.4))
cam.data.lens = 34
bpy.context.scene.camera = cam
sun_d = bpy.data.lights.new('Sun', 'SUN'); sun_d.energy = 2.7; sun_d.angle = 0.5
sun = bpy.data.objects.new('Sun', sun_d); setup_coll.objects.link(sun)
sun.rotation_euler = (math.radians(52), math.radians(6), math.radians(-8))
fill_d = bpy.data.lights.new('Fill', 'AREA'); fill_d.energy = 520; fill_d.shape = 'DISK'; fill_d.size = 6
fill = bpy.data.objects.new('Fill', fill_d); setup_coll.objects.link(fill)
fill.location = (-5, -9, 8); look_at(fill, (0, 2, 1.5))

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 1024; sc.render.resolution_y = 720
sc.world = bpy.data.worlds.new('W')
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.53, 0.53, 0.53, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.8

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
