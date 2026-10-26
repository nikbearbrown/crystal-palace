#!/usr/bin/env python3
"""Build hp-louvre-and-blind — Hyde Park 1851 opening louvre unit + canvas blind.

One 8 ft compartment-width unit of the upper-tier wall louvre bank, as
detailed on Downes Plate XXVII ("Details of machinery for moving
louvres", John Weale, April 1852): five S-corrugated galvanized
sheet-iron louvre blades E pivoting on 3/8 in pins in a timber case,
worked together by hoop-iron links L, two wooden bars M and a 3/8 in
connecting rod N from a worm-wheel O; the worm P is turned by the
grooved rope pulley Q with its endless rope R; 1 in shafting T runs
the length of the unit to an intermediate bearing S1 with crank U and
rod N' working a second pair of bars (the real shafting ran 108 ft
each side of the wheel — control D22 — and is cut at this unit's ends).

TWO STATES of the same prop, built as two posed copies side by side:
  collection Model_Open   — louvres open (blades rotated -42 deg, bars
                            raised 1 1/4 in), blind rolled UP.
  collection Model_Closed — louvres closed (blades nested shut), blind
                            DOWN over the bank.
The .glb exports Model_Open only. The canvas blind is the shading
element the film's scene plan pairs with this unit; Downes shows no
blind on Plate XXVII — its form here (head roller, two breadths with
a centre seam, bottom lath) is INFERRED, borrowing the only canvas
description in Downes (the roof canvas: two breadths, seam in the
centre, printed p.44). See NOTES.md.

Evidence: Downes Plate XXVII + text pp.39-40, 44; Plate XXII text for
the case; CONTROL-DIMENSIONS D22. Hyde Park 1851 ONLY.

Run: blender -b --python build_hp_louvre_and_blind.py
Outputs (in this folder): hp-louvre-and-blind.blend / .glb,
renders/front.png, side.png, three-quarter.png, closed-three-quarter.png
"""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
IN = 0.0254  # metres per inch

# ---------------------------------------------------------------- controls (inches)
UNIT_W      = 96.0     # one 8 ft wall compartment (Plate XXI subdivision) — module choice
K_W, K_T    = 10.0, 3.75   # wall plate K: 10 in wide (printed); 3 3/4 thick (plate-measured Fig.1)
K_TOP       = K_T
CASE_D      = 5.5      # case depth (plate-printed Fig.1 dim; Plate XXII: jambs 5 1/2 wide)
CASE_T      = 0.875    # case jamb/head thickness (Plate XXII text)
HEAD_UNDER  = K_TOP + 32.34   # case internal height (plate-measured)
HEAD_TOP    = HEAD_UNDER + CASE_T
PIN_Y       = -0.25    # blade pivot line: 2.5 in from case inner face (plate-measured)
PIN_Z0      = K_TOP + 3.46    # lowest blade pin above K top (plate-measured)
PITCH       = 6.40     # blade pitch (plate-measured: pins on Figs.1 and 2 agree)
N_BLADES    = 5        # five louvres above the wall plate (Downes text p.32; Plate XXVII)
PIN_D       = 0.375    # blade pivot pins (printed, text p.40)
BLADE_T     = 0.065    # sheet thickness (drawn); blade length between jambs:
BLADE_L     = 94.0
# Blade centreline profile: (d = inches toward EXTERIOR from pin, w = inches BELOW pin).
# Traced from Plate XXVII Fig.1 at the plate's own scale bar (70.8 px/in, checked
# against the printed 5 1/2 in dimension). Closed position.
BLADE_PROFILE = [(0.05, 0.35), (0.10, 0.02), (0.14, -0.55), (0.30, -1.35),
                 (0.48, -2.15), (0.57, -2.90), (0.58, -3.55), (0.50, -4.30),
                 (0.22, -4.95), (-0.18, -5.50), (-0.52, -5.95), (-0.70, -6.35),
                 (-0.62, -6.70), (-0.25, -6.95), (0.10, -7.06)]
# Lowest blade shuts against the sill strip: shortened drop (see NOTES).
BLADE_PROFILE_LOW = [(0.05, 0.35), (0.10, 0.02), (0.14, -0.55), (0.30, -1.35),
                     (0.48, -2.15), (0.56, -2.90), (0.52, -3.30), (0.30, -3.42)]
RIVET_W     = -2.90    # link rivet point on blade: 2.9 in below pin (plate-measured)
EYE_DROP    = 3.10     # link eye on bars M: 3.1 in below pin (plate-measured)
BAR_Y       = -3.00    # bars M centre plane (on case inner face)
BAR_W, BAR_T = 1.0, 0.5    # bars M section (plate-printed Fig.1: 1 in x 1/2 in)
BAR_GAP_C   = 0.8125   # bar centres either side of station centre (5/8 in gap, Fig.2)
LINK_W      = 1.0      # hoop-iron link width (printed, text p.40)
WPIN_D      = 0.4375   # wooden pins through bars (plate: 7/16 in at the eye, Fig.1)
ROD_D       = 0.375    # connecting rods N, N' (plate-printed Figs.1/14: 3/8 in)
BAR_LIFT    = 1.25     # bar travel, closed -> open (plate-measured from dashed lines)
OPEN_ANG    = math.radians(-42.0)   # blade rotation, closed -> open (dashed lines, Fig.1)

# Drive (plate-measured from Plate XXVII unless noted)
SHAFT_Y     = -8.58    # shafting T line, in front of case inner face
SHAFT_Z     = K_TOP + 3.75   # shaft centre height (printed Fig.10: 3 3/4 in above K)
SHAFT_D     = 1.0      # shafting T (printed Fig.9: "Shafting 1 inch dia.")
WORMWHEEL_D = 5.5      # worm-wheel O (plate-measured)
WORMWHEEL_W = 1.0
WORM_Z      = 4.40     # worm/pulley axis height
PULLEY_D    = 18.0     # rope pulley Q (plate-measured, ~17-19 in; 18 adopted)
PULLEY_Y    = -12.55
CRANK_THROW = 2.5      # crank U pin radius (plate-measured Figs.10/13)
STN2_X      = 36.0     # intermediate station (bearing S1 + crank + bars) — module choice

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

setup_col = bpy.data.collections.new("RenderSetup"); scene.collection.children.link(setup_col)

X = Vector((1, 0, 0)); Y = Vector((0, 1, 0)); Z = Vector((0, 0, 1))

# ---------------------------------------------------------------- materials
def principled(name, colour, roughness, metal=0.0, backface=True):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*colour, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs: bsdf.inputs["Metallic"].default_value = metal
    if not backface:
        try: m.use_backface_culling = True
        except Exception: pass
    return m

MAT_GALV   = principled("GalvanizedIron", (0.52, 0.54, 0.56), 0.46, metal=0.85)
MAT_PAINT  = principled("PaintedIron", (0.76, 0.74, 0.69), 0.58, metal=0.15)
MAT_STEEL  = principled("Steel", (0.42, 0.43, 0.45), 0.35, metal=0.9)
MAT_TIMBER = principled("PaintedTimber", (0.85, 0.82, 0.76), 0.65)   # case, wall plate
MAT_DEAL   = principled("DealTimber", (0.78, 0.66, 0.50), 0.82)      # bars, roller, lath
MAT_CANVAS = principled("Canvas", (0.80, 0.75, 0.65), 0.96)
MAT_CANVAS_D = principled("CanvasSeam", (0.72, 0.67, 0.57), 0.96)
MAT_ROPE   = principled("Rope", (0.52, 0.45, 0.35), 1.0)

# ---------------------------------------------------------------- helpers
def prism(name, profile, origin, axis_a, axis_b, axis_e, e0, e1, material, col):
    """Closed prism: (a,b) profile extruded e0..e1 along axis_e. World-space geometry."""
    O, A, B, E = (Vector(v) for v in (origin, axis_a, axis_b, axis_e))
    n = len(profile); verts = []
    for e in (e0, e1):
        for (a, b) in profile:
            verts.append(tuple(O + A * a + B * b + E * e))
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(name); mesh.from_pydata(verts, [], faces); mesh.update()
    bm = bmesh.new(); bm.from_mesh(mesh)
    if bm.calc_volume() < 0: bmesh.ops.reverse_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh); obj.data.materials.append(material)
    col.objects.link(obj); return obj

def box(name, centre, size, material, col):
    bpy.ops.mesh.primitive_cube_add(location=centre)
    obj = bpy.context.object; obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    for c in obj.users_collection: c.objects.unlink(obj)
    col.objects.link(obj); obj.name = name; return obj

def tube(name, p1, p2, r, material, col, seg=14):
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1; L = d.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=L,
                                        location=(p1 + p2) / 2)
    obj = bpy.context.object
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    obj.data.materials.append(material)
    for c in obj.users_collection: c.objects.unlink(obj)
    col.objects.link(obj); obj.name = name; return obj

def strut(name, p1, p2, w, t, material, col):
    """Flat bar between two points in a Y-Z plane; width along world X."""
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1; L = d.length
    bpy.ops.mesh.primitive_cube_add(location=(p1 + p2) / 2)
    obj = bpy.context.object; obj.dimensions = (w, t, L)
    zax = d.normalized(); xax = Vector((1, 0, 0)); yax = zax.cross(xax).normalized()
    xax = yax.cross(zax).normalized()
    m = Matrix((xax, yax, zax)).transposed()
    obj.rotation_mode = 'QUATERNION'; obj.rotation_quaternion = m.to_quaternion()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    for c in obj.users_collection: c.objects.unlink(obj)
    col.objects.link(obj); obj.name = name; return obj

def revolve(name, profile, centre, material, col, seg=56):
    """Profile (r, dy) closed loop revolved about the Y axis through centre."""
    cx, cy, cz = centre; n = len(profile); verts = []
    for i in range(seg + 1):
        th = 2 * math.pi * i / seg
        for (r, dy) in profile:
            verts.append((cx + r * math.cos(th), cy + dy, cz + r * math.sin(th)))
    faces = []
    for i in range(seg):
        for j in range(n):
            k = (j + 1) % n
            faces.append((i * n + j, i * n + k, (i + 1) * n + k, (i + 1) * n + j))
    mesh = bpy.data.meshes.new(name); mesh.from_pydata(verts, [], faces); mesh.update()
    bm = bmesh.new(); bm.from_mesh(mesh)
    if bm.calc_volume() < 0: bmesh.ops.reverse_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh); obj.data.materials.append(material)
    col.objects.link(obj); return obj

def curve_tube(name, points, radius, material, col, bevel_res=2):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = radius; cu.bevel_resolution = bevel_res
    sp = cu.splines.new('POLY'); sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points): p.co = (*co, 1.0)
    obj = bpy.data.objects.new(name, cu); col.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target='MESH')
    obj.data.materials.append(material); obj.name = name; return obj

def ribbon_profile(centreline, thick):
    """Closed thin polygon around a (d, w) centreline in the Y-Z plane."""
    pts = [Vector(p) for p in centreline]; left, right = [], []
    for i, p in enumerate(pts):
        q = pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]
        n = Vector((-q.y, q.x)).normalized() * (thick / 2)
        left.append(tuple(p + n)); right.append(tuple(p - n))
    return left + right[::-1]

def rot_x(v, a):
    c, s = math.cos(a), math.sin(a)
    return Vector((v.x, v.y * c - v.z * s, v.y * s + v.z * c))

# ---------------------------------------------------------------- unit builder
def build_unit(state, xoff, col):
    """state: 'open' or 'closed'. All dimensions inches -> metres via IN.
       Local origin: x = unit centre, z = 0 at underside of wall plate K."""
    opn = (state == 'open')
    ang = OPEN_ANG if opn else 0.0
    lift = BAR_LIFT if opn else 0.0
    ox = xoff
    def P(x, y, z):  # local inches -> world metres
        return Vector((ox + x * IN, y * IN, z * IN))

    # --- wall plate K
    box("WallPlate_K", P(0, -2.25, K_T / 2), (UNIT_W * IN, K_W * IN, K_T * IN), MAT_TIMBER, col)
    # --- case: jambs, head, lining strips, shut strip
    jx = UNIT_W / 2 - CASE_T / 2
    for s in (-1, 1):
        box(f"CaseJamb_{'L' if s<0 else 'R'}", P(s * jx, 0, (K_TOP + HEAD_UNDER) / 2),
            (CASE_T * IN, CASE_D * IN, (HEAD_UNDER - K_TOP) * IN), MAT_TIMBER, col)
        box(f"Lining_{'L' if s<0 else 'R'}", P(s * (jx - CASE_T / 2 - 0.55), -CASE_D / 2 + 0.19, (K_TOP + HEAD_UNDER) / 2),
            (1.1 * IN, 0.375 * IN, (HEAD_UNDER - K_TOP) * IN), MAT_TIMBER, col)
    box("CaseHead", P(0, 0, (HEAD_UNDER + HEAD_TOP) / 2),
        (UNIT_W * IN, CASE_D * IN, CASE_T * IN), MAT_TIMBER, col)
    box("LiningHead", P(0, -CASE_D / 2 + 0.19, HEAD_UNDER - 0.55),
        ((UNIT_W - 2) * IN, 0.375 * IN, 1.1 * IN), MAT_TIMBER, col)
    box("ShutStrip", P(0, -CASE_D / 2 + 0.19, K_TOP + 1.25),
        (91.8 * IN, 0.375 * IN, 2.5 * IN), MAT_DEAL, col)

    pin_z = [PIN_Z0 + i * PITCH for i in range(N_BLADES)]
    # --- pivot pins (fixed in case; blades turn on them)
    for i, pz in enumerate(pin_z):
        tube(f"PivotPin_{i}", P(-UNIT_W / 2 + 0.4, PIN_Y, pz), P(UNIT_W / 2 - 0.4, PIN_Y, pz),
             PIN_D / 2 * IN, MAT_STEEL, col, seg=12)

    # --- blades (origin at pin; rotation poses them)
    for i, pz in enumerate(pin_z):
        prof_in = BLADE_PROFILE_LOW if i == 0 else BLADE_PROFILE
        closed = ribbon_profile([(d, w) for (d, w) in prof_in], BLADE_T)
        obj = prism(f"Blade_{i}", [(a * IN, b * IN) for (a, b) in closed],
                    (0, 0, 0), Y, Z, X, -BLADE_L / 2 * IN, BLADE_L / 2 * IN, MAT_GALV, col)
        obj.location = P(0, PIN_Y, pz); obj.rotation_euler = (ang, 0, 0)
        roll = tube(f"BladeRoll_{i}", (-BLADE_L / 2 * IN, 0, 0), (BLADE_L / 2 * IN, 0, 0),
                    0.28 * IN, MAT_GALV, col, seg=12)
        roll.location = P(0, PIN_Y, pz); roll.rotation_euler = (ang, 0, 0)

    def blade_point(i, d, w):
        """World point of a blade-local (d, w) in this state's pose."""
        v = rot_x(Vector((0, d, w)), ang)
        return P(0, PIN_Y, pin_z[i]) + Vector((0, v.y * IN, v.z * IN))

    # --- bars M, links L, wooden pins at two stations
    stations = [("C", 0.0, True), ("E", STN2_X, False)]
    for tag, xs, is_centre in stations:
        for s in (-1, 1):
            box(f"BarsM_{tag}_{'L' if s<0 else 'R'}",
                P(xs + s * BAR_GAP_C, BAR_Y, (K_TOP + 0.2 + lift + HEAD_UNDER - 0.5 + lift) / 2),
                (BAR_W * IN, BAR_T * IN, (HEAD_UNDER - K_TOP - 0.7) * IN), MAT_DEAL, col)
        for i, pz in enumerate(pin_z):
            eye = Vector((ox + xs * IN, BAR_Y * IN, (pz - EYE_DROP + lift) * IN))
            riv = blade_point(i, 0.50, RIVET_W) + Vector((xs * IN, 0, 0))
            strut(f"Link_{tag}_{i}", riv, eye, LINK_W * IN, 0.07 * IN, MAT_STEEL, col)
            # eye ring (torus, axis X)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.36 * IN, minor_radius=0.155 * IN,
                                             major_segments=18, minor_segments=8, location=eye)
            eo = bpy.context.object; eo.rotation_euler = (0, math.radians(90), 0)
            eo.data.materials.append(MAT_STEEL)
            for c in eo.users_collection: c.objects.unlink(eo)
            col.objects.link(eo); eo.name = f"LinkEye_{tag}_{i}"
            tube(f"WoodPin_{tag}_{i}", Vector((ox + (xs - 1.35) * IN, BAR_Y * IN, (pz - EYE_DROP + lift) * IN)),
                 Vector((ox + (xs + 1.35) * IN, BAR_Y * IN, (pz - EYE_DROP + lift) * IN)),
                 WPIN_D / 2 * IN, MAT_DEAL, col, seg=10)
            tube(f"Rivet_{tag}_{i}", riv + Vector((0, -0.10 * IN, 0)), riv + Vector((0, 0.10 * IN, 0)),
                 0.16 * IN, MAT_STEEL, col, seg=8)

    # --- block a + rod N (centre station)
    blk_z = 33.55 + lift
    box("Block_a", P(0, BAR_Y, blk_z), (0.62 * IN, 0.55 * IN, 1.5 * IN), MAT_STEEL, col)
    for dz in (-0.95, 0.95):
        tube(f"BlockNut_{dz}", P(0, BAR_Y, blk_z + dz - 0.14), P(0, BAR_Y, blk_z + dz + 0.14),
             0.30 * IN, MAT_STEEL, col, seg=6)
    # worm-wheel O group (origin at wheel centre, posed by rotation)
    oc = P(0, SHAFT_Y, SHAFT_Z)
    o_ang = math.radians(-40) if opn else 0.0
    disc = tube("WormWheel_O", (-WORMWHEEL_W / 2 * IN, 0, 0), (WORMWHEEL_W / 2 * IN, 0, 0),
                WORMWHEEL_D / 2 * IN, MAT_PAINT, col, seg=28)
    disc.location = oc; disc.rotation_euler = (o_ang, 0, 0)
    sock = tube("WheelSocket_O", (-1.8 * IN, 0, 0), (1.8 * IN, 0, 0), 0.75 * IN, MAT_PAINT, col, seg=16)
    sock.location = oc; sock.rotation_euler = (o_ang, 0, 0)
    for k in range(20):
        a = 2 * math.pi * k / 20
        off = rot_x(Vector((0, (WORMWHEEL_D / 2 + 0.18) * math.cos(a), (WORMWHEEL_D / 2 + 0.18) * math.sin(a))), o_ang) * IN
        t = box(f"WheelTooth_{k}", oc + off, (WORMWHEEL_W * 0.92 * IN, 0.34 * IN, 0.40 * IN), MAT_PAINT, col)
        t.rotation_euler = (a + o_ang - math.pi / 2, 0, 0)
    pin_off = rot_x(Vector((0, 0, 2.2)), o_ang)
    opin = oc + Vector((0.95 * IN, pin_off.y * IN, pin_off.z * IN))
    tube("WheelPin_O", oc + Vector((0.45 * IN, pin_off.y * IN, pin_off.z * IN)),
         oc + Vector((1.45 * IN, pin_off.y * IN, pin_off.z * IN)), 0.28 * IN, MAT_STEEL, col, seg=10)
    # rod N from block to wheel pin, with fork cheeks
    rod_top = P(0, BAR_Y, blk_z - 0.75)
    tube("Rod_N", rod_top, opin, ROD_D / 2 * IN, MAT_STEEL, col, seg=10)
    for s in (-1, 1):
        dirv = (rod_top - opin).normalized()
        strut(f"Fork_{s}", opin + Vector((s * 0.33 * IN, 0, 0)) + dirv * 2.0 * IN,
              opin + Vector((s * 0.33 * IN, 0, 0)) - dirv * 0.9 * IN,
              0.16 * IN, 0.5 * IN, MAT_STEEL, col)

    # --- bearing S (two-piece) on cleat c
    box("BearingS_Base", P(0, -7.9, K_TOP + 0.3), (4.6 * IN, 3.4 * IN, 0.6 * IN), MAT_PAINT, col)
    for s in (-1, 1):
        box(f"BearingS_Cheek_{s}", P(s * 1.32, SHAFT_Y, (K_TOP + SHAFT_Z + 0.4) / 2),
            (0.8 * IN, 1.7 * IN, (SHAFT_Z - K_TOP + 0.4) * IN), MAT_PAINT, col)
    box("BearingS_Cap", P(0, SHAFT_Y, SHAFT_Z + 0.95), (3.5 * IN, 1.8 * IN, 0.6 * IN), MAT_PAINT, col)
    tube("BearingS_WormBoss", P(0, -6.6, WORM_Z), P(0, -8.2, WORM_Z), 0.85 * IN, MAT_PAINT, col, seg=14)
    box("Cleat_c", P(0, -8.9, K_TOP - 0.95), (3.4 * IN, 3.2 * IN, 1.9 * IN), MAT_TIMBER, col)

    # --- shafting T with end collars
    tube("Shafting_T", P(-47.5, SHAFT_Y, SHAFT_Z), P(40.5, SHAFT_Y, SHAFT_Z),
         SHAFT_D / 2 * IN, MAT_STEEL, col, seg=14)
    for cx in (-46.5, 39.5):
        tube(f"ShaftCollar_{cx}", P(cx - 0.4, SHAFT_Y, SHAFT_Z), P(cx + 0.4, SHAFT_Y, SHAFT_Z),
             0.75 * IN, MAT_PAINT, col, seg=14)

    # --- worm P + its shaft to pulley Q
    tube("WormShaft_P", P(0, -6.4, WORM_Z), P(0, PULLEY_Y, WORM_Z), 0.44 * IN, MAT_STEEL, col, seg=12)
    tube("WormCore", P(0, -10.6, WORM_Z), P(0, -6.6, WORM_Z), 0.40 * IN, MAT_STEEL, col, seg=12)
    helix = []
    turns, span = 7, 4.0
    for k in range(turns * 10 + 1):
        t = k / (turns * 10); a = 2 * math.pi * turns * t
        helix.append((ox + 0.42 * IN * math.cos(a), (-10.6 + span * t) * IN,
                      WORM_Z * IN + 0.42 * IN * math.sin(a)))
    curve_tube("WormThread", helix, 0.10 * IN, MAT_STEEL, col, bevel_res=1)

    # --- pulley Q (group origin at hub centre; spokes posed per state)
    qc = P(0, PULLEY_Y, WORM_Z)
    rim_prof = [(r * IN, dy * IN) for (r, dy) in
                [(8.05, -0.85), (8.95, -0.85), (9.0, -0.30), (8.55, 0.0),
                 (9.0, 0.30), (8.95, 0.85), (8.05, 0.85), (8.30, 0.0)]]
    rim = revolve("PulleyRim_Q", rim_prof, (qc.x, qc.y, qc.z), MAT_PAINT, col)
    q_ang = math.radians(25) if opn else 0.0
    hub = tube("PulleyHub_Q", qc + Vector((0, -0.85 * IN, 0)), qc + Vector((0, 0.85 * IN, 0)),
               1.35 * IN, MAT_PAINT, col, seg=20)
    for k in range(6):
        a = q_ang + k * math.pi / 3
        d = Vector((math.cos(a), 0, math.sin(a)))
        mid = qc + d * 5.1 * IN
        sp = box(f"PulleySpoke_{k}", mid, (7.6 * IN, 0.62 * IN, 1.05 * IN), MAT_PAINT, col)
        sp.rotation_euler = (0, -a, 0)
        tip = qc + d * 8.15 * IN
        tp = box(f"SpokeTip_{k}", tip, (1.15 * IN, 0.55 * IN, 1.9 * IN), MAT_PAINT, col)
        tp.rotation_euler = (0, -a, 0)

    # --- endless rope R (cut at -29.5 in; the loop continued down out of frame)
    Rr = 8.35
    rope_pts = [(ox - Rr * IN, PULLEY_Y * IN, -29.5 * IN), (ox - Rr * IN, PULLEY_Y * IN, (WORM_Z - 0.2) * IN)]
    for k in range(1, 24):
        a = math.pi + math.pi * k / 24
        rope_pts.append((ox + Rr * IN * math.cos(a), PULLEY_Y * IN, (WORM_Z + Rr * math.sin(a)) * IN))
    rope_pts.append((ox + Rr * IN, PULLEY_Y * IN, -29.5 * IN))
    curve_tube("Rope_R", rope_pts, 0.19 * IN, MAT_ROPE, col)

    # --- intermediate bearing S1 + crank U + rod N' (station E)
    bx = STN2_X
    box("BearingS1_Base", P(bx + 0.4, SHAFT_Y, K_TOP + 0.25), (3.0 * IN, 2.4 * IN, 0.5 * IN), MAT_PAINT, col)
    box("BearingS1_Stem", P(bx + 0.4, SHAFT_Y, (K_TOP + SHAFT_Z) / 2),
        (1.7 * IN, 1.5 * IN, (SHAFT_Z - K_TOP - 0.5) * IN), MAT_PAINT, col)
    tube("BearingS1_Boss", P(bx - 0.35, SHAFT_Y, SHAFT_Z), P(bx + 1.15, SHAFT_Y, SHAFT_Z),
         1.05 * IN, MAT_PAINT, col, seg=16)
    crank_c = P(bx - 1.9, SHAFT_Y, SHAFT_Z)
    c_ang = math.radians(-35) if opn else 0.0
    crank_prof = [(-0.81, -0.55), (-0.30, -0.83), (0.30, -0.83), (0.81, -0.55),
                  (0.86, 0.10), (0.46, 0.95), (0.27, CRANK_THROW), (-0.27, CRANK_THROW),
                  (-0.46, 0.95), (-0.86, 0.10)]
    crank = prism("Crank_U", [(a * IN, b * IN) for (a, b) in crank_prof],
                  (0, 0, 0), Y, Z, X, -0.24 * IN, 0.24 * IN, MAT_PAINT, col)
    crank.location = crank_c; crank.rotation_euler = (c_ang, 0, 0)
    cpin_off = rot_x(Vector((0, 0, CRANK_THROW)), c_ang)
    cpin = crank_c + Vector((0, cpin_off.y * IN, cpin_off.z * IN))
    tube("CrankPin_U", cpin + Vector((-0.55 * IN, 0, 0)), cpin + Vector((0.55 * IN, 0, 0)),
         0.28 * IN, MAT_STEEL, col, seg=10)
    n_top = Vector((ox + bx * IN, BAR_Y * IN, (13.6 + lift) * IN))
    tube("Rod_N1", cpin, n_top, ROD_D / 2 * IN, MAT_STEEL, col, seg=10)
    tube("RodN1_Pin", n_top + Vector((-1.35 * IN, 0, 0)), n_top + Vector((1.35 * IN, 0, 0)),
         WPIN_D / 2 * IN, MAT_DEAL, col, seg=10)

    # --- canvas blind on head roller (INFERRED assembly — see NOTES)
    # Roller hangs below the case head on the interior face; roll clears
    # the raised bars/block (checked: >0.3 in everywhere).
    ROLL_Y, ROLL_Z = -4.60, HEAD_UNDER - 2.40
    tube("BlindRoller", P(-47.3, ROLL_Y, ROLL_Z), P(47.3, ROLL_Y, ROLL_Z),
         1.25 * IN, MAT_DEAL, col, seg=14)
    for s in (-1, 1):
        box(f"BlindBracketArm_{s}", P(s * 47.35, -3.68, ROLL_Z),
            (0.3 * IN, 1.9 * IN, 0.45 * IN), MAT_PAINT, col)
        box(f"BlindBracketDrop_{s}", P(s * 47.35, ROLL_Y, ROLL_Z + 0.55),
            (0.3 * IN, 0.5 * IN, 2.6 * IN), MAT_PAINT, col)
    if opn:
        # blind UP: canvas rolled on the roller, short tail + lath hanging
        tube("BlindRoll", P(-46.5, ROLL_Y, ROLL_Z), P(46.5, ROLL_Y, ROLL_Z),
             2.3 * IN, MAT_CANVAS, col, seg=18)
        box("BlindTail", P(0, ROLL_Y - 0.12, ROLL_Z - 4.45), (93 * IN, 0.09 * IN, 4.3 * IN), MAT_CANVAS, col)
        box("BlindLath", P(0, ROLL_Y - 0.12, ROLL_Z - 6.85), (93 * IN, 0.55 * IN, 1.0 * IN), MAT_DEAL, col)
    else:
        # blind DOWN: two breadths (centre gap lets rod N pass), seam strips, laths
        for s in (-1, 1):
            cx = s * (1.1 + 45.4 / 2)
            seg_x, seg_z = 26, 12
            verts, faces = [], []
            z_top, z_bot = HEAD_UNDER - 1.30, K_TOP + 1.45
            for j in range(seg_z + 1):
                for i2 in range(seg_x + 1):
                    fx = i2 / seg_x; fz = j / seg_z
                    x = cx + (fx - 0.5) * 45.4
                    z = z_top + (z_bot - z_top) * fz
                    y = -4.85 + 0.34 * math.sin(x / 7.5) * math.sin(math.pi * min(fz * 1.15, 1.0)) \
                        + 0.10 * math.sin(z / 5.0)
                    verts.append((ox + x * IN, y * IN, z * IN))
            for j in range(seg_z):
                for i2 in range(seg_x):
                    a0 = j * (seg_x + 1) + i2
                    faces.append((a0, a0 + 1, a0 + seg_x + 2, a0 + seg_x + 1))
            mesh = bpy.data.meshes.new(f"BlindPanel_{s}")
            mesh.from_pydata(verts, [], faces); mesh.update()
            po = bpy.data.objects.new(f"BlindPanel_{s}", mesh)
            po.data.materials.append(MAT_CANVAS); col.objects.link(po)
            bpy.ops.object.select_all(action='DESELECT'); po.select_set(True)
            bpy.context.view_layer.objects.active = po
            mod = po.modifiers.new("thick", 'SOLIDIFY'); mod.thickness = 0.05 * IN
            bpy.ops.object.modifier_apply(modifier=mod.name)
            box(f"BlindSeam_{s}", P(s * 1.32, -4.88, (z_top + z_bot) / 2),
                (0.45 * IN, 0.07 * IN, (z_top - z_bot) * IN), MAT_CANVAS_D, col)
            box(f"BlindLath_{s}", P(cx, -4.85, z_bot - 0.45), (45.4 * IN, 0.55 * IN, 1.0 * IN), MAT_DEAL, col)

    return col

col_open = bpy.data.collections.new("Model_Open");   scene.collection.children.link(col_open)
col_closed = bpy.data.collections.new("Model_Closed"); scene.collection.children.link(col_closed)
build_unit('open', 0.0, col_open)
build_unit('closed', 3.90, col_closed)

# ---------------------------------------------------------------- render setup
world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9

def add_plane(name, size, z, material):
    mesh = bpy.data.meshes.new(name); s = size / 2
    mesh.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
    mesh.update(); obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material); setup_col.objects.link(obj); return obj

add_plane("Backdrop", 80, -0.86, principled("BackdropGrey", (0.60, 0.60, 0.60), 0.95))

def add_light(name, ltype, loc, energy, size=None):
    data = bpy.data.lights.new(name, ltype); data.energy = energy
    if size: data.shape = 'DISK'; data.size = size
    obj = bpy.data.objects.new(name, data); obj.location = loc
    setup_col.objects.link(obj); return obj

sun = add_light("Sun", 'SUN', (4, -3, 7), 3.2)
sun.rotation_euler = (math.radians(52), 0, math.radians(38))
add_light("SoftAbove", 'AREA', (0.5, -0.5, 6.5), 520, size=7.0)
fill = add_light("Fill", 'AREA', (-6, 3, 2.5), 300, size=5.0)
fill.rotation_euler = (math.radians(65), 0, math.radians(-115))

def look_at(cam, target):
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector(target) - cam.location).to_track_quat('-Z', 'Y')

def add_cam(name, loc, target, ortho=None, lens=40):
    data = bpy.data.cameras.new(name)
    if ortho: data.type = 'ORTHO'; data.ortho_scale = ortho
    else: data.lens = lens
    obj = bpy.data.objects.new(name, data); obj.location = loc
    setup_col.objects.link(obj); look_at(obj, target); return obj

tgt_o = (0, -0.10, 0.30)
cams = {
    "front":        add_cam("CamFront", (0, -8.5, 0.32), tgt_o, ortho=3.15),
    "side":         add_cam("CamSide", (8.5, -0.10, 0.15), (0, -0.10, 0.15), ortho=2.7),
    "three-quarter": add_cam("Cam34", (2.9, -3.7, 2.05), (0, -0.15, 0.22)),
    "closed-three-quarter": add_cam("Cam34C", (3.90 + 2.9, -3.7, 2.05), (3.90, -0.15, 0.22)),
}

scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
try: scene.cycles.device = 'CPU'
except Exception: pass
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False

# ---------------------------------------------------------------- save / export / render
blend_path = os.path.join(HERE, "hp-louvre-and-blind.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action='DESELECT')
for obj in col_open.objects: obj.select_set(True)
bpy.context.view_layer.objects.active = col_open.objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, "hp-louvre-and-blind.glb"),
                          export_format='GLB', use_selection=True)

def tri_count(col):
    return sum(len(p.vertices) - 2 for o in col.objects
               if o.type == 'MESH' for p in o.data.polygons)
print(f"OPEN:   {len(col_open.objects)} objects, {tri_count(col_open)} tris")
print(f"CLOSED: {len(col_closed.objects)} objects, {tri_count(col_closed)} tris")
print(f"UNIT (m): width {UNIT_W*IN:.3f}  height {(HEAD_TOP)*IN:.3f} (K underside to case head)")

os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
for name, cam in cams.items():
    scene.camera = cam
    # each render shows exactly one state (the staged copy beside it
    # would otherwise show through gaps in the side elevation)
    col_open.hide_render = (name == "closed-three-quarter")
    col_closed.hide_render = (name != "closed-three-quarter")
    scene.render.filepath = os.path.join(HERE, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
print("DONE")
