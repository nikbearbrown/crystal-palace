"""CP042 cascades candidate dimension check vs the 1856 Guide ('The Fountains', page after Muse OCR 0220) and the r05 map read.
usage: blender -b rounds/candidates/sydenham-1856-r13_cp042cascade.blend -P checks/cp042_cascades_check.py -- checks/<out>.txt"""
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
def dep(s): L.append('DEPARTURE ' + s)
XW = (500 - 541) * 4.28; YJ = -100 - (560 - 265) * 4.28
S = bpy.data.objects['cp042_cascades_causeway_arcade_stone']; W = bpy.data.objects['cp042_cascades_water_running']; I = bpy.data.objects['cp042_water_temples_iron_glass']
def faces(o, mname):
    me = o.data; mats = [m.name if m else '' for m in me.materials]
    return [(o.matrix_world @ p.center) / FT for p in me.polygons if mats[p.material_index] == mname], me, mats
for xa, tag in ((XW, 'west'), (-XW, 'east')):
    # pools: water faces in the channel strip, distinct levels
    wc, me, mats = faces(W, 'water')
    lv = sorted({round(c.z, 2) for c in wc if abs(c.x - xa) < 21 and -1752 < c.y < -1369}, reverse=True)
    chk(f'{tag}: number of cascades (falls between channel pools + into the head basin)', len(lv), 12, 0, 'falls')
    drops = [a - b for a, b in zip(lv, lv[1:])]
    note(f'{tag}: pool levels {lv[0]:.2f} .. {lv[-1]:.2f} ft, drop per fall {drops[0] if drops else 0:.2f} ft (I)')
    # arcade breadth: front faces of the piers at the arcade face
    me = S.data; mats = [m.name if m else '' for m in me.materials]
    xs = []
    for p in me.polygons:
        if mats[p.material_index] != 'cp042_ashlar_portland' or p.normal.y > -0.99: continue
        c = p.center / FT
        if abs(c.y + 1790.0) < 0.05 and abs(c.x - xa) <= 61:
            for i in p.vertices: xs.append(me.vertices[i].co.x / FT)
    chk(f'{tag}: stone arcade breadth', max(xs) - min(xs), 120, 0.5)
    # fall: lip (head-basin water) to great-basin water
    hz = max(c.z for c in wc if abs(c.x - xa) < 50 and -1789 < c.y < -1751)
    gw = bpy.data.objects['park_basins_water_cp042']; gp = min(gw.data.polygons, key=lambda p: (((gw.matrix_world @ p.center) / FT) - Vector((math.copysign(518, xa), -1962, 0))).xy.length)
    zw = (gw.matrix_world @ gw.data.vertices[gp.vertices[0]].co).z / FT
    dep(f'{tag}: cataract fall {hz - zw:.2f} ft vs Guide 30 ft (D-SY-CP042-05: r05 levels; camera eye 2.6 ft above the basin water)')
    dep(f'{tag}: temple front -> arcade face {(YJ - 6) - (-1790.0):.1f} ft vs Guide 600 ft / 1852 plan 450 ft (D-SY-CP042-04: r05 map positions kept)')
    # temple: footprint of the iron screen (corner columns) on the r05 40 x 40 ft footprint
    me = I.data; vs = [I.matrix_world @ v.co / FT for v in me.vertices]
    tv = [v for v in vs if abs(v.x - xa) < 25 and abs(v.y - (YJ + 14)) < 25]
    cols = [v for v in tv if v.z < -100]
    chk(f'{tag}: iron screen column centres on the r05 temple footprint (40 ft, I)', max(v.x for v in cols) - min(v.x for v in cols) - 2 * 1.0 - 1.0, 40, 0.5)
    note(f'{tag}: temple height podium foot -> finial {max(v.z for v in tv) - (-109.07):.1f} ft (form/height I)')
# camera
cam = bpy.data.objects['CAM_CP042_cascade_50mm']; t = cam.matrix_world.translation; e = cam.matrix_world.to_euler()
dpos = (Vector(t) - Vector((-41.294304, -590.129395, -44.241711))).length / FT
chk('camera not moved (position)', dpos, 0.0, 0.01)
chk('camera not rotated (sum |d euler| rad)', abs(e.x - 1.590101) + abs(e.y) + abs(e.z - 0.171373), 0.0, 1e-5, 'rad')
chk('camera lens', cam.data.lens, 50.0, 0.0, 'mm')
ppl = [o for o in bpy.data.objects if o.name.startswith('cp042_visitor_')]
dmin = min((o.location - cam.location).length for o in ppl)
chk('nearest new figure to the hero lens >= 9 m', min(dmin, 9.0), 9.0, 0.0, 'm')
hs = []
for o in ppl:
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; hs.append((max(v.z for v in bb) - min(v.z for v in bb)) / FT)
note(f'people_lib visitors {len(ppl)}; heights incl. hats {min(hs):.1f}-{max(hs):.1f} ft; nearest {dmin:.1f} m')
col = bpy.data.collections['SY56_water_temples_cascades_running__18Jun1856']
chk('every new object carries the dated state', sum(1 for o in col.all_objects if o.get('cp_state') == col.get('cp_state')), len(col.all_objects), 0, 'objects')
note(f"dated collection {col.name} cp_state {col.get('cp_state')} objects {len(col.all_objects)}; date: {col.get('date')}")
hid = [o.name for o in bpy.data.objects if o.get('cp042_hidden_by_candidate')]
note(f'hidden (not deleted): {hid}')
hy = [o.name for o in bpy.data.objects if 'hyde' in o.name.lower() or 'HP_' in o.name]
chk('no Hyde Park objects in the round', len(hy), 0, 0, 'objects')
L.insert(0, f'CP042 cascades candidate check: {ok} PASS, {bad} FAIL (DEPARTURE lines are logged departures, not checks)')
open(out, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
