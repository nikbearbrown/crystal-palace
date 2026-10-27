"""Improve CP043 lake islands set: grass variation, water depth, rock strata, dino paint noise. Keep lighting."""
import bpy

def rebuild_noise_color(mat_name, colors, scale=12.0, rough=0.88, bump=0.12):
    m=bpy.data.materials.get(mat_name)
    if not m:
        print('skip missing', mat_name); return
    m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(700,0)
    bsdf=nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(450,0)
    bsdf.inputs['Roughness'].default_value=rough
    tc=nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-600,0)
    n=nt.nodes.new('ShaderNodeTexNoise'); n.location=(-350,80)
    n.inputs['Scale'].default_value=scale; n.inputs['Detail'].default_value=9
    ramp=nt.nodes.new('ShaderNodeValToRGB'); ramp.location=(-80,80)
    # distribute colors along ramp
    while len(ramp.color_ramp.elements)<len(colors):
        ramp.color_ramp.elements.new(0.5)
    for i,c in enumerate(colors):
        e=ramp.color_ramp.elements[i]
        e.position=i/(len(colors)-1) if len(colors)>1 else 0.5
        e.color=(*c,1)
    nb=nt.nodes.new('ShaderNodeTexNoise'); nb.location=(-350,-140)
    nb.inputs['Scale'].default_value=scale*2.2
    bumpn=nt.nodes.new('ShaderNodeBump'); bumpn.location=(200,-80)
    bumpn.inputs['Strength'].default_value=bump
    nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], nb.inputs['Vector'])
    nt.links.new(n.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(nb.outputs['Fac'], bumpn.inputs['Height'])
    nt.links.new(bumpn.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def improve_water():
    m=bpy.data.materials.get('lake_water_still')
    if not m: return
    m.use_nodes=True; nt=m.node_tree
    # find principled
    bsdf=None
    for n in nt.nodes:
        if n.type=='BSDF_PRINCIPLED': bsdf=n; break
    if not bsdf: return
    bsdf.inputs['Base Color'].default_value=(0.05,0.12,0.14,1)
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value=0.85
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value=0.85
    bsdf.inputs['Roughness'].default_value=0.05
    if 'IOR' in bsdf.inputs: bsdf.inputs['IOR'].default_value=1.333
    # slight volume-ish via darker base already

def main():
    rebuild_noise_color('grass_1854_young_turf',
        [(0.14,0.28,0.08),(0.22,0.36,0.10),(0.10,0.22,0.06),(0.28,0.30,0.12)],
        scale=18.0, rough=0.92, bump=0.18)
    rebuild_noise_color('sandstone_rocks',
        [(0.45,0.38,0.28),(0.55,0.48,0.35),(0.35,0.28,0.20),(0.50,0.42,0.32)],
        scale=6.0, rough=0.95, bump=0.35)
    rebuild_noise_color('lake_bank_mud',
        [(0.22,0.16,0.10),(0.30,0.22,0.12),(0.18,0.14,0.08)],
        scale=10.0, rough=0.96, bump=0.2)
    # dino paints — keep hue family, add mottling
    for mn, cols in [
        ('paint_megalosaurus_brown', [(0.35,0.25,0.14),(0.42,0.30,0.16),(0.28,0.20,0.12)]),
        ('paint_iguanodon_green_grey', [(0.32,0.36,0.28),(0.38,0.40,0.32),(0.26,0.30,0.24)]),
        ('paint_hylaeosaurus_olive', [(0.28,0.32,0.18),(0.34,0.36,0.20),(0.22,0.26,0.14)]),
        ('paint_plesiosaur_dun', [(0.40,0.36,0.28),(0.46,0.40,0.30),(0.32,0.28,0.22)]),
        ('paint_ichthyosaur_slate', [(0.30,0.32,0.34),(0.36,0.38,0.40),(0.24,0.26,0.28)]),
    ]:
        rebuild_noise_color(mn, cols, scale=22.0, rough=0.75, bump=0.08)
    improve_water()
    # foliage denser variation
    rebuild_noise_color('foliage',
        [(0.08,0.22,0.05),(0.12,0.28,0.08),(0.06,0.16,0.04),(0.18,0.30,0.10)],
        scale=40.0, rough=0.9, bump=0.05)
    out='/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok/rounds/dinosaurs-1854-r03.blend'
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print('saved', out)

if __name__=='__main__':
    main()
