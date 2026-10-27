"""Improve CP050 football set: pitch striping, bank wear, stand boards, goal posts. Keep lighting."""
import bpy


def ensure_noise_mat(name, base_rgb, rough=0.92, scale=12.0, mix=0.35, second=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (600,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (300,0)
    bsdf.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-600,0)
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.location = (-350,80)
    n1.inputs['Scale'].default_value = scale
    n1.inputs['Detail'].default_value = 8.0
    n1.inputs['Roughness'].default_value = 0.55
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-100,80)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (*base_rgb,1)
    c2 = second or tuple(max(0,min(1,c*0.7)) for c in base_rgb)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (*c2,1)
    # chalk lines overlay via wave for pitch only — handled separately
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector'])
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def pitch_with_stripes():
    m = bpy.data.materials.get('FB_Pitch') or bpy.data.materials.new('FB_Pitch')
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(800,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(550,0)
    bsdf.inputs['Roughness'].default_value = 0.9
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-700,0)
    # grass noise
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.location=(-450,120)
    n1.inputs['Scale'].default_value = 28.0; n1.inputs['Detail'].default_value = 10
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(-200,120)
    ramp.color_ramp.elements[0].color=(0.08,0.22,0.05,1)
    ramp.color_ramp.elements[1].color=(0.16,0.34,0.09,1)
    # wear patches
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.location=(-450,-80)
    n2.inputs['Scale'].default_value = 4.5; n2.inputs['Detail'].default_value = 4
    mix_wear = nt.nodes.new('ShaderNodeMixRGB'); mix_wear.location=(80,60)
    mix_wear.blend_type='MIX'; mix_wear.inputs['Fac'].default_value=0.25
    mix_wear.inputs['Color2'].default_value=(0.28,0.22,0.12,1)
    # stripe: absolute sin along Y via separate XYZ + math
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); sep.location=(-450,-250)
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation='MULTIPLY'; mul.inputs[1].default_value=0.12  # ~8.3m pitch lines
    mul.location=(-250,-250)
    sine = nt.nodes.new('ShaderNodeMath'); sine.operation='SINE'; sine.location=(-50,-250)
    absn = nt.nodes.new('ShaderNodeMath'); absn.operation='ABSOLUTE'; absn.location=(120,-250)
    gt = nt.nodes.new('ShaderNodeMath'); gt.operation='GREATER_THAN'; gt.inputs[1].default_value=0.92
    gt.location=(300,-250)
    mix_line = nt.nodes.new('ShaderNodeMixRGB'); mix_line.location=(350,40)
    mix_line.inputs['Color2'].default_value=(0.85,0.85,0.78,1)
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], mix_wear.inputs['Color1'])
    nt.links.new(n2.outputs['Fac'], mix_wear.inputs['Fac'])
    nt.links.new(sep.outputs['Y'], mul.inputs[0])
    nt.links.new(mul.outputs['Value'], sine.inputs[0])
    nt.links.new(sine.outputs['Value'], absn.inputs[0])
    nt.links.new(absn.outputs['Value'], gt.inputs[0])
    nt.links.new(mix_wear.outputs['Color'], mix_line.inputs['Color1'])
    nt.links.new(gt.outputs['Value'], mix_line.inputs['Fac'])
    nt.links.new(mix_line.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def improve_stand_boards():
    m = bpy.data.materials.get('boards_gapped') or bpy.data.materials.new('boards_gapped')
    m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(500,0)
    bsdf=nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(280,0)
    bsdf.inputs['Roughness'].default_value=0.85
    tc=nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-500,0)
    wave=nt.nodes.new('ShaderNodeTexWave'); wave.location=(-280,40)
    wave.wave_type='BANDS'; wave.bands_direction='X'
    wave.inputs['Scale'].default_value=18.0; wave.inputs['Distortion'].default_value=1.5
    ramp=nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(0,40)
    ramp.color_ramp.elements[0].color=(0.22,0.15,0.09,1)
    ramp.color_ramp.elements[1].color=(0.42,0.30,0.18,1)
    n=nt.nodes.new('ShaderNodeTexNoise'); n.location=(-280,-160)
    n.inputs['Scale'].default_value=40
    bump=nt.nodes.new('ShaderNodeBump'); bump.location=(100,-100)
    bump.inputs['Strength'].default_value=0.15
    nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
    nt.links.new(wave.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(n.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def thicken_goal_posts():
    for o in bpy.data.objects:
        if o.name.startswith('FB_Post_') and o.type=='MESH':
            # slight scale on thin axis if very thin
            d=o.dimensions
            if min(d.x,d.y)<0.12:
                # add metal mat
                pass
    # metal mat for posts
    m=bpy.data.materials.get('FB_GoalIron') or bpy.data.materials.new('FB_GoalIron')
    m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF')
    if b:
        b.inputs['Base Color'].default_value=(0.12,0.12,0.12,1)
        b.inputs['Roughness'].default_value=0.45
        if 'Metallic' in b.inputs: b.inputs['Metallic'].default_value=0.7
    for o in bpy.data.objects:
        if o.name.startswith('FB_Post_'):
            if m.name not in [s.name for s in o.data.materials]:
                if o.data.materials: o.data.materials[0]=m
                else: o.data.materials.append(m)

def main():
    pitch_with_stripes()
    ensure_noise_mat('FB_Bank', (0.24,0.28,0.12), scale=9.0, second=(0.32,0.24,0.12))
    ensure_noise_mat('FB_Dirt', (0.32,0.24,0.14), scale=14.0, second=(0.22,0.16,0.09))
    improve_stand_boards()
    thicken_goal_posts()
    # assign pitch mat to FB_Pitch
    o=bpy.data.objects.get('FB_Pitch')
    if o and o.data.materials:
        o.data.materials[0]=bpy.data.materials['FB_Pitch']
    out='/workspace/crystal-palace-football/course-models/crystal-palace-football-1895-grok/rounds/fb03_1895.blend'
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print('saved', out)

if __name__=='__main__':
    main()
