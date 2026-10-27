"""True ortho section: camera CAM_section_cut_x-300 with clip slice. Workbench, white bg.
usage: blender -b <round.blend> -P scripts/section_render.py -- <out.png>"""
import bpy, sys
out = sys.argv[sys.argv.index('--')+1]; sc = bpy.context.scene
for c in bpy.data.collections:
    if c.name.startswith('REF') or 'park' in c.name or 'PLACEHOLDER' in c.name.upper() or 'placeholders' in c.name or 'distant' in c.name.lower(): c.hide_render = True
sc.camera = bpy.data.objects['CAM_section_cut_x-300']
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = 2150; sc.render.resolution_y = 1100; sc.render.resolution_percentage = 100
cam = sc.camera.data; cam.clip_start = 24*0.3048; cam.clip_end = 36*0.3048  # slice x=-306..-294 through braced column line x=-300
sc.world.color = (1,1,1); cam.ortho_scale = 400*0.3048; sc.camera.location.z = 62*0.3048
sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'SINGLE'; sh.single_color = (0.12,0.12,0.14); sh.show_object_outline = True; sh.object_outline_color = (0,0,0)
sh.background_type = 'VIEWPORT'; sh.background_color = (1,1,1)
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 0
sc.render.filepath = out; bpy.ops.render.render(write_still=True); print('SECTION_OK', out)
