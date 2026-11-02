# Build scan-fig57-chinese-commission (Muse version).
# Source: coloured satirical frontispiece to Henry Sutherland Edwards, "An Authentic
# Account of the Chinese Commission" (1851), discussed in the source book as Orientalist
# caricature. The model preserves the composition — a robed official with a tall staff
# crossing a gangplank, attendants carrying a great kettle and a hamper, pagoda and junk
# behind — with all figures as dignified neutral silhouettes in period dress, and no
# caricature features or pseudo-script anywhere.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vignette_common import *

bpy.ops.wm.read_factory_settings(use_empty=True)

SLUG = "scan-fig57-chinese-commission"

# shore: stone quay strip at back, water strip at front
box("quay", (0, 1.55, 0.10), (6.4, 2.6, 0.20), mat("stone", (0.60, 0.57, 0.52), 0.95))
box("water", (0, -1.15, 0.02), (6.4, 2.8, 0.05), mat("water", (0.42, 0.55, 0.60), 0.35))
# gangplank sloping from quay down toward the viewer-left, as drawn
plank = box("gangplank", (-0.5, 0.15, 0.42), (0.55, 3.4, 0.07), mat("plankwood", (0.55, 0.42, 0.28), 0.85),
            rot=(math.radians(-7), 0, math.radians(4)))
for i in range(6):
    box("plank_batten", (-0.62 + i * 0.045, 0.95 - i * 0.32, 0.50 - i * 0.045), (0.6, 0.09, 0.03),
        mat("batten", (0.48, 0.36, 0.24), 0.85), rot=(math.radians(-7), 0, math.radians(4)))

# --- backdrop: distant hills, pagoda, junk on the water (flat set-dressing masses) ---
for i, (hx, hs) in enumerate(((-2.6, 1.1), (-1.2, 0.8), (2.9, 1.3))):
    cyl("hill", (hx, 3.1, hs / 2), 0.05, 1.25, hs, mat("hillmat", (0.55, 0.62, 0.55), 0.95), 18)
# pagoda (right rear): stacked tiers with oversailing roofs
PGX, PGY = 2.35, 2.75
tier_h = [0.62, 0.50, 0.40]
w = 0.85
z = 0.2
for i, th in enumerate(tier_h):
    box("pagoda_tier", (PGX, PGY, z + th / 2), (w, 0.5, th), mat("pagoda", (0.62, 0.55, 0.48), 0.9))
    box("pagoda_roof", (PGX, PGY, z + th + 0.05), (w + 0.34, 0.78, 0.10), mat("pagroof", (0.35, 0.38, 0.40), 0.8))
    z += th + 0.10
    w *= 0.78
cyl("pagoda_finial", (PGX, PGY, z + 0.12), 0.02, 0.02, 0.26, mat("pagfin", (0.35, 0.38, 0.40), 0.8), 8)
# junk (left rear, on the water behind the quay line): hull, mast, plain sail
box("junk_hull", (-2.35, 2.55, 0.42), (1.5, 0.34, 0.30), mat("junkwood", (0.42, 0.32, 0.22), 0.85))
box("junk_stern", (-3.0, 2.55, 0.62), (0.22, 0.36, 0.42), mat("junkwood2", (0.42, 0.32, 0.22), 0.85))
cyl("junk_mast", (-2.35, 2.55, 1.25), 0.025, 0.025, 1.5, mat("mast", (0.45, 0.35, 0.24), 0.85), 8)
box("junk_sail", (-2.35, 2.52, 1.38), (0.92, 0.03, 0.95), mat("sail", (0.80, 0.74, 0.62), 0.95))
for i in range(4):
    box("sail_batten", (-2.35, 2.50, 0.98 + i * 0.27), (0.94, 0.02, 0.03), mat("sailbat", (0.60, 0.52, 0.40), 0.9))

# --- Central official: long patterned robe, wide conical hat, tall plain staff ---
OX, OY = -0.35, 0.30
person(OX, OY, 1.82, "robe", (0.52, 0.22, 0.20), "conical", arm_r=(-0.25, 0.1), name_p="official")
# robe trim bands (dress detail only; no motifs, no script) — short sleeve-cylinders
# hugging the robe cone (radius interpolated from the robe profile)
for zz, rr in ((0.55, 0.205), (1.05, 0.172)):
    cyl("robe_band", (OX, OY, zz), rr, rr + 0.006, 0.07, mat("robetrim", (0.24, 0.30, 0.48), 0.8), 20)
box("sash", (OX, OY - 0.20, 1.12), (0.30, 0.03, 0.10), mat("sash", (0.80, 0.66, 0.30), 0.8))
# tall staff, plain pole with small finial (blank — the print's inscribed banner is NOT reproduced)
cyl("staff", (OX + 0.38, OY, 1.85), 0.016, 0.016, 3.5, mat("staffwood", (0.40, 0.30, 0.20), 0.7), 10)
sphere("staff_finial", (OX + 0.38, OY, 3.66), (0.05, 0.05, 0.05), mat("stafffin", (0.72, 0.60, 0.28), 0.35, 0.7), 12)

# --- Attendant with the great kettle (left rear, on the quay) ---
AX, AY = -1.85, 1.15
person(AX, AY, 1.70, "robe", (0.30, 0.36, 0.46), "cap", name_p="att_kettle")
# the kettle: big rounded vessel carried by its handle at his side
KX, KY, KZ = AX - 0.55, AY - 0.15, 0.78
sphere("kettle_body", (KX, KY, KZ), (0.30, 0.30, 0.27), mat("kettle", (0.55, 0.42, 0.30), 0.5, 0.4), 20)
cyl("kettle_lid", (KX, KY, KZ + 0.26), 0.16, 0.20, 0.07, mat("kettlelid", (0.45, 0.34, 0.24), 0.5, 0.4), 16)
sphere("kettle_knob", (KX, KY, KZ + 0.33), (0.045, 0.045, 0.045), mat("kettleknob", (0.35, 0.26, 0.18), 0.5), 10)
_c = cyl("kettle_spout", (KX + 0.30, KY, KZ + 0.10), 0.035, 0.055, 0.30, mat("kettlespout", (0.55, 0.42, 0.30), 0.5, 0.4), 12,
         rot=(0, math.radians(-50), 0))
torus("kettle_handle", (KX, KY, KZ + 0.30), 0.20, 0.018, mat("kettlehandle", (0.35, 0.26, 0.18), 0.5, 0.4),
      rot=(0, math.pi / 2, 0), major=20)

# --- Attendant with the hamper chest (right rear) ---
BX, BY = 1.15, 1.05
person(BX, BY, 1.68, "robe", (0.38, 0.30, 0.42), "cap", name_p="att_hamper")
box("hamper", (BX + 0.10, BY + 0.38, 1.02), (0.78, 0.34, 0.62), mat("hamper", (0.66, 0.55, 0.38), 0.95))
box("hamper_lid", (BX + 0.10, BY + 0.38, 1.36), (0.82, 0.38, 0.07), mat("hamperlid", (0.58, 0.47, 0.32), 0.95))
for dx in (-0.24, 0.0, 0.24):
    box("hamper_band", (BX + 0.10 + dx, BY + 0.38, 1.02), (0.05, 0.36, 0.64), mat("hamperband", (0.45, 0.36, 0.24), 0.9))
cyl("scroll_roll", (BX + 0.10, BY + 0.38, 1.50), 0.05, 0.05, 0.66, mat("scroll", (0.88, 0.84, 0.76), 0.9), 12,
    rot=(0, math.pi / 2, 0))

# --- Fourth attendant at the left edge holding a parasol over the party ---
PX, PY = -2.85, 0.75
person(PX, PY, 1.68, "robe", (0.44, 0.38, 0.30), "conical", name_p="att_parasol")
cyl("parasol_pole", (PX + 0.30, PY - 0.05, 1.75), 0.014, 0.014, 1.9, mat("parapole", (0.40, 0.30, 0.20), 0.7), 8,
    rot=(math.radians(8), math.radians(-6), 0))
cyl("parasol_canopy", (PX + 0.42, PY - 0.16, 2.72), 0.03, 0.62, 0.16, mat("parasol", (0.68, 0.30, 0.26), 0.9), 20)

tris = finalise(SLUG, (0.4, -8.8, 3.4), (0, 0.9, 1.35), res=(840, 1040))
print("DONE", SLUG, tris)
