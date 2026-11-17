"""CP036 colonnade candidate dimension check vs the 1856 Guide (Muse 0216 / 0208).
usage: blender -b rounds/candidates/sydenham-open54-r14_cp036colonnade.blend -P checks/cp036_colonnade_check.py -- checks/<out>.txt"""
import bpy, sys, math
from mathutils import Vector
FT = 0.3048
out = sys.argv[sys.argv.index('--') + 1]
L = []; ok = 0; bad = 0
def chk(name, model, src, tol, unit='ft'):
    global ok, bad
    p = abs(model - src) <= tol; ok += p; bad += (not p)
    L.append(f"{'PASS' if p else 'FAIL'} {name}: model {model:.2f} {unit} vs source {src} {unit} (tol {tol})")
def note(s): L.append('INFO ' + s)
S = bpy.data.objects['cp036_colonnade_structure']; me = S.data; mw = S.matrix_world
mats = [m.name if m else '' for m in me.materials]
def faces(mname): return [p for p in me.polygons if mats[p.material_index] == mname]
gw = faces('glass_wall'); gr = faces('glass_roof')
xs = sorted(set(round((mw @ me.vertices[p.vertices[0]].co).x / FT, 2) for p in gw))
ys = [(mw @ v.co).y / FT for p in gw for v in [me.vertices[i] for i in p.vertices]]
chk('colonnade length (south wing to station end)', max(ys) - min(ys), 720, 1.0)
chk('clear width between glass lines', xs[-1] - xs[0], 17, 0.25)
# floor to ridge / eave per bay: sample bay 10
fl = bpy.data.objects['cp036_colonnade_floor_steps']
mi = fl.matrix_world.inverted()
hit, loc, nor, idx = fl.ray_cast(mi @ Vector((-890 * FT, (-1334 + 24 * 10 + 4) * FT, 100.0)), (mi.to_3x3() @ Vector((0, 0, -1))).normalized())
zf = (fl.matrix_world @ loc).z / FT
iron = [p for p in me.polygons if mats[p.material_index] == 'iron_painted_OJ']
YC = -1334 + 24 * 10 + 12
gr10 = [p for p in gr if abs((mw @ p.center).y / FT - YC) < 1.0]
ridge = max((mw @ me.vertices[i].co).z / FT for p in gr10 for i in p.vertices)
chk('floor to ridge (bay 11)', ridge - 0.05 - zf, 18, 0.3)
eave = min((mw @ me.vertices[i].co).z / FT for p in gr10 for i in p.vertices)
note(f'eave above floor (bay 11) {eave - 0.05 - zf:.2f} ft (I)')
area = sum(p.area for p in gw + gr) / (FT * FT)
chk('glass area (sides + roof + steps)', area, 30000, 3000, 'sq ft')
note(f'floor area 720 x 17 = {720*17} sq ft; Guide superficial area 15,500 sq ft (implies ~21.5 ft overall incl. walls/eaves; U)')
fbb = [(fl.matrix_world @ Vector(c)) / FT for c in fl.bound_box]
chk('floor width', max(v.x for v in fbb) - min(v.x for v in fbb), 17, 0.25)
note(f'rise station end -> south wing {max(v.z for v in fbb) - min(v.z for v in fbb) - 1.5:.1f} ft (r14 levels, I)')
# people
ppl = [o for o in bpy.data.objects if o.name.startswith('cp036_visitor_')]
hs = []
for o in ppl:
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; hs.append((max(v.z for v in bb) - min(v.z for v in bb)) / FT)
note(f'people_lib visitors {len(ppl)}; heights incl. hats {min(hs):.1f}-{max(hs):.1f} ft')
cam = bpy.data.objects['CAM_CP036_covered_way_28mm']
dmin = min((o.location - cam.location).length for o in ppl)
chk('nearest new figure to the hero lens >= 9 m', max(dmin, 9.0) if dmin >= 9 else dmin, 9.0, 1e9 if dmin >= 9 else 0, 'm')
note(f'nearest new figure {dmin:.2f} m')
P = bpy.data.objects['cp036_avenue_of_exotics']; pb = [P.matrix_world @ Vector(c) for c in P.bound_box]
note(f'plants top {(max(v.z for v in pb))/FT:.1f} ft abs; plants x {min(v.x for v in pb)/FT:.1f}..{max(v.x for v in pb)/FT:.1f} ft (glass lines -898.5/-881.5)')
chk('plants stay inside the glass', 1.0 if (min(v.x for v in pb)/FT > -898.5 and max(v.x for v in pb)/FT < -881.5) else 0.0, 1.0, 0.0, 'bool')
chk('camera not moved (x, y ft)', (cam.location.x / FT + 886.0) ** 2 + (cam.location.y / FT + 1318.0) ** 2, 0.0, 0.01, 'ft^2')
col = bpy.data.collections['SY54_railway_colonnade_avenue__1854_1856']
note(f"dated collection {col.name} cp_state {col.get('cp_state')} objects {len(col.objects)}")
hid = [o.name for o in bpy.data.objects if o.get('cp036_hidden_by_candidate')]
note(f'hidden (not deleted): {hid}')
L.insert(0, f'CP036 colonnade candidate check: {ok} PASS, {bad} FAIL')
open(out, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
