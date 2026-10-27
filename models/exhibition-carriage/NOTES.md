# Exhibition carriage — candidate #33

A horse-drawn enclosed carriage of period type (brougham-like), built for
Hyde Park 1851 carriage-display dressing (film scene CP025). **No horse.**

## Sources

- `refs/plate-xxiv.jpg` — Dickinson's *Comprehensive Pictures of the Great
  Exhibition*, vol. 2, plate XXIV ("Cotton, carriages, etc."), British
  Library copy via Wikimedia Commons, **CC0** (manifest lists the file as
  CC0; the plate itself is an 1854 publication, public domain). Repo path:
  `references/muse-drive/images/commons/Cotton,_carriages,_etc_-_Dickinson's_comprehensive_pictures_of_the_Great_Exhibition_(1854)_vol_2,_plate_XXIV_-_BL.jpg`
- `refs/plate-xxiv-carriage-crop.jpg` and `refs/plate-xxiv-carriage-crop-4x.jpg`
  — crops of the plate made for this build (see below).

## What the reference actually shows — read this first

Plate XXIV is a wide interior of the cotton court. **Only one carriage is
legible anywhere in it**, and only just: in the deep background, seen
through the curtained opening at the left of the view, a dark enclosed
carriage body with a rectangular window, a lamp mounted high at its front,
and a hint of a large spoked wheel. It is small (the crop region is
200 × 170 px of a 1449 × 998 plate), partly occluded by visitors, and drawn
at a distance. **This model is therefore a period TYPE read loosely from
that glimpse — it is not, and cannot be, a portrait of a specific exhibited
carriage.** Every dimension is inferred (see below). If the film needs a
hero carriage, this is not it; it is background dressing, which is what the
candidate itself proposed ("a generic period carriage could be built from
it only loosely").

## Measured vs guessed

**Seen in the plate (qualitative only):** enclosed (not open) carriage;
dark japanned body; a glazed window in the body side; a lamp carried high
at the front of the body; large spoked wheels; the carriage stands in an
exhibition court among display cases.

**Everything else is inferred** from standard mid-19th-century British
carriage practice:

- Form chosen: a brougham-type enclosed body — panelled lower body, glazed
  upperworks with door window and rear quarter window, front glass,
  driver's box seat ahead of the cabin with footboard and dashboard, a pair
  of shafts, square lamps on the front body corners, full-elliptic springs
  front and rear, perch undercarriage with a fifth-wheel forecarriage.
- No part of that list except "enclosed, glazed, lamp, spoked wheels" is
  visible in the plate. The landau and victoria alternatives were set
  aside because the glimpsed body reads as a fixed-roof enclosed cabin,
  not a folding-head open carriage.

## Dimensions (ALL inferred — no dimensioned source exists)

Scale chain: period broughams ran a rear wheel of about 4 ft 6 in–4 ft 8 in
and a front wheel of about 3 ft; the plate's carriage, where it overlaps
the standing visitors at the opening, is consistent with a full-size
carriage and nothing smaller. Adopted:

| Part | Value |
|---|---|
| Rear wheel diameter | 1.40 m (14 spokes) |
| Front wheel diameter | 0.92 m (12 spokes) |
| Wheelbase | 2.26 m |
| Track | 1.58 m rear / 1.46 m front |
| Body | 2.38 m long (at the waist) × 1.44 m wide; floor at 1.12 m; roof crest 2.35 m |
| Overall (measured from the built model) | 4.41 m long (shaft tips to rear boot) × 1.92 m wide (across the door steps) × 2.35 m high |
| Overall uncertainty | ±15–20% — these are type dimensions, not measurements |

## Build

- Procedural `bpy` (`scripts/build_exhibition_carriage.py`), Blender 4.2,
  real-world metres, origin at base centre, scale applied.
- **12,288 triangles**, 214 mesh objects. Under the ~50k budget.
- Wheels are built spoke-by-spoke (dished pairs) with iron tyre and wooden
  felloe; springs are leaf arcs of chord segments; shafts are tapered
  two-segment poles.
- Renders: front / side / three-quarter on the standard neutral-grey rig
  (same world, ground, lights, cameras as sibling builds). **Engine note:**
  EEVEE hangs on this VM, so the renders were made with Cycles CPU on the
  identical rig — the same disclosed fallback the glass-topped display
  counter used.
- `renders/compare.png` sets the side render beside the enlarged plate
  crop. The comparison is honest about the gap: the reference carriage is
  a few dozen legible pixels; agreement can only be checked at the level
  of "enclosed dark body, window, lamp, big spoked wheels".

## Known inaccuracies

- Every dimension and every detail beyond the short "seen" list above is
  period inference, not observation.
- Colours (near-black green japan, dark painted wheels, blue-grey seat
  fabric) are generic period choices; the plate's carriage is in shadow
  and its colours cannot be read.
- The body is built from bevelled boxes: its lower panels show horizontal
  banding where a real body's panels curve continuously, and the roof is a
  cushion slab rather than a compound-curved panel.
- Door outline, handles, steps and interior seat are type details; none is
  visible in the reference.
- The far side of the carriage is a mirror of the near side by
  construction; no asymmetrical fitting is modelled.
- The shafts are modelled for a single horse (a pair, as the plate
  context would suggest for a carriage of this class in motion — though
  on exhibition it stood static, without horses at all).
