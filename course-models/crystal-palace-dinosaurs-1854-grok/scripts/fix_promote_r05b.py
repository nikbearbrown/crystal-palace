"""Fix CP043b then promote r05 KEEP:
- Delete CycadTrunk faces (brown diagonal Muse support) from both Iguanodons
- Nudge plesiosaur_3 fully out of CP043b left edge (floating grey hook)
- Reframe CP043b: waterline/island edge visible behind body; less empty grass+shadow
Promote: write dinosaurs-1854-r05.blend (live) from fixed cand. Trees/water untouched.
"""
import bpy, math, shutil, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

BASE = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
SRC = os.path.join(BASE, 'rounds/dinosaurs-1854-r05-cand.blend')
CAND = os.path.join(BASE, 'rounds/dinosaurs-1854-r05b-cand.blend')
LIVE = os.path.join(BASE, 'rounds/dinosaurs-1854-r05.blend')

shutil.copy2(SRC, CAND)
bpy.ops.wm.open_mainfile(filepath=CAND)

def delete_mat_faces(obj_name, mat_name):
    o = bpy.data.objects[obj_name]
    me = o.data
    idx = None
    for i, s in enumerate(o.material_slots):
        if s.material and s.material.name == mat_name:
            idx = i; break
    if idx is None:
        print('no mat', mat_name, 'on', obj_name); return 0
    # bmesh delete faces with that material_index
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me)
    faces = [f for f in bm.faces if f.material_index == idx]
    n = len(faces)
    bmesh.ops.delete(bm, geom=faces, context='FACES')
    bm.to_mesh(me); bm.free(); me.update()
    # clear unused slot material to empty (keep indices stable for other slots)
    print(f'  deleted {n} {mat_name} faces from {obj_name}')
    return n

delete_mat_faces('iguanodon_recumbent', 'CycadTrunk')
delete_mat_faces('iguanodon_standing', 'CycadTrunk')

# Floating grey hook = plesiosaur_3 clipped on left of CP043b — move west/out of this frustum
# but keep it in CP043 lake view. Shift it further south-west into water, lower.
p3 = bpy.data.objects.get('plesiosaur_3')
if p3:
    print('plesiosaur_3 before', list(p3.location))
    # Move left (more -X) and slightly +Y so 043b (looking from north) no longer clips a hook;
    # actually 043b cam looks from +Y toward -Y; left of frame is -X. Move p3 further -X out of frame.
    p3.location.x -= 6.0
    p3.location.z -= 0.4
    print('plesiosaur_3 after', list(p3.location))

# Reframe CP043b: NW of Muse looking SE — body fills frame, lake south visible behind/beside
cam = bpy.data.objects['CAM_CP043b_iguanodons_detail_50mm']
tgt = bpy.data.objects['iguanodon_recumbent']
tc = tgt.location + Vector((0.2, 0.0, 1.0))
# Closer, lower eye, from NNW so we look across body toward lake (south) and island edge
cam.location = Vector((tc.x - 4.5, tc.y + 14.0, 1.35))
aim = tc + Vector((1.5, -2.0, 0.05))  # bias toward lake/south and along body
cam.rotation_euler = (aim - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 50.0
cam.data.shift_x = 0.04   # bias content right a hair
cam.data.shift_y = 0.02   # a little more ground/water, less empty upper — wait we want LESS empty grass
# Empty grass was in foreground bottom. Looking more horizontal at body mid: raise aim z, lower shift_y negative to crop grass
cam.data.shift_y = -0.08
print('CP043b', [round(v,2) for v in cam.location], 'aim', [round(v,2) for v in aim])

# Soften the dominant tree shadow for this cam only by nudging sun? Prefer keep lighting.
# Instead: move the nearest tree casting on foreground if identifiable — trees are one joined mesh.
# Accept composition fix via framing.

# Assert water
w = bpy.data.materials['lake_water_still']
bsdf = next(n for n in w.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
assert abs(bsdf.inputs['Roughness'].default_value - 0.04) < 0.01

bpy.ops.wm.save_as_mainfile(filepath=CAND)
shutil.copy2(CAND, LIVE)
print('CAND', CAND)
print('LIVE', LIVE)
