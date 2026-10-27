"""usage: blender -b <round.blend> -P checks/dimension_check.py -- <out.txt>
Measures world-space bounds of named objects and compares with guide (1856) figures, feet. r11: state-aware
(SY-EARLY / POST66 / 1936 / 1936FIRE / 1936AFTER / RUINS / RUINS post-1941)."""
import bpy, sys
from mathutils import Vector
F = 0.3048; out = sys.argv[sys.argv.index('--')+1]
OB = bpy.data.objects
ROOT = next((c.name for c in bpy.context.scene.collection.children if c.name.startswith('SY-')), '?')
ST = ROOT.split('_')[0]; RUINS41 = ROOT == 'SY-RUINS_post1941'
def has(*n): return all(x in OB for x in n)
def bb(names):
    pts = []
    for n in names:
        o = OB[n]; pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p[i] for p in pts)/F for i in range(3)], [max(p[i] for p in pts)/F for i in range(3)]
rows = [f"STATE  root collection = {ROOT}"]
def chk(label, val, target, tol, src):
    ok = abs(val-target) <= tol; rows.append(f"{'PASS' if ok else 'FAIL'}  {label:46s} model {val:8.2f} ft  target {target:8.2f} ft  tol {tol}  [{src}]")
def flag(ok, label, src): rows.append(f"{'PASS' if ok else 'FAIL'}  {label:60s} [{src}]")
def na(label, why): rows.append(f"N/A   {label:46s} ({why})")
if has('main_floor'):
    lo, hi = bb(['main_floor']); chk('main building length (end walls)', hi[0]-lo[0], 1608, 1, 'guide p.35 B'); chk('general width', hi[1]-lo[1], 312, 1, 'guide p.35 B')
else: na('main building length / width', 'shell destroyed in this state')
if has('central_transept_vault_glass'):
    lo, hi = bb(['central_transept_vault_glass', 'SY_central_transept_walls']); chk('greatest width (central transept N-S extent)', hi[1]-lo[1], 384, 1, 'guide p.35 B')
    chk('central transept crown above main floor', hi[2], 174.25, 0.5, "guide p.35 B 174'3\""); chk('central transept span', hi[0]-lo[0], 120, 1, 'common figure; plan reads 104 inner lines (U)')
else: na('central transept', 'collapsed (FIRE) / destroyed')
if ST == 'SY-1936FIRE': flag(not has('central_transept_vault_glass') and has('ct_collapse_debris'), 'central transept COLLAPSED -> debris pile present', 'LFB/Wikipedia R that it fell; pile form I')
if has('nave_vault_glass'):
    lo, hi = bb(['nave_vault_glass']); chk('nave crown above main floor', hi[2], 110.25, 0.5, "guide p.35 B 110'3\""); chk('nave span', hi[1]-lo[1], 72, 0.5, 'section 0212 R')
else: na('nave', 'shell destroyed in this state')
lo, hi = bb(['basement_brick']); chk('basement depth below main floor', -lo[2], 23.58, 0.3, "guide p.35 B 197'10\"-174'3\"")
POST66 = ST != 'SY-EARLY'
for w in ('south', 'north'):
    if w == 'north' and POST66:
        flag(f'{w}_transept_vault_glass' not in OB, 'north transept ABSENT (post-1866 states)', '1866 fire, never rebuilt: R'); continue
    if not has(f'{w}_transept_vault_glass'): na(f'{w} transept', 'shell destroyed'); continue
    lo, hi = bb([f'{w}_transept_vault_glass']); chk(f'{w} transept centre x (plan 0205)', (lo[0]+hi[0])/2, -528 if w=='south' else 528, 8, 'plan 0205 R: -529/+523')
if has('wings_glass'): lo, hi = bb(['wings_glass']); chk('wing length (N-S direction, each)', hi[1]-lo[1], 574, 1, 'guide p.35 B')
else: na('wings', 'not modelled / gone')
if has('colonnade_roof'): lo, hi = bb(['colonnade_roof']); chk('railway colonnade length', hi[1]-lo[1], 720, 1, 'guide p.35 B')
# towers
for w in ('south', 'north'):
    t = f'water_tower_{w}'
    if RUINS41: flag(not has(t) and has(f'water_tower_base_{w}'), f'{w} water tower DEMOLISHED, brick base kept (post-1941)', 'HE/ADS R; base excavated 1985 R')
    else:
        flag(has(t), f'{w} water tower present', 'survived the fire R (Wikipedia/HE)')
        if has(t): lo, hi = bb([t]); chk(f'{w} tower top above main floor', hi[2], 284, 6, 'Brunel 284 ft (B, common figure)')
if ST == 'SY-RUINS' and not RUINS41:
    for w, tag in (('south', 'dismantled_autumn1940'), ('north', 'demolished_16Apr1941')):
        ok = has(f'water_tower_{w}') and any(tag in c.name for c in OB[f'water_tower_{w}'].users_collection)
        flag(ok, f'{w} tower in dated collection *{tag}*', 'dates: DEPARTURES r11')
if ST in ('SY-1936', 'SY-1936FIRE', 'SY-1936AFTER'): flag(has('south_tower_baird_mast_1933'), 'Baird mast on south tower (1933-)', 'R existence, U size')
# sphinxes
if has('terrace_sphinxes'):
    o = OB['terrace_sphinxes']; W = [o.matrix_world @ v.co / F for v in o.data.vertices]
    UTz = -23.58; body = [v for v in W if v.z > UTz + 3.05 and abs(v.x + 54.5) < 5]
    plin = [v for v in W if v.z < UTz + 3.05 and abs(v.x + 54.5) < 5]
    xs = sorted({round(v.x / 10) for v in W})
    rows.append(f"INFO  sphinx clusters along x (10 ft bins): {len(xs)} bins, bbox x {min(v.x for v in W):.0f}..{max(v.x for v in W):.0f} ft")
    chk('sphinx body length (first sphinx, x=-54.5)', max(v.y for v in body) - min(v.y for v in body), 15.75, 0.8, 'ArtUK SE19_JK_S106 D 480 cm R')
    chk('sphinx body height above plinth', max(v.z for v in body) - (UTz + 3.0), 5.9, 0.6, 'ArtUK H 180 cm R')
    sph_n = sum(1 for xc in (-54.5, 54.5, -548.5, -507.5, 507.5, 548.5) if any(abs(v.x - xc) < 4 and v.z > UTz + 7 for v in W))
    chk('sphinx count', sph_n, 6, 0, 'Park Trust: six, in pairs at three flights R')
else: flag(False, 'terrace sphinxes present', 'Park Trust six sphinxes R')
if ST == 'SY-1936AFTER': flag(has('collapsed_ironwork_field', 'north_end_standing_fragment'), 'aftermath debris + north-end standing fragment', 'Wikipedia R / extent I')
if ST == 'SY-RUINS': flag(not has('collapsed_ironwork_field') and has('column_footing_pads'), 'debris cleared, footing pads only', 'Ward demolition R; pads I')
if has('gallery_floors'):
    gal = OB['gallery_floors']; area = sum(p.area for p in gal.data.polygons if p.normal.z > 0.9)/(F*F)
    rows.append(f"INFO  gallery floor area modelled {area:,.0f} sq ft vs guide 261,568 sq ft (B) -> {area/261568:.0%}; remainder = galleries not yet modelled (outer tiers, transept galleries)")
open(out,'w').write('\n'.join(rows)+'\n'); print('\n'.join(rows))
