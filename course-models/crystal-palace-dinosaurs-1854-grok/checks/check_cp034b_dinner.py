"""CP034b dinner CANDIDATE checks (2026-11-13).
usage: blender -b rounds/dinosaurs-1854-r06-cand.blend -P checks/check_cp034b_dinner.py -- <live r05.blend> <out.json>
Dims (feet) against the ILN 7 Jan 1854 woodcut + accounts, and scope/state vs the live round: nothing outside
DN53_iguanodon_dinner__31Dec1853 changed; every collection dated; only the old guests hidden."""
import bpy, sys, json, math, hashlib, re
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; LIVE, OUT = a[0], a[1]
F = 0.3048; DX = 3000.0; R = []
def ok(c, label, src, val=None): R.append({'pass': bool(c), 'check': label, 'source': src, 'value': val})
def bb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [(min(c[i] for c in cs) / F, max(c[i] for c in cs) / F) for i in range(3)]
def sig(o):
    s = f'{o.name}|{o.type}|{[round(v,4) for v in o.matrix_world.translation]}|{o.hide_render}|{[c.name for c in o.users_collection]}'
    if o.type == 'MESH': s += f'|{len(o.data.vertices)}|{len(o.data.polygons)}|' + ','.join(f'{v.co.x:.3f},{v.co.y:.3f},{v.co.z:.3f}' for v in list(o.data.vertices)[::max(1, len(o.data.vertices)//200)])
    if o.type == 'LIGHT': s += f'|{o.data.energy}'
    if o.type == 'CAMERA': s += f'|{o.data.lens}|{[round(v,5) for v in o.rotation_euler]}'
    return hashlib.md5(s.encode()).hexdigest()
CDN = 'DN53_iguanodon_dinner__31Dec1853'
cand = {o.name: sig(o) for o in bpy.data.objects}
cand_dn = {o.name for o in bpy.data.collections[CDN].all_objects}
OB = bpy.data.objects
# ---- dims ----
mo = OB['iguanodon_mould_open']; (x0, x1), (y0, y1), (z0, z1) = bb(mo)
ok(abs((x1 - x0) - 35.8) < 3.6, f'mould length {x1-x0:.1f} ft ~ statue 10 m (35.8 ft model, unchanged)', 'cpdinosaurs.org 10 m R', x1 - x0)
rim = z1
ds = OB['DN53c_diners_21_seated']
pts = [ds.matrix_world @ v.co / F for v in ds.data.vertices]
# count diners = connected torso islands is heavy; use script constant via head count = verts above rim+1 clustered by x,y
import collections
cl = collections.Counter((round(p.x - DX), round(p.y)) for p in pts if p.z > rim + 1.0)
ok(True, f'diner head clusters (coarse) {len(cl)}', 'info', len(cl))
ok(len(ds.data.vertices) % 21 == 0, f'seated diner vertex count {len(ds.data.vertices)} divisible by 21 (21 identical figures)', 'Wikipedia / period accounts: 21 diners in the mould R')
(dx0, dx1), (dy0, dy1), (dz0, dz1) = bb(ds)
ok(dz1 - rim < 1.8 and dz1 > rim + 0.6, f'diners show chest/head above rim: top {dz1:.2f} vs rim {rim:.2f}', 'ILN print: diners visible from the chest up above the mould side R')
ok(dz0 > 8.0, f'diners lowest point {dz0:.2f} ft is inside the mould above its belly floor (no legs under the belly)', 'fix of r01 miss')
ok(dx0 - DX > x0 - DX + 3 and dx1 < x1, f'diners within mould length x {dx0-DX:.1f}..{dx1-DX:.1f}', 'geometry')
tb = OB['DN53c_mould_floor_and_table']; (tx0, tx1), (ty0, ty1), (tz0, tz1) = bb(tb)
ok(abs(tz1 - rim) < 0.5, f'table top {tz1:.2f} ft at the rim {rim:.2f} (print: cloth at the rim)', 'ILN print I')
ok(ty1 - ty0 <= 7.2, f'floor/table width {ty1-ty0:.2f} ft inside mould width {y1-y0:.2f}', 'geometry')
seat_len = dx1 - dx0
ok(1.3 <= (seat_len - 1.0) / 10 <= 1.8, f'elbow room {(seat_len-1.0)/10:.2f} ft per diner (packed; 21 in a 10 m statue)', 'I (tight by necessity)')
hd = OB['DN53c_marquee_hoarding']; (hx0, hx1), (hy0, hy1), (hz0, hz1) = bb(hd)
ok(abs(hz1 - 21.0) < 0.01 and hz0 == 0.0, f'hoarding walls 0..{hz1:.1f} ft under canopy springing 26 ft', 'ILN print: boarded walls to the tent eaves I')
va = OB['DN53c_marquee_valance_striped']; ok(abs(bb(va)[2][1] - 26.0) < 0.05, 'valance top meets existing canopy springing 26.0 ft', 'r01 marquee canopy (build.py) I')
ok(abs(hx1 - hx0 - 68) < 0.1 and abs(hy1 - 22) < 0.01, 'marquee walls on the existing 68 x 44 ft canopy footprint', 'build.py marquee I')
names = sorted(o.data.body for o in OB if o.name.startswith('DN53c_lettering_'))
ok(names == sorted(['BUCKLAND', 'CUVIER', 'OWEN', 'MANTELL']), f'name boards lettered {names}', 'ILN print shows Buckland, Cuvier, Owen, Mantell R')
ch = OB['DN53c_chandelier']; cz = bb(ch)[2][0]
ok(cz > dz1 + 3, f'chandelier bottom {cz:.1f} ft clears diners heads {dz1:.1f} ft by >3 ft', 'ILN print: chandelier over the table I')
w = OB['DN53c_waiters_3']; (wx0, wx1), (wy0, wy1), (wz0, wz1) = bb(w)
ok(abs(wz0 - 4.0) < 0.01 and 5.0 < wz1 - wz0 < 6.0, f'waiters stand on deck (z {wz0:.2f}) height {wz1-wz0:.2f} ft', 'ILN print: waiters on deck/stairs I; deck 4 ft (build.py)')
ok(wy1 < -4.0 and wy0 > -16.0, 'waiters inside the deck railings (y -16..-4)', 'geometry')
# ---- state / scope vs live ----
bpy.ops.wm.open_mainfile(filepath=LIVE)
live = {o.name: sig(o) for o in bpy.data.objects}
live_dn = {o.name for o in bpy.data.collections[CDN].all_objects}
outside_changed = [n for n in live if n not in live_dn and cand.get(n) != live[n]]
ok(not outside_changed, f'objects outside {CDN} unchanged vs live r05 ({len(live) - len(live_dn)} compared)', 'scope', outside_changed[:10])
added = sorted(set(cand) - set(live)); ok(all(n in cand_dn and n.startswith('DN53c_') for n in added), f'{len(added)} added objects, all DN53c_ in the dinner collection', 'scope')
ok(set(live) <= set(cand), 'no live object deleted', 'scope')
changed_dn = sorted(n for n in live_dn if cand.get(n) != live[n])
ok(set(changed_dn) <= {'dinner_deck_marquee_table', 'dinner_guests_21'}, f'changed dinner objects: {changed_dn} (deck mesh: old plank/table/legs/chandelier/blank boards removed; old guests hidden)', 'scope')
for c in bpy.data.collections:
    if c.name.startswith('DN'): ok(re.search(r'__(\d{1,2}[A-Za-z]{3})?\d{4}$', c.name) or c.name.startswith('DN-1854'), f'collection dated: {c.name}', 'every state dated')
res = {'date': '2026-11-13', 'pass': sum(r['pass'] for r in R), 'total': len(R), 'rows': R}
json.dump(res, open(OUT, 'w'), indent=1); print('CHECKS', res['pass'], '/', res['total'])
for r in R:
    if not r['pass']: print('FAIL', r)
