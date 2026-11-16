"""CP001 CANDIDATE (2026-11-16): 'The glow on the hill' — 30 November 1936, evening, seen from the park.

usage: blender -b rounds/sydenham-1936-r18b.blend -P scripts/candidate_cp001_glow.py [-- out.blend]
       (env CP001_NOSAVE=1: build in memory only)
Opens the live CP001 round (never writes it). The live hero (renders/r18_1936_CAM_CP001_prologue_distant_35mm.png) shows the
1936 palace in flat midday sun with an empty park and the 1866-lost north transept frame still standing; the storyboard asks for
'30 November 1936, evening: an orange glow reveals part of the palace silhouette beyond spectators; withhold the collapse'.
Adds dated collection SY36_prologue_glow__30Nov1936_c1945 (cp_state SY36-1936_30Nov1936_evening_precollapse) and:
  1. hides (never deletes) frame_SY_north_transept__lost1866 (storyboard: keep North Transept absent; burnt 30 Dec 1866, R);
  2. night world + faint moonlight from the east behind the ridge (moon ~16.5 d old, waning gibbous, U strength);
  3. an interior fire in the central-transept front office area spreading down the south (Sydenham) half of the nave,
     flames still inside the glass (glow, not collapse), interior blackbody lights;
  4. a fire-lit smoke column leaning south-east (wind 'freshly from the northwest');
  5. 1930s spectators (people_lib v3.4 1930s_man / 1930s_woman) on the lower park slope, backs to the lens.
Cameras NOT moved, exposure NOT changed (Filmic, -1.0 EV as the live blend). Units metres in the blend; feet in DEPARTURES.
Sources: storyboard CP001; Crystal Palace Foundation 'Disaster strikes, 1936' (Buckland saw a red glow c.7 pm; small fire in the
office area in the centre transept; first call 7:59 pm); London Walks 30 Nov (wind freshly from the NW, fire blown from the front
of the transept to the back and down the south-west wing; glow 'like a brilliant sunset'; smoke clouds to double the tower
height); Wikipedia 'Crystal Palace fire' (100,000 came to Sydenham Hill to watch; women's cloakroom).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view as w2c

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP001_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1936-r18b_cp001glow.blend')
STATE = 'SY36-1936_30Nov1936_evening_precollapse'
RNG = random.Random(301136)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP001_prologue_distant_35mm']
COLL = 'SY36_prologue_glow__30Nov1936_c1945'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = 'fire start centre-transept office area c.7pm R (CPF); NW wind R (London Walks); spectators R (100,000, Wikipedia), positions I; flame extent/time I'

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o

# ------------------------------------------------------------------ 1. north transept stub hidden (lost 1866)
HIDDEN = []
for nm in ('frame_SY_north_transept__lost1866',):
    o = bpy.data.objects.get(nm)
    if o and not o.hide_render:
        o.hide_render = True; o.hide_viewport = True; o['cp001_hidden_by_candidate'] = True; HIDDEN.append(nm)

# ------------------------------------------------------------------ 1b. drained south great basin (Corinthian FC ground 1922-36): no silt pool at the lens
# The lens stands inside the south great basin (x -274..-42, y -662..-534 m) 0.28 m above its dry-silt plane and 0.84 m above the
# basin floor stone, so the live frame's lower 40 % is a flat beige silt plane. By 1936 the basin had long been drained for the
# football ground (FA Cup 1895-1914; Corinthian FC home 1922-36, R). Mesh COPIES drop (a) the south-basin silt polygon and (b) the
# south-basin floor faces + the centre-fountain tazza/urns; originals hidden, not deleted. The park_slope grass (park_grass_r18)
# under the basin becomes the visible ground, 1.6 m below the lens as states.py intended. Rim walls/coping kept. North basin untouched.
SB = (-274.5, -41.5, -662.5, -533.5); SBC = Vector((-158.0, -598.0))
def inside(c): return SB[0] <= c.x <= SB[1] and SB[2] <= c.y <= SB[3]
def mesh_copy_drop(name, pred):
    o = bpy.data.objects[name]; me = o.data.copy(); me.name = name + '_cp001'
    bmc = bmesh.new(); bmc.from_mesh(me); mw = o.matrix_world
    kill = [f for f in bmc.faces if pred(f, mw)]; n = len(kill)
    bmesh.ops.delete(bmc, geom=kill, context='FACES'); bmc.to_mesh(me); bmc.free()
    no = bpy.data.objects.new(name + '_cp001', me); no.matrix_world = mw.copy()
    for c in o.users_collection: c.objects.link(no)
    no['cp_state'] = STATE; no['cp001_mesh_copy_of'] = name
    o.hide_render = True; o.hide_viewport = True; o['cp001_hidden_by_candidate'] = True; HIDDEN.append(name)
    return n
def pw(f, mw):
    c = mw @ f.calc_center_median(); return inside(c) and abs(c.z + 45.02) < 0.05
def ps(f, mw):
    c = mw @ f.calc_center_median()
    if not inside(c): return False
    if all((mw @ v.co).z < -45.85 for v in f.verts): return True                 # basin floor
    return (c.xy - SBC).length < 35.0                                            # centre tazza / urns
NW = mesh_copy_drop('park_basins_water', pw); NS = mesh_copy_drop('park_basins_stone', ps)
print('CP001 hidden', HIDDEN, 'silt faces dropped', NW, 'stone faces dropped', NS)

# ------------------------------------------------------------------ 2. night world + moon
w = sc.world; nt = w.node_tree; n = nt.nodes
bg = next(x for x in n if x.bl_idname == 'ShaderNodeBackground')
for lk in list(nt.links):
    if lk.to_node == bg: nt.links.remove(lk)
tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'], sep.inputs[0])
rp = n.new('ShaderNodeValToRGB'); cr = rp.color_ramp
cr.elements[0].position = 0.0; cr.elements[0].color = (0.020, 0.012, 0.010, 1)      # below horizon (unused, ground covers)
cr.elements[1].position = 0.10; cr.elements[1].color = (0.0045, 0.0055, 0.014, 1)   # night zenith
e = cr.elements.new(0.012); e.color = (0.040, 0.020, 0.012, 1)                       # warm horizon (London + fire skyglow, I)
nt.links.new(sep.outputs['Z'], rp.inputs[0]); nt.links.new(rp.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 1.0
sun = next(o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN')
sun.data.energy = 0.035; sun.data.color = (0.62, 0.72, 1.0)
sun.rotation_euler = (math.radians(90 - 18), 0, math.radians(180))   # light travelling -Y: moon low in the east behind the ridge
sc.cycles.volume_step_rate = 4.0; sc.cycles.volume_max_steps = 256

# ------------------------------------------------------------------ 3. interior fire (inside the glass; no collapse)
def flame_mat(name, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    for x in list(N): N.remove(x)
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission'); tr = N.new('ShaderNodeBsdfTransparent'); mx = N.new('ShaderNodeMixShader')
    geo = N.new('ShaderNodeNewGeometry'); mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 1.0, 0.3)
    L.new(geo.outputs['Position'], mp.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 8.0; L.new(mp.outputs[0], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.40; ramp.color_ramp.elements[1].position = 0.66; L.new(nz.outputs['Fac'], ramp.inputs[0])
    at = N.new('ShaderNodeAttribute'); at.attribute_name = 'hfac'
    inv = N.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; L.new(at.outputs['Fac'], inv.inputs[1])
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; L.new(inv.outputs[0], mul.inputs[0]); L.new(ramp.outputs['Color'], mul.inputs[1])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 2300; mr.inputs['To Max'].default_value = 1300; L.new(at.outputs['Fac'], mr.inputs['Value'])
    bb = N.new('ShaderNodeBlackbody'); L.new(mr.outputs['Result'], bb.inputs['Temperature'])
    L.new(bb.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = strength
    L.new(mul.outputs[0], mx.inputs[0]); L.new(tr.outputs[0], mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs['Surface'])
    try: m.surface_render_method = 'BLENDED'
    except Exception: pass
    return m
FLM = flame_mat('cp001_interior_flames', 22.0)
bm = bmesh.new(); hl = bm.verts.layers.float.new('hfac')
def tongue(x, y, z, r, h, seg=9):
    ring = [bm.verts.new((x + r * math.cos(2 * math.pi * i / seg), y + r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)]
    top = bm.verts.new((x + RNG.uniform(-0.15, 0.15) * h, y + RNG.uniform(0, 0.12) * h, z + h))
    for v in ring: v[hl] = 0.0
    top[hl] = 1.0
    for i in range(seg): bm.faces.new((ring[i], ring[(i + 1) % seg], top))
NT = 0
# fire seat: central transept front office area (x -18..18, y -62..-30), spreading back (+y) and down the south half of the nave (-x), I
for i in range(46):
    x = RNG.uniform(-17, 17); y = RNG.uniform(-58, 30); zb = 0.0 if RNG.random() < 0.75 else 7.5
    tongue(x, y, zb, RNG.uniform(1.4, 3.2), RNG.uniform(5, 16) * (1.25 if y < -25 else 1.0)); NT += 1
for i in range(70):
    x = -18 - abs(RNG.gauss(0, 55)); y = RNG.uniform(-44, 40)
    if x < -150: continue
    k = math.exp(-((x + 18) / 75) ** 2)
    zb = 0.0 if RNG.random() < 0.7 else 7.5
    tongue(x, y, zb, RNG.uniform(1.0, 2.6), RNG.uniform(3, 11) * (0.5 + k)); NT += 1
for i in range(10):                                         # first spread across the crossing to the north half (lighter, I)
    x = RNG.uniform(18, 45); y = RNG.uniform(-40, 30); tongue(x, y, 0.0, RNG.uniform(0.8, 1.8), RNG.uniform(2, 6)); NT += 1
me = bpy.data.meshes.new('cp001_interior_flames'); bm.to_mesh(me); bm.free(); me.materials.append(FLM)
fo = bpy.data.objects.new('cp001_interior_flames', me); sc.collection.objects.link(fo); link(fo); fo.visible_shadow = False
# interior fire light (blackbody ~1700-1900 K)
LIGHTS = [(0, -45, 6, 0.6e6), (0, -10, 10, 0.5e6), (0, 25, 12, 0.3e6), (-40, -15, 6, 0.35e6), (-75, 0, 6, 0.2e6),
          (-110, 5, 6, 0.1e6), (30, -10, 5, 0.08e6), (0, -30, 30, 0.3e6), (-20, 0, 70, 0.5e6)]   # last: lights the smoke base
for i, (x, y, z, p) in enumerate(LIGHTS):
    ld = bpy.data.lights.new(f'cp001_fire_light_{i}', 'POINT'); ld.energy = p; ld.shadow_soft_size = 6.0
    ld.color = (1.0, 0.42, 0.12)                                 # ~1800 K blackbody, as RGB (I)
    lo = bpy.data.objects.new(f'cp001_fire_light_{i}', ld); lo.location = (x, y, z); sc.collection.objects.link(lo); link(lo)

# ------------------------------------------------------------------ 4. smoke column lit from below, leaning SE (-x, +y)
def smoke_mat(name, density, emit, colr):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    for x in list(N): N.remove(x)
    out = N.new('ShaderNodeOutputMaterial'); pv = N.new('ShaderNodeVolumePrincipled'); tcn = N.new('ShaderNodeTexCoord')
    sub = N.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    s2 = N.new('ShaderNodeVectorMath'); s2.operation = 'SCALE'; s2.inputs['Scale'].default_value = 2.0
    gr = N.new('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'
    L.new(tcn.outputs['Generated'], sub.inputs[0]); L.new(sub.outputs[0], s2.inputs[0]); L.new(s2.outputs[0], gr.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.03; nz.inputs['Detail'].default_value = 10.0; nz.inputs['Roughness'].default_value = 0.68
    L.new(tcn.outputs['Object'], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.44; ramp.color_ramp.elements[1].position = 0.72; L.new(nz.outputs['Fac'], ramp.inputs[0])
    pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6; L.new(gr.outputs['Fac'], pw.inputs[0])
    mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L.new(pw.outputs[0], mu.inputs[0]); L.new(ramp.outputs['Color'], mu.inputs[1])
    md = N.new('ShaderNodeMath'); md.operation = 'MULTIPLY'; md.inputs[1].default_value = density; L.new(mu.outputs[0], md.inputs[0])
    L.new(md.outputs[0], pv.inputs['Density']); pv.inputs['Color'].default_value = (*colr, 1)
    if emit > 0:
        me_ = N.new('ShaderNodeMath'); me_.operation = 'MULTIPLY'; me_.inputs[1].default_value = emit; L.new(mu.outputs[0], me_.inputs[0])
        L.new(me_.outputs[0], pv.inputs['Emission Strength']); pv.inputs['Emission Color'].default_value = (1.0, 0.36, 0.08, 1)
    L.new(pv.outputs[0], out.inputs['Volume']); return m
SMK = {}
NP = 0
NPUFF = 20
for k in range(NPUFF):
    t = k / (NPUFF - 1)
    cx = -10 - 170 * t ** 1.4 + RNG.uniform(-35, 35) * (0.4 + t); cy = 10 + 170 * t ** 1.4 + RNG.uniform(-25, 25); cz = 55 + 330 * t + RNG.uniform(-20, 20)
    r = 35 + 100 * t * RNG.uniform(0.8, 1.2)
    emit = 0.25 * (1 - t) ** 3.0 + 0.002                      # underside lit by the fire, fading with height (I)
    key = round(emit, 2)
    m = smoke_mat(f'cp001_smoke_{k:02d}', 0.030 - 0.012 * t, emit, (0.055, 0.05, 0.047))
    bmS = bmesh.new()
    bmesh.ops.create_uvsphere(bmS, u_segments=16, v_segments=10, radius=1.0,
        matrix=Matrix.Translation(Vector((cx, cy, cz))) @ Matrix.Diagonal((r * RNG.uniform(1.0, 1.35), r * RNG.uniform(0.8, 1.0), r * RNG.uniform(0.55, 0.8), 1)))
    meS = bpy.data.meshes.new(f'cp001_smoke_{k:02d}'); bmS.to_mesh(meS); bmS.free(); meS.materials.append(m)
    so = bpy.data.objects.new(f'cp001_smoke_{k:02d}', meS); sc.collection.objects.link(so); link(so); so.visible_shadow = False; NP += 1

# ------------------------------------------------------------------ 5. spectators on the lower park slope
deps = bpy.context.evaluated_depsgraph_get()
GROUND = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and
          (o.name in ('park_slope', 'terrain', 'distant_ground') or o.name.startswith('central_walk') or o.name.startswith('r18_kerb'))]
fr = CAM.data.view_frame(scene=sc)
cl = CAM.location.copy()
fwd = (CAM.matrix_world.to_quaternion() @ Vector((0, 0, -1))); fwd.z = 0; fwd.normalize()
right = Vector((fwd.y, -fwd.x, 0))
def ground(x, y):
    best = None
    for g in GROUND:
        mi = g.matrix_world.inverted(); o_ = mi @ Vector((x, y, 200.0)); d_ = (mi.to_3x3() @ Vector((0, 0, -1))).normalized()
        hit, loc, nrm, idx = g.ray_cast(o_, d_)
        if hit:
            z = (g.matrix_world @ loc).z
            best = z if best is None else max(best, z)
    return best
def put(name, role, pose, x, y, seed):
    z = ground(x, y)
    if z is None: return None
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': 'mid', 'era': '1930s'}, seed=seed)
    o = bpy.data.objects[name]; link(o)
    o.location = (x, y, z)
    tx, ty = (0.0 - x), (0.0 - y)                                 # face the burning centre transept
    tx += RNG.uniform(-60, 60)
    o.rotation_euler = (0, 0, math.atan2(tx, -ty) + math.pi)
    o['cpl_people'] = 'cpl_people_v3'
    return o
people = 0; pts = []
# (distance ahead m, lateral m) groups; keep a window clear in front of the central transept (storyboard: glow beyond spectators)
ct = w2c(sc, CAM, Vector((0, -40, 20)))
for i in range(400):
    if people >= 64: break
    d = RNG.uniform(7, 75) if RNG.random() < 0.85 else RNG.uniform(75, 140)
    lat = RNG.uniform(-0.62, 0.62) * d + RNG.uniform(-3, 3)
    p = cl + fwd * d + right * lat
    if any((p.xy - q).length < 1.1 for q in pts): continue
    v = w2c(sc, CAM, Vector((p.x, p.y, (ground(p.x, p.y) or 0) + 1.6)))
    if not (0.02 < v.x < 0.98): continue
    if d < 30 and abs(v.x - ct.x) < 0.11: continue
    role = '1930s_man' if RNG.random() < 0.6 else '1930s_woman'
    pose = 'pointing' if RNG.random() < 0.06 else ('walking' if RNG.random() < 0.08 else 'standing')
    o = put(f'cp001_spectator_{people:02d}', role, pose, p.x, p.y, 1936000 + i)
    if o is None: continue
    pts.append(p.xy.copy()); people += 1
print('CP001 BUILT tongues', NT, 'lights', len(LIGHTS), 'smoke', NP, 'spectators', people, 'nearest',
      round(min((Vector((q.x, q.y)) - cl.xy).length for q in pts), 1))

if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP001 SAVED', OUT)
