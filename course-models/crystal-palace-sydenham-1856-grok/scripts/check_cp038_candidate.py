"""CP038 Egyptian Court lion-avenue CANDIDATE checks -> checks/cp038_lions_candidate_EARLY.txt
usage: blender -b rounds/candidates/sydenham-1856-r08_cp038lions.blend -P scripts/check_cp038_candidate.py"""
import bpy, math, os
from mathutils import Vector
F = 0.3048
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'checks', 'cp038_lions_candidate_EARLY.txt')
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
def wbb(o):
    ps = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p[i] for p in ps) / F for i in range(3)], [max(p[i] for p in ps) / F for i in range(3)]
def wverts(o): return [o.matrix_world @ v.co for v in o.data.vertices]
ST = 'SY54_egyptian_outer_court_lion_avenue__1854_1856'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP038_egyptian_hold_28mm']
# base values read from rounds/sydenham-1856-r08.blend (md5 0aa6e9ce), 2026-11-17
B_LOC = Vector((73.30439758300781, 20.935199737548828, 1.600000023841858)); B_ROT = (1.6600691080093384, -2.920267139217003e-09, 0.06514463573694229)
chk('camera not moved (position)', (cam.location - B_LOC).length, 0.0, 1e-4, 'm')
chk('camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('camera lens', cam.data.lens, 28.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; look v1.1 recipe sets -1.2 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
chk('world unchanged (sky)', 1 if (sc.world and sc.world.name == 'sky') else 0, 1, 0)
base_n = 292
chk('base objects all present (292 in r08) + new', len([o for o in bpy.data.objects if o.name not in col.all_objects]), base_n, 0, 'objects')
chk('nothing hidden (r08 has 1 hide_render object)', sum(1 for o in bpy.data.objects if o.hide_render), 1, 0, 'objects')
# lions: BM EA2 115 cm H x 216 cm L x 99 cm W
lion = bpy.data.objects['cp038_prudhoe_lion_casts_x6']
vs = wverts(lion); pl = bpy.data.objects['cp038_lion_plinths_sandstone']; zpl = max(v.z for v in wverts(pl)) / F
groups = {}
for v in vs: groups.setdefault((v.x / F > 241.81, min((82.0, 91.5, 101.0), key=lambda yc: abs(v.y / F - yc))), []).append(v)
nl = 0; Ls = []; Ws = []; Hs = []
for k, g in groups.items():
    nl += 1; Ls.append((max(v.y for v in g) - min(v.y for v in g)) / F); Ws.append((max(v.x for v in g) - min(v.x for v in g)) / F); Hs.append(max(v.z for v in g) / F - zpl)
chk('lion casts', nl, 6, 0, 'lions')
chk('lion length incl. base (BM EA2 216 cm = 7.09 ft)', max(Ls), 7.09, 0.15, 'ft')
chk('lion width incl. base (BM EA2 99 cm = 3.25 ft)', max(Ws), 3.25, 0.15, 'ft')
chk('lion height incl. base (BM EA2 115 cm = 3.77 ft)', max(Hs), 3.77, 0.20, 'ft')
info(f'lion L {min(Ls):.2f}-{max(Ls):.2f} ft, W {min(Ws):.2f}-{max(Ws):.2f} ft, H above plinth {min(Hs):.2f}-{max(Hs):.2f} ft; plinth top {zpl:.2f} ft')
lo, hi = wbb(lion); floor_top = 0.12
chk('lion bases sit on the plinth tops (min z = plinth top)', lo[2], zpl, 0.01, 'ft')
plo, phi = wbb(pl)
chk('plinths sit on the court floor (eg_floor top 0.12 ft)', plo[2], floor_top, 0.01, 'ft')
ge('plinths clear of the portico screen face (110.71 ft)', 110.71 - phi[1], 2.0, 'ft')
ge('plinths clear of the nave front wall (61.0 ft)', plo[1] - 61.0, 2.0, 'ft')
wk = bpy.data.objects['cp038_avenue_walk_flags']; wlo, whi = wbb(wk)
chk('walk width (I, 10 ft)', whi[0] - wlo[0], 10.0, 0.01, 'ft')
chk('walk on the bay axis (KX[3..4] centre 241.81 ft)', (whi[0] + wlo[0]) / 2, 241.81, 0.02, 'ft')
chk('walk reaches the portico face (gap)', 110.71 - whi[1], 0.05, 0.02, 'ft')
chk('walk sits on the floor', wlo[2], floor_top, 0.005, 'ft')
# inner gap between the plinth rows must hold the walk
xs_in = sorted(set(round(v.x / F, 2) for v in wverts(pl)))
inner_l = max(x for x in xs_in if x < 241.81); inner_r = min(x for x in xs_in if x > 241.81)
ge('clear avenue between plinth feet >= walk width', inner_r - inner_l, 10.0, 'ft')
# winged globe attached to the architrave over the centre bay
gl = [o for o in col.objects if o.name.startswith('cp038_winged_globe')]
glo = [min(wbb(o)[0][i] for o in gl) for i in range(3)]; ghi = [max(wbb(o)[1][i] for o in gl) for i in range(3)]
chk('winged globe centred on the open centre bay', (glo[0] + ghi[0]) / 2, 241.81, 0.05, 'ft')
ge('winged globe within the architrave band (z >= 17.6 ft)', glo[2], 17.6, 'ft')
ge('winged globe within the architrave band (19.4 - top >= 0)', 19.4 - ghi[2], 0.0, 'ft')
chk('winged globe attached to the architrave face (110.11 ft): back face within +-0.06 ft (negative = keyed in)', 110.11 - ghi[1], 0.0, 0.06, 'ft')
info(f'winged globe span {ghi[0]-glo[0]:.2f} ft, height {ghi[2]-glo[2]:.2f} ft (form I)')
# relief panels on the six screen walls
pn = [o for o in col.objects if o.name.startswith('cp038_portico_relief_panel_')]
chk('relief panels on the portico screen walls', len(pn), 6, 0, 'panels')
gaps = [110.71 - wbb(o)[1][1] for o in pn]
chk('relief panels flush on the screen face (gap)', max(gaps), 0.03, 0.005, 'ft')
ge('relief panels below the screen coping (7.5 ft)', 7.5 - max(wbb(o)[1][2] for o in pn), 0.0, 'ft')
ppl = [o for o in col.objects if o.name.startswith('cp038_visitor_')]
d = min((o.location - cam.location).length for o in ppl)
ge('nearest new figure to the hero lens >= 7.5 m', d, 7.5, 'm')
info(f'people_lib v3.4 1850s visitors {len(ppl)}; nearest {d:.1f} m')
nd = sum(1 for o in col.all_objects if o.get('cp_state') == ST)
chk('every new object carries the dated state', nd, len(col.all_objects), 0, 'objects')
inside = all(180 <= v <= 276 for o in col.all_objects for v in (wbb(o)[0][0], wbb(o)[1][0])) and all(60 <= wbb(o)[0][1] and wbb(o)[1][1] <= 111.6 for o in col.all_objects)
chk('all new geometry inside the Egyptian Court outer court (x 180..276, y 60..111.6 ft)', 1 if inside else 0, 1, 0)
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
imgs = [i.name for i in bpy.data.images if i.source == 'FILE' and not i.packed_file and any(u for u in [i.users])]
info(f'new materials procedural only; external unpacked images in file: {len(imgs)} (pre-existing)')
info(f'dated collection {col.name} ({len(col.all_objects)} objects) under {[c.name for c in bpy.data.collections if col.name in [k.name for k in c.children]]}')
dep('avenue laid inside the model outer court on the axis of the portico open centre bay (sources: avenue on the approach from the nave to the Ptolemaic portico; the r08 model puts that portico at the lower facade of the Hall of Columns) I')
dep('3 pairs of lions (count not in the sources) on 1.35 ft painted sandstone pedestals I; casts coloured red granite I/U')
dep('lion heads frontal toward the nave; EA1/EA2 have the head turned (BM) - simplified for readability I; form a smooth stand-in, not a scan')
dep('relief drawing (king with offering bowl before a blue Amun with was-sceptre and plumes, glyph column, starred sky band) generic, not traced from the Sydenham walls U; subject R (Phillips 1854)')
dep('winged globe with two uraei: form/colours I; position over the main entrance R (Wyatt 1854)')
dep('10 ft flagged walk I; 1850s visitors (5) positions I')
L.insert(0, f'CP038 Egyptian Court lion-avenue candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
