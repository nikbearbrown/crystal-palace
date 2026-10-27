# NOTES — Sydenham 1936 ruin fragment

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 4, item 17).
Scenes: CP001 (1936 prologue — silhouette dressing), CP062–CP064
(morning after, clearance, towers beyond the missing roof), CP065
as aftermath reference. **Sydenham, morning after the fire of
30 November 1936 only.** Labelled ruin: this is a damaged-state
prop — it must never be reused as an intact component, and its
members must not be "repaired" back into the standing building.

## What it is

One composed fragment of the wreckage — roughly one 24 ft bay's
worth of fallen structure — on an ash-covered ground slab
(8.6 × 6.6 m, a presentation base, not archaeology). Every
structural member is a **documented member of the real palace**,
heat-damaged by the failure modes the photographs show:

- **Standing column stump** — a tier-1 cast-iron column broken at
  ≈ 2.6 m: base plate, 6 in floor collar, shaft kinked 11° above
  1.7 m, dark bore at the break. Two fallen chunks of the same
  column lie beside it.
- **Fallen column** — a full tier-1 column length (5.8 m) lying
  diagonally, bent into a smooth shallow heat-sag curve, its floor
  collar still on the shaft, bore dark at the broken end.
- **Fallen plate girder** — one full 24 ft girder length across
  the back, ends propped on debris, middle sunk into the ash,
  twisted ≈ 13° progressively along its length (smooth per-vertex
  bend, not segmented).
- **Collapsed ridge-and-furrow roof section** — one furrow
  (2.44 m) × 3.6 m of the roof: both timber Paxton gutters (the
  far one broken, a middle length missing), the ridge piece
  slumped to ≈ 55% of its true rise, and 28 sash bars drooping
  between gutter and ridge. Four glass panes survive in the bars;
  the rest of the glass is gone, as in the photographs.
- **Charred floor boards** — seven boards (one snapped), mostly
  charcoal-black, one scorched brown.
- **Drooping rods** — four thin tie/louvre rods bent over in the
  wilted curves the 1867 engraving shows.
- **Glass scatter** — 24 small shards on the slab, concentrated
  under the roof section, plus a small stack of three unbroken
  panes slid off the panel.

Origin at the base centre of the slab, ground z = 0. Units:
metres. Blender 4.5.3. 132 objects, **3,872 triangles** (build log
and parsed `.glb` agree).

## Sources used (see `refs/REFERENCES.md` for the full table)

- **1936 state:** the morning-after aerial photograph (round 1,
  gallery 0587/0588, PD) — total collapse into a low, interlaced
  mat; nothing of the frame left standing. The prop's height,
  density and lie follow it.
- **Failure behaviour:** the ILN engraving of 12 Jan 1867 (round
  2, S67-01, PD) — the same structure after the 1866 fire, and the
  collection's only readable ground-level record of how this
  ironwork fails: smooth heat arcs, drooping thin members,
  stripped standing stubs, flat interlaced lengths. The 1936
  photographs in the repo are aerial/distant, so ground-level
  failure *detail* is read from 1867 and applied to the 1936
  state; that transfer is an interpretation, stated here plainly.
- **Members:** Downes 1852 plates via
  `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md`
  and the NOTES of `hyde-park-column-tier1` and
  `hp-roof-furrow-bay`.

## Dimensions — documented vs stylised

| Part | Value | Status |
|---|---|---|
| Bay length (girder, panel module) | 24 ft (7.315 m) | **Documented** — D06 |
| Column outer dia / bore | 10 in (0.254 m) / 8 in (0.203 m) | **Documented** — Plate VIII, D13; as built in the column prop |
| Column tier-1 height (fallen length) | 18 ft 11¾ in (5.77 m) | **Documented** — D14 |
| Floor collar | 6 in high | **Documented** — Plate VIII Fig. 3 |
| Base plate | 2 ft × 1 ft | **Documented** — D16 |
| Girder depth | 3 ft (0.914 m) | **Documented** — D10 |
| Girder flange width / web & flange thickness | 0.30 m / 25 mm / 45 mm | **Interpreted** — Plate VIII Fig. 12 proportions; not dimensioned in the controls |
| Furrow pitch (gutter–ridge–gutter) | 8 ft (2.438 m); slopes 2½:1 | **Documented** — D09, Plate XII |
| Sash bars | 1 in × 1⅜ in at 10½ in centres; strong bars 2½ in | **Documented** — Plate XII Fig. 10 + text |
| Ridge piece | 3 in wide | **Documented** — Plate XII Fig. 10 |
| Paxton gutter | 5 in base, 6 in deep | **Documented** — Plate XII Fig. 10 |
| Pane size (surviving panes/shards) | 49 in long × 10 in wide class | **Documented** — text p. 15 via the furrow prop |
| Floor boards | 9 in wide × 1½ in thick | **Documented** — 1851 Catalogue pp. 62–63 |
| **All damage** — sag depths, kink angle (11°), twist (13°), break heights, droop (55 mm per bar), slump (55% of rise), scatter positions | as built | **Stylised** — procedural readings of the photographs' behaviour, not measurements of any specific member |
| Slab size, ash mounds | 8.6 × 6.6 m | **Presentation choice** — the real wreckage field was the whole 1,848 ft footprint |

## Materials

All procedural, no photo textures: heat-blackened iron (dark,
semi-metallic), ash-dusted iron (mid grey — the girder and some
column pieces, matching the pale ash-covered lengths in the
aerial), charcoal, scorched timber, and a transmissive pale
blue-green glass for shards/panes. Colours are matched by eye to
the (monochrome) photographs' tonal range; the real morning-after
palette — black, ash grey, rust beginning — is a reading, not a
record.

## What was NOT modelled / known inaccuracies

- **No fire, smoke or glow** — this is the morning after.
- **No people, no clearance machinery, no towers** — CP062's
  towers are `sy-tower-study` / the shell's job; the plan's rule
  that CP062 must not open on a fully cleared plateau is served
  by dressing this fragment (and siblings) across the ridge.
- The girder's internal stiffeners and the column's capital
  connecting piece are omitted — the girder is web + flanges
  only, as in the column prop's simplification.
- The transept's great arched ribs (74 ft class) are not in this
  fragment: the aerial shows them down and indistinguishable
  in the mat at this scale; a hero rib belongs to the SY36 shell,
  not this dressing prop.
- Ash mounds are smooth presentation drifts; at the slab corners
  they read slightly soft in close-up.
- One build-script note: the girder's sag uses
  `max(0, sin(πt))**1.5` with t clamped — an earlier draft
  produced complex numbers from a hair-negative sine at the end
  vertices and failed; the clamp is deliberate.

## Relationship to other models

A damaged-state sibling of the Wave 0–1 structural props: its
column, girder and roof members share their dimensions with
`hyde-park-column-tier1` and `hp-roof-furrow-bay` because all
derive from the same Downes plates. It is a fuller, composed
fragment than the minimal twisted-member variant of this item
also recorded in the build plan — one bay of interlaced wreckage
rather than a single broken member — and it is staged locally for
the film's dressing kit either way.

## QC (2026-10-26)

- Evidence read directly: both 1936 photographs, an enlarged
  crop of the aerial's wreckage field, and the 1867 ILN ruins
  engraving (see `refs/`).
- Three build/render rounds, every render viewed:
  (1) the girder stood in the foreground and walled off the
  scene — moved to the back, palette lightened, rods darkened
  and thickened, a rod that read as a spike on the stump moved
  clear; (2) the girder, first built as nine rigid segments,
  read as a staircase — rebuilt as subdivided plates bent
  per-vertex, twist halved; (3) the smooth-bend build failed on
  a Python complex-power edge case (see above) — clamped and
  rebuilt clean.
- Counts verified two ways: build log **3,872 triangles**;
  parsed `.glb` **3,872 triangles**, 132 meshes, all objects
  unit scale. World bbox 8.84 × 6.6 m plan (girder overhang
  included), 2.66 m to the stump's broken top; the girder's
  sunk middle passes below slab-top into the ash, as intended.
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground, lights, cameras; not exported).

## Files

- `build_sy36_ruin_fragment_bay.py` — re-runnable build script
  (bpy); documented dimensions are named constants at the top.
  Set `SKIP_RENDER=1` to rebuild without the render pass.
- `sy36-ruin-fragment-bay.blend` — model + render setup.
- `sy36-ruin-fragment-bay.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 960 × 720, Cycles CPU.
- `refs/` — the photographs/engraving used, and `REFERENCES.md`.
