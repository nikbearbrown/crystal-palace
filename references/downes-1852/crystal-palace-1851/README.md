# Crystal Palace 1851 — source pack (pilot for the building-walkthrough skill)

## What this is, why, what we found

**What.** The first source pack for the planned building-walkthrough skill: where the evidence
for the 1851 Crystal Palace comes from, before any Blender model exists. The pilot source is
Charles Downes, *The Building Erected in Hyde Park for the Great Exhibition* (London: John
Weale, 1852): 28 plates drawn from the contractors' (Fox, Henderson & Co.) working drawings,
plus William Cowper's technical text.

**Why.** Rule of the skill: drawings first, model second. A model with no measured drawings
behind it is a confident guess. This pack is the "drawings first" step.

**Intended use (Bear, 2026-10-17).** The model will serve **both a film walkthrough and
possibly game assets**. So the Blender work is one editable master `.blend` with separate film
and game deliverables exported from it, not two models. The Crystal Palace suits this: it is
built from a few parts repeated on a 24 ft grid (column, girder, truss, sash bay), which are
natural game-kit pieces. Game-side rules live in
`/Users/bear/Documents/CoWork/bear-textbooks/books/walker/BLENDER.md`; film-side rules (subdivision,
UDIM, USD) are not written yet.

**What we found (2026-10-17).**

1. **The EPUB was a poor derivative; the full scan is not.** The 99-image EPUB held only partial
   crops. The full Internet Archive JP2 set (187 pages, 110 MB, downloaded with Bear's yes) holds
   every plate as **one whole image** (foldouts scanned flat, up to 11,630 px wide). No stitching
   was needed.
2. **All 28 plates are indexed and confirmed**, each by the plate number printed in its corner:
   plates 1–20, 20a, 21–27. See `PLATE-INDEX.md`.
3. **20 of 22 text dimensions now agree with the drawings**, some by measurement and some because
   the plate prints the same figure: the three tier widths, the 24 ft bay, the 8 ft gutter pitch,
   the 1,848 ft length (1,845 ft by bay count), the 936 × 48 ft north addition, the 48 and 72 ft
   avenues, the girder tops and gallery floor heights, the 8 in column and base plates, the 72 ft
   truss, the concrete pads, and the 74 ft 4 in vault. Agreements are within about 1% (2% for the
   warped plan sheet), and the plate measurements are now reproducible by script, inside the printed scale bar's own ±0.7% scatter. One more (D21) is
   consistent but not independent, and one (D22, the 108 ft louvre run) is on no plate. They rest on
   six sheets: Plates I, VI, VIII, X, XVIII and XX. See `CONTROL-DIMENSIONS.md`; raw numbers in
   `MEASUREMENTS.md`.
4. **The column-height "conflict" was my misreading plus OCR errors, and it is closed.** The
   connecting piece is 3 ft 4½ in (the OCR said 4¼), standing 2¼ in above and below the 3 ft girder
   it carries; Plate VIII prints the pieces (19 ft 2 in to the girder bottom, 3 ft 0 in, 2¼ in), and
   the printed page's pieces add up to the stated 62 ft 4¼ in exactly. **The OCR is unreliable on
   fractions**: read every fractional figure off the page or plate before it goes in a model.
5. **Warp, not tilt.** Plate I's sheet is warped (long lines at −0.8° in the middle, −1.4° to −2.1° on
   the left), so a tilt correction is the wrong tool; the plan's own 24 ft column grid is the ruler.

## The model so far (2026-10-17)

A Blender model built by script from these plates, in `model/` (see `model/BUILD-LOG.md`, and
`DEPARTURES-LEDGER.md` for every place it differs from the record). It is built part by part: the
current file, `model/crystal-palace-west-02_v001.blend`, is the first 12 bays from the west end (288 of the
1,848 ft): the three-tier frame on its 24 ft grid, gallery floors and railings, the void ends, the roofs, a
ground slab, and the first two staircases with their cross galleries (bay 8, 192 to 216 ft). It passes
25 gated controls (of 29 that apply) against the plates' figures, and its section along a stair lies on
Plate XV's. Missing: the transept and its vault, all walls and louvres, the north strip, the west entrance,
glazing detail, ten of the twelve staircases, colour. A full review render takes about 2 minutes on this
Mac. A fresh session should start from `HANDOFF.md`.

## Files

| File | What it holds |
|---|---|
| `SOURCES.md` | Tiered source table, rights column, where the scan lives |
| `PLATE-INDEX.md` | The 28 plates: number, title, JPEG, scan page, width (confirmed) |
| `CONTROL-DIMENSIONS.md` | 22 dimensions from the text, with plate-check status |
| `controls.json` | **DRAFT** model-vs-controls file for `walker/scripts/blender/check_controls.py`: 23 controls, with the part naming and properties decided (2026-10-17). No model exists yet, so it has only been run against throwaway stub models |
| `MEASUREMENTS.md` | Raw pixel values and methods behind each check, and the printed-page readings |
| `DEPARTURES-LEDGER.md` | Empty ledger template: every place the model differs from the record |
| `model/` | The Blender model: `parts.py`, `build_slice.py` (takes a range of grid lines), `render_preview.py`, versioned `.blend` files, `previews/`, and `BUILD-LOG.md`. Built so far: slice 01 (the Plate VI section, one bay) and the first six bays from the west end, both with gallery floors, railings and void ends; see the log |
| `tools/` | Five measuring scripts (Plates VI, I, X, XVIII, XX) plus `common.py` and `run_all.sh`; saved runs in `tools/output/`. Run `bash tools/run_all.sh` |
| `epub-contact-sheets/` | Contact sheets of the (partial) EPUB images; superseded by the full scan |
| `text/downes-1852-ocr-fulltext.txt` | Full OCR text of the book, page by page (`[page N]`) |

Local-only files (git-ignored via `../.gitignore`):

- `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/source-scans/jp2.zip` (110 MB)
- `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/source-scans/pages/` (raw JP2 pages)
- `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/source-scans/plates/` (28 working JPEGs, 94 MB)
- `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/rbsc_building-erected-hyde-park_folioNA6750L6D71852.epub`

## The draft controls file (`controls.json`)

35 controls in the format `check_controls.py` reads (D01–D15, D18–D20, D23–D34; D05, D10, D11 and D19 split
into several; D23 to D34 were added as the model reached the void ends and the stairs). Left out, with reasons in the file: D16 (four base-plate variants, assignment not in the
table), D17 (a range), D21 (not independent), D22 (on no plate).

**Decided 2026-10-17 (Bear):** the tolerance policy (tight modelling tolerance for plate-printed
controls; the larger of 0.5% and the scale-bar scatter for plate-checked ones), and the part naming:
`part_id` is the unique ID and `part_kind` the kind; `column_shaft` (symmetric, above the floor) is
separate from `column_base`, so spans and D13 (the 8 in column) use the shaft; single-part controls
use a `sample` property, not a name; plan rows are whole-word `tags` (`nave_edge`, `avenue_A1`,
`north_strip_edge`); `require_props` makes an untagged part an error; the origin is the centre of the
nave and transept crossing at floor level. The truss controls are decided too (D19a is the truss face to
face, 71.2 ft ±0.4, plate-checked; D19b is 6.0 ft ±0.1, plate-printed). **Nothing is open in the file.**

Mechanics tested first on a throwaway stub (it caught a tier-3 piece 0.4 ft too high and a column 1 ft off
its line, and an empty scene gave "matches no parts" errors). Now run against the real models: slice 01
17 of 17, the first six bays 19 of 19, the first 12 bays 25 gated passes and 4 text controls reported, no
failure. Several controls are true by construction (the model is built to the same figures); the gate catches
build mistakes, not misreadings of the plates, which is what the overlays and the ledger are for.

## Not done yet

- Every one of the 22 rows has now been looked at, and D23 to D34 added for the void ends and the first stairs. The
  prose also names more dimensions (sash-bars, lead flats, the other ten staircases) not yet in the table.
- The scripts search windows chosen by eye and print every candidate line; they do not find the windows
  themselves. A version that does, and a check against a model's geometry, are still to be written.
- D22 (108 ft louvre run) is confirmed on the printed page but on no plate; it can only be checked by
  counting louvre bays on Plates XXI–XXII. The remaining unmeasured items are the rib section (1 ft 6 in
  × 8 in, printed page only) and the prose figures on pages 19–58 beyond the 22 rows.
- Rights of the scan itself (McGill terms) are not checked; the 1852 work is public domain.
