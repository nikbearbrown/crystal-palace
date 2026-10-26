# CONTROL-DIMENSIONS — from Cowper's text, checked against Downes's plates

Executive summary: 22 dimensions the text states outright, checked against the plates and the
printed page on 2026-10-17 in four passes. **20 now agree with the drawings** (some by measurement,
some because the plate prints the same figure), **1 is consistent** (D21, not independent), and **1
cannot be checked on any plate** (D22, the 108 ft louvre run). **Nothing is open.** The column-height
"conflict" (D14, D15, D18 vs D11) was my misreading plus OCR errors, not the source's: the connecting
piece is 3 ft 4½ in (the OCR said 4¼), it stands 2¼ in above and below the 3 ft girder it carries,
and the printed pieces add up to the stated 62 ft 4¼ in exactly. The vertical datum and the building
length (1,845 ft by bay count, against 1,848 stated) are also settled. Two more rows, D23 and D24 (where the gallery voids begin, printed on Plate II), were added when the model reached the void ends, and ten more, D25 to D34 (the first staircases and the stair bay, Plates I, II, XV to XVII and printed pages 31 to 35), when it reached 288 ft.

A control = a dimension read off a Tier 1 sheet (or printed on it) that the model is tested
against, independent of the model. Status vocabulary:

- `text` — stated in the prose only (OCR), not yet looked at on a plate
- `plate-printed` — the same figure is printed on the plate itself
- `plate-checked` — measured on the plate against its own scale or its own 24 ft grid
- `plate-open` — measured or read, and unresolved

How precise: the printed scale bar on Plate VI has ±0.7% tick scatter, the plan sheets are
paper-warped, and the rows measured by script look in windows chosen by eye (±0.2 ft on Plate VI,
roughly ±1–2% elsewhere). Treat agreements below about 1% as "agree", not as exact.
Reproducible: `bash tools/run_all.sh` runs the five scripts (`measure_plate_vi.py`, `_i`, `_x`, `_xviii`,
`_xx`) and saves the output with library versions and plate checksums to `tools/output/`. The raw
numbers, and where each script differs from my earlier hand readings, are in `MEASUREMENTS.md`.

Source for every row: `text/downes-1852-ocr-fulltext.txt`, EPUB page numbers (`[page N]`).

| ID | Dimension | Value | Plate | Status | Evidence |
|---|---|---|---|---|---|
| D01 | Length, centre to centre of columns | 1848 ft | I | **plate-checked** + printed | Plate I prints "1848 · 0". End walls 9,063 px apart ÷ mean dot pitch 117.9 px = 76.9 bays × 24 ft = 1,845 ft (−0.2%). Against the scale bar (4.94 px/ft) it reads 1,835 ft (−0.7%), inside the bar's scatter |
| D02 | Width of lowest tier | 408 ft | I, VI | **plate-checked** + printed | Plate VI: 405.8 ft (−0.5%). Plate I prints "408 · 0" at both end walls |
| D03 | Width of second tier | 264 ft | VI | **plate-checked** | Plate VI: 262.8 ft (−0.5%) |
| D04 | Width of third tier | 120 ft | VI | **plate-checked** | Plate VI: 119.6 ft (−0.3%) |
| D05 | North-side addition to lowest tier | 936 ft × 48 ft | I | **plate-printed** + checked | Plate I prints "936 · 0" along it and "48 · 0" at its ends; its north dimension chain 216 + 936 + 696 = 1,848 ft closes. Script (`tools/measure_plate_i.py`): end walls 4,581 px apart = **936.0 ft** with the local dot pitch (+0.04%), 931 ft with the single global pitch; depth: seven wall posts, six 8 ft intervals = 48 ft |
| D06 | Primary unit | 24 ft | I, VI, X | **plate-checked** + printed | Plate VI third tier: bays 587.8–597 px, mean 591.7 px = 23.9 ft. Plate I dot pitch 117.9 px = 23.9 ft at 4.94 px/ft. Plate X prints "24'. 0"" on both girder elevations |
| D07 | Wider avenues | 48 ft | I | **plate-printed** + checked | Plate I prints "48 · 0" in several bays. Script: dot pairs on one row near 48 ft in the crossing area, 8 pairs, median 48.0 ft (−0.1%), range 46.5–49.1 |
| D08 | Central avenue (nave) | 72 ft | I | **plate-printed** + checked | Plate I prints "72 · 0" across the crossing. Script: dot pairs on one row near 72 ft, 7 pairs, median 72.4 ft (+0.6%), range 71.7–75.8 |
| D09 | Gutter pitch | 8 ft | VI, XII | **plate-checked** | Plate VI third-tier roof: ridge finials repeat every 197.5 px = 7.98 ft |
| D10 | Girder depth | 3 ft | VIII, X, VI | **plate-printed** + checked (rough) | Plate VIII Fig. 3 prints "3'. 0"" between the girder bearing lines, and Fig. 12 prints it on the girder. Earlier checks: | Plate VIII Fig. 3 prints "3'. 0"" between the girder bearing lines, and Fig. 12 prints it on the girder. Script (`tools/measure_plate_x.py`): with the printed "24'. 0"" centre-to-centre as ruler (220.5 px/ft), the girder is 23.25 ft face to face (printed 23 ft 3¼ in, −0.08%) and 2.97 ft deep between the inner flange lines (−1.0%), 3.16 ft overall including flanges. Plate VI tier 3 lines at 2.63, 3.04 and 3.28 ft are candidates only |
| D11 | Ground floor to top of girders, tiers 1–3 | 22 ft 2 in; 42 ft 2 in; 62 ft 2 in | VI, VIII | **plate-printed** (tier 1) + checked | Plate VIII Fig. 3 prints "19'. 2"" from the floor to the girder bottom and "3'. 0"" for the girder: 22 ft 2 in for tier 1 exactly. Plate VI: datum = the ground-floor line at the column feet on Plate VI (y = 2697). Top-flange lines read 62.34 and 42.30 ft above it (+0.17 and +0.13 ft, inside ±0.2 ft); tier spacing 20.04 ft. Script (`tools/measure_plate_vi.py`) reproduces these. The tier-1 line is ambiguous: candidate lines read 23.01, 22.50 and 21.99 ft; assuming the 20 ft spacing it picks 22.50 ft (+0.33 ft), so tier 1 rests on the printed 19 ft 2 in + 3 ft 0 in |
| D12 | Gallery floor above ground floor | 22 ft 11 in | VI | **plate-checked** | Plate VI gallery floor line reads 23.01 ft (+0.09 ft). Printed page 31: "The surface of the Gallery floor is 22 ft. 11 in. above the ground floor" (the OCR read "11 im") |
| D13 | Column external diameter | 8 in | VIII | **plate-printed** + printed page | Plate VIII Fig. 13 prints "8"" across the flats. The printed text (p. 4 of the book) says "external diameter is in every case 8 in., the internal diameter only being varied", wall thickness ⅜ in to 1¼ in (the OCR read this as "2 in. to 1¼ in.") |
| D14 | Outer ground-floor column, height above floor (= bottom of the connecting piece) | 18 ft 11¾ in | VIII | **plate-printed** + printed page | The printed page reads 18 ft 11¾ in. Plate VIII Fig. 3 prints "19'. 2"" from the floor to the girder bottom and Fig. 12 prints "2¼"" for the piece below the girder: 19 ft 2 in − 2¼ in = 18 ft 11¾ in exactly. Also 3¾ in (B above floor) + 18 ft 8 in (column A) = 18 ft 11¾ in, as the page says. The elevations are drawn broken, so this is arithmetic on printed figures, not a scaled height |
| D15 | Connecting piece length | **3 ft 4½ in** (OCR said 4¼) | VIII | **plate-printed** + printed page | The printed page reads 3 ft 4½ in in all three places (Figs. 1, 3, 6). 2¼ in below the girder (printed, Fig. 12) + 3 ft 0 in girder (printed) + 2¼ in above = 3 ft 4½ in, symmetric about the girder |
| D16 | Base plates | 2 ft × 1 ft (outer ground-floor column) up to 3 ft × 2 ft | VIII | **plate-printed** | Plate VIII's base plans print "2'. 0" × 1'. 0"" (Figs. 1 and 3), "2'. 0" × 1'. 6"" (Figs. 4 and 5), "3'. 0" × 1'. 6"" (Figs. 6–8) and "3'. 0" × 2'. 0"" (Figs. 9–10), as the text says |
| D17 | Foundation concrete depth | 1 to 4 ft | VI | **plate-checked** (loose) | Plate VI shows a pad under each column. Script: of 18 columns, 10 give clean readings under a stated rule (top 1.2–2.1 ft below the floor line, thickness 1–3.5 ft, width 1.4–4 ft): pad thickness 1.25–3.48 ft, width 1.58–3.72 ft, deeper and wider under the inner columns that carry more. Consistent with "1 to 4 ft, varying with the load"; the other 8 picked up pile outlines or nothing, so it is a loose check |
| D18 | Total height of outer column, three-storey (top of the upper connecting piece) | 62 ft 4¼ in | VIII | **plate-checked** (printed page) | The printed page gives the pieces: 18 ft 11¾ in, then 3 ft 4½ in, 16 ft 7½ in, 3 ft 4½ in, 16 ft 7½ in, 3 ft 4½ in. They sum to 62 ft 4¼ in, exactly the stated total (and 22 ft 4¼ in, 42 ft 4¼ in on the way up) |
| D19 | Wrought-iron truss over nave | 72 ft × 6 ft deep | XX | **plate-printed** | Plate XX Fig. 1 prints "36'. 0"" for half the strong deep truss and "6'. 0"" for its depth. Script (`tools/measure_plate_xx.py`): the panels are 8 ft (147.6 px/ft, ±0.5%); first post to the truss centre line 28.01 ft (36 − 8); centre line to the left-edge lines 35.0–35.8 ft (−0.5% to −2.7% depending on which line is the column centre line); depth 6.10 ft between outer rail edges (+1.7%). For a model: the 72 ft is centre to centre of columns (tested as D08); a truss part measures face to face about 71.2 ft (four estimates, 70.8–71.6 ft) and 6.0 ft deep outer to outer (the printed 6'. 0" runs from the top of the top rail to the underside of the bottom rail; arrow tips read 5.93 ft). See `controls.json` D19a and D19b |
| D20 | Transept rib, extrados diameter | 74 ft 4 in; section 1 ft 6 in × 8 in | XVIII | **plate-checked** (diameter) | Script (`tools/measure_plate_xviii.py`): scale bar 58.57 px/ft (0/10/20/30 ft ticks, ±0.7%); springing axis y 2,603 to crown of the extrados y 432 = 2,171 px = radius 37.07 ft, diameter **74.14 ft** (stated 74 ft 4 in = 74.33 ft, −0.26%). Using the next rib lines as the crown would give 72.8–73.8 ft, so the choice of the extrados line matters. Printed page 37: "a general section of 1 ft. 6 in. deep by 8 in. wide, and 74 ft. 4 in. diameter on the extrados". Rib depth: candidate lines 1.43 and 1.61 ft below the extrados |
| D21 | Timber rib cut radius | 37 ft | XVIII | consistent with D20 | Script radius 37.07 ft (+0.19% vs 37 ft); not an independent measurement, since the plate shows the arc, not the cutting template. Printed page 36: "cut to a curve of 37-ft. radius" (the same page gives pieces 13⅝ in wide, about 9 ft 6 in long, 4 in thick; the OCR read 13⅝ as "138") |
| D22 | Louvre run moved by one wheel | 108 ft each side | XXVII | text | No plate shows this: Plate XXVII draws the louvre mechanism at detail scale (1 ft bar). Printed page 53 confirms the figure: "A length of 108 ft. on each side of the wheel is thus set in motion simultaneously". It can only be checked against the prose, or by counting louvre bays on Plates XXI–XXII |
| D23 | Avenue voids start this far from the west end (gallery plan) | 24 ft | II | **plate-printed** | Plate II prints "24.0" at the west end. A ruler laid from the west wall (4.4 px per ft in the crop) puts the void's west edge on the 24 ft line within about 0.3 ft (by eye). Added 2026-10-17 when the model reached the void ends |
| D24 | The nave void starts this far from the west end | 72 ft | II | **plate-printed** | Plate II prints "72.0". Same ruler: the nave void's west edge sits on the 72 ft line within about 0.3 ft (by eye). Also the avenue voids run 168 ft ("168.0") to 192 ft, then a 24 ft landing for the first staircases ("24.0"); not yet a control |
| D25 | The first avenue voids run this long (gallery plan) | 168 ft | II | **plate-printed** | Plate II prints "168.0" between the void's west end (24 ft in) and the stair bay (192 ft in). Added 2026-10-17 |
| D26 | The stair bay between the two avenue voids | 24 ft | II | **plate-printed** | Plate II prints "24.0"; it holds the cross gallery and the two staircases (192 to 216 ft). The next void is printed "192.0" (216 to 408 ft), not built beyond 288 ft |
| D27 | Stair landing width | 8 ft | XV, p. 31 | plate-checked | Text: "a landing 24 ft. long and 8 ft. wide". The Plate XV plan puts the two rows of landing columns 8.0 ft apart (by eye on a gridded crop) |
| D28 | Stair landing length | 24 ft | p. 31 | text | Text only. The columns that carry it stand 22 ft 7 in apart (D29) |
| D29 | Landing columns, outermost to outermost | 22 ft 7 in (7 ft 1 in + 8 ft 5 in + 7 ft 1 in) | XVII Fig. 1, p. 32 | **plate-printed** | Plate XVII Fig. 1 prints 7' 1", 8' 5", 7' 1"; the text says the same. They are the centre-to-centre distances of the strings of the lower flights |
| D30 | Top of a landing column above the floor | 10 ft 8 in | p. 33 | text | Text: the column is 13 ft 1 in long, 10 ft 8 in above the floor and 2 ft 5 in below, 5 in outside, ½ in of metal. Plate XVI Fig. 4 not read for figures |
| D31 | Landing surface above the floor | 11 ft 5½ in (half of 22 ft 11 in) | XV | plate-checked | Printed nowhere. `tools/measure_plate_xv.py`: beam top 11.55 ft by the plate's bar (tilt-corrected ground line), and 0.499 of the plate's own gallery floor line |
| D32 | Stair flight run, floor to landing | 20 ft (20 treads of 1 ft; the landing is the 21st step) | XV, p. 32 | plate-checked | Text: 21 steps in each flight. Plan: riser lines 0.995 ft apart, 20 intervals span 19.90 ft (script) |
| D33 | Cross gallery over a staircase, long side | 48 ft | p. 31 | text | Text only: it equals the 48 ft avenue void of D07 |
| D34 | Cross gallery, short side | 24 ft | p. 31 | text | Text only: it equals the 24 ft stair bay of D26. The two well-holes (8 ft by 16 ft) cannot be a gate control: a gap has no part to measure |

## The column stack (D14, D15, D18 vs D11), worked in inches

First pass I read D14 + D15 = 22 ft 4 in as "disagrees with the girder top at 22 ft 2 in", and thought
the source contradicted itself. Two things were wrong. The connecting piece does not top out flush
with the girder (it is longer than the girder is deep and the girder sits inside it), and the OCR
had misread several fractions. Reading the printed page (jp2 page 0017) settles it:

| Piece (printed page) | Length | Running top above ground floor |
|---|---|---|
| Lower column B top | 3¾ in | 3¾ in |
| Column A | 18 ft 8 in | 18 ft 11¾ in (= D14) |
| Connecting piece C | 3 ft 4½ in | **22 ft 4¼ in** |
| Column E (tier 2) | 16 ft 7½ in | 38 ft 11¾ in |
| Connecting piece F | 3 ft 4½ in | **42 ft 4¼ in** |
| Column (tier 3) | 16 ft 7½ in | 58 ft 11¾ in |
| Connecting piece H | 3 ft 4½ in | **62 ft 4¼ in** (= D18, as printed) |

- Girder tops (D11) are 22 ft 2 in, 42 ft 2 in, 62 ft 2 in. Piece tops are **2¼ in above them on all
  three tiers**.
- Girder bottom = girder top − 3 ft 0 in = 19 ft 2 in (printed on Plate VIII Fig. 3). The piece starts
  at 18 ft 11¾ in, **2¼ in below** the girder bottom (printed on Fig. 12 as "2¼""): 19 ft 2 in − 2¼ in
  = 18 ft 11¾ in, exactly D14.
- 2¼ in below + 3 ft 0 in girder + 2¼ in above = 3 ft 4½ in = D15. Symmetric about the girder.
- **Nothing is left over.** The stack reaches the stated 62 ft 4¼ in exactly. The ¼ in "residual" in
  my second pass came entirely from the OCR (4¼ for 4½, 7¾ for 7½).

**OCR warning.** The OCR is unreliable on fractions, which is where the gate lives. Confirmed misreads:
3 ft 4½ in read as 4¼; 16 ft 7½ in read as 7¾ or "'74"; 3¾ in read as "33 in."; wall thickness
⅜ in read as "2 in"; glass slope 2½ to 1 read as 24 to 1; 13⅝ in read as 138; 31st read as 81st. Treat every fractional figure in this table that was not read off the
printed page or a plate as unverified. These have now been read on the page (table below).

The lesson for the gate: a figure that looks wrong may be the wrong figure being compared, or a
misread one. Work the build-up and read the printed page before declaring a conflict.

## Printed-page check of the fractional and text-only figures (2026-10-17)

Each figure below was read off the scanned printed page (jp2 pages 0015–0053; the book's own page
numbers differ), not off the OCR. "OCR" says what the text layer had.

| Figure | Printed page | Printed | OCR said |
|---|---|---|---|
| Glass length; slope | 15 | 49 inches; **2½ to 1** | 49 inches; **24 to 1** (wrong) |
| Gutter pitch; unit | 15, 12 | 8 feet; 24 ft ("one primary dimension, 24 feet") | same |
| Contract dates | 15 | 26th July 1850; **31st** October; 26th September | 81st October (wrong) |
| Tier widths; length | 16 | 408 ft, 264 ft, 120 ft; 1848 ft "or about 1850 ft over all"; 936 ft × 48 ft | same |
| External diameter; wall thickness | 17 | 8 in; **⅜ in to 1¼ in** | 2 in to 1¼ in (wrong) |
| Concrete depth; base plates | 17 | 1 ft to 4 ft; 1 ft × 2 ft up to 3 ft × 2 ft | same |
| Column above floor; socket | 17 | 18 ft 11¾ in; 4 ft 9 in | 113 in (11¾); same |
| Connecting piece | 17 | **3 ft 4½ in** (three places) | 3 ft 4¼ in (wrong) |
| Fig. 3: B above floor; A; tier columns | 17 | **3¾ in**; 18 ft 8 in; **16 ft 7½ in** (twice) | 33 in (wrong); same; 7¾ / "'74" (wrong) |
| Total height, three-storey | 17 | 62 ft 4¼ in | 62 ft 4¼ in |
| Girder depth; tier tops | 19 | 3 ft; 22 ft 2 in, 42 ft 2 in, 62 ft 2 in | same |
| Gallery floor | 31 | **22 ft 11 in** | 22 ft 11 im (damaged, right value) |
| Rib: pieces; cut radius | 36 | 13⅝ in wide, 9 ft 6 in long, 4 in thick; 37-ft. radius | 138 in wide (wrong); same |
| Rib section; extrados | 37 | 1 ft 6 in deep by 8 in wide; 74 ft 4 in diameter | same |
| Truss | 24 | 72 ft long and 6 ft deep | same |
| Louvre run | 53 | 108 ft on each side of the wheel | same |

So the OCR was right on whole feet and inches and wrong on fractions: **7 of the 8 wrong
readings were fractions** (the eighth was a date). Every fractional figure used in this table is now read off the page or the
plate. Nothing else in the 22 rows disagrees with the printed page.

## What changed from the first pass

- The earlier "19.7 ft tier spacing" was wrong: it came from reading the wrong line. With the actual
  top-flange lines the spacing is 20.04 ft.
- "Tilt-corrected" turned out to be the wrong idea for Plate I. A 1.3° tilt changes a length by 0.03%.
  The real error is paper warp (lines on the left of the sheet run at −1.4° to −2.1°, in the middle
  and right at −0.8°). The plan's own 24 ft column grid is a better ruler than the scale bar.

## Not yet done

All 22 rows have now been looked at. What remains:

- **D22** needs a count of louvre bays on Plates XXI–XXII, or stays prose-only.
- **D20's rib section** (1 ft 6 in × 8 in) is confirmed on the printed page and only loosely on the
  plate (candidate lines 1.43 and 1.61 ft deep).
- The scripts look in windows chosen by eye and print every candidate; a script that finds its own
  windows (so a different scan could be measured unattended) has not been written.
- The prose on pages 19 to 58 names further per-component dimensions (sash-bars, staircase flights,
  lead flats, gutter sections) that are not in this table.

A real dimension gate wants 10 to 20 independent controls. We have 20 that agree, but many share a
sheet (D02–D04, D06, D09, D11, D12, D17 are all Plate VI; D01, D05, D07, D08 are all Plate I), so
the agreements rest on six sheets: Plates I, VI, VIII, X, XVIII and XX.
