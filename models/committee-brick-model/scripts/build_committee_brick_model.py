#!/usr/bin/env python3
"""Build committee-brick-model -- the 1850 Building Committee's official
brick design for the Great Exhibition building, presented as a period
architect's tabletop model on a base board (film scene CP007).

The scheme (never built; displaced by Paxton's glass design) is taken
from the engravings published in 1850-51:
  * ILN, 22 June 1850, p.445 -- perspective + ground plan with a printed
    scale bar (the controlling dimension source).
  * Berlyn & Fowler, "The Crystal Palace" (1851), p.22 -- ground plan
    ("Ground Plan of the Building Committee's Design"), p.24 -- exterior
    perspective.
Published size adopted (see NOTES.md): 2,000 ft long overall (measured
off the ILN plan against its own scale bar), ~470 ft deep, central
sheet-iron dome 200 ft in diameter (published figure), ~175 ft high.

Presentation scale: 1:500.  The model building is 1.2192 m long on a
1.38 x 0.42 m board.  Origin at the base centre of the BOARD.
Units are metres throughout; object scale is applied before export.

Run (after scripts/make_textures.py):
    blender -b --python scripts/build_committee_brick_model.py
Set CBM_NORENDER=1 to skip rendering.
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector

# ------------------------------------------------------------------ paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "textures")
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(RENDERS, exist_ok=True)

# ------------------------------------------------------------------ scale
FT = 0.3048 / 500.0            # one real foot at 1:500, in metres
L = 2000.0 * FT                # 1.2192 m -- building length
DEPTH = 470.0 * FT             # 0.2865 m
BOARD_Z = 0.018                # board thickness
PLINTH = 0.005                 # site plinth on the board
Z0 = BOARD_Z + PLINTH          # building base height (top of plinth)

EAVE = 48.0 * FT               # main range eaves
RIDGE = 82.0 * FT              # main range ridge
PAV_EAVE = 40.0 * FT           # end pavilion eaves
PAV_RIDGE = 55.0 * FT          # end pavilion ridge
CORR_TOP = 28.0 * FT           # pent-roof corridor: wall junction
CORR_EAVE = 20.0 * FT          # pent-roof corridor: outer eave
CORR_D = 26.0 * FT             # corridor depth out from the wall
ARCADE_H = 18.0 * FT           # ground-floor arcade register
X_ROT = -L / 2 + 0.465 * L     # rotunda axis (46.5% from the west end)

# ------------------------------------------------------------------ clean
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model_coll = bpy.data.collections.new("Model")
scene.collection.children.link(model_coll)
render_coll = bpy.data.collections.new("Render")
scene.collection.children.link(render_coll)


def link(obj, coll=model_coll):
    coll.objects.link(obj)
    return obj


# ------------------------------------------------------------------ materials
def _lin(c):
    """sRGB channel -> linear (Blender node defaults are linear)."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def principled(name, color=None, tex=None, rough=0.9, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if color:
        bsdf.inputs["Base Color"].default_value = \
            (_lin(color[0]), _lin(color[1]), _lin(color[2]), 1.0)
    if tex:
        node = m.node_tree.nodes.new("ShaderNodeTexImage")
        img = bpy.data.images.load(os.path.join(TEX, tex))
        img.colorspace_settings.name = 'sRGB'
        node.image = img
        node.extension = 'REPEAT'
        m.node_tree.links.new(node.outputs["Color"], bsdf.inputs["Base Color"])
    return m


MAT_BRICK = principled("Brick", tex="brick.png", rough=0.95)
MAT_ARCADE = principled("StoneArcade", tex="arcade.png", rough=0.9)
MAT_STONE = principled("StoneTrim", color=(0.70, 0.64, 0.52), rough=0.9)
MAT_SLATE = principled("RoofSlate", color=(0.15, 0.17, 0.21), rough=0.85)
MAT_DOME = principled("SheetIronDome", tex="dome.png", rough=0.5, metallic=0.25)
MAT_CLERE = principled("DrumClerestory", tex="clerestory.png", rough=0.85)
MAT_GLASS = principled("ArchGlazing", tex="archwindow.png", rough=0.32,
                       metallic=0.05)
MAT_WOOD = principled("BoardWood", tex="wood.png", rough=0.7)
MAT_WOODTRIM = principled("BoardTrim", color=(0.09, 0.06, 0.032), rough=0.6)
MAT_PLINTH = principled("SitePlinth", color=(0.48, 0.50, 0.44), rough=1.0)
MAT_POST = principled("PaintedIron", color=(0.14, 0.13, 0.115), rough=0.8)
MAT_BRASS = principled("Brass", color=(0.50, 0.36, 0.13), rough=0.35,
                       metallic=0.9)
MAT_DARK = principled("DarkOpening", color=(0.045, 0.045, 0.05), rough=0.95)

BRICK_CUBES = []   # cubes that need world-scale cube-projected brick UVs


# ------------------------------------------------------------------ helpers
def cube(name, size, loc, mat, brick=False):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        o.data.materials.append(mat)
    link(o)
    if brick:
        BRICK_CUBES.append(o)
    return o


def cylinder(name, radius, depth, loc, mat, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
                                        location=loc, vertices=vertices)
    o = bpy.context.active_object
    o.name = name
    if mat:
        o.data.materials.append(mat)
    link(o)
    return o


def scale_uv(obj, su, sv):
    uv = obj.data.uv_layers.active.data
    for loop in uv:
        loop.uv.x *= su
        loop.uv.y *= sv


def signed_volume(verts, faces):
    vol = 0.0
    for f in faces:
        v0 = Vector(verts[f[0]])
        for i in range(1, len(f) - 1):
            vol += v0.dot(Vector(verts[f[i]]).cross(
                Vector(verts[f[i + 1]]))) / 6.0
    return vol


def orient_faces(verts, faces):
    """Flip face winding if the closed solid's signed volume is negative,
    so normals end up outward deterministically."""
    if signed_volume(verts, faces) < 0:
        return [tuple(reversed(f)) for f in faces]
    return faces


def prism(name, axis, start, end, half_w, z_eave, z_ridge, mat, c=0.0):
    """Triangular-section roof prism. axis 'X': ridge runs along X,
    cross-section in YZ. axis 'Y': ridge along Y, cross-section in XZ.
    c = centre offset of the cross-section (along Y for 'X', X for 'Y')."""
    if axis == 'X':
        prof = [(c - half_w, z_eave), (c + half_w, z_eave), (c, z_ridge)]
        a = [(start, y, z) for (y, z) in prof]
        b = [(end, y, z) for (y, z) in prof]
    else:
        prof = [(c - half_w, z_eave), (c + half_w, z_eave), (c, z_ridge)]
        a = [(x, start, z) for (x, z) in prof]
        b = [(x, end, z) for (x, z) in prof]
    verts = a + b
    # closed solid: two slope quads, bottom quad, two end triangles
    faces = [(0, 2, 5, 3), (1, 4, 5, 2), (0, 1, 4, 3),
             (0, 2, 1), (3, 4, 5)]
    faces = orient_faces(verts, faces)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    link(obj)
    if mat:
        mesh.materials.append(mat)
    # fix normals outward
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def arch_panel(name, cy, w, spring_h, base_z, mat, thick=0.0012):
    """Round-arch panel in the XZ plane at depth cy (faces +/-Y).
    Outline: rectangle up to spring_h, semicircle of radius w/2 on top.
    UVs are planar 0..1 over the bounding box (glazing texture)."""
    r = w / 2.0
    pts = [(-r, 0.0), (r, 0.0), (r, spring_h)]
    steps = 14
    for i in range(1, steps):
        a = i * math.pi / steps          # 0 -> pi: over the crown, R to L
        pts.append((r * math.cos(a), spring_h + r * math.sin(a)))
    pts.append((-r, spring_h))
    h_tot = spring_h + r
    y0, y1 = cy - thick / 2, cy + thick / 2
    verts = [(x, y0, base_z + z) for (x, z) in pts] + \
            [(x, y1, base_z + z) for (x, z) in pts]
    n = len(pts)
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces = orient_faces(verts, faces)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    link(obj)
    if mat:
        mesh.materials.append(mat)
    uv = mesh.uv_layers.new(name="UVMap")
    for loop in mesh.loops:
        v = mesh.vertices[loop.vertex_index]
        uv.data[loop.index].uv = ((v.co.x + r) / w, (v.co.z - base_z) / h_tot)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def band_plane(name, cx, cy, length, height, z_base, bay, mat, flip=False):
    """Vertical arcade-texture plane; u tiles every `bay` metres."""
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = (length, height, 0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.rotation_euler = (math.radians(90 if not flip else -90), 0, 0)
    o.location = (cx, cy, z_base + height / 2)
    if mat:
        o.data.materials.append(mat)
    link(o)
    uv = o.data.uv_layers.active.data
    for loop in uv:
        loop.uv.x *= length / bay
    return o


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


# ================================================================== BOARD
cube("BaseBoard", (1.38, 0.42, BOARD_Z), (0, 0, BOARD_Z / 2), MAT_WOOD)
# edge trim: four raised strips around the board's top edge
cube("TrimS", (1.38, 0.012, 0.007), (0, -0.204, BOARD_Z - 0.0035), MAT_WOODTRIM)
cube("TrimN", (1.38, 0.012, 0.007), (0, 0.204, BOARD_Z - 0.0035), MAT_WOODTRIM)
cube("TrimW", (0.012, 0.396, 0.007), (-0.684, 0, BOARD_Z - 0.0035), MAT_WOODTRIM)
cube("TrimE", (0.012, 0.396, 0.007), (0.684, 0, BOARD_Z - 0.0035), MAT_WOODTRIM)
# site plinth the building sits on
cube("SitePlinth", (1.30, 0.355, PLINTH), (0, 0, BOARD_Z + PLINTH / 2),
     MAT_PLINTH)
# blank brass title plaque on the front edge (presentational device)
cube("Plaque", (0.08, 0.0015, 0.013), (0, -0.2105, 0.009), MAT_BRASS)

XW, XE = -L / 2, L / 2            # building west/east faces
PAV = 140.0 * FT                  # end pavilion length
RX0, RX1 = XW + PAV, XE - PAV     # main range span

# ================================================================== MAIN RANGE
cube("MainWalls", (RX1 - RX0, DEPTH, EAVE), ((RX0 + RX1) / 2, 0, Z0 + EAVE / 2),
     MAT_BRICK, brick=True)
prism("MainRoof", 'X', RX0 - 0.004, RX1 + 0.004, DEPTH / 2 + 0.004,
      Z0 + EAVE, Z0 + RIDGE, MAT_SLATE)
# eaves cornice strips
for s in (-1, 1):
    cube("EavesCornice", (RX1 - RX0, 0.0016, 0.0018),
         ((RX0 + RX1) / 2, s * (DEPTH / 2 + 0.0006), Z0 + EAVE - 0.0012),
         MAT_STONE)
# arcade register on both faces
for s in (-1, 1):
    band_plane("ArcadeBand", (RX0 + RX1) / 2, s * (DEPTH / 2 + 0.0006),
               RX1 - RX0, ARCADE_H, Z0, 12.0 * FT, MAT_ARCADE, flip=(s > 0))

# ================================================================== END PAVILIONS
for sgn, (px0, px1) in ((-1, (XW, XW + PAV)), (1, (XE - PAV, XE))):
    pcx = (px0 + px1) / 2
    pd = DEPTH + 0.008
    cube("PavilionWalls", (PAV, pd, PAV_EAVE), (pcx, 0, Z0 + PAV_EAVE / 2),
         MAT_BRICK, brick=True)
    prism("PavilionRoof", 'X', px0 - 0.003, px1 + 0.003, pd / 2 + 0.003,
          Z0 + PAV_EAVE, Z0 + PAV_RIDGE, MAT_SLATE)
    # wide arch panel on the end face
    p = arch_panel("PavilionArch", 0, 40.0 * FT, 24.0 * FT, Z0 + 0.0008,
                   MAT_GLASS)
    p.rotation_euler = (0, 0, math.radians(90))
    p.location = (sgn * (L / 2 + 0.0008), 0, 0)
    for s in (-1, 1):
        band_plane("PavilionArcade", pcx, s * (pd / 2 + 0.0006), PAV,
                   ARCADE_H, Z0, 12.0 * FT, MAT_ARCADE, flip=(s > 0))

# ================================================================== CROSS GABLES
GABLES = [(-L / 2 + 0.290 * L, "A"), (-L / 2 + 0.730 * L, "B")]
for gx, tag in GABLES:
    gd = DEPTH + 0.012
    cube(f"Gable{tag}Block", (0.055, gd, 62.0 * FT),
         (gx, 0, Z0 + 62.0 * FT / 2), MAT_BRICK, brick=True)
    prism(f"Gable{tag}Roof", 'Y', -(gd / 2 + 0.002), gd / 2 + 0.002,
          0.055 / 2 + 0.002, Z0 + 62.0 * FT, Z0 + 88.0 * FT, MAT_SLATE, c=gx)
    for s in (-1, 1):
        fy = s * (gd / 2 + 0.0007)
        gp = arch_panel(f"Gable{tag}Arch", fy, 52.0 * FT, 40.0 * FT,
                        Z0 + 0.0008, MAT_GLASS)
        gp.location.x = gx
        # flanking oculi in the gable wall, beside the arch and below
        # the roof springing (kept inside the roof prism's end plane)
        oy = s * (gd / 2 + 0.0004)
        for dx in (-0.020, 0.020):
            ring = cylinder(f"Gable{tag}OculusRing", 0.0036, 0.0008,
                            (gx + dx, oy, Z0 + 52.0 * FT), MAT_STONE,
                            vertices=20)
            ring.rotation_euler = (math.radians(90), 0, 0)
            disc = cylinder(f"Gable{tag}Oculus", 0.0028, 0.0012,
                            (gx + dx, oy, Z0 + 52.0 * FT), MAT_DARK,
                            vertices=20)
            disc.rotation_euler = (math.radians(90), 0, 0)
        band_plane(f"Gable{tag}Arcade", gx, fy, 0.055, ARCADE_H, Z0,
                   12.0 * FT, MAT_ARCADE, flip=(s > 0))

# ================================================================== PORCHES
def porch(cx, width_ft, proj, apex_ft, panel_w_ft, panel_spring_ft, tag):
    for s in (-1, 1):
        cy = s * (DEPTH / 2 + proj / 2)
        cube(f"Porch{tag}", (width_ft * FT, proj, 40.0 * FT),
             (cx, cy, Z0 + 40.0 * FT / 2), MAT_BRICK, brick=True)
        prism(f"Porch{tag}Roof", 'Y', cy - s * (proj / 2 + 0.002),
              cy + s * (proj / 2 + 0.002), width_ft * FT / 2 + 0.0015,
              Z0 + 40.0 * FT, Z0 + apex_ft * FT, MAT_SLATE, c=cx)
        fy = s * (DEPTH / 2 + proj + 0.0007)
        p = arch_panel(f"Porch{tag}Arch", fy, panel_w_ft * FT,
                       panel_spring_ft * FT, Z0 + 0.0008, MAT_GLASS)
        p.location.x = cx


porch(-L / 2 + 0.420 * L, 33, 0.010, 52, 16, 24, "S1")
porch(-L / 2 + 0.550 * L, 33, 0.010, 52, 16, 24, "S2")
porch(X_ROT, 46, 0.012, 60, 24, 28, "Centre")

# ================================================================== PENT-ROOF CORRIDORS
features = []
for gx, _ in GABLES:
    features.append((gx - 0.0275, gx + 0.0275))
for fx, fw in ((-L / 2 + 0.420 * L, 33 * FT), (-L / 2 + 0.550 * L, 33 * FT),
               (X_ROT, 46 * FT)):
    features.append((fx - fw / 2, fx + fw / 2))
features.sort()


def segments(x0, x1):
    segs, cur = [], x0
    for a, b in features:
        if a > cur:
            segs.append((cur, min(a, x1)))
        cur = max(cur, b)
    if cur < x1:
        segs.append((cur, x1))
    return [(a, b) for a, b in segs if b - a > 0.004]


slope_len = math.hypot(CORR_D, CORR_TOP - CORR_EAVE)
slope_ang = math.atan2(CORR_TOP - CORR_EAVE, CORR_D)
post_verts = []
bm = bmesh.new()
for s in (-1, 1):
    yw = s * DEPTH / 2
    yo = s * (DEPTH / 2 + CORR_D)
    zmid = Z0 + (CORR_TOP + CORR_EAVE) / 2
    for a, b in segments(XW + 0.002, XE - 0.002):
        seg_len = b - a
        roof = cube("CorridorRoof", (seg_len, slope_len, 0.0011),
                    ((a + b) / 2, (yw + yo) / 2, zmid), MAT_SLATE)
        roof.rotation_euler = (-s * slope_ang, 0, 0)
        beam = cube("CorridorBeam", (seg_len, 0.0016, 0.0022),
                    ((a + b) / 2, yo - s * 0.0008, Z0 + CORR_EAVE - 0.0013),
                    MAT_STONE)
        # colonnade posts along this segment
        x = a + 0.004
        while x < b - 0.002:
            vs = bmesh.ops.create_cube(bm, size=1.0)["verts"]
            bmesh.ops.scale(bm, verts=vs, vec=(0.0011, 0.0011, CORR_EAVE - 0.0024))
            bmesh.ops.translate(bm, verts=vs,
                                vec=(x, yo - s * 0.0016,
                                     Z0 + (CORR_EAVE - 0.0024) / 2))
            x += 20.0 * FT
mesh = bpy.data.meshes.new("ColonnadePosts")
bm.to_mesh(mesh)
bm.free()
posts = bpy.data.objects.new("ColonnadePosts", mesh)
link(posts)
posts.data.materials.append(MAT_POST)

# ================================================================== ROTUNDA + DOME
drum_r = 100.0 * FT
drum = cylinder("Drum", drum_r, 78.0 * FT - 10.0 * FT,
                (X_ROT, 0, Z0 + (78.0 * FT + 10.0 * FT) / 2), MAT_BRICK,
                vertices=64)
scale_uv(drum, 16.0, (78.0 * FT - 10.0 * FT) / 0.024)
band = cylinder("DrumBand", drum_r + 0.0006, 95.0 * FT - 78.0 * FT,
                (X_ROT, 0, Z0 + (95.0 * FT + 78.0 * FT) / 2), MAT_CLERE,
                vertices=64)
cylinder("DrumCorniceLow", drum_r + 0.0018, 0.0018,
         (X_ROT, 0, Z0 + 77.0 * FT), MAT_STONE, vertices=64)
cylinder("DrumCornice", drum_r + 0.0025, 0.0022,
         (X_ROT, 0, Z0 + 95.0 * FT + 0.001), MAT_STONE, vertices=64)

# dome: surface of revolution, elliptical-leaning profile (published
# views show a broad, slightly pointed "squat" dome), texture-ribbed
spring_z = Z0 + 95.0 * FT
rise = 80.0 * FT
SEG, RINGS = 72, 14
prof = []
for j in range(RINGS + 1):
    t = j / RINGS
    r = drum_r * (math.cos(t * math.pi / 2) ** 0.80)
    z = spring_z + rise * (math.sin(t * math.pi / 2) ** 1.25)
    if r < 0.0115:
        r = 0.0115
    prof.append((r, z))
verts, faces, uvs = [], [], []
for j, (r, z) in enumerate(prof):
    for i in range(SEG):
        a = 2 * math.pi * i / SEG
        verts.append((X_ROT + r * math.cos(a), r * math.sin(a), z))
        uvs.append((i / SEG, j / RINGS))
for j in range(RINGS):
    for i in range(SEG):
        i2 = (i + 1) % SEG
        a0 = j * SEG + i
        b0 = j * SEG + i2
        c0 = (j + 1) * SEG + i2
        d0 = (j + 1) * SEG + i
        faces.append((a0, b0, c0, d0))
top_c = len(verts)
verts.append((X_ROT, 0, prof[-1][1]))
uvs.append((0.5, 1.0))
for i in range(SEG):
    i2 = (i + 1) % SEG
    faces.append((RINGS * SEG + i, RINGS * SEG + i2, top_c))
dome_mesh = bpy.data.meshes.new("Dome")
dome_mesh.from_pydata(verts, [], faces)
dome_mesh.update()
dome = bpy.data.objects.new("Dome", dome_mesh)
link(dome)
dome_mesh.materials.append(MAT_DOME)
uvl = dome_mesh.uv_layers.new(name="UVMap")
for loop in dome_mesh.loops:
    uvl.data[loop.index].uv = uvs[loop.vertex_index]
for p in dome_mesh.polygons:
    p.use_smooth = True
cylinder("DomeCap", 0.0135, 0.003, (X_ROT, 0, prof[-1][1] + 0.0015),
         MAT_STONE, vertices=32)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0028, location=(
    X_ROT, 0, prof[-1][1] + 0.0058), segments=12, ring_count=8)
fin = bpy.context.active_object
fin.name = "DomeFinial"
fin.data.materials.append(MAT_BRASS)
link(fin)

# ================================================================== brick UV pass
for o in BRICK_CUBES:
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.024, correct_aspect=False)
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

# ================================================================== counts
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in model_coll.objects:
    if o.type == 'MESH':
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        ev.to_mesh_clear()
print(f"TRIANGLES: {tris}")
print(f"OBJECTS: {len(model_coll.objects)}")

# ================================================================== save + glb
for img in bpy.data.images:
    if img.type == 'IMAGE':
        try:
            img.pack()
        except Exception:
            pass
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,
                                                  "committee-brick-model.blend"))
bpy.ops.object.select_all(action='DESELECT')
for o in model_coll.objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,
                                                "committee-brick-model.glb"),
                          export_format='GLB', use_selection=True,
                          export_apply=True, export_yup=True)
print("EXPORTED GLB")

# ================================================================== renders
if os.environ.get("CBM_NORENDER") != "1":
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = int(os.environ.get("CBM_SAMPLES", "64"))
    scene.cycles.use_denoising = True
    scene.cycles.device = 'CPU'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    world = bpy.data.worlds.new("W")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = \
        (0.62, 0.62, 0.62, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    scene.world = world
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'

    bpy.ops.mesh.primitive_plane_add(size=9, location=(0, 0, -0.002))
    gnd = bpy.context.active_object
    gnd.name = "Ground"
    gm = principled("GroundGrey", color=(0.55, 0.55, 0.55), rough=1.0)
    gnd.data.materials.append(gm)
    link(gnd, render_coll)

    sun_data = bpy.data.lights.new("Sun", 'SUN')
    sun_data.energy = 3.2
    sun_data.angle = 0.12
    sun = bpy.data.objects.new("Sun", sun_data)
    sun.rotation_euler = (math.radians(52), math.radians(10),
                          math.radians(-38))
    sun.location = (-1.5, -2.0, 2.5)
    link(sun, render_coll)

    fill_data = bpy.data.lights.new("Fill", 'AREA')
    fill_data.energy = 350
    fill_data.shape = 'DISK'
    fill_data.size = 3.0
    fill = bpy.data.objects.new("Fill", fill_data)
    fill.location = (1.6, 1.4, 1.3)
    link(fill, render_coll)
    look_at(fill, (0, 0, 0.02))

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 40
    cam = bpy.data.objects.new("Cam", cam_data)
    link(cam, render_coll)
    scene.camera = cam

    VIEWS = {
        "front": ((0, -1.22, 0.13), (0, 0, 0.05)),
        "side": ((-1.02, -0.05, 0.12), (0, 0, 0.05)),
        "three-quarter": ((-0.95, -0.78, 0.48), (0, 0, 0.03)),
    }
    only = os.environ.get("CBM_VIEWS", "").split(",")
    for name, (pos, tgt) in VIEWS.items():
        if only != [""] and name not in only:
            continue
        cam.location = pos
        look_at(cam, tgt)
        scene.render.filepath = os.path.join(RENDERS, name + ".png")
        bpy.ops.render.render(write_still=True)
        print("RENDERED", name)
    # re-save so the .blend also carries the render setup
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(
        ROOT, "committee-brick-model.blend"))
print("BUILD DONE")
