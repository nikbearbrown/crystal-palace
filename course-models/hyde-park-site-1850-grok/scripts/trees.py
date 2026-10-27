"""Park trees for the Grok HP-SITE / MOVE sets. build_elm() is the transept r10 elm (Grok, build_transept.py) with the
vault clamps removed (open park, before the building) and the leaf cards in their own object so a season can hide or
recolour them. Feet in, metres out."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
FT = 0.3048
def _tube(bm, a, b, ra, rb, seg=8):
    d = (b - a); 
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    A = [bm.verts.new(a + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * ra) for k in range(seg)]
    B = [bm.verts.new(b + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * rb) for k in range(seg)]
    for k in range(seg): bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])

def leaf_material(name="GT_ElmLeaf", c0=(0.035, 0.065, 0.015), c1=(0.13, 0.19, 0.045)):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links; b = n["Principled BSDF"]
    ramp = n.new("ShaderNodeValToRGB"); noise = n.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.6
    ramp.color_ramp.elements[0].color = (*c0, 1); ramp.color_ramp.elements[1].color = (*c1, 1)
    l.new(noise.outputs["Fac"], ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.7
    tc = n.new("ShaderNodeTexCoord"); vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 3.0
    l.new(tc.outputs["UV"], vor.inputs["Vector"])
    lt = n.new("ShaderNodeMath"); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.42
    l.new(vor.outputs["Distance"], lt.inputs[0]); l.new(lt.outputs[0], b.inputs["Alpha"])
    m.diffuse_color = (*c1, 1)
    m["ramp_node"] = ramp.name
    return m

def build_elm(name, x, y, z0, H, D, CR, seed, bark, leaf, coll, cards_per=150, props=None):
    rnd = random.Random(seed); bm = bmesh.new(); tips = []
    def branch(p, d, length, radius, depth, wig):
        n = max(2, int(length / 4)); cur = Vector(p); dirv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dirv = (dirv + Vector((rnd.uniform(-wig, wig), rnd.uniform(-wig, wig), rnd.uniform(-wig / 3, wig / 2)))).normalized()
            cur = cur + dirv * (length / n); cur.z = min(cur.z, H - 1.0); pts.append(cur.copy())
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            r0 = radius * (1 - 0.6 * i / n); r1 = radius * (1 - 0.6 * (i + 1) / n)
            _tube(bm, a, b, r0, r1, 8 if radius > 0.6 else 5)
        if depth == 0: tips.extend(pts[len(pts) // 2:]); return
        for k in range(4 if depth >= 2 else 3):
            t = rnd.uniform(0.35, 0.95); base = pts[max(1, min(len(pts) - 1, int(round(t * n))))]
            ang = rnd.uniform(0, 2 * math.pi)
            nd = (dirv + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.1, 0.6)))).normalized()
            branch(base, nd, length * rnd.uniform(0.45, 0.62), radius * 0.5, depth - 1, wig * 1.3)
    trunk_h = H * 0.30
    branch((0, 0, -0.5), (0, 0, 1), trunk_h + 0.5, D / 2, 0, 0.03); tips.clear()
    top = Vector((0, 0, trunk_h))
    for k in range(5):
        ang = 2 * math.pi * k / 5 + rnd.uniform(-.3, .3); spread = rnd.uniform(0.45, 0.8)
        branch(top, Vector((math.cos(ang) * spread, math.sin(ang) * spread, 1)).normalized(), (H - trunk_h) * rnd.uniform(0.55, 0.7), D * 0.26, 3, 0.10)
    for k in range(6):
        zb = trunk_h * rnd.uniform(0.75, 1.0) + (H - trunk_h) * rnd.uniform(0.0, 0.25); ang = rnd.uniform(0, 2 * math.pi)
        branch(Vector((0, 0, zb)), Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.35, 0.7))).normalized(), CR * rnd.uniform(0.55, 0.8), D * 0.14, 2, 0.12)
    bmesh.ops.scale(bm, vec=(FT, FT, FT), verts=bm.verts)
    me = bpy.data.meshes.new(name + "_wood"); bm.to_mesh(me); bm.free(); me.materials.append(bark)
    for pg in me.polygons: pg.use_smooth = True
    W = bpy.data.objects.new(name + "_WOOD", me); W.location = (x * FT, y * FT, z0 * FT); coll.objects.link(W)
    W["part_kind"] = "elm_wood"
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    zc = trunk_h + (H - trunk_h) * 0.5; hz = (H - trunk_h) * 0.62; cl = cards = 0
    for tp in tips:
        if rnd.random() < 0.05: continue
        c = Vector(tp) + Vector((rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(0, 2.5))); r = rnd.uniform(3.0, 5.0)
        if c.z < H * 0.26: continue
        if math.hypot(c.x, c.y) + r * 0.6 > CR or (c.z - zc) / hz > 1.0 or c.z + r > H: continue
        cl += 1
        for j in range(cards_per):
            v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() * (r * rnd.uniform(0.55, 1.0) ** 0.5); v.z *= 0.75
            q = c + v; nrm = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 1))).normalized()
            t1 = nrm.cross(Vector((0.3, 0.2, 1))).normalized(); t2 = nrm.cross(t1); sz = rnd.uniform(0.45, 0.8) * (150 / cards_per) ** 0.5
            vs = [bm.verts.new((q + (t1 * sx + t2 * sy) * sz) * FT) for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            f = bm.faces.new(vs)
            for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lp[uvl].uv = uv
            cards += 1
    me = bpy.data.meshes.new(name + "_leaves"); bm.to_mesh(me); bm.free(); me.materials.append(leaf)
    L = bpy.data.objects.new(name + "_LEAVES", me); L.location = W.location; coll.objects.link(L)
    L["part_kind"] = "elm_leaves"; L["clusters"] = cl; L["cards"] = cards
    for o in (W, L):
        for k, v in (props or {}).items(): o[k] = v
    return W, L

def round_tree_mesh(name, seed, H, bark, foliage, crown=0.2):
    """cheap broadleaf (x06 exterior mesh_park_tree recipe, Grok) for distant rows; origin at the trunk foot"""
    rr = random.Random(seed); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=1.4 * FT, radius2=0.9 * FT, depth=H * 0.5 * FT,
                          matrix=Matrix.Translation((0, 0, H * 0.25 * FT)))
    nb = len(bm.faces)
    for k in range(9):
        a = rr.uniform(0, 2 * math.pi); d = rr.uniform(0, H * 0.18); z = rr.uniform(H * 0.5, H * 0.82); r = rr.uniform(H * (crown - 0.06), H * (crown + 0.02))
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r * FT, matrix=Matrix.Translation((d * math.cos(a) * FT, d * math.sin(a) * FT, z * FT)))
    bm.faces.ensure_lookup_table()
    for f in bm.faces[nb:]: f.material_index = 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(bark); me.materials.append(foliage)
    return me
