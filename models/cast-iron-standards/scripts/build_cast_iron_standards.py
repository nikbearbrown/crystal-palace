#!/usr/bin/env python3
"""Build the four Crystal Palace cast-iron standards A-D (Downes 1852, Plate 20a).

Hyde Park 1851 building components. Procedural bpy, Blender 4.2.
Real-world metres. Each standard is ONE joined mesh object (Standard_A..D),
origin at its base centre, standing in a row on a neutral grey rig.
Dimensions: plate measured at ~22.5 px/in against its own printed dimensions
(6 in waist and 9 in bolt spacings on Standard D, 2.25 in angle legs and
7/8 in rivets on Standard B, 4 in strap width on Standard A, Fig. 5).
"""
import bpy
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/cast-iron-standards")
RENDERS = os.path.join(OUT, "renders")
os.makedirs(RENDERS, exist_ok=True)

IN = 0.0254  # inch in metres

# ---------------------------------------------------------------- materials
def make_mat(name, color, metallic=0.85, rough=0.55):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return m

IRON = None   # set in main after scene clear
TIMBER = None
GREY = None

# ---------------------------------------------------------------- helpers
def apply_scale(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

def bevel(obj, width=0.0016, segments=1):
    mod = obj.modifiers.new("bev", 'BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)

def box(name, size, loc, mat, bev=0.0016):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.dimensions = size
    apply_scale(o)
    if mat:
        o.data.materials.append(mat)
    if bev:
        bevel(o, bev)
    return o

def cyl(name, r, depth, loc, axis='Z', mat=None, verts=14):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    if axis == 'X':
        o.rotation_euler = (0, math.radians(90), 0)
    elif axis == 'Y':
        o.rotation_euler = (math.radians(90), 0, 0)
    if mat:
        o.data.materials.append(mat)
    return o

def rivet(name, loc, axis, r=0.0159, mat=None):
    """Squashed-sphere rivet head; axis = outward normal direction ('+Y','-Y','+X','-X')."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=5, radius=r, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    if axis in ('+Y', '-Y'):
        o.scale = (1.0, 0.5, 1.0)
    elif axis in ('+X', '-X'):
        o.scale = (0.5, 1.0, 1.0)
    else:
        o.scale = (1.0, 1.0, 0.5)
    apply_scale(o)
    if mat:
        o.data.materials.append(mat)
    return o

def prism(name, outline, axis, thickness, mat, bev=0.0012, center=0.0):
    """Extrude a 2D outline (list of (u,v)) along an axis.
    axis 'Y': outline is (x,z), extrusion along Y centred on `center`.
    axis 'X': outline is (y,z), extrusion along X centred on `center`.
    axis 'Z': outline is (x,y), extrusion along Z from `center` upward."""
    n = len(outline)
    verts = []
    if axis == 'Y':
        for s in (-thickness / 2, thickness / 2):
            for (u, v) in outline:
                verts.append((u, center + s, v))
    elif axis == 'X':
        for s in (-thickness / 2, thickness / 2):
            for (u, v) in outline:
                verts.append((center + s, u, v))
    else:  # Z
        for s in (0.0, thickness):
            for (u, v) in outline:
                verts.append((u, v, center + s))
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))                    # back cap
    faces.append(tuple(range(n, 2 * n)))                         # front cap
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if mat:
        me.materials.append(mat)
    if bev:
        bevel(o, bev)
    return o

def ring_prism(name, outline, rings, mat, bev=0.0):
    """Outline (x,y) lofted through rings = [(z, sx, sy), ...]; capped."""
    n = len(outline)
    verts = []
    for (z, sx, sy) in rings:
        for (u, v) in outline:
            verts.append((u * sx, v * sy, z))
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    top = (len(rings) - 1) * n
    faces.append(tuple(range(top, top + n)))
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            a, b = r * n + i, r * n + j
            c, d = (r + 1) * n + j, (r + 1) * n + i
            faces.append((a, b, c, d))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if mat:
        me.materials.append(mat)
    if bev:
        bevel(o, bev)
    return o

def catmull_sample(points, samples_per_seg=10):
    """points: [(t, v)] sorted by t; returns dense [(t, v)] with smooth curve."""
    pts = [(points[0][0] - (points[1][0] - points[0][0]), 2 * points[0][1] - points[1][1])] + \
          list(points) + \
          [(points[-1][0] + (points[-1][0] - points[-2][0]), 2 * points[-1][1] - points[-2][1])]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples_per_seg):
            u = s / samples_per_seg
            u2, u3 = u * u, u * u * u
            t = p1[0] * (1 - u) + p2[0] * u
            v = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * u +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)
            out.append((t, v))
    out.append(points[-1])
    return out

def join_parts(parts, name):
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    o.name = name
    return o

# ================================================================ STANDARD A
def build_A():
    parts = []
    H = 2.192                      # overall height (m), tab top
    strap_w = 4 * IN               # 0.1016 face width (Fig. 5 dimension)
    strap_t = 1.375 * IN           # thickness (Fig. 5 fraction label, read as 1 3/8)
    gap = 0.94 * IN                # clear gap between straps (measured)
    pitch = gap + strap_t
    # boss/pin heights on the strap (z, m) read from Fig. 7
    boss_z = [0.376, 0.818, 1.414, 1.872]
    boss_r = 1.95 * IN
    neck_hw = 1.42 * IN            # half width of waisted neck
    clamp_z = (1.02, 1.30)         # slotted clamp zone: full width

    def half_w(z):
        w = neck_hw
        # end discs
        for zc, r in ((0.0508, 0.0508), (2.141, 0.0508)):
            d = abs(z - zc)
            if d < r:
                w = max(w, math.sqrt(r * r - d * d))
        for zc in boss_z:
            d = abs(z - zc)
            if d < boss_r:
                w = max(w, math.sqrt(boss_r * boss_r - d * d))
        if clamp_z[0] <= z <= clamp_z[1]:
            w = max(w, strap_w / 2)
        # top tab: narrower rounded tongue above the clevis pin (Fig. 7)
        d = abs(z - 2.138)
        if d < 1.42 * IN:
            w = max(w, math.sqrt((1.42 * IN) ** 2 - d * d)) if z > 2.052 else w
        return min(w, strap_w / 2)

    outline = []
    zs = [i * 0.012 for i in range(int(H / 0.012) + 1)] + [H]
    for z in zs:
        outline.append((half_w(z), z))
    for z in reversed(zs):
        outline.append((-half_w(z), z))
    for sy in (-pitch / 2, pitch / 2):
        parts.append(prism("A_strap", outline, 'Y', strap_t, IRON, center=sy))
        # central raised rib on the outer face (interpretation of Fig. 7 centre lines)
        rib = box("A_rib", (1.15 * IN, 0.004, 1.86),
                  (0, sy + (strap_t / 2 + 0.002) * (1 if sy > 0 else -1), 1.06), IRON, bev=0.001)
        parts.append(rib)
    # distance bosses + through pins
    pin_z = [0.104, 0.376, 0.818, 1.414, 1.872, 2.052]
    for z in pin_z:
        parts.append(cyl("A_boss", 1.2 * IN, gap, (0, 0, z), axis='Y', mat=IRON))
        parts.append(cyl("A_pin", 0.5625 * IN, pitch + strap_t + 0.012, (0, 0, z), axis='Y', mat=IRON))
        for sy in (-(pitch / 2 + strap_t / 2 + 0.004), pitch / 2 + strap_t / 2 + 0.004):
            parts.append(rivet("A_pinhead", (0, sy, z), '+Y' if sy > 0 else '-Y', r=0.81 * IN, mat=IRON))
    # clamp gussets (brace connection, Figs. 5/7): plates on outer faces + big rivets
    for sy in (-(pitch / 2 + strap_t / 2), pitch / 2 + strap_t / 2):
        parts.append(box("A_gusset", (0.115, 0.012, 0.28),
                         (0, sy + (0.006 if sy > 0 else -0.006), 1.16), IRON, bev=0.002))
        for z in (1.075, 1.245):
            parts.append(rivet("A_gusset_rivet",
                               (0, sy + (0.014 if sy > 0 else -0.014), z),
                               '+Y' if sy > 0 else '-Y', r=0.95 * IN, mat=IRON))
    # foot bracket M (Figs. 21-23): paired curved cheeks + feet + base plate N
    prof = [(0.0, 0.305), (0.05, 0.298), (0.12, 0.262), (0.19, 0.205), (0.26, 0.140),
            (0.33, 0.088), (0.40, 0.058), (0.432, 0.050), (0.432, 0.0), (0.0, 0.0)]
    for sx in (-1, 1):
        parts.append(prism("A_bracket", prof, 'X', 1.0 * IN, IRON, center=sx * (1.25 * IN + 0.5 * IN)))
        parts.append(box("A_foot", (2.75 * IN, 0.462, 0.025),
                         (sx * (1.25 * IN + 1.375 * IN), 0.201, 0.0325), IRON, bev=0.002))
        for (yy, zz, rr) in ((0.09, 0.10, 1.0 * IN), (0.29, 0.07, 1.0 * IN), (0.055, 0.215, 0.75 * IN)):
            parts.append(rivet("A_bracket_bolt",
                               (sx * (1.25 * IN + 1.0 * IN + 0.004), yy, zz),
                               '+X' if sx > 0 else '-X', r=rr, mat=IRON))
    parts.append(box("A_baseplate_N", (0.23, 0.50, 0.02), (0, 0.20, 0.01), IRON, bev=0.002))
    return join_parts(parts, "Standard_A")

# ================================================================ STANDARD B
ANGLE_OUTLINE_CACHE = {}
def angle_outline(hx, hy):
    """L cross-section outline (x,y) for the corner angle at (+hx,+hy), legs inward."""
    leg, th = 2.25 * IN, 0.25 * IN
    return [(hx, hy), (hx - leg, hy), (hx - leg, hy - th), (hx - th, hy - th),
            (hx - th, hy - leg), (hx, hy - leg)]

def mirrored(outline, mx, my):
    return [(x * mx, y * my) for (x, y) in outline]

def build_BC(is_c, height, hy, shaft_z, pins_z, rows_z, tongue_top_z, top_pin_z):
    parts = []
    hx = 5.0 * IN / 2
    z0, z1 = shaft_z
    if not is_c:
        for mx in (1, -1):
            for my in (1, -1):
                ol = mirrored(angle_outline(hx, hy), mx, my)
                if mx * my < 0:
                    ol = list(reversed(ol))
                parts.append(prism("angle", ol, 'Z', z1 - z0, IRON, center=z0))
        # face plates closing the box between angle legs (front/back narrow, sides wider)
        th = 0.375 * IN
        fw = 2 * (hx - 2.25 * IN)   # front plate width (0.5 in)
        sw = 2 * (hy - 2.25 * IN)   # side plate width (1.8 in)
        for sy in (1, -1):
            parts.append(box("B_faceplate", (fw, th, z1 - z0), (0, sy * (hy - th / 2), (z0 + z1) / 2), IRON, bev=0.001))
        for sx in (1, -1):
            parts.append(box("B_sideplate", (th, sw, z1 - z0), (sx * (hx - th / 2), 0, (z0 + z1) / 2), IRON, bev=0.001))
        # stitch rivets on all four faces
        for z in rows_z:
            for x in (-(hx - 1.125 * IN), hx - 1.125 * IN):
                for sy in (1, -1):
                    parts.append(rivet("B_rivet", (x, sy * (hy + 0.002), z), '+Y' if sy > 0 else '-Y', mat=IRON))
            for y in (-(hy - 1.125 * IN), hy - 1.125 * IN):
                for sx in (1, -1):
                    parts.append(rivet("B_rivet", (sx * (hx + 0.002), y, z), '+X' if sx > 0 else '-X', mat=IRON))
        # splice plates on the side faces at mid height (Fig. 13 hatched insert)
        for sx in (1, -1):
            parts.append(box("B_splice", (0.006, sw + 0.02, 0.21), (sx * (hx + 0.003), 0, 1.155), IRON, bev=0.001))
    else:
        # C: corner angles lofted with a gentle barrel taper (Fig. 14), no face plates
        rings_z = [z0, 0.70, 1.10, 1.50, z1]
        taper = [0.945, 0.988, 1.0, 0.988, 0.945]
        rings = [(z, 1.0, t) for z, t in zip(rings_z, taper)]
        for mx in (1, -1):
            for my in (1, -1):
                ol = mirrored(angle_outline(hx, hy), mx, my)
                if mx * my < 0:
                    ol = list(reversed(ol))
                parts.append(ring_prism("C_angle", ol, rings, IRON))
        # central tie bar (centre line member in Fig. 14)
        parts.append(box("C_tiebar", (0.25 * IN, 3.5 * IN, z1 - z0), (0, 0, (z0 + z1) / 2), IRON, bev=0.001))
        # batten bands wrapping the section
        for z in (0.21, 0.48, 0.83, 1.19, 1.55, 1.90):
            t = 1.0 - 0.065 * ((z - 1.10) / 1.10) ** 2
            wy = hy * t + 0.004
            wx = hx + 0.004
            parts.append(box("C_batten_f", (2 * wx, 0.0095, 2.5 * IN), (0, wy - 0.0048, z), IRON, bev=0.001))
            parts.append(box("C_batten_b", (2 * wx, 0.0095, 2.5 * IN), (0, -wy + 0.0048, z), IRON, bev=0.001))
            parts.append(box("C_batten_l", (0.0095, 2 * wy, 2.5 * IN), (wx - 0.0048, 0, z), IRON, bev=0.001))
            parts.append(box("C_batten_r", (0.0095, 2 * wy, 2.5 * IN), (-wx + 0.0048, 0, z), IRON, bev=0.001))
            for x in (-0.032, 0.032):
                for sy in (1, -1):
                    parts.append(rivet("C_batten_rivet", (x, sy * (wy + 0.003), z), '+Y' if sy > 0 else '-Y', r=0.0135, mat=IRON))
        # timber packing block K inside the frame (Fig. 14)
        parts.append(box("K_block", (0.10, 0.105, 0.26), (0, 0, 1.06), TIMBER, bev=0.002))
        # stitch rivets along the angle legs, front/back faces only (as drawn)
        for z in rows_z:
            for x in (-(hx - 1.125 * IN), hx - 1.125 * IN):
                for sy in (1, -1):
                    parts.append(rivet("C_rivet", (x, sy * (hy * (1.0 - 0.065 * ((z - 1.10) / 1.10) ** 2) + 0.002), z),
                                       '+Y' if sy > 0 else '-Y', mat=IRON))
    # cross pins through the side centre plates (B) / frame (C)
    for z in pins_z:
        parts.append(cyl("pin", 0.5625 * IN, 2 * hx + 0.004, (0, 0, z), axis='X', mat=IRON))
        for sx in (1, -1):
            parts.append(rivet("pinhead", (sx * (hx + 0.003), 0, z), '+X' if sx > 0 else '-X', r=1.0 * IN, mat=IRON))
    # end tongues + pins (top into girder G clevis, bottom over girder H)
    for (za, zb, pinz, cap_top) in ((z0 - 0.15, z0 + 0.15, 0.073, False), (z1 - 0.15, tongue_top_z, top_pin_z, True)):
        mid = (za + zb) / 2
        parts.append(box("tongue", (0.375 * IN, 1.8 * IN, zb - za), (0, 0, mid), IRON, bev=0.002))
        if cap_top:
            parts.append(cyl("tongue_cap", 0.9 * IN, 0.375 * IN, (0, 0, zb), axis='X', mat=IRON))
        parts.append(cyl("tongue_pin", 0.6875 * IN, 2 * hx + 0.018, (0, 0, pinz), axis='X', mat=IRON))
        for sx in (1, -1):
            parts.append(rivet("tongue_pinhead", (sx * (hx + 0.006), 0, pinz), '+X' if sx > 0 else '-X', r=0.95 * IN, mat=IRON))
    return parts

def build_B():
    rows = [0.235, 0.47, 0.75, 1.02, 1.29, 1.57, 1.85]
    pins = [0.35, 0.60, 0.88, 1.16, 1.43, 1.71, 1.99]
    parts = build_BC(False, 2.207, 6.3 * IN / 2, (0.15, 2.06), pins, rows, 2.207, 2.174)
    return join_parts(parts, "Standard_B")

def build_C():
    rows = [0.28, 0.62, 0.96, 1.30, 1.64, 1.95]
    pins = [0.35, 0.88, 1.43, 1.99]
    parts = build_BC(True, 2.195, 5.2 * IN / 2, (0.15, 2.05), pins, rows, 2.195, 2.12)
    return join_parts(parts, "Standard_C")

# ================================================================ STANDARD D
def build_D():
    parts = []
    plate_t = 0.875 * IN
    # flange (in-plane) profile: half width vs z, waist 6 in at z=0.975 (Fig. 18)
    fw = [(0.045, 8.75 * IN), (0.20, 7.3 * IN), (0.35, 5.25 * IN), (0.55, 4.0 * IN),
          (0.78, 3.35 * IN), (0.975, 3.1 * IN), (1.17, 3.4 * IN), (1.35, 4.05 * IN),
          (1.52, 5.0 * IN), (1.68, 6.6 * IN), (1.82, 8.85 * IN), (1.885, 9.9 * IN)]
    dense = catmull_sample(fw, 7)
    outline = [(w, z) for (z, w) in dense] + [(-w, z) for (z, w) in reversed(dense)]
    parts.append(prism("D_flange", outline, 'Y', plate_t, IRON, center=0.0))
    # web (perpendicular) profile: half depth vs z, gently convex (Fig. 19)
    wd = [(0.045, 2.85 * IN), (0.35, 2.64 * IN), (0.60, 2.54 * IN), (0.975, 2.60 * IN),
          (1.35, 2.54 * IN), (1.60, 2.64 * IN), (1.885, 2.85 * IN)]
    dense_w = catmull_sample(wd, 7)
    outline_w = [(d, z) for (z, d) in dense_w] + [(-d, z) for (z, d) in reversed(dense_w)]
    parts.append(prism("D_web", outline_w, 'X', plate_t, IRON, center=0.0))
    # base + capital plates (19.8 in x 5.7 in from Fig. 18/19)
    parts.append(box("D_base", (19.8 * IN, 5.7 * IN, 0.045), (0, 0, 0.0225), IRON, bev=0.003))
    parts.append(box("D_capital", (19.8 * IN, 5.7 * IN, 0.05), (0, 0, 1.91), IRON, bev=0.003))
    # base bolts at 9 in spacing (Fig. 18 dimension)
    for x in (-9 * IN, 0.0, 9 * IN):
        parts.append(cyl("D_bolt", 0.6875 * IN, 0.028, (x, 0, 0.055), axis='Z', mat=IRON))
        parts.append(rivet("D_bolthead", (x, 0, 0.072), '+Z', r=0.95 * IN, mat=IRON))
    # waist boss: pads on web faces + through bolt (Figs. 19/20), pads on flange faces (Fig. 18)
    for sx in (1, -1):
        parts.append(box("D_boss", (0.019, 6.0 * IN, 0.23), (sx * (plate_t / 2 + 0.0095), 0, 0.975), IRON, bev=0.002))
    for sy in (1, -1):
        parts.append(box("D_boss_f", (4.0 * IN, 0.008, 0.16), (0, sy * (plate_t / 2 + 0.004), 0.975), IRON, bev=0.001))
    parts.append(cyl("D_bolt_waist", 0.4375 * IN, 0.115, (0, 0, 0.975), axis='X', mat=IRON))
    for sx in (1, -1):
        parts.append(rivet("D_bolt_waist_head", (sx * 0.055, 0, 0.975), '+X' if sx > 0 else '-X', r=0.75 * IN, mat=IRON))
    # top tongue into girder G (Fig. 19)
    parts.append(box("D_tongue", (0.875 * IN, 1.8 * IN, 0.13), (0, 0, 1.975), IRON, bev=0.002))
    parts.append(cyl("D_tongue_cap", 0.9 * IN, 0.875 * IN, (0, 0, 2.04), axis='X', mat=IRON))
    parts.append(cyl("D_top_pin", 0.6875 * IN, 0.095, (0, 0, 1.985), axis='X', mat=IRON))
    for sx in (1, -1):
        parts.append(rivet("D_top_pinhead", (sx * 0.048, 0, 1.985), '+X' if sx > 0 else '-X', r=0.9 * IN, mat=IRON))
    return join_parts(parts, "Standard_D")

# ================================================================ rig + main
def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def build_rig():
    rig = []
    floor = box("Backdrop_floor", (40, 40, 0.1), (0, 0, -0.05), GREY, bev=0)
    wall = box("Backdrop_wall", (40, 0.1, 14), (0, 5.2, 7), GREY, bev=0)
    rig += [floor, wall]
    def light(name, loc, energy, size, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy = energy
        ld.shape = 'DISK'
        ld.size = size
        ld.color = color
        o = bpy.data.objects.new(name, ld)
        bpy.context.collection.objects.link(o)
        o.location = loc
        look_at(o, (0, 0, 1.0))
        return o
    rig.append(light("Key", (-5, -6, 7), 1100, 5.0))
    rig.append(light("Fill", (6, -3, 3.5), 320, 4.0))
    rig.append(light("Rim", (1, 5, 6), 500, 3.0))
    return rig

def shot(name, loc, target, lens=55):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    o = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

def main():
    global IRON, TIMBER, GREY
    bpy.ops.wm.read_factory_settings(use_empty=True)
    IRON = make_mat("CastIron", (0.16, 0.16, 0.17), 0.85, 0.52)
    TIMBER = make_mat("Timber", (0.45, 0.32, 0.18), 0.0, 0.85)
    GREY = make_mat("BackdropGrey", (0.5, 0.5, 0.5), 0.0, 1.0)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    objs = []
    for builder, x in ((build_A, -1.65), (build_B, -0.55), (build_C, 0.55), (build_D, 1.65)):
        o = builder()
        o.location = (x, 0, 0)
        objs.append(o)

    build_rig()

    # stats
    total = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris = len(o.data.loop_triangles)
        total += tris
        bb = [o.matrix_world @ Vector(c) for c in o.boundBox] if False else None
        dims = o.dimensions
        print(f"STATS {o.name}: tris={tris} dims=({dims.x:.3f} x {dims.y:.3f} x {dims.z:.3f}) loc={tuple(round(v,2) for v in o.location)}")
    print(f"STATS TOTAL tris={total}")

    # save blend
    blend_path = os.path.join(OUT, "cast-iron-standards.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("saved", blend_path)

    # GLB: prop objects only
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    glb_path = os.path.join(OUT, "cast-iron-standards.glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', use_selection=True)
    print("saved", glb_path)

    if os.environ.get('BUILD_ONLY'):
        print('BUILD_ONLY: skipping renders')
        return
    # renders
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1300
    scene.render.resolution_y = 1020
    scene.world = bpy.data.worlds.new("W")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.32, 0.32, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    cams = {
        "front": shot("CamFront", (0, -6.6, 1.10), (0, 0, 1.02), lens=58),
        "side": shot("CamSide", (-7.6, 0, 1.12), (0, 0, 1.02)),
        "three-quarter": shot("CamTQ", (4.7, -4.9, 2.7), (0, 0, 0.92)),
    }
    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(RENDERS, name + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", name)

if __name__ == "__main__":
    main()
