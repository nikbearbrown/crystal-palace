#!/usr/bin/env python3
"""Build the Egyptian Court colossi prop for the Crystal Palace film.

Pair of seated pharaoh statues of Abu Simbel type on a shared pedestal,
as photographed facing the nave of the Sydenham Crystal Palace
(reference: references/image-leads/uxqanywewcl.jpg in nikbearbrown/crystal-palace).

All dimensions in metres. Statue height 20.0 m above its plinth
(INFERRED from the photograph's pedestal-door ratio, corroborated by the
1856 General Guide Book, p.50, which states the gigantic figures in the
northern transept are the size of the sitting figures of the original
temple of Aboo Simbel). See NOTES.md in the model folder.

Run: blender -b --python build_colossi.py
Outputs (next to this script's parent folder):
  egyptian-court-colossi.blend, egyptian-court-colossi.glb,
  renders/front.png, renders/side.png, renders/three-quarter.png
"""
import bpy
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 0.45            # statue plinth slab thickness (statue local z offset)
PED_H = 5.9         # pedestal height
FIG_H = 20.0        # statue height above slab top

# ---------------------------------------------------------------- materials
def make_mat(name, color, rough=0.92):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

STONE = STONE_LIGHT = STONE_BAND = DARK = GREY = None

def init_materials():
    global STONE, STONE_LIGHT, STONE_BAND, DARK, GREY
    STONE       = make_mat("Sandstone",      (0.635, 0.525, 0.380))
    STONE_LIGHT = make_mat("SandstoneLight", (0.700, 0.600, 0.450))
    STONE_BAND  = make_mat("SandstoneBand",  (0.520, 0.415, 0.285))
    DARK        = make_mat("RecessDark",     (0.130, 0.105, 0.080), 1.0)
    GREY        = make_mat("BackdropGrey",   (0.46, 0.46, 0.46), 1.0)

# ---------------------------------------------------------------- helpers
def finish_obj(o, material=None, bevel=0.0):
    if material:
        o.data.materials.append(material)
    if bevel > 0:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        mod = o.modifiers.new("bev", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def box(name, cx, cy, cz, sx, sy, sz, material=None, bevel=0.0,
        rotx=0.0, roty=0.0, rotz=0.0):
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    o = bpy.context.active_object
    o.name = name
    o.dimensions = (sx, sy, sz)
    o.rotation_euler = (rotx, roty, rotz)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return finish_obj(o, material, bevel)

def frustum(name, cx, cy, z0, z1, sx0, sy0, sx1, sy1, dx=0.0, dy=0.0,
            material=None, bevel=0.0):
    """Tapered box: bottom size (sx0, sy0) at z0, top (sx1, sy1) at z1,
    top centre offset by (dx, dy). Centred on (cx, cy) at the base."""
    v = [
        (cx - sx0/2, cy - sy0/2, z0), (cx + sx0/2, cy - sy0/2, z0),
        (cx + sx0/2, cy + sy0/2, z0), (cx - sx0/2, cy + sy0/2, z0),
        (cx + dx - sx1/2, cy + dy - sy1/2, z1), (cx + dx + sx1/2, cy + dy - sy1/2, z1),
        (cx + dx + sx1/2, cy + dy + sy1/2, z1), (cx + dx - sx1/2, cy + dy + sy1/2, z1),
    ]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return finish_obj(o, material, bevel)

def lathe(name, cx, cy, cz, profile, material=None, segments=28):
    """Surface of revolution about the Z axis. profile = [(r, z), ...]
    in figure-local heights (z measured from the statue slab top)."""
    verts, faces = [], []
    n = len(profile)
    for (r, z) in profile:
        for j in range(segments):
            a = 2 * math.pi * j / segments
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), cz + z))
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, i * segments + j2,
                          (i + 1) * segments + j2, (i + 1) * segments + j))
    # cap fans
    cb = len(verts); verts.append((cx, cy, cz + profile[0][1]))
    ct = len(verts); verts.append((cx, cy, cz + profile[-1][1]))
    for j in range(segments):
        j2 = (j + 1) % segments
        faces.append((cb, j2, j))
        base = (n - 1) * segments
        faces.append((ct, base + j, base + j2))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return finish_obj(o, material, 0.0)

def drape_collar(name, cx, z_top, z_bot, mats, xw=2.9, yfront=-0.55):
    """Broad wesekh collar draped on the chest: a parametric band whose
    plan curve hugs the torso front and wraps toward the shoulders.
    z values are absolute world z. Alternating materials per row band."""
    cols, rows = 14, 5
    verts, faces, fmat = [], [], []
    for r_i in range(rows):
        v = r_i / (rows - 1)                    # 0 top -> 1 bottom
        z = z_top + (z_bot - z_top) * v
        for c_i in range(cols):
            t = -1 + 2 * c_i / (cols - 1)
            x = xw * t
            y = yfront + (0.55 - yfront) * t * t
            k = 0.55 + 0.45 * v                 # pull in toward the neck at top
            x *= k
            y = y * k + 0.40 * (1 - k)
            zz = z + 0.55 * t * t * v           # lower edge rises at the sides
            verts.append((cx + x, y, zz))
    for r_i in range(rows - 1):
        for c_i in range(cols - 1):
            a = r_i * cols + c_i
            b = a + 1
            c = a + cols + 1
            d = a + cols
            faces.append((a, d, c, b))
            fmat.append(r_i % 2)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    for m in mats:
        me.materials.append(m)
    for poly, mi in zip(me.polygons, fmat):
        poly.material_index = mi
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    mod = o.modifiers.new("sol", "SOLIDIFY")
    mod.thickness = 0.06
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def cyl(name, cx, cy, cz, r, h, material=None, verts=20, rotx=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h,
                                        location=(cx, cy, cz), rotation=(rotx, 0, 0))
    o = bpy.context.active_object
    o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return finish_obj(o, material, 0.0)

# ---------------------------------------------------------------- one colossus
def build_colossus(tag, cx):
    """Seated pharaoh, Abu Simbel type. Local origin: statue centreline on
    the shared plinth slab top (z = PED_H + B in world). Front faces -Y."""
    z0 = PED_H + B
    def Z(h):  # height above slab top -> world z
        return z0 + h
    # throne back slab
    box(f"{tag}_BackSlab", cx, 3.25, Z(8.6), 6.6, 1.3, 17.2, STONE, 0.06)
    # throne side cheeks + seat
    for s in (-1, 1):
        box(f"{tag}_Cheek{s}", cx + s * 3.15, 1.2, Z(3.45), 1.1, 4.6, 6.9, STONE, 0.05)
        # recessed relief panel on the outer face (border + inner panel, no glyphs)
        box(f"{tag}_PanelFrame{s}", cx + s * 3.72, 1.2, Z(3.6), 0.10, 3.4, 5.2, STONE_LIGHT, 0.02)
        box(f"{tag}_PanelInner{s}", cx + s * 3.76, 1.2, Z(3.6), 0.08, 2.9, 4.6, STONE_BAND, 0.02)
    box(f"{tag}_Seat", cx, 1.2, Z(6.65), 7.4, 4.8, 0.5, STONE, 0.04)
    box(f"{tag}_Fascia", cx, -0.5, Z(3.2), 5.2, 0.5, 6.4, STONE, 0.04)
    # legs: feet, toes, shins, knees, thighs
    for s in (-1, 1):
        lx = cx + s * 1.6
        # solid throne mass under each thigh, behind the shins
        box(f"{tag}_Support{s}", lx, 1.1, Z(5.1), 3.3, 2.6, 3.6, STONE, 0.05)
        box(f"{tag}_Foot{s}", lx, -1.55, Z(0.85), 2.5, 4.0, 1.7, STONE_LIGHT, 0.16)
        for i in range(5):  # toes, middle longest, projecting past the foot front
            tl = (0.48, 0.58, 0.64, 0.56, 0.44)[i]
            box(f"{tag}_Toe{s}_{i}", lx - 0.9 + i * 0.45, -3.85 + tl / 2,
                Z(0.55), 0.38, tl, 1.1, STONE_LIGHT, 0.14)
        frustum(f"{tag}_Shin{s}", lx, -0.3, Z(1.4), Z(7.55),
                2.2, 2.3, 2.8, 3.0, dy=-0.05, material=STONE, bevel=0.15)
        box(f"{tag}_Knee{s}", lx, -1.95, Z(7.35), 3.0, 1.9, 1.5, STONE, 0.4)
        box(f"{tag}_Thigh{s}", lx + s * 0.02, -0.05, Z(7.7), 3.3, 4.6, 2.4,
            STONE, 0.26, rotx=0.045)
    # kilt
    box(f"{tag}_KiltFront", cx, -0.5, Z(8.4), 3.3, 0.32, 2.75, STONE_BAND, 0.06, rotx=0.64)
    for s in (-1, 1):
        box(f"{tag}_KiltSide{s}", cx + s * 2.85, 0.45, Z(8.15), 1.8, 3.3, 2.3, STONE, 0.12)
    box(f"{tag}_Waistband", cx, 0.85, Z(9.55), 5.3, 2.6, 0.55, STONE_BAND, 0.05)
    # torso
    frustum(f"{tag}_Torso", cx, 1.2, Z(9.3), Z(14.9), 5.4, 2.6, 6.0, 2.8,
            material=STONE, bevel=0.20)
    box(f"{tag}_Shoulders", cx, 1.15, Z(14.55), 7.4, 2.5, 1.1, STONE, 0.25)
    cyl(f"{tag}_Navel", cx, -0.12, Z(10.6), 0.10, 0.06, DARK, 12, rotx=math.pi / 2)
    # arms: upper arm vertical, forearm on thigh, hand + fingers on knee
    for s in (-1, 1):
        ax = cx + s * 2.85
        box(f"{tag}_UpperArm{s}", ax, 0.85, Z(12.2), 1.95, 2.1, 4.3, STONE, 0.28)
        box(f"{tag}_Elbow{s}", cx + s * 2.8, 1.0, Z(9.9), 1.8, 1.9, 1.6, STONE, 0.3)
        box(f"{tag}_Forearm{s}", cx + s * 2.65, -0.65, Z(8.55), 1.7, 3.6, 1.35, STONE, 0.24)
        hx = cx + s * 2.5
        box(f"{tag}_Hand{s}", hx, -1.7, Z(8.4), 2.0, 2.0, 0.85, STONE_LIGHT, 0.22)
        for i in range(4):
            box(f"{tag}_Finger{s}_{i}", hx - 0.6 + i * 0.4, -2.8, Z(8.05),
                0.38, 1.05, 0.55, STONE_LIGHT, 0.14, rotx=0.45)
        # cartouche plate on the outer upper arm (seen in the photograph)
        box(f"{tag}_ArmPlate{s}", cx + s * 3.89, 0.85, Z(12.4), 0.10, 0.8, 1.9, STONE_LIGHT, 0.03)
        box(f"{tag}_ArmPlateIn{s}", cx + s * 3.95, 0.85, Z(12.4), 0.06, 0.55, 1.55, STONE_BAND, 0.02)
    # broad collar draped across the chest (stepped bands)
    drape_collar(f"{tag}_Collar", cx, Z(14.7), Z(10.95), [STONE_BAND, STONE_LIGHT])
    # chest cartouche pendant (oval ring, no inscription)
    cyl(f"{tag}_ChestCart", cx, -0.18, Z(11.9), 0.55, 0.14, STONE_LIGHT, 24, rotx=math.pi / 2)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.62, minor_radius=0.07,
                                     major_segments=24, minor_segments=8,
                                     location=(cx, -0.2, Z(11.9)), rotation=(math.pi / 2, 0, 0))
    ring = bpy.context.active_object
    ring.name = f"{tag}_ChestRing"
    ring.scale = (1.0, 1.45, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ring.data.materials.append(STONE_BAND)
    # neck + head
    cyl(f"{tag}_Neck", cx, 1.1, Z(15.25), 1.05, 0.8, STONE, 20)
    hy = 1.1  # head centre y
    box(f"{tag}_Skull", cx, hy, Z(16.9), 2.9, 2.5, 3.3, STONE, 0.38)
    box(f"{tag}_Jaw", cx, hy - 0.08, Z(15.75), 2.3, 2.1, 1.15, STONE, 0.3)
    box(f"{tag}_Nose", cx, hy - 1.42, Z(16.55), 0.62, 0.75, 1.55, STONE, 0.18)
    box(f"{tag}_Brow", cx, hy - 1.3, Z(17.35), 2.35, 0.35, 0.42, STONE, 0.1)
    for s in (-1, 1):
        box(f"{tag}_Eye{s}", cx + s * 0.68, hy - 1.32, Z(16.95), 0.78, 0.18, 0.34, STONE_LIGHT, 0.12)
        box(f"{tag}_Ear{s}", cx + s * 1.42, hy - 0.6, Z(16.6), 0.42, 0.8, 1.15, STONE, 0.15)
    box(f"{tag}_Mouth", cx, hy - 1.3, Z(15.95), 0.95, 0.16, 0.2, STONE_BAND, 0.05)
    # false beard: long, broad, banded (very prominent in the photograph)
    box(f"{tag}_Beard", cx, hy - 1.40, Z(13.65), 1.6, 0.55, 3.1, STONE, 0.1)
    for i, bz in enumerate((12.6, 13.2, 13.8, 14.4, 15.0)):
        box(f"{tag}_BeardBand{i}", cx, hy - 1.70, Z(bz), 1.66, 0.1, 0.16, STONE_BAND, 0.03)
    # nemes headdress: striped wings (alternating tone slices) + back fall
    box(f"{tag}_NemesBand", cx, hy - 1.38, Z(17.62), 3.1, 0.7, 0.5, STONE_BAND, 0.06)
    box(f"{tag}_NemesTop", cx, hy + 0.05, Z(18.35), 3.2, 2.6, 0.75, STONE, 0.25)
    for side in (-1, 1):
        for i in range(6):
            ztop = 17.6 - i * 0.6
            outer = 1.5 + (i + 1) * 0.30
            yf = -0.2 + i * 0.13           # front edge drifts back going down
            depth = 2.5 - yf
            w = outer - 1.05
            box(f"{tag}_NemesWing{side}_{i}", cx + side * (1.05 + w / 2), hy - 0.75 + yf + depth / 2,
                Z(ztop - 0.3), w, depth, 0.6,
                STONE if i % 2 == 0 else STONE_BAND, 0.05)
    for i in range(4):  # back fall of the nemes
        ztop = 17.3 - i * 0.68
        box(f"{tag}_NemesBack{i}", cx, hy + 1.5, Z(ztop - 0.34), 2.9, 0.5, 0.68,
            STONE if i % 2 == 0 else STONE_BAND, 0.05)
    # tall crown (lathe) + uraeus boss
    profile = [(0.02, 17.6), (1.30, 17.6), (1.38, 17.85), (1.40, 18.6),
               (1.38, 19.2), (1.22, 19.65), (0.70, 19.92), (0.02, 20.0)]
    lathe(f"{tag}_Crown", cx, hy, z0, profile, STONE_LIGHT, 32)
    cyl(f"{tag}_Uraeus", cx, hy - 1.43, Z(18.35), 0.13, 0.5, STONE_BAND, 10)
    cyl(f"{tag}_UraeusDisc", cx, hy - 1.46, Z(18.68), 0.2, 0.1, STONE_BAND, 14, rotx=math.pi / 2)

# ---------------------------------------------------------------- small standing figure
def build_figure(tag, cx, cy, base_z, h):
    """Small family figure of the Abu Simbel group (mother/wife/daughter
    in the 1856 guide). Simplified standing figure in a long robe."""
    w = 0.33 * h
    frustum(f"{tag}_Robe", cx, cy, base_z, base_z + 0.60 * h,
            w, 0.20 * h, w * 0.62, 0.15 * h, material=STONE, bevel=0.03)
    box(f"{tag}_Torso", cx, cy, base_z + 0.70 * h, w * 0.8, 0.15 * h, 0.22 * h, STONE, 0.03)
    for s in (-1, 1):
        box(f"{tag}_Arm{s}", cx + s * (w * 0.42), cy, base_z + 0.55 * h,
            0.05 * h, 0.09 * h, 0.42 * h, STONE, 0.02)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, radius=0.085 * h,
                                         location=(cx, cy, base_z + 0.90 * h))
    head = bpy.context.active_object
    head.name = f"{tag}_Head"
    head.data.materials.append(STONE)
    box(f"{tag}_Wig", cx, cy + 0.03 * h, base_z + 0.86 * h,
        0.17 * h, 0.15 * h, 0.24 * h, STONE_BAND, 0.03)
    box(f"{tag}_Feet", cx, cy - 0.09 * h, base_z + 0.015 * h,
        0.16 * h, 0.10 * h, 0.03 * h, STONE, 0.01)

# ---------------------------------------------------------------- pedestal
def build_pedestal():
    box("PED_Block", 0, 0.7, PED_H / 2, 17.2, 9.8, PED_H, STONE, 0.05)
    box("PED_BaseCourse", 0, 0.7, 0.18, 17.5, 10.1, 0.36, STONE_BAND, 0.03)
    box("PED_Cornice", 0, 0.7, PED_H - 0.18, 17.7, 10.3, 0.36, STONE, 0.03)
    # slotted front band: dark recess surface just proud of the block face,
    # stone pilasters standing further proud, square holes row above.
    # (Block front face is at y = -4.2; more negative = further forward.)
    box("PED_SlotBack", 0, -4.18, 2.35, 16.6, 0.06, 3.7, DARK, 0.0)
    n = 31
    for i in range(n):
        x = -8.0 + i * (16.0 / (n - 1))
        if abs(x) < 1.7:
            continue  # doorway interrupts the pattern
        box(f"PED_Pilaster{i}", x, -4.23, 2.35, 0.36, 0.14, 3.7, STONE, 0.02)
        box(f"PED_Hole{i}", x, -4.21, 4.42, 0.3, 0.04, 0.3, DARK, 0.0)
    # central doorway with lintel and a lit notice board inside
    for s in (-1, 1):
        box(f"PED_Jamb{s}", s * 1.25, -4.24, 1.4, 0.3, 0.12, 2.8, STONE_LIGHT, 0.02)
    box("PED_Lintel", 0, -4.24, 2.95, 2.8, 0.12, 0.35, STONE_LIGHT, 0.02)
    box("PED_DoorDark", 0, -4.22, 1.4, 2.3, 0.08, 2.8, DARK, 0.0)
    box("PED_DoorBoard", 0, -4.27, 1.55, 1.5, 0.04, 1.05, STONE_LIGHT, 0.0)
    box("PED_Step", 0, -4.45, 0.09, 2.6, 0.5, 0.18, STONE, 0.02)
    # shared plinth slab under both statues
    box("PED_Plinth", 0, 0.25, PED_H + B / 2, 17.0, 8.3, B, STONE_LIGHT, 0.04)

# ---------------------------------------------------------------- scene
def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    init_materials()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    build_pedestal()
    build_colossus("L", -4.3)
    build_colossus("R", 4.3)
    base = PED_H + B
    # family figures: between the legs of each colossus (2.8 m),
    # taller figures at the outer sides and between the pair (4.7 m)
    build_figure("FIG_L_between", -4.3, -0.25, base, 2.8)
    build_figure("FIG_R_between", 4.3, -0.25, base, 2.8)
    build_figure("FIG_L_outer", -7.85, 0.2, base, 4.7)
    build_figure("FIG_R_outer", 7.85, 0.2, base, 4.7)
    build_figure("FIG_Centre", 0.0, -0.9, base, 4.7)

    tris = 0
    meshes = 0
    for o in bpy.data.objects:
        if o.type == "MESH":
            meshes += 1
            for p in o.data.polygons:
                tris += len(p.vertices) - 2
    print(f"MESHES={meshes} TRIS={tris}")
    dims = (17.7, 10.3, PED_H + B + FIG_H)
    print(f"DIMS={dims}")

    blend_path = os.path.join(ROOT, "egyptian-court-colossi.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("SAVED", blend_path)

    glb_path = os.path.join(ROOT, "egyptian-court-colossi.glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB",
                              export_apply=True)
    print("EXPORTED", glb_path)

    # ---- render rig (added after save/export so the prop files stay clean)
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.01))
    ground = bpy.context.active_object
    ground.name = "Ground"
    ground.data.materials.append(GREY)

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.42, 0.42, 0.42, 1.0)
    bg.inputs[1].default_value = 0.4

    def sun(name, loc, energy, angle_deg, shadow=True):
        ld = bpy.data.lights.new(name, "SUN")
        ld.energy = energy
        ld.angle = math.radians(angle_deg)
        ld.use_shadow = shadow
        lo = bpy.data.objects.new(name, ld)
        bpy.context.collection.objects.link(lo)
        lo.location = loc
        lo.rotation_euler = (math.radians(52), math.radians(8), math.radians(-38))
        return lo
    sun("KeySun", (-20, -25, 40), 3.4, 18)
    sun("FillSun", (30, 18, 25), 0.7, 30, shadow=False)

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 42
    cam_data.clip_end = 600
    cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam

    import mathutils
    target = mathutils.Vector((0, 0.3, 12.4))

    def shoot(name, pos):
        cam.location = pos
        direction = target - mathutils.Vector(pos)
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        scene.render.filepath = os.path.join(ROOT, "renders", name)
        bpy.ops.render.render(write_still=True)
        print("RENDERED", name)

    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1400
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    if hasattr(scene.eevee, "use_shadows"):
        scene.eevee.use_shadows = True

    shoot("front.png", (0, -50, 13.8))
    shoot("side.png", (50, 0.3, 13.8))
    shoot("three-quarter.png", (-35, -39, 18.5))

if __name__ == "__main__":
    main()
