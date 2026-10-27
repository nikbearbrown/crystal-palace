# Build script — chatsworth-great-stove-rib-bay
# One structural rib bay of Paxton's Great Stove (Great Conservatory),
# Chatsworth, Derbyshire, 1836-40. Evidence-derived companion to the
# illustrative models/chatsworth-glasshouse-rib-bay/ already on main.
#
# Controlling dimensions are PERIOD-PRINTED (Morris, Picturesque Views
# of Seats, pp.49-52; Black's Guide 1864; Cokayne 1889 — all agreeing):
#   plan 123 ft wide; central arched roof span 70 ft, crown 67 ft,
#   springing on cast-iron pillars 28 ft high.
# Profile form read from the 19th-century photograph of the building
# (project round-2 collection, S03). Everything else is flagged
# inferred/guessed in NOTES.md. Re-runnable: factory reset -> build ->
# save .blend -> export .glb -> render front/side/three-quarter.
#
# Blender 4.5.3, headless:  blender -b -P build_chatsworth_great_stove_rib_bay.py
import bpy, math, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "chatsworth-great-stove-rib-bay"

FT = 0.3048
# ---- printed dimensions (period sources) ----
SPAN_C   = 70 * FT          # 21.336  central arch span
PILLAR_H = 28 * FT          # 8.5344  springing height / pillar height
CROWN    = 67 * FT          # 20.4216 overall height
WIDTH    = 123 * FT         # 37.4904 total width
# ---- inferred / chosen (flagged in NOTES) ----
BAY      = 8 * FT           # 2.4384  bay width — INFERRED (Paxton's 8 ft module habit + photo rib density)
VALLEY_Z = 7.90             # side roof top / valley level — read off photo proportions
FOOT_Z   = 2.00             # side glazing foot (top of ventilator band) — photo-read
PLINTH_H = 1.05             # stone plinth height — photo-read
RIB_W    = 0.15             # central rib width  — GUESSED
RIB_D    = 0.30             # central rib radial depth (5 laminations x 0.06) — GUESSED
SIDE_RIB_W, SIDE_RIB_D = 0.11, 0.20   # side arch section — GUESSED
COL_R    = 0.125            # cast-iron pillar radius — GUESSED
FURROW_AMP = 0.055          # ridge-and-furrow zigzag amplitude — INFERRED

A  = SPAN_C / 2.0           # central ellipse semi-span  10.668
Z0 = PILLAR_H               # central ellipse centre height
B  = CROWN - PILLAR_H       # central ellipse semi-rise  11.8872
HW = WIDTH / 2.0            # 18.7452
SX_C, SZ_C = A, FOOT_Z      # side ellipse centre (x,z)
SA = (HW - 0.145) - A       # side ellipse semi-run  7.932
SB = VALLEY_Z - FOOT_Z      # side ellipse semi-rise 5.90

# ---------------------------------------------------------------- materials
def get_mat(name, rgb, rough=0.85, metal=0.0, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

MAT_LAM = MAT_TIMBER = MAT_IRON = MAT_STONE = MAT_STONE_D = MAT_GLASS = None

def init_materials():
    global MAT_LAM, MAT_TIMBER, MAT_IRON, MAT_STONE, MAT_STONE_D, MAT_GLASS
    MAT_LAM = [get_mat("TimberPaintedA", (0.84, 0.80, 0.72)),
               get_mat("TimberPaintedB", (0.70, 0.64, 0.55)),
               get_mat("TimberPaintedC", (0.77, 0.72, 0.63))]
    MAT_TIMBER = MAT_LAM[0]
    MAT_IRON   = get_mat("IronPainted", (0.16, 0.18, 0.19), rough=0.55, metal=0.55)
    MAT_STONE  = get_mat("StonePlinth", (0.58, 0.55, 0.50), rough=0.95)
    MAT_STONE_D= get_mat("StoneRecess", (0.38, 0.36, 0.33), rough=0.95)
    MAT_GLASS  = get_mat("Glass", (0.62, 0.72, 0.76), rough=0.08, alpha=0.52)

# ---------------------------------------------------------------- helpers
_groups = {}
def _register(obj, group):
    _groups.setdefault(group, []).append(obj.name)

def _bake(ob):
    """Bake the object's world matrix into its mesh; reset to identity.
    Keeps later joins a pure merge (no transform_apply distortion)."""
    bpy.context.view_layer.update()
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = Matrix.Identity(4)

def add_box(name, centre, xdir, size, mat, group, ydir=None, zdir=None):
    """Unit cube placed by basis: xdir/ydir/zdir are unit axes, size=(sx,sy,sz)."""
    X = Vector(xdir).normalized()
    if zdir is not None:
        Z = Vector(zdir).normalized()
        Y = Vector(ydir).normalized() if ydir is not None else Z.cross(X).normalized()
        X = Y.cross(Z).normalized()
    elif ydir is not None:
        Y = Vector(ydir).normalized()
        Z = X.cross(Y).normalized()
        Y = Z.cross(X).normalized()
    else:
        Y = Vector((0, 1, 0))
        Z = X.cross(Y).normalized()
        Y = Z.cross(X).normalized()
    sx, sy, sz = size
    C = Vector(centre)
    M = Matrix(((X.x*sx, Y.x*sy, Z.x*sz, C.x),
                (X.y*sx, Y.y*sy, Z.y*sz, C.y),
                (X.z*sx, Y.z*sy, Z.z*sz, C.z),
                (0, 0, 0, 1)))
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.object
    ob.name = name
    ob.matrix_world = M
    _bake(ob)
    if mat:
        ob.data.materials.append(mat)
    _register(ob, group)
    return ob

def seg_box(name, p1, p2, width_y, depth, mat, group, normal_off=0.0, n1=None, n2=None):
    """Box spanning profile segment p1->p2 (XZ plane), centred on the segment,
    optionally offset along the segment normals."""
    a, b = Vector(p1), Vector(p2)
    if n1 is not None:
        a = a + Vector(n1) * normal_off
        b = b + Vector(n2) * normal_off
    mid = (a + b) / 2
    d = b - a
    length = d.length
    xdir = d / length
    return add_box(name, mid, xdir, (length * 1.04, width_y, depth), mat, group)

def join_group(group, new_name):
    names = _groups.get(group, [])
    if not names:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    objs = [bpy.data.objects[n] for n in names]
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = new_name
    return ob

# profile samplers ------------------------------------------------------
def central_pts(n=30):
    pts, nrms = [], []
    for i in range(n + 1):
        t = math.pi * i / n
        x, z = A * math.cos(t), Z0 + B * math.sin(t)
        nrm = Vector((B * math.cos(t), 0, A * math.sin(t))).normalized()
        pts.append((x, 0, z)); nrms.append(nrm)
    return pts, nrms

def side_pts(sign, n=11):
    pts, nrms = [], []
    for i in range(n + 1):
        p = (math.pi / 2) * i / n
        x = SX_C + SA * math.sin(p)
        z = SZ_C + SB * math.cos(p)
        # tangent dP/dp = (SA cos p, -SB sin p) in (x,z); outward normal = (-tz, tx)
        tx, tz = SA * math.cos(p), -SB * math.sin(p)
        nrm = Vector((-tz, 0, tx)).normalized()
        pts.append((sign * x, 0, z)); nrms.append(Vector((sign * nrm.x, 0, nrm.z)))
    if sign < 0:
        pts.reverse(); nrms.reverse()
    return pts, nrms

# ---------------------------------------------------------------- build
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_materials()
    model = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(model)

    y0, y1 = -BAY / 2, BAY / 2
    cpts, cnrm = central_pts(30)
    glass_groups = []

    for end_i, y in enumerate((y0, y1)):
        # central laminated rib: 5 bands across the radial depth
        for i in range(len(cpts) - 1):
            for k in range(5):
                off = -(0.045 + 0.06 * k)
                p1 = Vector(cpts[i]) + cnrm[i] * off
                p2 = Vector(cpts[i + 1]) + cnrm[i + 1] * off
                mid = (p1 + p2) / 2; mid.y = y
                d = p2 - p1
                add_box(f"CRib_{end_i}_{i}_{k}", mid, d.normalized(),
                        (d.length * 1.05, RIB_W, 0.058), MAT_LAM[k % 3], "RibsCentral")
        # springing blocks
        for s in (-1, 1):
            add_box(f"Spring_{end_i}_{s}", (s * A, y, Z0 - 0.16), (1, 0, 0),
                    (0.52, 0.30, 0.34), MAT_IRON, "Ironwork")
        # cast-iron pillars
        for s in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=COL_R,
                                                depth=PILLAR_H - 0.30,
                                                location=(s * A, y, (PILLAR_H - 0.30) / 2 + 0.22))
            ob = bpy.context.object; ob.name = f"Column_{end_i}_{s}"
            _bake(ob)
            ob.data.materials.append(MAT_IRON); _register(ob, "Ironwork")
            add_box(f"ColBase_{end_i}_{s}", (s * A, y, 0.11), (1, 0, 0),
                    (0.44, 0.44, 0.22), MAT_IRON, "Ironwork")
            add_box(f"ColCap_{end_i}_{s}", (s * A, y, Z0 - 0.05), (1, 0, 0),
                    (0.46, 0.36, 0.10), MAT_IRON, "Ironwork")
        # side arches (lighter laminated ribs), rib continues to plinth
        for s in (1, -1):
            spts, snrm = side_pts(s, 11)
            for i in range(len(spts) - 1):
                seg_box(f"SRib_{end_i}_{s}_{i}", (spts[i][0], y, spts[i][2]),
                        (spts[i + 1][0], y, spts[i + 1][2]), SIDE_RIB_W, SIDE_RIB_D,
                        MAT_LAM[1], "RibsSide", normal_off=-0.115, n1=snrm[i], n2=snrm[i + 1])
            # straight foot down to plinth top
            fx = s * (HW - 0.145)
            add_box(f"SFoot_{end_i}_{s}", (fx, y, (FOOT_Z + PLINTH_H) / 2), (1, 0, 0),
                    (SIDE_RIB_D, SIDE_RIB_W, FOOT_Z - PLINTH_H), MAT_LAM[1], "RibsSide",
                    zdir=(0, 0, 1))
            # stone corbel under rib foot
            add_box(f"Corbel_{end_i}_{s}", (s * (HW - 0.10), y, PLINTH_H - 0.14), (1, 0, 0),
                    (0.55, 0.30, 0.28), MAT_STONE, "Plinth")

    # valley gutters + ledge, ridge cap
    for s in (-1, 1):
        add_box(f"Valley_{s}", (s * (A + 0.10), 0, VALLEY_Z + 0.30), (1, 0, 0),
                (0.55, BAY + 0.12, 0.26), MAT_IRON, "Ironwork")
        add_box(f"Ledge_{s}", (s * (A + 0.05), 0, VALLEY_Z + 0.45), (1, 0, 0),
                (0.85, BAY + 0.12, 0.05), MAT_TIMBER, "Purlins")
    add_box("RidgeCap", (0, 0, CROWN + 0.045), (1, 0, 0),
            (0.26, BAY + 0.06, 0.09), MAT_TIMBER, "Purlins")

    # purlins (longitudinal, under the glass, at profile stations)
    for i in range(2, len(cpts) - 1, 4):
        p, n = Vector(cpts[i]), cnrm[i]
        t = Vector(cpts[i + 1]) - Vector(cpts[i - 1])
        c = p - n * 0.075
        add_box(f"PurlinC_{i}", (c.x, 0, c.z), t.normalized(), (0.10, BAY, 0.12),
                MAT_TIMBER, "Purlins")
    for s in (1, -1):
        spts, snrm = side_pts(s, 11)
        for i in range(2, len(spts) - 1, 3):
            p, n = Vector(spts[i]), snrm[i]
            t = Vector(spts[i + 1]) - Vector(spts[i - 1])
            c = p - n * 0.07
            add_box(f"PurlinS_{s}_{i}", (c.x, 0, c.z), t.normalized(), (0.09, BAY, 0.11),
                    MAT_TIMBER, "Purlins")

    # glazing: ridge-and-furrow glass + bars following each profile
    NY = 12
    ys = [-BAY / 2 + BAY * j / NY for j in range(NY + 1)]
    zoff = [FURROW_AMP if j % 2 == 0 else 0.0 for j in range(NY + 1)]

    def glass_mesh(name, pts, nrms):
        verts, faces = [], []
        for i, p in enumerate(pts):
            for j, yy in enumerate(ys):
                v = Vector(p) + nrms[i] * (zoff[j] + 0.012)
                verts.append((v.x, yy, v.z))
        for i in range(len(pts) - 1):
            for j in range(NY):
                a = i * (NY + 1) + j; b = a + NY + 1
                faces.append((a, b, b + 1, a + 1))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces); me.update()
        ob = bpy.data.objects.new(name, me)
        ob.data.materials.append(MAT_GLASS)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    g1 = glass_mesh("GlassCentral", cpts, cnrm); glass_groups.append(g1)
    for s in (1, -1):
        spts, snrm = side_pts(s, 11)
        g = glass_mesh(f"GlassSide_{s}", spts, snrm); glass_groups.append(g)

    # glazing bars on the ridge lines of the furrows
    def bars_for(pts, nrms, tag):
        for j in range(0, NY + 1, 2):
            for i in range(len(pts) - 1):
                seg_box(f"Bar_{tag}_{j}_{i}",
                        (pts[i][0], ys[j], pts[i][2]), (pts[i + 1][0], ys[j], pts[i + 1][2]),
                        0.045, 0.03, MAT_TIMBER, "Bars",
                        normal_off=zoff[j] + 0.028, n1=nrms[i], n2=nrms[i + 1])
    bars_for(cpts, cnrm, "C")
    for s in (1, -1):
        spts, snrm = side_pts(s, 11)
        bars_for(spts, snrm, f"S{s}")

    # plinth walls with arched recess panels (photo-read), along y
    for s in (-1, 1):
        add_box(f"Plinth_{s}", (s * (HW - 0.02), 0, PLINTH_H / 2), (1, 0, 0),
                (0.45, BAY + 0.12, PLINTH_H), MAT_STONE, "Plinth")
        # arch recess: flat arch-shaped panel on the outer face
        X0 = s * (HW - 0.02 + 0.228)
        r, yb, zb = 0.72, 0.0, 0.30
        av = []
        av.append((X0, yb - r, 0.08)); av.append((X0, yb - r, zb))
        for k in range(9):
            a = math.pi - math.pi * k / 8
            av.append((X0, yb + r * math.cos(a), zb + r * math.sin(a)))
        av.append((X0, yb + r, 0.08))
        me = bpy.data.meshes.new(f"ArchRecess_{s}")
        me.from_pydata(av, [], [tuple(range(len(av)))]); me.update()
        ob = bpy.data.objects.new(f"ArchRecess_{s}", me)
        ob.data.materials.append(MAT_STONE_D)
        bpy.context.scene.collection.objects.link(ob)
        glass_groups.append(ob)  # keep with unjoined singles (renamed below)

    # ventilator band: diagonal lattice panels at the foot of each side
    for s in (-1, 1):
        X = s * (HW - 0.115)
        zw, zh = 1.05, 2.00
        zmid = (zw + zh) / 2
        for k in range(3):
            yc = -BAY / 2 + BAY * (k + 0.5) / 3
            cw = BAY / 3
            add_box(f"VentT_{s}_{k}", (X, yc, zh - 0.03), (1, 0, 0), (0.04, cw, 0.06),
                    MAT_TIMBER, "Vent")
            add_box(f"VentB_{s}_{k}", (X, yc, zw + 0.03), (1, 0, 0), (0.04, cw, 0.06),
                    MAT_TIMBER, "Vent")
            diag_len = math.hypot(cw - 0.08, zh - zw - 0.10)
            ang = math.atan2(zh - zw - 0.10, cw - 0.08)
            for sgn in (1, -1):
                yd = Vector((0, math.cos(ang * sgn), math.sin(ang * sgn)))
                add_box(f"VentD_{s}_{k}_{sgn}", (X, yc, zmid), (1, 0, 0), (0.035, diag_len, 0.05),
                        MAT_TIMBER, "Vent", ydir=yd)

    # join groups into single meshes
    for grp, new in (("RibsCentral", "Ribs_Central_Laminated"),
                     ("RibsSide", "Ribs_SideArches"),
                     ("Ironwork", "Ironwork_Pillars_Gutters"),
                     ("Purlins", "Purlins_Ridge_Valley"),
                     ("Bars", "GlazingBars"),
                     ("Plinth", "PlinthWalls"),
                     ("Vent", "VentilatorBand")):
        ob = join_group(grp, new)
        if ob:
            model.objects.link(ob) if ob.name not in model.objects else None
    for ob in glass_groups:
        if ob.name not in model.objects:
            model.objects.link(ob)
    # move any stragglers created in scene collection into Model
    for ob in list(bpy.context.scene.collection.objects):
        if ob.name not in model.objects:
            model.objects.link(ob)

    # ------------------------------------------------------------ render setup
    setup = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(setup)
    bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, -0.01))
    gp = bpy.context.object; gp.name = "BackdropGround"
    gm = get_mat("BackdropGrey", (0.52, 0.52, 0.52), rough=1.0)
    gp.data.materials.append(gm)
    setup.objects.link(gp); bpy.context.scene.collection.objects.unlink(gp)

    sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 3.0; sun.angle = 0.12
    so = bpy.data.objects.new("Sun", sun); so.rotation_euler = (math.radians(48), 0, math.radians(-35))
    setup.objects.link(so)
    fill = bpy.data.lights.new("Fill", 'AREA'); fill.energy = 900; fill.shape = 'DISK'; fill.size = 40
    fo = bpy.data.objects.new("Fill", fill); fo.location = (-25, 30, 30)
    fo.rotation_euler = (math.radians(120), 0, math.radians(150))
    setup.objects.link(fo)

    def look_at(ob, target):
        d = Vector(target) - ob.location
        ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

    cams = {}
    for nm, loc, tgt in (("front", (0, -72, 11.0), (0, 0, 9.8)),
                         ("side", (65, 0, 10.5), (0, 0, 9.8)),
                         ("three-quarter", (40, -46, 28), (0, 0, 8.0))):
        cd = bpy.data.cameras.new(nm); cd.lens = 50
        co = bpy.data.objects.new("Cam_" + nm, cd)
        co.location = loc; look_at(co, tgt)
        setup.objects.link(co); cams[nm] = co

    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 96
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 960, 640
    sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.45, 0.45, 0.45, 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

    # tidy: mesh datablocks take their object names
    for ob in model.objects:
        if ob.type == 'MESH':
            ob.data.name = ob.name

    os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SLUG + ".blend"))

    # GLB: Model collection only
    bpy.ops.object.select_all(action='DESELECT')
    for ob in model.objects:
        ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, SLUG + ".glb"),
                              export_format='GLB', use_selection=True)

    for nm, co in cams.items():
        sc.camera = co
        sc.render.filepath = os.path.join(HERE, "renders", nm + ".png")
        bpy.ops.render.render(write_still=True)

    # report counts
    tris = 0
    for ob in model.objects:
        if ob.type == 'MESH':
            tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
    print(f"RESULT objects={len(model.objects)} triangles={tris}")

build()
