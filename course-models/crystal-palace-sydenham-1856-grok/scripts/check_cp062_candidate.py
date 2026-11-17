"""CP062 morning-after CANDIDATE checks -> checks/cp062_morning_candidate_RUINS.txt
usage: blender -b rounds/candidates/sydenham-ruins-r17_cp062morning.blend -P scripts/check_cp062_candidate.py"""
import bpy, math, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp062_morning_candidate_RUINS.txt')
L = []; npass = nfail = 0
def chk(name, model, src, tol, unit=''):
    global npass, nfail
    ok = abs(model - src) <= tol; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.3f} {unit} vs source {src} {unit} (tol {tol})")
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY36-AFTER_1Dec1936_morning'; CN = 'SY36_morning_after_smoke_wreck__1Dec1936'
sc = bpy.context.scene; col = bpy.data.collections[CN]
cam = bpy.data.objects['CAM_CP062_morning_between_towers_35mm']
# base values read from rounds/sydenham-ruins-r17.blend (md5 2c3343c6), 2026-11-17
B_LOC = Vector((-200.0, -70.0, 28.0)); B_ROT = (1.7688294649124146, -5.9198015378569835e-08, 0.7440017461776733)
chk('camera not moved (position)', (cam.location - B_LOC).length, 0.0, 1e-4, 'm')
chk('camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('exposure unchanged in the blend (AgX MHC -0.7 EV, saved by the dud-fix v4 look pass; recipe re-applies -0.7 on both sides)', sc.view_settings.exposure, -0.7, 1e-6, 'EV')
chk('view transform / look unchanged (AgX, AgX - Medium High Contrast)', 1 if (sc.view_settings.view_transform, sc.view_settings.look) == ('AgX', 'AgX - Medium High Contrast') else 0, 1, 0)
w = sc.world
chk('world unchanged (sky, 9 nodes)', 1 if (w.name == 'sky' and len(w.node_tree.nodes) == 9) else 0, 1, 0)
sun = bpy.data.objects['sun']
chk('sun unchanged (energy 1.6, rot x 1.0821 z 1.6)', abs(sun.data.energy - 1.6) + abs(sun.rotation_euler.x - 1.0821040868759155) + abs(sun.rotation_euler.z - 1.6), 0.0, 1e-5)
lights = [o for o in bpy.data.objects if o.type == 'LIGHT']
chk('no lights added', len(lights), 1, 0, 'lights')
new = set(o.name for o in col.all_objects)
base = [o for o in bpy.data.objects if o.name not in new]
chk('nothing deleted (base object count)', len(base), 206, 0, 'objects')
chk('nothing hidden (base hide_render count: horizon_haze_r17, horizon_fill_r17, REF plan, as in the base)', sum(1 for o in base if o.hide_render), 3, 0, 'objects')
nd = sum(1 for o in col.all_objects if o.get('cp_state') == ST)
chk('every new object carries the dated state', nd, len(col.all_objects), 0, 'objects')
t = bpy.data.objects['water_tower_south']; tz = max((t.matrix_world @ Vector(c)).z for c in t.bound_box)
chk('South Tower unchanged (lantern top z, model)', tz, 86.563, 0.001, 'm')
m = bpy.data.objects['cp062_after_baird_mast_1933']; mz = max((m.matrix_world @ Vector(c)).z for c in m.bound_box)
chk("Baird mast height above the lantern (repo r11 'lattice mast 50 ft'; HE R existence, U height)", (mz - tz) / FT, 50.0, 1.0, 'ft')
mx = (m.matrix_world @ Vector(m.bound_box[0])); ok = (-289 < mx.x < -274) and (11 < mx.y < 26)
chk('Baird mast sits on the South Tower', 1 if ok else 0, 1, 0)
smoke = [o for o in col.objects if o.name.startswith('cp062_smoke_')]
srcs = {}
for o in smoke:
    k = o.name.split('_')[2]
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
    if k not in srcs or c.z < srcs[k].z: srcs[k] = c
inside = all(-246 <= c.x <= -150 and -48.5 <= c.y <= 48.5 for c in srcs.values())
chk('every smoke plume rises from the burnt-out south end of the footprint (x -246..-150, y +-48.3 m)', 1 if inside else 0, 1, 0)
def clear_of_tower(o):
    bb = [o.matrix_world @ Vector(b) for b in o.bound_box]
    return max(p.x for p in bb) < -289 or min(p.x for p in bb) > -274 or max(p.y for p in bb) < 11 or min(p.y for p in bb) > 26
chk('no smoke volume intersects the South Tower', sum(0 if clear_of_tower(o) else 1 for o in smoke), 0, 0, 'volumes')
# smoke must not cross the tower in the hero frame: projected centres stay right of the tower's right edge
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
tx = max(world_to_camera_view(sc, cam, t.matrix_world @ Vector(c)).x for c in t.bound_box) * 1280
lefts = []
for o in smoke:
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
    v = world_to_camera_view(sc, cam, c)
    if v.z > 0 and 0 <= v.y <= 1: lefts.append(v.x * 1280)
chk('in-frame smoke puff centres right of the tower silhouette (hero frame, px)', 1 if min(lefts) > tx else 0, 1, 0)
info(f'tower right edge {tx:.0f} px; leftmost in-frame puff centre {min(lefts):.0f} px; {len(lefts)} of {len(smoke)} puffs in frame')
wf = bpy.data.objects['cp062_after_collapsed_ironwork_field']; wz = max((wf.matrix_world @ Vector(c)).z for c in wf.bound_box)
chk('appended wreck field low, as in 0587 (max height above the main floor, AFTER state)', wz, 16.2, 0.1, 'm')
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
info(f'dated collection {CN} ({len(col.all_objects)} objects: {len(smoke)} smoke puffs in {len(srcs)} plumes, 2 haze volumes, 3 appended AFTER-state objects) under SY-RUINS_c1937-40')
info('bottom frame edge at the south end of the footprint is ~18-25 m above the main floor (camera z 28 m, 11 deg up-tilt, 16.1 deg half v-FOV): the wreck field (<= 16.2 m) is state-correct but not seen in the hero; only the lowest ~quarter of the Baird mast shows above the lantern (frame top cuts it)')
dep('smoke drifts NE on the model grid (as the repo FIRE state, wind U); London Walks gives the wind of the night as NW (would carry smoke SE / towards the garden) - morning wind not researched; lean chosen to keep the tower clear I')
dep('smoke volumes are absorption + matched emission (no scattering) so they converge at the live 32 spp; tone/density I (0587 shows pale smoke/steam haze)')
dep('plume count (5), heights (up to ~100 m) and positions on the south end I; that the south end was burnt out R (London Walks: fire blown down through the south-west wing)')
dep('cleared c.1937-40 footing pads / footprint ground of the base round stay under the appended 1 Dec 1936 wreck (below the hero sightline; not hidden)')
dep('Baird mast form/height U (repo r11 stand-in); a short lattice stub above the lantern in the hero, cut by the frame top')
L.insert(0, f'CP062 morning-after candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
