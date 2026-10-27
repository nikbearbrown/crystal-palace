#!/usr/bin/env python3
"""Build the 1851 Great Exhibition medal in Blender 4.2.

A 39 mm white-metal disc (diameter documented in the repo manifest).
Both faces are polar grids displaced from the heightmaps drawn by
make_heightmaps.py (which see for method and transcription sources),
with the same heightmaps as bump maps for micro-detail. Struck rim
profile is built into the grid; the edge is a plain rounded band
(no edge view survives - see NOTES.md).

Run: blender -b -P scripts/build_exhibition_medal.py
Outputs: ../exhibition-medal-1851.blend, ../exhibition-medal-1851.glb,
../renders/{front,reverse,side,three-quarter}.png
"""
import bpy, math, os, sys
import numpy as np
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(BASE, "work")
MM = 0.001

# ------------------------------------------------------------- parameters
R_OUT = 19.5          # mm, equator radius (diameter 39 mm, documented)
R_FACE = 19.42        # mm, face grid outer radius
HT = 1.05             # mm, half-thickness at the field (inferred)
RELIEF_OBV = 0.34     # mm at heightmap white (obverse)
RELIEF_REV = 0.20     # mm at heightmap white (reverse)
SECTORS = 192
CANVAS_HALF = 512.0 / (500.0 / 19.5)   # mm spanned by half the heightmap
S_PX = 500.0 / 19.5                     # heightmap px per mm

def smoothstep(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)

def rim_profile(r):
    """Extra height (mm) of the struck rim above the field, by radius."""
    if r <= 16.9:
        return 0.0
    if r <= 18.35:
        return 0.5 * smoothstep((r - 16.9) / 1.45)
    return 0.5 - 0.38 * smoothstep((r - 18.35) / 1.07)

# ------------------------------------------------------------- heightmaps
def load_sampler(fname):
    img = bpy.data.images.load(os.path.join(WORK, fname))
    w, h = img.size
    arr = np.asarray(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[:, :, 0]
    arr = arr[::-1, :]                       # Blender rows are bottom-up
    bpy.data.images.remove(img)
    return arr

def sample(arr, xs, zs):
    px = 512.0 + xs * S_PX
    py = 512.0 - zs * S_PX
    x0 = np.floor(px).astype(int); y0 = np.floor(py).astype(int)
    fx = px - x0; fy = py - y0
    x0 = np.clip(x0, 0, 1023); x1 = np.clip(x0 + 1, 0, 1023)
    y0 = np.clip(y0, 0, 1023); y1 = np.clip(y0 + 1, 0, 1023)
    return (arr[y0, x0] * (1 - fx) * (1 - fy) + arr[y0, x1] * fx * (1 - fy) +
            arr[y1, x0] * (1 - fx) * fy + arr[y1, x1] * fx * fy)

# ------------------------------------------------------------- mesh
def build_medal():
    obv = load_sampler("height_obverse_soft.png")
    rev = load_sampler("height_reverse_soft.png")

    # radial stations: eased grid + explicit rim stations
    radii = [0.0]
    n = 44
    for i in range(1, n + 1):
        radii.append(R_FACE * (i / n) ** 0.95)
    for extra in (17.3, 17.7, 18.05, 18.35, 18.7, 19.05):
        if extra < R_FACE:
            radii.append(extra)
    radii = sorted(set(round(r, 4) for r in radii if r <= R_FACE))
    if radii[-1] < R_FACE:
        radii.append(R_FACE)
    rings = radii[1:]                      # ring 0 = first radius > 0
    print("rings:", len(rings))

    verts = []        # (x, y, z) metres; disc in XZ plane, centre z=+R_OUT
    side = []         # 0 obverse(-Y) 1 reverse(+Y) 2 band
    faces = []        # index tuples
    fmat = []         # material index per face
    ZC = R_OUT        # disc centre height (origin at base centre)

    def add_face_grid(arr, relief_max, ysign, mirror_x):
        """Returns (centre_idx, ring_start_indices). Normal faces ysign."""
        base = len(verts)
        # centre vertex
        c = sample(arr, np.array([0.0]), np.array([0.0]))[0]
        verts.append((0.0, ysign * (HT + rim_profile(0.0) + relief_max * c) * MM,
                      ZC * MM))
        side.append(0 if ysign < 0 else 1)
        ring_idx = []
        for r in rings:
            start = len(verts)
            ring_idx.append(start)
            th = np.linspace(0, 2 * math.pi, SECTORS, endpoint=False)
            xs = r * np.cos(th); zs = r * np.sin(th)
            sx = -xs if mirror_x else xs
            h = sample(arr, sx, zs)
            ys = ysign * (HT + rim_profile(r) + relief_max * h)
            for j in range(SECTORS):
                verts.append((xs[j] * MM, ys[j] * MM, (ZC + zs[j]) * MM))
                side.append(0 if ysign < 0 else 1)
        # centre fan
        for j in range(SECTORS):
            jn = (j + 1) % SECTORS
            if ysign < 0:
                faces.append((base, ring_idx[0] + jn, ring_idx[0] + j))
            else:
                faces.append((base, ring_idx[0] + j, ring_idx[0] + jn))
            fmat.append(0 if ysign < 0 else 1)
        # ring quads as triangles
        for k in range(len(rings) - 1):
            a0, b0 = ring_idx[k], ring_idx[k + 1]
            for j in range(SECTORS):
                jn = (j + 1) % SECTORS
                if ysign < 0:
                    faces.append((a0 + j, b0 + jn, b0 + j))
                    faces.append((a0 + j, a0 + jn, b0 + jn))
                else:
                    faces.append((a0 + j, b0 + j, b0 + jn))
                    faces.append((a0 + j, b0 + jn, a0 + jn))
                fmat.extend([0 if ysign < 0 else 1] * 2)
        return base, ring_idx

    _, obv_rings = add_face_grid(obv, RELIEF_OBV, -1, False)
    _, rev_rings = add_face_grid(rev, RELIEF_REV, +1, True)

    # ---- edge band: face outer rings -> r=19.5 at y=-0.45 -> +0.45 -> rev
    obv_outer = obv_rings[-1]
    rev_outer = rev_rings[-1]
    band_rows = []
    for (rr, yy) in ((R_OUT, -0.45), (R_OUT, 0.45)):
        start = len(verts)
        th = np.linspace(0, 2 * math.pi, SECTORS, endpoint=False)
        for j in range(SECTORS):
            verts.append((rr * math.cos(th[j]) * MM, yy * MM,
                          (ZC + rr * math.sin(th[j])) * MM))
            side.append(2)
        band_rows.append(start)
    rows = [obv_outer, band_rows[0], band_rows[1], rev_outer]
    for k in range(3):
        a0, b0 = rows[k], rows[k + 1]
        for j in range(SECTORS):
            jn = (j + 1) % SECTORS
            faces.append((a0 + j, b0 + j, b0 + jn, a0 + jn))
            fmat.append(2)

    me = bpy.data.meshes.new("MedalMesh")
    me.from_pydata(verts, [], faces)
    me.update()

    # UVs (per loop): planar disc mapping; reverse mirrored so the
    # lettering reads correctly seen from behind
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index]
            x_mm = v.co.x / MM; z_mm = v.co.z / MM - ZC
            s = side[me.loops[li].vertex_index]
            if s == 1:
                u = 0.5 - x_mm / (2 * CANVAS_HALF)
            else:
                u = 0.5 + x_mm / (2 * CANVAS_HALF)
            vv = 0.5 + z_mm / (2 * CANVAS_HALF)
            uv.data[li].uv = (u, vv)
    for i, poly in enumerate(me.polygons):
        poly.material_index = fmat[i]
        poly.use_smooth = fmat[i] != 2

    ob = bpy.data.objects.new("exhibition-medal-1851", me)
    bpy.context.collection.objects.link(ob)
    return ob

# ------------------------------------------------------------- materials
def metal_material(bump_name, bump_file):
    mat = bpy.data.materials.new(bump_name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.68, 0.69, 0.71, 1.0)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.54
    if bump_file:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(os.path.join(WORK, bump_file))
        tex.image.colorspace_settings.name = "Non-Color"
        tex.extension = "CLIP"
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.65
        bump.inputs["Distance"].default_value = 0.00045
        nt.links.new(tex.outputs["Color"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
        # devices slightly rougher than the polished field
        ramp = nt.nodes.new("ShaderNodeMapRange")
        ramp.inputs["From Min"].default_value = 0.0
        ramp.inputs["From Max"].default_value = 1.0
        ramp.inputs["To Min"].default_value = 0.46
        ramp.inputs["To Max"].default_value = 0.62
        nt.links.new(tex.outputs["Color"], ramp.inputs["Value"])
        nt.links.new(ramp.outputs["Result"], bsdf.inputs["Roughness"])
    return mat

# ------------------------------------------------------------- rig
def point_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def build_rig():
    scene = bpy.context.scene
    # ground
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0))
    g = bpy.context.active_object
    g.name = "BackdropGround"
    gm = bpy.data.materials.new("GreyGround")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.38, 0.38, 0.38, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.data.materials.append(gm)
    # lights
    C = (0, 0, R_OUT * MM)
    def area(name, pos, energy, size):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy = energy; ld.shape = 'DISK'; ld.size = size
        o = bpy.data.objects.new(name, ld)
        o.location = pos
        bpy.context.collection.objects.link(o)
        point_at(o, C)
        return o
    area("Key", (-0.85, -0.45, 0.75), 2.6, 0.55)
    area("Fill", (0.80, -0.35, 0.25), 0.8, 0.50)
    area("Rim", (0.25, 0.80, 0.85), 1.9, 0.45)
    # cameras
    def cam(name, pos, lens=52.0):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens; cd.clip_start = 0.005; cd.clip_end = 2.0
        o = bpy.data.objects.new(name, cd)
        o.location = pos
        bpy.context.collection.objects.link(o)
        point_at(o, C)
        return o
    cams = {
        "front": cam("CamFront", (0, -0.104, R_OUT * MM)),
        "reverse": cam("CamReverse", (0, 0.104, R_OUT * MM)),
        "side": cam("CamSide", (0.104, 0, R_OUT * MM)),
        "three-quarter": cam("CamTQ", (-0.060, -0.080, 0.078)),
    }
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 80
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium Contrast'
    scene.view_settings.exposure = 1.0
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.30, 0.30, 0.30, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    return cams

# ------------------------------------------------------------- main
def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    medal = build_medal()
    mats = [metal_material("WhiteMetalObverse", "height_obverse.png"),
            metal_material("WhiteMetalReverse", "height_reverse.png"),
            metal_material("WhiteMetalEdge", None)]
    for m in mats:
        medal.data.materials.append(m)
    tris = sum(len(p.vertices) - 2 for p in medal.data.polygons)
    print(f"TRIANGLES: {tris}")
    print(f"DIMS: {medal.dimensions.x:.4f} x {medal.dimensions.y:.4f} x {medal.dimensions.z:.4f} m")

    cams = build_rig()
    scene = bpy.context.scene
    for img in bpy.data.images:
        if img.name.startswith("height_"):
            try:
                img.pack()
            except Exception as e:
                print("pack:", img.name, e)
    blend_path = os.path.join(BASE, "exhibition-medal-1851.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("saved", blend_path)

    bpy.ops.object.select_all(action='DESELECT')
    medal.select_set(True)
    bpy.context.view_layer.objects.active = medal
    glb_path = os.path.join(BASE, "exhibition-medal-1851.glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                              use_selection=True)
    print("saved", glb_path)

    if "--norender" in sys.argv:
        print("skipping renders")
        return
    out = {"front": "front.png", "reverse": "reverse.png",
           "side": "side.png", "three-quarter": "three-quarter.png"}
    for key, fname in out.items():
        scene.camera = cams[key]
        scene.render.filepath = os.path.join(BASE, "renders", fname)
        bpy.ops.render.render(write_still=True)
        print("rendered", fname)

main()
