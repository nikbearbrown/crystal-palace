# Build script: scan-fig72-brompton-boilers (Muse version)
# Reference: fig-72_brompton-boilers-south-kensington-exhibition-1862.png
# ILN coloured view (24 May 1862) captioned "The 'Brompton Boilers'".
# NOTE: despite the nickname, the view shows the 1862 International
# Exhibition building in South Kensington: a long BRICK arcaded frontage
# with two glazed domes (the larger at screen-right), flags along the roof,
# and horse-drawn traffic on the open ground in front. The image governs:
# this model is that building (excerpt), NOT corrugated sheds.
# Conventions: metres, origin at base centre, camera from +Y (screen-left=+X,
# so the big dome sits at world -X).
import bpy, math, os

# clear the default startup scene (cube/camera/light)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
from mathutils import Vector

PKG = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig72-brompton-boilers"

def srgb2lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

def mat(name, srgb, rough=0.9, metal=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb2lin(srgb), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.dimensions = dims
    if material: ob.data.materials.append(material)
    return ob

def cyl(name, loc, r_top, r_bot, depth, material=None, rot=(0, 0, 0), verts=18):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    if material: ob.data.materials.append(material)
    return ob

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    ob = bpy.context.active_object; ob.name = name; ob.scale = scale
    if material: ob.data.materials.append(material)
    return ob

BRICK  = mat("brick_warm", (0.62, 0.42, 0.26), 0.95)
BRICK_D = mat("brick_shade", (0.50, 0.33, 0.20), 0.95)
STONE  = mat("stone_trim", (0.72, 0.62, 0.48), 0.9)
GLASS_D = mat("window_dark", (0.13, 0.16, 0.19), 0.35, 0.1)
DOME_GL = mat("dome_glass", (0.62, 0.68, 0.70), 0.25, 0.1, alpha=0.55)
DOME_RIB = mat("dome_rib", (0.30, 0.30, 0.32), 0.6, 0.4)
SLATE  = mat("slate_roof", (0.25, 0.26, 0.30), 0.9)
GROUND = mat("plaza_earth", (0.58, 0.45, 0.30), 1.0)
FLAG   = mat("flag_red", (0.55, 0.12, 0.10), 0.9)
DARK   = mat("dark_detail", (0.08, 0.07, 0.07), 0.9)
HORSE1 = mat("horse_brown", (0.25, 0.16, 0.10), 0.85)
HORSE2 = mat("horse_black", (0.10, 0.09, 0.09), 0.85)
CARR   = mat("carriage_green", (0.10, 0.16, 0.12), 0.6)
CARR2  = mat("carriage_maroon", (0.25, 0.08, 0.08), 0.6)
FIG1   = mat("fig_coat", (0.12, 0.11, 0.13), 0.9)
FIG2   = mat("fig_dress", (0.35, 0.22, 0.20), 0.9)
FIG3   = mat("fig_redcoat", (0.45, 0.10, 0.08), 0.9)
SKIN   = mat("skin", (0.78, 0.60, 0.48), 0.7)

box("plaza", (0, 8, -0.05), (140, 64, 0.1), GROUND)

FRONT_Y = 0.0        # front wall plane
WALL_H = 11.0

def arcade_run(x0, x1, name):
    """Brick wall with repeated round-arched window bays between x0..x1."""
    L = x1 - x0; cx = (x0 + x1) / 2
    box(name + "_wall", (cx, FRONT_Y - 1.2, WALL_H / 2), (L, 2.4, WALL_H), BRICK)
    box(name + "_cornice", (cx, FRONT_Y - 1.15, WALL_H + 0.35), (L + 0.3, 2.7, 0.7), STONE)
    box(name + "_plinth", (cx, FRONT_Y - 1.1, 0.5), (L + 0.2, 2.6, 1.0), BRICK_D)
    bay = 3.8
    n = int(L // bay)
    for i in range(n):
        bx = x0 + bay * (i + 0.5)
        # pier
        box(name + "_pier", (bx - bay / 2 + 0.3, FRONT_Y + 0.06, WALL_H / 2), (0.6, 0.14, WALL_H), BRICK_D)
        # arched window: dark rectangle + half-round head, pale surround
        box(name + "_win", (bx, FRONT_Y + 0.05, 4.6), (1.7, 0.10, 7.2), GLASS_D)
        cyl(name + "_winhead", (bx, FRONT_Y + 0.05, 8.2), 0.85, 0.85, 0.10, GLASS_D,
            rot=(math.radians(90), 0, 0), verts=20)
        cyl(name + "_archring", (bx, FRONT_Y + 0.02, 8.2), 1.02, 1.02, 0.06, STONE,
            rot=(math.radians(90), 0, 0), verts=20)
    # low pitched slate roof behind the parapet
    box(name + "_roof", (cx, FRONT_Y - 3.4, WALL_H + 1.1), (L, 5.2, 0.18), SLATE,
        rot=(math.radians(16), 0, 0))

def pavilion(cx, w, h, name, door=True):
    box(name + "_block", (cx, FRONT_Y - 1.5, h / 2), (w, 3.0, h), BRICK)
    box(name + "_cornice", (cx, FRONT_Y - 1.45, h + 0.3), (w + 0.4, 3.3, 0.6), STONE)
    # gable / pediment hint
    box(name + "_gable", (cx, FRONT_Y - 1.5, h + 1.15), (w * 0.55, 2.6, 1.7), BRICK)
    # oculus
    cyl(name + "_oculus", (cx, FRONT_Y + 0.06, h - 0.6), 0.55, 0.55, 0.1, GLASS_D,
        rot=(math.radians(90), 0, 0), verts=20)
    if door:
        box(name + "_door", (cx, FRONT_Y + 0.05, 3.1), (2.6, 0.12, 6.2), GLASS_D)
        cyl(name + "_doorhead", (cx, FRONT_Y + 0.05, 6.2), 1.3, 1.3, 0.12, GLASS_D,
            rot=(math.radians(90), 0, 0), verts=20)
        cyl(name + "_doorring", (cx, FRONT_Y + 0.02, 6.2), 1.5, 1.5, 0.06, STONE,
            rot=(math.radians(90), 0, 0), verts=20)
    for sx in (-1, 1):  # flanking arched windows
        wx = cx + sx * w * 0.32
        box(name + "_win", (wx, FRONT_Y + 0.05, 4.4), (1.5, 0.10, 6.8), GLASS_D)
        cyl(name + "_winhead", (wx, FRONT_Y + 0.05, 7.8), 0.75, 0.75, 0.10, GLASS_D,
            rot=(math.radians(90), 0, 0), verts=20)

def dome(cx, R, drum_h, name):
    # rotunda drum set back behind the front block; glass clamped to a cap
    z0 = drum_h
    cy = FRONT_Y - 7.2
    drum = cyl(name + "_drum", (cx, cy, z0 - 2.3), R * 1.0, R * 1.02, 5.0, BRICK_D, verts=28)
    drum.scale = (1, 0.82, 1)
    glass = sphere(name + "_glass", (cx, cy, z0), R, DOME_GL, scale=(1, 0.82, 1))
    for v in glass.data.vertices:
        if v.co.z < -0.3:
            v.co.z = -0.3
    # cut the lower half visually by a stone ring at springing
    cyl(name + "_ring", (cx, cy, z0 + 0.15), R * 1.01, R * 1.03, 0.35, STONE, verts=28)
    for i in range(9):  # meridian ribs (half-torus arcs)
        a = math.pi * i / 9
        bpy.ops.mesh.primitive_torus_add(major_radius=R * 0.99, minor_radius=0.07,
                                         major_segments=24, minor_segments=6,
                                         location=(cx, cy, z0))
        rib = bpy.context.active_object; rib.name = name + "_rib"
        rib.rotation_euler = (0, a, 0)
        rib.scale = (1, 0.82, 1)
        rib.data.materials.append(DOME_RIB)
    for f in (0.38, 0.66, 0.88):  # latitude rings
        bpy.ops.mesh.primitive_torus_add(major_radius=R * math.sin(math.acos(f)) * 0.99,
                                         minor_radius=0.06, major_segments=28, minor_segments=6,
                                         location=(cx, cy, z0 + R * f))
        ring = bpy.context.active_object; ring.name = name + "_lat"
        ring.scale = (1, 0.82, 1)
        ring.data.materials.append(DOME_RIB)
    # finial + flag
    cyl(name + "_finial", (cx, cy, z0 + R + 0.7), 0.05, 0.12, 1.6, DOME_RIB)
    sphere(name + "_finial_ball", (cx, cy, z0 + R + 0.55), 0.22, STONE)

def flag(x, y, z, s=1.0):
    cyl("flag_pole", (x, y, z + 1.1 * s), 0.03 * s, 0.03 * s, 2.2 * s, DARK)
    box("flag_cloth", (x - 0.55 * s, y, z + 1.85 * s), (1.1 * s, 0.03, 0.62 * s), FLAG,
        rot=(0, 0, 0.06))

# ---------- compose the excerpt ----------
# big dome pavilion at world -X (screen-right), arcade runs to +X (screen-left)
pavilion(-17.5, 17.5, 13.5, "pavilion_big")
dome(-17.5, 8.2, 14.3, "dome_big")
pavilion(-6.5, 6.5, 12.2, "pavilion_mid", door=True)
arcade_run(-3.0, 17.0, "arcade_east")
pavilion(19.5, 6.0, 12.0, "pavilion_west", door=True)
arcade_run(22.5, 33.0, "arcade_far")
# far small dome at the left end of the excerpt (partly cropped by frame)
pavilion(35.5, 14.0, 12.6, "pavilion_far")
dome(35.5, 6.4, 13.4, "dome_small")
# roof flags as in the print (plain red)
for fx in (-6.5, 0.5, 8.0, 19.5, 26.0, 31.0):
    flag(fx, FRONT_Y - 1.2, WALL_H + 0.7)
flag(-17.5, FRONT_Y - 7.2, 14.3 + 8.2 + 1.2, s=1.15)

# ---------- foreground traffic: horses, carriages, figures ----------
def horse(name, x, y, rot, material):
    g = bpy.data.objects
    body = sphere(name + "_body", (x, y, 1.45), 0.64, material, scale=(1.55, 0.62, 0.78))
    neck = box(name + "_neck", (x + 0.85, y, 1.85), (0.55, 0.30, 0.75), material, rot=(0, 0, 0))
    neck.rotation_euler = (0, math.radians(-40), 0)
    head = box(name + "_head", (x + 1.34, y, 2.20), (0.54, 0.22, 0.30), material)
    head.rotation_euler = (0, math.radians(28), 0)
    for lx, ly in ((0.55, 0.22), (0.55, -0.22), (-0.55, 0.22), (-0.55, -0.22)):
        cyl(name + "_leg", (x + lx, y + ly, 0.55), 0.06, 0.078, 1.1, material, verts=10)
    tail = cyl(name + "_tail", (x - 0.95, y, 1.55), 0.03, 0.09, 0.8, material,
               rot=(0, math.radians(24), 0), verts=8)
    grp = [body, neck, head, tail] + [o for o in g if o.name.startswith(name + "_leg")]
    for o in grp:
        o.rotation_euler = (o.rotation_euler[0], o.rotation_euler[1], o.rotation_euler[2])
    # rotate whole horse about its centre
    for o in grp:
        loc = Vector(o.location); rel = loc - Vector((x, y, 0))
        c, s = math.cos(rot), math.sin(rot)
        o.location = Vector((x + rel.x * c - rel.y * s, y + rel.x * s + rel.y * c, loc.z))
        o.rotation_euler = (o.rotation_euler[0], o.rotation_euler[1], o.rotation_euler[2] + rot)
    return grp

def carriage(name, x, y, rot, material, with_horse=True):
    obs = []
    obs.append(box(name + "_cabin", (x, y, 1.35), (1.7, 1.05, 1.05), material))
    obs.append(box(name + "_roof", (x, y, 1.95), (1.8, 1.15, 0.10), DARK))
    obs.append(box(name + "_driver_box", (x + 1.15, y, 1.30), (0.4, 0.9, 0.5), material))
    for wx, wy, wr in ((0.62, 0.58, 0.55), (0.62, -0.58, 0.55), (-0.62, 0.58, 0.38), (-0.62, -0.58, 0.38)):
        w = cyl(name + "_wheel", (x + wx, y + wy, wr), wr, wr, 0.07, DARK,
                rot=(math.radians(90), 0, 0), verts=18)
        obs.append(w)
    # driver figure
    obs.append(cyl(name + "_driver", (x + 1.15, y, 1.95), 0.13, 0.17, 0.55, FIG1))
    obs.append(sphere(name + "_driver_head", (x + 1.15, y, 2.32), 0.10, SKIN))
    if with_horse:
        obs += horse(name + "_horse", x + 2.6, y, 0.0, HORSE1)
        obs.append(box(name + "_shafts", (x + 1.8, y, 1.15), (1.1, 0.7, 0.06), DARK))
    for o in obs:
        loc = Vector(o.location); rel = loc - Vector((x, y, 0))
        c, s = math.cos(rot), math.sin(rot)
        o.location = Vector((x + rel.x * c - rel.y * s, y + rel.x * s + rel.y * c, loc.z))
        o.rotation_euler = (o.rotation_euler[0], o.rotation_euler[1], o.rotation_euler[2] + rot)
    return obs

def person(name, x, y, h, material, skirt=False):
    if skirt:
        cyl(name + "_skirt", (x, y, 0.26 * h), 0.085 * h, 0.20 * h, 0.52 * h, material)
        base = 0.52 * h
    else:
        cyl(name + "_legs", (x, y, 0.24 * h), 0.075 * h, 0.095 * h, 0.48 * h, FIG1)
        base = 0.48 * h
    cyl(name + "_torso", (x, y, base + 0.15 * h), 0.105 * h, 0.088 * h, 0.30 * h, material)
    sphere(name + "_head", (x, y, base + 0.30 * h + 0.075 * h), 0.068 * h, SKIN)
    cyl(name + "_hat", (x, y, base + 0.30 * h + 0.135 * h), 0.085 * h, 0.088 * h, 0.03 * h, DARK)

carriage("carr1", -8.0, 8.5, 0.12, CARR)
carriage("carr2", 6.5, 10.5, -0.08, CARR2)
carriage("carr3", 20.0, 7.5, 0.30, CARR, with_horse=True)
horse("rider_horse1", -14.5, 12.0, -0.15, HORSE2)
person("rider1", -14.5, 12.0, 1.72, FIG3)  # mounted figure sits high (stylised)
for o in bpy.data.objects:
    if o.name.startswith("rider1_"):
        o.location.z += 1.15
horse("rider_horse2", 13.0, 13.5, 0.2, HORSE1)
person("rider2", 13.0, 13.5, 1.72, FIG1)
for o in bpy.data.objects:
    if o.name.startswith("rider2_"):
        o.location.z += 1.15
# pedestrian groups
person("ped1", -3.5, 6.0, 1.70, FIG1)
person("ped2", -3.0, 6.2, 1.60, FIG2, skirt=True)
person("ped3", 11.5, 5.6, 1.72, FIG1)
person("ped4", 12.1, 5.8, 1.58, FIG2, skirt=True)
person("ped5", 25.5, 6.4, 1.70, FIG3)
person("ped6", -11.0, 5.4, 1.66, FIG1)

# ---------- scene / lights / camera ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 1100; sc.render.resolution_y = 620
w = sc.world; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb2lin((0.78, 0.74, 0.66)), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.9

d = bpy.data.lights.new("sun", 'SUN'); d.energy = 2.6; d.color = (1.0, 0.95, 0.86)
o = bpy.data.objects.new("sun", d); sc.collection.objects.link(o)
o.rotation_euler = (math.radians(48), math.radians(-12), math.radians(28))
d2 = bpy.data.lights.new("sky", 'SUN'); d2.energy = 0.5; d2.color = (0.9, 0.93, 1.0)
o2 = bpy.data.objects.new("sky", d2); sc.collection.objects.link(o2)
o2.rotation_euler = (math.radians(110), 0, math.radians(-60))

cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 30; cam_d.clip_end = 300
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
cam.location = (-4.0, 56.0, 10.0)
cam.rotation_mode = 'QUATERNION'
cam.rotation_quaternion = (Vector((5.0, 0, 6.0)) - cam.location).to_track_quat('-Z', 'Y')
sc.camera = cam

for ob in bpy.data.objects:
    if ob.type == 'MESH':
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        ob.select_set(False)

tris = 0
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        ob.data.calc_loop_triangles()
        tris += len(ob.data.loop_triangles)
print("TRIANGLES:", tris)

sc.render.filepath = os.path.join(PKG, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PKG, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PKG, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
