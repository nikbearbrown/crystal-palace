"""CANDIDATE S67b: unmistakable Jan 1867 north-transept FIRE ruins for CP047/CP048.

From EARLY r16 (intact), destroy the north transept in-place per ILN 1867-01-12:
- Remove vault glass / front roofs; leave skeletal frame + twisted/fallen iron
- Char Muse colossi (kept in situ — they survived the fire per crystal.dircon / S67)
- Rubble field, collapsed wing stubs, blackened/broken adjacent glazing
- Overcast winter sky (dated-state departure, logged)
- Reframe CP047/CP048 onto the north-end gap so damage reads at a glance

Also patches live post66-r10: remove leftover north-transept frame stub (white-slab-adjacent fix KEEP).
"""
import bpy, math, os, shutil, random
from mathutils import Vector, Matrix, Euler

SY = '/workspace/crystal-palace-sydenham/course-models/crystal-palace-sydenham-1856-grok'
SRC = os.path.join(SY, 'rounds/sydenham-1856-r16.blend')
OUT = os.path.join(SY, 'rounds/sydenham-s67b-fire-cand.blend')
POST66_LIVE = os.path.join(SY, 'rounds/sydenham-post66-r10.blend')

NX0, NX1 = 149.5, 172.5
NY0, NY1 = -47.5, 47.5

def mat_rgb(name, rgb, rough=0.9, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*rgb, 1)
    bsdf.inputs['Roughness'].default_value = rough
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_charred_iron(name='s67b_charred_iron'):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 6.5
    noise.inputs['Detail'].default_value = 14
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.0
    cr.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1)
    cr.color_ramp.elements[1].position = 1.0
    cr.color_ramp.elements[1].color = (0.08, 0.06, 0.045, 1)
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.85
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Roughness'].default_value = 0.97
    bsdf.inputs['Metallic'].default_value = 0.35
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_soot_stone(name='s67b_soot_stone'):
    return mat_rgb(name, (0.12, 0.10, 0.08), rough=0.95)

def mat_broken_glass(name='s67b_broken_black_glass'):
    m = mat_rgb(name, (0.04, 0.045, 0.05), rough=0.55, metallic=0.05)
    # low transmission leftover shards feel opaque blackened
    return m

def mat_rubble(name='s67b_rubble'):
    return mat_rgb(name, (0.22, 0.16, 0.11), rough=0.92)

def box(name, col, mat, x0,x1,y0,y1,z0,z1):
    me = bpy.data.meshes.new(name)
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    f = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me.from_pydata(v,[],f); me.update(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); col.objects.link(o); return o

def strut(name, col, mat, p0, p1, r=0.4, seg=7):
    import bmesh
    me = bpy.data.meshes.new(name)
    d = Vector(p1) - Vector(p0)
    L = d.length
    if L < 0.05: return None
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r*0.75,
                          depth=L, matrix=Matrix.Identity(4))
    quat = Vector((0,0,1)).rotation_difference(d.normalized())
    bmesh.ops.rotate(bm, cent=(0,0,0), matrix=quat.to_matrix(), verts=bm.verts)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(Vector(p0)+Vector(p1))*0.5)
    bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); col.objects.link(o); return o

def set_overcast_winter_sky():
    """Grey overcast Jan 1867 sky — dated-state departure."""
    w = bpy.context.scene.world
    if not w:
        w = bpy.data.worlds.new('s67b_overcast_jan1867'); bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    # flat cool grey overcast
    bg.inputs['Color'].default_value = (0.42, 0.45, 0.48, 1)
    bg.inputs['Strength'].default_value = 0.55
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    # soft sun still present but dimmed if exists
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.data.type == 'SUN':
            o.data.energy = min(o.data.energy, 2.2)
            o.data.color = (0.85, 0.88, 0.92)
    # exposure
    sc = bpy.context.scene
    sc.view_settings.exposure = -0.35
    print('overcast winter sky set')

def reframe_fire_cams():
    """Point CP047/CP048 at the north-end gap + colossi ruins (ILN-like)."""
    # Colossi centre ~ (160.9, -33.8, ~15)
    colossi_aim = Vector((160.9, -33.8, 14.0))
    gap_centre = Vector((161.0, 0.0, 18.0))

    c47 = bpy.data.objects.get('CAM_CP047_north_end_35mm')
    c48 = bpy.data.objects.get('CAM_CP048_terrace_hold_35mm')
    # CP047: from garden south of colossi, eye-ish, looking NNE into the ruined bay
    # — colossi midground, twisted ribs and open sky behind, rubble foreground
    if c47:
        c47.location = Vector((155.0, -78.0, 3.5))
        aim = Vector((162.0, -20.0, 16.0))
        c47.rotation_euler = (aim - c47.location).to_track_quat('-Z', 'Y').to_euler()
        c47.data.lens = 28.0  # wider to take in gap + ribs
        print('CP047 fire frame', [round(v,1) for v in c47.location])
    # CP048: from SE terrace, looking NW at the cut where transept met nave —
    # shows gap in the palace massing, charred adjacent wing, fallen iron
    if c48:
        c48.location = Vector((195.0, -70.0, 4.0))
        aim = Vector((161.0, -10.0, 18.0))
        c48.rotation_euler = (aim - c48.location).to_track_quat('-Z', 'Y').to_euler()
        c48.data.lens = 32.0
        print('CP048 fire frame', [round(v,1) for v in c48.location])

def destroy_north_transept(scar, char, glass_b, rubble_m, soot):
    rs = random.Random(18670112)
    # Remove / hide glass + roofs of north transept (open to sky)
    kill_names = [
        'north_transept_vault_glass',
        'SY_north_transept__lost1866_front_roofs',
        'SY_north_transept__lost1866_walls',
    ]
    for nm in kill_names:
        o = bpy.data.objects.get(nm)
        if o:
            print('  remove', nm)
            bpy.data.objects.remove(o, do_unlink=True)

    # Char existing iron frames / ribs
    for nm in ('frame_SY_north_transept__lost1866', 'north_transept_vault_ribs',
               'SY_north_transept__lost1866_frame'):
        o = bpy.data.objects.get(nm)
        if not o or o.type != 'MESH':
            continue
        if o.data.materials:
            o.data.materials[0] = char
        else:
            o.data.materials.append(char)
        print('  charred', nm)

    # Warp: add many twisted/fallen girders in and around the bay (ILN)
    for i in range(55):
        x = rs.uniform(NX0 - 4, NX1 + 8)
        y = rs.uniform(NY0 - 5, NY1 + 5)
        z0 = rs.uniform(0.2, 4.0)
        span = rs.uniform(8, 28)
        rise = rs.uniform(-2, 18)
        ang = rs.uniform(0, math.pi * 2)
        # sagging arc
        p0 = (x, y, z0)
        mid = (x + math.cos(ang)*span*0.5, y + math.sin(ang)*span*0.5, z0 + rise)
        p1 = (x + math.cos(ang)*span, y + math.sin(ang)*span, max(0.3, z0 + rs.uniform(-1, 6)))
        strut(f's67b_twist_{i:02d}a', scar, char, p0, mid, r=rs.uniform(0.25, 0.7))
        strut(f's67b_twist_{i:02d}b', scar, char, mid, p1, r=rs.uniform(0.2, 0.55))

    # Standing stripped cage uprights (ILN left of colossi)
    for i in range(10):
        x = NX0 + 1.5 + i * 2.2
        for y in (-38.0, -30.0, 20.0, 30.0):
            h = rs.uniform(18, 32)
            lean = rs.uniform(-3, 3)
            strut(f's67b_upright_{i}_{int(y)}', scar, char,
                  (x, y, 0.0), (x + lean, y + rs.uniform(-1,1), h), r=0.55)

    # Collapsed wing stubs east of bay (charred short wall remnants)
    box('s67b_collapsed_wing_E', scar, soot, NX1, NX1 + 14, -20, 20, 0.0, rs.uniform(4, 9))
    box('s67b_collapsed_wing_W', scar, soot, NX0 - 12, NX0, -15, 15, 0.0, rs.uniform(3, 7))

    # Rubble / debris field (dark ground)
    box('s67b_ash_ground', scar, mat_rgb('s67b_ash', (0.07, 0.06, 0.05), 0.98),
        NX0 - 15, NX1 + 20, NY0 - 8, NY1 + 8, -0.15, 0.45)
    for i in range(40):
        x = rs.uniform(NX0 - 10, NX1 + 15)
        y = rs.uniform(NY0 - 5, NY1 + 5)
        s = rs.uniform(0.8, 3.5); h = rs.uniform(0.5, 2.8)
        box(f's67b_rubble_{i:02d}', scar, rubble_m, x-s, x+s, y-s*0.6, y+s*0.6, 0.3, 0.3+h)

    # Blackened / broken glazing on adjacent nave near the cut
    nave = bpy.data.objects.get('nave_vault_glass')
    if nave and nave.data.materials:
        # assign broken-glass mat to object (whole vault — heavy but reads)
        # Better: duplicate a dark patch boxes over adjacent bays as boarded/black panes
        pass
    for i, x0 in enumerate((135.0, 140.0, 145.0, 173.0, 178.0, 183.0)):
        box(f's67b_black_glaze_{i}', scar, glass_b,
            x0, x0 + 4.5, -40, 40, 8.0, 22.0)

    # Smoke stain volumes (billowy dark near gap) — mesh cards with dark translucent mat
    smoke = mat_rgb('s67b_smoke_stain', (0.25, 0.25, 0.26), rough=1.0)
    smoke.blend_method = 'HASHED' if hasattr(smoke, 'blend_method') else smoke.blend_method
    for i, (cx, cy, cz, sx, sy, sz) in enumerate((
        (161, -10, 28, 25, 20, 12),
        (155, 15, 22, 18, 14, 10),
        (170, -25, 20, 14, 12, 8),
    )):
        box(f's67b_smoke_stain_{i}', scar, smoke,
            cx-sx, cx+sx, cy-sy, cy+sy, cz-sz, cz+sz)
        o = bpy.data.objects[f's67b_smoke_stain_{i}']
        o.visible_shadow = False

def char_colossi(char_stone):
    col = bpy.data.collections.get('SY56_north_transept_colossi_muse__lost1866')
    if not col:
        print('  no colossi collection'); return
    n = 0
    for o in col.objects:
        if o.type != 'MESH' or not o.data:
            continue
        # soot-tint existing mats by replacing with charred stone copy
        if o.data.materials:
            for i, slot in enumerate(o.material_slots):
                if slot.material:
                    nm = slot.material.name + '_s67b_soot'
                    if nm not in bpy.data.materials:
                        mc = slot.material.copy(); mc.name = nm
                        for node in mc.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED' and 'Base Color' in node.inputs:
                                c = list(node.inputs['Base Color'].default_value)
                                node.inputs['Base Color'].default_value = (c[0]*0.25, c[1]*0.22, c[2]*0.18, c[3])
                                node.inputs['Roughness'].default_value = 0.95
                        slot.material = mc
                    else:
                        slot.material = bpy.data.materials[nm]
        n += 1
    print(f'  sooted {n} colossi mesh objects')

def patch_post66_live_white_slab():
    """KEEP fix: remove leftover north-transept frame stub from live post66-r10."""
    if not os.path.isfile(POST66_LIVE):
        print('no post66 live'); return
    bpy.ops.wm.open_mainfile(filepath=POST66_LIVE)
    removed = 0
    for nm in list(bpy.data.objects.keys()):
        if 'north_transept__lost1866' in nm or nm.startswith('frame_SY_north_transept'):
            bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
            removed += 1
    if 'SY_north_transept__lost1866' in bpy.data.collections:
        c = bpy.data.collections['SY_north_transept__lost1866']
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
    bpy.ops.wm.save_as_mainfile(filepath=POST66_LIVE)
    print(f'post66 live: removed {removed} leftover north-transept objs (white-slab KEEP fix)')

def main():
    shutil.copy2(SRC, OUT)
    bpy.ops.wm.open_mainfile(filepath=OUT)
    print('S67b from', SRC)

    root = bpy.data.collections.get('SY-EARLY_c1856') or bpy.context.scene.collection
    scar = bpy.data.collections.new('SY_S67b_fire_ruins__cand')
    try:
        root.children.link(scar)
    except Exception:
        bpy.context.scene.collection.children.link(scar)

    char = mat_charred_iron()
    glass_b = mat_broken_glass()
    rubble_m = mat_rubble()
    soot = mat_soot_stone()

    destroy_north_transept(scar, char, glass_b, rubble_m, soot)
    char_colossi(soot)
    set_overcast_winter_sky()
    reframe_fire_cams()

    scar['credit'] = 'S67b ILN 1867-01-05/12 fire ruins CANDIDATE — overcast Jan 1867 sky departure'
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print('CANDIDATE saved', OUT)

    # live post66 white-slab / leftover frame KEEP fix
    patch_post66_live_white_slab()

if __name__ == '__main__':
    main()
