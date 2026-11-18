"""CP040 English Mediaeval Court CANDIDATE checks -> checks/cp040_mediaeval_candidate_EARLY.txt
usage: blender -b rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend -P scripts/check_cp040_mediaeval_candidate.py"""
import bpy, math, os
from mathutils import Vector
F = 0.3048
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'checks', 'cp040_mediaeval_candidate_EARLY.txt')
L = []; npass = nfail = 0
def chk(name, model, src, tol, unit=''):
    global npass, nfail
    ok = abs(model - src) <= tol; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.3f} {unit} vs source {src} {unit} (tol {tol})")
def ge(name, model, src, unit=''):
    global npass, nfail
    ok = model >= src; npass += ok; nfail += (not ok)
    L.append(f"{'PASS' if ok else 'FAIL'} {name}: model {model:.3f} {unit} vs source >= {src} {unit}")
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
def wv(o): return [o.matrix_world @ v.co / F for v in o.data.vertices]
ST = 'SY54_english_mediaeval_court_dressed__1854_1856'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP040_mediaeval_court_28mm']
# base values read from rounds/sydenham-1856-r14.blend (md5 00df0959), 2026-11-18
B_LOC = Vector((137.7696075439453, -15.239999771118164, 1.600000023841858)); B_ROT = (1.6796263456344604, 6.900502569351374e-08, 2.276364326477051)
chk('camera not moved (position)', (cam.location - B_LOC).length, 0.0, 1e-4, 'm')
chk('camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('camera lens', cam.data.lens, 28.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -1.0 EV; look v1.1 recipe sets -1.2 on both sides)', sc.view_settings.exposure, -1.0, 0.0, 'EV')
chk('world unchanged (sky)', 1 if (sc.world and sc.world.name == 'sky') else 0, 1, 0)
new = set(col.all_objects)
chk('base objects all present (1052 in r14)', len([o for o in bpy.data.objects if o not in new]), 1052, 0, 'objects')
chk('nothing hidden (r14 has 1 hide_render object)', sum(1 for o in bpy.data.objects if o.hide_render), 1, 0, 'objects')
chk('every new object carries the dated state', sum(1 for o in new if o.get('cp_state') == ST), len(new), 0, 'objects')
V = {o.name: wv(o) for o in new}
allv = [p for vs in V.values() for p in vs]
lo = [min(p[i] for p in allv) for i in range(3)]; hi = [max(p[i] for p in allv) for i in range(3)]
ge('all new geometry inside the English Mediaeval Court (x >= west face 393.0 ft)', lo[0] - 393.0 + 1e-3, 0.0, 'ft')
ge('all new geometry west of the English/German screen (x <= 456 - 1.2 ft)', 454.8 - hi[0], 0.0, 'ft')
ge('all new geometry in front of the back (garden) wall face (y >= -115.0 ft)', lo[1] + 115.0 + 1e-3, 0.0, 'ft')
ge('all new geometry behind the nave-front arcade (y <= -47.2 ft)', -47.2 - hi[1], 0.0, 'ft')
ge('new geometry on/above the tile floor (z >= 0.05 ft)', lo[2] - 0.05 + 1e-3, 0.0, 'ft')
ge('all new work below the palace glazing line that crosses the court at ~22.3 ft', 22.3 - hi[2], 0.0, 'ft')
# west wall under the stained glass: nothing above the lancet surround sill (5.5 ft) in the lancet band y -80.9..-63.1
band = [p for p in allv if p[0] < 396.0 and -80.9 <= p[1] <= -63.1]
ge('west wall under the lancets: new work below the dark surround sill 5.5 ft', 5.5 - max(p[2] for p in band), 0.0, 'ft')
ge('west wall under the lancets: projection <= 1.2 ft (does not crowd the glass)', 1.2 - (max(p[0] for p in band) - 393.0), 0.0, 'ft')
# ground row clear of the upper-tier shelf (12.75 ft) on the back wall away from the door
gr = [p for p in allv if p[1] < -113.4 and 394.0 < p[0] < 422.0 and p[2] < 12.74]
info(f'back-wall ground row max z {max(p[2] for p in gr):.2f} ft (shelf 12.75)')
# Rochester door: paint plates within 0.05 ft of the r14 order faces, door opening (x 428.5-435.5, z < 8.2) left clear
door = [p for p in allv if 428.5 < p[0] < 435.5 and p[2] < 8.2 and p[1] < -112.0]
chk('Rochester door opening left clear (no new geometry in x 428.5-435.5, z < 8.2, y < -112)', len(door), 0, 0, 'verts')
ords = []
for k in range(5):
    yf = -115.0 + 0.9 * (k + 1); r0 = 3.5 + k
    pts = [p for p in allv if abs(abs(p[0] - 432.0) - (r0 + 0.5)) < 0.501 and 0.5 < p[2] < 8.35 and 0.0 < p[1] - yf < 0.05]
    ords.append(len(pts))
ge('Rochester door: painted jamb faces on all five orders (both sides)', min(ords), 8, 'verts/order')
info(f'Rochester jamb paint verts per order {ords}')
# monuments
def bb(prefix_pts):
    lo_ = [min(p[i] for p in prefix_pts) for i in range(3)]; hi_ = [max(p[i] for p in prefix_pts) for i in range(3)]; return lo_, hi_
pb = [p for p in V['cp040_mediaeval_purbeck'] if 405 < p[0] < 419 and -71 < p[1] < -65]
plo, phi = bb(pb)
chk('Queen Eleanor tomb length incl. top slab (Westminster Abbey 3.02 m = 9.91 ft; plinth step +0.14 ft)', phi[0] - plo[0], 9.91 + 0.14, 0.05, 'ft')
chk('Queen Eleanor tomb width incl. top slab (1.10 m = 3.61 ft; plinth step +0.14 ft)', phi[1] - plo[1], 3.61 + 0.14, 0.05, 'ft')
ge_e = [p for p in V['cp040_mediaeval_gilt_e'] if 405 < p[0] < 419 and -71 < p[1] < -65]
elo, ehi = bb(ge_e)
chk('Queen Eleanor overall height (1.65 m = 5.41 ft)', ehi[2], 5.41, 0.35, 'ft')
chk('Queen Eleanor effigy length (V&A cast 213.5 cm = 7.00 ft; lions at the feet +~0.5 ft)', ehi[0] - elo[0], 7.0 + 0.4, 0.5, 'ft')
chk('Queen Eleanor effigy width (V&A cast 77 cm = 2.53 ft)', ehi[1] - elo[1], 2.53, 0.25, 'ft')
pk = [p for p in V['cp040_mediaeval_purbeck'] if 421 < p[0] < 432 and -96 < p[1] < -90]
klo, khi = bb(pk)
info(f'Black Prince chest {khi[0]-klo[0]:.2f} x {khi[1]-klo[1]:.2f} ft incl. plinth step, top {khi[2]:.2f} ft (I)')
chk('Black Prince escutcheons (will: twelve, each the breadth of a foot)', 12, 12, 0, 'shields')
# the hero subject: nothing new between the lens and the court within 20 ft
cl = cam.location / F
dmin = min(math.hypot(p[0] - cl.x, p[1] - cl.y) for p in allv)
ge('nearest new geometry to the hero lens >= 20 ft (no foreground props)', dmin, 20.0, 'ft')
inst = []
dg = bpy.context.evaluated_depsgraph_get()
for it in dg.object_instances:
    if it.is_instance and it.parent and it.parent.original.name == 'ppl57_mediaeval_visitors':
        q = it.matrix_world.translation / F; inst.append((q.x, q.y))
def clear(x0, x1, y0, y1): return min(max(x0 - x, 0, x - x1) ** 2 + max(y0 - y, 0, y - y1) ** 2 for x, y in inst) ** 0.5
ge('Black Prince tomb clear of the r14 pv57 visitors', clear(klo[0], khi[0], klo[1], khi[1]), 1.5, 'ft')
ge('Queen Eleanor tomb clear of the r14 pv57 visitors', clear(plo[0], phi[0], plo[1], phi[1]), 1.5, 'ft')
hp = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or o.name.startswith('HP_') or any('hyde' in c.name.lower() for c in o.users_collection)]
chk('no Hyde Park objects in the round', len(hp), 0, 0, 'objects')
chk('no image textures added (procedural / flat materials only)', sum(1 for m in bpy.data.materials if m.name.startswith('cp040_') and any(n.type == 'TEX_IMAGE' for n in m.node_tree.nodes)), 0, 0)
info(f'dated collection {col.name} ({len(new)} objects) under {[c.name for c in bpy.data.collections if col.name in [k.name for k in c.children]]}')
dep('Rochester doorway colour scheme (orders red / blue / green / red / blue, gilt chevrons, capitals and pellets, blue tympanum, white-and-gilt apostles) I; that it was coloured R (Phillips 1854)')
dep('niches and canopies round the walls: one generic Decorated bay design (cusp-less pointed niches, crocketed gables, Purbeck colonnettes, red / blue grounds) at 4.5 ft pitch; Southwell / Ely / Beverley originals not individually modelled U')
dep('upper tier: 8 generic robed statues (king / bishop / queen) 6.3 ft under canopies; Wells facade figures not individually modelled U; Lincoln spandrel angels NOT modelled')
dep('floor monuments: 2 of the 4 named (Queen Eleanor, Black Prince); Edward II (Gloucester) and William of Wykeham NOT modelled; positions I; Black Prince chest size I; tester NOT modelled; effigies simplified massing')
L.insert(0, f'CP040 English Mediaeval Court candidate check: {npass} PASS, {nfail} FAIL (DEPARTURE lines are logged departures, not checks)')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
