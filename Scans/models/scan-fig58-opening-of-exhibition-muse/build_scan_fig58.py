# Build script — scan-fig58-opening-of-exhibition (Muse version)
# Reference: fig-58_opening-great-exhibition-hc-selous-1851.png (H. C. Selous, 1851-2)
# The opening ceremony, 1 May 1851: royal dais with crimson-and-gold canopy at the
# centre of the transept, royal party and officials, crowd in the nave, Osler crystal
# fountain hinted at right, crystal fountain + transept arch as backdrop.
# All figures stylised — NO likenesses. Backdrop architecture simplified, flagged.
import bpy, math, os, random

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig58-opening-of-exhibition"
random.seed(58)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, rgb, rough=0.85, metallic=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m

FLOOR  = mat("Floor", (0.62, 0.58, 0.52))
CARPET = mat("CarpetRed", (0.48, 0.10, 0.12))
CRIMSON = mat("Crimson", (0.45, 0.08, 0.11))
GOLD   = mat("Gold", (0.72, 0.55, 0.22), 0.45, 0.55)
ARCH   = mat("ArchPale", (0.78, 0.78, 0.74))
GLASS  = mat("GlassPale", (0.75, 0.83, 0.85), 0.25)
WHITE  = mat("White", (0.88, 0.86, 0.82))
BLUE   = mat("SashBlue", (0.15, 0.25, 0.55))
SKIN   = mat("Skin", (0.80, 0.62, 0.50))
DARK   = mat("Dark", (0.16, 0.15, 0.14))
COATS = [mat("CoatA", (0.30, 0.24, 0.20)), mat("CoatB", (0.22, 0.20, 0.22)), mat("CoatC", (0.38, 0.30, 0.22))]
DRESS = [mat("DressA", (0.55, 0.42, 0.45)), mat("DressB", (0.40, 0.45, 0.55)), mat("DressC", (0.60, 0.52, 0.38)),
         mat("DressD", (0.35, 0.40, 0.33))]

def box(name, loc, dims, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    return o

def cyl(name, loc, r1, r2, depth, material, verts=12, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def sph(name, loc, scale, material, seg=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    for p in o.data.polygons: p.use_smooth = True
    return o

# ----- stylised figures (shared low-poly set) -----
FIG = {}
def build_prototypes():
    # MAN: legs+coat+arms+head+tophat merged into one mesh
    parts = []
    def add(op, **kw):
        op(**kw); parts.append(bpy.context.object)
    add(bpy.ops.mesh.primitive_cube_add, location=(-0.075, 0, 0.40)); parts[-1].dimensions = (0.085, 0.09, 0.80)
    add(bpy.ops.mesh.primitive_cube_add, location=(0.075, 0, 0.40)); parts[-1].dimensions = (0.085, 0.09, 0.80)
    add(bpy.ops.mesh.primitive_cube_add, location=(0, 0, 1.10)); parts[-1].dimensions = (0.40, 0.24, 0.62)
    add(bpy.ops.mesh.primitive_cube_add, location=(-0.245, 0, 1.12)); parts[-1].dimensions = (0.075, 0.075, 0.55)
    add(bpy.ops.mesh.primitive_cube_add, location=(0.245, 0, 1.12)); parts[-1].dimensions = (0.075, 0.075, 0.55)
    add(bpy.ops.mesh.primitive_uv_sphere_add, segments=10, ring_count=6, location=(0, 0, 1.585))
    parts[-1].scale = (0.082, 0.086, 0.10)
    add(bpy.ops.mesh.primitive_cone_add, vertices=12, radius1=0.115, radius2=0.115, depth=0.014, location=(0, 0, 1.665))
    add(bpy.ops.mesh.primitive_cone_add, vertices=12, radius1=0.080, radius2=0.087, depth=0.16, location=(0, 0, 1.75))
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.join()
    FIG['man'] = bpy.context.object; FIG['man'].name = "ProtoMan"
    # WOMAN: crinoline cone + bodice + head + bonnet
    parts = []
    add(bpy.ops.mesh.primitive_cone_add, vertices=12, radius1=0.34, radius2=0.15, depth=0.86, location=(0, 0, 0.43))
    add(bpy.ops.mesh.primitive_cube_add, location=(0, 0, 1.04)); parts[-1].dimensions = (0.30, 0.20, 0.36)
    add(bpy.ops.mesh.primitive_uv_sphere_add, segments=10, ring_count=6, location=(0, 0, 1.345))
    parts[-1].scale = (0.078, 0.082, 0.095)
    add(bpy.ops.mesh.primitive_uv_sphere_add, segments=10, ring_count=6, location=(0, -0.015, 1.385))
    parts[-1].scale = (0.095, 0.10, 0.085)
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.join()
    FIG['woman'] = bpy.context.object; FIG['woman'].name = "ProtoWoman"
    # CHILD
    parts = []
    add(bpy.ops.mesh.primitive_cone_add, vertices=10, radius1=0.20, radius2=0.12, depth=0.55, location=(0, 0, 0.275))
    add(bpy.ops.mesh.primitive_cube_add, location=(0, 0, 0.66)); parts[-1].dimensions = (0.24, 0.16, 0.26)
    add(bpy.ops.mesh.primitive_uv_sphere_add, segments=10, ring_count=6, location=(0, 0, 0.87))
    parts[-1].scale = (0.070, 0.073, 0.082)
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.join()
    FIG['child'] = bpy.context.object; FIG['child'].name = "ProtoChild"
    for k in FIG: FIG[k].hide_render = True

def place(kind, x, y, ry=0.0, material=None, hs=1.0, z=0.0):
    src = FIG[kind]
    o = src.copy(); o.data = src.data  # linked duplicate (shared mesh)
    o.hide_render = False; o.hide_viewport = False
    o.location = (x, y, z); o.rotation_euler = (0, 0, ry); o.scale = (hs, hs, hs)
    bpy.context.collection.objects.link(o)
    if material:
        o.data = src.data.copy()
        o.data.materials.clear(); o.data.materials.append(material)
        if kind == 'man':  # legs etc all one mat slot set: keep simple — single coat material
            pass
    return o

build_prototypes()
# give prototypes base materials (single material look per figure is fine at this scale)
FIG['man'].data.materials.append(COATS[0])
FIG['woman'].data.materials.append(DRESS[0])
FIG['child'].data.materials.append(DRESS[2])

# ----- floor & carpet -----
box("Floor", (0, 0, -0.03), (17.0, 10.0, 0.06), FLOOR)
box("Carpet", (0, 0.6, 0.006), (3.2, 7.6, 0.012), CARPET)

# ----- dais (centre) -----
box("DaisStep1", (0, -1.2, 0.09), (7.4, 4.6, 0.18), CARPET)
box("DaisStep2", (0, -1.2, 0.26), (6.4, 3.9, 0.16), CARPET)
box("DaisTop", (0, -1.2, 0.42), (5.6, 3.3, 0.16), CARPET)

# ----- canopy: 4 gold columns, slab top, valance, back drape -----
for cx in (-2.5, 2.5):
    for cy in (-2.5, 0.1):
        cyl("CanopyCol", (cx, cy, 0.5 + 1.9), 0.055, 0.07, 3.8, GOLD, 10)
        sph("ColFinial", (cx, cy, 4.48), (0.09, 0.09, 0.12), GOLD)
box("CanopyTop", (0, -1.2, 4.62), (5.9, 3.9, 0.22), CRIMSON)
box("CanopyCrest", (0, -1.2, 4.86), (1.6, 0.5, 0.26), GOLD)
for i in range(13):  # valance scallops (front)
    sph("Valance", (-2.64 + i * 0.44, 0.78, 4.42), (0.23, 0.06, 0.17), CRIMSON, 8)
box("BackDrapeL", (-2.45, -2.52, 2.6), (0.85, 0.08, 3.9), CRIMSON)
box("BackDrapeR", (2.45, -2.52, 2.6), (0.85, 0.08, 3.9), CRIMSON)
box("BackDrapeC", (0, -2.56, 3.4), (4.1, 0.07, 2.3), CRIMSON)

# ----- thrones -----
for tx in (-0.55, 0.55):
    box("ThroneSeat", (tx, -1.55, 0.78), (0.85, 0.7, 0.14), GOLD)
    box("ThroneBack", (tx, -1.92, 1.55), (0.85, 0.12, 1.7), CRIMSON)
    box("ThroneBase", (tx, -1.55, 0.57), (0.8, 0.65, 0.28), GOLD)

# ----- royal party & officials on the dais (stylised, no likenesses) -----
place('woman', -0.55, -1.15, 0.0, DRESS[3], 0.97, z=0.50)   # Queen figure: dark dress + 
sph("QueenSash", (-0.55, -1.02, 0.0), (0.001, 0.001, 0.001), BLUE, 6)  # placeholder removed below
bpy.data.objects.remove(bpy.context.scene.objects.get("QueenSash"), do_unlink=True)
box("QueenSashBand", (-0.55, -1.00, 1.53), (0.30, 0.03, 0.10), BLUE, (math.radians(24), 0, 0))
place('man', 0.55, -1.15, 0.0, COATS[1], 1.03, z=0.50)      # Prince figure
box("PrinceSash", (0.55, -1.00, 1.60), (0.34, 0.03, 0.10), BLUE, (math.radians(-24), 0, 0))
place('child', -1.35, -0.55, 0.2, None, 1.0, z=0.50)
place('child', 1.35, -0.55, -0.2, None, 0.92, z=0.50)
place('man', -1.85, -1.35, 0.3, COATS[2], 1.0, z=0.50)      # official with staff
cyl("Staff", (-1.62, -1.15, 1.5), 0.02, 0.02, 2.0, GOLD, 8)
place('man', 1.90, -1.30, -0.3, WHITE, 1.0, z=0.50)         # robed cleric (white)
place('man', -2.55, -0.75, 0.5, COATS[0], 1.0, z=0.50)
place('woman', 2.60, -0.80, -0.5, DRESS[0], 1.0, z=0.50)
place('man', 2.55, -1.75, -0.4, COATS[2], 1.0, z=0.50)
place('woman', -2.60, -1.80, 0.4, DRESS[1], 1.0, z=0.50)
# choir boys / attendants row behind canopy sides
for i in range(4):
    place('child', -2.95, -2.2 + i * 0.55, 0.3, WHITE, 0.95, z=0.34)
    place('child', 2.95, -2.2 + i * 0.55, -0.3, WHITE, 0.95, z=0.34)

# ----- foreground crowd: silhouette masses flanking the aisle -----
for side in (-1, 1):
    for row in range(4):
        y = 1.1 + row * 0.85
        n = 6 - (row % 2)
        for i in range(n):
            x = side * (2.6 + i * 0.78) + random.uniform(-0.08, 0.08)
            if abs(x) > 8.2: continue
            kind = 'woman' if (i + row) % 2 == 0 else 'man'
            place(kind, x, y + random.uniform(-0.1, 0.1), math.pi + random.uniform(-0.2, 0.2),
                  None, random.uniform(0.95, 1.04))
    # standing groups nearer dais (courtiers)
    for i in range(3):
        place('man' if i % 2 else 'woman', side * (3.6 + i * 0.9), -0.4 + (i % 2) * 0.5,
              math.pi * 0.9, None, 1.0, z=0.18 if i == 0 else 0.0)
# a few foreground backs, bottom corners (as painted)
place('man', -5.6, 4.6, math.pi, COATS[1], 1.25)
place('woman', -4.6, 4.8, math.pi, DRESS[1], 1.22)
place('woman', 5.4, 4.7, math.pi, DRESS[0], 1.24)
place('man', 4.5, 4.9, math.pi, COATS[0], 1.26)

# ----- backdrop: transept arch + columns + banners -----
for cx in (-6.4, 6.4):
    cyl("ArchCol", (cx, -4.6, 3.25), 0.16, 0.20, 6.5, ARCH, 12)
bpy.ops.mesh.primitive_torus_add(major_radius=6.4, minor_radius=0.16, major_segments=32,
                                 minor_segments=8, location=(0, -4.6, 6.5),
                                 rotation=(math.radians(90), 0, 0))
arch = bpy.context.object; arch.name = "TranseptArch"
import bmesh  # keep only the upper half of the ring (local +Y becomes +Z after rotation)
bm = bmesh.new(); bm.from_mesh(arch.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < 0], context='VERTS')
bm.to_mesh(arch.data); bm.free()
arch.scale = (1, 1, 0.55)
bpy.ops.object.transform_apply(scale=True)
arch.data.materials.append(ARCH)
# banners hanging below the arch (abstract colours, no arms drawn)
for bx, bm2 in ((-4.4, BLUE), (-2.9, mat("BannerRed", (0.55, 0.15, 0.15))), (2.9, WHITE), (4.4, BLUE)):
    box("Banner", (bx, -4.45, 4.95), (0.85, 0.05, 2.6), bm2)
    cyl("BannerRod", (bx, -4.45, 6.30), 0.03, 0.03, 1.0, GOLD, 8, (0, math.radians(90), 0))

# ----- Osler crystal fountain hint (right, as painted) -----
FX, FY = -5.6, -3.4
cyl("FountainBase", (FX, FY, 0.5), 0.75, 0.9, 1.0, GLASS, 16)
cyl("FountainStem", (FX, FY, 1.7), 0.10, 0.16, 1.4, GLASS, 10)
sph("FountainTier1", (FX, FY, 2.35), (0.62, 0.62, 0.16), GLASS)
cyl("FountainStem2", (FX, FY, 2.9), 0.06, 0.09, 0.9, GLASS, 8)
sph("FountainTier2", (FX, FY, 3.3), (0.40, 0.40, 0.12), GLASS)
sph("FountainDrop", (FX, FY, 3.85), (0.10, 0.10, 0.28), GLASS)
# elm hint left (the great elm inside the transept)
cyl("ElmTrunk", (5.9, -3.9, 1.6), 0.22, 0.34, 3.2, mat("Bark", (0.35, 0.28, 0.20)), 8)
sph("ElmCanopy", (5.9, -3.9, 4.4), (1.7, 1.3, 1.5), mat("Leaf", (0.30, 0.42, 0.24)))

# ----- camera / light / render -----
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 960; scene.render.resolution_y = 660
scene.render.filepath = os.path.join(OUT, "preview.png")
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
bpy.ops.object.light_add(type='SUN', location=(5, 7, 10))
sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(48), 0, math.radians(30))
bpy.ops.object.camera_add(location=(0.0, 15.6, 5.4))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(77), 0, math.radians(180))
cam.data.lens = 30

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)

dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for ob in scene.objects:
    if ob.type == 'MESH':
        ev = ob.evaluated_get(dg); me = ev.to_mesh()
        me.calc_loop_triangles(); tris += len(me.loop_triangles)
        ev.to_mesh_clear()
print("TOTAL_TRIS", tris)
