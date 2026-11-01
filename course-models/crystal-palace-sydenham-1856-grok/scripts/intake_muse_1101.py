"""CANDIDATE (2026-11-01 reference intake): Muse alhambra-lion-fountain (CP041) + assyrian-lamassu (CP037)
appended into the live SY-EARLY round as collection instances. Opens rounds/sydenham-1856-r16.blend, NEVER saves it.
  blender -b rounds/sydenham-1856-r16.blend -P scripts/intake_muse_1101.py -- rounds/candidates/sydenham-1856-r16-muse-courts.blend
  ... -- <out.blend> --cam-only   (adds only the extra Nineveh camera; for the 'before' render, written outside the repo)
Dated-state tags: every new collection/instance carries cp_state / cp_dated; Hyde Park objects never touched."""
import bpy, os, sys, math
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); VD = os.path.join(HERE, '..', 'vendor')
a = sys.argv[sys.argv.index('--') + 1:]; OUT = a[0]; CAM_ONLY = '--cam-only' in a
FT = 0.3048
root = bpy.data.collections['SY-EARLY_c1856']
def floor_z(x, y, z0=5.0):  # below the gallery floors (~7 m)
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, n, i, o, m = bpy.context.scene.ray_cast(dg, Vector((x, y, z0)), Vector((0, 0, -1)))
    print('FLOOR', round(x, 2), round(y, 2), hit, o.name if o else None, round(loc.z, 3) if hit else None, flush=True)
    return loc.z if hit else 0.0
def cam(name, loc, target, lens):
    c = bpy.data.objects.get(name)
    if c is None:
        c = bpy.data.objects.new(name, bpy.data.cameras.new(name)); bpy.data.collections['CAMERAS'].objects.link(c)
    c.location = loc; c.data.lens = lens; c.data.sensor_width = 36
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    c['candidate'] = 'muse_courts_1101'; return c
# extra candidate camera: Nineveh Court nave facade (plan 0205 no. 27), 28 mm, eye 1.6 m, no roll
NX = 709 * FT
cam('CAM_CP037_nineveh_facade_28mm', (NX - 3.0, 4.0, 1.6), (NX + 0.5, 19.0, 2.4), 28)
if not CAM_ONLY:
    libc = bpy.data.collections.get('MUSE_props_lib__instanced_not_rendered')
    def lib(name):
        path = os.path.join(VD, 'muse-' + name, name + '.blend')
        pre = set(bpy.data.images)
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.objects = [n for n in src.objects if not n.startswith(('Ground', 'Backdrop', 'RenderCam', 'Camera', 'Sun', 'Light'))]
        lc = bpy.data.collections.new('MUSE_' + name); libc.children.link(lc)
        objs = [o for o in dst.objects if o is not None and o.type in ('MESH', 'CURVE', 'EMPTY')]
        keep = set(objs)
        for o in objs:
            if o.parent is not None and o.parent not in keep:
                mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
            lc.objects.link(o)
        for c in list(bpy.data.collections):   # drop appended source wrappers (e.g. Muse 'Water')
            if c.users == 0: bpy.data.collections.remove(c)
        for im in set(bpy.data.images) - pre:  # only images appended from Muse; textures are relative to their blend; pack so the candidate is self-contained
            if im.packed_file is None and im.source == 'FILE':
                try: im.filepath = os.path.join(VD, 'muse-' + name, 'textures', os.path.basename(im.filepath)); im.reload(); im.pack()
                except Exception as ex: print('PACKFAIL', im.name, ex)
        print('LIB', name, len(objs), flush=True); return lc
    def inst(lc, col, name, x, y, z, rz, state, dated):
        e = bpy.data.objects.new(name, None); e.instance_type = 'COLLECTION'; e.instance_collection = lc
        e.location = (x, y, z); e.rotation_euler = (0, 0, rz); col.objects.link(e)
        e['credit'] = 'Muse / models/%s @ origin/main a62ba2e (see vendor/muse-%s/CREDIT.md)' % (lc.name[5:], lc.name[5:])
        e['cp_state'] = state; e['cp_dated'] = dated; e['candidate'] = 'muse_courts_1101'; return e
    # --- CP041: Muse lion fountain replaces grok al_lions + al_lions_jet at the Court of the Lions centre ---
    for n in ('al_lions', 'al_lions_jet'):
        o = bpy.data.objects[n]; o.hide_render = True; o.hide_viewport = True
    fx, fy = 161.04, 25.60
    fz = floor_z(fx, fy - 2.3)
    colA = bpy.data.collections.new('SY56_alhambra_lion_fountain_muse__dated_c1856'); root.children.link(colA)
    colA['cp_state'] = 'SY-EARLY_c1856'; colA['cp_dated'] = 'Alhambra Court opened 1854; this state c.1856'
    inst(lib('alhambra-lion-fountain'), colA, 'muse_alhambra-lion-fountain_inst', fx, fy, fz, 0.0,
         'SY-EARLY_c1856', 'Alhambra Court 1854 (guide 1856 pp.66-69)')
    # --- CP037: 4 lamassu on the Nineveh Court nave facade (plan 0205 no. 27, facade y~63 ft, entrance x~709 ft) ---
    colN = bpy.data.collections.new('SY54_court_nineveh_lamassu_muse__1854_lost1866'); root.children.link(colN)
    colN['cp_state'] = 'SY-EARLY_c1856'; colN['cp_dated'] = 'Nineveh Court opened 1854; destroyed in the 30 Dec 1866 north-end fire'
    LL = lib('assyrian-lamassu'); yb = 60.5 * FT
    for i, (xf, rz) in enumerate(((683, 0.0), (696, 0.0), (722, math.pi), (735, math.pi))):  # heads (+x local) toward the entrance
        x = xf * FT; z = floor_z(x, yb)
        inst(LL, colN, 'muse_assyrian-lamassu_inst_%d' % i, x, yb, z, rz, 'SY-EARLY_c1856', 'Nineveh Court 1854-1866')
    t = bpy.data.texts.new('CREDIT_MUSE_INTAKE_1101')
    t.write('CANDIDATE muse_courts_1101 (2026-11-01)\n'
            'Muse alhambra-lion-fountain (origin/main a62ba2e) unmodified at Court of the Lions centre; grok al_lions/al_lions_jet hidden.\n'
            'Muse assyrian-lamassu x4 unmodified on the Nineveh Court nave facade (plan 0205 no.27), tagged SY54 ... lost1866.\n'
            'Nineveh Court architecture itself NOT modelled (bulls stand free in the north nave). Extra cam CAM_CP037_nineveh_facade_28mm.\n')
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
print('SAVED', OUT, flush=True)
