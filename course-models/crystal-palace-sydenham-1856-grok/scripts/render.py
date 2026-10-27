"""usage: blender -b <round.blend> -P scripts/render.py -- <outdir> <tag> <scale%> <samples> [cams...]
Env:
  PEOPLE_ERA=1850s|1890s|1910s|1930s  — adopt people before each cam (default: skip)
  NO_PEOPLE=1                         — force skip adopt
  KEEP_LIGHTING=1 or --keep-lighting  — preserve blend sun/world/exposure (no look override)
  RES=WxH  EXPO=float
"""
import bpy, sys, os
a = sys.argv[sys.argv.index('--')+1:]; out, tag, pct, spp = a[0], a[1], int(a[2]), int(a[3]); cams = a[4:]
sc = bpy.context.scene; sc.render.resolution_percentage = pct; sc.cycles.samples = spp
if os.environ.get('RES'): sc.render.resolution_x, sc.render.resolution_y = map(int, os.environ['RES'].split('x'))
# keep-lighting: do not let a look pass rewrite sun/world/exposure
keep_lighting = os.environ.get('KEEP_LIGHTING', '').strip() in ('1', 'true', 'yes') or '--keep-lighting' in a
if keep_lighting:
    print('KEEP_LIGHTING exposure', sc.view_settings.exposure,
          'look', getattr(sc.view_settings, 'look', ''), flush=True)
elif os.environ.get('EXPO'):
    sc.view_settings.exposure = float(os.environ['EXPO'])
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(os.environ.get('THREADS', '8'))

era = os.environ.get('PEOPLE_ERA', '').strip()
if era and not os.environ.get('NO_PEOPLE'):
    scripts = os.path.dirname(os.path.abspath(__file__))
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from cpl_people import adopt_people_v31, PEOPLE_VERSION
    r = adopt_people_v31(era=era, seed=int(os.environ.get('PEOPLE_SEED', '0') or '0'))
    print('PEOPLE_ADOPT', PEOPLE_VERSION, era, r, flush=True)

for c in cams:
    sc.camera = bpy.data.objects[c]
    sc.render.filepath = os.path.join(out, f'{tag}_{c}.png'); bpy.ops.render.render(write_still=True); print('RENDERED', c, flush=True)
