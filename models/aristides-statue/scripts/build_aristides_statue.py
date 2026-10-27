#!/usr/bin/env python3
"""Build the Aristides (or Aeschines) statue prop for the Crystal Palace film.

Profile-first procedural build from the Rijksmuseum stereograph
RP-F-2012-96-327 (CC0): the draped orator in clean side profile on its
0.90 m court plinth. Statue faces -X; its (photographed) left side is -Y;
the plinth's labelled face is -Y. All dimensions in metres.
Figure: 2.00 m cast (anchor shared with display-plinth / krater-vase builds).
"""
import bpy
import math
import random
from mathutils import Vector

random.seed(1877)

# ---------------------------------------------------------------- clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass

# ---------------------------------------------------------------- materials
def make_mat(name, rgb, rough=0.55):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

PLASTER = make_mat("CastPlaster", (0.885, 0.865, 0.825), 0.58)
PLASTER_BRIGHT = make_mat("CastPlasterSlab", (0.94, 0.925, 0.895), 0.5)
EBON = make_mat("EbonisedPlinth", (0.045, 0.04, 0.036), 0.42)
EBON_PLATE = make_mat("EbonisedLabelPlate", (0.10, 0.092, 0.082), 0.5)

SLAB_TOP = 1.05          # world z of the statue slab's top (plinth 0.90 + slab 0.15)
FIG = 2.00               # figure height, soles to crown

def finish(obj, mat, smooth=True):
    if mat:
        obj.data.materials.append(mat)
    if smooth and obj.type == 'MESH':
        for p in obj.data.polygons:
            p.use_smooth = True
    bpy.context.view_layer.objects.active = obj
    return obj

def mesh_obj(name, verts, faces, mat=None, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return finish(ob, mat, smooth)

# ================================================================ BODY LOFT
# Ring table: (z_f, front_u, back_u, half_width)  u measured from hem-front
# line; world x = u - 0.13.  z_f measured from the soles (slab top).
RINGS = [
    (0.14, -0.006, 0.268, 0.193),
    (0.22, -0.004, 0.258, 0.198),
    (0.32, -0.012, 0.254, 0.201),
    (0.45, -0.034, 0.250, 0.204),
    (0.58, -0.046, 0.246, 0.207),
    (0.72, -0.056, 0.243, 0.210),
    (0.86, -0.076, 0.239, 0.212),
    (0.97, -0.098, 0.236, 0.213),
    (1.07, -0.118, 0.235, 0.214),
    (1.16, -0.112, 0.237, 0.215),
    (1.26, -0.096, 0.241, 0.218),
    (1.35, -0.078, 0.246, 0.222),
    (1.43, -0.064, 0.256, 0.227),
    (1.52, -0.056, 0.256, 0.230),
    (1.58, -0.050, 0.250, 0.226),
    (1.64, -0.034, 0.242, 0.208),
    (1.69, -0.008, 0.222, 0.168),
    (1.73,  0.012, 0.198, 0.118),
    (1.75,  0.020, 0.185, 0.095),
]
NSEG = 64

def lean(z):
    """Slight forward (-x) lean of the whole draped mass, as photographed."""
    return -0.062 * max(0.0, min(1.0, (z - 0.60) / 1.05))

def hem_lift(phi, y):
    """Bottom edge of the drapery: flat 0.105 except a raised notch at the
    back-centre where the patterned support block stands between the feet."""
    backness = max(0.0, math.cos(phi))          # phi=0 -> +x (back)
    g = math.exp(-((backness - 1.0) / 0.45) ** 2) * math.exp(-(y / 0.085) ** 2)
    return 0.105 + 0.125 * g

def fold_scale(z, phi):
    """Radial fold displacement multiplier for one ring vertex."""
    s1 = 1.0 if z < 0.9 else max(0.30, 1.0 - (z - 0.9) * 0.85)
    if z < 0.6:
        s1 *= 1.25
    m = 1.0 + s1 * 0.020 * math.sin(9 * phi + 1.1 + 0.8 * math.sin(z * 2.2))
    m += 0.006 * math.sin(23 * phi + 2.0) * (0.4 + 0.6 * s1)
    # broad diagonal groove sweeping front -> left as z falls (himation fold)
    if 0.92 < z < 1.50:
        phid = math.pi + (1.46 - z) * 1.55
        d = math.atan2(math.sin(phi - phid), math.cos(phi - phid))
        m -= 0.011 * math.exp(-(d / 0.38) ** 2)
    m += random.uniform(-0.0012, 0.0012)
    return m

verts, faces = [], []
ring_start = []
for (z, fu, bu, hw) in RINGS:
    xc = (fu + bu) / 2.0 - 0.13 + lean(z)
    a = (bu - fu) / 2.0
    ring_start.append(len(verts))
    for j in range(NSEG):
        phi = 2.0 * math.pi * j / NSEG
        dx, dy = a * math.cos(phi), hw * math.sin(phi)
        m = fold_scale(z, phi)
        zz = SLAB_TOP + z
        if z == RINGS[0][0]:
            zz = SLAB_TOP + hem_lift(phi, dy)
        verts.append((xc + dx * m, dy * m, zz))
for i in range(len(RINGS) - 1):
    s0, s1 = ring_start[i], ring_start[i + 1]
    for j in range(NSEG):
        jn = (j + 1) % NSEG
        faces.append((s0 + j, s0 + jn, s1 + jn, s1 + j))
# bottom cap fan (under the hem, hidden) and top cap fan (under the neck)
z0, fu0, bu0, _ = RINGS[0]
xc0 = (fu0 + bu0) / 2.0 - 0.13 + lean(z0)
ci = len(verts); verts.append((xc0, 0.0, SLAB_TOP + 0.05))
for j in range(NSEG):
    faces.append((ci, ring_start[0] + (j + 1) % NSEG, ring_start[0] + j))
zt, fut, but, _ = RINGS[-1]
xct = (fut + but) / 2.0 - 0.13 + lean(zt)
ci = len(verts); verts.append((xct, 0.0, SLAB_TOP + zt + 0.03))
last = ring_start[-1]
for j in range(NSEG):
    faces.append((ci, last + j, last + (j + 1) % NSEG))
body = mesh_obj("DraperyBody", verts, faces, PLASTER)

# hem roll: a weighted cloth edge following the bottom ellipse
def tube(name, path_pts, thick, wide, mat, flat_axis='radial', xc_of_z=None,
         seg=10, cap_ends=True, taper=0.0):
    """Tube along a 3D path. Cross-section ellipse: `thick` along flat_axis
    ('radial' = away from body axis, 'y' = world Y), `wide` perpendicular."""
    pts = [Vector(p) for p in path_pts]
    # tangents
    tv, fv = [], []
    for i, p in enumerate(pts):
        p0 = pts[max(0, i - 1)]; p1 = pts[min(len(pts) - 1, i + 1)]
        t = (p1 - p0); t.normalize(); tv.append(t)
    vs, fs = [], []
    npts = len(pts)
    for i, p in enumerate(pts):
        if taper:
            fi = min(1.0, i / max(1.0, npts * taper), (npts - 1 - i) / max(1.0, npts * taper))
            rf = 0.30 + 0.70 * (fi * fi * (3 - 2 * fi))
        else:
            rf = 1.0
        if flat_axis == 'y':
            e1 = Vector((0, 1, 0))
        else:
            zf = p.z - SLAB_TOP
            xc = xc_of_z(zf) if xc_of_z else 0.0
            e1 = Vector((p.x - xc, p.y, 0.0))
            if e1.length < 1e-6: e1 = Vector((1, 0, 0))
            e1.normalize()
        e2 = tv[i].cross(e1)
        if e2.length < 1e-6: e2 = Vector((0, 0, 1))
        e2.normalize()
        e1 = e2.cross(tv[i]); e1.normalize()
        for j in range(seg):
            al = 2.0 * math.pi * j / seg
            off = e1 * (math.cos(al) * thick * rf) + e2 * (math.sin(al) * wide * rf)
            vs.append(tuple(p + off))
    for i in range(len(pts) - 1):
        for j in range(seg):
            jn = (j + 1) % seg
            fs.append((i * seg + j, i * seg + jn, (i + 1) * seg + jn, (i + 1) * seg + j))
    if cap_ends:
        for end_i, flip in ((0, True), (len(pts) - 1, False)):
            ci = len(vs); vs.append(tuple(pts[end_i]))
            base = end_i * seg
            for j in range(seg):
                jn = (j + 1) % seg
                fs.append((ci, base + jn, base + j) if flip else (ci, base + j, base + jn))
    return mesh_obj(name, vs, fs, mat)

def catmull(pts, samples):
    P = [Vector(p) for p in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(len(P) - 3):
        for k in range(samples):
            t = k / samples
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * P[i + 1]) + (-P[i] + P[i + 2]) * t +
                             (2 * P[i] - 5 * P[i + 1] + 4 * P[i + 2] - P[i + 3]) * t2 +
                             (-P[i] + 3 * P[i + 1] - 3 * P[i + 2] + P[i + 3]) * t3)))
    out.append(tuple(P[-2]))
    return out

def xc_at(zf):
    for i in range(len(RINGS) - 1):
        (z1, f1, b1, _), (z2, f2, b2, _) = RINGS[i], RINGS[i + 1]
        if z1 <= zf <= z2:
            t = (zf - z1) / (z2 - z1)
            return ((f1 + (f2 - f1) * t) + (b1 + (b2 - b1) * t)) / 2.0 - 0.13 + lean(zf)
    return (RINGS[-1][1] + RINGS[-1][2]) / 2.0 - 0.13 + lean(RINGS[-1][0])

def ab_at(zf):
    for i in range(len(RINGS) - 1):
        (z1, f1, b1, w1), (z2, f2, b2, w2) = RINGS[i], RINGS[i + 1]
        if z1 <= zf <= z2:
            t = (zf - z1) / (z2 - z1)
            return ((b1 + (b2 - b1) * t) - (f1 + (f2 - f1) * t)) / 2.0, w1 + (w2 - w1) * t
    return (RINGS[-1][2] - RINGS[-1][1]) / 2.0, RINGS[-1][3]

# hem edge roll
hem_path = []
for j in range(NSEG + 1):
    phi = 2.0 * math.pi * j / NSEG
    a, b = (RINGS[0][2] - RINGS[0][1]) / 2.0, RINGS[0][3]
    xc = (RINGS[0][1] + RINGS[0][2]) / 2.0 - 0.13 + lean(RINGS[0][0])
    y = b * math.sin(phi)
    hem_path.append((xc + a * math.cos(phi), y, SLAB_TOP + hem_lift(phi, y) + 0.004))
tube("HemRoll", hem_path, 0.010, 0.010, PLASTER, flat_axis='radial',
     xc_of_z=lambda z: xc_at(z), cap_ends=False)

# diagonal himation roll: front chest -> left side -> back, descending
roll_ctrl = []
for (zf, phideg) in [(1.46, 172), (1.38, 196), (1.28, 224), (1.17, 250),
                     (1.08, 272), (1.02, 294), (1.00, 310)]:
    a, b = ab_at(zf); xc = xc_at(zf)
    phi = math.radians(phideg)
    x, y = xc + a * math.cos(phi), b * math.sin(phi)
    # push out along the ellipse normal a touch
    n = Vector((math.cos(phi) / a, math.sin(phi) / b, 0.0)); n.normalize()
    p = Vector((x, y, SLAB_TOP + zf)) + n * 0.004
    roll_ctrl.append(tuple(p))
tube("HimationRoll", catmull(roll_ctrl, 7), 0.020, 0.040, PLASTER,
     flat_axis='radial', xc_of_z=xc_at)

# hanging swag on the left face (cloth over the wrapped left forearm):
# a shallow scoop band ON the surface, bottoming at mid-thigh (z_f ~0.92)
def surf_point(zf, phideg, push):
    a, b = ab_at(zf); xc = xc_at(zf)
    phi = math.radians(phideg)
    x, y = xc + a * math.cos(phi), b * math.sin(phi)
    n = Vector((math.cos(phi) / a, math.sin(phi) / b, 0.0)); n.normalize()
    p = Vector((x, y, SLAB_TOP + zf)) + n * push
    return tuple(p)

swag_phiz = [(200, 1.32), (215, 1.12), (232, 0.99), (248, 0.925),
             (264, 0.95), (278, 1.08), (288, 1.24)]
swag_ctrl = [surf_point(z, ph, 0.004) for (ph, z) in swag_phiz]
tube("SideSwag", catmull(swag_ctrl, 8), 0.016, 0.050, PLASTER, flat_axis='radial',
     xc_of_z=xc_at, taper=0.30)
fore_phiz = [(244, 1.10), (256, 1.015), (268, 1.045)]
fore_ctrl = [surf_point(z, ph, -0.006) for (ph, z) in fore_phiz]
tube("WrappedForearm", catmull(fore_ctrl, 6), 0.038, 0.038, PLASTER, flat_axis='y', taper=0.25)

# back flap: the himation's hanging end behind the legs, pointed tip
flap_rows = [  # (z_f, centre_x, half_width_y, y_centre)
    (1.00, 0.112, 0.072, -0.010),
    (0.85, 0.126, 0.098, -0.012),
    (0.65, 0.148, 0.096, -0.014),
    (0.46, 0.174, 0.092, -0.016),
    (0.33, 0.194, 0.068, -0.020),
    (0.28, 0.204, 0.020, -0.030),
]
vs, fs = [], []
COLS = 5
for (zf, cx, hw, yc) in flap_rows:
    for j in range(COLS):
        t = j / (COLS - 1)
        y = yc - hw + 2 * hw * t
        bow = 0.012 * math.sin(t * math.pi)          # edges curl back (+x)
        vs.append((cx + bow, y, SLAB_TOP + zf))
for i in range(len(flap_rows) - 1):
    for j in range(COLS - 1):
        fs.append((i * COLS + j, i * COLS + j + 1, (i + 1) * COLS + j + 1, (i + 1) * COLS + j))
flap = mesh_obj("HangingFlap", vs, fs, PLASTER)
solid = flap.modifiers.new("sol", 'SOLIDIFY'); solid.thickness = 0.030; solid.offset = 0.0
bpy.context.view_layer.objects.active = flap
bpy.ops.object.modifier_apply(modifier="sol")
from mathutils import Matrix as _Mtx
_fpiv = Vector((0.16, -0.01, 0.0))
_fm = (_Mtx.Translation(_fpiv) @ _Mtx.Rotation(math.radians(-24.0), 4, 'Z')
       @ _Mtx.Translation(-_fpiv))
flap.matrix_world = _fm @ flap.matrix_world

# chest knot: the bunched cloth clutched at the sternum (+ schematic hand)
def blob(name, loc, scale, mat, noise=0.0, seed=3):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=18, radius=1.0, location=loc)
    ob = bpy.context.active_object; ob.name = name; ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if noise:
        rnd = random.Random(seed)
        for v in ob.data.vertices:
            n = v.co.normalized()
            v.co += n * rnd.uniform(-noise, noise)
    return finish(ob, mat)

blob("ChestKnot", (-0.188, 0.012, SLAB_TOP + 1.415), (0.048, 0.075, 0.070), PLASTER, noise=0.006, seed=11)
blob("HandHint", (-0.172, 0.048, SLAB_TOP + 1.330), (0.024, 0.026, 0.021), PLASTER, noise=0.002, seed=12)

# ================================================================ HEAD
HX = -0.085  # head axis x (slightly forward of the collar centre)
neck = bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.060, radius2=0.050,
                                       depth=0.20, location=(HX + 0.004, 0, SLAB_TOP + 1.70))
neck_ob = bpy.context.active_object; neck_ob.name = "Neck"; finish(neck_ob, PLASTER)
blob("Cranium", (HX + 0.006, 0, SLAB_TOP + 1.884), (0.112, 0.090, 0.104), PLASTER)
blob("Face", (HX - 0.030, 0, SLAB_TOP + 1.806), (0.080, 0.070, 0.090), PLASTER)
blob("Beard", (HX - 0.038, 0, SLAB_TOP + 1.745), (0.058, 0.060, 0.052), PLASTER, noise=0.004, seed=21)
blob("BeardLow", (HX - 0.030, 0, SLAB_TOP + 1.713), (0.040, 0.048, 0.034), PLASTER, noise=0.004, seed=22)
# nose: small schematic wedge
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.020, radius2=0.010, depth=0.080,
                                location=(HX - 0.112, 0, SLAB_TOP + 1.804),
                                rotation=(0, math.radians(-78), math.radians(45)))
nose = bpy.context.active_object; nose.name = "Nose"; nose.scale = (1.0, 0.55, 1.0)
bpy.ops.object.transform_apply(scale=True); finish(nose, PLASTER)
# hair: back/side mass, bald crown in front-top; curls via vertex noise
blob("HairMass", (HX + 0.024, 0, SLAB_TOP + 1.868), (0.108, 0.095, 0.098), PLASTER, noise=0.005, seed=31)
blob("HairNape", (HX + 0.056, 0, SLAB_TOP + 1.800), (0.040, 0.068, 0.040), PLASTER, noise=0.005, seed=32)
for side, sy in (("L", -1), ("R", 1)):
    blob(f"HairLock{side}", (HX + 0.020, sy * 0.074, SLAB_TOP + 1.855),
         (0.036, 0.018, 0.046), PLASTER, noise=0.004, seed=33 + (side == "R"))
    blob(f"Ear{side}", (HX + 0.006, sy * 0.080, SLAB_TOP + 1.838),
         (0.011, 0.006, 0.016), PLASTER)

# tilt the head group slightly forward (pensive, as photographed)
from mathutils import Matrix
_pivot = Vector((HX, 0, SLAB_TOP + 1.735))
_M = (Matrix.Translation(_pivot) @ Matrix.Rotation(math.radians(-5.0), 4, 'Y')
      @ Matrix.Translation(-_pivot))
for _nm in ("Neck", "Cranium", "Face", "Beard", "BeardLow", "Nose", "HairMass",
            "HairNape", "HairLockL", "HairLockR", "EarL", "EarR"):
    _ob = bpy.data.objects.get(_nm)
    if _ob:
        _ob.matrix_world = _M @ _ob.matrix_world

# ================================================================ FEET
def build_foot(name, heel_x, y_c, mat):
    secs = [  # (dx from heel, half_w, centre_z, half_h)
        (0.000, 0.034, 0.042, 0.030), (0.050, 0.040, 0.046, 0.034),
        (0.110, 0.043, 0.044, 0.032), (0.170, 0.043, 0.039, 0.025),
        (0.220, 0.039, 0.033, 0.018), (0.255, 0.032, 0.028, 0.013),
        (0.276, 0.020, 0.023, 0.008),
    ]
    NS = 14
    vs, fs = [], []
    for (dx, hw, cz, hh) in secs:
        for j in range(NS):
            al = 2 * math.pi * j / NS
            y = y_c + hw * math.sin(al)
            z = SLAB_TOP + max(0.012, cz + hh * math.cos(al)) if math.cos(al) < 0 else SLAB_TOP + cz + hh * math.cos(al)
            vs.append((heel_x - dx, y, z))
    for i in range(len(secs) - 1):
        for j in range(NS):
            jn = (j + 1) % NS
            fs.append((i * NS + j, (i + 1) * NS + j, (i + 1) * NS + jn, i * NS + jn))
    ci = len(vs); vs.append((heel_x + 0.012, y_c, SLAB_TOP + 0.040))
    for j in range(NS):
        fs.append((ci, j, (j + 1) % NS))
    ci = len(vs); last = (len(secs) - 1) * NS
    vs.append((heel_x - 0.282, y_c, SLAB_TOP + 0.023))
    for j in range(NS):
        fs.append((ci, last + (j + 1) % NS, last + j))
    foot = mesh_obj(name, vs, fs, mat)
    # sandal sole: widened flat slab under the foot
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(heel_x - 0.128, y_c, SLAB_TOP + 0.007))
    sole = bpy.context.active_object; sole.name = name + "Sole"
    sole.scale = (0.300, 0.098, 0.014); bpy.ops.object.transform_apply(scale=True)
    finish(sole, mat, smooth=False)
    # toe strap: one thin band across the toes
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(heel_x - 0.196, y_c, SLAB_TOP + 0.052))
    st = bpy.context.active_object; st.name = name + "Strap"
    st.scale = (0.032, 0.092, 0.008); st.rotation_euler = (0, math.radians(18), 0)
    bpy.ops.object.transform_apply(scale=True); finish(st, mat, smooth=False)
    # big-toe hint
    blob(name + "Toe", (heel_x - 0.248, y_c - 0.016, SLAB_TOP + 0.020), (0.020, 0.013, 0.011), mat)

build_foot("FootL", -0.070, -0.068, PLASTER)   # advanced, on the photographed side
build_foot("FootR", -0.028, +0.074, PLASTER)   # slightly back

# ================================================================ SUPPORT BLOCK
# The small patterned object between the feet: a low block whose front face
# carries an arcaded band over vertical flutes. Read schematically from the
# stereograph; see NOTES.md.
def box(name, loc, size, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object; ob.name = name; ob.scale = tuple(size)
    bpy.ops.object.transform_apply(scale=True)
    return finish(ob, mat, smooth=False)

SB = (0.075, -0.002, SLAB_TOP)   # block centre x, y, base z
box("SupportBlock", (SB[0], SB[1], SLAB_TOP + 0.110), (0.115, 0.165, 0.220), PLASTER)
# arcaded band: five small half-round bumps along the top of the -x face
for i in range(5):
    yy = SB[1] - 0.058 + i * 0.029
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.0115, depth=0.016,
                                        location=(SB[0] - 0.0615, yy, SLAB_TOP + 0.183),
                                        rotation=(0, math.radians(90), 0))
    arc = bpy.context.active_object; arc.name = f"SupportArch{i}"
    finish(arc, PLASTER)
# band rail above the arches + flutes below
box("SupportBand", (SB[0] - 0.058, SB[1], SLAB_TOP + 0.205), (0.006, 0.150, 0.018), PLASTER)
for i in range(6):
    yy = SB[1] - 0.0625 + i * 0.025
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.0055, depth=0.128,
                                        location=(SB[0] - 0.0585, yy, SLAB_TOP + 0.082))
    fl = bpy.context.active_object; fl.name = f"SupportFlute{i}"
    finish(fl, PLASTER)

# ================================================================ PLINTH + SLAB
# Court plinth per models/display-plinth (0.90 m high; foot 0.90 x 0.65;
# base-moulding zone 0.185; straight shaft; stepped cap; top slab 0.84 x 0.59).
box("PlinthFloorSlab", (0, 0, 0.025), (0.90, 0.65, 0.05), EBON)
box("PlinthStep", (0, 0, 0.0725), (0.865, 0.615, 0.045), EBON)
# chamfer frustum between step and shaft
def frustum(name, z0, z1, s0, s1, mat):
    vs, fs = [], []
    for (zz, (sx, sy)) in ((z0, s0), (z1, s1)):
        vs += [(-sx / 2, -sy / 2, zz), (sx / 2, -sy / 2, zz),
               (sx / 2, sy / 2, zz), (-sx / 2, sy / 2, zz)]
    fs = [(0, 1, 2, 3), (7, 6, 5, 4),
          (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_obj(name, vs, fs, mat, smooth=False)
frustum("PlinthChamfer", 0.095, 0.185, (0.865, 0.615), (0.805, 0.555), EBON)
box("PlinthShaft", (0, 0, 0.505), (0.805, 0.555, 0.64), EBON)
box("PlinthCapStep", (0, 0, 0.840), (0.825, 0.575, 0.03), EBON)
box("PlinthTopSlab", (0, 0, 0.8775), (0.84, 0.59, 0.045), EBON)
# recessed unlettered label plate, high on the -Y (labelled) face
box("LabelPlate", (0, -0.2805, 0.66), (0.37, 0.006, 0.17), EBON_PLATE)
box("LabelPlateInner", (0, -0.2825, 0.66), (0.33, 0.004, 0.135), EBON)
# the statue's own white base slab (numbered 324 in the photograph)
box("StatueSlab", (0, 0, 0.955), (0.98, 0.62, 0.11), PLASTER_BRIGHT)
box("StatueSlabTop", (0, 0, 1.0325), (1.00, 0.64, 0.035), PLASTER_BRIGHT)

# ================================================================ FINISH
bpy.ops.object.select_all(action='SELECT')
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        ev = ob.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print(f"TOTAL TRIANGLES (evaluated): {tris}")
xs = [v.co.x for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
ys = [v.co.y for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
zs = [v.co.z for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
print(f"BBOX x [{min(xs):.3f},{max(xs):.3f}] y [{min(ys):.3f},{max(ys):.3f}] z [{min(zs):.3f},{max(zs):.3f}]")
print(f"OBJECTS: {len(bpy.context.scene.objects)}")

import os
OUT = os.path.expanduser("~/workspace/cp-models/aristides-statue")
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/aristides-statue.blend")
bpy.ops.export_scene.gltf(filepath=f"{OUT}/aristides-statue.glb",
                          export_format='GLB', export_apply=True)
print("SAVED blend + glb")
