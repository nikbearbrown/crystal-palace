# hp-louvre-and-blind

One 8 ft compartment of the Hyde Park upper-wall **louvre bank**, with
its full operating mechanism and its canvas blind — the ventilation and
shading gear of the 1851 building: five galvanized-iron louvre blades
in a timber case, worked by wooden bars, hoop-iron links, connecting
rods, shafting, a worm and worm-wheel, and a large rope pulley, with a
canvas blind on a roller at the head of the bank. Scenes **CP015,
CP028**. Wave 1, item 4 of `models/SCENE-BUILD-PLAN.md`, built to
Downes/Cowper, *The Building Erected in Hyde Park…* (1852),
**Plate XXVII** and its text — see `refs/REFERENCES.md`. Hyde Park
1851 only; nothing from Sydenham.

## The two states (required by the plan)

The mechanism is stored as **two posed copies of the same prop in one
.blend**, in two collections:

- **`Model_Open`** at x = 0 — louvres open (blades rotated −42° about
  their pivot pins, bars M raised the full 1¼ in travel, worm-wheel
  and crank posed mid-stroke), blind **up** (canvas rolled on its
  roller, short tail and lath hanging).
- **`Model_Closed`** at x = +3.90 m — louvres closed (blades nested
  shut, bottom blade's lip on the shut strip, bars lowered), blind
  **down** (two canvas breadths covering the bank).

Plate XXVII Fig. 1 itself draws exactly this pair — solid lines
closed, dashed lines open — so both poses follow the plate. The .glb
exports **`Model_Open`** only (the working state); both states live
in the .blend. Renders: front / side / three-quarter of the open
state, plus `closed-three-quarter.png` of the closed state.

## Dimensions

Plate scale on the repo scan: **70.8 px per inch**, calibrated on the
plate's own 12 in scale bar and verified against the printed 5½ in
dimension in Fig. 1 (390 px measured). "Plate-measured" below means
scaled off the scan at that rate. Fractions were read off the plate;
the repo OCR misreads them (see REFERENCES).

**Printed on the plate or in the Downes text**

| Part | Value | Source |
|---|---|---|
| Louvre case depth (jamb/head width) | 5½ in | Fig. 1 printed dimension; Plate XXII text |
| Case jambs and head, thickness | ⅞ in | Plate XXII text |
| Case lining | ⅜ in | Plate XXII text |
| Shut strip (lower blade shuts against it) | 2½ in × ⅜ in | Plate XXII text |
| Wall plate K, width | 10 in | Plate XXII text |
| Number of blades | 5 | "OUTER WALLS" p. 32 (five louvres above the wall-plate); Fig. 1 |
| Blade pivot pins | Ø⅜ in, 2 9/16 in long | LOUVRES text; Figs. 3–4 |
| Hoop-iron links L | 1 in wide | LOUVRES text |
| Bars M M, section | 1 in × ½ in | Fig. 1 printed dimension |
| Rod N / N′ | Ø⅜ in, eye Ø9/16 in | Fig. 14 (N′); Fig. 1 (N) |
| Bearing S¹ base / shaft centre above plate | 3 in / 3¾ in | Fig. 10 printed dimensions |
| Crank U holes | 1 1/16 in (shaft), 9/16 in (pin) | Fig. 13 |
| Shafting T T | Ø1 in | Fig. 9 ("Shafting 1 inch dia."); LOUVRES text |
| Shafting run from one wheel | 108 ft each side | LOUVRES text; control D22 (prose only) |

**Measured from the plate (scale-calibrated)**

| Part | Value |
|---|---|
| Pivot pitch (pin to pin) | 6.40 in |
| Lowest pin above top of K | 3.46 in; case internal height ≈ 32.3 in |
| Blade profile | S-curve traced from Fig. 1: max bulge +0.58 in (exterior) / −0.70 in (interior) from the pin centre-line, lip 7.06 in below the pin; pin 2.5 in from the case's inner face |
| Link eye / blade rivet below pin | 3.1 in / 2.9 in |
| Bar travel, closed → open | ≈ 1¼ in (dashed lines, Fig. 1) |
| Wall plate K, thickness | 3¾ in (see conflict below) |
| Worm-wheel O, diameter | ≈ 5.5 in |
| Rope pulley Q, diameter | ≈ 18 in (17–19 in across Figs. 1, 2, 10–11) |
| Worm P | ≈ Ø0.8 in × 4.6 in long |
| Crank U throw | ≈ 2.5 in |
| Bearing S: two-piece, on wall plate K with wooden cleat *c* | form from Figs. 6–9 |

**Inferred or guessed — not in the evidence**

- **Unit width 96 in (8 ft).** Plate XXVII draws one compartment's
  mechanism but states no width. 8 ft is the bay module of the
  building (24 ft bays divided into three 8 ft compartments, Plate
  XXI subdivision as used by the other Wave 1 wall props). The blade
  length (94 in) follows from the case width less end clearances.
- **Blade sheet thickness 0.065 in** — "sheet iron" (Introduction);
  no gauge is given anywhere. A heavy sheet, chosen so the S-profile
  reads at render distance.
- **The blind is an inferred assembly.** No blind is drawn on Plate
  XXVII, and Downes's louvre chapter never mentions one. What the
  evidence does support: the building's canvas was "in two breadths,
  with the seam in the centre" (p. 44, of the roof canvas). The blind
  here borrows that construction — two breadths with a centre seam —
  on an ordinary timber head roller (Ø2½ in; roll Ø4.6 in wound) with
  iron end brackets and a bottom lath. The 2.2 in centre gap between
  the breadths is a modelling accommodation so the connecting rod N
  can pass, as it must in front of the bank; it is not evidenced. The
  panel's gentle billow is hand-shaped geometry, **not** a cloth
  simulation.
- **Colours** are interpretive: galvanized grey blades; the case,
  wall plate and drive ironwork in a pale painted finish as on the
  other Wave 1 props; plain deal for bars M, roller and laths;
  unbleached canvas.
- The bottom blade is drawn shorter than its four fellows (lip
  3.4 in below its pin instead of 7.06 in) so that it meets the shut
  strip as Fig. 1 shows; the plate's lowest blade curve is partly
  hidden behind the worm-wheel in Fig. 1 and cannot be traced in
  full.

**Conflicts in the evidence (both readings stated, one modelled)**

- Wall plate K thickness: **3¾ in measured on Fig. 1**, but the text
  for a related wall plate gives 2½ in. Modelled 3¾ in (the drawn
  figure governs this unit).
- Wooden pins through the bars M: **Ø7/16 in measured on Fig. 1**;
  the OCR'd prose reads ⅝ in, but the OCR is unreliable on fractions
  and no printed plate dimension settles it. Modelled 7/16 in.

## Omissions

- **Ornamental plate F and casting c** (Fig. 1) belong to the
  alternating arch and wall in front of the bank — other props; the
  arch itself is research-gated in the plan and is not part of this
  mechanism unit.
- **Double bearing S²** (Fig. 12) stands at junctions of the real
  shafting; the prop's shafting is cut at the unit's ends, so no
  junction exists to carry one.
- **Shafting T T truncated** at the unit ends (with shaft collars).
  The real run is 108 ft each side of the wheel (D22); a 216 ft prop
  is not a prop.
- **Rope R cut** at 29½ in below the underside of K: the endless rope
  in reality continues down the (unmodelled) wall below and back up.
- The worm's thread is a helical tube (single-start, stylised) and
  the worm-wheel teeth are plain radial blocks; the plate draws both
  at small scale.
- The blade's pin roll (the curved top of the S where it wraps the
  pin) is simplified to the pin passing through the blade's top land,
  and the two end pins of each blade are modelled as one continuous
  pin across the bank.
- The **lower, ground-floor** louvres and their mitre-wheel hand
  drive (Figs. 15–22) are a different apparatus and a different prop.
- The wall below the plate, the windows beneath the bank, and the
  gallery structure are other props; z = 0 is the underside of the
  wall plate K (the mounting datum), so the drive gear and ropes
  hang below the origin plane, in front of where that wall would be.

## Materials

Galvanized iron (blades); pale painted iron (pulley, worm-wheel,
crank, bearings, brackets); bright steel (links, rods, shafting,
pins); painted timber (case, wall plate K); plain deal (bars M,
roller, laths, shut strip); unbleached canvas (blind); hemp rope.
Principled BSDF throughout, flat colours, no textures.

## Triangle counts

Recounted from the saved files (evaluated mesh data), not from the
build log:

- `Model_Open`: 138 objects, **8,436 triangles**; overall
  2.438 m wide × 0.410 m deep × 1.688 m high (z from the cut rope
  ends at −0.749 m to the case head top at +0.939 m).
- `Model_Closed`: 141 objects, **11,192 triangles** (the two
  subdivided blind panels account for the difference).
- The .glb (open state) parses back at 138 meshes / 8,436 triangles,
  matching the .blend exactly.

(Under the 50k ceiling of `MUSE-PROMPT.md` §2 either way it is
counted.)

## QC

- All four renders viewed. Open state: the five S-blades read as
  slats with shadow gaps, the linkage (links, two bar stations, block
  and rod) is legible behind them, the pulley-and-rope composition
  matches Fig. 2, and the blind roll sits at the head. Closed state:
  the two canvas breadths cover the bank, rod N passes through the
  centre gap to the worm-wheel, and the shafting, bearing S¹ and
  crank U remain visible below the blind's bottom lath, as they would
  in the building.
- Two defects found in the first build and fixed in the script:
  the blind roller originally sat proud of the case head and its roll
  intersected the linkage block — the roller was moved below the head
  underside on the interior face with clearances checked; and
  coplanar top faces of case head and jambs (and of shut strip and
  linings) produced black z-fighting patches in the side and
  three-quarter views — jambs now stop at the head underside and the
  shut strip stops short of the linings.
- The two staged states stand side by side, so each render isolates
  its state with the other collection's `hide_render` (toggled after
  the .blend is saved, so the file itself keeps both states live);
  without that, the side elevation showed a composite of both states
  through each other's gaps.
- A bounding-box audit of the saved .blend caught two more defects
  invisible or ambiguous at render distance: the worm-wheel teeth
  offsets missed an inch→metre conversion and sat on a 2.93 m
  phantom ring around the drive (two of them had appeared as stray
  specks in the front render); and the link eyes and wooden pins sat
  3.1 in *above* each pivot pin instead of 3.1 in below it (a sign
  error — the top pair poked above the case head, which the plate
  geometry forbids). Both fixed in the script and the package
  rebuilt; the audit was re-run clean (overall size below).
- `.glb` verified by parsing it back: 138 meshes / 8,436 triangles,
  open state only (blind roll present, no blind panels), matching
  the .blend's `Model_Open` count exactly.
- `.blend` re-opens with collections `Model_Open`, `Model_Closed`,
  `RenderSetup`.
