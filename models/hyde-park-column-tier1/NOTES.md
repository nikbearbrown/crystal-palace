# NOTES — Hyde Park tier-1 iron column + girder stub

Prop for the Crystal Palace film. Hyde Park 1851 building only — no
Sydenham evidence is used in this model.

## What it is

One ground-floor column of the 1851 Hyde Park palace, from the floor
to the top of its tier-1 girder, with a short truncated girder stub
showing how the girder meets the column. Origin at the base centre,
floor level (z = 0). Units: metres. Blender 4.2+.

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-008.jpg` — Downes
  Plate VIII, "Details of columns" (John Weale, Jan 1852). Fig. 3/4/5
  full columns, Fig. 12 girder connection (enlarged), Fig. 13 flange
  plan. This is the primary visual source; see `refs/` for crops.
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` —
  dimension controls D06, D10, D11 (see below).
- `references/downes-1852/crystal-palace-1851/MEASUREMENTS.md` —
  printed-page heights (jp2 p.0017) and wall-thickness range.
- `references/downes-1852/crystal-palace-1851/PLATE-INDEX.md` —
  plate identification (Plate VIII = Details of columns).
- Cross-check only (geometry NOT copied): the course model's column
  dimensions in `course-models/crystal-palace-1851-claude/` — used to
  confirm the 18 ft 11¾ in lower-column height, nothing else.

## Dimensions — measured/printed vs guessed

| Part | Value | Status |
|---|---|---|
| Floor to girder bottom | 19 ft 2 in (5.842 m) | Printed on Plate VIII, Fig. 3 (19' 2"); control D11 |
| Girder depth | 3 ft 0 in (0.914 m) | Printed on Plate VIII, Fig. 12 (3' 0"); control D10 |
| Floor to girder top | 22 ft 2 in (6.756 m) | D11 (19' 2" + 3' 0") |
| Column bore | 8 in (0.203 m) | Printed on Plate VIII, Fig. 13 plan (8") |
| Wall thickness | 1 in nominal | Printed range ⅜–1¼ in; 1 in chosen inside it → outer diameter 10 in (0.254 m). Marked nominal, not a printed figure |
| Floor collar height | 6 in (0.152 m) | Fig. 3 dimension at the ground-floor line |
| Capital bolts | 1¼ in (0.032 m) dia, 4 at diagonals | Fig. 13 plan |
| Base foot plan | 2 ft 0 in × 1 ft 6 in | Fig. 4 plan at h.h. — but this is the BELOW-floor foundation base (piece B), so it is NOT modelled above floor; recorded here so the omission is explicit |
| Intermediate collar rings | At ~2 m and ~4 m, 0.10 m tall | Seen on Plate VIII shafts; positions proportional, NOT dimensioned — inferred |
| Girder stub length | 1.5 m, cut | Truncation is a modelling choice, marked on the model; the real girder ran the full 24 ft bay |
| Girder web profile | Triangular, deep at column tapering out | Simplified from Fig. 12's triangular bracket profile; the plate's internal stiffeners are not modelled |
| Paint colour | Light warm grey/off-white painted iron | Interpretive: matches the light appearance of columns in 1851 interior photographs; the exact 1851 paint colour is NOT verified. Ironwork was painted, not bare metal |

## What was NOT modelled / known inaccuracies

- The flared foundation base (piece B) below floor level — excluded
  deliberately; the prop starts at the floor collar.
- The D pipe (7 in) through the base — below-floor detail, excluded.
- Shaft wall is modelled as a solid-looking tube; the real column was
  hollow cast iron (8 in bore). The bore is not visible from outside
  at film distance, so no inner surface is modelled.
- Capital flange is a regular octagon; the plate's flange (Fig. 13) is
  an octagonal-ish plate with four bolt-lug ears — approximated.
- Bolt heads/nuts are simplified cylinders, not hex nuts.
- The girder stub is a simplification: top/bottom flanges + triangular
  web, without the plate's internal stiffener detail or the second
  girder direction (the real joint carried girders both ways).
- No glass, gutters, or gallery elements — this is the column alone.

## Relationship to other models

This is an independent prop built from the plates. It is NOT copied
from `course-models/crystal-palace-1851-claude/` (Claude's west-half
building model) or from `blender-deliverables/` (whose scene resembles
Sydenham and must not stand in for 1851 — see REVIEW.md, "What to keep
separate"). Dimensions agree with those models where they overlap
because all three derive from the same Downes plates.

## QC (2026-10-26)

- First render run produced blank grey images: the build script's
  `look_at()` set `rotation_quaternion` on a camera still in XYZ
  euler mode, so the camera looked straight down at the backdrop.
  Fixed (`rotation_mode = 'QUATERNION'` first) and re-rendered
  from the saved `.blend`; all three re-renders were viewed and
  show the column, collar rings, capital flange/bolts and girder
  stub as described above.
- Girder stub in the renders: the triangular web tapers from full
  3 ft depth at the column to 0.30 m at the cut, while the top
  flange runs horizontal at full depth — so a gap opens between
  the sloping web top and the top flange toward the cut. That gap
  follows the plate's Fig. 12 layout (sloping Q under a horizontal
  top line) and is part of the stated simplification, not a
  rendering error. Internal stiffeners are not modelled.
- Counts from the exported `.glb`: 21 objects, 2,560 triangles,
  4,024 vertices — well under the ~50,000-triangle prop budget.
  Height 6.756 m (22 ft 2 in to girder top).

## Files

- `hyde-park-column-tier1.blend` — model collection `Model` plus a
  `RenderSetup` collection (backdrop, lights, cameras; not exported).
- `hyde-park-column-tier1.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` — neutral grey
  backdrop, same lighting, 1080×1440.
- `refs/` — key Plate VIII crops used (derived from the in-repo plate
  scan) and a full reference list.
