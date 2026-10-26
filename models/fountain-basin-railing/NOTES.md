# Fountain-basin railing — NOTES

## What this is

A 90° quadrant of the ornamental cast-iron railing that rings the basin of
the Osler Crystal Fountain: four identical bays of floral cast panels between
finialed posts, a rounded handrail, bands of small turned knobs above and
below each panel, and a low floor curb following the curve. It is built to
pair with candidate #12 (the fountain itself, not yet built), so the arc is
delivered as a quadrant that can be repeated or re-radiussed.

Film context: the fountain is the transept centrepiece (storyboard CP022).
This railing is documented by one photograph — see "Open questions" below
before captioning it to a specific building or year.

## Sources used

- **Primary — the only clear view of the railing:**
  `references/muse-drive/images/commons/View_of_Transept,_Looking_South_MET_DP238264.jpg`
  (photograph, Metropolitan Museum of Art; manifest licence **CC0**,
  http://creativecommons.org/publicdomain/zero/1.0/deed.en; 2788 × 3863 px).
  Copied into `refs/`. The railing fills the foreground: one full panel bay
  and the post finials are legible at the left; the run curves away to the
  right, ringing the basin with the fountain playing behind it.
- **Basin-size cross-check:**
  `references/muse-drive/images/commons/Catalogue_of_the_great_exhibition_Wellcome_L0022578.jpg`
  (engraving, CC BY 4.0) and
  `references/muse-drive/images/commons/Great_Exhibition_fountain_1851.jpg`
  (engraving, public domain). Both show the 1851 Hyde Park basin as a plain
  low circular rim — no railing — with its diameter readable against the
  fountain.
- **Checked, no fountain/basin dimension found:**
  `references/muse-drive/review/dimensions-from-1856-guide.json` (building
  dimensions only); the Routledge 1851 guide plan (scan p.0007, gallery
  0726) marks the fountain with a small symbol circle, not a measurable
  basin outline; `REVIEW.md` and `MODEL-AND-FILM-PLAN.md` discuss the
  fountain but give no basin size.

## Dimensions — measured vs inferred

| Dimension | Value | Basis |
|---|---|---|
| Overall height, floor to top of handrail | **1.07 m** | **Inferred.** No railing dimension exists in the references. Anchor: the bay's proportions measured from the photograph (next rows), set to a plausible period railing height. Treat as ±10%. |
| Panel field height | 0.64 m | **Measured proportion:** in the photograph's nearest bay the panel is ≈65% of the total height; upper knob band ≈15%; lower band + bottom rail + curb ≈20%. Applied to the 1.07 m anchor. |
| Bay width (chord, post centre to post centre) | 1.37 m | **Measured proportion + fit:** nearest bay's width ≈ its height in image space, ≈1.3 × height after correcting for the bay's oblique (~40°) angle; the 4-bay quadrant at R 3.5 m gives chord 1.366 m, consistent with that ratio. |
| Panel width | 1.30 m | Bay chord minus post shaft (Ø 0.072 m). |
| Basin radius R | **3.5 m** (basin Ø 7.0 m ≈ 23 ft) | **Inferred.** Wellcome engraving: basin Ø ≈ 0.85 × fountain height; fountain height is documented historically at ~27 ft (8.2 m) → Ø ≈ 7.0 m. The opening-day engraving implies a smaller basin (Ø ≈ 5.3 m, R ≈ 2.7 m). Engravings are not measured drawings, so the radius carries wide uncertainty. All parts are parametric in R in the build script — re-run with a new R if the fountain build (candidate #12) settles a different basin. |
| Post height to finial tip | 1.32 m | Post profile read from the photograph (finial rises ≈ 0.25 m above the handrail). |
| Post spacing | 22.5° (arc length 1.37 m) | 4 bays per 90° quadrant, chosen so the bay proportion above holds at R 3.5 m. |
| Panel cast thickness | 0.03 m | **Guessed** — typical light ornamental casting; not measurable from the photograph. |
| Mesh | 44,494 triangles, one joined mesh, 23,625 vertices | Bounding box 3.66 × 3.66 × 1.32 m; origin at the centre of the arc's circle, base at z = 0, real-world metres, scale applied. |

## What was seen vs what was guessed

**Seen in the photograph, and modelled:**

- A curved run of repeated bays ringing the basin.
- One large ornate cast panel per bay: a wide oval medallion containing a
  radial flower (central boss, petals radiating to the oval), vine scrolls
  and leaf forms filling the panel corners, and a strong vertical/horizontal
  cross behind the medallion.
- A row of small turned knob (bud) ornaments in a band above each panel,
  and a matching band below it.
- A smooth rounded top handrail following the curve.
- Posts between bays with collar rings, topped by a finial: a pointed
  spire passing through a ring.
- A low curb/plinth strip at the floor line following the curve.
- Dark, black-painted iron throughout.

**Guessed or interpreted (not traceable from the photograph):**

- The exact motif. The repeat is legible, but not line-by-line: petal
  count (16 + 16), scroll paths, tendrils and leaf shapes are a
  **schematic interpretation at the same visual density**, not a
  foundry-exact copy of the casting.
- The post turning profile and finial construction.
- Every absolute dimension in the table above (all are inferred or
  proportion-derived, as labelled).
- Panels are bent to the basin radius. The photograph is consistent with
  either curved castings or short flat facets; at 1.37 m bays the
  difference is ~3 cm and cannot be resolved from the image.

## Known inaccuracies / open questions

- **A second treatment is visible in the same photograph** and is **not
  modelled**: further along the run, a taller section of plain vertical
  balusters over a panel band, its top rail rising — possibly a stair or
  terrace-edge section of the same screen. One photograph cannot resolve
  it.
- **Hyde Park or Sydenham?** The two 1851 engravings show the Hyde Park
  basin rim plain, with visitors standing at it and no railing. The
  panelled railing is documented only by the transept photograph in this
  collection. Whether it is an 1851 fitting, a Sydenham addition, or both
  is **not established by the repo's references** — flagged here, not
  resolved. Do not caption this model as certainly 1851.
- The fountain (candidate #12) is unbuilt; this quadrant's handrail ends
  are open tube ends and will read as unfinished until the arc is joined
  into a fuller ring.
- The back face of the panels is the same casting thickness throughout;
  any rear bracing the original may have had is not visible in the
  photograph and is not modelled.

## Build

- `scripts/build_fountain_basin_railing.py` — fully procedural bpy
  (Blender 4.2, headless). Key parameters (R, bays, heights) are at the
  top of the file.
- `scripts/render_rig.py` — the fixed neutral-grey studio rig used for
  `renders/` (Cycles; it opens the saved .blend and does not modify it).
  Note: EEVEE hangs in this VM, hence Cycles.
- Renders: `front.png` (outside the arc on its bisector), `side.png`
  (along the arc), `three-quarter.png`, and `compare.jpg` (photograph
  crop at left, front render at right).
- Built over three rounds: proportions and structure from the photograph
  (r1), motif density increased to match the photograph's fill (r2),
  final polish of oval size, petal width and knob seating (r3).
