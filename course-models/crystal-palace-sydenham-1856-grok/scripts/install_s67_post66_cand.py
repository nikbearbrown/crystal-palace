"""CANDIDATE S67: dress SY-POST66 for CP047/CP048 with 1866-67 north-transept fire scar
evidence from muse-round2 S67 (ILN 1867-01-05/12). Does not rebuild EARLY.
- Remove leftover north-transept frame stub that survived into post66-r10.
- Scorched ground + warped iron remnants on former north-transept footprint.
- Sooted/charred blanking at the cut (north face of former bay).
- Darken adjacent nave iron near the fire zone.
CANDIDATE only — live starts untouched.
"""
import bpy, math, os, shutil, random
from mathutils import Vector, Matrix

SY = '/workspace/crystal-palace-sydenham/course-models/crystal-palace-sydenham-1856-grok'
SRC = os.path.join(SY, 'rounds/sydenham-post66-r10.blend')
OUT = os.path.join(SY, 'rounds/sydenham-post66-s67-cand.blend')

# Former north transept footprint (model feet) — matches EARLY vault extents
NX0, NX1 = 149.5, 172.5
NY0, NY1 = -40.5, 40.5
GZ = -6.0  # approx terrace/ground near garden front cams (cams at z~-5.6)

def mat(name, rgb, rough=0.9):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*rgb, 1)
    bsdf.inputs['Roughness'].default_value = rough
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_charred(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 12
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.0
    cr.color_ramp.elements[0].color = (0.02, 0.015, 0.012, 1)
    cr.color_ramp.elements[1].position = 1.0
    cr.color_ramp.elements[1].color = (0.12, 0.08, 0.05, 1)
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Metallic'].default_value = 0.15
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def box_mesh(name, col, mat_, x0, x1, y0, y1, z0, z1):
    me = bpy.data.meshes.new(name)
    verts = [
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1),
    ]
    faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me.from_pydata(verts, [], faces); me.update()
    me.materials.append(mat_)
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    return o

def cylinder_between(name, col, mat_, p0, p1, r=0.35, seg=8):
    """Simple tapered strut as a stretched cube approx."""
    me = bpy.data.meshes.new(name)
    d = Vector(p1) - Vector(p0)
    length = d.length
    if length < 1e-3:
        return None
    # build along Z then rotate
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r*0.85,
                          depth=length, matrix=Matrix.Identity(4))
    # align +Z to d
    quat = Vector((0,0,1)).rotation_difference(d.normalized())
    bmesh.ops.rotate(bm, cent=(0,0,0), matrix=quat.to_matrix(), verts=bm.verts)
    mid = (Vector(p0) + Vector(p1)) * 0.5
    bmesh.ops.translate(bm, verts=bm.verts, vec=mid)
    bm.to_mesh(me); bm.free()
    me.materials.append(mat_)
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    return o

def main():
    shutil.copy2(SRC, OUT)
    bpy.ops.wm.open_mainfile(filepath=OUT)
    print('S67 cand from', SRC)

    # --- remove leftover north-transept stub ---
    for nm in list(bpy.data.objects.keys()):
        if 'north_transept__lost1866' in nm or nm.startswith('frame_SY_north_transept'):
            o = bpy.data.objects[nm]
            print('  remove leftover', nm)
            bpy.data.objects.remove(o, do_unlink=True)
    if 'SY_north_transept__lost1866' in bpy.data.collections:
        c = bpy.data.collections['SY_north_transept__lost1866']
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
        print('  removed collection SY_north_transept__lost1866')

    # --- S67 fire-scar collection ---
    root = bpy.data.collections.get('SY-POST66_c1868') or bpy.context.scene.collection
    scar = bpy.data.collections.new('SY_POST66_S67_fire_scar__cand')
    root.children.link(scar)

    ash = mat('s67_ash_scorched_ground', (0.09, 0.07, 0.05), 0.97)
    char = mat_charred('s67_charred_iron')
    soot = mat('s67_soot_blanking', (0.18, 0.16, 0.14), 0.92)
    rubble = mat('s67_rubble_brick', (0.28, 0.18, 0.12), 0.9)

    # Scorched ground pad on former footprint (slightly proud of terrace)
    # Use cam-relative ground: garden front ~ z=-6 to -8
    z_g = -7.2
    box_mesh('s67_scorch_pad', scar, ash, NX0 - 2, NX1 + 2, NY0 - 2, NY1 + 2, z_g, z_g + 0.35)

    # Charred blanking wall on the south face of the former bay (where nave was cut / infilled edge)
    # A dark temporary / fire-scarred vertical face facing the camera approaches from -Y
    box_mesh('s67_charred_blanking_south', scar, soot,
             NX0, NX1, NY0 - 0.4, NY0 + 0.4, z_g, z_g + 18.0)
    # thin north blanking too
    box_mesh('s67_charred_blanking_north', scar, soot,
             NX0, NX1, NY1 - 0.4, NY1 + 0.4, z_g, z_g + 14.0)

    # Warped iron remnants (S67 engraving: curved girders amid debris) — density I
    rs = random.Random(1866)
    for i in range(28):
        x = rs.uniform(NX0 + 1, NX1 - 1)
        y = rs.uniform(NY0 + 2, NY1 - 2)
        z0 = z_g + 0.3
        # kinked / arched remnant
        span = rs.uniform(6, 16)
        rise = rs.uniform(2, 9)
        ang = rs.uniform(0, math.pi)
        dx, dy = math.cos(ang) * span, math.sin(ang) * span
        mid = (x + dx * 0.5, y + dy * 0.5, z0 + rise)
        p0 = (x, y, z0 + rs.uniform(0, 1.5))
        p1 = (x + dx, y + dy, z0 + rs.uniform(0, 2))
        cylinder_between(f's67_warped_iron_{i:02d}a', scar, char, p0, mid, r=rs.uniform(0.25, 0.55))
        cylinder_between(f's67_warped_iron_{i:02d}b', scar, char, mid, p1, r=rs.uniform(0.2, 0.45))

    # Rubble piles near blanking (I)
    for i in range(12):
        x = rs.uniform(NX0, NX1)
        y = rs.uniform(NY0 - 1, NY0 + 8)
        s = rs.uniform(1.2, 3.5)
        h = rs.uniform(0.8, 2.4)
        box_mesh(f's67_rubble_{i:02d}', scar, rubble,
                 x - s, x + s, y - s * 0.7, y + s * 0.7, z_g, z_g + h)

    # Soot-darken nearby nave / gallery iron materials (multiply base color)
    fire_zone_x = (NX0 - 20, NX1 + 30)
    darkened = 0
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.data or not o.data.materials:
            continue
        # skip our new scar objs
        if o.name.startswith('s67_'):
            continue
        # rough world centre
        try:
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            cx = sum(v.x for v in bb) / 8
        except Exception:
            continue
        if not (fire_zone_x[0] <= cx <= fire_zone_x[1]):
            continue
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.use_nodes:
                continue
            # clone per-object soot tint so we don't mutate shared EARLY mats permanently in this cand file only
            nm = m.name + '_s67soot'
            if nm in bpy.data.materials:
                slot.material = bpy.data.materials[nm]
                continue
            mc = m.copy(); mc.name = nm
            for n in mc.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED' and 'Base Color' in n.inputs:
                    c = list(n.inputs['Base Color'].default_value)
                    n.inputs['Base Color'].default_value = (c[0] * 0.45, c[1] * 0.42, c[2] * 0.40, c[3])
                    if 'Roughness' in n.inputs:
                        n.inputs['Roughness'].default_value = min(1.0, n.inputs['Roughness'].default_value + 0.15)
            slot.material = mc
            darkened += 1
    print('  soot-darkened material slots near fire zone:', darkened)

    # Tag
    scar['credit'] = 'S67 ILN 1867-01-05/12 (muse-round2) — fire scar dressing CANDIDATE'
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print('CANDIDATE saved', OUT)

if __name__ == '__main__':
    main()
