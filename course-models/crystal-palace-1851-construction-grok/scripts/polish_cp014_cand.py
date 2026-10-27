"""CANDIDATE polish CP014 on k01 → rounds/candidates/k01_cp014.blend. Does not touch live k01."""
import bpy, bmesh, math, sys, os
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FT = 0.3048
def ft(v): return v * FT

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SRC = argv[argv.index("--src") + 1] if "--src" in argv else "rounds/k01.blend"
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/k01_cp014.blend"
root = os.path.dirname(HERE)
src = SRC if os.path.isabs(SRC) else os.path.join(root, SRC)
out = OUT if os.path.isabs(OUT) else os.path.join(root, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=src)

def mat(name, col, rough=0.85, metal=0.0, emit=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    if "Metallic" in b.inputs: b.inputs["Metallic"].default_value = metal
    if emit and "Emission Strength" in b.inputs:
        b.inputs["Emission Color"].default_value = (*col, 1)
        b.inputs["Emission Strength"].default_value = emit
    return m

WATER = mat("CP014_WaterCand", (0.04, 0.28, 0.85), 0.12, 0.0, 0.35)
COND = mat("CP014_CondCand", (0.12, 0.75, 0.78), 0.18, 0.0, 0.55)
DROP = mat("CP014_DropCand", (0.08, 0.45, 0.9), 0.1, 0.0, 0.4)

coll = bpy.data.collections.get("CP014_CAND") or bpy.data.collections.new("CP014_CAND")
if coll.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(coll)

def link_mesh(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    return ob

# denser rain streaks on glass slopes (Paxton roof)
bm = bmesh.new()
for gx in (-4.0, 4.0):
    for yy in (1.5, 2.8, 4.0, 5.5, 7.0, 8.5, 10.0, 11.5):
        # thin water ribbon down the glass into the gutter
        z1 = 25.2 + 0.05 * yy
        z0 = 23.9 + 0.02 * yy
        x0 = gx * 0.55
        verts = [
            bm.verts.new((ft(x0 - 0.04), ft(yy), ft(z1))),
            bm.verts.new((ft(x0 + 0.04), ft(yy), ft(z1))),
            bm.verts.new((ft(gx * 0.85), ft(yy + 0.15), ft(z0))),
            bm.verts.new((ft(gx * 0.85 - 0.06), ft(yy - 0.1), ft(z0))),
        ]
        try: bm.faces.new(verts)
        except: pass
link_mesh("CP014_cand_rain_streaks", bm, [WATER])

# condensation droplets under Paxton gutters
bm = bmesh.new()
for x in (-4.0, 4.0):
    for y in (2.0, 4.0, 6.0, 8.0, 10.0, 12.0):
        for k in range(3):
            bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=4, radius=ft(0.04 + 0.01 * (k % 2)),
                matrix=__import__('mathutils').Matrix.Translation((ft(x + (k-1)*0.12), ft(y), ft(23.7 - 0.08*k))))
link_mesh("CP014_cand_cond_drops", bm, [COND])

# thicker water column inside hollow column (visible on cut face)
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=10,
                      radius1=ft(0.18), radius2=ft(0.16), depth=ft(22.0),
                      matrix=__import__('mathutils').Matrix.Translation((0, ft(0.08), ft(8.0))))
link_mesh("CP014_cand_column_water", bm, [WATER])

# water in outlet pipe + puddle at brick drain
bm = bmesh.new()
# half-pipe water along outlet toward +x
for i in range(12):
    t0, t1 = i/12, (i+1)/12
    x0, x1 = 1.2 + 10.0*t0, 1.2 + 10.0*t1
    z = -2.6
    bm.faces.new([
        bm.verts.new((ft(x0), ft(0.05), ft(z+0.08))),
        bm.verts.new((ft(x1), ft(0.05), ft(z+0.08))),
        bm.verts.new((ft(x1), ft(0.35), ft(z))),
        bm.verts.new((ft(x0), ft(0.35), ft(z))),
    ])
# puddle at drain end
bmesh.ops.create_circle(bm, cap_ends=True, segments=16, radius=ft(0.9),
    matrix=__import__('mathutils').Matrix.Translation((ft(12.0), ft(0.4), ft(-2.55))))
link_mesh("CP014_cand_pipe_puddle", bm, [WATER, DROP])

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
