#!/usr/bin/env python3
"""
scan-fig31-goods-for-the-home
Colour exhibition view (fig.31, "Goods for the home") of a decorative-
furnishings stand at the Great Exhibition, 1851: ornate upright piano
(centre), hooded porter's chair (right), display boards of door furniture
(left/back), trays, pedestal urn and two stylised visitors, on a low
red-carpeted platform against a brown display wall.

Scale ESTIMATED: anchored on an upright piano ~1.30 m high and adult
figures ~1.62-1.75 m. See NOTES.md. Units: metres. Origin at base
centre of the platform, at floor level. Blender 4.5.3, re-runnable.
No readable text anywhere: signs and sheet music are blank.
"""
import bpy, math, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig31-goods-for-the-home"

# ---------------------------------------------------------------- scene reset
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass  # orphan purge below handles leftovers
bpy.ops.outliner.orphans_purge(do_recursive=True)

# ---------------------------------------------------------------- materials
def mat(name, rgb, metallic=0.0, rough=0.65):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return m

BLACK_LACQ = mat("black_lacquer", (0.015, 0.012, 0.012), 0.15, 0.28)
DARK_WOOD  = mat("dark_carved_wood", (0.11, 0.05, 0.025), 0.0, 0.5)
MID_WOOD   = mat("mid_wood", (0.28, 0.15, 0.07), 0.0, 0.6)
GILT       = mat("gilt", (0.83, 0.58, 0.16), 0.85, 0.32)
BRASS      = mat("brass", (0.62, 0.44, 0.14), 0.9, 0.35)
SILVER     = mat("silvered_tray", (0.62, 0.62, 0.60), 0.9, 0.3)
IRON_DARK  = mat("dark_iron_bronze", (0.10, 0.09, 0.08), 0.6, 0.5)
RED_CARPET = mat("red_carpet", (0.42, 0.04, 0.05), 0.0, 0.95)
RED_CURT   = mat("deep_red_curtain", (0.36, 0.03, 0.05), 0.0, 0.9)
WALL_BROWN = mat("brown_display_wall", (0.30, 0.19, 0.11), 0.0, 0.85)
FLOOR_PALE = mat("pale_boards", (0.62, 0.52, 0.38), 0.0, 0.8)
FLOOR_LINE = mat("board_groove", (0.38, 0.30, 0.20), 0.0, 0.9)
UPHOL_RED  = mat("orange_red_upholstery", (0.46, 0.085, 0.018), 0.0, 0.82)  # FIX R2: deeper orange-red
UPHOL_DARK = mat("dark_green_upholstery", (0.07, 0.14, 0.08), 0.0, 0.8)
IVORY      = mat("ivory_keys", (0.92, 0.90, 0.82), 0.0, 0.35)
EBONY_KEY  = mat("ebony_keys", (0.02, 0.02, 0.02), 0.0, 0.4)
PAPER      = mat("blank_paper", (0.95, 0.94, 0.90), 0.0, 0.9)
INLAY_TEAL = mat("inlay_teal", (0.015, 0.045, 0.035), 0.1, 0.42)   # FIX R1: deep green-black, was bright teal
INLAY_RED  = mat("inlay_floral_red", (0.20, 0.035, 0.04), 0.1, 0.45)  # FIX R1: deep burgundy, was bright pink-red
INLAY_CREAM= mat("inlay_cream", (0.85, 0.75, 0.50), 0.1, 0.45)
# FIX R1/R2: muted inlay dots + deeper hood gilt / upholstery tones
DOT_ROSE   = mat("muted_floral_rose", (0.38, 0.20, 0.16), 0.05, 0.55)
DOT_CREAM  = mat("muted_floral_cream", (0.58, 0.50, 0.36), 0.05, 0.55)
DOT_SAGE   = mat("muted_floral_sage", (0.25, 0.32, 0.20), 0.05, 0.55)
HOOD_GILT  = mat("hood_gilt_deep", (0.62, 0.38, 0.09), 0.72, 0.42)
CAB_DOOR   = mat("cabinet_door_dark", (0.06, 0.028, 0.026), 0.12, 0.42)
SKIN       = mat("skin", (0.82, 0.60, 0.44), 0.0, 0.65)
BLUE_BOD   = mat("blue_bodice", (0.10, 0.20, 0.48), 0.0, 0.8)
WHITE_SKIRT= mat("white_skirt", (0.90, 0.88, 0.84), 0.0, 0.9)
YELLOW_BON = mat("yellow_bonnet", (0.85, 0.62, 0.15), 0.0, 0.8)
BLACK_COAT = mat("black_coat", (0.02, 0.02, 0.025), 0.0, 0.7)
GREY_TROU  = mat("grey_trousers", (0.22, 0.22, 0.24), 0.0, 0.85)
WHITE_SHIRT= mat("white_shirt", (0.93, 0.93, 0.92), 0.0, 0.85)

# ---------------------------------------------------------------- helpers
def _finish(obj, material, bevel=0.0):
    if material:
        obj.data.materials.append(material)
    if bevel > 0:
        mod = obj.modifiers.new("soft", 'BEVEL')
        mod.width = bevel; mod.segments = 2
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if obj.type == 'MESH':
        bpy.ops.object.shade_smooth() if bevel else None
    obj.select_set(False)
    return obj

def box(name, loc, size, material, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, material, bevel)

def cyl(name, loc, radius, depth, material, rot=(0, 0, 0), verts=16, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    return _finish(o, material, bevel)

def sphere(name, loc, scale, material, seg=14, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

def cone(name, loc, r1, r2, depth, material, verts=18):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    if material: o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

def torus(name, loc, major, minor, material, rot=(0, 0, 0), maj_seg=20, min_seg=8):
    bpy.ops.mesh.primitive_torus_add(major_segments=maj_seg, minor_segments=min_seg,
                                     major_radius=major, minor_radius=minor,
                                     location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name
    if material: o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

def lathe(name, profile, material, seg=20, loc=(0, 0, 0)):
    """profile: list of (radius, z) bottom->top. Closed-ish solid of revolution."""
    verts, faces = [], []
    n = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(seg):
            a = 2 * math.pi * j / seg
            verts.append((loc[0] + r * math.cos(a), loc[1] + r * math.sin(a), loc[2] + z))
    for i in range(n - 1):
        for j in range(seg):
            a = i * seg + j; b = i * seg + (j + 1) % seg
            c = b + seg; d = a + seg
            faces.append((a, b, c, d))
    # caps
    bc = len(verts); verts.append((loc[0], loc[1], loc[2] + profile[0][1]))
    tc = len(verts); verts.append((loc[0], loc[1], loc[2] + profile[-1][1]))
    for j in range(seg):
        faces.append((bc, (j + 1) % seg, j))
        top0 = (n - 1) * seg
        faces.append((tc, top0 + j, top0 + (j + 1) % seg))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    if material: me.materials.append(material)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.shade_smooth(); o.select_set(False)
    return o

def grid_mesh(name, rows, material):
    """rows: list of rows of (x,y,z) vertices, quad strip grid."""
    verts, faces = [], []
    w = len(rows[0])
    for row in rows:
        verts.extend(row)
    for i in range(len(rows) - 1):
        for j in range(w - 1):
            a = i * w + j; b = a + 1; c = a + w + 1; d = a + w
            faces.append((a, b, c, d))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    if material: me.materials.append(material)
    me.materials[0].use_backface_culling = False if material else None
    return o

PT = 0.18  # platform top height

# ================================================================ SETTING
# pale boarded floor in front of / under the platform
box("floor_boards", (0, 1.15, 0.01), (6.6, 4.7, 0.02), FLOOR_PALE)
for i in range(9):  # grooves
    box(f"floor_groove_{i}", (-2.9 + i * 0.72, 1.15, 0.021), (0.018, 4.7, 0.004), FLOOR_LINE)
# platform
box("platform", (0, 0, PT / 2), (5.6, 2.5, PT), MID_WOOD)
box("platform_carpet", (0, 0, PT + 0.012), (5.44, 2.34, 0.024), RED_CARPET)
box("platform_front_trim", (0, 1.26, PT - 0.03), (5.6, 0.03, 0.05), GILT)
# back display wall
box("display_wall", (0, -1.32, 1.45), (5.6, 0.10, 2.9), WALL_BROWN)
box("wall_top_cornice", (0, -1.30, 2.92), (5.7, 0.14, 0.07), DARK_WOOD)
box("wall_skirting", (0, -1.26, 0.30), (5.6, 0.05, 0.24), DARK_WOOD)
for wx in (-2.78, 2.78):
    box(f"wall_side_post_{wx}", (wx, -1.30, 1.45), (0.09, 0.13, 2.9), DARK_WOOD)
# hanging blank sign boards on the wall (text deliberately omitted)
box("sign_board_left_blank", (-1.55, -1.255, 2.45), (1.15, 0.03, 0.30), INLAY_CREAM, bevel=0.01)
box("sign_board_right_blank", (1.15, -1.255, 2.52), (1.30, 0.03, 0.26), INLAY_CREAM, bevel=0.01)
# deep-red curtain at right: folded sheet generated as a sine-wave grid
rows = []
for iz in range(7):
    z = 0.25 + iz * 0.4
    row = []
    for ix in range(25):
        x = -2.81 + ix * 0.033
        y = -1.24 + 0.055 * math.sin(ix * 1.55)
        row.append((x, y, z))
    rows.append(row)
grid_mesh("curtain_right", rows, RED_CURT)
box("curtain_rail", (-2.42, -1.24, 2.68), (0.9, 0.05, 0.05), GILT)

# ================================================================ PIANO (centre)
PX, PY = 0.0, -0.42   # piano centre, on platform
PZ = PT               # base z
# main case
box("piano_case", (PX, PY, PZ + 0.66), (1.44, 0.60, 1.14), BLACK_LACQ, bevel=0.02)
box("piano_bottom_plinth", (PX, PY, PZ + 0.07), (1.48, 0.64, 0.14), BLACK_LACQ, bevel=0.01)
box("piano_top_lid", (PX, PY, PZ + 1.255), (1.48, 0.64, 0.07), BLACK_LACQ, bevel=0.01)
# gilt stringing lines
for gx in (-0.70, 0.70):
    box(f"piano_gilt_line_{gx}", (PX + gx, PY + 0.305, PZ + 0.72), (0.018, 0.012, 1.0), GILT)
box("piano_gilt_line_top", (PX, PY + 0.305, PZ + 1.20), (1.40, 0.012, 0.018), GILT)
# three inlay panels on the upper front (papier-mache style: gilt frame,
# coloured ground, small floral dots)
for i, cx in enumerate((-0.46, 0.0, 0.46)):
    ground = (INLAY_TEAL, INLAY_RED, INLAY_TEAL)[i]
    box(f"piano_inlay_frame_{i}", (PX + cx, PY + 0.308, PZ + 0.99), (0.40, 0.014, 0.42), GILT)
    box(f"piano_inlay_panel_{i}", (PX + cx, PY + 0.314, PZ + 0.99), (0.34, 0.012, 0.36), ground)
    # FIX R1: small muted floral dots only (was large bright polka dots)
    for (dx, dz, mm) in ((-0.08, 0.07, DOT_CREAM), (0.07, 0.02, DOT_ROSE),
                         (-0.02, -0.08, GILT), (0.09, -0.09, DOT_SAGE),
                         (0.0, 0.11, DOT_ROSE), (-0.10, -0.03, DOT_CREAM)):
        sphere(f"piano_floral_{i}_{dx}_{dz}", (PX + cx + dx, PY + 0.322, PZ + 0.99 + dz),
               (0.014, 0.007, 0.014), mm, seg=8, rings=6)
# pierced/carved top rail: rail + row of small gilt knobs + two finials
box("piano_top_rail", (PX, PY + 0.16, PZ + 1.335), (1.36, 0.05, 0.09), BLACK_LACQ, bevel=0.01)
for i in range(11):
    sphere(f"piano_rail_pierce_{i}", (PX - 0.55 + i * 0.11, PY + 0.195, PZ + 1.335),
           (0.020, 0.012, 0.026), GILT, seg=8, rings=6)
for fx in (-0.68, 0.68):
    sphere(f"piano_finial_{fx}", (PX + fx, PY + 0.16, PZ + 1.40), (0.045, 0.045, 0.06), GILT, seg=10, rings=8)
# keyboard block, fall, keys
box("piano_keybed", (PX, PY + 0.42, PZ + 0.70), (1.30, 0.22, 0.09), BLACK_LACQ, bevel=0.01)
box("piano_fall", (PX, PY + 0.335, PZ + 0.795), (1.22, 0.03, 0.10), BLACK_LACQ, rot=(math.radians(18), 0, 0))
box("piano_keys_white", (PX, PY + 0.475, PZ + 0.715), (1.16, 0.13, 0.018), IVORY)
box("piano_keys_black", (PX, PY + 0.505, PZ + 0.732), (1.10, 0.055, 0.016), EBONY_KEY)
for kx in (-0.60, 0.60):  # cheek blocks
    box(f"piano_cheek_{kx}", (PX + kx, PY + 0.44, PZ + 0.73), (0.09, 0.20, 0.06), GILT, bevel=0.01)
# music desk + blank sheet of music (NO notation)
box("piano_music_desk", (PX, PY + 0.295, PZ + 0.94), (0.56, 0.02, 0.30), DARK_WOOD,
    rot=(math.radians(24), 0, 0))
box("piano_sheet_music_blank", (PX, PY + 0.312, PZ + 0.955), (0.42, 0.006, 0.27), PAPER,
    rot=(math.radians(24), 0, 0))
# lower front panel + candle sconces
box("piano_lower_panel", (PX, PY + 0.308, PZ + 0.38), (1.10, 0.014, 0.44), BLACK_LACQ)
box("piano_lower_panel_frame", (PX, PY + 0.314, PZ + 0.38), (1.00, 0.010, 0.36), GILT)  # FIX R1: gilt framing
box("piano_lower_panel_inlay", (PX, PY + 0.318, PZ + 0.38), (0.94, 0.010, 0.30), INLAY_RED)
for sx in (-0.60, 0.60):
    cyl(f"piano_sconce_arm_{sx}", (PX + sx, PY + 0.36, PZ + 0.92), 0.016, 0.12, GILT, rot=(math.radians(90), 0, 0), verts=8)
    cyl(f"piano_candle_{sx}", (PX + sx, PY + 0.42, PZ + 0.97), 0.014, 0.11, INLAY_CREAM, verts=8)
# legs / pedal lyre
for lx in (-0.62, 0.62):
    lathe(f"piano_leg_{lx}", [(0.055, 0.0), (0.038, 0.10), (0.055, 0.24), (0.036, 0.38), (0.05, 0.50)],
          BLACK_LACQ, seg=12, loc=(PX + lx, PY + 0.18, PZ + 0.02))
    cyl(f"piano_caster_{lx}", (PX + lx, PY + 0.18, PZ + 0.025), 0.032, 0.03, BRASS, rot=(math.radians(90), 0, 0), verts=10)
box("piano_pedal_lyre", (PX, PY + 0.10, PZ + 0.22), (0.07, 0.07, 0.36), BLACK_LACQ)
for px_ in (-0.025, 0.025):
    box(f"piano_pedal_{px_}", (PX + px_, PY + 0.16, PZ + 0.045), (0.018, 0.07, 0.012), BRASS)
# piano stool: round top, turned column, three feet
SX, SY = PX + 0.05, PY + 0.78
lathe("piano_stool_column", [(0.16, 0.0), (0.05, 0.03), (0.035, 0.18), (0.06, 0.32), (0.04, 0.40)],
      DARK_WOOD, seg=14, loc=(SX, SY, PZ))
cyl("piano_stool_seat", (SX, SY, PZ + 0.455), 0.185, 0.05, UPHOL_RED, verts=20)
torus("piano_stool_seat_rim", (SX, SY, PZ + 0.435), 0.175, 0.016, GILT, maj_seg=20)
for i in range(3):
    a = i * 2 * math.pi / 3 + 0.5
    box(f"piano_stool_foot_{i}", (SX + 0.11 * math.cos(a), SY + 0.11 * math.sin(a), PZ + 0.025),
        (0.20, 0.045, 0.04), DARK_WOOD, rot=(0, 0, -a))

# flanking low cabinets (background goods either side of the piano)
for ci, cx in enumerate((-1.12, 1.08)):
    box(f"side_cabinet_{ci}", (cx, -0.78, PZ + 0.42), (0.72, 0.42, 0.84), DARK_WOOD, bevel=0.015)
    box(f"side_cabinet_top_{ci}", (cx, -0.78, PZ + 0.86), (0.78, 0.46, 0.04), BLACK_LACQ)
    box(f"side_cabinet_door_frame_{ci}", (cx, -0.562, PZ + 0.45), (0.56, 0.012, 0.61), GILT)  # FIX R4
    box(f"side_cabinet_door_inlay_{ci}", (cx, -0.565, PZ + 0.45), (0.5, 0.015, 0.55), CAB_DOOR)
    sphere(f"side_cabinet_knob_{ci}", (cx, -0.575, PZ + 0.45), (0.022, 0.012, 0.022), GILT, seg=8, rings=6)
    # candlestick + small vase on top
    lathe(f"candlestick_{ci}", [(0.05, 0.0), (0.018, 0.05), (0.03, 0.12), (0.016, 0.20)], BRASS, seg=12, loc=(cx - 0.2, -0.82, PZ + 0.88))
    cyl(f"candle_{ci}", (cx - 0.2, -0.82, PZ + 1.13), 0.011, 0.09, INLAY_CREAM, verts=8)
    lathe(f"small_vase_{ci}", [(0.035, 0.0), (0.055, 0.07), (0.025, 0.15), (0.04, 0.19)], INLAY_RED, seg=12, loc=(cx + 0.18, -0.82, PZ + 0.88))

# ================================================================ HOODED PORTER'S CHAIR (right)
HX, HY = -1.82, -0.42
HZ = PZ
# seat base + cushion
box("hooded_base", (HX, HY, HZ + 0.16), (0.82, 0.74, 0.30), GILT, bevel=0.02)  # FIX R2: gilt carved frame
box("hooded_seat_cushion", (HX, HY + 0.02, HZ + 0.335), (0.70, 0.62, 0.09), UPHOL_RED, bevel=0.03)
# legs (gilt, cabriole suggested by taper lathe)
for lx in (-0.34, 0.34):
    for ly in (-0.28, 0.28):
        lathe(f"hooded_leg_{lx}_{ly}", [(0.045, 0.0), (0.028, 0.07), (0.042, 0.13)], GILT, seg=10,
              loc=(HX + lx, HY + ly, HZ))
# arms: gilt posts + pads
for ax in (-0.38, 0.38):
    cyl(f"hooded_arm_post_{ax}", (HX + ax, HY + 0.24, HZ + 0.48), 0.028, 0.30, GILT, verts=10)
    box(f"hooded_arm_pad_{ax}", (HX + ax, HY + 0.05, HZ + 0.645), (0.07, 0.48, 0.05), UPHOL_RED,
        rot=(math.radians(-4), 0, 0), bevel=0.02)
    sphere(f"hooded_arm_knob_{ax}", (HX + ax, HY + 0.27, HZ + 0.66), (0.038, 0.038, 0.038), GILT, seg=10, rings=8)
# hood shell: parametric arc (Y-Z profile) swept across width, gilt outside
rows = []
ARC_CY, ARC_CZ, ARC_R = HY - 0.10, HZ + 1.02, 0.58
for ia in range(13):
    t = math.radians(-72 + ia * 14.5)   # from low back, over the top, to front overhang
    y = ARC_CY + ARC_R * math.sin(t) * -1.0
    z = ARC_CZ + ARC_R * math.cos(t) * 1.0
    # remap: at ia=0 want low/back (y back, z low); use param below instead
    rows.append((y, z))
# rebuild profile explicitly: angle phi from vertical-back to overhang
prof = []
for ia in range(13):
    phi = math.radians(-105 + ia * 15.0)  # -105 (low, behind) .. +75 (overhang front)
    y = (HY - 0.18) + 0.60 * math.sin(phi + math.radians(90)) * 0 - 0.60 * math.cos(phi) * -1.0
    prof.append(phi)
hood_rows = []
for ia in range(15):
    # FIX R2: arc extended at both ends (245deg low/back .. -35deg front)
    # so the hood curves DOWN and encloses the sitter instead of roofing.
    s = ia / 14.0
    ang = math.radians(245 - s * 280)
    yy = (HY - 0.14) + 0.60 * math.cos(ang)
    zz = (HZ + 1.02) + 0.60 * math.sin(ang)
    row = []
    for ix in range(7):
        w = -0.44 + ix * (0.88 / 6)
        row.append((HX + w, yy, zz))
    hood_rows.append(row)
grid_mesh("hooded_hood_shell", hood_rows, HOOD_GILT)
# FIX R2: hanging side cheeks — skirt panels at each side following the
# arc down 0.42 m, closing the hood at the sides.
for sx_sign in (-1, 1):
    cheek_rows = []
    for ia in range(15):
        s = ia / 14.0
        ang = math.radians(245 - s * 280)
        yy = (HY - 0.14) + 0.60 * math.cos(ang)
        zz = (HZ + 1.02) + 0.60 * math.sin(ang)
        cheek_rows.append([(HX + sx_sign * 0.445, yy, zz),
                           (HX + sx_sign * 0.445, yy, zz - 0.42)])
    grid_mesh(f"hooded_hood_cheek_{sx_sign}", cheek_rows, HOOD_GILT)
# inner upholstered back panel (deep orange-red, following the full arc)
inner_rows = []
for ia in range(11):
    s = ia / 10.0
    ang = math.radians(245 - s * 255)
    yy = (HY - 0.14) + 0.545 * math.cos(ang)
    zz = (HZ + 1.02) + 0.545 * math.sin(ang)
    inner_rows.append([(HX - 0.36, yy, zz), (HX - 0.18, yy, zz), (HX, yy, zz),
                       (HX + 0.18, yy, zz), (HX + 0.36, yy, zz)])
grid_mesh("hooded_inner_back", inner_rows, UPHOL_RED)
# deep buttons on inner back (small dark spheres, grid following the arc)
for ia, s in enumerate((0.12, 0.35, 0.58, 0.80)):
    ang = math.radians(245 - s * 255)
    yy = (HY - 0.14) + 0.53 * math.cos(ang); zz = (HZ + 1.02) + 0.53 * math.sin(ang)
    for bx in (-0.24, -0.08, 0.08, 0.24):
        sphere(f"hooded_button_{ia}_{bx}", (HX + bx, yy + 0.018, zz), (0.013, 0.010, 0.013), DARK_WOOD, seg=6, rings=5)
# side wings (lowered/lengthened, FIX R2) + crest
for wx in (-0.44, 0.44):
    box(f"hooded_wing_{wx}", (HX + wx, HY - 0.02, HZ + 0.82), (0.045, 0.55, 1.20), GILT, bevel=0.015)
sphere("hooded_crest", (HX, HY - 0.28, HZ + 1.70), (0.075, 0.05, 0.09), GILT, seg=10, rings=8)
# FIX R2: rim now sits on the new lowered front edge of the arc
cyl("hooded_hood_rim", (HX, HY + 0.35, HZ + 0.68), 0.024, 0.90, GILT, rot=(0, 0, math.radians(90)), verts=10)

# small ornate side chair in front of the hooded chair, blank card on seat
CX, CY = -1.42, 0.52
box("sidechair_seat", (CX, CY, PZ + 0.45), (0.44, 0.40, 0.05), DARK_WOOD, bevel=0.01)
box("sidechair_cushion", (CX, CY, PZ + 0.485), (0.40, 0.36, 0.035), UPHOL_DARK, bevel=0.015)
for lx in (-0.19, 0.19):
    for ly in (-0.17, 0.17):
        h = 0.45 if ly > 0 else 0.88
        cyl(f"sidechair_leg_{lx}_{ly}", (CX + lx, CY + ly, PZ + h / 2), 0.020, h, DARK_WOOD, verts=8)
box("sidechair_toprail", (CX, CY - 0.175, PZ + 0.845), (0.42, 0.035, 0.08), DARK_WOOD, bevel=0.01)
box("sidechair_splat", (CX, CY - 0.175, PZ + 0.66), (0.09, 0.03, 0.30), DARK_WOOD, bevel=0.01)
sphere("sidechair_crest", (CX, CY - 0.175, PZ + 0.905), (0.045, 0.025, 0.045), GILT, seg=8, rings=6)
box("sidechair_card_blank", (CX - 0.05, CY + 0.02, PZ + 0.512), (0.16, 0.11, 0.006), PAPER,
    rot=(math.radians(4), 0, math.radians(-12)))

# gilt pedestal urn beside the chairs
UX, UY = -2.48, 0.05
for i in range(3):
    a = i * 2 * math.pi / 3 + 0.4
    box(f"urn_tripod_leg_{i}", (UX + 0.15 * math.cos(a), UY + 0.15 * math.sin(a), PZ + 0.16),
        (0.30, 0.045, 0.045), GILT, rot=(0, math.radians(18), -a))
cyl("urn_pedestal_column", (UX, UY, PZ + 0.42), 0.045, 0.62, GILT, verts=12)
cyl("urn_pedestal_top", (UX, UY, PZ + 0.75), 0.14, 0.035, GILT, verts=16)
lathe("urn_vase", [(0.055, 0.0), (0.10, 0.05), (0.065, 0.13), (0.155, 0.30), (0.185, 0.42),
                   (0.135, 0.52), (0.165, 0.57)], GILT, seg=18, loc=(UX, UY, PZ + 0.77))
for hx in (-0.185, 0.185):
    torus(f"urn_handle_{hx}", (UX + hx, UY, PZ + 1.12), 0.055, 0.013, GILT,
          rot=(0, math.radians(90), 0), maj_seg=12)

# large round trays / plaques at the right edge: one hanging, two leaning
def tray(name, loc, r, face_mat, rot=(0, 0, 0)):
    cyl(name, loc, r, 0.025, face_mat, rot=rot, verts=24)
    torus(name + "_rim", loc, r - 0.012, 0.016, GILT, rot=rot, maj_seg=24)
    sphere(name + "_boss", (loc[0], loc[1] + 0.02, loc[2]), (r * 0.30, 0.02, r * 0.30),
           INLAY_RED, seg=10, rings=8)
tray("tray_hanging", (-2.42, -1.24, 1.78), 0.34, SILVER, rot=(math.radians(90), 0, 0))
# hanging boss offset fix: boss placed generically above; leaning trays face forward (+Y)
cyl("tray_lean_1", (-2.62, -0.78, PZ + 0.34), 0.36, 0.025, BRASS, rot=(math.radians(78), 0, 0), verts=24)
torus("tray_lean_1_rim", (-2.62, -0.845, PZ + 0.34), 0.345, 0.016, GILT, rot=(math.radians(78), 0, 0), maj_seg=24)
cyl("tray_lean_2", (-2.30, -0.92, PZ + 0.26), 0.28, 0.025, INLAY_TEAL, rot=(math.radians(80), 0, 0), verts=20)
torus("tray_lean_2_rim", (-2.30, -0.975, PZ + 0.26), 0.265, 0.014, GILT, rot=(math.radians(80), 0, 0), maj_seg=20)
box("tray_stand_small", (-2.62, -0.62, PZ + 0.10), (0.30, 0.06, 0.20), DARK_WOOD)

# ================================================================ LEFT / BACK: door-furniture boards
for bi, bx in enumerate((2.42, 1.88, 1.34)):
    bw = 0.46
    box(f"door_board_{bi}", (bx, -1.245, 1.18), (bw, 0.035, 1.30), DARK_WOOD, bevel=0.008)
    box(f"door_board_frame_{bi}", (bx, -1.225, 1.86), (bw + 0.04, 0.03, 0.05), GILT)
    for r in range(4):            # rows of knobs
        for c in range(3):
            kx = bx - 0.14 + c * 0.14
            kz = 0.78 + r * 0.27
            if (r + c + bi) % 3 == 0:   # finger plate in some cells
                box(f"finger_plate_{bi}_{r}_{c}", (kx, -1.222, kz), (0.055, 0.008, 0.17), BRASS)
                sphere(f"plate_knob_{bi}_{r}_{c}", (kx, -1.212, kz), (0.018, 0.012, 0.018), BRASS, seg=6, rings=5)
            elif (r + c + bi) % 3 == 1:  # escutcheon
                box(f"escutcheon_{bi}_{r}_{c}", (kx, -1.222, kz), (0.045, 0.008, 0.075), BRASS)
                sphere(f"keyhole_{bi}_{r}_{c}", (kx, -1.216, kz), (0.008, 0.006, 0.012), BLACK_LACQ, seg=6, rings=5)
            else:                        # round knob on stem
                cyl(f"knob_stem_{bi}_{r}_{c}", (kx, -1.222, kz), 0.008, 0.025, BRASS, rot=(math.radians(90), 0, 0), verts=6)
                sphere(f"knob_{bi}_{r}_{c}", (kx, -1.20, kz), (0.024, 0.018, 0.024), BRASS, seg=8, rings=6)
# diagonal carved panel (stair-rail-like) above the boards
diag = box("diagonal_carved_panel", (1.95, -1.22, 2.28), (2.30, 0.05, 0.20), DARK_WOOD,
           rot=(0, 0, math.radians(-24)), bevel=0.01)
for i in range(7):
    a = math.radians(-24)
    dx = -0.85 + i * 0.28
    lx = 1.95 + dx * math.cos(a); lz = 2.28 + dx * math.sin(a)
    cyl(f"diagonal_baluster_{i}", (lx, -1.17, lz - 0.22), 0.020, 0.30, DARK_WOOD,
        rot=(0, 0, a), verts=8)
box("diagonal_rail_lower", (1.95, -1.22, 2.02), (2.30, 0.05, 0.07), DARK_WOOD, rot=(0, 0, math.radians(-24)))

# metal firescreen / fireback panel at far left (relief simplified to bumps)
FX2, FY2 = 2.52, -0.35
box("firescreen_frame", (FX2, FY2, PZ + 0.62), (0.62, 0.05, 1.05), IRON_DARK,
    rot=(0, math.radians(-18), 0), bevel=0.01)
box("firescreen_panel", (FX2 - 0.055, FY2 + 0.028, PZ + 0.62), (0.50, 0.02, 0.90), IRON_DARK,
    rot=(0, math.radians(-18), 0))
# raised scene: simplified sun / figure bumps on the panel face
ca, sa = math.cos(math.radians(-18)), math.sin(math.radians(-18))
def on_panel(dx, dz):
    return (FX2 - 0.075 - dx * ca, FY2 + 0.045 - dx * sa, PZ + 0.62 + dz)
for (dx, dz, rr, mm) in ((-0.12, 0.22, 0.07, GILT), (0.10, 0.18, 0.05, GILT), (0.0, -0.05, 0.09, IRON_DARK),
                         (-0.13, -0.22, 0.05, GILT), (0.14, -0.20, 0.06, IRON_DARK)):
    p = on_panel(dx, dz)
    sphere(f"firescreen_relief_{dx}_{dz}", p, (rr, 0.02, rr), mm, seg=8, rings=6)
for lx in (-0.24, 0.24):
    p = on_panel(lx, -0.52)
    cyl(f"firescreen_foot_{lx}", (p[0], p[1], PZ + 0.05), 0.022, 0.12, IRON_DARK, verts=8)

# low display table front-left with small goods (trays, boxes)
box("front_table_top", (2.05, 0.55, PZ + 0.52), (1.0, 0.55, 0.04), DARK_WOOD, bevel=0.01)
for lx in (-0.44, 0.44):
    for ly in (-0.22, 0.22):
        box(f"front_table_leg_{lx}_{ly}", (2.05 + lx, 0.55 + ly, PZ + 0.26), (0.05, 0.05, 0.52), DARK_WOOD)
# FIX R5: unclear grey disc + pink block replaced — a round tray leaning
# up at the back of the table, one small dark lidded box, one dark vessel.
cyl("front_table_tray_leaning", (2.28, 0.62, PZ + 0.68), 0.145, 0.018, SILVER, rot=(math.radians(68), 0, 0), verts=20)
torus("front_table_tray_leaning_rim", (2.28, 0.62, PZ + 0.68), 0.132, 0.013, GILT, rot=(math.radians(68), 0, 0), maj_seg=20)
box("front_table_box_dark", (1.84, 0.60, PZ + 0.585), (0.23, 0.17, 0.09), DARK_WOOD, bevel=0.01)
box("front_table_box_lid", (1.84, 0.60, PZ + 0.638), (0.19, 0.13, 0.018), BLACK_LACQ, bevel=0.005)
lathe("front_table_vessel_dark", [(0.032, 0.0), (0.052, 0.05), (0.022, 0.11), (0.036, 0.145)], IRON_DARK, seg=10, loc=(2.02, 0.40, PZ + 0.54))

# ================================================================ VISITORS (stylised, no likenesses)
def figure_head(x, y, z, hair_mat=None):
    sphere("head", (x, y, z), (0.085, 0.088, 0.105), SKIN, seg=12, rings=10)
    if hair_mat:
        sphere("hair", (x, y - 0.012, z + 0.028), (0.088, 0.09, 0.075), hair_mat, seg=10, rings=8)

# woman: blue bodice, white full skirt, yellow bonnet -- left of piano, facing goods (+/- -Y)
WX2, WY2 = 1.08, 0.38
cone("woman_skirt", (WX2, WY2, PZ + 0.42), 0.335, 0.125, 0.84, WHITE_SKIRT, verts=20)
cone("woman_bodice", (WX2, WY2, PZ + 1.02), 0.102, 0.128, 0.36, BLUE_BOD, verts=14)  # FIX R3: slight bodice taper (narrow waist)
cone("woman_bodice_taper", (WX2, WY2, PZ + 0.90), 0.125, 0.105, 0.12, BLUE_BOD, verts=14)
sphere("woman_head", (WX2, WY2, PZ + 1.335), (0.082, 0.085, 0.10), SKIN, seg=12, rings=10)
# bonnet: dome + brim, yellow
sphere("woman_bonnet", (WX2, WY2 + 0.018, PZ + 1.375), (0.098, 0.10, 0.085), YELLOW_BON, seg=12, rings=8)
cyl("woman_bonnet_brim", (WX2, WY2 - 0.045, PZ + 1.345), 0.105, 0.014, YELLOW_BON, rot=(math.radians(78), 0, 0), verts=16)
# arms (simplified, angled down/forward)
for sgn in (-1, 1):
    cyl(f"woman_arm_{sgn}", (WX2 + sgn * 0.15, WY2 - 0.03, PZ + 1.02), 0.032, 0.34, BLUE_BOD,
        rot=(math.radians(28), 0, sgn * math.radians(22)), verts=8)
    sphere(f"woman_hand_{sgn}", (WX2 + sgn * 0.205, WY2 - 0.115, PZ + 0.885), (0.032, 0.032, 0.038), SKIN, seg=8, rings=6)
box("woman_shawl", (WX2, WY2 + 0.075, PZ + 1.10), (0.24, 0.03, 0.20), INLAY_CREAM, rot=(math.radians(10), 0, 0))

# man: black tailcoat + top hat, beside her, slightly behind
# FIX R3: period silhouette instead of a plain cylinder — tapered torso
# (lathe profile: flared skirt -> narrow waist -> chest -> shoulders),
# trousered legs visible below the coat, coat tails behind, angled arms.
MX, MY = 1.48, 0.18
for sgn in (-1, 1):
    cyl(f"man_leg_{sgn}", (MX + sgn * 0.082, MY, PZ + 0.35), 0.050, 0.64, GREY_TROU, verts=10)
    box(f"man_shoe_{sgn}", (MX + sgn * 0.082, MY - 0.045, PZ + 0.025), (0.085, 0.20, 0.045), BLACK_COAT)
_man_torso = lathe("man_coat_torso", [(0.185, 0.0), (0.178, 0.09), (0.138, 0.26), (0.126, 0.42),
                                      (0.142, 0.60), (0.152, 0.68), (0.062, 0.76)],
                   BLACK_COAT, seg=16, loc=(MX, MY, PZ + 0.62))
_man_torso.scale = (1.0, 0.80, 1.0)  # elliptical torso, not a round tube
_man_torso.location.y = MY * 0.20    # compensate: lathe verts bake MY in, scaling would shift the centre
bpy.ops.object.select_all(action='DESELECT'); _man_torso.select_set(True)
bpy.context.view_layer.objects.active = _man_torso
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
_man_torso.select_set(False)
box("man_tail_left", (MX - 0.075, MY + 0.105, PZ + 0.52), (0.115, 0.025, 0.46), BLACK_COAT, rot=(math.radians(8), 0, math.radians(3)))
box("man_tail_right", (MX + 0.075, MY + 0.105, PZ + 0.52), (0.115, 0.025, 0.46), BLACK_COAT, rot=(math.radians(8), 0, math.radians(-3)))
box("man_shirt", (MX, MY - 0.118, PZ + 1.16), (0.105, 0.02, 0.24), WHITE_SHIRT)
sphere("man_head", (MX, MY, PZ + 1.475), (0.084, 0.087, 0.102), SKIN, seg=12, rings=10)
cyl("man_tophat", (MX, MY, PZ + 1.665), 0.088, 0.21, BLACK_COAT, verts=16)
cyl("man_tophat_brim", (MX, MY, PZ + 1.565), 0.135, 0.014, BLACK_COAT, verts=18)
for sgn in (-1, 1):
    # arms: angled down and slightly forward from the shoulder, elbow suggested
    cyl(f"man_arm_{sgn}", (MX + sgn * 0.168, MY - 0.025, PZ + 1.06), 0.036, 0.42, BLACK_COAT,
        rot=(math.radians(22), 0, sgn * math.radians(20)), verts=8)
    sphere(f"man_hand_{sgn}", (MX + sgn * 0.215, MY - 0.085, PZ + 0.865), (0.033, 0.033, 0.04), SKIN, seg=8, rings=6)
cyl("man_cane", (MX + 0.27, MY - 0.10, PZ + 0.45), 0.011, 0.90, DARK_WOOD, rot=(math.radians(6), 0, math.radians(-4)), verts=8)

# ---------------------------------------------------------------- scale / cleanup
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.select_set(True)
bpy.context.view_layer.objects.active = bpy.context.scene.objects[0] if bpy.context.scene.objects else None
bpy.ops.object.select_all(action='DESELECT')

# triangle count
tris = 0
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        for p in o.data.polygons:
            tris += max(0, len(p.vertices) - 2)
print(f"TRIANGLE_COUNT {tris}")
print(f"OBJECT_COUNT {len(bpy.context.scene.objects)}")

# ---------------------------------------------------------------- save + export
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"),
                          export_format='GLB', export_apply=True)

# ---------------------------------------------------------------- preview render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False
world = bpy.data.worlds.new("W") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9

sun_data = bpy.data.lights.new("Sun", 'SUN'); sun_data.energy = 3.0
sun_data.angle = math.radians(25)
sun = bpy.data.objects.new("Sun", sun_data); scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(52), 0, math.radians(-32))
fill_data = bpy.data.lights.new("Fill", 'AREA'); fill_data.energy = 350; fill_data.size = 4.0
fill = bpy.data.objects.new("Fill", fill_data); scene.collection.objects.link(fill)
fill.location = (-3.5, 4.5, 3.5)

cam_data = bpy.data.cameras.new("Cam"); cam_data.lens = 42
cam = bpy.data.objects.new("Cam", cam_data); scene.collection.objects.link(cam)
cam.location = (2.05, 5.9, 2.55)
target = Vector((0.05, -0.15, 0.85))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
