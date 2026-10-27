# Build: glass-topped display counter (1851 nave counter run unit), candidate #37
# Sources: Talbot, View of Eastern Nave (1851); Dickinson plate XXIV (Cotton court).
# Form: long low slab-sided counter runs, waist height, dark timber carcase with
# panelled faces and a flat glazed top in timber sash framing. Dimensions are
# INFERRED (see NOTES.md): length 12 ft = half the 24 ft structural bay; depth
# 2 ft 6 in; overall height 0.94 m from figure scale in Dickinson's plate.
import bpy, math, os, json
from mathutils import Vector

WORK = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(WORK)
RENDERS = os.path.join(OUT_DIR, "renders")
os.makedirs(RENDERS, exist_ok=True)

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass

MODEL = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(MODEL)
RIG = bpy.data.collections.new("Rig")
bpy.context.scene.collection.children.link(RIG)

# ---------------------------------------------------------------- dimensions (m)
L = 3.658          # 12 ft unit, tiles 2 per 24 ft bay
D = 0.762          # 2 ft 6 in
PLINTH_H = 0.102
PLINTH_IN = 0.025  # plinth recess from faces
CARC_H = 0.736     # carcase above plinth
CORN_H = 0.026     # capping/cornice band
TOP_H = 0.076      # glazed top frame height
Z0 = PLINTH_H               # carcase bottom
Z1 = Z0 + CARC_H            # carcase top = 0.838
Z2 = Z1 + CORN_H            # top frame bottom = 0.864
Z3 = Z2 + TOP_H             # overall top = 0.940
BED_Z = Z1 + 0.010          # display bed just above carcase top

# ---------------------------------------------------------------- materials
def mat(name, color, rough=0.65, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "DITHERED"
    return m

# dark-stained timber: the counters read near-black in Talbot's photograph
# and dark grey-green in Dickinson's plate (round-3 colour fix)
TIMBER  = mat("TimberDark",  (0.070, 0.042, 0.024), 0.62)
PANEL   = mat("TimberPanel", (0.105, 0.062, 0.033), 0.58)
CLOTH   = mat("BedCloth",    (0.045, 0.085, 0.050), 0.96)
GLASS   = mat("Glass",       (0.82, 0.88, 0.86), 0.08, alpha=0.22)
GROUND_M = mat("RigGrey",    (0.52, 0.52, 0.52), 0.95)

# ---------------------------------------------------------------- helpers
def box(name, size, loc, material, coll=MODEL):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        o.data.materials.append(material)
    for c in list(o.users_collection):
        c.objects.unlink(o)
    coll.objects.link(o)
    return o

# ---------------------------------------------------------------- carcase
# plinth (recessed)
box("Plinth", (L - 2*PLINTH_IN, D - 2*PLINTH_IN, PLINTH_H), (0, 0, PLINTH_H/2), TIMBER)
# solid core, inset 12 mm behind the nominal faces so applied panelling
# can sit in front of it with no coplanar faces (round-1 z-fighting fix)
CORE_IN = 0.012
box("CarcaseCore", (L - 2*CORE_IN, D - 2*CORE_IN, CARC_H), (0, 0, Z0 + CARC_H/2), TIMBER)

# applied frame-and-panel trim: frame members run from the core face to
# 6 mm proud of the nominal face; panel faces sit 2 mm below the nominal
# face, i.e. 8 mm below the frame face and 10 mm proud of the core.
FRAME_T = 0.018
PANEL_T = 0.010
RAIL_H = 0.115      # top/bottom rail height on faces
STILE_W = 0.115

def face(axis_sign, axis):
    """Add frame+panels on one long face (axis='y') or end (axis='x')."""
    if axis == 'y':
        surf = axis_sign * (D/2)
        off = surf - axis_sign * 0.003
        n_pan = 3
        span = L
    else:
        surf = axis_sign * (L/2)
        off = surf - axis_sign * 0.003
        n_pan = 1
        span = D
    zc = Z0 + CARC_H/2
    ph = CARC_H - 2*RAIL_H           # panel height
    # rails
    for dz in (-(CARC_H/2 - RAIL_H/2), CARC_H/2 - RAIL_H/2):
        if axis == 'y':
            box(f"Rail{axis}{axis_sign:+d}{dz:+.2f}", (span, FRAME_T, RAIL_H), (0, off, zc + dz), TIMBER)
        else:
            box(f"Rail{axis}{axis_sign:+d}{dz:+.2f}", (FRAME_T, span, RAIL_H), (off, 0, zc + dz), TIMBER)
    # stiles + panels
    seg = span / n_pan
    for i in range(n_pan + 1):
        s = -span/2 + i*seg
        if axis == 'y':
            box(f"StileY{axis_sign:+d}_{i}", (STILE_W, FRAME_T, ph), (s, off, zc), TIMBER)
        else:
            box(f"StileX{axis_sign:+d}_{i}", (FRAME_T, STILE_W, ph), (off, s, zc), TIMBER)
    poff = surf - axis_sign * 0.007
    for i in range(n_pan):
        c = -span/2 + (i + 0.5)*seg
        pw = seg - STILE_W
        if axis == 'y':
            box(f"PanelY{axis_sign:+d}_{i}", (pw, PANEL_T, ph), (c, poff, zc), PANEL)
        else:
            box(f"PanelX{axis_sign:+d}_{i}", (PANEL_T, pw, ph), (poff, c, zc), PANEL)

face(+1, 'y'); face(-1, 'y'); face(+1, 'x'); face(-1, 'x')

# capping / cornice band with slight overhang
box("Cornice", (L + 0.03, D + 0.03, CORN_H), (0, 0, Z1 + CORN_H/2), TIMBER)

# ---------------------------------------------------------------- glazed top
# display bed (dark cloth) below the glass
box("DisplayBed", (L - 0.09, D - 0.09, 0.012), (0, 0, BED_Z), CLOTH)
# sash frame: perimeter rails + 2 cross mullions -> 3 panes
FR_W = 0.062
fr_z = Z2 + TOP_H/2
box("TopRailFront", (L + 0.03, FR_W, TOP_H), (0,  (D + 0.03)/2 - FR_W/2, fr_z), TIMBER)
box("TopRailBack",  (L + 0.03, FR_W, TOP_H), (0, -(D + 0.03)/2 + FR_W/2, fr_z), TIMBER)
box("TopRailEndL",  (FR_W, D + 0.03 - 2*FR_W, TOP_H), (-(L + 0.03)/2 + FR_W/2, 0, fr_z), TIMBER)
box("TopRailEndR",  (FR_W, D + 0.03 - 2*FR_W, TOP_H), ( (L + 0.03)/2 - FR_W/2, 0, fr_z), TIMBER)
inner_L = L + 0.03 - 2*FR_W
for i in (1, 2):
    x = -inner_L/2 + i * (inner_L/3)
    box(f"TopMullion_{i}", (0.045, D + 0.03 - 2*FR_W, TOP_H*0.8), (x, 0, fr_z), TIMBER)
# glass panes, thin, near top of frame
pane_w = inner_L/3 - 0.045
for i in range(3):
    x = -inner_L/2 + (i + 0.5) * (inner_L/3)
    box(f"GlassPane_{i}", (pane_w, D + 0.03 - 2*FR_W - 0.01, 0.004), (x, 0, Z3 - 0.012), GLASS)

# ---------------------------------------------------------------- rig
gnd = box("Ground", (40, 30, 0.1), (0, 0, -0.051), GROUND_M, coll=RIG)
# uniform neutral-grey world as the backdrop (a boxed backdrop showed a
# black unlit edge in the 3/4 view in round 1)
_w = bpy.context.scene.world
if _w is None:
    _w = bpy.data.worlds.new("World")
    bpy.context.scene.world = _w
_w.use_nodes = True
_w.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
_w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

sun_data = bpy.data.lights.new("Sun", "SUN"); sun_data.energy = 3.2; sun_data.angle = 0.25
sun = bpy.data.objects.new("Sun", sun_data); RIG.objects.link(sun)
sun.location = (-6, -8, 12); sun.rotation_euler = (math.radians(52), math.radians(-8), math.radians(-32))

fill_data = bpy.data.lights.new("Fill", "AREA"); fill_data.energy = 500
fill_data.shape = "RECTANGLE"; fill_data.size = 10; fill_data.size_y = 4
fill = bpy.data.objects.new("Fill", fill_data); RIG.objects.link(fill); fill.location = (4, -8, 6)

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(name, loc, target, lens=40):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 200
    o = bpy.data.objects.new(name, cd); RIG.objects.link(o); o.location = loc
    look_at(o, target); return o

CAM_FRONT = camera("CamFront", (0, -7.2, 0.72), (0, 0, 0.46))
CAM_SIDE  = camera("CamSide",  (-7.2, 0, 0.72), (0, 0, 0.46))
CAM_34    = camera("Cam34",    (4.6, -5.2, 2.4), (0, 0, 0.40))
CAM_RUN   = camera("CamRun",   (7.8, -8.6, 3.4), (0, 0, 0.40), 42)

# ---------------------------------------------------------------- transforms + stats
bpy.context.view_layer.objects.active = None
for o in list(MODEL.objects):
    if o.type == "MESH":
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True); bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action="DESELECT")

dg = bpy.context.evaluated_depsgraph_get()
tris = 0; meshes = 0
for o in MODEL.objects:
    if o.type == "MESH":
        meshes += 1
        ev = o.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
stats = {"objects": meshes, "triangles": tris, "length_m": L, "depth_m": D, "height_m": Z3}
print("STATS", json.dumps(stats))
with open(os.path.join(WORK, "stats.json"), "w") as f:
    json.dump(stats, f, indent=1)

# ---------------------------------------------------------------- save + export (single unit)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "glass-topped-display-counter.blend"))
bpy.ops.object.select_all(action="DESELECT")
for o in MODEL.objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, "glass-topped-display-counter.glb"),
                          export_format="GLB", use_selection=True, export_apply=True)
bpy.ops.object.select_all(action="DESELECT")

# ---------------------------------------------------------------- renders
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.eevee.taa_render_samples = 64
scene.render.film_transparent = False
for cam, fname, rx, ry in ((CAM_FRONT, "front.png", 1500, 900),
                           (CAM_SIDE, "side.png", 1100, 900),
                           (CAM_34, "three-quarter.png", 1400, 1000)):
    scene.camera = cam
    scene.render.resolution_x = rx; scene.render.resolution_y = ry
    scene.render.filepath = os.path.join(RENDERS, fname)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname)

# run render: duplicate the unit twice along X to show the tiled counter run
dupes = []
for k in (-1, 1):
    for o in list(MODEL.objects):
        n = o.copy(); n.data = o.data
        n.location = o.location + Vector((k * (L + 0.03), 0, 0))
        MODEL.objects.link(n); dupes.append(n)
scene.camera = CAM_RUN
scene.render.resolution_x = 1600; scene.render.resolution_y = 1000
scene.render.filepath = os.path.join(RENDERS, "run-three-quarter.png")
bpy.ops.render.render(write_still=True)
print("RENDERED run-three-quarter.png")
for n in dupes: bpy.data.objects.remove(n, do_unlink=True)
print("DONE")
