# Build script: scan-fig68-victoria-and-children (Muse version)
# Reference: fig-68_queen-victoria-and-children-john-callcott-horsley.png
# John Callcott Horsley, portrait group of Queen Victoria and her children (c.1865).
# Posed interior group: standing man with document at screen-left, table with
# globe at centre, Queen seated centre-right gesturing toward the globe,
# children grouped around, elder boy standing at screen-right.
# Conventions: metres, origin at base centre, camera looks from +Y so
# screen-left = world +X. Run: blender -b -P this_script.py
import bpy, math, os

# clear the default startup scene (cube/camera/light)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
from mathutils import Vector

PKG = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig68-victoria-and-children"

# ---------- helpers ----------
def srgb2lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

def mat(name, srgb, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*srgb2lin(srgb), 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

def _finish(ob, material=None):
    if material:
        ob.data.materials.append(material)
    return ob

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    ob.dimensions = dims
    return _finish(ob, material)

def cyl(name, loc, r_top, r_bot, depth, material=None, rot=(0, 0, 0), verts=20):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    return _finish(ob, material)

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    ob = bpy.context.active_object; ob.name = name
    ob.scale = scale
    return _finish(ob, material)

def limb(name, p1, p2, r1, r2, material):
    """Tapered cylinder between two points."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2; d = p2 - p1; L = d.length
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=r1, radius2=r2, depth=L, location=mid)
    ob = bpy.context.active_object; ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    ob.data.materials.append(material)
    return ob

# ---------- materials ----------
DARK   = mat("near_black_cloth", (0.05, 0.045, 0.05))
COAT   = mat("dark_coat", (0.07, 0.06, 0.07))
TROUS  = mat("trousers", (0.16, 0.15, 0.15))
SKIN   = mat("skin_plain", (0.78, 0.60, 0.48), 0.7)
PAPER  = mat("paper", (0.92, 0.90, 0.84), 0.95)
WOOD   = mat("dark_wood", (0.16, 0.09, 0.05), 0.6)
WOOD2  = mat("mid_wood", (0.30, 0.18, 0.10), 0.65)
WALL   = mat("wall_dark", (0.13, 0.11, 0.10), 0.95)
FLOOR  = mat("floor_wood", (0.23, 0.15, 0.09), 0.8)
DRAPE  = mat("drape_deep_red", (0.22, 0.05, 0.06), 0.95)
LACE   = mat("lace_white", (0.90, 0.88, 0.84), 0.9)
GLOBE_M = mat("globe_ocean", (0.35, 0.48, 0.55), 0.5)
LAND   = mat("globe_land", (0.62, 0.52, 0.33), 0.6)
DRESS1 = mat("girl_dress_light", (0.55, 0.58, 0.62), 0.9)
DRESS2 = mat("girl_dress_rose", (0.45, 0.30, 0.30), 0.9)
DRESS3 = mat("child_dress_cream", (0.72, 0.66, 0.55), 0.9)
HAIR   = mat("hair_brown", (0.20, 0.13, 0.08), 0.8)
HAIR2  = mat("hair_fair", (0.45, 0.33, 0.18), 0.8)
GILT   = mat("gilt", (0.55, 0.42, 0.18), 0.45, 0.6)

# ---------- figure builder (house style: tapered masses, plain heads) ----------
def figure(name, x, y, h, female=False, seated=False, coat=COAT, bottom=TROUS,
           hair=HAIR, arm_pose="down", facing=0.0):
    g = []
    hr = 0.068 * h                      # head radius
    if seated:
        # skirt/thigh mass on chair, torso upright
        g.append(cyl(name+"_skirt_mass", (x, y, 0.46), 0.16*h/1.6, 0.24*h/1.6, 0.42, coat))
        torso_base = 0.62
    elif female:
        g.append(cyl(name+"_skirt", (x, y, 0.26*h), 0.085*h, 0.20*h, 0.52*h, coat))
        torso_base = 0.52 * h
    else:
        leg_l = 0.47 * h
        for s in (-1, 1):
            g.append(cyl(name+"_leg", (x + s*0.055*h, y, leg_l/2), 0.038*h, 0.05*h, leg_l, bottom))
        torso_base = leg_l
    torso_h = 0.30 * h
    tz = torso_base + torso_h / 2
    g.append(cyl(name+"_torso", (x, y, tz), 0.105*h, 0.088*h, torso_h, coat))
    # shoulders / arms
    sh_y = torso_base + torso_h * 0.88
    for s, side in ((-1, "L"), (1, "R")):
        sh = (x + s*0.115*h, y, sh_y)
        r_arm = 0.030 * h
        if arm_pose == "point" and side == "R":
            # near-side arm extended toward +X (toward table/globe), thinner
            hand = (x + 0.40*h, y + 0.03*h, sh_y - 0.12*h)
            r_arm = 0.023 * h
        elif arm_pose == "hold" :
            hand = (x - s*0.02*h, y + 0.13*h, torso_base + 0.06*h)
        else:
            hand = (x + s*0.13*h, y + 0.01, torso_base + 0.05*h)
        g.append(limb(name+"_arm"+side, sh, hand, r_arm, r_arm + 0.006*h, coat))
        g.append(sphere(name+"_hand"+side, hand, 0.032*h, SKIN))
    head_z = torso_base + torso_h + hr * 0.95
    g.append(sphere(name+"_head", (x, y, head_z), hr, SKIN))
    g.append(sphere(name+"_hair", (x, y - 0.012*h, head_z + 0.018*h), hr*1.02, hair, scale=(1, 1, 0.82)))
    return g

# ---------- room ----------
box("floor", (0, 0.1, -0.03), (5.4, 3.0, 0.06), FLOOR)
box("back_wall", (0, -0.85, 1.35), (5.4, 0.12, 2.7), WALL)
# dark chimney-breast column at screen-left edge (seen in image left)
box("dark_column_L", (2.25, -0.78, 1.30), (0.55, 0.18, 2.6), mat("column_dark", (0.09, 0.08, 0.08)))
# deep-red drape panel at screen-right
box("drape_R", (-2.15, -0.80, 1.25), (0.7, 0.10, 2.5), DRAPE)
box("drape_valance", (-2.15, -0.80, 2.42), (0.74, 0.12, 0.28), DRAPE)

# ---------- furniture ----------
# central table
box("table_top", (0.45, -0.10, 0.76), (1.25, 0.62, 0.05), WOOD)
for sx in (-1, 1):
    for sy in (-1, 1):
        box("table_leg", (0.45 + sx*0.55, -0.10 + sy*0.24, 0.37), (0.06, 0.06, 0.74), WOOD)
# papers / the map-document spread on the table (blank sheets, no lettering)
box("table_paper1", (0.28, -0.02, 0.795), (0.55, 0.38, 0.012), PAPER, rot=(0, 0, 0.10))
box("table_paper2", (0.62, -0.22, 0.79), (0.42, 0.30, 0.010), PAPER, rot=(0, 0, -0.22))
# globe on stand (centre-left of table, as in image)
cyl("globe_stand", (0.78, -0.12, 0.83), 0.035, 0.075, 0.09, WOOD2)
sphere("globe", (0.78, -0.12, 1.06), 0.155, GLOBE_M)
sphere("globe_land_patch", (0.70, -0.035, 1.10), 0.10, LAND, scale=(0.55, 0.45, 0.8))
bpy.ops.mesh.primitive_torus_add(major_radius=0.165, minor_radius=0.008,
                                 location=(0.78, -0.12, 1.06), rotation=(0.35, 0.2, 0))
mer = bpy.context.active_object; mer.name = "globe_meridian"; mer.data.materials.append(GILT)

# queen's chair (high back, partly behind her)
box("chair_back", (-0.88, -0.42, 0.95), (0.62, 0.07, 1.15), WOOD)
box("chair_seat", (-0.88, -0.22, 0.47), (0.62, 0.45, 0.07), DRAPE)
for sx in (-1, 1):
    box("chair_leg", (-0.88 + sx*0.26, -0.10, 0.22), (0.05, 0.05, 0.44), WOOD)

# ---------- figures ----------
# standing man, screen-left, holding a document at his waist
figure("man", 1.62, -0.18, 1.76, coat=COAT, bottom=TROUS, arm_pose="hold")
box("held_document", (1.62, 0.06, 0.92), (0.34, 0.02, 0.44), PAPER, rot=(0.12, 0, 0.05))

# Queen seated centre-right, right arm (world +X side = her screen-left arm)
# extended toward the globe. In the image she gestures with the arm nearer
# the table; that is the +X arm of the figure.
figure("queen", -0.82, -0.18, 1.60, female=True, seated=True, coat=DARK, arm_pose="point")
# white lace collar + cuffs suggestion
bpy.ops.mesh.primitive_torus_add(major_radius=0.075, minor_radius=0.02,
                                 location=(-0.82, -0.15, 1.13), rotation=(math.radians(78), 0, 0))
col = bpy.context.active_object; col.name = "queen_collar"; col.data.materials.append(LACE)
# small crown / coronet glint (she wears a small crown in the painting)
cyl("queen_coronet", (-0.82, -0.19, 1.335), 0.055, 0.062, 0.035, GILT, verts=12)

# elder boy standing screen-right
figure("boy_elder", -1.62, -0.25, 1.38, coat=COAT, bottom=TROUS, hair=HAIR2)
# older girl standing behind the table (centre)
figure("girl_elder", 0.02, -0.42, 1.32, female=True, coat=DRESS3, hair=HAIR2)
# girl foreground centre, light dress, dark collar band
figure("girl_front", 0.12, 0.38, 1.12, female=True, coat=DRESS1, hair=HAIR2)
bpy.ops.mesh.primitive_torus_add(major_radius=0.052, minor_radius=0.016,
                                 location=(0.12, 0.40, 0.94), rotation=(math.radians(80), 0, 0))
cb = bpy.context.active_object; cb.name = "girl_collar"; cb.data.materials.append(DARK)
# child beside the queen (front-right group)
figure("child_r", -1.18, 0.28, 1.00, female=True, coat=DRESS2)
# small child centre-front
figure("child_small", -0.35, 0.48, 0.82, female=True, coat=DRESS3, hair=HAIR2)
# boy at left foreground near the man (holds a book-like block, blank)
figure("boy_young", 1.15, 0.30, 1.02, coat=mat("boy_jacket", (0.13, 0.12, 0.14)), bottom=TROUS)
box("boy_book_blank", (1.15, 0.44, 0.52), (0.16, 0.035, 0.22), mat("book_cover", (0.25, 0.10, 0.08)), rot=(0.3, 0, 0))

# ---------- scene, lights, camera ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 800
sc.render.film_transparent = False
w = sc.world; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb2lin((0.16, 0.15, 0.14)), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.55

def area(name, loc, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energy; d.shape = 'DISK'; d.size = size
    d.color = color
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 0) if False else (loc)).rotation_difference(Vector((0, 0, 1))) if False else o.rotation_quaternion
    # point light straight down-ish toward group centre
    direction = Vector((0, 0, 0.8)) - Vector(loc)
    o.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(direction.normalized())
    return o

area("key", (2.6, 3.2, 3.4), 900, 2.2, (1.0, 0.93, 0.82))
area("fill", (-2.8, 3.4, 1.8), 260, 2.6, (0.9, 0.93, 1.0))

cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 46; cam_d.clip_end = 100
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
cam.location = (0.35, 4.6, 1.75)
cam.rotation_mode = 'QUATERNION'
cam.rotation_quaternion = (Vector((0, 0, 0.85)) - cam.location).to_track_quat('-Z', 'Y')
sc.camera = cam

# ---------- finalise ----------
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
