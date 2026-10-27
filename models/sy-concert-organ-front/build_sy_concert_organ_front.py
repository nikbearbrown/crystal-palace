# Build script — sy-concert-organ-front
# Pipe front of the great concert organ of the Sydenham Crystal
# Palace central transept (Gray & Davison, built for the first
# Handel Festival, June 1857). PIPE FRONT + CASE FRONT ONLY:
# no console, no mechanism, no interior. Re-runnable:
#   blender -b -noaudio --python build_sy_concert_organ_front.py
#
# Evidence (see refs/REFERENCES.md and NOTES.md):
#   - Lead 0057: albumen stereo photograph, c.1860-c.1880
#     (Rijksmuseum RP-F-2012-96-339) — the front in the transept.
#   - Lead 0595: Negretti & Zambra photograph of a Handel
#     Festival (halftone, "The Queen's Empire") — the front read
#     in detail; arrangement identical to 0057.
#   - The Engineer, 2 June 1882, "The Great Organ at the Crystal
#     Palace": the instrument "stands on a stout platform or
#     floor, 40ft. wide by about 25ft. deep"; "The space occupied
#     by the instrument is 40ft. wide by 24ft. deep"; largest
#     pipe a wooden pipe 2ft square and 32ft long (pedal, internal
#     — NOT a front pipe). Section plate p.400.
#
# Dimensions are grouped by evidence status in NOTES.md.
# All sizes in metres.

import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "sy-concert-organ-front"

# ---------------------------------------------------------------------------
# Dimensions
#
# PRINTED (The Engineer 1882): overall width 40 ft = 12.192 m.
W = 12.19
# MEASURED from lead 0595 (visual grounding, see NOTES.md):
#   front height / width = 0.668  ->  H = 8.14 m (+-10%)
H = 8.15
# Vertical zones as fractions of the photographed front, applied
# to H (metres):
BASE_H = 2.55        # panelled lower case (medallion panels)
IMPOST_H = 0.60      # decorated band with oval cartouches
PIPE_Z = BASE_H + IMPOST_H          # 3.15 pipe sill level
TOWER_TOP = 7.80     # top of tower pipes
CAP_TOP = H                         # top of tower caps/crenellation
# Case depth: NOMINAL front-module depth only (flagged in NOTES).
# The instrument itself was 24 ft deep (Engineer) — not modelled.
CASE_BACK_Y = 0.45
FLAT_Y = -0.45       # plane of the flats' pipe centres
# Tower centres (measured fractions of W, symmetrised):
TOWER_OUTER_X = 4.35
TOWER_INNER_X = 1.90
TOWER_PIPE_R = 0.50  # arc radius of the tower pipe cluster
TOWER_DRUM_R = 0.63

# Post-build Y shift so the footprint (tower drum front -1.08 to
# case back +0.45) is centred on the origin.
YOFF = 0.32


def clean_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def make_collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def mat_solid(name, rgb, roughness, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def box(coll, name, cx, cy, cz, sx, sy, sz, mat):
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (sx / 2, sy / 2, sz / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False,
                                   scale=True)
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob


def cyl(coll, name, cx, cy, cz, r, h, mat, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r,
                                        depth=h,
                                        location=(cx, cy, cz))
    ob = bpy.context.active_object
    ob.name = name
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob


def oval(coll, name, cx, cy, cz, rw, rh, depth, mat):
    """Flattened, vertically stretched cylinder = oval plaque,
    built by baking the scale into the vertices."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=1.0,
                                        depth=1.0,
                                        location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = name
    for v in ob.data.vertices:
        v.co.x *= rw
        v.co.y *= rh
        v.co.z *= depth
    ob.location = (cx, cy, cz)
    ob.rotation_euler = (math.radians(90), 0, 0)
    # rotation turns the cylinder axis to Y; bake it
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True,
                                   scale=False)
    ob.select_set(False)
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob


def pipe(coll, name, x, y, zbase, length, dia, gold, band_mat,
         mouth_mat, bands=False):
    """One front pipe: cylinder body on the sill, dark mouth slot,
    optional dark diaper bands (tower pipes, as read in photos)."""
    r = dia / 2
    cyl(coll, name, x, y, zbase + length / 2, r, length, gold,
        verts=12 if dia >= 0.2 else 8)
    # mouth: small dark slot on the front face, ~0.55 m above sill
    mz = zbase + min(0.55, length * 0.22)
    box(coll, name + "_mouth", x, y - r - 0.004, mz,
        dia * 0.58, 0.012, 0.17, mouth_mat)
    if bands:
        for f in (0.55, 0.82):
            cyl(coll, name + f"_band{int(f*100)}", x, y,
                zbase + length * f, r + 0.006, 0.20, band_mat,
                verts=12)


def build(model, mats):
    wood, wood_light, gold, gilt, band_m, mouth_m, dark = (
        mats["wood"], mats["wood_light"], mats["gold"],
        mats["gilt"], mats["band"], mats["mouth"], mats["dark"])

    front_face = FLAT_Y - 0.10        # base front plane, -0.55
    carcass_cy = (front_face + CASE_BACK_Y) / 2
    carcass_d = CASE_BACK_Y - front_face
    # Upper case: front boards at y=-0.35, BEHIND the flat pipes
    # (pipe centres at FLAT_Y=-0.45 stand proud of the boards).
    upper_cy, upper_d = 0.05, 0.80    # spans y -0.35..+0.45

    # ---- carcass -------------------------------------------------
    box(model, "CarcassBase", 0, carcass_cy, BASE_H / 2,
        W, carcass_d, BASE_H, wood)
    box(model, "CarcassUpper", 0, upper_cy, (PIPE_Z + 7.45) / 2,
        W, upper_d, 7.45 - PIPE_Z, wood)
    # dark backdrop immediately behind the flat pipes
    box(model, "PipeBackdrop", 0, -0.33, (PIPE_Z + 7.9) / 2,
        W - 0.3, 0.04, 7.9 - PIPE_Z, dark)
    # pipe sill rail, full width, slight projection
    box(model, "PipeSill", 0, -0.325, PIPE_Z - 0.05,
        W, 0.55, 0.12, wood_light)
    # top rail / case roof line behind the towers
    box(model, "TopRail", 0, upper_cy, 7.52, W, upper_d, 0.16,
        wood_light)

    # ---- base panels + oval medallions ---------------------------
    panels = ((-5.55, 0.95), (-3.95, 1.45), (-2.30, 1.45),
              (2.30, 1.45), (3.95, 1.45), (5.55, 0.95))
    for i, (px, pw) in enumerate(panels):
        box(model, f"BasePanel{i}", px, front_face - 0.015, 1.28,
            pw, 0.05, 1.95, wood_light)
        mrw = 0.40 if pw > 1.2 else 0.28
        oval(model, f"Medallion{i}", px, front_face - 0.05, 1.32,
             mrw, 0.56, 0.05, gilt)
        oval(model, f"MedallionIn{i}", px, front_face - 0.065, 1.32,
             mrw * 0.68, 0.40, 0.05, wood)

    # ---- console recess (console itself NOT modelled) -----------
    # A near-black panel set INTO the base front (front face 0.06
    # behind the panel faces): reads as the dark opening the
    # detached console stood in front of.
    box(model, "ConsoleRecess", 0, front_face - 0.035, 1.40,
        2.20, 0.03, 2.80, dark)
    # canopy slab over the recess (seen in both photographs)
    box(model, "ConsoleCanopy", 0, -0.60, 2.86,
        2.50, 0.40, 0.10, wood_light)
    box(model, "RecessPanelL", -1.28, front_face - 0.015, 1.28,
        0.30, 0.05, 1.95, wood_light)
    box(model, "RecessPanelR", 1.28, front_face - 0.015, 1.28,
        0.30, 0.05, 1.95, wood_light)

    # ---- impost band + cartouches --------------------------------
    box(model, "ImpostBand", 0, -0.31, BASE_H + IMPOST_H / 2,
        W, 0.50, IMPOST_H, wood)
    cart_xs = (-5.15, -3.12, 0.0, 3.12, 5.15)
    for i, cx in enumerate(cart_xs):
        wdt = 2.10 if i == 2 else 1.50
        oval(model, f"Cartouche{i}", cx, front_face - 0.045,
             BASE_H + IMPOST_H / 2, wdt / 2, 0.21, 0.05, gilt)

    # ---- towers ----------------------------------------------------
    for ti, tx in enumerate((-TOWER_OUTER_X, -TOWER_INNER_X,
                             TOWER_INNER_X, TOWER_OUTER_X)):
        # corbel block carrying the projecting tower drum
        box(model, f"Tower{ti}Corbel", tx, -0.72, PIPE_Z - 0.13,
            1.34, 0.72, 0.30, wood)
        # drum base + top cornice ring (towers are round projections)
        cyl(model, f"Tower{ti}Drum", tx, FLAT_Y, PIPE_Z + 0.14,
            TOWER_DRUM_R, 0.28, wood, verts=20)
        cyl(model, f"Tower{ti}Cornice", tx, FLAT_Y, TOWER_TOP + 0.10,
            TOWER_DRUM_R + 0.02, 0.20, wood_light, verts=20)
        # crenellation: small blocks around the top arc
        for k in range(9):
            a = math.radians(-80 + k * 20)
            bx = tx + (TOWER_DRUM_R + 0.02) * math.sin(a)
            by = FLAT_Y - (TOWER_DRUM_R + 0.02) * math.cos(a)
            box(model, f"Tower{ti}Cren{k}", bx, by, CAP_TOP - 0.075,
                0.13, 0.13, 0.15, wood)
        # 7 pipes on the forward arc, tallest at the centre
        prof = (0.90, 0.965, 1.0, 1.0, 1.0, 0.965, 0.90)
        for k in range(7):
            a = math.radians(-66 + k * 22)
            px = tx + TOWER_PIPE_R * math.sin(a)
            py = FLAT_Y - TOWER_PIPE_R * math.cos(a)
            length = (TOWER_TOP - PIPE_Z) * prof[k]
            dia = 0.30 - 0.012 * abs(k - 3)
            pipe(model, f"Tower{ti}Pipe{k}", px, py, PIPE_Z + 0.26,
                 length - 0.26, dia, gold, band_m, mouth_m,
                 bands=True)

    # ---- flats -----------------------------------------------------
    def flat(name, cx, width, n, dia, len_edge, len_mid, shape,
             rail_extra=0.55):
        for k in range(n):
            f = k / (n - 1) if n > 1 else 0.5
            px = cx - width / 2 + f * width
            if shape == "arch":        # shallow arch, longest centre
                ln = len_edge + (len_mid - len_edge) * math.sin(
                    math.pi * f) ** 0.7
            else:                      # inverted V, longest at edges
                ln = len_mid + (len_edge - len_mid) * abs(2 * f - 1)
            pipe(model, f"{name}Pipe{k}", px, FLAT_Y, PIPE_Z, ln,
                 dia, gold, band_m, mouth_m)
        # horizontal mouth rail across the flat (seen in photos)
        box(model, name + "Rail", cx, FLAT_Y - dia / 2 - 0.03,
            PIPE_Z + 0.62, width + dia, 0.05, 0.09, wood_light)
        # shallow top rail
        topz = PIPE_Z + max(len_edge, len_mid) + 0.10
        box(model, name + "Top", cx, (front_face + 0.28) / 2,
            topz, width + rail_extra, 0.28 - front_face, 0.14,
            wood_light)

    # intermediate flats (between outer and inner towers)
    flat("FlatL", -3.12, 1.20, 9, 0.115, 2.55, 2.80, "arch")
    flat("FlatR", 3.12, 1.20, 9, 0.115, 2.55, 2.80, "arch")
    # centre flat: tops in a shallow inverted V (as photographed)
    flat("FlatC", 0.0, 2.54, 19, 0.105, 3.00, 2.55, "vee")
    # side bays beyond the outer towers
    flat("FlatSL", -5.55, 0.95, 7, 0.10, 2.30, 2.50, "arch",
         rail_extra=0.10)
    flat("FlatSR", 5.55, 0.95, 7, 0.10, 2.30, 2.50, "arch",
         rail_extra=0.10)

    # ---- pediment cluster above the centre flat -------------------
    ped_base = 6.62
    box(model, "PedimentBoard", 0, -0.40, ped_base - 0.07,
        2.30, 0.25, 0.14, wood)
    n_ped = 11
    for k in range(n_ped):
        f = k / (n_ped - 1)
        px = -0.95 + f * 1.90
        ln = 0.55 + 0.85 * math.sin(math.pi * f)
        pipe(model, f"PedimentPipe{k}", px, FLAT_Y, ped_base,
             ln, 0.09, gold, band_m, mouth_m)

    # side cheeks with finials at the case edges
    for sx in (-1, 1):
        box(model, f"Cheek{sx}", sx * (W / 2 - 0.17), upper_cy,
            (PIPE_Z + 7.45) / 2, 0.34, upper_d, 7.45 - PIPE_Z, wood)
        cyl(model, f"Finial{sx}", sx * (W / 2 - 0.17), carcass_cy,
            7.62, 0.07, 0.34, gilt, verts=10)


def main():
    clean_scene()
    model = make_collection("Model")
    setup = make_collection("Setup")

    mats = {
        "wood": mat_solid("CaseWood", (0.145, 0.095, 0.065), 0.82),
        "wood_light": mat_solid("CaseWoodLight", (0.23, 0.155, 0.105), 0.78),
        "gold": mat_solid("FrontPipeGold", (0.78, 0.55, 0.18), 0.42, metallic=0.9),
        "gilt": mat_solid("GiltBronze", (0.55, 0.42, 0.20), 0.45, metallic=0.65),
        "band": mat_solid("PipeDiaperBand", (0.16, 0.09, 0.06), 0.6, metallic=0.2),
        "mouth": mat_solid("PipeMouth", (0.05, 0.04, 0.035), 0.9),
        "dark": mat_solid("CaseDark", (0.045, 0.035, 0.03), 0.95),
    }
    build(model, mats)

    # centre the footprint on the origin (base centre, z = 0)
    for ob in model.objects:
        if ob.type == "MESH":
            for v in ob.data.vertices:
                v.co.y += YOFF
            ob.data.update()

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    # ---- render setup (not exported) ----
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -0.01))
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

    bpy.ops.object.light_add(type="SUN", location=(8, -9, 14))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(52), 0, math.radians(38))
    for c in sun.users_collection:
        c.objects.unlink(sun)
    setup.objects.link(sun)
    bpy.ops.object.light_add(type="AREA", location=(-9, -4, 8))
    fill = bpy.context.active_object
    fill.data.energy = 700
    fill.data.shape = "DISK"
    fill.data.size = 10
    for c in fill.users_collection:
        c.objects.unlink(fill)
    setup.objects.link(fill)

    def look_at(ob, target):
        ob.rotation_euler = (Vector(target) - ob.location).to_track_quat("-Z", "Y").to_euler()

    cams = {}
    for name, loc, tgt in (
            ("Front", (0, -17.5, 4.3), (0, 0, 3.9)),
            ("Side", (17.5, 0, 4.3), (0, 0, 3.9)),
            ("ThreeQuarter", (11.5, -11.5, 7.0), (0, 0, 3.6))):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.active_object
        cam.name = "Cam" + name
        cam.data.lens = 42
        look_at(cam, tgt)
        for c in cam.users_collection:
            c.objects.unlink(cam)
        setup.objects.link(cam)
        cams[name] = cam

    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 768
    scene.render.image_settings.file_format = "PNG"

    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    out_blend = os.path.join(ROOT, SLUG + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print("saved", out_blend)

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

    pts = []
    for ob in model.objects:
        if ob.type == "MESH":
            for c in ob.bound_box:
                pts.append(ob.matrix_world @ Vector(c))
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    print(f"BBOX x {min(xs):.3f}..{max(xs):.3f}  y {min(ys):.3f}..{max(ys):.3f}"
          f"  z {min(zs):.3f}..{max(zs):.3f}")

    for name, cam in cams.items():
        scene.camera = cam
        fn = "three-quarter.png" if name == "ThreeQuarter" else name.lower() + ".png"
        scene.render.filepath = os.path.join(ROOT, "renders", fn)
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath)


if __name__ == "__main__":
    main()
