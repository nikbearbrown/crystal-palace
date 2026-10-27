# Hawkins 1852-54 reconstructions as metaball stand-ins (feet; local +X = head, origin on the ground under the body).
# These are the WRONG 1854 Owen/Hawkins forms on purpose: quadrupedal rhino-like Iguanodon with a nose horn,
# hump-shouldered quadruped Megalosaurus, spiny Hylaeosaurus, basking ichthyosaurs with ringed eyes, swan-necked
# plesiosaurs, Megatherium hugging a tree, Irish elk. Proportions read from public photographs of the surviving
# sculptures and the 1853 ILN studio print (grade I); overall sizes D-checked where a source gives one (see checks/).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Quaternion
from mb import mb_mesh, append_mesh, FT

def Q(axis, deg): return Quaternion(axis, math.radians(deg))
def legs4(xf, xh, yo, top, rf, rh, foot=1.25, splay=0.25):
    e = []
    for s in (-1, 1):
        e += [("cap", (xf, s*yo, top), (xf+0.3, s*(yo+splay), 0.9), rf), ("ell", (xf+0.5, s*(yo+splay), 0.45), (foot*1.15, foot, 0.5)),
              ("cap", (xh, s*yo, top), (xh, s*(yo+splay), 0.9), rh), ("ell", (xh+0.4, s*(yo+splay), 0.45), (foot*1.25, foot*1.05, 0.5))]
    return e

def cones(bm, pts, mat_index=0):
    """pts: (base(x,y,z) ft, tip(x,y,z) ft, r ft) -> crisp cones (spines, horns, teeth)"""
    for b, t, r in pts:
        b, t = Vector(b), Vector(t); d = t - b
        res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=7, radius1=r*FT, radius2=0.02*FT, depth=d.length*FT)
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        bmesh.ops.transform(bm, matrix=Matrix.Translation(((b + t) / 2) * FT) @ q.to_matrix().to_4x4(), verts=res['verts'])

def build(name, groups, extra=None):
    bm = bmesh.new()
    for elems, res in groups:
        me = mb_mesh(name + "_g", elems, res); append_mesh(bm, me, Matrix()); bpy.data.meshes.remove(me)
    nsm = len(bm.faces)
    if extra: extra(bm)
    bm.faces.ensure_lookup_table()
    for i in range(nsm, len(bm.faces)): bm.faces[i].smooth = False
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me

# ---------------- Iguanodon (statue 10 m x 2.7 m high: cpdinosaurs.org) ----------------
def iguanodon(recumbent=False):
    dz = -2.2 if recumbent else 0.0
    B = [("ell", (0, 0, 5.6+dz), (8.2, 3.5, 2.9)), ("ell", (4.2, 0, 5.9+dz), (3.6, 3.2, 3.0)), ("ell", (-5.0, 0, 5.6+dz), (3.6, 3.2, 2.9)),
         ("cap", (6.5, 0, 6.0+dz), (9.4, 0, 6.0+dz), 1.95),                                          # thick short neck
         ("cap", (-7.5, 0, 4.9+dz), (-12.5, 0.6, 3.1+dz*0.6), 2.3), ("cap", (-12.5, 0.6, 3.1+dz*0.6), (-16.8, 1.8, 1.4), 1.35),
         ("cap", (-16.8, 1.8, 1.4), (-20.2, 3.6, 0.55), 0.6)]
    if recumbent:   # legs folded under, elbows and knees out to the sides
        for s in (-1, 1):
            B += [("ell", (5.0, s*3.2, 1.2), (2.6, 1.3, 1.2)), ("ell", (7.0, s*3.5, 0.5), (1.6, 1.2, 0.5)),
                  ("ell", (-4.6, s*3.4, 1.4), (3.0, 1.5, 1.4)), ("ell", (-2.0, s*3.8, 0.5), (1.8, 1.3, 0.5))]
    else:
        B += legs4(4.6, -5.2, 2.5, 5.0, 1.2, 1.45, 1.3, 0.35)
    hz = 6.2 + dz + (0.9 if recumbent else 0)
    H = [("ell", (11.2, 0, hz-0.5), (2.9, 1.45, 1.4)), ("ell", (11.6, 0, hz-1.4), (2.6, 1.25, 0.6)), ("ell", (13.8, 0, hz-0.8), (1.1, 1.05, 0.95)),
         ("cap", (9.6, 0, hz+0.1), (13.3, 0, hz+0.2), 0.8)]
    for s in (-1, 1): H += [("ball", (10.8, s*1.2, hz+0.3), 0.45), ("cap", (10.0, s*1.15, hz-1.0), (14.2, s*0.85, hz-1.25), 0.22)]   # eye boss, lip line
    def extra(bm):
        cones(bm, [((13.2, 0, hz+0.4), (13.6, 0, hz+1.9), 0.45)])                                   # Owen/Hawkins nose horn (actually the thumb spike)
        cones(bm, [((x, 0, 5.6+dz + 2.95*math.sqrt(max(0, 1-(x/8.6)**2))+0.05), (x-0.25, 0, 5.6+dz + 2.95*math.sqrt(max(0, 1-(x/8.6)**2))+0.55), 0.35)
                   for x in [i*1.2 - 7.2 for i in range(13)]])                                         # low dorsal frill (U)
    return build('hawkins_iguanodon_recumbent' if recumbent else 'hawkins_iguanodon_standing', [(B, 0.32), (H, 0.2)], extra)

# ---------------- Megalosaurus (statue 10 m x 3.5 m high: Historic England) ----------------
def megalosaurus():
    B = [("ell", (0, 0, 6.2), (7.2, 3.2, 3.4)), ("ell", (3.0, 0, 7.6), (3.6, 3.0, 3.6)), ("ell", (-5.0, 0, 6.0), (3.4, 3.0, 3.1)),
         ("cap", (5.5, 0, 8.4), (8.6, 0, 8.0), 1.75),
         ("cap", (-7.5, 0, 5.8), (-12.5, -0.4, 3.6), 2.0), ("cap", (-12.5, -0.4, 3.6), (-16.8, -1.2, 1.3), 1.1), ("cap", (-16.8, -1.2, 1.3), (-20.2, -2.6, 0.45), 0.45)]
    B += legs4(4.0, -5.4, 2.3, 6.0, 1.15, 1.4, 1.2, 0.3)
    H = [("ell", (10.9, 0, 8.2), (2.9, 1.15, 1.05)), ("ell", (11.2, 0, 7.5), (2.7, 1.0, 0.45)),           # upper head
         ("cap", (9.0, 0, 6.9), (13.4, 0, 6.1), 0.48),                                                     # dropped lower jaw (open mouth)
         ("ball", (10.6, -0.95, 8.75), 0.36), ("ball", (10.6, 0.95, 8.75), 0.36)]
    def extra(bm):
        t = []
        for s in (-1, 1):
            for i in range(9):
                x = 9.6 + i*0.42; t.append(((x, s*0.72, 7.25 - (x-9.6)*0.05), (x+0.05, s*0.72, 6.65 - (x-9.6)*0.05), 0.12))      # upper teeth
                x2 = 9.8 + i*0.4; zz = 6.9 - (x2-9.0)*0.18; t.append(((x2, s*0.45, zz+0.35), (x2, s*0.45, zz+0.85), 0.1))   # lower teeth
        cones(bm, t)
    return build('hawkins_megalosaurus', [(B, 0.32), (H, 0.18)], extra)

# ---------------- Hylaeosaurus (animal ~5 m: cpdinosaurs.org; statue size I) ----------------
def hylaeosaurus():
    B = [("ell", (0, 0, 2.9), (5.6, 2.5, 2.0)), ("cap", (4.5, 0, 3.1), (7.2, 0, 2.9), 1.1),
         ("cap", (-4.5, 0, 2.8), (-9.0, 0.5, 1.6), 1.4), ("cap", (-9.0, 0.5, 1.6), (-13.5, 1.8, 0.45), 0.55)]
    for s in (-1, 1):   # sprawling lizard limbs
        B += [("cap", (3.0, s*1.8, 2.4), (3.4, s*3.6, 1.6), 0.6), ("cap", (3.4, s*3.6, 1.6), (3.9, s*3.9, 0.3), 0.5), ("ell", (4.3, s*4.0, 0.25), (0.9, 0.7, 0.3)),
              ("cap", (-3.2, s*1.8, 2.4), (-3.8, s*3.8, 1.7), 0.75), ("cap", (-3.8, s*3.8, 1.7), (-3.6, s*4.2, 0.3), 0.55), ("ell", (-3.2, s*4.3, 0.25), (1.0, 0.75, 0.3))]
    H = [("ell", (8.4, 0, 2.7), (1.6, 0.85, 0.75)), ("ell", (9.6, 0, 2.5), (0.7, 0.6, 0.5)), ("ball", (8.6, -0.7, 3.05), 0.22), ("ball", (8.6, 0.7, 3.05), 0.22)]
    def extra(bm):
        sp = []
        for i in range(16):   # Mantell's 'dermal spines' set as a single dorsal row (Hawkins' reading, wrong)
            x = 6.0 - i*1.05
            top = 2.9 + 2.0*math.sqrt(max(0, 1-(x/5.8)**2)) if x > -5.6 else 2.8 - (abs(x)-4.5)*0.27
            ht = 2.6*math.exp(-((x+0.5)/5.5)**2) + 0.5
            sp.append(((x, 0, top-0.15), (x-0.35, 0, top+ht), 0.42))
        for s in (-1, 1):
            for i in range(8):
                x = 4.0 - i*1.1; yy = 2.5*math.sqrt(max(0.05, 0.75-(x/5.6)**2)); sp.append(((x, s*(yy-0.15), 3.9), (x-0.2, s*(yy+0.75), 4.45), 0.26))   # flank scutes
        cones(bm, sp)
    return build('hawkins_hylaeosaurus', [(B, 0.26), (H, 0.16)], extra)

# ---------------- Ichthyosaurus (Hawkins: big sclerotic-ringed eye, paddles, basking; size I) ----------------
def ichthyosaur(lift=8.0):
    q = Q((0, 1, 0), -lift)
    B = [("ell", (0, 0, 1.7), (6.5, 1.9, 1.8)), ("cap", (5.0, 0, 2.0), (6.8, 0, 2.2), 1.45), ("ell", (7.4, 0, 2.3), (1.8, 1.35, 1.3)),
         ("cap", (-5.0, 0, 1.5), (-9.5, 0, 0.8), 1.0), ("cap", (-9.5, 0, 0.8), (-13.5, 0, 0.4), 0.45)]
    for s in (-1, 1):
        B += [("ell", (3.2, s*2.6, 0.6), (1.6, 1.1, 0.25), Q((1, 0, 0), s*-15) @ Q((0, 0, 1), s*-25)),
              ("ell", (-3.5, s*2.1, 0.5), (1.1, 0.8, 0.22), Q((0, 0, 1), s*-20))]
    S = [("cap", (8.6, 0, 2.25), (10.6, 0, 2.05), 0.55), ("cap", (10.6, 0, 2.05), (12.4, 0, 1.85), 0.4), ("cap", (12.4, 0, 1.85), (13.8, 0, 1.7), 0.24),
         ("cap", (8.4, 0, 1.7), (10.6, 0, 1.55), 0.42), ("cap", (10.6, 0, 1.55), (13.3, 0, 1.45), 0.22)]
    def extra(bm):
        for s in (-1, 1):   # raised sclerotic-ring disc round the huge eye (Hawkins' signature feature)
            r = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14, radius1=0.95*FT, radius2=0.8*FT, depth=0.3*FT)
            m = Matrix.Translation(Vector((7.5, s*1.15, 2.55))*FT) @ Matrix.Rotation(-s*math.pi/2, 4, 'X')
            bmesh.ops.transform(bm, matrix=m, verts=r['verts'])
    me = build('hawkins_ichthyosaur', [(B, 0.24), (S, 0.14)], extra)
    me.transform(q.to_matrix().to_4x4()); return me

# ---------------- Plesiosaurus (swan neck raised, four paddles; size I) ----------------
def plesiosaur(curl=1.0):
    B = [("ell", (0, 0, 1.8), (3.8, 2.3, 1.45)), ("cap", (-3.0, 0, 1.6), (-7.5, 0.4, 0.8), 0.7), ("cap", (-7.5, 0.4, 0.8), (-9.5, 1.2, 0.5), 0.3)]
    for s in (-1, 1):
        B += [("ell", (2.2, s*3.0, 1.0), (1.8, 1.1, 0.22), Q((0, 0, 1), s*-30)), ("ell", (-2.0, s*2.9, 0.9), (1.5, 0.9, 0.2), Q((0, 0, 1), s*25))]
    pts = [(Vector((3.0 + 4.2*math.sin(t*1.35), 1.1*curl*math.sin(t*2.2), 2.2 + 6.4*t**1.15))) for t in [i/10 for i in range(11)]]
    N = [("cap", tuple(pts[i]), tuple(pts[i+1]), 1.05 - i*0.065) for i in range(10)]
    p = pts[-1]; N += [("ell", (p.x+0.8, p.y, p.z+0.1), (1.0, 0.45, 0.42))]
    return build('hawkins_plesiosaur', [(B, 0.22), (N, 0.14)])

# ---------------- Megatherium (upright against a tree; up to 6 m: ArtUK/cpdinosaurs; statue size I) ----------------
def megatherium():
    B = [("ell", (0, 0, 4.2), (3.3, 3.2, 3.2)), ("ell", (1.4, 0, 8.2), (2.6, 2.6, 3.6), Q((0, 1, 0), 20)), ("ell", (2.8, 0, 11.4), (1.8, 1.9, 1.7)),
         ("cap", (-2.4, 0, 3.6), (-5.4, 0, 0.6), 1.7)]
    for s in (-1, 1):
        B += [("cap", (0.2, s*2.3, 4.0), (0.6, s*2.6, 0.8), 1.45), ("ell", (1.4, s*2.6, 0.45), (2.0, 1.1, 0.5)),
              ("cap", (2.4, s*2.1, 10.6), (4.4, s*1.9, 12.6), 0.85), ("cap", (4.4, s*1.9, 12.6), (5.4, s*0.9, 13.7), 0.6)]
    H = [("ell", (3.6, 0, 13.2), (1.3, 1.0, 1.05)), ("ell", (4.7, 0, 12.9), (0.75, 0.65, 0.6)), ("cap", (5.2, 0, 12.85), (5.95, 0, 12.35), 0.32), ("ball", (4.0, -0.75, 13.6), 0.18), ("ball", (4.0, 0.75, 13.6), 0.18)]
    def extra(bm):
        cones(bm, [((5.4, s*0.9 + d, 13.7), (6.1, s*0.5 + d, 14.0), 0.18) for s in (-1, 1) for d in (-0.25, 0, 0.25)])   # claws
    return build('hawkins_megatherium', [(B, 0.24), (H, 0.15)], extra)

# ---------------- Irish elk (Megaloceros; antler span to 3.6 m: animal; statue size I) ----------------
def elk(stag=True, k=1.0, lying=False):
    B = [("ell", (0, 0, 5.1), (3.4, 1.2, 1.25)), ("ell", (2.2, 0, 5.4), (1.5, 1.2, 1.45)), ("cap", (2.8, 0, 6.0), (4.0, 0, 7.4), 0.72),
         ("ell", (4.6, 0, 7.45), (1.15, 0.45, 0.48), Q((0, 1, 0), 22)), ("ball", (-3.3, 0, 5.4), 0.35)]
    for s in (-1, 1):
        B += [("cap", (2.5, s*0.75, 4.4), (2.6, s*0.75, 0.25), 0.27), ("cap", (-2.4, s*0.75, 4.6), (-2.6, s*0.75, 0.25), 0.3)]
    if lying:   # reclining doe (R: surviving reclining doe): drop the body 3.4 ft, fold the legs under it
        def dz(e):
            e = list(e); e[1] = (e[1][0], e[1][1], e[1][2] - 3.4)
            if e[0] == 'cap': e[2] = (e[2][0], e[2][1], e[2][2] - 3.4)
            return tuple(e)
        B = [dz(e) for e in B[:5]]
        for s in (-1, 1):
            B += [("cap", (2.2, s*0.95, 1.2), (3.9, s*0.9, 0.35), 0.26), ("cap", (-2.2, s*1.0, 1.4), (-0.6, s*1.15, 0.4), 0.32)]
    groups = [(B, 0.14)]
    extra = None
    if stag:
        def extra(bm):
            cn = []
            for s in (-1, 1):
                base = Vector((4.3, s*0.3, 7.95)); b1 = Vector((4.1, s*1.9, 8.35)); b2 = Vector((3.8, s*2.9, 8.8))
                cn += [(base, b1, 0.2), (b1, b2, 0.17), (Vector((4.3, s*0.7, 8.05)), Vector((5.5, s*1.0, 8.7)), 0.1)]   # beams + brow tine
                pts = []   # palm: curved plate, outline points at two thicknesses -> hull
                for t in range(9):
                    u = t/8; ang = math.radians(-50 + 140*u); rr = 2.6 + 0.5*math.sin(u*math.pi)
                    c = Vector((3.6 + rr*0.55*math.cos(ang), s*(3.0 + rr*0.85*math.sin(ang*0.5 + 0.6)), 8.9 + rr*0.5*math.sin(ang)))
                    pts += [c, c + Vector((0, 0, 0.22))]
                    if t % 2 == 0: cn.append((c, c + Vector((0.4*math.cos(ang), s*0.9, 0.7 + 0.5*math.sin(ang))), 0.12))   # tines on the rim
                pts += [b2, b2 + Vector((0, 0, 0.2))]
                h = bmesh.ops.convex_hull(bm, input=[bm.verts.new(p*FT) for p in pts])
            cones(bm, [(tuple(a), tuple(b), r) for a, b, r in cn])
    me = build('hawkins_irish_elk_' + ('stag' if stag else 'hind'), groups, extra)
    me.transform(Matrix.Scale(k, 4)); return me
