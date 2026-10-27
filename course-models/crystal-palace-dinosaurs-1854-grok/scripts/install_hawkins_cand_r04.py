"""CANDIDATE r04: install recognisable Hawkins sculptures + broadleaf trees + soft water.
Does NOT overwrite live start renders. Saves rounds/dinosaurs-1854-r04-cand.blend.
"""
import bpy, bmesh, math, os, random, shutil
from mathutils import Vector, Matrix

BASE = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
PACK = '/workspace/crystal-palace-dinosaurs/models/hawkins-dinosaurs/hawkins-dinosaurs.blend'
SRC = os.path.join(BASE, 'rounds/dinosaurs-1854-r03b.blend')
OUT = os.path.join(BASE, 'rounds/dinosaurs-1854-r04-cand.blend')

# scene object name -> pack mesh object name
SWAP = {
    'iguanodon_standing': 'hawkins_iguanodon_standing',
    'iguanodon_recumbent': 'hawkins_iguanodon_recumbent',
    'megalosaurus': 'hawkins_megalosaurus',
    'hylaeosaurus': 'hawkins_hylaeosaurus',
    'ichthyosaur_1': 'hawkins_ichthyosaur',
    'ichthyosaur_2': 'hawkins_ichthyosaur',
    'ichthyosaur_3': 'hawkins_ichthyosaur',
    'plesiosaur_1': 'hawkins_plesiosaur',
    'plesiosaur_2': 'hawkins_plesiosaur',
    'plesiosaur_3': 'hawkins_plesiosaur',
}

def append_pack():
    with bpy.data.libraries.load(PACK, link=False) as (data_from, data_to):
        want = list({v for v in SWAP.values()})
        data_to.objects = [n for n in data_from.objects if n in want]
    imported = {}
    for o in data_to.objects:
        if o is None: continue
        # keep out of view; we only need mesh data
        bpy.context.collection.objects.link(o)
        o.hide_render = True; o.hide_viewport = True
        imported[o.name] = o
    return imported

def replace_mesh(scene_obj, src_obj):
    """Swap mesh, match prior world dimensions, keep location/rotation."""
    old_dim = scene_obj.dimensions.copy()
    # copy mesh so multiple ichthyosaurs don't share edits oddly
    me = src_obj.data.copy()
    me.name = scene_obj.name + '_cand'
    # assign materials from pack (already on me)
    old_me = scene_obj.data
    scene_obj.data = me
    # reset object scale first
    scene_obj.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    new_dim = scene_obj.dimensions.copy()
    # uniform-ish scale to match length (X) primarily, clamp extremes
    sx = (old_dim.x / new_dim.x) if new_dim.x > 1e-3 else 1.0
    sy = (old_dim.y / new_dim.y) if new_dim.y > 1e-3 else 1.0
    sz = (old_dim.z / new_dim.z) if new_dim.z > 1e-3 else 1.0
    # prefer mostly uniform; average with slight height priority for standing forms
    s = (sx + sy + sz) / 3.0
    # keep height closer for land animals
    if 'ichthy' not in scene_obj.name and 'plesio' not in scene_obj.name:
        s = 0.55 * sx + 0.20 * sy + 0.25 * sz
    scene_obj.scale = (s, s, s)
    bpy.context.view_layer.update()
    # apply scale into mesh so dimensions stick
    mw = scene_obj.matrix_world.copy()
    me.transform(Matrix.Diagonal((*scene_obj.scale, 1.0)))
    me.update()
    scene_obj.scale = (1, 1, 1)
    # re-ground land animals: bottom of mesh at previous bottom z roughly
    # (preserve location.z which was set for ground/waterline)
    print(f'  swapped {scene_obj.name}: old_dim={[round(v,2) for v in old_dim]} '
          f'new_dim={[round(v,2) for v in scene_obj.dimensions]} scale={round(s,3)}')
    # orphan old mesh if unused
    if old_me.users == 0:
        bpy.data.meshes.remove(old_me)

def soft_water():
    m = bpy.data.materials.get('lake_water_still')
    if not m or not m.use_nodes: return
    nt = m.node_tree
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf: return
    # soften hard mirror reflections of trees
    bsdf.inputs['Roughness'].default_value = 0.32
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 0.55
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 0.55
    bsdf.inputs['Base Color'].default_value = (0.06, 0.13, 0.14, 1)
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.35
    elif 'Specular' in bsdf.inputs:
        bsdf.inputs['Specular'].default_value = 0.35
    # bump the existing noise if present for gentle ripple
    for n in nt.nodes:
        if n.type == 'TEX_NOISE':
            n.inputs['Scale'].default_value = 2.2
    bump = next((n for n in nt.nodes if n.type == 'BUMP'), None)
    if bump:
        bump.inputs['Strength'].default_value = 0.16
    else:
        # add mild ripple bump
        tc = next((n for n in nt.nodes if n.type == 'TEX_COORD'), None)
        if tc is None:
            tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-600, -200)
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.location = (-350, -200)
        nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 6
        bump = nt.nodes.new('ShaderNodeBump'); bump.location = (200, -120)
        bump.inputs['Strength'].default_value = 0.16
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    print('water softened: roughness=0.32 transmission=0.55')

def mat_bark():
    m = bpy.data.materials.get('bark')
    if m: return m
    m = bpy.data.materials.new('bark'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.18, 0.12, 0.07, 1)
    b.inputs['Roughness'].default_value = 0.9
    return m

def mat_leaf():
    m = bpy.data.materials.get('foliage') or bpy.data.materials.get('leaf')
    if m is None:
        m = bpy.data.materials.new('foliage'); m.use_nodes = True
    m.use_nodes = True
    b = next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'), None)
    if b is None:
        b = m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    # darker parkland leaf, less lime-blob
    b.inputs['Base Color'].default_value = (0.045, 0.12, 0.03, 1)
    b.inputs['Roughness'].default_value = 0.88
    return m

def strut(bm, a, b, r, mat_idx=0, segs=6):
    a, b = Vector(a), Vector(b)
    d = b - a
    if d.length < 1e-4: return
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs,
                                radius1=r, radius2=r * 0.55, depth=d.length)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4(),
                        verts=res['verts'])
    for f in {f for v in res['verts'] for f in v.link_faces}:
        f.material_index = mat_idx; f.smooth = True

def broadleaf(bm, x, y, z, h, kind, rr):
    """Broadleaf: tapered trunk, many scaffold branches, dense small leaf-card clusters (not mega-spheres)."""
    trunk_top = z + h * (0.62 if kind == 'mature' else 0.55)
    tip = (x + rr.uniform(-0.3, 0.3), y + rr.uniform(-0.3, 0.3), trunk_top)
    strut(bm, (x, y, z - 0.5), tip, max(0.20, h * 0.026), 0, 8)
    # upright leader
    strut(bm, tip, (tip[0], tip[1], z + h * 0.95), max(0.08, h * 0.01), 0, 5)
    n_br = 8 if kind == 'mature' else 5
    branch_tips = []
    for i in range(n_br):
        ang = i * (2 * math.pi / n_br) + rr.uniform(-0.25, 0.25)
        elev = rr.uniform(0.15, 0.55)
        L = h * rr.uniform(0.30, 0.48)
        bx = x + L * math.cos(ang) * math.cos(elev)
        by = y + L * math.sin(ang) * math.cos(elev)
        bz = trunk_top * 0.85 + L * math.sin(elev) * 0.85
        strut(bm, (x, y, trunk_top - h * 0.08), (bx, by, bz), max(0.06, h * 0.01), 0, 5)
        branch_tips.append((bx, by, bz))
        for k in range(3):
            a2 = ang + rr.uniform(-0.8, 0.8)
            L2 = L * rr.uniform(0.30, 0.55)
            tx = bx + L2 * math.cos(a2); ty = by + L2 * math.sin(a2)
            tz = bz + L2 * rr.uniform(0.05, 0.35)
            strut(bm, (bx, by, bz), (tx, ty, tz), max(0.03, h * 0.005), 0, 4)
            branch_tips.append((tx, ty, tz))
    # many small flattened leaf clusters at tips (reads as foliage mass, not 4 giant blobs)
    cr = h * (0.10 if kind == 'mature' else 0.09)
    for (cx, cy, cz) in branch_tips:
        for _ in range(2 if kind == 'mature' else 1):
            ox, oy, oz = rr.uniform(-cr, cr), rr.uniform(-cr, cr), rr.uniform(-cr * 0.4, cr * 0.6)
            rx = cr * rr.uniform(0.9, 1.4)
            ry = cr * rr.uniform(0.9, 1.4)
            rz = cr * rr.uniform(0.35, 0.55)
            res = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
            bmesh.ops.transform(bm,
                matrix=Matrix.Translation(Vector((cx+ox, cy+oy, cz+oz))) @ Matrix.Diagonal(Vector((rx, ry, rz, 1))),
                verts=res['verts'])
            for f in {f for v in res['verts'] for f in v.link_faces}:
                f.material_index = 1; f.smooth = True

def rebuild_trees():
    """Replace blob trees with broadleaf parkland + young island planting. Same seed layout."""
    old = bpy.data.objects.get('trees_parkland_and_young_island_planting')
    col = None
    if old:
        for c in old.users_collection:
            col = c; break
        bpy.data.objects.remove(old, do_unlink=True)
    if col is None:
        col = bpy.data.collections.get('DN54_lake_islands__1854')
    # ground approx from terrain; use simple: parkland at z=2.0 islands ~1.5
    # Match planting extents from build.py (metres: build uses feet*0.3048)
    F = 0.3048
    def ground_approx(x, y):
        # soft falloff — enough for trunk bases
        return 1.6
    # Island centres in metres (from build ISL * F roughly matching dims)
    # From object positions: secondary sculptures around x=-30..20, y=0..12
    # Use same relative layout as build planting but in metres matching current terrain span
    bm = bmesh.new()
    rr = random.Random(7)
    # mature N parkland
    for i in range(42):
        x = rr.uniform(-143, 180)
        y = rr.uniform(46, 78)
        h = rr.uniform(12.0, 22.0)
        broadleaf(bm, x, y, ground_approx(x, y), h, 'mature', rr)
    # mature S behind viewers
    for i in range(22):
        x = rr.uniform(-143, 180)
        y = rr.uniform(-79, -66)
        h = rr.uniform(12.0, 18.0)
        broadleaf(bm, x, y, ground_approx(x, y), h, 'mature', rr)
    # young island planting — secondary / tertiary / primary-ish
    islands = [
        (-10, 8, 45, 22, 'secondary'),   # where dinos stand
        (95, 12, 28, 18, 'tertiary'),
        (-70, 5, 30, 16, 'primary'),
    ]
    for cx, cy, a, b, nm in islands:
        n = 14 if nm == 'secondary' else 8
        for i in range(n):
            t = rr.uniform(0, 2 * math.pi)
            r = rr.uniform(0.55, 0.85)
            x = cx + a * r * math.cos(t)
            y = cy + b * r * math.sin(t)
            if y < cy - 0.2 * b and nm == 'secondary':
                continue  # keep S viewing face open
            h = rr.uniform(3.5, 6.5)
            broadleaf(bm, x, y, ground_approx(x, y), h, 'young', rr)
    me = bpy.data.meshes.new('trees_parkland_and_young_island_planting')
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('trees_parkland_and_young_island_planting', me)
    col.objects.link(o)
    me.materials.append(mat_bark())
    me.materials.append(mat_leaf())
    print('trees rebuilt broadleaf', 'verts', len(me.vertices), 'dim', [round(v, 1) for v in o.dimensions])

def also_improve_megatherium_tree():
    """Softer multi-lobe canopy on megatherium tree (same spirit)."""
    old = bpy.data.objects.get('megatherium_tree')
    if not old: return
    col = old.users_collection[0] if old.users_collection else None
    loc_hint = (91.44 + 1.9, 16.76, 1.4)  # near megatherium
    bpy.data.objects.remove(old, do_unlink=True)
    bm = bmesh.new(); rr = random.Random(99)
    x, y = 93.3, 16.8
    z = 1.4
    h = 11.0
    broadleaf(bm, x, y, z, h, 'mature', rr)
    me = bpy.data.meshes.new('megatherium_tree')
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('megatherium_tree', me)
    if col: col.objects.link(o)
    else: bpy.context.collection.objects.link(o)
    me.materials.append(mat_bark()); me.materials.append(mat_leaf())
    print('megatherium_tree rebuilt')

def main():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    print('opened', SRC)
    imported = append_pack()
    print('imported', list(imported))
    for scene_name, pack_name in SWAP.items():
        so = bpy.data.objects.get(scene_name)
        src = imported.get(pack_name)
        if not so or not src:
            print('SKIP missing', scene_name, pack_name); continue
        replace_mesh(so, src)
    # remove hidden pack helpers
    for o in list(imported.values()):
        if o.name in bpy.data.objects:
            bpy.data.objects.remove(o, do_unlink=True)
    rebuild_trees()
    also_improve_megatherium_tree()
    soft_water()
    # keep lighting from r03b (exposure etc. already in file)
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print('CANDIDATE saved', OUT)

if __name__ == '__main__':
    main()
