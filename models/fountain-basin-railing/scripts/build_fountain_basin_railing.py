#!/usr/bin/env python3
"""
Fountain-basin railing — Crystal Palace (Osler Crystal Fountain basin screen).

Procedural build, Blender 4.2, headless.
Source: MET photograph DP238264 (CC0), "View of Transept, Looking South" —
the curved railing with floral cast panels fills the foreground.
The panel motif is a schematic INTERPRETATION read from that photograph
(central radial flower in an oval wreath, vine scrolls, leaf forms,
knob bands, finialed posts). It is not a foundry-exact pattern.

Geometry: 90-degree quadrant, 4 bays, radius R (inferred, see NOTES.md).
Origin at the centre of the arc's circle, floor at z = 0, metres.
"""
import bpy
import math
import os
import sys
from mathutils import Vector

# ----------------------------------------------------------------------------
# Parameters (metres)
# ----------------------------------------------------------------------------
R = 3.5                 # basin radius — INFERRED (see NOTES.md)
BAYS = 4
ARC = math.radians(90)  # total arc
BAY_ANG = ARC / BAYS
TOTAL_H = 1.07          # top of handrail — inferred anchor height
PANEL_Z0 = 0.26         # panel frame bottom
PANEL_Z1 = 0.90         # panel frame top
POST_R = 0.036

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Scene reset
# ----------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ----------------------------------------------------------------------------
# Material — dark painted cast iron (as it reads in the photograph)
# ----------------------------------------------------------------------------
def make_iron():
    mat = bpy.data.materials.new("CastIronDark")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.035, 0.038, 0.036, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.65
    bsdf.inputs["Roughness"].default_value = 0.52
    return mat

IRON = make_iron()

def link_obj(obj):
    bpy.context.collection.objects.link(obj)
    for poly in obj.data.polygons:
        poly.use_smooth = False
    if obj.data.materials:
        pass
    obj.data.materials.append(IRON)
    return obj

def mesh_obj(name, verts, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    return link_obj(ob)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def arc_prism(name, r_mid, width, z0, z1, a0, a1, segs=12):
    """Annular-sector prism (curved flat rail) centred on origin."""
    r_in, r_out = r_mid - width / 2, r_mid + width / 2
    verts, faces = [], []
    for i in range(segs + 1):
        a = a0 + (a1 - a0) * i / segs
        ca, sa = math.cos(a), math.sin(a)
        verts += [(r_in * ca, r_in * sa, z0), (r_out * ca, r_out * sa, z0),
                  (r_in * ca, r_in * sa, z1), (r_out * ca, r_out * sa, z1)]
    for i in range(segs):
        b = i * 4
        faces += [(b, b + 4, b + 5, b + 1),          # bottom
                  (b + 2, b + 3, b + 7, b + 6),      # top
                  (b, b + 2, b + 6, b + 4),          # inner
                  (b + 1, b + 5, b + 7, b + 3)]      # outer
    faces += [(0, 1, 3, 2),
              ((segs) * 4, (segs) * 4 + 2, (segs) * 4 + 3, (segs) * 4 + 1)]
    return mesh_obj(name, verts, faces)

def arc_tube(name, r_mid, tube_r, z, a0, a1, segs=24, sides=10, squash=0.82):
    """Round-profile rail following the arc (torus segment)."""
    verts, faces = [], []
    for i in range(segs + 1):
        a = a0 + (a1 - a0) * i / segs
        ca, sa = math.cos(a), math.sin(a)
        for j in range(sides):
            t = 2 * math.pi * j / sides
            rr = r_mid + tube_r * math.cos(t)
            verts.append((rr * ca, rr * sa, z + tube_r * squash * math.sin(t)))
    faces = []
    for i in range(segs):
        for j in range(sides):
            jn = (j + 1) % sides
            a_ = i * sides + j
            b_ = (i + 1) * sides + j
            c_ = (i + 1) * sides + jn
            d_ = i * sides + jn
            faces.append((a_, b_, c_, d_))
    return mesh_obj(name, verts, faces)

def lathe(name, profile, segments=14, centre=(0.0, 0.0)):
    """Spin a (r, z) profile around the z axis at centre (x, y)."""
    cx, cy = centre
    verts, faces = [], []
    n = len(profile)
    for (r, z) in profile:
        for j in range(segments):
            a = 2 * math.pi * j / segments
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(segments):
            jn = (j + 1) % segments
            faces.append((i * segments + j, (i + 1) * segments + j,
                          (i + 1) * segments + jn, i * segments + jn))
    ob = mesh_obj(name, verts, faces)
    # cap top/bottom with triangle fans via extra faces to a centroid
    return ob

def curve_tube(name, pts, radius, bevel_res=1, res=6):
    """Tube along a 3D polyline/spline given as Vector list (already in place)."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = bevel_res
    cu.resolution_u = res
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.active_object
    ob.data.materials.append(IRON)
    ob.select_set(False)
    return ob

def ball(name, loc, scale, seg=10, rings=7):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings,
                                         location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(IRON)
    return ob

# ----------------------------------------------------------------------------
# Knob (small turned bud ornament for the bands above/below the panel)
# ----------------------------------------------------------------------------
KNOB_PROFILE = [(0.0, 0.0), (0.013, 0.0), (0.007, 0.012), (0.006, 0.03),
                (0.020, 0.045), (0.026, 0.06), (0.018, 0.078), (0.006, 0.09),
                (0.0, 0.098)]

def _knob_at(x, y, z_base):
    prof = [(r, z + z_base) for (r, z) in KNOB_PROFILE]
    return lathe("Knob", prof, segments=8, centre=(x, y))

# ----------------------------------------------------------------------------
# Post with spire-and-ring finial (read from the photograph)
# ----------------------------------------------------------------------------
POST_PROFILE = [(0.0, 0.0), (0.078, 0.0), (0.078, 0.045), (0.052, 0.065),
                (0.040, 0.10), (0.034, 0.22), (0.046, 0.26), (0.046, 0.30),
                (0.034, 0.34), (0.034, 0.78), (0.047, 0.82), (0.047, 0.86),
                (0.035, 0.90), (0.035, 1.00), (0.052, 1.03), (0.052, 1.06),
                (0.020, 1.09), (0.014, 1.12)]

def build_post(a):
    x, y = R * math.cos(a), R * math.sin(a)
    lathe("Post", POST_PROFILE, segments=14, centre=(x, y))
    # ring (torus, plane tangent to the arc) above the post top
    bpy.ops.mesh.primitive_torus_add(major_radius=0.040, minor_radius=0.010,
                                     major_segments=14, minor_segments=6,
                                     location=(x, y, 1.175))
    ring = bpy.context.active_object
    ring.name = "PostRing"
    # torus axis (default Z) -> radial direction, so the ring's plane is the
    # tangent-vertical plane and the loop reads face-on from outside the arc
    ring.rotation_euler = (0, math.radians(90), a)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    ring.data.materials.append(IRON)
    # spire: slim cone through the ring
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.020, radius2=0.0,
                                    depth=0.24, location=(x, y, 1.20))
    spire = bpy.context.active_object
    spire.name = "PostSpire"
    spire.data.materials.append(IRON)
    # small ball at spire base
    ball("PostBall", (x, y, 1.10), (0.020, 0.020, 0.020), seg=8, rings=6)

# ----------------------------------------------------------------------------
# One floral panel, built FLAT in local coords then bent onto the arc.
# Local: x across the bay chord [-W/2, W/2], y = thickness, z up.
# ----------------------------------------------------------------------------
PANEL_W = 1.30           # flat width between post centrelines minus posts
PANEL_T = 0.030          # cast thickness

def bend(ob, r_bend=R):
    """Bend a flat object (built around x=0, y=0) onto radius r_bend.
    After bending, the panel centre sits at (0, R, z), spanning angles
    around the +Y direction (pi/2)."""
    me = ob.data
    for v in me.vertices:
        x, y, z = v.co
        ang = x / r_bend
        rr = r_bend + y
        v.co = (rr * math.sin(ang), rr * math.cos(ang), z)
    me.update()

def panel_parts():
    """Return list of objects forming one flat panel, centred at origin."""
    parts = []
    zc = (PANEL_Z0 + PANEL_Z1) / 2
    ph = PANEL_Z1 - PANEL_Z0
    # frame: top / bottom rails + side stiles (boxes)
    def box(name, sx, sy, sz, loc):
        bpy.ops.mesh.primitive_cube_add(location=loc)
        ob = bpy.context.active_object
        ob.name = name
        ob.dimensions = (sx, sy, sz)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob.data.materials.append(IRON)
        parts.append(ob)
        return ob
    box("PanelRailTop", PANEL_W, PANEL_T, 0.05, (0, 0, PANEL_Z1 - 0.025))
    box("PanelRailBot", PANEL_W, PANEL_T, 0.05, (0, 0, PANEL_Z0 + 0.025))
    box("PanelStileL", 0.04, PANEL_T, ph, (-PANEL_W / 2 + 0.02, 0, zc))
    box("PanelStileR", 0.04, PANEL_T, ph, (PANEL_W / 2 - 0.02, 0, zc))
    # centre cross (strong vertical + horizontal axes read in the photograph)
    box("PanelCrossV", 0.020, 0.016, ph - 0.06, (0, -0.002, zc))
    box("PanelCrossH", PANEL_W - 0.08, 0.016, 0.020, (0, -0.002, zc))

    # oval wreath ring (ellipse tube)
    pts = []
    NA, NB = 0.53, 0.25
    for i in range(41):
        t = 2 * math.pi * i / 40
        pts.append(Vector((NA * math.cos(t), 0, zc + NB * math.sin(t))))
    parts.append(curve_tube("OvalRing", pts, 0.017, res=2))
    # inner small ring
    pts = []
    for i in range(25):
        t = 2 * math.pi * i / 24
        pts.append(Vector((0.105 * math.cos(t), 0.004, zc + 0.105 * math.sin(t))))
    parts.append(curve_tube("InnerRing", pts, 0.010, res=2))
    # central boss
    parts.append(ball("Boss", (0, 0.006, zc), (0.048, 0.014, 0.048), seg=12, rings=8))

    # radial petals — TWO rings of narrow, slightly swept petals, so the
    # flower reads as dense as it does in the photograph
    def petal_at(phi, r0, r1, width, tilt=0.22):
        mid = (r0 + r1) / 2
        length = (r1 - r0)
        cx, cz = mid * math.cos(phi), zc + mid * math.sin(phi)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5,
                                             location=(cx, 0.004, cz))
        petal = bpy.context.active_object
        petal.name = "Petal"
        petal.scale = (length / 2, 0.010, width)
        petal.rotation_euler = (0, -(phi + tilt), 0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        petal.rotation_euler = (0, -(phi + tilt), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        petal.data.materials.append(IRON)
        parts.append(petal)

    for k in range(16):
        phi = 2 * math.pi * k / 16
        er = (NA * NB) / math.sqrt((NB * math.cos(phi)) ** 2 + (NA * math.sin(phi)) ** 2)
        petal_at(phi, 0.10, er * 0.86, 0.021)
    for k in range(16):
        phi = 2 * math.pi * (k + 0.5) / 16
        er = (NA * NB) / math.sqrt((NB * math.cos(phi)) ** 2 + (NA * math.sin(phi)) ** 2)
        petal_at(phi, 0.105, min(0.175, er * 0.5), 0.016, tilt=0.34)

    # corner scrolls — flat spirals in the four corners
    for sx_ in (-1, 1):
        for sz_ in (-1, 1):
            cx = sx_ * (PANEL_W / 2 - 0.165)
            cz = zc + sz_ * (ph / 2 - 0.095)
            pts = []
            turns, steps = 1.8, 22
            for i in range(steps + 1):
                t = turns * 2 * math.pi * i / steps
                rr = 0.014 + 0.080 * (i / steps)
                pts.append(Vector((cx + sx_ * rr * math.cos(t), 0,
                                   cz + sz_ * rr * math.sin(t))))
            parts.append(curve_tube("CornerScroll", pts, 0.0105, res=2))
            # tendril from scroll toward the oval
            mx = sx_ * (PANEL_W / 2 - 0.32)
            mz = zc + sz_ * (ph / 2 - 0.17)
            pts = [Vector((cx - sx_ * 0.06, 0, cz)),
                   Vector((mx, 0, mz)),
                   Vector((sx_ * 0.44, 0, zc + sz_ * 0.155))]
            parts.append(curve_tube("Tendril", pts, 0.0085, res=3))

    # shallow S-tendrils running inside the top and bottom frame edges
    for sz_ in (-1, 1):
        zt = zc + sz_ * (ph / 2 - 0.062)
        pts = [Vector((-0.46, 0, zt)),
               Vector((-0.22, 0, zt - sz_ * 0.028)),
               Vector((0.0, 0, zt)),
               Vector((0.22, 0, zt - sz_ * 0.028)),
               Vector((0.46, 0, zt))]
        parts.append(curve_tube("EdgeTendril", pts, 0.008, res=3))

    # leaves — small flattened lens shapes on the scrolls / oval edge
    leaf_spots = []
    for sx_ in (-1, 1):
        for sz_ in (-1, 1):
            leaf_spots += [(sx_ * 0.545, zc + sz_ * 0.10, 0.5 * sx_ * sz_),
                           (sx_ * 0.40, zc + sz_ * 0.245, -0.4 * sx_),
                           (sx_ * 0.185, zc + sz_ * 0.27, 0.9 * sz_)]
    leaf_spots += [(0.0, zc + 0.27, 0.0), (0.0, zc - 0.27, 0.0),
                   (0.545, zc, 1.2), (-0.545, zc, -1.2)]
    for (lx, lz, rot) in leaf_spots:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5,
                                             location=(lx, 0.002, lz))
        leaf = bpy.context.active_object
        leaf.name = "Leaf"
        leaf.scale = (0.020, 0.009, 0.052)
        leaf.rotation_euler = (0, rot, 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        leaf.data.materials.append(IRON)
        parts.append(leaf)
    return parts

# ----------------------------------------------------------------------------
# Build the quadrant: arc a in [0, 90 deg]; rotate so bisector faces -Y later.
# Panels are bent around origin at radius R.
# ----------------------------------------------------------------------------
all_objs = []

# floor curb (continuous)
all_objs.append(arc_prism("Curb", R, 0.16, 0.0, 0.05, 0, ARC, segs=36))
# bottom rail + mid rails for knob bands (continuous arcs)
all_objs.append(arc_prism("BottomRail", R, 0.055, 0.075, 0.135, 0, ARC, segs=36))
all_objs.append(arc_prism("LowerBandRail", R, 0.035, 0.155, 0.185, 0, ARC, segs=36))
all_objs.append(arc_prism("UpperBandRail", R, 0.035, 0.925, 0.955, 0, ARC, segs=36))
# handrail (rounded tube on the arc)
all_objs.append(arc_tube("Handrail", R, 0.034, 1.032, 0, ARC, segs=48, sides=8))

# knobs along both bands
spacing = 0.165
n_knobs = int(ARC * R / spacing)
for i in range(n_knobs + 1):
    a = ARC * i / n_knobs
    all_objs.append(_knob_at(R * math.cos(a), R * math.sin(a), 0.175))
    all_objs.append(_knob_at(R * math.cos(a), R * math.sin(a), 0.932))

# posts at bay boundaries
for i in range(BAYS + 1):
    build_post(i * BAY_ANG)

# panels: build flat, bend onto the arc, rotate to bay centres.
# After bend() a panel spans angles around pi/2 (the +Y direction);
# rotating by (mid - pi/2) about Z centres it on the bay mid-angle.
import mathutils
for i in range(BAYS):
    parts = panel_parts()
    for ob in parts:
        bend(ob)
    mid = (i + 0.5) * BAY_ANG
    M = mathutils.Matrix.Rotation(mid - math.pi / 2, 4, 'Z')
    for ob in parts:
        ob.matrix_world = M @ ob.matrix_world
    bpy.context.view_layer.update()
    for ob in parts:
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        ob.select_set(False)
    all_objs += parts

# ----------------------------------------------------------------------------
# Join everything into one object, apply transforms, centre origin at circle
# centre (already), base at z=0 (already).
# ----------------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.context.collection.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = bpy.context.collection.objects[0]
if len(bpy.context.collection.objects) > 1:
    bpy.ops.object.join()
model = bpy.context.active_object
model.name = "FountainBasinRailing"
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# stats
me = model.data
tris = sum(max(0, len(p.vertices) - 2) for p in me.polygons)
print(f"MODEL tris={tris} verts={len(me.vertices)} dims={tuple(round(d,3) for d in model.dimensions)}")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "fountain-basin-railing.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, "fountain-basin-railing.glb"),
                          export_format='GLB', export_apply=True)
print("SAVED blend + glb")
