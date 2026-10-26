# BUILD_NOTES: Crystal Palace 1851 (Claude)

## Summary

**What this is.** The iron frame of the 1851 Crystal Palace as built in Hyde Park, west half only (37 bays, 888 ft between the end column lines), as a Blender scene, a GLB, ten review views and two plate comparisons.

**Why it exists.** It is the pilot for a planned "building walkthrough" method for famous historical buildings: drawings first, model second, a dimension gate that fails the build when the model leaves the plates' figures, and a departures ledger that says honestly what is measured, inferred or simplified.

**What was found.** The frame passes every figure that was tested; it is not a likeness of the building (see the README). Two text-only checks report wrong numbers because of a sample tag (below).

## Dimensions and counts (from `checks/scene-counts.json`, counted from the .blend)

- Placed parts: **7,757** (all but the floor slab are instances of the 12 library collections; 164 library mesh objects)
- Parts by kind: girder 2,586, ridge 1,887, connecting_piece 1,368, column_shaft 684, column_upper 684, balustrade 274, gallery_floor 169, stair_column 64, stair_flight 32, stair_landing 8, floor_ground 1
- Triangles: **1,081,608** counting every instance (evaluated meshes)
- Materials: 4 (MAT_Floor, MAT_Glass, MAT_Iron, MAT_Wood)
- Between column lines: 888 ft long (line 0 to line 37) × 408 ft wide (outer columns), girder tops at 22′ 2″, 42′ 2″, 62′ 2″
- Bounding box of everything placed: 900.6 × 409.2 × 64.3 ft (the ground slab runs 12 ft past the last column line, the connecting-piece flanges stand proud, and the slab is 6 in below the floor line)
- Scene units: metres, scale 1.0; origin at the centre of the nave and transept crossing, floor top at z = 0
- Blender 5.1.2; the GLB has 3.0 MB, 165 meshes, 59,082 nodes, 4 materials, no textures

## Dimension gate (`checks/gate-west-03_v001.json`)

29 controls run, **25 gated pass, 0 fail**, 4 text-only reported, 6 skipped (D01, D05a, D05b, D19a, D19b, D20: no such parts yet). Status words: plate-printed (the plate prints the figure; tight tolerance), plate-checked (read off a plate; the larger of 0.5% and the scale bar's scatter), text (printed page only; reported, never gates).

| Control | What | Stated | Measured | Status | Result |
|---|---|---|---|---|---|
| D02 | Width of the lowest tier, outer column to outer column (408 ft) | 408 ft | 408.0000 ft | plate-printed | pass |
| D03 | Width of the second tier: outermost columns that reach tier 2 or 3 (264 ft) | 264 ft | 264.0000 ft | plate-checked | pass |
| D04 | Width of the third tier: columns that reach tier 3 (120 ft) | 120 ft | 120.0000 ft | plate-checked | pass |
| D06 | Bay pitch along the length: every column spacing is 24 ft | 24 ft | 24.0000 ft | plate-printed | pass |
| D07 | One 48 ft avenue, between its bounding column rows | 48 ft | 48.0000 ft | plate-printed | pass |
| D08 | The 72 ft nave, between its bounding column rows | 72 ft | 72.0000 ft | plate-printed | pass |
| D09 | Ridge-and-valley roof: gutter pitch across the width (8 ft) | 8 ft | 8.0000 ft | plate-checked | pass |
| D10a | Cast-iron girder depth, tier 1 (3 ft) | 3 ft | 3.0000 ft | plate-printed | pass |
| D10b | One 24 ft girder, face to face (23 ft 3 1/4 in) | 23.2708 ft | 23.2709 ft | plate-printed | pass |
| D11a | Top of the tier-1 girders above the ground floor (22 ft 2 in) | 22.1667 ft | 22.1667 ft | plate-printed | pass |
| D11b | Top of the tier-2 girders above the ground floor (42 ft 2 in) | 42.1667 ft | 42.1667 ft | plate-checked | pass |
| D11c | Top of the tier-3 girders above the ground floor (62 ft 2 in) | 62.1667 ft | 62.1667 ft | plate-checked | pass |
| D12 | Gallery floor surface above the ground floor (22 ft 11 in) | 22.9167 ft | 22.9167 ft | plate-checked | pass |
| D13 | Column external diameter, one sample shaft, stated in inches (8 in) | 8 in | 7.9995 in | plate-printed | pass |
| D14 | Top of the column above the ground floor (18 ft 11 3/4 in) | 18.9792 ft | 18.9792 ft | plate-printed | pass |
| D15 | Connecting piece length, tier 1 (3 ft 4 1/2 in) | 3.375 ft | 3.3750 ft | plate-printed | pass |
| D18 | Top of the tier-3 connecting piece above the ground floor (62 ft 4 1/4 in) | 62.3542 ft | 62.3542 ft | plate-checked | pass |
| D23 | Plate II: the avenue voids start 24 ft from the west end (west-end line to the… | 24 ft | 24.0000 ft | plate-printed | pass |
| D24 | Plate II: the nave void starts 72 ft from the west end | 72 ft | 72.0000 ft | plate-printed | pass |
| D25 | Plate II: the first avenue voids run 168 ft (line where they begin to the stai… | 168 ft | 168.0000 ft | plate-printed | pass |
| D26 | Plate II: the stair bay between the two avenue voids is 24 ft | 24 ft | 24.0000 ft | plate-printed | pass |
| D27 | Stair landing width (8 ft), one sample landing | 8 ft | 8.0000 ft | plate-checked | pass |
| D28 | Stair landing length (24 ft), one sample landing | 24 ft | 647.9999 ft | text | reported |
| D29 | Landing columns, outermost to outermost along the landing: 7 ft 1 in + 8 ft 5 … | 22.5833 ft | 22.5833 ft | plate-printed | pass |
| D30 | Top of a landing column above the floor (10 ft 8 in) | 10.6667 ft | 10.6667 ft | text | reported |
| D31 | Landing surface above the ground floor (11 ft 5 1/2 in, half of the 22 ft 11 i… | 11.4583 ft | 11.4583 ft | plate-checked | pass |
| D32 | Stair flight run, floor to landing (20 treads of 1 ft; the landing is the 21st… | 20 ft | 20.0000 ft | plate-checked | pass |
| D33 | Cross gallery over a staircase, length across the avenue void (48 ft) | 48 ft | 48.0000 ft | text | reported |
| D34 | Cross gallery over a staircase, width (24 ft) | 24 ft | 647.9999 ft | text | reported |

D28 and D34 read 648 ft against 24 ft: the `sample` tag that should select one stair part is set on four (one per stair bay), and the check measures all four together. The parts are 24 ft by construction. The gate does not fail on text-only controls, so the build passed.

## Method

1. **Read the plate or the printed page for every figure** (the book's OCR is wrong on fractions) and put the figures into `controls.json` with how each was measured.
2. **Build by script**: `scripts/build_slice.py --lines 0:37` places parts from `scripts/parts.py` on the 24 ft grid (18 column rows, line i at 24 i ft from the west end), with the plan (voids, stair bays) as read from Plates I and II.
3. **Gate**: a Blender script measures the evaluated geometry against `controls.json` and exits non-zero on a miss.
4. **Ledger**: every inference, simplification or departure is a row in `DEPARTURES-LEDGER.md`.
5. **Regression**: `scripts/part_signature.py` hashes every part's name, kind, position, rotation and properties. The builder reproduces the earlier files' hashes (31d28a05cb53a430 for lines 4:5, baa9ab74096de122 for 0:6, ede6c112ab6a9a58 for 0:12) and this model's own, **af709609ae4364c6** (7,757 parts).
6. **Compare with the plates**: `scripts/render_preview.py` renders the section views, `scripts/compare_plate_vi.py` and `compare_plate_xv.py` register them on the plates and write the overlays. Both are consistency checks.
7. **Publish**: `scripts/publish_assets.py` adds the lights and cameras, saves the scene, renders the views and exports the GLB; `scripts/make_compare.py` makes the comparison images; `scripts/make_pages.py` writes these pages.

## Departures ledger

`DEPARTURES-LEDGER.md` has 28 rows: 7 match the record, 9 simplified, 6 inferred, 3 departures, 3 scope notes (strongest word in each row's Status). The figures drawn from the ledger's text rather than a control include the roof rise (1.6 ft), the railing height (3.06 ft) and the stair landing level.

## Rebuild it

```bash
blender --background --python scripts/build_slice.py -- --out rebuilt.blend --lines 0:37
blender --background rebuilt.blend --python scripts/part_signature.py     # prints SIG af709609ae4364c6 7757
blender --background rebuilt.blend --python scripts/publish_assets.py -- --stage-dir out --steps blend,shaded,glb
```

The gate script (`check_controls.py`) and the plate scans are not in this folder. Written and run under Blender 5.1.2; 4.2 is untested.

## Comparison rounds

Two plate comparisons (Plate VI section; Plate XV stair section), each a registration of a render on the plate. No iterative likeness rounds.

## Known limitations

- **Unfinished.** 37 of the building's 77 bays: the west half, to the transept's west face. Not built: the transept and its vault, the east half, the walls, doors and louvres, the north strip, the west entrance and end wall, glazing and sash bars, base plates and foundation pads, and six of the twelve avenue staircases (the ledger lists everything).
- **Look.** White, grey and wood preview materials, opaque roof sheets and a generic dark ground. Owen Jones's 1851 colour scheme is not applied.
- **Simplified and inferred.** The ledger has 28 rows: 7 match the record, 9 are simplified, 6 are inferred (roof rise 1.6 ft, railing height 3.06 ft, the stair going and landing level, among others), 3 are departures (the solid 6 in floor slab, no colour, the preview lighting) and 3 are scope notes.
- **The plate overlays are consistency checks.** The model was built from the same plates' figures, so a close match shows where the model is missing parts, not that the plates were read correctly.
- **Two text-only checks read wrongly.** D28 and D34 report 648 ft against 24 ft, because the `sample` tag that selects one stair part now sits on four parts (one per stair bay) and the check measures all four together. The parts are 24 ft by construction; the report is misleading, not the model.
- **Blender version.** The .blend was saved in Blender 5.1.2. It was not opened in Blender 4.2, so 4.2 compatibility is untested; the GLB or `scripts/build_slice.py` are the safer routes in an older Blender.
- **GLB.** Flat PBR colours only, no textures. Collection instances become shared meshes (165 meshes, 59,082 nodes).
- **Plate scans are not in this folder.** The comparison scripts need the Internet Archive scans of Plates VI and XV; the images here are crops of them.

## Assessment and review

As a likeness of the Crystal Palace this model is poor. It is a bare iron frame under plain grey roofs: no glass, no walls, no colour, no transept and no vault, which is the part that gives the real building its silhouette. Someone who knows the palace would see the three stepped tiers and the ridge-and-valley roofs and might guess what it is going for, but would not take it for the building. What it is good for is a dimensioned frame: its figures were tested against the plates, and every place it infers or simplifies is written down in the ledger. That is the author's own assessment, made by looking at the renders next to the plates; Professor Bear's review is pending.

Human review: pending (Professor Bear).
