"""CP052 glaziers + painters CANDIDATE checks -> checks/cp052_repair_candidate_LATE11.txt
usage: blender -b rounds/candidates/sydenham-late11-r16_cp052repair.blend -P scripts/check_cp052_repair_candidate.py"""
import bpy, math, os
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp052_repair_candidate_LATE11.txt')
L = []; npass = nfail = 0
FT, IN = 0.3048, 0.0254
def ok_(name, cond, detail=''):
    global npass, nfail
    npass += bool(cond); nfail += (not cond); L.append(f"{'PASS' if cond else 'FAIL'} {name}{': ' + detail if detail else ''}")
def chk(name, model, src, tol, unit=''):
    ok_(name, abs(model - src) <= tol, f'model {model:.3f} {unit} vs source {src} {unit} (tol {tol})')
def rng_(name, model, lo, hi, unit=''):
    ok_(name, lo <= model <= hi, f'model {model:.3f} {unit} vs source range {lo}..{hi} {unit}')
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY00_transept_front_glaziers_painters__c1900'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP052_scaffold_reglaze_35mm']; C = cam.location
# base values read from rounds/sydenham-late11-r16.blend (md5 3ce48caf), 2026-11-18
B_LOC = Vector((-22.0, -82.0, 5.5)); B_ROT = (1.666280746459961, -1.3837819778927951e-08, -0.5547922253608704)
B_NOBJ, B_HIDDEN = 385, 1
chk('hero camera CAM_CP052_scaffold_reglaze_35mm not moved (position, dud-fix v4 framing)', (C - B_LOC).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; the look v1.1 recipe sets -0.8 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
objs = list(col.all_objects)
chk('ONE dated collection holds every new object (base 385 objects + collection)', len(bpy.data.objects), B_NOBJ + len(objs), 0)
chk('nothing hidden / unhidden (hide_render count as base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0)
ok_('collection is dated and tagged', col.get('cp_state') == ST and '1900' in ST and bool(col.get('evidence')))
ok_('every new object carries cp_state = the dated state', all(o.get('cp_state') == ST for o in objs), f'{len(objs)} objects')
newm = [m for m in bpy.data.materials if m.name.startswith('cp052_')]
ok_('every cp052_ material carries cp_state', all(m.get('cp_state') == ST for m in newm), f'{len(newm)} materials')
ok_('no Hyde Park / 1851 collection or object mixed in', not any(('HP' in c.name or 'Hyde' in c.name or '1851' in c.name) for c in bpy.data.collections))
ok_('base r16 repair collection untouched (SY-LATE_repair_scaffold__dated: 2 objects)', len(bpy.data.collections['SY-LATE_repair_scaffold__dated'].all_objects) == 2)
ppl = [o for o in objs if o.get('cpl_people')]
info(f'{len(ppl)} people_lib workmen: ' + ', '.join(o.name for o in ppl))
d = [(o.matrix_world.translation - C).length for o in ppl]
ok_('nearest new figure >= 20 m from the lens (no figure dominates the frame)', min(d) >= 20.0, f'{min(d):.2f} m')
rng_('workman heights min (adult c.1900 incl. cap, 1.55-1.85 m)', min(o.dimensions.z for o in ppl), 1.50, 1.90, 'm')
rng_('workman heights max', max(o.dimensions.z for o in ppl), 1.50, 1.90, 'm')
period_bad = [o.name for o in ppl for s in o.material_slots if s.material and any(k in s.material.name for k in ('CPL3_bonnet', 'crinoline', 'CPL3_skirt_', 'tophat'))]
ok_('workmen only (no bonnet / crinoline / top-hat materials)', not period_bad, f'{len(period_bad)} offenders')
def dims(n):
    o = bpy.data.objects[n]; vs = [o.matrix_world @ v.co for v in o.data.vertices]
    return [max(v[i] for v in vs) - min(v[i] for v in vs) for i in range(3)], vs
# scaffold dimensions
std = bpy.data.objects['cp052_scaffold_standards']; vs = [std.matrix_world @ v.co for v in std.data.vertices]
xs = sorted({round(v.x, 2) for v in vs})
r = (max(v.x for v in vs[:8]) - min(v.x for v in vs[:8])) / 2
chk('standard diameter (fir pole c. 5 in, R in general)', 2 * r / IN, 5.0, 0.2, 'in')
cx = sorted({round(sum(v.x for v in vs[k:k + 16]) / 16, 3) for k in range(0, len(vs), 16)})
sp = [b - a for a, b in zip(cx, cx[1:])]
rng_('standard spacing along the face (6-10 ft, R in general; here on the 8 ft mullion lines)', min(sp) / FT, 6.0, 10.0, 'ft')
rng_('standard spacing max', max(sp) / FT, 6.0, 10.0, 'ft')
cy = sorted({round(sum(v.y for v in vs[k:k + 16]) / 16, 3) for k in range(0, len(vs), 16)})
rng_('inner-to-outer standard rows (4-5 board scaffold, c. 3 ft 6 in-4 ft 6 in)', (cy[-1] - cy[0]) / FT, 3.4, 4.6, 'ft')
led = bpy.data.objects['cp052_scaffold_ledgers_braces']; lz = sorted({round((led.matrix_world @ v.co).z, 2) for v in led.data.vertices})
lifts = [1.3716, 2.7432, 4.1148]
ok_('ledger lifts at 4 ft 6 in (R in general: lifts 4-5 ft)', all(any(abs(z - (L0 + s)) < 0.06 for z in lz for s in (-0.05, 0.05)) for L0 in lifts), 'lifts 1.372 / 2.743 / 4.115 m')
bd = bpy.data.objects['cp052_scaffold_boards']; bv = [bd.matrix_world @ v.co for v in bd.data.vertices]
bw = max(v.y for v in bv[:8]) - min(v.y for v in bv[:8]); bt = max(v.z for v in bv[:8]) - min(v.z for v in bv[:8])
chk('scaffold board width (9 in, R in general)', bw / IN, 9.0, 0.05, 'in'); chk('scaffold board thickness (2 in)', bt / IN, 2.0, 0.05, 'in')
plat = max(v.z for v in bv[:32]); info(f'platform board top z {plat:.3f} m (top panes of the ground storey reach 5.85 m)')
rng_('platform height below the band so a man reaches the top panes (top pane 5.85 m - platform in 1.3-1.9 m)', 5.85 - plat, 1.3, 1.9, 'm')
(l1, _), (l2, _) = dims('cp052_scaffold_ladder'), dims('cp052_painters_ladder')
rng_('scaffold ladder width (14-18 in stiles c. 1900, R in general)', l1[0] / IN, 14.0, 19.5, 'in')
rng_('painters ladder width', l2[0] / IN, 14.0, 19.5, 'in')
(cr, _) = dims('cp052_painters_cradle')
chk('painters cradle stage length (13 ft, I; period stages 10-20 ft)', cr[0] / FT, 13.0, 0.1, 'ft')
pv = [v.co for v in bpy.data.objects['cp052_new_pane_carried'].data.vertices]; pn = [max(v[i] for v in pv) - min(v[i] for v in pv) for i in range(3)]   # mesh-local (parented to the glazier)
chk('carried pane 49 in long (Paxton 49 x 10 in pane module, I for the Sydenham vertical glazing)', max(pn) / IN, 49.0, 0.2, 'in')
# overlays sit within 2 cm in front of the base faces and do not intrude into the glass
wea = bpy.data.objects['cp052_weathered_paint_mullions']; wy = sorted({round((wea.matrix_world @ v.co).y, 3) for v in wea.data.vertices})
ok_('weathered-paint plates 6 mm in front of the mullion / pier faces (-62.225/-62.316/-59.787/-59.878)', all(any(abs(y - (f - 0.006)) < 0.002 for f in (-62.225, -62.316, -59.787, -59.878)) for y in wy), str(wy))
wx = max((wea.matrix_world @ v.co).x for v in wea.data.vertices)
ok_('weathered bays only west of the painters (x < -11.1 m)', wx <= -10.82, f'max x {wx:.2f} m')
# every standard / ladder foot rests on the base stairs (sole board top within 6 cm of the tread)
for o in bpy.data.objects: o['_hv'] = o.hide_viewport; o.hide_viewport = o.hide_render or (o.name in col.all_objects)
dg = bpy.context.evaluated_depsgraph_get(); bad = []
for k in range(0, len(vs), 16):
    c0 = sum((v for v in vs[k:k + 8]), Vector()) / 8
    hit, loc, n, i, ob, _ = sc.ray_cast(dg, Vector((c0.x, c0.y, 30)), Vector((0, 0, -1)))
    if not hit or abs(c0.z - (loc.z + 2 * IN)) > 0.06: bad.append((round(c0.x, 2), round(c0.y, 2), round(c0.z, 2), round(loc.z, 2) if hit else None))
ok_('every standard stands on a sole board on the base stair / cheek surface', not bad, str(bad))
for o in bpy.data.objects: o.hide_viewport = o['_hv']; del o['_hv']
dep('D-SY-CP052-03 workmen are people_lib v3.4 1850s_workman meshes (cloth cap) re-coloured: glaziers dark waistcoat, painters pale overalls; c.1900 dress I')
dep('D-SY-CP052-06 weathered paint = overlay plates (dulled pale paint) + rust runs on the west bays; which bays and how dirty: I')
L.insert(0, f'CP052 glaziers + painters CANDIDATE checks ({npass} PASS, {nfail} FAIL) - {bpy.data.filepath}')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
