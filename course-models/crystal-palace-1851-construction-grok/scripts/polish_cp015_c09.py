"""CP015 set polish on c04 → c09: denser louvre blades, hanging canvas flaps, floor plank grooves, wall boarding grit."""
import bpy, bmesh, math, sys, os
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FT = 0.3048
def ft(v): return v * FT
def inch(v): return v * FT / 12.0

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/c09.blend"
SRC = argv[argv.index("--src") + 1] if "--src" in argv else "rounds/c04.blend"

bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(HERE), SRC) if not os.path.isabs(SRC) else SRC)

def mat(name, col, rough=0.85, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    if "Metallic" in b.inputs: b.inputs["Metallic"].default_value = metal
    return m

CANVAS = mat("CP015_Canvas", (0.55, 0.48, 0.36), 0.92)
CANVAS_D = mat("CP015_CanvasDeep", (0.38, 0.32, 0.24), 0.95)
IRON = mat("CP015_LouvreIron", (0.12, 0.11, 0.10), 0.55, 0.35)
WOOD = mat("CP015_Board", (0.42, 0.32, 0.20), 0.88)
FLOOR = mat("CP015_Floor", (0.48, 0.40, 0.28), 0.9)

coll = bpy.data.collections.get("LOUVRE_CANVAS") or bpy.data.collections.new("LOUVRE_CANVAS")
if coll.name not in bpy.context.scene.collection.children:
    try: bpy.context.scene.collection.children.link(coll)
    except: pass

def new_mesh(name, bm, mats, loc=(0,0,0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    coll.objects.link(ob)
    return ob

# hanging canvas flaps under canvas-roof zone (x 228-300, y~-180)
bm = bmesh.new()
for xi, x in enumerate(range(232, 300, 12)):
    for yi, y in enumerate((-198.0, -186.0, -174.0)):
        # flap hanging from girder line
        z1 = 19.0
        drop = 4.5 + (xi + yi) % 3
        # two-layer flap with slight fold
        for s, mat_i in ((0.0, 0), (0.15, 1)):
            bm.faces.new([
                bm.verts.new((ft(x - 4.5), ft(y + s), ft(z1))),
                bm.verts.new((ft(x + 4.5), ft(y + s), ft(z1))),
                bm.verts.new((ft(x + 4.2), ft(y + s + 0.4), ft(z1 - drop))),
                bm.verts.new((ft(x - 4.2), ft(y + s - 0.2), ft(z1 - drop * 0.92))),
            ])
me = bpy.data.meshes.new("CP015_canvas_flaps")
bm.to_mesh(me); bm.free()
me.materials.append(CANVAS); me.materials.append(CANVAS_D)
for i, p in enumerate(me.polygons):
    p.material_index = i % 2
ob = bpy.data.objects.new("CP015_canvas_flaps", me)
coll.objects.link(ob)

# thicker louvre blades (static open) in front of existing wall at xc=240,264,288
bm = bmesh.new()
for xc in (240, 264, 288):
    for band, (z0, z1), nbl in (("low", (3.5, 5.0), 4), ("high", (14.0, 18.6), 10)):
        for k in range(nbl):
            z = z0 + (z1 - z0) * (k + 0.5) / nbl
            # tilted blade ~35 deg (thicker)
            half = (z1 - z0) / nbl * 0.48
            # box then rotate via verts offset
            y0 = -204.0 - 0.15
            # parallelogram cross-section reading as open blade
            dx = 11.5
            tip = half * 0.7  # forward tilt
            verts = [
                (ft(xc - dx), ft(y0), ft(z - half)),
                (ft(xc + dx), ft(y0), ft(z - half)),
                (ft(xc + dx), ft(y0 + tip), ft(z + half * 0.3)),
                (ft(xc - dx), ft(y0 + tip), ft(z + half * 0.3)),
            ]
            # thickness
            y1 = y0 - 0.12
            verts2 = [(v[0], ft(y1), v[2]) for v in [(xc-dx,0,z-half),(xc+dx,0,z-half),(xc+dx,0,z+half*0.3),(xc-dx,0,z+half*0.3)]]
            # simpler: thin box
            bm.faces.new([
                bm.verts.new((ft(xc - dx), ft(y0), ft(z - half * 0.2))),
                bm.verts.new((ft(xc + dx), ft(y0), ft(z - half * 0.2))),
                bm.verts.new((ft(xc + dx), ft(y0 + 0.55), ft(z + half * 0.55))),
                bm.verts.new((ft(xc - dx), ft(y0 + 0.55), ft(z + half * 0.55))),
            ])
me = bpy.data.meshes.new("CP015_louvre_thick")
bm.to_mesh(me); bm.free()
me.materials.append(IRON)
ob = bpy.data.objects.new("CP015_louvre_thick", me)
coll.objects.link(ob)

# floor plank grooves in camera FOV under blinds
bm = bmesh.new()
for i in range(40):
    y = -200 + i * 2.0
    # groove line as thin trough
    bm.faces.new([
        bm.verts.new((ft(220), ft(y), ft(0.05))),
        bm.verts.new((ft(310), ft(y), ft(0.05))),
        bm.verts.new((ft(310), ft(y + 0.08), ft(0.02))),
        bm.verts.new((ft(220), ft(y + 0.08), ft(0.02))),
    ])
me = bpy.data.meshes.new("CP015_plank_grooves")
bm.to_mesh(me); bm.free()
me.materials.append(FLOOR)
ob = bpy.data.objects.new("CP015_plank_grooves", me)
coll.objects.link(ob)

# wall boarding battens on louvre walls
bm = bmesh.new()
for xc in (240, 264, 288):
    for z in (1.0, 2.2, 6.5, 9.0, 11.5, 16.5):
        bm.faces.new([
            bm.verts.new((ft(xc - 12), ft(-204.2), ft(z))),
            bm.verts.new((ft(xc + 12), ft(-204.2), ft(z))),
            bm.verts.new((ft(xc + 12), ft(-204.2), ft(z + 0.25))),
            bm.verts.new((ft(xc - 12), ft(-204.2), ft(z + 0.25))),
        ])
me = bpy.data.meshes.new("CP015_wall_battens")
bm.to_mesh(me); bm.free()
me.materials.append(WOOD)
ob = bpy.data.objects.new("CP015_wall_battens", me)
coll.objects.link(ob)

# canvas roll props on floor
bm = bmesh.new()
for i, (x, y) in enumerate(((250, -190), (270, -188), (255, -185))):
    # cylinder roll
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12,
                          radius1=ft(0.55), radius2=ft(0.55), depth=ft(6.0),
                          matrix=__import__('mathutils').Matrix.Translation((ft(x), ft(y), ft(0.55))) @
                                 __import__('mathutils').Matrix.Rotation(math.radians(90), 4, 'Y'))
me = bpy.data.meshes.new("CP015_canvas_rolls")
bm.to_mesh(me); bm.free()
me.materials.append(CANVAS_D)
ob = bpy.data.objects.new("CP015_canvas_rolls", me)
coll.objects.link(ob)

out_path = OUT if os.path.isabs(OUT) else os.path.join(os.path.dirname(HERE), OUT)
bpy.ops.wm.save_as_mainfile(filepath=out_path)
print("SAVED", out_path)
