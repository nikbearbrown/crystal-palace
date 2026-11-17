"""CP042 CANDIDATE (2026-11-17, no verdict): 'The landscape performs' - the Water Temples, the twelve cascades and the
stone-arcade cataract into the great basins, RUNNING on the first complete display of the waterworks, 18 June 1856.

usage: blender -b rounds/sydenham-1856-r13.blend -P scripts/candidate_cp042_cascades.py [-- out.blend]
       (env CP042_NOSAVE=1: build in memory only)
Opens rounds/sydenham-1856-r13.blend (md5 74dc7aa3; never written) - the blend the live CP042 hero
renders/r13_1856_CAM_CP042_cascade_50mm.png was rendered from (look v1.1 apply_render.py --scene-id CP042 --era 1851
--tod exterior_afternoon --spp 24 --res 1280x720 --no-people; re-render max diff 0)
-> rounds/candidates/sydenham-1856-r13_cp042cascade.blend.
Live hero shows: the r05 cascade as 16 bare white stone slabs (a white stair) with white-box foam on every riser, the
r05 'water temple' as a 4-post slab placeholder, the cascade foot running on into the great basin at water level,
and the nearest great-basin rim jets as thick opaque white tubes over the top-left of the frame.
Sources:
  Guide to the Crystal Palace and Park, 1856, 'The Fountains' (page after Muse OCR 0220; text via e-rara pagetext 8640245):
    'Beyond these, as we advance down the central path, are the iron Water Temples, from which the water rushes down a
     series of twelve cascades, extending for a distance of 600 feet, till it falls over the stone arcade in the great
     fountain basins, forming a glittering cataract 120 feet broad, with a fall of thirty feet. The Water Temples with
     their cascades and falls, and the two great fountains into the basins of which they discharge, constitute the lower
     series, which is played only on grand occasions.'
  Muse OCR 0220 (same Guide): the cascades and the two largest fountains run only 'on the days of great exhibition'.
  1857 map 0591 (r05 read): temples J at map dy 560, cascades L at dx 500 / 582, great basins M (positions kept).
  18 June 1856: waterworks first brought into complete operation, Queen present (R, as D-R13-W1).
Adds dated collection SY56_water_temples_cascades_running__18Jun1856 (both sides, mirrored about the axis):
  1. r05/r13 cascade steps, cascade water, temple placeholder and the r13 cascade foam/spray/outfalls removed from mesh
     COPIES (originals hidden, not deleted);
  2. iron Water Temple on the r05 40 x 40 ft footprint: stone podium, arcaded cast-iron screen (3 round arches a side),
     entablature + cresting, glazed iron-ribbed dome, lantern, finial (form and heights I), water sheets from the front;
  3. twelve cascades (R count) in a 40 ft stone channel on a raised causeway with gravel walks and grass banks, each
     cascade a white-water sheet + foam + spray over a stone sill, urn piers at every fall (forms I);
  4. a 120 ft broad (R) head basin ending in a stone arcade (11 arches) over which a semi-transparent veil falls into the
     great basin, with a cataract pool kerb where the arcade stands beyond the r05 basin outline; fall 10 ft (R 30 ft,
     see DEPARTURES: the r05 park levels leave only 42 ft between temple and basin and the camera eye is 2.6 ft above the
     basin water, so a 30 ft wall would blank the whole frame);
  5. the great-basin rim jets nearest the hero lens (< 160 ft) rebuilt finer (thin core + broken droplet stream);
  6. pv57 visitor points inside the new works dropped (mesh COPY, original hidden); people_lib 1850s visitors on the
     causeway walks and at the cataract pool.
Cameras NOT moved, sun/world/exposure NOT changed, terrain NOT changed. Units metres in the blend; feet here.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP042_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r13_cp042cascade.blend')
STATE = 'SY56_water_temples_cascades_running__18Jun1856'
COLL = 'SY56_water_temples_cascades_running__18Jun1856'
RNG = random.Random(18061856042)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP042_cascade_50mm']
CAMP = CAM.matrix_world.translation / FT
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(col)
col['cp_state'] = STATE
col['date'] = '18 June 1856 (first complete display, R); cascades + great fountains played on grand occasions only (R); cascades out of use by 1874 (R, HE register)'
col['evidence'] = ('iron Water Temples; twelve cascades over 600 ft; stone arcade cataract 120 ft broad, 30 ft fall (R, 1856 Guide); '
                   'positions r05 map 0591 read (R/I); channel width, causeway, temple form, arcade arches, fall height modelled 10 ft (I)')
INFO = {}; HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp042_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# ------------------------------------------------------------------ r05/r13 levels (read from the blend, not assumed)
def mdx(dx): return (dx - 541) * 4.28            # 1857 map 0591 display px -> model ft (params MAP_FT_PER_DPX, R)
def mdy(dy): return -100 - (dy - 265) * 4.28
dg = bpy.context.evaluated_depsgraph_get()
GROUND_OBJ = {'park_slope', 'park_paths_gravel', 'terrain'}
def ground(x, y):
    o = Vector((x * FT, y * FT, 60.0))
    for _ in range(40):
        r = sc.ray_cast(dg, o, Vector((0, 0, -1)))
        if not r[0]: return None
        if r[4].name in GROUND_OBJ: return r[1].z / FT
        o = r[1] + Vector((0, 0, -0.003))
    return None
XW = mdx(500)                       # west cascade axis -175.48 ft (east = +175.48)
YJ = mdy(560)                       # r05 temple: y YJ-6 .. YJ+34
ZJ = ground(XW - 40, YJ - 4)        # ground at the temple front
YM = mdy(700)
wb = bpy.data.objects['park_basins_water']
_gp = min(wb.data.polygons, key=lambda p: ((wb.matrix_world @ p.center) / FT - Vector((mdx(420), YM, 0))).xy.length)   # west great basin
ZW = (wb.matrix_world @ wb.data.vertices[_gp.vertices[0]].co).z / FT                 # great-basin water level
INFO['levels_ft'] = dict(temple_ground=round(ZJ, 2), basin_water=round(ZW, 2))

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.85, bump=0.1, metal=0.0, spec=0.3):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 5.0; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = 0.3; rp.color_ramp.elements[1].position = 0.72
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m
def ashlar(name, c1, c2, mortar, course=1.5, block=3.0):
    """coursed ashlar: brick texture in world-ish object coords, courses along z (feet -> metres)"""
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); br = N.new('ShaderNodeTexBrick')
    br.inputs['Scale'].default_value = 1.0 / (block * FT); br.inputs['Mortar Size'].default_value = 0.012
    br.inputs['Color1'].default_value = (*c1, 1); br.inputs['Color2'].default_value = (*c2, 1); br.inputs['Mortar'].default_value = (*mortar, 1)
    br.inputs['Brick Width'].default_value = 1.0; br.inputs['Row Height'].default_value = course / block
    sx_ = N.new('ShaderNodeSeparateXYZ'); cb = N.new('ShaderNodeCombineXYZ'); mx = N.new('ShaderNodeMath'); mx.operation = 'ADD'
    L.new(tc.outputs['Object'], sx_.inputs[0]); L.new(sx_.outputs['X'], mx.inputs[0]); L.new(sx_.outputs['Y'], mx.inputs[1])
    L.new(mx.outputs[0], cb.inputs['X']); L.new(sx_.outputs['Z'], cb.inputs['Y']); L.new(cb.outputs[0], br.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    mixc = N.new('ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.inputs['Factor'].default_value = 0.18
    L.new(br.outputs['Color'], mixc.inputs[6]); L.new(nz.outputs['Color'], mixc.inputs[7]); L.new(mixc.outputs[2], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.88; b.inputs['Specular IOR Level'].default_value = 0.25
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.12; L.new(br.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m
MAT = bpy.data.materials
M = dict(
    stone=ashlar('cp042_ashlar_portland', (0.44, 0.42, 0.37), (0.39, 0.37, 0.33), (0.30, 0.29, 0.26)),
    coping=nmat('cp042_stone_coping', (0.50, 0.48, 0.43), (0.57, 0.55, 0.49), 9.0, 0.8, 0.05),
    veil=None,
    recess=nmat('cp042_arch_recess_wet', (0.10, 0.11, 0.11), (0.16, 0.17, 0.17), 6.0, 0.35, 0.05, 0.0, 0.5),
    floor=nmat('cp042_channel_bed', (0.22, 0.24, 0.22), (0.30, 0.31, 0.28), 8.0, 0.6, 0.05),
    water=MAT['water'], spray=MAT['water_spray_running'], foam=MAT['water_foam_running'],
    grass=MAT['grass'], gravel=MAT['gravel'], iron=MAT['iron_exterior_pale'], glass=MAT['glass_roof'],
    iron_dark=nmat('cp042_iron_bronze_green', (0.10, 0.16, 0.13), (0.15, 0.22, 0.18), 12.0, 0.45, 0.02, 0.5),
)
def veil_mat(name):
    """falling sheet: vertical streaks (noise stretched along z) drive alpha 0.12..0.9; white-water tint, soft emission"""
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / (0.9 * FT), 1 / (0.9 * FT), 1 / (14.0 * FT)); L.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0; nz.inputs['Detail'].default_value = 6.0; nz.inputs['Roughness'].default_value = 0.6
    L.new(mp.outputs[0], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].position = 0.38; rp.color_ramp.elements[1].position = 0.62
    rp.color_ramp.elements[0].color = (0.12, 0.12, 0.12, 1); rp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1)
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Alpha'])
    b.inputs['Base Color'].default_value = (0.86, 0.91, 0.94, 1); b.inputs['Roughness'].default_value = 0.35
    b.inputs['Transmission Weight'].default_value = 0.3; b.inputs['IOR'].default_value = 1.33
    b.inputs['Emission Color'].default_value = (0.9, 0.95, 1.0, 1); b.inputs['Emission Strength'].default_value = 0.18
    m.diffuse_color = (0.85, 0.9, 0.95, 0.6); return m
M['veil'] = veil_mat('cp042_cataract_veil')
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}

class Kit:
    """bmesh builder, inputs in FEET (world), stored in metres"""
    def __init__(s): s.bm = bmesh.new()
    def _t(s, k, n0):
        s.bm.faces.ensure_lookup_table()
        for j in range(n0, len(s.bm.faces)): s.bm.faces[j].material_index = IX[k]
    def v(s, p): return s.bm.verts.new((p[0] * FT, p[1] * FT, p[2] * FT))
    def poly(s, k, pts):
        n0 = len(s.bm.faces); s.bm.faces.new([s.v(p) for p in pts]); s._t(k, n0)
    def box(s, k, x0, x1, y0, y1, z0, z1):
        x0, x1 = min(x0, x1), max(x0, x1); y0, y1 = min(y0, y1), max(y0, y1)
        n0 = len(s.bm.faces); vs = [s.v(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[j] for j in f])
        s._t(k, n0)
    def prism(s, k, sec0, sec1):
        """closed prism between two cross-sections (lists of 3D points, same count, ccw)"""
        n0 = len(s.bm.faces); a = [s.v(p) for p in sec0]; b = [s.v(p) for p in sec1]; n = len(a)
        for j in range(n): s.bm.faces.new([a[j], a[(j + 1) % n], b[(j + 1) % n], b[j]])
        s.bm.faces.new(list(reversed(a))); s.bm.faces.new(b); s._t(k, n0)
    def cyl(s, k, a, b, r, seg=10, cap=True, r2=None):
        A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); u = d.cross(up).normalized(); w = u.cross(d).normalized()
        n0 = len(s.bm.faces); r2 = r if r2 is None else r2
        ra = [s.v(A + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r) for j in range(seg)]
        rb = [s.v(B + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r2) for j in range(seg)]
        for j in range(seg): s.bm.faces.new([ra[j], ra[(j + 1) % seg], rb[(j + 1) % seg], rb[j]])
        if cap: s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb)
        s._t(k, n0)
    def bar(s, k, a, b, w, t=None):
        t = t or w; A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.v(p + sd * (i * w / 2) + u * (j * t / 2)) for p in (A, B) for (i, j) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[j] for j in f])
        s._t(k, n0)
    def lathe(s, k, cx, cy, prof, seg=16):
        n0 = len(s.bm.faces); rings = []
        for r, z in prof:
            rings.append([s.v((cx + max(r, 1e-3) * math.cos(2 * math.pi * j / seg), cy + max(r, 1e-3) * math.sin(2 * math.pi * j / seg), z)) for j in range(seg)])
        for a, b in zip(rings, rings[1:]):
            for j in range(seg): s.bm.faces.new([a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]])
        s.bm.faces.new(list(reversed(rings[0]))); s.bm.faces.new(rings[-1]); s._t(k, n0)
    def rect(s, k, x0, x1, y0, y1, z):
        x0, x1 = min(x0, x1), max(x0, x1); y0, y1 = min(y0, y1), max(y0, y1)
        s.poly(k, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)])
    def drop(s, k, c, r):
        n0 = len(s.bm.faces); x, y, z = c
        vs = [s.v((x + dx * r, y + dy * r, z + dz * r)) for dx, dy, dz in ((1, 0, -0.4), (-0.5, 0.87, -0.4), (-0.5, -0.87, -0.4), (0, 0, 1.4))]
        for t_ in ((0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)): s.bm.faces.new([vs[i] for i in t_])
        s._t(k, n0)
    def done(s, name, smooth=False):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in ML: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(name, me); col.objects.link(ob); ob['cp_state'] = STATE
        return ob

# ------------------------------------------------------------------ 1. remove the r05/r13 cascades + temple placeholder (mesh copies)
def copy_obj(o, tag='_cp042'):
    me = o.data.copy(); me.name = o.data.name + tag
    n = bpy.data.objects.new(o.name + tag, me); n.matrix_world = o.matrix_world.copy()
    for c in o.users_collection: c.objects.link(n)
    for m_ in o.modifiers:
        nm_ = n.modifiers.new(m_.name, m_.type)
        if m_.type == 'NODES': nm_.node_group = m_.node_group
    for k_ in o.keys():
        try: n[k_] = o[k_]
        except Exception: pass
    n['cp042_mesh_copy_of'] = o.name; hide(o); return n
def faces_world(o):
    mw = o.matrix_world; me = o.data
    return mw, me
def near_set(v, vals, tol=0.05): return any(abs(v - q) <= tol for q in vals)
CY0, CY1 = mdy(690) - 8, YJ + 34.2          # r05 cascade + temple y-extent (-1927 .. -1328 ft)
YF = -1790.0                                # arcade face (new); head basin -1750 .. YF
YH = -1750.0
AW = 60.0                                   # arcade half-width (120 ft broad, R)
POOL_S = -1838.0                            # cataract-pool south kerb line
def in_pool_rect(x, y, s):
    xa = s * XW
    return abs(x - xa) <= AW + 3.5 and POOL_S - 1.0 <= y <= YF + 1.0
# park_basins_stone: r05 step boxes (x_ +-14), temple boxes (x_ +-20, posts x_ +-16 +-1.2) -> delete; rim blocks under the
# new cataract pool -> delete (replaced by the pool kerb)
ps = bpy.data.objects['park_basins_stone']; psn = copy_obj(ps)
bm = bmesh.new(); bm.from_mesh(psn.data); mw = psn.matrix_world
kill = []; nstep = 0; nrim = 0
for f in bm.faces:
    vs = [(mw @ v.co) / FT for v in f.verts]
    for s in (-1, 1):
        xa = s * XW
        xs = [v.x - xa for v in vs]
        if all(CY0 <= v.y <= CY1 for v in vs) and all(near_set(x, (-14, 14, -20, 20, -17.2, -14.8, 14.8, 17.2)) for x in xs):
            kill.append(f); nstep += 1; break
        c = sum(vs, Vector()) / len(vs)
        if in_pool_rect(c.x, c.y, s) and -151.5 <= c.z <= -146.0 and f.calc_area() / (FT * FT) < 2000:
            kill.append(f); nrim += 1; break
bmesh.ops.delete(bm, geom=list(set(kill)), context='FACES'); bm.to_mesh(psn.data); bm.free()
INFO['r05_cascade_temple_faces_removed'] = nstep; INFO['rim_faces_removed_under_pool'] = nrim
pw = bpy.data.objects['park_basins_water']; pwn = copy_obj(pw)
bm = bmesh.new(); bm.from_mesh(pwn.data); mw = pwn.matrix_world; kill = []
for f in bm.faces:
    vs = [(mw @ v.co) / FT for v in f.verts]
    for s in (-1, 1):
        if all(CY0 <= v.y <= CY1 for v in vs) and all(near_set(v.x - s * XW, (-11, 11)) for v in vs): kill.append(f); break
bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(pwn.data); bm.free(); INFO['r05_cascade_water_faces_removed'] = len(kill)

# waterworks foam / spray / drops: remove r13 cascade sheets, ribbons, foam, drops, temple outfalls (loose parts wholly
# inside the cascade strips) and the great-basin rim-jet arcs nearest the lens (rebuilt finer below)
NEAR_JET_FT = 230.0
zM = ZW + 0.6 - 3.5
RIMJ = []                                   # (p0, p1) of the great-basin rim jets near the lens (waterworks.py r13 formula)
for dxm in (420, 662):
    x_ = mdx(dxm)
    for k in range(40):
        t = 2 * math.pi * k / 40; ex = math.copysign(abs(math.cos(t)) ** 0.5, math.cos(t)); ey = math.copysign(abs(math.sin(t)) ** 0.5, math.sin(t))
        p0 = Vector((x_ + 372 * ex, YM + 202 * ey, zM + 3.5)); p1 = Vector((x_ + 330 * ex, YM + 170 * ey, ZW))
        if (p0.xy - CAMP.xy).length < NEAR_JET_FT: RIMJ.append((p0, p1))
def seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / ab.dot(ab))); return (p - (a + ab * t)).length
def loose_parts(bm):
    bm.verts.ensure_lookup_table(); seen = set(); parts = []
    for f0 in bm.faces:
        if f0.index in seen: continue
        stack = [f0]; part = []; seen.add(f0.index)
        while stack:
            f = stack.pop(); part.append(f)
            for e in f.edges:
                for g in e.link_faces:
                    if g.index not in seen: seen.add(g.index); stack.append(g)
            for v in f.verts:
                for g in v.link_faces:
                    if g.index not in seen: seen.add(g.index); stack.append(g)
        parts.append(part)
    return parts
for nm in ('waterworks_foam', 'waterworks_spray', 'waterworks_drops'):
    o = bpy.data.objects[nm]; on = copy_obj(o)
    bm = bmesh.new(); bm.from_mesh(on.data); bm.faces.ensure_lookup_table(); mw = on.matrix_world
    for i, f in enumerate(bm.faces): f.index = i
    kill = []; ncas = 0; njet = 0
    for part in loose_parts(bm):
        vs = [(mw @ v.co) / FT for f in part for v in f.verts]
        hit = False
        for s in (-1, 1):
            if all(abs(v.x - s * XW) <= 14.7 and CY0 <= v.y <= CY1 for v in vs): hit = True; ncas += 1; break
        if not hit and nm == 'waterworks_spray' and RIMJ:
            for p0, p1 in RIMJ:
                pl = [p0.lerp(p1, i / 12) + Vector((0, 0, 4 * 16 * (i / 12) * (1 - i / 12))) for i in range(13)]
                if all(min(seg_dist(v, a, b) for a, b in zip(pl, pl[1:])) < 2.5 for v in vs): hit = True; njet += 1; break
        if hit: kill.extend(part)
    bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(on.data); bm.free()
    INFO[f'{nm}_parts_removed'] = (ncas, njet)
INFO['near_rim_jets'] = len(RIMJ)

# ------------------------------------------------------------------ shared levels for the new works
NC = 12                                   # twelve cascades (R)
YT = YJ - 6.0                             # temple front (-1368.6)
LP = (YT - YH) / NC                       # pool length in the channel
F_ARC = 10.0                              # modelled cataract fall (R 30 ft; D-SY-CP042-05)
W0 = ZJ + 1.5                             # head pool at the temple
WH = ZW + F_ARC                           # broad head basin behind the arcade
DROP = (W0 - WH) / NC
LV = [W0 - DROP * k for k in range(NC + 1)]       # LV[0] temple pool ... LV[12] head basin
CH = 20.0                                 # half clear width of the channel (40 ft, I)
WALL = 3.0; WALK = 12.0
INFO['cascade'] = dict(n=NC, pool_len_ft=round(LP, 2), drop_ft=round(DROP, 2), run_temple_to_arcade_ft=round(YT - YF, 1),
                       fall_ft=F_ARC, head_level=round(WH, 2), top_level=round(W0, 2))

K = Kit()          # stone, coping, causeway, channel
WK = Kit()         # water, veils, foam, drops
IK = Kit()         # ironwork + glass (temples)
def gz(x, y):
    g = ground(x, y); return g if g is not None else ZW - 1.5
URN_PIERS = 0
def urn(x, y, z):
    K.box('coping', x - 1.6, x + 1.6, y - 1.6, y + 1.6, z, z + 3.2); K.box('coping', x - 1.9, x + 1.9, y - 1.9, y + 1.9, z + 3.2, z + 3.6)
    K.lathe('coping', x, y, [(0.6, z + 3.6), (0.9, z + 3.9), (0.45, z + 4.3), (1.25, z + 5.1), (1.35, z + 5.9), (0.9, z + 6.5), (1.15, z + 6.7), (0.1, z + 7.2)], seg=12)

for s in (-1, 1):
    xa = s * XW; AX = -1 if xa > 0 else 1          # AX: direction from this cascade toward the central axis
    # -------- causeway + channel, pool by pool (k = 0..11), y from YT down to YH
    for k in range(NC):
        ya = YT - LP * k; yb = YT - LP * (k + 1); w = LV[k]; top = w + 1.5
        ga = gz(xa + s * 0, ya); gb = gz(xa, yb)
        o_ = CH + WALL + WALK
        # causeway body with grass banks (1:2) both sides; walks on top
        for side in (-1, 1):
            xin = xa + side * (CH + WALL); xout = xa + side * o_
            secs = []
            for yy, gg in ((ya, ga), (yb, gb)):
                h = max(top - 0.3 - gg, 0.5); xb_ = xout + side * 2.0 * h
                secs.append([(xin, yy, gg - 1.0), (xb_, yy, gg - 1.0), (xout, yy, top - 0.3), (xin, yy, top - 0.3)] if side > 0 else
                            [(xin, yy, gg - 1.0), (xin, yy, top - 0.3), (xout, yy, top - 0.3), (xb_, yy, gg - 1.0)])
            # grass bank surface + gravel walk as separate skins over the prism
            K.prism('grass', secs[0], secs[1])
            K.poly('gravel', [(xin, ya, top - 0.25), (xout, ya, top - 0.25), (xout, yb, top - 0.25), (xin, yb, top - 0.25)] if side > 0 else
                             [(xout, ya, top - 0.25), (xin, ya, top - 0.25), (xin, yb, top - 0.25), (xout, yb, top - 0.25)])
            # channel side wall + coping
            K.box('stone', xa + side * CH, xa + side * (CH + WALL), yb, ya, min(ga, gb) - 1.0, top)
            K.box('coping', xa + side * (CH - 0.3), xa + side * (CH + WALL + 0.3), yb, ya, top, top + 0.6)
        # channel bed under the pool
        K.box('floor', xa - CH, xa + CH, yb, ya, min(ga, gb) - 1.0, w - 1.6)
        WK.rect('water', xa - CH, xa + CH, yb, ya, w)
        # the fall at yb: sill + white-water sheet + foam + spray (from LV[k] to LV[k+1]); the 12th falls into the head basin
        wn = LV[k + 1]
        K.box('coping', xa - CH, xa + CH, yb - 0.4, yb + 1.6, wn - 1.0, w - 0.15)
        nseg = 5
        for j in range(nseg):
            t0, t1 = j / nseg, (j + 1) / nseg
            def P(t, x): return (x, yb - 0.4 - 2.6 * t ** 0.7, w + 0.15 - (w - wn + 0.15) * t * t)
            WK.poly('foam', [P(t0, xa - CH), P(t0, xa + CH), P(t1, xa + CH), P(t1, xa - CH)])
        WK.box('foam', xa - CH, xa + CH, yb - 8.0, yb - 2.4, wn - 0.05, wn + 0.35)
        for j in range(40):
            WK.drop('spray', (xa + RNG.uniform(-CH + 0.5, CH - 0.5), yb - RNG.uniform(1.0, 6.5), wn + RNG.uniform(0.1, 2.0)), RNG.uniform(0.08, 0.18))
        # urn piers at the fall on both walls
        for side in (-1, 1):
            urn(xa + side * (CH + WALL / 2), yb, max(w, wn) + 2.1 if False else top + 0.6); URN_PIERS += 1
        # steps on the walks at each fall (riser of DROP)
        for side in (-1, 1):
            xin = xa + side * (CH + WALL); xout = xa + side * o_
            K.box('coping', xin, xout, yb - 1.4, yb + 0.0, wn + 1.2, top - 0.25)
    # -------- head basin (120 ft broad) on a stone-walled platform, arcade face at YF
    top = WH + 1.5
    gH = min(gz(xa + s * 50, YH), gz(xa - s * 50, YH)); gF = ZW - 3.0
    K.box('floor', xa - AW, xa + AW, YF, YH, gF, WH - 1.6)
    WK.rect('water', xa - AW, xa + AW, YF + 0.5, YH, WH)
    for side in (-1, 1):
        xo = xa + side * AW
        K.box('stone', xo, xo + side * 3.5, YF, YH + 3.5, gF, top)
        K.box('coping', xo - side * 0.3, xo + side * 3.8, YF - 0.3, YH + 3.8, top, top + 0.8)
        # north wall of the head basin either side of the channel mouth
        K.box('stone', xa + side * (CH + WALL), xo + side * 3.5, YH, YH + 3.5, gH - 1.0, top)
        K.box('coping', xa + side * (CH + WALL), xo + side * 3.8, YH - 0.3, YH + 3.8, top, top + 0.8)
        # big end piers of the arcade with urns
        K.box('stone', xo - side * 0.5, xo + side * 5.5, YF - 2.5, YF + 6.0, gF, top + 3.0)
        K.box('coping', xo - side * 0.8, xo + side * 5.8, YF - 2.8, YF + 6.3, top + 3.0, top + 3.8)
        urn(xo + side * 2.5, YF + 1.75, top + 3.8)
        # grass bank behind the side walls down to the park ground
        for yy0, yy1 in ((YF, YF + 20), (YF + 20, YH + 3.5)):
            g0, g1 = gz(xo + side * 6, yy0), gz(xo + side * 6, yy1)
            h0, h1 = max(top - g0, 0.5), max(top - g1, 0.5)
            sa = [(xo + side * 3.5, yy0, g0 - 1), (xo + side * (3.5 + 2 * h0), yy0, g0 - 1), (xo + side * 3.5, yy0, top - 0.6)]
            sb = [(xo + side * 3.5, yy1, g1 - 1), (xo + side * (3.5 + 2 * h1), yy1, g1 - 1), (xo + side * 3.5, yy1, top - 0.6)]
            if side < 0: sa, sb = [sa[0], sa[2], sa[1]], [sb[0], sb[2], sb[1]]
            K.prism('grass', sa, sb)
    # -------- the arcade: 11 round arches, pier 3 ft, opening ~7.6 ft, recess 2.5 ft, cornice; lip at WH
    NA = 11; PIER = 3.0; OPEN = (2 * AW - (NA + 1) * PIER) / NA
    zs0 = ZW - 3.0; spring = ZW + 3.2; rad = OPEN / 2; zc = WH - 0.2
    K.box('recess', xa - AW, xa + AW, YF + 2.5, YF + 4.0, zs0, zc)                 # back of the arch recesses
    K.box('stone', xa - AW, xa + AW, YF + 4.0, YF + 8.0, zs0, zc)                  # wall core
    for i in range(NA + 1):
        px = xa - AW + i * (PIER + OPEN)
        K.box('stone', px, px + PIER, YF, YF + 2.5, zs0, zc)                        # piers
    for i in range(NA):
        x0 = xa - AW + PIER + i * (PIER + OPEN); xc = x0 + rad
        n = 8                                                                       # arch spandrel: face strip above the semicircle
        for j in range(n):
            a0, a1 = math.pi * j / n, math.pi * (j + 1) / n
            p0 = (xc - rad * math.cos(a0), spring + rad * math.sin(a0)); p1 = (xc - rad * math.cos(a1), spring + rad * math.sin(a1))
            K.prism('stone', [(p0[0], YF, p0[1]), (p0[0], YF, zc), (p0[0], YF + 2.5, zc), (p0[0], YF + 2.5, p0[1])],
                             [(p1[0], YF, p1[1]), (p1[0], YF, zc), (p1[0], YF + 2.5, zc), (p1[0], YF + 2.5, p1[1])])
            K.bar('coping', (p0[0], YF - 0.25, p0[1]), (p1[0], YF - 0.25, p1[1]), 0.7, 0.5)        # archivolt
        K.box('coping', xc - 0.6, xc + 0.6, YF - 0.45, YF + 0.2, spring + rad - 0.4, spring + rad + 1.0)   # keystone
    K.box('coping', xa - AW - 0.5, xa + AW + 0.5, YF - 1.0, YF + 8.0, zc, WH + 0.05)          # lip / cornice the water runs over
    K.box('coping', xa - AW - 0.5, xa + AW + 0.5, YF - 0.6, YF + 0.4, ZW + 2.2, ZW + 2.8)      # impost band
    # -------- the cataract veil over the arcade (semi-transparent spray + foam streaks), foot foam, spray cloud
    nseg = 8
    def V(t, x): return (x, YF - 1.1 - 4.5 * t ** 0.6, WH + 0.1 - (WH + 0.1 - ZW) * t * t)
    for j in range(nseg):
        t0, t1 = j / nseg, (j + 1) / nseg
        WK.poly('veil', [V(t0, xa - AW + 0.3), V(t0, xa + AW - 0.3), V(t1, xa + AW - 0.3), V(t1, xa - AW + 0.3)])
    xx = xa + AW            # (r1 foam ribbons dropped: the veil material carries the streaks)
    while xx < xa + AW - 1.0:                                                         # streaks: foam ribbons, gaps between
        wst = RNG.uniform(0.25, 0.9)
        for j in range(nseg):
            t0, t1 = j / nseg, (j + 1) / nseg
            a, b = V(t0, xx), V(t1, xx); c, d = V(t1, xx + wst), V(t0, xx + wst)
            off = (0, -0.15, 0)
            WK.poly('foam', [tuple(p + q for p, q in zip(a, off)), tuple(p + q for p, q in zip(d, off)), tuple(p + q for p, q in zip(c, off)), tuple(p + q for p, q in zip(b, off))])
        xx += wst + RNG.uniform(2.0, 5.5)
    WK.box('foam', xa - AW, xa + AW, YF - 14.0, YF - 4.0, ZW - 0.05, ZW + 0.55)
    for j in range(900):
        WK.drop('spray', (xa + RNG.uniform(-AW, AW), YF - RNG.uniform(3.0, 15.0), ZW + RNG.uniform(0.1, 1.0) * RNG.uniform(0.2, 4.5)), RNG.uniform(0.07, 0.16))
    WK.box('foam', xa - AW - 0.5, xa + AW + 0.5, YF - 1.6, YF - 0.9, WH - 0.35, WH + 0.25)                 # white lip where it breaks
    # -------- cataract pool where the arcade stands beyond the r05 basin outline (kerb + bed + water)
    K.box('floor', xa - AW - 3.5, xa + AW + 3.5, POOL_S, YF, ZW - 1.7, ZW - 1.1)
    WK.rect('water', xa - AW - 3.5, xa + AW + 3.5, POOL_S, YF, ZW + 0.01)
    xk = xa + AX * (AW + 3.5)                                                        # axis-side kerb (beyond the r05 basin tip)
    K.box('stone', xk, xk + AX * 3.0, POOL_S - 3.0, YF, ZW - 3.0, ZW + 0.6)
    K.box('coping', xk - AX * 0.2, xk + AX * 3.3, POOL_S - 3.3, YF, ZW + 0.6, ZW + 1.0)
    # south kerb from the r05 rim (x ~ +-152) to the outer kerb
    xr = -AX * 150.0
    K.box('stone', xr, xk, POOL_S - 3.0, POOL_S, ZW - 3.0, ZW + 0.6)
    K.box('coping', xr, xk + AX * 3.3, POOL_S - 3.3, POOL_S + 0.2, ZW + 0.6, ZW + 1.0)

    # -------- 2. iron Water Temple on the r05 footprint (x_ +-20, YJ-6 .. YJ+34): podium, arcaded screen, dome
    yc = YJ + 14.0; zb = ZJ
    K.box('stone', xa - 23, xa + 23, yc - 23, yc + 23, zb - 2.0, zb + 4.0)
    K.box('coping', xa - 23.6, xa + 23.6, yc - 23.6, yc + 23.6, zb + 4.0, zb + 4.6)
    WK.rect('water', xa - 17, xa + 17, yc - 17, yc + 17, zb + 4.3)
    zf = zb + 4.6; ztop = zf + 24.0
    for cx in (-20, 20):
        for cy in (-20, 20):
            IK.cyl('iron', (xa + cx, yc + cy, zf), (xa + cx, yc + cy, ztop), 1.0, seg=12)                   # corner columns
            IK.box('iron', xa + cx - 1.5, xa + cx + 1.5, yc + cy - 1.5, yc + cy + 1.5, zf, zf + 1.2)
    for ax in ('x', 'y'):
        for side in (-1, 1):
            for i in range(4):
                u = -20 + i * (40 / 3)
                p = (xa + u, yc + side * 20) if ax == 'x' else (xa + side * 20, yc + u)
                if i in (1, 2): IK.cyl('iron', (p[0], p[1], zf), (p[0], p[1], zf + 17.0), 0.55, seg=10)
            for i in range(3):                                                                               # 3 round arches a side
                u0 = -20 + i * (40 / 3); r_ = 20 / 3; uc = u0 + r_
                n = 10
                for j in range(n):
                    a0, a1 = math.pi * j / n, math.pi * (j + 1) / n
                    q0 = (uc - r_ * math.cos(a0), zf + 17.0 + r_ * math.sin(a0) * 0.85); q1 = (uc - r_ * math.cos(a1), zf + 17.0 + r_ * math.sin(a1) * 0.85)
                    if ax == 'x': A_ = (xa + q0[0], yc + side * 20, q0[1]); B_ = (xa + q1[0], yc + side * 20, q1[1])
                    else: A_ = (xa + side * 20, yc + q0[0], q0[1]); B_ = (xa + side * 20, yc + q1[0], q1[1])
                    IK.bar('iron', A_, B_, 0.7, 0.9)
                # spandrel ring ornament
                if ax == 'x': IK.cyl('iron', (xa + uc, yc + side * 20 - 0.3, zf + 22.6), (xa + uc, yc + side * 20 + 0.3, zf + 22.6), 0.9, seg=10)
                else: IK.cyl('iron', (xa + side * 20 - 0.3, yc + uc, zf + 22.6), (xa + side * 20 + 0.3, yc + uc, zf + 22.6), 0.9, seg=10)
            # railing at the base between columns
            if ax == 'x': IK.bar('iron', (xa - 20, yc + side * 20, zf + 3.2), (xa + 20, yc + side * 20, zf + 3.2), 0.25, 0.25)
            else: IK.bar('iron', (xa + side * 20, yc - 20, zf + 3.2), (xa + side * 20, yc + 20, zf + 3.2), 0.25, 0.25)
    IK.box('iron', xa - 21.5, xa + 21.5, yc - 21.5, yc + 21.5, ztop, ztop + 2.4)                        # entablature
    IK.box('iron', xa - 22.3, xa + 22.3, yc - 22.3, yc + 22.3, ztop + 2.4, ztop + 3.0)                  # cornice
    for i in range(29):                                                                                  # cresting finials
        u = -21 + i * 1.5
        for (px, py) in ((xa + u, yc - 21.6), (xa + u, yc + 21.6), (xa - 21.6, yc + u), (xa + 21.6, yc + u)):
            IK.cyl('iron', (px, py, ztop + 3.0), (px, py, ztop + 4.4), 0.12, seg=4, r2=0.04)
    for (px, py) in ((xa - 20, yc - 20), (xa + 20, yc - 20), (xa - 20, yc + 20), (xa + 20, yc + 20)):        # corner urns on the cornice
        IK.lathe('iron', px, py, [(0.9, ztop + 3.0), (1.3, ztop + 4.2), (0.6, ztop + 5.2), (0.15, ztop + 6.2)], seg=10)
    zd = ztop + 3.0; RD = 18.5
    prof = [(RD, zd), (RD, zd + 1.5)] + [(RD * math.cos(a), zd + 1.5 + 14.0 * math.sin(a)) for a in [math.pi / 2 * i / 8 for i in range(1, 8)]] + [(3.2, zd + 15.0)]
    IK.lathe('glass', xa, yc, prof, seg=24)                                                              # glazed dome
    for i in range(16):                                                                                  # iron ribs
        a = 2 * math.pi * i / 16; pts = [(r * math.cos(a), r * math.sin(a), z) for r, z in prof]
        for (p0, p1) in zip(pts, pts[1:]): IK.bar('iron', (xa + p0[0] * 1.01, yc + p0[1] * 1.01, p0[2]), (xa + p1[0] * 1.01, yc + p1[1] * 1.01, p1[2]), 0.45, 0.45)
    IK.lathe('iron', xa, yc, [(3.6, zd + 15.0), (3.6, zd + 15.6), (2.8, zd + 15.6), (2.8, zd + 20.0), (3.4, zd + 20.0), (3.4, zd + 20.6),
                              (2.2, zd + 22.2), (0.5, zd + 23.6), (0.9, zd + 24.6), (0.08, zd + 27.0)], seg=12)   # lantern + finial
    # water from the temple: sheets over the podium front into pool 0 + small jets in the temple basin
    for j in range(4):
        t0, t1 = j / 4, (j + 1) / 4
        def T(t, x): return (x, YT - 0.6 - 2.0 * t ** 0.7, zb + 4.35 - (zb + 4.35 - LV[0]) * t * t)
        WK.poly('foam', [T(t0, xa - 16), T(t0, xa + 16), T(t1, xa + 16), T(t1, xa - 16)])
    WK.box('foam', xa - 18, xa + 18, YT - 7.0, YT - 1.8, LV[0] - 0.05, LV[0] + 0.35)
    for cx in (-9, 0, 9):
        pts = [(xa + cx, yc - 6 + 0, zb + 4.3 + 0), (xa + cx, yc - 10, zb + 4.3 + 6), (xa + cx, yc - 14, zb + 4.3 + 2)]
        for p0, p1 in zip(pts, pts[1:]): WK.cyl('spray', p0, p1, 0.35, seg=6, r2=0.25)
INFO['urn_piers'] = URN_PIERS

# ------------------------------------------------------------------ 5. near-lens great-basin rim jets, rebuilt finer
for p0, p1 in RIMJ:
    n = 22; pts = []
    for i in range(n + 1):
        t = i / n; pts.append(Vector((p0.x + (p1.x - p0.x) * t, p0.y + (p1.y - p0.y) * t, p0.z + (p1.z - p0.z) * t + 4 * 16 * t * (1 - t))))
    for i in range(n):
        w_ = 0.16 * (1 - 0.5 * i / n)
        if i < n * 0.4: WK.cyl('spray', tuple(pts[i]), tuple(pts[i + 1]), 0.06 * (1 - 0.4 * i / n), seg=6, cap=False)
    for i in range(260):                                                  # breaking stream: droplets spreading along the arc
        t = RNG.random() ** 0.8; j = min(int(t * n), n - 1); u = t * n - j
        c = pts[j].lerp(pts[j + 1], u); spread = 0.15 + 1.6 * t * t
        WK.drop('spray', (c.x + RNG.gauss(0, spread), c.y + RNG.gauss(0, spread), c.z + RNG.gauss(0, spread * 0.6)), RNG.uniform(0.03, 0.08))

K.done('cp042_cascades_causeway_arcade_stone'); WK.done('cp042_cascades_water_running'); IK.done('cp042_water_temples_iron_glass')

# ------------------------------------------------------------------ 6. visitors
pp = bpy.data.objects['ppl57_waterworks_visitors']; mwp = pp.matrix_world
drop = []
for vv in pp.data.vertices:
    p = (mwp @ vv.co) / FT
    for s in (-1, 1):
        xa = s * XW
        if (abs(p.x - xa) < CH + WALL + WALK + 30 and YH - 2 <= p.y <= YJ + 40) or (abs(p.x - xa) < AW + 12 and POOL_S - 6 <= p.y <= YH + 6):
            drop.append(vv.index); break
pme = pp.data.copy(); pme.name = pp.data.name + '_cp042'
bq = bmesh.new(); bq.from_mesh(pme); bq.verts.ensure_lookup_table()
bmesh.ops.delete(bq, geom=[bq.verts[i] for i in drop], context='VERTS'); bq.to_mesh(pme); bq.free()
pn = bpy.data.objects.new(pp.name + '_cp042', pme); pn.matrix_world = mwp.copy()
for c in pp.users_collection: c.objects.link(pn)
for m_ in pp.modifiers:
    nm_ = pn.modifiers.new(m_.name, m_.type)
    if m_.type == 'NODES': nm_.node_group = m_.node_group
for k_ in pp.keys():
    try: pn[k_] = pp[k_]
    except Exception: pass
pn['people_count'] = len(pme.vertices); pn['cp042_mesh_copy_of'] = pp.name; hide(pp)
INFO['pv57_points_dropped'] = len(drop); INFO['pv57_points_kept'] = len(pme.vertices)

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o
people = []
def put(name, role, pose, x, y, z, rz, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]; link(o); o.location = (x * FT, y * FT, z * FT); o.rotation_euler = (0, 0, rz)
    o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
ROLES = ('1850s_lady', '1850s_lady', '1850s_gentleman', '1850s_gentleman', '1850s_lady', '1850s_gentleman', '1850s_girl', '1850s_boy')
n = 0; nearest = 1e9
def face_to(x, y, tx, ty): return math.atan2(ty - y, tx - x) + math.pi / 2     # people_lib local -y faces forward
for s in (-1, 1):
    xa = s * XW; AX = -1 if xa > 0 else 1
    for k in range(1, NC):
        ya = YT - LP * k; yb = YT - LP * (k + 1); top = LV[k] + 1.5 - 0.25
        for side in (-1, 1):
            for j in range(RNG.choice((1, 2, 2, 3))):
                y = RNG.uniform(yb + 3, ya - 3); x = xa + side * (CH + WALL + RNG.uniform(2.0, WALK - 2.0))
                d = (Vector((x, y, top)) - CAMP).length * FT
                if d < 30: continue
                role = ROLES[RNG.randrange(len(ROLES))]
                pose = 'standing' if RNG.random() < 0.55 else ('pointing' if RNG.random() < 0.3 else 'walking')
                rz = face_to(x, y, xa, y) + RNG.uniform(-0.5, 0.5) if pose != 'walking' else (0.0 if RNG.random() < 0.5 else math.pi) + RNG.uniform(-0.2, 0.2)
                put(f'cp042_visitor_{n:03d}', role, pose, x, y, top, rz, 1856420 + n * 11, 'mid' if d < 90 else 'crowd'); n += 1; nearest = min(nearest, d)
    # at the cataract-pool kerb (axis side) and on the head-basin walls, watching the fall
    for j in range(10):
        y = RNG.uniform(YF - 4, YH - 4); x = xa + AX * (AW + 3.5 + 2 * (WH + 1.5 - ZW) + RNG.uniform(3.0, 14.0)); z = gz(x, y)
        d = (Vector((x, y, z)) - CAMP).length * FT
        if d < 60: continue
        role = ROLES[RNG.randrange(len(ROLES))]
        put(f'cp042_visitor_{n:03d}', role, 'standing' if RNG.random() < 0.7 else 'pointing', x, y, z, face_to(x, y, xa, YF) + RNG.uniform(-0.4, 0.4), 1856420 + n * 11, 'mid' if d < 90 else 'crowd'); n += 1
        nearest = min(nearest, d)
INFO['people_lib_visitors'] = len(people); INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP042 BUILT', INFO, 'hidden', HIDDEN)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP042 SAVED', OUT)
