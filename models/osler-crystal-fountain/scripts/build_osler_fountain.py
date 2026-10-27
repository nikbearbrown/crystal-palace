#!/usr/bin/env python3
"""
Osler Crystal Fountain (candidate #12) — fully procedural bpy build.

Hyde Park 1851 transept centrepiece, F. & C. Osler of Birmingham.
Governing references (all in repo refs/):
  - Wellcome engraving L0022578 (CC BY 4.0)  — governs structure & detail
  - Opening-day engraving 1851 (PD)          — silhouette cross-check
  - Nash lithograph, The Transept (PD)       — distant silhouette
  - MET photograph DP238264 (CC0)            — Sydenham; form comparison only

Scale: total height 27 ft = 8.2296 m (documented figure — see NOTES.md).
Basin diameter DEFINED by this build: 7.2 m (R 3.6 m).

All proportions are lathe-of-revolution parts + instanced repeats.
Real-world metres, Z up, origin at base (basin floor) centre.
"""
import bpy
import math
import os
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "osler-crystal-fountain"

# ---------------------------------------------------------------- parameters
FT = 0.3048
H_TOTAL = 27 * FT            # 8.2296 m — documented height, see NOTES.md
BASIN_R = 3.6                # basin radius DEFINED here (diameter 7.2 m)

# ---------------------------------------------------------------- clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------------------------------------------------------------- materials
def make_glass(name, tint, thickness, rough=0.04):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*tint, 1.0)
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["Roughness"].default_value = rough
    b.inputs["IOR"].default_value = 1.52
    # NB Blender 4.2 Principled has no Thickness socket; refraction depth
    # comes from the closed-shell geometry itself, as modelled.
    b.inputs["Specular IOR Level"].default_value = 1.0
    return m

GLASS = make_glass("OslerGlass", (0.965, 0.985, 0.975), 0.035)
GLASS_THICK = make_glass("OslerGlassThick", (0.93, 0.965, 0.945), 0.09, 0.09)

WATER = bpy.data.materials.new("FallingWater")
WATER.use_nodes = True
wb = WATER.node_tree.nodes["Principled BSDF"]
wb.inputs["Base Color"].default_value = (0.82, 0.90, 0.97, 1.0)
wb.inputs["Transmission Weight"].default_value = 0.9
wb.inputs["Roughness"].default_value = 0.10
wb.inputs["IOR"].default_value = 1.33
wb.inputs["Alpha"].default_value = 0.22
WATER.blend_method = 'BLEND' if hasattr(WATER, 'blend_method') else None

WATER_STILL = bpy.data.materials.new("BasinWater")
WATER_STILL.use_nodes = True
sb = WATER_STILL.node_tree.nodes["Principled BSDF"]
sb.inputs["Base Color"].default_value = (0.45, 0.55, 0.58, 1.0)
sb.inputs["Roughness"].default_value = 0.15
sb.inputs["Metallic"].default_value = 0.0
sb.inputs["Alpha"].default_value = 0.88

STONE = bpy.data.materials.new("BasinStone")
STONE.use_nodes = True
tb = STONE.node_tree.nodes["Principled BSDF"]
tb.inputs["Base Color"].default_value = (0.78, 0.76, 0.72, 1.0)
tb.inputs["Roughness"].default_value = 0.5

# ---------------------------------------------------------------- helpers
def lathe(name, profile, material, segments=72, flutes=0, closed_loop=False):
    """profile: list of (r, z, amp) — amp = radial flute amplitude fraction
    at that ring (0 = smooth). Returns the created object."""
    verts, faces = [], []
    rings = len(profile)
    for i, (r, z, amp) in enumerate(profile):
        for j in range(segments):
            th = 2.0 * math.pi * j / segments
            rr = r * (1.0 + amp * math.cos(flutes * th)) if flutes else r
            verts.append((rr * math.cos(th), rr * math.sin(th), z))
    nfaces = rings - 1 + (1 if closed_loop else 0)
    for i in range(nfaces):
        i2 = (i + 1) % rings
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, i * segments + j2,
                          i2 * segments + j2, i2 * segments + j))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    for p in mesh.polygons:
        p.use_smooth = True
    return obj

def box(name, size, loc, material, rot_z=0.0, rot_x=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    o.rotation_euler = (rot_x, 0.0, rot_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        o.data.materials.append(material)
    return o

def place(obj, loc, rot_z=0.0, scale=None):
    obj.location = loc
    obj.rotation_euler = (0.0, 0.0, rot_z)
    if scale:
        obj.scale = scale
    return obj

P = []  # (r, z) plain profile helper
def prof(pts, amp=0.0):
    return [(r, z, amp) for (r, z) in pts]

# ================================================================ BASIN
# rim ring — closed lathe loop, plain solid ring (stone: interpretation)
rim_profile = [
    (3.24, 0.02, 0), (3.26, 0.16, 0), (3.30, 0.28, 0), (3.40, 0.355, 0),
    (3.52, 0.375, 0), (3.60, 0.335, 0), (3.615, 0.24, 0), (3.60, 0.10, 0),
    (3.55, 0.0, 0), (3.30, 0.0, 0),
]
lathe("BasinRim", rim_profile, STONE, segments=96, closed_loop=True)

# basin floor disc
bpy.ops.mesh.primitive_circle_add(radius=BASIN_R, vertices=96,
                                  fill_type='NGON', location=(0, 0, 0.0))
floor = bpy.context.active_object
floor.name = "BasinFloor"
floor.data.materials.append(STONE)

# still water disc
bpy.ops.mesh.primitive_circle_add(radius=3.26, vertices=96,
                                  fill_type='NGON', location=(0, 0, 0.29))
wdisc = bpy.context.active_object
wdisc.name = "BasinWater"
wdisc.data.materials.append(WATER_STILL)

# ================================================================ STEPS (stone)
lathe("StepLower", prof([(1.24, 0.0), (1.26, 0.07), (1.24, 0.16),
                         (1.18, 0.215), (0.9, 0.22), (0.9, 0.0)]),
      STONE, segments=72, closed_loop=True)
lathe("StepUpper", prof([(1.10, 0.22), (1.11, 0.30), (1.08, 0.40),
                         (1.0, 0.44), (0.9, 0.44), (0.9, 0.22)]),
      STONE, segments=72, closed_loop=True)

# ================================================================ BASE DRUM (glass, thick)
drum_profile = [
    (0.98, 0.44, 0), (1.0, 0.52, 0), (0.96, 0.72, 0), (0.925, 1.0, 0),
    (0.925, 1.28, 0), (0.96, 1.46, 0), (1.0, 1.52, 0), (1.0, 1.58, 0),
    (0.86, 1.58, 0), (0.86, 0.44, 0),
]
lathe("BaseDrum", drum_profile, GLASS_THICK, segments=72, closed_loop=True)

# panel blocks around drum base (8) + buttress fins (8) + shell cartouches (4)
def radial_prism(name, tri, half_thick, material):
    """Triangular prism in the (r, z) plane at angle 0, extruded tangentially.
    tri: [(r, z), (r, z), (r, z)]. Copy-rotate for the other positions."""
    (r1, z1), (r2, z2), (r3, z3) = tri
    t = half_thick
    verts = [(r1, -t, z1), (r2, -t, z2), (r3, -t, z3),
             (r1, t, z1), (r2, t, z2), (r3, t, z3)]
    faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    return obj

fin0 = radial_prism("ButtressFin",
                    [(1.24, 0.44), (0.94, 1.34), (1.06, 1.38)],
                    0.05, GLASS_THICK)
for k in range(8):
    a = k * math.pi / 4.0
    ca, sa = math.cos(a), math.sin(a)
    blk = box(f"PanelBlock{k}", (0.36, 0.10, 0.20),
              (1.03 * ca, 1.03 * sa, 0.56), GLASS_THICK, rot_z=-a + math.pi / 2)
    cap = box(f"PanelCap{k}", (0.40, 0.13, 0.05),
              (1.03 * ca, 1.03 * sa, 0.685), GLASS_THICK, rot_z=-a + math.pi / 2)
    if k:
        o = fin0.copy()
        bpy.context.collection.objects.link(o)
        o.name = f"ButtressFin{k}"
        o.rotation_euler = (0.0, 0.0, a)

# shell cartouches: fluted flattened discs on the drum faces (schematic)
shell_profile = [(0.012, 0.0, 0), (0.10, 0.012, 0.10), (0.19, 0.03, 0.14),
                 (0.26, 0.055, 0.16), (0.285, 0.085, 0.12)]
for k in range(4):
    a = k * math.pi / 2.0 + math.pi / 4.0
    sh = lathe(f"ShellCartouche{k}", shell_profile, GLASS_THICK,
               segments=36, flutes=9)
    sh.rotation_mode = 'ZYX'
    sh.rotation_euler = (math.pi / 2, 0.0, -a + math.pi / 2)
    sh.location = (0.90 * math.cos(a), 0.90 * math.sin(a), 1.02)
    sh.scale = (1.0, 1.0, 1.15)

# base pinnacles (8): pointed glass buds around the drum shoulder
pin_profile = prof([(0.105, 0.0), (0.115, 0.04), (0.075, 0.10), (0.085, 0.24),
                    (0.105, 0.40), (0.09, 0.55), (0.05, 0.70), (0.014, 0.83),
                    (0.004, 0.88)])
pin_mesh_obj = lathe("PinnacleBase", pin_profile, GLASS, segments=28)
place(pin_mesh_obj, (0.80, 0.0, 1.12))
for k in range(1, 8):
    a = k * math.pi / 4.0
    o = pin_mesh_obj.copy()
    bpy.context.collection.objects.link(o)
    o.name = f"PinnacleBase{k}"
    place(o, (0.80 * math.cos(a), 0.80 * math.sin(a), 1.12))

# ================================================================ ARCADE STAGE
# central core
lathe("ArcadeCore", prof([(0.27, 1.58), (0.29, 1.66), (0.25, 2.2),
                          (0.25, 2.9), (0.29, 3.02), (0.27, 3.10),
                          (0.20, 3.10), (0.20, 1.58)]),
      GLASS_THICK, segments=48, closed_loop=True)
# ring plate at arcade top
lathe("ArcadePlate", prof([(0.98, 3.0), (0.98, 3.10), (0.90, 3.14),
                           (0.30, 3.14), (0.30, 3.0)]),
      GLASS_THICK, segments=72, closed_loop=True)
# columns (8) with capital flare
col_profile = prof([(0.055, 0.0), (0.062, 0.03), (0.042, 0.09), (0.040, 0.55),
                    (0.042, 0.95), (0.062, 1.02), (0.070, 1.06)])
col0 = lathe("ArcadeColumn", col_profile, GLASS, segments=20)
place(col0, (0.80, 0.0, 1.58))
for k in range(1, 8):
    a = k * math.pi / 4.0
    o = col0.copy()
    bpy.context.collection.objects.link(o)
    o.name = f"ArcadeColumn{k}"
    place(o, (0.80 * math.cos(a), 0.80 * math.sin(a), 1.58))

# pointed arch ribs between columns (8 bays)
def arch_rib(name, R=0.80, spring_z=2.64, half_chord=0.306, centre_off=0.12,
             tube=0.030, material=GLASS):
    Ra = half_chord + centre_off
    apex_z = spring_z + math.sqrt(max(Ra * Ra - centre_off * centre_off, 0.01))
    pts = []
    # left arc: centre at (+centre_off, spring_z) in local (x=chord, z)
    for i in range(13):
        t = i / 12.0
        ang = math.pi - t * (math.pi - math.atan2(apex_z - spring_z, centre_off))
        # param by angle around left centre from springing point to apex
        x = centre_off + Ra * math.cos(ang)
        z = spring_z + Ra * math.sin(ang)
        pts.append((x, z))
    for i in range(1, 13):
        t = i / 12.0
        ang = math.atan2(apex_z - spring_z, centre_off) + t * (
            math.pi - math.atan2(apex_z - spring_z, centre_off))
        x = -centre_off + Ra * math.cos(ang)
        z = spring_z + Ra * math.sin(ang)
        pts.append((x, z))
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = tube
    cu.bevel_resolution = 2
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for i, (x, z) in enumerate(pts):
        sp.points[i].co = (x, 0.0, z, 1.0)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob.select_set(False)
    if material:
        ob.data.materials.append(material)
    return ob

arch0 = arch_rib("ArchRib")
# position: bay centred at angle 22.5°, radius R, chord along local X
def place_arch(o, ang, R=0.80):
    o.rotation_euler = (0, 0, ang)
    # local +X after rot_z is tangential if we offset position along the
    # bisector and rotate so X is tangent: place at bisector point.
    o.location = (R * math.cos(ang), R * math.sin(ang), 0.0)
place_arch(arch0, math.radians(22.5))
for k in range(1, 8):
    o = arch0.copy()
    bpy.context.collection.objects.link(o)
    o.name = f"ArchRib{k}"
    place_arch(o, math.radians(22.5 + 45 * k))

# ================================================================ GREAT DISH
# wide shallow umbrella dish, fluted underside, scalloped rim
dish_profile = [
    (0.30, 3.10, 0.0), (0.55, 3.16, 0.010), (0.85, 3.26, 0.016),
    (1.10, 3.38, 0.022), (1.30, 3.50, 0.028), (1.415, 3.585, 0.035),
    (1.43, 3.615, 0.038),                       # rim
    (1.41, 3.635, 0.035), (1.28, 3.595, 0.022), (1.05, 3.52, 0.014),
    (0.75, 3.45, 0.008), (0.45, 3.40, 0.0), (0.30, 3.38, 0.0),
    (0.28, 3.10, 0.0),
]
lathe("GreatDish", dish_profile, GLASS, segments=96, flutes=24,
      closed_loop=True)

# stem above great dish
lathe("BowlStem", prof([(0.17, 3.55), (0.15, 3.75), (0.17, 3.92),
                        (0.30, 3.98), (0.30, 3.90), (0.13, 3.88),
                        (0.13, 3.55)]),
      GLASS_THICK, segments=48, closed_loop=True)

# ================================================================ WIDE FLUTED BOWL
bowl_profile = [
    (0.30, 3.95, 0.0), (0.55, 3.96, 0.01), (0.78, 4.02, 0.018),
    (0.885, 4.16, 0.028), (0.92, 4.34, 0.04), (0.925, 4.42, 0.05),
    (0.90, 4.44, 0.045), (0.86, 4.30, 0.03), (0.72, 4.14, 0.015),
    (0.45, 4.06, 0.0), (0.30, 4.05, 0.0),
]
lathe("WideBowl", bowl_profile, GLASS, segments=80, flutes=16,
      closed_loop=True)

# ================================================================ MIDDLE DRUM
mid_profile = [
    (0.34, 4.05, 0), (0.44, 4.14, 0.01), (0.50, 4.38, 0.03),
    (0.515, 4.68, 0.035), (0.47, 4.95, 0.03), (0.36, 5.14, 0.01),
    (0.335, 5.23, 0), (0.30, 5.23, 0), (0.30, 4.05, 0),
]
lathe("MiddleDrum", mid_profile, GLASS_THICK, segments=64, flutes=12,
      closed_loop=True)

# middle pinnacles (6), standing on the wide bowl's floor around the drum,
# tips level with the drum top, as in the engraving
pin2_profile = prof([(0.085, 0.0), (0.092, 0.04), (0.06, 0.10), (0.07, 0.26),
                     (0.085, 0.44), (0.07, 0.62), (0.038, 0.81),
                     (0.010, 0.94), (0.003, 0.99)])
pin2 = lathe("PinnacleMid", pin2_profile, GLASS, segments=24)
place(pin2, (0.58, 0.0, 4.05))
for k in range(1, 6):
    a = k * math.pi / 3.0
    o = pin2.copy()
    bpy.context.collection.objects.link(o)
    o.name = f"PinnacleMid{k}"
    place(o, (0.58 * math.cos(a), 0.58 * math.sin(a), 4.05))

# ================================================================ SMALL DISH + CUP
lathe("SmallDishStem", prof([(0.085, 5.20), (0.075, 5.32), (0.10, 5.36),
                             (0.10, 5.20)]),
      GLASS, segments=32, closed_loop=True)
sdish_profile = [
    (0.10, 5.32, 0.0), (0.24, 5.35, 0.02), (0.36, 5.40, 0.035),
    (0.425, 5.445, 0.05), (0.43, 5.465, 0.05), (0.40, 5.45, 0.03),
    (0.28, 5.42, 0.01), (0.12, 5.40, 0.0),
]
lathe("SmallDish", sdish_profile, GLASS, segments=64, flutes=12,
      closed_loop=True)
cup_profile = [
    (0.07, 5.44, 0.0), (0.10, 5.52, 0.01), (0.20, 5.62, 0.025),
    (0.30, 5.72, 0.04), (0.345, 5.80, 0.05), (0.33, 5.82, 0.045),
    (0.24, 5.72, 0.02), (0.12, 5.60, 0.0), (0.07, 5.52, 0.0),
]
lathe("FlowerCup", cup_profile, GLASS, segments=64, flutes=10,
      closed_loop=True)

# ================================================================ SPIKE + STACKED CUPS
lathe("Spike", prof([(0.040, 5.78), (0.030, 6.6), (0.026, 7.4),
                     (0.020, 8.02), (0.004, H_TOTAL)]),
      GLASS, segments=20, closed_loop=True)
cup_sizes = [(6.02, 0.155), (6.48, 0.135), (6.88, 0.115), (7.24, 0.098),
             (7.56, 0.082)]
for i, (z0, r) in enumerate(cup_sizes):
    cp = [(0.020, z0, 0), (r * 0.55, z0 + 0.03, 0.02), (r * 0.85, z0 + 0.11, 0.04),
          (r, z0 + 0.20, 0.05), (r * 0.94, z0 + 0.215, 0.04),
          (r * 0.6, z0 + 0.13, 0.01), (0.024, z0 + 0.06, 0)]
    lathe(f"SpikeCup{i}", cp, GLASS, segments=36, flutes=8, closed_loop=True)

# ================================================================ WATER (playing state)
# bell sheet falling from the spike top — shoulders quickly, then falls
# near-straight, per the engravings; fine flutes read as falling streaks
bell_profile = [
    (0.05, 8.18, 0.0), (0.22, 7.95, 0.006), (0.36, 7.60, 0.010),
    (0.44, 7.10, 0.012), (0.49, 6.60, 0.012), (0.53, 6.10, 0.012),
    (0.55, 5.62, 0.012),
]
lathe("WaterBell", bell_profile, WATER, segments=72, flutes=60)
# sheet: small dish -> wide bowl
lathe("WaterSheetSmall", [(0.415, 5.42, 0.012), (0.42, 5.0, 0.012),
                          (0.425, 4.48, 0.012)], WATER, segments=64, flutes=48)
# sheet: wide bowl -> great dish
lathe("WaterSheetBowl", [(0.905, 4.36, 0.010), (0.91, 4.0, 0.010),
                         (0.915, 3.68, 0.010)], WATER, segments=64, flutes=56)
# sheet: great dish -> basin (slight outward bow as it falls)
lathe("WaterSheetGreat", [(1.415, 3.56, 0.008), (1.425, 2.6, 0.008),
                          (1.445, 1.4, 0.008), (1.47, 0.36, 0.008)],
      WATER, segments=96, flutes=72)

# arcs: middle drum -> wide bowl rim (6 parabolic jets)
def water_arc(name, ang):
    p0 = Vector((0.30 * math.cos(ang), 0.30 * math.sin(ang), 5.05))
    p2 = Vector((0.88 * math.cos(ang), 0.88 * math.sin(ang), 4.40))
    p1 = (p0 + p2) / 2 + Vector((0, 0, 0.28))
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = 0.013
    cu.bevel_resolution = 1
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(1)
    sp.bezier_points[0].co = p0
    sp.bezier_points[0].handle_right = p1
    sp.bezier_points[1].co = p2
    sp.bezier_points[1].handle_left = p1
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob.select_set(False)
    ob.data.materials.append(WATER)
    return ob

for k in range(6):
    water_arc(f"WaterArc{k}", k * math.pi / 3.0 + math.pi / 6.0)

# ---------------------------------------------------------------- finish
# Apply scale where an object actually carries one (the shell cartouches).
# Instanced copies share mesh data and sit at scale 1, so they need nothing.
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
    if o.type == 'MESH' and tuple(o.scale) != (1.0, 1.0, 1.0):
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False,
                                       scale=True)
        o.select_set(False)

os.makedirs(BASE, exist_ok=True)
blend_path = os.path.join(BASE, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(BASE, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')

# stats
total_tris = 0
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        n = sum(len(p.vertices) - 2 for p in o.data.polygons)
        total_tris += n
        print(f"OBJ {o.name:22s} tris={n}")
print(f"TOTAL_TRIS {total_tris}")
print(f"OBJECTS {len([o for o in bpy.context.scene.objects if o.type=='MESH'])}")
print(f"HEIGHT {H_TOTAL:.4f} m  BASIN_D {2*BASIN_R:.2f} m")
print("BUILD DONE")
