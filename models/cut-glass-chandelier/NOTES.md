# Cut-glass chandelier — NOTES

## What this is

The great cut-glass chandelier illustrated in *The Crystal Palace and its
contents* (London, 1851–52) — a Hyde Park 1851 exhibition showpiece, for
nave/court dressing in the film (storyboard **CP019, CP025**). A "tent"
chandelier, all glass: canopy and icicle fringe, a diamond-cut shaft
draped with bead chains, a ring of fluted finial vases on scroll arms,
a mid candle ring, then a trumpet-flared cone carrying a second candle
tier in two rows, scallop shells, rosette-bead swags, a lozenge fringe,
ball pendants, and a central petal-cup finial ending in a faceted ball.

Origin at the base centre — the bottom tip of the central finial ball,
the object's lowest point. Real-world metres, Z up, all transforms baked
into the geometry. **Total height 5.5 m (adopted — see below); maximum
diameter 4.05 m at the rim.**

## Sources used

- **The single governing reference**, copied into `refs/`:
  `references/muse-drive/images/commons/Crystal_Palace00.jpg` — engraving
  from *The Crystal Palace, and its contents* (collective work, London,
  1851–1852); manifest licence **Public domain**; 1276 × 1600 px. A full
  frontal elevation with every tier drawn, used as an elevation drawing.
- No other view of this chandelier exists in the collection. The manifest
  was searched: the only other "chandelier" rows are a Dickinson plate
  that names one in passing and a modern photograph of the V&A rotunda
  chandelier — neither is this object, and neither was used.
- Candidate #32 in `models/CANDIDATES.md` ("Osler-type" there is a
  stylistic comparison in the candidates list, **not** a documented
  attribution — this build claims no maker).

## Size — adopted, not documented

No dimension for this chandelier exists anywhere in the repo references:
the plate carries no scale, no caption dimension and no human figure.
The overall height of **5.5 m** is adopted as a grand-exhibition scale
for a nave showpiece of 96 lights (plausible range roughly 4.5–6.5 m).
Every proportion below is a measured fraction of the total height, so
the model rescales cleanly if a documented size ever surfaces:
multiply all dimensions by (true height / 5.5). **Do not quote 5.5 m as
the original's size.**

## Measured from the engraving

Silhouette scan of the plate (ink bbox x 63–1204, y 44–1548, centre
x 634) plus feature positions read from enlarged crops:

- Overall width/height **0.759**; rim radius 0.368 × H; canopy radius
  0.093 × H.
- Shaft: near-straight taper, r 0.069–0.0755 × H between z 0.541 and
  0.905 × H, with beaded ring ridges every ~0.036 × H (all z from the
  finial tip).
- Fluted mid band z 0.485–0.541 × H; cone a trumpet flare from
  r 0.078 × H at z 0.485 to r 0.345 × H at z 0.245, read at nine heights.
- Upper finial vases: fluted bodies z 0.620–0.715 × H on a ring of
  radius 0.195 × H; spear tips to z ≈ 0.80 × H; inverted pendant cups
  below the vases to z 0.552 × H.
- Mid candle ring: cups at z 0.497 × H, ring radius 0.235 × H, drops
  hanging below to z ≈ 0.435 × H.
- Lower spears: tips z 0.458 × H on a ring of radius 0.300 × H.
- Lower candle tier in **two rows**: inner cups z 0.285 × H, tips
  z ≈ 0.351 × H, at R 0.300 × H; outer cups z ≈ 0.21 × H at
  R 0.345 × H — the outer row stands on the rim band's top edge.
- Lozenge fringe bottom z ≈ 0.10 × H; ball pendants centred
  z ≈ 0.117 × H; finial petal cup r 0.070 × H; bottom ball
  Ø ≈ 0.052 × H.

## Guessed / inferred — read before use

- **Absolute size** (above) is the largest inference in the model.
- **Counts** are nearest regular-ring readings of the engraver's
  projections, not censuses: 12 finial vases (projections at
  |x|/R ≈ 0.38 / 0.71–0.79 / 1.0), 24 mid candles, 12 lower spears
  (projections 0.87 / 1.0 of R), 24 inner + 48 outer lower candles —
  **96 candles in total** — and 12 tent chains. The engraver's spacing
  is not perfectly regular; another regular count (e.g. 8 or 16 vases)
  can be argued from the same plate.
- **Everything behind the frontal plane** is inferred from the
  elevation's radial symmetry: the object is built as a solid of
  revolution with radial repeats, which the plate supports, but no
  side or rear detail is documented.
- **Scroll arms** are simplified tubes with a volute curl; the plate's
  arms are flat acanthus scrollwork.
- **Scallop shells** behind the outer candle row are plain cupped fans;
  their ribbing is not resolved in the plate at this scale.
- The **suspension stem and eye** above the canopy (object
  `Suspension_ADDED`) are a practical addition for scene use — the
  plate's frame ends at the canopy. Hide or delete the object if a
  pure plate state is wanted.
- **Diamond cutting** is a procedural bump texture (packed into the
  .blend; source PNG in `textures/`), not cut geometry. The GLB
  therefore carries smooth glass — the cutting lives in the .blend.
- Small repeated parts (beads, drops, cups, spears) use a
  partial-transmission glass (0.6) rather than full transmission, to
  keep studio renders tractable; the six body lathes use full
  transmission. Candles are unlit wax, as drawn.

## Build

- Procedural bpy, Blender 4.2: `scripts/build_cut_glass_chandelier.py`.
  Every repeated element (chain beads, drops, rosette beads, candles,
  spears, vases) is one low-poly unit merged as transformed copies.
- **25 objects; 47,356 triangles** evaluated (the count a scene pays;
  unique unit geometries total only a few hundred triangles).
- Renders: one fixed neutral-grey rig, `scripts/render_rig.py`
  (front = the +X view, so a spear and shell face the camera as in the
  plate); `scripts/make_compare.py` builds `renders/compare.png`.
- Built over four rounds against the plate: round 1 established the
  silhouette; round 2 lowered the rim band so the outer candle row
  stands proud, centred a tent chain on the front, deepened the vase
  fluting and gave the small glass partial transmission; round 3
  shrank the added suspension eye and lifted the cone with a low fill;
  round 4 took the diamond bump off the vases (the plate's vases are
  fluted, not diamond-cut), softened it on the cone so the flare reads
  as glass rather than mesh, and tightened the chain-bead pitch to the
  plate's spacing.

## Known inaccuracies

- In the empty grey studio the glass reads paler and more opalescent
  than cut glass would against a dark hall; the materials are honest
  glass, the void behind them is empty.
- Chain beads follow one smooth size ramp (pitch 0.027 → 0.038 × H);
  the plate's beads vary more irregularly.
- The canopy's frieze ornament (fan/shell motifs in the plate) is
  rendered as plain stepped rings.
