# NOTES — Cast-iron column, complete (three-storey)

Prop for the Crystal Palace film. Hyde Park 1851 building only — no
Sydenham evidence is used in this model.

## What it is

The COMPLETE three-storey outer column of the 1851 Hyde Park palace, as
drawn in Downes Plate VIII Figs. 6–8, modelled once so it can be
instanced everywhere the building needs its standard column:

- foundation piece **B** — flared foot on a 3 ft 0 in × 1 ft 6 in base
  plate, rising to 3¾ in above the ground floor;
- lower column **A** — 18 ft 8 in;
- connecting piece **C** — 3 ft 4½ in, carrying the tier-1 girder in its
  bearing (girder bottom 19 ft 2 in, top 22 ft 2 in);
- tier-2 column **E** — 16 ft 7½ in;
- connecting piece **F** — 3 ft 4½ in (tier-2 girder, top 42 ft 2 in);
- tier-3 column **G** — 16 ft 7½ in;
- top connecting piece **H** — 3 ft 4½ in, open at the top, one girder
  bracket only (Fig. 6), total height **62 ft 4¼ in (19.006 m) above the
  ground floor**.

Short truncated girder stubs (0.85 m, cut) sit in the bearings of C, F
and H so the joint reads in isolation; the real girders spanned the full
24 ft bay. The Plate XIV ornamental bands — octagonal ogee-profile
collars — dress the column at the two gallery floors (22 ft 11 in and
42 ft 11 in).

Units: metres. Origin at the centre of the column at ground-floor level
(z = 0); the foundation foot extends 0.610 m below the origin.
Blender 4.2+. 92 objects, 3,284 triangles.

## Relationship to `hyde-park-column-tier1/`

That prop (another builder) models ONLY the tier-1 length — floor to
the top of the first girder, 22 ft 2 in — with a girder stub. This model
is the full-height general component (all three tiers, both gallery
joints, the top connection, the foundation foot and the ornamental
bands). They are complementary, not duplicates; where they overlap they
differ in one dimension, reconciled below.

## The 8-inch question (read this before reusing either model)

- The tier-1 NOTES read Plate VIII Fig. 13's printed "8"" as the column
  **bore**, chose a nominal 1 in wall inside the printed ⅜–1¼ in range,
  and modelled a 10 in (0.254 m) outer diameter.
- Fig. 13's 8 in dimension line in fact runs across the **outside of the
  section** (it is the middle segment of the 3½ + 8 + 3½ in chain across
  the connecting-piece plan), and Downes's printed text (p. 17, read off
  the printed page in `CONTROL-DIMENSIONS.md` D13) states outright:
  "the external diameter is in every case 8 in., the internal diameter
  only being varied", wall thickness ⅜ in to 1¼ in.
- **This model therefore uses the printed external diameter, 8 in
  (0.203 m).** On the same evidence the tier-1 prop's shaft is ~25 %
  oversize in diameter. The discrepancy is recorded here, not silently
  papered over; the tier-1 folder is the other builder's and has not
  been altered.

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-008.jpg` — Downes
  Plate VIII, "Details of columns" (John Weale, Jan 1852; public
  domain). Figs. 1–5 single/two-storey columns and bases, Figs. 6–8 the
  three-storey column, Fig. 12 the girder connection enlarged, Fig. 13
  the connecting-piece plan enlarged. Crops in `refs/`.
- `references/downes-1852/source-scans/plates/plate-014.jpg` — Plate
  XIV, "Details of gallery, and ornamental bands on columns"; Figs.
  9–13 are the band: Fig. 11 elevation, Fig. 12 octagonal plan,
  Fig. 13 the ogee profile ("b projects ⅝ in"). Crop in `refs/`.
- `references/muse-drive/images/commons/The_Crystal_Palace_page_52b.jpg`
  — "Section of column of the Crystal Palace" (manifest licence: Public
  domain). The small diagram that shows the shaft section: a round tube
  with four external longitudinal ribs.
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` —
  controls D10–D18, read off the printed pages and plates by the
  project's dimension pass (the stack arithmetic below is D14/D15/D18).
- `references/downes-1852/crystal-palace-1851/PLATE-INDEX.md` — plate
  identification.

## Dimensions — measured/printed vs guessed

| Part | Value | Status |
|---|---|---|
| Total height above floor | 62 ft 4¼ in (19.006 m) | **Printed** (text p. 17; D18) — and the pieces below sum to it exactly |
| Piece stack | B top +3¾ in; A 18 ft 8 in; C 3 ft 4½ in; E 16 ft 7½ in; F 3 ft 4½ in; G 16 ft 7½ in; H 3 ft 4½ in | **Printed** (text p. 17; D14/D15) |
| Girder depth / seating | 3 ft 0 in; connecting piece stands 2¼ in below and above it | **Printed** (Plate VIII Figs. 3, 12; D10/D11/D15) |
| Girder tops | 22 ft 2 in / 42 ft 2 in / 62 ft 2 in | **Printed** (D11) |
| Gallery floors | 22 ft 11 in (and +20 ft) — bands sit at these levels | **Printed** text p. 31 (D12) + plate-checked |
| External diameter | 8 in (0.203 m), every tier | **Printed** (text p. 17; Fig. 13; D13) — see the 8-inch section above |
| Shaft wall / bore | wall 9/16 in → bore 6⅞ in (0.175 m) | **Printed** on the joint plans at o.o / m.m / l.l (9/16 in); wall range in text ⅜–1¼ in |
| Connecting-piece drum wall | 11/16 in | **Printed** on Fig. 13 |
| Base plate (foot plan) | 3 ft 0 in × 1 ft 6 in (Figs. 6–8 size) | **Printed** on Plate VIII (D16) |
| Bolt holes | 1¼ in dia, 4 at the diagonals | **Printed** (Fig. 13) |
| Bolt spacing | 10 in (lower joints), 9¾ in (upper) | **Printed** (Fig. 6 / Fig. 13) |
| Connecting-piece plates P | octagon Ø ≈ 0.48 m across corners, 2¼ in thick (= the printed proud amount) | Plate-**measured** proportion, thickness printed |
| Drum outer diameter | 0.254 m (10 in) | Plate-**measured** estimate (Fig. 12 against the printed 3 ft girder) |
| Girder-bearing lugs P | protrude ±X at both plate levels | Seen Fig. 12/13; size estimated |
| Ornamental band | octagonal, max Ø ≈ 0.53 m, 0.50 m tall, ogee profile | Profile **seen** (Pl. XIV Fig. 13, ⅝ in projection printed); plan **seen** (Fig. 12); absolute size plate-measured estimate |
| Foundation depth below floor | 0.610 m (2 ft) | **Inferred** — concrete depth is printed as 1–4 ft varying with load (D17); B is drawn broken on the plate, so no single depth is dimensioned |
| Girder stubs | 0.85 m long, flanges 0.22 m wide, web tapered 0.85 → 0.52 m deep | Truncation is a **modelling choice**; depth at the column is the printed 3 ft |
| Bracing strap on G | plate + nut on the +Y face | **Seen** in Fig. 6 elevation; size estimated |
| Paint colour | light warm grey painted iron | **Interpretive** (as the tier-1 prop): ironwork was painted, exact 1851 colour not verified |

## The bore

The columns were hollow cast iron (they doubled as rainwater
down-pipes). The bore **is modelled**: every shaft and drum is a true
tube with the printed wall thickness, so the bore is visible at the open
top of H, at the foot, and in section. The interior carries a dark
material (`BoreDark`) so the tube reads hollow rather than glassy.

## What was NOT modelled / known inaccuracies

- The girder stubs are simplifications: solid tapered web, top and
  bottom flanges. The plate's triangular web lightening and internal
  stiffeners (Fig. 12) are not cut, and the wedges/pins (T, U, S of
  Fig. 12) at the girder ends are not modelled.
- Flange plates are regular octagons; the plate's joint plans show
  octagonal plates with shaped bolt-lug ears — approximated by the
  octagon plus separate hex nuts. Bolt heads are hex nuts only (no
  shanks through hidden plates except where the joint shows them).
- The ornamental band is a lathed (8-sided) reading of the Plate XIV
  profile; the plate's panelled casing construction (Fig. 12's separate
  C panels) is represented by the collar form and four spacer blocks,
  not by individual panels.
- The foundation piece B is drawn broken on Plate VIII; its flare
  profile is read from Figs. 1–10 and its depth is inferred (above).
  The D pipe (7 in) through the base of Figs. 3/5 is not modelled.
- The shaft ribs follow the page-52b section diagram; their exact width
  is estimated. In Fig. 13 the section's flats are chord flats rather
  than raised ribs — the model splits the difference with low ribs
  (6 mm proud), recorded here.
- Diagonal bracing between columns is Plate IX's subject, not this
  prop's; the single strap on G is the only bracing fitting included.

## QC

- Build script prints the evaluated count from the saved model:
  92 objects, 3,284 triangles — well under the ~50,000 budget.
- Stack check: modelled tops land at 18 ft 11¾ in / 22 ft 4¼ in /
  38 ft 11¾ in / 42 ft 4¼ in / 58 ft 11¾ in / 62 ft 4¼ in, matching the
  printed running totals (CONTROL-DIMENSIONS stack table) to <1 mm.
- Round 1 renders: stack, stubs and bands all read correctly; the
  three-quarter camera clipped the top of H and the iron read too pale
  — camera pulled back, iron darkened, stubs shortened 0.95 → 0.85 m
  with a deeper web end.
- Round 2 renders viewed: front, side, three-quarter and the tier-1
  joint close-up (compare `renders/detail-tier1-joint.png` with
  `refs/plate-008-fig12-connection.jpg`: plates P, drum and the girder
  seated between them).

## Files

- `cast-iron-column.blend` — model collection `Model` plus an empty
  `RenderSetup` collection (the render script builds its rig fresh).
- `cast-iron-column.glb` — `Model` collection only.
- `renders/` — front, side, three-quarter, tier-1 joint close-up, and
  a plate-vs-model compare.
- `refs/` — the two plates, the section diagram, and the crops used.
- `scripts/` — `build_cast_iron_column.py` (the model is the script),
  `render_cast_iron_column.py` (fixed neutral-grey rig, Cycles CPU).
