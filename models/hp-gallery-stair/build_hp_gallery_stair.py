#!/usr/bin/env python3
"""
build_hp_gallery_stair.py — Hyde Park 1851 gallery stair flight + landing
edge + gallery-pattern rail section (prop: hp-gallery-stair).

Evidence: Downes (1852) Plates II, XV, XVI, XVII and
CONTROL-DIMENSIONS.md rows D12, D27-D34 (repo nikbearbrown/crystal-palace).
Hyde Park 1851 ONLY. Units: metres. Origin at base centre of the prop
footprint, ground floor z = 0. Re-runnable:

    blender -b -P build_hp_gallery_stair.py

Outputs (next to this script): hp-gallery-stair.blend, hp-gallery-stair.glb,
renders/front.png, renders/side.png, renders/three-quarter.png
"""
import bpy, math, os
from mathutils import Vector, Matrix

IN = 0.0254

# ---------------------------------------------------------------- printed /
# plate-checked controls (CONTROL-DIMENSIONS.md) ---------------------------
RISERS_PER_FLIGHT = 21                      # D32, text p.32
TREADS = 20                                 # D32 (the landing is the 21st step)
RISE_TO_LANDING_IN = 137.5                  # D31: 11 ft 5.5 in = half of D12
RISER = RISE_TO_LANDING_IN * IN / RISERS_PER_FLIGHT   # 0.16631 m
GOING = 12.0 * IN                           # D32: treads of 1 ft
RUN = TREADS * GOING                        # 6.096 m
LANDING_Z = RISERS_PER_FLIGHT * RISER       # 3.4925 m
LANDING_DEPTH = 8.0 * 12 * IN               # D27: landing 8 ft wide (run dir.)
STRING_CC = (7 * 12 + 1) * IN               # D29: flight strings 7 ft 1 in c/c
LANDING_COL_DIA = 5.0 * IN                  # D30: landing column 5 in OD
LANDING_COL_TOP = (10 * 12 + 8) * IN        # D30: column top 10 ft 8 in
RAIL_H = (3 * 12 + 1.875) * IN              # Pl. XVII Fig.7 print: 3 ft 1 7/8 in
POST_FINIAL = 6.25 * IN                     # Pl. XVII Fig.7 print: finial 6 1/4 in

# ------------------------------------------------------- plate-measured ----
# (measured on the plate scans against their own printed dimensions;
#  see NOTES.md for the method and the residuals)
STRING_DEPTH = 0.26          # Pl. XV section: ~10 in perpendicular depth
HAND_ABOVE_NOSE = 0.855      # Pl. XV section: handrail top ~33 in vertical
                             # above the nosing line
LATTICE_PITCH = 0.25         # Pl. XVII Fig.12: diamond pitch ~9.8 in
LATTICE_PERIOD = 0.457       # Pl. XVII Fig.12: wave period ~18 in
LATTICE_AMP = 0.125          # bars cross their neighbours (antiphase)
BOSS_ROWS = (0.246, 0.474, 0.702)   # crossing heights above floor, Fig.12

# ---------------------------------------------------------------- inferred ---
TREAD_THICK = 0.045          # treads read ~2 in on Pl. XV section; 45 mm used
STRING_WEB = 0.022
STRING_FLANGE_W = 0.105
DECK_BOARD_W = 0.229         # 9 in boards (as the floor prop; not printed
                             # for the landing) - see NOTES
JOIST_D, JOIST_W = 7 * IN, 2.5 * IN   # landing joist printed Pl. XVI: 7 x 2.5

X0 = -(RUN + LANDING_DEPTH) / 2.0     # origin at base centre of footprint
SLOPE = RISER / GOING
ANG = math.atan(SLOPE)

# ---------------------------------------------------------------- materials --
def make_mats():
    def mat(name, rgb, rough=0.6, metal=0.0):
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = rough
        bsdf.inputs["Metallic"].default_value = metal
        return m
    return {
        "iron":  mat("PaintedIron", (0.80, 0.78, 0.74), 0.55, 0.10),
        "rail":  mat("TimberHandrail", (0.42, 0.30, 0.19), 0.70),
        "deck":  mat("TimberDeck", (0.72, 0.63, 0.50), 0.80),
    }
MATS = None  # set in main

# ------------------------------------------------------------- batch mesh ----
class Batch:
    """Accumulates boxes / octahedra into one mesh with identity transform."""
    def __init__(self):
        self.verts = []
        self.faces = []
    def _quad(self, a, b, c, d):
        base = len(self.verts)
        self.verts += [a, b, c, d]
        self.faces.append((base, base + 1, base + 2, base + 3))
    def box(self, centre, basis, size):
        """basis: (a, b, c) orthonormal Vectors = local x/y/z axes."""
        a, b, c = basis
        cx, cy, cz = centre
        hx, hy, hz = (s / 2.0 for s in size)
        P = lambda i, j, k: Vector((cx, cy, cz)) + a * i * hx + b * j * hy + c * k * hz
        v = [P(-1, -1, -1), P(1, -1, -1), P(1, 1, -1), P(-1, 1, -1),
             P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)]
        base = len(self.verts)
        self.verts += v
        for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                  (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            self.faces.append(tuple(base + i for i in f))
    def box_xyz(self, centre, size):
        self.box(centre, (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))), size)
    def bar(self, p1, p2, width, thick, normal):
        """Box from p1 to p2; width measured in the plane normal to `normal`."""
        d = (p2 - p1)
        L = d.length
        d.normalize()
        w = normal.cross(d)
        w.normalize()
        mid = (p1 + p2) / 2.0
        self.box(mid, (d, w, normal), (L, width, thick))
    def octa(self, centre, hx, hy, hz):
        cx, cy, cz = centre
        base = len(self.verts)
        self.verts += [Vector((cx + hx, cy, cz)), Vector((cx - hx, cy, cz)),
                       Vector((cx, cy + hy, cz)), Vector((cx, cy - hy, cz)),
                       Vector((cx, cy, cz + hz)), Vector((cx, cy, cz - hz))]
        for f in [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4),
                  (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]:
            self.faces.append(tuple(base + i for i in f))
    def build(self, name, material, collection):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.verts, [], self.faces)
        me.update()
        ob = bpy.data.objects.new(name, me)
        collection.objects.link(ob)
        if material:
            me.materials.append(material)
        import bmesh
        bm = bmesh.new(); bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me); bm.free()
        return ob

def lathe(name, profile, material, collection, location, segments=24):
    """profile: list of (radius, z). Revolved about the local z axis."""
    verts, faces = [], []
    for r, z in profile:
        for i in range(segments):
            t = 2 * math.pi * i / segments
            verts.append((r * math.cos(t), r * math.sin(t), z))
    for j in range(len(profile) - 1):
        for i in range(segments):
            a = j * segments + i
            b = j * segments + (i + 1) % segments
            faces.append((a, b, b + segments, a + segments))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    ob.location = location
    if material:
        me.materials.append(material)
    return ob

# ------------------------------------------------------------- the stair -----
def z_top(u):
    """String top-edge line (tangent under the tread brackets)."""
    return (u / GOING) * RISER + RISER - 0.095

def z_nose(u):
    return (u / GOING) * RISER + RISER

def build_flight(col):
    iron = MATS["iron"]
    y_str = STRING_CC / 2.0
    # ---- strings (web profile + flange strips), both sides
    for side in (-1, 1):
        b = Batch()
        y = side * y_str
        prof = [(0.0, 0.0), (0.0, z_top(0.0)), (6.18, z_top(6.18)),
                (6.18, z_top(6.18) - STRING_DEPTH / math.cos(ANG)),
                (0.412, 0.0)]
        # web: extrude the 2D profile across the web thickness
        nv = len(b.verts)
        for (u, z) in prof:
            b.verts.append(Vector((X0 + u, y - STRING_WEB / 2, z)))
        for (u, z) in prof:
            b.verts.append(Vector((X0 + u, y + STRING_WEB / 2, z)))
        n = len(prof)
        for i in range(n):
            j = (i + 1) % n
            b.faces.append((nv + i, nv + j, nv + j + n, nv + i + n))
        b.faces.append(tuple(nv + i for i in range(n - 1, -1, -1)))
        b.faces.append(tuple(nv + n + i for i in range(n)))
        # flanges: strips following the top and bottom edges
        d = Vector((math.cos(ANG), 0, math.sin(ANG)))
        nrm = Vector((0, 1, 0))
        wdir = nrm.cross(d)
        for sgn, off in ((1, 0.0), (-1, -STRING_DEPTH / math.cos(ANG) + 0.012)):
            # bottom flange starts at u=0.46: the web's bottom edge is
            # flat on the floor until u=0.412, and a sloped flange begun
            # earlier would dip up to 58 mm below floor level there
            u1, u2 = (0.30, 6.15) if sgn > 0 else (0.46, 6.15)
            pa = Vector((X0 + u1, y, z_top(u1) + off))
            pb = Vector((X0 + u2, y, z_top(u2) + off))
            mid = (pa + pb) / 2
            L = (pb - pa).length
            b.box(mid, (d, nrm, wdir), (L, STRING_FLANGE_W, 0.02))
        b.build(f"String_{'L' if side < 0 else 'R'}", iron, col)
    # ---- treads + brackets
    bt = Batch(); bb = Batch()
    for i in range(1, TREADS + 1):
        z = i * RISER
        xc = X0 + (i - 0.5) * GOING
        bt.box_xyz((xc, 0, z - TREAD_THICK / 2),
                   (GOING + 0.02, STRING_CC - 0.05, TREAD_THICK))
        for side in (-1, 1):
            u = (i - 0.5) * GOING
            cz = z_top(u) + 0.025
            bb.box((X0 + u, side * y_str, cz),
                   (Vector((math.cos(ANG), 0, math.sin(ANG))),
                    Vector((0, 1, 0)),
                    Vector((-math.sin(ANG), 0, math.cos(ANG)))),
                   (0.10, 0.034, 0.05))
    bt.build("Treads", iron, col)
    bb.build("TreadBrackets", iron, col)
    # ---- flight balustrades, both sides
    for side in (-1, 1):
        y = side * y_str
        nrm = Vector((0, 1, 0))
        b = Batch()
        zb = lambda u: z_nose(u) + 0.055
        zt = lambda u: z_nose(u) + HAND_ABOVE_NOSE - 0.075
        # diagonal lattice bars, two families
        # Diamond pitch counted on Plate XV's section: 18 boss crossings
        # along the flight, 13.0 in apart horizontally -> intercept step
        # = pitch * tan(55 deg) = 0.47.
        for m in (math.tan(math.radians(55)), -math.tan(math.radians(55))):
            c = -9.5
            while c < 11.5:
                pts = []
                # boundary lines: z = SLOPE*u + zb0 / zt0
                zb0 = RISER + 0.055
                zt0 = RISER + HAND_ABOVE_NOSE - 0.075
                for bnd in (zb0, zt0):
                    u = (bnd - c) / (m - SLOPE)
                    pts.append((u, SLOPE * u + bnd))
                (u1, z1), (u2, z2) = pts
                lo, hi = min(u1, u2), max(u1, u2)
                lo = max(lo, 0.06); hi = min(hi, 6.12)
                if hi - lo > 0.12:
                    zz1 = m * lo + c; zz2 = m * hi + c
                    # keep only if the segment stays inside the strip
                    if (zb(lo) - 0.03 <= zz1 <= zt(lo) + 0.03 and
                            zb(hi) - 0.03 <= zz2 <= zt(hi) + 0.03):
                        b.bar(Vector((X0 + lo, y, zz1)), Vector((X0 + hi, y, zz2)),
                              0.019, 0.007, nrm)
                c += 0.47
        # bosses at crossings of the two families
        m1 = math.tan(math.radians(55)); m2 = -m1
        cs1 = [(-9.5 + 0.47 * k) for k in range(46)]
        for c1 in cs1:
            for c2 in cs1:
                u = (c2 - c1) / (m1 - m2)
                z = m1 * u + c1
                if 0.15 < u < 6.05 and zb(u) + 0.09 < z < zt(u) - 0.09:
                    b.octa((X0 + u, y, z), 0.030, 0.016, 0.052)
        # standards (plumb flat bars); the top one is omitted - the
        # landing newel / corner standard closes the panel instead
        for u in (0.12, 1.65, 3.18, 4.71):
            h = zt(u) - zb(u) + 0.075
            b.box_xyz((X0 + u, y, zb(u) + h / 2 - 0.03), (0.055, 0.014, h))
        # handrail: main slope + easement to landing-rail height (+y side
        # continues as the landing rail; -y side ends at the landing edge)
        pts = [(X0 - 0.02, z_nose(0) + HAND_ABOVE_NOSE - 0.037),
               (X0 + 5.30, z_nose(5.30) + HAND_ABOVE_NOSE - 0.037),
               (X0 + 5.95, LANDING_Z + RAIL_H - 0.115),
               (X0 + 6.28, LANDING_Z + RAIL_H - 0.040)]
        if side < 0:
            # far side: the easement ends at a landing newel standing on
            # the deck edge - it does not continue as the landing rail
            pts[-1] = (X0 + 6.06, LANDING_Z + RAIL_H - 0.050)
            b.box_xyz((X0 + 6.06, y, (LANDING_Z + LANDING_Z + RAIL_H - 0.05) / 2),
                      (0.055, 0.014, RAIL_H - 0.05))
        for p, q in zip(pts, pts[1:]):
            b.bar(Vector((p[0], y, p[1])), Vector((q[0], y, q[1])),
                  0.075, 0.062, nrm)
        # foot scroll (flat spiral in the panel plane)
        import math as _m
        cx, cz = X0 + 0.10, z_nose(0) + HAND_ABOVE_NOSE - 0.16
        prev = None
        for k in range(15):
            t = k / 14.0 * _m.pi * 2.5
            r = 0.135 - 0.085 * (t / (_m.pi * 2.5))
            px = cx + r * _m.sin(t) * 0.9
            pz = cz + r * _m.cos(t)
            if prev is not None:
                b.bar(Vector((prev[0], y, prev[1])), Vector((px, y, pz)),
                      0.034, 0.05, nrm)
            prev = (px, pz)
        b.build(f"Balustrade_{'L' if side < 0 else 'R'}", iron, col)

def build_landing(col):
    iron, deck_m, rail_m = MATS["iron"], MATS["deck"], MATS["rail"]
    u0, u1 = RUN, RUN + LANDING_DEPTH          # local run coords
    xa, xb = X0 + u0, X0 + u1
    deck_top = LANDING_Z
    # ---- deck boards (butt-jointed; gallery floor has iron tongues,
    #      modelled plain - see NOTES)
    b = Batch()
    y = -1.18 + DECK_BOARD_W / 2
    while y < 1.18:
        b.box_xyz(((xa + xb) / 2, y, deck_top - 0.019),
                  (LANDING_DEPTH + 0.06, DECK_BOARD_W - 0.004, 0.038))
        y += DECK_BOARD_W + 0.004
    b.build("LandingDeck", deck_m, col)
    # ---- joists spanning the 8 ft, + arrival-edge joist the string bolts to
    b = Batch()
    for yy in (-1.07, -0.46, 0.15, 0.76):
        # joists stop short of the edge girder's outer face: joist ends
        # exactly coplanar with that face rendered black (coincident-
        # surface artefact), so the girder closes the edge alone
        b.box_xyz((xa + (LANDING_DEPTH - 0.07) / 2, yy, deck_top - 0.038 - JOIST_D / 2),
                  (LANDING_DEPTH - 0.07, JOIST_W, JOIST_D))
    b.box_xyz((xa + 0.032, 0, deck_top - 0.038 - JOIST_D / 2),
              (JOIST_W, 2.42, JOIST_D))
    b.build("LandingJoists", deck_m, col)
    # ---- iron edge girder at the front (+x) edge, on the column capital
    b = Batch()
    b.box_xyz((xb - 0.03, 0, deck_top - 0.038 - JOIST_D / 2),
              (0.06, 2.42, JOIST_D))
    b.box_xyz((xb - 0.03, 0, deck_top - 0.038 + 0.011),
              (0.16, 2.42, 0.022))
    b.build("LandingEdgeGirder", iron, col)
    # ---- landing column: 5 in tube, flared foot, capital plate
    colx, coly = xb - 0.26, 0.80
    lathe("LandingColumnFoot",
          [(0.145, 0.0), (0.145, 0.02), (0.10, 0.10),
           (LANDING_COL_DIA / 2, 0.30), (LANDING_COL_DIA / 2, 0.34)],
          iron, col, (colx, coly, 0.0))
    lathe("LandingColumn",
          [(LANDING_COL_DIA / 2, 0.0), (LANDING_COL_DIA / 2, LANDING_COL_TOP - 0.30)],
          iron, col, (colx, coly, 0.30))
    b = Batch()
    b.box_xyz((colx, coly, LANDING_COL_TOP + 0.013), (0.20, 0.20, 0.026))
    b.box_xyz((colx, coly, 0.013), (0.32, 0.32, 0.026))
    b.build("LandingColumnPlates", iron, col)
    # ---- landing rail (gallery pattern, Pl. XVII Fig. 12) along +y edge
    y = 1.10
    nrm = Vector((0, 1, 0))
    deck = LANDING_Z
    b = Batch()
    # bottom channel T
    b.box_xyz(((xa + xb) / 2 + 0.02, y, deck + 0.025), (LANDING_DEPTH + 0.1, 0.10, 0.05))
    # corner standard where the flight handrail easement arrives
    b.box_xyz((xa + 0.06, y, deck + RAIL_H / 2), (0.055, 0.014, RAIL_H - 0.07))
    # wavy bars
    z0 = deck + 0.045
    z1 = deck + RAIL_H - 0.070
    bars = []
    xc = xa + 0.12
    i = 0
    while xc < xb - 0.10:
        bars.append(xc)
        phi = 0.0 if i % 2 == 0 else math.pi
        prev = None
        steps = 22
        for k in range(steps + 1):
            z = z0 + (z1 - z0) * k / steps
            xx = xc + LATTICE_AMP * math.sin(2 * math.pi * (z - z0) / LATTICE_PERIOD + phi)
            if prev is not None:
                b.bar(Vector((prev[0], y, prev[1])), Vector((xx, y, z)),
                      0.019, 0.007, nrm)
            prev = (xx, z)
        xc += LATTICE_PITCH
        i += 1
    # bosses S at crossings
    for p, q in zip(bars, bars[1:]):
        for dz in BOSS_ROWS:
            b.octa(((p + q) / 2, y, deck + dz), 0.024, 0.016, 0.048)
    # frame standard N at mid-run
    sx = (xa + xb) / 2 + 0.1
    for dx in (-0.135, 0.135):
        b.box_xyz((sx + dx, y, (z0 + z1) / 2), (0.030, 0.013, z1 - z0))
    b.bar(Vector((sx - 0.135, y, z0 + 0.02)), Vector((sx + 0.135, y, z1 - 0.02)), 0.019, 0.007, nrm)
    b.bar(Vector((sx - 0.135, y, z1 - 0.02)), Vector((sx + 0.135, y, z0 + 0.02)), 0.019, 0.007, nrm)
    b.octa((sx, y, (z0 + z1) / 2), 0.024, 0.016, 0.048)
    b.build("LandingRailLattice", iron, col)
    # timber handrail L, from the flight easement to the post
    b = Batch()
    xa_r = X0 + 6.30
    xb_r = xb - 0.10
    b.box_xyz(((xa_r + xb_r) / 2, y, deck + RAIL_H - 0.0475),
              (xb_r - xa_r, 0.064, 0.045))
    b.build("LandingHandrail", rail_m, col)
    # rounded top of the handrail: half-cylinder
    import bmesh
    me = bpy.data.meshes.new("LandingHandrailTop")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=12, radius1=0.032,
                          radius2=0.032, depth=xb_r - xa_r)
    bm.transform(Matrix.Rotation(math.radians(90), 4, 'Y'))
    bm.transform(Matrix.Translation(((xa_r + xb_r) / 2, y, deck + RAIL_H - 0.025)))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("LandingHandrailTop", me)
    col.objects.link(ob); me.materials.append(rail_m)
    # ---- standard post M (Pl. XVII Fig. 7/8) at the far corner
    px, py = xb - 0.10, y
    b = Batch()
    b.box_xyz((px, py, deck + 0.013), (0.165, 0.165, 0.026))       # base plate 6.5 in
    b.box_xyz((px, py, deck + 0.72 + (RAIL_H - 0.72) / 2),
              (0.19, 0.19, RAIL_H - 0.72))                          # cap block
    b.build("PostMBlocks", iron, col)
    lathe("PostMShaft",
          [(0.083, 0.0), (0.070, 0.05), (0.066, 0.30), (0.070, 0.60),
           (0.084, 0.66), (0.084, 0.72), (0.062, 0.735)],
          iron, col, (px, py, deck + 0.026))
    lathe("PostMFinial",
          [(0.062, 0.0), (0.078, 0.012), (0.030, 0.030), (0.052, 0.055),
           (0.074, 0.095), (0.058, 0.128), (0.020, 0.150), (0.0, POST_FINIAL)],
          iron, col, (px, py, deck + RAIL_H))

# ------------------------------------------------------------- scene ---------
def look_at(ob, target):
    ob.rotation_mode = 'QUATERNION'
    direction = Vector(target) - ob.location
    ob.rotation_quaternion = direction.to_track_quat('-Z', 'Y')

def build_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    model = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(model)
    setup = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(setup)
    build_flight(model)
    build_landing(model)
    # ---- render setup: floor, lights, cameras (NOT exported)
    me = bpy.data.meshes.new("Ground")
    me.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)],
                   [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", me)
    setup.objects.link(g)
    gm = bpy.data.materials.new("BackdropGrey")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.52, 0.52, 0.52, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    me.materials.append(gm)
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN'))
    sun.data.energy = 3.2; sun.data.angle = 0.35
    sun.location = (6, -7, 12); setup.objects.link(sun)
    look_at(sun, (0, 0, 1.5))
    fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", 'AREA'))
    fill.data.energy = 900; fill.data.shape = 'DISK'; fill.data.size = 9
    fill.location = (-8, 6, 8); setup.objects.link(fill)
    look_at(fill, (0, 0, 1.5))
    cams = {}
    for name, pos, tgt in (
            ("front", (-0.3, -15.0, 3.4), (-0.3, 0.0, 1.95)),
            ("side", (13.5, -1.2, 3.4), (0.4, 0.0, 2.0)),
            ("three-quarter", (-9.6, -10.0, 6.8), (0.0, 0.0, 1.8))):
        cd = bpy.data.cameras.new(name)
        cd.lens = 55
        co = bpy.data.objects.new("Cam_" + name, cd)
        co.location = pos; setup.objects.link(co)
        look_at(co, tgt)
        cams[name] = co
    return model, setup, cams

def main():
    global MATS
    MATS = make_mats()
    model, setup, cams = build_scene()
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.view_settings.view_transform = 'Filmic'
    world = bpy.data.worlds.new("W") if not bpy.data.worlds else bpy.data.worlds[0]
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.60, 0.60, 0.60, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.85
    here = os.path.dirname(os.path.abspath(__file__))
    blend = os.path.join(here, "hp-gallery-stair.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    os.makedirs(os.path.join(here, "renders"), exist_ok=True)
    for name, cam in cams.items():
        scene.camera = cam
        out = os.path.join(here, "renders", name + ".png")
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print("rendered", out)
    # export GLB: Model collection only
    bpy.ops.object.select_all(action='DESELECT')
    for ob in model.objects:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = model.objects[0]
    glb = os.path.join(here, "hp-gallery-stair.glb")
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB',
                              use_selection=True, export_apply=True)
    tris = sum(len(ob.data.polygons) and sum(p.loop_total - 2 for p in ob.data.polygons)
               for ob in model.objects if ob.type == 'MESH')
    print(f"MODEL objects={len(model.objects)} triangles={tris}")

if __name__ == "__main__":
    main()
