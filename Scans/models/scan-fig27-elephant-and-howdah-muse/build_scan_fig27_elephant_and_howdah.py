# Build script: scan-fig27-elephant-and-howdah
# The India Court exhibit after John Nash: a stuffed INDIAN elephant
# (simplified clean low-poly form, ~2.8 m at the shoulder) wearing a gold
# caparison and garland, standing on a stepped plinth; a canopied howdah
# mounted on its back; a second canopied howdah displayed on a stand;
# draped textile backdrop; rope barrier; three attendant figures
# (stylised, no likenesses). Unseen sides are interpretation.
# Re-runnable: blender -b --python build_scan_fig27_elephant_and_howdah.py
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig27-elephant-and-howdah"

bpy.ops.wm.read_factory_settings(use_empty=True)
model_col = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_col)

def mat(name, rgb, rough=0.9, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

GREY   = mat("ElephantGrey", (0.36, 0.345, 0.33))
GREYD  = mat("ElephantShade", (0.29, 0.275, 0.26))
IVORY  = mat("TuskIvory", (0.85, 0.82, 0.74), 0.5)
GOLD   = mat("HowdahGold", (0.62, 0.44, 0.12), 0.55, 0.25)
GOLDD  = mat("CaparisonDeep", (0.45, 0.22, 0.08), 0.7)
WHITE  = mat("PaintedWhite", (0.78, 0.76, 0.72))
GARL   = mat("GarlandWhite", (0.82, 0.80, 0.76))
STONE  = mat("PlinthStone", (0.42, 0.42, 0.43))
ROPE   = mat("BarrierDark", (0.08, 0.07, 0.07))
FABRIC1 = mat("TextileRed", (0.42, 0.14, 0.10))
FABRIC2 = mat("TextileOchre", (0.55, 0.38, 0.14))
FABRIC3 = mat("TextileSlate", (0.25, 0.28, 0.33))
SKIN   = mat("SkinTone", (0.42, 0.29, 0.19))
TUNIC  = mat("TunicWhite", (0.75, 0.72, 0.66))
SASH   = mat("SashPink", (0.62, 0.35, 0.38))
DARKC  = mat("CoatDark", (0.10, 0.09, 0.10))
GROUND = mat("GroundGrey", (0.32, 0.32, 0.32))

def link(obj, col=model_col):
    col.objects.link(obj)
    return obj

def finish(obj, material=None):
    if material:
        obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    return link(obj)

def loft(name, sections, material, seg=22):
    """sections: list of (x, cy, cz, ry, rz) — elliptical rings along X."""
    verts, faces = [], []
    for (x, cy, cz, ry, rz) in sections:
        for j in range(seg):
            a = 2 * math.pi * j / seg
            verts.append((x, cy + ry * math.cos(a), cz + rz * math.sin(a)))
    n = len(sections)
    for i in range(n - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            faces.append((i * seg + j, (i + 1) * seg + j, (i + 1) * seg + j2, i * seg + j2))
    # end caps as fans
    base = len(verts)
    verts.append(sections[0][:3] if False else (sections[0][0], sections[0][1], sections[0][2]))
    for j in range(seg):
        faces.append((base, (j + 1) % seg, j))
    base2 = len(verts)
    off = (n - 1) * seg
    verts.append((sections[-1][0], sections[-1][1], sections[-1][2]))
    for j in range(seg):
        faces.append((base2, off + j, off + (j + 1) % seg))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    return finish(ob, material)

def ball(name, pos, scale, material, seg=18):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2,
                                         location=pos)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(ob, material)

def tube(name, p1, p2, r, material, seg=10, r2=None):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r, radius2=r if r2 is None else r2,
                                    depth=d.length, location=(p1 + p2) / 2)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return finish(ob, material)

def box(name, pos, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = size
    ob.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        ob.data.materials.append(material)
    return link(ob)

def lathe(name, profile, material, centre=(0, 0, 0), segments=24):
    verts, faces = [], []
    n = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(segments):
            a = 2 * math.pi * j / segments
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, i * segments + j2,
                          (i + 1) * segments + j2, (i + 1) * segments + j))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.location = centre
    return finish(ob, material)

def chain_tube(name, points, r, material, seg=8):
    for i in range(len(points) - 1):
        tube(f"{name}{i}", points[i], points[i + 1], r, material, seg=seg)

# ================= PLINTH =================
box("PlinthStep1", (0, 0, 0.09), (4.6, 2.9, 0.18), STONE)
box("PlinthStep2", (0, 0, 0.255), (4.1, 2.45, 0.15), STONE)

# ================= ELEPHANT (faces +X) =================
# Body loft: rear (-X) to shoulder (+X). Shoulder height ~2.8 m above plinth top (0.33).
body_secs = [
    (-2.05, 0, 1.95, 0.28, 0.42),
    (-1.85, 0, 2.00, 0.62, 0.78),
    (-1.45, 0, 2.02, 0.80, 0.98),
    (-0.90, 0, 2.04, 0.88, 1.06),
    (-0.30, 0, 2.05, 0.90, 1.08),
    (0.35, 0, 2.06, 0.885, 1.07),
    (0.90, 0, 2.05, 0.84, 1.02),
    (1.35, 0, 2.00, 0.72, 0.90),
    (1.65, 0, 1.95, 0.52, 0.72),
]
loft("Body", body_secs, GREY)
# legs: columnar, slight taper
for i, (lx, ly) in enumerate(((-1.45, 0.52), (-1.45, -0.52), (1.05, 0.55), (1.05, -0.55))):
    tube(f"Leg{i}", (lx, ly, 1.55), (lx + (0.04 if lx > 0 else -0.03), ly, 0.36), 0.235, GREY, seg=16, r2=0.20)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.215, depth=0.10,
                                        location=(lx + (0.04 if lx > 0 else -0.03), ly, 0.36))
    ft = bpy.context.active_object
    ft.name = f"Foot{i}"
    finish(ft, GREYD)
# head loft: neck to domed forehead (Indian elephant: twin dome)
head_secs = [
    (1.55, 0, 2.10, 0.50, 0.62),
    (1.85, 0, 2.22, 0.56, 0.72),
    (2.10, 0, 2.34, 0.565, 0.78),
    (2.32, 0, 2.38, 0.52, 0.74),
    (2.48, 0, 2.30, 0.42, 0.62),
    (2.56, 0, 2.16, 0.30, 0.48),
]
loft("Head", head_secs, GREY)
ball("ForeheadDomeL", (2.24, 0.19, 2.90), (0.26, 0.21, 0.20), GREY)
ball("ForeheadDomeR", (2.24, -0.19, 2.90), (0.26, 0.21, 0.20), GREY)
# trunk: tapering chain of segments, hangs and curls at the tip
trunk_pts = [(2.52, 0, 2.05), (2.62, 0, 1.70), (2.66, 0, 1.32), (2.64, 0, 0.98),
             (2.58, 0, 0.72), (2.46, 0, 0.55), (2.30, 0, 0.52)]
radii = [0.19, 0.165, 0.14, 0.115, 0.09, 0.068]
for i in range(len(trunk_pts) - 1):
    tube(f"Trunk{i}", trunk_pts[i], trunk_pts[i + 1], radii[i], GREY, seg=14, r2=radii[i + 1] if i + 1 < len(radii) else 0.05)
# tusks: long, curving slightly up (as in the image)
for s, sgn in (("L", 1), ("R", -1)):
    pts = [(2.42, sgn * 0.17, 1.92), (2.72, sgn * 0.21, 1.70), (2.98, sgn * 0.24, 1.58), (3.18, sgn * 0.26, 1.55)]
    for i in range(3):
        tube(f"Tusk{s}{i}", pts[i], pts[i + 1], 0.055 - i * 0.014, IVORY, seg=10, r2=0.041 - i * 0.013)
# ears: INDIAN elephant — smaller ears, do not cover the shoulder
for s, sgn in (("L", 1), ("R", -1)):
    ear = ball(f"Ear{s}", (1.98, sgn * 0.57, 2.48), (0.27, 0.06, 0.40), GREYD)
    ear.rotation_euler = (math.radians(sgn * 12), 0, math.radians(-8))
# eyes (animal detail)
for s, sgn in (("L", 1), ("R", -1)):
    ball(f"Eye{s}", (2.38, sgn * 0.40, 2.42), (0.035, 0.03, 0.035), ROPE, seg=10)
# tail
chain_tube("Tail", [(-2.02, 0, 2.30), (-2.22, 0, 1.85), (-2.28, 0, 1.45)], 0.045, GREY)
ball("TailTuft", (-2.29, 0, 1.32), (0.06, 0.06, 0.13), GREYD, seg=10)

# ================= CAPARISON + GARLAND =================
# Cloth over the back: top panel follows the back line; side panels hang.
# Top panel as a lofted shell strip (reuse loft with narrow ry around back top)
cap_secs = [
    (-1.30, 0, 2.62, 0.86, 0.55),
    (-0.80, 0, 2.68, 0.93, 0.58),
    (-0.20, 0, 2.70, 0.95, 0.59),
    (0.40, 0, 2.68, 0.93, 0.58),
    (0.95, 0, 2.60, 0.87, 0.54),
]
loft("CaparisonTop", cap_secs, GOLD)
for s, sgn in (("L", 1), ("R", -1)):
    # hanging side panel: series of quads via a thin box, slightly angled
    box(f"CaparisonSide{s}", (-0.18, sgn * 0.90, 2.05), (2.15, 0.05, 1.18), GOLD,
        rot=(0, 0, 0))
    box(f"CaparisonPanel{s}", (-0.18, sgn * 0.935, 2.02), (0.85, 0.02, 0.80), GOLDD)
    # fringe row
    for i in range(9):
        fx = -1.18 + i * 0.25
        ball(f"Fringe{s}{i}", (fx, sgn * 0.92, 1.44), (0.035, 0.02, 0.07), GOLDD, seg=6)
# garland: white flower strands hanging at the neck front
for s, sgn in (("L", 1), ("R", -1)):
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((1.95 + 0.12 * math.sin(t * math.pi), sgn * (0.34 + 0.14 * t),
                    2.55 - 1.10 * t))
    for i, p in enumerate(pts):
        ball(f"Garland{s}{i}", p, (0.052, 0.052, 0.065), GARL, seg=8)

# ================= HOWDAH ON THE BACK =================
# white platform + railing at the back, four poles, gold domed canopy
box("HowdahDeck", (-0.15, 0, 3.16), (1.5, 1.15, 0.09), WHITE)
for sx in (-0.85, 0.55):
    for sy in (-0.52, 0.52):
        tube(f"HowdahPost{sx}{sy}", (sx, sy, 3.20), (sx, sy, 3.52), 0.028, WHITE, seg=8)
for sy in (-0.52, 0.52):
    tube(f"HowdahRailS{sy}", (-0.85, sy, 3.50), (0.55, sy, 3.50), 0.022, WHITE, seg=8)
for sx in (-0.85, 0.55):
    tube(f"HowdahRailE{sx}", (sx, -0.52, 3.50), (sx, 0.52, 3.50), 0.022, WHITE, seg=8)
box("HowdahSeat", (-0.15, 0, 3.30), (1.1, 0.8, 0.16), GOLDD)
# canopy poles angled out to the dome rim
for sx, sy in ((-0.95, -0.60), (-0.95, 0.60), (0.65, -0.60), (0.65, 0.60)):
    tube(f"CanopyPole{sx}{sy}", (-0.15 + sx * 0.55, sy * 0.75, 3.20), (sx, sy, 4.42), 0.026, WHITE, seg=8)
lathe("HowdahCanopy", [(0.001, 5.28), (0.30, 5.22), (0.52, 5.05), (0.78, 4.78),
                       (0.98, 4.52), (1.06, 4.44), (1.02, 4.38), (0.001, 4.36)],
      GOLD, centre=(-0.15, 0, 0))
ball("CanopyFinial", (-0.15, 0, 5.33), (0.05, 0.05, 0.07), GOLDD, seg=10)
# canopy valance fringe
for i in range(14):
    a = 2 * math.pi * i / 14
    ball(f"Valance{i}", (-0.15 + 1.03 * math.cos(a), 1.03 * math.sin(a), 4.34),
         (0.04, 0.04, 0.06), GOLDD, seg=6)

# ================= SECOND HOWDAH ON A STAND (right rear) =================
ox, oy = 2.6, 2.55
box("Stand2Top", (ox, oy, 1.02), (1.7, 1.25, 0.08), WHITE)
for sx in (-0.75, 0.75):
    for sy in (-0.52, 0.52):
        tube(f"Stand2Leg{sx}{sy}", (ox + sx, oy + sy, 0), (ox + sx, oy + sy, 1.02), 0.04, WHITE, seg=8)
box("Stand2Seat", (ox, oy, 1.16), (1.25, 0.9, 0.18), GOLDD)
for sx, sy in ((-0.85, -0.62), (-0.85, 0.62), (0.85, -0.62), (0.85, 0.62)):
    tube(f"Stand2Pole{sx}{sy}", (ox + sx * 0.6, oy + sy * 0.6, 1.10), (ox + sx, oy + sy, 2.28), 0.024, WHITE, seg=8)
lathe("Stand2Canopy", [(0.001, 3.02), (0.28, 2.97), (0.55, 2.80), (0.85, 2.52),
                       (1.02, 2.32), (1.08, 2.26), (1.03, 2.20), (0.001, 2.18)],
      GOLD, centre=(ox, oy, 0))
ball("Stand2Finial", (ox, oy, 3.07), (0.045, 0.045, 0.06), GOLDD, seg=10)

# ================= TEXTILE BACKDROP (left rear) =================
box("DrapeWall", (-1.4, 3.05, 2.2), (6.4, 0.10, 4.4), FABRIC3)
# swags: tubes along hanging curves + vertical side drapes
for i, cx in enumerate((-3.6, -1.4, 0.8)):
    m = (FABRIC1, FABRIC2, FABRIC1)[i]
    pts = []
    for k in range(9):
        t = k / 8
        pts.append((cx - 1.0 + 2.0 * t, 2.96, 3.95 - 0.55 * math.sin(t * math.pi)))
    chain_tube(f"Swag{i}", pts, 0.085, m)
    for s in (-1, 1):
        box(f"Drape{i}{s}", (cx + s * 1.02, 2.97, 2.9), (0.30, 0.06, 2.1), m)
box("DrapeValance", (-1.4, 2.96, 4.28), (6.4, 0.07, 0.22), FABRIC2)

# ================= ROPE BARRIER (front) =================
post_x = [-2.2, -0.8, 0.8, 2.2]
for i, px in enumerate(post_x):
    tube(f"BarrierPost{i}", (px, -2.35, 0), (px, -2.35, 0.78), 0.028, ROPE, seg=8)
    ball(f"BarrierKnob{i}", (px, -2.35, 0.82), (0.045, 0.045, 0.045), ROPE, seg=8)
for i in range(len(post_x) - 1):
    pts = []
    for k in range(7):
        t = k / 6
        pts.append((post_x[i] + t * (post_x[i + 1] - post_x[i]), -2.35,
                    0.76 - 0.13 * math.sin(t * math.pi)))
    chain_tube(f"BarrierRope{i}", pts, 0.018, ROPE, seg=6)

# ================= ATTENDANTS (stylised, at the elephant's front-left) =================
def attendant(tag, pos, scale=1.0, dress=TUNIC, sash=False, turban=True, sash_side=1):
    x0, y0 = pos
    h = 1.68 * scale
    # long tunic / robe
    prof = [(0.001, 0.02), (0.20 * scale, 0.03), (0.185 * scale, 0.35 * scale),
            (0.155 * scale, 0.75 * scale), (0.150 * scale, 1.02 * scale),
            (0.165 * scale, 1.28 * scale), (0.125 * scale, 1.42 * scale),
            (0.001, 1.47 * scale)]
    verts, faces = [], []
    seg = 18
    for i, (r, z) in enumerate(prof):
        for j in range(seg):
            a = 2 * math.pi * j / seg
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(len(prof) - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            faces.append((i * seg + j, i * seg + j2, (i + 1) * seg + j2, (i + 1) * seg + j))
    me = bpy.data.meshes.new(tag + "Dress")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(tag + "Dress", me)
    ob.location = (x0, y0, 0)
    finish(ob, dress)
    for s in (-1, 1):
        tube(f"{tag}Arm{s}", (x0 + s * 0.165 * scale, y0, 1.36 * scale),
             (x0 + s * 0.20 * scale, y0 + 0.03, 0.92 * scale), 0.042 * scale, dress)
    ball(f"{tag}Head", (x0, y0, h - 0.10 * scale), (0.080 * scale, 0.076 * scale, 0.096 * scale), SKIN, seg=14)
    if turban:
        ball(f"{tag}Turban", (x0, y0, h - 0.015 * scale), (0.092 * scale, 0.090 * scale, 0.055 * scale), TUNIC, seg=14)
    if sash:
        box(f"{tag}Sash", (x0, y0 + sash_side * 0.10 * scale, 1.16 * scale), (0.24 * scale, 0.045, 0.12), SASH,
            rot=(0, 0, math.radians(-30)))

attendant("AttA", (0.55, -1.55), 1.0, TUNIC)
attendant("AttB", (0.0, -1.78), 1.0, DARKC, sash=True, sash_side=-1)
attendant("AttChild", (-0.55, -1.62), 0.62, TUNIC)

# ================= RENDER SETUP =================
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
g = bpy.context.active_object
g.name = "Ground"
g.data.materials.append(GROUND)
setup_col.objects.link(g)
bpy.context.scene.collection.objects.unlink(g)

world = bpy.data.worlds.new("W")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def light(name, typ, loc, energy, size=4):
    ld = bpy.data.lights.new(name, typ)
    ld.energy = energy
    if typ == 'AREA':
        ld.shape = 'DISK'; ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    setup_col.objects.link(ob)
    return ob

sun = light("Sun", 'SUN', (2.5, 3.5, 5), 3.0)
sun.rotation_euler = (math.radians(55), 0, math.radians(35))
light("Fill", 'AREA', (4.5, 5.5, 3.5), 800)

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
setup_col.objects.link(cam)
# front-right three-quarter, comparable to Nash's view (elephant head to the right)
cam.location = (7.3, -7.5, 3.9)
_target = Vector((0.1, 0.1, 2.05))
cam.rotation_quaternion = (_target - cam.location).to_track_quat('-Z', 'Y')
cam.rotation_mode = 'XYZ'
cam.rotation_euler = cam.rotation_quaternion.to_euler()
cam_data.lens = 40
bpy.context.scene.camera = cam

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.device = 'CPU'
sc.render.resolution_x = 1024
sc.render.resolution_y = 700
sc.render.filepath = os.path.join(HERE, "renders", "preview.png")
sc.view_settings.view_transform = 'Filmic'

# ================= EXPORT =================
tris = 0
for ob in model_col.objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print("TRIANGLES:", tris, "OBJECTS:", len(model_col.objects))

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SLUG + ".blend"))
bpy.ops.object.select_all(action='DESELECT')
for ob in model_col.objects:
    ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, SLUG + ".glb"),
                          use_selection=True, export_apply=True)
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
