#!/usr/bin/env python3
"""Build hp-roof-furrow-bay — Hyde Park 1851 roof glazing panel.

One repeatable unit of the ridge-and-furrow roof: a full 24 ft bay length
(control D06) of one furrow — two glass slopes at 2 1/2 to 1 (Plate XII
Fig. 10) between a centre ridge piece and two timber Paxton gutters at
8 ft pitch (control D09), with timber sash bars at the Plate XII Fig. 3
chain spacings (10 1/2 in typical, 11 1/4 in flanking the strong bars)
and 49 in x 10 in panes (Downes text p.15 / printed-page check).

Evidence: Downes 1852 Plates XII-XIV, XVIII; CONTROL-DIMENSIONS D06/D09;
Downes text (glass roof / sash-bar manufacture). Hyde Park 1851 ONLY.

Run: blender -b --python build_hp_roof_furrow_bay.py
Outputs (in this folder): hp-roof-furrow-bay.blend / .glb,
renders/front.png, side.png, three-quarter.png
"""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
IN = 0.0254  # metres per inch

# ---------------------------------------------------------------- controls
BAY_IN        = 288.0    # 24 ft panel length (D06)
HALF_PITCH_IN = 48.0     # ridge centreline to gutter centreline (D09: 8 ft pitch)
RISE_IN       = HALF_PITCH_IN / 2.5          # slope 2 1/2 to 1 (Plate XII Fig. 10)
THETA         = math.atan2(RISE_IN, HALF_PITCH_IN)   # 21.80 deg
SLOPE_LEN_IN  = math.hypot(HALF_PITCH_IN, RISE_IN)   # 51.70 in

# Bar chain along the 24 ft gutter, inches from panel start (Plate XII Fig. 3):
# margins 5 1/4; 10 1/2 typical; 11 1/4 flanking the wide (strong-bar) notches.
BAR_POS_IN = [5.25, 15.75, 26.25, 36.75, 48.0, 59.25, 69.75, 80.25, 90.75,
              101.25, 111.75, 122.25, 132.75, 144.0, 155.25, 165.75, 176.25,
              186.75, 197.25, 207.75, 218.25, 228.75, 240.0, 251.25, 261.75,
              272.25, 282.75]
STRONG_IN = {48.0, 144.0, 240.0}   # three stronger bars in every 24 ft (text)

# Glass: 49 in long (text p.15). Slope coords u from ridge centreline:
GLASS_U0, GLASS_U1 = 0.1, 49.1     # top edge housed in ridge piece; foot at gutter cheek
BAR_U0, BAR_U1     = 1.6, 48.6     # feet housed in the gutter-top notches (Fig. 3)
GLASS_T_IN         = 0.08          # ~2 mm, from the stated 16 oz per sq ft

# Vertical stack (inches, z = 0 at underside of gutters):
GUTTER_TOP_IN = 6.0
# Glass underside plane passes 0.15 in above the gutter cheek at x = 45.6 in:
CREST_GLASS_Z_IN = GUTTER_TOP_IN + 0.15 + 45.6 * (RISE_IN / HALF_PITCH_IN)  # 24.39
RIDGE_CREST_Z_IN = CREST_GLASS_Z_IN + 1.35   # glass enters ridge 1.35 below crest (Fig. 10)

# Profiles (inches). Gutter: (x across, z up), centred on gutter centreline.
GUTTER_PROFILE = [(-2.50, 0.00), (2.50, 0.00), (2.50, 2.30), (2.05, 2.75),
                  (2.05, 3.05), (2.45, 3.30), (2.85, 5.55), (2.85, 6.00),
                  (1.95, 6.00), (1.80, 5.10), (1.45, 4.15), (0.90, 3.62),
                  (0.00, 3.50),
                  (-0.90, 3.62), (-1.45, 4.15), (-1.80, 5.10), (-1.95, 6.00),
                  (-2.85, 6.00), (-2.85, 5.55), (-2.45, 3.30), (-2.05, 3.05),
                  (-2.05, 2.75), (-2.50, 2.30)]
# channel top width 3.9 in, channel 2.50 in deep (1 1/4 + 1 1/4, Fig. 10),
# base 5 in wide (printed), side condensation grooves, cheeks to 5.7 in at top.

# Ridge piece: (x across, z up) with origin at the crest; 3 in wide (printed).
RIDGE_PROFILE = [(-1.50, -3.55), (1.50, -3.55), (1.50, -0.80), (0.19, -0.28),
                 (0.19, 0.00), (-0.19, 0.00), (-0.19, -0.28), (-1.50, -0.80)]

# Sash bars: profile (v across panel length, h above glass-underside plane).
# Ordinary bar: 1 in wide, 1 3/8 in deep overall (Plate XII Fig. 10 + text);
# raised central rib 3/8 in wide; glass seats on the shoulders at h = 0.
ORD_BAR = [(-0.50, -1.00), (0.50, -1.00), (0.50, 0.00), (0.1875, 0.00),
           (0.1875, 0.375), (-0.1875, 0.375), (-0.1875, 0.00), (-0.50, 0.00)]
# Strong bar: 2 1/2 in wide (printed); depth taken as 1 7/8 in overall
# (interior figure on the plate section; the 15/16 reading is also possible —
# see NOTES). Same rib/shoulder top so the glass plane stays true.
STRONG_BAR = [(-1.25, -1.50), (1.25, -1.50), (1.25, 0.00), (0.1875, 0.00),
              (0.1875, 0.375), (-0.1875, 0.375), (-0.1875, 0.00), (-1.25, 0.00)]

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

model_col = bpy.data.collections.new("Model");          scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup");    scene.collection.children.link(setup_col)

def extrude_profile(name, profile, origin, axis_a, axis_b, axis_e, e0, e1, material):
    """Closed prism: profile (a,b) points extruded from e0 to e1 along axis_e."""
    O, A, B, E = (Vector(v) for v in (origin, axis_a, axis_b, axis_e))
    n = len(profile)
    verts = []
    for e in (e0, e1):
        for (a, b) in profile:
            p = O + A * a + B * b + E * e
            verts.append(tuple(p))
    faces = []
    faces.append(tuple(reversed(range(n))))                    # cap at e0
    faces.append(tuple(range(n, 2 * n)))                       # cap at e1
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bm = bmesh.new(); bm.from_mesh(mesh)
    if bm.calc_volume() < 0:
        bmesh.ops.reverse_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material)
    model_col.objects.link(obj)
    return obj

def box(name, centre, size, material, collection=None):
    bpy.ops.mesh.primitive_cube_add(location=centre)
    obj = bpy.context.object
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    for col in obj.users_collection: col.objects.unlink(obj)
    (collection or model_col).objects.link(obj)
    obj.name = name
    return obj

# ---------------------------------------------------------------- materials
def principled(name, colour, roughness, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*colour, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    for k, v in kw.items():
        if k in bsdf.inputs: bsdf.inputs[k].default_value = v
    return m

# Painted timber: pale warm off-white — the roof reads light in the 1851
# photographs (interpretive; exact 1851 paint colour not verified).
MAT_TIMBER = principled("PaintedTimber", (0.86, 0.83, 0.77), 0.62)
MAT_GLASS  = principled("SheetGlass", (0.93, 0.97, 0.96), 0.06,
                        **{"Transmission Weight": 1.0, "IOR": 1.52})

X = Vector((1, 0, 0)); Y = Vector((0, 1, 0)); Z = Vector((0, 0, 1))

# ---------------------------------------------------------------- gutters
for side, gx in (("L", -HALF_PITCH_IN), ("R", HALF_PITCH_IN)):
    extrude_profile(f"PaxtonGutter_{side}",
                    [(x * IN, z * IN) for x, z in GUTTER_PROFILE],
                    (gx * IN, 0, 0), X, Z, Y,
                    -BAY_IN / 2 * IN, BAY_IN / 2 * IN, MAT_TIMBER)

# ---------------------------------------------------------------- ridge
extrude_profile("RidgePiece",
                [(x * IN, z * IN) for x, z in RIDGE_PROFILE],
                (0, 0, RIDGE_CREST_Z_IN * IN), X, Z, Y,
                -BAY_IN / 2 * IN, BAY_IN / 2 * IN, MAT_TIMBER)

# ---------------------------------------------------------------- slopes
cos_t, sin_t = math.cos(THETA), math.sin(THETA)
crest_glass = Vector((0, 0, CREST_GLASS_Z_IN * IN))
for side in (+1, -1):
    d = Vector((side * cos_t, 0, -sin_t))        # down-slope
    nrm = Vector((side * sin_t, 0, cos_t))       # outward normal
    tag = "R" if side > 0 else "L"
    for pos in BAR_POS_IN:
        strong = pos in STRONG_IN
        prof = STRONG_BAR if strong else ORD_BAR
        extrude_profile(
            f"SashBar_{tag}_{pos:06.2f}", [(v * IN, h * IN) for v, h in prof],
            crest_glass + Y * ((pos - BAY_IN / 2) * IN), Y, nrm, d,
            BAR_U0 * IN, BAR_U1 * IN, MAT_TIMBER)
    bounds = [0.0] + BAR_POS_IN + [BAY_IN]
    for i in range(len(bounds) - 1):
        v0, v1 = bounds[i], bounds[i + 1]
        prof = [(-(v1 - v0) / 2 * IN, 0.0), ((v1 - v0) / 2 * IN, 0.0),
                ((v1 - v0) / 2 * IN, GLASS_T_IN * IN), (-(v1 - v0) / 2 * IN, GLASS_T_IN * IN)]
        extrude_profile(
            f"Pane_{tag}_{i:02d}", prof,
            crest_glass + Y * (((v0 + v1) / 2 - BAY_IN / 2) * IN), Y, nrm, d,
            GLASS_U0 * IN, GLASS_U1 * IN, MAT_GLASS)

# ---------------------------------------------------------------- render setup
world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9

def add_plane(name, size, z, material):
    mesh = bpy.data.meshes.new(name)
    s = size / 2
    mesh.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material)
    setup_col.objects.link(obj)
    return obj

add_plane("Backdrop", 60, -0.002, principled("BackdropGrey", (0.60, 0.60, 0.60), 0.95))

def add_light(name, ltype, loc, energy, size=None):
    data = bpy.data.lights.new(name, ltype)
    data.energy = energy
    if size: data.shape = 'DISK'; data.size = size
    obj = bpy.data.objects.new(name, data)
    obj.location = loc
    setup_col.objects.link(obj)
    return obj

sun = add_light("Sun", 'SUN', (4, -3, 7), 3.2)
sun.rotation_euler = (math.radians(52), 0, math.radians(38))
add_light("SoftAbove", 'AREA', (0.5, -0.5, 6.5), 520, size=7.0).rotation_euler = (0, 0, 0)
fill = add_light("Fill", 'AREA', (-6, 3, 2.5), 300, size=5.0)
fill.rotation_euler = (math.radians(65), 0, math.radians(-115))

def look_at(cam, target):
    cam.rotation_mode = 'QUATERNION'
    dirv = Vector(target) - cam.location
    cam.rotation_quaternion = dirv.to_track_quat('-Z', 'Y')

def add_cam(name, loc, target, ortho=None, lens=40):
    data = bpy.data.cameras.new(name)
    if ortho: data.type = 'ORTHO'; data.ortho_scale = ortho
    else: data.lens = lens
    obj = bpy.data.objects.new(name, data)
    obj.location = loc
    setup_col.objects.link(obj)
    look_at(obj, target)
    return obj

centre = (0, 0, 0.33)
cams = {
    "front":        add_cam("CamFront", (0, -9.5, 0.42), centre, ortho=2.95),
    "side":         add_cam("CamSide", (10.5, 0, 0.42), centre, ortho=8.1),
    "three-quarter": add_cam("Cam34", (5.2, -6.2, 3.4), (0, 0, 0.15)),
}

scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
try: scene.cycles.device = 'CPU'
except Exception: pass
scene.render.resolution_x = 960
scene.render.resolution_y = 640
scene.render.film_transparent = False

# ---------------------------------------------------------------- save/export
bpy.ops.object.select_all(action='DESELECT')
for obj in model_col.objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = model_col.objects[0]
blend_path = os.path.join(HERE, "hp-roof-furrow-bay.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, "hp-roof-furrow-bay.glb"),
                          export_format='GLB', use_selection=True)

tris = sum(len(p.vertices) - 2 for o in model_col.objects for p in o.data.polygons)
print(f"MODEL: {len(model_col.objects)} objects, {tris} triangles")
print(f"OVERALL (m): X {2*(HALF_PITCH_IN+2.85)*IN:.3f}  Y {BAY_IN*IN:.3f}  Z {RIDGE_CREST_Z_IN*IN:.3f}")

os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
for name, cam in cams.items():
    scene.camera = cam
    scene.render.filepath = os.path.join(HERE, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
print("DONE")
