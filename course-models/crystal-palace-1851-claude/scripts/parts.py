"""Part library for the Crystal Palace model: each builder returns a collection that is NOT linked to the
scene (instance sources, per controls.json), with the part's origin where ARCHITECTURE.md / BLENDER.md want it.

Scene units are metres (scale 1.0); every dimension below is written in feet and inches and converted.
Dimensions come from Downes 1852 (see ../MEASUREMENTS.md, ../CONTROL-DIMENSIONS.md); anything not on a
plate is marked INFERRED here and in ../DEPARTURES-LEDGER.md. Shapes are deliberately simple: the plates
give figured dimensions and outlines, not a single authoritative solid, and detail should be added only
where the camera will see it.

Run inside Blender (this module needs bpy).
"""
import math

import bmesh
import bpy

FT = 0.3048
IN = FT / 12.0


def ft(feet, inches=0.0):
    """Feet (and inches) to scene metres."""
    return (feet + inches / 12.0) * FT


def inch(i):
    return i * IN


# the dimensions the controls test -----------------------------------------------------------------
SHAFT_R = inch(4)                       # 8 in across (Plate VIII Fig. 13, printed page 4)
SHAFT_H = ft(18, 11.75)                 # top of the lower column above the floor (D14)
UPPER_H = ft(16, 7.5)                   # the 16 ft 7 1/2 in column between connecting pieces (printed page 4)
PIECE_H = ft(3, 4.5)                    # connecting piece (D15)
GIRDER_L = ft(23, 3.25)                 # 24 ft girder, face to face (Plate X prints 23 ft 3 1/4 in)
GIRDER_D = ft(3)                        # depth between bearing surfaces (Plate VIII, X)
PIECE_BELOW_GIRDER = inch(2.25)         # the piece starts 2 1/4 in below the girder (Plate VIII Fig. 12)
TIER_RISE = UPPER_H + PIECE_H           # 20 ft from one connecting piece to the next
ROOF_PITCH = ft(8)                      # gutter to gutter (D09)
ROOF_RISE = ft(1.6)                     # INFERRED: 49 in glass on a slope of 2 1/2 to 1 over a 4 ft run
GALLERY_T = inch(9)                     # floor structure on the girder tops: surface is 22 ft 11 in, girder top 22 ft 2 in (D12)
# The railing heights are READ OFF Plate VI's face-on lattice band (rows 2052, 2070, 2116 against the floor line at
# 2127.7, 24.74 px/ft), not printed on a plate: INFERRED, good to about 0.05 ft per reading.
RAIL_H = ft(3, 0.75)                    # top of the railing above the floor: 3.06 ft
PLINTH_H = inch(5.75)                   # cast-iron plinth: 5.7 in
RAIL_TOP_H = inch(8.75)                 # top rail band: 8.7 in (the handrail is a 2 x 3 in strip under a 2 3/4 in round rail, page 22)

# Staircases (printed pages 31 to 35, Plates XV to XVII). Printed: two flights 8 ft wide with 8 ft between them, a landing
# 24 ft long and 8 ft wide, 21 steps in each flight, eight landing columns 5 in across and 10 ft 8 in above the floor, the
# columns 7 ft 1 in / 8 ft 5 in / 7 ft 1 in apart (also printed on Plate XVII Fig. 1), step 1 ft 2 in wide and 1 1/2 in
# thick, riser 7 1/2 in deep. READ OFF Plate XV (73.65 px/ft): the landing deck is 11.46 ft above the floor, which is half
# of the 22 ft 11 in gallery surface; the going is 1.0 ft (12.1 in read) and the rise 6.5 in (6.49 read).
STAIR_RISE = inch(137.5)                # floor to landing, and landing to gallery: half of 22 ft 11 in = 275 in
STAIR_STEPS = 21                        # printed; 20 treads and the landing as the 21st step
STAIR_RISER = STAIR_RISE / STAIR_STEPS  # 6.55 in, between the read 6.49 in and the printed riser board of 7 1/2 in
STAIR_GOING = ft(1)                     # read off the plan, 1.0 ft
STAIR_RUN = STAIR_GOING * (STAIR_STEPS - 1)   # 20 ft, which with the 8 ft landing makes the 48 ft avenue
STAIR_STRING_CC = ft(7, 1)              # printed: centre to centre of the strings of a flight
STAIR_STRING_W = inch(4)                # INFERRED
STAIR_STRING_D = inch(16)               # vertical depth of the string, read off Plate XV (about 1.15 ft square to the slope)
STAIR_TREAD_W, STAIR_TREAD_T = inch(14), inch(1.5)   # printed: 1 ft 2 in wide, 1 1/2 in thick
STAIR_RISER_T = inch(1.25)              # printed riser board thickness
STAIR_RAIL_H = inch(32)                 # handrail above the nosing line, read off Plate XV (2.7 ft)
LANDING_L, LANDING_W = ft(24), ft(8)    # printed
LANDING_COL_R = inch(2.5)               # printed: 5 in external diameter
LANDING_COL_H = ft(10, 8)               # printed: of the 13 ft 1 in column, 10 ft 8 in is above the floor
LANDING_COL_X = (-ft(11, 3.5), -ft(4, 2.5), ft(4, 2.5), ft(11, 3.5))   # printed 7 ft 1 in, 8 ft 5 in, 7 ft 1 in apart
CROSS_GALLERY_L, CROSS_GALLERY_W = ft(48), ft(24)   # printed: across the avenue void, between the two main galleries
WELL_W, WELL_L = ft(8), ft(16)          # printed: the two well-holes that take the upper flights


def _material(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1.0)
    return m


def _collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)  # idempotent: rebuild from scratch
    return c


def _mesh(coll, name, verts, faces, mat="MAT_Iron", recalc=True):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in verts]
    for f in faces:
        bm.faces.new([vs[i] for i in f])
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(_material(mat, (0.82, 0.82, 0.80)))
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def box(coll, name, x0, x1, y0, y1, z0, z1, mat="MAT_Iron"):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return _mesh(coll, name, v, f, mat)


def cylinder(coll, name, r, z0, z1, seg=24, mat="MAT_Iron"):
    ring = [(r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    v = [(x, y, z0) for x, y in ring] + [(x, y, z1) for x, y in ring]
    f = [tuple(range(seg - 1, -1, -1)), tuple(range(seg, 2 * seg))]
    f += [(k, (k + 1) % seg, seg + (k + 1) % seg, seg + k) for k in range(seg)]
    return _mesh(coll, name, v, f, mat)


def bar_xz(coll, name, a, b, thick, y0, y1, mat="MAT_Iron", clip_x=None):
    """A straight bar from point a to point b in the XZ plane (each (x, z)), `thick` across the bar in that
    plane, running from y0 to y1. `clip_x` = (xmin, xmax) keeps the corners inside those limits: the corners of an
    angled bar swing out past its end points, and unclipped they poke beyond the end faces of a girder."""
    (ax, az), (bx, bz) = a, b
    d = math.hypot(bx - ax, bz - az)
    ux, uz = (bx - ax) / d, (bz - az) / d
    nx, nz = -uz * thick / 2, ux * thick / 2
    p = [(ax - nx, az - nz), (bx - nx, bz - nz), (bx + nx, bz + nz), (ax + nx, az + nz)]
    if clip_x:
        p = [(min(max(x, clip_x[0]), clip_x[1]), z) for x, z in p]
    v = [(x, y0, z) for x, z in p] + [(x, y1, z) for x, z in p]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return _mesh(coll, name, v, f, mat)


def prism_xz(coll, name, pts, y0, y1, mat="MAT_Iron"):
    """A convex polygon `pts` [(x, z), ...] in the XZ plane, extruded from y0 to y1."""
    n = len(pts)
    v = [(x, y0, z) for x, z in pts] + [(x, y1, z) for x, z in pts]
    f = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    f += [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    return _mesh(coll, name, v, f, mat)


# parts -------------------------------------------------------------------------------------------
def column_shaft():
    """Lower column above the floor: 8 in across, 18 ft 11 3/4 in tall. Origin at the foot on the axis.
    The Plate VIII section has four flat and four cylindrical faces; here it is a plain cylinder (simplified)."""
    c = _collection("PART_ColumnShaft")
    cylinder(c, "shaft", SHAFT_R, 0, SHAFT_H)
    return c


def column_upper():
    """The 16 ft 7 1/2 in column that stands between two connecting pieces. Origin at its foot on the axis."""
    c = _collection("PART_ColumnUpper")
    cylinder(c, "upper", SHAFT_R, 0, UPPER_H)
    return c


def connecting_piece():
    """Connecting piece, 3 ft 4 1/2 in long. Origin at its foot on the axis. Body 10 in across with a flange
    at each end (Plate VIII Fig. 12, 13); the four snugs and keyways are not modelled."""
    c = _collection("PART_ConnectingPiece")
    cylinder(c, "body", inch(5), 0, PIECE_H)
    cylinder(c, "flange_lo", inch(7), 0, inch(1.5))
    cylinder(c, "flange_hi", inch(7), PIECE_H - inch(1.5), PIECE_H)
    return c


def girder24():
    """Cast-iron trellis girder, 23 ft 3 1/4 in long and 3 ft deep (Plate X Fig. 3), lying along X.
    Origin at the bottom centre. Top and bottom flanges, two end struts, two inner struts at the thirds, and an
    X of diagonals in each of the three panels. Section sizes are SIMPLIFIED (Plate X sections a-f)."""
    c = _collection("PART_Girder24")
    L, D = GIRDER_L, GIRDER_D
    hx = L / 2
    ft_d, fb_d = inch(5), inch(5)                       # flange depths
    box(c, "flange_top", -hx, hx, -inch(3), inch(3), D - ft_d, D)
    box(c, "flange_bot", -hx, hx, -inch(4), inch(4), 0, fb_d)
    w = inch(1.5)
    for i, x in enumerate((-hx, hx - inch(3), -L / 6 - inch(1.5), L / 6 - inch(1.5))):
        box(c, f"strut_{i}", x, x + inch(3), -w, w, fb_d, D - ft_d)
    xs = [-hx, -L / 6, L / 6, hx]
    for k in range(3):
        x0, x1 = xs[k], xs[k + 1]
        bar_xz(c, f"diag_a{k}", (x0, fb_d), (x1, D - ft_d), inch(3), -w, w, clip_x=(-hx, hx))
        bar_xz(c, f"diag_b{k}", (x0, D - ft_d), (x1, fb_d), inch(3), -w, w, clip_x=(-hx, hx))
    return c


def roof_unit():
    """One ridge-and-valley roof unit: 8 ft gutter to gutter, 24 ft long (one bay) along X, two glass slopes
    rising from the valley to a ridge ROOF_RISE above it (INFERRED: slope 2 1/2 to 1 over a 4 ft run, from
    page 15). Origin at the valley level, centre of the unit. The solidify gives the sheet a 1 in thickness
    (evaluated geometry), growing downward so the ridge line is the top."""
    c = _collection("PART_RoofUnit")
    hx, hy = ft(12), ROOF_PITCH / 2
    v = [(-hx, -hy, 0), (hx, -hy, 0), (hx, 0, ROOF_RISE), (-hx, 0, ROOF_RISE),
         (-hx, 0, ROOF_RISE), (hx, 0, ROOF_RISE), (hx, hy, 0), (-hx, hy, 0)]
    ob = _mesh(c, "roof", v, [(0, 1, 2, 3), (4, 5, 6, 7)], "MAT_Glass", recalc=False)  # winding is upward
    m = ob.modifiers.new("Thick", "SOLIDIFY")
    m.thickness = inch(1)
    m.offset = -1
    return c


def gallery_panel():
    """One 24 x 24 ft panel of gallery floor: boards, joists and binders resting on the girder tops, 9 in thick
    (22 ft 2 in to 22 ft 11 in). Origin at the bottom centre. SIMPLIFIED to a solid slab; the real floor is
    1 in boards on trussed and common joists on binders (Plate XIV)."""
    c = _collection("PART_GalleryPanel")
    box(c, "panel", -ft(12), ft(12), -ft(12), ft(12), 0, GALLERY_T, "MAT_Floor")
    return c


def _balustrade(name, length_ft):
    """A run of gallery railing along X, `length_ft` long (Plate XVII): a cast-iron plinth, a lattice of crossing bars,
    a top rail, and standards about every 6 ft (equally spaced, both ends included). Origin at the floor surface,
    centre of the run. The lattice is SIMPLIFIED: the plate shows two rows of overlapping curved bars with rosettes
    where they cross; here straight bars cross in a single row. Heights are INFERRED (see RAIL_H, PLINTH_H)."""
    c = _collection(name)
    hx = ft(length_ft) / 2
    t = inch(2)                                      # thickness across the railing (y)
    box(c, "plinth", -hx, hx, -t / 2, t / 2, 0, PLINTH_H)
    box(c, "rail", -hx, hx, -inch(1.5), inch(1.5), RAIL_H - RAIL_TOP_H, RAIL_H)
    zb, zt = PLINTH_H, RAIL_H - RAIL_TOP_H
    w = ft(1.5)                                      # width of one cross of the lattice
    n = int(math.ceil(2 * hx / w - 1e-9))
    for k in range(n):
        x0 = -hx + k * w
        bar_xz(c, f"lat_a{k}", (x0, zb), (x0 + w, zt), inch(0.8), -inch(0.4), inch(0.4), clip_x=(-hx, hx))
        bar_xz(c, f"lat_b{k}", (x0, zt), (x0 + w, zb), inch(0.8), -inch(0.4), inch(0.4), clip_x=(-hx, hx))
    n_posts = int(math.ceil(length_ft / 6.0 - 1e-9)) + 1
    for k in range(n_posts):
        x = -hx + k * (2 * hx) / (n_posts - 1)
        xa, xb = max(x - inch(0.875), -hx), min(x + inch(0.875), hx)
        box(c, f"post{k}", xa, xb, -inch(0.7), inch(0.7), PLINTH_H, RAIL_H - RAIL_TOP_H)
    return c


def balustrade24():
    """One 24 ft run of gallery railing (see _balustrade)."""
    return _balustrade("PART_Balustrade24", 24)


def balustrade8():
    """One 8 ft run of railing, for the sides of a stair landing (see _balustrade)."""
    return _balustrade("PART_Balustrade8", 8)


def stair_flight():
    """One straight flight, run 20 ft (20 treads of 1 ft and the landing as the 21st step), rising 137.5 in in 21
    risers. Origin on the floor line at the foot of the first riser, centred across the 8 ft width; the flight runs
    along +X and rises. Two strings (I-section in life, plain polygons here), 20 treads, 20 risers, a handrail on each
    side and a baluster at every tread. SIMPLIFIED: the standards are plain bars, no lattice, no volutes, no diagonal
    struts. Used for the ground flights and, set on the landing, for the flights that go up to the galleries."""
    c = _collection("PART_StairFlight")
    r, g, run, rise = STAIR_RISER, STAIR_GOING, STAIR_RUN, STAIR_RISE
    slope = r / g                                    # the nosing line rises r per going
    half = STAIR_STRING_CC / 2
    n = STAIR_STEPS - 1                              # treads
    top = lambda x: r + slope * x - inch(3)          # top edge of the string, 3 in under the nosing line
    xe = run
    xb = (STAIR_STRING_D - top(0)) / slope           # where the bottom edge of the string meets the floor line
    poly = [(0, top(0)), (xe, top(xe)), (xe, top(xe) - STAIR_STRING_D), (xb, 0), (0, 0)]
    for side, y in (("a", -half), ("b", half)):
        prism_xz(c, f"string_{side}", poly, y - STAIR_STRING_W / 2, y + STAIR_STRING_W / 2)
    for i in range(1, n + 1):
        x0 = (i - 1) * g
        box(c, f"tread_{i}", x0, min(x0 + STAIR_TREAD_W, run), -half, half, i * r - STAIR_TREAD_T, i * r, "MAT_Wood")
        box(c, f"riser_{i}", x0, x0 + STAIR_RISER_T, -half, half, (i - 1) * r, i * r - STAIR_TREAD_T, "MAT_Wood")
    for side, y in (("a", -half - inch(1.5)), ("b", half + inch(1.5))):
        a = (0, r + STAIR_RAIL_H)
        b = (run, r + slope * run + STAIR_RAIL_H)
        bar_xz(c, f"handrail_{side}", a, b, inch(2.75), y - inch(1.5), y + inch(1.5), "MAT_Wood", clip_x=(0, run))
        for i in range(1, n + 1):
            xc = (i - 1) * g + g / 2
            z_rail = r + slope * xc + STAIR_RAIL_H - inch(1.4)
            box(c, f"baluster_{side}{i}", xc - inch(0.75), xc + inch(0.75), y - inch(0.75), y + inch(0.75), i * r, z_rail)
    return c


def stair_landing():
    """The landing deck, 24 x 8 ft, its top 137.5 in above the floor, 9 1/2 in thick (on the tops of the eight small
    columns, 10 ft 8 in). Origin at floor level under the centre. SIMPLIFIED to one slab: the real landing is boards on
    joists on two cast-iron girders along the long sides (printed page 32)."""
    c = _collection("PART_StairLanding")
    box(c, "deck", -LANDING_L / 2, LANDING_L / 2, -LANDING_W / 2, LANDING_W / 2, LANDING_COL_H, STAIR_RISE, "MAT_Floor")
    return c


def stair_column():
    """One of the eight small columns that carry a landing: 5 in across, 10 ft 8 in above the floor (printed). Origin at
    the foot on the axis. The 2 ft 5 in below the floor and the 1 ft 3 in base plate are not modelled; the section
    is a plain cylinder (the plate shows a hollow casting, 1/2 in metal)."""
    c = _collection("PART_StairColumn")
    cylinder(c, "shaft", LANDING_COL_R, 0, LANDING_COL_H)
    return c


def cross_gallery():
    """The gallery that covers a staircase: 24 ft (along X) by 48 ft (across the avenue void) and 9 in thick, with the
    two well-holes (8 ft wide by 16 ft long, printed) at the ends that take the upper flights. Origin at the bottom
    centre. SIMPLIFIED like the other gallery floors: a solid slab, here three boxes around the holes."""
    c = _collection("PART_CrossGallery")
    hx, hy, wx, wy = CROSS_GALLERY_W / 2, CROSS_GALLERY_L / 2, WELL_W / 2, WELL_L
    box(c, "strip_w", -hx, -wx, -hy, hy, 0, GALLERY_T, "MAT_Floor")
    box(c, "strip_e", wx, hx, -hy, hy, 0, GALLERY_T, "MAT_Floor")
    box(c, "strip_mid", -wx, wx, -hy + wy, hy - wy, 0, GALLERY_T, "MAT_Floor")
    return c


def build_all():
    """Build every part collection (unlinked) and return them by name."""
    return {
        "column_shaft": column_shaft(), "column_upper": column_upper(), "connecting_piece": connecting_piece(),
        "girder24": girder24(), "roof_unit": roof_unit(), "gallery_panel": gallery_panel(),
        "balustrade24": balustrade24(), "balustrade8": balustrade8(), "stair_flight": stair_flight(),
        "stair_landing": stair_landing(), "stair_column": stair_column(), "cross_gallery": cross_gallery(),
    }
