# Build scan-fig51-peace (Muse version) — "Peace! — A Sketch from the Crystal
# Palace", Punch 5 July 1851 (catalog fig. 51).
# As DRAWN: a single cannon on its carriage displayed under a scalloped canopy
# at the "Great Peace Festival", attended by two tall soldiers, while a crowd
# of bonneted schoolgirls in aprons and their chaperone look on. (The brief's
# armour-stands guess is not in the image; there are no armour stands.)
# Stylised dignified figures only; no lettering.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vignette_common import *

bpy.ops.wm.read_factory_settings(use_empty=True)

SLUG = "scan-fig51-peace"
IRON = mat("iron", (0.16, 0.16, 0.17), 0.45, 0.55)
BRONZE = mat("bronze", (0.30, 0.26, 0.18), 0.38, 0.7)
WOOD = mat("carriagewood", (0.36, 0.25, 0.15), 0.75)
CANVAS = mat("canvas", (0.80, 0.76, 0.68), 0.95)

ground(8.0, 5.0, (0.60, 0.58, 0.55), y_off=0.1)

# --- Canopy over the exhibit ---
for x in (-2.9, 2.9):
    for y in (0.5, 2.3):
        cyl("canopy_post", (x, y, 1.8), 0.05, 0.05, 3.6, mat("postwood", (0.45, 0.36, 0.26), 0.8), 12)
box("canopy_roof", (0, 1.4, 3.66), (6.3, 2.3, 0.10), CANVAS)
x = -2.9
while x <= 2.91:
    sphere("valance", (x, 0.30, 3.44), (0.18, 0.06, 0.18), CANVAS, 12)
    x += 0.36
box("valance_band", (0, 0.30, 3.58), (6.1, 0.05, 0.14), CANVAS)
# plain draped backdrop panel behind the exhibit (blank)
box("backdrop", (0, 2.42, 1.9), (6.1, 0.06, 3.5), mat("drape", (0.74, 0.70, 0.64), 0.95))

# --- Cannon: barrel pointing right, two-wheel carriage, centre-right ---
barrel_y = 1.30
cyl("barrel", (0.95, barrel_y, 1.30), 0.085, 0.125, 2.5, BRONZE, 24, rot=(0, math.pi / 2, 0))
cyl("muzzle_ring", (2.14, barrel_y, 1.30), 0.115, 0.115, 0.14, BRONZE, 24, rot=(0, math.pi / 2, 0))
cyl("breech_ring", (-0.22, barrel_y, 1.30), 0.145, 0.145, 0.16, BRONZE, 24, rot=(0, math.pi / 2, 0))
sphere("cascabel", (-0.44, barrel_y, 1.30), (0.075, 0.075, 0.075), BRONZE, 14)
for sgn in (-1, 1):
    wy = barrel_y + sgn * 0.44
    torus("wheel_rim", (0.70, wy, 1.04), 0.54, 0.045, WOOD, rot=(math.pi / 2, 0, 0), major=28)
    cyl("wheel_hub", (0.70, wy, 1.04), 0.10, 0.10, 0.10, IRON, 16, rot=(math.pi / 2, 0, 0))
    for k in range(6):
        a = math.radians(k * 30)
        ob = box("wheel_spoke", (0, 0, 0), (0.05, 0.05, 1.0), WOOD)
        ob.location = (0.70, wy, 1.04)
        ob.rotation_euler = (a, 0, 0)
box("cheek_l", (0.60, barrel_y - 0.32, 1.07), (1.2, 0.08, 0.5), WOOD)
box("cheek_r", (0.60, barrel_y + 0.32, 1.07), (1.2, 0.08, 0.5), WOOD)
box("trail", (-0.85, barrel_y, 0.44), (1.6, 0.16, 0.14), WOOD, rot=(0, math.radians(-32), 0))
for sx, sz in ((2.30, 0.09), (2.50, 0.09), (2.40, 0.26)):
    sphere("shot", (sx, 1.95, sz), (0.09, 0.09, 0.09), IRON, 14)

# --- Two tall soldiers guarding the piece (left of it, as drawn) ---
person(-1.75, 1.65, 1.88, "man", (0.20, 0.22, 0.30), "shako", arm_l=(0.55, 0.1), name_p="sold1")
person(-1.10, 1.75, 1.90, "man", (0.24, 0.20, 0.20), "shako", name_p="sold2")

# --- Crowd of bonneted schoolgirls, mostly BACKS to viewer as drawn (fdir=+1,
# facing the cannon; their aprons are on the far side). The two girls at the
# left edge turn outward in the print, so they face the viewer (fdir=-1). ---
crowd = [(-3.30, -0.85, 1.52, (0.30, 0.28, 0.34), -1),
         (-2.72, -1.05, 1.38, (0.42, 0.32, 0.30), -1),
         (-2.12, -0.80, 1.34, (0.26, 0.32, 0.38), 1),
         (-1.50, -1.15, 1.28, (0.44, 0.38, 0.30), 1),
         (-0.90, -0.85, 1.44, (0.34, 0.30, 0.38), 1),
         (-0.30, -1.20, 1.36, (0.34, 0.26, 0.30), 1),
         (0.35, -0.95, 1.42, (0.28, 0.34, 0.28), 1),
         (1.00, -1.20, 1.32, (0.40, 0.30, 0.36), 1),
         (1.65, -0.90, 1.26, (0.32, 0.38, 0.42), 1),
         (2.20, -1.15, 1.16, (0.46, 0.36, 0.28), 1),
         (2.68, -0.85, 1.06, (0.36, 0.30, 0.32), 1)]
for i, (px, py, ph, pc, fd) in enumerate(crowd):
    person(px, py, ph, "girl", pc, "bonnet", name_p=f"crowd{i}", fdir=fd)
# adult chaperone at the right edge, as drawn
person(3.35, -0.50, 1.70, "woman", (0.38, 0.34, 0.36), "bonnet", name_p="chap", fdir=1)

tris = finalise(SLUG, (0.3, -8.8, 3.2), (0, 0.8, 1.45), res=(1024, 768))
print("DONE", SLUG, tris)
