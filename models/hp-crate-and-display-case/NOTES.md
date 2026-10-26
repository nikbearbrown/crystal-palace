# NOTES — 1851 exhibition table case (vitrine) + deal packing crate

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 1, item 6).
Scenes: CP019 (the world arrives in cases), CP024 (machinery section
dressing — case/barrier, not the machine itself), CP025 (jewel case —
**case only, empty: no jewel and no invented Koh-i-Noor case design**),
CP030 (packing crates replace exhibits). Hyde Park 1851 building only.

## What it is

A two-object set in one `Model` collection (object names prefixed
`Case_` / `Crate_`; that prefixing, rather than separate collections,
is the set structure chosen, so the pair exports as one `.glb` and can
still be split by name in any scene). Origin at the **base centre of
the case**; the crate stands beside it, its centre 1.70 m along +X,
with a 0.20 m gap from the case's end. Units: metres. Blender 4.2+
(built with 4.5.3). All geometry is world-space with identity object
scale (scale applied by construction).

**The case** is the standard 1851 table case (desk case) that
Dickinson's plate XXIV shows three times in the Cotton court: a
timber table frame on four turned legs, a deep apron/frieze under
the top, and a shallow **hipped glazed lid** — trapezoidal long
slopes with one centre mullion each, triangular glazed ends, hip
bars at the corners and a ridge bar — over a flat, empty display bed.

**The crate** is a plain mid-19th-century packing case: horizontal
deal boards with narrow gaps, vertical corner and mid battens
sitting 6 mm proud of the horizontal top/bottom battens, boarded
bottom, and a separate battened lid resting on top.

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- Dickinson's Comprehensive Pictures, vol. 2, plate XXIV (Cotton
  court), British Library copy, CC0 —
  `references/muse-drive/images/commons/Cotton,_carriages,_etc_-_Dickinson's_comprehensive_pictures_of_the_Great_Exhibition_(1854)_vol_2,_plate_XXIV_-_BL.jpg`.
  The controlling source for the case's form; the manifest describes
  it as showing "cases of crepe, muslin and cotton goods".
- Dickinson plate V (India No. 4), CC0 — a timber-framed glazed
  cabinet with a shallow pitched glazed top in the mid-background:
  corroboration that this case family, not the modern flat-top
  vitrine, is the period norm. (Most India exhibits sit on open
  draped plinths.)
- Dickinson plate XXI (Moving Machinery), public domain — the
  machinery court's long glazed counter case and open plinths:
  context for CP024, not dimensioned from.
- Dickinson plate X, CC0 — glass domes and a small glazed booth
  cabinet; checked, different devices, not modelled.
- Nash, The Foreign Nave (plate 2), public domain — checked; a
  crowd panorama, nothing legible at modelling scale.
- The round-1 manifest (8,860 catalogue rows) was searched for
  case/vitrine/crate/packing/jewel descriptions: **plate XXIV is
  the only case evidence in the collection, and there is no image
  of a packing crate anywhere in the repo references** (see the
  crate's status below).

## Dimensions — stated plainly: ALL SIZES ARE GUESSED

No dimensioned drawing, catalogue entry or measurement of an 1851
table case or packing case exists in the references. Every size
below is a **guess**, made by proportion against the people in
plate XXIV (standing figures taken as ≈1.70 m) for the case, and
by period-plausible handling size for the crate. The *forms* are
plate-evidenced; the *numbers* are not measurements and must not be
quoted as such.

| Part | Value | Basis / status |
|---|---|---|
| Case overall length | 1.90 m | **Guessed** — in plate XXIV the centre case spans roughly two onlookers side by side; the left case about the same |
| Case overall depth | 0.95 m | **Guessed** — ≈ half the length, as drawn |
| Case height to lid eave | 0.82 m | **Guessed** — the eave sits at a standing man's hip in the plate |
| Case height to ridge | 1.00 m | **Guessed** — the plates' lids are shallow; rise 0.18 m over the 0.475 m half-depth (≈21°) |
| Leg height (floor→apron) | 0.64 m | **Guessed** — follows from eave and apron guesses |
| Apron depth | 0.18 m | **Guessed** — the deep frieze band is a seen feature; its depth is proportioned from the crops |
| Lid pane division | 2 lights per long slope + 1 triangular light per end | **Seen (read from the crops)** — centre mullion and hip bars are visible; at plate resolution the exact count per slope is a reading, not a certainty |
| Glazing bars | 34 × 26 mm | **Guessed** — slim timber bars as drawn |
| Bed | flat, at 0.795 m, empty | **Seen** — exhibits lie flat on the bed in the plate; the model ships empty (CP025 rule) |
| Crate overall | 1.12 × 0.73 × 0.73 m incl. battens/lid | **Guessed, generic** — a two-man-lift packing case size; no evidence (below) |
| Crate boards | 22 mm thick, ≈132 mm wide, 6 mm shadow gaps | **Guessed, generic period practice** |
| Crate battens | 95 mm wide; horizontals 28 mm, verticals 34 mm thick | **Guessed, generic** — the 6 mm step between them is a modelling fix (see QC), not a period claim |

## The crate's evidence status (read this before using it)

No packing crate is pictured in any reference in this repo — not in
the Dickinson plates, not in the Nash plates, not anywhere in the
round-1 manifest's 8,860 rows. The crate is therefore **generic
period construction** (deal boards + battens + a battened lid, the
ordinary mid-19th-century packing case), included because CP019 and
CP030 cannot be staged without crates at all. Details that a crate
of the period *might* have had were **omitted for lack of evidence
rather than invented**: no rope handles, no iron corner straps, no
stencilled lettering or marks of any kind, and no stencil panel.
If a plate or photograph of an 1851 Exhibition packing case is
found, this crate should be rebuilt from it.

## What was NOT modelled / known inaccuracies

- **The grand exhibitor's cabinet** at the right of plate XXIV
  (fluted corner columns, pediment, gilt frieze) — a one-off
  showpiece; deliberately not the model (see refs/REFERENCES.md).
- **Contents.** The case ships empty. In the plate the beds carry
  fabric samples and books; modelling generic contents would
  invent exhibits, and CP025 expressly forbids an invented jewel
  or Koh-i-Noor case design.
- **The lid's opening gear** — hinges, stays, locks: not legible
  in the plates, not modelled. The lid is a fixed cover.
- **Leg turning** is a stylised lathe profile of the plate's
  overall form (foot, taper, swell, collar, square top block).
  The plates suggest reeding on the legs; fluting/reeding is not
  modelled.
- **Joinery and fixings** — no mortises, screws or nails anywhere;
  crate nailing is implied by the battens only.
- **Materials/colour are interpretive.** The plates are
  hand-coloured: the case reads as warm medium-brown stained
  timber, the crate as pale deal. The model uses flat colours in
  that relationship (case darker, crate paler) with no grain,
  wear or weathering. Renders are the house neutral-grey setup,
  so both read paler on screen than the values suggest.
- **Glass** is a single-alpha material (0.16) on flat panes; no
  thickness, no period glass unevenness, no reflections modelling
  beyond the material. Panes are single-sided quads inset 10 mm
  inside the lid frame.
- The crate lid is a separate resting piece (12 mm shadow gap),
  not fixed down — correct for a case being packed or unpacked,
  and it can be lifted off in a scene.

## QC (2026-10-26)

- The plate was read from enlargements of the actual file
  (`refs/crop_xxiv_cases_left.png`, `crop_xxiv_cases_centre.png`),
  not from the thumbnail: leg form, apron, hip bars, centre
  mullion and triangular end lights were all confirmed there.
- Render round 1 showed **black squares on the crate wherever a
  vertical batten crossed a horizontal one** — the two battens'
  outer faces were exactly coplanar, the same coincident-surface
  artefact family the stair prop hit. Fixed by making the
  vertical battens 6 mm proud (VBAT_T in the script). The same
  round showed the set blown out to near-white — it read as a
  modern white vitrine, the exact failure the build plan warns
  against — so light energies were cut and the timber values
  darkened, and the lid rise reduced (0.24 m → 0.18 m) to the
  shallower pitch the plates show. Round 2's front view was
  checked clean before the full set was rendered.
- All four final renders were viewed. `front.png`: the case's
  long elevation — legs, deep apron, hipped lid with its mullion —
  with the crate's boarded, battened front beside it, no black
  artefacts. `side.png` is the view from the crate end (the crate
  in front, the case's triangular glazed end above it) — from
  this side the case is partly occluded by the crate, which is
  the honest consequence of the set layout; the case alone is
  fully visible in `case-three-quarter.png`, where the lid's
  hip geometry, end triangle and bed all read. In
  `three-quarter.png` a dark line at the crate's lid gap is the
  shadow of the resting lid's 12 mm slit, not an artefact.
- Counts, verified two ways (build log and an independent parse
  of the exported `.glb` — they agree): **87 objects, 2,278
  triangles** for the whole set — far under the ~50,000 triangle
  prop budget. GLB extents: 1.93 m across the set's long axis
  (case 1.90 m + eaves overhang), 1.016 m high (the case ridge),
  matching the design figures.
- Build incident, recorded for honesty: the geometry/export
  stage finished and saved, but the first render batch's
  process died with its session after two of four renders; the
  remaining two views were rendered from the saved `.blend`
  with the identical setup (same cameras, lights, samples) by a
  small top-up script. All four shipped renders are of the same
  final build.
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground plane, lights, four cameras; not
  exported).

## Files

- `build_hp_crate_and_display_case.py` — re-runnable build script
  (bpy); all dimensions are named constants at the top, with the
  guessed status stated in the header. Set `HPCASE_NORENDER=1`
  to rebuild geometry/exports without rendering.
- `hp-crate-and-display-case.blend` — model + render setup.
  Origin at the case's base centre.
- `hp-crate-and-display-case.glb` — `Model` collection only,
  87 objects (`Case_*` and `Crate_*`).
- `renders/front.png`, `side.png`, `three-quarter.png` — the set
  (both objects), neutral grey backdrop, same lighting, 960 × 720,
  Cycles CPU 64 samples + denoise; plus
  `renders/case-three-quarter.png` — the case alone, same setup.
- `refs/` — the Dickinson plates XXIV, XXI, V, X and the Nash
  Foreign Nave copied from the repo, three enlargements of plate
  XXIV, and `REFERENCES.md` with repo paths and licences.
