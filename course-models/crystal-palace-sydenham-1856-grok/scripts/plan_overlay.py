"""Top-down ortho Workbench render registered to plan 0205 pixel space, composited over the plan.
usage: blender -b <round.blend> -P scripts/plan_overlay.py -- <out.png>"""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(__file__)); from params import *
out = sys.argv[sys.argv.index('--')+1]
W, H = 5669, 2763; s = PLAN_PX_PER_FT; DS = 3
sc = bpy.context.scene
for c in bpy.data.collections:
    if c.name.startswith('SY_terraces') or c.name.startswith('REF'): c.hide_render = True
cam = bpy.data.objects['CAM_plan_overlay_top']; cd = cam.data; cd.type = 'ORTHO'
cx_ft = (W/2 - PLAN_X0)/s; cy_ft = -(H/2 - PLAN_Y0)/s
cam.location = (cx_ft*F, cy_ft*F, 900); cam.rotation_euler = (0, 0, 0)
cd.ortho_scale = (W/s)*F; cd.clip_end = 2000
sc.camera = cam; sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x = W//DS; sc.render.resolution_y = H//DS; sc.render.resolution_percentage = 100
sc.render.film_transparent = True
sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'SINGLE'; sh.single_color = (0.9, 0.1, 0.1)
sc.render.filepath = out + '.raw.png'; bpy.ops.render.render(write_still=True)
print('OVERLAY_RAW', out)
