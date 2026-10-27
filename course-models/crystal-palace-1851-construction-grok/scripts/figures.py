"""Copied from the transept branch (scripts/figures.py, Grok Bot); construction adds base=False for live horses.
Sculpture and crowd stand-ins for the HP51 dressing (r09). Generic forms, not likenesses of any catalogued work.
Statues: metaball figures evaluated to meshes, so limbs blend into one carved mass with a classical support strut,
drapery and an integral base. Crowd: low-poly lathe people in 1851 dress (frock coat + top hat; full skirt + bonnet)."""
import bpy, bmesh, math
from mathutils import Vector, Matrix, Quaternion
K = 0.575            # visible radius / metaball radius at threshold 0.6, stiffness 2 (measured)

def _mb_mesh(name, elems, scale, res=0.011):
    mb = bpy.data.metaballs.new("MB_" + name); mb.render_resolution = res; mb.resolution = res; mb.threshold = 0.6
    ob = bpy.data.objects.new("MBX" + name.replace("_", "").replace(".", ""), mb)
    bpy.context.scene.collection.objects.link(ob)
    for e in elems:
        kind = e[0]
        if kind == "ball":
            el = mb.elements.new(type='BALL'); el.co = e[1]; el.radius = e[2] / K
        elif kind == "cap":
            a, b, r = Vector(e[1]), Vector(e[2]), e[3]; d = b - a
            el = mb.elements.new(type='CAPSULE'); el.co = (a + b) / 2; el.radius = r / K
            el.size_x = d.length / 2; el.rotation = Vector((1, 0, 0)).rotation_difference(d.normalized())
        elif kind == "ell":
            el = mb.elements.new(type='ELLIPSOID'); el.co = e[1]; el.radius = 1.0 / K
            el.size_x, el.size_y, el.size_z = e[2]
            if len(e) > 3: el.rotation = e[3]
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); me.name = name
    bpy.data.objects.remove(ob); bpy.data.metaballs.remove(mb)
    me.transform(Matrix.Scale(scale, 4))
    for p in me.polygons: p.use_smooth = True
    return me

def _box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
    for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        bm.faces.new([vs[i] for i in f])

def _join(me, extra_boxes, scale):
    """append integral base slabs (unit coords) to a metaball mesh"""
    bm = bmesh.new(); bm.from_mesh(me)
    for b in extra_boxes: _box(bm, *[v * scale for v in b])
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = p.use_smooth
    return me

# ---- standing figures, unit height (crown ~1.0), facing -y ----
def _legs(weight_x=-0.05, free_x=0.06, free_fwd=-0.035):
    return [("cap", (weight_x, 0, 0.49), (weight_x + 0.005, 0, 0.28), 0.052), ("cap", (weight_x + 0.005, 0, 0.28), (weight_x + 0.005, 0.01, 0.05), 0.036),
            ("cap", (weight_x + 0.005, 0, 0.03), (weight_x + 0.005, -0.06, 0.022), 0.024),
            ("cap", (free_x, 0, 0.49), (free_x + 0.025, free_fwd, 0.28), 0.05), ("cap", (free_x + 0.025, free_fwd, 0.28), (free_x + 0.04, 0.04, 0.06), 0.034),
            ("cap", (free_x + 0.04, 0.04, 0.04), (free_x + 0.05, -0.02, 0.022), 0.023)]
def _torso(female=False):
    w = 0.9 if female else 1.0
    t = [("ell", (0, 0, 0.925), (0.055, 0.062, 0.07)), ("cap", (0, 0.005, 0.83), (0, 0.005, 0.885), 0.03),
         ("ell", (0, 0.005, 0.735), (0.115 * w, 0.065, 0.09)), ("cap", (-0.11 * w, 0.005, 0.79), (0.11 * w, 0.005, 0.79), 0.04),
         ("ell", (0, 0.005, 0.6), (0.085 * w, 0.055, 0.08)), ("ell", (0.0, 0.005, 0.51), (0.105 * (1.08 if female else 1), 0.065, 0.065))]
    if female: t += [("ball", (0, 0.055, 0.95), 0.032), ("ball", (-0.04, -0.045, 0.75), 0.035), ("ball", (0.04, -0.045, 0.75), 0.035)]
    else: t += [("ell", (0, 0.01, 0.955), (0.058, 0.062, 0.04))]    # hair cap
    return t
def _strut(x=-0.13):   # the tree-stump support with a fall of drapery: the classical-marble giveaway
    return [("cap", (x, 0.04, 0.0), (x, 0.04, 0.34), 0.042), ("ell", (x + 0.01, 0.03, 0.31), (0.05, 0.045, 0.07)),
            ("ell", (x + 0.015, 0.02, 0.2), (0.035, 0.04, 0.1))]

FIGS = {
 # Apollo-type: weight on right leg, left arm raised, cloak on the left shoulder, strut by the weight leg
 "hero": lambda: _torso() + _legs() + _strut() + [
     ("cap", (-0.12, 0.005, 0.78), (-0.15, 0.01, 0.6), 0.032), ("cap", (-0.15, 0.01, 0.6), (-0.15, -0.025, 0.45), 0.026), ("ball", (-0.15, -0.03, 0.43), 0.024),
     ("cap", (0.12, 0.005, 0.78), (0.2, 0.0, 0.9), 0.031), ("cap", (0.2, 0.0, 0.9), (0.215, -0.01, 1.03), 0.025), ("ball", (0.215, -0.01, 1.055), 0.023),
     ("ell", (0.15, 0.035, 0.68), (0.045, 0.03, 0.15)), ("ell", (0.1, 0.045, 0.8), (0.06, 0.03, 0.04))],
 # orator / portrait statue: long cloak to the ground, right arm forward
 "orator": lambda: _torso() + _legs(-0.045, 0.05, -0.02) + [
     ("ell", (0, 0.02, 0.45), (0.15, 0.1, 0.4)), ("ell", (0.0, 0.03, 0.12), (0.17, 0.12, 0.12)),
     ("cap", (-0.12, 0.005, 0.78), (-0.14, -0.05, 0.62), 0.032), ("cap", (-0.14, -0.05, 0.62), (-0.12, -0.17, 0.66), 0.026), ("ball", (-0.115, -0.19, 0.665), 0.024),
     ("cap", (0.12, 0.005, 0.78), (0.15, 0.0, 0.6), 0.032), ("cap", (0.15, 0.0, 0.6), (0.14, -0.04, 0.47), 0.026), ("ell", (0.15, -0.02, 0.5), (0.05, 0.04, 0.12))],
 # draped female (peplos): stacked skirt with vertical folds, one hand at the breast, urn in the other
 "draped": lambda: _torso(True) + [
     ("ell", (0, 0.0, 0.42), (0.12, 0.085, 0.13)), ("ell", (0, 0.0, 0.25), (0.13, 0.095, 0.12)), ("ell", (0, 0.0, 0.08), (0.145, 0.11, 0.09))] + [
     ("cap", (0.12 * math.cos(a), 0.09 * math.sin(a), 0.02), (0.1 * math.cos(a), 0.075 * math.sin(a), 0.5), 0.022) for a in [k * math.pi / 5 for k in range(10)]] + [
     ("cap", (-0.105, 0.0, 0.79), (-0.13, -0.03, 0.63), 0.03), ("cap", (-0.13, -0.03, 0.63), (-0.03, -0.075, 0.71), 0.024),
     ("cap", (0.105, 0.0, 0.79), (0.14, 0.0, 0.62), 0.03), ("cap", (0.14, 0.0, 0.62), (0.16, -0.04, 0.49), 0.024), ("ell", (0.17, -0.05, 0.45), (0.045, 0.045, 0.055)),
     ("cap", (-0.09, -0.05, 0.82), (0.11, -0.06, 0.55), 0.03)],
 # Greek-Slave type: weight on one leg, wrists joined in front, drapery over a post at her side
 "nude_post": lambda: _torso(True) + _legs(-0.04, 0.05, -0.04) + [
     ("cap", (-0.1, 0.005, 0.79), (-0.12, -0.02, 0.62), 0.028), ("cap", (-0.12, -0.02, 0.62), (-0.02, -0.08, 0.52), 0.022),
     ("cap", (0.1, 0.005, 0.79), (0.12, -0.02, 0.62), 0.028), ("cap", (0.12, -0.02, 0.62), (0.02, -0.08, 0.52), 0.022), ("ball", (0, -0.085, 0.51), 0.026),
     ("cap", (0.2, 0.02, 0.0), (0.2, 0.02, 0.52), 0.045), ("ell", (0.2, 0.0, 0.42), (0.06, 0.06, 0.13)), ("ell", (0.19, -0.01, 0.25), (0.05, 0.05, 0.12))],
 # seated figure on a rock (Prometheus / philosopher type)
 "seated": lambda: [("ell", (0, 0.03, 0.18), (0.2, 0.17, 0.18)), ("ell", (0.05, 0.08, 0.32), (0.13, 0.11, 0.09)),
     ("ell", (0, 0.03, 0.66), (0.055, 0.062, 0.07)), ("cap", (0, 0.03, 0.57), (0, 0.035, 0.62), 0.03), ("ell", (0, 0.04, 0.48), (0.11, 0.065, 0.09)),
     ("cap", (-0.105, 0.04, 0.53), (0.105, 0.04, 0.53), 0.04), ("ell", (0, 0.04, 0.37), (0.09, 0.06, 0.07)),
     ("cap", (-0.06, 0.02, 0.33), (-0.07, -0.17, 0.34), 0.05), ("cap", (-0.07, -0.17, 0.34), (-0.075, -0.2, 0.06), 0.035),
     ("cap", (0.06, 0.02, 0.33), (0.08, -0.15, 0.3), 0.05), ("cap", (0.08, -0.15, 0.3), (0.1, -0.12, 0.05), 0.035),
     ("cap", (-0.12, 0.04, 0.52), (-0.13, -0.02, 0.38), 0.03), ("cap", (-0.13, -0.02, 0.38), (-0.06, -0.15, 0.36), 0.025),
     ("cap", (0.12, 0.04, 0.52), (0.2, 0.06, 0.66), 0.03), ("cap", (0.2, 0.06, 0.66), (0.17, 0.02, 0.8), 0.025)],
 # bust on a herm (for the small Muse display plinths)
 "bust": lambda: [("ell", (0, 0, 0.84), (0.11, 0.125, 0.14)), ("cap", (0, 0.01, 0.66), (0, 0.01, 0.74), 0.06),
     ("ell", (0, 0.01, 0.56), (0.24, 0.12, 0.12)), ("ell", (0, 0.02, 0.88), (0.115, 0.125, 0.09)), ("cap", (0, 0.01, 0.12), (0, 0.01, 0.42), 0.075),
     ("ell", (0, 0.01, 0.45), (0.12, 0.08, 0.05))],
}

def statue_mesh(kind, height_m, mat, base=True):
    me = _mb_mesh(f"SCULPT_{kind}", FIGS[kind](), height_m)
    if base and kind not in ("bust",):
        w = 0.22 if kind not in ("seated",) else 0.26
        _join(me, [(-w, w, -0.17, 0.15, -0.0, 0.035)], height_m)
    me.materials.append(mat); return me

def horse_group_mesh(name, length_m, mat, rearing=False, rider=True, base=True):
    """equestrian stand-in, unit = horse body+head length ~1.0, horse faces +x; integral rock base"""
    fl = [("cap", (0.3, 0.07, 0.55), (0.32, 0.07, 0.28), 0.045), ("cap", (0.32, 0.07, 0.28), (0.33, 0.07, 0.04), 0.028)]
    if rearing:
        fl += [("cap", (0.3, -0.07, 0.6), (0.44, -0.07, 0.62), 0.045), ("cap", (0.44, -0.07, 0.62), (0.47, -0.07, 0.48), 0.028)]
        fl[:2] = [("cap", (0.3, 0.07, 0.6), (0.42, 0.07, 0.7), 0.045), ("cap", (0.42, 0.07, 0.7), (0.46, 0.07, 0.56), 0.028)]
        body = [("ell", (0.0, 0, 0.66), (0.34, 0.14, 0.15), Quaternion((0, 1, 0), -0.35)), ("ell", (0.28, 0, 0.78), (0.13, 0.13, 0.14)),
                ("ell", (-0.26, 0, 0.55), (0.14, 0.14, 0.14)), ("cap", (0.33, 0, 0.88), (0.43, 0, 1.08), 0.075), ("cap", (0.44, 0, 1.1), (0.56, 0, 1.0), 0.05)]
        hind = [("cap", (-0.28, s, 0.5), (-0.2, s, 0.25), 0.055) for s in (0.07, -0.07)] + [("cap", (-0.2, s, 0.25), (-0.27, s, 0.03), 0.03) for s in (0.07, -0.07)]
    else:
        fl += [("cap", (0.3, -0.07, 0.55), (0.42, -0.07, 0.42), 0.045), ("cap", (0.42, -0.07, 0.42), (0.4, -0.07, 0.3), 0.028)]
        body = [("ell", (0, 0, 0.62), (0.36, 0.14, 0.15)), ("ell", (0.3, 0, 0.63), (0.12, 0.13, 0.14)), ("ell", (-0.28, 0, 0.64), (0.13, 0.14, 0.14)),
                ("cap", (0.36, 0, 0.7), (0.5, 0, 0.92), 0.075), ("cap", (0.5, 0, 0.95), (0.62, 0, 0.82), 0.05)]
        hind = [("cap", (-0.3, s, 0.58), (-0.33, s, 0.33), 0.055) for s in (0.07, -0.07)] + [("cap", (-0.33, s, 0.33), (-0.31, s, 0.03), 0.03) for s in (0.07, -0.07)]
    tail = [("cap", (-0.42, 0, 0.68), (-0.5, 0, 0.36), 0.032)]
    rid = []
    if rider:
        z0 = 0.86 if not rearing else 0.92
        rid = [("ell", (0.0, -0.02, z0 + 0.1), (0.075, 0.055, 0.12)), ("ell", (-0.01, -0.02, z0 + 0.27), (0.045, 0.05, 0.055)),
               ("ell", (0.0, -0.1, z0 - 0.05), (0.13, 0.1, 0.16)),                # skirt / cloak falling on the near side
               ("cap", (0.0, -0.06, z0 + 0.18), (0.12, -0.08, z0 + 0.12), 0.025), ("cap", (0.0, 0.03, z0 + 0.18), (0.1, 0.06, z0 + 0.1), 0.025)]
    me = _mb_mesh(name, body + fl + hind + tail + rid, length_m)
    if base: _join(me, [(-0.5, 0.55, -0.2, 0.2, -0.0, 0.05)], length_m)
    me.materials.append(mat); return me

# ---- crowd (feet) ----
def _lathe(bm, prof, seg, cx=0.0, cy=0.0, ox=0.0):
    rings = [[bm.verts.new((cx + r * math.cos(2 * math.pi * k / seg) + ox, cy + r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)] for r, z in prof]
    for A, B in zip(rings, rings[1:]):
        for k in range(seg): bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])
    if prof[-1][0] > 0: bm.faces.new(rings[-1])
    return len(prof)

def person_mesh(name, kind, mats, FT=0.3048):
    """kind 'man' | 'woman' | 'girl'; mats = [main, second, skin, hat]. One mesh with 4 slots, metres."""
    bm = bmesh.new(); f = FT
    slots = []   # (faces_before, mat_index)
    def mark(i):
        for fa in bm.faces:
            if fa.material_index == 0 and not fa.tag: fa.material_index = i; fa.tag = True
    if kind == "man":
        for s in (-0.28, 0.28):                       # trousers
            _lathe(bm, [(0.2 * f, 0.0), (0.21 * f, 1.0 * f), (0.25 * f, 2.6 * f), (0.0, 2.6 * f)], 8, ox=s * f); 
        mark(1)
        _lathe(bm, [(0.0, 1.95 * f), (0.66 * f, 1.95 * f), (0.6 * f, 2.9 * f), (0.55 * f, 3.6 * f), (0.64 * f, 4.35 * f), (0.4 * f, 4.7 * f), (0.0, 4.75 * f)], 10); mark(0)
        for s in (-0.66, 0.66):
            _lathe(bm, [(0.16 * f, 3.0 * f), (0.18 * f, 4.4 * f), (0.0, 4.5 * f)], 6, ox=s * f)
        mark(0)
        _lathe(bm, [(0.0, 4.75 * f), (0.3 * f, 4.85 * f), (0.36 * f, 5.15 * f), (0.3 * f, 5.42 * f), (0.0, 5.5 * f)], 10); mark(2)
        _lathe(bm, [(0.0, 5.32 * f), (0.48 * f, 5.32 * f), (0.48 * f, 5.38 * f), (0.3 * f, 5.38 * f), (0.32 * f, 6.0 * f), (0.0, 6.0 * f)], 10); mark(3)
    else:
        sc = 1.0 if kind == "woman" else 0.68
        _lathe(bm, [(0.0, 0.02 * f), (1.25 * sc * f, 0.02 * f), (1.2 * sc * f, 0.5 * sc * f), (0.95 * sc * f, 1.6 * sc * f), (0.6 * sc * f, 2.8 * sc * f), (0.4 * sc * f, 3.25 * sc * f), (0.0, 3.25 * sc * f)], 14); mark(0)
        _lathe(bm, [(0.4 * sc * f, 3.2 * sc * f), (0.48 * sc * f, 3.9 * sc * f), (0.55 * sc * f, 4.25 * sc * f), (0.3 * sc * f, 4.45 * sc * f), (0.0, 4.5 * sc * f)], 10); mark(1)
        _lathe(bm, [(0.0, 4.45 * sc * f), (0.27 * sc * f, 4.55 * sc * f), (0.33 * sc * f, 4.82 * sc * f), (0.27 * sc * f, 5.08 * sc * f), (0.0, 5.12 * sc * f)], 10); mark(2)
        if kind == "woman":   # bonnet: a hood open to the front (-y)
            _lathe(bm, [(0.0, 4.72 * f), (0.38 * f, 4.78 * f), (0.42 * f, 5.05 * f), (0.3 * f, 5.25 * f), (0.0, 5.3 * f)], 10, cy=0.06 * f); mark(3)
        for s in (-0.55, 0.55):
            _lathe(bm, [(0.14 * sc * f, 2.9 * sc * f), (0.15 * sc * f, 4.2 * sc * f), (0.0, 4.3 * sc * f)], 6, ox=s * sc * f)
        mark(1)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    return me
