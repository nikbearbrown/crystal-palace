#!/usr/bin/env python3
"""Build the 1851 vacuum sugar apparatus (copper vacuum pan) from the Talbot
calotype in references/muse-drive/images/commons/.
Procedural bpy, Blender 4.2. All dimensions in metres, origin at base centre
(floor under the pan axis). Front of the apparatus faces -Y (camera side in
the photograph).

Proportions measured off the photograph (1501x2059 px):
  sphere dia 1000 px (adopted 2.20 m); dome neck dia 0.18 D; swan-neck tube
  0.115 D; leg separation 0.48 D; condenser dia 0.17 D; total height ~1.9 D.
"""
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------- materials
def mat(name, color, metallic=1.0, rough=0.3, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.blend_method = 'BLEND'
    return m

COPPER  = mat("CopperPolished", (0.62, 0.24, 0.11), 1.0, 0.19)
COPPER2 = mat("CopperPipe",     (0.66, 0.28, 0.13), 1.0, 0.22)
BRASS   = mat("Brass",          (0.50, 0.33, 0.10), 1.0, 0.32)
IRON    = mat("CastIron",       (0.045, 0.045, 0.05), 0.55, 0.62)
STEEL   = mat("SteelDark",      (0.16, 0.16, 0.17), 0.9, 0.42)
GLASS   = mat("GaugeGlass",     (0.75, 0.85, 0.85), 0.0, 0.06, alpha=0.30)
DARK    = mat("DarkHole",       (0.01, 0.01, 0.01), 0.0, 0.9)

# ---------------------------------------------------------------- helpers
def finish(obj, material=None):
    if material:
        obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    bpy.context.collection.objects.link(obj) if obj.name not in bpy.context.collection.objects else None
    return obj

def revolve(name, profile, material, seg=48):
    """profile: list of (r, z) from bottom to top. Lathe about Z axis."""
    verts, faces = [], []
    n = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(seg):
            a = 2 * math.pi * j / seg
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            a, b, c, d = i * seg + j, i * seg + j2, (i + 1) * seg + j2, (i + 1) * seg + j
            faces.append((a, b, c, d))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return finish(ob, material)

def tube_path(name, pts, radius, material, seg=20):
    """Tube along a 3D polyline with parallel-transport frames."""
    pts = [Vector(p) for p in pts]
    # parallel transport
    t0 = (pts[1] - pts[0]).normalized()
    up = Vector((0, 0, 1)) if abs(t0.z) < 0.9 else Vector((1, 0, 0))
    n0 = (up - t0 * up.dot(t0)).normalized()
    frames = []
    n = n0
    for i in range(len(pts)):
        if i == 0:
            t = (pts[1] - pts[0]).normalized()
        elif i == len(pts) - 1:
            t = (pts[-1] - pts[-2]).normalized()
        else:
            t = (pts[i + 1] - pts[i - 1]).normalized()
        n = (n - t * n.dot(t)).normalized()
        b = t.cross(n)
        frames.append((t, n, b))
    verts, faces = [], []
    for i, p in enumerate(pts):
        t, n, b = frames[i]
        for j in range(seg):
            a = 2 * math.pi * j / seg
            off = n * (radius * math.cos(a)) + b * (radius * math.sin(a))
            verts.append(tuple(p + off))
    for i in range(len(pts) - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            faces.append((i * seg + j, i * seg + j2, (i + 1) * seg + j2, (i + 1) * seg + j))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return finish(ob, material)

def arc_pts(centre, radius, a0, a1, n, plane='XZ', fixed=0.0):
    out = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        if plane == 'XZ':
            out.append((centre[0] + radius * math.cos(a), fixed, centre[1] + radius * math.sin(a)))
        else:  # XY vertical plane facing dir handled by caller transforms
            out.append((centre[0] + radius * math.cos(a), centre[1] + radius * math.sin(a), fixed))
    return out

def cyl(name, loc, radius, height, material, seg=28, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=radius, depth=height, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    return finish(ob, material)

def ball(name, loc, radius, material, seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=radius, location=loc)
    ob = bpy.context.object
    ob.name = name
    return finish(ob, material)

def box(name, loc, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if material:
        ob.data.materials.append(material)
    return ob

def torus(name, loc, R, r, material, rot=(0, 0, 0), seg=28):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=seg,
                                     minor_segments=10, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    return finish(ob, material)

def disc_bolts(name, centre, z, ring_r, count, bolt_r, bolt_h, material):
    for i in range(count):
        a = 2 * math.pi * i / count
        cyl(f"{name}_{i}", (centre[0] + ring_r * math.cos(a), centre[1] + ring_r * math.sin(a), z),
            bolt_r, bolt_h, material, seg=8)

def oriented(name, builder, point, normal):
    """Run builder() creating object at origin aligned +Z, then orient +Z to normal at point."""
    ob = builder()
    q = Vector((0, 0, 1)).rotation_difference(Vector(normal))
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = q
    ob.location = point
    return ob

# ---------------------------------------------------------------- the pan
ZC = 1.42          # sphere centre height
RS = 1.10          # sphere radius

# ---------------------------------------------------------------- the pan
prof = []
steps = 44
for i in range(steps + 1):
    th = math.pi * i / steps            # 0 bottom .. pi top
    r = RS * math.sin(th)
    z = ZC - RS * math.cos(th)
    prof.append((max(r, 0.0001), z))
revolve("Pan", prof, COPPER, seg=72)

# girdle ring: two bands + rivet heads
revolve("GirdleBand", [(0.955, 0.715), (0.975, 0.715), (0.985, 0.75), (0.985, 0.80),
                       (0.965, 0.80), (0.965, 0.715)], IRON, seg=64)
revolve("GirdleBandTop", [(0.99, 0.80), (1.015, 0.815), (1.015, 0.875), (0.99, 0.885),
                          (0.955, 0.885), (0.955, 0.80)], COPPER2, seg=64)
for i in range(48):
    a = 2 * math.pi * i / 48
    b = ball(f"Rivet_{i}", (1.012 * math.cos(a), 1.012 * math.sin(a), 0.848), 0.016, COPPER2, seg=10)
    b.scale = (1, 1, 0.75)

# scrolled bracket feet under the ring (inferred - lost in shadow in the photo)
for k, ang in enumerate((45, 135, 225, 315)):
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    P0 = Vector((0.95 * dx, 0.95 * dy, 0.78))
    P1 = Vector((0.97 * dx, 0.97 * dy, 0.32))
    P2 = Vector((1.16 * dx, 1.16 * dy, 0.05))
    pts = []
    for i in range(9):
        t = i / 8
        p = (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t ** 2 * P2
        pts.append(tuple(p))
    tube_path(f"Bracket_{k}", pts, 0.034, IRON, seg=12)
    box(f"FootPad_{k}", (1.16 * dx, 1.16 * dy, 0.018), (0.20, 0.13, 0.036), IRON,
        rot=(0, 0, -a))

# ---------------------------------------------------------------- dome neck
revolve("DomeNeck", [(0.345, 2.44), (0.315, 2.52), (0.27, 2.565), (0.245, 2.60),
                     (0.225, 2.635), (0.205, 2.66), (0.20, 2.70), (0.20, 3.20),
                     (0.235, 3.21), (0.235, 3.24)], COPPER2, seg=48)
revolve("DomeFlange", [(0.20, 3.21), (0.275, 3.225), (0.275, 3.285), (0.20, 3.30)], COPPER, seg=48)
disc_bolts("DomeBolt", (0, 0), 3.295, 0.238, 12, 0.013, 0.03, BRASS)
# maker's plate (plain - the lettering in the photograph is illegible, not invented)
box("MakersPlate", (0, -0.208, 2.94), (0.17, 0.012, 0.24), BRASS)

# ---------------------------------------------------------------- swan neck
path = [(0, 0, 3.24), (0, 0, 3.47)]
path += arc_pts((0.525, 3.47), 0.525, math.pi, 0, 20)[1:]
path += [(1.05, 0, 3.30), (1.05, 0, 3.14)]
tube_path("SwanNeck", path, 0.13, COPPER, seg=28)

# ---------------------------------------------------------------- condenser column
cyl("CondenserBody", (1.05, 0, 2.58), 0.19, 0.90, COPPER2, seg=40)
revolve("CondenserTopFlange", [(0.19, 2.98), (0.248, 3.0), (0.248, 3.085), (0.19, 3.10)],
        COPPER, seg=40).location = (1.05, 0, 0)
disc_bolts("CondBolt", (1.05, 0), 3.095, 0.218, 10, 0.012, 0.028, BRASS)
cyl("CondenserCollar", (1.05, 0, 3.13), 0.158, 0.09, COPPER2, seg=32)
revolve("CondenserBottom", [(0.085, 1.84), (0.13, 1.92), (0.185, 2.02), (0.19, 2.08),
                            (0.235, 2.10), (0.235, 2.17), (0.19, 2.18)], COPPER2, seg=40).location = (1.05, 0, 0)
# downcomer leg, offset outward below the column (hidden behind pan in photo; inferred)
dc = [(1.05, 0, 1.90), (1.05, 0, 1.52)]
dc += arc_pts((1.19, 1.52), 0.14, math.pi, math.pi / 2, 6)[1:]   # elbow out
dc += [(1.33, 0, 1.30), (1.33, 0, 0.50)]
tube_path("Downcomer", dc, 0.082, COPPER2, seg=20)
cyl("DowncomerFlange", (1.33, 0, 0.44), 0.125, 0.05, COPPER2, seg=24)
# column side fittings: lever handle + gauge glass on the front face
cyl("CondLever", (1.30, 0, 2.62), 0.016, 0.24, BRASS, seg=12, rot=(0, math.pi / 2, 0))
ball("CondLeverKnob", (1.43, 0, 2.62), 0.030, IRON, seg=14)
cyl("CondGaugeTop", (1.05, -0.205, 2.80), 0.020, 0.07, BRASS, seg=12)
cyl("CondGaugeGlass", (1.05, -0.215, 2.50), 0.015, 0.52, GLASS, seg=12)
cyl("CondGaugeBottom", (1.05, -0.205, 2.20), 0.020, 0.07, BRASS, seg=12)

# ------------------------------------------------- fittings on the pan shell
def shoulder_fitting(name, polar_deg, az_deg):
    """Ball-capped standpipe on the sphere shoulder. az from -Y (front) toward +X."""
    pol, az = math.radians(polar_deg), math.radians(az_deg)
    d = Vector((math.sin(pol) * math.sin(az), -math.sin(pol) * math.cos(az), math.cos(pol)))
    p = Vector((0, 0, ZC)) + d * (RS - 0.01)
    def build():
        prof = [(0.058, 0.0), (0.055, 0.03), (0.030, 0.06), (0.026, 0.10),
                (0.040, 0.115), (0.040, 0.135), (0.020, 0.145), (0.0001, 0.15)]
        return revolve(name + "_stem", prof, BRASS, seg=24)
    ob = oriented(name, build, p, d)
    b = ball(name + "_ball", tuple(p + d * 0.185), 0.047, BRASS, seg=18)
    return ob

shoulder_fitting("ShoulderValveA", 52, 15)
shoulder_fitting("ShoulderValveB", 55, 46)

# tall gauge glass on the right shoulder (vertical, trumpet foot on the shell)
gx, gy = 0.80, -0.26
gz = ZC + math.sqrt(RS ** 2 - gx ** 2 - gy ** 2)
fg = revolve("GaugeFoot", [(0.085, gz - 0.06), (0.06, gz + 0.02), (0.032, gz + 0.09),
                           (0.028, gz + 0.12)], BRASS, seg=24)
fg.location = (gx, gy, 0)
cyl("GaugeGlassTube", (gx, gy, gz + 0.36), 0.018, 0.46, GLASS, seg=14)
cyl("GaugeGlassCap", (gx, gy, gz + 0.615), 0.034, 0.035, BRASS, seg=14)
revolve("GaugeCapFlare", [(0.018, gz + 0.575), (0.036, gz + 0.60), (0.038, gz + 0.63)],
        BRASS, seg=20).location = (gx, gy, 0)

# small round boss on the right flank
pol, az = math.radians(78), math.radians(38)
d = Vector((math.sin(pol) * math.sin(az), -math.sin(pol) * math.cos(az), math.cos(pol)))
p = Vector((0, 0, ZC)) + d * (RS - 0.005)
def boss_build():
    return cyl("FlankBoss", (0, 0, 0.02), 0.045, 0.06, BRASS, seg=20)
oriented("FlankBossO", boss_build, p, d)
def boss_hole():
    return cyl("FlankBossHole", (0, 0, 0.055), 0.018, 0.012, DARK, seg=14)
oriented("FlankBossHoleO", boss_hole, p, d)

# ---------------------------------------------------------------- twin standpipes (front left)
for sx in (-0.945, -0.815):
    cyl(f"Standpipe_{sx}", (sx, -0.98, 0.735), 0.037, 1.47, IRON, seg=20)
    cyl(f"StandBase_{sx}", (sx, -0.98, 0.03), 0.075, 0.06, IRON, seg=20)
cyl("StandManifold", (-0.88, -0.98, 1.51), 0.105, 0.15, BRASS, seg=24)
torus("StandManifoldRing", (-0.88, -0.98, 1.455), 0.118, 0.016, BRASS, rot=(0, 0, 0))
for sx in (-0.945, -0.815):
    cyl(f"Bonnet_{sx}", (sx, -0.98, 1.635), 0.047, 0.11, BRASS, seg=18)
    torus(f"BonnetRing_{sx}", (sx, -0.98, 1.60), 0.052, 0.010, BRASS)
    torus(f"BonnetRing2_{sx}", (sx, -0.98, 1.675), 0.052, 0.010, BRASS)
    cyl(f"BonnetStem_{sx}", (sx, -0.98, 1.725), 0.016, 0.07, STEEL, seg=12)
# elbow on the right bonnet arcing toward the pan (clean quarter bend + stub)
edir = Vector((0.64, 0.77, 0))
ep = []
for i in range(7):
    t = (math.pi / 2) * i / 6
    p = Vector((-0.815, -0.98, 1.76)) + edir * (0.10 * math.sin(t)) + Vector((0, 0, 0.10 * (1 - math.cos(t))))
    ep.append(tuple(p))
ep.append(tuple(Vector((-0.815, -0.98, 1.86)) + edir * 0.26))
tube_path("StandElbow", ep, 0.030, BRASS, seg=14)
# small lever on the left bonnet
cyl("StandLever", (-0.975, -0.98, 1.80), 0.009, 0.17, STEEL, seg=10, rot=(0, math.radians(38), 0))
ball("StandLeverKnob", (-1.005, -0.98, 1.865), 0.020, IRON, seg=12)

# ---------------------------------------------------------------- draw-off tap (left)
tap_dir = Vector((-0.788, -0.615, 0)).normalized()
tap_base = Vector((-0.824, -0.644, 1.08))
tap_end = tap_base + tap_dir * 0.38
tube_path("TapPipe", [tuple(tap_base - tap_dir * 0.05), tuple(tap_end)], 0.034, BRASS, seg=16)
cyl("TapBonnet", (tap_end.x, tap_end.y, 1.17), 0.042, 0.13, BRASS, seg=16)
bar1 = box("TapHandleA", (tap_end.x, tap_end.y, 1.265), (0.17, 0.022, 0.022), IRON)
bar2 = box("TapHandleB", (tap_end.x, tap_end.y, 1.265), (0.022, 0.17, 0.022), IRON)
# spout: curves down and slightly out, bulbous pendant below the tip
sp = [tuple(tap_end), (tap_end.x - 0.03, tap_end.y - 0.035, 1.03),
      (tap_end.x - 0.045, tap_end.y - 0.055, 0.97), (tap_end.x - 0.045, tap_end.y - 0.055, 0.90)]
tube_path("TapSpout", sp, 0.026, BRASS, seg=14)
pend_prof = [(0.0001, 0.90), (0.016, 0.885), (0.042, 0.845), (0.048, 0.80),
             (0.036, 0.755), (0.0001, 0.735)]
pb = revolve("TapPendant", pend_prof, BRASS, seg=22)
pb.location = (tap_end.x - 0.045, tap_end.y - 0.055, 0)

# ------------------------------------------------- centre discharge valve + long rod
cyl("CentreValveBody", (-0.25, -1.03, 1.00), 0.052, 0.14, BRASS, seg=16, rot=(math.pi / 2, 0, 0))
torus("CentreWheel", (-0.25, -1.115, 1.03), 0.055, 0.011, IRON)
for s in range(3):
    a = s * math.pi / 3
    box(f"CentreSpoke_{s}", (-0.25, -1.115, 1.03), (0.105, 0.008, 0.012), IRON, rot=(0, 0, 0))
    bpy.context.object.rotation_euler = (0, 0, a)
    bpy.context.object.location = (-0.25, -1.115, 1.03)
cyl("CentreRod", (-0.25, -1.06, 0.52), 0.008, 0.78, STEEL, seg=10)
box("CentreGrip", (-0.25, -1.06, 0.135), (0.10, 0.016, 0.016), IRON)

# ------------------------------------------------- front-right valve stand
cyl("RightStandPipe", (0.55, -1.02, 0.46), 0.029, 0.92, IRON, seg=16)
cyl("RightStandBase", (0.55, -1.02, 0.03), 0.065, 0.06, IRON, seg=16)
cyl("RightBonnet", (0.55, -1.02, 0.985), 0.050, 0.13, BRASS, seg=18)
torus("RightBonnetRing", (0.55, -1.02, 0.95), 0.054, 0.010, BRASS)
torus("RightWheel", (0.55, -1.02, 1.085), 0.052, 0.010, IRON)
cyl("RightStem", (0.55, -1.02, 1.05), 0.013, 0.05, STEEL, seg=10)

# ------------------------------------------------- far-right valve stack
cyl("StackPipe", (1.48, -0.55, 0.76), 0.045, 1.52, IRON, seg=18)
cyl("StackBase", (1.48, -0.55, 0.035), 0.085, 0.07, IRON, seg=18)
for i, vz in enumerate((0.95, 1.22, 1.48)):
    ball(f"StackValve_{i}", (1.48, -0.55, vz), 0.066, BRASS, seg=16)
    torus(f"StackWheel_{i}", (1.48, -0.635, vz), 0.050, 0.010, IRON, rot=(math.pi / 2, 0, 0))
    cyl(f"StackStem_{i}", (1.48, -0.60, vz), 0.012, 0.07, STEEL, seg=10, rot=(math.pi / 2, 0, 0))
# horizontal connector from the pan to the stack
tube_path("StackConnector", [(0.94, -0.35, 1.05), (1.20, -0.46, 1.05), (1.46, -0.54, 1.05)],
          0.040, COPPER2, seg=16)

# ---------------------------------------------------------------- stats + save
bpy.ops.object.select_all(action='SELECT')
tris = 0
for ob in bpy.context.selected_objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print(f"OBJECTS: {len(bpy.data.objects)}  TRIANGLES: {tris}")

out = os.path.expanduser("~/workspace/cp-models/vacuum-sugar-apparatus")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "vacuum-sugar-apparatus.blend"))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "vacuum-sugar-apparatus.glb"),
                          export_format='GLB', export_apply=True)
print("SAVED blend + glb")
