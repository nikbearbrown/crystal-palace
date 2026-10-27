#!/usr/bin/env python3
"""Garden urn on pedestal — Crystal Palace (Sydenham) candidate #16.

Campana urn on a square pedestal, modelled from the Delamotte/Rijksmuseum
photograph RP-F-F01134-AL (CC0) and RP-F-F01212-16-1 (CC0): tall white
campana vases on square pedestals recur along the Sydenham garden paths,
on the fountain-basin rim and on the terrace parapet piers. No single urn
is shown close; the silhouette family is fixed, absolute size inferred
(see NOTES.md). Procedural lathe + stacked pedestal boxes. Blender 4.2.
"""
import bpy, math, os, sys
from mathutils import Vector

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUND_TAG = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "r1"

# ---------------------------------------------------------------- parameters
PED_H = 0.98          # pedestal height (m) — inferred, see NOTES.md
URN_H = 0.81          # urn height above pedestal
RIM_R = 0.345         # urn mouth radius (rim dia 0.69 m)
TOTAL_H = PED_H + URN_H

# ---------------------------------------------------------------- clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------------------------------------------------------------- materials
def stone_mat(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

MAT_URN = stone_mat("UrnStone", (0.74, 0.72, 0.66))
MAT_PED = stone_mat("PedestalStone", (0.68, 0.66, 0.60))
MAT_SOIL = stone_mat("SoilDark", (0.16, 0.12, 0.09), 1.0)

# ---------------------------------------------------------------- lathe urn
def build_urn():
    # (radius, z_rel_to_pedestal_top) outer profile, foot -> lip -> inner wall
    prof = [
        (0.000, 0.000), (0.175, 0.000), (0.195, 0.015), (0.190, 0.045),
        (0.132, 0.070), (0.106, 0.110), (0.101, 0.155), (0.148, 0.195),
        (0.153, 0.228), (0.122, 0.260), (0.128, 0.288), (0.162, 0.340),
        (0.208, 0.420), (0.245, 0.510), (0.272, 0.600), (0.296, 0.680),
        (0.322, 0.735), (0.342, 0.775), (0.348, 0.795), (0.332, 0.812),
        (0.310, 0.797), (0.298, 0.740), (0.280, 0.665), (0.000, 0.645),
    ]
    SEG = 72
    LOBES = 16
    def gadroon(r, z, theta):
        # shallow lobes on the lower bell only (z 0.27..0.56), tapering out
        if 0.26 < z < 0.54:
            t = (z - 0.26) / 0.28
            amp = 0.0075 * math.sin(math.pi * min(t, 1.0))
            return r + amp * math.cos(LOBES * theta)
        return r
    verts, faces = [], []
    for (r, z) in prof:
        for i in range(SEG):
            th = 2 * math.pi * i / SEG
            rr = gadroon(r, z, th) if r > 0.01 else r
            verts.append((rr * math.cos(th), rr * math.sin(th), PED_H + z))
    n = len(prof)
    for j in range(n - 1):
        for i in range(SEG):
            a = j * SEG + i
            b = j * SEG + (i + 1) % SEG
            c = (j + 1) * SEG + (i + 1) % SEG
            d = (j + 1) * SEG + i
            faces.append((a, b, c, d))
    me = bpy.data.meshes.new("UrnMesh")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new("GardenUrn", me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(MAT_URN)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob

def box(name, sx, sy, z0, z1, mat, bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, (z0 + z1) / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (sx, sy, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        mod = ob.modifiers.new("bev", 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier="bev")
    ob.data.materials.append(mat)
    return ob

urn = build_urn()
# soil disc just inside the mouth
bpy.ops.mesh.primitive_cylinder_add(radius=0.280, depth=0.02, vertices=48,
                                    location=(0, 0, PED_H + 0.668))
soil = bpy.context.active_object
soil.name = "Soil"
soil.data.materials.append(MAT_SOIL)

# pedestal: plinth / scotia step / die / cove / cap slab / bed
box("PedPlinth", 0.67, 0.67, 0.00, 0.10, MAT_PED)
box("PedScotia", 0.57, 0.57, 0.10, 0.16, MAT_PED)
box("PedDie",    0.51, 0.51, 0.16, 0.78, MAT_PED)
box("PedCove",   0.57, 0.57, 0.78, 0.84, MAT_PED)
box("PedCap",    0.63, 0.63, 0.84, 0.94, MAT_PED)
box("PedBed",    0.55, 0.55, 0.94, PED_H, MAT_PED)

# ---------------------------------------------------------------- stats
tris = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print(f"STATS tris={tris} objects={len(bpy.context.scene.objects)} total_h={TOTAL_H:.2f} rim_dia={2*RIM_R:.2f}")

# ---------------------------------------------------------------- save + glb
os.makedirs(f"{OUT}/renders", exist_ok=True)
os.makedirs(f"{OUT}/work", exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/garden-urn.blend")
bpy.ops.export_scene.gltf(filepath=f"{OUT}/garden-urn.glb", export_format='GLB')

# ---------------------------------------------------------------- render rig
def grey_mat(name, v):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (v, v, v, 1.0)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    return m

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.001))
ground = bpy.context.active_object
ground.data.materials.append(grey_mat("GroundGrey", 0.42))
ground.name = "StudioGround"
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 6.5, 4.0))
bd = bpy.context.active_object
bd.rotation_euler = (math.radians(90), 0, 0)
bd.data.materials.append(grey_mat("BackdropGrey", 0.52))
bd.name = "StudioBackdrop"

def add_light(name, loc, power, size=3.0):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = power
    ld.shape = 'DISK'
    ld.size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    direction = Vector((0, 0, 0.9)) - lo.location
    lo.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

add_light("Key", (2.6, -2.8, 3.6), 480, 3.5)
add_light("Fill", (-3.2, -0.6, 1.8), 140, 3.0)
add_light("Rim", (0.6, 3.2, 3.0), 280, 2.5)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

def make_cam(name, loc, look=(0, 0, 0.88)):
    cd = bpy.data.cameras.new(name)
    cd.lens = 50
    co = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(co)
    co.location = loc
    direction = Vector(look) - co.location
    co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return co

D = 4.6
cams = {
    "front": make_cam("CamFront", (0, -D, 1.05)),
    "side": make_cam("CamSide", (D, 0, 1.05)),
    "three-quarter": make_cam("CamTQ", (D * 0.72, -D * 0.72, 1.55)),
}
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.03
if ROUND_TAG == "final":
    scene.cycles.samples = 32
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1150
else:
    scene.cycles.samples = 16
    scene.render.resolution_x = 640
    scene.render.resolution_y = 736
scene.cycles.use_denoising = True
scene.render.film_transparent = False

final_dir = f"{OUT}/renders"
ONLY = sys.argv[sys.argv.index("--") + 2] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 2 else None
for view, cam in cams.items():
    if ONLY and view != ONLY:
        continue
    scene.camera = cam
    dest = final_dir if ROUND_TAG == "final" else f"{OUT}/work"
    tag = "" if ROUND_TAG == "final" else f"_{ROUND_TAG}"
    scene.render.filepath = f"{dest}/{view}{tag}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", view)
print("DONE", ROUND_TAG)
