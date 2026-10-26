#!/usr/bin/env python3
"""
build_sy_fountain_basin.py — one of the pair of Great Fountain basins
(plan key "MM — Basins of large fountains") from the Sydenham grounds,
for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 15; CP042).

Re-runnable: ~/workspace/tools/blender/blender -b --python build_sy_fountain_basin.py
Outputs sy-fountain-basin.blend, sy-fountain-basin.glb and renders/.

The basin is built as a radial sweep around the medallion centre:
the water outline R(theta) is the max of a central scalloped ellipse
(the medallion) and two rectangular arms (west/east), exactly the
plan-form the 1856 guide foldout draws. The rim, apron, inner wall
and floor are rings at radial offsets from that outline. The water
surface is a separate object (WaterDisc) so a scene can hide it;
the low centre plinth is a separate object (CentrePlinth) and is
INFERRED — no photograph resolves the submerged centre.

Dimensions are grouped below by evidence status. See NOTES.md.
"""

import bpy
import math
import os
from mathutils import Vector

# ----------------------------------------------------------------------------
# PLAN-MEASURED (outline shape + proportions, 1856 guide foldout plan,
# refs/plan-1856-guide-palace-and-park.jpg, keyed "MM"; corroborated by
# the Routledge 1854 foldout). Absolute size from the 1862 grounds map
# (refs/plan-1862-grounds-map.jpg) ratioed against the palace length
# 1,608 ft = 490.1 m (Phillips 1854 / 1856 guide, agreed figure).
# The 1856 foldout's own palace-ratio gives a basin ~1.8x larger; the
# foldout is a pictorial key plan and is NOT trusted for absolute size
# (see NOTES.md "The scale conflict").
# ----------------------------------------------------------------------------
BASIN_LENGTH   = 138.0   # m, water outline overall E-W (1862 map: 160/567 x 490.1)
BASIN_DEPTH    = 79.0    # m, water outline overall N-S at the medallion
MEDALLION_AX   = 28.5    # m, medallion ellipse semi-axis E-W (57 m across)
MEDALLION_BX   = 39.5    # m, medallion ellipse semi-axis N-S (79 m across)
ARM_HALF_WIDTH = 16.0    # m, half-width (N-S) of the E-W arms
ARM_INNER_X    = 18.0    # m, arms leave the medallion zone beyond |x| > 18
ARM_END_X      = BASIN_LENGTH / 2.0   # 69 m, arm end (east: flat, at the central walk)
WEST_CAP_X     = -(ARM_END_X - ARM_HALF_WIDTH)  # west arm ends in a rounded scalloped
                                                # terminus (plan), centre of its cap circle
SCALLOPS       = 14      # lobes around the medallion (counted on both plans)
SCALLOP_AMP    = 0.042   # radial amplitude of the lobes (fraction of local radius)

# ----------------------------------------------------------------------------
# PHOTO-ESTIMATED (verticals, from refs/photo-italian-garden-fountains-
# album.jpg and refs/photo-great-fountains-playing-1886.jpg: the rim
# reads as a low stone kerb, coping about knee height above the walk,
# water a few inches below the coping). No dimensioned source exists.
# ----------------------------------------------------------------------------
COPING_TOP_Z   = 0.86    # m above surrounding ground (z = 0)
APRON_TOP_Z    = 0.48    # m, the raised surround walk inside the outer edge
APRON_WIDTH    = 4.3     # m, surround band outside the water outline (plan band, photo-checked)
WATERLINE_Z    = 0.55    # m, still water level (0.31 m below coping top)

# ----------------------------------------------------------------------------
# INFERRED / GUESSED (flagged in NOTES.md)
# ----------------------------------------------------------------------------
FLOOR_Z        = -1.05   # m, basin floor — unseen in every source; a working depth
PLINTH_R       = 5.5     # m, centre nozzle plinth radius (submerged; inferred)
PLINTH_TOP_Z   = 0.40    # m, plinth top, just below the waterline
BOSS_R         = 1.8     # m, central nozzle boss radius (inferred)
BOSS_TOP_Z     = 0.66    # m, boss top, just above the waterline (jet origin)

N_THETA        = 1200    # radial samples around the outline

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------
# Outline
# ----------------------------------------------------------------------------
def ray_ellipse(theta, a, b):
    c, s = math.cos(theta), math.sin(theta)
    return 1.0 / math.sqrt((c / a) ** 2 + (s / b) ** 2)


def ray_rect(theta, x0, x1, half_w):
    """Distance from origin to an axis-aligned rectangle along the ray, or 0."""
    dx, dy = math.cos(theta), math.sin(theta)
    tmin, tmax = 0.0, float("inf")
    for o, d, lo, hi in ((0.0, dx, x0, x1), (0.0, dy, -half_w, half_w)):
        if abs(d) < 1e-9:
            if o < lo or o > hi:
                return 0.0
        else:
            t1 = (lo - o) / d
            t2 = (hi - o) / d
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return 0.0
    return tmax if tmax > 0 else 0.0


def ray_circle(theta, cx, cy, r):
    """Distance from origin to a circle along the ray (far intersection), or 0."""
    dx, dy = math.cos(theta), math.sin(theta)
    ox, oy = -cx, -cy
    b = ox * dx + oy * dy
    c = ox * ox + oy * oy - r * r
    disc = b * b - c
    if disc < 0:
        return 0.0
    t = -b + math.sqrt(disc)
    return t if t > 0 else 0.0


def water_radius(theta):
    r_e = ray_ellipse(theta, MEDALLION_AX, MEDALLION_BX)
    r_w = ray_rect(theta, WEST_CAP_X, -ARM_INNER_X, ARM_HALF_WIDTH)
    r_cap = ray_circle(theta, WEST_CAP_X, 0.0, ARM_HALF_WIDTH)
    r_a = ray_rect(theta, ARM_INNER_X, ARM_END_X, ARM_HALF_WIDTH)
    r0 = max(r_e, r_w, r_cap, r_a)
    # Scallops live on the medallion; fade them out where an arm dominates.
    w = (r_e / r0) ** 2 if r0 > 0 else 0.0
    # Phase: a lobe peak falls due south (theta = -pi/2), as both plans draw
    # a cusp at the medallion's southernmost point.
    lobe = math.cos(SCALLOPS * (theta + math.pi / 2.0))
    return r0 * (1.0 + SCALLOP_AMP * lobe * w)


def outline_points():
    pts = []
    for i in range(N_THETA):
        th = 2.0 * math.pi * i / N_THETA
        r = water_radius(th)
        pts.append((r * math.cos(th), r * math.sin(th), th, r))
    return pts


# ----------------------------------------------------------------------------
# Mesh helpers
# ----------------------------------------------------------------------------
def ring_vertices(pts, d, z):
    """Outline offset radially by d (star-shaped outline: radial offset is a
    good approximation of the true normal offset at these proportions)."""
    return [( (r + d) * math.cos(th), (r + d) * math.sin(th), z )
            for (_, _, th, r) in pts]


def build_basin(pts, mat_stone, mat_inner):
    # (radial offset from water outline, z, material) — swept top to bottom
    rings = [
        ( APRON_WIDTH, -0.30, mat_stone),   # apron outer skirt (below ground)
        ( APRON_WIDTH,  APRON_TOP_Z - 0.08, mat_stone),  # apron outer edge
        ( 0.80,         APRON_TOP_Z, mat_stone),          # apron inner edge
        ( 0.55,         0.76, mat_stone),                 # coping outer face
        ( 0.12,         COPING_TOP_Z, mat_stone),         # coping top, outer
        (-0.28,         COPING_TOP_Z - 0.02, mat_stone), # coping top, inner roll
        (-0.30,         0.30, mat_inner),                 # inner wall
        (-0.30,         FLOOR_Z, mat_inner),              # inner wall foot
    ]
    verts = []
    for d, z, _ in rings:
        verts.extend(ring_vertices(pts, d, z))
    faces = []
    face_mats = []
    n = N_THETA
    for band in range(len(rings) - 1):
        mi = rings[band][2]
        for i in range(n):
            j = (i + 1) % n
            a = band * n + i
            b = band * n + j
            c = (band + 1) * n + j
            dd = (band + 1) * n + i
            faces.append((a, b, c, dd))
            face_mats.append(mi)
    # Floor fan from the last ring to the centre
    centre_idx = len(verts)
    verts.append((0.0, 0.0, FLOOR_Z))
    base = (len(rings) - 1) * n
    for i in range(n):
        j = (i + 1) % n
        faces.append((base + i, centre_idx, base + j))
        face_mats.append(mat_inner)
    mesh = bpy.data.meshes.new("BasinMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(bpy.data.materials["Stone"])
    mesh.materials.append(bpy.data.materials["BasinInner"])
    for poly, mi in zip(mesh.polygons, face_mats):
        poly.material_index = mi
        poly.use_smooth = False
    mesh.update()
    obj = bpy.data.objects.new("Basin", mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def build_fan_disc(name, z, radius_fn, mat_name):
    verts = [(0.0, 0.0, z)]
    faces = []
    for i in range(N_THETA):
        th = 2.0 * math.pi * i / N_THETA
        r = radius_fn(th)
        verts.append((r * math.cos(th), r * math.sin(th), z))
    for i in range(N_THETA):
        j = (i + 1) % N_THETA
        faces.append((0, i + 1, j + 1))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(bpy.data.materials[mat_name])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def build_cylinder(name, radius, z0, z1, mat_name, segments=72):
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments, radius=radius,
                                        depth=z1 - z0, location=(0, 0, (z0 + z1) / 2.0))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(bpy.data.materials[mat_name])
    return obj


# ----------------------------------------------------------------------------
# Scene setup
# ----------------------------------------------------------------------------
def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        pass  # factory-empty is already clean


def add_camera(name, location, look_at, ortho=None, lens=35.0):
    cam_data = bpy.data.cameras.new(name)
    if ortho:
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = ortho
    else:
        cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = location
    direction = Vector(look_at) - Vector(location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return cam


def build():
    reset_scene()
    make_material("Stone", (0.66, 0.64, 0.59), 0.95)       # pale stone / lead-toned kerb
    make_material("BasinInner", (0.13, 0.15, 0.16), 0.65)  # dark underwater read
    make_material("Water", (0.08, 0.14, 0.16), 0.07)       # still water disc
    make_material("Ground", (0.5, 0.5, 0.5), 1.0)

    model = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(model)
    setup = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(setup)

    pts = outline_points()
    basin = build_basin(pts, 0, 1)
    water = build_fan_disc("WaterDisc", WATERLINE_Z,
                           lambda th: water_radius(th) - 0.05, "Water")
    plinth = build_cylinder("CentrePlinth", PLINTH_R, FLOOR_Z, PLINTH_TOP_Z, "Stone")
    boss = build_cylinder("CentreBoss", BOSS_R, PLINTH_TOP_Z, BOSS_TOP_Z, "Stone")
    for o in (basin, water, plinth, boss):
        for c in list(o.users_collection):
            c.objects.unlink(o)
        model.objects.link(o)

    # Render setup: ground, sun, cameras (not exported)
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, -0.31))
    ground = bpy.context.active_object
    ground.name = "GroundPlane"
    ground.data.materials.append(bpy.data.materials["Ground"])
    for c in list(ground.users_collection):
        c.objects.unlink(ground)
    setup.objects.link(ground)

    sun_data = bpy.data.lights.new("Sun", 'SUN')
    sun_data.energy = 3.0
    sun_data.angle = 0.3
    sun = bpy.data.objects.new("Sun", sun_data)
    setup.objects.link(sun)
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-35))

    world = bpy.data.worlds.new("W")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

    cams = {
        "front":        add_camera("CamFront", (0, -205, 12), (0, 0, 0), ortho=170),
        "side":         add_camera("CamSide", (-205, 0, 12), (0, 0, 0), ortho=110),
        "three-quarter": add_camera("CamTQ", (-128, -128, 82), (0, 0, 0), lens=32),
    }
    for c in cams.values():
        for col in list(c.users_collection):
            col.objects.unlink(c)
        setup.objects.link(c)

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
    print(f"SY-FOUNTAIN-BASIN triangles (Model): {tris}")
    assert tris < 50000, "over the 50k prop budget"

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "sy-fountain-basin.blend"))

    # GLB: Model collection only
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in model.objects:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, "sy-fountain-basin.glb"),
                              export_format='GLB', use_selection=True, export_apply=True)

    for view, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT_DIR, "renders", view + ".png")
        bpy.ops.render.render(write_still=True)
        print(f"SY-FOUNTAIN-BASIN rendered {view}")


if __name__ == "__main__":
    build()
