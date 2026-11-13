"""CP060 CANDIDATE (2026-11-13): SY36 external fire response, 30 November 1936 — 'Water cannot save the whole building'.

usage: blender -b rounds/sydenham-1936fire-r12.blend -P scripts/candidate_cp060_hose_crews.py [-- out.blend]
       (env CP060_NOSAVE=1: build in memory only)
Opens the FIRE round (never writes it), adds dated collection SY36_parade_hose_crews__30Nov1936 and hides (never deletes)
the crowd36_parade blocks that stand inside the CAM_CP060 frustum within 330 ft of the lens (the storyboard asks for a
'clear exterior perimeter' with a hose leading to a crew; the spectators belong to CP061). Cameras are NOT moved.
Sources (DEPARTURES D-SY-CP060-01..):
  * Storyboard CP060: firefighters work hoses outside the building; 35 mm at a clear exterior perimeter, follow a hose toward crew.
  * Science Museum Group co8223615 (Daily Herald, E. G. Malindine, 30 Nov 1936): firemen at the fire; 88 engines, 483 firefighters.
  * Manchester Guardian 1 Dec 1936 (archive repr. 2021): 'miles of wriggling hosepipes ... muddy streets' -> wet Parade, slack hose lines.
  * London Walks / contemporary accounts: 'great difficulty in obtaining adequate water pressure'; molten glass 'forcing the firemen back'
    -> branch crews stand off the facade (~40-55 ft), jets fall short/low, I.
  * LFB 2 3/4 in canvas delivery hose (R, size); branch pipe ~2.5 ft brass (I); crews of 3 on a branch (I).
Units: feet (F converts). Parade road surface ZPAR = -0.5 (dress36.py).
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view as w2c

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP060_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1936fire-r12_cp060hose.blend')
STATE = 'SY36-FIRE_30Nov1936'
ZPAR = -0.5
FACADE_Y = 156.0                 # Parade wall line (build.py wall_y(156, ...))
HOSE_R = 2.75 / 2 / 12           # R: 2 3/4 in delivery hose, charged = round
RNG = random.Random(301136)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP060_crowd_watching_35mm']

COLL = 'SY36_parade_hose_crews__30Nov1936'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]:
    sc.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = 'hose crews R (Daily Herald 30 Nov 1936); wet streets + hose R (Guardian 1 Dec 1936); positions, counts I'

def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m
M_HOSE = mat('cp060_wet_canvas_hose', (0.30, 0.26, 0.19), 0.45)       # wet canvas darkens (I)
M_BRASS = mat('cp060_branch_brass', (0.62, 0.43, 0.16), 0.3, 1.0)

def wet_road_mat():
    m = bpy.data.materials.get('cp060_wet_parade_puddles')
    if m: return m
    m = bpy.data.materials.new('cp060_wet_parade_puddles'); m.use_nodes = True; nt = m.node_tree; n = nt.nodes
    pb = n.get('Principled BSDF'); tc = n.new('ShaderNodeTexCoord'); ns = n.new('ShaderNodeTexNoise'); ns2 = n.new('ShaderNodeTexNoise')
    ns.inputs['Scale'].default_value = 0.09; ns.inputs['Detail'].default_value = 3.0
    ns2.inputs['Scale'].default_value = 1.4; ns2.inputs['Detail'].default_value = 6.0
    cr = n.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.56; cr.color_ramp.elements[1].position = 0.60
    cr.color_ramp.elements[0].color = (0.62, 0.62, 0.62, 1); cr.color_ramp.elements[1].color = (0.04, 0.04, 0.04, 1)   # trodden mud -> puddle roughness
    cc = n.new('ShaderNodeValToRGB'); cc.color_ramp.elements[0].position = 0.56; cc.color_ramp.elements[1].position = 0.60
    cc.color_ramp.elements[0].color = (0.075, 0.058, 0.042, 1); cc.color_ramp.elements[1].color = (0.014, 0.013, 0.013, 1)
    mx = n.new('ShaderNodeMath'); mx.operation = 'MULTIPLY_ADD'; mx.inputs[1].default_value = 0.15
    nt.links.new(tc.outputs['Object'], ns.inputs['Vector']); nt.links.new(tc.outputs['Object'], ns2.inputs['Vector'])
    nt.links.new(ns2.outputs['Fac'], mx.inputs[0]); nt.links.new(ns.outputs['Fac'], mx.inputs[2])
    nt.links.new(mx.outputs[0], cr.inputs['Fac']); nt.links.new(mx.outputs[0], cc.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], pb.inputs['Roughness']); nt.links.new(cc.outputs['Color'], pb.inputs['Base Color'])
    return m

HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp060_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# ------------------------------------------------------------------ 0. clear the perimeter: crowd blocks in the CP060 frustum < 330 ft
for o in list(bpy.data.objects):
    if o.name.startswith('crowd36_parade') and not o.hide_render:
        cen = o.matrix_world @ (sum((Vector(b) for b in o.bound_box), Vector()) / 8)
        v = w2c(sc, CAM, cen); d = (cen - CAM.location).length / F
        if v.z > 0 and -0.1 < v.x < 1.1 and d < 330: hide(o)
pl = bpy.data.objects.get('police_line_parade')
if pl: hide(pl)                # one object across the Parade; it fronted the hidden crowd (CP058 fire-r12 side effect, reported)
print('CP060 hidden', len(HIDDEN))

# ------------------------------------------------------------------ helpers: screen column u -> ground point at world y
cl = CAM.location / F
fr = CAM.data.view_frame(scene=sc); tr, br, bl, tl = fr
def ground_ray(u, v):
    p = CAM.matrix_world @ (bl + (br - bl) * u + (tl - bl) * v); d = (p - CAM.location)
    t = (ZPAR * F - CAM.location.z) / d.z; return (CAM.location + d * t) / F
def at(u, y):
    g = ground_ray(u, 0.08); nad = Vector((cl.x, cl.y, ZPAR)); d = g - nad
    t = (y - nad.y) / d.y; return Vector((nad.x + d.x * t, nad.y + d.y * t, ZPAR))

def curve_obj(name, pts, r, m, radii=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r * F; cu.bevel_resolution = 2; cu.resolution_u = 8
    sp = cu.splines.new('NURBS' if len(pts) > 3 else 'POLY'); sp.points.add(len(pts) - 1)
    for i, (p, q) in enumerate(zip(sp.points, pts)):
        p.co = (q[0] * F, q[1] * F, q[2] * F, 1)
        if radii: p.radius = radii[i]
    if sp.type == 'NURBS': sp.use_endpoint_u = True; sp.order_u = 3
    cu.materials.append(m); o = bpy.data.objects.new(name, cu); col.objects.link(o); o['cp_state'] = STATE; return o

def snake(a, b, n, wig, rng, lift=HOSE_R):
    a, b = Vector(a), Vector(b); d = b - a; L = d.length; nrm = Vector((-d.y, d.x, 0)).normalized(); pts = []
    ph = rng.uniform(0, 6.28)
    for i in range(n + 1):
        t = i / n; w = math.sin(math.pi * t) * (wig * math.sin(ph + t * rng.uniform(5, 8)) + rng.uniform(-wig, wig) * 0.3)
        q = a + d * t + nrm * w; pts.append((q.x, q.y, ZPAR + lift))
    return pts

def put(name, role, pose, p, face, seed, lod='mid'):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1930s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)
    o.location = (p.x * F, p.y * F, p.z * F)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]))       # base meshes face local -Y
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'
    return o

# ------------------------------------------------------------------ 1. wet Parade (puddles reflect the fire)
bm = bmesh.new()
X0, X1, Y0, Y1 = -560.0, -60.0, FACADE_Y + 2.0, 345.0
vs = [bm.verts.new(Vector(c) * F) for c in [(X0, Y0, ZPAR + 0.03), (X1, Y0, ZPAR + 0.03), (X1, Y1, ZPAR + 0.03), (X0, Y1, ZPAR + 0.03)]]
bm.faces.new(vs); me = bpy.data.meshes.new('cp060_wet_parade'); bm.to_mesh(me); bm.free()
wet = bpy.data.objects.new('cp060_wet_parade', me); col.objects.link(wet); me.materials.append(wet_road_mat()); wet['cp_state'] = STATE

# ------------------------------------------------------------------ 2. branch crews: 3 firemen on each branch, standing off the facade
CREWS = [(0.26, 0.172), (0.50, 0.160), (0.76, 0.150)]       # (screen u, v) -> ground point, ~100-140 ft from the lens (I)
SRC = [(0.40, -0.04), (0.55, -0.04), (0.70, -0.04)]           # hoses enter from below the frame (pumps on the Parade behind the lens, I)
crew_pts = []; hoses = []; jets = []; men = 0
for k, ((u, y), (su, sv)) in enumerate(zip(CREWS, SRC)):
    p = ground_ray(u, y); p.z = ZPAR
    fwd = (CAM.matrix_world.to_3x3() @ Vector((0, 0, -1))); fwd.z = 0; fwd.normalize()
    aim = (fwd + Vector((0, -0.35, 0)) + Vector((RNG.uniform(-0.12, 0.12), RNG.uniform(-0.12, 0.12), 0))).normalized()   # away from the lens, into the front
    back = -aim
    side = Vector((-aim.y, aim.x, 0))
    # branch: held at hip/chest by the branchman, nozzle 2.5 ft ahead
    noz0 = p + aim * 1.2 + Vector((0, 0, 3.4)); noz1 = noz0 + aim * 2.5 + Vector((0, 0, 0.55))
    curve_obj(f'cp060_branch_{k}', [tuple(noz0), tuple(noz1)], 0.09, M_BRASS)
    put(f'cp060_branchman_{k}', '1930s_fireman', 'hauling', p, (aim.x, aim.y), 6060 + k * 10)
    put(f'cp060_backup_{k}a', '1930s_fireman', 'hauling', p + back * 4.5 + side * 0.9, (aim.x, aim.y), 6061 + k * 10)
    put(f'cp060_backup_{k}b', '1930s_fireman', 'hauling', p + back * 9.0 - side * 0.6, (aim.x, aim.y), 6062 + k * 10)
    men += 3
    # hose: nozzle tail -> along the crew -> back across the wet road to the frame bottom
    s = ground_ray(su, sv)
    tail = p + back * 12.0
    pts = [(noz0.x, noz0.y, noz0.z - 0.4), (p.x + back.x * 2, p.y + back.y * 2, 2.6), (p.x + back.x * 5, p.y + back.y * 5, 2.4),
           (p.x + back.x * 8, p.y + back.y * 8, 1.0), (tail.x, tail.y, ZPAR + HOSE_R)]
    pts += snake(tail, s, 9, 6.0, RNG)[1:]
    hoses.append(pts)
    # jet: pressure is poor -> a short, low arc that breaks into spray before the glazing (I)
    reach = RNG.uniform(70, 85)                                  # low-pressure throw, falls short of the burning front (I)
    tgt = noz1 + aim * reach; tgt.z = ZPAR + 1.0
    jet = []; n = 18; peak = RNG.uniform(16, 21)
    for i in range(n + 1):
        t = i / n; q = noz1.lerp(tgt, t); q.z += 4 * peak * t * (1 - t); jet.append(tuple(q))
    jets.append(jet)
    crew_pts.append(p)
    print('CP060 crew', k, 'at', tuple(round(c) for c in p), 'dist', round((p - cl).length))
for i, h in enumerate(hoses):
    curve_obj(f'cp060_hose_{i}', h, HOSE_R, M_HOSE)
# slack spare lines (uncharged, flat) wriggling across the road (Guardian: 'miles of wriggling hosepipes')
for i in range(4):
    a = ground_ray(RNG.uniform(0.05, 0.95), -0.05); b = at(RNG.uniform(0.05, 0.95), RNG.uniform(205, 230))
    curve_obj(f'cp060_slack_hose_{i}', snake(a, b, 10, 9.0, RNG, lift=0.05), 0.07, M_HOSE)
def jet_water_mat(name, opacity, emit):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes
    pb = n.get('Principled BSDF'); out = n.get('Material Output')
    pb.inputs['Base Color'].default_value = (0.85, 0.87, 0.9, 1); pb.inputs['Roughness'].default_value = 0.35
    pb.inputs['Emission Color'].default_value = (1.0, 0.55, 0.25, 1); pb.inputs['Emission Strength'].default_value = emit   # spray scattering fire light (I)
    tr = n.new('ShaderNodeBsdfTransparent'); lw = n.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    mm = n.new('ShaderNodeMath'); mm.operation = 'MAXIMUM'; mm.inputs[1].default_value = 1.0 - opacity
    mx = n.new('ShaderNodeMixShader'); nt.links.new(lw.outputs['Facing'], mm.inputs[0]); nt.links.new(mm.outputs[0], mx.inputs[0])
    nt.links.new(pb.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])
    try: m.surface_render_method = 'BLENDED'
    except Exception: pass
    return m
CORE = jet_water_mat('cp060_jet_core_firelit', 0.8, 0.3); SPRAY = jet_water_mat('cp060_jet_spray_firelit', 0.18, 0.18)
for i, j in enumerate(jets):
    nn = len(j); kb = int(nn * 0.62)                                   # solid stream breaks up ~60 % along the throw (I)
    curve_obj(f'cp060_jet_core_{i}', j[:kb + 1], 0.13, CORE, [1.0 + 0.8 * (i_ / kb) for i_ in range(kb + 1)])
    sp = j[kb - 1:]; ns_ = len(sp)
    curve_obj(f'cp060_jet_spray_{i}', sp, 0.25, SPRAY, [0.8 + 10.0 * (i_ / (ns_ - 1)) ** 1.3 for i_ in range(ns_)])

# ------------------------------------------------------------------ 3. a hose runner and an officer on the road (the 'follow the hose' line)
r0 = hoses[1][len(hoses[1]) // 2]; r1 = hoses[1][len(hoses[1]) // 2 + 1]
dd = Vector((r1[0] - r0[0], r1[1] - r0[1], 0)).normalized()
put('cp060_hose_runner', '1930s_fireman', 'walking', Vector((r0[0] + 2.5, r0[1], ZPAR)), (-dd.x, -dd.y), 6091)
off = at(0.64, 214.0)
put('cp060_officer', '1930s_fireman', 'pointing', off, (-0.3, -1.0), 6092)
men += 2
for o in list(col.objects):
    if o.name.startswith('cp060_') and o.type == 'MESH' and 'fireman' in str(o.get('cpl_role', '')):
        d = (o.location / F - cl).length
        if d < 44: print('CP060 WARN close figure', o.name, round(d))
print('CP060 BUILT crews', len(CREWS), 'men', men, 'hoses', len(hoses) + 4, 'jets', len(jets))

if OUT != '--nosave':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP060 SAVED', OUT)
