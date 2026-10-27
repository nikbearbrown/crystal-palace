#!/usr/bin/env python3
"""Build sy-renaissance-arch-fragment — one repeatable bay of the
Sydenham Renaissance Court's loggia arcade (1854): a semicircular
arch on piers with an applied Ionic pilaster order, spandrel
roundels, and a full entablature with a carved frieze. The second
fragment of SCENE-BUILD-PLAN Wave 3 item 13 (the Gothic fragment,
sy-gothic-arch-fragment, is its pair).

Run:  blender -b -P build_sy_renaissance_arch_fragment.py

Form source: the stereograph of the court catalogued as
"CrystalPalaceItalianCourt.jpg" (round-1 collection) — the loggia
arcade with the Gaillon fountain and a Medici tomb in front of it,
identified as the 1856 guide's Renaissance Court by the guide's own
contents list (p.97: the fountain "from the Chateau de Gaillon" in
the centre of the court; the lunettes "under the ceiling of the
small loggia, or gallery"). The guide (pp.95-99) describes the
court as an assemblage of copied exhibits; no prototype for the
arcade itself is named in the pages consulted, so the bay is
modelled from the photograph.

The module spans pier-centre to pier-centre: the end piers are
HALF piers carrying HALF pilasters, cut at the module edges, so
copies placed side by side at the 3.80 m pitch compose full piers
with full Ionic pilasters, and the entablature bands continue.

This court was a VICTORIAN reproduction (the Fine Arts Courts were
directed by Matthew Digby Wyatt) — plaster-and-timber readings of
Renaissance originals assembled in south London in 1854, not
archaeological Renaissance building. See NOTES.md.
"""
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "sy-renaissance-arch-fragment"

# ---------------------------------------------------------------------------
# Dimensions (metres). See NOTES.md for the derivation of every group.
#
# FORM (from the stereograph): round arch between piers; an Ionic
# pilaster centred on each pier, rising past the arch springing to a
# full entablature (two-fascia architrave, carved frieze, cornice);
# a patera roundel in each spandrel flanking the pilaster at capital
# height; moulded imposts at the springings; a plain panelled attic
# course above the cornice (the base of the upper gallery wall).
# PROPORTIONS measured on the stereograph's left eye by visual
# grounding (perspective-corrected with the arch itself: apparent
# span / 2x rise = 0.970 foreshortening):
#   arch span / bay pitch = 0.744 (apparent) -> 0.76 corrected
#   (adopted 2.90 / 3.80 = 0.763)
#   pilaster width / pitch ~ 0.13 ; floor->cornice / pitch ~ 1.78
# ABSOLUTE SIZE is an ESTIMATE (+/-20%): anchored on the cast of
# Michelangelo's Lorenzo de' Medici (seated height 1.78 m) on the
# tomb in front of the arcade in the same photograph (165 px/m at
# the tomb's depth), giving pitch 3.81 m and span 2.91 m.
# No dimension is printed in any source used.
# ---------------------------------------------------------------------------
BAY_W = 3.80            # pier centre to pier centre
HALF_W = BAY_W / 2.0
WALL_F = -0.30          # wall front plane (front is -y)
WALL_B = 0.30           # wall back plane

ZS = 3.72               # arch springing line
R_IN = 1.45             # arch intrados radius (span 2.90)

# Vertical stack (z) — cornice top measured ~6.77-6.87 m; the
# archivolt/architrave junction is set so the archivolt crown dies
# just under the architrave, as the photograph shows.
ARCHITRAVE_Z = 5.50     # underside of architrave = abacus top
FRIEZE_Z0, FRIEZE_Z1 = 5.85, 6.42
CORNICE_TOP = 6.87
TOTAL_H = 7.17          # top of the attic course (cut)

PALE = (0.615, 0.58, 0.515)     # mouldings, capitals, archivolt
MID = (0.45, 0.415, 0.365)      # wall, piers, pilaster shafts
MID_DARK = (0.355, 0.325, 0.285)  # panel fields, shaft frame lines

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

def mat_solid(name, rgb, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

def signed_volume(me):
    me.calc_loop_triangles()
    vol = 0.0
    for tri in me.loop_triangles:
        v = [me.vertices[i].co for i in tri.vertices]
        vol += v[0].dot(v[1].cross(v[2])) / 6.0
    return vol

def flip_mesh_faces(ob):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bm.to_mesh(ob.data)
    bm.free()

def finish_mesh(name, verts, faces, coll, mat, smooth=False):
    """Build a mesh from pydata; winding is construction-consistent,
    so orientation is fixed deterministically by the signed-volume
    test (flip ALL faces if negative)."""
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if signed_volume(me) < 0:
        flip_mesh_faces(ob)
    if mat:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return ob

def box_obj(name, size, loc, coll, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

def prism_xz(name, outline, y0, y1, coll, mat):
    """Extrude a simple (x, z) outline polygon between y0 (back) and
    y1 (front) into a closed prism."""
    n = len(outline)
    verts = [(x, y0, z) for (x, z) in outline] + \
            [(x, y1, z) for (x, z) in outline]
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return finish_mesh(name, verts, faces, coll, mat)

def prism_yz(name, outline, x0, x1, coll, mat):
    """Extrude a simple (y, z) outline polygon between x0 and x1."""
    n = len(outline)
    verts = [(x0, y, z) for (y, z) in outline] + \
            [(x1, y, z) for (y, z) in outline]
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return finish_mesh(name, verts, faces, coll, mat)

def prim(name, coll, mat, op, loc, **kw):
    """Create a bpy.ops primitive at the origin (rotation/scale
    baked), then place it by object location (unit scale kept)."""
    op(location=(0, 0, 0), **kw)
    ob = bpy.context.active_object
    ob.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ob.location = loc
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

def disc(name, r, depth, loc, coll, mat, verts=28):
    return prim(name, coll, mat, bpy.ops.mesh.primitive_cylinder_add,
                loc, vertices=verts, radius=r, depth=depth,
                rotation=(math.pi / 2, 0, 0))

def taper_prism(name, s, u0, u1a, u1b, yf0, yf1, yb, z0, z1, coll, mat):
    """A prism against the pier at module edge s (+1 right, -1
    left): u measured from the pier centre toward the bay centre;
    the section tapers from u1a (at z0) to u1b (at z1); the outer
    face (u=0) stays on the module edge plane x = s*HALF_W."""
    def X(u):
        return s * (HALF_W - u)
    # 8 verts: bottom ring (z0, width u1a) + top ring (z1, width u1b)
    vb = [(X(u0), yf0, z0), (X(u1a), yf0, z0), (X(u1a), yb, z0),
          (X(u0), yb, z0)]
    vt = [(X(u0), yf1, z1), (X(u1b), yf1, z1), (X(u1b), yb, z1),
          (X(u0), yb, z1)]
    verts = vb + vt
    faces = [(0, 1, 2, 3),          # bottom
             (4, 7, 6, 5),          # top (reversed vs bottom)
             (0, 4, 5, 1),          # front
             (2, 6, 7, 3),          # back
             (1, 5, 6, 2),          # inner (tapered) face
             (3, 7, 4, 0)]          # module-edge face
    return finish_mesh(name, verts, faces, coll, mat)

def ubox(name, s, uc, uw, y0, y1, z0, z1, coll, mat):
    """Box against pier s, centred at u=uc with u-width uw."""
    cx = s * (HALF_W - uc)
    return box_obj(name, (uw, y1 - y0, z1 - z0),
                   (cx, (y0 + y1) / 2, (z0 + z1) / 2), coll, mat)

def arch_band_outline(r_in, r_out, z_spring, drop, n=30):
    """(x, z) outline of a semicircular arch band (annulus half-ring
    with optional vertical drops at the springings)."""
    pts = [(-r_in, z_spring - drop), (-r_in, z_spring)]
    for k in range(1, n):
        th = math.pi - (k / n) * math.pi
        pts.append((r_in * math.cos(th), z_spring + r_in * math.sin(th)))
    pts.append((r_in, z_spring))
    pts.append((r_in, z_spring - drop))
    pts.append((r_out, z_spring - drop))
    pts.append((r_out, z_spring))
    for k in range(1, n):
        th = (k / n) * math.pi
        pts.append((r_out * math.cos(th), z_spring + r_out * math.sin(th)))
    pts.append((-r_out, z_spring))
    pts.append((-r_out, z_spring - drop))
    return pts

# ---------------------------------------------------------------------------
def build_pilaster(coll, mats, s):
    """Half pilaster + half pier at module edge s, cut at x=s*HALF_W.
    u = distance from the pier centre toward the bay centre."""
    tag = "L" if s < 0 else "R"
    # --- pier body and base (pier half-width 0.45) ---
    # QC (rev 2): the parts stacked at the module edge PARTITION the
    # (y, z) plane of the cut face without volume overlap — in rev 1
    # the pier box ran z 0->ZS straight through the base steps and
    # the pilaster was embedded 20 mm into the pier front, so pairs
    # of EXPOSED faces shared the x=+/-HALF_W plane and Cycles
    # rendered the coincident faces black (proven by isolation:
    # the base boxes alone render clean; with the pier present the
    # overlapped band goes black under sun-only and fill-only
    # alike). Parts now butt at shared planes instead of
    # interpenetrating across the cut plane.
    ubox(f"Pier{tag}", s, 0.225, 0.45, WALL_F, WALL_B, 0.24, ZS,
         coll, mats["mid"])
    ubox(f"Pier{tag}Base1", s, 0.255, 0.51, -0.37, WALL_B, 0.0, 0.14,
         coll, mats["pale"])
    ubox(f"Pier{tag}Base2Rear", s, 0.24, 0.48, WALL_F, WALL_B,
         0.14, 0.24, coll, mats["pale"])
    ubox(f"Pier{tag}Base2Front", s, 0.38, 0.20, -0.345, WALL_F,
         0.14, 0.24, coll, mats["pale"])
    # --- impost at the springing (inner side + front cap strip) ---
    ubox(f"Impost{tag}Block", s, 0.45, 0.14, -0.305, 0.05, 3.42, 3.60,
         coll, mats["pale"])
    ubox(f"Impost{tag}Cap", s, 0.45, 0.18, -0.315, 0.05, 3.60, ZS,
         coll, mats["pale"])
    ubox(f"Impost{tag}Front", s, 0.225, 0.45, -0.34, WALL_F, 3.60, ZS,
         coll, mats["pale"])
    # --- pilaster (half; full width = 2x the u extents). The
    # plinth stands on the pier's base step; all pilaster parts
    # butt the pier front plane (back at WALL_F) instead of
    # embedding into it ---
    ubox(f"Pil{tag}Plinth", s, 0.14, 0.28, -0.385, WALL_F, 0.14, 0.31,
         coll, mats["pale"])
    ubox(f"Pil{tag}Base", s, 0.1325, 0.265, -0.375, WALL_F, 0.31, 0.38,
         coll, mats["pale"])
    taper_prism(f"Pil{tag}Shaft", s, 0.0, 0.25, 0.2175,
                -0.37, -0.37, WALL_F, 0.38, 5.10, coll, mats["mid"])
    # shaft panel frame (inner strip + rails; the outer strip is
    # contributed by the neighbouring module when tiled). The rails
    # stop 6 mm short of the module edge so their end faces are not
    # coplanar with the shaft's cut face.
    ubox(f"Pil{tag}FrameStrip", s, 0.17, 0.03, -0.378, -0.364,
         0.55, 4.75, coll, mats["dark"])
    ubox(f"Pil{tag}FrameTop", s, 0.0945, 0.177, -0.378, -0.364,
         4.75, 4.79, coll, mats["dark"])
    ubox(f"Pil{tag}FrameBot", s, 0.0945, 0.177, -0.378, -0.364,
         0.51, 0.55, coll, mats["dark"])
    # --- Ionic capital (half): necking, echinus flare, bolster,
    # one volute (the pair composes when tiled), abacus ---
    ubox(f"Pil{tag}Necking", s, 0.1125, 0.225, -0.375, WALL_F,
         5.10, 5.16, coll, mats["pale"])
    taper_prism(f"Pil{tag}Echinus", s, 0.0, 0.23, 0.29,
                -0.375, -0.40, WALL_F, 5.16, 5.32, coll, mats["pale"])
    # bolster stops 8 mm short of the module edge (rev 1's end cap
    # was coplanar with the echinus cut face and rendered black)
    prim(f"Pil{tag}Bolster", coll, mats["pale"],
         bpy.ops.mesh.primitive_cylinder_add,
         (s * (HALF_W - 0.1215), -0.385, 5.24),
         vertices=20, radius=0.055, depth=0.227,
         rotation=(0, math.pi / 2, 0))
    vx = s * (HALF_W - 0.235)
    disc(f"Pil{tag}Volute", 0.088, 0.05, (vx, -0.40, 5.24),
         coll, mats["pale"])
    disc(f"Pil{tag}VoluteRing", 0.057, 0.064, (vx, -0.403, 5.24),
         coll, mats["pale"], verts=20)
    disc(f"Pil{tag}VoluteBoss", 0.026, 0.08, (vx, -0.408, 5.24),
         coll, mats["pale"], verts=16)
    ubox(f"Pil{tag}Abacus", s, 0.1525, 0.305, -0.415, WALL_F,
         5.32, 5.44, coll, mats["pale"])
    ubox(f"Pil{tag}AbacusTop", s, 0.145, 0.29, -0.40, WALL_F,
         5.44, ARCHITRAVE_Z, coll, mats["pale"])

def main():
    clean_scene()
    model = make_collection("Model")
    setup = make_collection("RenderSetup")
    mats = {
        "pale": mat_solid("CourtStone_PalePlaster", PALE, 0.92),
        "mid": mat_solid("CourtWall_MidTone", MID, 0.95),
        "dark": mat_solid("CourtInset_Dark", MID_DARK, 0.95),
    }

    build_pilaster(model, mats, -1)
    build_pilaster(model, mats, +1)

    # --- spandrel wall: full module width, arch hole at R_IN ---
    outline = [(-HALF_W, ZS), (-R_IN, ZS)]
    for k in range(1, 30):
        th = math.pi - (k / 30) * math.pi
        outline.append((R_IN * math.cos(th), ZS + R_IN * math.sin(th)))
    outline += [(R_IN, ZS), (HALF_W, ZS), (HALF_W, ARCHITRAVE_Z),
                (-HALF_W, ARCHITRAVE_Z)]
    prism_xz("SpandrelWall", outline, WALL_B, WALL_F, model, mats["mid"])

    # --- archivolt: wide fascia band with a drop to the imposts,
    # plus a raised outer roll (radii stepped 5-10 mm off the
    # neighbouring surfaces so no two faces are coincident).
    # Rev 2: the ROLL is the proudest line (front -0.38), the
    # fascia sits behind it (front -0.35) — the photograph shows
    # the outer roll as the strongest archivolt line; rev 1 had
    # the prominence the wrong way round ---
    prism_xz("ArchivoltBand",
             arch_band_outline(1.44, 1.68, ZS, 0.28),
             -0.275, -0.35, model, mats["pale"])
    prism_xz("ArchivoltRoll",
             arch_band_outline(1.672, 1.75, ZS, 0.0),
             -0.28, -0.38, model, mats["pale"])

    # --- spandrel roundels (paterae): ring + boss, one per
    # spandrel, flanking the pilasters at capital height ---
    for s in (-1, +1):
        tag = "L" if s < 0 else "R"
        cx = s * (HALF_W - 0.45)
        disc(f"Roundel{tag}", 0.17, 0.035, (cx, -0.3175, 5.24),
             model, mats["pale"])
        disc(f"Roundel{tag}Ring", 0.115, 0.05, (cx, -0.325, 5.24),
             model, mats["pale"], verts=24)
        disc(f"Roundel{tag}Boss", 0.052, 0.065, (cx, -0.3325, 5.24),
             model, mats["pale"], verts=20)

    # --- entablature (full-width bands; butt at the module edges
    # and continue across tiled copies) ---
    box_obj("ArchitraveF1", (BAY_W, 0.635, 0.17), (0, -0.0175, 5.585),
            model, mats["pale"])
    box_obj("ArchitraveF2", (BAY_W, 0.665, 0.18), (0, -0.0325, 5.76),
            model, mats["pale"])
    box_obj("FriezeGround", (BAY_W, 0.625, FRIEZE_Z1 - FRIEZE_Z0),
            (0, -0.0125, (FRIEZE_Z0 + FRIEZE_Z1) / 2), model, mats["mid"])
    # beads: proud front strips on the frieze ground, stopping
    # 4 mm short of the module edges (rev 1 ran them full width
    # through the ground box, and their coincident end faces
    # rendered as black lines)
    box_obj("FriezeBeadB", (BAY_W - 0.008, 0.032, 0.05),
            (0, -0.334, 5.895), model, mats["pale"])
    box_obj("FriezeBeadT", (BAY_W - 0.008, 0.032, 0.05),
            (0, -0.334, 6.375), model, mats["pale"])
    # a thin running stem at frieze centre height, tying the
    # relief motifs together as the carved rinceaux vine of the
    # photograph (the motifs themselves stay simplified)
    box_obj("FriezeStem", (BAY_W - 0.008, 0.032, 0.045),
            (0, -0.334, (FRIEZE_Z0 + FRIEZE_Z1) / 2),
            model, mats["pale"])
    # frieze relief — a SIMPLIFIED stand-in for the carved rinceaux
    # frieze of the photograph (central medallion, ring scrolls,
    # leaves, small discs); see NOTES.md
    fz = (FRIEZE_Z0 + FRIEZE_Z1) / 2
    disc("FriezeMedallion", 0.15, 0.045, (0, -0.3475, fz),
         model, mats["pale"], verts=32)
    disc("FriezeMedallionBoss", 0.065, 0.06, (0, -0.355, fz),
         model, mats["pale"], verts=20)
    for s in (-1, +1):
        tag = "L" if s < 0 else "R"
        prim(f"FriezeScroll{tag}", model, mats["pale"],
             bpy.ops.mesh.primitive_torus_add,
             (s * 0.95, -0.345, fz),
             major_radius=0.10, minor_radius=0.026,
             major_segments=24, minor_segments=10,
             rotation=(math.pi / 2, 0, 0))
        disc(f"FriezeScroll{tag}Dot", 0.04, 0.05, (s * 0.95, -0.35, fz),
             model, mats["pale"], verts=16)
        prim(f"FriezeLeaf{tag}", model, mats["pale"],
             bpy.ops.mesh.primitive_cone_add,
             (s * 0.52, -0.34, fz),
             vertices=16, radius1=0.055, radius2=0.0, depth=0.17,
             rotation=(0, s * math.pi / 2, 0))
        # squash the leaf in depth after rotation is baked
        leaf = bpy.context.active_object
        leaf.scale = (1.0, 0.45, 1.0)
        bpy.ops.object.transform_apply(location=False, rotation=False,
                                       scale=True)
        disc(f"FriezeDisc{tag}", 0.048, 0.04, (s * 1.48, -0.345, fz),
             model, mats["pale"], verts=20)
    # --- cornice: bedmould, corona, sloped crown ---
    box_obj("CorniceBed", (BAY_W, 0.69, 0.12), (0, -0.045, 6.48),
            model, mats["pale"])
    box_obj("CorniceCorona", (BAY_W, 0.75, 0.20), (0, -0.075, 6.64),
            model, mats["pale"])
    prism_yz("CorniceCrown",
             [(-0.45, 6.74), (-0.36, CORNICE_TOP), (WALL_B, CORNICE_TOP),
              (WALL_B, 6.74)],
             -HALF_W, HALF_W, model, mats["pale"])
    # --- attic course (base of the upper gallery wall, cut) ---
    box_obj("Attic", (BAY_W, 0.615, TOTAL_H - CORNICE_TOP),
            (0, -0.0075, (CORNICE_TOP + TOTAL_H) / 2), model, mats["mid"])
    box_obj("AtticPanelT", (2.42, 0.025, 0.035), (0, -0.3225, 7.1325),
            model, mats["dark"])
    box_obj("AtticPanelB", (2.42, 0.025, 0.035), (0, -0.3225, 6.9075),
            model, mats["dark"])
    box_obj("AtticPanelL", (0.035, 0.025, 0.19), (-1.2125, -0.3225, 7.02),
            model, mats["dark"])
    box_obj("AtticPanelR", (0.035, 0.025, 0.19), (1.2125, -0.3225, 7.02),
            model, mats["dark"])

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
    bpy.ops.object.light_add(type="AREA", location=(6, -6, 7))
    fill = bpy.context.active_object
    fill.data.energy = 500
    fill.data.shape = "DISK"; fill.data.size = 8
    for c in fill.users_collection:
        c.objects.unlink(fill)
    setup.objects.link(fill)

    def look_at(ob, target):
        ob.rotation_euler = (Vector(target) - ob.location).to_track_quat("-Z", "Y").to_euler()

    look_at(fill, (0, 0, 3.2))

    def add_cam(name, loc, tgt, lens=50):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.active_object
        cam.name = "Cam" + name
        cam.data.lens = lens
        look_at(cam, tgt)
        for c in cam.users_collection:
            c.objects.unlink(cam)
        setup.objects.link(cam)
        return cam

    cams = {
        "front": add_cam("Front", (0, -17, 4.0), (0, 0, 3.45)),
        "side": add_cam("Side", (17, 0, 4.0), (0, 0, 3.45)),
        "three-quarter": add_cam("ThreeQuarter", (11, -11, 6.0),
                                 (0, 0, 3.2)),
    }

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

    bpy.ops.object.select_all(action="DESELECT")
    for ob in model.objects:
        ob.select_set(True)
    out_glb = os.path.join(ROOT, SLUG + ".glb")
    bpy.ops.export_scene.gltf(filepath=out_glb, export_format="GLB",
                              use_selection=True, export_apply=True)
    print("exported", out_glb)

    tris = 0
    xs, ys, zs = [], [], []
    for ob in model.objects:
        if ob.type == "MESH":
            tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
            for corner in ob.bound_box:
                w = ob.matrix_world @ Vector(corner)
                xs.append(w.x); ys.append(w.y); zs.append(w.z)
    print(f"OBJECTS {len(model.objects)} TRIS {tris}")
    print(f"BBOX x {min(xs):.2f}..{max(xs):.2f}  y {min(ys):.2f}.."
          f"{max(ys):.2f}  z {min(zs):.2f}..{max(zs):.2f}")

    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(ROOT, "renders", name + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath)

    # ---- tiled view: three-bay proof composed from COPIES ONLY ----
    # Defect found in review (see NOTES.md QC): rendering the original
    # module objects alongside visible duplicates of themselves makes
    # the ORIGINALS shade dark-to-black in Cycles in this file
    # (empirical artefact — not mirroring, normals or materials: the
    # module alone renders clean, and copies alone render clean).
    # So the proof is built from three full copies at -pitch/0/+pitch
    # with the originals removed. In-memory only: the saved .blend
    # (written above) and the .glb keep the single module.
    origs = list(model.objects)
    copies = []
    for dx in (-BAY_W, 0.0, BAY_W):
        for ob in origs:
            d = ob.copy()
            d.data = ob.data.copy()
            d.location.x += dx
            model.objects.link(d)
            copies.append(d)
    for ob in origs:
        bpy.data.objects.remove(ob, do_unlink=True)
    tcam = add_cam("Tiled", (14, -15, 6.4), (0, 0, 3.1))
    scene.camera = tcam
    scene.render.filepath = os.path.join(ROOT, "renders",
                                         "tiled-three-quarter.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", scene.render.filepath)
    for d in copies:
        bpy.data.objects.remove(d, do_unlink=True)
    bpy.data.objects.remove(tcam, do_unlink=True)

if __name__ == "__main__":
    main()
