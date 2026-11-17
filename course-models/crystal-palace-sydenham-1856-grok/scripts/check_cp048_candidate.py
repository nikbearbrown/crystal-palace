"""CP048 upper-terrace north walk CANDIDATE checks -> checks/cp048_terrace_candidate_POST66.txt
usage: blender -b rounds/candidates/sydenham-post66-r10_cp048terrace.blend -P scripts/check_cp048_candidate.py"""
import bpy, math, os
from mathutils import Vector
FT = 0.3048
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'checks', 'cp048_terrace_candidate_POST66.txt')
L = []; npass = nfail = 0
def chk(name, model, src, tol, unit=''):
    global npass, nfail
    ok = abs(model - src) <= tol; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.3f} {unit} vs source {src} {unit} (tol {tol})")
def ge(name, model, src, unit=''):
    global npass, nfail
    ok = model >= src; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.2f} {unit} vs source >= {src} {unit}")
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY68_upper_terrace_north_walk_bedding_visitors__summer1868'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP048_terrace_hold_35mm']
# base values read from rounds/sydenham-post66-r10.blend @972145e (md5 ed31acf2), 2026-11-17
B_LOC = Vector((122.8239974975586, -95.40239715576172, -5.588098526000977)); B_ROT = (1.718343734741211, 1.453138622764527e-07, -1.1425179243087769)
chk('camera not moved (position)', (cam.location - B_LOC).length, 0.0, 1e-4, 'm')
chk('camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; the look v1.1 recipe overrides to -0.8 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
w = bpy.data.objects['cp048_front_walk_48ft']; xs = [(w.matrix_world @ v.co) for v in w.data.vertices]
chk("front walk breadth (1854 Guide / c.1853 report: terrace walk '48 ft broad')", (max(v.y for v in xs) - min(v.y for v in xs)) / FT, 48.0, 0.05, 'ft')
gz = bpy.data.objects['terrace_gravel']; ZG = max((gz.matrix_world @ Vector(v)).z for v in gz.bound_box)
chk('new surfaces sit on the model terrace (front walk above gravel top)', min(v.z for v in xs) - ZG, 0.012, 0.002, 'm')
ppl = [o for o in col.objects if o.name.startswith('cp048_visitor_')]
d = min((o.location - cam.location).length for o in ppl)
ge('nearest new figure to the hero lens >= 8 m', d, 8.0, 'm')
hs = [o.dimensions.z for o in ppl if 'boy' not in o.name and 'girl' not in o.name]
info(f'people_lib v3.4 1850s visitors {len(ppl)}; nearest {d:.1f} m; heights {min(o.dimensions.z for o in ppl):.2f}-{max(o.dimensions.z for o in ppl):.2f} m incl. hats/children')
nd = sum(1 for o in col.all_objects if o.get('cp_state') == ST)
chk('every new object carries the dated state', nd, len(col.all_objects), 0, 'objects')
inside = all(19.9 <= (o.matrix_world @ Vector(c)).x <= 255.3 and -101.8 <= (o.matrix_world @ Vector(c)).y <= -48.0
             for o in col.all_objects for c in o.bound_box)
chk('all new geometry inside the north half of the upper terrace (x 20..255.2 m, y -101.75..-48.1 m)', 1 if inside else 0, 1, 0)
hid = [o.name for o in bpy.data.objects if o.get('cp048_hidden_by_candidate')]
chk('nothing hidden or deleted by the candidate', len(hid), 0, 0, 'objects')
for nm in ('frame_main', 'wings_glass', 'water_tower_north', 'terrace_gravel', 'basement_brick'):
    o = bpy.data.objects.get(nm)
    if o: chk(f'base object {nm} still rendered', 0 if o.hide_render else 1, 1, 0)
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
info(f'dated collection {col.name} ({len(col.all_objects)} objects) under SY-POST66_c1868; beds {len([o for o in col.objects if o.name.startswith("cp048_bedding_")])} bedding objects, vases in cp048_tazza_vases')
dep('turf band + bed panels laid flat on the model terrace (source: 50 ft grass slope below the walk; model terrace 171 ft deep, D-SY-CP033-10 kept) I')
dep('ribbon bedding pattern (blue edge / yellow band / scarlet centre), plants and colours I; massed bedding on the terraces R in general')
dep('tazza vases on pedestals at the panel corners I (forms and spacing not traced from a source)')
dep('visitors in people_lib 1850s dress for c.1868 I (crinoline-era silhouettes still worn); numbers and positions I')
dep('dressing confined to the north half of the upper terrace (x 20..255 m); the south half keeps the base gravel (scope of the CP048 shot)')
L.insert(0, f'CP048 upper-terrace north walk candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
