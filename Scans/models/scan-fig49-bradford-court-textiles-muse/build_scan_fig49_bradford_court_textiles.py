#!/usr/bin/env python3
"""Build scan-fig49-bradford-court-textiles — Bradford Court, Great Exhibition 1851.

Composed ~6 m section from the colour reference (fig-49):
  LEFT   timber display kiosk/cabinet with crest, glazed upper, fabrics inside
  CENTRE tall boldly striped hangings in soft folds under a canopy frame
  RIGHT  sloped-glass mahogany counter + second glazed cabinet behind it
  FIGURES two bonneted women in white shawls + a child in a red coat / straw hat
Scale ESTIMATED from the figures (women ~1.6 m). Metres, origin at base centre.
Re-runnable:  blender --background --python build_scan_fig49_bradford_court_textiles.py
"""
import bpy, math, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig49-bradford-court-textiles"

# ---------------------------------------------------------------- setup
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------------------------------------------------------------- procedural textures
def make_stripe_texture():
    """Vertical stripes of varied width/colour, as on the centre hangings."""
    W, H = 1024, 512
    img = bpy.data.images.new("StripeFabric", W, H)
    seq = [  # (width_px, rgba)
        (70, (0.92, 0.88, 0.80, 1)), (26, (0.62, 0.10, 0.08, 1)),
        (48, (0.13, 0.22, 0.42, 1)), (18, (0.92, 0.88, 0.80, 1)),
        (34, (0.78, 0.55, 0.10, 1)), (54, (0.72, 0.16, 0.14, 1)),
        (20, (0.25, 0.38, 0.22, 1)), (60, (0.85, 0.55, 0.60, 1)),
        (24, (0.45, 0.58, 0.70, 1)), (44, (0.30, 0.45, 0.28, 1)),
        (16, (0.92, 0.88, 0.80, 1)), (38, (0.55, 0.12, 0.20, 1)),
    ]
    total = sum(w for w, _ in seq)
    bands, x = [], 0
    while x < W:
        for w, c in seq:
            bands.append((x, x + w, c)); x += w
    px = [0.0] * (W * H * 4)
    for bx0, bx1, c in bands:
        for xx in range(max(bx0, 0), min(bx1, W)):
            shade = 0.96 + 0.07 * math.sin(xx * 0.55)   # woven / fold shading hint
            r, g, b = (min(1, c[0] * shade), min(1, c[1] * shade), min(1, c[2] * shade))
            for yy in range(H):
                i = (yy * W + xx) * 4
                px[i:i + 4] = (r, g, b, 1.0)
    img.pixels = px
    img.pack()
    return img

def make_floor_texture():
    W, H = 1024, 512
    img = bpy.data.images.new("FloorBoards", W, H)
    px = [0.0] * (W * H * 4)
    rows = 12
    rh = H // rows
    for yy in range(H):
        row = yy // rh
        base = 0.72 + 0.05 * math.sin(row * 2.7)
        seam = 0.45 if yy % rh < 2 else 1.0
        for xx in range(W):
            grain = 0.97 + 0.04 * math.sin(xx * 0.05 + row * 3.0)
            joint = 0.5 if (xx + row * 170) % 340 < 2 else 1.0
            v = base * grain * seam * joint
            i = (yy * W + xx) * 4
            px[i:i + 4] = (v * 0.98, v * 0.86, v * 0.68, 1.0)
    img.pixels = px
    img.pack()
    return img

STRIPE_IMG = make_stripe_texture()
FLOOR_IMG = make_floor_texture()

# ---------------------------------------------------------------- materials
def srgb_to_linear(c):
    """Convert one sRGB channel (0-1, as colours are normally picked) to the
    linear value Blender's Base Color socket expects. Fix round 1: the fabric
    colours were authored as display/sRGB values but fed straight into the
    linear socket, which lifts them ~a gamma step in the render — rich cloth
    came out as pastel blobs (baby blue, pink, cream)."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def mat(name, color, rough=0.85, metallic=0.0, alpha=1.0, image=None, repeat=(1, 1),
        srgb=False):
    if srgb:
        color = tuple(srgb_to_linear(c) for c in color)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        try: m.surface_render_method = 'BLENDED'
        except Exception: pass
    if image is not None:
        tex = m.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = image
        tex.extension = 'REPEAT'
        coord = m.node_tree.nodes.new("ShaderNodeTexCoord")
        mapping = m.node_tree.nodes.new("ShaderNodeMapping")
        mapping.inputs["Scale"].default_value = (repeat[0], repeat[1], 1.0)
        m.node_tree.links.new(coord.outputs["UV"], mapping.inputs["Vector"])
        m.node_tree.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
        m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return m

M = {
    'wood':      mat("TimberPolished", (0.30, 0.155, 0.065), 0.55),
    'wood_dark': mat("MahoganyDark", (0.155, 0.05, 0.038), 0.5),
    'wood_mid':  mat("TimberMid", (0.38, 0.21, 0.09), 0.6),
    'brass':     mat("Brass", (0.62, 0.45, 0.16), 0.35, metallic=0.85),
    'gold':      mat("GoldTrim", (0.72, 0.52, 0.14), 0.4, metallic=0.6),
    'glass':     mat("Glass", (0.82, 0.90, 0.94), 0.04, alpha=0.10),
    'floor':     mat("FloorBoards", (1, 1, 1), 0.8, image=FLOOR_IMG, repeat=(1, 2)),
    'stripe':    mat("StripedFabric", (1, 1, 1), 0.9, image=STRIPE_IMG),
    'dark_base': mat("DarkPlinth", (0.16, 0.09, 0.07), 0.7),
    'banner_red':mat("BannerRedBlank", (0.34, 0.045, 0.05), 0.9),
    'cream':     mat("ClothCream", (0.90, 0.86, 0.76), 0.95),
    'white':     mat("ClothWhite", (0.94, 0.93, 0.90), 0.95),
    'skin':      mat("Skin", (0.87, 0.65, 0.52), 0.7),
    'red_coat':  mat("ChildRedCoat", (0.45, 0.09, 0.09), 0.85),
    'straw':     mat("StrawHat", (0.82, 0.66, 0.34), 0.9),
    'green_rib': mat("GreenRibbon", (0.25, 0.45, 0.22), 0.8),
}
# Fix round 1 — palette (sRGB, converted to linear in mat()): richer,
# saturated mid-tones matching the reference cloths (deep greens, burgundy,
# plum purple, ochre, russet) instead of the old pastel set. Only one light
# cloth remains (cream wool, idx 5) for the white pieces in the reference.
FABRIC_COLORS = [(0.46, 0.09, 0.13), (0.13, 0.30, 0.18), (0.12, 0.20, 0.44),
                 (0.74, 0.47, 0.08), (0.36, 0.14, 0.40), (0.87, 0.82, 0.70),
                 (0.60, 0.11, 0.10), (0.08, 0.34, 0.32), (0.54, 0.26, 0.10),
                 (0.36, 0.42, 0.22), (0.40, 0.17, 0.26), (0.20, 0.36, 0.26)]
FABRICS = [mat(f"Fabric{i:02d}", c, 0.95, srgb=True) for i, c in enumerate(FABRIC_COLORS)]

# ---------------------------------------------------------------- helpers
def box(name, loc, size, material, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = size
    if material: o.data.materials.append(material)
    if bevel > 0:
        mod = o.modifiers.new("bev", 'BEVEL'); mod.width = bevel; mod.segments = 2
    return o

def cyl(name, loc, radius, depth, material, vertices=16, rot=(0, 0, 0), r2=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
                                        location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if r2 is not None:  # taper: scale top ring via cone primitive instead
        pass
    if material: o.data.materials.append(material)
    return o

def cone(name, loc, r_bottom, r_top, depth, material, vertices=20):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r_bottom, radius2=r_top,
                                    depth=depth, location=loc)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def ball(name, loc, radius, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=radius, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    if material: o.data.materials.append(material)
    return o

def grid_mesh(name, verts, faces, material, uvs=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if uvs:
        uv = me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            uv.data[loop.index].uv = uvs[loop.vertex_index]
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if material: me.materials.append(material)
    return o

def hanging_cloth(name, cx, cy, top_z, width, height, material,
                  segx=36, segy=16, amp=0.055, freq=5.0, phase=0.0, sway=0.05):
    """Vertical cloth panel with gentle catenary-style folds, deepening downward."""
    verts, uvs, faces = [], [], []
    for j in range(segy + 1):
        v = j / segy
        for i in range(segx + 1):
            u = i / segx
            fold = math.sin(u * freq * 2 * math.pi + phase) * amp * (0.25 + 0.75 * v)
            fold += math.sin(u * freq * 5.3 + phase * 2) * amp * 0.3 * v
            x = cx + (u - 0.5) * width
            y = cy + fold + sway * v * math.sin(u * math.pi)
            z = top_z - v * height
            verts.append((x, y, z)); uvs.append((u * 2.0, 1 - v))
    for j in range(segy):
        for i in range(segx):
            a = j * (segx + 1) + i; b = a + 1; c = a + segx + 1; d = c + 1
            faces.append((a, c, d, b))
    return grid_mesh(name, verts, faces, material, uvs)

def fold_material(base_mat):
    """Darker shade of a fabric material, for the fold ridge welts."""
    name = base_mat.name + "_Fold"
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    src = base_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
    dark = tuple(max(0.0, c * 0.62) for c in src[:3])
    return mat(name, dark, 0.97)

def cloth_mound(name, loc, scale, material):
    """A pile of folded cloth. Fix round 1: the plain scaled sphere read as a
    smooth stone/egg, so the mesh now gets (a) light noise displacement,
    (b) three shallow crease grooves carved across the upper surface, and
    (c) three low ridge welts — segmented boxes in a darker shade of the
    same fabric, following the dome — along the same fold lines. Cheap:
    no cloth sim."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.30,
                                         location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    if material: o.data.materials.append(material)
    seed = (sum((i + 1) * ord(ch) for i, ch in enumerate(name)) % 89) * 0.37
    fold_ys = (-0.115, 0.0, 0.115)  # local fold lines, run along X
    me = o.data
    for v in me.vertices:
        p = v.co
        if p.length < 1e-6:
            continue
        n = p.normalized()
        d = (0.006 * math.sin(p.y * 31.0 + seed)
             + 0.004 * math.sin(p.x * 23.0 + seed * 1.7)
             + 0.003 * math.sin((p.x + p.z) * 41.0 + seed * 0.6))
        if p.z > 0.0:  # crease grooves, fading toward the equator
            fade = min(1.0, p.z / 0.18)
            for fy in fold_ys:
                d -= 0.017 * fade * math.exp(-((p.y - fy) / 0.034) ** 2)
        v.co = p + n * d
    me.update()
    # ridge welts along the fold lines, 3 short segments each so they hug
    # the dome instead of floating at the ends
    ex, ey, ez = 0.30 * scale[0], 0.30 * scale[1], 0.30 * scale[2]
    fm = fold_material(material)
    yaw0 = ((seed * 57.0) % 0.22) - 0.11
    for k, fy in enumerate(fold_ys):
        y_off = fy * scale[1]
        yaw = yaw0 + (k - 1) * 0.05
        cy, sy = math.cos(yaw), math.sin(yaw)
        for xs in (-0.40 * ex, 0.0, 0.40 * ex):
            f = 1.0 - (xs / ex) ** 2 - (y_off / ey) ** 2
            z_top = loc[2] + ez * math.sqrt(max(f, 0.05))
            box(f"{name}_Fold{k}", (loc[0] + cy * xs - sy * y_off,
                                    loc[1] + sy * xs + cy * y_off,
                                    z_top - 0.002),
                (ex * 0.46, 0.020, 0.014), fm, bevel=0.004, rot=(0, 0, yaw))
    return o

# ================================================================ FLOOR
floor = box("Floor_Boarded", (0, 0, -0.03), (6.6, 4.2, 0.06), M['floor'])
# orient plank texture along X: default cube UVs are fine for the top face

# ================================================================ LEFT — TIMBER KIOSK
KX = -2.05  # kiosk centre x
# panelled base
box("Kiosk_Base", (KX, 0.25, 0.38), (1.95, 1.05, 0.76), M['wood'])
box("Kiosk_BasePlinth", (KX, 0.25, 0.03), (2.02, 1.12, 0.06), M['wood_dark'])
box("Kiosk_BaseTopRail", (KX, 0.25, 0.79), (2.0, 1.10, 0.06), M['wood_mid'])
# circular motifs + rectangular panels on the front face (y = -0.285)
for dx in (-0.48, 0.48):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.115, minor_radius=0.018,
        major_segments=24, minor_segments=8, location=(KX + dx, -0.295, 0.38), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object; t.name = "Kiosk_BaseCircleMotif"; t.data.materials.append(M['wood_dark'])
    cyl("Kiosk_BaseCircleDisc", (KX + dx, -0.288, 0.38), 0.10, 0.015, M['wood_mid'],
        vertices=24, rot=(math.pi / 2, 0, 0))
for dx in (-0.82, 0.0, 0.82):
    if abs(dx) < 0.1: continue
    box("Kiosk_BasePanel", (KX + dx, -0.29, 0.38), (0.26, 0.012, 0.44), M['wood_mid'])
# corner + mullion posts of the glazed upper storey
for dx, dy in ((-0.95, -0.28), (0.95, -0.28), (-0.95, 0.78), (0.95, 0.78), (0.0, -0.28)):
    box("Kiosk_Post", (KX + dx, 0.25 + dy, 1.55), (0.07, 0.07, 1.48), M['wood'])
# top entablature + shallow glazed roof
box("Kiosk_TopRail", (KX, 0.25, 2.32), (2.05, 1.15, 0.10), M['wood'])
box("Kiosk_RoofSlab", (KX, 0.25, 2.44), (1.80, 0.90, 0.05), M['wood_mid'])
box("Kiosk_RoofGlass", (KX, 0.25, 2.48), (1.30, 0.55, 0.03), M['glass'])
box("Kiosk_RoofRidge", (KX, 0.25, 2.52), (1.85, 0.10, 0.05), M['wood_dark'])
# glass panes (front + sides)
box("Kiosk_GlassFront", (KX, -0.285, 1.55), (1.86, 0.015, 1.42), M['glass'])
box("Kiosk_GlassSideL", (KX - 0.965, 0.25, 1.55), (0.015, 1.0, 1.42), M['glass'])
box("Kiosk_GlassSideR", (KX + 0.965, 0.25, 1.55), (0.015, 1.0, 1.42), M['glass'])
# pediment crest: stepped base, oval plaque with gold rim and blue centre
box("Kiosk_CrestBase", (KX - 0.55, 0.10, 2.55), (0.40, 0.14, 0.32), M['wood'])
cyl("Kiosk_CrestOvalRim", (KX - 0.55, 0.02, 2.82), 0.20, 0.04, M['gold'], vertices=24, rot=(math.pi / 2, 0, 0))
o = cyl("Kiosk_CrestOval", (KX - 0.55, 0.0, 2.82), 0.16, 0.045, mat("CrestBlue", (0.15, 0.25, 0.5), 0.6),
        vertices=24, rot=(math.pi / 2, 0, 0)); o.scale = (1.0, 1.30, 1.0)
ball("Kiosk_CrestScrollL", (KX - 0.80, 0.10, 2.62), 0.055, M['wood_dark'])
ball("Kiosk_CrestScrollR", (KX - 0.30, 0.10, 2.62), 0.055, M['wood_dark'])
# interior: draped fabrics hanging at the back + piled / folded cloth on shelves
for i, fx in enumerate((-0.62, -0.05, 0.52)):
    hanging_cloth(f"Kiosk_Drape{i}", KX + fx, 0.62, 2.22, 0.52, 1.30,
                  FABRICS[i * 2], segx=14, segy=10, amp=0.04, freq=3.0, phase=i * 1.3)
box("Kiosk_Shelf", (KX, 0.30, 1.02), (1.80, 0.85, 0.05), M['wood_dark'])
for i, (fx, fz) in enumerate(((-0.60, 1.22), (-0.05, 1.30), (0.52, 1.20), (-0.32, 0.95), (0.25, 0.97))):
    cloth_mound(f"Kiosk_ClothPile{i}", (KX + fx, 0.05, fz), (1.05, 0.80, 0.45), FABRICS[(i * 3 + 1) % len(FABRICS)])
for i, fx in enumerate((-0.70, 0.05, 0.68)):
    box(f"Kiosk_FoldedStack{i}", (KX + fx, 0.02, 0.90), (0.34, 0.30, 0.16),
        FABRICS[(i * 4 + 2) % len(FABRICS)], bevel=0.03)

# ================================================================ CENTRE — STRIPED HANGINGS
CX = 0.15
# dark plinth / low counter beneath the hangings
box("Centre_Plinth", (CX, 0.55, 0.33), (2.70, 1.05, 0.66), M['dark_base'])
box("Centre_PlinthTop", (CX, 0.55, 0.68), (2.74, 1.09, 0.05), M['wood_dark'])
# canopy frame: brass posts with finials + flat canopy roof
for dx, dy in ((-1.32, 0.05), (1.32, 0.05), (-1.32, 1.05), (1.32, 1.05)):
    cyl("Centre_Post", (CX + dx, dy, 1.80), 0.035, 2.25, M['brass'], vertices=12)
    ball("Centre_Finial", (CX + dx, dy, 2.97), 0.05, M['gold'], scale=(1, 1, 1.5))
box("Centre_CanopyRoof", (CX, 0.55, 2.95), (2.78, 1.18, 0.07), M['wood_dark'])
box("Centre_CanopyValance", (CX, 0.0, 2.82), (2.78, 0.04, 0.20), M['wood_mid'])
# the signature hangings: two broad striped panels + a narrower third at the right
hanging_cloth("StripeHanging_Main", CX - 0.48, 0.28, 2.90, 1.55, 2.18, M['stripe'],
              segx=44, segy=18, amp=0.065, freq=4.2, phase=0.0)
hanging_cloth("StripeHanging_Right", CX + 0.72, 0.42, 2.90, 0.95, 2.05, M['stripe'],
              segx=30, segy=18, amp=0.055, freq=3.6, phase=1.7)
hanging_cloth("StripeHanging_Back", CX - 0.10, 0.95, 2.90, 2.20, 2.20, M['stripe'],
              segx=36, segy=14, amp=0.04, freq=3.0, phase=3.1)
# a striped length draped over the plinth front edge
hanging_cloth("StripeHanging_PlinthDrape", CX + 0.55, -0.02, 0.70, 0.70, 0.55, M['stripe'],
              segx=18, segy=8, amp=0.03, freq=3.0, phase=0.6)

# blank deep-red banner (lettering in the original omitted — see NOTES)
hanging_cloth("Banner_RedBlank", 1.05, 1.55, 3.55, 1.35, 0.62, M['banner_red'],
              segx=20, segy=8, amp=0.03, freq=2.0, phase=0.4)
cyl("Banner_Rail", (1.05, 1.55, 3.58), 0.02, 1.5, M['wood_dark'], vertices=8, rot=(0, math.pi / 2, 0))

# ================================================================ RIGHT — SLOPED-GLASS COUNTER
RX = 2.30
# mahogany base (front at y ~ -1.05, in the near right foreground)
box("Counter_Base", (RX, -0.55, 0.45), (1.55, 1.0, 0.90), M['wood_dark'])
box("Counter_BasePlinth", (RX, -0.55, 0.04), (1.62, 1.07, 0.08), mat("CounterPlinth", (0.12, 0.05, 0.04), 0.6))
box("Counter_GoldLine", (RX, -1.06, 0.68), (1.56, 0.015, 0.025), M['gold'])
# fabrics inside the counter
for i, (fx, fc) in enumerate(((-0.45, 10), (0.05, 0), (0.50, 8))):
    cloth_mound(f"Counter_Cloth{i}", (RX + fx, -0.62, 0.92), (0.85, 0.80, 0.45), FABRICS[fc % len(FABRICS)])
cyl("Counter_ClothRoll", (RX - 0.15, -0.35, 0.95), 0.09, 0.80, M['white'], vertices=12, rot=(0, math.pi / 2, 0))
# sloped glass top, sloping down toward the viewer (-Y)
slope = math.radians(28)
glass = box("Counter_GlassSlope", (RX, -0.55, 1.13), (1.50, 1.05, 0.02), M['glass'], rot=(slope, 0, 0))
# frame bars around / across the sloped glass
for dx in (-0.74, 0.0, 0.74):
    box("Counter_GlassBarV", (RX + dx, -0.55, 1.145), (0.045, 1.10, 0.035), M['wood_dark'], rot=(slope, 0, 0))
for dy, dz in ((-1.03, 0.90), (-0.07, 1.36)):
    box("Counter_GlassBarH", (RX, dy, dz), (1.52, 0.05, 0.035), M['wood_dark'], rot=(slope, 0, 0))
box("Counter_BackBoard", (RX, 0.02, 1.18), (1.55, 0.06, 0.62), M['wood_dark'])

# ================================================================ RIGHT REAR — SECOND GLAZED CABINET
GX, GY = 2.45, 1.15
box("Cabinet2_Base", (GX, GY, 0.30), (1.65, 0.70, 0.60), M['wood'])
for dx, dy in ((-0.79, -0.32), (0.79, -0.32), (-0.79, 0.32), (0.79, 0.32), (0.0, -0.32)):
    box("Cabinet2_Post", (GX + dx, GY + dy, 1.28), (0.06, 0.06, 1.36), M['wood_mid'])
box("Cabinet2_TopRail", (GX, GY, 1.99), (1.70, 0.75, 0.08), M['wood'])
box("Cabinet2_GlassFront", (GX, GY - 0.345, 1.28), (1.55, 0.015, 1.30), M['glass'])
hanging_cloth("Cabinet2_DrapeL", GX - 0.42, GY + 0.18, 1.92, 0.62, 1.22,
              mat("DrapeSage", (0.52, 0.58, 0.48), 0.95), segx=14, segy=10, amp=0.04, freq=3.0)
hanging_cloth("Cabinet2_DrapeR", GX + 0.42, GY + 0.18, 1.92, 0.62, 1.22,
              mat("DrapeGrey", (0.55, 0.52, 0.50), 0.95), segx=14, segy=10, amp=0.04, freq=3.0, phase=1.2)
# simplified gold crest plaque centred between the drapes (heraldic device in the original)
ball("Cabinet2_Crest", (GX, GY - 0.05, 1.45), 0.16, M['gold'], scale=(1.0, 0.45, 1.25))
box("Cabinet2_CrestBase", (GX, GY - 0.05, 1.22), (0.22, 0.10, 0.08), M['gold'])

# ================================================================ FIGURES (stylised, no likenesses)
def woman(name, x, y, skirt_mat, phase=0.0):
    """~1.62 m: full skirt, white shawl, bonnet with green ribbon. Faces -Y (viewer)."""
    cone(f"{name}_Skirt", (x, y, 0.45), 0.335, 0.155, 0.90, skirt_mat, vertices=22)
    cone(f"{name}_Shawl", (x, y, 1.13), 0.21, 0.105, 0.48, M['white'], vertices=18)
    # shawl point hanging down the front
    cone(f"{name}_ShawlPoint", (x, y - 0.16, 0.86), 0.02, 0.11, 0.42, M['white'], vertices=4)
    # sleeves / forearms angled down-forward, hands meeting at the front
    for s in (-1, 1):
        cyl(f"{name}_Arm", (x + s * 0.13, y - 0.10, 1.02), 0.035, 0.34, M['white'],
            vertices=10, rot=(math.radians(52), 0, s * math.radians(-18)))
    ball(f"{name}_Head", (x, y - 0.014, 1.53), 0.092, M['skin'], scale=(0.92, 0.95, 1.05))
    # bonnet: dome over the back/top of the head + brim framing the face
    ball(f"{name}_Bonnet", (x, y + 0.042, 1.565), 0.105, M['cream'], scale=(1.0, 0.92, 0.92))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.105, minor_radius=0.020,
        major_segments=20, minor_segments=8, location=(x, y - 0.045, 1.545), rotation=(math.radians(18), 0, 0))
    t = bpy.context.object; t.name = f"{name}_BonnetBrim"; t.data.materials.append(M['cream'])
    # green ribbon bow under the chin
    ball(f"{name}_Ribbon", (x, y - 0.095, 1.44), 0.035, M['green_rib'], scale=(1.3, 0.6, 0.8))

woman("Woman1", 0.74, -0.42, mat("SkirtGreenStripe", (0.50, 0.55, 0.38), 0.95))
woman("Woman2", 1.14, -0.22, mat("SkirtPale", (0.72, 0.68, 0.58), 0.95), phase=1.0)

# child (~0.98 m): red coat, white stockings, straw hat, holding a thin stick
CXc, CYc = 0.30, -0.78
for s in (-1, 1):
    cyl("Child_Leg", (CXc + s * 0.055, CYc, 0.14), 0.028, 0.28, M['white'], vertices=8)
    box("Child_Shoe", (CXc + s * 0.055, CYc - 0.02, 0.02), (0.05, 0.11, 0.035), M['wood_dark'])
cone("Child_Coat", (CXc, CYc, 0.50), 0.185, 0.105, 0.46, M['red_coat'], vertices=16)
cyl("Child_Arm", (CXc + 0.13, CYc - 0.05, 0.52), 0.026, 0.26, M['red_coat'],
    vertices=8, rot=(math.radians(40), 0, math.radians(-25)))
ball("Child_Head", (CXc, CYc, 0.845), 0.082, M['skin'], scale=(0.92, 0.95, 1.05))
cyl("Child_HatBrim", (CXc, CYc, 0.915), 0.155, 0.018, M['straw'], vertices=20)
ball("Child_HatDome", (CXc, CYc, 0.93), 0.085, M['straw'], scale=(1, 1, 0.55))
cyl("Child_Stick", (CXc + 0.20, CYc - 0.13, 0.28), 0.008, 0.55, M['wood_dark'],
    vertices=6, rot=(math.radians(24), 0, math.radians(-14)))

# ================================================================ APPLY SCALE, CAMERA, LIGHTS
bpy.ops.object.select_all(action='SELECT')
for o in bpy.context.selected_objects:
    if o.type == 'MESH':
        bpy.context.view_layer.objects.active = o
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

cam_data = bpy.data.cameras.new("Camera"); cam_data.lens = 42
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (4.35, -5.55, 2.85)
target = Vector((0.05, 0.15, 1.05))
direction = target - Vector(cam.location)
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(3, -2, 6))
sun = bpy.context.object; sun.data.energy = 1.8; sun.rotation_euler = (math.radians(50), 0, math.radians(35))
bpy.ops.object.light_add(type='AREA', location=(-2, -4, 4))
area = bpy.context.object; area.data.energy = 200; area.data.size = 4
area.rotation_euler = (math.radians(60), 0, math.radians(-20))

world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.32, 0.32, 0.32, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55

scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.filepath = os.path.join(OUT, "preview.png")

# ================================================================ SAVE + EXPORT + REPORT
tris = 0
for o in bpy.data.objects:
    if o.type == 'MESH':
        tris += sum(max(0, len(p.vertices) - 2) for p in o.data.polygons)
print(f"TRIANGLES: {tris}")
print(f"OBJECTS: {len([o for o in bpy.data.objects if o.type=='MESH'])}")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"),
                          export_format='GLB', export_apply=True)
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
