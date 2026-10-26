# NOTES — Present-day plateau / outline aid

Prop for the Crystal Palace film. Present-day Sydenham park
only — an overlay aid, not a building, not a reconstruction.

## What it is

A flat rectangular outline (4 strips) with 6 marker posts,
sized to the Sydenham footprint, for the CP072/CP076 overlay
shots: the missing footprint appears briefly over the empty
site and fades while the camera is still. Origin at rectangle
centre, ground level. Units: metres. Blender 4.2+.

## Dimensions — sourced vs guessed

| Part | Value | Status |
|---|---|---|
| Outline length | 1,608 ft (490.1 m) | Sourced: 1856 guide before/after table, p.35 (via REVIEW.md) |
| Outline width | 384 ft (117.0 m) | Sourced: same table, Sydenham greatest width |
| Strip width / thickness | 3.0 m / 0.1 m | Modelling choice — overlay legibility, not a surveyed line (a 0.5 m strip is sub-pixel from 600 m up in QC, so the strips were widened) |
| Marker posts | 1.2 m square, 2.5 m tall, corners + long-side midpoints | Modelling choice — same legibility reason |
| Overlay colour | Strong amber | Interpretive, chosen to read against grass/plateau (a pale ochre washed out to near-invisible at full-footprint scale in QC) |

## What this prop must NOT be used for

- Registration is future work: a georeferenced Sydenham plan
  + modern survey is required before this outline can be
  placed accurately. Until then it is labelled approximate.
- Never put a Hyde Park grid on Sydenham terrain — this
  outline is Sydenham length/width only.
- Never present the outline as the building, or as evidence
  of where any particular wall stood.

## Files

- `park-now-plateau-marker.blend` — model collection `Model`
  plus a `RenderSetup` collection (not exported).
- `park-now-plateau-marker.glb` — `Model` collection only.
- `renders/front.png` (top-down view — an eye-level front
  would show only strip edges), `side.png` (eye-level
  profile), `three-quarter.png` — neutral grey backdrop,
  same lighting, 1080×1440.
