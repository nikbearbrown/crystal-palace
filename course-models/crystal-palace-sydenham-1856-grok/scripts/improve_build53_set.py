"""CP033 BUILD53 set improve: clay noise, spoil/cut dressing, timber/iron stock, scaffold decks,
tram sleepers — no people edits, no lighting rewrite.
usage: blender -b rounds/sydenham-build53-r14.blend -P scripts/improve_build53_set.py -- rounds/sydenham-build53-r18.blend
"""
import bpy, sys, math, os, random
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/tmp/sydenham-build53-r18.blend'
R = random.Random(1853)

def mat_noise(n, c0, c1, rough=0.92, scale=8.0, bump=0.12, detail=5.0):
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
    cr.color_ramp.elements[0].position = 0.32
    cr.color_ramp.elements[0].color = (*c0, 1)
    cr.color_ramp.elements[1].position = 0.7
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

def box_m(name, coll, x0, x1, y0, y1, z0, z1, mat_):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    if mat_: me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); return ob

def ico_blob(name, coll, loc, scale, mat_):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    me = ob.data
    me.materials.clear(); me.materials.append(mat_)
    for p in me.polygons: p.use_smooth = True
    # unlink from scene collection, link to ours
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

# Find / make dress collection under BUILD
B = bpy.data.collections.get('SY-BUILD_construction_1853__dated')
if B is None:
    B = bpy.data.collections.new('SY-BUILD_construction_1853__dated')
    bpy.context.scene.collection.children.link(B)
D = bpy.data.collections.get('SY_BUILD53_dress_r18')
if D is None:
    D = bpy.data.collections.new('SY_BUILD53_dress_r18')
    B.children.link(D)

M_clay = mat_noise('build53_clay_r18', (0.22, 0.14, 0.08), (0.38, 0.26, 0.14), rough=0.95, scale=6.5, bump=0.18)
M_clay2 = mat_noise('build53_clay_wet_r18', (0.16, 0.11, 0.07), (0.28, 0.18, 0.10), rough=0.7, scale=4.0, bump=0.1)
M_meadow = mat_noise('build53_meadow_r18', (0.07, 0.12, 0.04), (0.16, 0.24, 0.08), rough=0.95, scale=28.0, bump=0.08)
M_timber = mat_noise('build53_timber_r18', (0.28, 0.18, 0.10), (0.42, 0.30, 0.16), rough=0.88, scale=14.0, bump=0.15)
M_iron = mat_solid('build53_iron_r18', (0.09, 0.09, 0.10), rough=0.45, metal=0.6)
M_gravel = mat_noise('build53_gravel_r18', (0.18, 0.16, 0.13), (0.30, 0.26, 0.20), rough=0.95, scale=20.0, bump=0.12)
M_mud = mat_noise('build53_mud_r18', (0.14, 0.10, 0.06), (0.22, 0.15, 0.09), rough=0.55, scale=3.5, bump=0.05)

# Remat existing clay/meadow targets
for nm in ('terrace_gravel', 'terrain', 'ground_under_palace', 'earth_spoil_heaps_cuttings',
           'central_walk', 'central_walk.001', 'central_walk.002', 'central_walk.003', 'central_walk.004'):
    o = bpy.data.objects.get(nm)
    if not o or not getattr(o, 'data', None): continue
    if not hasattr(o.data, 'materials'): continue
    o.data.materials.clear(); o.data.materials.append(M_clay)
ps = bpy.data.objects.get('park_slope')
if ps and ps.data:
    # keep dual slots: clay + meadow
    while len(ps.data.materials) < 2:
        ps.data.materials.append(None)
    ps.data.materials[0] = M_clay
    ps.data.materials[1] = M_meadow

# Remat timber / wagons / rails with richer mats
for nm, m in (('build53_timber', M_timber), ('build53_tip_wagons', M_timber),
              ('build53_tramway_rails', M_iron), ('build53_horses', None)):
    o = bpy.data.objects.get(nm)
    if not o or not o.data or m is None: continue
    if o.data.materials:
        o.data.materials[0] = m
    else:
        o.data.materials.append(m)

# Camera-facing spoil extras (CP033 cam ~ (79,-329,-23) looking toward palace)
# Place mounds + baulks in mid-ground between cam and palace
cam = bpy.data.objects.get('CAM_CP033_slope_up_35mm')
# Spoil mounds along tram lines and mid-slope
for i in range(14):
    x = R.uniform(-40, 220)
    y = R.uniform(-900, -280)
    z = -45 + R.uniform(-5, 8)  # approximate slope band; will sit on clay visually
    # try ray-ish: use park_slope z via nearest if available — approximate from cam band
    # linear fall: at y=-329 z~-23 cam; palace y~-60 z~0 → rough z ≈ -0.08*(y+60) for mid
    z = -0.075 * (y + 100) + R.uniform(-2, 3)
    r = R.uniform(8, 22)
    h = r * R.uniform(0.35, 0.55)
    ico_blob(f'b53_r18_spoil_{i}', D, (x, y, z), (r, r * 0.85, h), M_clay if i % 3 else M_clay2)

# Timber baulk stacks in midground (visible from slope cam)
for i, (x, y) in enumerate(((40, -520), (120, -480), (200, -560), (-30, -440), (90, -380), (160, -620))):
    z = -0.075 * (y + 100)
    for k in range(4):
        box_m(f'b53_r18_baulk_{i}_{k}', D,
              x - 6 + k * 0.1, x + 6 + k * 0.1,
              y - 0.4 + k * 0.35, y + 0.4 + k * 0.35,
              z + k * 0.55, z + 0.45 + k * 0.55, M_timber)

# Iron girder stock near lookat
for i, (x, y) in enumerate(((60, -350), (100, -320), (140, -400))):
    z = -0.075 * (y + 100) + 0.3
    for k in range(5):
        box_m(f'b53_r18_girder_{i}_{k}', D,
              x - 10, x + 10, y + k * 1.2, y + k * 1.2 + 0.35,
              z, z + 0.55, M_iron)

# Scaffold deck platforms (planks) mid-slope toward frame
for i, (x, y, zh) in enumerate(((70, -250, 12), (110, -220, 18), (30, -280, 8), (150, -200, 22))):
    z = -0.05 * (y + 80)
    box_m(f'b53_r18_deck_{i}', D, x - 8, x + 8, y - 4, y + 4, z + zh, z + zh + 0.35, M_timber)
    # uprights
    for sx, sy in ((-7, -3), (7, -3), (-7, 3), (7, 3)):
        box_m(f'b53_r18_upright_{i}_{sx}_{sy}', D,
              x + sx - 0.2, x + sx + 0.2, y + sy - 0.2, y + sy + 0.2,
              z, z + zh, M_timber)

# Tram sleeper boards under existing rails (visual density)
# Sample tramway object bounds
tram = bpy.data.objects.get('build53_tramway_rails')
if tram:
    for k in range(0, 40):
        # three lines roughly as eras.py: (-300,-230), (300,230), (-620,-560) in feet → metres *0.3048
        for li, (xa, xb) in enumerate(((-91.4, -70.1), (91.4, 70.1), (-189.0, -170.7))):
            t = k / 39.0
            y = -51.8 - k * 7.315  # -170*ft - k*24*ft
            x = xa + (xb - xa) * t
            z = -0.075 * (y + 100) + 0.15
            box_m(f'b53_r18_sleeper_{li}_{k}', D, x - 1.2, x + 1.2, y - 0.18, y + 0.18, z, z + 0.22, M_timber)

# Mud/puddle patches near cam foreground
for i in range(8):
    x = R.uniform(40, 160)
    y = R.uniform(-700, -450)
    z = -0.075 * (y + 100) + 0.05
    box_m(f'b53_r18_puddle_{i}', D, x - 4, x + 4, y - 2.5, y + 2.5, z, z + 0.04, M_mud)

# Site fence posts along a tram edge
for k in range(20):
    y = -700 + k * 18
    x = 25
    z = -0.075 * (y + 100)
    box_m(f'b53_r18_fence_{k}', D, x - 0.12, x + 0.12, y - 0.12, y + 0.12, z, z + 2.4, M_timber)

print('IMPROVED BUILD53 set; expo', bpy.context.scene.view_settings.exposure, flush=True)
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT, flush=True)
