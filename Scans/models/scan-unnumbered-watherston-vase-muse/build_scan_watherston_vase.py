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

# ============================================================ vase body
SLUG = "scan-unnumbered-watherston-vase"
GOLD = make_mat("SilverGilt", (198, 158, 82), roughness=0.30, metallic=1.0)
GOLD_D = make_mat("GiltRecess", (148, 112, 54), roughness=0.42, metallic=1.0)
SILVER = make_mat("SilverFigure", (206, 202, 194), roughness=0.34, metallic=1.0)
DARK = make_mat("NicheShadow", (50, 38, 22), roughness=0.7, metallic=0.3)

# ---- lathe body: lobed foot -> stem knop -> bowl -> rim shelf (top z 0.49)
profile = [(0.001, 0.0), (0.200, 0.0), (0.212, 0.012), (0.198, 0.030),
           (0.155, 0.045), (0.162, 0.062), (0.128, 0.078), (0.086, 0.105),
           (0.070, 0.140), (0.076, 0.170), (0.116, 0.200), (0.126, 0.226),
           (0.100, 0.252), (0.160, 0.282), (0.236, 0.332), (0.284, 0.400),
           (0.300, 0.452), (0.316, 0.466), (0.316, 0.486), (0.288, 0.492)]
lathe("VaseBody", profile, GOLD, segments=48)
torus("RimRope", (0, 0, 0.479), 0.308, 0.0085, GOLD_D, rot=(0, 0, 0))
torus("FootRope", (0, 0, 0.020), 0.203, 0.007, GOLD_D)
torus("StemBand", (0, 0, 0.213), 0.121, 0.007, GOLD_D)

# garland swags + berries around the bowl
for s in range(6):
    a0 = math.radians(s * 60 + 8)
    a1 = math.radians(s * 60 + 52)
    pts = []
    for k in range(11):
        t = k / 10
        a = a0 + (a1 - a0) * t
        r = 0.288 + 0.012 * math.sin(math.pi * t)
        z = 0.415 - 0.052 * (math.sin(math.pi * t) ** 0.9)
        pts.append((r * math.sin(a), r * math.cos(a), z))
    tube(f"BowlSwag{s}", pts, 0.0075, GOLD_D)
    for k in range(1, 5):
        t = k / 5
        a = a0 + (a1 - a0) * t
        r = 0.292 + 0.012 * math.sin(math.pi * t)
        z = 0.412 - 0.052 * (math.sin(math.pi * t) ** 0.9)
        ball(f"SwagBerry{s}_{k}", (r * math.sin(a), r * math.cos(a), z),
             (0.0105, 0.0105, 0.0105), GOLD, seg=8)
# satyr-mask medallion at the bowl front
ball("BowlMask", (0, 0.297, 0.385), (0.032, 0.011, 0.034), GOLD_D, seg=14)
for sx in (-1, 1):
    cone(f"MaskHorn{sx}", (sx * 0.034, 0.292, 0.415), 0.008, 0.002, 0.035,
         GOLD_D, rot=(math.radians(115), 0, sx * 0.5), vertices=10)
# rim pendants hanging at four diagonals
for s in range(4):
    a = math.radians(45 + s * 90)
    x, y = 0.30 * math.sin(a), 0.30 * math.cos(a)
    cone(f"RimPendant{s}", (x, y, 0.425), 0.016, 0.004, 0.075, GOLD_D,
         rot=(math.pi, 0, 0), vertices=12)
    tube(f"PendantScroll{s}",
         [(x * 0.92, y * 0.92, 0.475), (x * 1.03, y * 1.03, 0.45),
          (x * 0.99, y * 0.99, 0.415)], 0.006, GOLD_D)

# ---- standing worthies around the rim (plain statues; no likenesses)
NAMES = ["Nelson", "Shakespeare", "Wellington", "Watt", "Milton", "Newton"]
for i, nm in enumerate(NAMES):
    a = math.radians(i * 60)
    x, y = 0.252 * math.sin(a), 0.252 * math.cos(a)
    cyl(f"StatueBase_{nm}", (x, y, 0.50), 0.040, 0.02, GOLD_D, vertices=16)
    figure(f"Worthy_{nm}", (x, y, 0.51), 0.180, SILVER, SILVER,
           facing=-a)
# central niche behind the front statue (Shakespeare, i=0 at +Y front):
# dark recess panel + arch frame + curtain swags
box("NichePanel", (0, 0.208, 0.600), (0.100, 0.012, 0.210), DARK)
tube("NicheArch", arc_pts_xz(0, 0.216, 0.655, 0.052, 0.0, math.pi, 11),
     0.007, GOLD)
for sx in (-1, 1):
    cyl(f"NicheColumn{sx}", (sx * 0.052, 0.216, 0.565), 0.006, 0.145, GOLD,
        vertices=10)
    pts = []
    for k in range(8):
        t = k / 7
        pts.append((sx * (0.048 - 0.028 * t), 0.222 - 0.008 * t,
                    0.700 - 0.105 * (t ** 1.3)))
    tube(f"NicheCurtain{sx}", pts, 0.009, GOLD_D)

# ---- canopy: brackets, entablature ring, flame finials, drum + dome
for s in range(4):
    a = math.radians(45 + s * 90)
    x0, y0 = 0.24 * math.sin(a), 0.24 * math.cos(a)
    x1, y1 = 0.27 * math.sin(a), 0.27 * math.cos(a)
    tube(f"CanopyBracket{s}", [(x0, y0, 0.50), (x1 * 1.04, y1 * 1.04, 0.60),
                               (x1, y1, 0.700)], 0.008, GOLD_D)
    cyl(f"FinialPost{s}", (x1, y1, 0.737), 0.020, 0.035, GOLD, vertices=12)
    ball(f"FinialBulb{s}", (x1, y1, 0.770), (0.021, 0.021, 0.027), GOLD,
         seg=12)
    cone(f"FinialFlame{s}", (x1, y1, 0.814), 0.011, 0.001, 0.052, GOLD,
         vertices=12)
cyl("CanopyRing", (0, 0, 0.705), 0.295, 0.032, GOLD, vertices=40)
torus("CanopyRingRope", (0, 0, 0.723), 0.295, 0.006, GOLD_D)
# draped swags between the canopy posts (front + sides suggested)
for s in range(4):
    a = math.radians(s * 90)
    mx, my = 0.268 * math.sin(a), 0.268 * math.cos(a)
    tx, ty = math.cos(a), -math.sin(a)
    pts = []
    for k in range(11):
        t = k / 10
        off = (t - 0.5) * 0.26
        pts.append((mx + tx * off, my + ty * off,
                    0.695 - 0.050 * (math.sin(math.pi * t) ** 0.9)))
    tube(f"CanopySwag{s}", pts, 0.009, GOLD_D)
# central drum + dome
lathe("CanopyDrum", [(0.001, 0.0), (0.128, 0.0), (0.134, 0.018),
                     (0.118, 0.045), (0.122, 0.062)], GOLD, segments=36,
      location=(0, 0, 0.721))
ball("CanopyDome", (0, 0, 0.775), (0.118, 0.118, 0.045), GOLD, seg=24)
torus("DrumGarland", (0, 0, 0.733), 0.130, 0.007, GOLD_D)

# ---- finial: standing robed figure on the dome (abstract statue)
figure("FinialFigure", (0, 0, 0.812), 0.145, SILVER, SILVER, facing=0.0)

# ---- seated putti + foliage mounds flanking the stem
FOL = make_mat("FoliageGilt", (128, 102, 52), roughness=0.55, metallic=0.9)
for sx in (-1, 1):
    a = math.radians(sx * 38)
    cx, cy = 0.155 * math.sin(a), 0.155 * math.cos(a)
    for k, (ox, oy, sc) in enumerate(((0, 0, 0.055), (0.05, 0.02, 0.042),
                                      (-0.048, 0.025, 0.045),
                                      (0.01, -0.045, 0.04))):
        ball(f"Foliage{sx}_{k}", (cx + ox, cy + oy, 0.028),
             (sc, sc * 0.9, sc * 0.62), FOL, seg=10)
    ball(f"FoliageSeat{sx}", (cx, cy, 0.055), (0.062, 0.058, 0.035), FOL,
         seg=12)
    seated_figure(f"Putto{sx}", (cx, cy, 0.055), 0.19, SILVER, SILVER,
                  facing=-a)

finish(SLUG, cam_loc=(0.55, 1.78, 0.64), cam_target=(0, 0, 0.46), lens=50,
       key_e=42, key_loc=(0.45, 0.55, 0.85), fill_e=16, res=(760, 960),
       ground_size=2.4)
