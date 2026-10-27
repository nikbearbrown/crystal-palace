"""usage: blender -b <round.blend> -P checks/dimension_check.py -- <out.txt>
Measures world-space bounds of named objects and compares with guide (1856) figures, feet. r11: state-aware
(SY-EARLY / POST66 / 1936 / 1936FIRE / 1936AFTER / RUINS / RUINS post-1941)."""
import bpy, sys
from mathutils import Vector
F = 0.3048; out = sys.argv[sys.argv.index('--')+1]
OB = bpy.data.objects
ROOT = next((c.name for c in bpy.context.scene.collection.children if c.name.startswith('SY-') or c.name.startswith('SY54')), '?')
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
BUILD = ST == 'SY-BUILD'; PRE56 = ST in ('SY-BUILD', 'SY54')
if BUILD: na('main building length / width', 'under construction: floor laid only to x=+150 (D-R14-B1)')
elif has('main_floor'):
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
POST66 = ST not in ('SY-EARLY', 'SY-CONCERT57', 'SY-BUILD', 'SY54')
for w in ('south', 'north'):
    if w == 'north' and POST66:
        flag(f'{w}_transept_vault_glass' not in OB, 'north transept ABSENT (post-1866 states)', '1866 fire, never rebuilt: R'); continue
    if not has(f'{w}_transept_vault_glass'): na(f'{w} transept', 'not yet glazed (1853)' if BUILD else 'shell destroyed'); continue
    lo, hi = bb([f'{w}_transept_vault_glass']); chk(f'{w} transept centre x (plan 0205)', (lo[0]+hi[0])/2, -528 if w=='south' else 528, 8, 'plan 0205 R: -529/+523')
if BUILD: na('wings', 'south wing frame only, north wing not begun (D-R14-B1)')
elif has('wings_glass'): lo, hi = bb(['wings_glass']); chk('wing length (N-S direction, each)', hi[1]-lo[1], 574, 1, 'guide p.35 B')
else: na('wings', 'not modelled / gone')
if has('colonnade_roof'): lo, hi = bb(['colonnade_roof']); chk('railway colonnade length', hi[1]-lo[1], 720, 1, 'guide p.35 B')
# towers
for w in ('south', 'north'):
    t = f'water_tower_{w}'
    if PRE56: flag(not has(t), f'{w} water tower ABSENT (built 1855-56)', 'tower dates R: DEPARTURES TOWER_DATE'); continue
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
elif BUILD: flag(True, 'terrace sphinxes ABSENT (set up for the 1854 opening)', 'Park Trust R (1854); BUILD date c.1853 I')
else: flag(False, 'terrace sphinxes present', 'Park Trust six sphinxes R')
if ST == 'SY-1936AFTER': flag(has('collapsed_ironwork_field', 'north_end_standing_fragment'), 'aftermath debris + north-end standing fragment', 'Wikipedia R / extent I')
# r12: sculpted sphinx (nemes headdress reaches the crown) + 1936 dressing (PPL-20C)
if has('terrace_sphinxes'):
    head = [v for v in W if abs(v.x + 54.5) < 5 and v.z > UTz + 3.0 + 5.0]
    flag(len(head) > 50, 'sphinx r12: sculpted head/nemes above 5 ft over plinth (%d verts)' % len(head), 'surviving CP sphinxes, photographs R; form I')
if ST == 'SY-1936FIRE':
    pumps = [o for o in OB if o.name.startswith('pump_')]; tls = [o for o in OB if o.name.startswith('TL_ladder_')]
    rows.append(f"INFO  appliances modelled: {len(pumps)} pumps + {len(tls)} turntable ladders (LFB attendance 89 appliances, 438 firemen R; modelled subset I)")
    flag(len(pumps) >= 10 and len(tls) >= 3, 'FIRE: >=10 pumps and >=3 turntable ladders present', 'LFB attendance R')
    if has('pump_parade_00'):
        lo, hi = bb(['pump_parade_00']); chk('LFB pump length (1930s Leyland/Dennis)', hi[0]-lo[0] if hi[0]-lo[0] > hi[1]-lo[1] else hi[1]-lo[1], 25, 3, 'typical 1930s pump ~7.5 m I')
if ST in ('SY-1936FIRE', 'SY-1936AFTER'):
    flag(has('police_line_parade') or has('police_line_lower_terrace'), 'police line present', 'press photos of cordons R; positions I')
    flag(any(o.name.startswith('crowd36_') for o in OB), 'crowd stand-ins present', 'contemporary reports of ~100,000 onlookers R; density I')
if ST == 'SY-1936AFTER' and has('collapsed_ironwork_field'):
    m = OB['collapsed_ironwork_field'].active_material
    bc = m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value if m and m.use_nodes else (1, 1, 1, 1)
    flag(m is not None and 'charred' in m.name, 'AFTER stumps/ironwork use charred-black iron (%s)' % (m.name if m else None), 'aerial 0587/0588 dark wreckage R; tone I')
if ST == 'SY-RUINS': flag(not has('collapsed_ironwork_field') and has('column_footing_pads'), 'debris cleared, footing pads only', 'Ward demolition R; pads I')
# r13: CONCERT57 (CP045), Fine Arts courts (CP039/CP040), waterworks running (CP042)
def pc(n): return OB[n].get('people_count', 0) if n in OB else 0
def collof(n, tag): return n in OB and any(tag in c.name for c in OB[n].users_collection)
if ST == 'SY-CONCERT57':
    chk('performers (orchestra + chorus) count', pc('ppl57_performers_choir_band'), 2396, 360, 'Handel Festival 1857: 2,000 chorus + 396 band, Times/Grove R; +-15%')
    flag(pc('ppl57_audience') > 5000, 'audience > 5,000 figures (%d)' % pc('ppl57_audience'), 'attendance 11,000-17,000 per day R; modelled subset U')
    flag(has('organ_case_1857', 'organ_front_pipes_1857', 'costa_rostrum', 'royal_box_1857'), 'organ, Costa rostrum and royal box present', 'Gray & Davison organ 1857 R; forms I')
    flag(collof('handel_orchestra_tiers', '1857'), 'orchestra tiers in a dated 1857 collection', 'rule')
    if has('handel_orchestra_tiers'):
        lo, hi = bb(['handel_orchestra_tiers']); chk('orchestra N-S width (fills transept)', hi[1]-lo[1], 216, 20, 'transept 384 ft less aisles/galleries; ~216 I')
if ST in ('SY-EARLY', 'SY-CONCERT57'):
    for n, lab in (('ppl57_pompeian_visitors', 'Pompeian'), ('ppl57_greekroman_visitors', 'Greek/Roman'), ('ppl57_mediaeval_visitors', 'Mediaeval')):
        flag(n in OB and any('SY54_court' in c.name for c in OB[n].users_collection), f'{lab} court present in a dated SY54 collection', '1854 guidebooks R (Scharf, Digby Wyatt)')
if ST == 'SY-EARLY':
    flag(collof('waterworks_spray', '18Jun1856') and collof('waterworks_foam', '18Jun1856'), 'waterworks RUNNING in dated collection *18Jun1856*', 'first full display 18 Jun 1856 R')
    if has('waterworks_spray'):
        o = OB['waterworks_spray']; gc = list(o.get('great_centres_ft', []))
        for i in range(0, len(gc), 2):
            V = [o.matrix_world @ v.co / F for v in o.data.vertices]; V = [v for v in V if (v.x-gc[i])**2 + (v.y-gc[i+1])**2 < 36]
            if V: chk('great-basin centre plume height above water (%+.0f)' % gc[i], max(v.z for v in V) - min(v.z for v in V), 200, 20, 'period claim up to 250 ft R(claim); modelled 200 I')
    flag(pc('ppl57_waterworks_visitors') > 1500, 'waterworks visitors > 1,500 (%d)' % pc('ppl57_waterworks_visitors'), 'U numbers')
# r14: BUILD53 (CP033), OPEN54 (CP035) + station (CP036), LATE11 (CP049-54), WAR (CP056)
def maxx(n):
    o = OB[n]; return max((o.matrix_world @ v.co).x for v in o.data.vertices) / F if len(o.data.vertices) else -9999
if BUILD:
    flag(has('ridge_furrow_roofs') and maxx('ridge_furrow_roofs') <= -340, 'glazing only south of x=-350 (max x %.0f)' % (maxx('ridge_furrow_roofs') if has('ridge_furrow_roofs') else 0), 'erection front U (D-R14-B1)')
    flag(has('frame_SY_main_frame') and maxx('frame_SY_main_frame') < 805, 'frame present but partial', 'I')
    flag(not has('nave_vault_glass') and not has('central_transept_vault_glass'), 'no vault glazing yet', 'I')
    flag(has('earth_spoil_heaps_cuttings', 'build53_tramway_rails', 'build53_timber'), 'earthworks, tramways and scaffolding present', 'Paxton park works 1852-54 R; forms I')
    flag(pc('ppl53_navvies_erectors') > 600, 'navvies/erectors > 600 figures (%d)' % pc('ppl53_navvies_erectors'), 'workforce up to ~6,400 in 1853-54 R(claim); modelled subset U')
    flag(collof('ppl53_navvies_erectors', 'c1853') or collof('earth_spoil_heaps_cuttings', '1853'), 'construction dressing in a dated 1853 collection', 'rule')
if ST == 'SY54':
    flag(not has('park_basins_water') and not has('fountain_jets'), 'no great fountains/cascades or jets (opened 1856)', 'R')
    flag(has('open54_dais', 'open54_flagpoles', 'open54_choir_stand'), 'dais, flags and choir stand present', 'ILN 17 Jun 1854 engravings R(existence); forms I')
    flag(collof('open54_dais', '10Jun1854'), 'opening dressing in a dated 10Jun1854 collection', 'rule')
    flag(pc('ppl54_opening_day') > 5000, 'opening-day figures inside > 5,000 (%d)' % pc('ppl54_opening_day'), '~40,000 present R(press); modelled subset U')
    if has('covered_way_roof_glass'):
        lo, hi = bb(['covered_way_roof_glass']); chk('covered way (colonnade) length', hi[1]-lo[1], 720, 2, 'guide p.35 B 720 ft')
        flag(hi[2] - lo[2] > 50, 'covered way steps down the slope (drop %.0f ft)' % (hi[2] - lo[2]), 'I (was flat r01-r13)')
    flag(has('station_shed_roof_glass', 'station_platforms', 'train_carriage_bodies') and collof('station_platforms', '1854'), 'Low Level station shed, platforms, train in a dated 1854 collection', 'station opened 10 Jun 1854 R; form U')
    flag(pc('ppl54_station_visitors') > 600, 'station/covered-way visitors > 600 (%d)' % pc('ppl54_station_visitors'), 'U')
if ST == 'SY-LATE':
    flag(has('late11_pavilions_render', 'late11_pavilions_stone', 'late11_all_red_route_rails'), 'Festival of Empire replicas + All-Red Route railway present', 'Festival of Empire 1911 R; sites/forms I/U')
    flag(any(m.name == 'late_boarded_panes_zinc' for m in bpy.data.materials), 'wear: boarded panes material present', 'I')
    flag(pc('ppl11_festival_crowd') > 3000, 'Edwardian crowd > 3,000 (%d)' % pc('ppl11_festival_crowd'), 'U')
if ST == 'SY-WAR':
    flag(pc('ppl15_rnd_ratings') > 900, 'RND ratings > 900 (%d)' % pc('ppl15_rnd_ratings'), 'HMS Crystal Palace trained ~125,000 men 1914-19 R(claim); modelled subset U')
    flag(has('war_masts') and collof('war_masts', '1914-18'), 'ensign/mast in dated 1914-18 collection', 'I')
cams = [o for o in OB if o.type == 'CAMERA']
flag(all(abs(o.data.sensor_width - 36) < 0.01 for o in cams), 'all %d cameras on a 36 mm sensor' % len(cams), 'rule')
flag(all(abs(o.matrix_world.to_euler().y) < 1e-3 or abs(abs(o.matrix_world.to_euler().y) - 3.14159) < 1e-3 for o in cams if o.data.type != 'ORTHO'), 'no camera roll', 'rule')
if has('gallery_floors'):
    gal = OB['gallery_floors']; area = sum(p.area for p in gal.data.polygons if p.normal.z > 0.9)/(F*F)
    rows.append(f"INFO  gallery floor area modelled {area:,.0f} sq ft vs guide 261,568 sq ft (B) -> {area/261568:.0%}; remainder = galleries not yet modelled (outer tiers, transept galleries)")
open(out,'w').write('\n'.join(rows)+'\n'); print('\n'.join(rows))
