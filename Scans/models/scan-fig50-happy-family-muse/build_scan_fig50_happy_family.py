# Build scan-fig50-happy-family (Muse version) — John Tenniel, "The Happy Family
# in Hyde Park", Punch 19 July 1851 (catalog fig. 50).
# As DRAWN (the image governs, not the picnic description in the brief): the
# nations of the world are penned together inside a tall barred cage beneath
# the Crystal Palace transept fan window, dancing in pairs on two levels,
# while large foreground spectators watch from outside the bars. Figures are
# dignified stylised forms in varied period/national dress silhouettes --
# no caricature features, no likenesses, no lettering.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vignette_common import *
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

SLUG = "scan-fig50-happy-family"
STEEL = mat("steel", (0.30, 0.31, 0.33), 0.45, 0.6)
FRAME = mat("framewood", (0.42, 0.33, 0.24), 0.8)
GLASS = mat("glass", (0.80, 0.88, 0.90), 0.2, 0.0, alpha=0.30)
BACK = mat("backdrop", (0.86, 0.85, 0.80), 0.95)

def beam(name, p1, p2, r, material):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    ob = cyl(name, (0, 0, 0), r, r, d.length, material, 10)
    ob.location = (p1 + p2) / 2
    ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    return ob

def half_disc(cx, cy, cz, R, material, thick=0.04, n=24):
    verts, faces = [], []
    for k in range(2):
        y = cy + k * thick
        verts.append((cx, y, cz))
        for i in range(n + 1):
            a = math.pi * i / n
            verts.append((cx + R * math.cos(a), y, cz + R * math.sin(a)))
    for i in range(n):
        faces.append((0, 1 + i, 2 + i))
        b0 = (n + 1) + 0
        faces.append((b0, b0 + 2 + i, b0 + 1 + i))
        faces.append((1 + i, (n + 1) + 1 + i, (n + 1) + 2 + i, 2 + i))
    me = bpy.data.meshes.new("fan_glass")
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new("fan_glass", me)
    bpy.context.collection.objects.link(ob)
    me.materials.append(material)
    return ob

ground(9.6, 6.4, (0.60, 0.58, 0.55), y_off=0.2)

# --- pale backdrop inside the cage so the dancers read against it ---
box("cage_back", (0, 2.05, 2.15), (8.5, 0.08, 4.3), BACK)

# --- The cage: front at y=1.2, width 8.4, top rail 4.3, mid rail 2.15 ---
cage_y = 1.2
for x in (-4.2, -2.8, -1.4, 0.0, 1.4, 2.8, 4.2):
    box("cage_post", (x, cage_y, 2.15), (0.11, 0.11, 4.3), FRAME)
for z in (0.07, 2.15, 4.24):
    box("cage_rail", (0, cage_y, z), (8.55, 0.09, 0.12), FRAME)
x = -4.02
while x <= 4.03:
    cyl("cage_bar", (x, cage_y, 2.15), 0.018, 0.018, 4.14, STEEL, 8)
    x += 0.24
for sgn in (-1, 1):  # short barred side returns
    for i in range(4):
        cyl("side_bar", (sgn * 4.25, cage_y - 0.22 - i * 0.24, 2.15), 0.016, 0.016, 4.1, STEEL, 8)
    box("side_rail", (sgn * 4.25, cage_y - 0.5, 4.24), (0.08, 1.1, 0.10), FRAME)
    box("side_rail2", (sgn * 4.25, cage_y - 0.5, 0.07), (0.08, 1.1, 0.10), FRAME)

# --- Transept fan window above: semicircle ONLY, hub at z=4.35, R=3.9 ---
hub = (0, 1.55, 4.35)
R = 3.9
prev = None
for i in range(25):
    a = math.pi * i / 24
    p = (R * math.cos(a), 1.55, 4.35 + R * math.sin(a))
    if prev is not None:
        beam("fan_rim", prev, p, 0.06, FRAME)
    prev = p
for a_deg in range(0, 181, 15):
    a = math.radians(a_deg)
    beam("fan_spoke", hub, (R * math.cos(a), 1.55, 4.35 + R * math.sin(a)), 0.028, FRAME)
# inner concentric arc
prev = None
for i in range(19):
    a = math.pi * i / 18
    p = (R * 0.62 * math.cos(a), 1.55, 4.35 + R * 0.62 * math.sin(a))
    if prev is not None:
        beam("fan_arc2", prev, p, 0.03, FRAME)
    prev = p
cyl("fan_hub", hub, 0.17, 0.17, 0.09, FRAME, 20, rot=(math.pi / 2, 0, 0))
half_disc(0, 1.58, 4.35, R - 0.06, GLASS)
box("fan_sill", (0, 1.5, 4.32), (8.6, 0.35, 0.14), FRAME)

# pennant flags at both top corners (blank, as all lettering/devices are omitted)
for sgn in (-1, 1):
    cyl("flag_pole", (sgn * 4.55, 1.3, 5.0), 0.02, 0.02, 1.7, STEEL, 8)
    tri_prism("flag", (sgn * 4.55, 1.3, 5.78), (sgn * 4.55, 1.3, 5.30),
              (sgn * 5.05, 1.3, 5.54), 0.014, mat("flagcloth" + str(sgn), (0.72, 0.70, 0.66), 0.9))

# --- Dancing pairs inside the cage ---
# upper tier: standing on a plinth step (base z=2.28), heads below the top rail
box("dance_step", (0, 1.68, 2.14), (7.9, 0.75, 0.28), mat("stepmat", (0.52, 0.48, 0.44), 0.9))
import vignette_common as _vc
_orig_person = _vc.person
def dancer(x, y, H, dress, coat, hat, zbase, name_p, arm_l, arm_r):
    # person() builds from z=0; lift EVERY object the call created to the tier
    # base (hat brims/spheres are not all parented to the group, so diff the
    # scene object set -- lifting only group children stranded the brims).
    before = set(bpy.context.scene.objects)
    g = _orig_person(x, y, H, dress, coat, hat, arm_l=arm_l, arm_r=arm_r, name_p=name_p)
    if zbase:
        # Lift only parentless new objects: the group empty (which carries
        # its parented children with it) and any loose hat parts. Lifting
        # children as well double-moves them.
        for ob in set(bpy.context.scene.objects) - before:
            if ob.parent is None:
                ob.location.z += zbase
    return g

pairs_up = [(-3.1, (0.45, 0.20, 0.22), "top", (0.25, 0.30, 0.48)),
            (-1.55, (0.20, 0.32, 0.28), "turban", (0.55, 0.45, 0.20)),
            (0.0, (0.48, 0.42, 0.30), "cap", (0.30, 0.42, 0.30)),
            (1.55, (0.24, 0.24, 0.40), "shako", (0.50, 0.28, 0.28)),
            (3.1, (0.36, 0.26, 0.20), "conical", (0.42, 0.34, 0.46))]
for i, (px, mc, mh, wc) in enumerate(pairs_up):
    dancer(px - 0.30, 1.66, 1.66, "man", mc, mh, 2.28, f"dmu{i}", (0.5, -0.6), (-0.4, 0.5))
    dancer(px + 0.30, 1.66, 1.58, "woman", wc, "bonnet", 2.28, f"dwu{i}", (-0.5, 0.5), (0.4, -0.6))
pairs_lo = [(-2.3, (0.35, 0.28, 0.20), "cap", (0.42, 0.30, 0.42)),
            (-0.4, (0.28, 0.22, 0.34), "top", (0.58, 0.50, 0.34)),
            (1.5, (0.40, 0.26, 0.18), "turban", (0.32, 0.46, 0.50)),
            (3.2, (0.30, 0.30, 0.30), "cap", (0.48, 0.36, 0.28))]
for i, (px, mc, mh, wc) in enumerate(pairs_lo):
    dancer(px - 0.29, 1.62, 1.70, "man", mc, mh, 0.0, f"dml{i}", (0.6, -0.5), (-0.3, 0.6))
    dancer(px + 0.29, 1.62, 1.62, "woman", wc, "bonnet", 0.0, f"dwl{i}", (-0.6, 0.6), (0.3, -0.5))

# --- Spectators in front of the bars (large in frame, as drawn) ---
person(-3.65, -1.15, 1.64, "woman", (0.40, 0.36, 0.38), "bonnet", name_p="sp1")
person(-2.95, -0.75, 1.78, "man", (0.22, 0.24, 0.34), "shako", name_p="sp3")
person(-3.25, -1.55, 1.74, "man", (0.32, 0.28, 0.24), "cap", name_p="sp2")
person(-1.95, -1.85, 1.76, "man", (0.55, 0.52, 0.48), "top", arm_r=(-0.2, 0.15), name_p="sp4")
cyl("cane", (-1.62, -1.92, 0.55), 0.013, 0.013, 1.1, mat("canemat", (0.30, 0.22, 0.14), 0.6), 8)
person(2.05, -1.55, 1.78, "man", (0.16, 0.15, 0.16), "none", arm_r=(-0.9, 0.3), name_p="sp5")
cyl("pointer", (1.55, -1.40, 1.08), 0.012, 0.012, 1.0, mat("pointermat", (0.35, 0.26, 0.16), 0.6), 8,
    rot=(0, math.radians(83), 0))
person(3.15, -1.35, 1.66, "woman", (0.66, 0.60, 0.55), "bonnet", name_p="sp6")
for rr, zz in ((0.30, 0.16), (0.26, 0.38), (0.22, 0.58)):
    cyl("flounce", (3.15, -1.35, zz), rr - 0.05, rr, 0.10, mat("flouncemat", (0.60, 0.54, 0.49), 0.9), 20)
person(0.25, -1.95, 1.12, "girl", (0.50, 0.44, 0.40), "bonnet", name_p="sp7")
person(-0.85, -1.35, 1.30, "girl", (0.44, 0.40, 0.44), "conical", name_p="sp8")

tris = finalise(SLUG, (0.4, -13.8, 4.8), (0, 0.7, 2.7), res=(880, 1100))
print("DONE", SLUG, tris)
