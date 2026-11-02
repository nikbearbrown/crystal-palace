#!/usr/bin/env python3
"""scan-fig42-looking-for-lodgings — Muse version.
Cruikshank 'Looking for lodgings' (Mayhew's Sandboys): cramped cellar lodging.
Run: blender -b --python build_scan_fig42_looking_for_lodgings.py
"""
import bpy, math, os
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig42-looking-for-lodgings"

# ---------- scene reset ----------
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
    elif kind == 'torus': bpy.ops.mesh.primitive_torus_add(major_segments=20, minor_segments=8, major_radius=kw.get('R',0.5), minor_radius=kw.get('r',0.08))
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
    return ob

# ---------- stylised figure ----------
def figure(name, h=1.68, dress='coat', coat=(0.16,0.15,0.17), lower=(0.25,0.22,0.2),
           skin=(0.85,0.65,0.52), hat='top', hat_col=(0.08,0.08,0.09),
           arm_l=0.15, arm_r=0.15, arm_lz=0.12, arm_rz=-0.12, lean=0.0, leg_spread=0.0, shawl=None):
    parts = []
    root = prim('box', name+'_root', None, loc=(0,0,0.01), scale=(0.01,0.01,0.01))
    parts.append(root)
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
        # coat skirt flare
        parts.append(prim('cone', name+'_coatsk', coat_m, loc=(0,0,h*0.44), r1=h*0.115, r2=h*0.095, d=h*0.14))
    for s, ang, angz in ((-1, arm_l, arm_lz), (1, arm_r, arm_rz)):
        parts.append(prim('cyl', name+'_arm', coat_m, loc=(s*h*0.125, 0, h*0.615), r=h*0.028, d=h*0.34,
                          rot=(ang, 0, angz + (0.10 if s<0 else -0.10))))
        parts.append(prim('sph', name+'_hand', skin_m, loc=(s*h*(0.125+0.10*math.sin(angz)*-1), -math.sin(ang)*h*0.16, h*0.615-math.cos(ang)*h*0.17), r=h*0.028))
    parts.append(prim('sph', name+'_head', skin_m, loc=(0,0,h*0.905), scale=(0.92,0.98,1.06), r=h*0.068))
    hz = h*0.965
    if hat == 'top':
        parts.append(prim('cyl', name+'_brim', hat_m, loc=(0,0,hz), r=h*0.085, d=0.012))
        parts.append(prim('cyl', name+'_crown', hat_m, loc=(0,0,hz+h*0.05), r=h*0.058, d=h*0.10))
    elif hat == 'bonnet':
        parts.append(prim('sph', name+'_bonnet', hat_m, loc=(0,-h*0.018,h*0.925), scale=(1.0,1.05,0.95), r=h*0.075))
        parts.append(prim('cyl', name+'_bbrim', hat_m, loc=(0,h*0.045,h*0.955), r=h*0.07, d=0.01, rot=(0.5,0,0)))
    elif hat == 'cap':
        parts.append(prim('cone', name+'_cap', hat_m, loc=(0,0,h*0.965), r1=h*0.075, r2=h*0.045, d=h*0.05))
    elif hat == 'hair':
        parts.append(prim('sph', name+'_hair', mat('hair', (0.16,0.13,0.11)), loc=(0,-h*0.012,h*0.922), scale=(1.02,1.06,0.92), r=h*0.072))
    elif hat == 'broad':
        parts.append(prim('cyl', name+'_brim', hat_m, loc=(0,0,hz), r=h*0.105, d=0.012))
        parts.append(prim('sph', name+'_crown', hat_m, loc=(0,0,hz+0.01), scale=(1,1,0.55), r=h*0.062))
    ob = join(parts, name)
    ob.rotation_euler = (lean, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return ob

def place(ob, x, y, rotz=0.0):
    ob.location = (x, y, 0)
    ob.rotation_euler = (0, 0, rotz)
    return ob

# ---------- materials ----------
brick  = mat('brick', (0.42,0.30,0.24))
brick_d= mat('brick_dark', (0.38,0.27,0.21))
plaster= mat('plaster', (0.62,0.58,0.52))
wood   = mat('wood', (0.36,0.26,0.17))
wood_d = mat('wood_dark', (0.25,0.18,0.12))
floor_m= mat('floor', (0.38,0.33,0.28))
cloth  = mat('cloth_white', (0.78,0.76,0.70))
ham_m  = mat('hammock', (0.40,0.37,0.33))
blanket= mat('blanket', (0.30,0.24,0.28))
rug_m  = mat('rug', (0.42,0.22,0.18))
metal  = mat('metal', (0.35,0.35,0.38), 0.5)
candle_m = mat('candle', (0.92,0.88,0.78))

# ---------- room shell ----------
W, D, SPRING, RISE = 5.2, 3.8, 1.95, 1.15   # width, depth, vault springing height, rise
# floor
prim('box', 'Floor', floor_m, loc=(0,0,-0.05), scale=(W/2, D/2, 0.05))
# back wall (brick) with subtle courses
prim('box', 'BackWall', brick, loc=(0, D/2, 1.65), scale=(W/2, 0.09, 1.68))
for i in range(8):
    prim('box', 'Course', brick_d, loc=(0, D/2-0.095, 0.35+i*0.38), scale=(W/2, 0.012, 0.02))
# side walls
prim('box', 'WallL', brick, loc=(-W/2, 0, 1.0), scale=(0.09, D/2, 1.0))
prim('box', 'WallR', brick, loc=( W/2, 0, 1.0), scale=(0.09, D/2, 1.0))
# barrel vault (custom arc-extruded shell)
def vault_mesh():
    import math as m
    R = ((W/2)**2 + RISE**2) / (2*RISE)
    cz = SPRING + RISE - R
    segs = 16
    verts, faces = [], []
    for y in (-D/2, D/2):
        for i in range(segs+1):
            x = -W/2 + W*i/segs
            z = cz + m.sqrt(max(R*R - x*x, 0.0))
            verts.append((x, y, z))
    for i in range(segs):
        a, b, c, d = i, i+1, i+segs+1, i+segs+2
        faces.append((a, b, c)); faces.append((b, d, c))
    me = bpy.data.meshes.new('VaultMesh')
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new('Vault', me)
    model_coll.objects.link(ob)
    me.materials.append(brick_d)
    if me.polygons[0].normal.z > 0: me.flip_normals()
    for poly in me.polygons: poly.use_smooth = True
    return ob
vault_mesh()
# gable infill above side walls is omitted (open section, as a stage vignette)

# ---------- doorway (left wall, raised, door ajar) ----------
prim('box', 'DoorStep', wood_d, loc=(-W/2+0.28, 0.55, 0.16), scale=(0.42, 0.45, 0.16))
prim('box', 'DoorFrameT', wood_d, loc=(-W/2+0.02, 0.55, 2.02), scale=(0.10, 0.52, 0.08))
door = prim('box', 'Door', wood, loc=(-W/2+0.30, 0.24, 1.13), scale=(0.035, 0.42, 0.79), rot=(0,0,0.5))
prim('box', 'DoorGlow', mat('door_light', (0.58,0.53,0.44)), loc=(-W/2+0.10, 0.55, 1.15), scale=(0.02, 0.40, 0.80))

# ---------- hammock slung diagonally ----------
def hammock_mesh():
    A = (-1.60, 0.80, 2.85); B = (2.55, -0.50, 2.10)
    import math as m
    nu, nv = 10, 4
    verts, faces = [], []
    ax = (B[0]-A[0], B[1]-A[1], B[2]-A[2])
    # perpendicular (horizontal) for width
    L = m.sqrt(ax[0]**2 + ax[1]**2)
    px, py = -ax[1]/L, ax[0]/L
    for i in range(nu+1):
        s = i/nu
        cx, cy, cz = A[0]+ax[0]*s, A[1]+ax[1]*s, A[2]+ax[2]*s
        sag = m.sin(m.pi*s)*0.60
        for j in range(nv+1):
            w = j/nv - 0.5
            z = cz - sag - (1-(2*w)**2)*0.10
            verts.append((cx + px*w*1.05, cy + py*w*1.05, z))
    for i in range(nu):
        for j in range(nv):
            a = i*(nv+1)+j; b = a+nv+1
            faces.append((a, b, a+1)); faces.append((b, b+1, a+1))
    me = bpy.data.meshes.new('HammockMesh')
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new('Hammock', me)
    model_coll.objects.link(ob)
    me.materials.append(ham_m)
    for poly in me.polygons: poly.use_smooth = True
    # dark bedding mass in the hammock
    return ob
hammock_mesh()
# gathered rope ends
prim('cyl', 'RopeA', ham_m, loc=(-1.78, 0.86, 2.94), r=0.02, d=0.45, rot=(1.1, 0, 0.7))
prim('cyl', 'RopeB', ham_m, loc=(2.58, -0.55, 2.20), r=0.02, d=0.3, rot=(1.2, 0, -0.4))
prim('box', 'HammockBedding', blanket, loc=(0.48, 0.15, 1.90), scale=(0.80, 0.30, 0.05), rot=(0, 0.16, -0.30))

# ---------- furniture ----------
# bed along back-right wall
prim('box', 'BedFrame', wood_d, loc=(1.45, 1.42, 0.24), scale=(0.95, 0.42, 0.24))
prim('box', 'BedMattress', cloth, loc=(1.45, 1.42, 0.52), scale=(0.92, 0.40, 0.09))
prim('box', 'BedBlanket', mat('bed_blanket', (0.45,0.32,0.26)), loc=(1.62, 1.42, 0.56), scale=(0.70, 0.41, 0.07))
prim('box', 'Pillow', cloth, loc=(0.68, 1.42, 0.58), scale=(0.16, 0.30, 0.06))
prim('box', 'BedHead', wood_d, loc=(0.48, 1.42, 0.55), scale=(0.05, 0.42, 0.55))
# small table + chair centre
prim('box', 'TableTop', wood, loc=(0.0, 0.38, 0.72), scale=(0.42, 0.30, 0.025))
for dx in (-0.36, 0.36):
    for dy in (-0.24, 0.24):
        prim('cyl', 'TableLeg', wood_d, loc=(0.0+dx, 0.38+dy, 0.36), r=0.022, d=0.72)
prim('box', 'ChairSeat', wood, loc=(0.38, 0.30, 0.46), scale=(0.19, 0.18, 0.025))
prim('box', 'ChairBack', wood, loc=(0.38, 0.50, 0.72), scale=(0.19, 0.025, 0.28))
for dx in (-0.17, 0.17):
    for dy in (-0.16, 0.16):
        prim('cyl', 'ChairLeg', wood_d, loc=(0.38+dx*0.85, 0.30+dy*0.85, 0.23), r=0.018, d=0.46)
# two small stools foreground
for (sx, sy, rz) in ((0.8, -1.05, 0.2), (1.32, -0.82, -0.35)):
    prim('box', 'StoolTop', wood, loc=(sx, sy, 0.34), scale=(0.26, 0.13, 0.03), rot=(0,0,rz))
    for dx in (-0.2, 0.2):
        prim('cyl', 'StoolLeg', wood_d, loc=(sx+dx*math.cos(rz), sy+dx*math.sin(rz), 0.16), r=0.02, d=0.33)
# barrel washstand right, with jug and basin
prim('cyl', 'Barrel', wood, loc=(2.18, 0.95, 0.38), r=0.30, d=0.76)
prim('torus', 'Hoop1', metal, loc=(2.18, 0.95, 0.18), R=0.305, r=0.012, rot=(math.pi/2,0,0))
prim('torus', 'Hoop2', metal, loc=(2.18, 0.95, 0.6), R=0.30, r=0.012, rot=(math.pi/2,0,0))
prim('box', 'WashBoard', wood_d, loc=(2.18, 0.95, 0.79), scale=(0.36, 0.36, 0.03))
prim('cyl', 'Basin', mat('tin', (0.6,0.62,0.65), 0.4), loc=(2.05, 0.88, 0.85), r=0.16, d=0.09)
prim('cyl', 'JugBody', cloth, loc=(2.38, 1.05, 0.90), r=0.07, d=0.16)
prim('torus', 'JugHandle', cloth, loc=(2.47, 1.05, 0.93), R=0.05, r=0.012, rot=(0, math.pi/2, 0))
# rug centre floor
prim('box', 'Rug', rug_m, loc=(0.35, -0.15, 0.012), scale=(0.85, 0.60, 0.012), rot=(0,0,0.06))
# small framed picture on back wall
prim('box', 'Picture', wood_d, loc=(-0.35, D/2-0.11, 1.62), scale=(0.16, 0.015, 0.21))
prim('box', 'PictureIn', mat('pic_in', (0.66,0.63,0.56)), loc=(-0.35, D/2-0.125, 1.62), scale=(0.12, 0.008, 0.16))

# ---------- figures ----------
# tall man ducking in the doorway
f = figure('ManDoor', h=1.80, dress='coat', coat=(0.13,0.12,0.13), lower=(0.30,0.27,0.24), hat='top', lean=0.5, arm_l=0.3, arm_r=0.2)
place(f, -2.02, 0.45, -1.75)
# bonneted woman behind him
f = figure('WomanDoor', h=1.62, dress='skirt', coat=(0.28,0.22,0.20), hat='bonnet', shawl=(0.35,0.28,0.22), arm_l=0.25, arm_r=0.25)
place(f, -1.78, 0.38, -1.9)
# cloaked man with cane
f = figure('ManCloak', h=1.74, dress='coat', coat=(0.20,0.17,0.15), lower=(0.55,0.50,0.44), hat='top', arm_r=0.55, arm_l=0.1)
place(f, -1.15, 0.02, -1.85)
prim('cyl', 'Cane', wood_d, loc=(-0.94, 0.30, 0.42), r=0.012, d=0.85, rot=(0.12,0,0.05))
# woman with umbrella
f = figure('WomanUmb', h=1.64, dress='skirt', coat=(0.24,0.26,0.30), hat='bonnet', shawl=(0.30,0.26,0.24), arm_r=0.5)
place(f, -0.62, -0.06, -1.95)
prim('cone', 'Umbrella', mat('umb', (0.15,0.14,0.16)), loc=(-0.28, -0.30, 0.48), r1=0.05, r2=0.010, d=0.72, rot=(0.55, 0, -0.35))
# landlady with candlestick, arm raised toward hammock
f = figure('Landlady', h=1.66, dress='skirt', coat=(0.22,0.19,0.20), hat='hair', arm_l=0.55, arm_r=2.5, arm_rz=-0.15)
place(f, 1.45, -0.35, 2.0)
prim('cyl', 'Candlestick', metal, loc=(1.16, -0.50, 0.90), r=0.045, d=0.05)
prim('cyl', 'Candle', candle_m, loc=(1.16, -0.50, 1.00), r=0.014, d=0.16)
flame = prim('sph', 'Flame', mat('flame', (1.0,0.75,0.35), 0.3), loc=(1.16, -0.50, 1.12), scale=(0.6,0.6,1.3), r=0.02)
flame.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1.0, 0.6, 0.2, 1.0)
flame.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.0

# front header (gable flat) closing the vault mouth at the top of frame
prim('box', 'FrontHeader', brick_d, loc=(0, -D/2-0.06, 3.15), scale=(W/2+0.1, 0.06, 0.72))

# ---------- render setup ----------
def look_at(ob, target):
    import mathutils
    d = mathutils.Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
setup_coll.objects.link(cam)
cam.location = (0.4, -6.4, 1.85)
look_at(cam, (0, 0.4, 1.15))
cam.data.lens = 44
bpy.context.scene.camera = cam
sun_d = bpy.data.lights.new('Sun', 'SUN'); sun_d.energy = 2.6; sun_d.angle = 0.4
sun = bpy.data.objects.new('Sun', sun_d); setup_coll.objects.link(sun)
sun.rotation_euler = (math.radians(55), math.radians(10), math.radians(-35))
fill_d = bpy.data.lights.new('Fill', 'AREA'); fill_d.energy = 350; fill_d.shape = 'DISK'; fill_d.size = 5
fill = bpy.data.objects.new('Fill', fill_d); setup_coll.objects.link(fill)
fill.location = (-2.5, -3.5, 3.2); look_at(fill, (0, 0.5, 1.0))
pt_d = bpy.data.lights.new('CandleLight', 'POINT'); pt_d.energy = 6; pt_d.color = (1.0, 0.72, 0.42)
pt = bpy.data.objects.new('CandleLight', pt_d); setup_coll.objects.link(pt)
pt.location = (1.16, -0.50, 1.15)

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 24
sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 720
sc.world = bpy.data.worlds.new('W')
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

# ---------- save, render, export ----------
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
