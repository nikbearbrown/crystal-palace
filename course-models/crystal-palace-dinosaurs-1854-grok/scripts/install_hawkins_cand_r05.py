"""CANDIDATE r05: dinosaurs only on r03b base (KEEP trees/water/reflections).
- Muse iguanodon for BOTH Iguanodon slots (standing = mirrored/re-posed copy).
- Stronger stone/sage scale paint on Megalosaurus, Hylaeosaurus, plesiosaurs, ichthyosaurs.
- Reframe CAM_CP043b as Muse-iguanodon hero (50 mm, eye height, lake/edge behind, no crop).
Does not touch trees or lake_water materials/meshes.
"""
import bpy, math, os, shutil
from mathutils import Vector, Matrix, Euler

BASE = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
SRC = os.path.join(BASE, 'rounds/dinosaurs-1854-r03b.blend')
OUT = os.path.join(BASE, 'rounds/dinosaurs-1854-r05-cand.blend')
MUSE_IG = '/workspace/models-main-ro/models/iguanodon/iguanodon.blend'
SKIP = {'GroundBase'}  # keep Trunk with animal

def mat_stone(name, top, belly, rough=0.82, scale=20.0, bump=0.9):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (700, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (450, 0)
    bsdf.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-700, 0)
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location = (-450, 120)
    vor.feature = 'F1'; vor.inputs['Scale'].default_value = scale
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.location = (-150, 120)
    cr.color_ramp.elements[0].position = 0.0
    cr.color_ramp.elements[0].color = (*top, 1)
    cr.color_ramp.elements[1].position = 1.0
    cr.color_ramp.elements[1].color = (*belly, 1)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.location = (-450, -120)
    nz.inputs['Scale'].default_value = 2.8; nz.inputs['Detail'].default_value = 10
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.location = (150, 80)
    mix.inputs[7].default_value = (top[0] * 0.55, top[1] * 0.62, top[2] * 0.45, 1)
    bumpn = nt.nodes.new('ShaderNodeBump'); bumpn.location = (250, -80)
    bumpn.inputs['Strength'].default_value = bump
    # dirt in crevices
    dark = nt.nodes.new('ShaderNodeMix'); dark.data_type = 'RGBA'; dark.location = (300, 80)
    dark.inputs['Factor'].default_value = 0.25
    dark.inputs[7].default_value = (top[0] * 0.35, top[1] * 0.38, top[2] * 0.28, 1)
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(vor.outputs['Distance'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], mix.inputs[6])
    nt.links.new(nz.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(mix.outputs[2], dark.inputs[6])
    nt.links.new(vor.outputs['Distance'], dark.inputs['Factor'])
    nt.links.new(dark.outputs[2], bsdf.inputs['Base Color'])
    nt.links.new(vor.outputs['Distance'], bumpn.inputs['Height'])
    nt.links.new(bumpn.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def append_muse_parts():
    with bpy.data.libraries.load(MUSE_IG, link=False) as (df, dt):
        dt.objects = [n for n in df.objects if n not in SKIP]
    parts = []
    for o in dt.objects:
        if o is None or o.type != 'MESH':
            if o: bpy.data.objects.remove(o, do_unlink=True)
            continue
        bpy.context.collection.objects.link(o)
        o['credit'] = 'models/iguanodon (Muse, main) — append-only'
        parts.append(o)
    return parts

def join_parts(name, parts):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    if ob.data: ob.data.name = name
    ob['credit'] = 'models/iguanodon (Muse, main) — append-only'
    return ob

def duplicate_object(ob, name):
    copy = ob.copy()
    copy.data = ob.data.copy()
    copy.name = name
    if copy.data: copy.data.name = name
    bpy.context.collection.objects.link(copy)
    return copy

def swap_into(scene_name, new_ob, heading_deg=None, mirror_y=False):
    old = bpy.data.objects.get(scene_name)
    assert old, scene_name
    loc = old.location.copy()
    rot = old.rotation_euler.copy()
    dim_old = old.dimensions.copy()
    col = old.users_collection[0]
    for c in list(old.users_collection):
        c.objects.unlink(old)
    bpy.data.objects.remove(old, do_unlink=True)
    for c in list(new_ob.users_collection):
        c.objects.unlink(new_ob)
    col.objects.link(new_ob)
    new_ob.name = scene_name
    if new_ob.data: new_ob.data.name = scene_name + '_muse'
    new_ob.location = loc
    if heading_deg is not None:
        new_ob.rotation_euler = Euler((0, 0, math.radians(heading_deg)), 'XYZ')
    else:
        new_ob.rotation_euler = rot
    if mirror_y:
        new_ob.scale = (-1.0, 1.0, 1.0)
    else:
        new_ob.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    # match plan length to prior slot roughly
    sx = abs(dim_old.x / max(new_ob.dimensions.x, 1e-3))
    # Muse is ~9.3m; don't inflate past 1.15
    s = min(max(sx, 0.85), 1.12)
    new_ob.scale = (-s if mirror_y else s, s, s)
    bpy.ops.object.select_all(action='DESELECT')
    new_ob.select_set(True)
    bpy.context.view_layer.objects.active = new_ob
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # ground: bottom at prior bottom-ish
    zs = [v.co.z for v in new_ob.data.vertices]
    zmin = min(zs)
    # park earth under Muse — keep location.z as island ground, shift mesh so belly sits
    # Muse origin is base centre; location already at ground for old blob
    print(f'  {scene_name}: dim={[round(v,2) for v in new_ob.dimensions]} '
          f'loc={[round(v,2) for v in new_ob.location]} mirror={mirror_y}')
    return new_ob

def paint_existing(names, mat):
    for n in names:
        o = bpy.data.objects.get(n)
        if not o or o.type != 'MESH':
            continue
        if o.data.materials:
            o.data.materials[0] = mat
        else:
            o.data.materials.append(mat)
        print('  painted', n, mat.name)

def reframe_cp043b(target_name='iguanodon_recumbent'):
    """50 mm eye-height hero on Muse Iguanodon; lake/island edge behind; no crop."""
    cam = bpy.data.objects.get('CAM_CP043b_iguanodons_detail_50mm')
    tgt = bpy.data.objects.get(target_name)
    assert cam and tgt
    # Target centre roughly body mid
    tc = tgt.location + Vector((0, 0, 1.1))
    # Camera south of animal so lake (further south / lower Y behind? 
    # Island animals at y~5-7; water is y negative. Put camera at mid-south
    # looking NNE at animal so water is in foreground OR put camera on island
    # S of animal looking N with trees/lake edge behind.
    # User: "lake or island edge behind it" → background = lake/edge.
    # Camera on south bank / water side looking north at animal.
    # Distance ~14–16 m for 50 mm filling most of frame with ~10 m animal.
    cam.location = Vector((tc.x - 1.5, tc.y - 14.5, 1.65))
    # aim at body + slight head bias (+X for Muse)
    aim = tc + Vector((1.2, 0, 0.2))
    direction = aim - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 50.0
    # mild shift so animal isn't cropped — track to empty
    print('CP043b reframed', [round(v, 2) for v in cam.location],
          'aim', [round(v, 2) for v in aim])

def main():
    shutil.copy2(SRC, OUT)
    bpy.ops.wm.open_mainfile(filepath=OUT)
    print('base', SRC, '→', OUT, '(trees/water untouched)')

    # Muse append once, join, then duplicate for standing slot
    parts = append_muse_parts()
    hero = join_parts('_muse_ig_joined', parts)
    standing = duplicate_object(hero, '_muse_ig_standing_copy')
    # Recumbent: original Muse pose at recumbent slot (heading -25)
    swap_into('iguanodon_recumbent', hero, heading_deg=-25, mirror_y=False)
    # Standing slot: mirrored + different heading so it reads as the second animal
    # (DEPARTURES: both slots = Muse sprawled; standing is mirrored re-pose, not upright)
    swap_into('iguanodon_standing', standing, heading_deg=-150, mirror_y=True)

    # Painted stone/sage on other sculptures (meshes kept from r03b)
    meg = mat_stone('paint_megalosaurus_stone_grey_r05',
                    (0.30, 0.32, 0.28), (0.42, 0.40, 0.34), scale=16, bump=1.0)
    hyl = mat_stone('paint_hylaeosaurus_sage_r05',
                    (0.26, 0.30, 0.22), (0.36, 0.34, 0.26), scale=22, bump=0.85)
    ple = mat_stone('paint_plesiosaur_stone_r05',
                    (0.28, 0.30, 0.28), (0.40, 0.38, 0.32), scale=26, bump=0.7)
    ich = mat_stone('paint_ichthyosaur_slate_r05',
                    (0.24, 0.28, 0.30), (0.34, 0.36, 0.34), scale=28, bump=0.75)
    paint_existing(['megalosaurus'], meg)
    paint_existing(['hylaeosaurus', 'studio_hylaeosaurus_in_clay'], hyl)
    paint_existing([f'plesiosaur_{i}' for i in (1, 2, 3)], ple)
    paint_existing([f'ichthyosaur_{i}' for i in (1, 2, 3)], ich)
    # studio clay iguanodon can stay clay; park standing/recumbent are Muse

    reframe_cp043b('iguanodon_recumbent')

    sc = bpy.context.scene
    sc.render.resolution_x = 1920
    sc.render.resolution_y = 1080
    sc.render.resolution_percentage = 100
    # KEEP_LIGHTING from r03b (expo -1.4) — do not change
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print('CANDIDATE saved', OUT)
    print('water rough still', bpy.data.materials['lake_water_still'].node_tree.nodes[
        next(n.name for n in bpy.data.materials['lake_water_still'].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    ].inputs['Roughness'].default_value)

if __name__ == '__main__':
    main()
