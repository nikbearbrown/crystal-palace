# Shared helpers for Scans batch-9 vignette builds (self-contained copy per package).
# v2: seated-figure torso/neck gap fixed; materials support alpha; figures and
# chairs are facing-aware so backs/aprons/chair-backs land on the correct side.
import bpy, math, os
from mathutils import Vector

def srgb(c):
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)

_MATS = {}
def mat(name, rgb, rough=0.85, metallic=0.0, alpha=None):
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    lin = srgb(rgb)
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if alpha is not None:
        bsdf.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    _MATS[name] = m
    return m

def _finish(ob, material, name=None):
    if name: ob.name = name
    if material: ob.data.materials.append(material)
    return ob

def box(name, loc, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(ob, material, name)

def cyl(name, loc, r_top, r_bot, h, material, verts=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=h, location=loc, rotation=rot)
    return _finish(bpy.context.active_object, material, name)

def sphere(name, loc, scale, material, seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc)
    ob = bpy.context.active_object
    ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return _finish(ob, material, name)

def torus(name, loc, R, r, material, rot=(0, 0, 0), major=28, minor=10):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=major,
                                     minor_segments=minor, location=loc, rotation=rot)
    return _finish(bpy.context.active_object, material, name)

def tri_prism(name, p1, p2, p3, thick, material):
    verts = [(p1[0], p1[1], p1[2]), (p2[0], p2[1], p2[2]), (p3[0], p3[1], p3[2]),
             (p1[0], p1[1] + thick, p1[2]), (p2[0], p2[1] + thick, p2[2]), (p3[0], p3[1] + thick, p3[2])]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if material: me.materials.append(material)
    return ob

SKIN = (0.80, 0.62, 0.48)

def head(x, y, z_top, r, skin_rgb=SKIN):
    return sphere("head", (x, y, z_top - r), (r, r, r * 1.12), mat("skin", skin_rgb, 0.7))

def hat_top(x, y, z, r_head, color=(0.10, 0.10, 0.11)):
    m = mat("hatdark" + str(color), color, 0.6)
    cyl("tophat_brim", (x, y, z), r_head * 1.55, r_head * 1.55, 0.02, m, 20)
    return cyl("tophat_crown", (x, y, z + r_head * 1.05), r_head * 0.92, r_head * 1.0, r_head * 2.0, m, 20)

def hat_bonnet(x, y, z, r_head, color, fdir=-1):
    m = mat("bonnet" + str(color), color, 0.8)
    sphere("bonnet", (x, y - fdir * r_head * 0.25, z + r_head * 0.15),
           (r_head * 1.25, r_head * 1.25, r_head * 1.25), m)
    return torus("bonnet_brim", (x, y + fdir * r_head * 0.30, z), r_head * 1.05, r_head * 0.22, m,
                 rot=(math.pi / 2, 0, 0))

def hat_cap(x, y, z, r_head, color=(0.25, 0.22, 0.20), fdir=-1):
    m = mat("cap" + str(color), color, 0.85)
    sphere("cap", (x, y, z + r_head * 0.45), (r_head * 1.15, r_head * 1.15, r_head * 0.62), m)
    return box("cap_peak", (x, y + fdir * r_head * 1.25, z + r_head * 0.28),
               (r_head * 1.3, r_head * 1.0, 0.015), m)

def hat_shako(x, y, z, r_head, color=(0.12, 0.12, 0.14), fdir=-1):
    m = mat("shako" + str(color), color, 0.6)
    cyl("shako", (x, y, z + r_head * 0.95), r_head * 1.12, r_head * 0.98, r_head * 1.7, m, 20)
    return box("shako_peak", (x, y + fdir * r_head * 1.2, z + r_head * 0.35),
               (r_head * 1.25, r_head * 0.95, 0.015), mat("shakopeak", (0.05, 0.05, 0.05), 0.4))

def hat_conical(x, y, z, r_head, color=(0.76, 0.64, 0.40)):
    m = mat("strawhat" + str(color), color, 0.9)
    return cyl("conical_hat", (x, y, z + r_head * 0.75), 0.015, r_head * 2.5, r_head * 1.1, m, 24)

def hat_flatcap(x, y, z, r_head, color=(0.30, 0.28, 0.26)):
    m = mat("flatcap" + str(color), color, 0.85)
    return cyl("flatcap", (x, y, z + r_head * 0.55), r_head * 1.35, r_head * 1.45, r_head * 0.45, m, 18)

def arm(x, y, z_sh, length, angle_z, angle_x, material, r=0.045):
    ob = cyl("arm", (0, 0, 0), r * 0.75, r, length, material, 10)
    ob.rotation_euler = (angle_x, 0, angle_z)
    off = Vector((0, 0, -length / 2))
    off.rotate(ob.rotation_euler)
    ob.location = (x + off.x, y + off.y, z_sh + off.z)
    return ob

def person(x, y, H=1.7, dress="man", coat=(0.23, 0.20, 0.19), hat="top",
           arm_l=None, arm_r=None, skin_rgb=SKIN, name_p="fig", fdir=-1):
    """Stylised dignified figure. fdir=-1 faces -Y (toward a camera at -Y);
    fdir=+1 faces +Y (back to that camera). Body parts are built ABOVE hip
    height and the head overlaps the shoulders -- no floating heads."""
    g = bpy.data.objects.new(name_p, None)
    bpy.context.collection.objects.link(g)
    def P(ob):
        if ob is not None: ob.parent = g
        return ob
    r_head = 0.105 * (H / 1.7)
    cm = mat("coat" + name_p + str(coat), coat, 0.85)
    if dress in ("woman", "girl"):
        P(cyl("skirt", (x, y, H * 0.30), 0.135 * H / 1.7, 0.30 * H / 1.7, H * 0.60, cm, 20))
        P(cyl("bodice", (x, y, H * 0.72), 0.105 * H / 1.7, 0.135 * H / 1.7, H * 0.26, cm, 16))
        if dress == "girl":
            am = mat("apron" + name_p, (0.92, 0.90, 0.86), 0.9)
            P(box("apron", (x, y + fdir * 0.155 * H / 1.7, H * 0.33), (0.26 * H / 1.7, 0.02, H * 0.44), am))
    elif dress == "robe":
        P(cyl("robe", (x, y, H * 0.44), 0.125 * H / 1.7, 0.235 * H / 1.7, H * 0.88, cm, 20))
        P(sphere("shoulders", (x, y, H * 0.86), (0.16 * H / 1.7, 0.11 * H / 1.7, 0.09 * H / 1.7), cm))
    else:
        P(cyl("coat", (x, y, H * 0.45), 0.115 * H / 1.7, 0.175 * H / 1.7, H * 0.90, cm, 20))
        P(sphere("shoulders", (x, y, H * 0.86), (0.165 * H / 1.7, 0.115 * H / 1.7, 0.095 * H / 1.7), cm))
    P(head(x, y, H, r_head, skin_rgb))
    hz = H - r_head * 0.35
    if hat == "top": P(hat_top(x, y, hz, r_head))
    elif hat == "bonnet": P(hat_bonnet(x, y, hz, r_head, (0.45, 0.38, 0.33) if dress != "girl" else (0.62, 0.55, 0.48), fdir))
    elif hat == "cap": P(hat_cap(x, y, hz, r_head, fdir=fdir))
    elif hat == "shako": P(hat_shako(x, y, hz, r_head, fdir=fdir))
    elif hat == "conical": P(hat_conical(x, y, hz, r_head))
    elif hat == "flatcap": P(hat_flatcap(x, y, hz, r_head))
    elif hat == "turban":
        P(torus("turban", (x, y, hz + r_head * 0.35), r_head * 0.95, r_head * 0.5,
                mat("turban" + name_p, (0.88, 0.85, 0.80), 0.9)))
    elif hat == "wrap":
        P(sphere("headwrap", (x, y, hz + r_head * 0.30), (r_head * 1.18, r_head * 1.18, r_head * 0.85),
                 mat("wrap" + name_p, (0.70, 0.62, 0.50), 0.9)))
    sx = 0.175 * H / 1.7
    if arm_l: P(arm(x - sx, y, H * 0.80, H * 0.36, arm_l[0], arm_l[1], cm))
    if arm_r: P(arm(x + sx, y, H * 0.80, H * 0.36, arm_r[0], arm_r[1], cm))
    return g

def chair(x, y, seat_h=0.46, color=(0.35, 0.24, 0.15), face=(0.0, -1.0)):
    """Chair whose back stands OPPOSITE the facing direction `face`."""
    m = mat("chairwood" + str(color) + str(face), color, 0.8)
    fx, fy = face
    th = math.atan2(fy, fx) + math.pi / 2  # local +Y maps to -face (behind sitter)
    box("chair_seat", (x, y, seat_h), (0.46, 0.44, 0.04), m, rot=(0, 0, th))
    bx, by = x - fx * 0.21, y - fy * 0.21
    box("chair_back", (bx, by, seat_h + 0.32), (0.46, 0.04, 0.62), m, rot=(0, 0, th))
    ct, st = math.cos(th), math.sin(th)
    for lx, ly in ((-0.19, -0.18), (0.19, -0.18), (-0.19, 0.18), (0.19, 0.18)):
        wx, wy = x + lx * ct - ly * st, y + lx * st + ly * ct
        box("chair_leg", (wx, wy, seat_h / 2), (0.045, 0.045, seat_h), m)
    return m

def seated_person(x, y, H=1.7, coat=(0.3, 0.28, 0.26), hat="cap", seat_h=0.46,
                  skin_rgb=SKIN, name_p="seat", face=(0.0, -1.0), dress="man"):
    """Seated figure facing `face` (unit XY). Seated top-of-head is ~72% of
    the seat-to-standing span above the seat (real sitting height); torso and
    shoulders overlap the head -- no floating heads."""
    cm = mat("seatcoat" + name_p + str(coat), coat, 0.85)
    fx, fy = face
    r_head = 0.105 * (H / 1.7)
    T = seat_h + (H - seat_h) * 0.72  # seated top of head
    if dress == "woman":
        cyl("lap", (x + fx * 0.06, y + fy * 0.06, seat_h - 0.04), 0.21, 0.25, 0.24, cm, 16)
    else:
        cyl("lap", (x + fx * 0.06, y + fy * 0.06, seat_h - 0.04), 0.19, 0.23, 0.24, cm, 16)
    torso_h = (T - 2 * r_head - seat_h) + 0.14
    cyl("torso", (x, y, seat_h + torso_h / 2 - 0.04), 0.115 * H / 1.7, 0.15 * H / 1.7, torso_h, cm, 16)
    sphere("seat_shoulders", (x, y, T - 2 * r_head - 0.01), (0.16 * H / 1.7, 0.11 * H / 1.7, 0.10 * H / 1.7), cm)
    z_top = T
    head(x, y, z_top, r_head, skin_rgb)
    hz = z_top - r_head * 0.35
    if hat == "cap": hat_cap(x, y, hz, r_head, fdir=1 if fy < 0 else -1)
    elif hat == "top": hat_top(x, y, hz, r_head)
    elif hat == "bonnet": hat_bonnet(x, y, hz, r_head, (0.5, 0.42, 0.36), 1 if fy < 0 else -1)
    elif hat == "flatcap": hat_flatcap(x, y, hz, r_head)
    elif hat == "wrap":
        sphere("headwrap", (x, y, hz + r_head * 0.30), (r_head * 1.18, r_head * 1.18, r_head * 0.85),
               mat("wrap" + name_p, (0.70, 0.62, 0.50), 0.9))
    elif hat == "conical": hat_conical(x, y, hz, r_head)
    # arms resting toward the table (forward, slightly down, hugging the body)
    arm(x - 0.13 * H / 1.7, y, T - 2 * r_head - 0.06, 0.36 * (H / 1.7), 0.12, fy * 0.75, cm)
    arm(x + 0.13 * H / 1.7, y, T - 2 * r_head - 0.06, 0.36 * (H / 1.7), -0.12, fy * 0.75, cm)

def ground(w, d, color=(0.62, 0.60, 0.57), y_off=0.0):
    return box("ground", (0, y_off, -0.03), (w, d, 0.06), mat("groundmat" + str(color), color, 0.95))

def finalise(slug, cam_loc, cam_target, res=(960, 720), outdir=None):
    sc = bpy.context.scene
    sun_data = bpy.data.lights.new("sun", 'SUN'); sun_data.energy = 3.0
    sun = bpy.data.objects.new("sun", sun_data); bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(52), 0, math.radians(35))
    fill_data = bpy.data.lights.new("fill", 'AREA'); fill_data.energy = 350; fill_data.shape = 'DISK'; fill_data.size = 6
    fill = bpy.data.objects.new("fill", fill_data); bpy.context.collection.objects.link(fill)
    fill.location = (cam_loc[0] * 0.4, cam_loc[1] * 0.7, 5.5)
    fill.rotation_euler = (math.radians(70), 0, 0)
    world = bpy.data.worlds.new("W"); sc.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (*srgb((0.55, 0.55, 0.56)), 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.85
    cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam); cam.location = cam_loc
    d = Vector(cam_target) - Vector(cam_loc)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 48
    sc.cycles.use_denoising = True
    sc.cycles.device = 'CPU'
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.film_transparent = False
    outdir = outdir or os.path.dirname(os.path.abspath(__file__))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outdir, slug + ".blend"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(outdir, slug + ".glb"), export_format='GLB')
    sc.render.filepath = os.path.join(outdir, "preview.png")
    bpy.ops.render.render(write_still=True)
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    for ob in sc.objects:
        if ob.type == 'MESH':
            ev = ob.evaluated_get(dg); me = ev.to_mesh()
            tris += sum(len(p.vertices) - 2 for p in me.polygons)
            ev.to_mesh_clear()
    print("TRIS:", tris)
    return tris
