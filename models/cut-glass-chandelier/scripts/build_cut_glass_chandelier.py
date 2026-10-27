#!/usr/bin/env python3
"""
Build: Cut-glass chandelier (candidate #32) — Crystal Palace film prop.

Source: ONE engraving, `references/muse-drive/images/commons/Crystal_Palace00.jpg`
("Cut glass chandelier. From The Crystal Palace, and its contents, collective
work, London, 1851-1852"; manifest licence: Public domain). The plate is a
full frontal elevation, so every proportion below is MEASURED off it
(silhouette scan + feature positions, image 1276x1600, ink bbox
x 63..1204, y 44..1548, centre x 634). Absolute size is NOT in the source:
H = 5.5 m is an adopted grand-exhibition scale (see NOTES.md) -- all
proportions are fractions of H and hold at any rescale.

Design (fractions of total height H; z from the bottom tip of the finial):
  canopy r .093 z .955-1.0 + icicle fringe; diamond-cut shaft r ~.072
  z .541-.905; 12 fluted finial vases r .030 on scroll arms at R .195,
  bodies z .620-.715, spears to z .80, pendant cups below to z .555;
  fluted mid band z .485-.541; mid candle ring R .235 (24 candles, cups
  z .497); trumpet cone to the rim band r .368 z .155-.25; lower tier:
  12 crystal spears at R .300 (tips z .460), inner candle row R .300
  (24, cups z .285), shells behind the outer ring, outer candle row
  R .345 (48, cups z .222), rosette-bead swags on every ring, lozenge
  fringe under the rim, ball pendants, and the central petal-cup finial
  ending in a faceted ball at z 0. 12 tent chains of faceted beads drape
  the whole profile from canopy to rim.

Everything repeated (beads, drops, candles, spears, vases) is built once
as a low-poly unit and merged as transformed copies. Origin at the base
centre: (0,0,0) is the bottom tip of the central finial ball.
Real-world metres, Z up, all transforms baked into the geometry.
"""
import bpy
import math
import os
from mathutils import Vector, Matrix

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "cut-glass-chandelier"
H = 5.5  # adopted overall height, metres (INFERRED -- see NOTES.md)

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# ---------------------------------------------------------------- materials
def make_glass_cut(name="GlassCut", strength=0.65, distance=0.02):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.07
    bsdf.inputs["IOR"].default_value = 1.52
    bsdf.inputs["Transmission Weight"].default_value = 1.0
    img = bpy.data.images.load(os.path.join(BASE, "textures", "diamond_cut.png"))
    img.pack()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.extension = 'REPEAT'
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance
    nt.links.new(tex.outputs["Color"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m

def make_glass_fluted():
    # For the finial vases: full transmission, NO diamond bump -- their
    # read is the geometric fluting, as drawn (the plate's vases are
    # fluted, not diamond-cut).
    m = bpy.data.materials.new("GlassFluted")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["IOR"].default_value = 1.52
    bsdf.inputs["Transmission Weight"].default_value = 1.0
    return m

def make_glass_bright():
    # Small instanced elements: partial-transmission glossy dielectric --
    # full transmission on the big bodies, a lighter glass for the
    # hundreds of small parts so renders stay tractable. Stated in NOTES.md.
    m = bpy.data.materials.new("GlassBright")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.97, 0.98, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.10
    bsdf.inputs["IOR"].default_value = 1.52
    bsdf.inputs["Transmission Weight"].default_value = 0.6
    bsdf.inputs["Coat Weight"].default_value = 1.0
    bsdf.inputs["Coat Roughness"].default_value = 0.06
    return m

def make_wax():
    m = bpy.data.materials.new("CandleWax")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.96, 0.93, 0.85, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.45
    bsdf.inputs["Subsurface Weight"].default_value = 0.25
    bsdf.inputs["Subsurface Radius"].default_value = (0.02, 0.015, 0.01)
    return m

GLASS_CUT = make_glass_cut()
GLASS_CUT_SOFT = make_glass_cut("GlassCutSoft", strength=0.30, distance=0.010)
GLASS_FLUTED = make_glass_fluted()
GLASS_BRIGHT = make_glass_bright()
WAX = make_wax()

# ---------------------------------------------------------------- geom toolkit
# A geom is (verts, faces, uvs); faces are tuples of indices (quads or tris).

def lathe_geom(profile, segs, flute_n=0, flute_d=0.0, u_rep=1.0, v_rep=1.0):
    """Rotate a profile [(r, z), ...] (bottom -> top) about the Z axis."""
    verts, faces, uvs = [], [], []
    n = len(profile)
    for i in range(segs):
        th = 2.0 * math.pi * i / segs
        fm = 1.0 + (flute_d * math.cos(flute_n * th) if flute_n else 0.0)
        ct, st = math.cos(th), math.sin(th)
        for j, (r, z) in enumerate(profile):
            rr = r * fm
            verts.append((rr * ct, rr * st, z))
            uvs.append((i / segs * u_rep, j / max(1, n - 1) * v_rep))
    for i in range(segs):
        i2 = (i + 1) % segs
        for j in range(n - 1):
            a, b, c, d = i * n + j, i2 * n + j, i2 * n + j + 1, i * n + j + 1
            if profile[j][0] == 0.0 and profile[j + 1][0] == 0.0:
                continue
            if profile[j][0] == 0.0:
                faces.append((a, c, d))
            elif profile[j + 1][0] == 0.0:
                faces.append((a, b, c))
            else:
                faces.append((a, b, c, d))
    return verts, faces, uvs

def tube_geom(pts, radius, segs=6):
    """Tube along a planar (y=0) path of Vectors; capped ends."""
    verts, faces, uvs = [], [], []
    rings = []
    n = len(pts)
    for k, p in enumerate(pts):
        if k == 0:
            tan = pts[1] - pts[0]
        elif k == n - 1:
            tan = pts[-1] - pts[-2]
        else:
            tan = pts[k + 1] - pts[k - 1]
        tan.normalize()
        nrm = Vector((tan.z, 0.0, -tan.x))  # in-plane normal
        ring = []
        for i in range(segs):
            a = 2.0 * math.pi * i / segs
            off = nrm * (radius * math.cos(a)) + Vector((0, 1, 0)) * (radius * math.sin(a))
            ring.append(len(verts))
            verts.append(tuple(p + off))
            uvs.append((0.0, 0.0))
        rings.append(ring)
    for k in range(n - 1):
        for i in range(segs):
            i2 = (i + 1) % segs
            faces.append((rings[k][i], rings[k][i2], rings[k + 1][i2], rings[k + 1][i]))
    c0 = len(verts); verts.append(tuple(pts[0])); uvs.append((0, 0))
    c1 = len(verts); verts.append(tuple(pts[-1])); uvs.append((0, 0))
    for i in range(segs):
        i2 = (i + 1) % segs
        faces.append((rings[0][i2], rings[0][i], c0))
        faces.append((rings[-1][i], rings[-1][i2], c1))
    return verts, faces, uvs

def xg(geom, M):
    verts, faces, uvs = geom
    return [tuple(M @ Vector(v)) for v in verts], faces, uvs

def merge(geoms):
    V, F, U = [], [], []
    off = 0
    for verts, faces, uvs in geoms:
        V += verts
        U += list(uvs) if uvs else [(0.0, 0.0)] * len(verts)
        F += [tuple(i + off for i in f) for f in faces]
        off += len(verts)
    return V, F, U

def rotz(a):
    return Matrix.Rotation(a, 4, 'Z')

def trans(x, y, z):
    return Matrix.Translation((x, y, z))

def scl(sx, sy, sz):
    return Matrix.Diagonal((sx, sy, sz, 1.0))

def make_object(name, geom, mat, smooth=True):
    verts, faces, uvs = geom
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if uvs and len(uvs) == len(verts):
        uv = me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            uv.data[loop.index].uv = uvs[loop.vertex_index]
    if mat:
        me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob

def tri_count():
    total = 0
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            me = ob.data
            me.calc_loop_triangles()
            total += len(me.loop_triangles)
    return total

F = H  # shorthand: dimensions below are written as fractions of H times H

# ================================================================ UNIT GEOMS
# Faceted bead + flange (tent chains): unit height 1, max radius 0.55.
BEAD = lathe_geom([(0.0, 0.0), (0.55, 0.0), (0.55, 0.12), (0.47, 0.50),
                   (0.0, 1.0)], 6)
# Rosette swag bead: squat closed cylinder.
ROSETTE = lathe_geom([(0.0, 0.0), (0.5, 0.0), (0.5, 1.0), (0.0, 1.0)], 6)
# Lozenge drop: unit height 1, max radius 0.45 at mid.
DROP = lathe_geom([(0.0, 0.0), (0.45, 0.30), (0.45, 0.62), (0.0, 1.0)], 6)

def candle_geom(cup_h, candle_h, candle_r=0.0026 * F):
    """Glass cup (own geom) built separately; this returns (glass, wax)."""
    cup = lathe_geom([(0.0, 0.0), (0.040, 0.004), (0.044, 0.026),
                      (0.032, cup_h)], 6)
    wax = lathe_geom([(0.0, 0.0), (candle_r, 0.0), (candle_r * 0.92, candle_h * 0.82),
                      (candle_r * 0.45, candle_h * 0.96), (0.0, candle_h)], 6)
    wax = xg(wax, trans(0, 0, cup_h * 0.55))
    return cup, wax

def swag_geom(ring_r, span_deg, n_beads, bead_d, sag, attach_z):
    """Catenary-ish swag of rosette beads between adjacent points on a ring.
    Built in a local frame: origin at ring centre height attach_z, swag in
    the XZ plane spanning +/- span/2 around the +X direction."""
    parts = []
    half = math.radians(span_deg) / 2.0
    p0 = Vector((ring_r * math.cos(-half), ring_r * math.sin(-half), attach_z))
    p1 = Vector((ring_r * math.cos(half), ring_r * math.sin(half), attach_z))
    for i in range(n_beads):
        u = (i + 0.5) / n_beads
        pos = p0.lerp(p1, u)
        pos.z = attach_z - sag * (1.0 - (2.0 * u - 1.0) ** 2)
        # bead axis points radially outward (flat rosette face out), as drawn
        th_b = math.atan2(pos.y, pos.x)
        M = (trans(pos.x, pos.y, pos.z)
             @ rotz(th_b) @ Matrix.Rotation(math.pi / 2, 4, 'Y')
             @ scl(bead_d, bead_d, bead_d * 0.55) @ trans(0, 0, -0.5))
        parts.append(xg(ROSETTE, M))
    return merge(parts)

# ================================================================ BODIES
def prof(pts):
    return [(r * F, z * F) for r, z in pts]

# --- canopy: frieze disc + stepped underside, z .955..1.0
canopy = lathe_geom(prof([
    (0.0, 0.955), (0.055, 0.955), (0.078, 0.958), (0.090, 0.966),
    (0.093, 0.978), (0.093, 0.994), (0.088, 1.0), (0.0, 1.0)]), 36,
    u_rep=8, v_rep=1)
make_object("Canopy", canopy, GLASS_CUT)

# --- shaft: near-cylinder with beaded ring ridges, z .541..905
shaft_prof = [(0.0, 0.541), (0.062, 0.541)]
z = 0.548
while z < 0.900:
    r = 0.0755 - (z - 0.541) * (0.0065 / 0.364)
    shaft_prof.append((r, z))
    shaft_prof.append((r + 0.0022, z + 0.006))
    shaft_prof.append((r + 0.0022, z + 0.011))
    shaft_prof.append((r, z + 0.017))
    z += 0.0364
shaft_prof += [(0.069, 0.905), (0.0, 0.905)]
make_object("Shaft", lathe_geom(prof(shaft_prof), 36, u_rep=10, v_rep=7),
            GLASS_CUT)

# --- mid band: fluted drum, z .485..541
band = lathe_geom(prof([
    (0.0, 0.485), (0.066, 0.485), (0.078, 0.492), (0.080, 0.505),
    (0.080, 0.528), (0.076, 0.541), (0.0, 0.541)]), 48,
    flute_n=40, flute_d=0.045, u_rep=12, v_rep=1)
make_object("MidBand", band, GLASS_CUT)

# --- lower body: trumpet cone + rim band in one lathe, z .145..485
# (rim band top lowered to z .212 so the outer candle row stands proud of it;
#  three subtle beaded ridges up the cone, as drawn)
lower = lathe_geom(prof([
    (0.0, 0.145), (0.30, 0.148), (0.360, 0.155), (0.368, 0.170),
    (0.368, 0.212), (0.364, 0.228), (0.348, 0.240), (0.320, 0.262),
    (0.288, 0.285), (0.258, 0.306), (0.263, 0.315), (0.252, 0.326),
    (0.218, 0.340), (0.190, 0.362), (0.195, 0.371), (0.185, 0.380),
    (0.155, 0.398), (0.132, 0.418), (0.137, 0.427), (0.128, 0.436),
    (0.105, 0.450), (0.088, 0.470),
    (0.078, 0.485), (0.0, 0.485)]), 48, u_rep=14, v_rep=5)
make_object("LowerBody", lower, GLASS_CUT_SOFT)

# --- bottom finial: petal cup, fluted cone, collar, faceted ball
finial = lathe_geom(prof([
    (0.0, 0.0), (0.020, 0.004), (0.026, 0.018), (0.024, 0.038),
    (0.013, 0.052), (0.013, 0.058), (0.020, 0.064), (0.016, 0.072),
    (0.026, 0.088), (0.052, 0.112), (0.070, 0.138), (0.068, 0.158),
    (0.040, 0.168), (0.0, 0.168)]), 24, flute_n=12, flute_d=0.05,
    u_rep=6, v_rep=2)
make_object("BottomFinial", finial, GLASS_CUT)

# ================================================================ TENT CHAINS
CHAIN_PATH = [  # (r, z) fractions of H, canopy -> rim, hugging the profile
    (0.098, 0.958), (0.086, 0.900), (0.082, 0.800), (0.082, 0.700),
    (0.084, 0.600), (0.088, 0.545), (0.096, 0.500), (0.114, 0.462),
    (0.143, 0.425), (0.176, 0.388), (0.213, 0.350), (0.252, 0.315),
    (0.300, 0.282), (0.345, 0.250), (0.372, 0.218)]
path = [Vector((r * F, 0.0, z * F)) for r, z in CHAIN_PATH]
# arc-length table
segs_len = []
total_len = 0.0
for i in range(len(path) - 1):
    L = (path[i + 1] - path[i]).length
    segs_len.append(L)
    total_len += L

def point_at(s):
    """Point + tangent at arc length s along the chain path."""
    acc = 0.0
    for i, L in enumerate(segs_len):
        if s <= acc + L or i == len(segs_len) - 1:
            u = max(0.0, min(1.0, (s - acc) / L)) if L > 0 else 0.0
            p = path[i].lerp(path[i + 1], u)
            t = (path[i + 1] - path[i]).normalized()
            return p, t
        acc += L
    return path[-1], (path[-1] - path[-2]).normalized()

strand_parts = []
s = 0.0
while s < total_len:
    u = s / total_len
    pitch = (0.027 + 0.011 * u) * F           # beads grow down the strand
    p, t = point_at(s + pitch * 0.5)
    phi = math.atan2(t.x, t.z)                # tilt from +Z, in the XZ plane
    w = pitch * 0.58                          # bead width ~0.58 x pitch
    M = (trans(p.x, p.y, p.z)
         @ Matrix.Rotation(phi, 4, 'Y')
         @ scl(w / 1.1, w / 1.1, pitch))
    strand_parts.append(xg(BEAD, M))
    s += pitch
strand = merge(strand_parts)
chains = merge([xg(strand, rotz(math.radians(30 * k))) for k in range(12)])
make_object("TentChains", chains, GLASS_BRIGHT, smooth=False)

# ================================================================ UPPER FINIALS (x12)
R_VASE = 0.195 * F
# vase body + lid (GlassCut): pendant cup hangs below, dome + spear above
vase = lathe_geom(prof([
    (0.0, 0.617), (0.020, 0.617), (0.028, 0.626), (0.030, 0.645),
    (0.030, 0.700), (0.027, 0.715), (0.012, 0.724), (0.0, 0.726)]), 14,
    flute_n=12, flute_d=0.09)
vase = xg(vase, trans(R_VASE, 0, 0))
vases = merge([xg(vase, rotz(math.radians(22.5 + 30 * k))) for k in range(12)])
make_object("UpperVases", vases, GLASS_FLUTED)

# spear finial on the dome: small turned obelisk (unit local, base z .715)
spear_up = lathe_geom(prof([
    (0.0, 0.715), (0.016, 0.715), (0.018, 0.724), (0.008, 0.732),
    (0.011, 0.742), (0.009, 0.762), (0.005, 0.786), (0.0, 0.802)]), 10)
# pendant cup under the vase (inverted fluted cup)
pend = lathe_geom(prof([
    (0.0, 0.552), (0.008, 0.552), (0.013, 0.568), (0.021, 0.592),
    (0.024, 0.612), (0.022, 0.620), (0.0, 0.620)]), 12,
    flute_n=10, flute_d=0.05)
# scroll arm: tube from the shaft, small volute curl, out to the vase
arm_pts = [Vector((r * F, 0, z * F)) for r, z in [
    (0.070, 0.600), (0.082, 0.578), (0.100, 0.572), (0.112, 0.584),
    (0.106, 0.602), (0.128, 0.592), (0.158, 0.600), (0.182, 0.618),
    (0.192, 0.636)]]
arm = tube_geom(arm_pts, 0.0048 * F, 6)
# spear_up/pend are built around the axis; shift them out to R_VASE, then rotate.
finial_bright = []
for k in range(12):
    M = rotz(math.radians(22.5 + 30 * k))
    finial_bright.append(xg(xg(spear_up, trans(R_VASE, 0, 0)), M))
    finial_bright.append(xg(xg(pend, trans(R_VASE, 0, 0)), M))
    finial_bright.append(xg(arm, M))
make_object("UpperArmsSpearsPendants", merge(finial_bright), GLASS_BRIGHT)

# drops under the pendant cups + swags between them
vdrops = []
for k in range(12):
    a = math.radians(22.5 + 30 * k)
    vdrops.append(xg(DROP, trans(R_VASE * math.cos(a), R_VASE * math.sin(a),
                                 0.512 * F) @ scl(0.016 * F, 0.016 * F, 0.040 * F)))
make_object("VaseDrops", merge(vdrops), GLASS_BRIGHT, smooth=False)
vswags = merge([xg(swag_geom(R_VASE, 30.0, 5, 0.008 * F, 0.018 * F, 0.572 * F),
                   rotz(math.radians(22.5 + 30 * k + 15))) for k in range(12)])
make_object("VaseSwags", vswags, GLASS_BRIGHT, smooth=False)

# ================================================================ CANOPY FRINGE
fringe = []
for k in range(24):
    a = math.radians(15 * k)
    fringe.append(xg(DROP, trans(0.086 * F * math.cos(a), 0.086 * F * math.sin(a),
                                 0.898 * F) @ scl(0.013 * F, 0.013 * F, 0.058 * F)))
for k in range(18):
    a = math.radians(10 + 20 * k)
    fringe.append(xg(DROP, trans(0.064 * F * math.cos(a), 0.064 * F * math.sin(a),
                                 0.918 * F) @ scl(0.011 * F, 0.011 * F, 0.042 * F)))
make_object("CanopyFringe", merge(fringe), GLASS_BRIGHT, smooth=False)

# ================================================================ CANDLE RINGS
def ring_band(R, z, tube_r, name):
    prof_t = []
    for i in range(7):
        a = 2 * math.pi * i / 6
        prof_t.append((R + tube_r * math.cos(a), z + tube_r * math.sin(a)))
    g = lathe_geom(prof_t, 60)
    return make_object(name, g, GLASS_BRIGHT)

def candle_ring(R, z_cup, cup_h, candle_h, count, phase_deg, name):
    cup_g, wax_g = candle_geom(cup_h, candle_h)
    cups, waxs = [], []
    for k in range(count):
        a = math.radians(phase_deg + 360.0 * k / count)
        M = trans(R * math.cos(a), R * math.sin(a), z_cup)
        cups.append(xg(cup_g, M))
        waxs.append(xg(wax_g, M))
    make_object(name + "Cups", merge(cups), GLASS_BRIGHT)
    return merge(waxs)

wax_all = []
R_MID, R_IN, R_OUT = 0.235 * F, 0.300 * F, 0.352 * F
ring_band(R_MID, 0.490 * F, 0.0035 * F, "MidRingBand")
wax_all.append(candle_ring(R_MID, 0.497 * F, 0.055, 0.26, 24, 0.0, "Mid"))
ring_band(R_IN, 0.280 * F, 0.0035 * F, "InnerRingBand")
wax_all.append(candle_ring(R_IN, 0.285 * F, 0.055, 0.34, 24, 7.5, "Inner"))
ring_band(R_OUT, 0.212 * F, 0.0040 * F, "OuterRingBand")
wax_all.append(candle_ring(R_OUT, 0.218 * F, 0.055, 0.23, 48, 0.0, "Outer"))
make_object("CandleWax", merge(wax_all), WAX)

# swags + drops on the mid ring
mswags = merge([xg(swag_geom(R_MID, 15.0, 5, 0.011 * F, 0.016 * F, 0.490 * F),
                   rotz(math.radians(15 * k + 7.5))) for k in range(24)])
make_object("MidSwags", mswags, GLASS_BRIGHT, smooth=False)
mdrops = []
for k in range(24):
    a = math.radians(15 * k + 7.5)
    mdrops.append(xg(DROP, trans(R_MID * math.cos(a), R_MID * math.sin(a),
                                 0.428 * F) @ scl(0.014 * F, 0.014 * F, 0.034 * F)))
make_object("MidDrops", merge(mdrops), GLASS_BRIGHT, smooth=False)

# ================================================================ LOWER SPEARS + SHELLS
spear_lo = lathe_geom(prof([  # ornate stem, oval medallion, faceted point
    (0.0, 0.272), (0.020, 0.272), (0.022, 0.282), (0.010, 0.292),
    (0.009, 0.318), (0.016, 0.330), (0.016, 0.344), (0.009, 0.356),
    (0.012, 0.366), (0.018, 0.376), (0.008, 0.384), (0.011, 0.396),
    (0.013, 0.420), (0.009, 0.442), (0.0, 0.460)]), 8)
spear_lo = xg(spear_lo, trans(R_IN, 0, 0))
spears = merge([xg(spear_lo, rotz(math.radians(30 * k))) for k in range(12)])
make_object("LowerSpears", spears, GLASS_BRIGHT, smooth=False)

def shell_geom(radius, arc_deg=100.0, segs=9, rings=3):
    """Scallop fan: hinge at origin, opening up in the XZ plane, cupped -Y."""
    verts, faces, uvs = [], [], []
    idx = {}
    for j in range(rings + 1):
        for i in range(segs + 1):
            a = math.radians(-arc_deg / 2 + arc_deg * i / segs)
            rr = radius * j / rings
            x = rr * math.sin(a)
            z = rr * math.cos(a)
            y = -0.22 * rr * (j / rings)
            idx[(i, j)] = len(verts)
            verts.append((x, y, z))
            uvs.append((0.0, 0.0))
    for j in range(rings):
        for i in range(segs):
            faces.append((idx[(i, j)], idx[(i + 1, j)], idx[(i + 1, j + 1)],
                          idx[(i, j + 1)]))
    return verts, faces, uvs

shell = shell_geom(0.052 * F)
shells = []
for k in range(12):
    a = math.radians(30 * k)
    # local fan: hinge at origin, opens +Z (up), concave side +Y.
    # rotz(a - 90 deg) maps local +Y to the radial outward direction;
    # rotx(+12 deg) leans the fan top back against the cone.
    M = (trans(0.322 * F * math.cos(a), 0.322 * F * math.sin(a), 0.246 * F)
         @ rotz(a - math.pi / 2) @ Matrix.Rotation(math.radians(12), 4, 'X'))
    shells.append(xg(shell, M))
make_object("Shells", merge(shells), GLASS_BRIGHT)

# ================================================================ LOWER SWAGS + FRINGE + PENDANTS
lswags = merge([xg(swag_geom(R_OUT, 30.0, 9, 0.011 * F, 0.028 * F, 0.212 * F),
                   rotz(math.radians(30 * k + 15))) for k in range(12)])
make_object("LowerSwags", lswags, GLASS_BRIGHT, smooth=False)

fringe2 = []
for k in range(48):
    a = math.radians(7.5 * k + 3.75)
    fringe2.append(xg(DROP, trans(0.366 * F * math.cos(a), 0.366 * F * math.sin(a),
                                  0.104 * F) @ scl(0.017 * F, 0.017 * F, 0.052 * F)))
for k in range(12):  # ball pendants at the branch points
    a = math.radians(30 * k)
    ball = lathe_geom([(0.0, 0.0), (0.5, 0.08), (0.72, 0.35), (0.72, 0.62),
                       (0.42, 0.88), (0.0, 1.0)], 8)
    fringe2.append(xg(ball, trans(0.366 * F * math.cos(a), 0.366 * F * math.sin(a),
                                  0.100 * F) @ scl(0.030 * F, 0.030 * F, 0.034 * F)))
    stem = lathe_geom([(0.0, 0.0), (0.16, 0.0), (0.16, 1.0), (0.0, 1.0)], 6)
    fringe2.append(xg(stem, trans(0.366 * F * math.cos(a), 0.366 * F * math.sin(a),
                                  0.134 * F) @ scl(0.012 * F, 0.012 * F, 0.024 * F)))
make_object("RimFringe", merge(fringe2), GLASS_BRIGHT, smooth=False)

# ================================================================ SUSPENSION (ADDED -- not in the engraving)
stem = lathe_geom(prof([(0.0, 1.0), (0.008, 1.0), (0.008, 1.022), (0.0, 1.022)]), 10)
circ = [Vector((0.013 * F * math.cos(2 * math.pi * i / 16), 0.0,
                (1.022 + 0.013) * F + 0.013 * F * math.sin(2 * math.pi * i / 16)))
        for i in range(17)]
eye = tube_geom(circ, 0.0045 * F, 6)
make_object("Suspension_ADDED", merge([stem, eye]), GLASS_BRIGHT)

# ================================================================ SAVE + EXPORT + STATS
for ob in bpy.context.scene.objects:
    ob.select_set(False)
os.makedirs(os.path.join(BASE, "renders"), exist_ok=True)
blend_path = os.path.join(BASE, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(BASE, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
print("SAVED", blend_path)
print("EXPORTED", glb_path)
print("OBJECTS", len(bpy.context.scene.objects))
print("TRIANGLES_EVALUATED", tri_count())
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        print("  OBJ", ob.name, len(ob.data.polygons), "polys")
