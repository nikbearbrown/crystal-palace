#!/usr/bin/env python3
"""
Build script — scan-fig28-tunis-court
The Tunis Court, Great Exhibition 1851 (catalogue fig. 28): a composed
section, ~7 m wide, of one court bay — arched display alcoves with hats,
vessels and folded textiles, a draped carpet swag overhead, a glazed
display cabinet, two standing visitors, and in the foreground a draped
animal hide and leaning lutes.

Source: B/W engraving (see refs/REFERENCES.md). Geometric extraction only;
no repaired areas. Colours are INTERPRETIVE (source is monochrome) — a
muted period palette of deep red, indigo, ochre and cream.
Scale is ESTIMATED from the two standing figures, taken as ~1.70 m tall.
The Crystal Palace roof structure visible in the engraving is background
only and is deliberately NOT modelled.

Re-runnable:  blender -b --python build_scan_fig28_tunis_court.py
Produces scan-fig28-tunis-court.blend, .glb and preview.png beside the
script. Metres throughout. Origin at base centre (floor centre, z=0).
"""
import bpy, os, math, random
from mathutils import Vector

BASE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(1851)

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
model = bpy.data.collections.new("Model"); scene.collection.children.link(model)
setup = bpy.data.collections.new("RenderSetup"); scene.collection.children.link(setup)

# ---------------------------------------------------------------- materials
# FIX ROUND 1 (palette): colour values below are specified in sRGB (the
# intuitive paint-chip space) and converted to linear here. The original
# build passed sRGB-looking numbers straight into the linear Base Color
# socket, which lifted every colour ~a gamma step — deep red rendered as
# pastel pink, indigo as sky blue, hide brown as beige. Values are also
# deepened/desaturated throughout so the court reads as rich bazaar
# textiles, not toy blocks. Colours remain INTERPRETIVE (B/W source).
def _srgb2lin(c):
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def mat(name, rgb, rough=0.85, metal=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*(_srgb2lin(c) for c in rgb), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'BLENDED'
    return m

M = {
 'timber':  mat("TimberDark", (0.23,0.14,0.07), .8),
 'timberL': mat("TimberLight", (0.38,0.25,0.12), .8),
 'plaster': mat("AlcoveBack", (0.60,0.53,0.41), .95),
 'fascia':  mat("FasciaCream", (0.64,0.55,0.40), .9),
 'floor':   mat("FloorBoards", (0.36,0.25,0.13), .9),
 'red':     mat("TextileDeepRed", (0.44,0.10,0.08), .95),
 'reddark': mat("TextileMaroon", (0.27,0.06,0.05), .95),
 'red2':    mat("TextileRed2", (0.50,0.19,0.12), .95),
 'indigo':  mat("TextileIndigo", (0.09,0.13,0.29), .95),
 'ochre':   mat("TextileOchre", (0.56,0.37,0.12), .95),
 'cream':   mat("TextileCream", (0.70,0.60,0.43), .95),
 'stripe':  mat("CounterStripe", (0.11,0.11,0.19), .95),
 'brass':   mat("Brass", (0.50,0.36,0.14), .35, .85),
 'copper':  mat("Copper", (0.47,0.24,0.12), .4, .7),
 'pottery': mat("Pottery", (0.44,0.26,0.14), .8),
 'pottery2':mat("PotteryPale", (0.57,0.43,0.27), .8),
 'straw':   mat("StrawHat", (0.61,0.47,0.24), .95),
 'dark':    mat("CoatDark", (0.07,0.06,0.07), .9),
 'dark2':   mat("CoatBrown", (0.16,0.11,0.07), .9),
 'skin':    mat("SkinTone", (0.57,0.40,0.27), .8),
 'hide':    mat("AnimalHide", (0.30,0.19,0.10), .95),
 'hideL':   mat("HidePatch", (0.20,0.12,0.06), .95),
 'glass':   mat("Glass", (0.55,0.62,0.62), .08, 0.0, 0.22),
 'iron':    mat("IronDark", (0.06,0.06,0.07), .5, .6),
 'lute':    mat("LuteWood", (0.45,0.28,0.12), .6),
}

# ----------------------------------------------------------------- helpers
def link(obj, material=None):
    model.objects.link(obj)
    if material: obj.data.materials.append(material)
    return obj

def apply_tf(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.select_set(False)

def box(name, centre, size, material, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=centre, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.dimensions = size; apply_tf(o)
    return link(o, material)

def cyl(name, centre, radius, depth, material, rot=(0,0,0), verts=14, r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=radius,
        radius2=radius if r2 is None else r2, depth=depth,
        location=centre, rotation=rot)
    o = bpy.context.active_object; o.name = name; apply_tf(o)
    return link(o, material)

def sphere(name, centre, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, location=centre)
    o = bpy.context.active_object; o.name = name; o.scale = scale; apply_tf(o)
    return link(o, material)

def mesh_obj(name, verts, faces, material, mat_idx=None):
    me = bpy.data.meshes.new(name+"Mesh"); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me)
    if mat_idx:
        for f, mi in zip(me.polygons, mat_idx): f.material_index = mi
    return link(o, material)

def lathe(name, centre, profile, material, segs=14):
    """profile: list of (r, z) bottom->top, revolved about Z at centre."""
    cx, cy, cz = centre; verts = []; faces = []
    for r, z in profile:
        for i in range(segs):
            a = 2*math.pi*i/segs
            verts.append((cx+r*math.cos(a), cy+r*math.sin(a), cz+z))
    n = len(profile)
    for j in range(n-1):
        for i in range(segs):
            a=j*segs+i; b=j*segs+(i+1)%segs; c=b+segs; d=a+segs
            faces.append((a,b,c,d))
    if profile[0][0] > 0.001:  # bottom cap fan via centre vert
        verts.append((cx,cy,cz+profile[0][1])); ci=len(verts)-1
        for i in range(segs): faces.append((ci,(i+1)%segs,i))
    if profile[-1][0] > 0.001:
        verts.append((cx,cy,cz+profile[-1][1])); ci=len(verts)-1
        base=(n-1)*segs
        for i in range(segs): faces.append((ci, base+i, base+(i+1)%segs))
    return mesh_obj(name, verts, faces, material)

def disc_facing(name, centre, r, thick, material):
    return cyl(name, centre, r, thick, material, rot=(math.radians(90),0,0), verts=20)

def arc_band(name, cx, cy, z_base, r_in, band, thick, material):
    """Half-round arch band in the XZ plane, spanning pi..0."""
    segs=14; verts=[]; faces=[]
    for r in (r_in, r_in+band):
        for dy in (-thick/2, thick/2):
            for i in range(segs+1):
                a = math.pi - math.pi*i/segs
                verts.append((cx+r*math.cos(a), cy+dy, z_base+r*math.sin(a)))
    # vertex index: r(2) x dy(2) x i(segs+1)
    S=segs+1
    def idx(r,d,i): return r*2*S + d*S + i
    for i in range(segs):
        faces.append((idx(0,0,i), idx(0,0,i+1), idx(0,1,i+1), idx(0,1,i)))  # inner
        faces.append((idx(1,0,i), idx(1,1,i), idx(1,1,i+1), idx(1,0,i+1)))  # outer
        faces.append((idx(0,1,i), idx(0,1,i+1), idx(1,1,i+1), idx(1,1,i)))  # front
        faces.append((idx(0,0,i), idx(1,0,i), idx(1,0,i+1), idx(0,0,i+1)))  # back
    return mesh_obj(name, verts, faces, material)

def grid_surface(name, nu, nv, fn, materials):
    """fn(u,v)->(x,y,z,mat_index). materials: list."""
    verts=[]; faces=[]; midx=[]
    for j in range(nv):
        for i in range(nu):
            x,y,z,_ = fn(i/(nu-1), j/(nv-1)); verts.append((x,y,z))
    for j in range(nv-1):
        for i in range(nu-1):
            a=j*nu+i; faces.append((a,a+1,a+1+nu,a+nu))
            midx.append(fn((i+.5)/(nu-1),(j+.5)/(nv-1))[3])
    o = mesh_obj(name, verts, faces, materials[0], midx)
    for p in o.data.polygons: p.use_smooth = True
    for m in materials[1:]: o.data.materials.append(m)
    # solidify a touch for silhouette
    mod = o.modifiers.new("solid", 'SOLIDIFY'); mod.thickness = 0.015
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.modifier_apply(modifier="solid"); o.select_set(False)
    return o

def figure(name, x, y, coat, rotz=0.0, seated=False):
    """Stylised simplified figure, ~1.70 m standing. No likeness."""
    g = []
    ca, sa = math.cos(rotz), math.sin(rotz)
    def L(dx,dy): return (x+dx*ca-dy*sa, y+dx*sa+dy*ca)
    if not seated:
        # FIX ROUND 1 (figures): period silhouette, not a bare capsule —
        # trouser legs below the knee, a long coat whose skirt flares from
        # the waist to the knee, a tapered torso widening to the shoulders.
        for s in (-1,1):
            px,py = L(0.09*s,0)
            g.append(cyl(f"{name}Leg{s}", (px,py,0.30), 0.052, 0.60, M['dark'], verts=10))
            px,py = L(0.09*s,0.03)
            g.append(box(f"{name}Shoe{s}", (px,py,0.03), (0.09,0.24,0.06), M['iron']))
        g.append(cyl(f"{name}CoatSkirt", (x,y,0.79), 0.205, 0.50, coat, verts=12, r2=0.125))
        g.append(cyl(f"{name}Coat", (x,y,1.27), 0.125, 0.48, coat, verts=12, r2=0.15))
        g.append(sphere(f"{name}Shoulders", (x,y,1.50), (0.155,0.105,0.085), coat))
        for s in (-1,1):
            px,py = L(0.20*s,-0.02)
            g.append(cyl(f"{name}Arm{s}", (px,py,1.16), 0.042, 0.64, coat,
                         rot=(math.radians(8*s), math.radians(10*s), 0), verts=8))
    else:
        px,py = L(0,0.12)
        g.append(box(f"{name}Thighs", (px,py,0.62), (0.34,0.30,0.13), M['dark']))
        for s in (-1,1):
            px,py = L(0.09*s,0.26)
            g.append(cyl(f"{name}Shin{s}", (px,py,0.30), 0.05, 0.55, M['dark'], verts=8))
        g.append(cyl(f"{name}Coat", (x,y,1.02), 0.155, 0.62, coat, verts=12, r2=0.11))
        for s in (-1,1):
            px,py = L(0.19*s,0.05)
            g.append(cyl(f"{name}Arm{s}", (px,py,0.98), 0.038, 0.5, coat,
                         rot=(math.radians(-35), math.radians(8*s), 0), verts=8))
    hz = 1.68 if not seated else 1.46
    g.append(cyl(f"{name}Neck", (x,y,hz-0.13), 0.045, 0.10, M['skin'], verts=8))
    g.append(sphere(f"{name}Head", (x,y,hz), (0.082,0.088,0.102), M['skin']))
    # FIX ROUND 1: readable hat form — flat brim disc + raised crown —
    # instead of the old flat cap puck that read as a stacked block.
    g.append(cyl(f"{name}HatBrim", (x,y,hz+0.085), 0.125, 0.018, M['dark'], verts=14))
    g.append(cyl(f"{name}HatCrown", (x,y,hz+0.13), 0.082, 0.09, M['dark'], verts=12, r2=0.088))
    return g

# ================================================================== FLOOR
box("Floor", (0,0.3,-0.03), (7.0,4.8,0.06), M['floor'])
# plank grooves: thin dark strips across the floor
for i in range(9):
    box(f"PlankGroove{i}", (-3.2+i*0.8, 0.3, 0.006), (0.03,4.8,0.012), M['timber'])
# patterned carpet runner (foreground centre)
box("RunnerBase", (-0.4,1.35,0.012), (4.6,1.7,0.024), M['red'])
for i, cm in enumerate((M['cream'], M['indigo'], M['ochre'], M['indigo'], M['cream'])):
    box(f"RunnerStripe{i}", (-0.4, 0.68+i*0.34, 0.026), (4.6,0.10,0.006), cm)

# ============================================================ ALCOVE WALL
# Alcoves along the back (y=-1.55 back wall), openings facing +Y.
# Three bays: centres x=-2.45, -0.80, +0.85 ; width 1.55, springing z=2.05, r=0.775
ALC_X = [-2.45, -0.80, 0.85]; ALC_W = 1.55; BACK_Y = -1.55; FRONT_Y = -0.95
box("BackWall", (-0.8,-1.60,1.45), (5.3,0.10,2.90), M['plaster'])
# piers between / beside alcoves
for i, px in enumerate([-3.32,-1.625,0.025,1.70]):
    box(f"Pier{i}", (px,-1.02,1.28), (0.20,0.24,2.56), M['fascia'])
# fascia beam above arches
box("FasciaBeam", (-0.8,-1.02,3.02), (5.42,0.26,0.42), M['fascia'])
box("FasciaTrim", (-0.8,-0.90,2.83), (5.42,0.06,0.06), M['red'])
for i, cx in enumerate(ALC_X):
    arc_band(f"Arch{i}", cx, -1.02, 2.05, 0.68, 0.20, 0.26, M['fascia'])
    # alcove ceiling / soffit
    box(f"AlcoveCeil{i}", (cx,-1.28,2.88), (1.55,0.62,0.08), M['timberL'])
    # side cheeks
    for s in (-1,1):
        box(f"AlcoveCheek{i}_{s}", (cx+s*0.72,-1.28,1.30), (0.10,0.60,2.60), M['plaster'])

# --------------------------------------------- Alcove 1: hats + vessels
cx = ALC_X[0]
# straw hats: large discs with raised crowns, two rows on the back wall
hat_pos = [(-0.55,2.45),(-0.18,2.52),(0.20,2.45),(0.55,2.52)]
for i,(dx,z) in enumerate(hat_pos):
    disc_facing(f"Hat{i}", (cx+dx,-1.50,z), 0.21, 0.035, M['straw'])
    cyl(f"HatCrown{i}", (cx+dx,-1.46,z), 0.085, 0.07, M['straw'],
        rot=(math.radians(90),0,0), verts=12)
# FIX ROUND 1: second staggered row of smaller hats — alcove 1 in the
# engraving is packed with headwear; the single row read sparse.
for i,(dx,z) in enumerate([(-0.38,2.17),(0.02,2.21),(0.42,2.17)]):
    disc_facing(f"HatExtra{i}", (cx+dx,-1.50,z), 0.165, 0.03, M['straw'])
    cyl(f"HatExtraCrown{i}", (cx+dx,-1.465,z), 0.07, 0.06, M['straw'],
        rot=(math.radians(90),0,0), verts=12)
# decorative fans / plates (scalloped look: flattened cones) mid-left
for i,(dx,z) in enumerate([(-0.55,1.95),(-0.28,2.0),(-0.52,1.62),(-0.25,1.66)]):
    cyl(f"Fan{i}", (cx+dx,-1.51,z), 0.16, 0.03, M['ochre'] if i%2 else M['red2'],
        rot=(math.radians(90),0,0), verts=9)
# small plates in rows, right side
for r in range(3):
    for c in range(4):
        disc_facing(f"Plate{r}_{c}", (cx+0.08+c*0.17, -1.52, 1.98-r*0.22), 0.075, 0.02,
                    M['pottery2'] if (r+c)%2 else M['copper'])
# counter with dark vertically striped front
box("Counter1Top", (cx,-1.18,0.86), (1.55,0.62,0.06), M['timberL'])
box("Counter1Body", (cx,-1.18,0.42), (1.55,0.62,0.82), M['red'])
for i in range(11):
    box(f"CounterStripe{i}", (cx-0.70+i*0.14, -0.865, 0.42), (0.055,0.015,0.82),
        M['stripe'] if i%2 else M['ochre'])
# vessels on the counter (simplified lathe profiles)
lathe("EwerTall", (cx-0.58,-1.25,0.89),
      [(0.001,0),(0.05,0.01),(0.075,0.10),(0.045,0.24),(0.03,0.32),(0.045,0.38),(0.02,0.42),(0.001,0.43)], M['brass'])
cyl("EwerSpout", (cx-0.50,-1.25,1.20), 0.016, 0.20, M['brass'],
    rot=(0,math.radians(-55),0), verts=8, r2=0.008)
lathe("BottleA", (cx-0.34,-1.10,0.89),
      [(0.001,0),(0.055,0.01),(0.065,0.12),(0.025,0.26),(0.022,0.34),(0.035,0.37),(0.001,0.38)], M['copper'])
lathe("JarConicalLid", (cx-0.05,-1.28,0.89),
      [(0.001,0),(0.075,0.01),(0.085,0.14),(0.06,0.22),(0.001,0.23)], M['pottery'])
cyl("JarLid", (cx-0.05,-1.28,1.19), 0.005, 0.13, M['pottery2'], verts=10, r2=0.055)
lathe("BowlOnCounter", (cx+0.28,-1.12,0.89),
      [(0.001,0),(0.05,0.01),(0.11,0.05),(0.13,0.10),(0.125,0.11)], M['brass'])
lathe("PitcherB", (cx+0.52,-1.30,0.89),
      [(0.001,0),(0.06,0.01),(0.08,0.12),(0.05,0.26),(0.065,0.32),(0.001,0.34)], M['pottery2'])
lathe("BottleB", (cx+0.66,-1.08,0.89),
      [(0.001,0),(0.045,0.01),(0.05,0.10),(0.02,0.20),(0.018,0.27),(0.001,0.28)], M['brass'])
lathe("SmallJar", (cx+0.16,-1.34,0.89),
      [(0.001,0),(0.05,0.01),(0.055,0.09),(0.035,0.15),(0.001,0.16)], M['pottery'])
# FIX ROUND 1: three more small counter vessels in the gaps (front/back rows)
lathe("BottleC", (cx-0.69,-1.02,0.89),
      [(0.001,0),(0.04,0.01),(0.048,0.09),(0.02,0.18),(0.018,0.24),(0.001,0.25)], M['copper'])
lathe("SmallJarB", (cx+0.09,-1.04,0.89),
      [(0.001,0),(0.05,0.01),(0.058,0.08),(0.038,0.14),(0.001,0.15)], M['pottery'])
lathe("CupVessel", (cx+0.38,-1.40,0.89),
      [(0.001,0),(0.045,0.01),(0.06,0.07),(0.055,0.12),(0.001,0.13)], M['brass'])

# --------------------------------------- Alcove 2: folded textiles stack
cx = ALC_X[1]
# hanging cloths behind
for i,(dx,cm,ln) in enumerate([(-0.5,M['indigo'],1.5),(-0.17,M['cream'],1.65),
                               (0.17,M['red'],1.45),(0.5,M['ochre'],1.6)]):
    box(f"HangCloth2_{i}", (cx+dx,-1.48,2.85-ln/2), (0.30,0.03,ln), cm)
box("HangRod2", (cx,-1.48,2.88), (1.4,0.05,0.05), M['timber'])
# stacked folded textiles on a shelf/counter, patterned border strips
box("Counter2", (cx,-1.20,0.40), (1.55,0.55,0.80), M['indigo'])
for i in range(7):
    box(f"Counter2Band{i}", (cx-0.66+i*0.22, -0.915, 0.40), (0.10,0.015,0.80), M['ochre'])
stack_cols = [M['cream'], M['red2'], M['ochre'], M['indigo'], M['cream'], M['red']]
for i, cm in enumerate(stack_cols):
    zz = 0.86 + i*0.115
    box(f"FoldStack{i}", (cx-0.28,-1.22,zz), (0.85,0.55,0.105), cm)
    box(f"FoldStackBorder{i}", (cx-0.28,-0.935,zz), (0.85,0.012,0.035),
        M['indigo'] if i%2 else M['red'])
    box(f"FoldPile{i}", (cx+0.48,-1.22,0.86+i*0.09 if i<4 else 0.86), (0.42,0.5,0.085), cm)

# --------------------------------------- Alcove 3 (partial): hanging fabrics
cx = ALC_X[2]
for i,(dx,cm,ln) in enumerate([(-0.48,M['red'],1.7),(-0.15,M['cream'],1.55),
                               (0.18,M['indigo'],1.75),(0.5,M['cream'],1.5)]):
    # slight wave: two stacked segments, lower one nudged forward
    box(f"HangCloth3_{i}a", (cx+dx,-1.48,2.85-ln*0.28), (0.30,0.03,ln*0.56), cm)
    box(f"HangCloth3_{i}b", (cx+dx,-1.44,2.85-ln*0.78), (0.30,0.03,ln*0.44),
        cm, rot=(math.radians(4),0,0))
box("HangRod3", (cx,-1.48,2.88), (1.4,0.05,0.05), M['timber'])
box("Counter3", (cx,-1.20,0.38), (1.55,0.55,0.76), M['red'])
for i, cm in enumerate(stack_cols[:4]):
    box(f"Fold3_{i}", (cx,-1.22,0.82+i*0.11), (1.05,0.5,0.10), cm)
# seated figure among the textiles (in alcove 3, on the counter edge)
figure("SeatedFigure", cx+0.15, -1.02, M['dark2'], rotz=math.radians(-12), seated=True)
# NOTE seated figure base sits at counter top via leg/thigh z offsets in helper
# (its feet rest near z=0.03 relative — visually seated at the alcove front)

# ==================================================== HANGING CARPETS (top)
# large carpets draped over the fascia, top left — as in the engraving
for i,(hx,cm,bm,w) in enumerate([(-2.6,M['red'],M['cream'],1.5),
                                 (-1.05,M['indigo'],M['ochre'],1.4),
                                 (0.35,M['ochre'],M['red'],1.2)]):
    box(f"TopCarpet{i}", (hx,-0.82,3.85), (w,0.04,1.25), cm, rot=(math.radians(6),0,0))
    box(f"TopCarpetBorder{i}", (hx,-0.795,3.85), (w-0.24,0.045,1.0), bm,
        rot=(math.radians(6),0,0))
    box(f"TopCarpetFold{i}", (hx,-0.88,3.20), (w,0.05,0.16), cm)

# ==================================================== DRAPED CARPET SWAG
# catenary swag across the upper right, patterned border bands along edges
def swag_fn(u,v):
    x = 0.9 + u*3.4
    sag = math.sin(u*math.pi)          # 0 at ends, 1 mid
    z = 4.05 - sag*0.95 - v*0.95 + sag*v*0.25
    y = 0.15 - v*0.55 + sag*0.10
    mi = 0
    if v < 0.10 or v > 0.90: mi = 1     # border bands
    elif u < 0.05 or u > 0.95: mi = 1
    return (x,y,z,mi)
grid_surface("CarpetSwag", 20, 8, swag_fn, [M['red'], M['reddark']])
# hanging cords at swag ends
for sx in (0.95, 4.25):
    cyl(f"SwagCord{sx}", (sx,0.05,4.55), 0.012, 1.0, M['timber'], verts=6)

# ==================================================== GLAZED CABINET (right)
GX, GY = 2.95, -0.55
box("CabinetBase", (GX,GY,0.10), (1.15,0.55,0.20), M['timber'])
box("CabinetTop", (GX,GY,2.52), (1.20,0.60,0.10), M['timber'])
for sx in (-1,1):
    for sy in (-1,1):
        box(f"CabPost{sx}_{sy}", (GX+sx*0.55, GY+sy*0.25, 1.31), (0.06,0.06,2.32), M['timber'])
for i in range(3):  # shelves + hanging goods inside
    zz = 0.65 + i*0.62
    box(f"CabShelf{i}", (GX,GY,zz), (1.05,0.48,0.03), M['timberL'])
    for j, cm in enumerate((M['red'], M['cream'], M['indigo'])):
        box(f"CabGoods{i}_{j}", (GX-0.32+j*0.32, GY, zz+0.26), (0.24,0.30,0.44), cm)
# glass panes (front + side)
box("CabGlassFront", (GX,GY+0.285,1.31), (1.08,0.015,2.25), M['glass'])
box("CabGlassSide", (GX-0.585,GY,1.31), (0.015,0.50,2.25), M['glass'])
# mullion bars on the front glass
for i in range(3):
    box(f"CabMullion{i}", (GX-0.36+i*0.36, GY+0.29, 1.31), (0.03,0.02,2.25), M['timber'])
box("CabMullionH", (GX,GY+0.29,1.31), (1.08,0.02,0.03), M['timber'])
# patterned panel wall behind/right of cabinet (square-motif panels)
box("PanelWall", (3.62,0.55,1.25), (0.08,1.6,2.5), M['plaster'], rot=(0,0,math.radians(90-90)))
for r in range(3):
    for c in range(2):
        box(f"PanelMotif{r}_{c}", (3.57,0.18+c*0.72,0.55+r*0.72), (0.03,0.52,0.52),
            M['red'] if (r+c)%2 else M['indigo'])

# ============================================================ FIGURES
figure("VisitorA", 1.75, 0.85, M['dark'], rotz=math.radians(-25))
figure("VisitorB", 2.18, 0.95, M['dark2'], rotz=math.radians(160))

# ============================================== FOREGROUND: ANIMAL HIDE
# low support the hide is draped over
box("HideSupport", (2.75,1.95,0.24), (0.85,0.65,0.48), M['timber'])
def hide_fn(u,v):
    # u: along the hide, tail (on floor, pointing to centre-left) -> head end
    # v: across its width, which tapers toward the tail
    x = 0.55 + u*2.85
    taper = 0.35 + 0.65*u
    y = 1.55 + (v-0.5)*1.05*taper + u*0.55
    # FIX ROUND 1: smooth drape — cosine/smoothstep interpolation between
    # control heights instead of the old piecewise-linear profile, whose
    # sharp kinks read as folded card. Flat on the floor, rising over the
    # support (peak ~u=0.82), then falling away at the head end.
    keys = [(0.0,0.035),(0.55,0.075),(0.82,0.66),(0.93,0.585),(1.0,0.17)]
    z = keys[-1][1]
    for (u0,z0),(u1,z1) in zip(keys, keys[1:]):
        if u <= u1:
            t = (u-u0)/(u1-u0); t = t*t*(3-2*t)
            z = z0 + (z1-z0)*t; break
    z += 0.022*math.sin(v*math.pi)         # slight crown across the width
    mi = 1 if (v<0.08 or v>0.92) else 0
    return (x,y,z,mi)
grid_surface("AnimalHide", 26, 14, hide_fn, [M['hide'], M['hideL']])
# FIX ROUND 1: the old raised "fan flap" cone at the head end is removed.
# In its place, a low rolled fold lying across the hide's width at the
# crest — reads as the hide's folded-over edge, in the darker hide tone.
cyl("HideFoldedEdge", (3.13,2.05,0.625), 0.05, 0.90, M['hideL'],
    rot=(math.radians(90),0,0), verts=12)

# ============================================== FOREGROUND LEFT: LUTES
def lute(name, x, y, lean, rotz):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, location=(x,y,0.42))
    o = bpy.context.active_object; o.name = name+"Body"
    o.scale = (0.16,0.055,0.24); apply_tf(o); link(o, M['lute'])
    ca = math.radians(lean)
    nx, ny = x+0.02, y-0.02
    cyl(name+"Neck", (nx, ny+0.02, 0.42+0.48), 0.022, 0.62, M['timber'],
        rot=(math.radians(lean),0,rotz), verts=8)
    cyl(name+"Soundhole", (x, y-0.058, 0.42), 0.045, 0.012, M['dark'],
        rot=(math.radians(90),0,0), verts=12)
lute("LuteA", -3.05, -0.55, 18, 0)
lute("LuteB", -2.78, -0.50, 24, 0)
lute("LuteC", -3.28, -0.48, 12, 0)
# shallow metal bowl on the floor beside the lutes
lathe("FloorBowl", (-2.55,0.05,0.01),
      [(0.001,0),(0.07,0.01),(0.15,0.045),(0.17,0.09),(0.165,0.10)], M['brass'])

# ------------------------------------------- mirror to match the engraving
# Built with the hats alcove at -X; viewed from the front that places it on
# the wrong side versus the engraving (hats LEFT, cabinet + hide RIGHT).
# Bake all transforms, mirror the geometry in X and flip the faces back.
from mathutils import Matrix
for o in list(model.objects):
    if o.type != 'MESH': continue
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    o.select_set(False)
    o.data.transform(Matrix.Diagonal((-1.0, 1.0, 1.0, 1.0)))
    o.data.flip_normals()
    o.data.update()

# ------------------------------------------------------------------ render
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960; scene.render.resolution_y = 640
scene.render.filepath = os.path.join(BASE, "preview.png")
world = bpy.data.worlds.new("W"); scene.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5,0.5,0.5,1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

def look_at(obj, target):
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (Vector(target)-obj.location).to_track_quat('-Z','Y')

bpy.ops.object.camera_add(location=(-5.4,6.2,3.0))
cam = bpy.context.active_object; cam.data.lens = 38
look_at(cam, (0.6,-0.7,1.10))
# move camera into setup collection
scene.collection.objects.unlink(cam); setup.objects.link(cam)
scene.camera = cam
bpy.ops.object.light_add(type='SUN', location=(4,5,8))
sun = bpy.context.active_object; sun.data.energy = 2.0; sun.data.angle = 0.6
look_at(sun, (0,0,0.8)); scene.collection.objects.unlink(sun); setup.objects.link(sun)
bpy.ops.object.light_add(type='AREA', location=(-3,3,5))
fill = bpy.context.active_object; fill.data.energy = 220; fill.data.size = 4
look_at(fill, (0,0,1)); scene.collection.objects.unlink(fill); setup.objects.link(fill)

# exclude setup from GLB by exporting only Model later; save + render
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BASE, "scan-fig28-tunis-court.blend"))
bpy.ops.render.render(write_still=True)

# GLB: select model collection only
bpy.ops.object.select_all(action='DESELECT')
for o in model.objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(BASE, "scan-fig28-tunis-court.glb"),
                          export_format='GLB', use_selection=True)

tris = sum(len(o.data.polygons) and sum(p.loop_total-2 for p in o.data.polygons)
           for o in model.objects if o.type=='MESH')
print(f"TRIANGLES: {tris}")
print(f"OBJECTS: {len(model.objects)}")
