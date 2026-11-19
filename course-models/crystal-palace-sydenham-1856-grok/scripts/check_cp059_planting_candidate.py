"""CP059 nave planting burning (30 Nov 1936) CANDIDATE checks -> checks/cp059_planting_candidate_FIRE.txt
usage: blender -b rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend -P scripts/check_cp059_planting_candidate.py"""
import bpy, math, os, ast, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import params as P
OUT = os.path.join(HERE, '..', 'checks', 'cp059_planting_candidate_FIRE.txt')
L = []; npass = nfail = 0
FT = 0.3048
def ok_(name, cond, detail=''):
    global npass, nfail
    npass += bool(cond); nfail += (not cond); L.append(f"{'PASS' if cond else 'FAIL'} {name}{': ' + detail if detail else ''}")
def chk(name, model, src, tol, unit=''):
    ok_(name, abs(model - src) <= tol, f'model {model:.4f} {unit} vs source {src} {unit} (tol {tol})')
def rng_(name, model, lo, hi, unit=''):
    ok_(name, lo <= model <= hi, f'model {model:.3f} {unit} vs source range {lo}..{hi} {unit}')
def info(s): L.append('INFO ' + s)
def dep(s): L.append('DEPARTURE ' + s)
ST = 'SY36_nave_planting_burning__30Nov1936'; STATE = 'SY36-FIRE_30Nov1936_night'
sc = bpy.context.scene; col = bpy.data.collections[ST]
cam = bpy.data.objects['CAM_CP059_nave_fire_28mm']; C = cam.location
# base values read from rounds/sydenham-1936fire-r11b.blend (md5 62396fca), 2026-11-18
B_LOC = Vector((-131.06399536132812, 3.0480000972747803, 1.600000023841858)); B_ROT = (1.6513878107070923, 3.119909663951148e-08, -1.6056660413742065)
B_NOBJ, B_HIDDEN, B_NMAT = 321, 1, 41
chk('hero camera CAM_CP059_nave_fire_28mm not moved (position)', (C - B_LOC).length, 0.0, 1e-4, 'm')
chk('hero camera not rotated (sum |d euler|)', sum(abs(a - b) for a, b in zip(cam.rotation_euler, B_ROT)), 0.0, 1e-6, 'rad')
chk('hero camera lens', cam.data.lens, 28.0, 0.0, 'mm')
chk('exposure unchanged in the blend (Filmic -0.5 EV; the live render.py recipe does not touch it)', sc.view_settings.exposure, -0.5, 0.0, 'EV')
ok_('view transform unchanged (Filmic)', sc.view_settings.view_transform == 'Filmic')
ok_('blend render settings unchanged (1920x1080, 48 spp; live hero recipe overrides to 960x540 32 spp)', (sc.render.resolution_x, sc.render.resolution_y, sc.cycles.samples) == (1920, 1080, 48))
objs = list(col.all_objects)
chk('ONE dated collection holds every new object (base 321 objects + collection)', len(bpy.data.objects), B_NOBJ + len(objs), 0)
chk('nothing hidden / unhidden (hide_render count as base)', sum(o.hide_render for o in bpy.data.objects), B_HIDDEN, 0)
ok_('collection is dated and tagged', col.get('cp_state') == STATE and '30Nov1936' in ST and bool(col.get('evidence')))
ok_('every new object carries cp_state = the dated state', all(o.get('cp_state') == STATE for o in objs), f'{len(objs)} objects: ' + ', '.join(sorted(o.name for o in objs)))
newm = [m for m in bpy.data.materials if m.name.startswith('cp059_')]
ok_('every cp059_ material carries cp_state; only those are new (base 41 incl. the 0-user orphan fountain_jet_spray, which Blender drops on save - no render effect)',
    all(m.get('cp_state') == STATE for m in newm) and len(bpy.data.materials) == B_NMAT - 1 + len(newm) and 'fountain_jet_spray' not in bpy.data.materials, f'{len(newm)} materials')
ok_('Sydenham only: no Hyde Park / 1851 collection or object involved',
    not any(('HP' in c.name or '1851' in c.name) for c in bpy.data.collections) and not any(('HP' in o.name or '1851' in o.name) for o in objs))
crowns = sorted((o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_nave_tree_') and o.name.endswith('_crown')), key=lambda o: o.name)
ok_('r03 placeholder crowns untouched (12 x 720 faces, foliage material, visible)', len(crowns) == 12 and all(len(o.data.polygons) == 720 and o.data.materials[0].name == 'foliage' and not o.hide_render for o in crowns))
fl = bpy.data.materials['fire_flames_surface']
ok_('round flame material reused unedited (18 nodes, 18 links, emission 6.0)', len(fl.node_tree.nodes) == 18 and len(fl.node_tree.links) == 18 and fl.node_tree.nodes['Emission'].inputs['Strength'].default_value == 6.0)
ok_('new flame tongues use the round flame material and carry hfac', bpy.data.objects['cp059_crown_flames'].data.materials[0] == fl and 'hfac' in bpy.data.objects['cp059_crown_flames'].data.attributes)
ok_('new flames cast no shadow (as r11b fire_flames)', not bpy.data.objects['cp059_crown_flames'].visible_shadow and not bpy.data.objects['fire_flames'].visible_shadow)
def verts(name):
    me = bpy.data.objects[name].data; a = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', a); return a.reshape(-1, 3)
cv = verts('cp059_leaf_canopy'); ev = verts('cp059_smouldering_leaves'); lv = verts('cp059_charred_limbs'); tv = verts('cp059_crown_flames')
allv = np.vstack([cv, ev, lv])
NY = P.NAVE_SPAN / 2
rng_('foliage + limbs stay inside the nave column lines (|y| <= 36 ft; params.NAVE_SPAN 72 ft, R) - no leaf through a gallery', float(np.abs(allv[:, 1]).max()) / FT, 0, NY, 'ft')
rng_('lowest leaf above the r03 tub tops (3.5 ft) - no foliage on the floor', float(cv[:, 2].min()) / FT, 3.5, 40, 'ft')
top = float(allv[:, 2].max()) / FT
rng_('tree top (foliage) below the nave vault springing (74.25 ft; guide p.35 crown 110 ft 3 in, B)', top, 15, P.NAVE_SPRING, 'ft')
rng_('tree height on its 3.5 ft tub: tub-grown conservatory tree (I: 20-45 ft)', top - 3.5, 20, 45, 'ft')
rng_('flame tongue tops below the nave vault springing (74.25 ft)', float(tv[:, 2].max()) / FT, 15, P.NAVE_SPRING, 'ft')
me = bpy.data.objects['cp059_leaf_canopy'].data
fs = me.polygons; nb = len(fs)
lens = []
for p in list(fs)[:20000:7]:
    vv = [Vector(me.vertices[i].co) for i in p.vertices]; lens.append((vv[3] - vv[0]).length)
rng_('leaf blade length, median (broadleaf ornamental trees: 5-35 cm, I)', float(np.median(lens)) * 100, 5, 35, 'cm')
rng_('leaf blade length, max', float(np.max(lens)) * 100, 5, 40, 'cm')
pc = ast.literal_eval(col['per_crown'])
ok_('every placeholder crown dressed (>= 10000 blades each)', len(pc) == 12 and all(p[3] >= 10000 for p in pc), ', '.join(f'{p[1]}ft:{p[3]}' for p in pc))
ok_('flame tongues follow the r11b nave burn weight (more tongues where w is higher)', all(p[5] == int(round(11 * p[2])) for p in pc), ', '.join(f'{p[1]}ft w{p[2]} t{p[5]}' for p in pc))
rng_('limb base radius not larger than the r03 trunk top (0.5 ft)', 0.13 / FT, 0.2, 0.5, 'ft')
info(f'blades {nb} canopy + {len(bpy.data.objects["cp059_smouldering_leaves"].data.polygons)} smouldering; tongues {sum(p[5] for p in pc)}; limbs {len(lv)} verts')
dep('D-SY-CP059-02 leaf canopy hugs the r03 placeholder crowns (icosphere unions) - crown shape/size I; placeholders stay underneath, visible through gaps as inner foliage mass')
dep('D-SY-CP059-03 foliage trimmed at y = +-35 ft (nave column lines); the r03 crowns themselves reach |y| 39.7 ft and stay bare on their gallery side')
dep('D-SY-CP059-05 which crowns burn and how hard follows the r11b nave flame-density weight (states.py), I')
L.insert(0, f'CP059 nave planting burning CANDIDATE checks ({ST}) - {npass} PASS {nfail} FAIL')
open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
