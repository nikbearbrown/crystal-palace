# HANDOFF — the Crystal Palace 1851 Blender model (read this first)

Written 2026-10-17 for a fresh session that has none of this conversation. Everything below is true as of the end
of that day; where a number could drift it says where to re-check it.

## Summary: what is being built, why, how far it has got

**What.** A verified Blender model of the Crystal Palace as built in Hyde Park in 1851, made from Charles Downes's
1852 book of 28 working-drawing plates (*The Building Erected in Hyde Park for the Great Exhibition*, Weale, 1852,
with William Cowper's text). The aim is the whole palace (1,848 ft long, three tiers, a transept with a 74 ft
vault), built **part by part**: build a part, look at it, check it against the plates, then build the next part.

**Why.** It is the pilot for a planned **building-walkthrough skill** for famous historical buildings (Bear's idea,
from Chiang Ning's article on a Crystal Palace film made with Claude and Blender). The skill's value is not the
modelling, it is a **verified model**: drawings first, model second; a **dimension gate** that fails the build when
the model leaves the plates' figures; and a **departures ledger** that lists every place the model differs from the
record, so a film can say honestly what is measured, what is inferred and what is simplified. The one master
`.blend` must serve **both a film** (camera, lighting, narration by the Brutalist toolkit) **and possibly game
assets** (Walker, Bear's 2D/3D games package). Walker owns the Blender build rules and scripts; Brutalist owns
camera, lighting, render, voice and gates.

**Where it stands.** The model covers the **first 12 bays (288 ft) from the west end**: the three-tier cast-iron
frame on its 24 ft grid (columns, connecting pieces, girders), gallery floors and railings at 22 ft 11 in, the void
ends, the ridge-and-valley roofs, a ground slab, and the **first two staircases with their cross galleries** (bay
192 to 216 ft). 2,580 placed parts. It passes **25 gated controls** against the plates' figures (4 more text-only
controls are reported), and its section along a stair lies on Plate XV's drawing. **Not built:** the transept and
its vault, any wall, door or louvre, the north strip (936 x 48 ft), the west entrance and end wall, ten of the twelve
staircases, glazing detail, colour. Nothing has been rendered for a film; the renders in `model/previews/` are
review aids.

**What you must know before touching anything.** The checks are real but limited: several controls are true by
construction because the model is built to the same figures; the gate catches build mistakes, not misreadings of
the plates. The overlays on the plates are consistency checks, not independent evidence. Every inference and
simplification is a row in `DEPARTURES-LEDGER.md`; add a row for each new one. Nothing is committed or pushed.

## Files (all absolute)

Source pack, `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851/`:

| File | What it is |
|---|---|
| `README.md` | what the pack is, what was found, status; read after this file |
| `PLATE-INDEX.md` | all 28 plates (1-20, 20a, 21-27) with what each shows |
| `SOURCES.md` | where the scan and text came from, licence notes |
| `CONTROL-DIMENSIONS.md` | the figures the model is tested against (D01 to D34), each with its plate and status |
| `MEASUREMENTS.md` | the raw pixel readings behind them, and what was read by eye |
| `controls.json` | the same controls in the format `check_controls.py` reads (35 controls), plus the DECIDED naming and tolerance policy |
| `DEPARTURES-LEDGER.md` | every place the model departs from, infers from, or simplifies the record (rows 1 to 23) |
| `tools/` | `measure_plate_vi/i/x/xv/xviii/xx.py` (deterministic plate readings), `run_all.sh`, `common.py`, `gridcrop.py` (gridded crops for reading by eye), `output/` |
| `model/parts.py` | the part library (column, piece, girder, roof unit, gallery panel, railings, stair flight, landing, stair column, cross gallery) |
| `model/build_slice.py` | builds grid lines FIRST:LAST (`--lines 0:12`), refuses beyond line 12 |
| `model/render_preview.py` | headless review renders (views section, iso, nave, gallery, voidend, stairs, stairgal, stairsec; `--flat`, `--exposure`, `--focus-x`, `--samples`, `--device`) |
| `model/compare_plate_vi.py`, `model/compare_plate_xv.py` | overlay a render on Plate VI / Plate XV |
| `model/part_signature.py` | regression hash of a model's parts (known values inside) |
| `model/BUILD-LOG.md` | history, timings, traps, what was learned at each step |
| `model/crystal-palace-west-02_v001.blend` | **the current model** (lines 0:12). Older files are kept: `west-01_v001` (0:6), `slice-01_v001..v004` (one bay; v001 failed a control on purpose and is kept for history) |
| `model/previews/` | renders, plate overlays, `controls-*.txt/.json` outputs |

Source scans and working JPEGs (git-ignored, local only): `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/source-scans/plates/` (`plate-001.jpg` ... `plate-027.jpg`, `plate-020a.jpg`) and `.../source-scans/pages/` (raw JP2). Printed-page OCR text: `.../crystal-palace-1851/text/downes-1852-ocr-fulltext.txt`.

Walker (the gate script lives there), `/Users/bear/Documents/CoWork/bear-textbooks/books/walker/`:
`ARCHITECTURE.md` (the method: tiered source pack, eligibility gate, ledger, dimension gate, one master `.blend`),
`BLENDER.md` (the game-asset rules this pack's naming and units follow), `scripts/blender/check_controls.py` (the gate:
evaluated geometry, collection instances included, exit 1 on a miss), `make_test_building.py`, `test_controls.json`.
These four walker files are untracked in git; `books/architecture` is not a git repository at all.

Cluster (not used yet): read `/Users/bear/Documents/CoWork/bear-textbooks/books/hpc-aicr/skills/hpc/HPC.md` completely before any Explorer command, and **ask Bear before any `sbatch`**. Blender 5.1.2 runs on Explorer (Tests 0 to 3 passed 2026-10-18 and 10-22; no container needed; unpacked at `/projects/musictrainer/blender/5.1.2/`); the cluster loads the identical 2,580-part model and renders the same image as the Mac; a 4K 64-sample interior frame takes about 64 s on a V100 (CUDA) or 69 s on a T4 (OptiX); CPU nodes, A100 and H200 are not yet timed. **2026-10-18 investigation and render kit** (parallel frame workers, stitch, container recipe, test plan; a 4K interior frame costs 242 s on the Mac, so a 90 s film is about 145 Mac-hours): `/Users/bear/Documents/CoWork/bear-textbooks/books/hpc-aicr/Rendering-Blender-on-Explorer/README.md`.

## How to run it (from the crystal-palace-1851 folder, under bash)

Blender 5.1.2 at `/Applications/Blender.app/Contents/MacOS/Blender`.

```bash
cd /Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851
BL=/Applications/Blender.app/Contents/MacOS/Blender

# build (0.6 s): lines FIRST:LAST from the west end; never saves anything except --out
$BL --background --python-exit-code 1 --python model/build_slice.py -- --out model/crystal-palace-west-02_v002.blend --lines 0:12

# controls gate (6 s). Run from walker/. --only lists the controls that apply to the parts that exist; the rest are listed as skipped.
cd /Users/bear/Documents/CoWork/bear-textbooks/books/walker
$BL --background /Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851/model/crystal-palace-west-02_v001.blend \
  --python-exit-code 1 --python scripts/blender/check_controls.py -- \
  --controls /Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851/controls.json \
  --only D02,D03,D04,D06,D07,D08,D09,D10a,D10b,D11a,D11b,D11c,D12,D13,D14,D15,D18,D23,D24,D25,D26,D27,D28,D29,D30,D31,D32,D33,D34

# regression hash (must reproduce the known values in the file's docstring for any range that existed before)
$BL --background model/crystal-palace-west-02_v001.blend --python-exit-code 1 --python model/part_signature.py

# review renders, e.g. the stair section (flat) and the overlay on Plate XV
$BL --background model/crystal-palace-west-02_v001.blend --python-exit-code 1 --python model/render_preview.py -- \
  --out-dir model/previews --tag west02_v001 --views stairsec --focus-x -720 --samples 32 --flat
python3 -I model/compare_plate_xv.py --render model/previews/west02_v001_stairsec.png --tag west02_v001

# the plate readings, all scripts, with checksums
bash tools/run_all.sh
```

Timings on Bear's Mac (CPU, Cycles, 64 samples, 12 bays): four views 1 min 54 s, one iso view about 15 s, peak about
4 GB. Doubling the bays barely changed render time (pixels and samples dominate). Final-quality frames (hundreds of
samples, 4K) are the job for Explorer.

## Conventions you must keep

- **Units and axes.** Scene unit metres (scale 1.0); dimensions are written in feet and inches and converted by
  `ft()`. Origin = centre of the nave/transept crossing at floor level. X along the length (+X east), Y across the width
  (+Y north), Z up. West end X = -924 ft; the main block spans Y = -204 to +204 ft; the floor slab's top is z = 0.
  Grid: 24 ft; line i is 24 i ft from the west end; 18 column rows 24 ft apart.
- **Parts.** Each placed part is an empty that instances a library collection; the library collections are NOT
  linked to the scene (otherwise they are measured as parts at the origin). Every part carries `part_id` (= its
  object name, unique, no `.001` suffixes) and `part_kind`; optional `tier`, `level`, `top_tier`, `block`, `tags`
  (space-separated whole words), `span_ft`, `sample`, `stage`, `avenue`. The full table is in `controls.json` under
  `naming`. Controls select by property and tag, never by name.
- **Controls.** Status vocabulary: `text` (printed text only; reported, never fails), `plate-printed` (the plate prints
  the figure; tight modelling tolerance), `plate-checked` (read off a plate; tolerance = the larger of 0.5% and the scale
  bar's own scatter), `plate-open`. Policy and naming were DECIDED by Bear on 2026-10-17; do not re-open them.
- **Plate readings.** The book's OCR is unreliable on fractions: read every fractional figure off the printed page or
  plate before it goes in the model. Tesseract only locates lines. Plate I is paper-warped (use its own 24 ft dot grid as
  the ruler). The scans are slightly rotated and stretched (Plate XV: ground line tilts 0.21 degree; its width runs 1%
  over its bar), so register on the plate's own features and say what was assumed. Read by eye on `tools/gridcrop.py`
  crops (plate-pixel coordinates), then put every figure you rely on into a `tools/measure_plate_*.py` script, with the
  windows printed so a reader can see where a choice was ambiguous.
- **Honesty.** A figure is `matches record`, `simplified`, `inferred`, `departure` or `unverified` in the ledger.
  Never write that something is verified when only laid out or only consistent with its own source.
- **Shell.** Run multi-argument command lines under `bash`. Under zsh an unquoted `$VAR` holding several arguments is
  not split, and a batch of renders silently produced nothing.
- **Python.** Scripts use `python3 -I` (isolated), so each adds its own folder to `sys.path`.
- **Do not** commit, push, delete, or submit cluster jobs without Bear's say-so; keep Claude-only notes local;
  report files to Bear by absolute path.

## What the model contains and what it assumes (so you do not rediscover it)

- Column shaft 8 in across, top 18 ft 11 3/4 in; connecting piece 3 ft 4 1/2 in; girder 23 ft 3 1/4 in long, 3 ft deep,
  bottom 2 1/4 in above the piece's foot; girder tops 22 ft 2 in / 42 ft 2 in / 62 ft 2 in; tiers 408 / 264 / 120 ft wide.
- Gallery floor surface 22 ft 11 in, 9 in slab on the tier-1 girder tops; railing 3.06 ft high (INFERRED from Plate VI).
- Roof units 8 ft gutter to gutter, valley at the girder top, rise 1.6 ft (INFERRED from "2 1/2 to 1").
- Voids (Plate II): avenue voids 48 ft wide from 24 ft to 192 ft, stair bay 192 to 216 ft, avenue void again from 216 ft
  ("192.0" long, to 408 ft; built only to 288 ft); nave void 72 ft wide from 72 ft, no stairs.
- Stairs (Plates XV to XVII, text pages 31 to 35): per avenue, a 48 x 24 ft cross gallery with two 8 x 16 ft wells over
  the middle 8 ft of the bay; two ground flights (8 ft wide, 20 treads of 1 ft + landing = 21 steps, rise 137.5 in) from
  the nave-side edge to a 24 x 8 ft landing at the middle of the avenue (top at half the gallery height); one upper flight
  each way from the landing; eight 5 in landing columns at 7'1" / 8'5" / 7'1". Flights run across the avenue: 20 + 8 + 20 = 48 ft.
- Not modelled: see the "Not modelled yet" list in the ledger.

## Next steps, in the order I would take them

1. **Read the plan from 288 ft to the transept (924 ft)** on Plates I and II (gridded crops; the stair bays repeat every
   216 ft from 192 ft and the text's twelve staircases are six stair bays, so presumably 192, 408, 624 ft each side of
   the transept, but that is not read). Extend `STAIR_BAYS`, `AVENUE_VOID_BAYS` and `PLAN_DATA_LAST_LINE` in
   `build_slice.py`, keep the regression hashes, add ledger rows.
2. **Transept and vault** (Plates XVIII, XX, XXIV to XXVI): the 72 ft trusses, the 74 ft 4 in vault ribs. Controls
   D19a, D19b, D20 already exist in `controls.json` and are skipped until those parts exist.
3. **Walls, doors, louvres** (Plates XXI to XXIII, XXVII), the **north strip** (D05), the **west entrance and end
   wall**, glazing and sash bars, base plates and pads (D16, D17 are listed in `controls.json` `not_included` with
   reasons), then colour (Owen Jones's scheme: pale blue ironwork with yellow and red; a departure until applied).
4. **Explorer renders** for final quality: read HPC.md, check that Blender runs there, ask Bear before submitting.
5. **The film side** has not started: Brutalist needs the master `.blend` plus the ledger. The film may show only
   what the ledger allows, and every visible `inferred`, `simplified` or `departure` row is disclosed on screen or in
   the voiceover. (Film rules: see `/Users/bear/Documents/CoWork/bear-textbooks/books/CLAUDE.md`; the two-stage rule
   there says a layout session writes a BUILD-PROMPT.md and a cheaper session renders.)

## Decisions that are Bear's

Colour scheme and when to apply it; whether and when renders move to Explorer; commit and push of the four walker
files; whether the film should wait for the whole palace or use a finished stretch (for example the west 288 ft);
whether the game-asset export (BLENDER.md rules, one kit of repeated parts) starts before the film.

## Known weak spots (be suspicious of these first)

- Stair details are simplified and the handrail height, string depth and going are read off Plate XV by eye; the
  landing level (11.46 ft) is half the printed gallery height, and the plate reads 11.55 ft by its bar.
- D27 to D34 are partly by construction. D28, D30, D33, D34 are text-only (never gate).
- The gate does not look for parts that are missing, only for parts that are wrong; completeness is the ledger's job.
- The ground slab is a plain 6 in slab (the real floor was open boards on joists); the roof is opaque grey in the
  review renders, so interiors are dark (use `--exposure 2.5`).
