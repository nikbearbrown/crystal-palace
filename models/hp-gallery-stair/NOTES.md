# NOTES — Hyde Park gallery stair flight + landing edge + gallery rail

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 1, item 3).
Scenes: CP027 (another level of visitors — the stair seen from the
bottom, cut to the landing), CP023 (nave / gallery context).
Hyde Park 1851 building only — no Sydenham evidence is used in
this model.

## What it is

One complete lower flight of an 1851 Hyde Park gallery staircase,
from the ground floor to the mid landing, built as the plates show
it: 20 open-riser treads on two inclined plate strings, straight
X-lattice iron balustrades with lozenge bosses and scroll handrail
ends, arriving at the landing edge — landing deck on timber joists,
an iron edge girder, and one of the slender landing columns that
carry it. Along the landing's open edge runs a section of the
gallery-pattern rail: the wavy-bar lattice with lozenge bosses,
a frame standard, a timber handrail, and one fluted standard post
with its onion finial (Plate XVII's post M). The flight handrail
eases up at the top and joins that rail, as Plate XV's section
draws it.

Origin at the base centre of the prop's footprint, ground floor
z = 0. Units: metres. Blender 4.2+ (built with 4.5.3).

The real staircase is one of a mirrored pair in a 24 ft stair bay:
two lower flights (strings 7 ft 1 in apart, an 8 ft 5 in well
between the flights) rise to a shared landing 24 ft long × 8 ft
wide, and two upper flights (steps 22–42) climb back to the
gallery at 22 ft 11 in. This prop is a cut section of that
arrangement — one flight and the landing edge it serves — not the
whole bay (see "What was NOT modelled").

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- `references/downes-1852/source-scans/plates/plate-015.jpg` —
  Downes Plate XV: plans of the staircases and the section on
  line a.a. Primary visual source.
- `references/downes-1852/source-scans/plates/plate-016.jpg` —
  Plate XVI: stair ironwork details (balustrade panels, scroll,
  tread bearers, string joint, landing column).
- `references/downes-1852/source-scans/plates/plate-017.jpg` —
  Plate XVII: gallery railing details (Fig. 12 lattice elevation,
  Fig. 7/8 standard post M, Fig. 10 edge section).
- `references/downes-1852/source-scans/plates/plate-002.jpg` —
  Plate II, plan of galleries: where the stair bays sit.
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md`
  — dimension controls D12, D27–D34.

## Dimensions — printed/plate-checked vs measured vs inferred

| Part | Value | Status |
|---|---|---|
| Risers per flight | 21 (20 treads + landing as the 21st step) | **Printed** text p. 32; control D32; treads numbered 1–21 on Plate XV plan |
| Total rise, floor to landing | 11 ft 5½ in (3.4925 m) | **Plate-checked**, D31 (half of D12's 22 ft 11 in gallery height) |
| Riser height | 6.548 in (0.1663 m) | Derived: 137½ in ÷ 21 |
| Tread going | 1 ft (0.3048 m); flight run 20 ft (6.096 m) | **Plate-checked**, D32 (riser lines 0.995 ft apart on the plan) |
| Landing size | 24 ft long × 8 ft wide (2.438 m in the run direction) | **Printed** p. 31 / plate-checked, D27–D28. Only the 8 ft depth is modelled in full; the 24 ft length is cut (see below) |
| Flight width, string centres | 7 ft 1 in (2.159 m) | **Plate-printed** on Plate XVII Fig. 1; control D29 (the landing-column string centres 7'1" + 8'5" + 7'1") |
| Landing column | 5 in OD (0.127 m); top 10 ft 8 in (3.251 m) above floor | **Printed** text p. 33; control D30 (column is 13 ft 1 in long — 2 ft 5 in of it is below the floor and is not modelled) |
| Gallery/landing rail height | 3 ft 1⅞ in (0.953 m) to handrail top | **Printed** on Plate XVII Fig. 7; cross-checked on Plate XV section (37.0 in measured) |
| Standard post M | 3 ft 1⅞ in + 6¼ in finial = 3 ft 8⅛ in (1.121 m) overall; base plate 6½ in sq; shaft ≈ 6½ in across, bore 4¾ in | **Printed** on Plate XVII Figs. 7–8 (shaft modelled solid at 0.140 m nominal OD; the fluting and bore are not modelled) |
| Landing joist | 7 in × 2½ in (0.178 × 0.064 m) | **Printed** on Plate XVI ("Joist 7 × 2½") at the string joint |
| String depth | ≈ 10 in (0.26 m) perpendicular | **Measured** on Plate XV section against its 22 ft 11 in gallery height (63 px ⊥ at 6.14 px/in) |
| Flight handrail height | ≈ 33 in (0.855 m) vertical above the nosing line | **Measured** on Plate XV section the same way |
| Lattice diamond pitch (gallery rail) | ≈ 9.8 in (0.25 m); wave period ≈ 18 in (0.457 m); boss rows ≈ 9.7 / 18.1 / 27.6 in above the floor | **Measured** on Plate XVII Fig. 12 against Fig. 7's printed post height on the same plate |
| Flight balustrade diamonds | 13.0 in (0.33 m) horizontal pitch | **Counted/measured** on Plate XV section: 18 boss crossings along the flight, evenly spaced at 13.0 in (against the 22 ft 11 in calibration). Model bars at ±55° with a 0.47 m intercept step reproduce that pitch |
| Tread thickness | 0.045 m | **Inferred** — treads read ≈ 2 in thick on the section; no printed figure |
| String web/flange sizes | web 22 mm, flanges 105 × 20 mm | **Inferred** — Plate XVI's g.g section prints the splice bolts (⅞ in at 8 in centres), not the string section; sizes are proportioned from Plate XV |
| Deck board width | 9 in (0.229 m), butt-jointed | **Inferred** — no landing board width is printed in the sources used (the gallery floor was boarded with iron tongues, Berlyn p. 37; modelled plain and flagged) |
| Joist spacing on the landing | 0.61 m (2 ft) centres | **Inferred** — same assumption as the hp-floor-boards prop; not printed for the landing |
| Landing column capital/flare sizes | capital plate 0.20 m sq; foot flare to 0.29 m dia | **Proportioned** from Plate XVI Figs. 4/6, which draw the forms but print no sizes |
| Paint / materials | Painted iron, light warm grey; timber handrail and deck | **Interpretive** — Fig. 10's section shows wood grain in the gallery handrail (timber is evidenced); the ironwork was painted, exact 1851 colour not verified; treads modelled as iron from the ironwork detailing plates (XVI–XVII), material not stated in text |

## What was NOT modelled / known inaccuracies

- **The second flight and the upper flights (steps 22–42), the
  mirrored staircase, and the rest of the 24 ft landing** — the
  prop is one flight + the landing edge it arrives at, per the
  build plan. The landing deck is cut at the flight's width; in
  the building it runs the full 24 ft across both staircases.
- **Well-hole edges — deliberately unmodelled.** The gallery
  well-holes are documented as 8 ft × 16 ft openings (controls
  discussion at D34), but no plate used here draws their edge
  construction (kerbs, trimmers, rail returns) at modelling
  scale, so no well-hole edge is included rather than inventing
  one. The landing rail section stands on the landing's side
  edge (the edge Plate XV's section draws), not on a well-hole.
- **The gallery itself** — no gallery floor bay, girder or
  truss is included; the rail section sits on the landing edge,
  which uses the identical Plate XVII railing. A gallery-edge
  version differs only in what is under the rail (and in
  Fig. 10's curved stay bracket from standard to joist, which
  is not modelled).
- **The string's bolted joint** to the landing joist (Plate XVI
  Fig. 3 splice plate, ⅞ in bolts) is not modelled; the string
  dies into the arrival-edge joist. The joint exists in the real
  stair at exactly that point.
- **Tread bearers**: Plate XVI shows each tread carried on a
  T-iron bearer (I) on a bracket (K) screwed to the string. The
  model has plain bracket blocks at each tread end; the T-iron
  profile and screws are not modelled.
- **Balustrade panel feet**: on the plates the bottom diagonals
  of the flight panels curve into trefoil feet (Plate XVI
  panels G/H). The model's lattice bars are straight to the
  bottom boundary; the trefoil detail is omitted.
- **Post M fluting and bore**: the real standard is a hollow
  fluted casting (⅜ in wall, 4¾ in bore, Plate XVII Fig. 8).
  Modelled as a smooth solid shaft of the same outside size.
- **The landing column below the floor** (2 ft 5 in of its
  13 ft 1 in, down to its foundation) is excluded, like the
  column prop's below-floor base; the prop starts at the floor.
- Handrail scrolls are stylised spirals of the plate's overall
  size (≈ 8 in across, Plate XVI), not traced from the engraving.

## Relationship to other models

Built independently from the plates. It shares no geometry with
`course-models/crystal-palace-1851-claude/` (whose stairs the
storyboard flags as simplified) — no dimension was taken from
that model, because the plate-printed controls cover every
primary dimension of this prop. Heights agree with
`hyde-park-column-tier1` (same D11/D12 datum: gallery floor at
22 ft 11 in, so this prop's landing sits at exactly half that
prop's two-tier rise) and the landing joists match the member
sizes in `hp-floor-boards`.

## QC (2026-10-26)

- Plates read directly from the full-resolution scans; the
  measurements in the table were taken on the scans against the
  plates' own printed dimensions (method and residuals in the
  table), not copied from secondary summaries.
- First build's renders were viewed and showed three defects,
  all fixed and re-rendered: (1) the flight lattice stopped
  two-thirds up the flight — the diagonal-bar intercept range
  did not reach the upper flight; (2) the handrail easement at
  the landing kinked too steeply and overshot the landing rail;
  (3) the foot scroll rendered as a solid blob — its turns were
  spaced closer than the bar width. The string's top end was
  also trimmed so it dies into the landing joist instead of
  poking through the deck.
- Second QC round: the flight lattice, though complete, was
  twice too fine — counting boss crossings on Plate XV (18 over
  the flight) gives a 13.0 in pitch, and the bar spacing was
  reset to match. The far-side handrail easement also floated
  past the deck edge; it now ends at a landing newel, and a
  corner standard closes the landing rail's near end.
- Third QC round: the side render showed four black rectangles
  on the landing's edge girder. Toggling objects in a test
  render proved they were the joist ends, exactly coplanar
  with the girder's outer face — a coincident-surface artefact
  (both parts render correctly alone, and all face normals
  check out). The joists now stop 70 mm short and the girder
  closes the edge alone. A black seam at the flight's top
  standard had the same family of cause — the standard and
  the new landing newel interpenetrated by 15 mm — and was
  fixed by dropping the duplicate standard.
- Counts, verified three ways (build log, re-opening the saved
  `.blend`, and parsing the exported `.glb` — all agree):
  **18 objects, 6,596 triangles** — far under the ~50,000
  triangle prop budget. World bounding box 8.64 × 2.42 m plan,
  4.61 m to the finial tip (flight 6.10 m run + landing 2.44 m;
  landing surface at 3.49 m; post M overall 1.12 m above it).
  A first verification pass caught the string's bottom flange
  dipping 58 mm below floor level at the foot (the web's bottom
  edge is flat there, the flange is sloped); the flange now
  starts clear of the flat, and the shipped files are from the
  corrected build.
- The `.blend` contains two collections: `Model` (exported)
  and `RenderSetup` (ground plane, lights, cameras; not
  exported). The batch-built meshes are world-space geometry
  with identity transforms; the four lathed parts (landing
  column and foot, post shaft and finial) carry a location
  offset only — unit scale, no rotation, everywhere.

## Files

- `build_hp_gallery_stair.py` — re-runnable build script (bpy);
  all dimensions are named constants at the top, separated into
  printed / plate-measured / inferred groups.
- `hp-gallery-stair.blend` — model + render setup.
- `hp-gallery-stair.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 1200 × 900. Front is
  the flight elevation (the CP027 viewpoint); side is the view
  from the landing end; three-quarter from the foot of the
  flight.
- `refs/` — the four Downes plates used (copies from the repo),
  detail crops, and `REFERENCES.md`.
