# Build script — sy-classical-cast-base
# The standard dark cast pedestal of the Sydenham classical courts
# (Greek and Roman Sculpture Court), 1854. Re-runnable:
#   blender -b -noaudio --python build_sy_classical_cast_base.py
#
# Evidence (see refs/REFERENCES.md and NOTES.md):
#   - Delamotte album photograph "Greek and Roman Sculpture Court"
#     (MET DP323102, CC0) — the type in rows across the court.
#   - Stereo view "101. Statues in the Greek and Roman sculpture
#     court" (Rijksmuseum RP-F-2012-96-327, CC0) — eye-level profile:
#     plain dark square die, plinth-step + cove base moulding,
#     NO cap moulding; the light slab on top belongs to each cast.
#
# Dimensions are grouped by evidence status. All sizes in metres.

import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "sy-classical-cast-base"

# ---------------------------------------------------------------------------
# Dimensions
#
# MEASURED from the photographs (visual grounding, see NOTES.md):
#   figure pedestal height / statue height  = 0.468 (Aristides view)
#   bust pedestal height / bust height      = 1.48  (Minerva view)
#   base moulding (step + cove)             ~ 0.15-0.20 of total height
# DERIVED (adopted; life-size casts ~1.95 m standing, ~0.88 m bust):
FIG_HEIGHT = 0.91      # figure pedestal, total  (~3 ft; +-0.06)
FIG_DIE_W = 0.61       # figure pedestal die width (~2 ft; +-0.05)
BUST_HEIGHT = 1.30     # bust pedestal, total    (+-0.08)
BUST_DIE_W = 0.46      # bust pedestal die width (~1 ft 6 in; +-0.06)
# PROFILE (common to both, from the photographs):
BASE_H = 0.15          # height of the step + cove base moulding
BASE_PROJ = 0.038      # projection of the foot step beyond the die face
FOOT_H = 0.055         # height of the vertical foot step within the base

# Placement: the pair's footprint is centred on the origin (like the
# Egyptian column pair prop). Foot widths: fig 0.686, bust 0.536 —
# outer edges land at x = -0.978 and +0.978.
FIG_X = -0.635
BUST_X = 0.710

# Cove profile: (z fraction of the cove zone, inset from foot half-width
# as a fraction of BASE_PROJ). Smooth concave sweep, fillet at the top.
COVE_STEPS = (
    (0.00, 1.000),
    (0.13, 0.985),
    (0.32, 0.900),
    (0.52, 0.740),
    (0.72, 0.500),
    (0.88, 0.240),
    (1.00, 0.000),
)


def clean_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras,
                 bpy.data.lights, bpy.data.materials):
        pass  # keep datablocks simple; new scene is nearly empty anyway


def make_collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def mat_solid(name, rgb, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return m


def loft_mesh(name, cx, rings):
    """rings: list of (z, half_width). Builds a square-section loft
    centred on (cx, 0), capped top and bottom, world-space geometry."""
    verts = []
    for z, hw in rings:
        verts += [(cx - hw, -hw, z), (cx + hw, -hw, z),
                  (cx + hw, hw, z), (cx - hw, hw, z)]
    faces = []
    n = len(rings)
    for i in range(n - 1):
        a = i * 4
        b = (i + 1) * 4
        for s in range(4):
            s2 = (s + 1) % 4
            faces.append((a + s, b + s, b + s2, a + s2))
    # bottom cap (faces down) and top cap (faces up)
    faces.append((3, 2, 1, 0))
    t = (n - 1) * 4
    faces.append((t + 0, t + 1, t + 2, t + 3))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def build_pedestal(coll, mat, cx, height, die_w, tag):
    die_hw = die_w / 2.0
    foot_hw = die_hw + BASE_PROJ
    rings = [(0.0, foot_hw), (FOOT_H, foot_hw)]
    cove_h = BASE_H - FOOT_H
    for fz, fi in COVE_STEPS[1:]:
        rings.append((FOOT_H + fz * cove_h, foot_hw - fi * BASE_PROJ))
    rings.append((height, die_hw))  # die top (the die is part of the loft)
    mesh = loft_mesh(f"Pedestal{tag}", cx, rings)
    ob = bpy.data.objects.new(f"CastBase_{tag}", mesh)
    coll.objects.link(ob)
    ob.data.materials.append(mat)
    # Shade the cove band smooth, keep foot step / die / caps flat.
    # Faces: side quads are ordered ring by ring; the cove occupies the
    # rings from index 1..len-2 transitions. Simpler robust route:
    # smooth faces whose centroid z lies inside the cove zone.
    for poly in mesh.polygons:
        cz = sum(mesh.vertices[v].co.z for v in poly.vertices) / len(poly.vertices)
        if FOOT_H - 0.001 < cz < BASE_H - 0.002 and poly.normal.z < 0.9:
            poly.use_smooth = True
    return ob


def main():
    clean_scene()
    model = make_collection("Model")
    setup = make_collection("RenderSetup")

    # Very dark warm black-brown painted finish. The photographs are
    # black-and-white: they fix the tonal value (near-black) but not
    # the hue, which is unrecorded — see NOTES.md. Satin paint sheen.
    paint = mat_solid("PedestalPaint_Dark", (0.019, 0.015, 0.012), 0.62)

    build_pedestal(model, paint, FIG_X, FIG_HEIGHT, FIG_DIE_W, "Figure")
    build_pedestal(model, paint, BUST_X, BUST_HEIGHT, BUST_DIE_W, "Bust")

    # ---- render setup (not exported) ----
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.01))
    ground = bpy.context.active_object
    ground.name = "Ground"
    for c in ground.users_collection:
        c.objects.unlink(ground)
    setup.objects.link(ground)
    gm = mat_solid("BackdropGrey", (0.55, 0.55, 0.55), 1.0)
    ground.data.materials.append(gm)

    world = bpy.data.worlds["World"]
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    bpy.ops.object.light_add(type="SUN", location=(6, -7, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(55), 0, math.radians(35))
    for c in sun.users_collection:
        c.objects.unlink(sun)
    setup.objects.link(sun)
    bpy.ops.object.light_add(type="AREA", location=(-7, 5, 6))
    fill = bpy.context.active_object
    fill.data.energy = 500
    fill.data.shape = "DISK"
    fill.data.size = 8
    for c in fill.users_collection:
        c.objects.unlink(fill)
    setup.objects.link(fill)

    def look_at(ob, target):
        ob.rotation_euler = (Vector(target) - ob.location).to_track_quat("-Z", "Y").to_euler()

    cams = {}
    for name, loc in (("Front", (0, -4.4, 0.80)), ("Side", (4.4, 0, 0.80)),
                      ("ThreeQuarter", (3.1, -3.1, 1.9))):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.active_object
        cam.name = "Cam" + name
        cam.data.lens = 45
        look_at(cam, (0, 0, 0.55))
        for c in cam.users_collection:
            c.objects.unlink(cam)
        setup.objects.link(cam)
        cams[name] = cam

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 768
    scene.render.image_settings.file_format = "PNG"

    out_blend = os.path.join(ROOT, SLUG + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print("saved", out_blend)

    # GLB: Model collection only
    bpy.ops.object.select_all(action="DESELECT")
    for ob in model.objects:
        ob.select_set(True)
    out_glb = os.path.join(ROOT, SLUG + ".glb")
    bpy.ops.export_scene.gltf(filepath=out_glb, export_format="GLB",
                              use_selection=True, export_apply=True)
    print("exported", out_glb)

    tris = 0
    for ob in model.objects:
        if ob.type == "MESH":
            tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
    print(f"OBJECTS {len(model.objects)} TRIS {tris}")

    # world bbox of the model, for QC against the design dimensions
    xs, ys, zs = [], [], []
    for ob in model.objects:
        if ob.type == "MESH":
            for v in ob.data.vertices:
                xs.append(v.co.x); ys.append(v.co.y); zs.append(v.co.z)
    print(f"BBOX x {min(xs):.3f}..{max(xs):.3f}  y {min(ys):.3f}..{max(ys):.3f}"
          f"  z {min(zs):.3f}..{max(zs):.3f}")

    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(ROOT, "renders", name.lower() + ".png") \
            if name != "ThreeQuarter" else os.path.join(ROOT, "renders", "three-quarter.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath)


if __name__ == "__main__":
    main()
