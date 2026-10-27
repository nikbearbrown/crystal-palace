"""Build recognisable Hawkins 1854 Crystal Palace sculptures (candidate pack).
Run: blender -b --python build_hawkins_sculptures.py
Outputs: ../hawkins-dinosaurs.blend + preview renders.
"""
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix, Quaternion

random.seed(54)
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RES = 12  # loft ring segments

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for d in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for x in list(d): d.remove(x)

def mat_stone(name, top, belly, rough=0.72, scale=18.0, bump=0.45, **_kw):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location=(700,0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location=(450,0)
    bsdf.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location=(-700,0)
    # scale / cracked-cement look via Voronoi
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location=(-450,120)
    vor.feature='F1'; vor.inputs['Scale'].default_value = scale
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.location=(-150,120)
    cr.color_ramp.elements[0].position=0.0; cr.color_ramp.elements[0].color=(*top,1)
    cr.color_ramp.elements[1].position=1.0; cr.color_ramp.elements[1].color=(*belly,1)
    # moss mottling
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.location=(-450,-100)
    nz.inputs['Scale'].default_value=3.5; nz.inputs['Detail'].default_value=8
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type='RGBA'; mix.location=(150,80)
    mix.inputs['Factor'].default_value=0.35
    mix.inputs[7].default_value=(top[0]*0.55, top[1]*0.65, top[2]*0.45, 1)
    bumpn = nt.nodes.new('ShaderNodeBump'); bumpn.location=(250,-80)
    bumpn.inputs['Strength'].default_value=bump
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(vor.outputs['Distance'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], mix.inputs[6])
    nt.links.new(nz.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    nt.links.new(vor.outputs['Distance'], bumpn.inputs['Height'])
    nt.links.new(bumpn.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m

def loft_mesh(name, stations, segs=RES, closed=False):
    """stations: list of (cx,cy,cz, rx, ry) — elliptical rings in local Y-up? 
    Rings in XZ plane progressing along +X (head direction)."""
    verts=[]; faces=[]
    n=len(stations)
    for i,(cx,cy,cz,rx,ry) in enumerate(stations):
        for j in range(segs):
            a=2*math.pi*j/segs
            # ring in YZ, progress along X
            y=cy+rx*math.cos(a); z=cz+ry*math.sin(a)
            verts.append((cx,y,z))
    for i in range(n-1):
        for j in range(segs):
            a=i*segs+j; b=i*segs+((j+1)%segs)
            c=(i+1)*segs+((j+1)%segs); d=(i+1)*segs+j
            faces.append((a,b,c,d))
    # caps
    # front (head) center
    hx,hy,hz,hrx,hry=stations[-1]
    hi=len(verts); verts.append((hx+hrx*0.15, hy, hz))
    for j in range(segs):
        faces.append(((n-1)*segs+j, (n-1)*segs+((j+1)%segs), hi))
    tx,ty,tz,trx,try_=stations[0]
    ti=len(verts); verts.append((tx-trx*0.1, ty, tz))
    for j in range(segs):
        faces.append((j, ti, (j+1)%segs))
    me=bpy.data.meshes.new(name)
    me.from_pydata(verts,[],faces); me.update()
    for p in me.polygons: p.use_smooth=True
    return me

def add_cone(bm, base, tip, r0, segs=8):
    b,t=Vector(base),Vector(tip); d=t-b
    if d.length<1e-6: return
    res=bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs,
                              radius1=r0, radius2=0.01, depth=d.length)
    q=Vector((0,0,1)).rotation_difference(d.normalized())
    bmesh.ops.transform(bm, matrix=Matrix.Translation((b+t)/2) @ q.to_matrix().to_4x4(), verts=res['verts'])

def merge_mesh(base_me, extra_fn):
    bm=bmesh.new(); bm.from_mesh(base_me)
    extra_fn(bm)
    bm.to_mesh(base_me); bm.free(); base_me.update()
    return base_me

def leg_stations(hip, ankle, foot, r_hip, r_ankle):
    """Simple limb as loft along path."""
    hx,hy,hz=hip; ax,ay,az=ankle; fx,fy,fz=foot
    return [
        (hx, hy, hz, r_hip, r_hip*0.9),
        ((hx+ax)/2, (hy+ay)/2, (hz+az)/2, (r_hip+r_ankle)/2, (r_hip+r_ankle)/2*0.9),
        (ax, ay, az, r_ankle, r_ankle*0.85),
        (fx, fy, fz+0.08, r_ankle*1.3, 0.12),
    ]

def join_objects(name, objs, mat):
    """Join meshes into one object."""
    bpy.ops.object.select_all(action='DESELECT')
    ctx_objs=[]
    for o in objs:
        if o.data.materials: o.data.materials[0]=mat
        else: o.data.materials.append(mat)
        ctx_objs.append(o)
    bpy.context.view_layer.objects.active = ctx_objs[0]
    for o in ctx_objs: o.select_set(True)
    bpy.ops.object.join()
    ob=bpy.context.view_layer.objects.active
    ob.name=name; ob.data.name=name
    # origin to geometry bottom-ish
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # shift so z min ~ 0
    zs=[(ob.matrix_world @ v.co).z for v in ob.data.vertices]
    zmin=min(zs)
    ob.location.z -= zmin
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    for p in ob.data.polygons: p.use_smooth=True
    if 'ES' not in ob.modifiers:
        m=ob.modifiers.new('ES','EDGE_SPLIT'); m.split_angle=math.radians(35)
    return ob

def make_obj(name, me, mat, loc=(0,0,0)):
    if me.materials: me.materials[0]=mat
    else: me.materials.append(mat)
    o=bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location=loc
    return o

# ---------------- materials (stone-grey / green-grey) ----------------
def mats():
    return {
        'ig': mat_stone('Hawkins_Iguanodon_green_grey', (0.28,0.32,0.24), (0.38,0.36,0.28), scale=22, bump=0.85, rough=0.82),
        'meg': mat_stone('Hawkins_Megalosaurus_stone_grey', (0.32,0.34,0.30), (0.42,0.40,0.34), scale=18, bump=0.9, rough=0.8),
        'hyl': mat_stone('Hawkins_Hylaeosaurus_green_grey', (0.26,0.30,0.22), (0.36,0.34,0.26), scale=24, bump=0.75, rough=0.84),
        'ple': mat_stone('Hawkins_Plesiosaur_stone_grey', (0.30,0.32,0.30), (0.40,0.38,0.32), scale=28, bump=0.55, rough=0.78),
        'ich': mat_stone('Hawkins_Ichthyosaur_slate_grey', (0.24,0.28,0.30), (0.34,0.36,0.34), scale=30, bump=0.65, rough=0.8),
    }

# ---------------- builders ----------------
def build_iguanodon_standing(M):
    # Body stations along +X (tail -> head). Length ~10.5 m, height ~3.0 m
    body = [
        (-5.2, 0, 1.1, 0.35, 0.30),   # tail tip
        (-4.0, 0, 1.35, 0.55, 0.50),
        (-2.5, 0, 1.7, 0.95, 0.85),
        (-1.0, 0, 2.0, 1.25, 1.15),   # hips
        (0.5, 0, 2.15, 1.35, 1.25),   # mid
        (2.0, 0, 2.25, 1.40, 1.30),   # shoulders / chest
        (3.2, 0, 2.20, 1.15, 1.10),
        (4.0, 0, 2.15, 0.85, 0.80),   # neck base
        (4.7, 0, 2.25, 0.55, 0.55),   # neck
        (5.3, 0, 2.20, 0.70, 0.55),   # skull
        (5.9, 0, 2.05, 0.45, 0.40),   # snout
        (6.35, 0, 1.95, 0.22, 0.22),  # nose
    ]
    me=loft_mesh('ig_standing_body', body, segs=14)
    def extras(bm):
        # nose horn (Hawkins/Owen thumb-spike-as-horn)
        add_cone(bm, (6.15,0,2.25), (6.25,0,2.95), 0.18, segs=7)
        # dorsal ridge nubs
        for i,x in enumerate([x*0.7-3.5 for x in range(12)]):
            z=2.15+0.9*math.sqrt(max(0,1-(x/4.5)**2))
            add_cone(bm, (x,0,z), (x-0.05,0,z+0.28), 0.12, segs=5)
        # teeth hint
        for s in (-1,1):
            for i in range(5):
                add_cone(bm, (5.5+i*0.12, s*0.25, 1.95), (5.5+i*0.12, s*0.25, 1.78), 0.04, segs=4)
    merge_mesh(me, extras)
    body_o=make_obj('_tmp_ig_body', me, M['ig'])
    # Legs — pillar-like
    legs=[]
    for s in (-1,1):
        # fore
        st=leg_stations((3.0,s*0.85,1.7),(3.15,s*1.05,0.55),(3.35,s*1.1,0.05),0.38,0.28)
        legs.append(make_obj(f'_lf{s}', loft_mesh(f'ig_lf{s}', st, segs=10), M['ig']))
        # hind
        st=leg_stations((-1.2,s*0.95,1.6),(-1.0,s*1.15,0.55),(-0.75,s*1.2,0.05),0.45,0.32)
        legs.append(make_obj(f'_lh{s}', loft_mesh(f'ig_lh{s}', st, segs=10), M['ig']))
    return join_objects('hawkins_iguanodon_standing', [body_o]+legs, M['ig'])

def build_iguanodon_recumbent(M):
    # lower body, legs folded out
    body = [
        (-5.0, 0, 0.55, 0.30, 0.25),
        (-3.8, 0, 0.75, 0.50, 0.45),
        (-2.2, 0, 1.05, 0.95, 0.80),
        (-0.6, 0, 1.25, 1.20, 1.00),
        (1.0, 0, 1.35, 1.30, 1.10),
        (2.6, 0, 1.40, 1.25, 1.05),
        (3.8, 0, 1.45, 0.95, 0.85),
        (4.6, 0, 1.55, 0.60, 0.55),
        (5.3, 0, 1.70, 0.70, 0.55),  # head raised
        (5.9, 0, 1.75, 0.45, 0.40),
        (6.3, 0, 1.65, 0.22, 0.22),
    ]
    me=loft_mesh('ig_rec_body', body, segs=14)
    def extras(bm):
        add_cone(bm, (6.1,0,1.90), (6.2,0,2.45), 0.16, segs=7)
        for i,x in enumerate([x*0.65-3.2 for x in range(11)]):
            z=1.35+0.7*math.sqrt(max(0,1-(x/4.2)**2))
            add_cone(bm, (x,0,z), (x,0,z+0.22), 0.10, segs=5)
        for s in (-1,1):
            for i in range(4):
                add_cone(bm, (5.5+i*0.12, s*0.22, 1.55), (5.5+i*0.12, s*0.22, 1.40), 0.035, segs=4)
    merge_mesh(me, extras)
    body_o=make_obj('_tmp_igr', me, M['ig'])
    legs=[]
    for s in (-1,1):
        # folded fore — elbow out
        st=[(2.8,s*0.6,1.0,0.35,0.30),(3.2,s*1.4,0.7,0.30,0.25),(3.6,s*1.7,0.25,0.28,0.18),(3.9,s*1.75,0.08,0.35,0.10)]
        legs.append(make_obj(f'_rf{s}', loft_mesh(f'igr_f{s}', st, segs=10), M['ig']))
        st=[(-1.0,s*0.7,1.0,0.40,0.35),(-0.5,s*1.5,0.75,0.35,0.28),(0.2,s*1.8,0.28,0.30,0.18),(0.5,s*1.85,0.08,0.38,0.10)]
        legs.append(make_obj(f'_rh{s}', loft_mesh(f'igr_h{s}', st, segs=10), M['ig']))
    return join_objects('hawkins_iguanodon_recumbent', [body_o]+legs, M['ig'])

def build_megalosaurus(M):
    # shoulder hump peak ~3.5 m
    body = [
        (-5.0, 0, 1.0, 0.30, 0.25),
        (-3.8, 0, 1.4, 0.55, 0.50),
        (-2.4, 0, 1.9, 1.00, 0.95),
        (-1.0, 0, 2.3, 1.20, 1.20),
        (0.4, 0, 2.7, 1.30, 1.40),   # hump rising
        (1.6, 0, 3.0, 1.25, 1.50),   # shoulder hump peak
        (2.8, 0, 2.85, 1.10, 1.25),
        (3.8, 0, 2.70, 0.80, 0.85),  # neck
        (4.6, 0, 2.65, 0.55, 0.55),
        (5.3, 0, 2.55, 0.65, 0.45),  # long snout skull
        (6.0, 0, 2.40, 0.40, 0.30),
        (6.5, 0, 2.25, 0.18, 0.15),
    ]
    me=loft_mesh('meg_body', body, segs=14)
    def extras(bm):
        # open lower jaw
        jaw=[(4.4,0,2.25,0.35,0.18),(5.2,0,2.05,0.30,0.14),(5.9,0,1.95,0.18,0.10),(6.3,0,1.90,0.08,0.06)]
        # build jaw as separate cones for teeth
        for s in (-1,1):
            for i in range(8):
                x=4.7+i*0.2
                add_cone(bm, (x, s*0.28, 2.35), (x, s*0.28, 2.15), 0.05, segs=4)
                add_cone(bm, (x+0.05, s*0.22, 2.10), (x+0.05, s*0.22, 2.28), 0.045, segs=4)
        # brow bosses
        for s in (-1,1):
            add_cone(bm, (5.0, s*0.45, 2.75), (5.05, s*0.55, 2.95), 0.12, segs=6)
    merge_mesh(me, extras)
    # add jaw loft
    jaw_st=[(4.5,0,2.20,0.40,0.16),(5.3,0,2.00,0.32,0.12),(6.0,0,1.92,0.18,0.08),(6.35,0,1.88,0.07,0.05)]
    jaw_me=loft_mesh('meg_jaw', jaw_st, segs=10)
    body_o=make_obj('_meg_b', me, M['meg'])
    jaw_o=make_obj('_meg_j', jaw_me, M['meg'])
    legs=[]
    for s in (-1,1):
        st=leg_stations((2.4,s*0.8,1.9),(2.55,s*1.0,0.55),(2.75,s*1.05,0.05),0.36,0.26)
        legs.append(make_obj(f'_mf{s}', loft_mesh(f'meg_f{s}', st, segs=10), M['meg']))
        st=leg_stations((-1.4,s*0.9,1.7),(-1.2,s*1.1,0.55),(-0.95,s*1.15,0.05),0.42,0.30)
        legs.append(make_obj(f'_mh{s}', loft_mesh(f'meg_h{s}', st, segs=10), M['meg']))
    return join_objects('hawkins_megalosaurus', [body_o,jaw_o]+legs, M['meg'])

def build_hylaeosaurus(M):
    body=[
        (-4.0,0,0.7,0.25,0.22),
        (-2.8,0,1.0,0.55,0.50),
        (-1.4,0,1.3,0.95,0.80),
        (0.0,0,1.45,1.10,0.95),
        (1.4,0,1.50,1.05,0.90),
        (2.6,0,1.45,0.75,0.70),
        (3.4,0,1.40,0.45,0.42),
        (4.0,0,1.35,0.50,0.40),
        (4.5,0,1.25,0.28,0.25),
        (4.9,0,1.15,0.14,0.12),
    ]
    me=loft_mesh('hyl_body', body, segs=12)
    def extras(bm):
        # single dorsal row of large spines (Hawkins reading)
        for i in range(14):
            x=3.2 - i*0.55
            top=1.45+0.7*math.sqrt(max(0,1-(x/3.5)**2)) if abs(x)<3.5 else 1.2
            ht=1.1*math.exp(-((x)/3.2)**2)+0.35
            add_cone(bm, (x,0,top), (x-0.15,0,top+ht), 0.20, segs=6)
        # flank scutes
        for s in (-1,1):
            for i in range(7):
                x=2.5-i*0.7
                add_cone(bm, (x,s*0.9,1.5), (x-0.05,s*1.25,1.85), 0.12, segs=5)
    merge_mesh(me, extras)
    body_o=make_obj('_hyl_b', me, M['hyl'])
    legs=[]
    for s in (-1,1):
        st=[(1.8,s*0.55,1.1,0.28,0.24),(2.0,s*1.2,0.7,0.24,0.20),(2.2,s*1.45,0.2,0.22,0.14),(2.4,s*1.5,0.06,0.28,0.08)]
        legs.append(make_obj(f'_hf{s}', loft_mesh(f'hyl_f{s}', st, segs=8), M['hyl']))
        st=[(-1.2,s*0.6,1.05,0.32,0.28),(-1.4,s*1.25,0.7,0.28,0.22),(-1.3,s*1.5,0.2,0.24,0.14),(-1.1,s*1.55,0.06,0.30,0.08)]
        legs.append(make_obj(f'_hh{s}', loft_mesh(f'hyl_h{s}', st, segs=8), M['hyl']))
    return join_objects('hawkins_hylaeosaurus', [body_o]+legs, M['hyl'])

def build_plesiosaur(M, curl=1.0):
    # long swan neck raised
    body=[
        (-2.8,0,0.5,0.18,0.15),  # tail
        (-1.8,0,0.7,0.40,0.35),
        (-0.6,0,0.95,0.85,0.65),
        (0.6,0,1.05,1.00,0.75),  # torso
        (1.6,0,1.00,0.70,0.55),
        (2.2,0,1.15,0.35,0.32),  # neck base
        (2.6,0,1.55,0.28,0.26),
        (2.9,0,2.10,0.24,0.22),
        (3.15,0,2.55,0.22,0.20),
        (3.4,0,2.85,0.28,0.22),  # head
        (3.75,0,2.80,0.18,0.14),
        (4.0,0,2.70,0.08,0.07),
    ]
    me=loft_mesh('ple_body', body, segs=12)
    def extras(bm):
        for s in (-1,1):
            for i in range(4):
                add_cone(bm, (3.45+i*0.08, s*0.12, 2.70), (3.45+i*0.08, s*0.12, 2.58), 0.025, segs=4)
    merge_mesh(me, extras)
    body_o=make_obj('_ple_b', me, M['ple'])
    # paddles
    pads=[]
    for s in (-1,1):
        for x,yl in ((0.8,1.35),(-0.5,1.2)):
            st=[(x,s*0.5,0.7,0.25,0.12),(x+0.15,s*yl,0.55,0.45,0.08),(x+0.35,s*(yl+0.3),0.45,0.35,0.05),(x+0.55,s*(yl+0.15),0.40,0.15,0.03)]
            pads.append(make_obj(f'_pp{s}{x}', loft_mesh(f'ple_p{s}{x}', st, segs=8), M['ple']))
    return join_objects('hawkins_plesiosaur', [body_o]+pads, M['ple'])

def build_ichthyosaur(M, lift=12.0):
    body=[
        (-3.5,0,0.6,0.20,0.15),
        (-2.4,0,0.85,0.45,0.40),
        (-1.0,0,1.15,0.85,0.75),
        (0.4,0,1.30,1.00,0.90),
        (1.6,0,1.35,0.90,0.85),
        (2.6,0,1.40,0.70,0.70),  # head region
        (3.3,0,1.35,0.45,0.45),
        (3.9,0,1.25,0.28,0.25),
        (4.4,0,1.15,0.14,0.12),
    ]
    me=loft_mesh('ich_body', body, segs=14)
    def extras(bm):
        # sclerotic ring eyes — Hawkins signature
        for s in (-1,1):
            r=bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16,
                                    radius1=0.38, radius2=0.30, depth=0.12)
            m=Matrix.Translation(Vector((2.7, s*0.72, 1.55))) @ Matrix.Rotation(-s*math.pi/2, 4, 'X')
            bmesh.ops.transform(bm, matrix=m, verts=r['verts'])
        # dorsal fin
        add_cone(bm, (0.2,0,2.0), (0.0,0,2.7), 0.25, segs=6)
        # tail fluke hint
        add_cone(bm, (-3.3,0,0.7), (-3.8,0,1.3), 0.15, segs=5)
        add_cone(bm, (-3.3,0,0.5), (-3.7,0,0.15), 0.12, segs=5)
    merge_mesh(me, extras)
    body_o=make_obj('_ich_b', me, M['ich'])
    pads=[]
    for s in (-1,1):
        for x,yl in ((1.2,1.1),(-0.8,0.95)):
            st=[(x,s*0.4,0.8,0.22,0.10),(x+0.1,s*yl,0.55,0.40,0.07),(x+0.3,s*(yl+0.25),0.40,0.28,0.04)]
            pads.append(make_obj(f'_ip{s}{x}', loft_mesh(f'ich_p{s}{x}', st, segs=8), M['ich']))
    ob=join_objects('hawkins_ichthyosaur', [body_o]+pads, M['ich'])
    # tip nose slightly up
    ob.rotation_euler=(0, math.radians(-lift), 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    # re-ground
    zs=[v.co.z for v in ob.data.vertices]; ob.location.z -= min(zs)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    return ob

def setup_preview_light():
    sun=bpy.data.lights.new('Sun', 'SUN'); sun.energy=3.5
    so=bpy.data.objects.new('Sun', sun); bpy.context.collection.objects.link(so)
    so.rotation_euler=(math.radians(45),0,math.radians(35))
    world=bpy.data.worlds.new('W'); bpy.context.scene.world=world
    world.use_nodes=True
    bg=world.node_tree.nodes['Background']; bg.inputs[1].default_value=0.4

def main():
    clear()
    M=mats()
    # place in a row for pack preview
    objs=[]
    o=build_iguanodon_standing(M); o.location=(0,0,0); objs.append(o)
    o=build_iguanodon_recumbent(M); o.location=(14,0,0); objs.append(o)
    o=build_megalosaurus(M); o.location=(28,0,0); objs.append(o)
    o=build_hylaeosaurus(M); o.location=(42,0,0); objs.append(o)
    o=build_plesiosaur(M); o.location=(54,0,0); objs.append(o)
    o=build_ichthyosaur(M); o.location=(64,0,0); objs.append(o)
    setup_preview_light()
    for o in bpy.data.objects:
        if o.type=='MESH' and o.name.startswith('hawkins_'):
            print(o.name, 'dim', [round(v,2) for v in o.dimensions], 'verts', len(o.data.vertices))
    path=os.path.join(OUT, 'hawkins-dinosaurs.blend')
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print('saved', path)

if __name__=='__main__':
    main()
