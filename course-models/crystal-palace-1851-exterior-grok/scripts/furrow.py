"""Render-time furrow-bay proxy for combined views (EX27 / RL05). Never saved into anyone else's file.
Appends Muse's hp-roof-furrow-bay 'Model' meshes (models/hp-roof-furrow-bay on main, author Muse) read-only, joins
them into ONE mesh (2,390 tris: 54 sash bars, 3 strong bars, 56 panes, ridge piece, 2 Paxton gutters), turns it so
the ridge runs along X (Claude's and our convention), and swaps it in as the mesh of every flat 24 x 8 ft roof unit.
The instanced units then share one mesh, so ~5,000 bays cost ~2,400 tris of memory each only once."""
import bpy, bmesh, math
from mathutils import Matrix
FT = 0.3048
MUSE_FURROW = "/workspace/models-main-ro/models/hp-roof-furrow-bay/hp-roof-furrow-bay.blend"
Z_OFF = -5 * 0.0254          # Muse origin = gutter underside; our gutter box runs -5in..+1in about the unit origin

def plain_roof_glass():
    """EX19 exterior roof-glass recipe without the painted bar mask (the bars are real geometry here)."""
    m = bpy.data.materials.get("GT_FurrowGlass")
    if m: return m
    m = bpy.data.materials.new("GT_FurrowGlass"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new("ShaderNodeOutputMaterial")
    tr = n.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (0.58, 0.64, 0.64, 1)
    gl = n.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04
    fr = n.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.52
    mx = n.new("ShaderNodeMixShader"); l.new(fr.outputs[0], mx.inputs[0]); l.new(tr.outputs[0], mx.inputs[1]); l.new(gl.outputs[0], mx.inputs[2])
    df = n.new("ShaderNodeBsdfDiffuse"); df.inputs[0].default_value = (0.55, 0.58, 0.58, 1)
    mx2 = n.new("ShaderNodeMixShader"); mx2.inputs[0].default_value = 0.025; l.new(mx.outputs[0], mx2.inputs[1]); l.new(df.outputs[0], mx2.inputs[2])
    l.new(mx2.outputs[0], out.inputs[0]); m.diffuse_color = (0.58, 0.64, 0.64, 0.3)
    return m

def furrow_mesh(path=MUSE_FURROW):
    me = bpy.data.meshes.get("FURROW_BAY_by_Muse")
    if me: return me
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [o for o in src.objects if o != "Backdrop"]
    bm = bmesh.new(); mats = []
    rot = Matrix.Translation((0, 0, Z_OFF)) @ Matrix.Rotation(math.pi / 2, 4, 'Z')
    for o in dst.objects:
        if o is None or o.type != 'MESH': continue
        tmp = o.data.copy(); tmp.transform(rot @ o.matrix_world)
        remap = []
        for mt in tmp.materials:
            if mt not in mats: mats.append(mt)
            remap.append(mats.index(mt))
        for p in tmp.polygons: p.material_index = remap[p.material_index] if remap else 0
        bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
        bpy.data.objects.remove(o)
    me = bpy.data.meshes.new("FURROW_BAY_by_Muse"); bm.to_mesh(me); bm.free()
    glass = plain_roof_glass()
    for mt in mats:
        if mt and mt.name.startswith("PaintedTimber"):
            mt.name = "PaintedTimber_by_Muse"
        me.materials.append(glass if (mt and mt.name.startswith("SheetGlass")) else mt)
    me["credit"] = "Muse (models/hp-roof-furrow-bay, read-only append)"; me["tris"] = sum(len(p.vertices) - 2 for p in me.polygons)
    return me

def is_flat_unit(me):
    if me is None or len(me.polygons) > 12 or len(me.vertices) < 4: return False
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]; zt = max(zs)
    ridge = [v for v in me.vertices if v.co.z > zt - 0.01]
    return (abs((max(xs) - min(xs)) - 24 * FT) < 0.06 and abs((max(ys) - min(ys)) - 8 * FT) < 0.3
            and 0.4 < zt < 0.56 and all(abs(v.co.y) < 0.05 for v in ridge))   # a 1.6 ft rise with the ridge on y = 0

def swap_flat_roofs(path=MUSE_FURROW):
    """Every mesh object that is a flat 24 x 8 ft ridge-along-X roof unit (Claude's PART_RoofUnit 'roof', Grok's
    'roof_unit') gets the furrow-bay mesh. Returns the number of objects swapped."""
    fm = furrow_mesh(path); n = 0; seen = {}
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.data is fm: continue
        k = ob.data.name
        if k not in seen: seen[k] = is_flat_unit(ob.data)
        if seen[k]:
            ob.data = fm; ob["furrow_proxy"] = "Muse"; n += 1
            for sl in ob.material_slots: sl.link = 'DATA'   # drop review-only object-level glass overrides
    print("FURROW_SWAP objects", n, "meshes", [k for k, v in seen.items() if v], "tris/bay", fm["tris"], flush=True)
    return n
