"""CP001 1936 park establish: richer tree crowns/bark, grass/path noise, kerbs, road — no people, keep lighting.
Dated: 1936 prologue — palace + water towers remain (do not remove).
usage: blender -b rounds/sydenham-1936-r12.blend -P scripts/improve_1936_park_set.py -- rounds/sydenham-1936-r18.blend
"""
import bpy, sys, math, os, random
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/tmp/sydenham-1936-r18.blend'
R = random.Random(1936)

def mat_noise(n, c0, c1, rough=0.9, scale=12.0, bump=0.1, detail=6.0):
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
    cr.color_ramp.elements[0].position = 0.34
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

D = bpy.data.collections.get('SY_1936_park_dress_r18')
if D is None:
    D = bpy.data.collections.new('SY_1936_park_dress_r18')
    bpy.context.scene.collection.children.link(D)

M_leaf = mat_noise('park_leaf_r18', (0.08, 0.22, 0.06), (0.18, 0.36, 0.12), rough=0.88, scale=22.0, bump=0.07)
M_leaf2 = mat_noise('park_leaf2_r18', (0.12, 0.28, 0.08), (0.05, 0.16, 0.04), rough=0.9, scale=18.0, bump=0.06)
M_bark = mat_noise('park_bark_r18', (0.16, 0.10, 0.06), (0.28, 0.18, 0.10), rough=0.92, scale=16.0, bump=0.22)
M_grass = mat_noise('park_grass_r18', (0.12, 0.24, 0.08), (0.22, 0.36, 0.14), rough=0.95, scale=35.0, bump=0.08)
M_gravel = mat_noise('park_gravel_r18', (0.42, 0.38, 0.32), (0.55, 0.50, 0.42), rough=0.9, scale=18.0, bump=0.1)
M_road = mat_noise('park_road_r18', (0.18, 0.18, 0.17), (0.28, 0.27, 0.25), rough=0.95, scale=5.0, bump=0.06)
M_kerb = mat_solid('park_kerb_r18', (0.48, 0.46, 0.42), rough=0.85)

# Remat terrain / paths
for nm, m in (('park_slope', M_grass), ('terrain', M_grass), ('central_walk', M_gravel),
              ('terrace_gravel', M_gravel), ('central_walk.001', M_gravel),
              ('central_walk.002', M_gravel), ('central_walk.003', M_gravel)):
    o = bpy.data.objects.get(nm)
    if not o or not getattr(o, 'data', None) or not hasattr(o.data, 'materials'): continue
    o.data.materials.clear(); o.data.materials.append(m)

# Upgrade existing placeholder trees: bark + leaf noise; add secondary canopy blobs
crowns = [o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_park_tree') and 'crown' in o.name]
trunks = {o.name: o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_park_tree') and 'trunk' in o.name}
for i, crown in enumerate(crowns):
    if crown.data and crown.data.materials:
        crown.data.materials[0] = M_leaf if i % 2 == 0 else M_leaf2
    elif crown.data:
        crown.data.materials.append(M_leaf)
    for p in crown.data.polygons:
        p.use_smooth = True
    # find sibling trunk
    tname = crown.name.replace('_crown', '_trunk')
    trunk = trunks.get(tname) or bpy.data.objects.get(tname)
    if trunk and trunk.data:
        if trunk.data.materials:
            trunk.data.materials[0] = M_bark
        else:
            trunk.data.materials.append(M_bark)
    # secondary canopy blobs for volume (not people)
    loc = crown.matrix_world.translation.copy()
    sc = crown.dimensions
    for j in range(3):
        off = Vector((R.uniform(-0.35, 0.35) * sc.x,
                      R.uniform(-0.35, 0.35) * sc.y,
                      R.uniform(-0.15, 0.35) * sc.z))
        nm = f'r18_canopy_{i}_{j}'
        if nm in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=loc + off)
        ob = bpy.context.active_object
        ob.name = nm
        ob.scale = (sc.x * R.uniform(0.35, 0.55),
                    sc.y * R.uniform(0.35, 0.55),
                    sc.z * R.uniform(0.30, 0.50))
        ob.data.materials.append(M_leaf2 if j else M_leaf)
        for p in ob.data.polygons: p.use_smooth = True
        for c in list(ob.users_collection):
            c.objects.unlink(ob)
        D.objects.link(ob)

# Road strip near CP001 cam (foreground gray strip) — find large road-like objects or add kerbs along central walk
cw = bpy.data.objects.get('central_walk')
if cw:
    bb = [cw.matrix_world @ Vector(v) for v in cw.bound_box]
    x0, x1 = min(v.x for v in bb), max(v.x for v in bb)
    y0, y1 = min(v.y for v in bb), max(v.y for v in bb)
    z0 = max(v.z for v in bb)
    # kerbs along walk edges
    box_m('r18_kerb_L', D, x0 - 0.35, x0, y0, y1, z0, z0 + 0.18, M_kerb)
    box_m('r18_kerb_R', D, x1, x1 + 0.35, y0, y1, z0, z0 + 0.18, M_kerb)

# Parade / foreground road near cam CP001 at y~-655
cam = bpy.data.objects.get('CAM_CP001_prologue_distant_35mm')
if cam:
    # asphalt band in foreground of cam
    cy = cam.location.y
    cz = cam.location.z - 1.4
    box_m('r18_fg_road', D, -120, 120, cy - 5, cy + 35, cz - 0.05, cz + 0.08, M_road)
    box_m('r18_fg_kerb_N', D, -120, 120, cy + 34.5, cy + 35.2, cz + 0.08, cz + 0.22, M_kerb)
    box_m('r18_fg_kerb_S', D, -120, 120, cy - 5.2, cy - 4.5, cz + 0.08, cz + 0.22, M_kerb)

# Low hedge clumps along path (set dressing, not people)
for i in range(24):
    x = R.uniform(-90, 90)
    y = R.uniform(-600, -200)
    z = -0.06 * (y + 80) - 5  # rough
    if cam:
        # place near ground under cam sightline — use park_slope approx
        z = cam.location.z - 8 + R.uniform(-2, 4)
    nm = f'r18_hedge_{i}'
    if nm in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, z))
    ob = bpy.context.active_object
    ob.name = nm
    ob.scale = (R.uniform(2.5, 5.0), R.uniform(1.5, 3.0), R.uniform(1.0, 1.8))
    ob.data.materials.append(M_leaf2)
    for p in ob.data.polygons: p.use_smooth = True
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    D.objects.link(ob)

# Safety: do not hide water towers (1936 dated)
for nm in ('water_tower_north', 'water_tower_south', 'water_tower_base_north', 'water_tower_base_south'):
    o = bpy.data.objects.get(nm)
    if o:
        o.hide_render = False
        o.hide_viewport = False

print('IMPROVED 1936 park set; expo', bpy.context.scene.view_settings.exposure, flush=True)
# confirm towers exist
print('towers present', [n for n in ('water_tower_north','water_tower_south') if bpy.data.objects.get(n)], flush=True)
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT, flush=True)
