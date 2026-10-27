# NOTES — Brunel water tower, Sydenham (MASSING STUDY)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 4, item 18).
Scenes: CP042 (towers in a date-supported state), CP062 (the towers
standing beyond the missing roof, morning after the 1936 fire),
CP064 (skyline loses its markers). **Sydenham only.** This is ONE
tower of Brunel's pair; duplicate/mirror it for the pair.

## This is a massing study — read this first

This prop asserts **silhouette, proportions and overall height
only**. It is a scale/form reference for the shell builder and for
skyline and backdrop shots. It is **not** a reconstruction: Brunel's
drawings of the towers are **not in the collection** (round-2 review
searched; the ICE holds material under no open licence), and no
dimensioned elevation exists in the repo. A hero tower model must
wait for those drawings. Do not use this prop for close-ups, and do
not read any construction detail into it.

## The date gate

The towers were begun in August 1854 and **operational only from
2 June 1856** (Historic England, via round-2 review §S51). They
must **never appear in CP035's June 1854 opening state**. The
Delamotte photographs used here are captioned "1854" by Commons,
but a finished, working tower in them means they date from
completion — c.1856 (round-2 dating caveat, carried in the round-2
manifest). Valid states for this prop: c.1856 onward. Both towers
survived the 1936 fire (CP062); the south tower was dismantled in
sections in autumn 1940 and the north tower blown up on
16 April 1941 (GAPS-FOUND contradictions §9) — CP064's before/after
is by explicit time cuts; this prop itself asserts no demolition
narrative.

## What it is

A cylindrical open iron frame — 12 columns ringed with horizontal
bands and light diagonal bracing — carrying a projecting gallery
ring, an open arcaded lantern stage, and a steep conical cap with a
small finial. Inside the upper shaft sits a plain tank cylinder
(object `Tank_INFERRED`, separable — see below). A low concrete
ring plinth at the base. Origin at the base centre, ground at the
tower's own foot z = 0. Units: metres. Blender 4.5.3.

The form is read from the photographs (see `refs/REFERENCES.md`):
the Rijksmuseum garden-front view (S51-03, 1878–90) shows the whole
tower clear of the nave roof at full resolution — the shaft is a
panelled lattice cylinder (not a solid drum, and not a tank on
legs: the tank is inside the frame), the gallery ring projects
visibly, the lantern is an open stage of short posts with arched
openings, and the cap is a steep ribbed cone overhanging the
lantern, topped by a small knob finial. The two Delamotte views
(S51-01, S51-02, c.1856) confirm the same form on both towers.

## Dimensions — sourced vs measured vs inferred

### The height conflict (why four numbers exist, and which was used)

No period source in the collection prints a tower height: the
1854 dimension chapters (Routledge pp.25–26; Phillips p.28) cover
the palace only, and the 1856 guide's table has no tower entry.
The figures on record (all collected in round-2 review §S51 and
contradictions §9) are:

| Figure | Source |
|---|---|
| 280 ft (85.34 m) | ILN, 1941 |
| 282 ft (85.95 m) | secondary record, via round-2 review |
| 284 ft (86.56 m) | secondary record, via round-2 review |
| **86 m** | **Historic England** |

**Adopted: 86.0 m overall** — Historic England's figure, which is
also 282.2 ft, i.e. it lands on the 282 ft record and inside the
280–284 ft spread (the whole spread is ±0.7 %). **Datum:** none of
the collected sources states its datum. This model measures from
the ground at the tower's own base to the **tip of the finial**.
Whether the quoted figures include the finial, or were taken from
the palace terrace level rather than the tower's own foot on the
sloping site, is not recorded in the collection — that ambiguity
is itself about the size of the 280–284 ft disagreement, so treat
the height as **86 m ± 1 m**. The two towers stood on a ridge with
different local ground; when placing the pair, set each tower's
z = 0 at its own base, never on one shared datum.

### Proportions (photo-measured)

Vertical fractions were measured by visual grounding on
enlargements of S51-03 and S51-01. The two photographs **agree**:
cap + finial ≈ 18 % of total height, lantern + gallery ≈ 15.5 %,
shaft ≈ 67 %. Widths come from height/diameter ratios measured on
the same views (H/D between 5.0 on the near, high-resolution
S51-03 and 6.0 on the small, hazy S51-01; adopted 5.4). **No width
is dimensioned in any source** — treat all diameters as
photo-derived estimates, ±10–15 %.

| Part | Value | Status |
|---|---|---|
| Overall height | 86.0 m | **Adopted** (conflict above); ±1 m |
| Shaft (frame top) | 57.7 m (67 %) | **Photo-measured fraction** (both views agree) |
| Gallery ring top | 62.4 m (band 4.7 m) | **Photo-measured fraction** |
| Lantern top / cap eaves | 71.0 m (stage 8.6 m) | **Photo-measured fraction** |
| Cap + finial | 15.0 m (~18 %) | **Photo-measured fraction** |
| Shaft diameter | 16.0 m | **Photo-derived estimate** (H/D 5.0–6.0, adopted 5.4); ±10–15 % |
| Gallery diameter | 18.6 m | **Photo-estimated** (projects ~1.3 m per side) |
| Lantern diameter | 17.6 m | **Photo-estimated** |
| Cap eave diameter | 21.6 m | **Photo-measured ratio** — eaves/shaft = 1.39 on S51-03; adopted 1.35 |
| Columns | 12 | **Sourced** — "12 cast-iron columns on a concrete ring" (Historic England) |
| Shaft ring levels | 8 storeys | **Photo-counted, approximate** — the views show ~8 horizontal bands |
| Plinth | Ø 17.6 m × 1.2 m | **Kind sourced, size estimated** — the concrete ring is Historic England's; its drawn size is not (the base is tree-hidden in every view) |
| Tank | Ø 14.6 m, z 40–56 m | **INFERRED.** No source dimensions the tank or fixes its position. It is placed inside the upper shaft, where the photographs' shaft reads densest; object `Tank_INFERRED` can be hidden without changing the silhouette claim. |
| Column / brace sizes | Ø 0.45 m / 0.14 m bars | **Modelling choices** — massing language, not detail |

## What was NOT modelled / known inaccuracies

- **No detail, deliberately.** No pipework, stairs, ladders,
  gallery railing, lantern arch shapes (the stage is posts and
  rings — the arched openings read at distance), cap ribs (the cap
  is a smooth massing cone with a curved profile), or base
  openings. The tower's foot is hidden by trees in every
  photograph in the collection, so nothing at the base is evidenced
  beyond the concrete ring itself.
- **The bracing pattern is a suggestion.** The photographs show a
  fine lattice grid; this model uses one diagonal per bay per
  storey, alternating direction — enough to read as lattice at
  backdrop distance, not a record of the real bracing.
- **The second tower and the spacing are shell work.** The pair
  stood beyond the palace's two ends on the main axis (as the
  Delamotte views show them, one at each end); this prop is a
  single tower at its own origin.
- **Materials are flat procedural colours** (painted-iron grey,
  darker tank iron, concrete). The towers' actual paint scheme is
  not verified in the collection.
- **Condition is neutral, as-built c.1856.** No weathering, no
  wartime state, no damage.

## Relationship to the version already on main

`models/sy-water-tower-massing/` on main (parallel builder stream) is a
deliberately formless placeholder: two plain 70 m boxes, "every
size guessed, no form or height asserted", because that builder
found no tower elevation in the repo sources. This package is the
evidence-based study for the same slot, built after the round-2
collection landed the Delamotte and Rijksmuseum tower photographs
on branch `muse-round2`: real silhouette and proportions measured
on those photographs, and the height taken from Historic England's
figure with its conflict stated above. The two are not in conflict
about method — the placeholder's gap is exactly what round 2
filled.

## QC (2026-10-26)

- Evidence read directly: both proportion measurements taken by
  visual grounding on ×4/×5 enlargements of the actual
  photographs (crops kept in `refs/`); the two independent
  measurements agree on the vertical fractions to ~1 %.
- First render pass cropped the tower in the front and side
  views: Blender's ortho_scale is the frame *width*, so at
  960 × 720 the visible height was 0.75 × 102 m = 76.5 m < 86 m.
  Fixed (ortho 128, camera centre z = 43) and re-rendered; all
  three shipped renders show the whole tower.
- Counts: **10 objects, 8,472 triangles**, verified three ways —
  build log, re-opened `.blend`, parsed `.glb` (all agree) — well
  under the ~50,000 triangle prop budget. World bounding box
  21.6 × 21.6 m plan (the cap eaves), z 0.00–86.00 m — the top
  lands exactly on the adopted height. Unit scale throughout.
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground plane, sun, cameras; not exported).

## Files

- `build_sy_water_tower_massing.py` — re-runnable build script (bpy);
  all dimensions are named constants at the top, grouped into
  adopted / photo-measured / inferred.
- `sy-water-tower-massing.blend` — model + render setup.
- `sy-water-tower-massing.glb` — `Model` collection only (nodes named
  Plinth, ShaftColumns, ShaftRings, ShaftBracing, Tank_INFERRED,
  Gallery, GalleryLip, LanternPosts, LanternRings, Cap).
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 960 × 720. Front and side
  are orthographic elevations (the tower is rotationally near-
  symmetric, so they are near-identical by design); three-quarter
  is a perspective view from the south-west at height.
- `refs/` — the three photographs, the two measurement crops, and
  `REFERENCES.md`.
