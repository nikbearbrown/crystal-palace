#!/usr/bin/env python3
"""Build hp-crate-and-display-case: an 1851 exhibition table case (vitrine)
plus a period deal packing crate, as one prop set.

Blender 4.5.3, bpy. Re-runnable: clears the scene and rebuilds from the
constants below. Units: metres. Origin: base centre of the CASE; the
crate stands beside it (+X) in the same Model collection.

Evidence basis: Dickinson's Comprehensive Pictures, plate XXIV (Cotton
court) shows the standard 1851 table case repeatedly: a timber table
frame on turned legs with a deep apron, carrying a shallow hipped
(glazed gable) lid. ALL SIZES ARE GUESSED from the plates by proportion
against the standing figures (no dimensioned source exists) — see
NOTES.md. The crate has NO image evidence in the repo references; it
is plain period deal-and-batten construction and is labelled generic.

Env: HPCASE_NORENDER=1 skips rendering (geometry + exports only).
"""
import bpy, math, os, sys
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/crystal-palace-film/build/hp-crate-and-display-case")
SLUG = "hp-crate-and-display-case"

# ----------------------------------------------------------------------------
# CASE dimensions — GUESSED (see header). Read off Dickinson plate XXIV by
# proportion against standing figures ~1.70 m: lid eave at a man's hip,
# ridge a hand above it; case length about two onlookers' span.
# ----------------------------------------------------------------------------
CASE_L   = 1.90    # overall length (x)
CASE_D   = 0.95    # overall depth (y)
LEG_TOP  = 0.64    # floor -> underside of apron
APRON_H  = 0.18    # apron/frieze depth (0.64 -> 0.82)
EAVE_Z   = LEG_TOP + APRON_H          # 0.82, base of glazed lid
RIDGE_Z  = 1.00    # top of lid ridge (rise 0.18 — the plates' lids are shallow)
RIDGE_HALF = CASE_L/2 - CASE_D/2      # hipped lid: 0.475 (equal slopes)
APRON_T  = 0.035   # apron band thickness
LEG_INSET_X = 0.11 # leg centre inset from case ends
LEG_INSET_Y = 0.11
BAR_W    = 0.034   # glazing bar width
BAR_T    = 0.026   # glazing bar depth
BED_Z    = 0.795   # display bed top (inside, just below eave frame)
GLASS_IN = 0.010   # glass pane inset from lid outer surface

# CRATE dimensions — GUESSED, generic period packing case (no evidence).
CRATE_W  = 1.10    # x
CRATE_D  = 0.70    # y
CRATE_BODY_H = 0.68
BOARD_T  = 0.022
BOARD_PITCH = 0.138  # board height + gap
BAT_W    = 0.095   # batten width
BAT_T    = 0.028   # horizontal batten thickness (outside the boards)
VBAT_T   = 0.034   # vertical battens sit 6 mm proud of the horizontals —
                   # coplanar batten faces rendered as black squares in QC1
CRATE_X  = 1.70    # crate centre x (case ends at 0.95; gap 0.20)

# ----------------------------------------------------------------------------
def purge():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in list(bpy.data.collections):
        if coll.name != "Scene Collection":
            bpy.data.collections.remove(coll)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        pass  # orphaned data is harmless for a fresh save

def get_coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c

def mat(name, rgb, alpha=1.0, rough=0.75):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        m.surface_render_method = 'DITHERED'
    return m

MAT_CASE  = None  # set in main
MAT_CRATE = None
MAT_GLASS = None
MAT_BED   = None

def link(obj, coll):
    coll.objects.link(obj)
    return obj

def box(name, cx, cy, cz, sx, sy, sz, coll, material, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz), rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        o.data.materials.append(material)
    # primitive adds to scene collection; move to target collection
    for c in o.users_collection:
        c.objects.unlink(o)
    coll.objects.link(o)
    return o

def beam(name, p1, p2, w, t, side_hint, coll, material):
    """Box beam between two points. w = width along side dir, t = depth."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    L = d.length
    d.normalize()
    s = Vector(side_hint)
    s = s - d * s.dot(d)
    s.normalize()
    n = d.cross(s)
    hw, ht = w/2, t/2
    verts = []
    for p in (p1, p2):
        for a in (-hw, hw):
            for b in (-ht, ht):
                q = p + s*a + n*b
                verts.append(tuple(q))
    faces = [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    coll.objects.link(o)
    return o

def quad(name, pts, coll, material):
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata([tuple(p) for p in pts], [], [list(range(len(pts)))])
    me.update()
    o = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    o.visible_shadow = False
    coll.objects.link(o)
    return o

def lathe(name, profile, cx, cy, coll, material, segments=14):
    """profile: list of (r, z) bottom->top. Axis vertical at (cx, cy, 0)."""
    verts, faces = [], []
    rings = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(segments):
            a = 2*math.pi*j/segments
            verts.append((cx + r*math.cos(a), cy + r*math.sin(a), z))
    for i in range(rings-1):
        for j in range(segments):
            j2 = (j+1) % segments
            a = i*segments + j; b = i*segments + j2
            c = (i+1)*segments + j2; d2 = (i+1)*segments + j
            faces.append((a, b, c, d2))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    coll.objects.link(o)
    return o

# ----------------------------------------------------------------------------
def build_case(coll):
    L, D = CASE_L, CASE_D
    hx, hy = L/2, D/2
    # --- legs: turned (lathe) + square top block
    prof = [(0.001,0.0),(0.044,0.0),(0.044,0.024),(0.033,0.06),(0.030,0.18),
            (0.034,0.30),(0.041,0.42),(0.037,0.475),(0.051,0.505),(0.051,0.535),
            (0.038,0.555),(0.038,0.575),(0.001,0.575)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx*(hx-LEG_INSET_X), sy*(hy-LEG_INSET_Y)
            lathe(f"Case_Leg_{sx:+d}_{sy:+d}", prof, cx, cy, coll, MAT_CASE)
            box(f"Case_LegBlock_{sx:+d}_{sy:+d}", cx, cy, 0.575,
                0.095, 0.095, 0.13, coll, MAT_CASE)
    # --- apron / frieze band (deep band under the lid, plate XXIV)
    for sy in (-1, 1):
        box(f"Case_Apron_FB_{sy:+d}", 0, sy*(hy-APRON_T/2), LEG_TOP+APRON_H/2,
            L, APRON_T, APRON_H, coll, MAT_CASE)
    for sx in (-1, 1):
        box(f"Case_Apron_End_{sx:+d}", sx*(hx-APRON_T/2), 0, LEG_TOP+APRON_H/2,
            APRON_T, D-2*APRON_T, APRON_H, coll, MAT_CASE)
    # moulded bead along the top of the apron (the bright line under the lid)
    for sy in (-1, 1):
        box(f"Case_Bead_FB_{sy:+d}", 0, sy*(hy-0.006), EAVE_Z-0.012,
            L+0.012, 0.048, 0.024, coll, MAT_CASE)
    for sx in (-1, 1):
        box(f"Case_Bead_End_{sx:+d}", sx*(hx-0.006), 0, EAVE_Z-0.012,
            0.048, D+0.012, 0.024, coll, MAT_CASE)
    # bead along the bottom of the apron
    for sy in (-1, 1):
        box(f"Case_BeadLo_FB_{sy:+d}", 0, sy*(hy-APRON_T/2), LEG_TOP+0.014,
            L-0.02, APRON_T+0.014, 0.028, coll, MAT_CASE)
    for sx in (-1, 1):
        box(f"Case_BeadLo_End_{sx:+d}", sx*(hx-APRON_T/2), 0, LEG_TOP+0.014,
            APRON_T+0.014, D-2*APRON_T-0.02, 0.028, coll, MAT_CASE)
    # --- display bed (empty — CP025 ships the case empty)
    box("Case_Bed", 0, 0, BED_Z-0.015, L-2*APRON_T-0.01, D-2*APRON_T-0.01, 0.03,
        coll, MAT_BED)
    # --- lid eaves frame
    for sy in (-1, 1):
        box(f"Case_Eave_FB_{sy:+d}", 0, sy*(hy-0.02), EAVE_Z+0.008,
            L+0.02, 0.055, 0.032, coll, MAT_CASE)
    for sx in (-1, 1):
        box(f"Case_Eave_End_{sx:+d}", sx*(hx-0.02), 0, EAVE_Z+0.008,
            0.055, D+0.02, 0.032, coll, MAT_CASE)
    ez = EAVE_Z + 0.02
    # --- ridge bar
    box("Case_Ridge", 0, 0, RIDGE_Z, 2*RIDGE_HALF+0.06, 0.042, 0.036, coll, MAT_CASE)
    # --- hip bars: eave corners -> ridge ends (side hint = horizontal, out)
    for sx in (-1, 1):
        for sy in (-1, 1):
            beam(f"Case_Hip_{sx:+d}_{sy:+d}",
                 (sx*hx, sy*hy, ez), (sx*RIDGE_HALF, 0, RIDGE_Z),
                 BAR_W, BAR_T, (0, sy, 0), coll, MAT_CASE)
    # --- slope mullions: one centre bar per long slope (plate reading)
    for sy in (-1, 1):
        beam(f"Case_Mullion_{sy:+d}", (0, sy*hy, ez), (0, 0, RIDGE_Z),
             BAR_W, BAR_T, (1, 0, 0), coll, MAT_CASE)
    # --- glass panes (inset toward the inside of the lid)
    def slope_glass(sy, sx):  # half of a long slope
        e1 = Vector((sx*hx, sy*hy, ez)); e2 = Vector((0.0, sy*hy, ez))
        r1 = Vector((sx*RIDGE_HALF, 0, RIDGE_Z)); r2 = Vector((0.0, 0, RIDGE_Z))
        n = (e2-e1).cross(r2-e1); n.normalize()
        off = n * -GLASS_IN if n.z > 0 else n * GLASS_IN
        if (sy > 0) != (n.y > 0):  # push pane to the inside (away from viewer side)
            pass
        pts = [e1+off, e2+off, r2+off, r1+off]
        return [tuple(p) for p in pts]
    for sy in (-1, 1):
        for sx in (-1, 1):
            quad(f"Case_Glass_Slope_{sy:+d}_{sx:+d}", slope_glass(sy, sx), coll, MAT_GLASS)
    # end (triangular) panes
    for sx in (-1, 1):
        e1 = Vector((sx*hx, -hy, ez)); e2 = Vector((sx*hx, hy, ez))
        r = Vector((sx*RIDGE_HALF, 0, RIDGE_Z))
        n = (e2-e1).cross(r-e1); n.normalize()
        off = n * (GLASS_IN if n.x*sx < 0 else -GLASS_IN)
        quad(f"Case_Glass_End_{sx:+d}", [tuple(e1+off), tuple(e2+off), tuple(r+off)],
             coll, MAT_GLASS)

def build_crate(coll):
    cx0 = CRATE_X
    W, D, H = CRATE_W, CRATE_D, CRATE_BODY_H
    hx, hy = W/2, D/2
    n = 5
    board_h = (H - (n-1)*0.006) / n
    # front/back faces: horizontal boards
    for f, sy in (("F", 1), ("B", -1)):
        for i in range(n):
            z = board_h/2 + i*(board_h+0.006)
            box(f"Crate_Board_{f}_{i}", cx0, sy*(hy-BOARD_T/2), z,
                W, BOARD_T, board_h, coll, MAT_CRATE)
    # end faces: boards between front/back boards
    for f, sx in (("R", 1), ("L", -1)):
        for i in range(n):
            z = board_h/2 + i*(board_h+0.006)
            box(f"Crate_Board_{f}_{i}", cx0+sx*(hx-BOARD_T/2), 0, z,
                BOARD_T, D-2*BOARD_T, board_h, coll, MAT_CRATE)
    # bottom boards
    for i in range(4):
        y = -hy + BOARD_T + (D-2*BOARD_T) * (i+0.5)/4
        box(f"Crate_Bottom_{i}", cx0, y, BOARD_T/2, W-2*BOARD_T,
            (D-2*BOARD_T)/4 - 0.006, BOARD_T, coll, MAT_CRATE)
    # corner battens (both faces at each corner) — verticals proud (VBAT_T)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"Crate_Batten_CnrFB_{sx:+d}_{sy:+d}", cx0+sx*(hx-BAT_W/2-0.005),
                sy*(hy+VBAT_T/2), H/2, BAT_W, VBAT_T, H, coll, MAT_CRATE)
            box(f"Crate_Batten_CnrEnd_{sx:+d}_{sy:+d}", cx0+sx*(hx+VBAT_T/2),
                sy*(hy-BAT_W/2-0.005), H/2, VBAT_T, BAT_W, H, coll, MAT_CRATE)
    # top & bottom perimeter battens, front/back and ends
    for sy in (-1, 1):
        for zi, zc in (("Top", H-BAT_W/2), ("Bot", BAT_W/2)):
            box(f"Crate_Batten_FB_{zi}_{sy:+d}", cx0, sy*(hy+BAT_T/2), zc,
                W, BAT_T, BAT_W, coll, MAT_CRATE)
    for sx in (-1, 1):
        for zi, zc in (("Top", H-BAT_W/2), ("Bot", BAT_W/2)):
            box(f"Crate_Batten_End_{zi}_{sx:+d}", cx0+sx*(hx+BAT_T/2), 0, zc,
                BAT_T, D, BAT_W, coll, MAT_CRATE)
    # mid vertical battens on front/back (long faces) — also proud
    for sy in (-1, 1):
        box(f"Crate_Batten_Mid_{sy:+d}", cx0, sy*(hy+VBAT_T/2), H/2,
            BAT_W, VBAT_T, H, coll, MAT_CRATE)
    # lid: boards across the top + two cross battens (separate piece, resting)
    lid_z = H + 0.012
    for i in range(5):
        y = -hy + (D+0.02) * (i+0.5)/5
        box(f"Crate_LidBoard_{i}", cx0, y, lid_z, W+0.02,
            (D+0.02)/5 - 0.005, 0.024, coll, MAT_CRATE)
    for sx in (-1, 1):
        box(f"Crate_LidBatten_{sx:+d}", cx0+sx*(hx-0.16), 0, lid_z+0.024,
            BAT_W, D+0.02, 0.026, coll, MAT_CRATE)

# ----------------------------------------------------------------------------
def build_render_setup(coll):
    # ground
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0.6, 0, -0.001))
    g = bpy.context.active_object; g.name = "Ground"
    gm = mat("GroundGrey", (0.52, 0.52, 0.53), rough=1.0)
    g.data.materials.append(gm)
    for c in g.users_collection: c.objects.unlink(g)
    coll.objects.link(g)
    # lights
    def area(name, loc, energy, size):
        ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.shape = 'DISK'; ld.size = size
        o = bpy.data.objects.new(name, ld); o.location = loc; coll.objects.link(o)
        return o
    key = area("Key", (2.5, -3.5, 4.5), 300, 3.0)
    fill = area("Fill", (-3.5, 2.5, 2.5), 110, 3.0)
    top = area("Top", (0.5, 0.5, 5.5), 120, 2.5)
    for o in (key, fill, top):
        o.rotation_euler = (Vector((0.6, 0, 0.5)) - o.location).to_track_quat('-Z', 'Y').to_euler()
    # cameras
    def cam(name, loc, target):
        cd = bpy.data.cameras.new(name); cd.lens = 42
        o = bpy.data.objects.new(name, cd); o.location = loc
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        coll.objects.link(o)
        return o
    cams = {
        "front":        cam("CamFront", (0.62, -4.9, 1.02), (0.62, 0, 0.52)),
        "side":         cam("CamSide", (5.6, 0.0, 1.0), (0.62, 0, 0.50)),
        "three-quarter": cam("CamTQ", (3.6, -3.8, 2.3), (0.62, 0, 0.48)),
        "case-three-quarter": cam("CamCaseTQ", (2.3, -2.5, 1.65), (0, 0, 0.55)),
    }
    return cams

def render(cams, model_coll):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 960
    sc.render.resolution_y = 720
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new("W")
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.72, 0.72, 0.73, 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.4
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    crate_objs = [o for o in model_coll.objects if o.name.startswith("Crate_")]
    for name in ("front", "side", "three-quarter"):
        sc.camera = cams[name]
        sc.render.filepath = os.path.join(OUT, "renders", name + ".png")
        bpy.ops.render.render(write_still=True)
    # case alone
    for o in crate_objs: o.hide_render = True
    sc.camera = cams["case-three-quarter"]
    sc.render.filepath = os.path.join(OUT, "renders", "case-three-quarter.png")
    bpy.ops.render.render(write_still=True)
    for o in crate_objs: o.hide_render = False

def count_tris(coll):
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in coll.objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            me.calc_loop_triangles()
            total += len(me.loop_triangles)
            ev.to_mesh_clear()
    return total

def main():
    global MAT_CASE, MAT_CRATE, MAT_GLASS, MAT_BED
    purge()
    MAT_CASE  = mat("TimberCase",  (0.295, 0.215, 0.155), rough=0.62)
    MAT_CRATE = mat("TimberDeal",  (0.45, 0.385, 0.305), rough=0.9)
    MAT_BED   = mat("BedFelt",     (0.29, 0.27, 0.26), rough=1.0)
    MAT_GLASS = mat("Glass",       (0.92, 0.96, 0.97), alpha=0.16, rough=0.06)
    model = get_coll("Model")
    setup = get_coll("RenderSetup")
    build_case(model)
    build_crate(model)
    cams = build_render_setup(setup)
    tris = count_tris(model)
    print(f"[build] objects={len(model.objects)} triangles={tris}")
    # save blend
    blend_path = os.path.join(OUT, SLUG + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    # export glb: Model collection only
    bpy.ops.object.select_all(action='DESELECT')
    for o in model.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = model.objects[0]
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"),
                              export_format='GLB', use_selection=True,
                              export_apply=True)
    bpy.ops.object.select_all(action='DESELECT')
    if not os.environ.get("HPCASE_NORENDER"):
        render(cams, model)
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("[build] done")

main()
