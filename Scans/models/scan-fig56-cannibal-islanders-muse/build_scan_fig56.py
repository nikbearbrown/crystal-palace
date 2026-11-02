# Build scan-fig56-cannibal-islanders (Muse version).
# Source: a coloured 1851 refreshment-room caricature, presented in the source book as an
# example of racialized stereotyping of foreign visitors. The model preserves ONLY the
# scene's composition — diners at a laid round table, two attendants standing behind —
# with all figures rendered as dignified, neutral, stylised silhouettes. No caricature
# features of any kind are reproduced.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vignette_common import *

bpy.ops.wm.read_factory_settings(use_empty=True)

SLUG = "scan-fig56-cannibal-islanders"
CLOTH = mat("tablecloth", (0.93, 0.92, 0.89), 0.95)
PORC = mat("porcelain", (0.95, 0.94, 0.92), 0.35)
GLASSM = mat("glassware", (0.82, 0.88, 0.88), 0.2)

ground(6.4, 4.8, (0.58, 0.55, 0.52), y_off=0.1)
# refreshment-room hint: plain rear wall panel + serving sideboard
box("rear_wall", (0, 2.35, 1.7), (6.4, 0.10, 3.4), mat("wallmat", (0.72, 0.68, 0.62), 0.95))
box("sideboard", (-2.35, 1.95, 0.85), (1.5, 0.45, 1.1), mat("sidewood", (0.40, 0.28, 0.17), 0.75))
for i, px in enumerate((-2.65, -2.35, -2.05)):
    cyl("side_plate", (px, 1.95, 1.48), 0.13, 0.10, 0.03, PORC, 18, rot=(0.35, 0, 0))
cyl("side_ewer", (-2.35, 1.80, 1.62), 0.05, 0.09, 0.24, mat("metalware", (0.62, 0.60, 0.56), 0.3, 0.8), 14)

# --- Round table, cloth to the floor, centre (0, 0.15) ---
TX, TY = 0.0, 0.15
cyl("table_cloth", (TX, TY, 0.42), 1.02, 1.14, 0.84, CLOTH, 28)
cyl("table_top", (TX, TY, 0.86), 1.06, 1.06, 0.05, CLOTH, 28)
# centrepiece: joint of meat on an oval platter
sphere("platter", (TX, TY, 0.92), (0.34, 0.24, 0.035), PORC, 20)
sphere("joint", (TX, TY, 1.00), (0.24, 0.15, 0.11), mat("roast", (0.48, 0.30, 0.20), 0.7), 18)
cyl("joint_bone", (TX + 0.22, TY, 1.03), 0.022, 0.022, 0.16, mat("bone", (0.92, 0.90, 0.84), 0.6), 10,
    rot=(0, math.radians(70), 0))
# ewer / water jug
cyl("ewer_body", (TX - 0.55, TY - 0.35, 1.02), 0.045, 0.085, 0.26, mat("ewer", (0.66, 0.64, 0.60), 0.3, 0.8), 14)
torus("ewer_handle", (TX - 0.47, TY - 0.35, 1.04), 0.07, 0.014, mat("ewer2", (0.66, 0.64, 0.60), 0.3, 0.8),
      rot=(0, math.pi / 2, 0))
# wine bottle + glasses + plates + rolls around the table
cyl("bottle", (TX + 0.45, TY + 0.42, 1.00), 0.018, 0.05, 0.26, mat("bottle", (0.14, 0.22, 0.16), 0.25), 12)
for k in range(6):
    a = math.radians(k * 60 + 25)
    px, py = TX + 0.78 * math.cos(a), TY + 0.78 * math.sin(a)
    cyl("plate", (px, py, 0.905), 0.115, 0.09, 0.025, PORC, 18)
    gx, gy = TX + 0.58 * math.cos(a + 0.35), TY + 0.58 * math.sin(a + 0.35)
    cyl("glass", (gx, gy, 0.95), 0.032, 0.02, 0.10, GLASSM, 10)
    rx, ry = TX + 0.90 * math.cos(a - 0.4), TY + 0.90 * math.sin(a - 0.4)
    sphere("roll", (rx, ry, 0.92), (0.055, 0.04, 0.035), mat("bread", (0.76, 0.60, 0.38), 0.9), 10)

# --- Six diners seated around the table (neutral silhouettes, varied plain dress) ---
diner_specs = [(200, (0.30, 0.34, 0.44), "cap"), (140, (0.44, 0.36, 0.28), "none"),
               (80, (0.36, 0.28, 0.34), "cap"), (20, (0.28, 0.38, 0.32), "none"),
               (320, (0.46, 0.40, 0.30), "cap"), (265, (0.34, 0.30, 0.40), "none")]
for i, (deg, colr, ht) in enumerate(diner_specs):
    a = math.radians(deg)
    px, py = TX + 1.42 * math.cos(a), TY + 1.42 * math.sin(a)
    chair(px, py, 0.46, rot_z=0)
    seated_person(px, py, 1.68, colr, ht if ht != "none" else "cap" if i % 2 else "bonnet",
                  seat_h=0.48, name_p=f"diner{i}")

# --- Two attendants standing behind the table ---
# att1: left arm raised forward to carry the tray, right arm hanging;
# att2: left arm slightly forward (napkin over it), right arm hanging.
person(-0.85, 1.75, 1.74, "man", (0.18, 0.17, 0.18), "none",
       arm_l=(0.0, -1.15), arm_r=(0.0, 0.15), name_p="att1")
box("att1_shirt", (-0.85, 1.60, 1.08), (0.20, 0.03, 0.34), mat("shirt", (0.94, 0.93, 0.90), 0.9))
# tray with domed cover resting on att1's raised left hand
# (hand lands at approx (-1.03, 1.18, 1.14) with the arm above)
cyl("tray", (-1.03, 1.17, 1.16), 0.17, 0.17, 0.02, mat("traymat", (0.66, 0.64, 0.60), 0.3, 0.8), 20)
sphere("cloche", (-1.03, 1.17, 1.245), (0.15, 0.15, 0.10), mat("cloche", (0.70, 0.68, 0.64), 0.25, 0.85), 18)
sphere("cloche_knob", (-1.03, 1.17, 1.36), (0.03, 0.03, 0.03), mat("cloche2", (0.70, 0.68, 0.64), 0.25, 0.85), 10)
person(0.95, 1.80, 1.76, "man", (0.20, 0.18, 0.17), "none",
       arm_l=(0.0, -0.25), arm_r=(0.0, 0.12), name_p="att2")
box("att2_shirt", (0.95, 1.65, 1.10), (0.20, 0.03, 0.34), mat("shirt2", (0.94, 0.93, 0.90), 0.9))
box("napkin", (0.72, 1.68, 0.95), (0.05, 0.16, 0.30), mat("napkin", (0.95, 0.94, 0.92), 0.95))

tris = finalise(SLUG, (0.6, -6.9, 3.0), (0, 0.6, 1.0), res=(980, 800))
print("DONE", SLUG, tris)
