#!/usr/bin/env python3
"""CP071: replace flat olive slab + box ribs with Muse fan-vault bays
(true polychrome cream/red brick groin/fan vaults on octagonal columns).
PARK-NOW: keep dirt/wear floor + modern AREA lamps; KEEP_LIGHTING (no sun/world/expo).
usage: blender -b rounds/parknow-r18.blend -P scripts/improve_subway_vaults_r19.py -- rounds/parknow-r19.blend
"""
import bpy, sys, math, os
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/tmp/parknow-r19.blend'

MUSE = '/workspace/crystal-palace-park-modern/models/sy-subway-vault-bay/sy-subway-vault-bay.blend'
PITCH = 3.35
A = PITCH / 2.0
SPRINGING = 3.51
CROWN = 5.01

# Existing subway floor top (world)
FLOOR = bpy.data.objects.get('pk_subway_floor')
if FLOOR is None:
    raise SystemExit('pk_subway_floor missing')
bb = [FLOOR.matrix_world @ Vector(v) for v in FLOOR.bound_box]
z_floor = max(v.z for v in bb)  # top of floor slab
y0_old, y1_old = min(v.y for v in bb), max(v.y for v in bb)
print('floor top z', round(z_floor, 3), 'y', round(y0_old, 3), round(y1_old, 3), flush=True)

# Camera stays; we place grid so view looks down several bays (-Y)
CAM = bpy.data.objects.get('CAM_CP071_subway_interior_28mm')
cy = CAM.location.y if CAM else 69.8

# 3 rows (HE listing) × 6 bays along hall for depth in frame
NX = [-PITCH, 0.0, PITCH]
# place so camera sits mid-bay looking toward smaller Y
n_along = 6
y_first = cy - 2.5 * PITCH   # ~2.5 bays ahead of cam toward -Y end? cam looks -Y so ahead = smaller y
# Actually cam at 69.8 looking -Y: bays should span both ahead and behind for pillars framing
# Put column Ys so nearest framing columns are just ahead/beside cam
NY = [cy - 3.0 * PITCH + i * PITCH for i in range(n_along)]
# shift so we have wall at far (-Y) end shortly past first bay
print('grid X', NX)
print('grid Y', [round(y, 2) for y in NY], flush=True)

SUB = bpy.data.collections.get('G_STATION_subway')
if SUB is None:
    SUB = bpy.data.collections.new('G_STATION_subway')
    bpy.context.scene.collection.children.link(SUB)

# ---------------------------------------------------------------------------
# Remove old fake vault / rect cols / r18 box ribs / caps / bases / boards
# Keep: floor, walls (will rebuild), lights, seal, booking
# ---------------------------------------------------------------------------
KILL_PREFIXES = (
    'pk_vault_', 'pk_col_', 'pk_r18_rib', 'pk_r18_cap_', 'pk_r18_base_',
    'pk_r18_board_', 'pk_r18_lamp', 'pk_r18_string', 'pk_r18_dado',
    'pk_r18_handrail', 'pk_r18_cove', 'pk_r18_spring',
)
# also any leftover olive vault soffits by material name later
to_kill = []
for o in list(bpy.data.objects):
    if any(o.name.startswith(p) for p in KILL_PREFIXES):
        to_kill.append(o)
    elif o.name in (
        'pk_subway_vault_L', 'pk_subway_vault_R', 'pk_subway_vault_C',
        'pk_subway_soffit_L', 'pk_subway_soffit_R', 'pk_subway_ceiling',
        'pk_subway_rib_beam',
    ):
        to_kill.append(o)
for o in to_kill:
    bpy.data.objects.remove(o, do_unlink=True)
print('removed', len(to_kill), 'old subway dress objs', flush=True)

# Hide/remove old narrow side walls — rebuild wider to meet vaults
for wn in ('pk_subway_wall_L', 'pk_subway_wall_R', 'pk_subway_wall_N',
           'pk_subway_wall_S', 'pk_subway_end', 'pk_subway_back'):
    o = bpy.data.objects.get(wn)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# ---------------------------------------------------------------------------
# Append Muse Model meshes (read-only source; we copy into this blend)
# ---------------------------------------------------------------------------
PARTS = [
    'Plinth', 'BaseDrum', 'BaseRing', 'Shaft', 'CapitalScallop', 'CapitalBell',
    'FanFootRing', 'Vault',
    'RibDiag+1+1', 'RibDiag+1-1', 'RibDiag-1+1', 'RibDiag-1-1',
    'RibEdgex+1', 'RibEdgex-1', 'RibEdgey+1', 'RibEdgey-1',
]
with bpy.data.libraries.load(MUSE, link=False) as (data_from, data_to):
    want = [n for n in PARTS if n in data_from.objects]
    data_to.objects = want
print('appended', [o.name for o in data_to.objects], flush=True)

# Park the prototypes far away / hide; use as templates
PROTO = bpy.data.collections.get('MuseVaultProto') or bpy.data.collections.new('MuseVaultProto')
if PROTO.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(PROTO)
protos = {}
for o in data_to.objects:
    if o is None:
        continue
    # unlink from any auto-linked collection
    for c in list(o.users_collection):
        c.objects.unlink(o)
    PROTO.objects.link(o)
    o.hide_render = True
    o.hide_viewport = True
    o.location = (0, 0, -200)  # parked
    protos[o.name.split('.')[0]] = o  # strip .001 if any

# Ensure we keyed by base name
protos = {}
for o in PROTO.objects:
    base = o.name.split('.')[0]
    if base in PARTS:
        protos[base] = o

missing = [p for p in PARTS if p not in protos]
if missing:
    raise SystemExit(f'Missing Muse parts: {missing}')

# ---------------------------------------------------------------------------
# Dirt / wear on vault + cream brick (PARK-NOW restored-but-worn)
# ---------------------------------------------------------------------------
def add_dirt(mat_name, amount=0.18):
    M = bpy.data.materials.get(mat_name)
    if not M or not M.use_nodes:
        return
    nt = M.node_tree
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf:
        return
    # already dirtied?
    if any(n.name.startswith('DirtMix') for n in nt.nodes):
        return
    # find what feeds Base Color
    base_in = bsdf.inputs['Base Color']
    from_sock = base_in.links[0].from_socket if base_in.links else None
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.name = 'DirtMix'
    mix.inputs[0].default_value = amount  # Factor
    dirt = nt.nodes.new('ShaderNodeTexNoise')
    dirt.name = 'DirtNoise'
    dirt.inputs['Scale'].default_value = 4.5
    dirt.inputs['Detail'].default_value = 8.0
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.35
    cr.color_ramp.elements[0].color = (0.12, 0.09, 0.07, 1)
    cr.color_ramp.elements[1].position = 0.75
    cr.color_ramp.elements[1].color = (0.35, 0.28, 0.20, 1)
    nt.links.new(dirt.outputs['Fac'], cr.inputs['Fac'])
    # Factor from noise (patchy dirt)
    fac_cr = nt.nodes.new('ShaderNodeValToRGB')
    fac_cr.name = 'DirtFac'
    fac_cr.color_ramp.elements[0].position = 0.55
    fac_cr.color_ramp.elements[0].color = (0, 0, 0, 1)
    fac_cr.color_ramp.elements[1].position = 0.85
    fac_cr.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(dirt.outputs['Fac'], fac_cr.inputs['Fac'])
    nt.links.new(fac_cr.outputs['Color'], mix.inputs[0])
    if from_sock:
        nt.links.new(from_sock, mix.inputs[6])  # A_Color
    else:
        mix.inputs[6].default_value = base_in.default_value
    nt.links.new(cr.outputs['Color'], mix.inputs[7])  # B_Color
    nt.links.new(mix.outputs[2], base_in)  # Result_Color → Base Color
    # bump roughness up a touch
    bsdf.inputs['Roughness'].default_value = min(0.95, bsdf.inputs['Roughness'].default_value + 0.08)

add_dirt('VaultBrick', 0.22)
add_dirt('CreamBrick', 0.14)
add_dirt('FootRingBrick', 0.12)
add_dirt('Stone', 0.16)

# ---------------------------------------------------------------------------
# Instance bays
# ---------------------------------------------------------------------------
BAYS = bpy.data.collections.get('G_SUBWAY_VAULT_BAYS') or bpy.data.collections.new('G_SUBWAY_VAULT_BAYS')
if BAYS.name not in [c.name for c in SUB.children] and BAYS.name not in [c.name for c in bpy.context.scene.collection.children]:
    try:
        SUB.children.link(BAYS)
    except Exception:
        bpy.context.scene.collection.children.link(BAYS)

def instance_bay(ix, iy, wx, wy):
    """Duplicate all Muse parts translated so local origin (column base centre, floor z=0)
    lands at world (wx, wy, z_floor)."""
    tag = f'r19_bay_{ix}_{iy}'
    for pname, proto in protos.items():
        ob = proto.copy()  # shares mesh+materials
        ob.name = f'{tag}_{pname}'
        ob.hide_render = False
        ob.hide_viewport = False
        # proto was parked; world verts already in local Muse coords with floor at z=0
        # objects have location (0,0,-200) — reset and place
        ob.location = (wx, wy, z_floor)
        ob.rotation_euler = (0, 0, 0)
        ob.scale = (1, 1, 1)
        BAYS.objects.link(ob)

for ix, wx in enumerate(NX):
    for iy, wy in enumerate(NY):
        instance_bay(ix, iy, wx, wy)
print('instanced', len(NX) * len(NY), 'bays', flush=True)

# ---------------------------------------------------------------------------
# Side brick walls + end wall (vaults end in brick back wall)
# Walls just outside outer vault edges: ±(PITCH + A)
# ---------------------------------------------------------------------------
def mat_noise(n, c0, c1, rough=0.88, scale=28.0, bump=0.12):
    M = bpy.data.materials.get(n) or bpy.data.materials.new(n)
    M.use_nodes = True
    nt = M.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = 8.0
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.30
    cr.color_ramp.elements[0].color = (*c0, 1)
    cr.color_ramp.elements[1].position = 0.70
    cr.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = bump
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs[0], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = rough
    nt.links.new(b.outputs[0], out.inputs[0])
    M.diffuse_color = (*c0, 1)
    return M

M_wall = mat_noise('PK_SubwayWallBrick_r19', (0.62, 0.55, 0.42), (0.78, 0.70, 0.52), scale=40.0, bump=0.14)
M_wall_red = mat_noise('PK_SubwayWallRed_r19', (0.38, 0.12, 0.08), (0.50, 0.18, 0.10), scale=36.0, bump=0.12)
add_dirt('PK_SubwayWallBrick_r19', 0.20)

def box(name, x0, x1, y0, y1, z0, z1, mat_):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
          (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); SUB.objects.link(ob); return ob

wall_x = PITCH + A + 0.05   # just past outer vault edge
y_min = min(NY) - A
y_max = max(NY) + A
z_top = z_floor + CROWN + 0.35
# thick side walls
T = 0.45
box('pk_r19_wall_L', -wall_x - T, -wall_x, y_min, y_max, z_floor, z_top, M_wall)
box('pk_r19_wall_R',  wall_x, wall_x + T, y_min, y_max, z_floor, z_top, M_wall)
# far end (-Y): brick back wall — vaults terminate here
box('pk_r19_wall_end', -wall_x - T, wall_x + T, y_min - T, y_min, z_floor, z_top, M_wall)
# near end (+Y) soft close so we don't see void behind cam
box('pk_r19_wall_near', -wall_x - T, wall_x + T, y_max, y_max + T, z_floor, z_top, M_wall)
# red brick banding course at springing on walls
band_h = 0.22
zs = z_floor + SPRINGING - 0.05
box('pk_r19_band_L', -wall_x - T - 0.01, -wall_x + 0.02, y_min, y_max, zs, zs + band_h, M_wall_red)
box('pk_r19_band_R',  wall_x - 0.02, wall_x + T + 0.01, y_min, y_max, zs, zs + band_h, M_wall_red)

# ---------------------------------------------------------------------------
# Widen / dirty the floor (PARK-NOW dirt & wear — not clean Muse paving)
# ---------------------------------------------------------------------------
M_dirt = mat_noise('PK_SubwayDirtFloor_r19', (0.28, 0.24, 0.18), (0.42, 0.36, 0.28),
                   rough=0.95, scale=6.0, bump=0.18)
# patchy darker stains
nt = M_dirt.node_tree
bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
nz2 = nt.nodes.new('ShaderNodeTexNoise')
nz2.inputs['Scale'].default_value = 1.8
nz2.inputs['Detail'].default_value = 4.0
mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
mix.inputs[0].default_value = 0.35
# reconnect: existing color ramp → mix A, dark → B, noise fac
# find color ramp feeding base
from_sock = bsdf.inputs['Base Color'].links[0].from_socket
nt.links.new(from_sock, mix.inputs[6])
mix.inputs[7].default_value = (0.14, 0.11, 0.08, 1)
crf = nt.nodes.new('ShaderNodeValToRGB')
crf.color_ramp.elements[0].position = 0.45
crf.color_ramp.elements[0].color = (0,0,0,1)
crf.color_ramp.elements[1].position = 0.7
crf.color_ramp.elements[1].color = (1,1,1,1)
nt.links.new(nz2.outputs['Fac'], crf.inputs['Fac'])
nt.links.new(crf.outputs['Color'], mix.inputs[0])
nt.links.new(mix.outputs[2], bsdf.inputs['Base Color'])

box('pk_r19_floor', -wall_x - T, wall_x + T, y_min - T, y_max + T,
    z_floor - 0.12, z_floor + 0.01, M_dirt)
# hide old narrow floor under new one
FLOOR.hide_render = True
FLOOR.hide_viewport = True

# ---------------------------------------------------------------------------
# Modern lamps: keep existing AREA subway lights; reposition under vaults
# ---------------------------------------------------------------------------
# Bay centres (between columns) along centre aisle for hanging lamps
lamp_ys = []
for i in range(len(NY) - 1):
    lamp_ys.append(0.5 * (NY[i] + NY[i + 1]))
existing = [o for o in bpy.data.objects
            if o.type == 'LIGHT' and o.name.startswith('pk_subway_light')]
# hanging modern fixtures just below crown in centre aisle
lamp_z = z_floor + CROWN - 0.55
for i, ly in enumerate(lamp_ys):
    if i < len(existing):
        L = existing[i]
    else:
        light = bpy.data.lights.new(f'PK_SubLamp_r19_{i}', 'AREA')
        light.energy = 550.0
        light.color = (1.0, 0.95, 0.85)
        light.shape = 'DISK'
        light.size = 0.55
        L = bpy.data.objects.new(f'pk_subway_light_{i}', light)
        SUB.objects.link(L)
    L.location = (0.0, ly, lamp_z)
    L.rotation_euler = (0, 0, 0)
    if L.data.type == 'AREA':
        L.data.energy = 550.0
        L.data.color = (1.0, 0.95, 0.85)
        try:
            L.data.size = 0.55
        except Exception:
            pass
# hide extras
for j, L in enumerate(existing):
    if j >= len(lamp_ys):
        L.hide_render = True
# exit fill toward -Y end arch / wall
ex = bpy.data.objects.get('pk_subway_exit_fill')
if ex:
    ex.location = (0.0, y_min + 0.8, z_floor + 3.2)
    if ex.data.type == 'AREA':
        ex.data.energy = 280.0

# Small modern uplights at a few column bases (2025 restored look) — optional PARK-NOW
for i, (wx, wy) in enumerate([(0.0, NY[1]), (0.0, NY[3]), (-PITCH, NY[2]), (PITCH, NY[2])]):
    nm = f'pk_r19_uplight_{i}'
    if nm in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    light = bpy.data.lights.new(nm + '_data', 'SPOT')
    light.energy = 120.0
    light.color = (0.85, 0.92, 1.0)  # cool modern LED
    light.spot_size = math.radians(55)
    light.spot_blend = 0.45
    light.shadow_soft_size = 0.15
    ob = bpy.data.objects.new(nm, light)
    ob.location = (wx + 0.55, wy + 0.55, z_floor + 0.08)
    # aim upward
    ob.rotation_euler = (math.radians(-12), 0, math.radians(45 + i * 40))
    SUB.objects.link(ob)

# Ensure exposure untouched
print('exposure held', bpy.context.scene.view_settings.exposure, flush=True)
print('world', bpy.context.scene.world.name if bpy.context.scene.world else None, flush=True)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('SAVED', OUT, flush=True)
