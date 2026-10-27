# Metaball sculpting helper (feet in, metres out). Copied from grok-sydenham-1856 scripts/sculpt.py. The metaball-to-mesh helper is adapted from the HP executor's figures.py `_mb_mesh`
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

