#!/usr/bin/env python3
"""Build sy-terrace-step-and-arcade — Sydenham terrace step flight +
arcaded parapet (balustrade) module. Crystal Palace film, SCENE-BUILD-PLAN
Wave 3, item 14. Scenes CP042 / CP073. Sydenham only.

Re-runnable: blender --background --python build_sy_terrace_step_and_arcade.py
All dimensions are named constants below, grouped by evidence status.
See NOTES.md for the derivation of every number.
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Matrix, Vector

# ----------------------------------------------------------------------------
# DIMENSIONS (metres)
# --- Published (Historic England list entry 1064352, legacy description) ---
# The terrace balustrade is "of similar pattern of narrow round-headed
# arches" to the round-headed niche arcade below it; pilasters between
# groups of 3 niches are "carried up into the balustrade above", topped
# by vases or statues (NOT modelled). Flights of steps at intervals.
# --- Photo-counted (CPupperterraces02, late 1980s, upper terrace centre) ---
ARCHES_PER_BAY   = 15      # counted 89 openings across 6 pilaster bays (~15/bay)
# --- Photo-proportioned (same photo; Delamotte 1854 S57-01; geograph 3424917) ---
PARAPET_H        = 1.05    # parapet total height (~0.35 x niche-arch height)
ARCH_W           = 0.19    # narrow arch opening width
ARCH_PITCH       = 0.30    # arch centres along the bay (density from the count)
ARCH_H           = 0.55    # opening height incl. semicircular head
PLATE_T          = 0.20    # pierced plate thickness
BASE_H           = 0.25    # solid base band under the openings
COPING_H         = 0.12    # coping course
COPING_T         = 0.30    # coping thickness (overhangs plate both sides)
PILASTER_W       = 0.55    # pilaster width, carried up through the parapet
PILASTER_T       = 0.30    # pilaster thickness (proud of the plate)
PILASTER_CAP_H   = 0.08    # cap slab; vase/statue stood here — not modelled
BAY_LEN          = 5.00    # pilaster pitch = module length of the parapet bay
# --- Photo-estimated steps (2005 staircase photo; 1916 Quarter-deck painting) ---
STEP_RISE        = 0.15    # ~6 in; consistent across all views
STEP_GOING       = 0.70    # deep ceremonial treads; WEAKEST number (±0.15)
N_STEPS          = 4
FLIGHT_W         = 5.00    # module width = one parapet bay; tiles sideways
LANDING_D        = 1.50    # truncated top landing depth
# --- Cheek (raked parapet beside the flight) ---
CHEEK_T          = 0.24    # cheek plate thickness
CHEEK_ARCH_H     = 0.62    # cheek opening height (sits higher in the band)
CHEEK_ARCHES     = 9       # openings per cheek over the 4-step run
PIER_W           = 0.55    # square pier at the flight foot
PIER_H           = 1.05    # pier body height (cap above)
PIER_CAP_H       = 0.10

SLOPE = STEP_RISE / STEP_GOING            # 0.2143
RUN   = N_STEPS * STEP_GOING              # 2.80 m horizontal
RISE_TOT = N_STEPS * STEP_RISE            # 0.60 m

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Stone texture — painted by this script (numpy), no photographic texture.
def make_stone_texture(path, seed=7):
    rng = np.random.default_rng(seed)
    n = 512
    base = rng.normal(0.90, 0.018, (n, n)).astype(np.float32)
    # large soft blotches
    small = rng.normal(0.0, 1.0, (32, 32)).astype(np.float32)
    big = np.kron(small, np.ones((16, 16), np.float32))
    # smooth the blotches with a few box-blur passes
    for _ in range(6):
        big = (np.roll(big, 4, 0) + np.roll(big, -4, 0) + np.roll(big, 4, 1) + np.roll(big, -4, 1) + big) / 5.0
    img = np.clip(base + big * 0.022, 0.7, 1.0)
    # faint horizontal tooling lines
    img[::64, :] *= 0.97
    rgb = np.stack([img, img * 0.985, img * 0.945], axis=-1)
    rgba = np.concatenate([rgb, np.ones((n, n, 1), np.float32)], axis=-1)
    bimg = bpy.data.images.new("stone_tex", n, n, alpha=True)
    bimg.pixels = rgba.ravel().tolist()
    bimg.filepath_raw = path
    bimg.file_format = 'PNG'
    bimg.save()
    return path

def stone_material(name, tint, tex_img):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Base Color"].default_value = (*tint, 1.0)
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = tex_img
    tex.projection = 'BOX'
    tex.projection_blend = 0.3
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return m

# ----------------------------------------------------------------------------
# Helpers
def box(name, size, loc, mat, coll):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(scale=True)
    if mat: ob.data.materials.append(mat)
    for c in list(ob.users_collection): c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def join_objects(name, obs, coll):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name
    return ob

def arch_hole(cx, y0, w, h):
    """Upright round-headed opening outline (u,v), base at y0, total height h."""
    r = w / 2.0
    hs = h - r
    pts = [(cx - r, y0), (cx - r, y0 + hs)]
    for i in range(1, 7):
        a = math.pi - i * math.pi / 7.0
        pts.append((cx + r * math.cos(a), y0 + hs + r * math.sin(a)))
    pts.append((cx + r, y0 + hs))
    pts.append((cx + r, y0))
    return pts

def plate_mesh(name, outline, holes, thickness, matrix, mat, coll):
    """Pierced plate from a 2D outline + hole outlines (curve fill), extruded,
    then baked through `matrix` (4x4) into world space."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    cu.extrude = thickness / 2.0   # curve extrude extends BOTH ways: total = 2x
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
    # centre the extrusion on z=0
    zs = [v.co.z for v in ob.data.vertices]
    dz = -(min(zs) + max(zs)) / 2.0
    for v in ob.data.vertices: v.co.z += dz
    ob.data.transform(matrix)
    ob.matrix_world = Matrix.Identity(4)
    if mat: ob.data.materials.append(mat)
    ob.select_set(False)
    return ob

# matrices mapping plate space (x=u along run, y=v up, z=thickness) to world
def mat_run_x(tx, ty, tz):
    # parapet running along world X: X=u, Y=-thick, Z=v
    return Matrix(((1,0,0,tx),(0,0,-1,ty),(0,1,0,tz),(0,0,0,1)))
def mat_run_y(tx, ty, tz):
    # cheek running along world Y: X=thick, Y=u, Z=v
    return Matrix(((0,0,1,tx),(1,0,0,ty),(0,1,0,tz),(0,0,0,1)))

# ----------------------------------------------------------------------------
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    model = bpy.data.collections.new("Model"); scene.collection.children.link(model)
    setup = bpy.data.collections.new("RenderSetup"); scene.collection.children.link(setup)

    tex_path = os.path.join(OUT, "textures", "stone.png")
    make_stone_texture(tex_path)
    tex_img = bpy.data.images.load(tex_path)
    tex_img.pack()
    stone  = stone_material("Stone",       (0.760, 0.733, 0.678), tex_img)
    stone2 = stone_material("StoneCoping", (0.694, 0.667, 0.612), tex_img)

    # --- Flight: solid step blocks (full-height, per the solid-masonry read) ---
    steps = []
    for i in range(N_STEPS):
        z_top = (i + 1) * STEP_RISE
        yc = -(i + 0.5) * STEP_GOING
        steps.append(box(f"Step{i+1}", (FLIGHT_W, STEP_GOING, z_top),
                         (0.0, yc, z_top / 2.0), stone, model))
    join_objects("FlightSteps", steps, model)

    # --- Top landing slab (truncated) ---
    box("LandingSlab", (FLIGHT_W, LANDING_D, RISE_TOT),
        (0.0, -RUN - LANDING_D / 2.0, RISE_TOT / 2.0), stone, model)

    # --- Raked cheeks ---
    # profile space: u = horizontal distance from y=-3.15 (u=0) toward +Y
    # (downhill); v = world z. Nosing slope line through the step nosings:
    def z_line(u):  # u measured from y=-3.15 -> nosings at u=0.35..3.15
        return 0.825 - SLOPE * u
    U0, U1 = 0.0, 3.50
    # plate top edge: beside the landing (u < 0.35) it levels at the
    # landing parapet's plate height (RISE_TOT + 0.93); from the top
    # nosing (u = 0.35) it follows the nosing line + 0.93 downhill.
    TOP_END = RISE_TOT + (PARAPET_H - COPING_H)   # 1.53
    cheek_outline = [
        (U0, z_line(U0) - 0.45), (U1, z_line(U1) - 0.45),
        (U1, z_line(U1) + 0.93), (0.35, z_line(0.35) + 0.93),
        (U0, TOP_END),
    ]
    cheek_holes = []
    for k in range(CHEEK_ARCHES):
        uc = 0.62 + k * ARCH_PITCH
        cheek_holes.append(arch_hole(uc, z_line(uc) + 0.12, ARCH_W, CHEEK_ARCH_H))
    cheek_coping_outline = [
        (U0 - 0.03, TOP_END), (0.35, z_line(0.35) + 0.93),
        (U1 + 0.03, z_line(U1) + 0.93),
        (U1 + 0.03, z_line(U1) + 0.93 + COPING_H),
        (0.35, z_line(0.35) + 0.93 + COPING_H),
        (U0 - 0.03, TOP_END + COPING_H),
    ]
    cheek_x = FLIGHT_W / 2.0 + CHEEK_T / 2.0
    for side, sx in (("R", cheek_x), ("L", -cheek_x)):
        plate_mesh(f"CheekPlate_{side}", cheek_outline, cheek_holes, CHEEK_T,
                   mat_run_y(sx, -3.15, 0.0), stone, model)
        plate_mesh(f"CheekCoping_{side}", cheek_coping_outline, [], COPING_T,
                   mat_run_y(sx, -3.15, 0.0), stone2, model)

    # --- Piers at the flight foot ---
    for side, sx in (("R", cheek_x), ("L", -cheek_x)):
        body = box(f"PierBody_{side}", (PIER_W, PIER_W, PIER_H),
                   (sx, 0.10, PIER_H / 2.0), stone, model)
        base = box(f"PierBase_{side}", (PIER_W + 0.10, PIER_W + 0.10, 0.12),
                   (sx, 0.10, 0.06), stone, model)
        cap = box(f"PierCap_{side}", (PIER_W + 0.15, PIER_W + 0.15, PIER_CAP_H),
                  (sx, 0.10, PIER_H + PIER_CAP_H / 2.0), stone2, model)
        join_objects(f"Pier_{side}", [body, base, cap], model)

    # --- Level parapet bay along the landing's back edge ---
    # The bay STANDS ON the landing: all its z values offset by RISE_TOT.
    py = -RUN - LANDING_D + 0.15   # parapet centreline near landing back edge
    ZP = RISE_TOT
    box("ParapetBase", (BAY_LEN, 0.30, BASE_H), (0.0, py, ZP + BASE_H / 2.0), stone, model)
    plate_outline = [(0.0, BASE_H), (BAY_LEN, BASE_H),
                     (BAY_LEN, PARAPET_H - COPING_H), (0.0, PARAPET_H - COPING_H)]
    holes = []
    for k in range(ARCHES_PER_BAY):
        uc = 0.40 + k * ARCH_PITCH
        holes.append(arch_hole(uc, BASE_H, ARCH_W, ARCH_H))
    plate_mesh("ParapetPlate", plate_outline, holes, PLATE_T,
               mat_run_x(-BAY_LEN / 2.0, py, ZP), stone, model)
    box("ParapetCoping", (BAY_LEN + 0.06, COPING_T, COPING_H),
        (0.0, py, ZP + PARAPET_H - COPING_H / 2.0), stone2, model)
    # pilaster at the bay's start end (tiles: next bay's pilaster abuts)
    pil_x = -BAY_LEN / 2.0 - PILASTER_W / 2.0 + 0.02
    pb = box("PilasterBody", (PILASTER_W, PILASTER_T, PARAPET_H),
             (pil_x, py, ZP + PARAPET_H / 2.0), stone, model)
    pc = box("PilasterCap", (PILASTER_W + 0.14, PILASTER_T + 0.10, PILASTER_CAP_H),
             (pil_x, py, ZP + PARAPET_H + PILASTER_CAP_H / 2.0), stone2, model)
    pbs = box("PilasterBase", (PILASTER_W + 0.10, PILASTER_T + 0.06, 0.12),
              (pil_x, py, ZP + 0.06), stone, model)
    join_objects("ParapetPilaster", [pb, pc, pbs], model)

    # --- Render setup: ground, lights, cameras ---
    bpy.ops.mesh.primitive_plane_add(size=70.0, location=(0, 0, -0.01))
    g = bpy.context.active_object; g.name = "Ground"
    gm = bpy.data.materials.new("GroundGrey"); gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.52, 0.52, 0.52, 1.0)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.data.materials.append(gm)
    for c in list(g.users_collection): c.objects.unlink(g)
    setup.objects.link(g)

    bpy.ops.object.light_add(type='SUN', location=(6, 8, 10))
    sun = bpy.context.active_object; sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), math.radians(8), math.radians(35))
    for c in list(sun.users_collection): c.objects.unlink(sun)
    setup.objects.link(sun)
    bpy.ops.object.light_add(type='AREA', location=(-7, 6, 6))
    ar = bpy.context.active_object; ar.data.energy = 350.0; ar.data.size = 6.0
    ar.rotation_euler = (math.radians(60), 0, math.radians(-40))
    for c in list(ar.users_collection): c.objects.unlink(ar)
    setup.objects.link(ar)
    # dim back fill so the arch reveals / shadowed ground behind the
    # parapet do not crush to pure black
    bpy.ops.object.light_add(type='AREA', location=(0, -9, 3.5))
    bk = bpy.context.active_object; bk.data.energy = 120.0; bk.data.size = 8.0
    bk.rotation_euler = (math.radians(75), 0, math.radians(180))
    for c in list(bk.users_collection): c.objects.unlink(bk)
    setup.objects.link(bk)

    world = bpy.data.worlds.new("World"); scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    target = Vector((0.0, -1.55, 0.55))
    def camera(name, loc, ortho=None):
        cd = bpy.data.cameras.new(name)
        if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
        co = bpy.data.objects.new(name, cd)
        setup.objects.link(co)
        co.location = loc
        d = target - Vector(loc)
        co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        return co
    # Ortho cameras sit FAR back: with a near ortho camera, rays to the
    # cheeks' buried feet pass under the ground plane before reaching it
    # (the occluding plane surface lies behind the camera plane) and the
    # buried geometry shows through. Distance does not change ortho
    # framing, only where the rays start.
    cams = {
        "front":        camera("CamFront", (0.0, 26.0, 1.6), ortho=8.6),
        "side":         camera("CamSide", (26.0, -1.55, 1.6), ortho=8.6),
        "three-quarter": camera("CamTQ", (6.4, 5.6, 4.4)),
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

    # --- Tiled proof: flight repeated up the slope x3, parapet x3 along X ---
    dupes = []
    src_names = ["FlightSteps", "CheekPlate_R", "CheekPlate_L",
                 "CheekCoping_R", "CheekCoping_L"]
    for rep in (1, 2):
        for n in src_names:
            o = bpy.data.objects[n].copy()
            o.location = (0.0, -rep * RUN, rep * RISE_TOT)
            model.objects.link(o); dupes.append(o)
    for rep in (-1, 1):
        for n in ("ParapetBase", "ParapetPlate", "ParapetCoping",
                  "ParapetPilaster", "LandingSlab"):
            o = bpy.data.objects[n].copy()
            # tile the parapet bay sideways along the landing, on its slab
            o.location = (rep * BAY_LEN, 0.0, 0.0)
            model.objects.link(o); dupes.append(o)
    # the single landing/parapet would collide with repeated flights; hide
    # the first repeated flight's overlap is above the landing — acceptable
    # in the proof view; pull the camera back instead:
    tq2 = camera("CamTiled", (13.0, 12.0, 9.0))
    # widen target for the tiled view
    d = Vector((0.0, -4.2, 1.3)) - Vector((13.0, 12.0, 9.0))
    tq2.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    render(tq2, "tiled-three-quarter.png")
    for o in dupes:
        model.objects.unlink(o)
        bpy.data.objects.remove(o)
    setup.objects.unlink(tq2); bpy.data.objects.remove(tq2)

    # --- Export + save (Model collection only) ---
    bpy.ops.object.select_all(action='DESELECT')
    for o in model.objects: o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(OUT, "sy-terrace-step-and-arcade.glb"),
        export_format='GLB', use_selection=True)
    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.join(OUT, "sy-terrace-step-and-arcade.blend"))

    # --- Report ---
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in model.objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg)
            tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
    print(f"SY-TERRACE OBJECTS {len(model.objects)} TRIS {tris}")
    import mathutils
    allw = [o.matrix_world @ mathutils.Vector(c)
            for o in model.objects if o.type == 'MESH' for c in o.bound_box]
    print(f"SY-TERRACE BBOX X {min(w.x for w in allw):.2f}..{max(w.x for w in allw):.2f} "
          f"Y {min(w.y for w in allw):.2f}..{max(w.y for w in allw):.2f} "
          f"Z {min(w.z for w in allw):.2f}..{max(w.z for w in allw):.2f}")

if __name__ == "__main__":
    build()
