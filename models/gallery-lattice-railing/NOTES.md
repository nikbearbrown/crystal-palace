# NOTES — Gallery lattice railing and newel post

Candidate #19 from `models/CANDIDATES.md`. The repeating gallery-front
railing of the Hyde Park 1851 building: one lattice panel, one frame
standard, and one newel post (Downes's standard post M) with its gilt
bud finial. Film use: gallery edges throughout (cf. scenes CP023,
CP027). **Hyde Park 1851 only** — no Sydenham evidence is used.

Origin at the base centre of the assembled unit; z = 0 is the gallery
floor line (the lattice foot line of Plate XVII Fig. 12). Units:
metres. Blender 4.2. The unit arrays by translation: panel + standard
repeat at a pitch of **2.8127 m** (newel centre to standard centre);
place a newel at run ends and corners. `renders/run.png` shows three
pitches assembled that way.

## Relationship to `hp-gallery-stair`

That prop already contains a short landing-edge section of this same
Plate XVII railing, built for the stair's landing. This prop is the
**standalone, arrayable component** — a full panel plus both terminal
types (frame standard and newel M) — dimensioned independently from
the plate. No geometry is shared. Where the two overlap (rail height,
post M), the dimensions agree, because both were taken from the same
printed figures.

## Sources used (copies in `refs/`)

- `references/downes-1852/source-scans/plates/plate-017.jpg` — Downes
  (1852), Plate XVII: Fig. 12 railing elevation, Fig. 7 post M
  elevation, Fig. 8 post plan/section, Fig. 9 lattice foot and
  standard base detail, Fig. 10 section at the frame standard,
  Fig. 11 section at c.c, and the plate's scale bar. Primary source
  for everything modelled. Public domain.
- `references/muse-drive/images/commons/John_Absolon,_The_Transept_from_the_South_Gallery,_The_Great_Exhibition_of_1851.jpg`
  — Absolon watercolour, 1851. Colour evidence (below) and the
  newel's in-situ appearance. Public domain (manifest).
- `references/muse-drive/images/commons/The_great_industrial_exhibition_of_1851._Plate_3._The_British_nave_LCCN2003665158.jpg`
  — Nash/Dickinson Plate 3, the British nave: the railing in situ in
  long runs. Public domain (manifest). Copied into `refs/` at reduced
  resolution (3000 px wide); the full 9790 px file stays at the repo
  path above.

## Dimensions — printed vs measured vs inferred

Plate XVII Fig. 12 was calibrated against its own known height: the
handrail top stands the printed 3 ft 1⅞ in above the lattice foot
line (the same figure Fig. 7 prints for post M, floor to cap top),
which spans 1,461 px on the scan → **38.6 px/in**. Boss positions were
located on the scan by ink projection and visual grounding. The plate
is a fold-out photographed in a bound volume, so local scale varies
by a few percent; treat measured figures as ±4%.

| Part | Value | Status |
|---|---|---|
| Handrail top above floor | 3 ft 1⅞ in (0.962 m) | **Printed** (Fig. 7; cross-checked ≈37.0 in on Plate XV section by the stair build) |
| Newel post M overall | 3 ft 8⅛ in (1.121 m) | **Printed**: 3 ft 1⅞ in to cap top + 6¼ in finial (Fig. 7) |
| Post shaft / bore / wall | 6½ in / 4¾ in / ⅜ in | **Printed** (Fig. 8). Modelled solid (bore not cut) at 6½ in across |
| Post base plate | 6½ in sq, rounded corners; bolt holes ¾ in at 4⅞ in centres | **Printed** (Fig. 8); holes shown as dark insets, not drilled |
| Frame standard thickness | 1¼ in (0.0318 m) | **Printed** (Fig. 10 section) |
| Boss rows above foot line | 6.7 / 17.4 / 28.0 in (0.170 / 0.442 / 0.711 m); row spacing 10.65 in | **Measured** on Fig. 12 |
| Boss column pitch | 12.43 in (0.3157 m); rows staggered half a pitch | **Measured** on Fig. 12 |
| Lozenge boss | ≈3.1 × 2.2 in plate (0.080 × 0.055 m) | **Measured** on Fig. 12 |
| Bar face width | ≈0.39 in (0.010 m; ~15 px across the drawn strip) | **Measured** on Fig. 12 |
| Handrail depth | ≈1.9 in (0.048 m; the 72 px band of Fig. 12) | **Measured** |
| Frame standard width | 10.4 in (0.264 m) overall; uprights ≈0.7 in face | **Measured** on Fig. 12 |
| Post cap | 8 in sq (0.203 m) | **Measured** on Fig. 7 against the 6½ in shaft |
| Finial max diameter | ≈5.5 in (0.140 m) | **Measured** on Fig. 7, same basis |
| Bar thickness / rib | 4 mm + 1.3 mm rib each face | **Inferred** — Fig. 9 shows a ribbed face but prints no thickness |
| Hairpin leg gap | 40 mm | **Inferred** from Fig. 9's pair of verticals (unscaled detail) |
| Panel length | 8 lattice periods (2.526 m of lattice) | **Inferred** — Fig. 12 draws the lattice running continuously past one standard and prints no standard spacing; 8 periods ≈ the building's 8 ft module (cf. the 8 ft gutter pitch, control D09) |
| Handrail width / profile | 3 in (0.076 m), rounded top | **Inferred** from the Fig. 10 section |
| Bottom channel | 46 mm wide, 40 mm tall | **Interpretation** — see below |

## Construction notes

- The lattice is generated as swept ribbed bars: diagonal segments
  between boss rows (with a ±5 mm alternating bow, for the hand-made
  waviness the plate shows), hairpin U-turns at the foot, and broad
  ∩ crests at the top. Every crossing carries a lozenge boss: plate,
  raised inner lozenge, and a small gilt centre dome, standing proud
  toward the gallery side (−Y), as Fig. 10's section shows.
- Post M's shaft section follows Fig. 8: a 6½ in circle with four
  flat faces, one shallow flute per face. The fluting is simplified
  (no bore, no bolt rebates) and reads subtly at render distance.
- The frame standard's inner pattern follows Fig. 12: two diagonals
  crossing at a small centre lozenge, curving together into a cap
  curve at the top and a U at the bottom, inside a mitred liner
  frame. Its foot follows Fig. 9: stepped block with a screw head on
  the gallery face.
- All parts meet with butt joints or overlaps — no coplanar faces
  (an early build z-fought black squares at the liner corners in
  Cycles; fixed by construction, not by material tricks).

## Colour (from the Absolon watercolour)

- Lattice, bosses, frame standard, channel: **red** paint — the
  gallery railing reads as a strong red band across the transept in
  the watercolour, lattice and all.
- Newel post M: **deep blue** (the foreground post in the
  watercolour is blue with lighter blue panels; modelled as one blue,
  panels not painted in).
- Bud finial and boss centre domes: **gilt** — the finial is fully
  gilt in the watercolour; the near lattice in the same view shows
  light dots at the crossings, taken here as gilt boss centres.
- Handrail: dark polished timber (Fig. 10's section shows wood grain
  in the gallery handrail). Under this repo's standard render rig the
  timber renders lighter than its material values; the values, not
  the render, are the record: (0.24, 0.115, 0.050).

Nash's Plate 3 shows the railing pale at distance — that is
atmospheric perspective in the lithograph, not a different finish.

## What was NOT modelled / known inaccuracies

- **The below-floor structure.** On the plate, the lattice feet and
  the standard stand at the gallery edge with the edge girder (band
  T, ≈5½ in deep) below the floor line, and Fig. 10 shows a curved
  stay bracket from the standard down to the joist. The girder and
  bracket are gallery structure, not railing; the model instead
  gives the lattice a shallow bottom channel at floor level to house
  the feet (an interpretation), and the standard a Fig. 9-style foot
  block standing on the floor.
- **Standard spacing in the real building is not documented** in the
  sources used; the 8-period panel is a component convention (see
  the dimensions table), not a surveyed bay.
- The post's **bore, fluting depth and the handrail mortise** in the
  cap (dashed in Fig. 7) are not modelled; the handrail simply dies
  into the cap face, as it does visually in situ.
- Boss rosette detail: the plate's bosses carry an 8-petal flower;
  the model has the lozenge, inner lozenge and centre dome only.
- The slight **bow** given to the diagonal bars is a uniform ±5 mm
  convention, not traced bar-by-bar from the plate.

## Counts

Verified from the build (and by re-opening the saved `.blend`):
**6 objects, 25,872 triangles** — well under the ~50,000 prop budget.
Overall size 3.066 × 0.203 × 1.121 m (length × depth × height; the
depth is the newel cap; the lattice itself is 0.078 m thick at the
bosses). `.blend` collections: `Model` (exported to the `.glb`) and
`RenderSetup` (ground plane, lights, cameras; not exported). The
meshes are world-space geometry with identity transforms.

## Files

- `gallery-lattice-railing.blend` / `.glb`
- `renders/` — `front.png` (gallery side), `side.png` (from the
  standard end), `three-quarter.png`, `run.png` (three arrayed
  pitches; render-time duplicates, not in the saved file),
  `compare.png` (front render against Fig. 12)
- `refs/` — the three sources above
- `scripts/build_gallery_lattice_railing.py` — re-runnable build
  (bpy); all dimensions are named constants at the top, grouped into
  printed / measured / inferred
