#!/usr/bin/env python3
"""Build sy-water-tower-massing — Brunel water tower, Sydenham: MASSING STUDY ONLY.

One of the pair of water towers that flanked the Sydenham palace and
fed the great fountains. This is a silhouette / proportions prop for
skyline and backdrop shots (CP042 context, CP062, CP064) — NOT a
reconstruction. Brunel's tower drawings are not in the collection
(round-2 review, GAPS-FOUND S51), so no detail is claimed.

Form read from the photographs (see NOTES.md / refs/REFERENCES.md):
a cylindrical open iron frame of 12 columns (Historic England, via
round-2 review) ringed with horizontal bands and light diagonal
bracing, a projecting gallery ring near the top, an open arcaded
lantern stage, and a steep ribbed conical cap with a small finial.

Vertical proportions measured on the two best photographs
(S51-03 Rijksmuseum 1878-90; S51-01 Delamotte c.1854-56) agree:
shaft 67 %, gallery band 5.5 %, lantern 10 %, cap + finial 18 %.

Height: sources conflict — 280 ft (ILN 1941), 282 ft, 284 ft,
86 m (Historic England). Adopted: 86.0 m overall, ground at the
tower's own base to the tip of the finial. See NOTES.md.

Re-runnable: blender --background --python build_sy_water_tower_massing.py
"""
import math
import os

import bpy
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Dimensions (metres). Grouped by evidence status.
# ---------------------------------------------------------------------------
# ADOPTED from sources (conflict documented in NOTES.md):
TOTAL_H = 86.0        # 280 ft (ILN 1941) / 282 ft / 284 ft / 86 m (Hist. Eng.)
N_COLS = 12           # "12 cast-iron columns on a concrete ring" (Hist. Eng.)

# PHOTO-MEASURED proportions (fractions of TOTAL_H; two photographs agree):
SHAFT_TOP = 57.7      # 67.1 % — top of cylindrical frame / gallery underside
GALLERY_TOP = 62.4    # +5.5 % — projecting gallery ring band
LANTERN_TOP = 71.0    # +10.0 % — open arcaded stage; cap eaves sit here
CAP_TOP = TOTAL_H     # +17.9 % — conical cap + finial

# PHOTO-DERIVED widths (height/diameter ratios measured on S51-03 and
# S51-01: H/D between 5.0 and 6.0; adopted 5.4 — estimate, NOT surveyed):
SHAFT_D = 16.0        # cylindrical frame diameter
GALLERY_D = 18.6      # gallery ring projects ~1.3 m each side
LANTERN_D = 17.6      # lantern stage, between gallery and cap eaves
CAP_EAVE_D = 21.6     # cap eaves overhang: ~1.35x shaft (measured on S51-03)
PLINTH_D = 17.6       # concrete ring plinth (kind sourced, size estimated)
PLINTH_H = 1.2

# INFERRED (inside the frame; barely affects the silhouette):
TANK_D = 14.6         # water tank cylinder, hidden inside the lattice
TANK_Z0 = 40.0        # tank placement is a reading of the denser-reading
TANK_Z1 = 56.0        # upper shaft in the photographs — NOT dimensioned

# MODELLING choices (massing language, not detail claims):
COL_D = 0.45          # column tube diameter
STOREYS = 8           # ring levels on the shaft (photos show ~8 bands)
BRACE_T = 0.14        # diagonal brace bar thickness
LANTERN_COL_D = 0.35


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(name, rgb, roughness=0.85):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def link_only(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def cylinder(name, radius, z0, z1, mat, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=z1 - z0,
        location=(0, 0, (z0 + z1) / 2))
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    return obj


def torus_ring(name, radius, z, minor, mat, major_segments=32):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=major_segments, minor_segments=8,
        major_radius=radius, minor_radius=minor, location=(0, 0, z))
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    return obj


def beam_between(name, p1, p2, thickness, mat):
    """A thin box stretched between two points (for diagonal bracing)."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    direction = p2 - p1
    length = direction.length
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=mid)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (thickness, thickness, length)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(
        direction.normalized())
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def lathe(name, profile, mat, segments=28):
    """Surface of revolution from an (r, z) profile, bottom to top."""
    verts, faces = [], []
    n = len(profile)
    for r, z in profile:
        for i in range(segments):
            a = 2 * math.pi * i / segments
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for j in range(n - 1):
        for i in range(segments):
            a = j * segments + i
            b = j * segments + (i + 1) % segments
            c = (j + 1) * segments + (i + 1) % segments
            d = (j + 1) * segments + i
            faces.append((a, b, c, d))
    # cap the top with a fan if the profile ends off-axis
    if profile[-1][0] > 1e-6:
        centre = len(verts)
        verts.append((0, 0, profile[-1][1]))
        base = (n - 1) * segments
        for i in range(segments):
            faces.append((base + i, base + (i + 1) % segments, centre))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj


def join_objects(name, objects, mat):
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = name
    return joined


def add_camera(name, location, target, ortho=None, lens=35):
    data = bpy.data.cameras.new(name)
    if ortho:
        data.type = 'ORTHO'
        data.ortho_scale = ortho
    data.lens = lens
    data.clip_start = 0.5
    data.clip_end = 2000
    cam = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = location
    direction = Vector(target) - Vector(location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return cam


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    reset_scene()
    iron = make_material("IronPaint", (0.40, 0.385, 0.365), 0.8)
    iron_dark = make_material("TankIron", (0.23, 0.22, 0.21), 0.9)
    cap_mat = make_material("CapRoof", (0.34, 0.325, 0.31), 0.85)
    concrete = make_material("Concrete", (0.60, 0.585, 0.56), 0.95)
    ground_mat = make_material("Ground", (0.5, 0.5, 0.5), 1.0)

    model = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(model)
    setup = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(setup)

    r_shaft = SHAFT_D / 2

    # Plinth — concrete ring (kind from Historic England; size estimated)
    plinth = cylinder("Plinth", PLINTH_D / 2, 0.0, PLINTH_H, concrete)

    # Shaft — 12 columns
    columns = []
    for i in range(N_COLS):
        a = 2 * math.pi * i / N_COLS
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=10, radius=COL_D / 2, depth=SHAFT_TOP - PLINTH_H,
            location=(r_shaft * math.cos(a), r_shaft * math.sin(a),
                      (PLINTH_H + SHAFT_TOP) / 2))
        col = bpy.context.active_object
        col.data.materials.append(iron)
        columns.append(col)
    shaft_columns = join_objects("ShaftColumns", columns, iron)

    # Shaft — horizontal ring bands at each storey level
    rings = []
    for s in range(STOREYS + 1):
        z = PLINTH_H + s * (SHAFT_TOP - PLINTH_H) / STOREYS
        rings.append(torus_ring("Ring", r_shaft, z, 0.20, iron))
    shaft_rings = join_objects("ShaftRings", rings, iron)

    # Shaft — diagonal bracing, one diagonal per bay per storey,
    # direction alternating by storey (massing suggestion of lattice)
    braces = []
    for s in range(STOREYS):
        z0 = PLINTH_H + s * (SHAFT_TOP - PLINTH_H) / STOREYS
        z1 = PLINTH_H + (s + 1) * (SHAFT_TOP - PLINTH_H) / STOREYS
        for i in range(N_COLS):
            a0 = 2 * math.pi * i / N_COLS
            a1 = 2 * math.pi * (i + 1) / N_COLS
            p_a = (r_shaft * math.cos(a0), r_shaft * math.sin(a0), z0)
            p_b = (r_shaft * math.cos(a1), r_shaft * math.sin(a1), z1)
            p_c = (r_shaft * math.cos(a0), r_shaft * math.sin(a0), z1)
            p_d = (r_shaft * math.cos(a1), r_shaft * math.sin(a1), z0)
            p1, p2 = (p_a, p_b) if (s % 2 == 0) else (p_c, p_d)
            braces.append(beam_between("Brace", p1, p2, BRACE_T, iron))
    shaft_bracing = join_objects("ShaftBracing", braces, iron)

    # Tank — INFERRED: inside the upper shaft, under the gallery
    tank = cylinder("Tank_INFERRED", TANK_D / 2, TANK_Z0, TANK_Z1,
                    iron_dark, verts=28)

    # Gallery — projecting ring band with a lip at its top
    gallery = cylinder("Gallery", GALLERY_D / 2, SHAFT_TOP, GALLERY_TOP - 1.0,
                       iron, verts=28)
    gallery_lip = cylinder("GalleryLip", GALLERY_D / 2 + 0.5,
                           GALLERY_TOP - 1.0, GALLERY_TOP, iron, verts=28)

    # Lantern — open stage: 12 short posts + rings, NO wall
    posts = []
    r_lant = LANTERN_D / 2
    for i in range(N_COLS):
        a = 2 * math.pi * i / N_COLS
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=LANTERN_COL_D / 2, depth=LANTERN_TOP - GALLERY_TOP,
            location=(r_lant * math.cos(a), r_lant * math.sin(a),
                      (GALLERY_TOP + LANTERN_TOP) / 2))
        post = bpy.context.active_object
        post.data.materials.append(iron)
        posts.append(post)
    lantern_posts = join_objects("LanternPosts", posts, iron)
    lantern_rings = join_objects("LanternRings", [
        torus_ring("LRingB", r_lant, GALLERY_TOP + 0.25, 0.22, iron),
        torus_ring("LRingT", r_lant, LANTERN_TOP - 0.25, 0.22, iron),
    ], iron)

    # Cap — steep cone with a slightly flared, curved profile + ribs read
    # as a smooth massing cone; finial profile included in the lathe.
    eave_r = CAP_EAVE_D / 2
    cap_profile = [
        (eave_r, LANTERN_TOP),
        (eave_r * 0.94, LANTERN_TOP + 2.2),
        (eave_r * 0.80, LANTERN_TOP + 5.2),
        (eave_r * 0.60, LANTERN_TOP + 8.2),
        (eave_r * 0.38, LANTERN_TOP + 10.8),
        (eave_r * 0.18, LANTERN_TOP + 12.6),
        (0.55, LANTERN_TOP + 13.6),   # neck under finial
        (0.85, LANTERN_TOP + 14.1),   # finial knob
        (0.30, LANTERN_TOP + 14.6),
        (0.0, CAP_TOP),              # tip at the adopted total height
    ]
    cap = lathe("Cap", cap_profile, cap_mat, segments=28)

    model_objects = [plinth, shaft_columns, shaft_rings, shaft_bracing,
                     tank, gallery, gallery_lip, lantern_posts,
                     lantern_rings, cap]
    for o in model_objects:
        link_only(o, model)

    # --- Render setup (not exported) ---
    bpy.ops.mesh.primitive_plane_add(size=900, location=(0, 0, -0.05))
    ground = bpy.context.active_object
    ground.name = "GroundPlane"
    ground.data.materials.append(ground_mat)
    link_only(ground, setup)

    sun_data = bpy.data.lights.new("Sun", 'SUN')
    sun_data.energy = 3.0
    sun_data.angle = 0.3
    sun = bpy.data.objects.new("Sun", sun_data)
    setup.objects.link(sun)
    sun.rotation_euler = (math.radians(50), math.radians(10),
                          math.radians(-35))

    world = bpy.data.worlds.new("W")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = \
        (0.55, 0.55, 0.55, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

    # NOTE: Blender's ortho_scale is the frame WIDTH; at 960x720 the
    # visible height is ortho_scale * 720/960 = 0.75x. The tower is
    # 86 m tall, so ortho must be >= ~122 to frame it whole — first
    # pass used 102 (76.5 m visible) and cropped cap and base.
    centre = (0, 0, 43)
    cams = {
        "front": add_camera("CamFront", (0, -280, 43), centre, ortho=128),
        "side": add_camera("CamSide", (-280, 0, 43), centre, ortho=128),
        "three-quarter": add_camera("CamTQ", (-105, -105, 62), centre,
                                    lens=32),
    }
    for c in cams.values():
        link_only(c, setup)

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'

    # Verify triangle count on evaluated geometry
    deps = bpy.context.evaluated_depsgraph_get()
    tris = 0
    for o in model.objects:
        ev = o.evaluated_get(deps)
        m = ev.to_mesh()
        m.calc_loop_triangles()
        tris += len(m.loop_triangles)
        ev.to_mesh_clear()
    print(f"SY-TOWER-STUDY triangles (Model): {tris}")
    assert tris < 50000, "over the 50k prop budget"

    # Verify the overall height lands on the adopted figure
    max_z = max((o.matrix_world @ Vector(c)).z
                for o in model.objects for c in o.bound_box)
    min_z = min((o.matrix_world @ Vector(c)).z
                for o in model.objects for c in o.bound_box)
    print(f"SY-TOWER-STUDY bbox z: {min_z:.2f} .. {max_z:.2f} "
          f"(target 0 .. {TOTAL_H})")

    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.join(OUT_DIR, "sy-water-tower-massing.blend"))

    # GLB: Model collection only
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in model.objects:
        o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(OUT_DIR, "sy-water-tower-massing.glb"),
        export_format='GLB', use_selection=True, export_apply=True)

    for view, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT_DIR, "renders",
                                             view + ".png")
        bpy.ops.render.render(write_still=True)
        print(f"SY-TOWER-STUDY rendered {view}")


if __name__ == "__main__":
    build()
