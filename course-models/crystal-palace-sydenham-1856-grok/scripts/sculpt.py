# r12 sculpted stand-ins (feet). The metaball-to-mesh helper is adapted from the HP executor's figures.py `_mb_mesh`
# (course-models/crystal-palace-1851-transept-grok/scripts/figures.py, read-only; K = 0.575 measured there), rewritten
# here to work in feet with an element list; credit to that build. Forms are procedural stand-ins (grade I).
import bpy, bmesh, math
from mathutils import Vector, Matrix, Quaternion

K = 0.575   # visible radius / metaball radius at threshold 0.6 (HP executor, measured)
FT = 0.3048

def mb_mesh(name, elems, res=0.16, scale=FT):
    """elements in feet: ("ball", co, r) | ("cap", a, b, r) | ("ell", co, (sx, sy, sz)[, quat]). Returns a mesh in metres."""
    mb = bpy.data.metaballs.new("MB_" + name); mb.render_resolution = res; mb.resolution = res; mb.threshold = 0.6
    ob = bpy.data.objects.new("MBX_" + name, mb); bpy.context.scene.collection.objects.link(ob)
    for e in elems:
        k = e[0]
        if k == "ball":
            el = mb.elements.new(type='BALL'); el.co = e[1]; el.radius = e[2] / K
        elif k == "cap":
            a, b, r = Vector(e[1]), Vector(e[2]), e[3]; d = b - a
            el = mb.elements.new(type='CAPSULE'); el.co = (a + b) / 2; el.radius = r / K
            el.size_x = max(d.length / 2, 1e-4); el.rotation = Vector((1, 0, 0)).rotation_difference(d.normalized())
        elif k == "ell":
            el = mb.elements.new(type='ELLIPSOID'); el.co = e[1]; el.radius = 1.0 / K
            el.size_x, el.size_y, el.size_z = e[2]
            if len(e) > 3: el.rotation = e[3]
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); me.name = name
    bpy.data.objects.remove(ob); bpy.data.metaballs.remove(mb)
    me.transform(Matrix.Scale(scale, 4))
    for p in me.polygons: p.use_smooth = True
    return me

def append_mesh(bm, me, matrix):
    """append a (template) mesh into an existing bmesh under a world matrix (metres)."""
    tmp = bpy.data.meshes.new("tmp_append"); b2 = bmesh.new(); b2.from_mesh(me)
    bmesh.ops.transform(b2, matrix=matrix, verts=b2.verts); b2.to_mesh(tmp); b2.free()
    bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)

# ---------------- Tanis-type sphinx (Crystal Palace terrace, 1854) ----------------
# Origin = centre of the plinth top; long axis Y, head toward -Y (garden). ArtUK SE19_JK_S106: H 180 x D 480 cm
# (5.9 x 15.75 ft) -> paw tip y = -8.0, rump y = +7.6, crown 5.95 ft. Proportions from Commons photos (Udimu 2006
# side view; Doyle of London 2023 detail): long flat forepaws, lion body, haunch with folded hind leg, striped nemes
# with lappets on the breast, uraeus, square false beard, tail curled up along the right flank. Grade I (form).
def sphinx_parts():
    """three metaball groups that must not melt into each other (body / head+nemes / tail)."""
    B = [("ell", (0, 4.9, 1.6), (1.95, 2.6, 1.6)),                            # haunch / rump
         ("cap", (0, 4.0, 1.95), (0, -0.4, 2.1), 1.65),                       # barrel, level back
         ("ell", (0, -1.2, 2.3), (2.0, 1.8, 2.1)),                            # shoulders / chest
         ("ell", (0, -2.3, 2.35), (1.6, 1.1, 1.5))]                           # breast
    for s in (-1, 1):
        B += [("ell", (s*1.55, 4.5, 1.0), (0.72, 2.3, 1.0)),                  # folded hind leg (thigh)
              ("ell", (s*1.35, 1.9, 0.38), (0.55, 1.2, 0.38)),                # hind paw tucked forward
              ("cap", (s*1.3, -1.3, 1.6), (s*1.3, -3.4, 0.6), 0.85),          # foreleg (elbow -> wrist)
              ("cap", (s*1.3, -3.2, 0.5), (s*1.3, -7.35, 0.5), 0.58),         # forepaw, thick and flat-topped
              ("ell", (s*1.3, -7.35, 0.45), (0.62, 0.62, 0.45))]              # paw end (toes)
    H = [("ell", (0, -3.3, 4.45), (0.72, 0.58, 0.95)),                         # face
         ("ell", (0, -3.88, 4.38), (0.16, 0.2, 0.24)),                        # nose
         ("ell", (0, -3.72, 4.0), (0.32, 0.1, 0.08)),                         # mouth / lips
         ("cap", (0, -3.72, 3.55), (0, -3.84, 2.85), 0.25),                   # false beard
         ("ball", (0, -3.55, 5.55), 0.17)]                                    # uraeus on the nemes brow
    for s in (-1, 1):
        H += [("ell", (s*0.74, -3.1, 4.5), (0.12, 0.22, 0.3))]               # ears
    T = [("cap", (1.85, 7.1, 0.45), (2.0, 4.8, 0.95), 0.2),                    # tail curled up along the right flank
         ("cap", (2.0, 4.8, 0.95), (2.02, 2.9, 1.35), 0.18), ("ball", (2.0, 2.7, 1.4), 0.26)]
    return B, H, T, None

def nemes_hull(bm):
    """the striped royal headcloth as a crisp hull (flat-shaded): flaring wings, domed crown, two lappets (I)."""
    P = []
    for s in (-1, 1):
        P += [(s*0.95, -3.4, 5.5), (s*0.85, -1.9, 5.4), (s*1.6, -3.05, 3.55), (s*1.45, -1.6, 3.55), (s*1.25, -3.4, 4.6)]
    P += [(0, -2.7, 5.95), (0, -3.45, 5.75), (0, -1.6, 5.5)]
    r = bmesh.ops.convex_hull(bm, input=[bm.verts.new(Vector(p) * FT) for p in P])
    for s in (-1, 1):   # lappets: flat bands falling onto the breast
        Q = [(s*0.75, -3.4, 3.7), (s*1.35, -3.4, 3.7), (s*0.75, -2.95, 3.7), (s*1.35, -2.95, 3.7),
             (s*0.8, -3.55, 2.35), (s*1.28, -3.5, 2.35), (s*0.8, -3.15, 2.45), (s*1.28, -3.1, 2.45)]
        bmesh.ops.convex_hull(bm, input=[bm.verts.new(Vector(p) * FT) for p in Q])
    Q = [(-0.55, -1.7, 5.2), (0.55, -1.7, 5.2), (-0.5, -0.9, 3.6), (0.5, -0.9, 3.6), (-0.5, -1.6, 3.6), (0.5, -1.6, 3.6)]
    bmesh.ops.convex_hull(bm, input=[bm.verts.new(Vector(p) * FT) for p in Q])   # queue on the nape

def sphinx_mesh(name="sphinx_template", res=0.13):
    B, H, T, _ = sphinx_parts()
    me = mb_mesh(name, B, res); bm = bmesh.new(); bm.from_mesh(me)
    for k, el in (("h", H), ("t", T)):
        m2 = mb_mesh(name + k, el, res * 0.7); bm.from_mesh(m2); bpy.data.meshes.remove(m2)
    n0 = len(bm.faces); nemes_hull(bm); bm.faces.ensure_lookup_table()
    for fa in bm.faces: fa.smooth = fa.index < n0
    bm.to_mesh(me); bm.free()
    return me
