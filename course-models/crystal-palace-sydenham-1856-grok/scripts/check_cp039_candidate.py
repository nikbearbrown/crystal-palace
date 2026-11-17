"""CP039 Pompeian peristyle CANDIDATE checks -> checks/cp039_pompeian_candidate_EARLY.txt
usage: blender -b rounds/candidates/sydenham-1856-r13_cp039pompeian.blend -P scripts/check_cp039_candidate.py"""
import bpy, math, os
import numpy as np
from mathutils import Vector
FT = 0.3048
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'checks', 'cp039_pompeian_candidate_EARLY.txt')
L = []; npass = nfail = 0
def chk(name, model, src, tol, unit=''):
    global npass, nfail
    ok = abs(model - src) <= tol; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.2f} {unit} vs source {src} {unit} (tol {tol})")
def ge(name, model, src, unit=''):
    global npass, nfail
    ok = model >= src; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.2f} {unit} vs source >= {src} {unit}")
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
sc = bpy.context.scene
col = bpy.data.collections['SY54_pompeian_peristyle_painted__1854_1856']
cam = bpy.data.objects['CAM_CP039_pompeian_peristyle_28mm']
# r13 values (read from rounds/sydenham-1856-r13.blend, md5 74dc7aa3, 2026-11-17)
R13_LOC = Vector((-497.0, 121.0, 5.25)); R13_ROT = (1.5823650360107422, -1.3967732570563385e-07, 1.1416178941726685)
chk('camera not moved (position)', (cam.location / FT - R13_LOC).length, 0.0, 0.01, 'ft')
chk('camera not rotated (sum |d euler| rad)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, R13_ROT)), 0.0, 1e-5, 'rad')
chk('camera lens', cam.data.lens, 28.0, 0.0, 'mm')
chk('exposure unchanged (Filmic, r13 -1.0 EV)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
# columns: Ionic capitals with volutes on every peristyle column; red unfluted lower third kept (Scharf No. 18)
co = bpy.data.objects['cp039_ionic_columns']; me = co.data
zs = [(co.matrix_world @ v.co).z / FT for v in me.vertices]
COLS = [(-552.0 + i * 9.6, y) for i in range(6) for y in (126.0, 146.0)] + [(-552.0, 136.0), (-504.0, 136.0)]
ncap = 0
for x, y in COLS:
    vs = [(co.matrix_world @ v.co) / FT for v in me.vertices]
    if any(abs(v.x - x) < 1.2 and abs(v.y - y) < 1.2 and 13.3 < v.z < 13.9 for v in vs[::7]): ncap += 1
chk('peristyle columns with Ionic capitals (volute bolsters + abacus)', ncap, 14, 0, 'cols')
chk('fluted shaft from the top of the red unfluted third (Scharf: lower part not fluted, red)', min(z for z in zs if z > 4.0), 4.5, 0.01, 'ft')
red = bpy.data.objects['pompeian_red']; chk('r13 red lower thirds kept (pompeian_red rendered)', 0 if red.hide_render else 1, 1, 0)
# ceiling
ce = bpy.data.objects['cp039_ambulatory_ceiling']; cz = max((ce.matrix_world @ v.co).z / FT for v in ce.data.vertices)
info(f'ambulatory ceiling plane at {cz:.2f} ft (between the architrave soffit 14.3 and its top 15.6 ft, I); beams 0.55 ft deep on the column bays')
def img(name):
    im = bpy.data.images[name]; w, h = im.size; a = np.array(im.pixels[:]).reshape(h, w, 4)[::-1, :, :3]   # row 0 = top
    return a, w, h
a, w, h = img('cp039_cp039_end_wall_no23.png'); PPF = w / 66.8
def zone(u0, u1, z0, z1):
    return a[int((19.4 - z1) * PPF):int((19.4 - z0) * PPF), int(u0 * PPF):int(u1 * PPF)]
def frac(px, cond): p = px.reshape(-1, 3); return float(cond(p).mean())
whiteish = lambda p: (p.min(1) > 0.70) & (p.max(1) - p.min(1) < 0.20)
redish = lambda p: (p[:, 0] > 0.45) & (p[:, 1] < 0.30) & (p[:, 2] < 0.25)
yelish = lambda p: (p[:, 0] > 0.65) & (p[:, 1] > 0.45) & (p[:, 2] < 0.35)
mz = np.concatenate([zone(15.5, 24.5, 3.2, 13.0).reshape(-1, 3), zone(42.3, 66.0, 3.2, 13.0).reshape(-1, 3)])
ge("end wall No. 23 'general colour is white' (main zone outside the central compartments + lararium panel, share of white px)", 100 * frac(mz, whiteish), 60.0, '%')
dz = zone(0.0, 66.8, 0.3, 3.0)
ge("end wall No. 23 'Dado red and yellow' (share of red or yellow px in the dado)", 100 * frac(dz, lambda p: redish(p) | yelish(p)), 60.0, '%')
info('end wall: three central compartments (lyrist under a high canopy on thin gilt columns + yellow Victory biga on its architrave; '
     'priestess in blue with pitcher left; youth in purple with green wreath right), three dado recesses with the seated lyre girl centre (R content, drawing I)')
lr = bpy.data.objects['cp039_lararium']; lx = sum((lr.matrix_world @ v.co).x for v in lr.data.vertices) / len(lr.data.vertices) / FT
info(f"lararium aedicula (pedestal, red niche, pilasters, pediment, 2 bronze Lares) centred x {lx:.1f} ft on the end wall; 'rich Pompeian red, with a yellow ornament' panel behind (R form, position I)")
# footprint unchanged
st = bpy.data.objects['pompeian_stucco_cp039']; bb = [st.matrix_world @ Vector(c) for c in st.bound_box]
chk('court footprint unchanged: stucco walls x-extent (D-R13-F1, plan 0205 -562..-494 + wall thickness)', (max(v.x for v in bb) - min(v.x for v in bb)) / FT, 69.2, 0.05, 'ft')
chk('court footprint unchanged: stucco walls y-extent', (max(v.y for v in bb) - min(v.y for v in bb)) / FT, 93.7, 0.05, 'ft')
# people
ppl = [o for o in col.objects if o.name.startswith('cp039_visitor_')]
d = min((o.location - cam.location).length for o in ppl)
ge('nearest new figure to the hero lens >= 8 m (left foreground kept clear)', d, 8.0, 'm')
info(f'people_lib 1850s visitors {len(ppl)}; pv57 points kept in the court copy {bpy.data.objects["ppl57_pompeian_visitors_cp039"]["people_count"]} of {len(bpy.data.objects["ppl57_pompeian_visitors"].data.vertices)} (peristyle + tablinum + <7 m from the lens dropped)')
nd = sum(1 for o in col.all_objects if o.get('cp_state') == 'SY54_pompeian_peristyle_painted__1854_1856')
chk('every new object carries the dated state', nd, len(col.all_objects), 0, 'objects')
info(f'dated collection {col.name} objects {len(col.all_objects)}; court opened with the Palace 10 Jun 1854 (R), Scharf handbook 1854 (R); scheme held to 1856 (round EARLY) I')
pk = [i.name for i in bpy.data.images if i.name.startswith('cp039_')]
chk('cp039 textures packed in the blend', sum(1 for i in bpy.data.images if i.name.startswith('cp039_') and i.packed_file), len(pk), 0, 'images')
info('hidden (not deleted): ' + str(sorted(o.name for o in bpy.data.objects if o.get('cp039_hidden_by_candidate'))))
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
dep('ambulatory floor pattern (red signinum with white tessera net + black/white meander border) I: Scharf records Minton imitation mosaic for the atrium, not this pavement')
dep('peristyle garden planting (box-edged compartments, bay standards, roses, lilies, acanthus, one krater) I: Scharf only says laid out with plants like a garden, bordered with columns')
dep('west and tablinum-side wall schemes I (Scharf rule: black dado -> red/yellow walls); figures and vignettes are simplified paintings, not the Abbate tracings')
L.insert(0, f'CP039 Pompeian peristyle candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
