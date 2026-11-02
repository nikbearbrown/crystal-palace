#!/usr/bin/env python3
"""Build scan-fig36-pugin-medieval-court: Pugin's Medieval Court, Great Exhibition 1851.
Composed single court bay (~7 m wide) from the fig-36 colour view.
Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig36_pugin_medieval_court.py
Outputs .blend, .glb, preview.png beside this script.
No heraldry, no text/inscriptions. Fabric pattern is a procedural sun/flower repeat.
"""
import bpy, math, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig36-pugin-medieval-court"

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------- materials ----------
def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

STONE   = mat("PaleStone", (0.78, 0.74, 0.66), 0.85)
STONE_D = mat("StoneDark", (0.55, 0.51, 0.45), 0.9)
GILT    = mat("Gilt", (0.83, 0.62, 0.18), 0.35, 0.85)
GILT_D  = mat("GiltDark", (0.55, 0.40, 0.12), 0.45, 0.8)
SILVER  = mat("SilverPlate", (0.82, 0.83, 0.85), 0.25, 0.9)
BLACKM  = mat("BlackMetal", (0.05, 0.05, 0.06), 0.5, 0.6)
CANDLE  = mat("CandleWax", (0.95, 0.93, 0.86), 0.6)
WHITE   = mat("AltarClothWhite", (0.93, 0.92, 0.88), 0.8)
REDCARP = mat("RedCarpet", (0.45, 0.06, 0.08), 0.95)
BLUEW   = mat("DarkBlueWall", (0.03, 0.06, 0.16), 0.9)
WOOD    = mat("DarkWood", (0.11, 0.06, 0.025), 0.8)
WOOD_D  = mat("DarkWoodFloor", (0.13, 0.075, 0.035), 0.85)
PURPLE  = mat("PurpleDrape", (0.30, 0.12, 0.38), 0.9)
SKIN    = mat("SkinTone", (0.85, 0.65, 0.52), 0.7)
DRESS1  = mat("DressFloralCream", (0.88, 0.80, 0.62), 0.85)
DRESS2  = mat("DressBurgundy", (0.13, 0.02, 0.035), 0.85)
COAT    = mat("TailcoatBlack", (0.02, 0.02, 0.025), 0.8)
TROUSER = mat("TrousersGrey", (0.09, 0.09, 0.09), 0.85)
GREEN   = mat("Foliage", (0.16, 0.35, 0.14), 0.9)
FLOW_R  = mat("FlowerRed", (0.75, 0.15, 0.18), 0.7)
FLOW_W  = mat("FlowerWhite", (0.92, 0.90, 0.85), 0.7)
FLOW_P  = mat("FlowerPink", (0.85, 0.55, 0.60), 0.7)
DARKIN  = mat("PierceShadow", (0.10, 0.09, 0.08), 0.95)

GLASS = bpy.data.materials.new("GlassCase")
GLASS.use_nodes = True
gb = GLASS.node_tree.nodes["Principled BSDF"]
gb.inputs["Base Color"].default_value = (0.85, 0.92, 0.95, 1.0)
gb.inputs["Roughness"].default_value = 0.08
gb.inputs["Metallic"].default_value = 0.0
gb.inputs["Alpha"].default_value = 0.16
GLASS.surface_render_method = 'DITHERED'
if hasattr(GLASS, "blend_method"):
    try: GLASS.blend_method = 'BLEND'
    except Exception: pass

# Procedural red + gold sun/flower fabric texture (no symbols, no text)
def fabric_material():
    W = H = 256
    img = bpy.data.images.new("CanopyFabric", W, H)
    px = [(0.42, 0.05, 0.07, 1.0)] * (W * H)  # deep red ground
    def setp(x, y, c):
        x %= W; y %= H
        px[y * W + x] = c
    gold = (0.85, 0.62, 0.16, 1.0); gold2 = (0.95, 0.78, 0.30, 1.0)
    tile = 64
    for ty in range(0, H, tile):
        for tx in range(0, W, tile):
            cx, cy = tx + tile // 2, ty + tile // 2
            for a in range(12):  # sun/flower petals
                ang = a * math.pi / 6
                for r in (9, 12):
                    setp(cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang)), gold)
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    if dx * dx + dy * dy <= 25:
                        setp(cx + dx, cy + dy, gold2)
            for (ox, oy) in ((0, 0), (tile // 2, tile // 2)):  # small offset dot flowers
                sx, sy = tx + ox + 8, ty + oy + 8
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        if dx * dx + dy * dy <= 9:
                            setp(sx + dx, sy + dy, gold)
    img.pixels = [v for p in px for v in p]
    m = bpy.data.materials.new("CanopyRedGoldFabric")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.9
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
    tex.extension = 'REPEAT'
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (5, 5, 5)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return m
FABRIC = fabric_material()

# ---------- helpers ----------
def link(obj, material=None):
    bpy.context.collection.objects.link(obj)
    if material: obj.data.materials.append(material)
    return obj

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def cyl(name, loc, r, h, material=None, verts=14, rot=(0, 0, 0), r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r if r2 is None else r2,
                                    depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def cone(name, loc, r, h, material=None, verts=16, r2=0.0):
    return cyl(name, loc, r, h, material, verts=verts, r2=r2)

def sph(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, location=loc, radius=r)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def torus(name, loc, R, r, material=None, rot=(math.pi/2, 0, 0), seg=28):
    bpy.ops.mesh.primitive_torus_add(major_segments=seg, minor_segments=8,
                                     major_radius=R, minor_radius=r, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def strut(name, p1, p2, r, material):
    """Cylinder between two points (arms, chains, sloped edges)."""
    a, b = Vector(p1), Vector(p2)
    mid = (a + b) / 2; d = b - a
    o = cyl(name, tuple(mid), r, d.length, material, verts=8)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return o

def candle(name, loc, h=0.28, r=0.016):
    cyl(name, loc, r, h, CANDLE, verts=10)
    sph(name + "_flame", (loc[0], loc[1], loc[2] + h/2 + 0.02), 0.012,
        mat("Flame" + name, (1.0, 0.75, 0.25), 0.4), scale=(0.7, 0.7, 1.6))

def chalice(name, loc, s=1.0, material=SILVER):
    cyl(name + "_foot", (loc[0], loc[1], loc[2] + 0.01*s), 0.045*s, 0.02*s, material, verts=12)
    cyl(name + "_stem", (loc[0], loc[1], loc[2] + 0.06*s), 0.012*s, 0.09*s, material, verts=10)
    cone(name + "_cup", (loc[0], loc[1], loc[2] + 0.15*s), 0.05*s, 0.10*s, material, verts=14, r2=0.018*s)

def tall_pricket(name, x, y, z0, h=1.55):
    cyl(name + "_base", (x, y, z0 + 0.03), 0.11, 0.06, GILT, verts=12)
    cyl(name + "_shaft", (x, y, z0 + h/2), 0.022, h, GILT, verts=10)
    torus(name + "_knop", (x, y, z0 + h*0.55), 0.045, 0.014, GILT, rot=(math.pi/2, 0, 0), seg=16)
    cyl(name + "_pan", (x, y, z0 + h + 0.015), 0.05, 0.03, GILT, verts=12)
    candle(name + "_candle", (x, y, z0 + h + 0.17), 0.30)

def angel_figure(name, x, y, z0, s=1.0):
    """Simplified small angel atop a candlestick: cone robe, head, two wing slabs."""
    cone(name + "_robe", (x, y, z0 + 0.16*s), 0.075*s, 0.32*s, GILT, verts=12, r2=0.03*s)
    sph(name + "_head", (x, y, z0 + 0.38*s), 0.045*s, GILT)
    box(name + "_wingL", (x - 0.085*s, y - 0.01, z0 + 0.30*s), (0.03*s, 0.02, 0.20*s), GILT, rot=(0, 0.5, 0.25))
    box(name + "_wingR", (x + 0.085*s, y - 0.01, z0 + 0.30*s), (0.03*s, 0.02, 0.20*s), GILT, rot=(0, -0.5, -0.25))

# =========================================================
# FLOOR + BACK WALL  (bay ~7.4 m wide, 5.2 m deep)
# =========================================================
# floor boards: single slab + groove lines via thin dark boxes
box("FloorSlab", (0, 0.3, -0.03), (7.4, 5.2, 0.06), WOOD_D)
for i in range(13):
    x = -3.6 + i * 0.6
    box(f"FloorGroove{i}", (x, 0.3, 0.005), (0.02, 5.2, 0.012), DARKIN)
# back wall: dark blue panels with moulding strips (dims are x=width, y=thickness, z=height)
box("BackWall", (0, 2.9, 2.05), (7.4, 0.12, 4.1), BLUEW)
for i, x in enumerate((-2.7, -0.9, 0.9, 2.7)):
    box(f"WallPanel{i}", (x, 2.80, 1.95), (1.5, 0.06, 3.5), mat(f"BluePanel{i}", (0.04, 0.08, 0.20), 0.9))
    box(f"WallPanelTrim{i}", (x, 2.815, 1.95), (1.62, 0.03, 3.62), GILT_D)

# =========================================================
# CENTRE: PLATFORM, ALTAR + DRAPED CANOPY / TESTER
# =========================================================
CX, CY = -0.15, 1.15          # canopy centre plan position
PZ = 0.22                     # platform top height
box("PlatformStep", (CX, CY, 0.07), (3.1, 2.1, 0.14), WOOD)
box("PlatformCarpet", (CX, CY, 0.175), (2.9, 1.9, 0.09), REDCARP)
box("PlatformCarpetTop", (CX, CY, PZ + 0.005), (2.7, 1.7, 0.02), FABRIC)
# altar table + white cloth + red frontal
box("AltarTable", (CX, CY, PZ + 0.42), (1.5, 0.55, 0.84), WOOD)
box("AltarCloth", (CX, CY - 0.02, PZ + 0.86), (1.62, 0.66, 0.06), WHITE)
box("AltarFrontal", (CX, CY - 0.315, PZ + 0.45), (1.4, 0.03, 0.72), FABRIC)
# altar plate: chalices, small candlesticks, cross
chalice("ChaliceL", (CX - 0.45, CY, PZ + 0.89)); chalice("ChaliceR", (CX + 0.45, CY, PZ + 0.89))
chalice("ChaliceC", (CX, CY + 0.08, PZ + 0.89), s=0.8, material=GILT)
for sx in (-0.62, 0.62):
    cyl(f"AltarStick{sx}", (CX + sx, CY, PZ + 0.97), 0.035, 0.16, GILT, verts=10)
    candle(f"AltarCandle{sx}", (CX + sx, CY, PZ + 1.13), 0.16, 0.012)
box("AltarCrossV", (CX, CY + 0.14, PZ + 1.12), (0.03, 0.03, 0.42), GILT)
box("AltarCrossH", (CX, CY + 0.14, PZ + 1.20), (0.20, 0.03, 0.03), GILT)
cyl("AltarCrossBase", (CX, CY + 0.14, PZ + 0.92), 0.06, 0.03, GILT, verts=10)
# canopy posts (gilt) + tester frame
for px, py in ((-1.05, -0.75), (1.05, -0.75), (-1.05, 0.75), (1.05, 0.75)):
    cyl(f"CanopyPost{px}_{py}", (CX + px, CY + py, PZ + 1.55), 0.045, 3.1, GILT_D, verts=10)
    sph(f"CanopyFinial{px}_{py}", (CX + px, CY + py, PZ + 3.18), 0.07, GILT)
    cone(f"CanopySpire{px}_{py}", (CX + px, CY + py, PZ + 3.38), 0.05, 0.28, GILT, verts=10)
TOP = PZ + 3.1
box("TesterTop", (CX, CY, TOP + 0.05), (2.3, 1.7, 0.10), WOOD)
box("TesterFabricTop", (CX, CY, TOP + 0.12), (2.36, 1.76, 0.05), FABRIC)
# backdrop hanging (rear) + side drops + valance with cresting rail
box("CanopyBackdrop", (CX, CY + 0.72, PZ + 1.55), (2.14, 0.05, 3.05), FABRIC)
box("CanopyDropL", (CX - 1.04, CY + 0.35, PZ + 1.55), (0.05, 0.8, 3.05), FABRIC)
box("CanopyDropR", (CX + 1.04, CY + 0.35, PZ + 1.55), (0.05, 0.8, 3.05), FABRIC)
box("ValanceFront", (CX, CY - 0.78, TOP - 0.22), (2.2, 0.05, 0.5), FABRIC)
box("ValanceBack", (CX, CY + 0.78, TOP - 0.22), (2.2, 0.05, 0.5), FABRIC)
box("ValanceL", (CX - 1.08, CY, TOP - 0.22), (0.05, 1.6, 0.5), FABRIC)
box("ValanceR", (CX + 1.08, CY, TOP - 0.22), (0.05, 1.6, 0.5), FABRIC)
box("CrestingRail", (CX, CY - 0.82, TOP + 0.02), (2.3, 0.04, 0.10), GILT)
for i in range(9):  # gilt cresting fleurons (plain finials, no heraldry)
    cone(f"Crest{i}", (CX - 1.0 + i * 0.25, CY - 0.82, TOP + 0.16), 0.035, 0.18, GILT, verts=8)
# tall gilt prickets flanking altar (front pair carry angels)
tall_pricket("PricketL", CX - 1.25, CY - 0.55, PZ)
tall_pricket("PricketR", CX + 1.25, CY - 0.55, PZ)
tall_pricket("PricketLB", CX - 1.25, CY + 0.55, PZ, h=1.35)
tall_pricket("PricketRB", CX + 1.25, CY + 0.55, PZ, h=1.35)
angel_figure("AngelL", CX - 1.25, CY - 0.55, PZ + 1.62, s=0.9)
angel_figure("AngelR", CX + 1.25, CY - 0.55, PZ + 1.62, s=0.9)

# =========================================================
# HANGING GILT CORONA (ring chandelier), top-left of centre
# =========================================================
KX, KY, KZ = -1.55, 0.55, 3.30
torus("CoronaRing", (KX, KY, KZ), 0.52, 0.035, GILT, rot=(0, 0, 0), seg=32)
torus("CoronaRing2", (KX, KY, KZ + 0.10), 0.40, 0.022, GILT, rot=(0, 0, 0), seg=28)
for i in range(8):
    a = i * math.pi / 4
    x, y = KX + 0.52 * math.cos(a), KY + 0.52 * math.sin(a)
    cyl(f"CoronaCup{i}", (x, y, KZ + 0.03), 0.028, 0.05, GILT, verts=8)
    candle(f"CoronaCandle{i}", (x, y, KZ + 0.15), 0.20, 0.011)
    # chains to a ceiling point
    strut(f"CoronaChain{i}", (x, y, KZ + 0.05), (KX, KY, 4.25), 0.006, BLACKM)
sph("CoronaBoss", (KX, KY, 4.25), 0.05, GILT)

# =========================================================
# LEFT: GOTHIC SCREEN WITH STATUE NICHE + CANDELABRUM
# =========================================================
LX = -2.85
box("ScreenLBase", (LX, 1.0, 0.30), (1.55, 0.45, 0.60), STONE)
# body built around an open niche recess (no solid block behind the statue)
box("ScreenLSideL", (LX - 0.56, 1.0, 1.85), (0.33, 0.32, 2.55), STONE)
box("ScreenLSideR", (LX + 0.56, 1.0, 1.85), (0.33, 0.32, 2.55), STONE)
box("ScreenLTop", (LX, 1.0, 2.98), (1.45, 0.32, 0.30), STONE)
box("ScreenLBack", (LX, 1.13, 1.85), (1.45, 0.06, 2.55), STONE_D)
# purple drape visible inside niche, behind the statue
box("NicheDrape", (LX, 1.08, 1.90), (0.80, 0.05, 2.05), PURPLE)
# niche frame: jambs + pointed arch (two raked boxes + apex finial)
box("NicheJambL", (LX - 0.44, 0.86, 1.90), (0.13, 0.12, 2.0), STONE_D)
box("NicheJambR", (LX + 0.44, 0.86, 1.90), (0.13, 0.12, 2.0), STONE_D)
box("NicheArchL", (LX - 0.23, 0.87, 3.02), (0.58, 0.12, 0.12), STONE_D, rot=(0, 0.72, 0))
box("NicheArchR", (LX + 0.23, 0.87, 3.02), (0.58, 0.12, 0.12), STONE_D, rot=(0, -0.72, 0))
cone("NicheApexFinial", (LX, 0.87, 3.38), 0.06, 0.30, STONE_D, verts=8)
# side pinnacles
for sx in (-0.78, 0.78):
    box(f"ScreenLPinBase{sx}", (LX + sx, 1.0, 2.9), (0.22, 0.4, 0.9), STONE)
    cone(f"ScreenLPin{sx}", (LX + sx, 1.0, 3.55), 0.13, 0.55, STONE_D, verts=8, r2=0.02)
    sph(f"ScreenLPinBall{sx}", (LX + sx, 1.0, 3.86), 0.045, STONE_D)
# cornice
box("ScreenLCornice", (LX, 1.0, 3.22), (1.6, 0.44, 0.14), STONE_D)
# STATUE: simplified robed Virgin-and-Child-like exhibit figure (stone, no likeness)
SX, SY = LX, 0.86
cone("StatueRobe", (SX, SY, 1.28), 0.30, 1.30, STONE, verts=14, r2=0.13)
cyl("StatueTorso", (SX, SY, 1.95), 0.15, 0.35, STONE, verts=12)
sph("StatueHead", (SX, SY, 2.28), 0.105, STONE)
cone("StatueVeil", (SX, SY + 0.03, 2.22), 0.14, 0.30, STONE_D, verts=12, r2=0.05)
sph("StatueChildBody", (SX + 0.16, SY - 0.10, 1.78), 0.10, STONE, scale=(0.8, 0.7, 1.3))
sph("StatueChildHead", (SX + 0.17, SY - 0.12, 1.99), 0.06, STONE)
box("StatueArm", (SX + 0.10, SY - 0.12, 1.82), (0.26, 0.07, 0.07), STONE, rot=(0, 0, -0.3))
box("StatuePlinth", (SX, SY, 0.68), (0.55, 0.4, 0.16), STONE_D)
# tall black multi-branch candelabrum in front of screen
BX, BY = -2.05, 0.15
cyl("CandelabrumBase", (BX, BY, 0.05), 0.16, 0.10, BLACKM, verts=12)
cyl("CandelabrumStem", (BX, BY, 0.95), 0.028, 1.8, BLACKM, verts=10)
for i, (ox, oy, hh) in enumerate(((-0.28, 0, 1.95), (0.28, 0, 1.95), (-0.14, 0, 2.12), (0.14, 0, 2.12), (0, 0, 2.30))):
    if ox:
        strut(f"CandelabrumArm{i}", (BX, BY, hh - 0.22), (BX + ox, BY + oy, hh - 0.02), 0.013, BLACKM)
    cyl(f"CandelabrumCup{i}", (BX + ox, BY + oy, hh), 0.03, 0.05, BLACKM, verts=8)
    candle(f"CandelabrumCandle{i}", (BX + ox, BY + oy, hh + 0.12), 0.22, 0.012)
# floral / table display in front of left screen
box("FlowerTable", (-2.7, -0.15, 0.38), (0.85, 0.5, 0.06), WOOD)
for lx_, ly_ in ((-0.35, -0.18), (0.35, -0.18), (-0.35, 0.18), (0.35, 0.18)):
    box(f"FlowerTableLeg{lx_}_{ly_}", (-2.7 + lx_, -0.15 + ly_, 0.18), (0.05, 0.05, 0.36), WOOD)
cyl("FlowerVase", (-2.7, -0.15, 0.52), 0.09, 0.22, GILT_D, verts=10, r2=0.13)
_fl = [FLOW_R, FLOW_W, FLOW_P]
for i in range(9):
    a = i * 2.4
    sph(f"Flower{i}", (-2.7 + 0.16 * math.cos(a), -0.15 + 0.13 * math.sin(a), 0.72 + 0.07 * (i % 3)), 0.05, _fl[i % 3])
sph("FoliageBall", (-2.7, -0.15, 0.66), 0.15, GREEN, scale=(1, 0.85, 0.8))
chalice("TableChalice", (-2.35, -0.05, 0.41), s=0.9, material=GILT)

# =========================================================
# RIGHT: PALE PIERCED GOTHIC SCREEN + RED HANGINGS BEHIND
# =========================================================
RX = 2.55
box("ScreenRBackRed", (RX + 0.35, 1.85, 1.85), (1.15, 0.06, 3.3), FABRIC)  # red patterned hanging behind
box("ScreenRBase", (RX, 1.55, 0.22), (1.5, 0.4, 0.44), STONE)
# uprights + rails forming two pierced panels
for sx in (-0.68, 0.0, 0.68):
    box(f"ScreenRUpright{sx}", (RX + sx, 1.55, 1.75), (0.11, 0.16, 3.1), STONE)
box("ScreenRRailB", (RX, 1.55, 0.55), (1.45, 0.16, 0.14), STONE)
box("ScreenRRailM", (RX, 1.55, 1.80), (1.45, 0.16, 0.12), STONE)
box("ScreenRRailT", (RX, 1.55, 3.05), (1.45, 0.16, 0.14), STONE_D)
for px_ in (-0.34, 0.34):  # pierced panels: pale panel + dark quatrefoil discs (openwork approx.)
    box(f"PiercePanel{px_}", (RX + px_, 1.57, 1.17), (0.56, 0.05, 1.15), STONE)
    box(f"PiercePanelTop{px_}", (RX + px_, 1.57, 2.42), (0.56, 0.05, 1.15), STONE)
    for row, zz in enumerate((0.85, 1.17, 1.49, 2.10, 2.42, 2.74)):
        for col, oo in enumerate((-0.14, 0.14)):
            cyl(f"Pierce{px_}_{row}_{col}", (RX + px_ + oo, 1.53, zz), 0.055, 0.07, DARKIN, verts=10, rot=(math.pi/2, 0, 0))
    # pointed-arch top lights
    box(f"PierceArchL{px_}", (RX + px_ - 0.13, 1.57, 2.92), (0.30, 0.05, 0.06), STONE_D, rot=(0, 0.7, 0))
    box(f"PierceArchR{px_}", (RX + px_ + 0.13, 1.57, 2.92), (0.30, 0.05, 0.06), STONE_D, rot=(0, -0.7, 0))
for sx in (-0.68, 0.0, 0.68):  # delicate pinnacles / finials
    cone(f"ScreenRPin{sx}", (RX + sx, 1.55, 3.48), 0.075, 0.5, STONE_D, verts=8, r2=0.015)
    sph(f"ScreenRPinBall{sx}", (RX + sx, 1.55, 3.30), 0.05, STONE)

# =========================================================
# FOREGROUND RIGHT: GLASS DISPLAY CASE, PYRAMID TOP
# =========================================================
GX, GY = 2.05, -1.15
box("CaseTableTop", (GX, GY, 0.74), (1.25, 0.8, 0.07), WOOD)
for lx_, ly_ in ((-0.55, -0.32), (0.55, -0.32), (-0.55, 0.32), (0.55, 0.32)):
    box(f"CaseLeg{lx_}_{ly_}", (GX + lx_, GY + ly_, 0.36), (0.07, 0.07, 0.72), WOOD)
box("CaseBaseTrim", (GX, GY, 0.80), (1.18, 0.73, 0.05), GILT_D)
# plate inside: ewer, chalices, clock
cone("EwerBody", (GX - 0.32, GY, 0.94), 0.085, 0.24, SILVER, verts=12, r2=0.035)
cyl("EwerNeck", (GX - 0.32, GY, 1.10), 0.028, 0.09, SILVER, verts=10)
torus("EwerHandle", (GX - 0.24, GY, 1.0), 0.055, 0.012, SILVER, rot=(0, math.pi/2, 0), seg=16)
chalice("CaseChalice1", (GX + 0.05, GY - 0.12, 0.83), s=1.1, material=GILT)
chalice("CaseChalice2", (GX + 0.38, GY + 0.14, 0.83), s=0.9)
box("CaseClockBody", (GX + 0.30, GY - 0.18, 0.99), (0.20, 0.10, 0.32), GILT_D)
cyl("CaseClockFace", (GX + 0.30, GY - 0.245, 1.03), 0.075, 0.02, WHITE, verts=16, rot=(math.pi/2, 0, 0))
cone("CaseClockTop", (GX + 0.30, GY - 0.18, 1.20), 0.11, 0.10, GILT, verts=4)
cyl("CasePlate", (GX - 0.05, GY + 0.18, 0.845), 0.13, 0.02, SILVER, verts=16)
# pyramid glass top (4-sided cone, open) + frame edges
gp = cone("CaseGlassPyramid", (GX, GY, 1.22), 0.86, 0.78, GLASS, verts=4)
gp.rotation_euler = (0, 0, math.pi / 4)
# scale pyramid footprint to case rectangle
gp.scale = (0.74, 0.48, 1.0)
bpy.context.view_layer.objects.active = gp
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
for sx, sy in ((-0.60, -0.38), (0.60, -0.38), (-0.60, 0.38), (0.60, 0.38)):
    strut(f"CaseEdge{sx}_{sy}", (GX + sx, GY + sy, 0.84), (GX, GY, 1.60), 0.014, GILT_D)
sph("CaseApex", (GX, GY, 1.63), 0.035, GILT)

# =========================================================
# VISITORS — stylised simplified period figures, no likenesses
# =========================================================
def woman(name, loc, dress, rotz=0.0, bonnet=True):
    """Fix round 1: crinoline rebuilt as 3 stepped tiered flounces (stacked
    cone frustums, each upper tier stepping in but flaring out over the top
    of the tier below to suggest a flounce lip), a tapered bodice above the
    waist, and a bonnet. Still faceless / stylised, same overall height."""
    x, y = loc
    g = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(g)
    # --- tiered skirt: 3 stacked frustums, stepped in going up ---
    # tier 1 (bottom, widest): floor to ~0.40, flares to 0.36 at hem
    cone(name + "_skirtTier1", (x, y, 0.20), 0.36, 0.40, dress, verts=16, r2=0.275)
    # tier 2: sits on tier 1, its hem (0.30) overhangs tier 1's top (0.275) = flounce lip
    cone(name + "_skirtTier2", (x, y, 0.47), 0.30, 0.30, dress, verts=16, r2=0.225)
    # tier 3: hem (0.245) overhangs tier 2's top (0.225) = second flounce lip
    cone(name + "_skirtTier3", (x, y, 0.71), 0.245, 0.26, dress, verts=16, r2=0.165)
    # --- bodice: small taper from waist (0.15) up to shoulders/neck (0.105) ---
    cone(name + "_bodice", (x, y, 1.00), 0.15, 0.32, dress, verts=14, r2=0.105)
    # small rounded shoulder cap so the bodice does not end in a hard rim
    sph(name + "_shoulders", (x, y, 1.15), 0.105, dress, scale=(1.15, 0.85, 0.55))
    # neck + head (faceless); neck spans bodice top into the head so nothing floats
    cyl(name + "_neck", (x, y, 1.225), 0.04, 0.17, SKIN, verts=10)
    sph(name + "_head", (x, y, 1.38), 0.095, SKIN)
    if bonnet:
        sph(name + "_bonnet", (x, y + 0.02, 1.42), 0.115, WHITE, scale=(1, 1, 0.75))
        torus(name + "_bonnetBrim", (x, y - 0.03, 1.40), 0.10, 0.018, WHITE, rot=(0.5, 0, 0), seg=18)
    box(name + "_armL", (x - 0.155, y - 0.05, 1.02), (0.055, 0.055, 0.34), dress, rot=(0.3, 0, 0.35))
    box(name + "_armR", (x + 0.155, y - 0.05, 1.02), (0.055, 0.055, 0.34), dress, rot=(0.3, 0, -0.35))
    for o in bpy.context.collection.objects:
        pass
    return g

def man_tophat(name, loc):
    """Fix round 1: period silhouette instead of a rectangular slab --
    tapered trouser legs below, a coat skirt flaring from the waist to
    about the knee, a torso tapering from broad shoulders down to a
    narrow waist, slim tails behind, simple strut arms, head + top hat
    (hat unchanged). Faceless / stylised, same overall height (~1.88 m
    incl. hat, body ~1.66 m to crown of head / shoulders ~1.49 m)."""
    x, y = loc
    # --- legs below the coat skirt: tapered trousers + shoes (front = -Y) ---
    cyl(name + "_legL", (x - 0.085, y, 0.40), 0.058, 0.80, TROUSER, verts=10, r2=0.082)
    cyl(name + "_legR", (x + 0.085, y, 0.40), 0.058, 0.80, TROUSER, verts=10, r2=0.082)
    box(name + "_shoeL", (x - 0.085, y - 0.035, 0.025), (0.09, 0.21, 0.05), COAT)
    box(name + "_shoeR", (x + 0.085, y - 0.035, 0.025), (0.09, 0.21, 0.05), COAT)
    # --- tailcoat skirt: elliptical frustum flaring from waist to the knee ---
    skirt = cone(name + "_coatSkirt", (x, y, 0.94), 0.185, 0.36, COAT, verts=16, r2=0.148)
    skirt.scale = (1.19, 0.81, 1.0)  # applied by the global transform_apply at the end
    # slim tails hanging behind the skirt (back = +Y)
    box(name + "_tails", (x, y + 0.155, 0.84), (0.24, 0.04, 0.48), COAT, rot=(0.10, 0, 0))
    # --- torso: frustum tapering from broad shoulders to a narrow waist ---
    torso = cyl(name + "_torso", (x, y, 1.305), 0.148, 0.39, COAT, verts=14, r2=0.183)
    torso.scale = (1.18, 0.75, 1.0)
    # rounded shoulder cap
    sph(name + "_shoulders", (x, y, 1.485), 0.155, COAT, scale=(1.28, 0.78, 0.55))
    # shirt front on the tapered chest
    box(name + "_shirt", (x, y - 0.128, 1.33), (0.13, 0.02, 0.27), WHITE, rot=(0.10, 0, 0))
    # --- simple arms: struts shoulder -> hand, small skin hands ---
    strut(name + "_armL", (x - 0.20, y, 1.46), (x - 0.275, y - 0.02, 0.94), 0.046, COAT)
    strut(name + "_armR", (x + 0.20, y, 1.46), (x + 0.285, y - 0.05, 0.96), 0.046, COAT)
    sph(name + "_handL", (x - 0.275, y - 0.02, 0.92), 0.04, SKIN)
    sph(name + "_handR", (x + 0.285, y - 0.05, 0.94), 0.04, SKIN)
    # --- neck, head (faceless) and the top hat (kept from the original) ---
    cyl(name + "_neck", (x, y, 1.49), 0.045, 0.09, SKIN, verts=10)
    sph(name + "_head", (x, y, 1.585), 0.10, SKIN)
    cyl(name + "_hatBrim", (x, y, 1.66), 0.16, 0.02, COAT, verts=16)
    cyl(name + "_hatTop", (x, y, 1.77), 0.105, 0.22, COAT, verts=16)

woman("VisitorWomanCrinoline", (-1.85, -1.55), DRESS1)          # left foreground, floral tiered dress + bonnet (~1.50 m w/ bonnet ~1.53 top of head 1.47+)
man_tophat("VisitorManTopHat", (0.55, -1.75))                    # centre foreground, back three-quarter to displays (~1.88 m incl. hat; body ~1.75 m)
woman("VisitorWomanBurgundy", (3.05, -0.55), DRESS2)             # right, viewing the glass case

# scale figures: woman helper is ~1.47 m to head top — scale up group parts by name prefix
def scale_about(name_prefix, factor, base_z=0.0):
    for o in bpy.data.objects:
        if o.name.startswith(name_prefix) and o.type == 'MESH':
            o.location.z = base_z + (o.location.z - base_z) * factor
            o.location.x *= 1.0  # keep plan position; widen slightly below via scale
            o.scale = (o.scale[0] * (1 + (factor - 1) * 0.4), o.scale[1] * (1 + (factor - 1) * 0.4), o.scale[2] * factor)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
# women to ~1.65 m overall (head top 1.475*1.12 ≈ 1.65)
scale_about("VisitorWomanCrinoline", 1.12)
scale_about("VisitorWomanBurgundy", 1.12)

# =========================================================
# LIGHTING + CAMERA + RENDER
# =========================================================
bpy.ops.object.light_add(type='AREA', location=(3.5, -4.0, 5.0))
key = bpy.context.object; key.name = "KeyLight"; key.data.energy = 500; key.data.shape = 'DISK'; key.data.size = 3.0
key.rotation_euler = (math.radians(55), 0, math.radians(35))
bpy.ops.object.light_add(type='AREA', location=(-4.5, -2.0, 3.5))
fill = bpy.context.object; fill.name = "FillLight"; fill.data.energy = 200; fill.data.size = 2.5
fill.rotation_euler = (math.radians(65), 0, math.radians(-50))
bpy.ops.object.light_add(type='POINT', location=(CX, CY - 1.0, 3.0))
warm = bpy.context.object; warm.name = "CandleGlow"; warm.data.energy = 60
warm.data.color = (1.0, 0.8, 0.55)

world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.55

bpy.ops.object.camera_add(location=(5.4, -7.6, 3.2))
cam = bpy.context.object; cam.name = "PreviewCamera"
# aim camera at canopy centre
target = Vector((-0.3, 0.4, 1.25))
direction = target - Vector(cam.location)
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 38
scene.camera = cam

scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.05
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960; scene.render.resolution_y = 720
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium Contrast'

# apply scale on all meshes (idempotent safety)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')

# triangle count
tris = 0
dg = bpy.context.evaluated_depsgraph_get()
for o in bpy.data.objects:
    if o.type == 'MESH':
        ev = o.evaluated_get(dg)
        m = ev.to_mesh()
        m.calc_loop_triangles()
        tris += len(m.loop_triangles)
        ev.to_mesh_clear()
print(f"TRIANGLE_COUNT {tris}")
print(f"OBJECT_COUNT {len(bpy.data.objects)}")

blend_path = os.path.join(OUT, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(OUT, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", blend_path, glb_path)
