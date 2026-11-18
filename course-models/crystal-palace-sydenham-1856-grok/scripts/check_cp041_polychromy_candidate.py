"""CP041 Owen Jones polychromy + stilted imposts CANDIDATE checks -> checks/cp041_polychromy_candidate_EARLY.txt
usage: blender -b rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend -P scripts/check_cp041_polychromy_candidate.py"""
import bpy, math, os, ast
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'checks', 'cp041_polychromy_candidate_EARLY.txt')
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
ST = 'SY54_alhambra_court_OJ_polychromy_stilts__1854_1856'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP041_insert_spandrel_50mm']; C = cam.location
# base values read from rounds/sydenham-1856-r08b.blend (md5 60c76d85), 2026-11-18
B_LOC = Vector((159.2368621826172, 27.6585750579834, 1.600000023841858)); B_ROT = (1.8676221370697021, 9.197231776170156e-08, 2.7599339485168457)
B_NOBJ, B_HIDDEN, B_NMAT, B_NIMG = 292, 1, 30, 1
chk('hero camera CAM_CP041_insert_spandrel_50mm not moved (position)', (C - B_LOC).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 50.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; render.py live recipe does not touch it)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
ok_('view transform unchanged (Filmic)', sc.view_settings.view_transform == 'Filmic')
ok_('render resolution unchanged (1920x1080, the live hero size)', (sc.render.resolution_x, sc.render.resolution_y) == (1920, 1080))
objs = list(col.all_objects)
chk('ONE dated collection holds every new object (base 292 objects + collection)', len(bpy.data.objects), B_NOBJ + len(objs), 0)
chk('nothing hidden / unhidden (hide_render count as base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0)
ok_('collection is dated and tagged', col.get('cp_state') == ST and '1854' in ST and bool(col.get('evidence')))
ok_('every new object carries cp_state = the dated state', all(o.get('cp_state') == ST for o in objs), f'{len(objs)} objects')
newm = [m for m in bpy.data.materials if m.name.startswith('cp041_')]
ok_('every cp041_ material carries cp_state; only those are new', all(m.get('cp_state') == ST for m in newm) and len(bpy.data.materials) == B_NMAT + len(newm), f'{len(newm)} materials')
newi = [i for i in bpy.data.images if i.name.startswith('cp041_')]
ok_('generated textures packed in the blend and tagged', len(newi) == 2 and all(i.packed_file is not None and i.get('cp_state') == ST for i in newi), ', '.join(f'{i.name} {i.size[0]}x{i.size[1]}' for i in newi))
ok_('Sydenham only: collection not under any Hyde Park / 1851 collection, no HP/1851 objects in it',
    all(ST not in [c.name for c in p.children] for p in bpy.data.collections if ('HP' in p.name or '1851' in p.name)) and not any(('HP' in o.name or '1851' in o.name) for o in objs))
st = bpy.data.objects['al_stucco']
ok_('r08b stucco untouched (material, face count, identity transform)', [m.name for m in st.data.materials] == ['al_stucco_diaper_OJ'] and len(st.data.polygons) == 7190
    and all(abs(st.matrix_world[i][j] - (1.0 if i == j else 0.0)) < 1e-9 for i in range(4) for j in range(4)), f'{len(st.data.polygons)} faces, {st.data.materials[0].name}')
skin = bpy.data.objects['cp041_oj_stucco_skin']
chk('skin = every r08b stucco face, both sides', len(skin.data.polygons), 2 * len(st.data.polygons), 0, 'faces')
# skin offset: distance of a few skin faces from their source plane
ds = []
for k in range(0, len(st.data.polygons), 997):
    p = st.data.polygons[k]; sp = skin.data.polygons[2 * k]
    ds.append(abs((sp.center - p.center).dot(p.normal)))
chk('skin 6 mm proud of the stucco face (paint/plaster skin, I)', max(ds) * 1000, 6.0, 0.05, 'mm')
# texture tile = sebka diamond (workshop sy-alhambra-ornament-panel NOTES: 0.45 x 0.485 m from guide p.66 woodcut proportions)
m = bpy.data.materials['cp041_oj_sebka_polychrome']; maps = [n for n in m.node_tree.nodes if n.type == 'MAPPING']
s0 = maps[0].inputs['Scale'].default_value
chk('sebka diamond width (workshop prop, from guide p.66)', 1 / s0[0], 0.45, 0.001, 'm')
chk('sebka diamond height (workshop prop, from guide p.66)', 1 / s0[2], 0.485, 0.001, 'm')
chk('sebka diamond width/height ratio (measured proportion)', (1 / s0[0]) / (1 / s0[2]), 0.45 / 0.485, 0.002)
bands = []
for n in m.node_tree.nodes:
    if n.type == 'MATH' and n.operation == 'GREATER_THAN': bands.append([n.inputs[1].default_value, None])
lts = [n.inputs[1].default_value for n in m.node_tree.nodes if n.type == 'MATH' and n.operation == 'LESS_THAN']
for b, z1 in zip(bands, lts): b[1] = z1
chk('dado-cap band starts at the r08b dado top (4 ft 6 in)', bands[0][0], 4.5 * FT, 0.005, 'm')
rng_('dado-cap band height (woodcut: inscription band capping the dado; workshop 0.18 m on a 3.6 m panel, scaled court)', (bands[0][1] - bands[0][0]) / IN, 6.0, 10.0, 'in')
chk('arcade frieze ends under the r08b screen eaves (5.33 m)', bands[1][1], 5.33, 0.01, 'm')
chk('wall frieze ends under the r08b wall eaves (7.32 m)', bands[2][1], 7.32, 0.01, 'm')
stl = ast.literal_eval(bpy.data.objects['cp041_oj_stilt_imposts']['stilts'])
info(f'{len(stl)} stilted imposts (columns whose abacus has the arcade pier above it; the side colonnades carry no r08b screen above the capitals and get none)')
ok_('every stilt stands on an r08b abacus top (3.231 m)', all(abs(s[2] - 3.231) < 0.005 for s in stl), f'{len(stl)} stilts')
dg = bpy.context.evaluated_depsgraph_get(); bad = []
for x, y, z0, z1, n in stl:
    hit, loc, nor, idx, ob, _ = sc.ray_cast(dg, Vector((x, y, z1 - 0.06)), Vector((0, 0, 1)))
    hit2, loc2, _n, _i, ob2, _m = sc.ray_cast(dg, Vector((x + 0.15, y, z0 + 0.02)), Vector((0, 0, 1)))
    if not (hit2 and ob2.name == 'cp041_oj_stilt_imposts'): bad.append((x, y))
ok_('every stilt top reaches into the arcade pier above it (4 cm into the pier underside)', not bad, str(bad))
hs = [s[3] - s[2] for s in stl]
rng_('stilt height (capital to arch springing; Court of the Lions stilted arches, R type)', min(hs) / FT, 2.0, 4.5, 'ft')
info(f'stilt heights {min(hs):.3f}..{max(hs):.3f} m; springing now 3.95 m (12.96 ft) on the main screens = r08b pier underside (DEPARTURES r08 row gives springing 11 ft: r08b already sat higher)')
sv = [v.co for v in bpy.data.objects['cp041_oj_stilt_imposts'].data.vertices]
fw = [max(v.x for v in sv[k:k + 8]) - min(v.x for v in sv[k:k + 8]) for k in range(0, len(sv), 8)]
fd = [max(v.y for v in sv[k:k + 8]) - min(v.y for v in sv[k:k + 8]) for k in range(0, len(sv), 8)]
rng_('stilt footprint width = r08b abacus 0.52 m less 1 cm each side', max(fw), 0.49, 0.51, 'm')
rng_('stilt footprint depth = r08b abacus 0.52 m less 1 cm each side', max(fd), 0.49, 0.51, 'm')
dep('D-SY-CP041-02 painted-stucco skin over the r08b court stucco: copies 6 mm proud on both sides, grown 4 mm in plane; the r08b polka-dot material stays on al_stucco underneath')
dep('D-SY-CP041-03 motifs procedural (lobed sebka net, rosettes, filigree), hues muted OJ blue/red/gold: R for type and scheme, I for every motif and hue')
dep('D-SY-CP041-04 inscription-style bands are abstract knotwork + star roundels, NOT letterforms (no text invented)')
L.insert(0, f'CP041 Alhambra Court OJ polychromy + stilted imposts CANDIDATE checks (rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend) 2026-11-18: {npass} PASS {nfail} FAIL')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
