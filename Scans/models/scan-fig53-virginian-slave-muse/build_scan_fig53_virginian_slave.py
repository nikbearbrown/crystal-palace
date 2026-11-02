"""
Build script: scan-fig53-virginian-slave
John Tenniel, 'Virginian slave', Punch, 7 June 1851 — a British satirical
print aimed at American slavery, published during the Great Exhibition.
It parodies Powers' Greek Slave: an enslaved woman chained on a drum
pedestal inscribed 'E PLVRIBVS VNVM', leaning against a broken column
draped with the United States flag.
This model records the COMPOSITION with a simplified, dignified figure.
It deliberately does NOT reproduce the period engraving's caricatured
features. See NOTES.md for the full context statement.
Re-runnable: blender -b --python build_scan_fig53_virginian_slave.py
Scale: ESTIMATED monument scale (figure ~1.58 m; the print is a cartoon of
an imagined statue, so no real-world dimension exists).
"""
import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig53-virginian-slave"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

def make_mat(name, color, roughness=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

STONE = make_mat("PedestalStone", (0.62, 0.60, 0.57), roughness=0.8)
STONE_DARK = make_mat("PedestalStoneDark", (0.42, 0.40, 0.38), roughness=0.85)
BRONZE = make_mat("FigureBronzeDark", (0.145, 0.105, 0.085), roughness=0.62, metallic=0.35)
CLOTH = make_mat("ClothWrap", (0.52, 0.46, 0.40), roughness=0.9)
IRON = make_mat("ChainIron", (0.22, 0.21, 0.21), roughness=0.45, metallic=0.85)

def flag_texture():
    import numpy as np
    W, H = 256, 176
    img = bpy.data.images.new("USFlagTex", W, H)
    px = np.zeros((H, W, 4), dtype=np.float32)
    stripe_h = H / 13
    for y in range(H):
        band = int(y // stripe_h)
        col = (0.62, 0.16, 0.16) if band % 2 == 0 else (0.88, 0.86, 0.82)
        for x in range(W):
            px[y, x] = (*col, 1.0)
    # canton (upper hoist, drawn top-right of the texture for the drape)
    for y in range(int(H * 0.46), H):
        for x in range(int(W * 0.58), W):
            px[y, x] = (0.13, 0.16, 0.38, 1.0)
    for r in range(6):
        for c in range(7):
            cx = int(W * 0.615) + c * int(W * 0.055)
            cy = int(H * 0.515) + r * int(H * 0.072)
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if 0 <= cy + dy < H and 0 <= cx + dx < W:
                        px[cy + dy, cx + dx] = (0.92, 0.92, 0.9, 1.0)
    img.pixels.foreach_set(px.ravel())
    img.pack()
    return img

FLAG_MAT = make_mat("FlagCloth", (1, 1, 1), roughness=0.85)
FLAG_MAT.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 1, 1, 1)
_tex = FLAG_MAT.node_tree.nodes.new("ShaderNodeTexImage")
_tex.image = flag_texture()
FLAG_MAT.node_tree.links.new(_tex.outputs["Color"],
                             FLAG_MAT.node_tree.nodes["Principled BSDF"].inputs["Base Color"])

def link(ob, coll=model_coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def ball(name, loc, scale, mat=None, coll=None, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2 + 4,
                                         location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    for p in ob.data.polygons:
        p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll) if coll else ob

def cyl(name, loc, r, h, mat=None, vertices=32, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=h,
                                        location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll) if coll else ob

def box(name, loc, dims, mat, rot=(0, 0, 0), coll=model_coll):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def capsule(name, p1, p2, r, mat=None, coll=None):
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r,
                                        depth=(p2 - p1).length, location=mid)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = (p2 - p1).to_track_quat('Z', 'Y')
    if mat:
        ob.data.materials.append(mat)
    # Return the cylinder AND its end spheres as separate clean manifold
    # objects for the boolean union. (Joining them into one self-intersecting
    # mesh made the EXACT boolean drop geometry; leaving them out entirely
    # left stray unmaterialised balls in the scene.)
    ea = ball(name + "_A", tuple(p1), (r, r, r), mat)
    eb = ball(name + "_B", tuple(p2), (r, r, r), mat)
    bpy.ops.object.select_all(action='DESELECT')
    return [ob, ea, eb]

def lathe(name, profile, mat, segments=40, location=(0, 0, 0), coll=model_coll):
    verts, faces = [], []
    n = len(profile)
    for (r, z) in profile:
        for j in range(segments):
            a = 2.0 * math.pi * j / segments
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, (i + 1) * segments + j,
                          (i + 1) * segments + j2, i * segments + j2))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    ob.location = location
    if mat:
        ob.data.materials.append(mat)
    return ob

def torus(name, loc, R, r, mat, rot=(0, 0, 0), ms=32, coll=model_coll):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     major_segments=ms, minor_segments=8,
                                     location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def union_mesh(name, parts, mat, voxel=0.014):
    base = parts[0]
    base.name = name
    bpy.context.view_layer.objects.active = base
    for other in parts[1:]:
        mod = base.modifiers.new("u", 'BOOLEAN')
        mod.operation = 'UNION'
        mod.solver = 'EXACT'
        mod.object = other
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(other, do_unlink=True)
    rem = base.modifiers.new("remesh", 'REMESH')
    rem.mode = 'VOXEL'
    rem.voxel_size = voxel
    rem.use_smooth_shade = True
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.modifier_apply(modifier=rem.name)
    if mat:
        base.data.materials.clear()
        base.data.materials.append(mat)
    return base

def chain(name, p0, p1, sag, links_n=11, link_r=0.014):
    p0, p1 = Vector(p0), Vector(p1)
    src = None
    for i in range(links_n):
        t = i / max(1, links_n - 1)
        pos = (1 - t) * p0 + t * p1
        pos.z -= sag * 4 * t * (1 - t)
        bpy.ops.mesh.primitive_torus_add(major_radius=link_r, minor_radius=0.004,
                                         major_segments=10, minor_segments=5,
                                         location=tuple(pos))
        ob = bpy.context.active_object
        if src is None:
            src = ob
            ob.name = name
            ob.data.materials.append(IRON)
            link(ob, model_coll)
        else:
            ob.data = src.data
            ob.name = f"{name}_{i}"
            link(ob, model_coll)
        ob.rotation_euler = (math.pi / 2.4, (i % 2) * math.pi / 2, 0.4)
    bpy.ops.object.select_all(action='DESELECT')

# ================================================================= pedestal drum
cyl("BaseRing", (0, 0, 0.12), 0.52, 0.24, STONE, vertices=48, coll=model_coll)
cyl("BaseRing_Top", (0, 0, 0.255), 0.475, 0.03, STONE_DARK, vertices=48, coll=model_coll)
cyl("Drum", (0, 0, 0.55), 0.455, 0.58, STONE, vertices=48, coll=model_coll)
torus("Drum_RopeMoulding", (0, 0, 0.855), 0.455, 0.028, STONE_DARK)
cyl("Drum_TopDisc", (0, 0, 0.885), 0.475, 0.05, STONE, vertices=48, coll=model_coll)

# motto letters around the base ring front: E PLVRIBVS VNVM (as printed)
motto = "E PLVRIBVS VNVM"
R = 0.522
span = math.radians(112)
for i, ch in enumerate(motto):
    if ch == ' ':
        continue
    t = i / (len(motto) - 1)
    # letters run from +X (screen-left from the preview camera) to -X so the
    # motto reads left-to-right in the preview, as printed
    ang = span / 2 - t * span
    # rotation z = pi - ang makes each glyph's face point OUTWARD along the
    # radius (with -ang the faces point inward and the motto reads mirrored)
    bpy.ops.object.text_add(location=(R * math.sin(ang), R * math.cos(ang), 0.115),
                            rotation=(math.pi / 2, 0, math.pi - ang))
    ob = bpy.context.active_object
    ob.name = f"MottoLetter_{i}"
    ob.data.body = ch
    ob.data.align_x = 'CENTER'
    ob.data.align_y = 'CENTER'
    ob.data.size = 0.115
    ob.data.extrude = 0.006
    bpy.ops.object.convert(target='MESH')
    ob.data.materials.append(STONE_DARK)
    link(ob, model_coll)
bpy.ops.object.select_all(action='DESELECT')

# chain swags + rings on the drum front; crossed rifles (simplified) below
for i, rx in enumerate((-0.27, 0.0, 0.27)):
    torus(f"SwagRing_{i}", (rx, 0.445, 0.70), 0.026, 0.006, IRON, rot=(0.25, 0, 0), ms=16)
chain("SwagChain_L", (-0.27, 0.45, 0.695), (0.0, 0.455, 0.695), sag=0.075, links_n=9)
chain("SwagChain_R", (0.0, 0.455, 0.695), (0.27, 0.45, 0.695), sag=0.075, links_n=9)
for s in (-1, 1):
    box(f"CrossedRifle_{s}", (s * 0.10, 0.435, 0.44), (0.028, 0.018, 0.52),
        STONE_DARK, rot=(s * 0.5, 0, 0))
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.016, radius2=0.004,
                                depth=0.09, location=(0, 0.45, 0.335),
                                rotation=(math.pi, 0, 0))
ts = bpy.context.active_object
ts.name = "SwagTassel"
ts.data.materials.append(STONE_DARK)
link(ts, model_coll)
bpy.ops.object.select_all(action='DESELECT')

# ================================================================= broken column + flag
cyl("BrokenColumn", (-0.335, -0.06, 1.455), 0.105, 1.13, STONE, vertices=24,
    coll=model_coll)
cyl("Column_Base", (-0.335, -0.06, 0.945), 0.13, 0.10, STONE_DARK, vertices=24,
    coll=model_coll)
# jagged broken top: ring of small wedges
for k in range(7):
    a = k / 7 * 2 * math.pi
    box(f"ColumnBreak_{k}", (-0.335 + 0.075 * math.cos(a), -0.06 + 0.075 * math.sin(a),
                             2.03 + 0.02 * math.sin(k * 2.3)),
        (0.045, 0.045, 0.05 + 0.03 * abs(math.sin(k * 1.7))), STONE)
# draped flag hanging over the column front
seg_x, seg_z = 10, 18
verts, faces, uvs = [], [], []
W, H = 0.34, 0.92
for iz in range(seg_z + 1):
    for ix in range(seg_x + 1):
        fx = ix / seg_x - 0.5
        fz = iz / seg_z
        x = -0.335 + fx * W + 0.02 * math.sin(fz * 5.0)
        z = 1.06 + fz * H
        y = -0.06 + 0.115 + 0.028 * math.sin(fx * 9.0 + fz * 3.0) * (1 - fz * 0.4)
        verts.append((x, y, z))
        uvs.append((ix / seg_x, iz / seg_z))
for iz in range(seg_z):
    for ix in range(seg_x):
        a = iz * (seg_x + 1) + ix
        faces.append((a, a + 1, a + seg_x + 2, a + seg_x + 1))
me = bpy.data.meshes.new("Flag")
me.from_pydata(verts, [], faces)
me.update()
me.uv_layers.new(name="UVMap")
for loop in me.loops:
    me.uv_layers.active.data[loop.index].uv = uvs[loop.vertex_index]
for p in me.polygons:
    p.use_smooth = True
flag = bpy.data.objects.new("DrapedFlag", me)
flag.data.materials.append(FLAG_MAT)
model_coll.objects.link(flag)

# ================================================================= figure
TOP = 0.91  # drum top surface the figure stands on
parts = []
def P(ob):
    if isinstance(ob, list):
        parts.extend(ob)
    else:
        parts.append(ob)
    return ob

P(ball("Pelvis", (0.0, -0.005, TOP + 0.86), (0.148, 0.105, 0.115)))
P(ball("Waist", (0.0, -0.012, TOP + 0.975), (0.110, 0.085, 0.098)))
P(ball("Chest", (0.0, -0.022, TOP + 1.10), (0.127, 0.092, 0.108)))
P(ball("ShoulderBar", (0.0, -0.026, TOP + 1.185), (0.146, 0.084, 0.060)))
P(cyl("Neck", (0.0, -0.028, TOP + 1.245), 0.034, 0.10))
# legs (bare below the skirt hem). Sides: with the preview camera at +Y,
# screen-right is world -X, so her anatomical RIGHT is world +X.
P(capsule("LegL", (-0.068, 0.0, TOP + 0.42), (-0.062, 0.008, TOP + 0.075), 0.047))
P(capsule("LegL_Thigh", (-0.072, -0.002, TOP + 0.80), (-0.068, 0.0, TOP + 0.42), 0.062))
P(ball("FootL", (-0.060, 0.045, TOP + 0.020), (0.037, 0.088, 0.025)))
P(capsule("LegR", (0.070, 0.01, TOP + 0.42), (0.082, 0.030, TOP + 0.075), 0.046))
P(capsule("LegR_Thigh", (0.074, 0.004, TOP + 0.80), (0.070, 0.01, TOP + 0.42), 0.061))
P(ball("FootR", (0.084, 0.062, TOP + 0.020), (0.036, 0.086, 0.024)))
# arms lowered and crossed in front, hands meeting at the chains
P(capsule("ArmL_Upper", (-0.142, -0.020, TOP + 1.175), (-0.128, 0.012, TOP + 0.99), 0.035))
P(capsule("ArmL_Fore", (-0.128, 0.012, TOP + 0.99), (-0.022, 0.085, TOP + 0.845), 0.028))
P(ball("HandL", (-0.008, 0.095, TOP + 0.83), (0.025, 0.050, 0.020)))
P(capsule("ArmR_Upper", (0.142, -0.018, TOP + 1.175), (0.126, 0.014, TOP + 0.995), 0.035))
P(capsule("ArmR_Fore", (0.126, 0.014, TOP + 0.995), (0.016, 0.088, TOP + 0.85), 0.028))
P(ball("HandR", (0.006, 0.096, TOP + 0.835), (0.025, 0.050, 0.020)))
figure = union_mesh("Figure_VirginianSlave", parts, BRONZE, voxel=0.014)
link(figure, model_coll)

# wrapped cloth skirt (as drawn: cloth wrapped round the hips, to mid-shin)
lathe("Skirt", [
    (0.0, 0.335), (0.150, 0.335), (0.185, 0.36), (0.205, 0.45),
    (0.200, 0.58), (0.175, 0.72), (0.148, 0.84), (0.140, 0.90),
    (0.125, 0.90), (0.130, 0.80), (0.150, 0.62), (0.160, 0.45),
    (0.135, 0.36), (0.0, 0.345),
], CLOTH, segments=36, location=(0.0, 0.0, TOP))
# cloth wrap band across the torso (dignified simplification — see NOTES)
torus("TorsoWrap", (0.0, -0.018, TOP + 1.115), 0.118, 0.036, CLOTH,
      rot=(math.pi / 2 - 0.18, 0, 0), ms=28)

# head + headscarf (separate object, slight bow)
hparts = []
hparts.append(ball("Skull", (0, 0, 0.075), (0.068, 0.074, 0.090)))
hparts.append(ball("Face", (0.002, 0.016, 0.052), (0.056, 0.060, 0.068)))
hparts.append(ball("NeckStub", (0, 0, -0.005), (0.033, 0.033, 0.045)))
head = union_mesh("Head", hparts, BRONZE, voxel=0.010)
head.location = (0.0, -0.030, TOP + 1.27)
head.rotation_euler = (0.22, 0.0, 0.06)
link(head, model_coll)
# scarf: cap + front band + hanging tail at the back
ball("ScarfCap", (0.0, -0.048, TOP + 1.415), (0.082, 0.082, 0.062), CLOTH,
     coll=model_coll)
ball("ScarfTail", (0.0, -0.115, TOP + 1.30), (0.070, 0.028, 0.105), CLOTH,
     coll=model_coll)
torus("ScarfBand", (0.0, -0.028, TOP + 1.375), 0.078, 0.014, CLOTH,
      rot=(math.pi / 2 + 0.22, 0, 0), ms=24)

# chains: from the hands, down and across to the column; ankle shackle
chain("HandChain_Down", (0.0, 0.10, TOP + 0.83), (-0.08, 0.125, TOP + 0.45),
      sag=0.03, links_n=11)
chain("HandChain_ToColumn", (-0.02, 0.10, TOP + 0.84), (-0.315, 0.05, TOP + 0.80),
      sag=0.10, links_n=12)
torus("AnkleShackle", (0.082, 0.032, TOP + 0.085), 0.052, 0.008, IRON,
      rot=(0.15, 0, 0), ms=20)
torus("WristCuff_L", (-0.024, 0.086, TOP + 0.85), 0.030, 0.006, IRON,
      rot=(0.3, 0.2, 0), ms=16)
torus("WristCuff_R", (0.014, 0.089, TOP + 0.855), 0.030, 0.006, IRON,
      rot=(0.3, 0.2, 0), ms=16)

# ================================================================= render setup
def look_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.001))
ground = bpy.context.active_object
ground.name = "GroundPlane"
gm = make_mat("BackdropGrey", (0.46, 0.46, 0.46), roughness=1.0)
ground.data.materials.append(gm)
link(ground, setup_coll)

bpy.ops.object.camera_add(location=(0.55, 3.9, 1.70))
cam = bpy.context.active_object
cam.name = "PreviewCamera"
cam.data.lens = 50
look_at(cam, (0, 0, 1.18))
link(cam, setup_coll)
bpy.context.scene.camera = cam

def add_light(name, loc, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    li = bpy.context.active_object
    li.name = name
    li.data.energy = energy
    li.data.shape = 'DISK'
    li.data.size = size
    look_at(li, (0, 0, 1.1))
    return link(li, setup_coll)

add_light("KeyLight", (1.7, 2.1, 2.8), 120, 1.1)
add_light("FillLight", (-1.9, 1.4, 1.5), 40, 1.5)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.03
scene.render.resolution_percentage = 85
scene.cycles.use_denoising = True
scene.render.resolution_x = 720
scene.render.resolution_y = 1080
scene.world = bpy.data.worlds.new("GreyWorld")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.46, 0.46, 0.46, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.55

def tri_count(coll):
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for ob in coll.all_objects:
        ev = ob.evaluated_get(dg)
        try:
            me = ev.to_mesh()
            total += sum(len(p.vertices) - 2 for p in me.polygons)
            ev.to_mesh_clear()
        except Exception:
            pass
    return total

print(f"TRIANGLES: {tri_count(model_coll)}")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, SLUG + ".blend"))
bpy.ops.object.select_all(action='DESELECT')
for ob in model_coll.all_objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_coll.all_objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, SLUG + ".glb"),
                          export_format='GLB', use_selection=True, export_apply=True)
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath = os.path.join(OUT_DIR, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
