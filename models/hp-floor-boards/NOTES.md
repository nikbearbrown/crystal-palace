# NOTES — Hyde Park open-boarded ground-floor section

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 1, item 2).
Scenes: CP020 (preparing for feet and crowds), CP028 (daily work /
cleaning). Hyde Park 1851 building only — no Sydenham evidence is
used in this model.

## What it is

A short cut section of the 1851 ground floor exactly as Paxton
described it: separate floor boards with open ½-inch gaps between
them — the famous self-cleaning floor, dust and wash-water falling
through the gaps into the void below — carried on timber joists,
which rest on large timber sleepers. It is a section, not a slab:
the current course-model floor slab cannot stand in for these
boards (storyboard CP020 flag). Origin at the base centre (the
underside of the sleepers, at plan centre). Units: metres.
Blender 4.2+ (built with 4.5.3).

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- `references/muse-round2/images/S25-01-official-catalogue-1851-introduction-p62-flooring.jpg`
  (branch `muse-round2`) — Official Catalogue (1851), Introduction
  p. 62, quoting Paxton's Society of Arts paper of 13 Nov 1850.
  Primary source for all member sizes below.
- `references/muse-round2/images/S25-02-official-catalogue-1851-introduction-p63-flooring-conclusion.jpg`
  (branch `muse-round2`) — p. 63: the washing behaviour and the
  772,784 sq ft ground-floor area (context only).
- `references/muse-round2/images/S25-berlyn-1851-floor-description.jpg`
  (branch `muse-round2`) — Berlyn & Fowler (1851), p. 37:
  corroborates the ½-inch interval and distinguishes the gallery
  floor (iron tongues) from this floor.
- `references/downes-1852/crystal-palace-1851/` (branch `main`) —
  CONTROL-DIMENSIONS.md and MEASUREMENTS.md checked: Downes
  dimensions floor *levels*, not the floor members; Plate VI gives
  only a loose underfloor cross-check (below).

## Dimensions — printed vs inferred

| Part | Value | Status |
|---|---|---|
| Board thickness | 1½ in (0.038 m) | **Printed**, Catalogue p. 62 |
| Gap between boards | ½ in (0.013 m) | **Printed**, Catalogue p. 62; corroborated Berlyn p. 37 |
| Joist section | 7 in deep × 2½ in wide (0.178 × 0.064 m) | **Printed**, Catalogue p. 62 |
| Sleeper section | 13 in × 3¼ in (0.330 × 0.083 m) | **Printed**, Catalogue p. 62 — but see the orientation note below |
| Sleeper spacing | 8 ft (2.438 m), centre to centre | **Printed**, "at intervals of 8 feet apart", p. 62 |
| Floor top above sleeper base | 21½ in (0.546 m) | Sum of the printed members (13 + 7 + 1½) |
| Board width | 9 in (0.229 m) | **Inferred** — no board width is printed in any source used; see below |
| Joist spacing | 2 ft (0.610 m) centres | **Inferred** — no joist spacing is printed; see below |
| Section size | 16 ft × 12 ft (4.877 × 3.658 m) | Modelling choice: two full 8 ft sleeper intervals long; wide enough for the joists to span the 8 ft between sleepers with bearing length to spare at each side |
| Board count in section | 15 | Follows from the inferred 9 in width + printed ½ in gap across the 12 ft width (142 in of boarding, 1 in margin each side) |
| Ground-floor area | 772,784 sq ft | **Printed**, Catalogue p. 63 — scale context only, not modelled |

**Sleeper orientation (an interpretation, stated openly).** The
Catalogue sentence gives both members as "depth by width" for the
joists ("7 inches by 2½ inches" — 7 in is unambiguously the vertical
depth of a joist). The model reads the sleeper figures the same way:
13 in vertical depth × 3¼ in width, i.e. deep ground beams, which is
also how the sentence introduces them — "large timbers or sleepers".
The alternative reading (13 in wide × 3¼ in deep, laid flat like a
railway sleeper) cannot be excluded from the text alone. Downes
Plate VI offers only a weak cross-check: its measured ground line
sits ≈1⅓ ft below the floor line, between the two readings' totals
(21½ in vs 11¾ in), and that plate is not dimensioned for the floor
build-up, so it settles nothing. If the flat reading is ever
preferred, it is a one-line change: swap `SLEEP_D` and `SLEEP_W`
in the build script.

**Board width.** The Catalogue passage gives thickness and gap but
no width, and neither does Berlyn. 9 in is chosen because (a) it is
the width the secondary descriptions of this floor carry (the
round-1 review notes modern summaries giving 22 cm / 9 in widths
while the primary text states only thickness and gap — those
summaries are secondary, and are flagged as such), and (b) 9 in was
an ordinary deal-board width of the period. The width affects only
the board count and pitch across the section; every structural
member (thickness, gap, joists, sleepers) is primary-printed.

**Joist spacing.** Not printed anywhere in the sources used. 2 ft
centres is chosen because 1½ in boards need support at roughly that
pitch under crowd load, and because 2 ft divides both the printed
8 ft sleeper interval and the section evenly, in keeping with the
building's relentless 8 ft / 24 ft modular discipline. The seven
joists sit at −6, −4, −2, 0, +2, +4, +6 ft, one full pitch in from
the cut ends, so the section reads as cut from a continuous floor.

**Layout logic (structural reading of the text).** "Joists … which
rest upon … sleepers … at intervals of 8 feet apart": the joists
cross the sleepers at right angles and span the 8 ft intervals;
the boards lie across the joists, i.e. parallel to the sleepers.
The model follows that reading: sleepers run the 16 ft length,
spaced 8 ft apart across the 12 ft width; joists run across the
width on top of them; boards run the length on top of the joists.

## What was NOT modelled / known inaccuracies

- **The gallery floor** — a different construction (boards with
  iron tongues between them, Berlyn p. 37; the round-1 "Testing the
  Gallery Floor" item). Not modelled, not used as evidence.
- No ground or terrain under the sleepers: the prop's base is the
  sleeper underside, and the underfloor void (Paxton's "vacuity
  below") is open, as the cleaning system requires. A neutral grey
  backdrop plane sits in the render setup only.
- Board end joints / staggered butt joints: real boards were long
  lengths jointed over joists, but no source used here shows the
  jointing pattern, so boards run the full 16 ft unjointed. Marked
  as a simplification, not a claim.
- No nails, fixings, or the sweeping machine and hand-engine of
  Paxton's description (p. 62) — those are separate props if wanted;
  CP028's cleaning beat would need the machine designed from the
  text alone, as no image of it is in the references used here.
- Timber is plain coloured material with a slight per-board tint
  variation (a rendering aid so individual boards read on camera);
  no grain texture, no weathering. Colour is interpretive — new
  deal boards were pale, and the renders honestly show pale timber.
- Members are exact rectangular sections; no chamfers, wear, or
  the trellised *pathways* of Paxton's horticultural experiments
  (p. 62) — those were his glasshouse precursor, not this floor.

## Relationship to other models

Built independently from the Catalogue text. It shares no geometry
with `course-models/crystal-palace-1851-claude/` (whose solid floor
slab this prop exists to correct for CP020/CP028) or with
`hyde-park-column-tier1` — that prop starts at floor level, and its
floor datum (top of these boards, z = 0.546 m here) is where the
two would meet in a set.

## QC (2026-10-26)

- Evidence pages read directly from the scans (not from summaries):
  the p. 62 figures were transcribed from the printed page image —
  boards 1½ in thick, ½ in apart; joists 7 × 2½ in; sleepers
  13 × 3¼ in at 8 ft intervals — and p. 63's washing sentence and
  772,784 sq ft area confirmed on the page.
- All three renders were viewed. `front.png` is a true section
  across the width: board ends with the gaps between them on top,
  the joist profile band beneath, and the two sleeper sections at
  their 8 ft spacing below that. `side.png` shows the sleeper's
  length, the seven joist ends at their 2 ft rhythm and the open
  void between them. `three-quarter.png` shows the board deck from
  above at an angle: the gap lines run the full length of the deck
  and are clearly visible, with joist ends and one sleeper edge
  visible along the near side.
- Counts from the exported `.glb`, cross-checked by re-opening the
  saved `.blend`: **24 objects, 288 triangles** — 2 sleepers,
  7 joists, 15 boards, all simple boxes — far under the ~50,000
  triangle prop budget. GLB bounding box independently parsed:
  4.877 × 3.658 m plan, 0.546 m high, matching the design figures.
  (The build script's own in-session count print over-reads by one
  object; the saved files were recounted directly and agree with
  each other, so the file counts are the ones reported.)
- Build incident, recorded for honesty: the first (backgrounded)
  build run saved all outputs according to its Blender log, but the
  `.blend`, `.glb` and `three-quarter.png` were missing from the
  staging folder afterwards, while `front.png` and `side.png`
  survived. Cause not established. The build was re-run with the
  surviving renders skipped (`HPFB_SKIP` env option in the script),
  and every output was then re-verified on disk, as above.
- The `.blend` re-opens cleanly (it was re-opened for the recount
  and for the recovery render) and contains two collections:
  `Model` (exported) and `RenderSetup` (backdrop, lights, cameras;
  not exported).

## Files

- `build_hp_floor_boards.py` — re-runnable build script (bpy);
  all dimensions are named constants at the top, with the inferred
  values separated from the printed ones.
- `hp-floor-boards.blend` — model collection `Model` plus a
  `RenderSetup` collection (backdrop, lights, cameras; not
  exported). Origin at base centre; real-world metres; object
  transforms are identity (scale applied by construction).
- `hp-floor-boards.glb` — `Model` collection only, 24 objects.
- `renders/front.png`, `side.png`, `three-quarter.png` — neutral
  grey backdrop, same lighting, 960 × 720. Front is the
  cross-section view; side the longitudinal elevation.
- `refs/` — the three evidence page images copied from the repo,
  with `REFERENCES.md` giving repo paths, branches, content and
  licences.
