"""CP057 interwar-visitors CANDIDATE checks -> checks/cp057_visitors_candidate_1936.txt
usage: blender -b rounds/candidates/sydenham-1936-r11_cp057visitors.blend -P scripts/check_cp057_visitors_candidate.py"""
import bpy, math, os
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp057_visitors_candidate_1936.txt')
L = []; npass = nfail = 0
def ok_(name, cond, detail=''):
    global npass, nfail
    npass += bool(cond); nfail += (not cond); L.append(f"{'PASS' if cond else 'FAIL'} {name}{': ' + detail if detail else ''}")
def chk(name, model, src, tol, unit=''):
    ok_(name, abs(model - src) <= tol, f'model {model:.3f} {unit} vs source {src} {unit} (tol {tol})')
def rng_(name, model, lo, hi, unit=''):
    ok_(name, lo <= model <= hi, f'model {model:.3f} {unit} vs source range {lo}..{hi} {unit}')
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY36_lower_terrace_interwar_visitors__summer1936'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP057_1936_lower_terrace_35mm']; C = cam.location
# base values read from rounds/sydenham-1936-r11.blend (md5 40140697), 2026-11-18
B_LOC = Vector((100.58399963378906, -185.0135955810547, -11.684098243713379)); B_ROT = (1.7546972036361694, -5.479287423781898e-08, 0.7459310293197632)
B_NOBJ, B_HIDDEN = 306, 1
chk('hero camera CAM_CP057_1936_lower_terrace_35mm not moved (position)', (C - B_LOC).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 35.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; the look v1.1 recipe overrides to -0.8 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
objs = list(col.all_objects)
chk('ONE dated collection holds every new object (base 306 objects + collection)', len(bpy.data.objects), B_NOBJ + len(objs), 0)
chk('nothing hidden / unhidden (hide_render count as base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0)
ok_('collection is dated and tagged', col.get('cp_state') == ST and '1936' in ST and bool(col.get('evidence')))
ok_('every new object carries cp_state = the dated state', all(o.get('cp_state') == ST for o in objs), f'{len(objs)} objects')
newm = [m for m in bpy.data.materials if m.name.startswith('cp057_')]
ok_('every cp057_ material carries cp_state', all(m.get('cp_state') == ST for m in newm), f'{len(newm)} materials')
ok_('no Hyde Park / 1851 collection or object mixed in', not any(('HP' in c.name or 'Hyde' in c.name or '1851' in c.name) for c in bpy.data.collections))
ppl = [o for o in objs if o.get('cpl_people')]; skirts = [o for o in objs if o.name.endswith('_skirt')]
chairs = [o for o in objs if o.name.startswith('cp057_deckchair_') and o.name.endswith('_frame')]
info(f'{len(ppl)} people_lib 1930s figures, {len(skirts)} added skirts, {len(chairs)} deck chairs')
period_bad = [o.name for o in ppl for s in o.material_slots if s.material and any(k in s.material.name for k in ('CPL3_bonnet', 'CPL3_skirt_', 'crinoline'))]
ok_('all visitors in 1930s dress (no 1850s bonnet/crinoline/skirt materials)', not period_bad, f'{len(period_bad)} offenders')
d = [math.hypot(o.location.x - C.x, o.location.y - C.y) for o in ppl]
ok_('nearest new figure >= 28 m from the lens (no figure dominates the foreground)', min(d) >= 28.0, f'{min(d):.2f} m')
dc = [math.hypot(o.location.x - C.x, o.location.y - C.y) for o in chairs]
ok_('deck chairs >= 22 m from the lens (the two near clusters are empty)', min(dc) >= 22.0, f'{min(dc):.2f} m')
near_ch = [o for o in chairs if math.hypot(o.location.x - C.x, o.location.y - C.y) < 28.0]
ok_('chairs nearer than 28 m are unoccupied (no figure within 1.5 m of them)', all(min(math.hypot(p.location.x - c.location.x, p.location.y - c.location.y) for p in ppl) > 1.5 for c in near_ch), f'{len(near_ch)} near chairs')
stand = [o for o in ppl if o.dimensions.z > 1.5]   # seated figures are 1.16-1.43 m tall (legs forward)
rng_('standing adult heights min (1930s adults ~1.50-1.85 m)', min(o.dimensions.z for o in stand), 1.45, 1.90, 'm')
rng_('standing adult heights max', max(o.dimensions.z for o in stand), 1.45, 1.90, 'm')
fr = bpy.data.objects[chairs[0].name]; xs = [v.co.x for v in fr.data.vertices]; zs = [v.co.z for v in fr.data.vertices]
rng_('deck chair frame width (folding deck chair c. 22-26 in, I)', (max(xs) - min(xs)) / 0.0254, 22.0, 26.0, 'in')
rng_('deck chair top-bar height (c. 36-40 in, I)', max(zs) / 0.0254, 35.0, 40.0, 'in')
hz = [min(v.co.z for v in s.data.vertices) for s in skirts]
rng_('1930s day-dress hem above ground (mid-calf, c. 10-14 in)', min(hz) / 0.0254, 9.0, 15.0, 'in')
rng_('hem above ground, tallest woman', max(hz) / 0.0254, 9.0, 15.0, 'in')
# ground under every standing figure is lawn / walk / bank (not the dry basin, not the steps)
for o in bpy.data.objects: o['_hv'] = o.hide_viewport; o.hide_viewport = o.hide_render or (o.name in col.all_objects)
dg = bpy.context.evaluated_depsgraph_get(); bad = []
for o in ppl:
    hit, loc, nor, idx, ob, _ = sc.ray_cast(dg, Vector((o.location.x, o.location.y, 60)), Vector((0, 0, -1)))
    if not hit or ob.name not in ('terrain', 'park_paths_gravel', 'terrace_gravel') or abs(loc.z - o.location.z) > 0.2: bad.append(o.name)
ok_('every figure stands/sits on lawn, walk or bank turf (not in the basin, within 0.2 m of the surface)', not bad, f'{len(bad)} offenders {bad[:4]}')
for o in bpy.data.objects: o.hide_viewport = o['_hv']; del o['_hv']
dep('D-SY-CP057-02 people_lib 1930s figures are low-poly stand-ins; summer recolour of the coat/bodice slots (frock / suit colours I)')
dep('D-SY-CP057-04 skirts are simple elliptical frustums parented to each standing/walking woman (the library shell reads as trousers)')
dep('D-SY-CP057-06 seated figures on the bank use the library seated pose (legs straight forward); torso does not recline in deck chairs')
L.insert(0, f'CP057 interwar visitors CANDIDATE checks ({npass} PASS, {nfail} FAIL) - {bpy.data.filepath}')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
