"""CP053 lower-park trees in leaf, summer 1911 CANDIDATE checks -> checks/cp053_trees_candidate_LATE11.txt
usage: blender -b rounds/candidates/sydenham-late11-r14_cp053trees.blend -P scripts/check_cp053_trees_candidate.py"""
import bpy, math, os, ast, sys
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp053_trees_candidate_LATE11.txt')
L = []; npass = nfail = 0
def ok_(name, cond, detail=''):
    global npass, nfail
    npass += bool(cond); nfail += (not cond); L.append(f"{'PASS' if cond else 'FAIL'} {name}{': ' + detail if detail else ''}")
def chk(name, model, src, tol, unit=''):
    ok_(name, abs(model - src) <= tol, f'model {model:.4f} {unit} vs source {src} {unit} (tol {tol})')
def rng_(name, model, lo, hi, unit=''):
    ok_(name, lo <= model <= hi, f'model {model:.3f} {unit} vs source range {lo}..{hi} {unit}')
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY11_lower_park_trees_in_leaf__summer1911'; STATE = 'SY11-LATE_FestivalOfEmpire_summer1911'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP053_empire_pavilions_wide_35mm']; C = cam.location
# base values read from rounds/sydenham-late11-r14.blend (md5 9f90df23), 2026-11-19
B_LOC = Vector((18.288000106811523, -579.1199951171875, -38.06103515625)); B_ROT = (1.724176287651062, 1.8412391611377643e-09, 0.059928156435489655)
B_NOBJ, B_HIDDEN, B_NMAT, B_NNG = 364, 1, 69, 1
chk('hero camera CAM_CP053_empire_pavilions_wide_35mm not moved (position)', (C - B_LOC).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; the live look v1.1 recipe sets its own -0.8 at render time)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
ok_('view transform unchanged (Filmic)', sc.view_settings.view_transform == 'Filmic')
ok_('blend render settings unchanged (1920x1080, 48 spp; live recipe renders 1280x720 24 spp)', (sc.render.resolution_x, sc.render.resolution_y, sc.cycles.samples) == (1920, 1080, 48))
objs = list(col.all_objects)
chk('ONE dated collection holds every new object (base 364 objects + collection)', len(bpy.data.objects), B_NOBJ + len(objs), 0)
chk('nothing hidden / unhidden (hide_render count as base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0)
ok_('collection is dated and tagged', col.get('cp_state') == STATE and '1911' in ST and bool(col.get('evidence')))
ok_('every new object carries cp_state = the dated state', all(o.get('cp_state') == STATE for o in objs), f'{len(objs)} objects: ' + ', '.join(sorted(o.name for o in objs)))
newm = [m for m in bpy.data.materials if m.name.startswith('cp053_')]
ok_('the only new material is cp053_ and tagged', all(m.get('cp_state') == STATE for m in newm) and len(bpy.data.materials) == B_NMAT + len(newm) and len(newm) == 1, f'{len(newm)} material')
ng = bpy.data.node_groups.get('cp053_leaf_sprays')
ok_('the only new node group is the tagged geometry-nodes spray', ng is not None and ng.get('cp_state') == STATE and len(bpy.data.node_groups) == B_NNG + 1)
ok_('Sydenham only: no Hyde Park / 1851 collection or object involved',
    not any(('1851' in x.name or 'Hyde' in x.name or x.name.startswith('HP')) for x in list(bpy.data.collections) + list(bpy.data.objects)))
crowns = [o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_park_tree_') and o.name.endswith('_crown')]
ok_('r03 park placeholder crowns untouched (70 x 720 faces, foliage material, visible)',
    len(crowns) == 70 and all(len(o.data.polygons) == 720 and o.data.materials[0].name == 'foliage' and not o.hide_render for o in crowns))
b = bpy.data.materials['bark']; bc = tuple(round(v, 4) for v in b.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value)
ok_('round bark material reused unedited (2 nodes, 1 link, base colour 0.20/0.15/0.10)', len(b.node_tree.nodes) == 2 and len(b.node_tree.links) == 1 and bc == (0.2, 0.15, 0.1, 1.0))
can = bpy.data.objects['cp053_leaf_canopy']; lim = bpy.data.objects['cp053_limbs']
ok_('canopy = point cloud + geometry-nodes sprays (no faces of its own)', len(can.data.polygons) == 0 and can.modifiers[0].type == 'NODES' and can.modifiers[0].node_group == ng)
ok_('limbs use the round bark material', lim.data.materials[0] == b)
# spray / leaf parameters read from the node group
N = {n.bl_idname: n for n in ng.nodes}
nleaf = ng.nodes['Points'].inputs['Count'].default_value
rs = [n for n in ng.nodes if n.bl_idname == 'FunctionNodeRandomValue' and n.data_type == 'FLOAT' and n.inputs['Seed'].default_value == 13][0]
lmin, lmax = rs.inputs[2].default_value, rs.inputs[3].default_value
rng_('leaf blade length min (broadleaf park trees: lime / plane / sycamore / horse-chestnut leaflet 5-35 cm, I)', lmin * 100, 5, 35, 'cm')
rng_('leaf blade length max', lmax * 100, 5, 35, 'cm')
chk('leaves per twig spray', nleaf, 8, 0)
# per-tree geometry
P = np.array([tuple(v.co) for v in can.data.vertices])
dressed = ast.literal_eval(col['dressed_crowns'])
def in_frame(n):
    o = bpy.data.objects[n]; bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    for p in bb + [sum(bb, Vector()) / 8]:
        v = world_to_camera_view(sc, cam, p)
        if v.z > 0 and -0.12 < v.x < 1.12 and -0.12 < v.y < 1.12: return True
    return False
ok_('every dressed crown is in / near the hero frame (bbox corner or centre within 12 % of the frame)', all(in_frame(n) for n in dressed), f'{len(dressed)} of 70 crowns')
ok_('every park crown in / near the hero frame is dressed', sorted(n for n in (o.name for o in crowns) if in_frame(n)) == sorted(dressed))
TR = {n: (lambda tb: (sum(v.x for v in tb) / 8, sum(v.y for v in tb) / 8, min(v.z for v in tb)))([bpy.data.objects[n.replace('_crown', '_trunk')].matrix_world @ Vector(c) for c in bpy.data.objects[n.replace('_crown', '_trunk')].bound_box]) for n in dressed}
TXY = np.array([[TR[n][0], TR[n][1]] for n in dressed]); own = np.argmin(np.linalg.norm(P[:, None, :2] - TXY[None], axis=2), 1)
hmax = []; lowest = []; spread = []; per_sprays = []
for i, n in enumerate(dressed):
    Q = P[own == i]; tbot = TR[n][2]; per_sprays.append(len(Q))
    hmax.append(float(Q[:, 2].max()) + 0.4 + 0.3 - tbot); lowest.append(float(Q[:, 2].min()) - tbot)
    spread.append(float(max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1]))) + 0.8)
rng_('tallest dressed tree, crown top incl. spray radius + leaf (mature park tree c.55 years after the 1856 planting: 12-30 m, I)', max(hmax), 12, 30, 'm')
rng_('shortest dressed tree', min(hmax), 12, 30, 'm')
rng_('widest crown spread (mature lime / plane / chestnut 8-22 m, I)', max(spread), 8, 22, 'm')
rng_('lowest spray centre above the ground (head-room under the crown >= 3 m)', min(lowest), 3.0, 30, 'm')
ok_('every dressed crown has sprays (>= 5000 each)', min(per_sprays) >= 5000, ', '.join(f'{n[22:-6]}:{k}' for n, k in zip(dressed, per_sprays)))
info(f'sprays {len(P)} -> leaves {len(P) * nleaf}; limbs {len(lim.data.vertices)} verts; dressed {len(dressed)} of {len(crowns)} park crowns')
dep('D-SY-CP053-02 foliage hugs the r03 placeholder crowns (icosphere unions) - crown shape/size I; placeholders stay underneath as the inner mass')
dep('D-SY-CP053-04 only the 16 park crowns in/near the CAM_CP053_empire_pavilions_wide_35mm frame are dressed; the other 54 park placeholders in the round stay bare (seen only from other cameras)')
dep('D-SY-CP053-03 one 8-leaf spray (same leaf layout) instanced at every point with a random rotation / scale - repetition is below pixel size at >= 110 m')
txt = f'CP053 lower-park trees in leaf, summer 1911 CANDIDATE checks ({ST}) - {npass} PASS {nfail} FAIL\n' + '\n'.join(L) + '\n'
open(OUT, 'w').write(txt); print(txt)
