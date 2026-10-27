"""grokkit: small shared build kit for Grok Bot's Crystal Palace detail/offsite sets (copied per folder; no cross-folder imports).
Units: metres in Blender, geometry written in feet. Materials, a bmesh Kit (box/bar/cyl/wheel/lathe/poly), figures
(via figures.py), route cameras, sky/sun world, Cycles settings, save."""
import bpy, bmesh, math, os, json, random, importlib.util
from mathutils import Vector
FT = 0.3048
def ft(f): return f * FT
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("figures", os.path.join(HERE, "figures.py")); FG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(FG)
PFX = "GK_"
def reset(prefix):
    global PFX; PFX = prefix
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    return bpy.context.scene
def coll(n, parent=None):
    c = bpy.data.collections.new(n); (parent or bpy.context.scene.collection).children.link(c); return c
def mat(n, c, r=0.7, m=0.0, emit=None, alpha=None):
    M = bpy.data.materials.new(PFX + n); M.use_nodes = True; b = M.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m
    if emit: b.inputs["Emission Color"].default_value = (*emit[0], 1); b.inputs["Emission Strength"].default_value = emit[1]
    if alpha is not None: b.inputs["Alpha"].default_value = alpha
    M.diffuse_color = (*c, 1); return M
def mat_glass(n, tint, rough=0.05):
    M = bpy.data.materials.new(PFX + n); M.use_nodes = True; b = M.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*tint, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.5
    M.diffuse_color = (*tint, 0.4); return M
def mat_thin_glass(n, tint=(0.80, 0.86, 0.84), mix=0.10):
    """roof glazing: transparent with a little diffuse (no refraction; reads as thin sheet glass)"""
    M = bpy.data.materials.new(PFX + n); M.use_nodes = True; nt = M.node_tree; nn = nt.nodes; l = nt.links
    o = nn["Material Output"]; [nn.remove(x) for x in list(nn) if x != o]
    tr = nn.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (*tint, 1)
    gl = nn.new("ShaderNodeBsdfGlossy"); gl.inputs[1].default_value = 0.08
    df = nn.new("ShaderNodeBsdfDiffuse"); df.inputs[0].default_value = (*tint, 1)
    m1 = nn.new("ShaderNodeMixShader"); m1.inputs[0].default_value = mix; l.new(tr.outputs[0], m1.inputs[1]); l.new(df.outputs[0], m1.inputs[2])
    fr = nn.new("ShaderNodeFresnel"); fr.inputs[0].default_value = 1.5
    m2 = nn.new("ShaderNodeMixShader"); l.new(fr.outputs[0], m2.inputs[0]); l.new(m1.outputs[0], m2.inputs[1]); l.new(gl.outputs[0], m2.inputs[2])
    l.new(m2.outputs[0], o.inputs[0]); M.diffuse_color = (*tint, 0.3); return M
def mat_image(n, path, rough=0.8):
    M = bpy.data.materials.new(PFX + n); M.use_nodes = True; nt = M.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(path); t.image.pack()
    nt.links.new(t.outputs[0], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough; return M
class Kit:
    def __init__(s, mats): s.bm = bmesh.new(); s.mats = mats; s.uv = s.bm.loops.layers.uv.new("UVMap")
    def _t(s, i, n0):
        s.bm.faces.ensure_lookup_table()
        for k in range(n0, len(s.bm.faces)): s.bm.faces[k].material_index = i
    def box(s, i, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); vs = [s.bm.verts.new((ft(a), ft(b), ft(c))) for (a, b, c) in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[k] for k in f])
        s._t(i, n0)
    def quad(s, i, pts, uvs=((0, 0), (1, 0), (1, 1), (0, 1))):
        n0 = len(s.bm.faces); f = s.bm.faces.new([s.bm.verts.new(tuple(ft(v) for v in p)) for p in pts])
        for lp, uv in zip(f.loops, uvs): lp[s.uv].uv = uv
        s._t(i, n0); return f
    def poly(s, i, pts):
        n0 = len(s.bm.faces); s.bm.faces.new([s.bm.verts.new(tuple(ft(v) for v in p)) for p in pts]); s._t(i, n0)
    def bar(s, i, a, b, w, t=None):
        t = t or w; A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.bm.verts.new(p + sd * (ii * ft(w) / 2) + u * (jj * ft(t) / 2)) for p in (A, B) for (ii, jj) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[k] for k in f])
        s._t(i, n0)
    def cyl(s, i, a, b, r, seg=16, cap=True, r2=None):
        A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); u = d.cross(up).normalized(); w = u.cross(d).normalized()
        n0 = len(s.bm.faces); r2 = r if r2 is None else r2
        ra = [s.bm.verts.new(A + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * ft(r)) for k in range(seg)]
        rb = [s.bm.verts.new(B + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * ft(r2)) for k in range(seg)]
        for k in range(seg): s.bm.faces.new([ra[k], ra[(k + 1) % seg], rb[(k + 1) % seg], rb[k]])
        if cap: s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb)
        s._t(i, n0)
    def lathe(s, i, c, prof, seg=24):
        """surface of revolution about the vertical through c=(x,y); prof = [(r, z)] in feet"""
        n0 = len(s.bm.faces); rings = []
        for (r, z) in prof:
            rings.append([s.bm.verts.new((ft(c[0] + r * math.cos(2 * math.pi * k / seg)), ft(c[1] + r * math.sin(2 * math.pi * k / seg)), ft(z))) for k in range(seg)])
        for ra, rb in zip(rings, rings[1:]):
            for k in range(seg): s.bm.faces.new([ra[k], ra[(k + 1) % seg], rb[(k + 1) % seg], rb[k]])
        s._t(i, n0)
    def wheel(s, i, c, axis, r, w=0.5, rim=0.3, spokes=8):
        ax = Vector((1, 0, 0)) if axis == "x" else Vector((0, 1, 0)); C_ = Vector(c); u = Vector((0, 0, 1)); v = ax.cross(u)
        n = 28; pts = [C_ + (u * math.cos(2 * math.pi * k / n) + v * math.sin(2 * math.pi * k / n)) * (r - rim / 2) for k in range(n + 1)]
        for p, q in zip(pts, pts[1:]): s.bar(i, tuple(p), tuple(q), w, rim)
        for k in range(spokes):
            a = 2 * math.pi * k / spokes; s.bar(i, tuple(C_), tuple(C_ + (u * math.cos(a) + v * math.sin(a)) * (r - rim)), rim * 0.55)
        s.cyl(i, tuple(C_ - ax * w), tuple(C_ + ax * w), r * 0.14, 12)
    def done(s, name, coll_, x=0, y=0, z=0, rz=0, smooth=False, **props):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in s.mats: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(name, me); ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = (0, 0, rz); coll_.objects.link(ob)
        for k, v in props.items(): ob[k] = v
        return ob
# ---- figures ----
_pm = {}
def pm(kind, mats, style, key):
    if key not in _pm: _pm[key] = FG.person_mesh("P_" + key, kind, mats, style=style)
    return _pm[key]
def heading(dx, dy): return math.atan2(dy, dx) + math.pi / 2
def person(coll_, name, me, x, y, z, rz, R=None, **pr):
    ob = bpy.data.objects.new(name, me); ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = (0, 0, rz)
    kk = (R or random).uniform(0.95, 1.04); ob.scale = (kk, kk, kk); coll_.objects.link(ob); ob["part_kind"] = "figure"; ob["person"] = 1
    for a, b in pr.items(): ob[a] = b
    return ob
# ---- text labels (3D text, for cutaways) ----
def label(coll_, name, text, x, y, z, size_ft=1.0, rot=(math.pi / 2, 0, 0), m=None, align='LEFT'):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = text; cu.size = ft(size_ft); cu.align_x = align; cu.extrude = 0.004
    ob = bpy.data.objects.new(name, cu); ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = rot; coll_.objects.link(ob)
    if m: cu.materials.append(m)
    ob["part_kind"] = "label"; return ob
# ---- cameras from route, world, render ----
def cameras(route_path, coll_, units="ft"):
    route = json.load(open(route_path)); sc = bpy.context.scene; made = []
    k = FT if units == "ft" else 1.0
    for shot in route["shots"]:
        for key in ("start", "end"):
            if key not in shot: continue
            p = Vector([v * k for v in shot[key]["pos_ft"]]) + Vector(route.get("origin_m", (0, 0, 0)))
            q = Vector([v * k for v in shot[key]["look_ft"]]) + Vector(route.get("origin_m", (0, 0, 0)))
            cd = bpy.data.cameras.new(f"{shot['id']}_{key}"); cd.lens = shot["lens_mm"]; cd.sensor_width = 36; cd.clip_start = 0.05; cd.clip_end = 5000
            if shot.get("ortho_m"): cd.type = 'ORTHO'; cd.ortho_scale = shot["ortho_m"]
            co = bpy.data.objects.new(f"{shot['id']}_{key}", cd); co.location = p
            co.rotation_euler = (q - p).to_track_quat('-Z', 'Y').to_euler(); coll_.objects.link(co); made.append(co)
            if shot.get("res"): co["res"] = shot["res"]
    sc.camera = made[0]; return route
def world_sky(elev=30, rot=200, strength=0.3, sun_energy=3.0, sun_rot=(60, 0, 30), sun_col=(1.0, 0.94, 0.86), haze=None):
    sc = bpy.context.scene; w = bpy.data.worlds.new(PFX + "World"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; sky = w.node_tree.nodes.new("ShaderNodeTexSky")
    try: sky.sky_type = 'NISHITA'
    except TypeError: pass
    try: sky.sun_elevation = math.radians(elev); sky.sun_rotation = math.radians(rot)
    except AttributeError: pass
    if haze is not None:
        try: sky.air_density = haze[0]; sky.dust_density = haze[1]
        except AttributeError: pass
    w.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = strength
    sun = None
    if sun_energy:
        L = bpy.data.lights.new(PFX + "Sun", 'SUN'); L.energy = sun_energy; L.angle = math.radians(1.5); L.color = sun_col
        sun = bpy.data.objects.new(PFX + "Sun", L); sc.collection.objects.link(sun); sun.rotation_euler = tuple(math.radians(a) for a in sun_rot)
    return sun
def point(name, loc_ft, energy, col=(1, 0.9, 0.8), size=0.3, kind='POINT'):
    L = bpy.data.lights.new(name, kind); L.energy = energy; L.color = col
    if kind == 'AREA': L.size = size
    else: L.shadow_soft_size = size
    o = bpy.data.objects.new(name, L); o.location = tuple(ft(v) for v in loc_ft); bpy.context.scene.collection.objects.link(o); return o
def render_settings(exposure=0.0, look='AgX - Medium High Contrast', samples=64):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6; sc.cycles.transparent_max_bounces = 24
    sc.render.resolution_x = 1280; sc.render.resolution_y = 720
    try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = look
    except TypeError: pass
    sc.view_settings.exposure = exposure
def save(out, info, setname, seed):
    sc = bpy.context.scene; sc["grok_build"] = json.dumps({"set": setname, "seed": seed, "info": info})
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out), compress=True); print("SAVED", out, info)
