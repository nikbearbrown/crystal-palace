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

# ============================================================ fig-74 body
SLUG = "scan-fig74-festival-of-britain-poster"
BOARD = make_mat("MountingBoard", (74, 58, 44), roughness=0.8)
BLUE = make_mat("PosterBlue", (33, 66, 148), roughness=0.85)
NAVY = make_mat("PosterNavyBand", (18, 34, 84), roughness=0.85)
CREAM = make_mat("PosterCream", (233, 228, 205), roughness=0.85)
PALE = make_mat("PosterPaleDigit", (172, 188, 208), roughness=0.85)
WHITE = make_mat("PosterWhite", (240, 242, 245), roughness=0.85)
RED = make_mat("PosterRed", (198, 42, 48), roughness=0.85)
GOLDH = make_mat("BritanniaPale", (228, 208, 165), roughness=0.8)
FLAGB = make_mat("FlagBlue", (44, 74, 165), roughness=0.85)

# poster sheet: 1.00 x 1.50 m, bottom edge at z = 0.15, front faces +Y.
# Local poster height coordinate zp: 0 (bottom) .. 1.50 (top); world z = zp + 0.15.
ZB = 0.15
box("MountBoard", (0, -0.028, ZB + 0.75), (1.08, 0.03, 1.58), BOARD)
box("PosterSheet", (0, 0, ZB + 0.75), (1.00, 0.012, 1.50), BLUE)
FY = 0.0135  # design face offset

def pshape(name, outline, depth, mat):
    """outline in poster coords (x, zp); placed on the sheet face.
    Design x is in IMAGE space (right = image right); it is negated into
    world space because the +Y preview camera shows world +X on the left."""
    out = [(-x, zp + ZB) for (x, zp) in outline]
    return prism(name, out, depth, mat, plane='XZ', base=FY)

def pbox(name, cx, zp, w, h, mat, depth=0.004):
    return box(name, (-cx, FY + depth / 2, zp + ZB), (w, depth, h), mat)

# ---- top: blank year blocks (1851 left / 1951 right; lettering omitted)
pbox("YearBlockLeft", -0.335, 1.375, 0.27, 0.17, PALE)
pbox("YearBlockRight", 0.335, 1.375, 0.27, 0.17, WHITE)

# ---- bunting: three sagging strings of pennant flags across the top
flag_cols = [RED, WHITE, FLAGB]
fi = 0
for row, (ya, sag) in enumerate(((1.335, 0.045), (1.295, 0.055))):
    pts = []
    for k in range(25):
        t = k / 24
        pts.append((-0.49 + 0.98 * t, FY,
                    ZB + ya - sag * math.sin(math.pi * t)))
    tube(f"BuntingString{row}", pts, 0.0016, WHITE)
    for k in range(13):
        t = (k + 0.5) / 13
        cx = -0.49 + 0.98 * t
        cz = ZB + ya - sag * math.sin(math.pi * t)
        tri = [(cx - 0.020, cz / 1), (cx + 0.020, cz), (cx, cz - 0.052)]
        tri = [(x, z - ZB) for (x, z) in tri]
        pshape(f"Flag{fi}", tri, 0.0025, flag_cols[fi % 3])
        fi += 1

# ---- Festival emblem: compass star + disc + Britannia profile (no text)
EX, EZ = -0.02, 1.06
for i in range(8):
    a = i * math.pi / 4
    L = 0.165 if i % 2 == 0 else 0.105
    W = 0.030
    ca, sa = math.cos(a), math.sin(a)
    tip = (EX + L * ca, EZ + L * sa)
    b1 = (EX + W * (-sa), EZ + W * ca)
    b2 = (EX - W * (-sa), EZ - W * ca)
    pshape(f"StarPoint{i}", [b1, tip, b2], 0.004, RED)
disc = [(EX + 0.088 * math.cos(a), EZ + 0.088 * math.sin(a))
        for a in [2 * math.pi * k / 24 for k in range(24)]]
pshape("EmblemDisc", disc, 0.005, PALE)
head = [(-0.055, -0.050), (-0.062, 0.015), (-0.038, 0.055), (0.004, 0.063),
        (0.034, 0.046), (0.052, 0.028), (0.046, 0.017), (0.058, 0.006),
        (0.044, -0.004), (0.047, -0.014), (0.036, -0.028), (0.018, -0.040),
        (0.004, -0.060), (-0.022, -0.062)]
rim = [(EX - x * 1.46, EZ + z * 1.46) for (x, z) in head]
pshape("BritanniaHeadRim", rim, 0.0055, NAVY)
head = [(EX - x * 1.32, EZ + z * 1.32) for (x, z) in head]  # faces image-left, as printed
pshape("BritanniaHead", head, 0.0065, GOLDH)

# ---- striped banner ribbon at centre-left (as printed beside the map)
for i in range(7):
    pbox(f"BannerStripe{i}", -0.245, 0.665 + i * 0.048, 0.052, 0.048,
         RED if i % 2 == 0 else WHITE, depth=0.006)

# ---- map of Britain: pale flat silhouette from lon/lat coastal points
gb_ll = [(-5.72, 50.07), (-5.19, 50.31), (-4.53, 51.00), (-4.18, 51.18),
         (-4.05, 51.62), (-5.31, 51.88), (-4.98, 52.01), (-4.09, 52.41),
         (-4.05, 52.72), (-4.76, 52.81), (-4.27, 53.14), (-4.63, 53.31),
         (-3.83, 53.32), (-3.02, 53.45), (-3.06, 53.82), (-2.90, 54.08),
         (-3.59, 54.55), (-3.40, 54.90), (-4.50, 54.80), (-4.63, 55.46),
         (-4.77, 55.95), (-5.10, 56.20), (-5.47, 56.42), (-5.11, 56.82),
         (-5.80, 57.43), (-5.16, 57.90), (-4.99, 58.62), (-3.03, 58.64),
         (-3.08, 58.44), (-4.22, 57.48), (-3.87, 57.58), (-2.00, 57.69),
         (-2.09, 57.15), (-2.47, 56.71), (-2.80, 56.34), (-2.95, 56.05),
         (-2.51, 56.00), (-2.00, 55.77), (-1.43, 55.01), (-0.62, 54.49),
         (-0.45, 53.70), (0.12, 53.58), (1.30, 52.93), (1.73, 52.61),
         (1.75, 52.48), (1.31, 51.95), (1.15, 51.79), (0.72, 51.54),
         (1.38, 51.39), (1.31, 51.13), (0.59, 50.86), (-0.14, 50.82),
         (-1.09, 50.79), (-1.32, 50.87), (-1.88, 50.72), (-2.45, 50.61),
         (-2.94, 50.71), (-3.42, 50.62), (-3.51, 50.47), (-4.14, 50.33),
         (-5.07, 50.15), (-5.21, 49.96)]
gb = [(0.02 + (lon + 5.7) / 7.5 * 0.46 - 0.23,
       0.30 + (lat - 49.9) / 8.9 * 0.62) for (lon, lat) in gb_ll]
pshape("BritainMap", gb, 0.004, CREAM)

# ---- bottom navy band with blank title / date strips (lettering omitted)
pbox("BottomBand", 0, 0.17, 1.00, 0.34, NAVY, depth=0.003)
pbox("TitleStripBlank", 0, 0.225, 0.80, 0.105, PALE, depth=0.005)
pbox("DateStripBlank", 0, 0.075, 0.55, 0.058, PALE, depth=0.005)

finish(SLUG, cam_loc=(0.30, 3.3, 1.20), cam_target=(0, 0, 0.90), lens=50,
       key_e=150, key_loc=(1.2, 2.6, 2.6), fill_e=55, res=(760, 960),
       ground_size=8)
