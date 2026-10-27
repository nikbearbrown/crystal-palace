#!/usr/bin/env python3
"""Build the Crystal Palace gallery lattice railing + newel post (candidate #19).

Source: Downes (1852) *Descriptions and Drawings of the Crystal Palace*
Plate XVII, Figs. 7-12, cross-checked against the Absolon watercolour
(colour: red lattice, blue newel, gilt bud finial) and Nash's Plate 3
(British nave, in-situ runs). Hyde Park 1851 building only.

Procedural bpy, Blender 4.2. Real-world metres. Origin at the base
centre of the assembled unit (newel + one lattice panel + frame
standard). z = 0 is the gallery floor line (the lattice foot line of
Plate XVII Fig. 12).

Dimensions
----------
PRINTED on Plate XVII:
  - post M: floor to cap top 3 ft 1 7/8 in; bud finial 6 1/4 in;
    shaft 6 1/2 in across, bore 4 3/4 in, wall 3/8 in (Fig. 8);
    base plate 6 1/2 in sq; bolt holes 3/4 in at 4 7/8 in centres.
  - frame standard member 1 1/4 in thick (Fig. 10 section).
MEASURED on the plate scan (Fig. 12 calibrated by its own height:
  handrail top -> lattice foot = the printed 3 ft 1 7/8 in over
  1461 px, i.e. 38.6 px/in; features located by ink projection and
  visual grounding of the boss rosettes):
  - boss rows 6.7 / 17.4 / 28.0 in above the foot line (spacing 10.65 in)
  - boss column pitch 12.43 in, adjacent rows staggered half a pitch
  - frame standard 10.4 in overall width, uprights ~0.7 in face
  - lozenge boss ~3.1 x 2.2 in
INFERRED:
  - panel length 8 lattice periods = 2.526 m between newel and frame
    standard (the plate draws the lattice continuous past one
    standard; 8 periods keeps the assembly on the building's 8 ft
    module, cf. the 8 ft gutter pitch, CONTROL-DIMENSIONS D09)
  - bar face width ~0.39 in (15 px across the drawn strip on Fig. 12);
    bar thickness/rib inferred from Fig. 9 (ribbed face)
  - hairpin leg gap 40 mm (Fig. 9 pair of verticals, unscaled)
  - newel cap 8 in sq (scaled from Fig. 7 against the 6 1/2 in shaft)
  - colours from the Absolon watercolour (see NOTES.md)
"""
import bpy
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/gallery-lattice-railing")
RENDERS = os.path.join(OUT, "renders")
os.makedirs(RENDERS, exist_ok=True)

IN = 0.0254

# ---------------------------------------------------------------- dimensions
RAIL_TOP = 37.875 * IN            # 0.9620 m, printed (Fig. 7 / Fig. 12 datum)
HR_DEPTH = 0.048                  # handrail depth (measured: 72 px band, Fig. 12)
HR_UNDER = RAIL_TOP - HR_DEPTH    # 0.8920 handrail underside
HR_W = 0.076                      # handrail width (Fig. 10, ~3 in)
ROW1, ROW2, ROW3 = 0.170, 0.442, 0.711   # boss rows, measured (in: 6.7/17.4/28.0)
PITCH = 12.43 * IN                # 0.3157 boss column pitch, measured
STAG = PITCH / 2.0
HAIRPIN_GAP = 0.020               # half-gap of hairpin legs, inferred
FOOT_Z = 0.006                    # hairpin arc bottom
APEX_Z = 0.890                    # top hairpin apex (just under handrail)
BAR_W, BAR_T, BAR_RIB = 0.010, 0.004, 0.0013  # bar section: width measured
# on Fig. 12 (~15 px = 0.39 in); thickness/rib inferred from Fig. 9

X0 = 0.145                        # first hairpin/boss column (local coords)
NPER = 8                          # lattice periods in the panel
X1 = X0 + NPER * PITCH            # last column = 2.6707
STD_W = 10.4 * IN                 # frame standard overall width, measured
STD_CX = X1 + 0.010 + STD_W / 2   # standard centre x
STD_T = 1.25 * IN                 # standard member thickness (Y), printed Fig. 10
HAND_END = STD_CX + STD_W / 2 + 0.020
TOTAL_MIN, TOTAL_MAX = -0.1015, HAND_END   # cap half-width governs the left extreme
SHIFT = -(TOTAL_MIN + TOTAL_MAX) / 2.0    # centre the assembly on origin

# newel post M (printed dims)
POST_H = 37.875 * IN              # floor to cap top = 0.9620
FINIAL_H = 6.25 * IN              # 0.1588
SHAFT_D = 6.5 * IN                # 0.1651
PLATE_D = 6.5 * IN
PLATE_T = 0.012
BOLT_C = 4.875 * IN               # bolt hole centres
CAP_W = 0.203                     # 8 in, measured from Fig. 7

# ---------------------------------------------------------------- materials
def make_mat(name, color, metallic=0.0, rough=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return m

RED = BLUE = GILT = TIMBER = DARK = GREY = None

# ---------------------------------------------------------------- geometry kit
# A "geom" is (verts, faces, mat_tags) with faces as tuples and mat_tags
# parallel to faces (material index within the owning object's list).

def merge_geoms(geoms):
    verts, faces, tags = [], [], []
    for v, f, t in geoms:
        off = len(verts)
        verts.extend(v)
        faces.extend(tuple(i + off for i in face) for face in f)
        tags.extend(t)
    return verts, faces, tags

def sweep(profile, path, mat=0):
    """Sweep a 2D profile along a planar path.
    profile: list of (u, v); u = in-plane normal offset, v = Y offset.
    path: list of Vector (x, y, z) with y const (the panel plane).
    Returns a geom. End caps included.
    """
    n = len(profile)
    rings = []
    for i, p in enumerate(path):
        if i == 0:
            tan = path[1] - path[0]
        elif i == len(path) - 1:
            tan = path[-1] - path[-2]
        else:
            tan = path[i + 1] - path[i - 1]
        # in-plane normal: rotate tangent (tx, tz) by 90 deg in x-z plane
        tx, tz = tan.x, tan.z
        L = math.hypot(tx, tz) or 1.0
        nx, nz = -tz / L, tx / L
        ring = []
        for (u, v) in profile:
            ring.append((p.x + u * nx, p.y + v, p.z + u * nz))
        rings.append(ring)
    verts = [v for ring in rings for v in ring]
    faces, tags = [], []
    m = len(path)
    for i in range(m - 1):
        for j in range(n):
            k = (j + 1) % n
            faces.append((i * n + j, i * n + k, (i + 1) * n + k, (i + 1) * n + j))
            tags.append(mat)
    faces.append(tuple(range(n - 1, -1, -1)))
    tags.append(mat)
    base = (m - 1) * n
    faces.append(tuple(base + j for j in range(n)))
    tags.append(mat)
    return verts, faces, tags

def catmull(points, samples_per_seg=6, closed=False):
    """Catmull-Rom through Vector points; returns dense polyline."""
    pts = list(points)
    if len(pts) < 3:
        return pts
    ext = [pts[0] * 2 - pts[1]] + pts + [pts[-1] * 2 - pts[-2]]
    out = []
    for i in range(len(ext) - 3):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        for s in range(samples_per_seg):
            t = s / samples_per_seg
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t +
                              (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                              (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return out

def prism(axis, outline, lo, hi, mat=0):
    """Extrude a 2D outline between lo..hi along an axis.
    axis 'Y': outline (x,z); 'X': outline (y,z) -> (x from lo..hi); 'Z': outline (x,y)."""
    n = len(outline)
    verts = []
    for s in (lo, hi):
        for (a, b) in outline:
            if axis == 'Y':
                verts.append((a, s, b))
            elif axis == 'X':
                verts.append((s, a, b))
            else:
                verts.append((a, b, s))
    faces, tags = [], []
    faces.append(tuple(range(n - 1, -1, -1)))
    tags.append(mat)
    faces.append(tuple(range(n, 2 * n)))
    tags.append(mat)
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        tags.append(mat)
    return verts, faces, tags

def _box_at(cx, cy, cz, sx, sy, sz, mat=0):
    x0, x1, y0, y1, z0, z1 = cx-sx/2, cx+sx/2, cy-sy/2, cy+sy/2, cz-sz/2, cz+sz/2
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    f = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return v, f, [mat]*len(f)

def loft(rings, mat=0, cap_start=True, cap_end=True):
    """Loft rings: list of (z, [(x,y), ...]) all with equal point counts."""
    n = len(rings[0][1])
    verts = []
    for z, ring in rings:
        verts.extend((x, y, z) for (x, y) in ring)
    faces, tags = [], []
    for i in range(len(rings) - 1):
        for j in range(n):
            k = (j + 1) % n
            faces.append((i*n+j, i*n+k, (i+1)*n+k, (i+1)*n+j))
            tags.append(mat)
    if cap_start:
        faces.append(tuple(range(n - 1, -1, -1)))
        tags.append(mat)
    if cap_end:
        base = (len(rings) - 1) * n
        faces.append(tuple(base + j for j in range(n)))
        tags.append(mat)
    return verts, faces, tags

def lathe(profile, segments=40, rib=0, rib_amp=0.0, zbase=0.0, mat=0):
    """Lathe a (r, z) profile around Z. Optional radial rib modulation."""
    rings = []
    for (r, z) in profile:
        ring = []
        for i in range(segments):
            th = 2 * math.pi * i / segments
            rr = r
            if rib:
                fade = math.sin(math.pi * (z - profile[0][1]) /
                                max(1e-6, (profile[-1][1] - profile[0][1]))) ** 0.7
                rr = r * (1 + rib_amp * math.cos(rib * th) * fade)
            ring.append((rr * math.cos(th), rr * math.sin(th)))
        rings.append((z, ring))
    return loft(rings, mat=mat)

def shaft_outline(radius=0.0826, flat=0.0745, flute=0.005, samples=96):
    """Post M shaft section after Plate XVII Fig. 8: a 6 1/2 in circle
    with four flat faces (disc intersected with a square), each face
    carrying one shallow concave flute. Returns CCW (x, y) points."""
    pts = []
    for i in range(samples):
        th = 2 * math.pi * i / samples
        x, y = radius * math.cos(th), radius * math.sin(th)
        cx, cy = max(-flat, min(flat, x)), max(-flat, min(flat, y))
        # flute: on a flat, pull inward near the face centre
        if cx != x and abs(y) < 0.048:
            cx -= math.copysign(flute * math.cos(math.pi * y / (2 * 0.048)) ** 2, x)
        if cy != y and abs(x) < 0.048:
            cy -= math.copysign(flute * math.cos(math.pi * x / (2 * 0.048)) ** 2, y)
        pts.append((cx, cy))
    # drop consecutive duplicates left by clamping
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > 1e-5:
            out.append(p)
    return out

def rounded_rect_outline(half, corner_r, per_corner=6):
    """CCW outline of a rounded rectangle centred on origin, in (x, y)."""
    raw = []
    cc = [(half - corner_r, half - corner_r, 0.0),
          (-half + corner_r, half - corner_r, math.pi / 2),
          (-half + corner_r, -half + corner_r, math.pi),
          (half - corner_r, -half + corner_r, 3 * math.pi / 2)]
    for (cx, cy, a0) in cc:
        for i in range(per_corner + 1):
            a = a0 + (math.pi / 2) * i / per_corner
            raw.append((cx + corner_r * math.cos(a), cy + corner_r * math.sin(a)))
    return raw

def make_object(name, geom, materials):
    verts, faces, tags = geom
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for m in materials:
        me.materials.append(m)
    for poly, tag in zip(me.polygons, tags):
        poly.material_index = tag
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob

def V(x, z):
    return Vector((x, 0.0, z))

# ---------------------------------------------------------------- profiles
# bar cross-section (u = in-plane, v = across/Y): flat strip with a
# raised centre rib on both faces, after Fig. 9.
_hw, _ht, _hr = BAR_W / 2, BAR_T / 2, (BAR_T + 2 * BAR_RIB) / 2
_rw = 0.0022  # rib half-width
BAR_PROFILE = [(-_hw, -_ht), (-_rw, -_ht), (-_rw, -_hr), (_rw, -_hr),
               (_rw, -_ht), (_hw, -_ht), (_hw, _ht), (_rw, _ht),
               (_rw, _hr), (-_rw, _hr), (-_rw, _ht), (-_hw, _ht)]

def bar_path(points, samples=5):
    return catmull([V(x, z) for (x, z) in points], samples)

# ---------------------------------------------------------------- lattice
def build_lattice():
    geoms = []
    cols = [X0 + k * PITCH for k in range(NPER + 1)]          # even columns
    odd = [X0 + STAG + k * PITCH for k in range(NPER)]        # ROW2 columns
    # diagonal segments between boss rows (slight bow = hand-made waviness).
    # ROW1(even)->ROW2(odd): upper end may reach X0-STAG (dies into the
    # newel) but not X1+STAG (would cross the frame standard).
    # ROW2(odd)->ROW3(even): upper end within [X0, X1].
    pairs = [(ROW1, ROW2, cols, X0 - STAG, X1 - STAG),
             (ROW2, ROW3, odd, X0, X1)]
    for (zlo, zhi, lower, umin, umax) in pairs:
        zm = (zlo + zhi) / 2
        for c in lower:
            for sgn in (-1, 1):
                cx = c + sgn * STAG
                if cx < umin - 0.001 or cx > umax + 0.001:
                    continue
                k = int(round((c - X0) / (PITCH / 2)))
                bow = 0.005 if (k + (0 if sgn > 0 else 1)) % 2 == 0 else -0.005
                pts = [(c, zlo), ((c + cx) / 2 + bow, zm), (cx, zhi)]
                geoms.append(sweep(BAR_PROFILE, bar_path(pts, 3)))
    # bottom hairpins: legs splay from the ROW1 boss down to a U
    for c in cols:
        pts = [(c, ROW1), (c - 0.016, 0.105), (c - HAIRPIN_GAP, 0.052),
               (c - HAIRPIN_GAP, 0.020), (c, FOOT_Z + 0.004),
               (c + HAIRPIN_GAP, 0.020), (c + HAIRPIN_GAP, 0.052),
               (c + 0.016, 0.105), (c, ROW1)]
        geoms.append(sweep(BAR_PROFILE, bar_path(pts, 3)))
    # top hairpins: from ROW3 bosses up to apexes on odd columns
    for k in range(NPER + 1):
        u = X0 + STAG + k * PITCH
        if u > X1 + 0.001:
            continue
        pts = [(u - STAG, ROW3), (u - 0.105, 0.790), (u - 0.062, 0.855),
               (u, APEX_Z), (u + 0.062, 0.855), (u + 0.105, 0.790),
               (u + STAG, ROW3)]
        geoms.append(sweep(BAR_PROFILE, bar_path(pts, 4)))
    # left edge stub: ROW3 boss at X0 also throws a leg up-left (dies into newel)
    geoms.append(sweep(BAR_PROFILE, bar_path([(X0, ROW3), (X0 - 0.09, 0.80),
                                              (X0 - STAG, APEX_Z - 0.045)], 3)))
    # junction diagonals: last field bosses run into the standard upright
    jx = STD_CX - STD_W / 2 + 0.012
    for zlo in (ROW1, ROW3):
        pts = [(X1, zlo), ((X1 + jx) / 2, (zlo + ROW2) / 2), (jx, ROW2)]
        geoms.append(sweep(BAR_PROFILE, bar_path(pts, 3)))
    return merge_geoms(geoms)

def boss_geom(cx, cz, scale=1.0, gilt_centre=True, y_off=0.0):
    """Lozenge rosette boss at a crossing: plate + raised inner lozenge
    (red) and a small gilt centre dome. Bosses stand proud toward -Y
    (the gallery side, cf. Fig. 10 section)."""
    h, w = 0.040 * scale, 0.0275 * scale
    plate = prism('Y', [(0, -h), (w, 0), (0, h), (-w, 0)], -0.0095, 0.0035, mat=0)
    pv, pf, pt = plate
    pv = [(x + cx, y + y_off, z + cz) for (x, y, z) in pv]
    h2, w2 = 0.026 * scale, 0.018 * scale
    inner = prism('Y', [(0, -h2), (w2, 0), (0, h2), (-w2, 0)], -0.0135, -0.0095, mat=0)
    iv, inf, it = inner
    iv = [(x + cx, y + y_off, z + cz) for (x, y, z) in iv]
    geoms = [(pv, pf, pt), (iv, inf, it)]
    if gilt_centre:
        # squashed dome from a lathe, rotated to face -Y
        prof = [(0.0008, 0.0), (0.0055, 0.0018), (0.0075, 0.0042),
                (0.0068, 0.0068), (0.004, 0.0088), (0.0008, 0.0100)]
        dv, df, dt = lathe(prof, segments=14, mat=1)
        # lathe is around Z with z up; rotate -90 deg about X so +Z -> -Y,
        # then translate: base at y = -0.0135 (front face), centre (cx, cz)
        dv2 = [(cx + x, y_off - 0.0135 - z, cz + y) for (x, y, z) in dv]
        geoms.append((dv2, df, dt))
    return merge_geoms(geoms)

def build_bosses():
    geoms = []
    for c in [X0 + k * PITCH for k in range(NPER + 1)]:
        geoms.append(boss_geom(c, ROW1))
        geoms.append(boss_geom(c, ROW3))
    for c in [X0 + STAG + k * PITCH for k in range(NPER)]:
        geoms.append(boss_geom(c, ROW2))
    # junction bosses seated on the frame standard's left upright face
    # (Fig. 12 shows the field crossings halved on the uprights)
    for z in (ROW1, ROW2, ROW3):
        geoms.append(boss_geom(STD_CX - STD_W / 2 + 0.012, z, scale=0.92,
                               y_off=-0.0159))
    return merge_geoms(geoms)

# ---------------------------------------------------------------- rails
def build_handrail():
    d = HR_DEPTH
    prof = [(-d, -HR_W/2), (-d, HR_W/2), (-0.41 * d, HR_W/2),
            (-0.10 * d, 0.0335), (0.0, 0.024), (0.0, -0.024),
            (-0.10 * d, -0.0335), (-0.41 * d, -HR_W/2)]
    # profile (u = up from rail top, v = Y); path along X at rail top
    path = [Vector((x, 0, RAIL_TOP)) for x in (-0.06, 0.6, 1.4, 2.2, HAND_END)]
    return sweep(prof, path)

def build_channel():
    geoms = []
    x_lo, x_hi = 0.06, STD_CX + STD_W / 2
    # bottom channel: base strip + two side cheeks (feet house between);
    # cheek faces stand 1 mm proud of the base strip to avoid coplanar faces
    geoms.append(_box_at((x_lo + x_hi)/2, 0, 0.008, x_hi - x_lo, 0.044, 0.016, 0))
    for s in (-1, 1):
        geoms.append(_box_at((x_lo + x_hi)/2, s * 0.019, 0.024, x_hi - x_lo, 0.008, 0.032, 0))
    return merge_geoms(geoms)

# ---------------------------------------------------------------- frame standard
def build_standard():
    geoms = []
    up_w = 0.024                       # upright face width (measured ~0.7 in)
    z_lo, z_hi = 0.100, HR_UNDER
    rail_h = 0.045
    # uprights run BETWEEN the top/bottom rails (butt joints only: no two
    # boxes share a coplanar face, which z-fights black in Cycles)
    for s in (-1, 1):
        geoms.append(_box_at(STD_CX + s * (STD_W/2 - up_w/2), 0,
                             (z_lo + rail_h + z_hi - rail_h)/2,
                             up_w, STD_T, z_hi - z_lo - 2 * rail_h, 0))
    for (zc, hh) in ((z_lo + rail_h/2, rail_h), (z_hi - rail_h/2, rail_h)):
        geoms.append(_box_at(STD_CX, 0, zc, STD_W, STD_T, hh, 0))
    # inner liner (stands proud in Y), assembled as four butt-jointed bars:
    # uprights between the horizontals, horizontals between the uprights
    lin_w, lin_t = 0.018, STD_T + 0.008
    lin_x = STD_W/2 - up_w - lin_w/2    # liner upright centre offset
    lin_z0, lin_z1 = z_lo + rail_h, z_hi - rail_h     # 0.145 .. HR_UNDER-0.045
    for s in (-1, 1):
        geoms.append(_box_at(STD_CX + s * lin_x, 0, (lin_z0 + lin_z1)/2,
                             lin_w, lin_t, lin_z1 - lin_z0 - 0.038, 0))
    for zc in (lin_z0 + 0.0095, lin_z1 - 0.0095):
        geoms.append(_box_at(STD_CX, 0, zc, 2 * (lin_x - lin_w/2), lin_t, 0.019, 0))
    # inner pattern (Fig. 12): two wavy-bar diagonals that cross at the
    # centre lozenge and curve together into a cap curve at the top and
    # a U at the bottom of the frame
    rel = [(0.0, 0.848), (-0.032, 0.840), (-0.098, 0.820), (-0.049, 0.660),
           (0.0, 0.496), (0.049, 0.332), (0.078, 0.218), (0.030, 0.170),
           (0.0, 0.162)]
    geoms.append(sweep(BAR_PROFILE, bar_path([(STD_CX + dx, z) for (dx, z) in rel], 3)))
    rel2 = [(-dx, z) for (dx, z) in rel]
    geoms.append(sweep(BAR_PROFILE, bar_path([(STD_CX + dx, z) for (dx, z) in rel2], 3)))
    geoms.append(boss_geom(STD_CX, 0.496, scale=0.55, gilt_centre=False))
    # foot: base plate, stepped cove block, screw head on the front (Fig. 9)
    geoms.append(_box_at(STD_CX, 0, 0.006, 0.30, 0.15, 0.012, 0))
    geoms.append(_box_at(STD_CX, 0, 0.021, 0.27, 0.125, 0.018, 0))
    geoms.append(_box_at(STD_CX, 0, 0.040, 0.25, 0.108, 0.020, 0))
    geoms.append(_box_at(STD_CX, 0, 0.072, 0.235, 0.095, 0.045, 0))
    screw = lathe([(0.0008, 0.0), (0.011, 0.0), (0.011, 0.005), (0.0008, 0.006)],
                  segments=16, mat=1)
    sv, sf, st = screw
    sv = [(STD_CX + x, -0.0475 - z, 0.072 + y) for (x, y, z) in sv]
    geoms.append((sv, sf, st))
    return merge_geoms(geoms)

# ---------------------------------------------------------------- newel post M
def build_newel():
    geoms = []
    # base plate: rounded rect 6 1/2 in sq (Fig. 8), bolt holes as dark insets
    outline = rounded_rect_outline(PLATE_D/2, 0.028, per_corner=5)
    pv, pf, pt = prism('Z', outline, 0.0, PLATE_T, mat=0)
    geoms.append((pv, pf, pt))
    bc = BOLT_C / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            hv, hf, ht = lathe([(0.0008, 0.0), (0.0095, 0.0), (0.0095, 0.002)],
                               segments=12, mat=1)
            hv = [(x + sx * bc, y + sy * bc, z + PLATE_T - 0.001) for (x, y, z) in hv]
            geoms.append((hv, hf, ht))
    # shaft: fluted cushion section (Fig. 8), straight extrusion
    out = shaft_outline()
    sv, sf, st = prism('Z', out, PLATE_T, 0.795, mat=0)
    geoms.append((sv, sf, st))
    # cove: loft the shaft outline scaled up to the cap
    rings = []
    for (z, s) in ((0.795, 1.0), (0.812, 1.06), (0.830, 1.17), (0.845, 1.28)):
        rings.append((z, [(x * s, y * s) for (x, y) in out]))
    geoms.append(loft(rings, mat=0))
    # cap block (8 in sq), top at the printed 3 ft 1 7/8 in
    geoms.append(_box_at(0, 0, (0.845 + POST_H)/2, CAP_W, CAP_W, POST_H - 0.845, 0))
    # skirt + bead + ribbed bud finial (gilt), all lathe
    skirt = lathe([(0.096, POST_H), (0.089, POST_H + 0.012), (0.068, POST_H + 0.030),
                   (0.052, POST_H + 0.042), (0.047, POST_H + 0.049)], segments=36, mat=2)
    geoms.append(skirt)
    bead = lathe([(0.047, POST_H + 0.049), (0.056, POST_H + 0.055),
                  (0.047, POST_H + 0.062)], segments=36, mat=2)
    geoms.append(bead)
    zb = POST_H + 0.058
    bud = lathe([(0.041, zb), (0.060, zb + 0.020), (0.070, zb + 0.041),
                 (0.067, zb + 0.057), (0.054, zb + 0.077), (0.033, zb + 0.091),
                 (0.012, zb + 0.098), (0.0008, zb + FINIAL_H - 0.058)],
                segments=44, rib=10, rib_amp=0.07, mat=2)
    geoms.append(bud)
    return merge_geoms(geoms)

# ---------------------------------------------------------------- rig / render
def look_at(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def build_rig(model_coll):
    rig = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(rig)
    # ground plane (not exported)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.001))
    g = bpy.context.view_layer.objects.active
    g.name = "GroundPlane"
    g.data.materials.append(GREY)
    bpy.context.collection.objects.unlink(g)
    rig.objects.link(g)
    def light(name, loc, energy, size, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy = energy
        ld.shape = 'DISK'
        ld.size = size
        ld.color = color
        o = bpy.data.objects.new(name, ld)
        rig.objects.link(o)
        o.location = loc
        look_at(o, (0, 0, 0.5))
        return o
    light("Key", (-4.5, -5.5, 6.5), 1100, 5.0)
    light("Fill", (5.5, -2.5, 3.0), 320, 4.0)
    light("Rim", (0.5, 5.0, 5.5), 500, 3.0)
    return rig

def shot(rig, name, loc, target, lens=58):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    o = bpy.data.objects.new(name, cd)
    rig.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

def main():
    global RED, BLUE, GILT, TIMBER, DARK, GREY
    bpy.ops.wm.read_factory_settings(use_empty=True)
    RED = make_mat("RailingRedPaint", (0.36, 0.055, 0.038), 0.10, 0.48)
    BLUE = make_mat("NewelBluePaint", (0.070, 0.135, 0.33), 0.10, 0.44)
    GILT = make_mat("Gilt", (0.83, 0.60, 0.24), 0.95, 0.30)
    TIMBER = make_mat("HandrailTimber", (0.24, 0.115, 0.050), 0.0, 0.50)
    DARK = make_mat("DarkIron", (0.05, 0.05, 0.055), 0.6, 0.6)
    GREY = make_mat("BackdropGrey", (0.5, 0.5, 0.5), 0.0, 1.0)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    model = bpy.data.collections.new("Model")
    scene.collection.children.link(model)

    builders = [
        ("Lattice", build_lattice(), [RED]),
        ("Bosses", build_bosses(), [RED, GILT]),
        ("BottomChannel", build_channel(), [RED]),
        ("Handrail", build_handrail(), [TIMBER]),
        ("FrameStandard", build_standard(), [RED, DARK]),
        ("NewelPost", build_newel(), [BLUE, DARK, GILT]),
    ]
    objs = []
    for name, geom, mats in builders:
        # bake the centring shift into the geometry: identity transforms,
        # prop origin at the base centre of the assembly
        vs, fs, ts = geom
        geom = ([(x + SHIFT, y, z) for (x, y, z) in vs], fs, ts)
        ob = make_object(name, geom, mats)
        scene.collection.objects.unlink(ob)
        model.objects.link(ob)
        objs.append(ob)

    rig = build_rig(model)

    scene.world = bpy.data.worlds.new("W")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.32, 0.32, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

    # stats (world space, after shift)
    total = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris = len(o.data.loop_triangles)
        total += tris
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
        print(f"STATS {o.name}: tris={tris} "
              f"x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] z[{min(zs):.3f},{max(zs):.3f}]")
    print(f"STATS TOTAL tris={total}")

    blend_path = os.path.join(OUT, "gallery-lattice-railing.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("saved", blend_path)

    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    glb_path = os.path.join(OUT, "gallery-lattice-railing.glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', use_selection=True)
    print("saved", glb_path)

    if os.environ.get('BUILD_ONLY'):
        print('BUILD_ONLY: skipping renders')
        return

    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1300
    scene.render.resolution_y = 1020

    cams = {
        "front": shot(rig, "CamFront", (0, -5.4, 0.62), (0, 0, 0.52), lens=60),
        "side": shot(rig, "CamSide", (5.6, -0.4, 0.62), (0, 0, 0.50), lens=60),
        "three-quarter": shot(rig, "CamTQ", (3.1, -3.9, 2.1), (0, 0, 0.46), lens=55),
    }
    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(RENDERS, name + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", name)

    # arrayed run: two extra panel+standard copies (newel only at the start)
    array_pitch = STD_CX            # newel centre -> standard centre = 2.8127
    copies = []
    for k in (1, 2):
        for o in objs:
            if o.name == "NewelPost":
                continue
            d = o.copy()
            d.data = o.data
            model.objects.link(d)
            d.location.x = k * array_pitch
            d.location.y = 0.0006 * k   # sub-mm offset kills z-fighting
            copies.append(d)
    cam = shot(rig, "CamRun", (2.81, -11.0, 1.6), (2.81, 0, 0.48), lens=40)
    scene.camera = cam
    scene.render.filepath = os.path.join(RENDERS, "run.png")
    bpy.ops.render.render(write_still=True)
    print("rendered run")
    for d in copies:
        bpy.data.objects.remove(d, do_unlink=True)
    # re-save the clean blend (copies were never saved, but be certain)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("re-saved clean blend")

if __name__ == "__main__":
    main()
