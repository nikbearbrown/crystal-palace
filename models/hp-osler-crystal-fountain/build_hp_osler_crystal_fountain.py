# build_hp_osler_crystal_fountain.py
# Osler crystal fountain, Hyde Park 1851 (SCENE-BUILD-PLAN Wave 2, item 7).
# Built to the research spike report: ../osler-spike-report.md, section 5.
#
# Controlling dimension: overall height 27 ft = 8.23 m, basin waterline to
# top of glass spout (Official Descriptive and Illustrated Catalogue 1851,
# Class XXIV, exhibit No. 20, F. & C. Osler). All tier levels/diameters are
# photo-derived fractions of that height measured from the Ferrier 1851
# plate (RCIN 2800080) -- see NOTES.md and refs/REFERENCES.md.
#
# Datum: z = 0 is the basin waterline (= surrounding floor level). The
# basin shell extends 0.20 m below z = 0 (pool depth). Origin at the
# centre of the basin. Units: metres. All objects are world-space
# geometry with identity transforms (unit scale, applied by construction).
#
# Re-runnable: blender -b -noaudio --python build_hp_osler_crystal_fountain.py
# Env knobs: OSLER_SAMPLES (Cycles samples, default 256),
#            OSLER_VIEWS (comma list of front,side,three-quarter).

import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = int(os.environ.get("OSLER_SAMPLES", "256"))
VIEWS = os.environ.get("OSLER_VIEWS", "front,side,three-quarter").split(",")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

model_col = bpy.data.collections.new("Model")
scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
scene.collection.children.link(setup_col)

# ---------------------------------------------------------------- materials
def principled(name, colour, rough, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*colour, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

def glass(name, rough):
    """Cut-crystal glass: full transmission, IOR 1.52. The cutting is
    geometry (fluted lathes, flat shading); the material stays clean."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["IOR"].default_value = 1.52
    try:
        bsdf.inputs["Transmission Weight"].default_value = 1.0
    except KeyError:
        bsdf.inputs["Transmission"].default_value = 1.0
    try:
        bsdf.inputs["Specular IOR Level"].default_value = 1.0
    except KeyError:
        pass
    return mat

MAT_GLASS   = glass("CutCrystalGlass", 0.055)      # main glass
MAT_GLASS_F = glass("CutCrystalGlassFine", 0.035)  # stems / nozzle (polished)
MAT_FROST   = glass("InscriptionBandFrosted", 0.28)  # blank inscription band
MAT_WATER   = principled("BasinWater", (0.030, 0.042, 0.050), 0.07)
MAT_STONE_D = principled("BasinStoneDark", (0.145, 0.135, 0.125), 0.72)
MAT_STONE_P = principled("StepStonePale", (0.52, 0.50, 0.47), 0.82)
MAT_BACK    = principled("BackdropGrey", (0.60, 0.60, 0.60), 0.95)

# ---------------------------------------------------------------- geometry helpers
def lathe(profile, segments, flutes=0, closed=False):
    """Revolve a profile around the Z axis.
    profile: list of (r, z) or (r, z, fr, fz); fr/fz = radial / vertical
    flute modulation amplitude (cos(flutes*theta)), for cut-glass fluting.
    r = 0 points become single axis vertices. Returns (verts, faces)."""
    prof = []
    for p in profile:
        prof.append((p[0], p[1],
                     p[2] if len(p) > 2 else 0.0,
                     p[3] if len(p) > 3 else 0.0))
    verts, rings = [], []
    for (r, z, fr, fz) in prof:
        if r <= 1e-6:
            rings.append([len(verts)])
            verts.append((0.0, 0.0, z))
        else:
            ring = []
            for j in range(segments):
                th = 2.0 * math.pi * j / segments
                fl = math.cos(flutes * th) if flutes else 0.0
                rr, zz = r + fr * fl, z + fz * fl
                ring.append(len(verts))
                verts.append((rr * math.cos(th), rr * math.sin(th), zz))
            rings.append(ring)
    faces = []
    pairs = [(i, i + 1) for i in range(len(prof) - 1)]
    if closed:
        pairs.append((len(prof) - 1, 0))
    for (i, k) in pairs:
        a, b = rings[i], rings[k]
        if len(a) == 1 and len(b) == 1:
            continue
        if len(a) == 1:
            p = a[0]
            for j in range(segments):
                faces.append((p, b[(j + 1) % segments], b[j]))
        elif len(b) == 1:
            p = b[0]
            for j in range(segments):
                faces.append((a[j], a[(j + 1) % segments], p))
        else:
            for j in range(segments):
                j1 = (j + 1) % segments
                faces.append((a[j], a[j1], b[j1], b[j]))
    return verts, faces

def xform(verts, azimuth=0.0, dx=0.0, dy=0.0, dz=0.0):
    if azimuth:
        c, s = math.cos(azimuth), math.sin(azimuth)
        verts = [(x * c - y * s, x * s + y * c, z) for (x, y, z) in verts]
    if dx or dy or dz:
        verts = [(x + dx, y + dy, z + dz) for (x, y, z) in verts]
    return verts

def add_mesh(name, verts, faces, material, smooth=False, cast_shadow=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    if material:
        mesh.materials.append(material)
    for poly in mesh.polygons:
        poly.use_smooth = smooth
    obj = bpy.data.objects.new(name, mesh)
    model_col.objects.link(obj)
    if not cast_shadow:
        try:
            obj.visible_shadow = False
        except Exception:
            pass
    return obj

def bezier(p0, p1, p2, t):
    u = 1.0 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])

def tube(name, p0, p1, p2, azimuth, r0, r1, material, samples=11, radial=8):
    """Tube along a quadratic Bezier lying in a radial-vertical plane at
    the given azimuth. (u, z) plane points; built in world coordinates."""
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    binormal = (-sa, ca, 0.0)
    pts = [bezier(p0, p1, p2, i / (samples - 1)) for i in range(samples)]
    verts, rings = [], []
    for i, (u, z) in enumerate(pts):
        if i == 0:
            du, dz = pts[1][0] - u, pts[1][1] - z
        elif i == samples - 1:
            du, dz = u - pts[i - 1][0], z - pts[i - 1][1]
        else:
            du, dz = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(du, dz) or 1.0
        nu, nz = -dz / L, du / L                      # in-plane normal
        n3 = (nu * ca, nu * sa, nz)
        rad = r0 + (r1 - r0) * (i / (samples - 1))
        centre = (u * ca, u * sa, z)
        ring = []
        for j in range(radial):
            a = 2.0 * math.pi * j / radial
            off = tuple(rad * (math.cos(a) * n3[k] + math.sin(a) * binormal[k])
                        for k in range(3))
            ring.append(len(verts))
            verts.append(tuple(centre[k] + off[k] for k in range(3)))
        rings.append(ring)
    faces = []
    for i in range(samples - 1):
        for j in range(radial):
            j1 = (j + 1) % radial
            faces.append((rings[i][j], rings[i][j1], rings[i + 1][j1], rings[i + 1][j]))
    # end caps (fans to centre points)
    for end, flip in ((0, True), (samples - 1, False)):
        u, z = pts[end]
        ci = len(verts); verts.append((u * ca, u * sa, z))
        for j in range(radial):
            j1 = (j + 1) % radial
            faces.append((ci, rings[end][j1], rings[end][j]) if flip
                         else (ci, rings[end][j], rings[end][j1]))
    return add_mesh(name, verts, faces, material, smooth=True, cast_shadow=False)

def ring_torus(name, radius, z, tube_r, material, segments=72):
    prof = [(radius + tube_r * math.cos(2 * math.pi * k / 8),
             z + tube_r * math.sin(2 * math.pi * k / 8)) for k in range(8)]
    v, f = lathe(prof, segments, closed=True)
    return add_mesh(name, v, f, material, smooth=True, cast_shadow=False)

# ---------------------------------------------------------------- basin + water
# Spike report sec.5.1: shallow circular pool, dia 7.32 m (24 ft, published;
# photo reads ~26-27 ft -- adopted published figure, +-10% in NOTES).
# Basin material undocumented: dark stone/metal rim, INFERRED (sec.6.3).
v, f = lathe([
    (0.00, -0.20), (3.55, -0.20), (3.64, -0.12), (3.66, 0.02),
    (3.66, 0.10), (3.58, 0.13), (3.50, 0.09), (3.44, -0.02),
    (3.38, -0.10), (0.00, -0.10)], 128)
add_mesh("Basin", v, f, MAT_STONE_D, smooth=True)

# Still water surface at the waterline (not a "playing" state; no plume).
v, f = lathe([(0.00, -0.005), (3.40, -0.005), (3.40, 0.002), (0.00, 0.002)], 96)
add_mesh("BasinWater", v, f, MAT_WATER, smooth=True, cast_shadow=False)

# Sec.5.2: two concentric steps, top step at the waterline.
v, f = lathe([(0.00, -0.10), (1.60, -0.10), (1.60, -0.04), (0.00, -0.04)], 96)
add_mesh("StepLower", v, f, MAT_STONE_P, smooth=True)
v, f = lathe([(0.00, -0.04), (1.38, -0.04), (1.38, 0.00), (0.00, 0.00)], 96)
add_mesh("StepUpper", v, f, MAT_STONE_P, smooth=True)

# ---------------------------------------------------------------- plinth drum
# Sec.5.3: dia 2.30 m, top at 1.06 m. Fluted body (generic period fluting,
# sec.6.5). Inscription band left BLANK (lettering only partly legible,
# "...LONDON" -- must not be completed by invention, sec.6.5).
v, f = lathe([
    (0.00, 0.00, 0, 0), (1.10, 0.00, 0, 0), (1.13, 0.04, 0.004, 0),
    (1.13, 0.10, 0.004, 0), (1.06, 0.17, 0.010, 0), (1.03, 0.26, 0.014, 0),
    (1.04, 0.45, 0.018, 0), (1.05, 0.62, 0.018, 0), (1.03, 0.78, 0.014, 0),
    (1.06, 0.86, 0.006, 0), (1.12, 0.94, 0.004, 0), (1.12, 1.00, 0.002, 0),
    (0.98, 1.06, 0, 0), (0.00, 1.06, 0, 0)], 112, flutes=28)
add_mesh("PlinthDrum", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

# Blank frosted inscription band, proud of the drum body (z 0.50-0.74).
v, f = lathe([(1.048, 0.50), (1.068, 0.50), (1.068, 0.74), (1.048, 0.74)], 112)
add_mesh("InscriptionBand", v, f, MAT_FROST, smooth=True, cast_shadow=False)

# Ring of small cup finials around the drum's upper rim (sec.5.3).
CUP = [(0.00, 0.00), (0.030, 0.00), (0.040, 0.015), (0.030, 0.035),
       (0.028, 0.050), (0.045, 0.085), (0.052, 0.105), (0.040, 0.115),
       (0.012, 0.062), (0.00, 0.058)]
for k in range(12):
    az = 2.0 * math.pi * k / 12
    v, f = lathe(CUP, 12)
    v = xform(v, dx=1.06 * math.cos(az), dy=1.06 * math.sin(az), dz=1.00)
    add_mesh(f"DrumFinial{k:02d}", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

# Fluted flare where the stem cage leaves the drum top (ornament read
# from the plate; junction dressing, cf. sec.5.4).
v, f = lathe([
    (0.52, 1.06, 0.010, 0), (0.50, 1.12, 0.012, 0), (0.42, 1.28, 0.012, 0),
    (0.35, 1.44, 0.010, 0), (0.315, 1.44, 0, 0), (0.375, 1.27, 0, 0),
    (0.455, 1.11, 0, 0), (0.475, 1.06, 0, 0)], 96, flutes=24)
add_mesh("CageBaseFlare", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

# ---------------------------------------------------------------- stem cage
# Sec.5.4: drum top 1.06 -> tier-1 dome underside 3.02. Rod count 8-12
# not certainly readable in the print -- 12 used, INFERRED (sec.6.4).
v, f = lathe([
    (0.00, 1.06), (0.13, 1.06), (0.13, 1.20), (0.09, 1.45), (0.085, 2.00),
    (0.09, 2.60), (0.12, 2.90), (0.16, 3.02), (0.00, 3.02)], 48)
add_mesh("CentralStem", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

ROD = [(0.00, 1.30), (0.028, 1.30), (0.024, 2.98), (0.00, 2.98)]
for k in range(12):
    az = 2.0 * math.pi * k / 12
    v, f = lathe(ROD, 8)
    v = xform(v, dx=0.40 * math.cos(az), dy=0.40 * math.sin(az))
    add_mesh(f"CageRod{k:02d}", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)
ring_torus("CageRingLow", 0.40, 1.52, 0.014, MAT_GLASS_F)
ring_torus("CageRingHigh", 0.40, 2.78, 0.014, MAT_GLASS_F)

# ---------------------------------------------------------------- tier 1
# Sec.5.5: dome dia 2.84 m, rim 3.25, underside junction 3.02;
# top bowl dia 2.25 m, rim 4.19, back to back on the dome's crown.
v, f = lathe([
    (0.00, 3.02, 0, 0), (0.45, 3.05, 0.006, 0), (0.90, 3.12, 0.012, 0),
    (1.25, 3.19, 0.016, 0), (1.40, 3.235, 0.018, 0.010),
    (1.42, 3.25, 0.018, 0.012), (1.38, 3.29, 0.018, 0.010),
    (1.20, 3.38, 0.016, 0), (0.85, 3.50, 0.012, 0), (0.45, 3.60, 0.006, 0),
    (0.00, 3.64, 0, 0)], 144, flutes=36)
add_mesh("Tier1Dome", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

v, f = lathe([
    (0.00, 3.56, 0, 0), (0.35, 3.58, 0.008, 0), (0.65, 3.66, 0.016, 0),
    (0.90, 3.82, 0.024, 0), (1.05, 4.02, 0.028, 0.008),
    (1.125, 4.19, 0.028, 0.020), (1.09, 4.185, 0.024, 0.016),
    (0.95, 4.00, 0.020, 0), (0.70, 3.80, 0.012, 0), (0.35, 3.68, 0.006, 0),
    (0.00, 3.66, 0, 0)], 140, flutes=28)
add_mesh("Tier1Bowl", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

# ---------------------------------------------------------------- cluster + tier 2
# Sec.5.6: branching cluster between tier-1 bowl and tier 2 -- arm
# geometry is decorative inference from the plate, INFERRED (sec.6.4).
v, f = lathe([
    (0.00, 3.70), (0.085, 3.70), (0.065, 4.10), (0.055, 4.50),
    (0.075, 4.85), (0.06, 5.20), (0.05, 5.45), (0.085, 5.58),
    (0.10, 5.63), (0.00, 5.63)], 48)
add_mesh("ClusterStem", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

BIGCUP = [(r * 1.5, z * 1.5) for (r, z) in CUP]
for k in range(6):
    az = 2.0 * math.pi * k / 6 + math.pi / 6
    tube(f"ClusterArm{k}", (0.05, 4.30), (0.42, 4.38), (0.55, 4.92),
         az, 0.021, 0.016, MAT_GLASS_F)
    v, f = lathe(BIGCUP, 16)
    v = xform(v, dx=0.55 * math.cos(az), dy=0.55 * math.sin(az), dz=4.92)
    add_mesh(f"ClusterCup{k}", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

# Sec.5.7: tier 2 -- dome dia 1.25 m, rim 5.73; top bowl dia 0.99 m, rim 6.23.
v, f = lathe([
    (0.00, 5.63, 0, 0), (0.20, 5.645, 0.003, 0), (0.40, 5.675, 0.006, 0),
    (0.55, 5.705, 0.008, 0), (0.615, 5.725, 0.010, 0.005),
    (0.625, 5.73, 0.010, 0.006), (0.605, 5.745, 0.010, 0.005),
    (0.53, 5.79, 0.008, 0), (0.375, 5.84, 0.006, 0), (0.20, 5.885, 0.003, 0),
    (0.00, 5.90, 0, 0)], 112, flutes=28)
add_mesh("Tier2Dome", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

v, f = lathe([
    (0.00, 5.86, 0, 0), (0.16, 5.87, 0.004, 0), (0.30, 5.92, 0.008, 0),
    (0.42, 6.03, 0.012, 0), (0.485, 6.16, 0.014, 0.005),
    (0.495, 6.23, 0.014, 0.010), (0.475, 6.225, 0.012, 0.008),
    (0.42, 6.10, 0.010, 0), (0.32, 5.99, 0.006, 0), (0.16, 5.93, 0.003, 0),
    (0.00, 5.92, 0, 0)], 96, flutes=24)
add_mesh("Tier2Bowl", v, f, MAT_GLASS, smooth=False, cast_shadow=False)

# ---------------------------------------------------------------- upper stem + spout
# Sec.5.8/5.9: baluster stem 6.23 -> spout 8.23, knop, crown of thin
# arched supports below the nozzle. Water plume EXCLUDED (sec.5.9).
v, f = lathe([
    (0.00, 5.95), (0.07, 5.95), (0.055, 6.30), (0.045, 6.70),
    (0.075, 6.90), (0.095, 6.98), (0.07, 7.08), (0.042, 7.30),
    (0.040, 7.70), (0.048, 7.95), (0.065, 8.06), (0.00, 8.06)], 48)
add_mesh("UpperStem", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

ROD2 = [(0.00, 6.45), (0.011, 6.45), (0.011, 7.92), (0.00, 7.92)]
for k in range(6):
    az = 2.0 * math.pi * k / 6
    v, f = lathe(ROD2, 8)
    v = xform(v, dx=0.13 * math.cos(az), dy=0.13 * math.sin(az))
    add_mesh(f"UpperRod{k}", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)
ring_torus("UpperRingLow", 0.13, 6.52, 0.008, MAT_GLASS_F)
ring_torus("UpperRingHigh", 0.13, 7.88, 0.008, MAT_GLASS_F)

for k in range(6):
    az = 2.0 * math.pi * k / 6 + math.pi / 6
    tube(f"CrownArch{k}", (0.045, 7.80), (0.26, 7.86), (0.05, 8.12),
         az, 0.009, 0.009, MAT_GLASS_F, samples=9)

v, f = lathe([
    (0.00, 8.04), (0.052, 8.04), (0.046, 8.10), (0.024, 8.15),
    (0.030, 8.19), (0.014, 8.215), (0.00, 8.23)], 32)
add_mesh("SpoutNozzle", v, f, MAT_GLASS_F, smooth=True, cast_shadow=False)

# ---------------------------------------------------------------- render setup
world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9

def add_plane(name, size, z, material):
    mesh = bpy.data.meshes.new(name); s = size / 2
    mesh.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
    mesh.update(); obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material); setup_col.objects.link(obj); return obj

add_plane("Backdrop", 400, -0.205, MAT_BACK)

def add_light(name, ltype, loc, energy, size=None):
    data = bpy.data.lights.new(name, ltype); data.energy = energy
    if size: data.shape = 'DISK'; data.size = size
    obj = bpy.data.objects.new(name, data); obj.location = loc
    setup_col.objects.link(obj); return obj

sun = add_light("Sun", 'SUN', (5, -4, 9), 3.0)
sun.rotation_euler = (math.radians(52), 0, math.radians(38))
add_light("SoftAbove", 'AREA', (0.5, -0.5, 11.0), 900, size=8.0)
fill = add_light("Fill", 'AREA', (-8, 4, 4), 500, size=6.0)
fill.rotation_euler = (math.radians(65), 0, math.radians(-115))

# Emissive softboxes: invisible to the camera, visible to glossy /
# transmission rays -- they put the bright streaks into the glass that
# make cut crystal read as crystal rather than grey plastic.
def softbox(name, loc, rot, sx, sy, strength):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(-sx / 2, -sy / 2, 0), (sx / 2, -sy / 2, 0),
                      (sx / 2, sy / 2, 0), (-sx / 2, sy / 2, 0)], [], [(0, 1, 2, 3)])
    mesh.update()
    mat = bpy.data.materials.new(name + "Mat"); mat.use_nodes = True
    em = mat.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (1, 1, 1, 1); em.inputs[1].default_value = strength
    mat.node_tree.links.new(em.outputs[0], mat.node_tree.nodes["Material Output"].inputs[0])
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh); obj.location = loc
    obj.rotation_euler = rot; setup_col.objects.link(obj)
    for attr in ("visible_camera", "visible_shadow"):
        if hasattr(obj, attr):
            setattr(obj, attr, False)
    return obj

softbox("SoftboxFront", (0, -7.5, 5.0), (math.radians(90), 0, 0), 10, 6, 4.0)
softbox("SoftboxLeft", (-7.5, 2.0, 5.5), (math.radians(90), 0, math.radians(90)), 8, 6, 3.0)
softbox("SoftboxRight", (7.5, 2.0, 5.5), (math.radians(90), 0, math.radians(-90)), 8, 6, 3.0)
softbox("SoftboxTop", (0, 0, 12.5), (0, 0, 0), 9, 9, 3.0)

def look_at(cam, target):
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector(target) - cam.location).to_track_quat('-Z', 'Y')

def add_cam(name, loc, target, ortho=None, lens=40):
    data = bpy.data.cameras.new(name)
    if ortho: data.type = 'ORTHO'; data.ortho_scale = ortho
    else: data.lens = lens
    obj = bpy.data.objects.new(name, data); obj.location = loc
    setup_col.objects.link(obj); look_at(obj, target); return obj

tgt = (0, 0, 4.0)
cams = {
    # Blender ortho_scale is the HORIZONTAL extent at this aspect, so
    # 11.6 gives 8.7 m vertically -- enough for -0.20 .. 8.23.
    "front":         add_cam("CamFront", (0, -24, 4.0), tgt, ortho=11.6),
    "side":          add_cam("CamSide", (24, 0, 4.0), tgt, ortho=11.6),
    "three-quarter": add_cam("Cam34", (9.0, -12.0, 5.6), (0, 0, 3.85), lens=40),
}

scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
try: scene.cycles.device = 'CPU'
except Exception: pass
scene.cycles.max_bounces = 16
scene.cycles.transmission_bounces = 12
scene.cycles.transparent_max_bounces = 12
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 8
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False

# ---------------------------------------------------------------- save / export / render
blend_path = os.path.join(HERE, "hp-osler-crystal-fountain.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action='DESELECT')
for obj in model_col.objects: obj.select_set(True)
bpy.context.view_layer.objects.active = model_col.objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, "hp-osler-crystal-fountain.glb"),
                          export_format='GLB', use_selection=True)

def tri_count(col):
    return sum(len(p.vertices) - 2 for o in col.objects
               if o.type == 'MESH' for p in o.data.polygons)

zs = [v[2] for o in model_col.objects if o.type == 'MESH'
      for v in [tuple(vv.co) for vv in o.data.vertices]]
print(f"MODEL: {len(model_col.objects)} objects, {tri_count(model_col)} tris")
print(f"Z range: {min(zs):.3f} .. {max(zs):.3f} (spout top must be 8.230)")

os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
for name in VIEWS:
    scene.camera = cams[name]
    scene.render.filepath = os.path.join(HERE, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
print("DONE")
