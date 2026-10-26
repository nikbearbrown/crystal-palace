#!/usr/bin/env python3
"""Build sy-subway-vault-bay — one repeatable brick fan-vault bay of the
Crystal Palace High Level station subway (opened Dec 1865, Charles Barry Jr).

Sources: round-2 conservation photographs (2025 restored interior is the
primary geometry source), Historic England list entry 1385457 description
(3 rows x 5 octagonal cream-brick columns, stone capitals, ovolo stone base
mouldings, circular fan vaults in red & cream brick laid to form diamonds,
ovolo-moulded stone ribs, roundels with polychromatic diapering, central
cast-iron gas fitting). All dimensions are PHOTO-DERIVED ESTIMATES unless
marked published — see NOTES.md for the derivation of every number.

Run: blender -b -P build_sy_subway_vault_bay.py
Re-runnable: rebuilds model, textures, .blend, .glb and all renders.
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Vector

# ----------------------------------------------------------------------------
# Dimensions (metres). Groups follow the NOTES.md evidence table.
# ----------------------------------------------------------------------------
# Published (Historic England listing / Friends of CP Subway leaflet)
VAULT_THICKNESS   = 0.30   # "little more than 30 cm thick at the top of the arch"

# Photo-measured (method in NOTES.md; brick course gauge 0.075 m assumed)
COURSE            = 0.075  # brick + mortar course height, imperial 3 in gauging
PITCH             = 3.35   # column centres, square bay (fan radius ~31 courses)
COL_FLATS         = 0.73   # octagonal column across flats
SHAFT_H           = 2.55   # brick shaft height, ~34 courses counted
ROUNDEL_D         = 1.15   # central roundel diameter per cell (~0.34 x pitch)
GAS_D             = 0.45   # dark central gas-fitting disc diameter

# Photo-proportioned (ratios read off the photographs)
PLINTH_H          = 0.20   # square stone plinth
PLINTH_W          = 1.02
BASE_BRICK_H      = 0.16   # slightly wider brick base drum
BASE_BRICK_FLATS  = 0.82
BASE_RING_H       = 0.12   # stone ovolo moulding at base
CAP_SCALLOP_H     = 0.14   # scalloped stone band at capital foot
CAP_BELL_H        = 0.34   # flaring bell + ovolo rings above it
CAP_TOP_R         = 0.54   # radius of capital abacus / fan foot
SPRINGING         = PLINTH_H + BASE_BRICK_H + BASE_RING_H + SHAFT_H + CAP_SCALLOP_H + CAP_BELL_H  # 3.51
CROWN             = SPRINGING + 1.50   # roundel plane height
ARCH_CROWN        = SPRINGING + 1.15   # perimeter arch crown at bay-edge midpoints
RIB_W             = 0.15   # stone rib width
RIB_PROUD         = 0.05   # rib projection below vault surface (plus embed)
FLOOR_T           = 0.15   # floor slab patch thickness

A = PITCH / 2.0            # half pitch
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sy-subway-vault-bay"

# Palette (sampled by eye from the 2025 restored-interior photograph)
RED    = np.array([0.400, 0.105, 0.052])   # deep red brick, as restored 2025
CREAM  = np.array([0.760, 0.640, 0.455])
MORTAR = np.array([0.440, 0.395, 0.330])
STONE  = (0.520, 0.455, 0.350, 1.0)
IRON   = (0.055, 0.052, 0.055, 1.0)

rng = np.random.default_rng(1865)

# ----------------------------------------------------------------------------
# Texture painting (numpy). All textures are generated procedurally by this
# script — no external/photo textures anywhere in the model.
# ----------------------------------------------------------------------------
def save_image(name, arr):
    """arr: float array HxWx3 in 0..1 (sRGB-ish). Returns bpy image, packed."""
    h, w, _ = arr.shape
    img = bpy.data.images.new(name, w, h)
    rgba = np.ones((h, w, 4), dtype=np.float32)
    rgba[:, :, :3] = np.clip(arr, 0, 1).astype(np.float32)
    img.pixels.foreach_set(rgba.ravel())
    img.pack()
    path = os.path.join(HERE, "textures", name + ".png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.filepath_raw = path
    img.file_format = 'PNG'
    img.save()
    return img

def brick_jitter(shape, course_ids, brick_ids, amp=0.055):
    """Per-brick tonal jitter from a seeded hash of (course, brick) ids."""
    key = (course_ids * 131 + brick_ids * 17) % 1024
    lut = rng.uniform(-amp, amp, 1024).astype(np.float32)
    return lut[key]

def paint_vault_texture(size=2048):
    """Plan-view texture of one bay: column at centre, quarter roundels at the
    corners. Brick courses are concentric arcs around the column (the fan);
    colour bands step diagonally across each quadrant so four fans compose
    the diamond pattern of the real ceiling."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x = (xx / (size - 1) - 0.5) * PITCH          # metres, module coords
    y = (yy / (size - 1) - 0.5) * PITCH
    r = np.sqrt(x * x + y * y)
    th = np.arctan2(y, x)                        # -pi..pi
    course_f = r / COURSE
    course_i = np.floor(course_f)
    # angular brick joints: brick length ~0.225 m along the arc, staggered
    arc = np.maximum(r, 0.09)
    brick_f = (th * arc) / 0.225 + (course_i % 2) * 0.5
    brick_i = np.floor(brick_f)
    # --- colour bands: diagonal, stepped to the course grid ---------------
    # Quadrant phase is offset 45 degrees so band resets fall on the groins
    # (covered by the diagonal ribs), and bands run continuous across the
    # bay edges, as they do from fan to fan in the real ceiling.
    quad = ((th + math.pi / 4) % (math.pi / 2)) / (math.pi / 2)  # 0..1 per quadrant
    band = np.floor((course_i - quad * 9.0) / 9.0)   # ~9-course diagonal bands
    is_red = (band % 2) == 0
    # red foot ring at the springing (first 2 courses read red in the photos)
    is_red = np.where(course_i < 2, True, is_red)
    jit = brick_jitter(r.shape, course_i.astype(np.int32), brick_i.astype(np.int32))
    col = np.where(is_red[..., None], RED[None, None, :], CREAM[None, None, :])
    col = col * (1.0 + jit[..., None])
    # occasional darker red brick
    dark = ((course_i * 7 + brick_i * 3) % 23) == 0
    col = np.where(dark[..., None] & is_red[..., None], col * 0.78, col)
    # --- mortar ------------------------------------------------------------
    m_course = np.minimum(np.abs(course_f - np.round(course_f)) * COURSE,
                          1.0)  # distance to joint in metres-ish
    joint_c = (np.abs(course_f - np.round(course_f)) < 0.045)
    joint_b = (np.abs(brick_f - np.round(brick_f)) < np.maximum(0.045, 0.009 / arc))
    mortar = joint_c | joint_b
    col = np.where(mortar[..., None], MORTAR[None, None, :], col)
    # --- roundels at the four corners --------------------------------------
    for cx, cy in ((-A, -A), (A, -A), (-A, A), (A, A)):
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        in_r = d < ROUNDEL_D / 2
        if not in_r.any():
            continue
        ring = np.floor(d / COURSE)
        red_b = np.broadcast_to(RED[None, None, :], d.shape + (3,))
        cream_b = np.broadcast_to(CREAM[None, None, :], d.shape + (3,))
        mort_b = np.broadcast_to(MORTAR[None, None, :], d.shape + (3,))
        rcol = np.where(((ring % 2) == 0)[..., None], red_b, cream_b)
        # diaper: small checker squares in the second ring out
        diaper = ((np.floor((np.arctan2(y - cy, x - cx) + math.pi) / (math.pi / 8)) +
                   ring) % 2) == 0
        rcol = np.where(((ring == 3) & diaper)[..., None], cream_b, rcol)
        rcol = np.where(((ring == 3) & ~diaper)[..., None], red_b, rcol)
        rmort = np.abs(d / COURSE - np.round(d / COURSE)) < 0.06
        rcol = np.where(rmort[..., None], mort_b, rcol)
        col = np.where(in_r[..., None], rcol, col)
        gas = d < GAS_D / 2
        col = np.where(gas[..., None], np.array([0.10, 0.095, 0.10])[None, None, :], col)
    return col.astype(np.float32)

def paint_shaft_texture(w=1024, h=512):
    """Stretcher-bond cream brick wrapping the octagonal shaft. Texture height
    covers exactly the shaft; width covers the full perimeter."""
    per = 8 * COL_FLATS * math.tan(math.pi / 8)     # octagon perimeter
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xm = xx / w * per
    ym = yy / h * SHAFT_H
    course_f = ym / COURSE
    course_i = np.floor(course_f)
    brick_f = xm / 0.225 + (course_i % 2) * 0.5
    brick_i = np.floor(brick_f)
    jit = brick_jitter(course_f.shape, course_i.astype(np.int32),
                       brick_i.astype(np.int32), amp=0.05)
    col = CREAM[None, None, :] * (1.0 + jit[..., None])
    dark = ((course_i * 5 + brick_i * 11) % 29) == 0
    col = np.where(dark[..., None], col * 0.86, col)
    mortar = (np.abs(course_f - np.round(course_f)) < 0.07) | \
             (np.abs(brick_f - np.round(brick_f)) < 0.05)
    col = np.where(mortar[..., None], MORTAR[None, None, :] * 0.92, col)
    return col.astype(np.float32)

def paint_foot_texture(w=512, h=128):
    """Fan foot ring: red brick courses with one cream band (as photographed
    directly above the capital)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    course_f = yy / h * 6
    course_i = np.floor(course_f)
    brick_f = xx / w * 12 + (course_i % 2) * 0.5
    brick_i = np.floor(brick_f)
    base = np.where(((course_i >= 2) & (course_i <= 3))[..., None],
                    CREAM[None, None, :], RED[None, None, :])
    jit = brick_jitter(course_f.shape, course_i.astype(np.int32),
                       brick_i.astype(np.int32), amp=0.05)
    col = base * (1.0 + jit[..., None])
    mortar = (np.abs(course_f - np.round(course_f)) < 0.08) | \
             (np.abs(brick_f - np.round(brick_f)) < 0.05)
    col = np.where(mortar[..., None], MORTAR[None, None, :], col)
    return col.astype(np.float32)

def paint_floor_texture(size=1024):
    """Stone paving: large slabs in a 45-degree diamond layout, two tones
    (the listing: paved floors in alternating stone)."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x = xx / size * PITCH
    y = yy / size * PITCH
    slab = PITCH / 4.0
    u = (x + y) / slab
    v = (x - y) / slab
    chk = (np.floor(u) + np.floor(v)) % 2
    tone1 = np.array([0.470, 0.435, 0.375])
    tone2 = np.array([0.345, 0.320, 0.280])
    col = np.where((chk == 0)[..., None], tone1[None, None, :], tone2[None, None, :])
    noise = rng.uniform(-0.03, 0.03, (size // 8, size // 8)).astype(np.float32)
    noise = np.kron(noise, np.ones((8, 8), dtype=np.float32))
    col = col * (1.0 + noise[..., None])
    joint = (np.abs(u - np.round(u)) < 0.012) | (np.abs(v - np.round(v)) < 0.012)
    col = np.where(joint[..., None], np.array([0.16, 0.15, 0.14])[None, None, :], col)
    return col.astype(np.float32)

# ----------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------
def mat_image(name, img, rough=0.92):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = 'Linear'
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return m

def mat_plain(name, rgba, rough=0.85, metallic=0.0, noise_bump=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if noise_bump:
        nt = m.node_tree.nodes.new("ShaderNodeTexNoise")
        nt.inputs["Scale"].default_value = 22.0
        nt.inputs["Detail"].default_value = 3.0
        bp = m.node_tree.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = 0.12
        m.node_tree.links.new(nt.outputs["Fac"], bp.inputs["Height"])
        m.node_tree.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m

# ----------------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------------
def octagon_prism(name, flats, z0, z1, mat, uv_mode=None, tex_h=None):
    """Octagonal prism (flat faces at 0/90/180/270 deg), world-space mesh."""
    r = flats / (2 * math.cos(math.pi / 8))
    pts = []
    for i in range(8):
        a0 = math.pi / 8 + i * math.pi / 4
        pts.append((r * math.cos(a0), r * math.sin(a0)))
    verts, faces, uvs = [], [], []
    per = 8 * flats * math.tan(math.pi / 8)
    for i in range(8):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 8]
        base = len(verts)
        verts += [(x0, y0, z0), (x1, y1, z0), (x1, y1, z1), (x0, y0, z1)]
        faces.append((base, base + 1, base + 2, base + 3))
        u0 = (i * flats * math.tan(math.pi / 8)) / per
        u1 = ((i + 1) * flats * math.tan(math.pi / 8)) / per
        v0 = 0.0 if tex_h is None else z0 / tex_h
        v1 = 1.0 if tex_h is None else z1 / tex_h
        uvs += [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    # top and bottom caps (ngons)
    base = len(verts)
    verts += [(x, y, z0) for x, y in pts]
    faces.append(tuple(base + (7 - i) for i in range(8)))
    uvs += [(0.5 + x / per, 0.5 + y / per) for x, y in pts]
    base = len(verts)
    verts += [(x, y, z1) for x, y in pts]
    faces.append(tuple(base + i for i in range(8)))
    uvs += [(0.5 + x / per, 0.5 + y / per) for x, y in pts]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    uv = me.uv_layers.new(name="UVMap")
    for loop in me.loops:
        uv.data[loop.index].uv = uvs[loop.vertex_index]
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return ob

def box(name, sx, sy, sz, cx, cy, cz, mat):
    verts = [(cx + dx * sx / 2, cy + dy * sy / 2, cz + dz * sz / 2)
             for dz in (-1, 1) for dy in (-1, 1) for dx in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.loops[li].vertex_index
            uv.data[li].uv = ((verts[v][0] - cx) / PITCH + 0.5,
                              (verts[v][1] - cy) / PITCH + 0.5)
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return ob

def lathe(name, profile, mat, segments=40, ripple=0.0):
    """profile: list of (radius, z) bottom->top. Optional radial ripple
    (scalloped band): radius modulated by cos(segments/2 * theta)."""
    verts, faces = [], []
    rings = len(profile)
    for j, (rad, z) in enumerate(profile):
        for i in range(segments):
            t = i / segments * 2 * math.pi
            rr = rad
            if ripple:
                rr = rad * (1.0 + ripple * math.cos(8 * t))
            verts.append((rr * math.cos(t), rr * math.sin(t), z))
    for j in range(rings - 1):
        for i in range(segments):
            a = j * segments + i
            b = j * segments + (i + 1) % segments
            faces.append((a, b, b + segments, a + segments))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return ob

def vault_height(x, y):
    """Height field of the fan-vault soffit over the square bay module.
    Column (fan centre) at origin; roundel centres at the four corners.
    The fan leaves the capital rim (r0) at springing level and rises with a
    steep conoid-like profile that flattens toward the crown, as the
    photographs show."""
    r = math.hypot(x, y)
    r0 = 0.60
    if r <= r0:
        return SPRINGING - (r0 - r) * 0.10     # hidden cap above the capital
    th = math.atan2(y, x)
    rb = A / max(abs(math.cos(th)), abs(math.sin(th)))   # boundary distance
    t = min((r - r0) / (rb - r0), 1.0)
    h_end = ARCH_CROWN + (CROWN - ARCH_CROWN) * abs(math.sin(2 * th)) ** 1.3
    prof = math.sin(t * math.pi / 2) ** 0.7
    h = SPRINGING + (h_end - SPRINGING) * prof
    # flatten the roundel discs at the corners
    d = min(math.hypot(x - cx, y - cy) for cx in (-A, A) for cy in (-A, A))
    if d < 0.50:
        h = CROWN
    elif d < 0.66:
        w = (d - 0.50) / 0.16
        h = CROWN * (1 - w) + h * w
    return h

def vault_patch(name, mat, seg=64):
    verts, faces, uvs = [], [], []
    for j in range(seg + 1):
        for i in range(seg + 1):
            x = -A + PITCH * i / seg
            y = -A + PITCH * j / seg
            verts.append((x, y, vault_height(x, y)))
            uvs.append((i / seg, j / seg))
    for j in range(seg):
        for i in range(seg):
            a = j * (seg + 1) + i
            # wound for downward (-Z) soffit normals
            faces.append((a, a + seg + 1, a + seg + 2, a + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    uv = me.uv_layers.new(name="UVMap")
    for loop in me.loops:
        uv.data[loop.index].uv = uvs[loop.vertex_index]
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    core = bpy.data.materials.get("VaultCore")
    if core is None:
        core = mat_plain("VaultCore", (0.045, 0.028, 0.022, 1.0), rough=0.95)
    ob.data.materials.append(core)
    sol = ob.modifiers.new("thickness", 'SOLIDIFY')
    sol.thickness = VAULT_THICKNESS
    sol.offset = -1.0    # normals point down (soffit); bulk grows upward
    sol.material_offset = 1   # cut faces read as plain structure, not pattern
    if hasattr(sol, "material_offset_rim"):
        sol.material_offset_rim = 1
    return ob

def sweep_rib(name, path, mat, w=RIB_W):
    """Sweep an ovolo-ish stone rib profile along a 3D path (list of Vector).
    The path runs 0.012 above the vault surface; the profile embeds 0.055 up
    into the vault and stands RIB_PROUD below the surface."""
    prof = [(-w / 2, 0.055), (w / 2, 0.055), (w / 2, -0.02),
            (w * 0.26, -(RIB_PROUD + 0.012)), (-w * 0.26, -(RIB_PROUD + 0.012)),
            (-w / 2, -0.02)]
    verts, faces = [], []
    n = len(path)
    for k, p in enumerate(path):
        if k == 0:
            tan = (path[1] - path[0]).normalized()
        elif k == n - 1:
            tan = (path[-1] - path[-2]).normalized()
        else:
            tan = (path[k + 1] - path[k - 1]).normalized()
        side = Vector((0, 0, 1)).cross(tan)
        if side.length < 1e-4:
            side = Vector((1, 0, 0))
        side.normalize()
        up = tan.cross(side).normalized()
        if up.z < 0:
            up = -up
        for px, py in prof:
            v = p + side * px + up * py
            verts.append(tuple(v))
    m = len(prof)
    for k in range(n - 1):
        for i in range(m):
            a = k * m + i
            b = k * m + (i + 1) % m
            faces.append((a, b, b + m, a + m))
    faces.append(tuple(range(m - 1, -1, -1)))
    faces.append(tuple((n - 1) * m + i for i in range(m)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    for p in me.polygons:
        p.use_smooth = False
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return ob

def rib_path_diag(sx, sy):
    """From the capital rim to the roundel rim along a module diagonal."""
    pts = []
    steps = 16
    r_end = math.hypot(A, A) - ROUNDEL_D / 2 - 0.02
    for k in range(steps + 1):
        t = k / steps
        r = 0.55 + (r_end - 0.55) * t
        x = sx * r / math.sqrt(2)
        y = sy * r / math.sqrt(2)
        pts.append(Vector((x, y, vault_height(x, y) + 0.012)))
    return pts

def rib_path_edge(axis, sign):
    """Along a module edge, inset half a rib width so tiled neighbours pair
    up into one full rib instead of z-fighting."""
    inset = A - (RIB_W / 2 + 0.001)
    pts = []
    steps = 20
    lo = -A + ROUNDEL_D / 2 - 0.05
    hi = A - ROUNDEL_D / 2 + 0.05
    for k in range(steps + 1):
        s = lo + (hi - lo) * k / steps
        if axis == 'x':   # edge runs along x at y = sign*inset
            x, y = s, sign * inset
        else:
            x, y = sign * inset, s
        pts.append(Vector((x, y, vault_height(x, y) + 0.012)))
    return pts

def disc(name, cx, cy, z, radius, mat, seg=20, frac=1.0):
    """Flat disc (or quarter disc when frac<1, centred on the corner)."""
    verts = [(cx, cy, z)]
    faces = []
    steps = max(3, int(seg * frac))
    for i in range(steps + 1):
        t = i / steps * (math.pi / 2 if frac < 1 else 2 * math.pi)
        # quarter discs sit at module corners: orient into the module
        verts.append((cx + radius * math.cos(t) * (1 if frac == 1 else -np.sign(cx)),
                      cy + radius * math.sin(t) * (1 if frac == 1 else -np.sign(cy)), z))
    for i in range(1, steps + 1):
        faces.append((0, i, i + 1) if frac == 1 else (0, i + 1, i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return ob

# ----------------------------------------------------------------------------
# Assembly
# ----------------------------------------------------------------------------
def build_model():
    tex_vault = save_image("vault_brick", paint_vault_texture())
    tex_shaft = save_image("cream_brick", paint_shaft_texture())
    tex_foot = save_image("foot_ring", paint_foot_texture())
    tex_floor = save_image("floor_stone", paint_floor_texture())

    m_vault = mat_image("VaultBrick", tex_vault)
    m_cream = mat_image("CreamBrick", tex_shaft)
    m_foot = mat_image("FootRingBrick", tex_foot)
    m_floor = mat_image("FloorStone", tex_floor, rough=0.8)
    m_stone = mat_plain("Stone", STONE, rough=0.85, noise_bump=True)
    m_iron = mat_plain("IronDark", IRON, rough=0.55, metallic=0.65)

    col = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(col)
    objs = []

    def add(ob):
        col.objects.link(ob)
        objs.append(ob)
        return ob

    # Floor patch (top at z=0)
    add(box("FloorSlab", PITCH, PITCH, FLOOR_T, 0, 0, -FLOOR_T / 2, m_floor))

    # Column: plinth, brick base drum, stone ovolo ring, shaft, capital
    add(box("Plinth", PLINTH_W, PLINTH_W, PLINTH_H, 0, 0, PLINTH_H / 2, m_stone))
    z = PLINTH_H
    add(octagon_prism("BaseDrum", BASE_BRICK_FLATS, z, z + BASE_BRICK_H,
                      m_cream, tex_h=SHAFT_H))
    z += BASE_BRICK_H
    add(lathe("BaseRing", [(0.45, z), (0.50, z + 0.03), (0.505, z + BASE_RING_H * 0.55),
                           (0.46, z + BASE_RING_H), (0.43, z + BASE_RING_H)], m_stone))
    z += BASE_RING_H
    shaft_top = z + SHAFT_H
    add(octagon_prism("Shaft", COL_FLATS, z, shaft_top, m_cream, tex_h=SHAFT_H))
    z = shaft_top
    # scalloped band (stone, radial ripple), then flaring bell + ovolo rings
    add(lathe("CapitalScallop", [(0.40, z), (0.435, z + 0.03),
                                 (0.445, z + CAP_SCALLOP_H - 0.02),
                                 (0.42, z + CAP_SCALLOP_H)], m_stone,
              segments=64, ripple=0.016))
    z += CAP_SCALLOP_H
    add(lathe("CapitalBell", [(0.42, z), (0.46, z + 0.05), (0.50, z + 0.13),
                              (0.475, z + 0.19), (0.52, z + 0.24),
                              (0.545, z + CAP_BELL_H - 0.05),
                              (CAP_TOP_R, z + CAP_BELL_H)], m_stone))
    # red-brick fan foot ring, tucking under the vault patch edge
    add(lathe("FanFootRing", [(CAP_TOP_R, SPRINGING - 0.03),
                              (0.575, SPRINGING + 0.01),
                              (0.615, SPRINGING + 0.05)], m_foot))

    # Vault soffit patch
    add(vault_patch("Vault", m_vault))

    # Stone ribs: diagonals (capital -> roundel) and perimeter (edge) ribs
    for sx in (-1, 1):
        for sy in (-1, 1):
            add(sweep_rib(f"RibDiag{sx:+d}{sy:+d}", rib_path_diag(sx, sy), m_stone))
    for axis, sign in (('x', 1), ('x', -1), ('y', 1), ('y', -1)):
        add(sweep_rib(f"RibEdge{axis}{sign:+d}", rib_path_edge(axis, sign), m_stone))

    return col, objs

# ----------------------------------------------------------------------------
# Render setup
# ----------------------------------------------------------------------------
def build_render_setup():
    col = bpy.data.collections.new("RenderSetup")
    bpy.context.scene.collection.children.link(col)
    # neutral ground
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -FLOOR_T - 0.001))
    g = bpy.context.active_object
    g.name = "Ground"
    m = mat_plain("BackdropGrey", (0.42, 0.42, 0.42, 1.0), rough=1.0)
    g.data.materials.append(m)
    col.objects.link(g)
    bpy.context.scene.collection.objects.unlink(g)

    def area_light(name, loc, energy, size=6.0):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy = energy
        ld.shape = 'DISK'
        ld.size = size
        ob = bpy.data.objects.new(name, ld)
        ob.location = loc
        col.objects.link(ob)
        return ob

    def point_at(ob, target):
        ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

    key = area_light("KeyLight", (2.5, -3.5, 7.5), 700, 7.0)
    point_at(key, (0, 0, 2.0))
    fill = area_light("FillLight", (-5.0, 4.0, 4.5), 300, 6.0)
    point_at(fill, (0, 0, 2.2))
    up = area_light("DownLight", (0, 0, 6.4), 380, 5.0)   # light from above the vault rim
    point_at(up, (0, 0, 3.4))

    cams = {}
    def cam(name, loc, target, lens=42):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        ob = bpy.data.objects.new(name, cd)
        ob.location = loc
        point_at(ob, target)
        col.objects.link(ob)
        cams[name] = ob
        return ob

    # Visitor-height views of the single bay (front = looking along -Y)
    cam("CamFront", (0, 8.8, 1.7), (0, 0, 2.75), 38)
    cam("CamSide", (8.8, 0, 1.7), (0, 0, 2.75), 38)
    cam("Cam34", (6.4, 6.4, 1.15), (0, 0, 2.9), 40)
    # Tiled view echoing the 2025 photograph: low, down the hall
    cam("CamTiled", (-3.4, -3.0, 1.5), (4.5, 3.0, 3.35), 42)
    return cams

def tiled_copies(model_objs):
    """Duplicate the model objects on a 3 x 2 grid (shared mesh data) to
    prove the bay repeat. Returns the temp collection."""
    col = bpy.data.collections.new("Tiled")
    bpy.context.scene.collection.children.link(col)
    for gx in range(3):
        for gy in range(2):
            if gx == 0 and gy == 0:
                continue
            for ob in model_objs:
                n = ob.copy()
                n.location = Vector((gx * PITCH, gy * PITCH, 0)) + ob.location
                col.objects.link(n)
    return col

def tri_count(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    total = 0
    for ob in objs:
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        total += len(me.loop_triangles)
        ev.to_mesh_clear()
    return total

def render(cam_ob, path):
    sc = bpy.context.scene
    sc.camera = cam_ob
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)

def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.cycles.device = 'CPU'
    sc.render.resolution_x = 960
    sc.render.resolution_y = 720
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Filmic'
    sc.view_settings.look = 'Medium Contrast'
    sc.view_settings.exposure = 0.15
    world = bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.52, 0.52, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.55

    model_col, objs = build_model()
    cams = build_render_setup()

    out = os.path.join(HERE, SLUG + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=out)
    # GLB: Model collection only
    for ob in bpy.context.scene.objects:
        ob.select_set(False)
    for ob in objs:
        ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, SLUG + ".glb"),
                              use_selection=True, export_apply=True)
    for ob in bpy.context.scene.objects:
        ob.select_set(False)

    tris = tri_count(objs)
    dims = [ob.dimensions for ob in objs]
    print(f"TRIANGLES: {tris}")
    print(f"Objects: {len(objs)}")

    rd = os.path.join(HERE, "renders")
    os.makedirs(rd, exist_ok=True)
    render(cams["CamFront"], os.path.join(rd, "front.png"))
    render(cams["CamSide"], os.path.join(rd, "side.png"))
    render(cams["Cam34"], os.path.join(rd, "three-quarter.png"))

    # Tiled proof render, then remove the copies and re-save a clean blend
    tcol = tiled_copies(objs)
    render(cams["CamTiled"], os.path.join(rd, "tiled-three-quarter.png"))
    for ob in list(tcol.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.collections.remove(tcol)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("DONE")

if __name__ == "__main__":
    main()
