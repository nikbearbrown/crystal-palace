#!/usr/bin/env python3
"""Crystal Palace Scans batch 2 builder (machinery).
Usage: blender -b --python build_<slug>.py -- <slug>
Builds one model, saves .blend, renders preview.png, exports .glb, prints TRIS n.
Stylised low-poly interpretation from a single reference view; see NOTES.md.
"""
import bpy, sys, math, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SLUG = argv[0]
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16
scene.cycles.use_denoising = True
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.52, 0.52, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

MATS = {}
def mat(name, rgb, rough=0.8, metal=0.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    MATS[name] = m; return m

IRON   = mat("cast_iron", (0.10,0.10,0.11), 0.55, 0.55)
STEEL  = mat("steel", (0.45,0.47,0.50), 0.35, 0.8)
BRASS  = mat("brass", (0.55,0.40,0.16), 0.35, 0.85)
WOOD   = mat("wood", (0.48,0.34,0.19), 0.85)
WOOD_D = mat("wood_dark", (0.30,0.20,0.11), 0.85)
WOOD_L = mat("wood_light", (0.66,0.52,0.34), 0.85)
CREAM  = mat("canvas_cream", (0.82,0.78,0.68), 0.9)
WHITE  = mat("paper_white", (0.92,0.90,0.84), 0.9)
RED    = mat("paint_red", (0.55,0.10,0.08), 0.6)
RED_B  = mat("paint_red_bright", (0.56,0.10,0.06), 0.6)
GREEN  = mat("paint_green", (0.12,0.30,0.16), 0.6)
BLUE   = mat("paint_blue", (0.10,0.16,0.38), 0.6)
GOLD   = mat("gold_trim", (0.70,0.52,0.20), 0.4, 0.7)
BLACK  = mat("black_cloth", (0.05,0.05,0.06), 0.95)
BROWN  = mat("brown_coat", (0.30,0.19,0.11), 0.95)
GREY_C = mat("grey_cloth", (0.42,0.42,0.44), 0.95)
SKIN   = mat("skin", (0.80,0.60,0.45), 0.7)
FLOOR  = mat("floor_grey", (0.60,0.60,0.60), 0.95)

MODEL_OBJS = []
def _reg(ob, name=None):
    if name: ob.name = name
    if ob.type == 'MESH': MODEL_OBJS.append(ob)
    return ob

def box(name, loc, size, material=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.object; ob.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: ob.data.materials.append(material)
    return _reg(ob, name)

def cyl(name, loc, r, h, material=None, rot=(0,0,0), verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    ob = bpy.context.object
    if material: ob.data.materials.append(material)
    return _reg(ob, name)

def cone(name, loc, r1, r2, h, material=None, rot=(0,0,0), verts=20):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=h, location=loc, rotation=rot)
    ob = bpy.context.object
    if material: ob.data.materials.append(material)
    return _reg(ob, name)

def sph(name, loc, scale, material=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, location=loc)
    ob = bpy.context.object; ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: ob.data.materials.append(material)
    return _reg(ob, name)

def torus(name, loc, R, r, material=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=24, minor_segments=8, location=loc, rotation=rot)
    ob = bpy.context.object
    if material: ob.data.materials.append(material)
    return _reg(ob, name)

def limb(name, p1, p2, r, material):
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1+p2)/2; d = p2-p1
    ob = cyl(name, tuple(mid), r, d.length, material, verts=10)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0,0,1)).rotation_difference(d.normalized())
    return ob

def wheel(name, loc, R, material_rim, material_spoke, axis='Y', spokes=8, tube=0.035):
    rot = (math.radians(90),0,0) if axis=='Y' else (0,math.radians(90),0)
    g = []
    g.append(torus(name+"_rim", loc, R, tube, material_rim, rot=rot))
    hub_ax = {'Y':(math.radians(90),0,0),'X':(0,math.radians(90),0),'Z':(0,0,0)}[axis]
    g.append(cyl(name+"_hub", loc, tube*2.2, tube*3.4, material_spoke, rot=hub_ax, verts=12))
    for i in range(spokes//2):
        a = math.pi*i/(spokes//2)
        if axis=='Y': d = Vector((math.cos(a),0,math.sin(a)))
        elif axis=='X': d = Vector((0,math.cos(a),math.sin(a)))
        else: d = Vector((math.cos(a),math.sin(a),0))
        p = Vector(loc)
        g.append(limb(name+f"_sp{i}", tuple(p-d*(R-0.02)), tuple(p+d*(R-0.02)), tube*0.45, material_spoke))
    return g

# ---------- stylised period figure ----------
def figure(name, loc, h=1.72, female=False, coat=BLACK, hat='top', skin=SKIN, skirt_mat=None, apron=False, cap_mat=None):
    x,y,z = loc; s = h/1.72
    parts = []
    if female:
        parts.append(cone(name+"_skirt", (x,y,0.42*s), 0.30*s, 0.13*s, 0.84*s, skirt_mat or coat))
        parts.append(cyl(name+"_bodice", (x,y,1.05*s), 0.115*s, 0.44*s, coat, verts=14))
    else:
        parts.append(limb(name+"_legL", (x-0.09*s,y,0.02), (x-0.085*s,y,0.78*s), 0.055*s, GREY_C if coat!=BROWN else BROWN))
        parts.append(limb(name+"_legR", (x+0.09*s,y,0.02), (x+0.085*s,y,0.78*s), 0.055*s, GREY_C if coat!=BROWN else BROWN))
        parts.append(cyl(name+"_torso", (x,y,1.09*s), 0.135*s, 0.62*s, coat, verts=14))
        if apron: parts.append(box(name+"_apron", (x,y-0.125*s,0.92*s), (0.26*s,0.02,0.62*s), CREAM))
    parts.append(cyl(name+"_neck", (x,y,1.40*s), 0.045*s, 0.30*s, skin, verts=10))
    parts.append(sph(name+"_head", (x,y,1.56*s), (0.085*s,0.09*s,0.105*s), skin))
    # arms (simple, slightly forward-down)
    sh = 1.32*s
    parts.append(limb(name+"_armL", (x-0.17*s,y,sh), (x-0.24*s,y-0.08*s,0.92*s), 0.042*s, coat))
    parts.append(limb(name+"_armR", (x+0.17*s,y,sh), (x+0.24*s,y-0.08*s,0.92*s), 0.042*s, coat))
    if hat=='top':
        parts.append(cyl(name+"_tophat", (x,y,1.76*s), 0.075*s, 0.20*s, BLACK, verts=14))
        parts.append(cyl(name+"_brim", (x,y,1.665*s), 0.125*s, 0.015, BLACK, verts=18))
    elif hat=='bonnet':
        parts.append(sph(name+"_bonnet", (x,y-0.01,1.60*s), (0.105*s,0.11*s,0.10*s), mat("bonnet_brown",(0.25,0.16,0.10),0.95)))
        parts.append(sph(name+"_face", (x,y-0.045*s,1.565*s), (0.075*s,0.07*s,0.095*s), skin))
    elif hat=='cap':
        parts.append(cyl(name+"_cap", (x,y,1.665*s), 0.095*s, 0.06*s, cap_mat or BROWN, verts=14))
        parts.append(box(name+"_peak", (x,y-0.115*s,1.635*s), (0.13*s,0.07,0.015), cap_mat or BROWN))
    elif hat=='bowler':
        parts.append(sph(name+"_bowler", (x,y,1.66*s), (0.10*s,0.10*s,0.07*s), BLACK))
        parts.append(cyl(name+"_brim2", (x,y,1.635*s), 0.125*s, 0.012, BLACK, verts=18))
    return parts

# ================= FIG 29 — Platt cotton machines =================
def build_fig29():
    box("Floor", (0,0,-0.03), (10.5,5.6,0.06), WOOD_L)
    # principal carding/prep machine (centre)
    def carding(cx, cz_s=1.0, simple=False):
        box(f"CardBase_{cx}", (cx,0.4,0.30), (2.1,1.15,0.60), IRON)
        box(f"CardFrame_{cx}", (cx,0.35,0.72), (2.2,0.95,0.10), IRON)
        cyl(f"CardDrum_{cx}", (cx,0.35,1.02), 0.52, 1.75, STEEL, rot=(0,math.radians(90),0), verts=24)
        for sx in (-0.95,0.95):
            cyl(f"CardCheek_{cx}_{sx}", (cx+sx,0.35,1.02), 0.60, 0.07, IRON, rot=(0,math.radians(90),0), verts=24)
        cyl(f"FeedRollA_{cx}", (cx,-0.28,0.78), 0.11, 1.8, BRASS, rot=(0,math.radians(90),0))
        cyl(f"FeedRollB_{cx}", (cx,-0.28,0.56), 0.09, 1.8, STEEL, rot=(0,math.radians(90),0))
        if not simple:
            wheel(f"CardGear_{cx}", (cx+1.02,0.35,0.55), 0.30, IRON, STEEL, axis='X', spokes=6)
            box(f"CardLap_{cx}", (cx,-0.62,0.95), (1.5,0.5,0.06), CREAM, rot=(math.radians(-18),0,0))
    carding(0.0)
    carding(-2.9, simple=True); carding(3.0, simple=True)
    # arched covers row (left background)
    for i,cx in enumerate((-4.6,-3.4)):
        cyl(f"ArchCover_{i}", (cx,1.1,0.85), 0.62, 1.0, WOOD_D, rot=(math.radians(90),0,0), verts=18)
        box(f"ArchBase_{i}", (cx,1.1,0.35), (1.05,0.95,0.7), IRON)
    # line shafting overhead + hangers + belts
    cyl("LineShaft", (0,0.3,3.05), 0.045, 9.6, STEEL, rot=(0,math.radians(90),0))
    for hx in (-3.4,0.0,3.4):
        cyl(f"Hanger_{hx}", (hx,0.3,3.62), 0.03, 1.15, IRON)
        cyl(f"Pulley_{hx}", (hx,0.3,3.05), 0.30, 0.10, IRON, rot=(0,math.radians(90),0), verts=20)
        box(f"Belt_{hx}", (hx-0.25,0.32,2.05), (0.07,0.02,2.0), BROWN, rot=(0,0,math.radians(7)))
    # spinning frame background right
    box("SpinFrame", (4.9,1.5,0.55), (2.6,0.7,1.1), WOOD_D)
    for r in range(2):
        for i in range(9):
            cyl(f"Bobbin_{r}_{i}", (3.85+i*0.26, 1.32+r*0.36, 1.22), 0.028, 0.30, CREAM, verts=8)
    # protective rail in front (single bar + turned posts)
    for px in (-3.6,-1.2,1.2,3.6):
        cyl(f"RailPost_{px}", (px,-1.55,0.50), 0.05, 1.0, WOOD_D, verts=12)
        sph(f"RailFinial_{px}", (px,-1.55,1.06), (0.07,0.07,0.07), BRASS)
        box(f"RailBase_{px}", (px,-1.55,0.05), (0.22,0.22,0.10), WOOD_D)
    cyl("RailBar", (0,-1.55,0.93), 0.028, 7.6, WOOD, rot=(0,math.radians(90),0))
    # visitors (front of rail)
    figure("VisitorMan", (-1.7,-2.15,0), 1.74, coat=BLACK, hat='top')
    figure("VisitorWoman", (-2.6,-2.05,0), 1.63, female=True, coat=BROWN, hat='bonnet', skirt_mat=mat("dress_fig29",(0.36,0.28,0.22),0.95))
    figure("VisitorMan2", (2.5,-2.1,0), 1.72, coat=BROWN, hat='top')

# ================= FIG 30 — De La Rue envelope machine =================
def build_fig30():
    box("FloorBoards", (0,0,-0.03), (10,6,0.06), WOOD_L)
    box("Carpet", (0.3,0.1,0.005), (6.4,3.6,0.012), GREEN)
    # red stand back wall + cornice + display boards
    box("StandWall", (-0.7,1.85,1.45), (5.6,0.18,2.9), RED)
    box("StandCornice", (-0.7,1.85,2.98), (5.8,0.30,0.16), GOLD)
    for bx in (-2.45, 0.95):
        box(f"DisplayBoard_{bx}", (bx,1.73,1.95), (1.25,0.05,1.15), BLUE)
        for r in range(3):
            for c in range(4):
                box(f"Env_{bx}_{r}_{c}", (bx-0.42+c*0.28, 1.70, 1.62+r*0.33), (0.20,0.012,0.13), WHITE)
    # paper rolls + stacks on stand
    roll_cols = [(0.62,0.20,0.14),(0.80,0.72,0.30),(0.30,0.55,0.30),(0.85,0.80,0.75),(0.55,0.12,0.10)]
    for i in range(9):
        cm = mat(f"roll_{i}", roll_cols[i % len(roll_cols)], 0.85)
        cyl(f"PaperRoll_{i}", (-1.9+i*0.24, 1.45, 1.62), 0.105, 0.85, cm, verts=14)
    for i,(sx,sy,sz,c) in enumerate([(-2.9,0.9,0.5,(0.6,0.45,0.15)),(-2.5,0.85,0.72,(0.15,0.4,0.2)),(-2.1,0.95,0.42,(0.65,0.15,0.12)),(1.6,1.0,0.5,(0.2,0.35,0.45)),(2.0,0.9,0.66,(0.7,0.6,0.25))]):
        box(f"PaperStack_{i}", (sx,sy,sz), (0.55,0.7,0.16), mat(f"stack_{i}", c, 0.85))
    # rosette fans
    for i,fx in enumerate((-1.3,-0.7,-0.1,0.55,1.9,2.5)):
        sph(f"Rosette_{i}", (fx,0.75,1.28), (0.16,0.05,0.16), WHITE)
        cyl(f"RosetteStem_{i}", (fx,0.75,1.05), 0.015, 0.32, WOOD_D, verts=8)
    # glazed display counter (left front)
    box("Counter", (-2.2,-0.55,0.45), (2.3,1.1,0.9), RED)
    box("CounterGlass", (-2.2,-0.60,0.96), (2.2,0.80,0.03), mat("glass_hint",(0.65,0.72,0.75),0.25,0.1), rot=(math.radians(-18),0,0))
    for i,c in enumerate([(0.6,0.12,0.1),(0.15,0.35,0.2),(0.7,0.55,0.15),(0.2,0.25,0.55)]):
        box(f"CounterBook_{i}", (-2.95+i*0.5,-0.6,0.86), (0.34,0.5,0.07), mat(f"cbook_{i}", c, 0.8), rot=(math.radians(-24),0,0))
    # open sample book on counter end
    box("SampleBookL", (-0.75,-0.5,1.02), (0.5,0.62,0.03), WHITE, rot=(math.radians(-30),0,math.radians(8)))
    box("SampleBookR", (-0.30,-0.5,1.06), (0.5,0.62,0.03), WHITE, rot=(math.radians(-30),0,math.radians(-14)))
    # envelope machine (right-centre): iron table frame + press
    for lx in (0.75,2.15):
        box(f"MachineLeg_{lx}", (lx,0.15,0.48), (0.10,0.75,0.96), IRON)
        box(f"MachineFoot_{lx}", (lx,0.15,0.04), (0.34,0.95,0.08), IRON)
    box("MachineBed", (1.45,0.15,1.00), (1.65,0.85,0.09), IRON)
    box("MachineBedPaper", (1.40,0.05,1.06), (0.85,0.55,0.015), WHITE)
    wheel("Flywheel", (0.72,0.15,0.42), 0.34, IRON, STEEL, axis='X', spokes=6)
    box("PressUprightL", (1.05,0.32,1.32), (0.09,0.09,0.62), IRON)
    box("PressUprightR", (1.85,0.32,1.32), (0.09,0.09,0.62), IRON)
    box("PressHead", (1.45,0.32,1.60), (0.95,0.16,0.14), IRON)
    box("PressPlaten", (1.45,0.18,1.22), (0.55,0.4,0.08), STEEL)
    limb("PressLever", (1.45,0.35,1.66), (2.15,0.75,1.95), 0.03, IRON)
    sph("LeverKnob", (2.15,0.75,1.95), (0.055,0.055,0.055), WOOD_D)
    cyl("CrankWheel", (2.2,0.42,0.55), 0.16, 0.05, IRON, rot=(math.radians(90),0,0), verts=18)
    # rope rail: brass posts + bar
    for px in (-2.9,0.2,2.9):
        cyl(f"BrassPost_{px}", (px,-1.35,0.45), 0.028, 0.9, BRASS, verts=12)
        sph(f"BrassBall_{px}", (px,-1.35,0.94), (0.05,0.05,0.05), BRASS)
    cyl("RopeRail", (0,-1.35,0.86), 0.018, 6.0, mat("rope_red",(0.5,0.08,0.08),0.9), rot=(0,math.radians(90),0))
    # people: attendant at machine, 2 visitors
    figure("Attendant", (0.92,0.80,0), 1.70, coat=BLACK, hat='cap', cap_mat=BLACK)
    figure("VisitorTopHat", (3.15,-0.9,0), 1.76, coat=BLACK, hat='top')
    figure("VisitorWoman", (-3.35,-1.7,0), 1.62, female=True, coat=GREEN, hat='bonnet', skirt_mat=mat("dress_fig30",(0.62,0.35,0.32),0.95))

# ================= FIG 48 — Garrett agricultural stand =================
def build_fig48():
    box("Floor", (0,0,-0.03), (11.5,6.4,0.06), WOOD_L)
    W = 9.6; D = 3.6; colx = (-W/2+0.35,-W/6,W/6,W/2-0.35)
    # columns + capitals
    for i,cx in enumerate(colx):
        cyl(f"Column_{i}", (cx,1.55,1.85), 0.13, 3.7, WHITE, verts=16)
        box(f"ColBase_{i}", (cx,1.55,0.18), (0.4,0.4,0.36), WHITE)
        box(f"ColCap_{i}", (cx,1.55,3.78), (0.44,0.44,0.18), WHITE)
        sph(f"Urn_{i}", (cx,1.55,4.35), (0.16,0.16,0.24), BROWN)
        cone(f"UrnTop_{i}", (cx,1.55,4.62), 0.02, 0.09, 0.14, BROWN)
    # entablature with BLANK fascia boards (no lettering)
    box("FasciaFront", (0,1.55,3.98), (W+0.3,0.10,0.52), BLUE)
    box("FasciaSide", (W/2-0.05,0,3.98), (0.10,D+0.4,0.52), BLUE)
    box("GalleryFloor", (0,0,3.68), (W,D,0.12), WOOD_D)
    # gallery railing: red top rail + X braces + posts
    for gx in [x*0.5 for x in range(-9,10)]:
        cyl(f"GRailPost_{gx}", (gx,1.62,4.55), 0.02, 0.62, STEEL, verts=8)
    cyl("GRailTop", (0,1.62,4.88), 0.03, W, RED_B, rot=(0,math.radians(90),0))
    for i in range(8):
        limb(f"GX_{i}", (-W/2+0.3+i*1.15,1.62,4.30), (-W/2+1.35+i*1.15,1.62,4.82), 0.012, STEEL)
    # gallery machines: black threshing box (right), red machine (left), small wheels on top
    box("GalleryThresher", (2.6,0.3,4.55), (2.6,1.7,1.6), BLACK)
    box("GalleryThresherRoof", (2.6,0.3,5.42), (2.8,1.9,0.12), IRON)
    wheel("GalleryWheelA", (3.6,-0.75,5.62), 0.22, IRON, STEEL, axis='Y', spokes=6)
    wheel("GalleryWheelB", (2.0,-0.75,5.62), 0.18, IRON, STEEL, axis='Y', spokes=6)
    box("GalleryRedMachine", (-3.1,0.3,4.35), (2.2,1.5,1.15), RED_B)
    wheel("GalleryWheelC", (-3.4,-0.85,4.55), 0.42, IRON, WOOD_D, axis='Y', spokes=8)
    box("GalleryRedHopper", (-3.1,0.3,5.06), (1.2,0.9,0.30), IRON)
    # portable steam engine (ground, left-centre)
    cyl("Boiler", (-1.7,0.2,1.05), 0.42, 2.3, BLACK, rot=(0,math.radians(90),0), verts=22)
    cyl("BoilerBand", (-2.4,0.2,1.05), 0.435, 0.10, BRASS, rot=(0,math.radians(90),0), verts=22)
    cyl("ChimneyBase", (-2.65,0.2,1.62), 0.09, 0.35, IRON)
    box("Firebox", (-2.95,0.2,0.85), (0.55,0.8,1.3), IRON)
    wheel("EngineWheelL", (-2.5,-0.42,0.62), 0.62, RED_B, WOOD_D, axis='Y', spokes=10)
    wheel("EngineWheelR", (-1.1,-0.42,0.55), 0.55, RED_B, WOOD_D, axis='Y', spokes=10)
    wheel("EngineFlywheel", (-0.75,0.72,1.15), 0.52, IRON, STEEL, axis='Y', spokes=8)
    box("EngineFrame", (-1.7,-0.35,0.38), (2.5,0.12,0.14), IRON)
    # foreground machine (right): black body, sloped top, silver roller
    box("DrillBody", (3.1,0.5,0.72), (2.9,1.5,1.05), BLACK)
    box("DrillSlope", (2.55,0.5,1.30), (1.9,1.5,0.10), RED_B, rot=(0,0,math.radians(-14)))
    cyl("DrillRoller", (4.35,0.95,0.62), 0.14, 0.5, STEEL, rot=(math.radians(90),0,0), verts=16)
    box("DrillTail", (4.6,0.5,0.45), (0.5,1.3,0.5), IRON)
    # red cart/machine centre behind columns
    box("RedCart", (0.6,1.6,0.62), (1.9,1.1,0.85), RED_B)
    wheel("CartWheel", (0.0,2.2,0.55), 0.55, RED_B, WOOD_D, axis='Y', spokes=10)
    # small notice boards on column (blank)
    box("Notice1", (W/6,1.24,2.45), (0.34,0.03,0.44), WHITE)
    box("Notice2", (W/6,1.24,1.95), (0.34,0.03,0.44), WHITE)
    # visitors
    figure("Walker", (-3.6,-2.2,0), 1.76, coat=BLACK, hat='top')
    figure("Inspector1", (3.3,-1.9,0), 1.70, coat=BROWN, hat='bowler')
    figure("Inspector2", (4.25,-1.85,0), 1.78, coat=BLACK, hat='top')

# ================= FIG 38 — woodworking machinery 1850 =================
def build_fig38():
    box("Floor", (0,0,-0.03), (10,5.6,0.06), WOOD_L)
    # long planing bench (foreground left, running diagonally in view -> along X)
    for lx in (-3.4,-1.2,0.9):
        box(f"BenchLeg_{lx}", (lx,-0.7,0.42), (0.16,0.8,0.84), WOOD_D)
    box("BenchTop", (-1.25,-0.7,0.90), (4.6,1.0,0.10), WOOD)
    box("BenchRailLow", (-1.25,-1.05,0.22), (4.6,0.08,0.30), WOOD_D)
    box("BenchPlank", (-1.45,-0.7,1.00), (3.6,0.55,0.07), WOOD_L)
    box("BenchPlank2", (-1.0,-0.55,1.10), (2.6,0.4,0.06), WOOD_L)
    # planing machine (centre): tapered housing + big circular cutter disc
    box("MachineBase", (0.95,-0.55,0.30), (1.15,1.15,0.60), IRON)
    cone("MachineHousing", (0.95,-0.55,1.18), 0.62, 0.42, 0.85, IRON, verts=4)
    bpy.context.object.rotation_euler = (0,0,math.radians(45))
    cyl("CutterDisc", (0.32,-0.55,1.28), 0.42, 0.07, mat("disc_pale",(0.78,0.76,0.70),0.5,0.3), rot=(0,math.radians(90),0), verts=28)
    for i in range(3):
        a = i*math.radians(120)
        box(f"CutterSlot_{i}", (0.27,-0.55+math.sin(a)*0.2,1.28+math.cos(a)*0.2), (0.03,0.07,0.30), IRON, rot=(a,0,0))
    # top belt guard arch + belt to shaft on right
    torus("BeltGuard", (0.95,-0.55,1.86), 0.30, 0.045, IRON, rot=(0,math.radians(90),0))
    cyl("MainShaft", (2.6,-0.55,1.28), 0.06, 3.3, STEEL, rot=(0,math.radians(90),0))
    for px in (1.9,3.3,4.3):
        cyl(f"ShaftPulley_{px}", (px,-0.55,1.28), 0.19, 0.09, WOOD_D, rot=(0,math.radians(90),0), verts=18)
        box(f"ShaftPost_{px}", (px,-0.55,0.62), (0.12,0.3,1.24), WOOD_D)
    box("BeltRun1", (2.6,-0.38,1.02), (3.4,0.015,0.10), BROWN)
    box("BeltRun2", (2.6,-0.72,1.02), (3.4,0.015,0.10), BROWN)
    # operating lever (curved -> 3 segments) + small roller stand
    limb("Lever1", (1.50,-0.90,0.75), (1.75,-0.55,1.50), 0.032, WOOD_D)
    limb("Lever2", (1.75,-0.55,1.50), (1.90,-0.40,2.05), 0.032, WOOD_D)
    box("RollerStand", (1.42,-0.1,0.42), (0.5,0.45,0.84), IRON)
    cyl("Roller", (1.42,-0.1,0.90), 0.09, 0.4, STEEL, rot=(math.radians(90),0,0), verts=14)
    # timber stack right + loose pieces at machine base
    for i in range(4):
        box(f"PlankStack_{i}", (3.6,1.15,0.10+i*0.14), (2.6,0.85,0.11), WOOD_L if i%2 else WOOD)
    for i in range(3):
        box(f"Offcut_{i}", (0.5+i*0.3,-1.55,0.05), (0.4,0.18,0.08), WOOD_L, rot=(0,0,math.radians(i*25)))
    # background bench (left rear, no figures - workers below are the 3 counted)
    box("BackBench", (-3.3,1.6,0.75), (3.0,0.6,0.08), WOOD)
    for lx in (-4.5,-2.1):
        box(f"BackBenchLeg_{lx}", (lx,1.6,0.36), (0.12,0.5,0.72), WOOD_D)
    for i in range(3):
        box(f"BackPlank_{i}", (-3.3,1.55,0.86+i*0.09), (2.9,0.42,0.07), WOOD_L)
    # 3 stylised workers: feeder at bench, lever operator, plank handler right
    figure("Feeder", (-0.55,-1.55,0), 1.72, coat=GREY_C, hat='cap', apron=True, cap_mat=BROWN)
    figure("LeverOperator", (2.10,-1.25,0), 1.70, coat=BROWN, hat='cap', apron=False, cap_mat=BLACK)
    figure("PlankHandler", (3.9,-1.05,0), 1.74, coat=GREY_C, hat='cap', cap_mat=BROWN)

BUILDERS = {
 'scan-fig29-platt-cotton-machines': build_fig29,
 'scan-fig30-delarue-envelope-machine': build_fig30,
 'scan-fig48-garrett-agricultural-machinery': build_fig48,
 'scan-fig38-woodworking-machinery-1850': build_fig38,
}
CAMS = {
 'scan-fig29-platt-cotton-machines': ((-6.8,-7.2,3.1),(0.4,0.4,1.1)),
 'scan-fig30-delarue-envelope-machine': ((-5.6,-6.4,2.7),(0.1,0.2,1.0)),
 'scan-fig48-garrett-agricultural-machinery': ((-6.5,-15.5,4.6),(0,0,2.0)),
 'scan-fig38-woodworking-machinery-1850': ((1.6,-7.4,2.3),(0.1,0,1.0)),
}
BUILDERS[SLUG]()

# ground (render only, excluded from GLB)
bpy.ops.mesh.primitive_plane_add(size=80, location=(0,0,-0.065))
ground = bpy.context.object; ground.name = "Ground_RENDERONLY"
ground.data.materials.append(FLOOR)

# lights + camera
def look_at(ob, target):
    ob.rotation_euler = (Vector(target)-Vector(ob.location)).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='SUN', location=(6,-6,10))
sun = bpy.context.object; sun.data.energy = 3.0; look_at(sun, (0,0,0))
bpy.ops.object.light_add(type='AREA', location=(-5,-4,7))
area = bpy.context.object; area.data.energy = 900; area.data.shape='DISK'; area.data.size = 6; look_at(area, (0,0,1))
cam_loc, cam_tgt = CAMS[SLUG]
bpy.ops.object.camera_add(location=cam_loc)
cam = bpy.context.object; scene.camera = cam; look_at(cam, cam_tgt); cam.data.lens = 42

# apply transforms on model meshes
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active = MODEL_OBJS[0]
for ob in MODEL_OBJS:
    ob.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')

tris = 0
for ob in MODEL_OBJS:
    for p in ob.data.polygons: tris += len(p.vertices)-2
print("TRIS", tris)
print("OBJECTS", len(MODEL_OBJS))

scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.render.render(write_still=True)

# GLB: model objects only
bpy.ops.object.select_all(action='DESELECT')
for ob in MODEL_OBJS: ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB', use_selection=True)
bpy.ops.object.select_all(action='DESELECT')

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
print("DONE", SLUG)
