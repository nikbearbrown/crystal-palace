"""CP047 north-end terrace CANDIDATE checks -> checks/cp047_northend_candidate_POST66.txt
usage: blender -b rounds/candidates/sydenham-post66-r10_cp047northend.blend -P scripts/check_cp047_northend_candidate.py"""
import bpy, math, os
from mathutils import Vector
FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp047_northend_candidate_POST66.txt')
CP048_CAND = os.path.join(HERE, '..', 'rounds', 'candidates', 'sydenham-post66-r10_cp048terrace.blend')   # approved CP048 layout (= live r10_cp048terrace round)
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
ST = 'SY68_north_end_terrace_walk_bedding_visitors__summer1868'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP047_north_end_35mm']; c48 = bpy.data.objects['CAM_CP048_terrace_hold_35mm']
# base values read from rounds/sydenham-post66-r10.blend @972145e (md5 ed31acf2), 2026-11-18
B47 = (Vector((85.34400177001953, -99.66960144042969, -5.588098526000977)), (1.7484548091888428, 3.168012341348003e-08, -1.1047985553741455))
B48 = (Vector((122.8239974975586, -95.40239715576172, -5.588098526000977)), (1.718343734741211, 1.453138622764527e-07, -1.1425179243087769))
B_NOBJ, B_HIDDEN = 295, 1
chk('hero camera CAM_CP047_north_end_35mm not moved (position)', (cam.location - B47[0]).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B47[1])), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('CAM_CP048_terrace_hold_35mm not moved either', (c48.location - B48[0]).length + sum(abs(a - b) for a, b in zip(c48.rotation_euler, B48[1])), 0.0, 1e-4)
chk('exposure unchanged in the blend (Filmic -1.0 EV; the look v1.1 recipe overrides to -0.8 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
w = bpy.data.objects['cp048_front_walk_48ft']; xs = [(w.matrix_world @ v.co) for v in w.data.vertices]
chk("front walk breadth (1854 Guide / c.1853 report: terrace walk '48 ft broad')", (max(v.y for v in xs) - min(v.y for v in xs)) / FT, 48.0, 0.05, 'ft')
gz = bpy.data.objects['terrace_gravel']; ZG = max((gz.matrix_world @ Vector(v)).z for v in gz.bound_box)
chk('new surfaces sit on the model terrace (front walk above gravel top)', min(v.z for v in xs) - ZG, 0.012, 0.002, 'm')
cw = bpy.data.objects['cp048_cross_walks_12ft']; me = cw.data
f0 = me.polygons[0]; vx = [(cw.matrix_world @ me.vertices[i].co).x for i in f0.vertices]
chk('cross walk breadth (12 ft, I; D-SY-CP048-04)', (max(vx) - min(vx)) / FT, 12.0, 0.05, 'ft')
# the CP048 part must be the approved CP048 layout, object for object
n48 = [o for o in col.objects if o.name.startswith('cp048_')]
with bpy.data.libraries.load(CP048_CAND, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith('cp048_')]
app = {}
for o in dst.objects:
    if o is None: continue
    app[o.name.rsplit('.', 1)[0] if o.name.rsplit('.', 1)[-1].isdigit() else o.name] = o
same = 0; maxd = 0.0
for o in n48:
    t = app.get(o.name)
    if t is None or len(t.data.vertices) != len(o.data.vertices): continue
    d = max([(a.co - b.co).length for a, b in zip(o.data.vertices, t.data.vertices)] or [0.0])
    d = max(d, (o.location - t.location).length, (Vector(o.rotation_euler) - Vector(t.rotation_euler)).length, (o.scale - t.scale).length)
    maxd = max(maxd, d); same += d < 1e-5
chk('CP048-layout objects identical to the approved CP048 candidate (count, mesh verts, location / rotation / scale)', same, len(app), 0, 'objects')
chk('  ... and the count matches the approved 61', len(n48), 61, 0, 'objects')
info(f'max vertex / transform offset vs the approved CP048 layout {maxd:.2e} m')
for o in dst.objects:
    if o: bpy.data.objects.remove(o)
p47 = [o for o in col.objects if o.name.startswith('cp047_visitor_')]
pall = [o for o in col.objects if '_visitor_' in o.name]
d47 = min((o.location.to_2d() - cam.location.to_2d()).length for o in pall)
ge('nearest new figure to the CP047 lens >= 19 m', d47, 19.0, 'm')
F48 = (c48.matrix_world.to_3x3() @ Vector((0, 0, -1))).to_2d().normalized()
bad = [o.name for o in p47 if (o.location.to_2d() - c48.location.to_2d()).dot(F48) >= 0 and (o.location.to_2d() - c48.location.to_2d()).length < 14.0]
chk('CP047-only figures behind or >= 14 m in front of the CP048 lens', len(bad), 0, 0, 'figures')
ad = [o.dimensions.z for o in p47 if 'boy' not in o.name and 'girl' not in o.name]
info(f'people_lib 1850s visitors: {len(p47)} CP047-only + {len(pall) - len(p47)} from the CP048 layout; CP047-only heights {min(o.dimensions.z for o in p47):.2f}-{max(o.dimensions.z for o in p47):.2f} m incl. hats/children')
nd = sum(1 for o in col.all_objects if o.get('cp_state') == ST)
chk('every new object carries the dated state', nd, len(col.all_objects), 0, 'objects')
chk('new objects = base 295 + collection only', len(bpy.data.objects), B_NOBJ + len(col.all_objects), 0, 'objects')
chk('one dated collection (no leftover CP048 collection name)', 1 if bpy.data.collections.get('SY68_upper_terrace_north_walk_bedding_visitors__summer1868') is None else 0, 1, 0)
inside = all(19.9 <= (o.matrix_world @ Vector(c)).x <= 255.3 and -101.8 <= (o.matrix_world @ Vector(c)).y <= -48.0
             for o in col.all_objects for c in o.bound_box)
chk('all new geometry inside the north half of the upper terrace (x 20..255.2 m, y -101.75..-48.1 m)', 1 if inside else 0, 1, 0)
chk('nothing hidden by the candidate (hide_render count = base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0, 'objects')
for nm in ('wings_glass', 'water_tower_north', 'terrace_gravel', 'basement_brick', 'glazed_walls', 'facade_ironwork'):
    o = bpy.data.objects.get(nm)
    if o: chk(f'base object {nm} still rendered', 0 if o.hide_render else 1, 1, 0)
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
info(f'dated collection {col.name} ({len(col.all_objects)} objects) under {[c.name for c in bpy.data.collections if col.name in [k.name for k in c.children]]}')
dep('the summer-1868 terrace layout is the approved CP048 design reproduced unchanged (D-SY-CP048-02..10 apply: turf laid flat, ribbon pattern / vases I)')
dep('CP047-only visitors in people_lib 1850s dress for c.1868 I; numbers and positions I; nearest 19.8 m, none in the near foreground')
dep('dressing confined to the north half of the upper terrace (x 20..255 m), as CP048; south half keeps the base gravel (visible from ext_elevated_overview / plan_overlay_top)')
L.insert(0, f'CP047 north-end terrace candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
