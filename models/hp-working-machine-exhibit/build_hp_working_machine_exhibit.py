#!/usr/bin/env python3
"""Build hp-working-machine-exhibit: Nasmyth steam hammer, Great Exhibition 1851.

Re-runnable Blender 4.5.3 script. Metres, origin at base centre, scale applied.
Source: staging-folder SPIKE.md section 7 (revised 2026-10-27 under the parent
agent's spike guardrail corrections).

Key facts baked in:
- Overall height H = 5.00 m ASSUMED / UNCONFIRMED (nominal modelling assumption;
  NOT measured, NOT taken from SMG co46218, NOT borrowed from any other hammer).
  All other dimensions are the Ferrier photograph's (RCIN 2800024) fractions of H.
- Tup + piston rod are ONE object named "Tup", shipped at mid-stroke
  (location z = 0; rest = z -0.65 m; full raise = z +0.65 m; travel 1.30 m).
- Maker's plates are BLANK boxes (no invented inscription).
- Mechanism: single-acting direct-action; steam below piston lifts, gravity drops.

Run: ~/workspace/tools/blender/blender --background --python build_hp_working_machine_exhibit.py
Outputs (same folder as this script): hp-working-machine-exhibit.blend,
hp-working-machine-exhibit.glb, renders/{front,side,three-quarter,tup-raised}.png
"""

import math
import os
from pathlib import Path

import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
RENDERS = OUT / "renders"
RENDERS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- dimensions (m)
H = 5.00            # ASSUMED / UNCONFIRMED nominal height, floor -> top of eye
FEET_W = 3.61       # photo-measured 0.722 H, overall width across feet
SOLE_DEPTH = 1.55   # inferred
CYL_R = 0.24        # photo-measured 0.096 H diameter
CYL_Z0, CYL_Z1 = 3.18, 4.67   # photo-measured 0.636 / 0.934 H
THROAT = 0.67       # photo-measured 0.134 H, clear width between guides
FOOT_W = 0.88       # photo-estimated, each standard foot (X)
STD_DEPTH = 0.88    # inferred (Y at base)
ANVIL_FACE_Z = 0.59  # photo-measured 0.118 H
FOUND_Z = 0.35      # photo-measured 0.070 H, foundation block top
TUP_DIE_H, TUP_BLOCK_H = 0.22, 0.57   # photo-measured
TUP_W = 0.67        # photo-measured (~ throat)
TUP_DEPTH = 0.67    # inferred
ROD_R = 0.06        # photo-estimated (0.12 m diameter)
REST_DIE_Z = 0.64   # photo-measured 0.128 H, die bottom at rest
TRAVEL = 1.30       # inferred, modelled travel above rest
MID = TRAVEL / 2.0  # shipped mid-stroke offset above rest

FOOT_X = FEET_W / 2.0 - FOOT_W / 2.0   # 1.365, foot centres
STD_TOP_X = 0.55    # standard top centre (meets cylinder seat beam)


# ---------------------------------------------------------------- helpers
def mat(name, rgb, metallic=0.0, roughness=0.8):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m


IRON = mat("IronDark", (0.23, 0.23, 0.24), metallic=0.55, roughness=0.65)
IRON_MID = mat("IronMid", (0.38, 0.38, 0.39), metallic=0.55, roughness=0.55)
STEEL = mat("Steel", (0.55, 0.55, 0.56), metallic=0.8, roughness=0.35)
ANVIL_MAT = mat("AnvilDark", (0.16, 0.16, 0.17), metallic=0.6, roughness=0.5)
GROUND_MAT = mat("GroundGrey", (0.72, 0.72, 0.72), roughness=0.95)


def box(name, loc, size, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    o.data.materials.append(material)
    return o


def cyl(name, loc, radius, height, material, axis="Z", verts=32):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=height, location=loc)
    o = bpy.context.active_object
    o.name = name
    if axis == "X":
        o.rotation_euler = (0, math.radians(90), 0)
    elif axis == "Y":
        o.rotation_euler = (math.radians(90), 0, 0)
    o.data.materials.append(material)
    return o


def torus(name, loc, major, minor, material, plane="XZ"):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, location=loc)
    o = bpy.context.active_object
    o.name = name
    if plane == "XZ":
        o.rotation_euler = (math.radians(90), 0, 0)
    o.data.materials.append(material)
    return o


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.materials):
        for block in list(coll):
            if block.users == 0 and block.name not in (
                    "IronDark", "IronMid", "Steel", "AnvilDark", "GroundGrey"):
                coll.remove(block)


# ---------------------------------------------------------------- build
def build():
    clear_scene()
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0

    # --- ground (render aid only, not part of the prop) ---
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    g = bpy.context.active_object
    g.name = "GroundPlane"
    g.data.materials.append(GROUND_MAT)

    # --- sole plates + feet ---
    for s in (-1, 1):
        box(f"SolePlate_{'L' if s < 0 else 'R'}",
            (s * FOOT_X, 0, 0.06), (FOOT_W, SOLE_DEPTH, 0.12), IRON)
        box(f"Foot_{'L' if s < 0 else 'R'}",
            (s * FOOT_X, 0, 0.26), (FOOT_W, STD_DEPTH, 0.28), IRON)

    # --- A-form standards (slanted boxes, feet -> cylinder seat) ---
    z_bot, z_top = 0.40, CYL_Z0
    mid_x = (FOOT_X + STD_TOP_X) / 2.0
    mid_z = (z_bot + z_top) / 2.0
    length = math.hypot(FOOT_X - STD_TOP_X, z_top - z_bot)
    ang = math.atan2(FOOT_X - STD_TOP_X, z_top - z_bot)
    for s, tag in ((-1, "L"), (1, "R")):
        o = box(f"Standard_{tag}", (s * mid_x, 0, mid_z),
                (0.55, 0.42, length), IRON)
        o.rotation_euler = (0, s * ang, 0)

    # --- cylinder seat beam + rear low tie beam ---
    box("SeatBeam", (0, 0, CYL_Z0 - 0.11), (1.50, 0.40, 0.22), IRON)
    box("RearTieBeam", (0, -0.35, 0.55), (2.20, 0.25, 0.25), IRON)

    # --- guide bars (throat faces) ---
    for s in (-1, 1):
        box(f"Guide_{'L' if s < 0 else 'R'}",
            (s * (THROAT / 2.0 + 0.04), 0, 1.75), (0.07, 0.50, 2.80), STEEL)

    # --- steam cylinder: barrel, covers, lifting eye ---
    cyl("CylinderBarrel", (0, 0, (CYL_Z0 + CYL_Z1) / 2.0),
        CYL_R, CYL_Z1 - CYL_Z0, IRON_MID)
    cyl("CylinderBottomCover", (0, 0, CYL_Z0), 0.29, 0.12, IRON)
    cyl("CylinderTopCover", (0, 0, CYL_Z1), 0.29, 0.12, IRON)
    cyl("EyeNeck", (0, 0, 4.79), 0.10, 0.12, IRON)
    torus("LiftingEye", (0, 0, 4.82), 0.12, 0.04, IRON, plane="XZ")

    # --- anvil + foundation ---
    box("AnvilFoundation", (0, 0, FOUND_Z / 2.0), (1.30, 1.10, FOUND_Z), ANVIL_MAT)
    box("AnvilBlock", (0, 0, (FOUND_Z + ANVIL_FACE_Z) / 2.0),
        (0.80, 0.80, ANVIL_FACE_Z - FOUND_Z), ANVIL_MAT)

    # --- blank maker's plate on right standard foot (NO inscription) ---
    box("MakersPlate_Blank", (FOOT_X, 0.45, 0.26), (0.45, 0.02, 0.28), STEEL)

    # --- valve chest (front of cylinder, offset left) + bolts ---
    box("ValveChest", (-0.28, 0.38, 3.30), (0.54, 0.30, 0.64), IRON)
    for dx in (-0.20, 0.20):
        for dz in (-0.24, 0.24):
            cyl(f"ValveBolt_{dx:+.2f}_{dz:+.2f}",
                (-0.28 + dx, 0.55, 3.30 + dz), 0.03, 0.05, STEEL, axis="Y")
    # valve rod down the left side + hand lever (projects left) + grip
    cyl("ValveRod", (-0.62, 0.38, 2.20), 0.025, 1.90, STEEL)
    cyl("HandLever", (-1.04, 0.38, 3.15), 0.035, 0.98, STEEL, axis="X")
    cyl("HandLeverGrip", (-1.50, 0.38, 3.15), 0.05, 0.15, IRON, axis="X")

    # --- low handwheel (left) ---
    torus("Handwheel", (-1.10, 0.30, 1.15), 0.22, 0.03, IRON, plane="XZ")
    cyl("HandwheelAxle", (-1.10, 0.30, 1.15), 0.04, 0.50, STEEL, axis="Y")

    # --- Wilson self-acting gear, simplified (pattern evidence, flagged) ---
    cyl("WilsonSmallCylinder", (0.30, 0, 4.30), 0.11, 0.35, IRON_MID)
    cyl("MotionRod", (0.62, -0.15, 2.30), 0.02, 2.00, STEEL)

    # --- TUP (one object): die + block + piston rod + blank plate ---
    # Shipped at mid-stroke: die bottom = REST_DIE_Z + MID = 1.29 m.
    die_z0 = REST_DIE_Z + MID
    parts = [
        box("TupDie", (0, 0, die_z0 + TUP_DIE_H / 2.0),
            (0.50, 0.50, TUP_DIE_H), ANVIL_MAT),
        box("TupBlock", (0, 0, die_z0 + TUP_DIE_H + TUP_BLOCK_H / 2.0),
            (TUP_W, TUP_DEPTH, TUP_BLOCK_H), IRON),
        cyl("TupRod", (0, 0, die_z0 + TUP_DIE_H + TUP_BLOCK_H + 1.95 / 2.0),
            ROD_R, 1.95, STEEL),
        box("TupPlate_Blank", (0, TUP_DEPTH / 2.0 + 0.01,
                              die_z0 + TUP_DIE_H + TUP_BLOCK_H / 2.0),
            (0.40, 0.02, 0.22), STEEL),
    ]
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    tup = bpy.context.active_object
    tup.name = "Tup"
    # Origin at base centre so animators move it in Z only:
    # rest = location.z -0.65, shipped mid-stroke = 0, full raise = +0.65.
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    tup.location = (0, 0, 0)
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(location=False, rotation=True,
                                           scale=True)
    return tup


# ---------------------------------------------------------------- render
def look_at(cam, loc, target):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render_all(tup):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 960
    sc.render.resolution_y = 960
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new("GreyWorld")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.82, 0.82, 0.82, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    sun = bpy.data.lights.new("Sun", "SUN")
    sun.energy = 3.0
    so = bpy.data.objects.new("Sun", sun)
    sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))

    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    cam.name = "RenderCam"
    cam.data.lens = 50
    sc.camera = cam

    views = [
        ("front", (0, -7.5, 2.6)),
        ("side", (7.5, 0, 2.6)),
        ("three-quarter", (5.5, -5.5, 3.4)),
    ]
    for name, loc in views:
        look_at(cam, loc, (0, 0, 2.5))
        sc.render.filepath = str(RENDERS / f"{name}.png")
        bpy.ops.render.render(write_still=True)
    # Tup raised: shipped mid-stroke +0.65 m = full raise (rest + 1.30 m).
    tup.location.z = MID
    look_at(cam, (0, -7.5, 2.6), (0, 0, 2.5))
    sc.render.filepath = str(RENDERS / "tup-raised.png")
    bpy.ops.render.render(write_still=True)
    tup.location.z = 0.0


def stats():
    n_obj, tris = 0, 0
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and o.name != "GroundPlane":
            n_obj += 1
            mesh = o.data
            tris += sum(max(0, len(p.vertices) - 2) for p in mesh.polygons)
    return n_obj, tris


def main():
    tup = build()
    render_all(tup)
    blend = str(OUT / "hp-working-machine-exhibit.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=str(OUT / "hp-working-machine-exhibit.glb"),
        export_format="GLB", export_apply=True)
    n_obj, tris = stats()
    print(f"OBJECTS(mesh, excl ground): {n_obj}  TRIANGLES: {tris}")
    print(f"TUP: rest z=-0.65, shipped z=0 (die bottom 1.29 m), "
          f"raised z=+0.65 (die bottom 1.94 m), travel {TRAVEL} m")
    print(f"BLEND: {blend}")


main()
