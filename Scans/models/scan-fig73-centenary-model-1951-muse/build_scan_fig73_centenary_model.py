import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

# ---------------------------------------------------------------- materials
def _lin(v):
    v = v / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def srgb(rgb):
    return tuple(_lin(v) for v in rgb)

def make_mat(name, rgb, roughness=0.5, metallic=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*srgb(rgb), 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = 'DITHERED'
        except Exception:
            pass
    return m

# ---------------------------------------------------------------- helpers
def link(ob, coll=None):
    coll = coll or model_coll
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def box(name, loc, dims, mat, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def ball(name, loc, scale, mat, coll=None, seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(8, seg // 2),
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
    return link(ob, coll)

def cyl(name, loc, r, h, mat, vertices=24, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=h,
                                        location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def cone(name, loc, r1, r2, depth, mat, rot=(0, 0, 0), coll=None, vertices=24):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def torus(name, loc, major, minor, mat, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=36, minor_segments=10,
                                     location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def lathe(name, profile, mat, segments=40, location=(0, 0, 0), coll=None):
    """profile: list of (radius, z), revolved about the Z axis."""
    verts = []
    n = len(profile)
    for (r, z) in profile:
        for j in range(segments):
            a = 2 * math.pi * j / segments
            verts.append((location[0] + r * math.cos(a),
                          location[1] + r * math.sin(a),
                          location[2] + z))
    faces = []
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, i * segments + j2,
                          (i + 1) * segments + j2, (i + 1) * segments + j))
    # end caps when profile does not reach the axis
    if profile[0][0] > 0.001:
        ci = len(verts)
        verts.append((location[0], location[1], location[2] + profile[0][1]))
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((ci, j2, j))
    if profile[-1][0] > 0.001:
        ci = len(verts)
        base = (n - 1) * segments
        verts.append((location[0], location[1], location[2] + profile[-1][1]))
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((ci, base + j, base + j2))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    for p in me.polygons:
        p.use_smooth = True
    if mat:
        me.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def tube(name, points, radius, mat, coll=None):
    cu = bpy.data.curves.new(name + "Curve", 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.resolution_u = 1
    sp = cu.splines.new('POLY')
    sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points):
        p.co = (co[0], co[1], co[2], 1.0)
    ob = bpy.data.objects.new(name, cu)
    (coll or model_coll).objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def prism(name, outline, depth, mat, plane='XY', base=0.0, loc=(0, 0, 0), coll=None):
    """Extrude a 2D outline. plane 'XY': outline=(x,y), depth along +Z.
    plane 'XZ': outline=(x,z), depth along +Y. base offsets the start plane."""
    def P(pt, d):
        if plane == 'XY':
            return (loc[0] + pt[0], loc[1] + pt[1], loc[2] + base + d)
        elif plane == 'YZ':
            return (loc[0] + base + d, loc[1] + pt[0], loc[2] + pt[1])
        else:
            return (loc[0] + pt[0], loc[1] + base + d, loc[2] + pt[1])
    n = len(outline)
    verts = [P(p, 0.0) for p in outline] + [P(p, depth) for p in outline]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        i2 = (i + 1) % n
        faces.append((i, i2, n + i2, n + i))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    if mat:
        me.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def capsule_between(name, p1, p2, r, mat, coll=None):
    p1 = Vector(p1); p2 = Vector(p2)
    mid = (p1 + p2) / 2
    d = p2 - p1
    length = d.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=length,
                                        location=mid)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    if mat:
        ob.data.materials.append(mat)
    link(ob, coll)
    ball(name + "_a", tuple(p1), (r, r, r), mat, coll=coll, seg=12)
    ball(name + "_b", tuple(p2), (r, r, r), mat, coll=coll, seg=12)
    bpy.ops.object.select_all(action='DESELECT')
    return ob

def arc_pts_xz(cx, y, cz, r, a0, a1, n=13):
    return [(cx + r * math.cos(a), y, cz + r * math.sin(a))
            for a in [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]]

def arc_pts_xy(cx, cy, cz, r, a0, a1, n=13):
    return [(cx + r * math.cos(a), cy + r * math.sin(a), cz)
            for a in [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]]

def swag_pts(x0, x1, y, z0, sag, n=11):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        pts.append((x0 + (x1 - x0) * t, y, z0 - sag * (math.sin(math.pi * t) ** 0.8)))
    return pts

def _rot2(x, y, f):
    c, s = math.cos(f), math.sin(f)
    return (x * c - y * s, x * s + y * c)

def figure(name, loc, h, dress_mat, skin_mat, hat=None, facing=0.0,
           legs_mat=None, arm_mat=None):
    """Stylised standing figure, batch house style. Local front = +Y,
    rotated by `facing` about Z at loc."""
    arm_mat = arm_mat or dress_mat
    if legs_mat is None:
        prof = [(0.001, 0.0), (0.175, 0.0), (0.170, 0.03), (0.128, 0.30),
                (0.094, 0.50), (0.088, 0.55), (0.100, 0.63), (0.084, 0.70),
                (0.038, 0.735), (0.034, 0.765)]
    else:
        prof = [(0.001, 0.0), (0.105, 0.0), (0.100, 0.03), (0.088, 0.35),
                (0.082, 0.52), (0.096, 0.63), (0.082, 0.70),
                (0.037, 0.735), (0.033, 0.765)]
    prof = [(r * h, z * h) for (r, z) in prof]
    lathe(name + "_Body", prof, dress_mat, segments=24, location=loc)
    if legs_mat is not None:
        for sx in (-1, 1):
            dx, dy = _rot2(sx * 0.045 * h, 0.0, facing)
            cyl(name + f"_Leg{sx}", (loc[0] + dx, loc[1] + dy, loc[2] + 0.24 * h),
                0.033 * h, 0.48 * h, legs_mat, vertices=12)
    hx, hy = loc[0], loc[1]
    ball(name + "_Head", (hx, hy, loc[2] + 0.845 * h),
         (0.070 * h, 0.074 * h, 0.078 * h), skin_mat, seg=16)
    for sx in (-1, 1):
        ax, ay = _rot2(sx * 0.088 * h, 0.005 * h, facing)
        bx, by = _rot2(sx * 0.150 * h, 0.035 * h, facing)
        capsule_between(name + f"_Arm{sx}",
                        (loc[0] + ax, loc[1] + ay, loc[2] + 0.69 * h),
                        (loc[0] + bx, loc[1] + by, loc[2] + 0.42 * h),
                        0.027 * h, arm_mat)
    hz = loc[2] + 0.90 * h
    if hat == 'bonnet':
        bx, by = _rot2(0.0, -0.028 * h, facing)
        ball(name + "_Bonnet", (hx + bx, hy + by, hz),
             (0.078 * h, 0.080 * h, 0.070 * h), dress_mat, seg=14)
        fx, fy = _rot2(0.0, 0.045 * h, facing)
        cyl(name + "_BonnetBrim", (hx + fx, hy + fy, loc[2] + 0.875 * h),
            0.082 * h, 0.008 * h, dress_mat, vertices=18,
            rot=(math.radians(-18), 0, -facing))
    elif hat == 'top':
        cyl(name + "_TopHat", (hx, hy, loc[2] + 0.955 * h),
            0.056 * h, 0.115 * h, dress_mat, vertices=18)
        cyl(name + "_TopHatBrim", (hx, hy, loc[2] + 0.90 * h),
            0.088 * h, 0.008 * h, dress_mat, vertices=18)
    elif hat == 'flatcap':
        ball(name + "_Cap", (hx, hy, loc[2] + 0.905 * h),
             (0.074 * h, 0.076 * h, 0.038 * h), dress_mat, seg=14)
        fx, fy = _rot2(0.0, 0.075 * h, facing)
        box(name + "_CapPeak", (hx + fx, hy + fy, loc[2] + 0.885 * h),
            (0.07 * h, 0.05 * h, 0.008 * h), dress_mat, rot=(0, 0, -facing))
    elif hat == 'bowler':
        ball(name + "_Bowler", (hx, hy, hz),
             (0.066 * h, 0.066 * h, 0.052 * h), dress_mat, seg=14)
        cyl(name + "_BowlerBrim", (hx, hy, loc[2] + 0.885 * h),
            0.088 * h, 0.007 * h, dress_mat, vertices=18)

def seated_figure(name, loc, s, body_mat, skin_mat, facing=0.0):
    """True seated construction: lap mass on the seat, torso from hips,
    shins dropping from the lap front. s = overall scale (seated height
    approx 0.95*s). Local front = +Y rotated by `facing`."""
    def L(x, y, z):
        rx, ry = _rot2(x, y, facing)
        return (loc[0] + rx, loc[1] + ry, loc[2] + z)
    ball(name + "_Hips", L(0, 0, 0.44 * s), (0.105 * s, 0.10 * s, 0.085 * s),
         body_mat, seg=14)
    capsule_between(name + "_Lap", L(-0.055 * s, 0.03 * s, 0.45 * s),
                    L(0.055 * s, 0.03 * s, 0.45 * s), 0.072 * s, body_mat)
    capsule_between(name + "_LapFront", L(0, 0.05 * s, 0.46 * s),
                    L(0, 0.27 * s, 0.43 * s), 0.068 * s, body_mat)
    capsule_between(name + "_Torso", L(0, -0.01 * s, 0.48 * s),
                    L(0, -0.045 * s, 0.76 * s), 0.088 * s, body_mat)
    ball(name + "_Head", L(0, -0.05 * s, 0.885 * s),
         (0.068 * s, 0.072 * s, 0.076 * s), skin_mat, seg=14)
    for sx in (-1, 1):
        capsule_between(name + f"_Shin{sx}", L(sx * 0.075 * s, 0.27 * s, 0.42 * s),
                        L(sx * 0.08 * s, 0.30 * s, 0.06 * s), 0.042 * s, body_mat)
        capsule_between(name + f"_Arm{sx}", L(sx * 0.095 * s, -0.01 * s, 0.70 * s),
                        L(sx * 0.085 * s, 0.18 * s, 0.47 * s), 0.026 * s, body_mat)

# ---------------------------------------------------------------- render
def look_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

def tri_count(coll):
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for ob in coll.objects:
        ev = ob.evaluated_get(dg)
        try:
            me = ev.to_mesh()
            total += sum(len(p.vertices) - 2 for p in me.polygons)
            ev.to_mesh_clear()
        except Exception:
            pass
    return total

def finish(slug, cam_loc, cam_target, lens=50, key_e=200, key_loc=(3, 4, 5),
           fill_e=60, res=(960, 720), ground_size=14, world_str=0.5):
    bpy.ops.mesh.primitive_plane_add(size=ground_size, location=(0, 0, -0.002))
    g = bpy.context.active_object
    g.name = "GroundPlane"
    gm = make_mat("BackdropGrey", (115, 112, 110), roughness=1.0)
    g.data.materials.append(gm)
    link(g, setup_coll)
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.name = "PreviewCamera"
    cam.data.lens = lens
    look_at(cam, cam_target)
    link(cam, setup_coll)
    bpy.context.scene.camera = cam
    def add_light(nm, loc, e, size):
        bpy.ops.object.light_add(type='AREA', location=loc)
        li = bpy.context.active_object
        li.name = nm
        li.data.energy = e
        li.data.shape = 'DISK'
        li.data.size = size
        look_at(li, cam_target)
        return link(li, setup_coll)
    add_light("KeyLight", key_loc, key_e, max(1.0, ground_size * 0.25))
    add_light("FillLight", (-key_loc[0], key_loc[1] * 0.7, key_loc[2] * 0.5),
              fill_e, max(1.2, ground_size * 0.3))
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.03
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new("GreyWorld")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.45, 0.44, 0.43, 1)
    bg.inputs[1].default_value = world_str
    print(f"TRIANGLES: {tri_count(model_coll)}")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, slug + ".blend"))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in model_coll.objects:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = model_coll.objects[0]
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, slug + ".glb"),
                              export_format='GLB', use_selection=True,
                              export_apply=True)
    bpy.ops.object.select_all(action='DESELECT')
    scene.render.filepath = os.path.join(OUT_DIR, "preview.png")
    bpy.ops.render.render(write_still=True)
    print("DONE", slug)

# ============================================================ fig-73 body
SLUG = "scan-fig73-centenary-model-1951"
IRON = make_mat("PaintedIronWhite", (216, 212, 204), roughness=0.55, metallic=0.25)
IRON_D = make_mat("IronDark", (52, 52, 55), roughness=0.6, metallic=0.4)
DECKM = make_mat("DeckBoards", (148, 138, 122), roughness=0.9)
GLASSM = make_mat("VaultGlass", (196, 214, 222), roughness=0.08, metallic=0.1,
                  alpha=0.22)
CRIM = make_mat("BuntingCrimson", (128, 36, 42), roughness=0.85)
GOLD = make_mat("GiltTrim", (178, 138, 62), roughness=0.35, metallic=1.0)
LEAF = make_mat("ElmGreen", (74, 102, 62), roughness=0.95)
TRUNK = make_mat("ElmTrunk", (88, 70, 52), roughness=0.95)
SKIN = make_mat("SkinTone", (196, 158, 128), roughness=0.7)

DECK = 2.6           # top of the raised display platform
EAVE = DECK + 2.85   # pavilion eaves line

# ---------------- undercroft + deck
box("DeckSlab", (0, 0, DECK - 0.13), (14.6, 4.6, 0.26), IRON_D)
box("DeckFloor", (0, 0, DECK + 0.03), (14.6, 4.6, 0.06), DECKM)
for i, cx in enumerate([x * 1.0 for x in range(-7, 8)]):
    for sy in (-1, 1):
        cyl(f"UndercroftCol{i}_{sy}", (cx, sy * 1.9, (DECK - 0.26) / 2),
            0.085, DECK - 0.26, IRON_D, vertices=12)
# stair hint under the deck (image right, in shadow)
box("StairRun", (5.9, 0.7, 1.15), (2.6, 1.1, 0.18), IRON_D,
    rot=(0, math.radians(38), 0))
box("StairStringer", (5.9, 1.35, 1.5), (2.9, 0.06, 0.1), IRON_D,
    rot=(0, math.radians(38), 0))

# ---------------- deck railing (lattice panels, front + ends)
def railing(x0, x1, y):
    n = int(round((x1 - x0) / 0.875))
    for i in range(n + 1):
        cyl(f"RailPost{x0}_{i}", (x0 + i * 0.875, y, DECK + 0.53),
            0.022, 0.95, IRON, vertices=8)
    tube(f"RailTop{x0}", [(x0, y, DECK + 1.02), (x1, y, DECK + 1.02)],
         0.026, IRON)
    tube(f"RailBase{x0}", [(x0, y, DECK + 0.10), (x1, y, DECK + 0.10)],
         0.02, IRON)
    for i in range(n):
        cx = x0 + (i + 0.5) * 0.875
        for s in (-1, 1):
            box(f"RailLattice{x0}_{i}_{s}", (cx, y, DECK + 0.56),
                (1.06, 0.028, 0.045), IRON, rot=(0, s * math.radians(40), 0))
railing(-7.0, 7.0, 2.28)
for sx in (-1, 1):  # end rails: posts + top rail only
    for i in range(6):
        cyl(f"EndRailPost{sx}_{i}", (sx * 7.28, -2.28 + i * 0.912, DECK + 0.53),
            0.022, 0.95, IRON, vertices=8)
    tube(f"EndRailTop{sx}", [(sx * 7.28, -2.28, DECK + 1.02),
                             (sx * 7.28, 2.28, DECK + 1.02)], 0.026, IRON)

# ---------------- pavilion floor + columns + arches
box("PavilionFloor", (0, 0, DECK + 0.10), (13.8, 3.9, 0.08), DECKM)
COLX = [-6.6 + 1.65 * i for i in range(9)]
for side, sy in (("F", 1), ("B", -1)):
    for i, cx in enumerate(COLX):
        cyl(f"Column{side}{i}", (cx, sy * 1.75, DECK + 1.32), 0.048, 2.44,
            IRON, vertices=12)
    for i in range(8):
        cx = (COLX[i] + COLX[i + 1]) / 2
        tube(f"Arch{side}{i}",
             arc_pts_xz(cx, sy * 1.75, DECK + 1.62, 0.825, 0.0, math.pi, 13),
             0.030, IRON)
    # swag frieze band above the arches
    box(f"FriezeBoard{side}", (0, sy * 1.79, DECK + 2.62), (13.4, 0.05, 0.42),
        IRON)
    for i in range(8):
        cx = (COLX[i] + COLX[i + 1]) / 2
        tube(f"Swag{side}{i}",
             swag_pts(COLX[i] + 0.06, COLX[i + 1] - 0.06, sy * 1.83,
                      DECK + 2.78, 0.30), 0.026, CRIM)
        ball(f"Rosette{side}{i}", (COLX[i], sy * 1.83, DECK + 2.80),
             (0.05, 0.03, 0.05), GOLD, seg=10)

# eaves cornice + ridge crenellation
box("Cornice", (0, 0, EAVE), (13.7, 4.05, 0.10), IRON)
for i in range(41):
    for sy in (-1, 1):
        box(f"Crenel{i}_{sy}", (-6.6 + i * 0.33, sy * 1.98, EAVE + 0.11),
            (0.045, 0.03, 0.13), IRON)

# ---------------- barrel-vault roof (ribs + purlins + glass shell)
def vault_shell(name, radius, length, xc, zbase, mat, steps=18):
    verts, faces = [], []
    for i in range(steps + 1):
        a = math.pi * i / steps
        y = radius * math.cos(a)
        z = zbase + radius * math.sin(a)
        verts.append((xc - length / 2, y, z))
        verts.append((xc + length / 2, y, z))
    for i in range(steps):
        b = i * 2
        faces.append((b, b + 1, b + 3, b + 2))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    me.materials.append(mat)
    return link(ob)

vault_shell("NaveGlass", 1.95, 13.2, 0, EAVE + 0.05, GLASSM)
for i in range(17):
    cx = -6.6 + i * 0.825
    pts = [(cx, 1.95 * math.cos(a), EAVE + 0.05 + 1.95 * math.sin(a))
           for a in [math.pi * k / 16 for k in range(17)]]
    tube(f"VaultRib{i}", pts, 0.028, IRON)
for k, ang in enumerate((0.35, 0.8, 1.25, 1.85, 2.3, 2.75)):
    y = 1.95 * math.cos(ang)
    z = EAVE + 0.05 + 1.95 * math.sin(ang)
    tube(f"Purlin{k}", [(-6.6, y, z), (6.6, y, z)], 0.02, IRON)

# nave end gable (image left): fan disc + spokes
fan = [(1.95 * math.cos(a), EAVE + 0.05 + 1.95 * math.sin(a))
       for a in [math.pi * k / 12 for k in range(13)]]
prism("NaveEndFan", fan, 0.04, GLASSM, plane='YZ', base=-0.04, loc=(-6.60, 0, 0))
tube("NaveEndRim", [( -6.62, 1.95 * math.cos(a), EAVE + 0.05 + 1.95 * math.sin(a))
                    for a in [math.pi * k / 16 for k in range(17)]], 0.035, IRON)

# ---------------- transept crossing (front arch faces +Y at x = +1.65)
TX = 1.65
# transept vault: axis along Y -> custom shell
verts, faces = [], []
steps = 18
for i in range(steps + 1):
    a = math.pi * i / steps
    x = TX + 2.30 * math.cos(a)
    z = EAVE + 0.05 + 2.30 * math.sin(a)
    verts.append((x, -2.35, z))
    verts.append((x, 2.35, z))
for i in range(steps):
    b = i * 2
    faces.append((b, b + 1, b + 3, b + 2))
me = bpy.data.meshes.new("TranseptGlassMesh")
me.from_pydata(verts, [], faces)
me.update()
ob = bpy.data.objects.new("TranseptGlass", me)
me.materials.append(GLASSM)
link(ob)
for i in range(7):
    yy = -2.3 + i * 0.77
    pts = [(TX + 2.30 * math.cos(a), yy, EAVE + 0.05 + 2.30 * math.sin(a))
           for a in [math.pi * k / 16 for k in range(17)]]
    tube(f"TranseptRib{i}", pts, 0.03, IRON)
# front gable: rim arc + fan + spokes + arched openings below
tube("TranseptRim", [(TX + 2.30 * math.cos(a), 2.36,
                      EAVE + 0.05 + 2.30 * math.sin(a))
                     for a in [math.pi * k / 20 for k in range(21)]], 0.045, IRON)
fan2 = [(TX + 2.30 * math.cos(a), EAVE + 0.05 + 2.30 * math.sin(a))
        for a in [math.pi * k / 14 for k in range(15)]]
prism("TranseptFan", [(x, z) for (x, z) in fan2], 0.04, GLASSM, plane='XZ',
      base=2.32, loc=(0, 0, 0))
for k in range(7):
    a = math.pi * (k + 0.5) / 7
    tube(f"TranseptSpoke{k}", [(TX, 2.34, EAVE + 0.05),
                               (TX + 2.24 * math.cos(a), 2.34,
                                EAVE + 0.05 + 2.24 * math.sin(a))], 0.018, IRON)
# arched openings on the transept front (deck level)
for i, (ox, r) in enumerate(((-1.35, 0.66), (0.0, 0.95), (1.35, 0.66))):
    tube(f"TranseptOpening{i}",
         arc_pts_xz(TX + ox, 2.30, DECK + 1.55, r, 0.0, math.pi, 13),
         0.032, IRON)
    cyl(f"TranseptPier{i}a", (TX + ox - r, 2.30, DECK + 0.85), 0.045, 1.5,
        IRON, vertices=10)
    cyl(f"TranseptPier{i}b", (TX + ox + r, 2.30, DECK + 0.85), 0.045, 1.5,
        IRON, vertices=10)
# emblem roundel + drapes (numerals omitted: lettering)
cyl("EmblemDisc", (TX, 2.40, EAVE + 1.15), 0.44, 0.07, CRIM, vertices=28,
    rot=(math.radians(90), 0, 0))
star = []
for i in range(16):
    a = i * math.pi / 8
    r = 0.30 if i % 2 == 0 else 0.13
    star.append((TX + r * math.cos(a), EAVE + 1.15 + r * math.sin(a)))
prism("EmblemStar", star, 0.03, GOLD, plane='XZ', base=2.44)
for sx in (-1, 1):
    pts = []
    for k in range(9):
        t = k / 8
        pts.append((TX + sx * (0.15 + 0.75 * t), 2.38,
                    EAVE + 1.55 - 0.85 * (t ** 1.4)))
    tube(f"EmblemDrape{sx}", pts, 0.045, CRIM)

# interior hints: two elms + display blocks inside
for sx in (-1, 1):
    cyl(f"InnerElmTrunk{sx}", (sx * 3.6, 0, DECK + 0.75), 0.07, 1.3, TRUNK,
        vertices=8)
    ball(f"InnerElm{sx}", (sx * 3.6, 0, DECK + 1.85), (0.85, 0.8, 0.95), LEAF,
         seg=14)
box("DisplayBlockA", (-1.8, -0.6, DECK + 0.45), (1.6, 0.9, 0.7), IRON_D)
box("DisplayBlockB", (4.6, -0.4, DECK + 0.40), (1.3, 0.8, 0.6), IRON_D)

# ---------------- visitors on the deck (1950s silhouettes)
SUIT = make_mat("SuitDark", (44, 42, 46), roughness=0.85)
SUIT2 = make_mat("SuitBrown", (86, 66, 50), roughness=0.85)
DRESS1 = make_mat("DressFloral", (168, 150, 138), roughness=0.85)
DRESS2 = make_mat("DressWhite", (228, 224, 214), roughness=0.85)
DRESS3 = make_mat("DressNavy", (48, 56, 88), roughness=0.85)
TROUSER = make_mat("Trousers", (60, 56, 52), roughness=0.9)
figure("VisitorMan1", (-4.6, 1.55, DECK + 0.06), 1.74, SUIT, SKIN,
       hat='flatcap', facing=math.radians(160), legs_mat=TROUSER)
figure("VisitorBoy", (-4.05, 1.45, DECK + 0.06), 1.28, SUIT2, SKIN,
       facing=math.radians(190), legs_mat=TROUSER)
figure("VisitorWoman1", (-2.9, 1.35, DECK + 0.06), 1.63, DRESS1, SKIN,
       hat='bonnet', facing=math.radians(200))
figure("VisitorWoman2", (0.4, 1.65, DECK + 0.06), 1.66, DRESS2, SKIN,
       facing=math.radians(175))
figure("VisitorWoman3", (3.9, 1.15, DECK + 0.06), 1.62, DRESS3, SKIN,
       hat='bonnet', facing=math.radians(215))
figure("VisitorMan2", (4.6, 1.5, DECK + 0.06), 1.76, SUIT2, SKIN,
       hat='flatcap', facing=math.radians(140), legs_mat=TROUSER)
figure("VisitorWoman4", (6.1, 0.4, DECK + 0.06), 1.64, DRESS1, SKIN,
       facing=math.radians(250))

finish(SLUG, cam_loc=(11.5, 16.5, 6.9), cam_target=(0, 0, 2.8), lens=40,
       key_e=2600, key_loc=(9, 11, 15), fill_e=850, res=(960, 720),
       ground_size=40)
