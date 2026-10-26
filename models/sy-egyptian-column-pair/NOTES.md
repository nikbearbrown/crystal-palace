# NOTES — Egyptian Court column pair (Hall of Karnak columns)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 10).
Scene: CP038 (Egypt, interpreted in South London).
**Sydenham 1854 only** — no Hyde Park evidence is used in this model.

## The interpretation caveat (read first)

**These are Victorian reproductions and interpretations of Egyptian
forms, not archaeological Egypt and not originals.** The 1856 guide
says so itself, in so many words: the Egyptian Court's temple front
was "not taken from any one particular structure, but composed from
various sources, to illustrate Egyptian columns and capitals" (p.48),
and its contents were "illustrations of [Egyptian] styles, commencing
with the earliest, and terminating with the latest" (p.47) — a
didactic arrangement designed under Owen Jones's direction of the
Fine Arts Courts (executed with Joseph Bonomi's Egyptological
input). The columns modelled here are the court's own reduced,
painted plaster-and-timber readings of Karnak, made in south London
in 1854. They must not be presented — in the film or in these notes —
as a neutral or accurate account of ancient Egyptian architecture,
still less of an entire culture.

## What it is

A pair of columns of the court's **Hall of Karnak Columns** (the
guide's spelling "Hall of Karnac Columns" on the plan), as drawn in
the guide's own captioned woodcut **"Column from Karnak"** (p.51)
and laid out in rows in the "Ground Plan of Egyptian Court" (p.47).
Each column: a low round two-step plinth; a flaring collar of
pointed lotus petals around the shaft foot; a tapering cylindrical
shaft carved (here, painted) with figure reliefs in five horizontal
registers divided by glyph bands; a banded necking; a ribbed
cluster-bud capital; and a square abacus with a painted glyph band.
The pair stands at the plan's column pitch, each on its own plinth,
exactly as the woodcut shows a single column standing — the plan
shows the hall's columns in rows of six and seven, of which this
prop is a two-column module for CP038, not the hall.

Origin at the base centre of the pair's footprint, ground z = 0.
Units: metres. Blender 4.5.3.

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- 1856 guide p.51, "Column from Karnak" woodcut + text — the form
  source (profile, petal collar, register bands, capital, abacus).
- 1856 guide p.47, "Ground Plan of Egyptian Court" (round-1
  gallery 0226) — the Hall of Karnak layout; pitch measured on it.
- 1856 guide pp.48–50 text — facade capitals (palm/lotus/papyrus),
  the Amunsthph cluster columns, the Beni Hassan fluted column,
  the Hathor-headed lotus columns, and the Karnak size statement.
- 1856 guide ground plan (gallery 0205) — court position ONLY,
  per the build plan.

**Evidence limitation, stated plainly:** the task brief expected
dated Delamotte photographs of the Egyptian Court. There are none
in the round-1 collection (searched by filename and manifest) and
none in round 2 (whose only court photograph is the Roman Court).
The dated visual evidence for this prop is the 1856 guide's own
woodcuts and text — one captioned column elevation, one plan, and
prose descriptions. Everything the woodcut does not show (notably
the back of the capital and the exact relief content) is inferred
or decorative, and is flagged as such below.

## Dimensions — measured vs derived vs inferred

| Part | Value | Status |
|---|---|---|
| Total height, plinth foot to abacus top | 6.32 m | **Derived** (chain below) |
| Height ÷ shaft base diameter | 5.03 | **Measured** on the p.51 woodcut (visual-grounding measure: abacus top to plinth foot 485 units vs shaft width 184 units) |
| Shaft base diameter | 1.25 m | **Derived** (chain below) |
| Shaft top diameter | 1.03 m | **Proportioned** from the woodcut's taper |
| Column pitch in the pair | 1.85 m | **Derived**: plan pitch ÷ column square = 1.36–1.56, **measured** on the p.47 plan (adjacent centres 64 units, square width 47 units; row average 1.56); taken as 1.48 × diameter |
| Shaft height (plinth top to necking) | 4.90 m (z 0.22–5.12) | Model build-up from the ratios above |
| Plinth | 1.72 m dia, two steps, 0.22 m high | **Proportioned** from the woodcut (low round disc base) |
| Petal collar | 14 petals, foot z 0.24, tips z 0.82, max radius 0.70 m | Count and form **from the woodcut** (petals visible around the shaft foot); count is the model's reading of the drawing |
| Necking | z 5.12–5.42, three painted bands | **From the woodcut** |
| Capital | z 5.42–6.10, flares to 1.49 m dia, 18 ribs | **From the woodcut** (ribbed cluster-bud form; rib count is the model's reading) |
| Abacus | 1.32 m square × 0.22 m | **Proportioned** from the woodcut |

**The absolute-size chain (no dimension is printed anywhere in the
sources):** (1) the guide (p.50) states the court's columns are
"reduced models" of Karnak's, whose majority "are 47 feet high, and
some are 62 feet", and that the models are "very much below the
size" of the originals; (2) the courts were fitted into the
building's side-aisle zone, whose module the contemporary Routledge
guide gives as 24 ft aisles; (3) on the 1856 ground plan the
Egyptian Court's compartment is ≈ 1/22 of the building's 1,608 ft
length, ≈ 73 ft ≈ three 24 ft bays; (4) on the p.47 plan the Hall
of Karnak occupies ≈ 55% of the court's length (≈ 12 m), and its
seven-column rows at the measured pitch ratio give a pitch of
≈ 1.85 m and a shaft diameter of ≈ 1.25 m; (5) height follows from
the woodcut's measured H/D of 5.03 → 6.3 m, adopted as 6.32 m.
Every link after (1) is an estimate with wide tolerance (±20% would
not surprise); the *proportions* rest on the two measured ratios,
the *absolute size* is the weakest number in this prop and is
flagged accordingly.

## Paint and polychromy

The guide attests painted colour in the court generally — "coloured
sunk-reliefs" on the facade walls (p.48) and "the colouring is taken
from actual remains in Egypt" (p.49) — and Owen Jones's courts were
famously coloured. **No source in the collection gives the specific
colours of the Hall of Karnak columns.** The palette here is
therefore **interpretive, labelled as such**: a warm sand ground;
figure registers and glyph-like bands in Egyptian blue, red ochre,
green and gilt in the Jones manner; capital ribs alternating the
same colours; petal collar alternating blue/green/red. The
hieroglyph-like marks are decorative shapes generated procedurally
(`scripts/make_textures.py`); they are **not** copied inscriptions
and must not be read as text. The court's one real inscription —
the frieze naming Victoria in hieroglyphs (p.48) — belonged to the
facade entablature, which is not part of this prop.

## Why this pair, and not the court's other columns

The court contained at least four distinct column types, and the
guide keeps them separate: (a) the Ptolemaic facade colonnade,
capitals "palm- and lotus-leaved… papyrus… from the simple bud to
the full-blown flower" (p.48, text only); (b) the Court of
Amunsthph cluster columns, "eight stems and buds bound together",
cast from a British Museum granite original (p.49, text only);
(c) the Beni Hassan tomb's fluted proto-Doric column (p.49,
illustrated as "First order of Egyptian Column" — an architectural
fragment of a different part of the court); (d) lotus columns with
Hathor ("cow-eared Goddess") capitals (p.50, one clause, not
illustrated and its exact position in the court not stated). The
Hall of Karnak columns are the only type the guide both *draws in
elevation* and *places on the plan* as the court's central
colonnade, so they are the best-evidenced pair — the others would
be modelled from prose alone. If CP038 needs the facade or the
Hathor columns, they are separate props still to build, from
weaker evidence.

## What was NOT modelled / known inaccuracies

- **The entablature.** The woodcut draws the hieroglyph frieze and
  cavetto cornice the columns carried. A pair module that included
  a beam would assert a span and a junction the evidence does not
  fix; the prop stops at the abacus, as the build note specifies
  ("columns with capitals"). Scene builders add the hall's
  entablature at shell level.
- **Relief carving is paint, not geometry.** The woodcut's shaft
  is covered in figure relief; here the figures are flat painted
  silhouettes in five registers (procedural texture), with only
  the register divisions modelled as thin rings. At CP038's
  intended distance this reads correctly; in close-up it will not
  pass as carving.
- **The capital's ribs** are a radial modulation of the lathe
  profile plus painted stripes — the woodcut's ribbing is finer
  and its bud divisions are not individually modelled.
- **The plinth steps** are simplified to two round steps; the
  woodcut suggests a similar low disc but its edge detail is
  schematic.
- **The plan's squares.** On the p.47 plan the hall's columns are
  drawn as squares (a woodcut convention); the p.51 elevation
  shows the column itself is round. The model is round; the
  square plan marks were used only for pitch and count.
- No weathering, damage or 1866-fire state: the prop is the court
  as opened in 1854.

## QC (2026-10-26)

- Guide pages read at full resolution from the collection scans;
  both measured ratios (H/D on the woodcut, pitch/square on the
  plan) taken by visual grounding on enlarged crops, values and
  method in the table above.
- First build's front render was inspected and showed four
  defects, all fixed and re-rendered: (1) cameras framed too
  tightly, cropping capitals and plinths — moved back and
  re-aimed; (2) the petal collar bulged into a striped ball — its
  profile was widest mid-height; it is now widest low, tips
  curving into the shaft, as the woodcut's calyx reads; (3) the
  painted petal band in the shaft texture duplicated the geometry
  collar — removed from the texture; (4) the shaft figures were
  stark frontal pictograms — redrawn in profile at low contrast
  so they read as flat relief.
- Second QC pass: plinth and petal colours rendered pastel under
  Blender's linear workflow — deepened; the abacus's stretched
  top-face texture was replaced by a plain slab with a proud
  glyph band.
- Counts, verified three ways (build log, re-opening the saved
  `.blend`, parsing the exported `.glb`): **48 objects,
  10,264 triangles** — well under the ~50,000 triangle prop
  budget. World bounding box: 3.57 m wide (pair incl. plinths:
  1.85 m pitch + 1.72 m plinth diameter) × 1.72 m deep × 6.32 m
  high; columns at ±0.925 m.
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground plane, lights, cameras; not exported).
  Meshes are world-space geometry with identity transforms;
  the two abacus boxes carry a location offset only — unit
  scale, no rotation, everywhere.

## Files

- `scripts/build_sy_egyptian_column_pair.py` — re-runnable bpy
  build script; dimensions are named constants at the top,
  grouped by evidence status.
- `scripts/make_textures.py` — procedural painted textures
  (system python3 + PIL; run before the build script).
- `textures/` — the three generated paint textures.
- `sy-egyptian-column-pair.blend` — model + render setup.
- `sy-egyptian-column-pair.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 1024 × 768. Front shows
  the pair at plan pitch; side is end-on (the pair overlaps);
  three-quarter is the CP038 establishing view.
- `refs/` — the six guide pages used, two enlarged crops, and
  `REFERENCES.md`.

Staged locally for review; not yet pushed to the repo.
