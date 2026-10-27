"""Patch r05 cand: weather Muse IguanodonHide to stone/sage; reframe CP043b
with lake/island edge behind (camera N of hero looking S toward water)."""
import bpy, math
from mathutils import Vector, Euler

OUT = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok/rounds/dinosaurs-1854-r05-cand.blend'
bpy.ops.wm.open_mainfile(filepath=OUT)

def weather_hide(mat_name='IguanodonHide'):
    m = bpy.data.materials.get(mat_name)
    if not m or not m.use_nodes:
        print('no', mat_name); return
    nt = m.node_tree
    # Find Principled
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf:
        print('no bsdf'); return
    # Insert multiply/mix toward stone-grey + sage after whatever feeds Base Color
    # Stone top (0.32,0.34,0.28), sage belly tint (0.38,0.42,0.30)
    links_in = [l for l in nt.links if l.to_node == bsdf and l.to_socket == bsdf.inputs['Base Color']]
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.location = (bsdf.location.x - 200, bsdf.location.y)
    mix.inputs['Factor'].default_value = 0.55
    mix.inputs[7].default_value = (0.30, 0.33, 0.26, 1)  # stone-grey/sage target
    # dirt overlay
    mix2 = nt.nodes.new('ShaderNodeMix')
    mix2.data_type = 'RGBA'
    mix2.location = (bsdf.location.x - 50, bsdf.location.y)
    mix2.inputs['Factor'].default_value = 0.22
    mix2.inputs[7].default_value = (0.18, 0.17, 0.12, 1)
    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.location = (bsdf.location.x - 450, bsdf.location.y - 200)
    vor.inputs['Scale'].default_value = 18.0
    tc = nt.nodes.new('ShaderNodeTexCoord')
    tc.location = (bsdf.location.x - 650, bsdf.location.y - 200)
    bump = nt.nodes.new('ShaderNodeBump')
    bump.location = (bsdf.location.x - 50, bsdf.location.y - 180)
    bump.inputs['Strength'].default_value = 0.7
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    if links_in:
        src = links_in[0].from_socket
        nt.links.remove(links_in[0])
        nt.links.new(src, mix.inputs[6])
    else:
        # was default colour
        mix.inputs[6].default_value = list(bsdf.inputs['Base Color'].default_value)
    nt.links.new(mix.outputs[2], mix2.inputs[6])
    nt.links.new(vor.outputs['Distance'], mix2.inputs['Factor'])
    nt.links.new(mix2.outputs[2], bsdf.inputs['Base Color'])
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    # keep existing normal if any, else set bump
    norm_links = [l for l in nt.links if l.to_node == bsdf and l.to_socket == bsdf.inputs['Normal']]
    if not norm_links:
        nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Roughness'].default_value = max(bsdf.inputs['Roughness'].default_value, 0.88)
    print('weathered', mat_name)

weather_hide('IguanodonHide')

# Reframe CP043b: camera NORTH of Muse looking SOUTH so lake is behind the animal
cam = bpy.data.objects['CAM_CP043b_iguanodons_detail_50mm']
tgt = bpy.data.objects['iguanodon_recumbent']
tc = tgt.location + Vector((0.5, 0, 1.05))
# ~13 m north of animal, eye height; slight west so body fills 50mm without cropping head/tail
cam.location = Vector((tc.x - 2.0, tc.y + 13.0, 1.70))
aim = tc + Vector((0.8, -0.5, 0.05))
direction = aim - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 50.0
# mild horizontal shift if available
if hasattr(cam.data, 'shift_x'):
    cam.data.shift_x = 0.02
    cam.data.shift_y = -0.02
print('CP043b', [round(v,2) for v in cam.location], 'aim', [round(v,2) for v in aim])

# Ensure trees/water untouched — just assert
w = bpy.data.materials.get('lake_water_still')
bsdf = next(n for n in w.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
print('water rough', bsdf.inputs['Roughness'].default_value)
assert abs(bsdf.inputs['Roughness'].default_value - 0.04) < 0.01

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('patched', OUT)
