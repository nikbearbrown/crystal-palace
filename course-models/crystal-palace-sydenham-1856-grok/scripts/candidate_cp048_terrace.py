"""CP048 CANDIDATE (2026-11-17, no verdict): 'The missing transept stays missing' - the north end of the upper terrace in the
summer after the fire (c. summer 1868), dressed as a public garden walk with visitors carrying on toward the surviving
north end.

usage: blender -b <post66-r10 @972145e> -P scripts/candidate_cp048_terrace.py [-- out.blend]   (env CP048_NOSAVE=1: no save)
Base = rounds/sydenham-post66-r10.blend as committed in 972145e (md5 ed31acf2; extract with
  git show 972145e:course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-post66-r10.blend) - the blend the live CP048
  hero renders/post66r10_CAM_CP048_terrace_hold_35mm.png was rendered from (survey look v1.1 apply_render.py --scene-id CP048
  --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people; re-render max diff 0). The working-tree
  rounds/sydenham-post66-r10.blend (80f930f3, re-saved by S67b b4daf98) does NOT reproduce the hero and is not used / not touched.
  -> rounds/candidates/sydenham-post66-r10_cp048terrace.blend
Live hero shows: the lower 40 % of the frame is one flat, near-white, featureless plane (the upper terrace gravel), no people,
nothing between the camera and the garden front / north wing - the storyboard's 'visitors continue toward remaining public
spaces' does not read.
Sources (already in the repo / survey): Guide to the Crystal Palace and Park (1854) 'The Terraces' (upper terrace 1576 x 48 ft,
Bath-stone terrace wall, balustrade with statues - via DEPARTURES CP033 sources); Gardeners' Chronicle / Journal of Horticulture
c.1853 ('a raised terrace walk 48 ft broad over a grass slope 50 ft wide'); storyboard CP048 (From 1867, SY-POST66: north end
permanently altered, visitors continue toward remaining public spaces; hold where loss and surviving structure both read);
BUILD-PLAN PPL-VIC (1850s-1890s visitors). Paxton's terraces were laid out with massed bedding (R in general; the ribbon
pattern, plants and colours here are I). Architecture (main frame, north end, wing, tower) is NOT changed.
Adds dated collection SY68_upper_terrace_north_walk_bedding_visitors__summer1868 (north half of the upper terrace only,
x 20..255 m, between the garden front y -48.1 m and the balustrade walk):
  1. 48 ft rolled-gravel walk along the garden front (warm buff hoggin) + Bath-stone edging kerbs; the walk along the
     balustrade (camera side) gets the same hoggin surface (the model's near-white gravel material is left on the rest);
  2. turf band (I: the source's 50 ft grass slope laid flat on the model's 171 ft deep terrace, D-SY-CP033-10 departure kept)
     cut into panels by 12 ft cross walks on 96 ft bays;
  3. one ribbon-bedded oblong bed per panel (blue edging, yellow band, scarlet centre; I) on a low soil mound;
  4. Bath-stone tazza vases on pedestals at the walk corners of each panel, planted scarlet (I);
  5. people_lib v3.4 1850s visitors (crinoline-era dress, worn to c.1868; I) walking the front walk both ways, at the beds and
     heading for the north end, nearest >= 8 m from the hero lens, none in the near foreground.
Cameras NOT moved, sun/world/exposure/look NOT changed. Nothing deleted or hidden.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP048_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-post66-r10_cp048terrace.blend')
STATE = 'SY68_upper_terrace_north_walk_bedding_visitors__summer1868'
RNG = random.Random(1868048)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP048_terrace_hold_35mm']
col = bpy.data.collections.get(STATE) or bpy.data.collections.new(STATE)
parent = bpy.data.collections['SY-POST66_c1868']
if col.name not in [c.name for c in parent.children]: parent.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('1854 Guide upper terrace 48 ft walk R; c.1853 report 48 ft walk over 50 ft grass slope R (laid flat, I); massed '
                   'bedding on the terraces R (pattern/colours I); vases I; 1850s-dress visitors c.1868 I; storyboard CP048 visitors '
                   'continue toward remaining public spaces; architecture unchanged')
INFO = {}

# model levels (metres): upper terrace gravel top, garden front, balustrade line, north wing inner face
gz = bpy.data.objects['terrace_gravel']
ZG = max((gz.matrix_world @ Vector(v)).z for v in gz.bound_box)          # -7.188
YF = -48.1                                                               # garden front (basement brick face, raycast)
X0, X1 = 20.0, 255.2                                                     # north half; stops short of the north wing face (256.6)
YW = YF - 48 * FT                                                        # 48 ft front walk
YT0, YT1 = YW - 0.3, -85.5                                               # turf band (kerb 0.3 m)
YB = -101.75                                                             # inner face of the upper balustrade (build.py yU-1.5 ft +- 1.1 ft)
BAY = 96 * FT; XW = 12 * FT                                              # statue bays / cross walks
INFO['ZG'] = round(ZG, 3)

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.85, bump=0.15, p0=0.3, p1=0.72, coord='Object', detail=6.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail; L.new(tc.outputs[coord], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = p0; rp.color_ramp.elements[1].position = p1
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
        nz2 = N.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = scale * 18; L.new(tc.outputs[coord], nz2.inputs['Vector'])
        L.new(nz2.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    m['cp_state'] = STATE
    return m
M_WALK = nmat('cp048_hoggin_walk', (0.27, 0.21, 0.14), (0.38, 0.30, 0.20), scale=0.9, coord='Generated', bump=0.2)
M_TURF = nmat('cp048_turf', (0.06, 0.14, 0.03), (0.13, 0.23, 0.05), scale=0.35, coord='Generated', bump=0.25)
M_KERB = nmat('cp048_bath_stone_kerb', (0.50, 0.45, 0.36), (0.62, 0.56, 0.45), scale=3.0)
M_SOIL = nmat('cp048_bed_soil', (0.10, 0.07, 0.05), (0.17, 0.12, 0.08), scale=4.0)
M_VASE = nmat('cp048_bath_stone_vase', (0.46, 0.41, 0.32), (0.58, 0.52, 0.41), scale=4.0)
M_RED = nmat('cp048_bedding_scarlet', (0.06, 0.16, 0.04), (0.62, 0.04, 0.02), scale=9.0, p0=0.35, p1=0.5, rough=0.7)
M_YEL = nmat('cp048_bedding_yellow', (0.10, 0.20, 0.05), (0.85, 0.62, 0.06), scale=9.0, p0=0.35, p1=0.5, rough=0.7)
M_BLU = nmat('cp048_bedding_blue', (0.07, 0.16, 0.06), (0.10, 0.14, 0.55), scale=9.0, p0=0.35, p1=0.5, rough=0.7)
M_LEAF = nmat('cp048_bedding_leaf', (0.05, 0.13, 0.03), (0.12, 0.22, 0.05), scale=9.0)

def new_obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(mat)
    for p in me.polygons: p.use_smooth = False
    o['cp_state'] = STATE; return o
def box(bm, x0, x1, y0, y1, z0, z1):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r['verts']:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
def quad(bm, x0, x1, y0, y1, z):
    vs = [bm.verts.new(p) for p in ((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z))]; bm.faces.new(vs)

# ------------------------------------------------------------------ 1. front walk + kerbs
bm = bmesh.new(); quad(bm, X0, X1, YW, YF, ZG + 0.012); new_obj('cp048_front_walk_48ft', bm, M_WALK)
bm = bmesh.new(); quad(bm, X0, X1, YB, YT1 - 0.3, ZG + 0.012); new_obj('cp048_balustrade_walk', bm, M_WALK)
bm = bmesh.new()
box(bm, X0, X1, YW - 0.3, YW, ZG, ZG + 0.10)                           # walk / turf kerb
box(bm, X0, X1, YT1 - 0.3, YT1, ZG, ZG + 0.10)                         # turf / balustrade-walk kerb
# ------------------------------------------------------------------ 2. turf panels + cross walks
panels = []; x = X0
while x < X1 - 6:
    xa = x + (XW / 2 if x > X0 else 0.0); xb = min(x + BAY - XW / 2, X1)
    if xb - xa > 6: panels.append((xa, xb))
    x += BAY
for xa, xb in panels:
    for xe in (xa, xb):
        if X0 + 0.5 < xe < X1 - 0.5: box(bm, xe - 0.15, xe + 0.15, YT1, YT0, ZG, ZG + 0.10)
kerb = new_obj('cp048_bath_stone_kerbs', bm, M_KERB)
bm = bmesh.new()
for xa, xb in panels: quad(bm, xa + 0.15, xb - 0.15, YT1, YT0, ZG + 0.03)
new_obj('cp048_turf_panels', bm, M_TURF)
bm = bmesh.new()
for xa, xb in panels[1:]: quad(bm, xa - XW, xa, YT1, YT0, ZG + 0.012)
new_obj('cp048_cross_walks_12ft', bm, M_WALK)
INFO['turf_panels'] = len(panels)

# ------------------------------------------------------------------ 3. ribbon beds
def rrect_inside(px, py, cx, cy, hx, hy, r):
    dx = max(abs(px - cx) - (hx - r), 0.0); dy = max(abs(py - cy) - (hy - r), 0.0)
    return math.hypot(dx, dy) <= r
bm_soil = bmesh.new(); bands = {'red': bmesh.new(), 'yel': bmesh.new(), 'blu': bmesh.new(), 'leaf': bmesh.new()}
nblob = 0
def blob(bmx, x, y, z, r):
    res = bmesh.ops.create_icosphere(bmx, subdivisions=1, radius=r)
    sq = RNG.uniform(0.55, 0.8)
    for v in res['verts']: v.co = Vector((v.co.x + x, v.co.y + y, v.co.z * sq + z))
beds = []
for xa, xb in panels:
    cx, cy = (xa + xb) / 2, (YT0 + YT1) / 2
    hx, hy = min((xb - xa) / 2 - 3.2, 9.0), min((YT0 - YT1) / 2 - 3.6, 3.6)
    if hx < 2: continue
    beds.append((cx, cy, hx, hy))
    # soil mound: rounded oblong, crowned 0.25 m (I)
    res = bmesh.ops.create_grid(bm_soil, x_segments=24, y_segments=8, size=1.0)
    for v in res['verts']:
        u, w = v.co.x, v.co.y
        v.co = Vector((cx + u * hx, cy + w * hy, ZG + 0.06 + 0.25 * (1 - u * u) * (1 - w * w)))
    step = 0.26
    yy = cy - hy
    while yy <= cy + hy:
        xx = cx - hx
        while xx <= cx + hx:
            px, py = xx + RNG.uniform(-0.1, 0.1), yy + RNG.uniform(-0.1, 0.1)
            if rrect_inside(px, py, cx, cy, hx, hy, 1.4):
                u, w = (px - cx) / hx, (py - cy) / hy
                zc = ZG + 0.06 + 0.25 * (1 - u * u) * (1 - w * w)
                if not rrect_inside(px, py, cx, cy, hx - 0.45, hy - 0.45, 1.0): k, r = 'blu', 0.11
                elif not rrect_inside(px, py, cx, cy, hx - 1.15, hy - 1.15, 0.7): k, r = 'yel', 0.15
                else: k, r = 'red', 0.17
                if RNG.random() < 0.18: k = 'leaf'
                blob(bands[k], px, py, zc + r * 0.3, r * RNG.uniform(0.8, 1.25)); nblob += 1
            xx += step
        yy += step
new_obj('cp048_bed_soil_mounds', bm_soil, M_SOIL)
for k, m in (('red', M_RED), ('yel', M_YEL), ('blu', M_BLU), ('leaf', M_LEAF)):
    new_obj('cp048_bedding_' + k, bands[k], m)
INFO['ribbon_beds'] = len(beds); INFO['bedding_plants'] = nblob

# ------------------------------------------------------------------ 4. tazza vases on pedestals
bmv = bmesh.new(); bmf = bmesh.new(); nv = 0
def lathe(bmx, x, y, z0, prof, seg=16):
    rings = []
    for (r, z) in prof:
        rings.append([bmx.verts.new((x + r * math.cos(2 * math.pi * i / seg), y + r * math.sin(2 * math.pi * i / seg), z0 + z)) for i in range(seg)])
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(seg): bmx.faces.new((a[i], a[(i + 1) % seg], b[(i + 1) % seg], b[i]))
    bmx.faces.new(list(reversed(rings[0]))); bmx.faces.new(rings[-1])
VY = YT0 - 0.9
for xa, xb in panels:
    for vx in (xa + 1.0, xb - 1.0):
        box(bmv, vx - 0.45, vx + 0.45, VY - 0.45, VY + 0.45, ZG, ZG + 0.15)
        box(bmv, vx - 0.36, vx + 0.36, VY - 0.36, VY + 0.36, ZG + 0.15, ZG + 1.05)    # pedestal 3 ft 6 in (I)
        box(bmv, vx - 0.42, vx + 0.42, VY - 0.42, VY + 0.42, ZG + 1.05, ZG + 1.13)
        lathe(bmv, vx, VY, ZG + 1.13, [(0.26, 0.0), (0.26, 0.06), (0.11, 0.12), (0.09, 0.32), (0.16, 0.38), (0.42, 0.62), (0.50, 0.70), (0.47, 0.74)])
        for i in range(26):
            a = RNG.uniform(0, 2 * math.pi); rr = 0.42 * math.sqrt(RNG.random())
            blob(bmf, vx + rr * math.cos(a), VY + rr * math.sin(a), ZG + 1.13 + 0.74 + 0.12 * (1 - rr / 0.45), RNG.uniform(0.09, 0.14))
        nv += 1
new_obj('cp048_tazza_vases', bmv, M_VASE); new_obj('cp048_vase_geraniums', bmf, M_RED)
INFO['vases'] = nv

# ------------------------------------------------------------------ 5. visitors
people = []
camx, camy = CAM.location.x, CAM.location.y
def put(name, role, pose, x, y, face, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.location = (x, y, ZG + 0.012)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]) + RNG.uniform(-0.2, 0.2))   # base meshes face local -Y
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
E_, W_, N_, S_ = (1, 0), (-1, 0), (0, 1), (0, -1)
def toward(x, y, tx, ty): d = math.hypot(tx - x, ty - y); return ((tx - x) / d, (ty - y) / d)
G = []   # (x, y, role, pose, face)
# front walk: strollers in pairs both ways, a family heading north toward the surviving north end
for i, (x, dirn) in enumerate([(138, E_), (149, W_), (161, E_), (172, E_), (186, W_), (197, E_), (209, W_), (221, E_), (233, E_), (243, W_)]):
    y = YF - RNG.uniform(3.0, 12.0)
    a, b = ('1850s_lady', '1850s_gentleman') if i % 3 else ('1850s_lady', '1850s_lady')
    G.append((x, y, a, 'walking', dirn)); G.append((x + RNG.uniform(-0.3, 0.3), y - 0.75, b, 'walking', dirn))
for (x, y) in [(152.0, YF - 7.5), (204.0, YF - 9.0)]:
    G += [(x, y, '1850s_gentleman', 'walking', E_), (x + 0.4, y - 0.8, '1850s_lady', 'walking', E_),
          (x - 0.9, y - 0.3, '1850s_girl', 'walking', E_), (x - 0.8, y - 1.3, '1850s_boy', 'walking', E_)]
# groups at the beds (standing at the bed edges, looking at the planting) and on the cross walks
for (cx, cy, hx, hy) in beds:
    if cx < 128: continue
    for k in range(RNG.choice((2, 3))):
        side = RNG.choice((1, -1)); x = cx + RNG.uniform(-hx + 1, hx - 1); y = cy + side * (hy + RNG.uniform(0.7, 1.4))
        G.append((x, y, RNG.choice(('1850s_lady', '1850s_lady', '1850s_gentleman', '1850s_girl')), 'standing', toward(x, y, cx, cy)))
for xa, xb in panels[1:]:
    if xa < 140: continue
    x = xa - XW / 2 + RNG.uniform(-0.6, 0.6); y = RNG.uniform(YT1 + 3, YT0 - 3)
    G.append((x, y, RNG.choice(('1850s_gentleman', '1850s_lady')), 'walking', RNG.choice((N_, S_))))
# outer walk: a few figures well clear of the lens, a gentleman pointing toward the north end
G += [(178.0, -90.5, '1850s_gentleman', 'pointing', toward(178, -90.5, 250, -55)), (179.0, -91.2, '1850s_lady', 'standing', toward(179, -91.2, 250, -55)),
      (138.5, -91.8, '1850s_lady', 'walking', E_), (139.1, -92.6, '1850s_gentleman', 'walking', E_), (141.0, -98.8, '1850s_girl', 'walking', E_),
      (214.0, -92.0, '1850s_lady', 'walking', E_), (214.6, -92.7, '1850s_gentleman', 'walking', E_), (240.0, -88.0, '1850s_gentleman', 'walking', N_)]
nearest = 1e9; skipped = 0
for n, (x, y, role, pose, face) in enumerate(G):
    d = math.hypot(x - camx, y - camy)
    if d < 8.0 or not (X0 + 0.5 < x < X1 - 0.5): skipped += 1; continue
    put(f'cp048_visitor_{n:03d}', role, pose, x, y, face, 1868480 + n * 17, 'hero' if d < 18 else ('mid' if d < 60 else 'crowd'))
    nearest = min(nearest, d)
INFO['people_lib_visitors'] = len(people); INFO['skipped_near_lens'] = skipped; INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP048 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP048 SAVED', OUT)
