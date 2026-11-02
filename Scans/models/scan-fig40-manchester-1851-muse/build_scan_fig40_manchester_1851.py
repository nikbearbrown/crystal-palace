#!/usr/bin/env python3
"""scan-fig40-manchester-1851 — Muse version.
Cruikshank 'Manchester in 1851': the DESERTED street — everyone has
gone to the Great Exhibition. Terraced frontages, shop signs, lamps,
and emptiness.
Run: blender -b --python build_scan_fig40_manchester_1851.py
"""
import bpy, math, os, random
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig40-manchester-1851"
random.seed(40)

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
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, radius=kw.get('r',0.5))
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

# ---------- materials ----------
brick_a = mat('brick_a', (0.36,0.27,0.22))
brick_b = mat('brick_b', (0.30,0.23,0.19))
brick_c = mat('brick_c', (0.42,0.33,0.26))
stone   = mat('stone', (0.55,0.52,0.47))
win_m   = mat('window', (0.13,0.15,0.18), 0.35)
win_lit = mat('window_pale', (0.45,0.47,0.45), 0.5)
sign_m  = mat('sign_board', (0.72,0.68,0.60))
sign_d  = mat('sign_dark', (0.25,0.22,0.20))
road_m  = mat('road', (0.40,0.38,0.35))
pave_m  = mat('pavement', (0.52,0.50,0.46))
roof_m  = mat('roof', (0.22,0.21,0.23))
iron_m  = mat('iron', (0.12,0.12,0.13), 0.5)
far_m   = mat('far_silhouette', (0.38,0.36,0.36))

SHOP_SIGNS = 0  # blank boards only — no lettering is modelled

def building(name, cx, cy, w, d, h, facade_x, brick, n_floors=4, shop=True, seed=1):
    """Terraced building; facade faces the street at x=facade_x (sign of cx)."""
    rnd = random.Random(seed)
    parts = []
    parts.append(prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    parts.append(prim('box', name+'_body', brick, loc=(0,0,h/2), scale=(d/2, w/2, h/2)))
    # pitched roof (prism: 4-sided cone squashed)
    parts.append(prim('cone', name+'_roof', roof_m, loc=(0,0,h+1.2), r1=d*0.62, r2=0.06, d=2.4, verts=4, rot=(0,0,math.pi/4), scale=(0.75,0.85,1.0)))
    # chimney
    parts.append(prim('box', name+'_chim', brick, loc=(rnd.uniform(-d/4,d/4), rnd.uniform(-w/4,w/4), h+2.15), scale=(0.4,0.4,0.75)))
    fx = facade_x - cx  # local x of facade plane
    side = 1 if fx > 0 else -1
    # windows: rows of pale/dark insets on the facade
    for f in range(n_floors):
        z = 2.1 + f*2.35
        if z > h - 0.8: break
        cols = max(2, int(w / 1.35))
        for cix in range(cols):
            y = -w/2 + (cix + 0.5) * (w / cols)
            wm = win_lit if rnd.random() < 0.25 else win_m
            parts.append(prim('box', name+'_win', wm, loc=(fx + side*0.03, y, z), scale=(0.03, 0.33, 0.62)))
            parts.append(prim('box', name+'_sill', stone, loc=(fx + side*0.04, y, z-0.72), scale=(0.05, 0.42, 0.06)))
    if shop:
        # shopfront: recessed dark opening + fascia board
        parts.append(prim('box', name+'_shop', win_m, loc=(fx + side*0.02, 0, 0.95), scale=(0.03, w*0.36, 0.95)))
        parts.append(prim('box', name+'_fascia', sign_d, loc=(fx + side*0.06, 0, 2.15), scale=(0.05, w*0.42, 0.28)))
        # hanging sign board (blank)
        parts.append(prim('box', name+'_sign', sign_m, loc=(fx + side*0.35, w*0.28, 2.9), scale=(0.04, 0.55, 0.4)))
        parts.append(prim('cyl', name+'_signarm', iron_m, loc=(fx + side*0.18, w*0.28, 3.15), r=0.02, d=0.4, rot=(0, math.pi/2, 0)))
    else:
        parts.append(prim('box', name+'_door', sign_d, loc=(fx + side*0.03, w*0.2, 0.95), scale=(0.03, 0.45, 0.95)))
        # pasted poster boards (blank) — the 'GONE TO THE EXHIBITION' bills are left blank
        for k in range(2):
            parts.append(prim('box', name+'_poster', sign_m, loc=(fx + side*0.03, -w*0.25 + k*w*0.22, 1.5), scale=(0.02, 0.5, 0.7)))
    ob = join(parts, name)
    ob.location = (cx, cy, 0)
    return ob

# ---------- street layout: converging rows ----------
# street runs along Y; camera at -Y. Rows step away and narrow.
rows = [
    # (cy, half_width_of_street, height scale)
    (-6.0, 5.6, 1.00), (-0.5, 5.2, 0.97), (5.0, 4.9, 0.94), (10.5, 4.6, 0.90), (16.0, 4.3, 0.86),
]
seed = 100
for i, (cy, hw, hs) in enumerate(rows):
    w = 5.4
    hl = (13.5 - i*0.9) * hs
    hr = (12.5 - i*0.7) * hs
    building(f'BldL{i}', -(hw + 2.6), cy, w, 5.2, hl, -hw, [brick_a, brick_b, brick_c][i % 3],
             n_floors=4 if i < 3 else 3, shop=(i < 3), seed=seed + i)
    building(f'BldR{i}', (hw + 2.6), cy, w, 5.2, hr, hw, [brick_b, brick_c, brick_a][i % 3],
             n_floors=4 if i < 3 else 3, shop=(i != 1), seed=seed + 40 + i)

# road + pavements as continuous ribbons following the street's narrowing
def strip(name, mats, stations, z):
    # stations: list of (y, x_left, x_right)
    verts, faces = [], []
    for (y, xl, xr) in stations:
        verts.append((xl, y, z)); verts.append((xr, y, z))
    for i in range(len(stations) - 1):
        a = i * 2
        faces.append((a, a + 1, a + 2)); faces.append((a + 1, a + 3, a + 2))
    me = bpy.data.meshes.new(name + 'Mesh')
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me)
    model_coll.objects.link(ob)
    if mats: me.materials.append(mats)
    return ob
_st = [(-9.4, 5.75), (-6.0, 5.6), (-0.5, 5.2), (5.0, 4.9), (10.5, 4.6), (16.0, 4.3), (19.6, 4.15)]
strip('Road', road_m, [(y, -hw, hw) for (y, hw) in _st], 0.0)
strip('PaveL', pave_m, [(y, -hw - 1.12, -hw - 0.02) for (y, hw) in _st], 0.045)
strip('PaveR', pave_m, [(y, hw + 0.02, hw + 1.12) for (y, hw) in _st], 0.045)
# far end: closing block + chimney + spire silhouettes
prim('box', 'FarBlock', far_m, loc=(0, 21.5, 3.4), scale=(5.2, 1.2, 3.4))
prim('box', 'FarRoof1', far_m, loc=(-2.2, 21.5, 7.2), scale=(1.1, 1.0, 0.5))
prim('box', 'FarRoof2', far_m, loc=(0.6, 21.5, 7.5), scale=(0.9, 1.0, 0.7))
prim('box', 'FarRoof3', far_m, loc=(3.1, 21.5, 7.1), scale=(1.2, 1.0, 0.4))
prim('cyl', 'FarChimney', far_m, loc=(-3.4, 20.5, 7.5), r=0.5, d=11.0)
prim('cone', 'FarSpire', far_m, loc=(3.8, 20.2, 10.4), r1=0.8, r2=0.03, d=3.4)
prim('box', 'FarSpireBase', far_m, loc=(3.8, 20.2, 6.4), scale=(0.8, 0.8, 3.4))

# ---------- street lamps ----------
def lamp(name, x, y):
    parts = []
    parts.append(prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    parts.append(prim('cyl', name+'_post', iron_m, loc=(0,0,1.7), r=0.05, d=3.4))
    parts.append(prim('box', name+'_lantern', iron_m, loc=(0,0,3.55), scale=(0.14,0.14,0.22)))
    parts.append(prim('sph', name+'_glass', win_lit, loc=(0,0,3.55), r=0.09))
    parts.append(prim('cone', name+'_cap', iron_m, loc=(0,0,3.85), r1=0.17, r2=0.02, d=0.25))
    parts.append(prim('cyl', name+'_base', iron_m, loc=(0,0,0.25), r=0.11, d=0.5))
    ob = join(parts, name)
    ob.location = (x, y, 0)
    return ob
lamp('LampL0', -4.9, -8.5)
lamp('LampR0', 4.9, -3.5)
lamp('LampL1', -4.5, 2.0)
lamp('LampR1', 4.4, 7.5)
lamp('LampL2', -4.1, 12.5)

# ---------- the single distant figure (seated, right pavement) ----------
def figure(name, h=1.66, coat=(0.16,0.15,0.16), skin=(0.85,0.65,0.52)):
    parts = []
    parts.append(prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01)))
    cm = mat('fc', coat); sm = mat('fs', skin)
    # seated: torso upright, thighs horizontal, shins vertical
    parts.append(prim('cyl', name+'_torso', cm, loc=(0,0,h*0.62), r=h*0.095, d=h*0.38))
    for s in (-1, 1):
        parts.append(prim('cyl', name+'_thigh', cm, loc=(s*h*0.055, 0.14, h*0.30), r=h*0.035, d=h*0.28, rot=(math.pi/2.3,0,0)))
        parts.append(prim('cyl', name+'_shin', cm, loc=(s*h*0.055, 0.26, h*0.14), r=h*0.032, d=h*0.28))
        parts.append(prim('cyl', name+'_arm', cm, loc=(s*h*0.125, 0.02, h*0.58), r=h*0.027, d=h*0.32, rot=(0.25,0,0.12 if s<0 else -0.12)))
    parts.append(prim('sph', name+'_head', sm, loc=(0,0,h*0.885), scale=(0.92,0.98,1.06), r=h*0.068))
    parts.append(prim('cyl', name+'_brim', cm, loc=(0,0,h*0.945), r=h*0.085, d=0.012))
    parts.append(prim('cyl', name+'_crown', cm, loc=(0,0,h*0.995), r=h*0.058, d=h*0.10))
    return join(parts, name)

prim('box', 'Crate', mat('crate', (0.4,0.32,0.2)), loc=(4.35, 5.2, 0.28), scale=(0.3,0.3,0.28))
fig = figure('LoneFigure')
fig.location = (4.35, 5.15, 0.08)
fig.rotation_euler = (0, 0, -1.9)

# ---------- render setup ----------
def look_at(ob, target):
    import mathutils
    d = mathutils.Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
setup_coll.objects.link(cam)
cam.location = (0.6, -17.5, 7.5)
look_at(cam, (0, 6.0, 2.0))
cam.data.lens = 42
bpy.context.scene.camera = cam
sun_d = bpy.data.lights.new('Sun', 'SUN'); sun_d.energy = 2.4; sun_d.angle = 0.6
sun = bpy.data.objects.new('Sun', sun_d); setup_coll.objects.link(sun)
sun.rotation_euler = (math.radians(48), math.radians(12), math.radians(25))
fill_d = bpy.data.lights.new('Fill', 'AREA'); fill_d.energy = 350; fill_d.shape = 'DISK'; fill_d.size = 6
fill = bpy.data.objects.new('Fill', fill_d); setup_coll.objects.link(fill)
fill.location = (3, -8, 8); look_at(fill, (0, 4, 1))

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 760
sc.world = bpy.data.worlds.new('W')
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
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
