"""CP062 CANDIDATE (2026-11-17, no verdict): 'Morning between the towers' - 1 December 1936, the morning after the fire, seen
from the live CAM_CP062_morning_between_towers_35mm (camera NOT moved).

usage: blender -b rounds/sydenham-ruins-r17.blend -P scripts/candidate_cp062_morning.py [-- out.blend]   (env CP062_NOSAVE=1: no save)
Base = rounds/sydenham-ruins-r17.blend (md5 2c3343c6 = as committed in 80f43ba 'dud-fix v4', unchanged since) - the blend the
  live hero renders/r17q_ruins_CAM_CP062_morning_between_towers_35mm.png (md5 acc315a7) was rendered from (survey look v1.1
  apply_render.py --scene-id CP062 --era 1852 --tod exterior_morning --spp 32 --res 1280x720 --no-people: re-render max diff 0).
  -> rounds/candidates/sydenham-ruins-r17_cp062morning.blend
Live hero shows: the South Tower standing alone in a clean sky over an empty green plain - the c.1937-40 CLEARED plateau state
  (SY-RUINS_c1937-40), i.e. the storyboard's own warning 'do not ... use a fully cleared plateau for the morning after' (CP062
  flag B/R/U). Nothing in frame says a fire happened the night before.
Sources (repo / survey): storyboard CP062 (1 December 1936, SY-RUINS: twisted remains occupy the ridge; towers stand beyond
  the missing roof; narration 'In the morning, the towers still stood'); muse-drive 0587 (aerial view of the morning-after
  ruin: South Tower intact beside a LOW tangled wreck field, smoke/steam haze drifting off the wreck, railway colonnade
  intact); London Walks 30 Nov 1936 (wind 'freshly from the northwest'; fire 'blown ... down through the south-west wing',
  so the south end burnt out, R); Wikipedia / LFB (towers survived; 89 appliances, 438 firemen attended, R); Historic England
  via Inside Croydon (Baird mast on the South Tower from 1933, R existence / U form); this repo's own AFTER state
  (rounds/sydenham-1936after-r17.blend, states.py/dress36.py, DEPARTURES r11/r12): collapsed ironwork field, north-end
  fragment, Baird mast, LFB 100 ft turntable ladders on the Parade on 1 Dec 1936.
Adds dated collection SY36_morning_after_smoke_wreck__1Dec1936 (cp_state SY36-AFTER_1Dec1936_morning):
  1. the AFTER state's wreck, appended unmodified from rounds/sydenham-1936after-r17.blend (2d20fe45): collapsed_ironwork_field
     (charred, <= 16.2 m), north_end_standing_fragment, south_tower_baird_mast_1933. State-correct for 1 Dec 1936, but the wreck
     is BELOW the hero's sightline (bottom frame edge ~18-25 m over the south end) and only the lowest ~quarter of the mast
     shows above the lantern before the frame top cuts it;
  2. smoke rising from the smouldering south-end wreck: 5 plumes of noise-masked volume puffs (absorption + matched emission,
     no scattering, so they converge at the live 32 spp), grey low / paler high, leaning NE on the model grid so the tower
     stays clear (wind U, see departures), plus 2 thin low haze volumes over the plateau beyond the tower.
  (A 100 ft LFB turntable ladder damping down was tried in development and dropped: ~60 px in frame, read as a stray red line.)
Cameras NOT moved, world/sun/exposure/look NOT changed (the look v1.1 recipe still sets them at render time). Nothing deleted
or hidden; the c.1937-40 cleared-plateau footing pads stay underneath (below the sightline; logged departure).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP062_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-ruins-r17_cp062morning.blend')
AFTER_BLEND = os.environ.get('CP062_AFTER_BLEND', os.path.join(ROOT, 'rounds', 'sydenham-1936after-r17.blend'))
STATE = 'SY36-AFTER_1Dec1936_morning'
CNAME = 'SY36_morning_after_smoke_wreck__1Dec1936'
FT = 0.3048
RNG = random.Random(1121936)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP062_morning_between_towers_35mm']
root = bpy.data.collections['SY-RUINS_c1937-40']
col = bpy.data.collections.get(CNAME) or bpy.data.collections.new(CNAME)
if col.name not in [c.name for c in root.children]: root.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('storyboard CP062 1 Dec 1936 morning after, twisted remains, towers stand R; muse-drive 0587 aerial: low wreck '
                   'field + smoke/steam haze + South Tower intact R; NW wind 30 Nov R (London Walks), morning wind U, NE lean I; '
                   'AFTER-state wreck/mast appended from sydenham-1936after-r17 (I/R as logged there)')
INFO = {}

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE

# ------------------------------------------------------------------ 1. AFTER-state wreck + mast (appended)
WANT_OBJ = ['collapsed_ironwork_field', 'north_end_standing_fragment', 'south_tower_baird_mast_1933']
with bpy.data.libraries.load(AFTER_BLEND, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n in WANT_OBJ]
app = {}
for o in dst.objects:
    if o is None: continue
    o.name = 'cp062_after_' + o.name.replace('south_tower_', ''); col.objects.link(o); o['cp_state'] = STATE; app[o.name] = o
    o['appended_from'] = 'rounds/sydenham-1936after-r17.blend'
INFO['appended'] = sorted(app)

# ------------------------------------------------------------------ 2. smoke
RAD = float(os.environ.get('CP062_RAD', '1.1'))
def smoke_mat(name, density, colr, nscale=0.05):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    for x in list(N): N.remove(x)
    out = N.new('ShaderNodeOutputMaterial'); pv = N.new('ShaderNodeVolumePrincipled'); tcn = N.new('ShaderNodeTexCoord')
    sub = N.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    s2 = N.new('ShaderNodeVectorMath'); s2.operation = 'SCALE'; s2.inputs['Scale'].default_value = 2.0
    gr = N.new('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'
    L.new(tcn.outputs['Generated'], sub.inputs[0]); L.new(sub.outputs[0], s2.inputs[0]); L.new(s2.outputs[0], gr.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = nscale; nz.inputs['Detail'].default_value = 1.5; nz.inputs['Roughness'].default_value = 0.5
    L.new(tcn.outputs['Object'], nz.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.44; ramp.color_ramp.elements[1].position = 0.58
    L.new(nz.outputs['Fac'], ramp.inputs[0])
    pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.5; L.new(gr.outputs['Fac'], pw.inputs[0])
    mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L.new(pw.outputs[0], mu.inputs[0]); L.new(ramp.outputs['Color'], mu.inputs[1])
    md = N.new('ShaderNodeMath'); md.operation = 'MULTIPLY'; md.inputs[1].default_value = density; L.new(mu.outputs[0], md.inputs[0])
    # absorption + matched emission instead of scattering (converges at the live 32 spp without volume speckle):
    # an optically thick puff settles at radiance RAD x colr - i.e. lit grey smoke against the morning sky (I, look of 0587)
    L.new(md.outputs[0], pv.inputs['Density']); pv.inputs['Color'].default_value = (0, 0, 0, 1)
    pv.inputs['Absorption Color'].default_value = (0, 0, 0, 1)
    em0 = N.new('ShaderNodeMath'); em0.operation = 'MULTIPLY'; em0.inputs[1].default_value = RAD; L.new(md.outputs[0], em0.inputs[0])
    nz2 = N.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = nscale * 2.2; nz2.inputs['Detail'].default_value = 2.0
    L.new(tcn.outputs['Object'], nz2.inputs['Vector'])
    sh = N.new('ShaderNodeMapRange'); sh.inputs['From Min'].default_value = 0.35; sh.inputs['From Max'].default_value = 0.65
    sh.inputs['To Min'].default_value = 0.35; sh.inputs['To Max'].default_value = 1.30; L.new(nz2.outputs['Fac'], sh.inputs['Value'])
    em = N.new('ShaderNodeMath'); em.operation = 'MULTIPLY'; L.new(em0.outputs[0], em.inputs[0]); L.new(sh.outputs['Result'], em.inputs[1])   # sunlit / shadowed billows (I)
    L.new(em.outputs[0], pv.inputs['Emission Strength']); pv.inputs['Emission Color'].default_value = (*colr, 1)
    L.new(pv.outputs[0], out.inputs['Volume']); m['cp_state'] = STATE; return m

DRIFT = Vector((0.60, 0.80, 0)).normalized()            # lean NE on the model grid, as the repo's FIRE state smoke (states.py, wind U); see D-SY-CP062-05
# plume sources on the burnt-out south end of the footprint (x -245..-150, y -45..48; London Walks: SW wing burnt, R)
SOURCES = [(-243, 2, 1.00), (-240, 22, 0.85), (-244, 42, 0.70), (-244, -18, 0.60), (-232, -2, 0.60)]
NPUFF = 0
MATS = {}
for si, (sx, sy, sk) in enumerate(SOURCES):
    nseg = 14
    for k in range(nseg):
        t = k / (nseg - 1)
        h = 6 + 100 * t * sk                                      # puff centre height above the plateau (m)
        c = Vector((sx, sy, h)) + DRIFT * (0.004 * h * h) + Vector((RNG.uniform(-3, 3), RNG.uniform(-3, 3), RNG.uniform(-2, 2)))
        r = (5 + 22 * t ** 1.2) * sk ** 0.5 * RNG.uniform(0.85, 1.15)
        dens = round((0.70 - 0.55 * t) * sk, 3)                     # thick at the wreck, thinning as it spreads (I)
        tone = round(0.50 + 0.30 * t, 2)                          # grey-brown smoke low, paler smoke/steam higher (I)
        key = (dens, tone)
        m = MATS.get(key) or smoke_mat(f'cp062_smoke_{len(MATS):02d}', dens, (tone, tone * 0.975, tone * 0.94), nscale=0.05)
        MATS[key] = m
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0,
            matrix=Matrix.Translation(c) @ Matrix.Diagonal((r * RNG.uniform(1.0, 1.3), r * RNG.uniform(0.9, 1.2), r * RNG.uniform(0.75, 0.95), 1)))
        me = bpy.data.meshes.new(f'cp062_smoke_p{si}_{k:02d}'); bm.to_mesh(me); bm.free(); me.materials.append(m)
        o = bpy.data.objects.new(me.name, me); col.objects.link(o); o['cp_state'] = STATE; o.visible_shadow = False; NPUFF += 1
# thin low haze sheet over the plateau and Anerley side beyond the tower (0587 haze; I)
for k, (hx, hy, hz, rx, ry, rz) in enumerate([(-330, 120, 12, 160, 110, 22), (-230, 60, 14, 120, 70, 18)]):
    m = smoke_mat(f'cp062_haze_{k}', 0.06, (0.62, 0.62, 0.61), nscale=0.02)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=10, radius=1.0, matrix=Matrix.Translation(Vector((hx, hy, hz))) @ Matrix.Diagonal((rx, ry, rz, 1)))
    me = bpy.data.meshes.new(f'cp062_haze_{k}'); bm.to_mesh(me); bm.free(); me.materials.append(m)
    o = bpy.data.objects.new(me.name, me); col.objects.link(o); o['cp_state'] = STATE; o.visible_shadow = False; NPUFF += 1
INFO['smoke_volumes'] = NPUFF

for o in col.objects: o['cp_state'] = STATE
INFO['objects'] = len(col.objects)
print('CP062 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP062 SAVED', OUT)
