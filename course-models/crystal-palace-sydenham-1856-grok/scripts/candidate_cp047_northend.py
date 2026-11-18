"""CP047 CANDIDATE (2026-11-18, no verdict): 'The first permanent loss' - the truncated north end seen from the upper terrace
in the summer after the fire (c. summer 1868): the terrace in front of the surviving north end dressed as the public garden
walk it remained, with visitors carrying on toward the north wing.

usage: blender -b <post66-r10 @972145e> -P scripts/candidate_cp047_northend.py [-- out.blend]   (env CP047_NOSAVE=1: no save)
Base = rounds/sydenham-post66-r10.blend as committed in 972145e (md5 ed31acf2; extract with
  git show 972145e:course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-post66-r10.blend) - the blend the live CP047
  hero renders/r10final_CAM_CP047_north_end_35mm.png was rendered from (survey look v1.1, look/sydenham_logs/CP047.log:
  apply_render.py --scene-id CP047 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people; re-render max diff 0,
  verdict 'improved', kept_from after_raw). The working-tree rounds/sydenham-post66-r10.blend (80f930f3) is not used / not touched.
  -> rounds/candidates/sydenham-post66-r10_cp047northend.blend
Live hero shows: the bottom ~40 % of the frame is one flat, near-white, featureless gravel plane between the lens and the garden
  front / north wing; no people; nothing says 'public garden that carried on after the loss'.
Approach: the SAME summer-1868 terrace state that is already live for the CP048 hero (KEEP c44b7d3, D-SY-CP048-01..12) is
  reproduced here by running scripts/candidate_cp048_terrace.py unchanged (CP048_NOSAVE=1; deterministic seeds, identical
  geometry and visitors) so CP047 and CP048 show one consistent terrace, then the CP047 frame gets its own visitors in the
  part of the terrace mostly behind or beside the CP048 lens (x 96..140 m: the near beds, the cross walk, the outer walk), all >= 19 m from
  the CP047 lens (and behind / >= 14 m in front of the CP048 lens). Everything is gathered into ONE dated collection SY68_north_end_terrace_walk_bedding_visitors__summer1868
  (the CP048 builder's collection is renamed; cp_state retagged on every object and material).
Sources: as D-SY-CP048-01..11 (1854 Guide 'The Terraces': upper terrace walk 48 ft; c.1853 Gardeners' Chronicle report '48 ft
  walk over a 50 ft grass slope'; massed bedding on the terraces R in general, pattern I); storyboard CP047 'The first permanent
  loss - damage and adaptation' (SY66: north transept never rebuilt, the north end and the terraces stayed public: Historic
  England blog; crystal.dircon chronology; Aerofilms EPW021373 1928 'truncated north end', via PROGRESS r10); BUILD-PLAN PPL-VIC
  (CP047: 1850s-1890s visitors). Architecture (main frame, north end, wing, tower) NOT changed.
Cameras NOT moved, sun/world/exposure/look NOT changed. Nothing deleted or hidden.
"""
import bpy, math, os, sys, random, runpy
from mathutils import Vector

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP047_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-post66-r10_cp047northend.blend')
STATE = 'SY68_north_end_terrace_walk_bedding_visitors__summer1868'
STATE48 = 'SY68_upper_terrace_north_walk_bedding_visitors__summer1868'
assert bpy.data.collections.get(STATE48) is None and bpy.data.collections.get(STATE) is None, 'base already dressed'
n_before = len(bpy.data.objects)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)

# ------------------------------------------------------------------ 1. the live CP048 summer-1868 terrace, unchanged
os.environ['CP048_NOSAVE'] = '1'
g = runpy.run_path(os.path.join(HERE, 'candidate_cp048_terrace.py'), run_name='cp048_builder')
del os.environ['CP048_NOSAVE']
col = bpy.data.collections[STATE48]; col.name = STATE
INFO = {'cp048_layout_objects': len(col.objects)}
put48, RNG48 = g['put'], g['RNG']
ZG, YF, YW, YT0, YT1, YB, X0, X1, XW = (g[k] for k in ('ZG', 'YF', 'YW', 'YT0', 'YT1', 'YB', 'X0', 'X1', 'XW'))
beds, panels = g['beds'], g['panels']

# ------------------------------------------------------------------ 2. CP047-only visitors (x 96..140 m, >= 19 m from the CP047 lens)
from cpl_people import person_mesh
RNG = random.Random(1868047)
CAM = bpy.data.objects['CAM_CP047_north_end_35mm']
camx, camy = CAM.location.x, CAM.location.y
people = []
def put(name, role, pose, x, y, face, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.location = (x, y, ZG + 0.012)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]) + RNG.uniform(-0.2, 0.2))   # base meshes face local -Y
    o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
E_, W_, N_, S_ = (1, 0), (-1, 0), (0, 1), (0, -1)
def toward(x, y, tx, ty): d = math.hypot(tx - x, ty - y); return ((tx - x) / d, (ty - y) / d)
NE = (250.0, -55.0)          # the surviving north end / wing corner
G = []
# front walk west of the CP048 strollers
for i, (x, dirn) in enumerate([(99, E_), (107, W_), (115, E_), (124, E_), (131, W_)]):
    y = YF - RNG.uniform(3.0, 12.0)
    a, b = ('1850s_lady', '1850s_gentleman') if i % 2 == 0 else ('1850s_lady', '1850s_lady')
    G.append((x, y, a, 'walking', dirn)); G.append((x + RNG.uniform(-0.3, 0.3), y - 0.75, b, 'walking', dirn))
# groups at the two near beds (the CP048 builder only peopled beds with cx >= 128)
for (cx, cy, hx, hy) in beds:
    if not (85 < cx < 128): continue
    for k in range(3):
        side = -1 if k < 2 else 1; x = cx + RNG.uniform(-hx + 1.5, hx - 1.5); y = cy + side * (hy + RNG.uniform(0.7, 1.3))
        G.append((x, y, ('1850s_lady', '1850s_gentleman', '1850s_girl')[k], 'standing', toward(x, y, cx, cy)))
# cross walk between the near panels
for xa, xb in panels[1:]:
    if 100 < xa < 140:
        x = xa - XW / 2; G.append((x, YT1 + 6.0, '1850s_gentleman', 'walking', N_)); G.append((x + 0.5, YT1 + 6.6, '1850s_lady', 'walking', N_))
# outer (balustrade) walk: family heading for the north end, a gentleman pointing it out, a strolling couple
G += [(104.0, -93.0, '1850s_lady', 'walking', toward(104.0, -93.0, *NE)), (104.7, -93.7, '1850s_gentleman', 'walking', toward(104.7, -93.7, *NE)),
      (110.0, -90.0, '1850s_gentleman', 'pointing', toward(110, -90, *NE)), (110.8, -90.9, '1850s_lady', 'standing', toward(110.8, -90.9, *NE)),
      (111.3, -89.7, '1850s_girl', 'standing', toward(111.3, -89.7, *NE)),
      (115.0, -96.5, '1850s_lady', 'walking', E_), (115.6, -97.2, '1850s_gentleman', 'walking', E_), (116.6, -96.0, '1850s_boy', 'walking', E_)]
C48 = bpy.data.objects['CAM_CP048_terrace_hold_35mm']
F48 = (C48.matrix_world.to_3x3() @ Vector((0, 0, -1))).to_2d().normalized()
def clear_of_cp048(x, y):   # behind the CP048 lens, or >= 14 m in front of it (keeps the live CP048 frame's near ground as it is)
    v = Vector((x - C48.location.x, y - C48.location.y)); return v.dot(F48) < 0 or v.length >= 14.0
nearest = 1e9; skipped = 0
for n, (x, y, role, pose, face) in enumerate(G):
    d = math.hypot(x - camx, y - camy)
    if d < 19.0 or not clear_of_cp048(x, y) or not (X0 + 0.5 < x < X1 - 0.5) or not (YB + 0.4 < y < YF - 0.4): skipped += 1; continue
    put(f'cp047_visitor_{n:03d}', role, pose, x, y, face, 1868470 + n * 19, 'hero' if d < 25 else ('mid' if d < 60 else 'crowd'))
    nearest = min(nearest, d)
INFO['cp047_visitors'] = len(people); INFO['cp047_skipped'] = skipped; INFO['cp047_nearest_new_figure_m'] = round(nearest, 2)
n48 = [o for o in col.objects if o.name.startswith('cp048_visitor_')]
INFO['cp048_visitors_nearest_to_cp047_lens_m'] = round(min(math.hypot(o.location.x - camx, o.location.y - camy) for o in n48), 2)

# ------------------------------------------------------------------ 3. one dated state on everything
col['cp_state'] = STATE
col['evidence'] = ('reproduces the live CP048 summer-1868 terrace (D-SY-CP048-01..11: 1854 Guide upper terrace 48 ft walk R; c.1853 '
                   'report 48 ft walk over 50 ft grass slope R (laid flat, I); massed bedding R (pattern/colours I); vases I) + CP047 '
                   'visitors (PPL-VIC, 1850s dress worn c.1868 I; storyboard CP047 damage and adaptation, terraces stayed public R)')
for o in col.objects: o['cp_state'] = STATE
for m in bpy.data.materials:
    if m.get('cp_state') == STATE48: m['cp_state'] = STATE
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
print('CP047 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP047 SAVED', OUT)
