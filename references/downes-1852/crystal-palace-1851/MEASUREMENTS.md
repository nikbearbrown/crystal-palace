# MEASUREMENTS — raw numbers behind CONTROL-DIMENSIONS.md

Executive summary: how each control was measured, with the pixel values, so any row can be
re-checked. **Five scripts now reproduce the plate measurements** (`tools/`, run together with
`bash tools/run_all.sh`; output saved in `tools/output/run-2026-10-17.txt`). They replace the earlier
hand-assisted readings for Plates VI, I, X, XVIII and XX; the section "Script results vs the
hand-assisted readings" below says where the two agree and where the script changed a number. What
is still read by eye: the crops of printed figures on Plates I, VIII, XX and the printed text pages,
and the choice of search windows (the scripts look in windows picked by viewing the plate and print
every candidate line, but they do not discover the windows themselves). All pixel values are in the
full-resolution working JPEGs in
`/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/source-scans/plates/`
(git-ignored). Date: 2026-10-17.

## Script results vs the hand-assisted readings

Each script is deterministic (run twice, byte-identical output) and read-only. Numbers in feet use
the scale named in the script output. "Hand" is what the earlier sections of this file recorded.

| Check | Hand | Script | Change |
|---|---|---|---|
| Plate VI scale bar | 24.74 px/ft, ±0.7% | 24.74 px/ft, ±0.7% | none |
| Tier widths D02–D04 | 405.8 / 262.8 / 119.6 ft | 405.8 / 262.8 / 119.6 ft | none |
| Bay pitch D06 (tier 3) | 591.7 px = 23.9 ft | 591.7 px = 23.92 ft | none |
| Floor line; tier 3 and tier 2 girder tops | y 2697; 62.34, 42.30 ft; spacing 20.04 | same | none |
| Tier 1 girder top | "ambiguous 2140–2153" | candidates 23.01 / 22.50 / 21.99 ft; picks 22.50 (+0.33 ft vs 22 ft 2 in) by assuming 20 ft spacing | now explicit: loose, ±0.5 ft |
| Gallery floor D12 | 23.01 ft | 23.01 ft | none |
| Gutter pitch D09 | 197.5 px = 7.98 ft | 197 px = 7.96 ft (autocorrelation) | −0.02 ft |
| Concrete pads D17 | 9 readings; 1.25–3.07 ft thick; 1.6–3.7 ft wide | 10 readings; 1.25–3.48 ft thick; 1.58–3.72 ft wide (column 4 is added by the stated rule) | one more reading |
| Plate I dot pitch | 117.9 px mean | 118.0 px mean (282 pairs); bins 115.6–119.3 | none |
| Plate I length D01 | 9,063 px = 1,845 ft | 9,064 px = 1,845 ft with the local pitch (−0.17%); 1,843 ft with the global mean | none |
| North addition length D05 | 4,585 px; 933 ft (919–934 depending on pitch) | 4,581 px; **936.0 ft** with the local pitch (+0.04%); 931 ft with the global mean | **changed**: local-pitch integration gives the stated 936 |
| North addition depth D05 | six intervals = 48 ft | seven posts, six intervals = 48 ft | none (now counted by script) |
| Avenue and nave D07, D08 | 238 px = 48.2 ft; 352 px = 71.3 ft (single bays) | pair medians: 48.0 ft (8 pairs, 46.5–49.1); 72.4 ft (7 pairs, 71.7–75.8) | **changed**: medians of several pairs replace one pair |
| Plate XVIII scale | 58.4 px/ft | 58.57 px/ft, ±0.7% | +0.3% |
| Vault D20, D21 | radius 37.2 ft; diameter 74.3 ft | radius 37.07 ft; diameter 74.14 ft (−0.26%); 37-ft radius +0.19% | **changed** by 0.2 ft; next-candidate crown lines give 72.8–73.8 ft |
| Rib depth (1 ft 6 in) | not measured | candidate lines at 1.43 and 1.61 ft below the extrados | new, loose |
| Plate X girder D10 | ratio 7.9 → 3.0 ft (preview) | centre-to-centre 24 ft = 220.5 px/ft; face to face 23.25 ft (printed 23 ft 3¼ in, −0.08%); inner depth 2.97 ft (−1.0%); overall 3.16 ft; ratio 7.83 | new face-to-face check; depth now from lines |
| Plate XX truss D19 | 35.5 ft half length (from the column face); depth not measured | panels 8 ft = 147.6 px/ft (±0.5%); first post to centre line 28.01 ft; centre line to left-edge lines 35.0–35.8 ft (−0.5% to −2.7% vs 36 ft printed); depth 6.10 ft (+1.7%) | refined |

What the scripts could not settle:

- **Tier 1 girder top** (22 ft 2 in) stays loose. Lines at 22.50 and 21.99 ft bracket it; Plate VIII
  prints 19 ft 2 in + 3 ft 0 in, which is the reliable figure.
- **Vault crown.** The topmost line at the crown is taken as the extrados. The next lines (10 to 20 px
  lower) are rib lines; choosing one of them would lower the diameter by up to 1.4 ft.
- **Which left-edge line is the column centre line** on Plate XX. The script prints all seven; the
  nearest to the printed 36 ft is at x = 93 (35.83 ft).
- **Plate X depth** depends on which flange lines are taken; the inner pair gives 2.97 ft and the outer
  pair 3.16 ft.

## Plate VI (`plate-006.jpg`, 11,630 × 3,925 px)

- **Scale bar.** Ticks at 0, 10 … 100 ft along y ≈ 3219–3228. 0 at x = 4672.5, 100 ft at 7130.5
  → 24.58 px/ft over the whole bar; a fit to the 10–70 ft ticks gives 24.74 px/ft. Per-10-ft
  spacing runs 24.55–24.90 px/ft, so the bar itself scatters about ±0.7%. The script uses
  24.74; results change by about 0.6% with the other scale.
- **Tier widths (script).** Outer column lines: tier 1 x = 782.0 and 10,821.2; tier 2 x = 2,549.5
  and 9,049.5; tier 3 x = 4,326.6 and 7,285.3. Distances 10,039 / 6,500 / 2,959 px → 405.8 /
  262.8 / 119.6 ft at 24.74 px/ft (stated 408 / 264 / 120).
- **Bay pitch.** Tier 3 column lines at 4326.6, 4914.9, 5509, 6100, 6697.5, 7285.3 → gaps 588.3,
  594, 591, 597.5, 587.8 px; mean 591.7 px = 23.9 ft.
- **Vertical datum.** Floor line at the foot of the columns, y = 2697 (7 px thick group; the next
  line down, 2730, is the ground below the boards). Girder top-flange lines in a bay free of
  columns (x 5000–5420): tier 3 at y = 1154.8, tier 2 at 1650.5, tier 1 ambiguous at 2140.5–2153.
  Tier 3 → tier 2 = 495.7 px = 20.04 ft. Heights above the floor line: tier 3 = (2697 − 1154.8) /
  24.74 = 62.34 ft; tier 2 = (2697 − 1650.5) / 24.74 = 42.30 ft. Gallery floor line y = 2127.7 →
  23.01 ft. **Hand-assisted:** which line is "top flange" was chosen by looking, then checked
  against the 20 ft spacing; with the other candidate lines the answers move by 0.2–0.5 ft.
- **Gutter pitch.** Tier 3 roof finials in band y 1065–1100: pairs at x = 6885/6902, 7082/7100,
  7279/7297 → 197.5 px = 7.98 ft.

## Plate I (`plate-001.jpg`, 10,121 × 4,114 px)

- **Printed figures read from crops:** "1848 · 0" under the south entrance, "408 · 0" at both
  end walls, "48 · 0" at the east and west entrances, "24 · 0" beside the column grid.
- **Scale bar** 0–500 ft: roughly 4.94 px/ft (hand-read; the bar is slanted ~0.8° and its ends
  are hard to pin down). Used only as a cross-check.
- **Why not "tilt-corrected":** long lines on the sheet run at −0.8° in the middle and right but
  −1.4° to −2.1° on the left, so the sheet is warped, not just rotated. Rotation changes a
  length by under 0.03% anyway.
- **Column dots** (about 24 px discs found by blob detection, 659 of them). Median horizontal pitch
  by region: 118.4 (x 500–2000), 115.9 (2000–3500), 118.5 (3500–5000), 118.2 (5000–6500), 118.1
  (6500–8000), 118.7 px (8000–9600); mean over 260 pairs = 117.9 px. West and east end walls at
  x ≈ 519 and 9,581 (y 1900–2500) → 9,063 px = 76.9 bays. 77 × 24 = 1,848 ft; 76.9 × 24 = 1,845 ft.
  (A first attempt to chain the dots across the whole length stopped at the south entrance and a
  fold crease at x ≈ 4,780; it was abandoned in favour of the pitch-and-ends method.)

## Plates read by eye

- **Plate X (`plate-010.jpg`).** Both girder elevations print "24'. 0"" for their length and
  "23'. 3¼"" / "23'. 5¼"" between centre lines. Fig. 3 girder: length 1,765 px vs height about
  223 px in the 2,400-px preview → 7.9 → 3.0 ft deep. Hand-assisted from a preview image.
- **Plate XX (`plate-020.jpg`).** Fig. 1 prints "36'. 0"" under the half of the strong deep truss and
  "6'. 0"" for its depth; the bar for elevations runs 0–20 ft. Half-truss length read as 35.5 ft
  from the column face to the centre line (−1.4%).
- **Plate VIII (`plate-008.jpg`).** Fig. 13 (column plan) prints "8"" across the flats and "11/16"
  for the wall at the connecting piece; "10"" over the flange. The column elevations (Figs. 1 to
  10) are drawn broken, so heights are not scalable from them.

## Second pass (same day): D05, D07, D08, D16, D17, D20, D21, D22

### Plate I — north addition, avenues, nave (D05, D07, D08)

- **Printed figures** read from crops: "936 · 0" along the north addition, "216 · 0" to its west and
  "696 · 0" to its east (216 + 936 + 696 = 1,848); "48 · 0" at the addition's west and east ends;
  "24 · 0" and "48 · 0" labels on the bays; "72 · 0" across the crossing.
- **Addition corners:** west corner (1,562, 815), east corner (6,147, 752) → 4,585 px along the
  tilted wall. Wall posts on the thick line every 39.3 px (west, 19 posts counted) and 39.9 px
  (east, 12 posts): 5 posts per 24 ft bay (117.9 px / 3 = 39.3). 4,585 / 39.3 = 116.7 intervals × 8
  ft = 933 ft; at 39.9 px it is 919 ft. An automatic post count along the wall failed because the
  wall is not straight on the warped sheet (it found 10 peaks), so the corner-to-corner method
  stands. **Hand-assisted.**
- **Depth:** wall posts down the west end of the addition at y = 165, 208, 248, 288, 328, 368, 407
  → six intervals of about 40 px (8 ft each) = 48 ft.
- **Avenue and nave:** in the crop at x 4,000–5,800, y 1,250–1,900, a 48 ft bay between column lines
  is 375 → 613 = 238 px (48.2 ft at 4.94 px/ft); the crossing is 733 → 1,085 = 352 px (71.3 ft).
  Dot-row spacing detection (blob finder) caught only some of the dots and was not used.

### Plate XVIII — vault radius (D20, D21)

- **Scale bar** (Fig. 1 sections), 30 ft: ticks at 0, 10, 20, 30 ft on a 2,000-px crop of x
  2,300–4,900: 509, 956, 1,406, 1,858 → 447, 450, 452 display px per 10 ft; × 1.3 = 58.4 px/ft at
  full resolution (scatter about ±0.6%).
- **Springing axis** (dotted horizontal line): y = 2,603. **Crown of the extrados** at the centre
  line (x ≈ 4,030): y = 432. Difference 2,171 px = 37.2 ft; a quarter circle, so radius 37.2 ft and
  diameter 74.3 ft. An attempt to fit circles automatically (RANSAC on edge pixels, then radial
  search) was thrown off by other drawings on the sheet and by the rib hatching, giving radii from
  2,070 to 2,215 px; those results were discarded. **Hand-assisted** (springing and crown levels
  chosen by looking, ±10 px ≈ ±0.5%).

### Plate VIII — base plates (D16)

Base-plan crops at x 200–2,250, y 3,050–3,560 and x 2,150–5,300, y 3,300–3,600 print:
"2'. 0"" with "1'. 0"" (Figs. 1 and 3 plans), "2'. 0"" with "1'. 6"" (Figs. 4–5), and under the
bottom elevations "3'. 0" × 1'. 6"" (three figures) and "3'. 0" × 2'. 0"" (two).

### Plate VI — concrete pads (D17)

At each of the 18 tier-1 column lines (x = 782 + 590.4 k) a speckled block below the floor line
(y = 2,697) was looked for in y 2,740–3,060. Nine readings were clean: thickness 1.25, 1.45, 1.74 (twice),
1.78, 2.3, 2.54, 2.58, 3.07 ft and widths 1.6–3.7 ft (24.74 px/ft). The other columns picked up
the dashed pile outlines or the plank line instead. **Hand-assisted and noisy;** consistent with the
text, not a precise check.

### Plate XXVII — louvre machinery (D22)

Viewed whole at 2,000 px. It has a 1 ft bar ("Scale", 12 in graduations) and no drawing or
dimension that corresponds to a 108 ft run. D22 cannot be checked against this plate.

### Plate VIII — column stack (D14, D15, D18, third pass)

- **Fig. 1** (outer column, first tier) prints "4'. 9"" from the floor to the top of the socket, "4"" for
  the socket sleeve, "6"" and "4½"" at the joint at floor level. **Fig. 3** prints "19'. 2"" from the
  "Level of Ground Floor" to the lower dashed girder line, and "3'. 0"" between the two dashed girder
  lines. **Fig. 12** (connecting piece with girder Q) prints "3'. 0"" on the girder and, at the foot,
  "2¼"" from the girder bottom to the underside of the lower flange P (also "2⅛"" and "1½"" on the
  lugs). The girder in Fig. 12 is drawn broken, so the printed figure, not the drawn length, governs.
  Read from crops at x 200–1,500, y 1,250–2,450 (Fig. 1 and Fig. 3) and x 5,750–7,350, y 250–1,850
  (Fig. 12). No scaling was done.
- **Printed page** (jp2 page 0017, read from crops; the OCR had three of these wrong): height above
  floor 18 ft 11¾ in; connecting piece C 3 ft 4½ in; B top 3¾ in; column A 18 ft 8 in; column E
  16 ft 7½ in; tier-3 column 16 ft 7½ in; piece H 3 ft 4½ in; total 62 ft 4¼ in; wall thickness ⅜ to
  1¼ in.
- **Arithmetic** (inches): 19 ft 2 in = 230; 230 − 2.25 = 227.75 = 18 ft 11¾ in (D14). Stack of the
  printed pieces: 227.75 + 40.5 = 268.25 (22 ft 4¼ in) = girder top 266 + 2.25; + 199.5 + 40.5 =
  508.25 = 506 + 2.25; + 199.5 + 40.5 = 748.25 = 746 + 2.25 = the stated total. No residual.

### Printed-page readings (fourth and fifth passes)

Scanned pages read off crops (tesseract was used only to find where each line sits, never for the
numbers): jp2 pages 0015 (glass, dates), 0016 (tiers, length, addition), 0017 (columns, pieces, totals),
0019 (girder heights), 0024 (truss), 0031 (gallery floor), 0036 and 0037 (rib, radius, diameter), 0053
(louvre run). The full list with what the OCR said is in CONTROL-DIMENSIONS.md ("Printed-page check").

## Plate XV (`plate-015.jpg`, 8,510 × 3,838 px): the staircases (added 2026-10-17)

Reproduced by `tools/measure_plate_xv.py` (in `run_all.sh`; output in `tools/output/run-2026-10-17.txt`):

- Scale bar ("Scale for Plans and Section"): 0, 10 and 20 ft ticks at x 1572, 836 and 3047 → 73.60 px/ft over
  0–10 ft and 73.75 px/ft over 0–20 ft; used 73.67 px/ft (the two baselines differ by 0.2%).
- The ground-floor line tilts across the sheet (0.21°; rows 2361.5, 2366.5, 2369.5 at x 5250, 6750, 7450), so heights
  are taken from the line interpolated at the feature.
- Landing beam, at the landing: top line row 1514 → **11.55 ft** above ground, underside row 1564.5 → 10.86 ft.
  Main gallery floor line (left of the first column): rows 654.5 and 662 → 23.12 and 23.02 ft. Landing beam top over
  the plate's own gallery line = **0.499** (half = 0.500). The printed gallery surface is 22 ft 11 in (22.92 ft); the
  plate's lines read 0.4 to 0.9% high, as Plate VI did (D12, 23.01 ft).
- Three main columns (centre of each pair of lines): x 4375.0, 6161.8, 7945.5, so 1,787 and 1,784 px apart: 24.25
  and 24.21 ft by the bar, or 74.4 px/ft if they are 24 ft apart. The sheet is about 1% wider across than the bar says
  (paper stretch); the overlay `model/previews/west02_v001_overlay_plateXV.png` uses 74.4 across and 73.65 up.
- Plan: 20 solid riser lines found on the first flight, 0.995 ft apart on average (64 to 79 px); with the dashed
  landing-edge line, the 21 lines span **19.90 ft** over 20 intervals. The label "21" sits beyond the last line, on the
  landing: 20 treads and the landing are the 21 steps.

Read by eye on gridded crops (not scripted): the six lowest tread nosings, spaced 6.49 in in height and 12.1 in in
going on average; the string's vertical depth (about 16 in, 1.15 ft square to the slope); the handrail 2.7 ft above the
nosing line; the landing columns 8.0 ft apart in the plan (838 and 1,162 on the 0.55-scale crop: 324 px at 40.5 px/ft).
Plate XVII Fig. 1 prints "7' 1"", "8' 5"", "7' 1"" above the strings. Printed page 33: the landing column is 13 ft 1 in
long, 10 ft 8 in above the floor.

Positions on Plates I and II (crops with 100 px grids): the stair bay is the 24 ft between the first avenue void (west
edge 24 ft in, "168.0" long) and the next ("192.0" long): Plate II shows the two shaded well-holes, 8 ft wide and
about 17 ft long by eye (text: 16 ft), in the middle 8 ft strip at both ends of the 48 ft avenue; Plate I shows the
hatched ground flights in the half of the avenue next to the nave (north avenue: its south half; south avenue: its north
half), the dotted upper flight beyond the landing. These are read by eye.

## Not measured

D22 as above (column heights are resolved by arithmetic on printed figures, not by scaling, because
the plate's column elevations are broken drawings; see CONTROL-DIMENSIONS.md), the rib section in D20 (1 ft 6 in × 8 in), and anything in the
prose of pages 19–58 beyond the 22 rows in the table.
