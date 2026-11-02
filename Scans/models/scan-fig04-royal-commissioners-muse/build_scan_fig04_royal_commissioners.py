# Build script: scan-fig04-royal-commissioners
# Stylised group vignette after Henry Windham Phillips, "The Royal
# Commissioners for the Great Exhibition of 1851": 13 simplified gentlemen
# in 1851 dress around a long table with the exhibition plans. Figures are
# mannequin-like records of pose/dress — NO faces, NO likenesses.
# Re-runnable: blender -b --python build_scan_fig04_royal_commissioners.py
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig04-royal-commissioners"

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

COAT   = mat("CoatBlack", (0.045, 0.042, 0.04))
COAT2  = mat("CoatBrown", (0.09, 0.07, 0.055))
WAIST  = mat("WaistcoatPale", (0.62, 0.58, 0.5))
SHIRT  = mat("ShirtWhite", (0.8, 0.78, 0.74))
TROUS  = mat("TrousersDark", (0.07, 0.065, 0.06))
SKIN   = mat("SkinTone", (0.62, 0.45, 0.34))
HAIRD  = mat("HairDark", (0.06, 0.05, 0.045))
HAIRG  = mat("HairGrey", (0.5, 0.48, 0.45))
MAHOG  = mat("Mahogany", (0.16, 0.09, 0.05), 0.55)
PAPER  = mat("PlanPaper", (0.78, 0.75, 0.68))
UPHOL  = mat("Upholstery", (0.125, 0.05, 0.045))
WALL   = mat("WallPanel", (0.13, 0.115, 0.10))
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

def lathe_at(name, profile, material, pos, rot_y=0.0, segments=20):
    """Lathe around Z built at origin, then rotated about Y and placed.
    rot_y tilts the figure (lean). Positive rot_y tips the top toward +X;
    callers pass pre-rotated positions accordingly (kept simple: profiles
    are near-vertical, lean is small)."""
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
    ob.rotation_euler = (0, rot_y, 0)
    ob.location = pos
    return finish(ob, material)

def ball(name, pos, scale, material, seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2,
                                         location=pos)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(ob, material)

def tube(name, p1, p2, r, material, seg=10):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=d.length,
                                        location=(p1 + p2) / 2)
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


def shell(name, profile, material, pos, yaw, arc=1.9, segments=14):
    """Partial lathe shell (front arc) hugging a figure's chest, facing +Y
    locally, then yawed. Clean alternative to ellipsoid clothing panels."""
    a0, a1 = math.pi / 2 - arc / 2, math.pi / 2 + arc / 2
    verts, faces = [], []
    steps = segments
    for i, (r, z) in enumerate(profile):
        for j in range(steps + 1):
            a = a0 + (a1 - a0) * j / steps
            verts.append((r * math.cos(a), r * math.sin(a), z))
    cols = steps + 1
    for i in range(len(profile) - 1):
        for j in range(steps):
            faces.append((i * cols + j, i * cols + j + 1,
                          (i + 1) * cols + j + 1, (i + 1) * cols + j))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.rotation_euler = (0, 0, yaw)
    ob.location = (pos[0], pos[1], 0)
    return finish(ob, material)

def rot2d(x, y, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (x * c - y * s, x * s + y * c)

# ---------- parametric gentleman ----------
# Local frame: figure faces +Y. yaw rotates the frame in plan.
def gentleman(tag, pos, yaw, seated=False, coat=COAT, waist=WAIST,
              hair=HAIRD, arm_mode="rest", lean=0.0, hair_style="side"):
    """arm_mode: rest | write | point | hold_roll | table | clasp"""
    x0, y0 = pos[0], pos[1]
    def P(lx, ly, z):
        rx, ry = rot2d(lx, ly, yaw)
        return (x0 + rx, y0 + ry, z)
    if seated:
        hip_z, sh_z, head_z = 0.78, 1.22, 1.40
        # thighs forward, shins down
        for s in (-1, 1):
            tube(f"{tag}Thigh{s}", P(s * 0.095, 0.02, 0.80), P(s * 0.10, 0.34, 0.76), 0.062, TROUS)
            tube(f"{tag}Shin{s}", P(s * 0.10, 0.34, 0.76), P(s * 0.105, 0.36, 0.10), 0.048, TROUS)
            ex, ey, _z = P(s * 0.105, 0.44, 0.05)
            ball(f"{tag}Shoe{s}", (ex, ey, 0.045), (0.05, 0.12, 0.035), COAT)
        coat_prof = [(0.001, 0.70), (0.165, 0.74), (0.175, 0.92), (0.155, 1.10),
                     (0.165, 1.24), (0.135, 1.33), (0.001, 1.35)]
    else:
        hip_z, sh_z, head_z = 0.98, 1.44, 1.62
        for s in (-1, 1):
            tube(f"{tag}Leg{s}", P(s * 0.09, 0, 0.10), P(s * 0.095, 0, hip_z), 0.058, TROUS)
            ex, ey, _z = P(s * 0.09, 0.07, 0.05)
            ball(f"{tag}Shoe{s}", (ex, ey, 0.045), (0.05, 0.125, 0.035), COAT)
        coat_prof = [(0.001, 0.86), (0.155, 0.90), (0.160, 1.10), (0.148, 1.30),
                     (0.160, 1.46), (0.132, 1.55), (0.001, 1.57)]
    # torso (lathe) placed with yaw: build via lathe_at with Z-rotation trick —
    # lathe_at rotates about Y only, so bake yaw by rotating profile points:
    verts_profile = coat_prof
    # use a wrapper: create lathe then set rotation.z = yaw
    ob = lathe_at(f"{tag}Coat", verts_profile, coat, (x0, y0, 0.0))
    ob.rotation_euler = (0, 0, yaw)
    # waistcoat + shirt front (offset toward facing dir)
    if seated:
        shell(f"{tag}Waist", [(0.180, 0.80), (0.182, 0.95), (0.163, 1.10), (0.170, 1.22)],
              waist, (x0, y0), yaw, arc=1.9)
        shell(f"{tag}Shirt", [(0.170, 1.20), (0.172, 1.28), (0.140, 1.34)],
              SHIRT, (x0, y0), yaw, arc=1.1)
    else:
        shell(f"{tag}Waist", [(0.163, 1.02), (0.168, 1.18), (0.156, 1.32), (0.166, 1.44)],
              waist, (x0, y0), yaw, arc=1.9)
        shell(f"{tag}Shirt", [(0.168, 1.42), (0.165, 1.50), (0.138, 1.56)],
              SHIRT, (x0, y0), yaw, arc=1.1)
    # cravat / bow tie
    cx, cy, _z = P(0, 0.105, 0)
    ball(f"{tag}Cravat", (cx, cy, sh_z + 0.115), (0.05, 0.035, 0.028), COAT)
    # head + hair (featureless)
    hx, hy, _z = P(0, 0.01, 0)
    ball(f"{tag}Head", (hx, hy, head_z + 0.10), (0.082, 0.078, 0.10), SKIN)
    hax, hay, _z = P(0, -0.025, 0)
    ball(f"{tag}Hair", (hax, hay, head_z + 0.115), (0.086, 0.080, 0.098), hair)
    fx, fy, _z = P(0, 0.018, 0)
    ball(f"{tag}Face", (fx, fy, head_z + 0.098), (0.080, 0.076, 0.098), SKIN)
    if hair_style == "whiskers":
        for s in (-1, 1):
            wx2, wy2, _z = P(s * 0.082, 0.005, 0)
            ball(f"{tag}Whisk{s}", (wx2, wy2, head_z + 0.055), (0.022, 0.045, 0.055), hair)
    # arms
    shL, shR = P(-0.17, 0, sh_z), P(0.17, 0, sh_z)
    if arm_mode == "write":   # right arm forward onto table, left resting
        tube(f"{tag}ArmR1", shR, P(0.20, 0.18, sh_z - 0.28), 0.046, coat)
        tube(f"{tag}ArmR2", P(0.20, 0.18, sh_z - 0.28), P(0.13, 0.44, sh_z - 0.44), 0.038, coat)
        tube(f"{tag}ArmL1", shL, P(-0.20, 0.10, sh_z - 0.30), 0.046, coat)
        hx3, hy3, _z = P(0.13, 0.46, sh_z - 0.45)
        ball(f"{tag}HandR", (hx3, hy3, sh_z - 0.45), (0.032, 0.04, 0.025), SKIN)
    elif arm_mode == "point":  # leaning, right arm extended down-forward
        tube(f"{tag}ArmR1", shR, P(0.22, 0.16, sh_z - 0.30), 0.046, coat)
        tube(f"{tag}ArmR2", P(0.22, 0.16, sh_z - 0.30), P(0.16, 0.46, sh_z - 0.62), 0.038, coat)
        tube(f"{tag}ArmL1", shL, P(-0.19, 0.06, sh_z - 0.34), 0.046, coat)
    elif arm_mode == "hold_roll":  # both hands forward holding a roll
        tube(f"{tag}ArmR1", shR, P(0.20, 0.16, sh_z - 0.26), 0.046, coat)
        tube(f"{tag}ArmR2", P(0.20, 0.16, sh_z - 0.26), P(0.10, 0.40, sh_z - 0.40), 0.038, coat)
        tube(f"{tag}ArmL1", shL, P(-0.20, 0.16, sh_z - 0.26), 0.046, coat)
        tube(f"{tag}ArmL2", P(-0.20, 0.16, sh_z - 0.26), P(-0.08, 0.40, sh_z - 0.40), 0.038, coat)
    elif arm_mode == "table":  # both hands flat forward on the table (Albert)
        for s, sh in ((-1, shL), (1, shR)):
            tube(f"{tag}Arm{s}1", sh, P(s * 0.21, 0.16, sh_z - 0.28), 0.046, coat)
            tube(f"{tag}Arm{s}2", P(s * 0.21, 0.16, sh_z - 0.28), P(s * 0.17, 0.44, sh_z - 0.42), 0.038, coat)
            hx3, hy3, _z = P(s * 0.17, 0.47, sh_z - 0.43)
            ball(f"{tag}Hand{s}", (hx3, hy3, sh_z - 0.435), (0.035, 0.045, 0.02), SKIN)
    elif arm_mode == "clasp":  # hands clasped in lap/front
        for s, sh in ((-1, shL), (1, shR)):
            tube(f"{tag}Arm{s}1", sh, P(s * 0.20, 0.10, sh_z - 0.30), 0.046, coat)
            tube(f"{tag}Arm{s}2", P(s * 0.20, 0.10, sh_z - 0.30), P(s * 0.05, 0.26, sh_z - 0.46), 0.038, coat)
        hx3, hy3, _z = P(0, 0.27, sh_z - 0.47)
        ball(f"{tag}Hands", (hx3, hy3, sh_z - 0.47), (0.055, 0.04, 0.03), SKIN)
    else:  # rest: arms hang
        for s, sh in ((-1, shL), (1, shR)):
            tube(f"{tag}Arm{s}1", sh, P(s * 0.20, 0.02, sh_z - 0.30), 0.046, coat)
            tube(f"{tag}Arm{s}2", P(s * 0.20, 0.02, sh_z - 0.30), P(s * 0.19, 0.05, sh_z - 0.56), 0.038, coat)

# ================= TABLE + PLANS =================
box("TableTop", (0, 0, 0.755), (3.5, 1.15, 0.05), MAHOG)
box("TableApron", (0, 0, 0.70), (3.3, 0.95, 0.08), MAHOG)
for sx in (-1, 1):
    for sy in (-1, 1):
        lathe_at(f"TableLeg{sx}{sy}", [(0.001, 0), (0.052, 0.01), (0.040, 0.35),
                                       (0.046, 0.68), (0.055, 0.73)],
                 MAHOG, (sx * 1.60, sy * 0.45, 0))
# plan sheets on the table
box("PlanSheetBig", (0.62, 0.18, 0.795), (1.05, 0.78, 0.012), PAPER, rot=(0, 0, math.radians(-4)))
box("PlanSheetMid", (-0.45, -0.15, 0.79), (0.85, 0.62, 0.010), PAPER, rot=(0, 0, math.radians(3)))
box("PapersLeft", (-1.35, 0.10, 0.79), (0.45, 0.32, 0.02), PAPER, rot=(0, 0, math.radians(-8)))
# rolled plan (held by the white-haired commissioner, placed at his hands)
tube("PlanRoll", (-0.10, -0.70, 0.85), (0.20, -0.58, 0.88), 0.045, PAPER)
# dividers lying on the big sheet
tube("DividerA", (0.55, 0.20, 0.81), (0.72, 0.34, 0.81), 0.006, HAIRD, seg=6)
tube("DividerB", (0.55, 0.20, 0.81), (0.70, 0.10, 0.81), 0.006, HAIRD, seg=6)

# ================= CHAIRS =================
def chair(tag, pos, yaw, ornate=False):
    x0, y0 = pos[0], pos[1]
    def P(lx, ly, z):
        rx, ry = rot2d(lx, ly, yaw)
        return (x0 + rx, y0 + ry, z)
    a, b, c, d = P(-0.21, -0.19, 0), P(0.21, -0.19, 0), P(-0.21, 0.19, 0), P(0.21, 0.19, 0)
    for i, p in enumerate((a, b, c, d)):
        tube(f"{tag}Leg{i}", p, (p[0], p[1], 0.46), 0.022, MAHOG, seg=8)
    sx, sy, _z = P(0, 0, 0)
    box(f"{tag}Seat", (sx, sy, 0.47), (0.48, 0.44, 0.05), UPHOL if ornate else MAHOG,
        rot=(0, 0, yaw))
    h = 1.35 if ornate else 1.02
    p1, p2 = P(-0.21, -0.20, 0.46), P(0.21, -0.20, 0.46)
    tube(f"{tag}BackL", p1, P(-0.22, -0.22, h), 0.024, MAHOG, seg=8)
    tube(f"{tag}BackR", p2, P(0.22, -0.22, h), 0.024, MAHOG, seg=8)
    bx, by, _z = P(0, -0.22, 0)
    box(f"{tag}BackPanel", (bx, by, (0.46 + h) / 2 + 0.08), (0.46, 0.035, h - 0.55),
        UPHOL if ornate else MAHOG, rot=(0, 0, yaw))
    if ornate:
        for s in (-1, 1):
            fx, fy, _z = P(s * 0.22, -0.22, 0)
            ball(f"{tag}Finial{s}", (fx, fy, h + 0.04), (0.035, 0.035, 0.045), MAHOG, seg=10)

chair("ChairAlbert", (0.55, 0.94, 0), math.radians(180), ornate=True)
chair("ChairWriter", (-1.42, 0.92, 0), math.radians(180))
chair("ChairSecond", (-1.02, 0.95, 0), math.radians(180))
chair("ChairLean", (-0.52, 0.92, 0), math.radians(180))
chair("ChairWhite", (0.05, -0.97, 0), 0.0)
chair("ChairRight", (1.62, 0.80, 0), math.radians(215))

# ================= FIGURES (arrangement follows the painting) =================
# Seated row at the table (facing -Y toward table centre / +Y far side)
gentleman("Writer", (-1.42, 1.02, 0), math.radians(180), seated=True, arm_mode="write")
gentleman("Second", (-1.04, 1.06, 0), math.radians(195), seated=True, arm_mode="clasp")
gentleman("Leaner", (-0.52, 1.03, 0), math.radians(180), seated=True, arm_mode="clasp", hair=HAIRG)
gentleman("WhiteHair", (0.05, -1.05, 0), math.radians(15), seated=True, arm_mode="hold_roll", hair=HAIRG)
gentleman("Albert", (0.55, 1.02, 0), math.radians(180), seated=True, arm_mode="table")
gentleman("RightSeat", (1.66, 0.86, 0), math.radians(230), seated=True, arm_mode="rest")
# Standing row
gentleman("StandFL", (-1.78, 1.30, 0), math.radians(205), arm_mode="rest", hair_style="whiskers")
gentleman("Stand2", (-1.42, 1.38, 0), math.radians(195), arm_mode="rest")
gentleman("Stand3", (-1.02, 1.36, 0), math.radians(185), arm_mode="rest", hair=HAIRG)
gentleman("StandTall", (-0.28, 1.30, 0), math.radians(215), arm_mode="rest", coat=COAT2)
gentleman("Pointer", (0.30, 1.28, 0), math.radians(190), arm_mode="point", hair=HAIRG, hair_style="whiskers")
gentleman("StandBack", (0.98, 1.34, 0), math.radians(160), arm_mode="rest")
gentleman("StandRight", (1.52, 1.26, 0), math.radians(150), arm_mode="rest")

# ================= BACKDROP (minimal) =================
box("BackWall", (0, 2.05, 1.5), (5.6, 0.12, 3.0), WALL)
for sx in (-1.6, 1.9):
    box(f"Pilaster{sx}", (sx, 1.96, 1.5), (0.28, 0.10, 3.0), WALL)

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
light("Fill", 'AREA', (3.5, 4.5, 2.5), 900)

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
setup_col.objects.link(cam)
cam.location = (0.3, -4.6, 1.75)
_target = Vector((0.1, 0.55, 1.02))
cam.rotation_quaternion = (_target - cam.location).to_track_quat('-Z', 'Y')
cam.rotation_mode = 'XYZ'
cam.rotation_euler = cam.rotation_quaternion.to_euler()
cam_data.lens = 42
bpy.context.scene.camera = cam

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.device = 'CPU'
sc.render.resolution_x = 1024
sc.render.resolution_y = 640
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
