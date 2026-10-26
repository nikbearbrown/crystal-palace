# BUILD-LOG — Crystal Palace model

Executive summary: what was built, in which versions, what the controls said, and how long renders took.
Slice 01 is the transverse section at line A–B of Plate VI, one 24 ft bay deep, built entirely by script
(`build_slice.py` with `parts.py`), so it can be rebuilt or extended without hand edits. The previews are
a review aid; there is no final render yet.

## Files

| File | What it is |
|---|---|
| `parts.py` | part library: column shaft, upper column, connecting piece, 24 ft girder, roof unit (unlinked instance sources) |
| `build_slice.py` | builds grid lines FIRST:LAST (`--lines`, default 4:5 = slice 01; refuses beyond line 12, where the plan has not been read in detail) and saves `--out`; rebuilds from scratch each run |
| `render_preview.py` | headless renders (section, iso, nave, gallery, voidend, stairs, stairgal, stairsec); every path, resolution, sample count, device, focus point, exposure and a flat-lit mode are arguments |
| `crystal-palace-slice-01_v001.blend` | first build; kept because it FAILED D10b (see below) |
| `crystal-palace-slice-01_v002.blend` | first slice without a gallery; passes the 16 controls that applied then |
| `crystal-palace-slice-01_v003.blend` | adds the gallery floor and railings (railing heights were a first guess); passes 17 controls |
| `crystal-palace-slice-01_v004.blend` | **current**: railing heights read off Plate VI; passes all 17 controls that apply, D12 included |
| `crystal-palace-west-01_v001.blend` | the first six bays from the west end (`--lines 0:6`), with the void ends and cross railings |
| `crystal-palace-west-02_v001.blend` | **current**: bays 0 to 11 (`--lines 0:12`): the void ends, the stair bay at 192 to 216 ft with two staircases and cross galleries, and the avenue voids on to 288 ft |
| `compare_plate_vi.py` | overlays a section render on Plate VI and writes the stacked comparison |
| `compare_plate_xv.py` | overlays the `stairsec` render on Plate XV (the section along the stair) |
| `previews/diagnostic_cross-railing.blend` | DIAGNOSTIC ONLY, not part of the model: three railing runs across the nave void, to compare the railing face-on with the plate |
| `previews/` | renders, the comparison with Plate VI, and the control output (`controls-slice-01.txt/.json`) |

## 2026-10-17

- **v001**: 15 of 16 slice controls pass. **D10b fails**: the sample girder measures 23.338 ft against
  the printed 23 ft 3¼ in (+0.29%). Cause: the corners of the angled diagonals swing out past their end
  points, so they poke about 0.4 in past each end face. The gate found it; the eye would not have.
- **v002**: `bar_xz` clips bars to the girder's end faces. 16 of 16 pass:
  `--only D02,D03,D04,D06,D07,D08,D09,D10a,D10b,D11a,D11b,D11c,D13,D14,D15,D18`. Skipped by `--only`
  because the slice has no such part: D01, D05a, D05b, D12 (gallery floor), D19a, D19b (trusses), D20 (vault).
- **Parts in the slice**: 36 column shafts, 36 upper columns, 72 connecting pieces, 102 girders, 51 roof
  units, 1 floor.
- **Renders** (CPU, this Mac, 64 samples, the three views together): 35 s. Section 3000 x 800,
  iso 2000 x 1100, nave 2000 x 1100. The camera positions are arguments in the script.
- **Plate VI comparison**: `previews/slice01_v002_overlay_plateVI.png` (model lines in red over the
  plate, registered with the plate's scale bar and floor line) and `slice01_v002_vs_plateVI.png`.
  The columns, tier steps, girder bands and roof units coincide with the plate. That is a consistency
  check: the model and the plate share the same figures.
- **Explorer**: Bear says renders can go to Explorer. Previews do not need it (35 s here). Use it for
  final, high-sample or long-film renders. Before any cluster command read
  `books/hpc-aicr/skills/hpc/HPC.md`, and ask before submitting a job. Blender on Explorer has not been
  checked (this was written against 5.1.2).

## 2026-10-17, later: gallery floors and railings

- **Read first**: printed text pages 17 to 22 (galleries, staircases, railing; EPUB OCR pages 30 to 35),
  Plate II (extent), Plate XIV (floor construction), Plate XVII (railing). Plate II shows the gallery floor
  through the section line as four 24 ft strips with railings round the voids (24 + 48 + 24 + 72 + 24 +
  48 + 24 = 264 ft). The voids end 24 ft (avenues) and 72 ft (nave) from the west end, so the slice has
  only the long railings, not the cross railings that give Plate VI its lattice band.
- **v003**: four gallery panels (24 x 24 ft, 9 in thick on the girder tops, surface at 22 ft 11 in) and six
  railing runs. 17 of 17 controls pass with `--only` now including D12. The railing heights were a first guess
  (3 ft overall).
- **v004**: railing heights re-read off Plate VI's face-on lattice band (floor line at row 2127.7,
  top rail at 2052, lattice from 2070 to 2116, 24.74 px/ft): 3.06 ft overall, plinth 5.7 in, top band
  8.7 in. All 17 controls pass. Not printed on any plate, so INFERRED in the ledger.
- **Diagnostic**: with three railing runs placed across the nave void, the face-on band sits in the plate's
  lattice band top and bottom at both ends (`previews/zoom_railing_diag.png`). This confirms the reading
  against the plate it came from; it is not independent.
- **Renders** (v004, CPU, this Mac): section, nave and iso at 64 samples took 29 s together; the new
  `gallery` view at 96 samples took a few seconds.
- **What the section overlay can and cannot show**: the railings the slice contains run along X, so in the
  section they are seen end on and barely register. Plate VI's lattice band is the cross railing, outside
  the slice, so the overlay is unchanged from v002 for everything the plate can check.

## 2026-10-17, later still: the first six bays

- **Generalised** `build_slice.py` to `--lines FIRST:LAST`. Regression: `--lines 4:5` reproduces v004 exactly (a
  signature over every part's name, kind, position, rotation and properties: 308 parts, identical hash).
  The script refuses a range beyond line 8, because Plate II has been read only to 192 ft.
- **Read**: Plates I and II for the first 150 ft (void ends, west entrance, first staircases). Plate II prints
  "24.0" (avenue voids begin), "72.0" (nave void begins) and "168.0" (avenue void length to 192 ft). Two new
  controls, D23 and D24, test the first two (they are plate-printed; the positions agree with a ruler laid
  from the west wall to about 0.3 ft by eye).
- **Built** `crystal-palace-west-01_v001.blend`, lines 0:6: 126 column shafts, 126 upper columns, 252
  connecting pieces, 447 girders, 306 roof units, 37 gallery panels, 33 railing runs (long runs plus the cross
  railings at the void ends), 1 floor. Build time 0.8 s, 286 MB.
- **Controls** (`--only` the 19 that apply, D23 and D24 included): **19 of 19 pass**, in 1.6 s, 268 MB.
- **Renders** (this Mac, CPU, Cycles, 64 samples): four views (section 3000 x 800, iso, voidend, gallery) took
  1 min 46 s together; one iso view 13 s; the same iso on the one-bay slice 8 s. A flat-lit section at 32 samples
  takes 5 s. Peak memory about 3.4 GB for the six bays and 3.7 GB for the one-bay slice: it is a fixed baseline,
  not per part; this Mac has 48 GB. **Rough extrapolation, two points only:** about 8 s fixed plus 1 s per bay
  per view at 64 samples would be about 1.5 minutes per view for all 77 bays. Final quality (hundreds of
  samples, 4K, the full detail of every part) will cost far more, and is the job for Explorer.
- **Overlay on Plate VI** (`previews/west01_v001_flat_overlay_plateVI.png`): now includes the cross railings. With
  flat lighting they fall on the plate's lattice band at the two 48 ft avenue ends and the 72 ft nave end,
  with the right extents. That is a real cross-check between two plates: the void positions come from Plate II,
  the band extents are drawn on Plate VI. (With the key light the nave-end railing rendered dark and the
  overlay threshold dropped it; hence the new `--flat` mode.)
- **Nothing was merged or optimised**: parts still have several sub-meshes each (the railing has 39, the girder
  12); memory is not the constraint yet, so it was left alone. Merge them if a full-palace scene is slow.

## 2026-10-17, later again: the first staircases and 288 ft

- **Read**: printed pages 31 to 35 (staircases, landing, columns, step, railing), Plates XV, XVI, XVII (details), and
  Plates I and II from 192 to about 300 ft. The plan: a 24 ft stair bay (192 to 216 ft, "24.0"), then a second avenue
  void ("192.0" long, to 408 ft); the nave void goes on; each avenue's stair has two ground flights from the
  nave-side edge, a landing at the middle of the avenue and one upper flight each way, under a 48 x 24 ft cross
  gallery with two 8 x 16 ft well-holes. Flights run across the avenue: 20 + 8 + 20 = 48 ft.
- **Plate XV measured** by the new `tools/measure_plate_xv.py`: landing level 11.55 ft by the bar and 0.499 of the
  plate's own gallery line (so half of 22 ft 11 in: built at 137.5 in), 21 riser lines 0.995 ft apart over 19.90 ft,
  three main columns 24.2 ft apart (the sheet is 1% wider across than its bar). Details in `MEASUREMENTS.md`.
- **Built**: new parts (`stair_flight`, `stair_landing`, `stair_column`, `cross_gallery`, an 8 ft railing; the railing
  builder now takes any length and gives the old 24 ft run unchanged). `build_slice.py` lines 0:12 =
  `crystal-palace-west-02_v001.blend`: 234 column shafts, 234 upper columns, 468 connecting pieces, 861 girders, 612
  roof units, 63 gallery floors (two of them cross galleries), 81 railing runs, 8 flights, 2 landings, 16 landing
  columns, 1 floor. **Regression**: `--lines 4:5` reproduces v004 (hash 31d28a05cb53a430, 308 parts) and `--lines 0:6`
  reproduces west-01_v001 (hash baa9ab74096de122, 1,328 parts); `--lines 0:13` is refused.
- **Controls**: ten new (D25 to D34) in `controls.json`. `--only` the 29 that apply: **25 gated pass, 0 fail**, 4 text
  controls reported (D28, D30, D33, D34); skipped by `--only`: D01, D05a, D05b, D19a, D19b, D20 (no such parts yet).
  Several of the new ones are true by construction (the model is built to the same figures); the independent checks are
  below.
- **Independent check**: the `stairsec` section (orthographic along the flights) overlaid on Plate XV
  (`previews/west02_v001_overlay_plateXV.png`). The flights, the crossing of the ground and upper flights, the landing
  slab and its railings, the three main columns, the cross gallery and its railing, and the tier-1 girder band all
  fall on the plate's drawing. What the plate has and the model lacks: the diagonal bracing between the columns, the cast
  lattice and ornament, the I-section strings. That is still a consistency check, not independent evidence: the model is
  built from this sheet's figures.
- **Timings** (this Mac, CPU, Cycles, 64 samples): build 0.6 s, 330 MB (six bays 0.8 s, 286 MB); controls 5.7 s, 313 MB
  (six bays 1.6 s); four views (section, iso, voidend, gallery) **1 min 54 s**, 4.0 GB peak (six bays 1 min 46 s); one iso
  14.7 s (six bays 13 s); `stairs` + `stairgal` (2000 x 1300) 1 min 34 s, 4.3 GB. **Doubling the bays barely moved the
  render time**: pixels and samples dominate, not part count. That corrects the earlier "1 s per bay per view" guess:
  from 13 to 14.7 s for six more bays is about 0.3 s per bay, so all 77 bays would be roughly 30 to 40 s for one iso at
  64 samples (three points now, still an extrapolation). The controls gate is the part that grows with part count
  (1.6 s to 5.7 s for twice the bays and the stair instances), and is still negligible.
- **A shell trap**: under zsh an unquoted `$R` holding several arguments is not split, so a first batch of renders
  quietly produced nothing. Run multi-argument commands under `bash -c` (or arrays).
- **Interior views are dark** under the roofs; `render_preview.py` now takes `--exposure` (the `west02_v001_bright_*`
  renders use +2.5 stops). The roofs still shadow the floor.

## Next

Read the plan from 288 ft to the transept at 924 ft and build the transept and vault (Plates XVIII, XX, XXIV–XXVI).
The stair bays repeat every 216 ft from 192 ft; the text's twelve staircases are six stair bays, so presumably three
each side of the transept (192, 408 and 624 ft), but that is not read. Then the walls and louvres (Plates XXI–XXIII,
XXVII), the north strip, the west entrance and the end wall.
