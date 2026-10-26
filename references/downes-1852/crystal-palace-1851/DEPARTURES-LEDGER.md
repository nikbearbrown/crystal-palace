# DEPARTURES-LEDGER — Crystal Palace 1851

Executive summary: every place the model differs from the record, or relies on something the record does
not show. The film may show only what this ledger allows, and every `inferred`, `departure` and
`simplified` row that is visible is disclosed on screen or in the voiceover. Slice 01 (the transverse
section at line A–B, one bay deep, `model/crystal-palace-slice-01_v004.blend`; `model/crystal-palace-west-01_v001.blend`, the first six bays; `model/crystal-palace-west-02_v001.blend`, the first twelve bays with the first two staircases; and `model/crystal-palace-west-03_v001.blend`, the full west half to 888 ft with all six west-half avenue staircases) is the geometry so
far; the ledger will grow with the model. Status values: `matches record` · `simplified` (right size and
place, detail left out) · `inferred` (record silent or not yet read, reasoned from neighbouring parts) ·
`departure` (deliberately different) · `unverified` (kept from a Tier 3 mesh; none so far, there is no
Tier 3 mesh).

## Slice 01 (2026-10-17)

| # | Part | The record says | The model does | Status | Disclose in film? |
|---|---|---|---|---|---|
| 1 | Column shaft (`column_shaft`) | 8 in across, four flat and four cylindrical faces (Plate VIII Fig. 13); top 18 ft 11¾ in above the floor (printed page 4) | plain cylinder, 8 in across, top at 18 ft 11¾ in | matches record (size, height); section simplified | no |
| 2 | Upper column (`column_upper`) | 16 ft 7½ in between connecting pieces (printed page 4) | plain cylinder, 8 in across, 16 ft 7½ in | matches record (length); section simplified | no |
| 3 | Connecting piece (`connecting_piece`) | 3 ft 4½ in; starts 2¼ in below the girder (Plate VIII Fig. 12); flanges and four snugs (Fig. 12, 13) | cylinder 10 in across with two 14 in flange discs; no snugs or keyways | matches record (length, position); detail simplified | no |
| 4 | 24 ft girder (`girder`) | 23 ft 3¼ in long, 3 ft 0 in between bearing surfaces; flanges and sections a–f; a trellis of end struts, inner struts at the thirds and an X of diagonals in each panel (Plates VIII, X) | the same layout from boxes; flanges 5 in deep and 6 and 8 in wide, struts 3 in, diagonals 3 in clipped to the end faces; overall depth exactly 3 ft | matches record (length, depth, panel layout); sections simplified. Plate X reads 3.16 ft overall because the flanges project beyond the bearing lines; the model is 3.00 ft overall | no |
| 5 | Roof units (`ridge`) | gutter pitch 8 ft; glass 49 in long on a slope of 2½ to 1 (printed page 15); Paxton gutters, main gutters, sash bars (Plates XII, XIII, not yet read) | gabled sheets 8 ft wide and 24 ft long, rise 1.6 ft (a 4 ft run at 2½ to 1), 1 in thick, valley at the girder top of the tier | pitch matches record; valley level and rise **inferred** (read "2½ to 1" as 2½ horizontal to 1 vertical) | yes |
| 6 | Floor (`floor_ground`) | boarded floor on joists, open boarding to let dust through (the introduction; OCR text page 13) | solid slab 6 in thick, top face at z = 0 | **departure** (simplification) | yes, if the camera sees it |
| 7 | Stepping of the tiers | widths 408, 264, 120 ft; heights of girder tops 22 ft 2 in, 42 ft 2 in, 62 ft 2 in (Plate VI, VIII) | exactly that (an overlay of the section render on Plate VI registers closely by eye; not measured) | matches record. The overlay is a consistency check, not an independent one: the model was built from the same figures | no |
| 8 | Position of the slice | section line A–B is about 110 ft in from the west end on Plate I | the bay between grid lines 4 and 5 (96 to 120 ft from the west end) | matches record to within one bay | no |
| 9 | Materials and colour | Owen Jones's 1851 scheme (pale blue ironwork with yellow and red) | white clay material; pale tint on the roof sheets; no colour | **departure** (not yet applied) | yes |
| 10 | Light | 1851: opened by day only, no night lighting | a preview key light from the south-west (about 3000 K) and a weaker fill | **departure** (presentation only) | yes, as in the reference film |
| 11 | Gallery floor (`gallery_floor`) | the surface is 22 ft 11 in above the floor (printed page 17, D12); boards 1 in thick on trussed joists, common joists and binders resting on the girders (Plate XIV); through the section line the floor is four 24 ft strips either side of the 72 ft nave void and outboard of each 48 ft avenue void, 24 + 48 + 24 + 72 + 24 + 48 + 24 = 264 ft (Plate II) | four 24 x 24 ft solid slabs 9 in thick on the girder tops; surface at 22 ft 11 in | matches record (surface level, strip positions and widths); structure **simplified** (no joists, binders or trussing). The strip positions were read off Plate II by eye | no |
| 12 | Gallery railing (`balustrade`) | cast-iron standards, a plinth, a lattice of crossing curved bars with rosettes where they meet, and a top rail of a 2 x 3 in strip under a 2 3/4 in round rail (Plate XVII, printed page 22). **No plate prints the height** | a plinth, a single row of straight crossing bars, a top rail band and standards every 6 ft. Heights read off Plate VI's face-on lattice band: 3.06 ft overall, plinth 5.7 in, top band 8.7 in (good to about 0.05 ft per reading) | **inferred** (heights, and the 6 ft standard spacing) and **simplified** (the lattice). A diagnostic render of the railing across the nave void sits in the plate's band top and bottom at both ends, which only confirms the reading | yes |
| 13 | Railing runs in the slice | railings run round the edge of every void, so also across the void ends (Plate II) | six 24 ft runs along X, on the edges of the nave and avenue voids; **no cross railings**, because the voids end 24 and 72 ft from the west end, outside this bay | matches record for what the slice contains; the plate's face-on lattice band is a railing the slice does not have | no |

## West end, bays 0 to 5 (`model/crystal-palace-west-01_v001.blend`, 2026-10-17)

Everything in the table above applies to these bays too. What is new:

| # | Part | The record says | The model does | Status | Disclose in film? |
|---|---|---|---|---|---|
| 14 | Void ends (gallery plan) | the avenue voids begin 24 ft from the west end and run to 192 ft; the nave void begins 72 ft from the west end (Plate II prints "24.0", "168.0" and "72.0") | cross railings across each void end, built as three 24 ft runs (nave) and two (each avenue); the gallery floor is solid elsewhere, including all of bay 0 | matches record (positions, tested as D23 and D24); railing simplified as row 12 | no |
| 15 | The west end line (grid line 0) | the end wall carries the same 24 ft columns and, between them, wall posts every 8 ft (Plate I) | line 0 is an ordinary column line with the full tier stepping; no wall posts, no end wall | **simplified**: the end wall is not modelled; the end columns are placed as the controls need them | yes, if the camera looks at the end |
| 16 | Plate II read only to 192 ft | the plan continues with staircases from 192 ft and the transept at mid-length | the builder refused a range beyond line 8 (now line 12, row 23) | scope limit, not a departure | no |

## First staircases and the next voids, bays 8 to 11 (`model/crystal-palace-west-02_v001.blend`, 2026-10-17)

Everything above applies. What is new (printed text pages 31 to 35, Plates XV to XVII, Plates I and II):

| # | Part | The record says | The model does | Status | Disclose in film? |
|---|---|---|---|---|---|
| 17 | Stair flights (`stair_flight`) | two parallel flights 8 ft wide with 8 ft between them, to a landing, then one flight each way to the galleries; 21 steps in each flight; strings 7 ft 1 in centre to centre; step 1 ft 2 in wide and 1½ in thick, riser 7½ in deep and 1¼ in thick; hand rail a 2 x ¾ in strip under a 2¾ in round rail; elm treads and risers; cast-iron I-section strings (printed page 31 to 35, Plates XV, XVI) | flights 20 ft long (20 treads of 1 ft and the landing as the 21st step), rise 137.5 in in 21 risers of 6.55 in; strings 7 ft 1 in apart as plain polygons 4 in thick; treads 14 x 1½ in and risers 1¼ in; a handrail on each side 32 in above the nosing line; a plain baluster at every tread | counts, widths, spacing, thicknesses **match the record**. Rise per riser is derived (half of 22 ft 11 in over 21) and agrees with the 6.49 in read on Plate XV; the going (1 ft, read as 0.995 ft by script) and the strings' vertical depth (16 in) and the handrail height are **inferred** from Plate XV by eye. **Simplified**: no lattice standards, volutes, diagonal struts, nosing returns or I-section | yes, if the camera sees them |
| 18 | Landing and its columns (`stair_landing`, `stair_column`) | 24 ft long and 8 ft wide; eight small cast-iron columns 5 in outside, ½ in metal, 13 ft 1 in long of which 10 ft 8 in is above the floor, 7 ft 1 in, 8 ft 5 in and 7 ft 1 in apart (printed on Plate XVII Fig. 1 too), joined by girders along the sides; joists and boards on top; the landing level is not printed | one 24 x 8 ft slab 9½ in thick on the column tops, top at 137.5 in (11 ft 5½ in); eight plain cylinders 5 in across and 10 ft 8 in tall, at the printed spacing; 8 ft railing runs on the two ends and on the far side | sizes and column spacing **match the record**. Level **inferred** as half of the 22 ft 11 in gallery: the plate reads 11.55 ft by its scale bar and 0.499 of its own gallery line (script). **Simplified**: one slab for girders, joists and boards; solid columns; no base plates, nothing below the floor, no bracing. The landing runs to the axes of the main columns at both ends, so it overlaps them | yes |
| 19 | Cross gallery (`gallery_floor`, `XGAL_*`) | a gallery 48 ft long and 24 ft wide uniting the two main galleries, with two well-holes 8 ft wide by 16 ft long for the upper flights (page 31); Plate II shows them at the two ends of the avenue, over the middle 8 ft of the 24 ft bay | one 24 x 48 ft slab, 9 in thick, at the other gallery floors' level, with the two holes | sizes **match the record**; hole positions read off Plate II to about 1 ft. Slab structure **simplified** as row 11 | no |
| 20 | Railings at the stair bay | railings run round every void (Plate II); the plate marks "a" on both sides of the stair bay | cross railings across the avenue at lines 8 and 9 (4 runs each) like the other void ends; **none** round the inner ends of the wells; the landing's own railings (row 18) | cross railings **inferred** from the rule that voids are fenced; whether the wells were fenced beyond the flights' handrails is **not read** | yes |
| 21 | Where the flights start | Plate I draws the ground flights (hatched) at the nave-side end of each avenue's stair and the upper flights dotted; the south stair is the mirror of the north | ground flights from the nave-side edge of each avenue (y = ±60 ft), landing centred on the avenue (y = ±84), upper flights to y = ±60 and ±108 | **matches record**, read by eye from Plate I | no |
| 22 | Second pair of avenue voids | Plate II prints "192.0" for the void that follows the stair bay (216 to 408 ft) | built as void from line 9 to line 12 only, with long railings; its far end (408 ft) is not built | **matches record** to line 12 | no |
| 23 | Plate I and II read to 288 ft | the plan continues; twelve staircases in all (page 31) | the builder refuses a range beyond line 12; two of the twelve staircases exist (192 to 216 ft, north and south) | scope limit, not a departure | no |

## West half to transept, bays 0 to 36 (`model/crystal-palace-west-03_v001.blend`, 2026-10-18)

Everything above applies. What is new (Plates I and II, dim chain from 288 ft to 888 ft):

| # | Part | The record says | The model does | Status | Disclose in film? |
|---|---|---|---|---|---|
| 24 | Stair bays at 408-432 ft and 624-648 ft (lines 17 and 26) | Plate II prints "24.0" for both bays; hatched stair-wells are visible in the plan; the pattern repeats the first stair bay at 192-216 ft | same staircase geometry as rows 17-21 (cross gallery, two ground flights, landing, two upper flights, N and S avenues each) | **matches record** (bay dimensions, plate-printed; stair geometry inferred as for row 17) | same as rows 17-21 |
| 25 | Transept-access stair, 816-840 ft (line 34) | Plate II prints "24.0"; two hatched stair wells are visible in the plan at the avenue positions; this bay is distinct from the twelve avenue staircases (those are six bays × 2 avenues × 2 sides = 12; this is the extra access stair to the transept gallery) | same staircase geometry as the avenue stair bays (cross gallery, two ground flights, landing, two upper flights, N and S avenues) | **simplified**: the bay width matches the record; the stair type is unknown and modelled identical to the avenue staircases; the actual transept-gallery access stair detail is not read | yes |
| 26 | Fourth avenue void, 648-816 ft | Plate II prints two separate dim labels: "120.0" (648-768 ft, lines 27-32) and "48.0" (768-816 ft, lines 32-34); together 168 ft = one full avenue void; no structural divide is visible between the two labels | one uniform avenue void, identical to the other avenue voids; gallery floor absent, railings on the long edges and at both ends | **matches record**: the two labels are a plate annotation; the void is continuous. Fourth dim label ("48.0") left boundary is at line 32 (plate x ≈ 4262, outside the 5x crop at plate x 4300-4700, confirmed by arithmetic: 511 + 768 × 4.905 ≈ 4279 ± 5 px) | no |
| 27 | Pre-transept void, 840-888 ft (lines 35-37) | Plate II prints "48.0" | avenue void, 2 bays × 24 ft = 48 ft; gallery floor absent, railings on edges and ends | **matches record** (plate-printed) | no |
| 28 | Plan scope extended to line 37 (888 ft) | the plan continues east of the transept; twelve avenue staircases in all (page 31); west half has three avenue stair bays (192, 408, 624 ft), giving 6 of the 12 | builder now accepts --lines to 37; west half builds 6 of 12 avenue staircases (bays 8, 17, 26 N and S); 6 east-half mirrors, the transept itself, and everything east of it are not yet built | scope extension, supersedes row 23 | no |

## Not modelled yet (nothing below exists in the slice)

From Plate I at the west end, and not yet in the model: the west entrance (a 48 ft wide, 24 ft deep structure about 24 to 48 ft in, centred on the nave), the two small rooms with stairs either side of the entrance in the first bay, the wall posts and end wall, and the exhibit fittings.
Everything else from the list below also still applies.

Six of the twelve avenue staircases (the west half has three stair bays at 192, 408, and 624 ft, each with N and S staircases = 6; the east-half mirrors and everything east of the transept are not yet built); the diagonal bracing of the stair columns; the gallery's end bays; outer walls, doors and
louvres; glazing and sash bars (the roofs are plain sheets); base plates and the foundation pads; the 24,
48 and 72 ft trusses; the transept, its vault and ribs; cresting and finials; the north strip; trees,
fountains and fittings. The ground has no site.

## Slice build history

See `model/BUILD-LOG.md`.
