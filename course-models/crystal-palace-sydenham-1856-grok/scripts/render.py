"""usage: blender -b <round.blend> -P scripts/render.py -- <outdir> <tag> <scale%> <samples> [cams...]"""
import bpy, sys, os
a = sys.argv[sys.argv.index('--')+1:]; out, tag, pct, spp = a[0], a[1], int(a[2]), int(a[3]); cams = a[4:]
sc = bpy.context.scene; sc.render.resolution_percentage = pct; sc.cycles.samples = spp
if os.environ.get('RES'): sc.render.resolution_x, sc.render.resolution_y = map(int, os.environ['RES'].split('x'))   # e.g. RES=1080x1440 portrait compare
if os.environ.get('EXPO'): sc.view_settings.exposure = float(os.environ['EXPO'])   # r11: per-render exposure (0108 compare)
sc.render.threads_mode = 'FIXED'; sc.render.threads = 8
for c in cams:
    sc.camera = bpy.data.objects[c]
    sc.render.filepath = os.path.join(out, f'{tag}_{c}.png'); bpy.ops.render.render(write_still=True); print('RENDERED', c, flush=True)
