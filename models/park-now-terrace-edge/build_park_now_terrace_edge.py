# ============================================================================
# park-now-terrace-edge — present-day section of the Sydenham Upper
# Terrace edge (Crystal Palace Park, as it stands today): arcaded
# retaining wall + pierced parapet, empty statue plinths and sphinx-less
# bases on the plateau, gravel/grass surfaces, modern mesh fence.
#
# Wave 4, item 19 of models/SCENE-BUILD-PLAN.md. Scenes CP072/CP076
# (and the CP068-76 modern walk generally).
#
# PRESENT DAY ONLY. No 1854 dressing, no statues, no sphinxes (their
# plinths stand empty), no fountain water.
#
# Terrace dimensions are REUSED from the shipped evidence-derived
# terrace module (models/sy-terrace-step-and-arcade/NOTES.md, built
# by this stream): parapet = pierced arcade of narrow round-headed
# arches, 15 openings per 5.00 m bay, opening 0.19 x 0.55 m, pitch
# 0.30 m, plate 0.20 m, base band 0.25 m, coping 0.12 m, parapet
# total 1.05 m, pilaster 0.55 m wide. Wall niche rhythm (groups of 3
# between pilasters) is published (Historic England 1064352) and
# photo-counted on CPupperterraces02 (3 niches per parapet bay).
# Wall height / niche size / plinth sizes are photo-proportioned
# estimates — see NOTES.md; treat the set as +/-10-15 %.
#
# Axes: X along the terrace, Y depth (garden side -Y, plateau +Y,
# wall front face at y=0), Z up (garden ground z=0). Origin at the
# base centre of the section. Units: metres. Blender 4.5.3.
# ============================================================================
import bpy, math, os
import numpy as np
from mathutils import Matrix, Vector

# --- Section layout ---------------------------------------------------------
BAYS        = 7                 # composed section: 7 bays
BAY_LEN     = 5.00              # reused terrace module bay (pilaster pitch)
SEC_LEN     = BAYS * BAY_LEN    # 35.00 m between end-pilaster centres

# --- Terrace wall -----------------------------------------------------------
WALL_H      = 3.80              # garden ground -> plateau surface
WALL_T      = 0.90              # wall body thickness
PLINTH_H    = 0.35              # wall plinth band height
PLINTH_PROJ = 0.05              # plinth projection toward garden
NICHE_W     = 1.00              # niche opening width (photo-proportioned)
NICHE_H     = 2.95              # opening height incl. semicircular head
NICHE_PITCH = 1.50              # 3 per bay (counted on CPupperterraces02)
PLATE_T     = 0.40              # front plate thickness = niche recess depth
CORN_A_H    = 0.25              # cornice step 1: z 3.30..3.55, proj 0.03
CORN_B_H    = 0.25              # cornice step 2: z 3.55..3.80, proj 0.07
PIL_W       = 0.55              # wall pilaster width (reused)
PIL_PROJ    = 0.15              # pilaster projection toward garden

# --- Parapet (all reused from sy-terrace-step-and-arcade) --------------------
PAR_H       = 1.05              # parapet total above plateau
PAR_BASE_H  = 0.25              # base band
PAR_PLATE_T = 0.20              # pierced plate thickness
PAR_ARCH_W  = 0.19              # opening width
PAR_ARCH_H  = 0.55              # opening height
PAR_PITCH   = 0.30              # opening pitch -> 15 per bay
PAR_COP_H   = 0.12              # coping height
PAR_COP_T   = 0.34              # coping thickness (overhangs plate)
PAR_PIL_T   = 0.30              # parapet pilaster thickness
CAP_H       = 0.08              # pilaster cap slab (stands EMPTY)

# --- Surfaces ---------------------------------------------------------------
GRAVEL_TOP_D  = 4.00            # gravel strip behind parapet (geograph view)
GRASS_TOP_D   = 8.00            # grass plateau beyond
GRAVEL_FORE_D = 5.00            # gravel forecourt at wall foot (1980s view)
GRASS_FORE_D  = 4.50            # grass bank strip beyond (north-end view)

# --- Plinths (present day, EMPTY) -------------------------------------------
PLINTH_XS   = (-14.5, -8.0, -1.5, 5.0)   # statue plinth positions on gravel
PLINTH_Y    = 2.35
SPHINX_XS   = (11.4, 15.4)               # sphinx-less base pair
SPHINX_Y    = 2.45
SPHINX_L, SPHINX_W, SPHINX_H = 3.60, 1.50, 0.90   # two plain courses (photo)

# --- Modern fence (photographed on the plateau edge, geograph view) -------
FENCE_Y     = 1.30
FENCE_H     = 1.10
POST_PITCH  = 2.50

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Procedural textures (numpy) — no photographic textures anywhere.
def _blotches(rng, n, cells, amp):
    small = rng.normal(0.0, 1.0, (cells, cells)).astype(np.float32)
    big = np.kron(small, np.ones((n // cells, n // cells), np.float32))
    for _ in range(6):
        big = (np.roll(big, 4, 0) + np.roll(big, -4, 0) +
               np.roll(big, 4, 1) + np.roll(big, -4, 1) + big) / 5.0
    return big * amp

def _save_rgba(name, rgba, path):
    n = rgba.shape[0]
    img = bpy.data.images.new(name, n, n, alpha=True)
    img.pixels = rgba.ravel().tolist()
    img.filepath_raw = path
    img.file_format = 'PNG'
    img.save()
    return path

def make_textures(texdir):
    os.makedirs(texdir, exist_ok=True)
    rng = np.random.default_rng(19)
    n = 512
    # stone: warm grey mottle (as terrace prop) + greyer weathering cast
    base = rng.normal(0.88, 0.020, (n, n)).astype(np.float32)
    img = np.clip(base + _blotches(rng, n, 32, 0.024), 0.66, 1.0)
    img[::64, :] *= 0.97
    stone = np.stack([img, img * 0.985, img * 0.95], axis=-1)
    _save_rgba("stone_tex", np.concatenate(
        [stone, np.ones((n, n, 1), np.float32)], -1),
        os.path.join(texdir, "stone.png"))
    # gravel: fine speckle, grey-brown
    g = rng.normal(0.52, 0.075, (n, n)).astype(np.float32)
    g += _blotches(rng, n, 64, 0.05)
    dots = rng.random((n, n))
    g[dots > 0.985] += 0.22; g[dots < 0.015] -= 0.20
    gravel = np.stack([g * 1.02, g * 0.97, g * 0.88], axis=-1)
    _save_rgba("gravel_tex", np.concatenate(
        [np.clip(gravel, 0, 1), np.ones((n, n, 1), np.float32)], -1),
        os.path.join(texdir, "gravel.png"))
    # grass: two-scale green mottle with dry patches
    gr = 0.42 + rng.normal(0, 0.045, (n, n)).astype(np.float32) \
        + _blotches(rng, n, 32, 0.06)
    dry = np.clip(_blotches(rng, n, 16, 0.09), 0, 0.10)
    grass = np.stack([gr * 0.82 + dry, gr * 1.06, gr * 0.55], axis=-1)
    _save_rgba("grass_tex", np.concatenate(
        [np.clip(grass, 0, 1), np.ones((n, n, 1), np.float32)], -1),
        os.path.join(texdir, "grass.png"))
    # fence mesh: alpha grid (thin wires on 25 mm grid, drawn 4px/128)
    m = np.zeros((128, 128), np.float32)
    m[::8, :] = 1.0; m[:, ::8] = 1.0
    rgba = np.zeros((128, 128, 4), np.float32)
    rgba[..., 0] = 0.23; rgba[..., 1] = 0.22; rgba[..., 2] = 0.20
    rgba[..., 3] = m
    _save_rgba("mesh_tex", rgba, os.path.join(texdir, "fence_mesh.png"))

def load_tex(fname):
    img = bpy.data.images.load(os.path.join(OUT, "textures", fname))
    img.pack()
    return img

def tex_material(name, tex_img, tint=(1, 1, 1), rough=0.95, box=True,
                 alpha=False, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Base Color"].default_value = (*tint, 1.0)
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = tex_img
    if box:
        tex.projection = 'BOX'; tex.projection_blend = 0.3
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if alpha:
        m.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
        try: m.surface_render_method = 'DITHERED'
        except Exception: m.blend_method = 'CLIP'
    return m

def plain_material(name, rgba, rough=0.9, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return m

# ----------------------------------------------------------------------------
def box(name, size, loc, mat, coll):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name; ob.data.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(scale=True)
    if mat: ob.data.materials.append(mat)
    for c in list(ob.users_collection): c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def join_objects(name, obs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name; ob.data.name = name
    return ob

def arch_hole(cx, y0, w, h, seg=7):
    r = w / 2.0; hs = h - r
    pts = [(cx - r, y0), (cx - r, y0 + hs)]
    for i in range(1, seg):
        a = math.pi - i * math.pi / seg
        pts.append((cx + r * math.cos(a), y0 + hs + r * math.sin(a)))
    pts.append((cx + r, y0 + hs)); pts.append((cx + r, y0))
    return pts

def plate_mesh(name, outline, holes, thickness, matrix, mat, coll):
    """Pierced plate from a 2D outline + hole outlines (curve fill),
    extruded (curve extrude extends BOTH ways), baked through matrix."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    cu.extrude = thickness / 2.0
    def add(pts):
        sp = cu.splines.new('POLY')
        sp.points.add(len(pts) - 1)
        for p, co in zip(sp.points, pts):
            p.co = (co[0], co[1], 0.0, 1.0)
        sp.use_cyclic_u = True
    add(outline)
    for h in holes: add(h)
    ob = bpy.data.objects.new(name, cu)
    coll.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.active_object
    ob.data.name = name
    zs = [v.co.z for v in ob.data.vertices]
    dz = -(min(zs) + max(zs)) / 2.0
    for v in ob.data.vertices: v.co.z += dz
    ob.data.transform(matrix)
    ob.matrix_world = Matrix.Identity(4)
    if mat: ob.data.materials.append(mat)
    ob.select_set(False)
    return ob

def mat_front(tx, ty, tz):
    # plate space (u along X, v up) -> world: X=u, Y=extrusion, Z=v
    return Matrix(((1, 0, 0, tx), (0, 0, 1, ty), (0, 1, 0, tz),
                   (0, 0, 0, 1)))

# ----------------------------------------------------------------------------
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    model = bpy.data.collections.new("Model")
    scene.collection.children.link(model)
    setup = bpy.data.collections.new("RenderSetup")
    scene.collection.children.link(setup)

    make_textures(os.path.join(OUT, "textures"))
    stone = tex_material("Stone", load_tex("stone.png"),
                         (0.745, 0.718, 0.665))
    stone_dark = tex_material("StoneDark", load_tex("stone.png"),
                              (0.60, 0.578, 0.535))
    gravel = tex_material("Gravel", load_tex("gravel.png"))
    grass = tex_material("Grass", load_tex("grass.png"))
    steel = plain_material("FenceSteel", (0.145, 0.132, 0.118, 1),
                           rough=0.6, metallic=0.5)
    mesh_mat = tex_material("FenceMesh", load_tex("fence_mesh.png"),
                            rough=0.6, box=False, alpha=True,
                            metallic=0.3)

    x0 = -SEC_LEN / 2.0
    wall_top = WALL_H                      # 3.80
    plate_h = wall_top - PLINTH_H - (CORN_A_H + CORN_B_H)   # 2.95

    # --- Terrace wall -------------------------------------------------------
    # plinth spans y -0.05..0.45 (depth 0.50, centre y=0.20), z 0..0.35.
    # NOTE: box() bakes the passed location into the mesh (identity
    # object transforms) — never re-assign .location afterwards, or
    # the offset is applied twice (round-1 QC defect, see NOTES.md).
    box("WallPlinth", (SEC_LEN, WALL_T / 2 + PLINTH_PROJ, PLINTH_H),
        (0, (WALL_T / 2 - PLINTH_PROJ) / 2 - 0.0, PLINTH_H / 2),
        stone, model)

    plates = []
    for b in range(BAYS):
        cx = x0 + b * BAY_LEN
        outline = [(cx, 0), (cx + BAY_LEN, 0),
                   (cx + BAY_LEN, plate_h), (cx, plate_h)]
        holes = [arch_hole(cx + BAY_LEN / 2 + k * NICHE_PITCH, 0,
                           NICHE_W, NICHE_H) for k in (-1, 0, 1)]
        plates.append(plate_mesh(f"WallPlate{b}", outline, holes,
                                 PLATE_T,
                                 mat_front(0, PLATE_T / 2, PLINTH_H),
                                 stone, model))
    join_objects("WallFrontPlate", plates)

    box("WallBack", (SEC_LEN, WALL_T - PLATE_T, wall_top),
        (0, PLATE_T + (WALL_T - PLATE_T) / 2, wall_top / 2), stone, model)
    # cornice steps (corbelled toward the garden, per the geograph view)
    box("CorniceLow", (SEC_LEN, WALL_T + 0.03, CORN_A_H),
        (0, (WALL_T + 0.03) / 2 - 0.03, wall_top - CORN_B_H - CORN_A_H / 2),
        stone, model)
    box("CorniceHigh", (SEC_LEN, WALL_T + 0.07, CORN_B_H),
        (0, (WALL_T + 0.07) / 2 - 0.07, wall_top - CORN_B_H / 2),
        stone, model)

    pils = []
    for i in range(BAYS + 1):
        px = x0 + i * BAY_LEN
        pils.append(box(f"WallPilaster{i}",
                        (PIL_W, 0.70, wall_top),
                        (px, 0.20, wall_top / 2), stone, model))
    # pilasters span y -0.15..0.55 (centre y=0.20, depth 0.70), z 0..3.80
    join_objects("WallPilasters", pils)

    # --- Parapet (dimensions reused from sy-terrace-step-and-arcade) --------
    par_z = wall_top
    plates, bases, copings, ppils = [], [], [], []
    for b in range(BAYS):
        cx = x0 + b * BAY_LEN
        bases.append(box(f"ParBase{b}", (BAY_LEN, PAR_COP_T, PAR_BASE_H),
                         (cx + BAY_LEN / 2, PAR_COP_T / 2 - 0.02,
                          par_z + PAR_BASE_H / 2), stone, model))
        outline = [(cx, 0), (cx + BAY_LEN, 0),
                   (cx + BAY_LEN, PAR_H - PAR_BASE_H - PAR_COP_H),
                   (cx, PAR_H - PAR_BASE_H - PAR_COP_H)]
        holes = [arch_hole(cx + BAY_LEN / 2 + k * PAR_PITCH,
                           (PAR_H - PAR_BASE_H - PAR_COP_H - PAR_ARCH_H) / 2,
                           PAR_ARCH_W, PAR_ARCH_H)
                 for k in range(-7, 8)]
        plates.append(plate_mesh(f"ParPlate{b}", outline, holes,
                                 PAR_PLATE_T,
                                 mat_front(0, 0.15, par_z + PAR_BASE_H),
                                 stone, model))
        copings.append(box(f"ParCoping{b}", (BAY_LEN, PAR_COP_T, PAR_COP_H),
                           (cx + BAY_LEN / 2, PAR_COP_T / 2 - 0.02,
                            par_z + PAR_H - PAR_COP_H / 2), stone, model))
    join_objects("ParapetBase", bases)
    join_objects("ParapetPlate", plates)
    join_objects("ParapetCoping", copings)
    for i in range(BAYS + 1):
        px = x0 + i * BAY_LEN
        ppils.append(box(f"ParPilaster{i}", (PIL_W, PAR_PIL_T, PAR_H),
                         (px, PAR_PIL_T / 2 - 0.02, par_z + PAR_H / 2),
                         stone, model))
        ppils.append(box(f"ParCap{i}",
                         (PIL_W + 0.16, PAR_PIL_T + 0.12, CAP_H),
                         (px, (PAR_PIL_T + 0.12) / 2 - 0.02,
                          par_z + PAR_H + CAP_H / 2), stone, model))
    join_objects("ParapetPilasters", ppils)

    # --- Plateau + forecourt surfaces ---------------------------------------
    box("GravelTop", (SEC_LEN, GRAVEL_TOP_D, 0.15),
        (0, WALL_T + GRAVEL_TOP_D / 2, wall_top - 0.075), gravel, model)
    box("GrassTop", (SEC_LEN, GRASS_TOP_D, 0.18),
        (0, WALL_T + GRAVEL_TOP_D + GRASS_TOP_D / 2, wall_top - 0.09),
        grass, model)
    box("GravelForecourt", (SEC_LEN, GRAVEL_FORE_D, 0.15),
        (0, -GRAVEL_FORE_D / 2, -0.075), gravel, model)
    box("GrassForecourt", (SEC_LEN, GRASS_FORE_D, 0.15),
        (0, -GRAVEL_FORE_D - GRASS_FORE_D / 2, -0.095), grass, model)

    # --- Empty statue plinths on the plateau gravel --------------------------
    parts = []
    for j, px in enumerate(PLINTH_XS):
        parts.append(box(f"PlinthBase{j}", (1.24, 1.24, 0.16),
                         (px, PLINTH_Y, wall_top + 0.08), stone_dark, model))
        parts.append(box(f"PlinthDie{j}", (1.00, 1.00, 0.78),
                         (px, PLINTH_Y, wall_top + 0.16 + 0.39),
                         stone_dark, model))
        parts.append(box(f"PlinthCap{j}", (1.18, 1.18, 0.14),
                         (px, PLINTH_Y, wall_top + 0.16 + 0.78 + 0.07),
                         stone_dark, model))
    join_objects("StatuePlinths", parts)

    # --- Sphinx-less bases (plain two-course blocks; sphinxes NOT modelled) -
    parts = []
    for j, px in enumerate(SPHINX_XS):
        parts.append(box(f"SphinxBaseLow{j}", (SPHINX_L, SPHINX_W, 0.45),
                         (px, SPHINX_Y, wall_top + 0.225),
                         stone_dark, model))
        parts.append(box(f"SphinxBaseUp{j}",
                         (SPHINX_L - 0.16, SPHINX_W - 0.14, 0.45),
                         (px, SPHINX_Y, wall_top + 0.45 + 0.225),
                         stone_dark, model))
    join_objects("SphinxBases", parts)

    # --- Modern mesh fence behind the parapet (photographed) ----------------
    posts = []
    npost = int(SEC_LEN / POST_PITCH)
    for i in range(npost + 1):
        px = x0 + i * POST_PITCH
        posts.append(box(f"FencePost{i}", (0.07, 0.07, FENCE_H),
                         (px, FENCE_Y, wall_top + FENCE_H / 2),
                         steel, model))
    join_objects("FencePosts", posts)
    box("FenceRailTop", (SEC_LEN, 0.03, 0.035), (0, FENCE_Y, wall_top + 1.02),
        steel, model)
    box("FenceRailMid", (SEC_LEN, 0.03, 0.03), (0, FENCE_Y, wall_top + 0.58),
        steel, model)
    bpy.ops.mesh.primitive_plane_add(size=1.0,
                                     location=(0, FENCE_Y, wall_top + 0.55))
    mp = bpy.context.active_object
    mp.name = "FenceMesh"; mp.data.name = "FenceMesh"
    mp.dimensions = (SEC_LEN, FENCE_H - 0.06, 0)
    mp.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(scale=True)
    mp.data.materials.append(mesh_mat)
    for c in list(mp.users_collection): c.objects.unlink(mp)
    model.objects.link(mp)
    # tile the mesh texture along the run: texture holds 16 wire cells
    # per repeat; 88 x 2.6 repeats gives ~25 mm cells over 35 m x 1.04 m
    uv = mp.data.uv_layers.active.data
    for loop in uv: loop.uv = (loop.uv[0] * 88, loop.uv[1] * 2.6)

    # --- Render setup (same studio family as the terrace module) ------------
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.18))
    gp = bpy.context.active_object; gp.name = "GroundPlane"
    gp.data.materials.append(plain_material("BackdropGrey",
                                            (0.55, 0.55, 0.55, 1)))
    for c in list(gp.users_collection): c.objects.unlink(gp)
    setup.objects.link(gp)

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 20))
    sun = bpy.context.active_object; sun.data.energy = 3.2
    sun.rotation_euler = (math.radians(52), math.radians(12),
                          math.radians(-38))
    for c in list(sun.users_collection): c.objects.unlink(sun)
    setup.objects.link(sun)
    bpy.ops.object.light_add(type='AREA', location=(-14, 18, 14))
    ar = bpy.context.active_object
    ar.data.energy = 900.0; ar.data.size = 14.0
    ar.rotation_euler = (math.radians(58), 0, math.radians(150))
    for c in list(ar.users_collection): c.objects.unlink(ar)
    setup.objects.link(ar)
    bpy.ops.object.light_add(type='AREA', location=(10, -20, 6))
    bk = bpy.context.active_object
    bk.data.energy = 300.0; bk.data.size = 12.0
    bk.rotation_euler = (math.radians(80), 0, math.radians(180))
    for c in list(bk.users_collection): c.objects.unlink(bk)
    setup.objects.link(bk)

    world = bpy.data.worlds.new("World"); scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = \
        (0.55, 0.55, 0.55, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    target = Vector((0.0, 1.2, 2.3))
    def camera(name, loc, ortho=None):
        cd = bpy.data.cameras.new(name)
        if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
        co = bpy.data.objects.new(name, cd)
        setup.objects.link(co)
        co.location = loc
        d = target - Vector(loc)
        co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        return co
    # Ortho cameras sit FAR back (see the terrace module's QC note: with a
    # near ortho camera, buried geometry shows through the ground plane).
    cams = {
        "front": camera("CamFront", (0.0, -90.0, 2.8), ortho=44.0),
        "side":  camera("CamSide", (90.0, 1.2, 2.8), ortho=30.0),
        "three-quarter": camera("CamTQ", (25.0, -30.0, 14.5)),
    }

    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.film_transparent = False

    def render(cam_ob, filename):
        scene.camera = cam_ob
        scene.render.filepath = os.path.join(OUT, "renders", filename)
        bpy.ops.render.render(write_still=True)

    render(cams["front"], "front.png")
    render(cams["side"], "side.png")
    render(cams["three-quarter"], "three-quarter.png")

    # --- Export + save -------------------------------------------------------
    bpy.ops.object.select_all(action='DESELECT')
    for o in model.objects: o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(OUT, "park-now-terrace-edge.glb"),
        export_format='GLB', use_selection=True)
    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.join(OUT, "park-now-terrace-edge.blend"))

    # --- Report ---------------------------------------------------------------
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in model.objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg)
            tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
    print(f"PARKNOW OBJECTS {len(model.objects)} TRIS {tris}")
    allw = [o.matrix_world @ Vector(c)
            for o in model.objects if o.type == 'MESH' for c in o.bound_box]
    print(f"PARKNOW BBOX X {min(w.x for w in allw):.2f}..{max(w.x for w in allw):.2f} "
          f"Y {min(w.y for w in allw):.2f}..{max(w.y for w in allw):.2f} "
          f"Z {min(w.z for w in allw):.2f}..{max(w.z for w in allw):.2f}")

if __name__ == "__main__":
    build()
