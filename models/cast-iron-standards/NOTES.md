# NOTES — Cast-iron standards A–D (Downes Plate 20a)

Prop for the Crystal Palace film. **Hyde Park 1851 building only** — these
standards belong to the first, Hyde Park palace (Fox, Henderson & Co.'s iron
frame as drawn by Charles Downes). No Sydenham evidence is used anywhere in
this model, and nothing here should be dressed into a Sydenham scene.

## What it is

The four cast/built-up iron "standards" — tall structural uprights — detailed
on Downes Plate 20a, modelled as four separate objects in a row on one rig so
their differences read at a glance:

- **Standard_A** — the *end* standard (plate caption: "Details of End
  Standard A"). Not a casting but a pair of waisted flat straps, pinned
  together, with the curved foot bracket M of Figs. 21–23 at its base.
- **Standard_B** — a riveted built-up box: four 2¼ in angle irons closed by
  flat face plates, stitch-riveted, with cross-pins and a mid-height splice.
- **Standard_C** — the same angle-iron family left open: no face plates,
  discrete batten bands instead, and the timber packing block K drawn inside
  it in Fig. 14.
- **Standard_D** — the only one-piece casting: a cruciform-section standard
  whose flange swells from a 6 in waist to wide capital and base flanges
  (Figs. 18–20).

Origin at each standard's own base centre; units metres; Blender 4.2.
Girders **G** (top) and **H** (bottom) in the plate are the building's
girders, not part of the standards, and are not modelled — the standards end
at their connection tongues, pins and flanges. The diagonal bracing bars that
cross B, C and D at mid-height are likewise separate members and are omitted;
their bolt/pads at D's waist are modelled.

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-020a.jpg` — Downes
  Plate 20a (John Weale, 1852). Primary and only visual source; see
  `refs/` for the full plate and figure crops, and `refs/SOURCES.md` for
  licence (public domain, published 1850s; scan via Internet Archive).
- `references/downes-1852/crystal-palace-1851/PLATE-INDEX.md` — confirms
  plate 20a's subject from its captions ("Details of Cast-iron Standard A…
  B and C… D").
- `CONTROL-DIMENSIONS.md` / `MEASUREMENTS.md` in the same folder were
  checked: **neither carries any dimension for the standards**, so every
  dimension below comes from the plate itself.

## How the dimensions were got

The plate's own scale bar could not be read reliably from the scan (the
PLATE-INDEX warns the paper edge is curved and edge measurements drift), so
each figure was calibrated against **dimensions printed on that figure**,
then cross-checked between figures. All four calibrations land at
**≈ 22.5 px/inch (± ~4%)**, so the top-row figures are treated as drawn to
one common scale and heights were measured at that scale. Absolute heights
therefore carry roughly ±4% (± ~0.09 m) uncertainty.

| Printed dimension used | Where | Calibration it gives |
|---|---|---|
| Waist width 6 in at line c–c | Fig. 18 (D) | ≈ 23 px/in |
| Bolt centres 9 in either side of centre | Fig. 18 (D), top and base | ≈ 22.5 px/in |
| "Four L irons 2¼ × 2¼ × ¼ in", "⅞ in rivets" | Fig. 12 (B) | box width 5.0 in, rivet heads ≈ 28 px ≈ 1.25 in dia. ✓ |
| Strap width 4 in | Fig. 5 (A detail) | strap measures 83 px ≈ 3.7 in at common scale ✓ |

## Dimensions — measured vs inferred

| Part | Value (as built) | Status |
|---|---|---|
| A overall height | 2.19 m | Measured from Fig. 7 extent at plate scale |
| A strap width / thickness | 4 in / 1⅜ in | Width printed (Fig. 5); thickness read from Fig. 5's fraction label (½ with a preceding figure, read as 1⅜) — **partly inferred** |
| A strap gap (pair) | ≈ 0.94 in clear | Measured from Fig. 6 |
| A pin/boss heights | 0.10–2.05 m (6 pins) | Measured from Figs. 6/7 feature rows |
| A bracket M | 1 ft 5 in long × 1 ft 0 in deep; foot 8 in across | **Printed** on Figs. 21/22 (drawn at a larger scale than the elevations) |
| B overall height | 2.23 m (incl. rounded tongue cap) | Measured from Fig. 13 extent |
| B section | 5.0 in × 6.3 in box | Widths measured from Figs. 12/13; decomposition into 2¼ in angle legs + 0.5 in / 1.8 in face plates is forced by the printed angle size and **fits both views exactly** |
| B angle irons | 2¼ × 2¼ × ¼ in | **Printed** on Fig. 12 |
| B rivets | ⅞ in, ≈ 10.9 in pitch, 7 rows | Size printed; pitch measured |
| B cross-pins | 7, at 0.35–1.99 m | Measured from Fig. 13 |
| C overall height | 2.22 m | Measured from Fig. 14 extent |
| C section | 5.0 in × 5.2 in | 5.2 in measured from Fig. 14; the 5.0 in second dimension is **assumed** from B (C's front view is not drawn) |
| C barrel taper | ± ~6% of width, max at mid-height | Measured from Fig. 14 edge lines |
| C batten bands | 6, at 0.21–1.90 m | Count and positions measured approximately from Fig. 14 |
| C timber block K | 0.10 × 0.105 × 0.26 m at z ≈ 0.93–1.19 m | Position/size measured from Fig. 14's hatched block; exact size **inferred** |
| D casting height (flange to flange) | 1.93 m; 2.06 m incl. top tongue | Measured from Figs. 18/19 |
| D waist width | 6 in at z ≈ 0.98 m | **Printed** on Fig. 18 |
| D flange widths | 19.8 in at capital/base → 6 in waist (profile table in build script) | Measured from Fig. 18 silhouette at 9 heights |
| D web depth | ≈ 5.1–5.7 in, gentle convex curve | Measured from Fig. 19 |
| D plate thicknesses | ⅞ in both plates | Measured (web edge lines in Fig. 18, flange edge in Fig. 19 agree) |
| D base bolt spacing | 9 in either side of centre | **Printed** on Fig. 18 |

## What was measured/seen vs guessed

**Seen and modelled directly:** A's waisted strap profile with boss discs,
pin rows, clamp gusset zone and slotted opening (left open between the
straps — no distance boss there, as drawn); bracket M's quarter-round curve,
paired cheeks, feet and base plate N; B's box decomposition, rivet columns,
cross-pins, side splice plates and end tongues; C's open frame, batten bands,
central tie bar and the timber block K; D's full flare profile, cruciform
section, waist boss pads with the ⅞ in through-bolt, capital and base plates
with their bolt pattern.

**Inferred or interpreted (flagged, not fact):**
- The raised central rib on A's straps (from the centre lines in Fig. 7 —
  may be a groove or a drawn centre line rather than a rib).
- A's strap thickness (1⅜ in) and the exact assembly of bracket M to the
  straps (Figs. 21–23 draw the bracket against girder H and the column pair;
  how it met the straps is composed from the three figures).
- C's front-face width (5.0 in, borrowed from B) and its rivet row spacing;
  C is drawn in one elevation only.
- B/C end tongues: drawn extent is into the girders; the modelled tongue
  length and cap are the visible minimum.
- D's top tongue above the capital (from Fig. 19's side view) and the small
  ribbed pads on D's flange faces at the waist (line work in Fig. 18).
- All heights carry the ±4% scale uncertainty above.

**Known inaccuracies:**
- Plate thicknesses of B's face plates (⅜ in) are assumed from period
  practice, not printed.
- Rivet head diameters are modelled at ≈ 1.4× shank diameter (standard
  proportion), not measured individually.
- The scan's curved paper (see PLATE-INDEX) means profile measurements near
  the plate edges — chiefly D's capital/base widths — may be a few percent
  out; the 6 in waist and 9 in bolt spacings, being printed, anchor the
  middle of the sheet where the figures sit.
- Fig. 5's fraction label beside the 4 in strap dimension is partly
  illegible at scan resolution; if it reads 1½ in rather than 1⅜ in, A's
  straps are 3 mm thicker than modelled.

## Build

Procedural Blender 4.2 script: `scripts/build_cast_iron_standards.py`
(lathe-style profile extrusion for A's straps and D's two plates, L-profile
prisms for the angle irons, lofted rings for C's tapered angles).
One fixed grey rig for all renders; all four standards in a row in every view.

Triangles: A 8,932 · B 7,064 · C 6,620 · D 3,140 · **total 25,756**.
