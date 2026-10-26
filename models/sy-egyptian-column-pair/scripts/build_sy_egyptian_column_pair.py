#!/usr/bin/env python3
"""Build sy-egyptian-column-pair — a pair of the Sydenham Egyptian Court's
Hall of Karnak columns (1854), as drawn in the 1856 guide's captioned
woodcut "Column from Karnak" (p.51) and laid out in its "Ground Plan of
Egyptian Court" (p.47).

Run:  blender -b -P build_sy_egyptian_column_pair.py
Requires textures/ from scripts/make_textures.py (system python3 + PIL).

These are VICTORIAN (Owen Jones / Joseph Bonomi era) reproductions and
interpretations of Egyptian forms, built at Sydenham in 1854 — not
archaeological Egypt. See NOTES.md for the full evidence trail.
"""
import bpy, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEX = os.path.join(ROOT, "textures")
SLUG = "sy-egyptian-column-pair"

# ---------------------------------------------------------------------------
# Dimensions (metres). See NOTES.md for the derivation of every group.
#
# MEASURED on the 1856 guide's "Column from Karnak" woodcut (p.51):
#   total height / shaft base diameter = 5.03 (visual-grounding measure)
# MEASURED on the 1856 "Ground Plan of Egyptian Court" (p.47):
#   column pitch / column square = 1.36-1.56 in the Hall of Karnak rows
# PLAN/BUILDING-DERIVED (1856 ground plan 0205 + Routledge aisle module):
#   shaft base diameter 1.25 m, pitch 1.85 m (see NOTES.md chain)
# ---------------------------------------------------------------------------
SHAFT_D_BASE = 1.25
SHAFT_D_TOP = 1.03
SHAFT_Z0 = 0.22            # top of plinth
SHAFT_Z1 = 5.12            # top of shaft / start of necking
PITCH = 1.85               # column centres in the pair
PLINTH_R = 0.86
NECK_Z1 = 5.42
CAP_Z1 = 6.10
ABACUS_SIZE = 1.32
ABACUS_H = 0.22
TOTAL_H = CAP_Z1 + ABACUS_H          # 6.32 m
PETALS = 14
CAP_RIBS = 18

# ---------------------------------------------------------------------------
def clean_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in list(bpy.data.collections):
        if coll.name not in ("Collection",):
            bpy.data.collections.remove(coll)

def make_collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

def mat_solid(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

def mat_image(name, path, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    tex.image.colorspace_settings.name = "sRGB"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return m

def lathe_obj(name, profile, coll, mat, segments=64, phi_start=0.0,
              phi_len=2 * math.pi, mod_n=0, mod_amp=0.0, v_mode="profile"):
    """profile: list of (r, z). Returns object with world-space geometry."""
    rings = len(profile)
    verts, faces, uvs = [], [], []
    closed = abs(phi_len - 2 * math.pi) < 1e-9
    nseg = segments if closed else segments  # segments across phi_len
    for i in range(rings):
        r, z = profile[i]
        for j in range(nseg + (0 if closed else 1)):
            phi = phi_start + phi_len * (j / nseg)
            rr = r * (1.0 + mod_amp * math.cos(mod_n * phi)) if mod_n else r
            verts.append((rr * math.cos(phi), rr * math.sin(phi), z))
            u = j / nseg
            v = i / (rings - 1) if v_mode == "profile" else z
            uvs.append((u, v))
    cols = nseg if closed else nseg + 1
    for i in range(rings - 1):
        for j in range(nseg):
            a = i * cols + j
            b = i * cols + (j + 1) % cols if closed else i * cols + j + 1
            c = b + cols
            dd = a + cols
            faces.append((a, b, c, dd))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    uv_layer = me.uv_layers.new(name="UVMap")
    for loop in me.loops:
        uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if mat:
        me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    return ob

def box_obj(name, size, loc, coll, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # move to target collection
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

# ---------------------------------------------------------------------------
def build_column(model_coll, mats, x_off, tag):
    g = []
    # Plinth: two-step round disc base (woodcut shows a low round plinth)
    prof = [(0.0, 0.0), (PLINTH_R, 0.0), (PLINTH_R, 0.09), (0.80, 0.11),
            (0.80, 0.20), (0.70, 0.23), (0.645, 0.25), (0.0, 0.25)]
    o = lathe_obj(f"Plinth_{tag}", prof, model_coll, mats["stone"], segments=56)
    g.append(o)
    # Shaft: tapered, slight entasis; UV v spans the shaft so the five
    # painted registers run its full height
    prof = []
    steps = 10
    for i in range(steps + 1):
        t = i / steps
        r = (SHAFT_D_BASE / 2) * (1 - t) + (SHAFT_D_TOP / 2) * t
        r += 0.010 * math.sin(math.pi * t)          # entasis
        z = SHAFT_Z0 * (1 - t) + SHAFT_Z1 * t
        prof.append((r, z))
    o = lathe_obj(f"Shaft_{tag}", prof, model_coll, mats["shaft"], segments=64)
    g.append(o)
    # Register rings at the texture's register boundaries (v = .2,.4,.6,.8)
    for k in range(1, 5):
        t = k / 5.0
        z = SHAFT_Z0 + t * (SHAFT_Z1 - SHAFT_Z0)
        r = (SHAFT_D_BASE / 2) * (1 - t) + (SHAFT_D_TOP / 2) * t + 0.010 * math.sin(math.pi * t)
        prof = [(r + 0.004, z - 0.028), (r + 0.016, z), (r + 0.004, z + 0.028)]
        o = lathe_obj(f"RegisterRing{k}_{tag}", prof, model_coll, mats["dark"], segments=56)
        g.append(o)
    # Petal collar at the shaft foot (woodcut: pointed lotus petals rise
    # around the base) — closed thin-shell lathe segments, 3 paint colours
    pet_prof_outer = [(0.615, 0.24), (0.700, 0.33), (0.702, 0.46),
                      (0.662, 0.62), (0.622, 0.82)]
    pet_prof = pet_prof_outer + [(r - 0.035, z) for r, z in reversed(pet_prof_outer)]
    for colour_i, mat_key in enumerate(("petal_blue", "petal_green", "petal_red")):
        for p in range(PETALS):
            if p % 3 != colour_i:
                continue
            a0 = (p / PETALS) * 2 * math.pi
            o = lathe_obj(f"Petals{colour_i}_{p}_{tag}", pet_prof, model_coll,
                          mats[mat_key], segments=3,
                          phi_start=a0, phi_len=(2 * math.pi / PETALS) * 0.86)
            g.append(o)
    # Necking: stacked painted bands below the capital (woodcut)
    prof = [(0.518, SHAFT_Z1), (0.548, 5.17), (0.548, 5.23), (0.522, 5.27),
            (0.552, 5.31), (0.552, 5.37), (0.528, NECK_Z1)]
    o = lathe_obj(f"Necking_{tag}", prof, model_coll, mats["gold"], segments=56)
    g.append(o)
    # Capital: cluster-bud / inverted-bell form, ribbed (woodcut), painted
    prof = [(0.528, NECK_Z1), (0.560, 5.54), (0.615, 5.70), (0.685, 5.90),
            (0.735, 6.03), (0.745, CAP_Z1)]
    o = lathe_obj(f"Capital_{tag}", prof, model_coll, mats["capital"],
                  segments=72, mod_n=CAP_RIBS, mod_amp=0.018)
    g.append(o)
    # Abacus: square slab (plain painted stone) with a proud glyph band
    o = box_obj(f"Abacus_{tag}", (ABACUS_SIZE, ABACUS_SIZE, ABACUS_H),
                (0.0, 0.0, CAP_Z1 + ABACUS_H / 2), model_coll, mats["sand"])
    g.append(o)
    o = box_obj(f"AbacusBand_{tag}", (ABACUS_SIZE + 0.02, ABACUS_SIZE + 0.02, 0.11),
                (0.0, 0.0, CAP_Z1 + ABACUS_H / 2), model_coll, mats["abacus"])
    g.append(o)
    for ob in g:
        ob.location.x += x_off
    return g

# ---------------------------------------------------------------------------
def main():
    clean_scene()
    model = make_collection("Model")
    setup = make_collection("RenderSetup")
    mats = {
        "stone": mat_solid("PaintedStone_Plaster", (0.55, 0.47, 0.36), 0.95),
        "shaft": mat_image("ShaftPaint", os.path.join(TEX, "shaft_paint.png"), 0.9),
        "capital": mat_image("CapitalPaint", os.path.join(TEX, "capital_paint.png"), 0.9),
        "abacus": mat_image("AbacusPaint", os.path.join(TEX, "abacus_paint.png"), 0.9),
        "sand": mat_solid("PaintedSand", (0.62, 0.53, 0.38), 0.9),
        "dark": mat_solid("PaintBand_Dark", (0.23, 0.17, 0.12), 0.9),
        "gold": mat_solid("PaintBand_Gilt", (0.36, 0.26, 0.11), 0.8),
        "petal_blue": mat_solid("Petal_Blue", (0.10, 0.24, 0.42), 0.85),
        "petal_green": mat_solid("Petal_Green", (0.16, 0.36, 0.22), 0.85),
        "petal_red": mat_solid("Petal_RedOchre", (0.48, 0.16, 0.10), 0.85),
    }
    build_column(model, mats, -PITCH / 2, "L")
    build_column(model, mats, +PITCH / 2, "R")

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
    fill.data.shape = "DISK"; fill.data.size = 8
    for c in fill.users_collection:
        c.objects.unlink(fill)
    setup.objects.link(fill)

    def look_at(ob, target):
        ob.rotation_euler = (Vector(target) - ob.location).to_track_quat("-Z", "Y").to_euler()

    cams = {}
    for name, loc in (("Front", (0, -15.5, 3.6)), ("Side", (15.5, 0, 3.6)),
                      ("ThreeQuarter", (10.5, -10.5, 5.4))):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.active_object
        cam.name = "Cam" + name
        cam.data.lens = 45
        look_at(cam, (0, 0, 3.0))
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

    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(ROOT, "renders", name.lower() + ".png") \
            if name != "ThreeQuarter" else os.path.join(ROOT, "renders", "three-quarter.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath)

if __name__ == "__main__":
    main()
