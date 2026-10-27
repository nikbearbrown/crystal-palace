"""Fix floating r18 BUILD53 dress: snap Z to park_slope/terrain; drop sky decks."""
import bpy, math, os, sys
from mathutils import Vector, bvhtree

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/tmp/sydenham-build53-r18b.blend'


# Build BVH from park_slope + terrain + earth spoil
meshes = []
for nm in ('park_slope', 'terrain', 'ground_under_palace', 'earth_spoil_heaps_cuttings'):
    o = bpy.data.objects.get(nm)
    if o and o.type == 'MESH':
        meshes.append(o)

deps = bpy.context.evaluated_depsgraph_get()
bvh_list = []
for o in meshes:
    eo = o.evaluated_get(deps)
    me = eo.to_mesh()
    try:
        me.transform(o.matrix_world)
        bvh = bvhtree.BVHTree.FromPolygons([v.co.copy() for v in me.vertices],
                                           [p.vertices[:] for p in me.polygons])
        bvh_list.append(bvh)
    finally:
        eo.to_mesh_clear()

def ground_z(x, y, fallback=-30.0):
    best = None
    origin = Vector((x, y, 200.0))
    direction = Vector((0, 0, -1))
    for bvh in bvh_list:
        hit = bvh.ray_cast(origin, direction)
        if hit[0] is not None:
            z = hit[0].z
            if best is None or z > best:  # highest hit from above
                best = z
    return best if best is not None else fallback

D = bpy.data.collections.get('SY_BUILD53_dress_r18')
if not D:
    print('no dress coll'); raise SystemExit(1)

# Remove high scaffold decks/uprights that floated (recreate lower later)
remove_prefix = ('b53_r18_deck_', 'b53_r18_upright_')
for o in list(D.objects):
    if o.name.startswith(remove_prefix):
        bpy.data.objects.remove(o, do_unlink=True)

# Snap remaining dress objects
for o in list(D.objects):
    if o.type != 'MESH':
        continue
    # use object center xy
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    cx = 0.5 * (min(v.x for v in bb) + max(v.x for v in bb))
    cy = 0.5 * (min(v.y for v in bb) + max(v.y for v in bb))
    zmin = min(v.z for v in bb)
    gz = ground_z(cx, cy)
    dz = gz - zmin
    # spoil blobs: bottom should sit slightly into ground
    if 'spoil' in o.name:
        o.location.z += dz - 0.5
    elif 'puddle' in o.name:
        o.location.z += dz + 0.02
    elif 'fence' in o.name or 'sleeper' in o.name or 'baulk' in o.name or 'girder' in o.name:
        o.location.z += dz
    else:
        o.location.z += dz

# Add grounded scaffold platforms near construction (low decks on slope)
def box_m(name, coll, x0, x1, y0, y1, z0, z1, mat_):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    if mat_: me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); return ob

M_timber = bpy.data.materials.get('build53_timber_r18')
for i, (x, y) in enumerate(((70, -420), (110, -380), (40, -500), (150, -450), (90, -340))):
    gz = ground_z(x, y)
    box_m(f'b53_r18b_deck_{i}', D, x - 6, x + 6, y - 3, y + 3, gz + 2.2, gz + 2.5, M_timber)
    for sx, sy in ((-5, -2.5), (5, -2.5), (-5, 2.5), (5, 2.5)):
        box_m(f'b53_r18b_post_{i}_{sx}_{sy}', D,
              x + sx - 0.15, x + sx + 0.15, y + sy - 0.15, y + sy + 0.15,
              gz, gz + 2.2, M_timber)

# Extra cut-face benches near midfield (stepped clay blocks)
M_clay = bpy.data.materials.get('build53_clay_r18')
for i, (x, y) in enumerate(((180, -300), (200, -280), (160, -320), (220, -260))):
    gz = ground_z(x, y)
    for k in range(3):
        box_m(f'b53_r18b_bench_{i}_{k}', D,
              x - 12, x + 12, y - 2 + k * 3, y + 1 + k * 3,
              gz + k * 1.8, gz + 1.5 + k * 1.8, M_clay)

print('FIXED dress Z; sample ground', ground_z(79, -329), ground_z(100, -400))
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT)
