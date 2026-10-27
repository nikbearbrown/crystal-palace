"""CP071 set improve: patterned brick/tile, column bases/caps, dado, ribs, lamps, boards.
Opens parknow blend, dresses G_STATION_subway, saves round. Does NOT touch people or sun/world/exposure.
usage: blender -b rounds/parknow-r02.blend -P scripts/improve_subway_set.py -- rounds/parknow-r18.blend
"""
import bpy, sys, math, os
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/tmp/parknow-r18.blend'

def mat_noise(n, c0, c1, rough=0.85, scale=12.0, bump=0.08, detail=6.0):
    M = bpy.data.materials.get(n) or bpy.data.materials.new(n)
    M.use_nodes = True
    nt = M.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = detail
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.35
    cr.color_ramp.elements[0].color = (*c0, 1)
    cr.color_ramp.elements[1].position = 0.72
    cr.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = bump
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs[0], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = rough
    nt.links.new(b.outputs[0], out.inputs[0])
    M.diffuse_color = (*c0, 1)
    return M

def mat_solid(n, c, rough=0.85, metal=0.0):
    M = bpy.data.materials.get(n) or bpy.data.materials.new(n)
    M.use_nodes = True
    b = M.node_tree.nodes.get('Principled BSDF')
    if not b:
        for node in list(M.node_tree.nodes):
            M.node_tree.nodes.remove(node)
        out = M.node_tree.nodes.new('ShaderNodeOutputMaterial')
        b = M.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        M.node_tree.links.new(b.outputs[0], out.inputs[0])
    b.inputs['Base Color'].default_value = (*c, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    M.diffuse_color = (*c, 1)
    return M

def mat_checker(n, c0, c1, scale=6.0, rough=0.7):
    M = bpy.data.materials.get(n) or bpy.data.materials.new(n)
    M.use_nodes = True
    nt = M.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    ck = nt.nodes.new('ShaderNodeTexChecker')
    ck.inputs['Scale'].default_value = scale
    ck.inputs['Color1'].default_value = (*c0, 1)
    ck.inputs['Color2'].default_value = (*c1, 1)
    nt.links.new(ck.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    nt.links.new(b.outputs[0], out.inputs[0])
    M.diffuse_color = (*c0, 1)
    return M

def box(name, coll, x0, x1, y0, y1, z0, z1, mat_):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    if mat_: me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); return ob

# Collections
SUB = bpy.data.collections.get('G_STATION_subway')
if SUB is None:
    SUB = bpy.data.collections.new('G_STATION_subway_dress')
    bpy.context.scene.collection.children.link(SUB)

# Materials (richer than flat cream/orange)
M_cream = mat_noise('PK_VaultCream_r18', (0.72, 0.66, 0.52), (0.82, 0.76, 0.62), rough=0.88, scale=22.0, bump=0.10)
M_red = mat_noise('PK_VaultRed_r18', (0.38, 0.10, 0.07), (0.52, 0.16, 0.10), rough=0.88, scale=18.0, bump=0.12)
M_tile = mat_checker('PK_TileFloor_r18', (0.48, 0.28, 0.14), (0.62, 0.42, 0.22), scale=14.0, rough=0.55)
M_tile_border = mat_noise('PK_TileBorder_r18', (0.22, 0.18, 0.14), (0.32, 0.26, 0.20), rough=0.7, scale=8.0, bump=0.06)
M_stone = mat_noise('PK_StoneCap_r18', (0.45, 0.42, 0.36), (0.60, 0.56, 0.48), rough=0.9, scale=7.0, bump=0.14)
M_dado = mat_noise('PK_DadoTile_r18', (0.28, 0.22, 0.18), (0.40, 0.32, 0.26), rough=0.75, scale=30.0, bump=0.08)
M_iron = mat_solid('PK_IronFixture_r18', (0.12, 0.12, 0.13), rough=0.45, metal=0.55)
M_glass_lamp = mat_solid('PK_LampGlass_r18', (0.95, 0.90, 0.75), rough=0.25)
# mild emission on lamp glass for fixture read (set dressing; sun/world untouched)
try:
    b = M_glass_lamp.node_tree.nodes['Principled BSDF']
    b.inputs['Emission Color'].default_value = (1.0, 0.92, 0.75, 1)
    b.inputs['Emission Strength'].default_value = 2.5
except Exception:
    pass
M_board = mat_noise('PK_BoardFrame_r18', (0.55, 0.48, 0.38), (0.35, 0.30, 0.24), rough=0.8, scale=4.0, bump=0.05)
M_poster = mat_solid('PK_Poster_r18', (0.75, 0.70, 0.55), rough=0.9)

# Remat existing subway shell
remap = {
    'pk_subway_floor': M_tile,
    'pk_subway_wall_L': M_cream,
    'pk_subway_wall_R': M_cream,
    'pk_subway_exit': M_stone,
}
for o in bpy.data.objects:
    if o.name.startswith('pk_vault_bay_'):
        remap[o.name] = M_cream
    if o.name.startswith('pk_col_'):
        remap[o.name] = M_red
for nm, m in remap.items():
    o = bpy.data.objects.get(nm)
    if not o or not o.data: continue
    o.data.materials.clear()
    o.data.materials.append(m)

# Geometry extents (metres) from existing floor
fl = bpy.data.objects['pk_subway_floor']
bb = [fl.matrix_world @ Vector(v) for v in fl.bound_box]
x0, x1 = min(v.x for v in bb), max(v.x for v in bb)
y0, y1 = min(v.y for v in bb), max(v.y for v in bb)
z_floor = max(v.z for v in bb)
w = x1 - x0  # ~5.49
# wall height from wall_L
wl = bpy.data.objects.get('pk_subway_wall_L')
z_spring = z_floor + 2.44
if wl:
    bbw = [wl.matrix_world @ Vector(v) for v in wl.bound_box]
    z_spring = max(v.z for v in bbw)

# Floor border / drainage channel
box('pk_r18_floor_border_L', SUB, x0, x0 + 0.18, y0, y1, z_floor, z_floor + 0.02, M_tile_border)
box('pk_r18_floor_border_R', SUB, x1 - 0.18, x1, y0, y1, z_floor, z_floor + 0.02, M_tile_border)
box('pk_r18_drain_L', SUB, x0 + 0.02, x0 + 0.10, y0 + 0.3, y1 - 0.3, z_floor - 0.04, z_floor + 0.01, M_iron)
box('pk_r18_drain_R', SUB, x1 - 0.10, x1 - 0.02, y0 + 0.3, y1 - 0.3, z_floor - 0.04, z_floor + 0.01, M_iron)

# Dado band on walls (~1.1 m)
dado_h = 1.1
box('pk_r18_dado_L', SUB, x0 - 0.02, x0 + 0.04, y0, y1, z_floor, z_floor + dado_h, M_dado)
box('pk_r18_dado_R', SUB, x1 - 0.04, x1 + 0.02, y0, y1, z_floor, z_floor + dado_h, M_dado)
# Red brick string course at spring
box('pk_r18_string_L', SUB, x0 - 0.03, x0 + 0.05, y0, y1, z_spring - 0.18, z_spring + 0.05, M_red)
box('pk_r18_string_R', SUB, x1 - 0.05, x1 + 0.03, y0, y1, z_spring - 0.18, z_spring + 0.05, M_red)

# Column bases + capitals
cols = [o for o in bpy.data.objects if o.name.startswith('pk_col_')]
for o in cols:
    bb = [o.matrix_world @ Vector(v) for v in o.bound_box]
    cx = 0.5 * (min(v.x for v in bb) + max(v.x for v in bb))
    cy = 0.5 * (min(v.y for v in bb) + max(v.y for v in bb))
    cz0 = min(v.z for v in bb)
    cz1 = max(v.z for v in bb)
    hw, hd = 0.22, 0.18
    box(f'pk_r18_base_{o.name}', SUB, cx - hw, cx + hw, cy - hd, cy + hd, cz0, cz0 + 0.22, M_stone)
    box(f'pk_r18_cap_{o.name}', SUB, cx - hw, cx + hw, cy - hd, cy + hd, cz1 - 0.18, cz1 + 0.06, M_stone)

# Transverse vault ribs (iron) every other bay
bays = sorted([o for o in bpy.data.objects if o.name.startswith('pk_vault_bay_')], key=lambda o: o.name)
for i, o in enumerate(bays):
    if i % 2: continue
    bb = [o.matrix_world @ Vector(v) for v in o.bound_box]
    ya = min(v.y for v in bb); yb = max(v.y for v in bb)
    ym = 0.5 * (ya + yb)
    # thin rib strip across vault at mid-bay (approx crown height)
    zc = max(v.z for v in bb)
    box(f'pk_r18_rib_{i}', SUB, x0 + 0.05, x1 - 0.05, ym - 0.04, ym + 0.04, z_spring + 0.05, zc + 0.02, M_iron)

# Hanging lamp fixtures (geometry) under vault at bay centres
for i, o in enumerate(bays[::2]):
    bb = [o.matrix_world @ Vector(v) for v in o.bound_box]
    ym = 0.5 * (min(v.y for v in bb) + max(v.y for v in bb))
    zc = max(v.z for v in bb) - 0.15
    box(f'pk_r18_lamp_stem_{i}', SUB, -0.03, 0.03, ym - 0.03, ym + 0.03, zc - 0.55, zc, M_iron)
    box(f'pk_r18_lamp_bowl_{i}', SUB, -0.18, 0.18, ym - 0.18, ym + 0.18, zc - 0.72, zc - 0.52, M_glass_lamp)
    box(f'pk_r18_lamp_shade_{i}', SUB, -0.22, 0.22, ym - 0.22, ym + 0.22, zc - 0.55, zc - 0.48, M_iron)

# Interpretation / poster boards on side walls (set dressing)
for i, y in enumerate((y0 + 4.0, y0 + 10.0, y0 + 16.0)):
    box(f'pk_r18_board_L_{i}', SUB, x0 + 0.03, x0 + 0.08, y - 0.55, y + 0.55, z_floor + 1.35, z_floor + 2.15, M_board)
    box(f'pk_r18_poster_L_{i}', SUB, x0 + 0.08, x0 + 0.09, y - 0.48, y + 0.48, z_floor + 1.42, z_floor + 2.08, M_poster)
    box(f'pk_r18_board_R_{i}', SUB, x1 - 0.08, x1 - 0.03, y - 0.55, y + 0.55, z_floor + 1.35, z_floor + 2.15, M_board)
    box(f'pk_r18_poster_R_{i}', SUB, x1 - 0.09, x1 - 0.08, y - 0.48, y + 0.48, z_floor + 1.42, z_floor + 2.08, M_poster)

# Far-end patterned bulkhead face (south toward exit / north seal)
# Cam looks -Y so far end is smaller y (y0 / exit)
box('pk_r18_end_face', SUB, x0 + 0.05, x1 - 0.05, y0 + 0.02, y0 + 0.12, z_floor, z_spring + 0.3, M_cream)
box('pk_r18_end_arch_band', SUB, x0 + 0.3, x1 - 0.3, y0 + 0.12, y0 + 0.18, z_spring - 0.35, z_spring + 0.15, M_red)

# Handrail along R wall
box('pk_r18_rail', SUB, x1 - 0.28, x1 - 0.22, y0 + 1.0, y1 - 1.0, z_floor + 0.95, z_floor + 1.02, M_iron)
for k, y in enumerate((y0 + 3, y0 + 8, y0 + 13, y0 + 18)):
    box(f'pk_r18_rail_post_{k}', SUB, x1 - 0.30, x1 - 0.20, y - 0.04, y + 0.04, z_floor, z_floor + 1.0, M_iron)

# Do not touch lights / world / exposure
print('IMPROVED subway set; expo', bpy.context.scene.view_settings.exposure, flush=True)
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT, flush=True)
