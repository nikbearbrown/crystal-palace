#!/usr/bin/env python3
"""Build the Greek & Roman Court krater vase on its carved pedestal.

Candidate #17 from models/CANDIDATES.md. Procedural bpy, Blender 4.2.
Reference: Rijksmuseum stereograph RP-F-2012-96-327 (CC0) — the centre
krater of the pair in the Greek & Roman sculpture court, Sydenham.

Dimensions (photo-inferred, see NOTES.md):
  krater  0.87 m tall, rim dia 0.54 m
  pedestal 0.43 m tall, 0.43 m shaft width
  total assembly 1.30 m, origin at base centre.
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/krater-vase")
ROUND_TAG = os.environ.get("KRATER_ROUND", "r1")

# ---------------------------------------------------------------- clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model_coll = bpy.data.collections.new("MODEL")
scene.collection.children.link(model_coll)
rig_coll = bpy.data.collections.new("RIG")
scene.collection.children.link(rig_coll)

# ---------------------------------------------------------------- material
def plaster_mat():
    m = bpy.data.materials.new("CastPlaster")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.90, 0.88, 0.845, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.68
    return m

PLASTER = plaster_mat()

def link_model(obj):
    model_coll.objects.link(obj)
    try:
        scene.collection.objects.unlink(obj)
    except Exception:
        pass
    obj.data.materials.append(PLASTER) if obj.type == 'MESH' else None
    return obj

# ---------------------------------------------------------------- lathe helper
def catmull_rom(points, samples_per_seg=10):
    """points: list of (r, z). Returns smoothed (r, z) list."""
    pts = [Vector((p[0], p[1], 0.0)) for p in points]
    out = []
    ext = [pts[0] * 2 - pts[1]] + pts + [pts[-1] * 2 - pts[-2]]
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        for j in range(samples_per_seg):
            t = j / samples_per_seg
            t2, t3 = t * t, t * t * t
            q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
            out.append((max(q.x, 0.0), q.y))
    out.append((pts[-1].x, pts[-1].y))
    return out

def lathe(name, profile, segments=128):
    """profile: list of (r, z) from bottom to top; r may reach 0 at the ends."""
    verts, faces = [], []
    rings = []
    for (r, z) in profile:
        ring = []
        for s in range(segments):
            a = 2 * math.pi * s / segments
            ring.append(len(verts))
            verts.append((r * math.cos(a), r * math.sin(a), z))
        rings.append(ring)
    for i in range(len(profile) - 1):
        for s in range(segments):
            s2 = (s + 1) % segments
            faces.append((rings[i][s], rings[i][s2], rings[i + 1][s2], rings[i + 1][s]))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    # smooth shading
    for p in me.polygons:
        p.use_smooth = True
    return obj

# ---------------------------------------------------------------- krater body
R = 0.27          # rim radius
HK = 0.87         # krater height
ctrl = [
    (0.0,   0.470),   # interior bottom centre (r=0 closes the inside)
    (0.150, 0.470),
    (0.205, 0.500),
    (0.228, 0.600),
    (0.240, 0.720),
    (0.252, 0.800),   # inner wall up to lip
    (0.258, 0.862),
    (R,     HK),      # rim top outer
    (0.266, 0.845),   # rim roll
    (0.247, 0.790),   # below rim, outer — slight waist before the lip flare
    (0.243, 0.660),
    (0.232, 0.520),
    (0.226, 0.400),   # relief body bottom
    (0.214, 0.362),   # groove pinch
    (0.221, 0.345),   # groove lower lip
    (0.208, 0.305),   # bowl
    (0.178, 0.262),
    (0.140, 0.228),   # bowl underside
    (0.104, 0.195),   # neck above knop
    (0.112, 0.155),   # knop (cushion)
    (0.098, 0.118),
    (0.084, 0.090),   # stem min
    (0.104, 0.052),
    (0.132, 0.018),   # foot flare
    (0.138, 0.0),     # foot bottom edge
    (0.0,   0.0),     # close bottom
]
profile = catmull_rom(ctrl, samples_per_seg=3)
krater = lathe("Krater", profile, segments=88)
link_model(krater)

# groove beads at the relief-band borders
def torus(name, radius, tube, z):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=tube,
                                     major_segments=64, minor_segments=8,
                                     location=(0, 0, z))
    o = bpy.context.active_object
    o.name = name
    return link_model(o)

torus("BandBeadTop", 0.238, 0.005, 0.795)
torus("BandBeadBottom", 0.222, 0.005, 0.385)

# ---------------------------------------------------------------- schematic relief figure
def lathe_modulated(name, profile, segments=16, ripple=0.0, folds=7):
    """Lathe with a subtle sinusoidal radial ripple to suggest drapery folds."""
    verts, faces = [], []
    rings = []
    for (r, z) in profile:
        ring = []
        for s in range(segments):
            a = 2 * math.pi * s / segments
            rr = r * (1.0 + ripple * math.sin(a * folds)) if r > 0.01 else r
            ring.append(len(verts))
            verts.append((rr * math.cos(a), rr * math.sin(a), z))
        rings.append(ring)
    for i in range(len(profile) - 1):
        for s in range(segments):
            s2 = (s + 1) % segments
            faces.append((rings[i][s], rings[i][s2], rings[i + 1][s2], rings[i + 1][s]))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    for p in me.polygons:
        p.use_smooth = True
    return obj

def limb(name, p0, p1, r0, r1):
    """Tapered cylinder between two points."""
    d = Vector(p1) - Vector(p0)
    mid = (Vector(p0) + Vector(p1)) / 2
    bpy.ops.mesh.primitive_cone_add(radius1=r0, radius2=r1, depth=d.length,
                                    vertices=8, location=mid)
    o = bpy.context.active_object
    o.name = name
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    return o

def make_figure(name, height=0.35):
    """Low-relief draped standing figure, built facing +Y, base at z=0.
    Schematic: fluted robe, chest, arms resting at the sides, head."""
    parts = []
    robe_prof = [(0.0, 0.0), (0.064, 0.0), (0.061, 0.025), (0.049, 0.10),
                 (0.041, 0.19), (0.036, 0.225), (0.0, 0.228)]
    robe = lathe_modulated(name + "_robe", catmull_rom(robe_prof, 2),
                           segments=16, ripple=0.085, folds=6)
    parts.append(robe)
    # chest / shoulders — deliberately wider than the robe top so the
    # figure reads as a figure, not a cone
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10,
                                         radius=0.034, location=(0, 0, 0.243))
    chest = bpy.context.active_object
    chest.scale = (1.45, 0.80, 0.88)
    parts.append(chest)
    # head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10,
                                         radius=0.033, location=(0, 0, 0.302))
    head = bpy.context.active_object
    head.scale = (0.92, 1.0, 1.14)
    parts.append(head)
    # hair bun at the back
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=8,
                                         radius=0.0125, location=(0, -0.018, 0.312))
    parts.append(bpy.context.active_object)
    # arms: shoulder down and slightly out to hands at the robe
    parts.append(limb(name + "_armL", (-0.042, 0.004, 0.250), (-0.031, 0.018, 0.125), 0.0135, 0.0105))
    parts.append(limb(name + "_armR", (0.042, 0.004, 0.250), (0.031, 0.018, 0.125), 0.0135, 0.0105))
    # diagonal drapery sash across the chest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.002, 0.020, 0.20))
    sash = bpy.context.active_object
    sash.scale = (0.055, 0.010, 0.075)
    parts.append(sash)
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    fig = bpy.context.active_object
    fig.name = name
    s = height / 0.33
    fig.scale = (s, s, s)
    bpy.ops.object.transform_apply(scale=True)
    return fig

def body_radius_at(z):
    """approximate outer radius of the krater body at height z (from ctrl)."""
    pts = [(0.795, 0.252), (0.660, 0.243), (0.520, 0.232), (0.400, 0.226)]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z1 <= z <= z0:
            t = (z - z1) / (z0 - z1)
            return r1 + t * (r0 - r1)
    return 0.235

# relief figures around the krater body
N_FIG = 10
fig_proto = make_figure("FigProto", height=0.34)
fig_proto.hide_render = True
for i in range(N_FIG):
    a = 2 * math.pi * i / N_FIG
    z_base = 0.435
    r_mid = body_radius_at(0.60)
    f = fig_proto.copy()
    f.data = fig_proto.data.copy()
    link_model(f)
    f.hide_render = False
    # flatten radially (local Y after we rotate) then position
    f.scale = (1.0, 0.38, 1.0)
    bpy.context.view_layer.objects.active = f
    f.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    f.select_set(False)
    fx = (r_mid - 0.003) * math.cos(a)
    fy = (r_mid - 0.003) * math.sin(a)
    f.location = (fx, fy, z_base)
    f.rotation_euler = (0, 0, -a + 0.0)
    # orient figure's +Y (facing) radially outward: figure built facing +Y,
    # rotate about Z by (pi/2 - a) maps +Y to (cos a, sin a)
    f.rotation_euler = (0, 0, math.pi / 2 - a)
    f.name = f"ReliefFigure_{i:02d}"
bpy.data.objects.remove(fig_proto, do_unlink=True)

# ---------------------------------------------------------------- volute handles
def make_handle(side):
    """side: +1 for +X, -1 for -X. Strap handle rising from the lower body
    to the rim with a volute scroll at the top (in the X-Z plane)."""
    # main strap: bezier curve with round bevel
    cu = bpy.data.curves.new("HandleCurve", 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = 0.0135
    cu.bevel_resolution = 2
    cu.resolution_u = 16
    sp = cu.splines.new('BEZIER')
    pts = [
        (side * 0.150, 0, 0.235),   # lower attachment on the bowl
        (side * 0.255, 0, 0.330),
        (side * 0.302, 0, 0.520),   # outermost bow
        (side * 0.300, 0, 0.720),
        (side * 0.262, 0, 0.838),   # into the rim
    ]
    sp.bezier_points.add(len(pts) - 1)
    for bp, co in zip(sp.bezier_points, pts):
        bp.co = co
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new("Handle", cu)
    link_model(obj)
    # convert to mesh for clean glTF export
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)
    obj.name = "Handle_R" if side > 0 else "Handle_L"
    # volute scroll at the rim attachment: flat spiral tube in X-Z plane
    cu2 = bpy.data.curves.new("VoluteCurve", 'CURVE')
    cu2.dimensions = '3D'
    cu2.bevel_depth = 0.0105
    cu2.bevel_resolution = 2
    sp2 = cu2.splines.new('POLY')
    turns, steps = 1.6, 40
    sp2.points.add(steps)
    cx, cz = side * 0.276, 0.862
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi
        rr = 0.034 * (1 - t) + 0.004
        x = cx + side * rr * math.cos(ang) * 1.0
        z = cz + rr * math.sin(ang)
        sp2.points[i].co = (x, 0, z, 1.0)
    vobj = bpy.data.objects.new("Volute", cu2)
    link_model(vobj)
    bpy.context.view_layer.objects.active = vobj
    vobj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    vobj.select_set(False)
    vobj.name = "Volute_R" if side > 0 else "Volute_L"
    # widen the scroll slightly in Y so it reads as a disc
    vobj.scale = (1.0, 1.5, 1.0)
    bpy.context.view_layer.objects.active = vobj
    vobj.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    vobj.select_set(False)

make_handle(+1)
make_handle(-1)

# ---------------------------------------------------------------- pedestal
PED_H = 0.43
def loft_square(name, levels):
    """levels: list of (z, half_width). Lofted square-section mesh."""
    verts, faces = [], []
    rings = []
    for (z, hw) in levels:
        ring = []
        for (cx, cy) in [(hw, -hw), (hw, hw), (-hw, hw), (-hw, -hw)]:
            ring.append(len(verts))
            verts.append((cx, cy, z))
        rings.append(ring)
    for i in range(len(levels) - 1):
        for s in range(4):
            s2 = (s + 1) % 4
            faces.append((rings[i][s], rings[i][s2], rings[i + 1][s2], rings[i + 1][s]))
    # caps
    bc = len(verts); verts.append((0, 0, levels[0][0]))
    tc = len(verts); verts.append((0, 0, levels[-1][0]))
    for s in range(4):
        s2 = (s + 1) % 4
        faces.append((bc, rings[0][s2], rings[0][s]))
        faces.append((tc, rings[-1][s], rings[-1][s2]))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    return obj

ped_levels = [
    (0.000, 0.230),   # base block
    (0.020, 0.230),
    (0.032, 0.204),   # cove in
    (0.055, 0.212),   # bead
    (0.070, 0.215),   # shaft bottom
    (0.330, 0.215),   # shaft top
    (0.348, 0.200),   # cap cove
    (0.375, 0.228),   # cap block
    (0.395, 0.230),   # top slab
    (PED_H, 0.230),
]
pedestal = loft_square("Pedestal", ped_levels)
link_model(pedestal)

# pedestal relief panels: schematic figure groups on each face
panel_fig = make_figure("PanelFigProto", height=0.21)
panel_fig.hide_render = True
for face in range(4):
    a = face * math.pi / 2
    # panel backing plate
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    plate = bpy.context.active_object
    plate.scale = (0.30, 0.012, 0.235)
    bpy.ops.object.transform_apply(scale=True)
    dist = 0.215 + 0.002
    plate.location = (dist * math.cos(a), dist * math.sin(a), 0.20)
    # thin axis (local Y) radial, width (local X) tangential
    plate.rotation_euler = (0, 0, math.pi / 2 - a)
    link_model(plate)
    plate.name = f"Panel_{face}"
    for k, off in enumerate((-0.088, 0.0, 0.088)):
        f = panel_fig.copy()
        f.data = panel_fig.data.copy()
        link_model(f)
        f.hide_render = False
        f.scale = (1.0, 0.40, 1.0)
        bpy.context.view_layer.objects.active = f
        f.select_set(True)
        bpy.ops.object.transform_apply(scale=True)
        f.select_set(False)
        # local frame: radial dir (cos a, sin a); tangent dir (-sin a, cos a)
        rad = Vector((math.cos(a), math.sin(a), 0))
        tan = Vector((-math.sin(a), math.cos(a), 0))
        pos = rad * (0.215 + 0.006) + tan * off
        f.location = (pos.x, pos.y, 0.095)
        f.rotation_euler = (0, 0, math.pi / 2 - a)
        f.name = f"PanelFigure_{face}_{k}"
bpy.data.objects.remove(panel_fig, do_unlink=True)

# relief figures get a very slightly deeper plaster tone so the schematic
# carving reads against the body in a flat render (geometry is unchanged)
RELIEF_MAT = bpy.data.materials.new("CastPlasterRelief")
RELIEF_MAT.use_nodes = True
_rb = RELIEF_MAT.node_tree.nodes["Principled BSDF"]
_rb.inputs["Base Color"].default_value = (0.845, 0.825, 0.79, 1.0)
_rb.inputs["Roughness"].default_value = 0.72
for o in model_coll.objects:
    if o.type == 'MESH' and (o.name.startswith("ReliefFigure") or o.name.startswith("PanelFigure")):
        if o.data.materials:
            o.data.materials[0] = RELIEF_MAT
        else:
            o.data.materials.append(RELIEF_MAT)

# lift the krater assembly onto the pedestal
for o in list(model_coll.objects):
    if o.name not in ("Pedestal",) and not o.name.startswith("Panel"):
        o.location.z += PED_H

# ---------------------------------------------------------------- rig
def grey_mat(name, v):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (v, v, v, 1.0)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    return m

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(grey_mat("GroundGrey", 0.42))
rig_coll.objects.link(ground)
try:
    scene.collection.objects.unlink(ground)
except Exception:
    pass

# curved backdrop
verts = []
faces = []
import math as _m
seg = 24
for i in range(seg + 1):
    t = i / seg
    ang = _m.radians(-90 + 180 * t)
    x = 9.0 * _m.cos(ang)
    y = 9.0 * _m.sin(ang)
    verts.append((x, y, 0.0))
    verts.append((x, y, 7.0))
for i in range(seg):
    a, b, c, d = 2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2
    faces.append((a, b, c, d))
bme = bpy.data.meshes.new("BackdropMesh")
bme.from_pydata(verts, [], faces)
bme.update()
bd = bpy.data.objects.new("Backdrop", bme)
bd.data.materials.append(grey_mat("BackdropGrey", 0.52))
rig_coll.objects.link(bd)

def add_light(name, typ, loc, power, size=3.0):
    ld = bpy.data.lights.new(name, typ)
    ld.energy = power
    if typ == 'AREA':
        ld.shape = 'DISK'
        ld.size = size
    obj = bpy.data.objects.new(name, ld)
    obj.location = loc
    rig_coll.objects.link(obj)
    # point lights at assembly centre
    direction = Vector((0, 0, 0.65)) - Vector(loc)
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return obj

add_light("Key", 'AREA', (2.6, -2.8, 3.6), 900, 3.5)
add_light("Fill", 'AREA', (-3.2, -0.6, 1.8), 260, 3.0)
add_light("Rim", 'AREA', (0.6, 3.2, 3.0), 500, 2.5)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.5

# cameras on ONE fixed rig: same distance/height logic for all three views
CAM_TARGET = Vector((0, 0, 0.62))
def add_cam(name, loc):
    cd = bpy.data.cameras.new(name)
    cd.lens = 55
    obj = bpy.data.objects.new(name, cd)
    obj.location = loc
    direction = CAM_TARGET - Vector(loc)
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    rig_coll.objects.link(obj)
    return obj

cams = {
    "front": add_cam("CamFront", (0, -3.4, 0.85)),
    "side": add_cam("CamSide", (3.4, 0, 0.85)),
    "three-quarter": add_cam("CamTQ", (2.45, -2.45, 1.15)),
}

# ---------------------------------------------------------------- render setup
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.eevee.taa_render_samples = 64
scene.render.resolution_x = 1000
scene.render.resolution_y = 1150
scene.render.film_transparent = False

def count_tris():
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in model_coll.objects:
        if o.type != 'MESH':
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        total += len(me.loop_triangles)
        ev.to_mesh_clear()
    return total

TRIS = count_tris()
print(f"TRIANGLES: {TRIS}")

os.makedirs(f"{OUT}/renders", exist_ok=True)
os.makedirs(f"{OUT}/work", exist_ok=True)
for view, cam in cams.items():
    scene.camera = cam
    scene.render.filepath = f"{OUT}/work/render_{ROUND_TAG}_{view}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", view)

# save blend + glb + stats
scene.camera = cams["three-quarter"]
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/krater-vase.blend")
bpy.ops.object.select_all(action='DESELECT')
for o in model_coll.objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=f"{OUT}/krater-vase.glb", export_format='GLB',
                          use_selection=True, export_apply=True)
with open(f"{OUT}/work/stats_{ROUND_TAG}.txt", "w") as fh:
    fh.write(f"triangles={TRIS}\n")
    for o in sorted(model_coll.objects, key=lambda x: x.name):
        fh.write(f"object={o.name} type={o.type}\n")
print("DONE", ROUND_TAG)
