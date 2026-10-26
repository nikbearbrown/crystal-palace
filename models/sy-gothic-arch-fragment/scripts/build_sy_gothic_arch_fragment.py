#!/usr/bin/env python3
"""Build sy-gothic-arch-fragment — one repeatable bay of the Sydenham
English Mediaeval Court's cloister arcade (1854), the arcade the 1856
guide says was "founded in its arches and columns on the Abbey of
Guisborough, Yorkshire" (p.89, with the captioned woodcut "Arcade
from Guisborough"), cross-checked against the guide's "Elevation of
English Medieval Court towards the cloister" (p.92) and the
Rijksmuseum photograph of the French and Italian Mediaeval Vestibule
(RP-F-2012-96-334) for capital character and shaft material.

Run:  blender -b -P build_sy_gothic_arch_fragment.py

The module spans pier-centre to pier-centre: two pointed lights on
slender shafts under one moulded containing arch, a quatrefoil
panel in the spandrel, and the quatrefoil frieze band above a string
course. The end piers are HALF clusters (cut at the module edge), so
copies placed side by side compose full clustered piers.

These courts were VICTORIAN reproductions (the English Mediaeval
Court was designed under M. Digby Wyatt's direction of the Fine Arts
Courts) — plaster-and-timber readings of medieval originals, made in
south London in 1854. Not archaeological Gothic. See NOTES.md.
"""
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "sy-gothic-arch-fragment"

# ---------------------------------------------------------------------------
# Dimensions (metres). See NOTES.md for the derivation of every group.
#
# FORM (from the guide's Guisborough woodcut, p.89, and the cloister
# elevation, p.92): two lights per bay under one containing arch;
# quatrefoil panel centred in the spandrel; frieze of square
# quatrefoil panels above; clustered jamb shafts; foliate bell
# capitals with round abaci (photograph RP-F-2012-96-334).
# PROPORTIONS measured on the woodcuts (visual grounding, +/-10%):
#   light width (incl. its mouldings) / bay width  = 0.37
#   frieze band height / arcade height             ~ 0.13
# ABSOLUTE SIZE is an ESTIMATE (+/-20%): anchored on the vestibule
# photograph, where the great arch spans ~2.7 m against busts on
# pedestals (~1.65 m combined), and on human-scale cloister practice.
# No dimension is printed in any source used.
# ---------------------------------------------------------------------------
BAY_W = 2.40            # pier centre to pier centre
HALF_W = BAY_W / 2.0
WALL_BACK = 0.15        # wall/arch back plane (y)
PLINTH_H = 0.15
PLINTH_D = 0.68         # plinth slab depth, centred y=-0.02 (front is -y)

# Pier cluster (full plan): main shaft + 2 side shafts + 1 front shaft
PIER_R = 0.14
SIDE_R = 0.09
SIDE_DX = 0.205
FRONT_R = 0.09
FRONT_DY = -0.205       # front is -y
MULL_R = 0.085          # central mullion shaft

ZS_LIGHT = 2.05         # light springing = side/mullion capital top
ZS_CONT = 2.15          # containing-arch springing = main capital top

# Light arch (two-centred): support centres at x=0 and x=+/-0.995
LIGHT_CX = 0.4975
LIGHT_R = 0.60          # radius; half-span = R - off = 0.4975
# Containing arch (two-centred) across the full bay
CONT_R = 1.32           # radius; half-span = R - off = 1.20

STRING_Z0, STRING_Z1 = 3.78, 3.86
FRIEZE_Z0, FRIEZE_Z1 = 3.86, 4.22
TOTAL_H = 4.32          # cornice top

STONE = (0.60, 0.56, 0.485)
STONE_DARK = (0.47, 0.435, 0.375)
SHAFT_DARK = (0.145, 0.125, 0.11)

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

def finish_mesh(name, verts, faces, coll, mat, smooth=False, orient="volume"):
    """Build a mesh from pydata. The face construction in this script
    is winding-consistent, so orientation is fixed deterministically:
    for a closed solid, flip ALL faces if the signed volume is
    negative. (bmesh recalc_face_normals was tried first and left
    individual faces flipped on these prisms — do not use it here.)
    orient="none" leaves direction to the caller (lathes test
    radially against their axis)."""
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if orient == "volume" and signed_volume(me) < 0:
        flip_mesh_faces(ob)
    if mat:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return ob

def lathe_obj(name, profile, coll, mat, centre=(0.0, 0.0), segments=48,
              phi_start=0.0, phi_len=2 * math.pi, lobe_n=0, lobe_z=None,
              lobe_amp=0.0):
    """profile: list of (r, z). Lathe around the vertical axis through
    `centre`. phi measured from +x axis. Optional radial lobing applied
    only to rings whose z is inside lobe_z=(z0, z1) (the capital bell).
    Returns object with world-space geometry, unit scale."""
    rings = len(profile)
    closed = abs(phi_len - 2 * math.pi) < 1e-9
    verts = []
    for (r, z) in profile:
        amp = 0.0
        if lobe_n and lobe_z and lobe_z[0] <= z <= lobe_z[1]:
            # fade lobing in/out across the bell zone
            t = (z - lobe_z[0]) / max(1e-6, (lobe_z[1] - lobe_z[0]))
            amp = lobe_amp * math.sin(math.pi * min(1.0, max(0.0, t)))
        for j in range(segments + (0 if closed else 1)):
            phi = phi_start + phi_len * (j / segments)
            rr = r * (1.0 + amp * math.cos(lobe_n * phi)) if amp else r
            verts.append((centre[0] + rr * math.cos(phi),
                          centre[1] + rr * math.sin(phi), z))
    cols = segments if closed else segments + 1
    faces = []
    for i in range(rings - 1):
        for j in range(segments):
            a = i * cols + j
            b = i * cols + (j + 1) % cols if closed else i * cols + j + 1
            faces.append((a, b, b + cols, a + cols))
    if not closed:
        # cap the cut plane of a partial (demi) lathe with a flat
        # strip through the axis, so the solid is closed; the winding
        # (a0, a1, b1, b0) keeps every shared edge opposed to the
        # tube faces on both sides
        for i in range(rings - 1):
            a0 = i * cols
            a1 = (i + 1) * cols
            b0 = i * cols + segments
            b1 = (i + 1) * cols + segments
            faces.append((a0, a1, b1, b0))
    ob = finish_mesh(name, verts, faces, coll, mat, smooth=True,
                     orient="none")
    # orientation test for a lathe: face normals should point away
    # from the axis on average; flip if the build wound them inward
    score = 0.0
    for p in ob.data.polygons:
        c = p.center
        radial = (c.x - centre[0], c.y - centre[1], 0.0)
        score += p.normal.x * radial[0] + p.normal.y * radial[1]
    if score < 0:
        flip_mesh_faces(ob)
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
    faces.append(tuple(range(n - 1, -1, -1)))            # back ngon
    faces.append(tuple(range(n, 2 * n)))                 # front ngon
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return finish_mesh(name, verts, faces, coll, mat)

def arch_outline(cx, zs, R, off, w, drop=0.0, n=22):
    """Outline (x, z) of one arch band: intrados from left springing
    over apex to right springing, then extrados back. The two arc
    centres sit on the springing line at cx +/- off, so the
    half-span is R - off. Concentric orders MUST share the same
    `off` (same centres) and differ only in R — passing a constant
    half-span instead makes the orders cross each other."""
    hs = R - off
    rise = math.sqrt(R * R - off * off)
    intra, extra = [], []
    for k in range(n + 1):                      # left half: spring->apex
        t = k / n
        ang = math.pi - t * (math.pi - math.atan2(rise, -off))
        # centre of left arc is at (cx + off, zs)
        intra.append((cx + off + R * math.cos(ang), zs + R * math.sin(ang)))
        extra.append((cx + off + (R + w) * math.cos(ang),
                      zs + (R + w) * math.sin(ang)))
    # right half: mirror the left half about x = cx
    left_i = intra[:]
    left_e = extra[:]
    right_i = [(2 * cx - x, z) for (x, z) in reversed(left_i)]
    right_e = [(2 * cx - x, z) for (x, z) in reversed(left_e)]
    intra = left_i + right_i[1:]
    extra = left_e + right_e[1:]
    pts = []
    if drop > 0:
        pts.append((intra[0][0], zs - drop))
    pts += intra
    if drop > 0:
        pts.append((intra[-1][0], zs - drop))
        pts.append((extra[-1][0], zs - drop))
    pts += list(reversed(extra))
    if drop > 0:
        pts.append((extra[0][0], zs - drop))
    return pts

def clip_outline_x(pts, lo, hi):
    """Sutherland-Hodgman clip of an (x, z) polygon to lo <= x <= hi.
    Used to cut arch bands cleanly at a vertical plane (module edge,
    mullion face) instead of letting concentric orders overhang."""
    def clip(poly, keep_lo):
        out = []
        if not poly:
            return out
        prev = poly[-1]
        prev_in = (prev[0] >= lo) if keep_lo else (prev[0] <= hi)
        lim = lo if keep_lo else hi
        for cur in poly:
            cur_in = (cur[0] >= lo) if keep_lo else (cur[0] <= hi)
            if cur_in != prev_in:
                t = (lim - prev[0]) / (cur[0] - prev[0])
                out.append((lim, prev[1] + t * (cur[1] - prev[1])))
            if cur_in:
                out.append(cur)
            prev, prev_in = cur, cur_in
        return out
    return clip(clip(pts, True), False)

def shaft_profiles(r, z_spring, bell_h, z0=0.26):
    """Return (base_profile, shaft_profile, capital_profile) for one
    shaft of radius r whose capital top (springing) is at z_spring.
    The base starts at z0 (top of the shaft's plinth block, embedded
    0.02 into it)."""
    z_neck = z_spring - bell_h
    base = [(r * 1.5, z0), (r * 1.5, z0 + 0.04),
            (r * 1.22, z0 + 0.08), (r * 1.06, z0 + 0.13),
            (r * 1.20, z0 + 0.17), (r * 1.02, z0 + 0.20)]
    shaft = [(r * 1.02, z0 + 0.18), (r * 0.97, z0 + 0.26),
             (r * 0.94, (z0 + z_neck) / 2.0), (r * 0.92, z_neck - 0.05),
             (r * 1.08, z_neck - 0.015), (r * 1.10, z_neck + 0.02)]
    bell_r = r * 1.62
    cap = [(r * 1.10, z_neck), (r * 0.96, z_neck + 0.03),
           (r * 1.08, z_neck + bell_h * 0.35),
           (r * 1.38, z_neck + bell_h * 0.70),
           (bell_r, z_neck + bell_h * 0.92),
           (bell_r * 1.05, z_spring - 0.045),
           (bell_r * 1.10, z_spring - 0.02),
           (bell_r * 1.10, z_spring), (0.0, z_spring)]
    return base, shaft, cap, (z_neck + bell_h * 0.25, z_neck + bell_h * 0.95)

def build_shaft(coll, mats, name, cx, cy, r, z_spring, bell_h,
                phi_start=0.0, phi_len=2 * math.pi, segments=40):
    base, shaft, cap, lobe_z = shaft_profiles(r, z_spring, bell_h)
    lathe_obj(name + "_Base", base, coll, mats["stone"], centre=(cx, cy),
              segments=segments, phi_start=phi_start, phi_len=phi_len)
    lathe_obj(name + "_Shaft", shaft, coll, mats["shaft"], centre=(cx, cy),
              segments=segments, phi_start=phi_start, phi_len=phi_len)
    lathe_obj(name + "_Capital", cap, coll, mats["stone"], centre=(cx, cy),
              segments=segments, phi_start=phi_start, phi_len=phi_len,
              lobe_n=8, lobe_z=lobe_z, lobe_amp=0.09)

def build_pier(coll, mats, side):
    """Half-cluster pier at x = side*HALF_W, cut at the module edge.
    side=-1: left pier, kept half is x >= -HALF_W (phi -90..90 deg
    around each shaft centre gives the +x half)."""
    s = side
    px = s * HALF_W
    # octagonal plinth block (half, flat-topped), on the plinth slab
    lathe_obj(f"Pier{ 'L' if s<0 else 'R'}_Plinth",
              [(0.37, PLINTH_H), (0.37, PLINTH_H + 0.13),
               (0.0, PLINTH_H + 0.13)],
              coll, mats["stone"], centre=(px, 0.0), segments=8,
              phi_start=(-math.pi / 2 if s < 0 else math.pi / 2),
              phi_len=math.pi)
    phi0 = -math.pi / 2 if s < 0 else math.pi / 2
    # main demi-shaft -> containing-arch springing
    build_shaft(coll, mats, f"Pier{'L' if s<0 else 'R'}Main", px, 0.0,
                PIER_R, ZS_CONT, 0.28, phi_start=phi0, phi_len=math.pi)
    # inner side shaft (full) -> light springing
    build_shaft(coll, mats, f"Pier{'L' if s<0 else 'R'}Side",
                px - s * SIDE_DX, 0.0, SIDE_R, ZS_LIGHT, 0.22)
    # front demi-shaft -> rises with the main shaft
    build_shaft(coll, mats, f"Pier{'L' if s<0 else 'R'}Front",
                px, FRONT_DY, FRONT_R, ZS_CONT, 0.28,
                phi_start=phi0, phi_len=math.pi)
    # shared abacus slab over the cluster (half)
    ax0 = px if s < 0 else px - 0.34
    box_obj(f"Pier{'L' if s<0 else 'R'}_Abacus",
            (0.34, 0.58, 0.055), (ax0 + 0.17, 0.0, ZS_CONT - 0.0275),
            coll, mats["stone"])

def quatrefoil_mesh(name, cx, cz, size, y_face, depth, coll, mat):
    """A shallow-relief quatrefoil: 4 lobes + centre disc, merged."""
    import bmesh
    objs = []
    d = size * 0.205
    lr = size * 0.235
    for (dx, dz) in ((d, d), (d, -d), (-d, d), (-d, -d)):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=20, radius=lr, depth=depth,
            location=(cx + dx, y_face, cz + dz),
            rotation=(math.pi / 2, 0, 0))
        objs.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=size * 0.10, depth=depth * 1.05,
        location=(cx, y_face, cz), rotation=(math.pi / 2, 0, 0))
    objs.append(bpy.context.active_object)
    for ob in objs:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    ob.data.materials.append(mat)
    return ob

# ---------------------------------------------------------------------------
def main():
    clean_scene()
    model = make_collection("Model")
    setup = make_collection("RenderSetup")
    mats = {
        "stone": mat_solid("CourtStone_PalePlaster", STONE, 0.92),
        "stone_dark": mat_solid("CourtStone_Inset", STONE_DARK, 0.95),
        "shaft": mat_solid("Shaft_DarkPolished", SHAFT_DARK, 0.35),
    }

    # plinth slab (continuous, cut at module edges for tiling)
    box_obj("PlinthSlab", (BAY_W, PLINTH_D, PLINTH_H),
            (0, -0.02, PLINTH_H / 2), model, mats["stone"])

    # piers + mullion
    build_pier(model, mats, -1)
    build_pier(model, mats, +1)
    build_shaft(model, mats, "Mullion", 0.0, 0.0, MULL_R, ZS_LIGHT, 0.20)
    # mullion plinth block (flat-topped octagon)
    lathe_obj("Mullion_Plinth",
              [(0.19, PLINTH_H), (0.19, PLINTH_H + 0.13),
               (0.0, PLINTH_H + 0.13)],
              model, mats["stone"], centre=(0.0, 0.0), segments=8)

    # --- light arches: two moulded orders each (concentric: same
    # centres, off = LIGHT_R - LIGHT_CX); outlines clipped at the
    # mullion face and inside the pier side shaft so the two lights
    # never interpenetrate at the centre ---
    OFF_L = LIGHT_R - LIGHT_CX
    for s in (-1, +1):
        cx = s * LIGHT_CX
        lo, hi = (-1.04, -0.02) if s < 0 else (0.02, 1.04)
        o1 = clip_outline_x(
            arch_outline(cx, ZS_LIGHT, LIGHT_R, OFF_L, 0.085, drop=0.12),
            lo, hi)
        prism_xz(f"LightArch{'L' if s<0 else 'R'}_Order1", o1,
                 -0.02, WALL_BACK, model, mats["stone"])
        o2 = clip_outline_x(
            arch_outline(cx, ZS_LIGHT, LIGHT_R + 0.085, OFF_L, 0.075,
                         drop=0.12), lo, hi)
        prism_xz(f"LightArch{'L' if s<0 else 'R'}_Order2", o2,
                 -0.115, -0.02, model, mats["stone"])

    # --- containing arch: three moulded orders (concentric: same
    # centres, off = CONT_R - HALF_W), clipped at the module edges
    # so the bands end in clean vertical cut faces ---
    OFF_C = CONT_R - HALF_W
    c1 = clip_outline_x(arch_outline(0.0, ZS_CONT, CONT_R, OFF_C, 0.095),
                        -HALF_W, HALF_W)
    prism_xz("ContainingArch_Order1", c1, -0.06, WALL_BACK,
             model, mats["stone"])
    c2 = clip_outline_x(
        arch_outline(0.0, ZS_CONT, CONT_R + 0.095, OFF_C, 0.085),
        -HALF_W, HALF_W)
    prism_xz("ContainingArch_Order2", c2, -0.145, -0.06,
             model, mats["stone"])
    c3 = clip_outline_x(
        arch_outline(0.0, ZS_CONT, CONT_R + 0.180, OFF_C, 0.080),
        -HALF_W, HALF_W)
    prism_xz("ContainingArch_Order3", c3, -0.20, -0.145,
             model, mats["stone"])

    # --- spandrel wall above the containing arch extrados ---
    # The outline's sides run only from the extrados curve up to the
    # string course: dropping them to the springing line would
    # retrace the arch bands' own end faces (coincident opposite
    # faces — a defect caught in QC).
    off = CONT_R - HALF_W
    R3 = CONT_R + 0.26
    def extrados_z(x):
        ccx = -off if x >= 0 else off
        return ZS_CONT + math.sqrt(max(0.01, R3 * R3 - (x - ccx) ** 2))
    bottom = []
    for k in range(1, 24):
        x = HALF_W - (k / 24.0) * BAY_W
        bottom.append((x, min(extrados_z(x), STRING_Z0 - 0.02)))
    z_edge = extrados_z(HALF_W)
    outline = [(-HALF_W, z_edge), (-HALF_W, STRING_Z0),
               (HALF_W, STRING_Z0), (HALF_W, z_edge)] + bottom
    prism_xz("SpandrelWall", outline, -0.075, WALL_BACK,
             model, mats["stone"])

    # spandrel quatrefoil in a diamond panel (from the Guisborough
    # woodcut): diamond inset plate + raised quatrefoil
    dia = [(0.0, 3.02), (0.30, 3.30), (0.0, 3.58), (-0.30, 3.30)]
    prism_xz("SpandrelPanel", dia, -0.095, -0.07, model, mats["stone_dark"])
    quatrefoil_mesh("SpandrelQuatrefoil", 0.0, 3.30, 0.46, -0.105, 0.045,
                    model, mats["stone"])

    # --- string course, frieze band, cornice ---
    box_obj("StringCourse", (BAY_W, 0.36, STRING_Z1 - STRING_Z0),
            (0, -0.015, (STRING_Z0 + STRING_Z1) / 2), model, mats["stone"])
    box_obj("FriezeBand", (BAY_W, 0.27, FRIEZE_Z1 - FRIEZE_Z0),
            (0, 0.015, (FRIEZE_Z0 + FRIEZE_Z1) / 2), model, mats["stone"])
    for s in (-1, +1):
        cx = s * LIGHT_CX
        # square panel frame over each light (woodcut: one panel per
        # light), quatrefoil inside
        fw, fh, ft = 0.84, 0.30, 0.045
        zc = (FRIEZE_Z0 + FRIEZE_Z1) / 2
        box_obj(f"FriezeFrame{'L' if s<0 else 'R'}T",
                (fw, 0.03, ft), (cx, -0.125, zc + fh / 2), model, mats["stone_dark"])
        box_obj(f"FriezeFrame{'L' if s<0 else 'R'}B",
                (fw, 0.03, ft), (cx, -0.125, zc - fh / 2), model, mats["stone_dark"])
        box_obj(f"FriezeFrame{'L' if s<0 else 'R'}L",
                (ft, 0.03, fh), (cx - fw / 2, -0.125, zc), model, mats["stone_dark"])
        box_obj(f"FriezeFrame{'L' if s<0 else 'R'}R",
                (ft, 0.03, fh), (cx + fw / 2, -0.125, zc), model, mats["stone_dark"])
        quatrefoil_mesh(f"FriezeQuatrefoil{'L' if s<0 else 'R'}",
                        cx, zc, 0.27, -0.135, 0.03, model, mats["stone"])
    box_obj("Cornice1", (BAY_W, 0.33, 0.05),
            (0, -0.005, FRIEZE_Z1 + 0.025), model, mats["stone"])
    box_obj("Cornice2", (BAY_W, 0.28, 0.05),
            (0, 0.01, FRIEZE_Z1 + 0.075), model, mats["stone"])

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

    # aim the fill at the model (the exemplar's un-aimed fill points
    # straight down and leaves this prop's cut faces in darkness)
    look_at(fill, (0, 0, 2.0))

    cams = {}
    for name, loc, tgt in (
            ("Front", (0, -10.5, 2.4), (0, 0, 2.05)),
            ("Side", (10.5, 0, 2.4), (0, 0, 2.05)),
            ("ThreeQuarter", (7.2, -7.2, 3.9), (0, 0, 1.95))):
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.active_object
        cam.name = "Cam" + name
        cam.data.lens = 50
        look_at(cam, tgt)
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
