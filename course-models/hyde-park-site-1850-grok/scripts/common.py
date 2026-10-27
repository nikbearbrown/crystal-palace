"""Scene helpers shared by the Grok HP-SITE and MOVE builds (materials, objects, world, cameras, figures)."""
import bpy, math, json, os
from mathutils import Vector
FT = 0.3048
def ft(v): return v * FT
def mat(name, rgb, rough=0.8, metal=0.0, emit=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    m.diffuse_color = (*rgb, 1); return m
def noisy_mat(name, c0, c1, scale=0.05, rough=0.9, bump=0.0, detail=4.0):
    """ground-type material: two colours mixed by object-space noise (scale in 1/m)"""
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n["Principled BSDF"]; tc = n.new("ShaderNodeTexCoord"); no = n.new("ShaderNodeTexNoise")
    no.inputs["Scale"].default_value = scale; no.inputs["Detail"].default_value = detail
    l.new(tc.outputs["Object"], no.inputs["Vector"])
    r = n.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = (*c0, 1); r.color_ramp.elements[1].color = (*c1, 1)
    l.new(no.outputs["Fac"], r.inputs[0]); l.new(r.outputs[0], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    if bump:
        no2 = n.new("ShaderNodeTexNoise"); no2.inputs["Scale"].default_value = 40.0; l.new(tc.outputs["Object"], no2.inputs["Vector"])
        bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump
        l.new(no2.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*[(a + c) / 2 for a, c in zip(c0, c1)], 1); return m
COLLS = {}
def coll(name, parent):
    if name in COLLS: return COLLS[name]
    c = bpy.data.collections.new(name); parent.children.link(c); COLLS[name] = c; return c
def obj(name, me, c, loc=(0, 0, 0), rz=0.0, **props):
    o = bpy.data.objects.new(name, me); o.location = [ft(v) for v in loc]; o.rotation_euler = (0, 0, rz); c.objects.link(o)
    for k, v in props.items(): o[k] = v
    return o
def world(sun_elev=38, sun_rot=200, strength=0.35, sun_energy=3.2, exposure=-0.4, sun_color=(1.0, 0.96, 0.9)):
    sc = bpy.context.scene
    w = bpy.data.worlds.new("GT_World"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; sky = w.node_tree.nodes.new("ShaderNodeTexSky")
    try: sky.sky_type = 'NISHITA'
    except TypeError: pass
    try: sky.sun_elevation = math.radians(sun_elev); sky.sun_rotation = math.radians(sun_rot)
    except AttributeError: pass
    try: sky.sun_disc = False          # the lamp is the sun; the sky's own disc doubled it (MV log)
    except AttributeError: pass
    w.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = strength
    s = bpy.data.lights.new("GT_Sun", 'SUN'); s.energy = sun_energy; s.angle = math.radians(0.6); s.color = sun_color
    so = bpy.data.objects.new("GT_Sun", s); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(90 - sun_elev), 0, math.radians(sun_rot - 180 + 90))
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64; sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6; sc.cycles.transparent_max_bounces = 32
    sc.render.resolution_x = 1920; sc.render.resolution_y = 1080
    try: sc.view_settings.view_transform = 'AgX'
    except TypeError: sc.view_settings.view_transform = 'Filmic'
    sc.view_settings.exposure = exposure
    return so
def cameras(route_path, parent, zfun=lambda x, y: 0.0):
    """route JSON shots -> camera objects (no roll: to_track_quat('-Z','Y')). pos z is EYE height above local ground
    unless 'abs_z' is set; shots may carry 'ortho_ft' (top-down insert) and 'fstop'/'focus_ft'."""
    C = coll("CAMERAS", parent); out = []
    route = json.load(open(route_path))
    for shot in route["shots"]:
        for key in [k for k in ("start", "end", "tilt") if k in shot]:
            p = shot[key]; cd = bpy.data.cameras.new(f"{shot['id']}_{key}")
            cd.lens = shot["lens_mm"]; cd.sensor_width = 36.0; cd.clip_start = 0.02; cd.clip_end = 4000
            if "ortho_ft" in shot: cd.type = 'ORTHO'; cd.ortho_scale = ft(shot["ortho_ft"])
            ob = bpy.data.objects.new(f"{shot['id']}_{key}", cd); C.objects.link(ob)
            x, y, z = p["pos_ft"]; zg = 0.0 if p.get("abs_z") else zfun(x, y)
            ob.location = (ft(x), ft(y), ft(z + zg))
            lx, ly, lz = p["look_ft"]; lzg = 0.0 if p.get("abs_z") else zfun(lx, ly)
            d = Vector((ft(lx), ft(ly), ft(lz + lzg))) - ob.location
            ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
            ob["shot"] = shot["id"]; ob["eye_ft"] = z; ob["ground_ft"] = zg; ob["key"] = key
            if "fstop" in shot:
                cd.dof.use_dof = True; cd.dof.aperture_fstop = shot["fstop"]; cd.dof.focus_distance = ft(p.get("focus_ft", d.length / FT))
            out.append(ob)
    return out

def muse_collection(path, name, keep, credit, offset=(0, 0, 0)):
    """append a Muse kit read-only (never saved back) into a hidden collection for instancing"""
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if keep(n)]
    C = bpy.data.collections.new(name); C.instance_offset = offset; C["credit"] = credit
    for o in dst.objects:
        if o and o.type == 'MESH': C.objects.link(o)
    return C
def instance(name, C, parent, loc_ft, rz=0.0, scale=1.0, **props):
    e = bpy.data.objects.new(name, None); e.instance_type = 'COLLECTION'; e.instance_collection = C
    e.location = [ft(v) for v in loc_ft]; e.rotation_euler = (0, 0, rz); e.scale = (scale,) * 3; parent.objects.link(e)
    for k, v in props.items(): e[k] = v
    return e
MUSE_ROOT = "/workspace/models-main-ro/models"
