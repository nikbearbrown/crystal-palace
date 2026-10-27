# Build script — sy-post66-closure
# Post-1866 north-end closure dressing for the Crystal Palace film
# (SCENE-BUILD-PLAN Wave 4, item 16; scene CP048).
#
# Run:  blender -b --python build_sy_post66_closure.py
# Produces sy-post66-closure.blend, sy-post66-closure.glb and the
# four renders in renders/.  All dimensions are named constants,
# grouped by evidence status.  See NOTES.md for the full audit.
#
# Axes: X across the nave (bay direction), Y along the palace axis
# (+Y = north, toward the destroyed transept), Z up.  Origin at the
# base centre of the damaged bay, finished floor level z = 0.

import bpy, math, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------
# DOCUMENTED — the palace structural system (Downes 1852 plates via
# models/hyde-park-column-tier1/NOTES.md, controls D10/D11; the
# Sydenham palace reused the same 24 ft modular iron system)
BAY          = 7.3152   # 24 ft bay module / column centres
HALF_BAY     = BAY / 2
COL_OD       = 0.254    # column outer diameter, 10 in (bore 8 in)
COL_R        = COL_OD / 2
COLLAR_BASE_H = 0.152   # floor collar, 6 in
COLLAR_R     = 0.160
COLLAR_MID_R = 0.150    # intermediate collars (seen on Pl. VIII,
COLLAR_MID_H = 0.100    # positions proportional — inferred there)
COLLAR_Z     = (2.0, 4.0)
GIRDER_BOT   = 5.842    # floor to girder bottom, 19 ft 2 in
GIRDER_DEPTH = 0.914    # 3 ft 0 in
GIRDER_TOP   = GIRDER_BOT + GIRDER_DEPTH   # 22 ft 2 in = 6.756
FLANGE_W     = 0.300
FLANGE_T     = 0.050

# DOCUMENTED — palace floor (Paxton's printed figures, Official
# Catalogue 1851 pp.62-63, as modelled in hp-floor-boards)
BOARD_T      = 0.038    # board thickness 1 1/2 in (printed)
BOARD_W      = 0.229    # board width 9 in (inferred there)
BOARD_GAP    = 0.013    # open gap 1/2 in (printed)
JOIST_W      = 0.064    # fallen joist section 2 1/2 in (printed)
JOIST_D      = 0.178    # 7 in (printed)

# PLATE-READ — ILN 12 Jan 1867 ruins engraving: end-wall skeleton of
# light rails + diagonal flats in tiers, glazing gone; heat-drooped
# bars; fallen members.  Sections below are scaled reads, not
# dimensioned — see NOTES.md.
RAIL_H       = 0.140
RAIL_T       = 0.030
BRACE_W      = 0.110
BRACE_T      = 0.025
TIER_Z       = 2.921    # mid rail height (half the girder line)

# RECONSTRUCTION — closure screen (no image of the actual post-fire
# screen exists in the collection; evidence gate 6 stays open).
# Period-typical double-boarded timber partition, one bay wide,
# sized to the documented bay and girder line.
SCREEN_Y     = -3.400
SCREEN_H     = 6.600    # top of header, just under girder top
POST_S       = 0.150
SCR_BOARD_W  = 0.228
SCR_BOARD_T  = 0.025
SCR_GAP      = 0.006

# DRESSING — damage amounts (modest, per the engraving; guessed)
SAG          = 0.170    # girder mid-span heat sag
LEAN_TILTS   = (0.3, 1.1, 2.3)   # degrees, east column segments
LEAN_DIR     = Vector((0.41, 0.91, 0)).normalized()  # toward burn

# ------------------------------------------------------------------
def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in list(bpy.data.collections):
        if coll.name != 'Master Collection':
            bpy.data.collections.remove(coll)
    for m in list(bpy.data.meshes):  bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    for c in list(bpy.data.cameras): bpy.data.cameras.remove(c)
    for l in list(bpy.data.lights):  bpy.data.lights.remove(l)

def make_collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

# ---- materials ----------------------------------------------------
def principled(name, color, rough=0.9, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    return m

def char_material(name, c_dark, c_light):
    """Procedural char: noise-driven near-black variation.
    No photographic texture anywhere in this prop."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes['Principled BSDF']
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 9.0
    noise.inputs['Detail'].default_value = 4.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*c_dark, 1.0)
    ramp.color_ramp.elements[1].color = (*c_light, 1.0)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.96
    return m

MAT = {}
def build_materials():
    MAT['char_deep']  = char_material('CharDeep',  (0.004,0.003,0.003), (0.020,0.016,0.013))
    MAT['char_mid']   = char_material('CharMid',   (0.010,0.008,0.007), (0.035,0.027,0.020))
    MAT['scorch']     = char_material('Scorched',  (0.030,0.020,0.012), (0.075,0.052,0.032))
    MAT['iron_black'] = principled('IronBlackened', (0.030,0.028,0.026), 0.82, 0.55)
    MAT['board_a']    = principled('ScreenBoardA', (0.400,0.330,0.250), 0.92)
    MAT['board_b']    = principled('ScreenBoardB', (0.345,0.278,0.205), 0.92)
    MAT['board_c']    = principled('ScreenBoardC', (0.455,0.385,0.295), 0.92)
    MAT['board_new']  = principled('ScreenBoardNew', (0.520,0.420,0.290), 0.88)
    MAT['timber_frame'] = principled('ScreenFrame', (0.360,0.285,0.205), 0.90)
    MAT['timber_shore'] = principled('ShoreTimber', (0.520,0.400,0.265), 0.85)
    MAT['timber_dark']  = principled('ShoreSole',   (0.300,0.225,0.155), 0.90)

# ---- geometry helpers ----------------------------------------------
def _link(obj, coll):
    coll.objects.link(obj)
    return obj

def box(name, coll, size, loc, rot=(0.0,0.0,0.0), mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    o.rotation_euler = rot
    if mat: o.data.materials.append(mat)
    _link(o, coll)
    return o

def cyl(name, coll, r, h, loc, rot=(0.0,0.0,0.0), mat=None, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=loc)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = rot
    if mat: o.data.materials.append(mat)
    _link(o, coll)
    return o

def beam_between(name, coll, p1, p2, w, d, mat):
    """Box of section w x d whose local Z runs from p1 to p2."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    direction = p2 - p1
    length = direction.length
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=mid)
    o = bpy.context.object
    o.name = name
    o.dimensions = (w, d, length)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0,0,1)).rotation_difference(direction.normalized())
    if mat: o.data.materials.append(mat)
    _link(o, coll)
    return o

def tube(name, coll, points, r, mat):
    """Polyline tube through points (heat-drooped bars)."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = r
    cu.bevel_resolution = 2
    sp = cu.splines.new('POLY')
    sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points):
        p.co = (*co, 1.0)
    o = bpy.data.objects.new(name, cu)
    coll.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.object
    o.name = name
    if mat: o.data.materials.append(mat)
    return o

# ------------------------------------------------------------------
# DAMAGED BAY
# ------------------------------------------------------------------
def girder_top_z(x):
    return GIRDER_TOP - SAG * (1.0 - (x / HALF_BAY) ** 2)

def build_floor(coll):
    patch_w, patch_d, cy = 8.6, 4.6, 0.55
    pitch = BOARD_W + BOARD_GAP
    n = int(patch_w / pitch)
    x0 = -((n - 1) * pitch) / 2
    omit_north = {29, 30, 31, 32, 33, 34}   # burnt away, NE corner
    for i in range(n):
        x = x0 + i * pitch
        # south segment — scorched
        box(f'Bay_FloorS_{i:02d}', coll, (BOARD_W, 2.30, BOARD_T),
            (x, cy - 1.15, -BOARD_T/2), mat=MAT['scorch'])
        # north segment — deep char
        if i not in omit_north:
            box(f'Bay_FloorN_{i:02d}', coll, (BOARD_W, 2.30, BOARD_T),
                (x, cy + 1.15, -BOARD_T/2), mat=MAT['char_mid'])
    # one fallen board across the burnt corner
    box('Bay_FloorFallen', coll, (BOARD_W, 2.30, BOARD_T),
        (3.35, 2.05, 0.02), rot=(0.0, 0.0, math.radians(38)), mat=MAT['char_deep'])
    # fallen charred joist ends (printed palace joist section)
    joists = [((1.4, 1.9, 0.05), 0.5), ((-0.8, 2.2, 0.05), -0.9),
              ((2.6, 0.9, 0.05), 1.9), ((-2.2, 1.5, 0.05), 0.15)]
    for j, ((x, y, z), a) in enumerate(joists):
        box(f'Bay_Joist_{j}', coll, (1.35 + 0.3 * j, JOIST_W, JOIST_D),
            (x, y, z), rot=(0.0, 0.0, a), mat=MAT['char_deep'])

def build_column(coll, side):
    """side = -1 west (upright), +1 east (heat-leaning)."""
    x_base = side * HALF_BAY
    tag = 'West' if side < 0 else 'East'
    if side < 0:
        # upright, two-tone char split at the 2 m collar
        cyl(f'Bay_Col{tag}_ShaftLo', coll, COL_R, 2.0, (x_base, 0, 1.0), mat=MAT['char_deep'])
        cyl(f'Bay_Col{tag}_ShaftHi', coll, COL_R, GIRDER_BOT - 2.0,
            (x_base, 0, 2.0 + (GIRDER_BOT - 2.0) / 2), mat=MAT['iron_black'])
        cyl(f'Bay_Col{tag}_CollarBase', coll, COLLAR_R, COLLAR_BASE_H,
            (x_base, 0, COLLAR_BASE_H / 2), mat=MAT['char_deep'])
        for z in COLLAR_Z:
            cyl(f'Bay_Col{tag}_Collar_{int(z)}', coll, COLLAR_MID_R, COLLAR_MID_H,
                (x_base, 0, z), mat=MAT['iron_black'])
        cyl(f'Bay_Col{tag}_Capital', coll, 0.225, 0.08,
            (x_base, 0, GIRDER_BOT + 0.04), mat=MAT['iron_black'], verts=8)
        top = Vector((x_base, 0, GIRDER_BOT))
    else:
        # leaning: three segments, breaks hidden at the collars
        bounds = [0.0, COLLAR_Z[0], COLLAR_Z[1], GIRDER_BOT]
        pos = Vector((x_base, 0, 0.0))
        for k in range(3):
            z0, z1 = bounds[k], bounds[k + 1]
            L = z1 - z0
            tilt = math.radians(LEAN_TILTS[k])
            axis = Vector((LEAN_DIR.x * math.sin(tilt),
                           LEAN_DIR.y * math.sin(tilt),
                           math.cos(tilt)))
            centre = pos + axis * (L / 2)
            q = Vector((0, 0, 1)).rotation_difference(axis)
            o = cyl(f'Bay_Col{tag}_Seg{k}', coll, COL_R, L,
                    tuple(centre), mat=MAT['char_deep'] if k == 0 else MAT['iron_black'])
            o.rotation_mode = 'QUATERNION'
            o.rotation_quaternion = q
            top = pos + axis * L
            # collar at the segment base (not at z=0: base collar below)
            if k > 0:
                c = cyl(f'Bay_Col{tag}_Collar_{int(z0)}', coll, COLLAR_MID_R,
                        COLLAR_MID_H, tuple(pos + axis * (COLLAR_MID_H / 2)),
                        mat=MAT['iron_black'])
                c.rotation_mode = 'QUATERNION'
                c.rotation_quaternion = q
            pos = top
        cyl(f'Bay_Col{tag}_CollarBase', coll, COLLAR_R, COLLAR_BASE_H,
            (x_base, 0, COLLAR_BASE_H / 2), mat=MAT['char_deep'])
        cap = cyl(f'Bay_Col{tag}_Capital', coll, 0.225, 0.08,
                  tuple(pos + Vector((0, 0, 0.04))), mat=MAT['iron_black'], verts=8)
        top = pos
    # capital bolts (Plate VIII Fig. 13: four at the diagonals)
    for bx, by in ((0.13, 0.13), (0.13, -0.13), (-0.13, 0.13), (-0.13, -0.13)):
        cyl(f'Bay_Col{tag}_Bolt', coll, 0.016, 0.05,
            (top.x + bx, top.y + by, GIRDER_BOT + 0.105), mat=MAT['iron_black'], verts=8)
    return top

def build_girder(coll):
    segs = 5
    for i in range(segs):
        x0 = -HALF_BAY + i * BAY / segs
        x1 = -HALF_BAY + (i + 1) * BAY / segs
        xm = (x0 + x1) / 2
        zt0, zt1 = girder_top_z(x0), girder_top_z(x1)
        zc = (zt0 + zt1) / 2 - GIRDER_DEPTH / 2
        ang = math.atan2(-(zt1 - zt0), x1 - x0)
        L = (x1 - x0) / math.cos(ang)
        # web
        box(f'Bay_GirderWeb_{i}', coll, (L, 0.030, GIRDER_DEPTH - 2 * FLANGE_T),
            (xm, 0, zc), rot=(0.0, ang, 0.0), mat=MAT['iron_black'])
        # flanges
        for s, nm in ((1, 'Top'), (-1, 'Bot')):
            off = Vector((0, 0, s * (GIRDER_DEPTH / 2 - FLANGE_T / 2)))
            # rotate offset about Y by the segment slope
            ca, sa = math.cos(ang), math.sin(ang)
            ox = off.x * ca + off.z * sa
            oz = -off.x * sa + off.z * ca
            box(f'Bay_Girder{nm}_{i}', coll, (L, FLANGE_W, FLANGE_T),
                (xm + ox, 0, zc + oz), rot=(0.0, ang, 0.0), mat=MAT['iron_black'])

def build_end_frame(coll):
    """Skeletal end-wall framing in the bay plane (ILN plate read):
    light rails + diagonal flats in two tiers, glazing gone."""
    x_in = HALF_BAY - 0.14
    # mid rail
    box('Bay_FrameRail', coll, (2 * x_in, RAIL_T, RAIL_H), (0, 0, TIER_Z), mat=MAT['iron_black'])
    # X braces, two tiers; pair offset in Y so they cross cleanly
    tiers = [(0.30, TIER_Z - RAIL_H / 2), (TIER_Z + RAIL_H / 2, GIRDER_BOT - 0.05)]
    for t, (z0, z1) in enumerate(tiers):
        for s, yo in ((1, 0.022), (-1, -0.022)):
            p1 = Vector((-x_in * s, yo, z0))
            p2 = Vector((x_in * s, yo, z1))
            beam_between(f'Bay_FrameBrace_{t}_{s}', coll, p1, p2, BRACE_W, BRACE_T, MAT['iron_black'])
    # roof stubs from the column heads: straight length, then a
    # heat-kinked drooping length (plate-read; modest angles)
    for side in (-1, 1):
        xh = side * HALF_BAY
        zt = girder_top_z(xh)
        d1 = Vector((0, math.cos(math.radians(30)), math.sin(math.radians(30))))
        p0 = Vector((xh, 0, zt))
        p1 = p0 + d1 * 2.4
        beam_between(f'Bay_Rafter_{side}_a', coll, p0, p1, 0.140, 0.100, MAT['iron_black'])
        d2 = Vector((0, math.cos(math.radians(14)), math.sin(math.radians(14))))
        p2 = p1 + d2 * 1.0
        beam_between(f'Bay_Rafter_{side}_b', coll, p1, p2, 0.140, 0.100, MAT['char_mid'])
    # drooping centre tie stub
    p0 = Vector((0, 0, GIRDER_TOP - SAG - 0.05))
    p1 = p0 + Vector((0, 0.95, 0.10))
    p2 = p1 + Vector((0, 0.75, -0.28))
    beam_between('Bay_TieStub_a', coll, p0, p1, 0.120, 0.090, MAT['iron_black'])
    beam_between('Bay_TieStub_b', coll, p1, p2, 0.120, 0.090, MAT['char_mid'])
    # heat-drooped bars hanging in catenary-like curves (the
    # engraving's most distinctive damage read)
    tube('Bay_Droop_0', coll, [(-2.4, 0.06, GIRDER_TOP - 0.02), (-2.4, 0.85, 6.05),
                              (-2.4, 1.55, 4.85), (-2.4, 1.95, 3.55)], 0.016, MAT['char_deep'])
    tube('Bay_Droop_1', coll, [(1.2, 0.06, GIRDER_TOP - 0.02), (1.2, 0.80, 6.20),
                              (1.2, 1.45, 5.10), (1.2, 1.80, 3.90)], 0.016, MAT['char_deep'])
    # hanging sash bars, glazing stripped; one bent
    for x, L in ((-1.5, 1.1), (0.4, 0.7)):
        box(f'Bay_Sash_{x}', coll, (0.035, 0.020, L),
            (x, 0.10, GIRDER_TOP - SAG * (1 - (x / HALF_BAY) ** 2) - L / 2), mat=MAT['char_mid'])
    beam_between('Bay_SashBent_a', coll, (2.2, 0.10, GIRDER_TOP - 0.13),
                 (2.2, 0.10, GIRDER_TOP - 1.03), 0.035, 0.020, MAT['char_mid'])
    beam_between('Bay_SashBent_b', coll, (2.2, 0.10, GIRDER_TOP - 1.03),
                 (2.2, 0.42, GIRDER_TOP - 1.55), 0.035, 0.020, MAT['char_mid'])
    # fallen girder length on the floor (echoes the plate's fallen
    # diagonal member; an in-situ floor piece, not the 1936 prop)
    import mathutils
    yaw, roll = math.radians(-28), math.radians(5)
    rot = mathutils.Matrix.Rotation(yaw, 4, 'Z') @ mathutils.Matrix.Rotation(roll, 4, 'X')
    centre = Vector((2.3, 1.7, 0.16))
    for dz, nm, th in ((0.17, 'Top', FLANGE_T), (-0.17, 'Bot', FLANGE_T), (0.0, 'Web', 0.28)):
        size = (2.4, FLANGE_W, th) if nm != 'Web' else (2.4, 0.030, 0.28)
        loc = centre + (rot @ Vector((0, 0, dz)))
        o = box(f'Bay_Fallen{nm}', coll, size, tuple(loc), mat=MAT['char_deep'])
        o.rotation_mode = 'QUATERNION'
        o.rotation_quaternion = rot.to_quaternion()

# ------------------------------------------------------------------
# SHORING — standard period timber shoring practice (reconstruction;
# no shoring is visible in the surviving 1866-67 images consulted)
# ------------------------------------------------------------------
def build_shoring(coll):
    # two dead shores under the sagging girder
    for sx in (-1.8, 1.8):
        soffit = GIRDER_BOT - SAG * (1 - (sx / HALF_BAY) ** 2)
        box(f'Shore_DeadSole_{sx}', coll, (1.10, 0.42, 0.08), (sx, -0.30, 0.04), mat=MAT['timber_dark'])
        box(f'Shore_DeadPost_{sx}', coll, (0.22, 0.22, 5.47), (sx, -0.30, 0.08 + 5.47 / 2), mat=MAT['timber_shore'])
        box(f'Shore_DeadCap_{sx}', coll, (0.26, 0.66, 0.07), (sx, -0.30, 5.585), mat=MAT['timber_shore'])
        for s in (1, -1):  # wedge pair, opposed slopes
            box(f'Shore_DeadWedge_{sx}_{s}', coll, (0.30, 0.22, 0.055),
                (sx, -0.30, (5.62 + soffit) / 2), rot=(0.0, s * math.radians(7), 0.0), mat=MAT['timber_dark'])
    # X-brace between the dead shores, on their nave face,
    # lapped at the crossing like the screen braces
    for s, yo in ((1, -0.44), (-1, -0.474)):
        beam_between(f'Shore_DeadBrace_{s}', coll,
                     (-1.8 * s, yo, 0.55), (1.8 * s, yo, 5.15),
                     0.090, 0.030, MAT['timber_shore'])
    # waling across the end frame's burn face, at the raking-shore heads
    box('Shore_Waling', coll, (6.90, 0.14, 0.18), (0, 0.17, 5.30), mat=MAT['timber_shore'])
    # two raking shores from the burn side
    for sx in (-2.7, 2.7):
        box(f'Shore_RakeSole_{sx}', coll, (0.55, 1.15, 0.09), (sx, 3.32, 0.005), mat=MAT['timber_dark'])
        box(f'Shore_RakeCleat_{sx}', coll, (0.40, 0.14, 0.16), (sx, 3.80, 0.06), mat=MAT['timber_dark'])
        beam_between(f'Shore_Rake_{sx}', coll, (sx, 3.28, 0.10), (sx, 0.26, 5.24),
                     0.240, 0.200, MAT['timber_shore'])
    # one raking shore against the leaning east column
    box('Shore_RakeSole_E', coll, (1.15, 0.55, 0.09), (5.80, 0, 0.005), mat=MAT['timber_dark'])
    box('Shore_RakeCleat_E', coll, (0.14, 0.40, 0.16), (5.28, 0, 0.06), mat=MAT['timber_dark'])
    box('Shore_BearingBlock_E', coll, (0.20, 0.34, 0.60),
        (HALF_BAY + 0.20, 0, 4.25), mat=MAT['timber_shore'])
    beam_between('Shore_Rake_E', coll, (5.72, 0, 0.10), (HALF_BAY + 0.30, 0, 4.22),
                 0.240, 0.200, MAT['timber_shore'])

# ------------------------------------------------------------------
# CLOSURE SCREEN — period-typical double-boarded timber partition
# (RECONSTRUCTION: the actual post-fire screen is not pictured in
# any source in the collection; see NOTES.md)
# ------------------------------------------------------------------
def build_screen(coll):
    import random
    rng = random.Random(1867)
    y = SCREEN_Y
    box('Screen_Sole', coll, (7.465, 0.24, 0.10), (0, y, 0.012), mat=MAT['timber_dark'])
    for px in (-HALF_BAY, -1.2192, 1.2192, HALF_BAY):
        box(f'Screen_Post_{px}', coll, (POST_S, POST_S, SCREEN_H - 0.10),
            (px, y, 0.10 + (SCREEN_H - 0.10) / 2), mat=MAT['timber_frame'])
    # rails/header recessed 6 mm behind the post faces and cut
    # flush with the post outer faces: exactly coplanar post/rail
    # faces z-fought into black patches in the first build's front
    # render, and the full-length rails poked past the end posts
    for z0, z1, nm in ((0.10, 0.25, 'RailBot'), (3.275, 3.425, 'RailMid'), (6.42, 6.60, 'Header')):
        box(f'Screen_{nm}', coll, (7.465, POST_S, z1 - z0), (0, y + 0.006, (z0 + z1) / 2), mat=MAT['timber_frame'])
    pitch = SCR_BOARD_W + SCR_GAP
    n = 31
    x0 = -((n - 1) * pitch) / 2
    board_mats = [MAT['board_a'], MAT['board_b'], MAT['board_c']]
    for face, fy in (('Nave', y - 0.0875), ('Burn', y + 0.0875)):
        for i in range(n):
            x = x0 + i * pitch
            m = rng.choice(board_mats)
            proud = 0.0
            if face == 'Nave' and i == 24:   # one replaced board (dressing)
                m, proud = MAT['board_new'], -0.004
            box(f'Screen_Board{face}_{i:02d}', coll,
                (SCR_BOARD_W, SCR_BOARD_T, 6.32), (x, fy + proud, 0.10 + 3.16), mat=m)
    # Diagonal braces on the nave face.  Both sit at the same
    # offset; where they cross near the top, one brace is butted
    # (split with a short gap) rather than lapped — a first fix
    # that offset the second brace in Y buried it in the board
    # layer, and coincident side faces at a full crossing
    # z-fought black in the very first build.
    beam_between('Screen_Brace_1', coll,
                 (-3.45, y - 0.117, 0.35), (0.25, y - 0.117, 6.15),
                 0.140, 0.030, MAT['timber_frame'])
    _b0, _b1 = Vector((3.45, y - 0.117, 0.35)), Vector((-0.25, y - 0.117, 6.15))
    _dir = _b1 - _b0
    _len = _dir.length
    _dir.normalize()
    _cross = _b0 + _dir * (_len * 0.9324)   # the crossing point
    beam_between('Screen_Brace_2a', coll, _b0, _cross - _dir * 0.13,
                 0.140, 0.030, MAT['timber_frame'])
    beam_between('Screen_Brace_2b', coll, _cross + _dir * 0.13, _b1,
                 0.140, 0.030, MAT['timber_frame'])

# ------------------------------------------------------------------
# RENDER SETUP (not exported)
# ------------------------------------------------------------------
def build_render_setup(coll):
    m = principled('BackdropGrey', (0.46, 0.46, 0.46), 1.0)
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -BOARD_T))
    g = bpy.context.object
    g.name = 'Ground'
    g.data.materials.append(m)
    _link(g, coll)
    sun_data = bpy.data.lights.new('Sun', 'SUN')
    sun_data.energy = 3.2
    sun_data.angle = math.radians(8)
    sun = bpy.data.objects.new('Sun', sun_data)
    sun.rotation_euler = (math.radians(52), math.radians(-18), math.radians(-32))
    coll.objects.link(sun)
    area_data = bpy.data.lights.new('Fill', 'AREA')
    area_data.energy = 900
    area_data.shape = 'RECTANGLE'
    area_data.size = 9
    area_data.size_y = 6
    fill = bpy.data.objects.new('Fill', area_data)
    fill.location = (7.5, 6.5, 7.0)
    fill.rotation_mode = 'QUATERNION'
    fill.rotation_quaternion = Vector((7.5, 6.5, 7.0)).rotation_difference(Vector((0, 0, 0)))
    # point the area light back at the set centre
    fill.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(
        (Vector((0, 0, 2.6)) - Vector((7.5, 6.5, 7.0))).normalized())
    coll.objects.link(fill)

def add_camera(coll, name, loc, target, lens=42):
    # proper look-at with world +Z as up: rotation_difference()
    # alone leaves the roll arbitrary and rolled the side view 90
    # degrees in the first build (QC catch — see NOTES.md)
    import mathutils
    data = bpy.data.cameras.new(name)
    data.lens = lens
    cam = bpy.data.objects.new(name, data)
    cam.location = loc
    z_axis = (Vector(loc) - Vector(target)).normalized()
    x_axis = Vector((0, 0, 1)).cross(z_axis).normalized()
    y_axis = z_axis.cross(x_axis)
    mat = mathutils.Matrix.Identity(3)
    mat.col[0], mat.col[1], mat.col[2] = x_axis, y_axis, z_axis
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = mat.to_quaternion()
    coll.objects.link(cam)
    return cam

# ------------------------------------------------------------------
def main():
    clean_scene()
    build_materials()
    bay = make_collection('DamagedBay')
    shore = make_collection('Shoring')
    screen = make_collection('ClosureScreen')
    setup = make_collection('RenderSetup')

    build_floor(bay)
    build_column(bay, -1)
    build_column(bay, +1)
    build_girder(bay)
    build_end_frame(bay)
    build_shoring(shore)
    build_screen(screen)
    build_render_setup(setup)

    cams = {
        'front':        add_camera(setup, 'CamFront', (0, -14.5, 4.6), (0, -0.6, 3.1)),
        'side':         add_camera(setup, 'CamSide', (14.5, -0.4, 4.0), (0.4, -0.2, 2.9)),
        'three-quarter': add_camera(setup, 'CamTQ', (-10.5, -11.5, 7.6), (0, -0.2, 2.7)),
        'damaged-bay':  add_camera(setup, 'CamBay', (7.2, 6.8, 4.8), (0.4, 0.1, 3.4), lens=38),
    }

    # apply scale + rotation on all model objects (unit scale,
    # world-space geometry; locations kept)
    model_objs = [o for c in (bay, shore, screen) for o in c.objects]
    bpy.ops.object.select_all(action='DESELECT')
    for o in model_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = model_objs[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')

    # save, export, render
    blend_path = os.path.join(OUT, 'sy-post66-closure.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    for o in model_objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, 'sy-post66-closure.glb'),
                              export_format='GLB', use_selection=True,
                              export_apply=True)
    bpy.ops.object.select_all(action='DESELECT')

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = int(os.environ.get('CP_SAMPLES', '128'))
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    world = bpy.data.worlds.new('W')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs[0].default_value = (0.36, 0.36, 0.36, 1)
    world.node_tree.nodes['Background'].inputs[1].default_value = 0.55
    scene.world = world
    for name, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT, 'renders', name + '.png')
        bpy.ops.render.render(write_still=True)

    # counts from evaluated meshes
    dg = bpy.context.evaluated_depsgraph_get()
    total_tris, total_objs = 0, 0
    for o in model_objs:
        ev = o.evaluated_get(dg)
        if ev.type == 'MESH':
            me = ev.data
            me.calc_loop_triangles()
            total_tris += len(me.loop_triangles)
            total_objs += 1
    print(f'SY-POST66-CLOSURE: {total_objs} objects, {total_tris} triangles')

main()
