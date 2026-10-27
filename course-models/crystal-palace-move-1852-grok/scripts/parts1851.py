"""Hyde Park 1851 iron part library (Grok Bot), shared by HP-SITE (CP009 first stacks) and MOVE/K-JOINT (CP032).
Geometry is written in FEET into a bmesh and scaled to metres in finish(). Local frames:
  column / connecting piece: axis +Z from z=0;  girder: length along +X centred on x=0, top at z=0, depth down to -3 ft.
Sources (Downes 1852, Plate VIII Figs 3, 12, 13 + text p. 4-6, OCR in references/downes-1852):
  connecting piece 3 ft 4 1/2 in long, flanges with four snugs each; snug groove 2 in wide x 1/2 in deep; girder bottom
  projection R fits the groove; wrought-iron key S driven into the matched grooves at the top; keys T driven top and bottom
  between the snugs and the girder's projecting ends U; wrought-iron keys within 200 ft of the ends and of the transept,
  wooden (oak) keys on the two ~500 ft intermediate runs; columns 8 in outside; 4 bolts column<->connecting piece.
Interpretive (not dimensioned in the plate text): flange plan, snug height, U/T sizes, girder web pattern (see DEPARTURES)."""
import bpy, bmesh, math
from mathutils import Vector, Matrix
FT = 0.3048
I = 1.0 / 12.0                      # one inch in feet
CONN_L = 3.375                      # 3 ft 4 1/2 in (D15)
COL_R = 4 * I                       # 8 in outside
FL_T = 1.25 * I                     # flange thickness (interpretive)
SNUG_H = 1.0 * I                    # snug height above / below the flange face (interpretive)
GIRDER_D = 3.0                      # 3 ft deep cast-iron girder (Plate VIII Fig 12 '3 ft 0 in')
GIRDER_L = 24.0 - 2 * COL_R - 2 * 0.25 * I     # between column faces, 1/4 in clearance each end

def finish(bm, name, mats):
    bmesh.ops.scale(bm, vec=(FT, FT, FT), verts=bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    return me
def mark(bm, n0, idx):
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = idx
def box(bm, x0, x1, y0, y1, z0, z1, M=None):
    vs = [bm.verts.new((a, b, c)) for a, b, c in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                                  (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    if M is not None:
        for v in vs: v.co = M @ v.co
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])
def rod(bm, a, b, r, seg=8, r2=None):
    a = Vector(a); b = Vector(b); d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=d.length, matrix=M)
def beam(bm, a, b, w, t):
    a = Vector(a); b = Vector(b); d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cube(bm, size=1.0, matrix=M @ Matrix.Diagonal((w, t, d.length, 1)))
def prism(bm, poly, z0, z1, M=None):
    """extrude a closed 2D polygon (feet) from z0 to z1"""
    lo = [bm.verts.new((x, y, z0)) for x, y in poly]; hi = [bm.verts.new((x, y, z1)) for x, y in poly]
    if M is not None:
        for v in lo + hi: v.co = M @ v.co
    n = len(poly)
    bm.faces.new(list(reversed(lo))); bm.faces.new(hi)
    for k in range(n): bm.faces.new([lo[k], lo[(k + 1) % n], hi[(k + 1) % n], hi[k]])
def lathe(bm, prof, seg=24, M=None):
    """closed profile [(r, z)] revolved about Z"""
    rings = []
    for (r, z) in prof:
        ring = [bm.verts.new((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)]
        rings.append(ring)
    if M is not None:
        for ring in rings:
            for v in ring: v.co = M @ v.co
    n = len(rings)
    for j in range(n):
        a, b = rings[j], rings[(j + 1) % n]
        for k in range(seg):
            try: bm.faces.new([a[k], a[(k + 1) % seg], b[(k + 1) % seg], b[k]])
            except ValueError: pass
def wedge(bm, x0, x1, y0, y1, z0, z1, t0, t1, M=None):
    """a key tapering along +Z: x-thickness t0 at z0 -> t1 at z1, flat face at x0"""
    vs = [bm.verts.new(p) for p in [(x0, y0, z0), (x0 + t0, y0, z0), (x0 + t0, y1, z0), (x0, y1, z0),
                                    (x0, y0, z1), (x0 + t1, y0, z1), (x0 + t1, y1, z1), (x0, y1, z1)]]
    if M is not None:
        for v in vs: v.co = M @ v.co
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])

def flange_poly():
    """connecting-piece flange in plan (Fig. 13): a square turned 45 deg with rounded bolt lobes on the diagonals and
    flats on the four faces that carry the snugs. ~10 in between opposite bolt centres on the square."""
    pts = []
    for k in range(4):
        a = math.radians(45 + 90 * k)
        cx, cy = 5.3 * I * math.cos(a), 5.3 * I * math.sin(a)          # bolt lobe centre
        for j in range(7):
            t = a - math.radians(70) + math.radians(140) * j / 6
            pts.append((cx + 1.35 * I * math.cos(t), cy + 1.35 * I * math.sin(t)))
        # face flat toward the next quadrant
        af = math.radians(90 + 90 * k)
        for s in (-1.6, 1.6):
            pts.append((5.6 * I * math.cos(af) - s * I * math.sin(af), 5.6 * I * math.sin(af) + s * I * math.cos(af)))
    return pts
FLANGE = flange_poly()

def add_column(bm, L, mi_shaft=0, top_flange=True, bot_flange=True, bore=True, M=None):
    """tier column, 8 in outside, flanged both ends with 4 bolt lugs; hollow (bore) so stacked ends read as tubes"""
    M = M or Matrix()
    rin = 3.0 * I if bore else 0.0
    prof = [(rin, 0.0), (COL_R, 0.0), (COL_R, L), (rin, L)] if bore else [(0.0, 0.0), (COL_R, 0.0), (COL_R, L), (0.0, L)]
    lathe(bm, prof, 24, M)
    for (z0, z1, on) in ((0.0, 1.0 * I, bot_flange), (L - 1.0 * I, L, top_flange)):
        if not on: continue
        lathe(bm, [(rin + 0.01, z0), (5.6 * I, z0), (5.6 * I, z1), (rin + 0.01, z1)], 24, M)
        for k in range(4):
            a = math.radians(45 + 90 * k)
            box(bm, -1.1 * I, 1.1 * I, -1.1 * I, 1.1 * I, z0, z1, M @ Matrix.Translation((5.3 * I * math.cos(a), 5.3 * I * math.sin(a), 0)))

def add_connecting_piece(bm, M=None, mi_iron=0, mi_bolt=None, faces=(0, 1, 2, 3)):
    """connecting piece C (Fig 12/13): tube 8 in, flanges P top and bottom, four snugs per flange with a 2 in x 1/2 in
    groove (modelled as two cheeks), four bolts with nuts on each flange. Bottom at z=0, top at CONN_L."""
    M = M or Matrix()
    rin = 3.0 * I
    lathe(bm, [(rin, 0), (COL_R, 0), (COL_R, CONN_L), (rin, CONN_L)], 24, M)
    for z0, z1 in ((0.0, FL_T), (CONN_L - FL_T, CONN_L)):
        prism(bm, FLANGE, z0, z1, M)
        for k in range(4):
            a = math.radians(45 + 90 * k)
            R = Matrix.Translation((5.3 * I * math.cos(a), 5.3 * I * math.sin(a), 0))
            # bolt + nut through each lobe (nut on the inside face)
            rod(bm, (M @ R @ Vector((0, 0, z0 - 0.7 * I))), (M @ R @ Vector((0, 0, z1 + 0.7 * I))), 0.5 * I, 6)
            zn0, zn1 = (z1, z1 + 0.85 * I) if z0 == 0.0 else (z0 - 0.85 * I, z0)
            rod(bm, (M @ R @ Vector((0, 0, zn0))), (M @ R @ Vector((0, 0, zn1))), 0.95 * I, 6)
    # snugs: on each face, bottom snug sits on the bottom flange, top snug hangs from the top flange
    for k in faces:
        af = math.radians(90 * k)
        Rz = M @ Matrix.Rotation(af, 4, 'Z')
        for (zb, zt) in ((FL_T, FL_T + SNUG_H), (CONN_L - FL_T - SNUG_H, CONN_L - FL_T)):
            # cheeks either side of the 2 in groove; groove floor 1/2 in deep
            for s in (-1, 1):
                box(bm, COL_R - 0.1 * I, 7.5 * I, s * 1.0 * I, s * 1.5 * I, zb, zt, Rz)
            if zb < 1.0:  box(bm, COL_R - 0.1 * I, 7.5 * I, -1.0 * I, 1.0 * I, zb, zt - 0.5 * I, Rz)
            else:         box(bm, COL_R - 0.1 * I, 7.5 * I, -1.0 * I, 1.0 * I, zb + 0.5 * I, zt, Rz)

def add_girder(bm, M=None, L=GIRDER_L, ends=True):
    """24 ft cast-iron girder (3 ft deep), length along X centred at 0, top at z=0. Top flange 4 in, bottom flange
    5 in, 1 in webs; three 8 ft panels with V diagonals (interpretive of Plate X); end standards with the bottom
    projection R (into the snug groove), the top groove for key S and the projecting ends U for keys T."""
    M = M or Matrix()
    D = GIRDER_D; h = L / 2
    box(bm, -h, h, -2.0 * I, 2.0 * I, -0.75 * I, 0.0, M)                    # top flange
    box(bm, -h, h, -0.5 * I, 0.5 * I, -3.0 * I, -0.75 * I, M)               # top web lip
    box(bm, -h, h, -2.5 * I, 2.5 * I, -D, -D + 1.0 * I, M)                  # bottom flange
    box(bm, -h, h, -0.5 * I, 0.5 * I, -D + 1.0 * I, -D + 3.0 * I, M)
    xs = [-h + k * (L / 3) for k in range(4)]
    for k, x in enumerate(xs):
        w = 2.0 * I if k in (0, 3) else 1.5 * I
        xa = x if k == 0 else (x - w if k == 3 else x - w / 2)
        box(bm, xa, xa + w, -0.6 * I, 0.6 * I, -D + 1.0 * I, -0.75 * I, M)       # verticals / end standards
    for k in range(3):
        x0, x1 = xs[k], xs[k + 1]; xm = (x0 + x1) / 2
        for xa in (x0, x1):
            a = Vector((xa, 0, -2.5 * I)); b = Vector((xm, 0, -D + 1.5 * I))
            d = b - a; Q = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
            bmesh.ops.create_cube(bm, size=1.0, matrix=M @ Matrix.Translation((a + b) / 2) @ Q @ Matrix.Diagonal((2.0 * I, 1.0 * I, d.length, 1)))
    if not ends: return
    for s in (-1, 1):
        xe = s * h
        # projection R under the bottom flange at the end: 1 3/4 in wide tongue, 1/2 in down, 3 in long (sits in the snug groove)
        x0, x1 = sorted((xe, xe - s * 3.2 * I))
        box(bm, x0, x1, -0.85 * I, 0.85 * I, -D - 0.5 * I, -D, M)
        # projecting ends U, top and bottom, 4 in back from the end face (keys T are driven between these and the snugs)
        u0, u1 = sorted((xe - s * 4.0 * I, xe - s * 5.0 * I))
        box(bm, u0, u1, -1.5 * I, 1.5 * I, 0.0, SNUG_H, M)                 # U top (stands beside the top snug)
        box(bm, u0, u1, -1.5 * I, 1.5 * I, -D - SNUG_H, -D, M)             # U bottom
GIRDER_TOP_IN_CP = CONN_L - FL_T - SNUG_H          # girder top level inside a connecting piece (local z, ft)

def add_keys(bm, M=None, which="iron", driven=True):
    """keys for ONE girder end at a connecting piece face (frame: girder runs +X from the column, column axis at x=0,
    z=0 at the bottom of the connecting piece). S: top groove key; T: tapered keys top and bottom."""
    M = M or Matrix()
    zt = GIRDER_TOP_IN_CP
    lift = 0.0 if driven else 0.9
    # S: bar in the matched grooves (snug underside + girder top), 3 in long; exploded = lifted out and drawn back
    Sx = Matrix.Translation((0, 0, 0)) if driven else Matrix.Translation((6.0 * I, 0, 0.9))
    box(bm, COL_R + 0.3 * I, 7.3 * I, -0.95 * I, 0.95 * I, zt - 0.5 * I, zt + 0.5 * I, M @ Sx)
    # T top / bottom: tapered keys in the gap between the snug tip (7.5 in) and the girder's projecting end U
    xg = 7.55 * I
    for (zlo, zhi, sgn) in ((zt - 0.2 * I, zt + SNUG_H + 1.6 * I, 1), (FL_T - 1.6 * I, FL_T + SNUG_H + 0.2 * I, -1)):
        dz = lift * sgn
        # tapered: thick end at the struck head (top key: head up; bottom key: head down)
        if sgn > 0: wedge(bm, xg, xg, -1.4 * I, 1.4 * I, zlo + dz, zhi + dz, 0.55 * I, 0.95 * I, M)
        else:       wedge(bm, xg, xg, -1.4 * I, 1.4 * I, zlo + dz, zhi + dz, 0.95 * I, 0.55 * I, M)
