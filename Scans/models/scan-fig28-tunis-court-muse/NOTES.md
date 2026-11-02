# NOTES — scan-fig28-tunis-court (Muse version)

## Subject

A composed section (~7 m wide, one court bay) of the **Tunis Court** at the
Great Exhibition of 1851, modelled from the black-and-white engraving
catalogued as fig. 28 ("The 'Tunis Court'"). It is a composed section, not a
reconstruction of the whole court: three arched display alcoves, overhead
carpets and a draped carpet swag, a glazed display cabinet, two standing
visitors, a seated figure, and the foreground animal hide and lutes.

## Scale — ESTIMATED

- **Basis:** the two standing men in dark coats at centre-right of the
  engraving, taken as ~1.70 m tall. All other dimensions are scaled from
  them by proportion against the image: alcove arches spring at ~2.05 m with
  crowns at ~2.9 m, counters ~0.85 m high, cabinet ~2.55 m high, swag
  attachment ~4.05 m. Overall footprint 7.0 m × 4.8 m.
- This scale is **estimated**, not measured from any printed dimension; no
  dimension for this court is given in the catalogue entry.

## Colour caveat — INTERPRETIVE

The source is a **monochrome engraving**. Every colour in the model is an
interpretation: a plausible muted period palette for North African textiles
and goods (deep reds, indigo, ochre, cream), dark timber, brass/copper and
terracotta vessels, pale straw hats. No colour should be cited as evidence.

## Assumptions and interpretations

- **Alcove row straightened:** in the engraving the alcoves recede in
  perspective along the left; the model lays three bays out in a straight
  row on a back wall so the bay can be reused as a set piece. Bay width
  (~1.55 m openings), depth (~0.6 m) and pier width are proportions read
  from the image, not measured facts.
- **Alcove contents distributed:** hats/plates/vessels are placed in
  alcove 1, folded textiles in alcove 2, hanging fabrics in alcove 3,
  following the left-to-right order in the engraving; exact counts and
  positions within each alcove are approximate.
- **Vessels** are simplified lathe profiles (ewer with spout, bottles,
  conical-lidded jar, bowls). The engraving's hatching does not resolve
  individual profiles, handles or decoration.
- **Textile patterns** are reduced to solid muted colours with contrasting
  border bands; the woven/geometric patterns visible in the engraving are
  not reproduced motif-for-motif.
- **Carpet swag** is a catenary-like draped grid with border bands along
  its edges; its patterned field in the engraving is not reproduced.
- **Animal hide** (foreground right) is an interpretation of the signature
  dark shape: a hide draped over a low timber support, tail trailing
  on the floor toward the centre, with a folded edge at the head end
  (reworked in fix round 1 — see Build / QC).
  Species, exact outline and the support are not identifiable in the source.
- **Figures** are stylised, simplified period-dress forms (dark coats,
  caps), with **no likenesses** and no caricature. Two standing visitors
  (~1.70 m, the scale reference) and one seated figure among the textiles
  in alcove 3.
- **Glazed cabinet:** thin timber frame with transparent panes and simple
  boxed goods on shelves; the engraving does not resolve the individual
  objects inside.
- **Unseen sides** (backs of the alcove wall, cabinet and counters, the
  underside of the swag) are reasonable plain interpretations, not evidence.
- **Not modelled:** the Crystal Palace roof/iron structure (background in
  the engraving only), any text or signage (none is legible / none added).

## Build / QC

- Script: `build_scan_fig28_tunis_court.py` (Blender 4.5.3, bpy, re-runnable:
  `blender -b --python build_scan_fig28_tunis_court.py`).
- Metres throughout; origin at base centre (floor centre, z = 0); object
  scales applied.
- Triangle count: **10,508 triangles** / 227 objects (build log
  `TRIANGLES: 10508` after fix round 1; originally 8,288 / 210), well
  under the 50k budget.
- The whole model was mirrored in X at the end of the build (transforms
  baked, geometry mirrored, faces flipped) so that, from the front, the
  left-to-right order matches the engraving: hats alcove left, cabinet and
  hide right, swag upper right. The preview is rendered from the
  cabinet/hide end, looking along the alcove row — the engraving's
  viewpoint.
- `preview.png` is a Cycles CPU render, neutral grey background, 960 × 640,
  from a front-right three-quarter viewpoint comparable to the engraving
  (looking along the alcove row with the draped swag overhead). The preview
  was visually checked against the reference before delivery.

### Fix round 1 (2026-11-01, parent audit)

All fixes made in `build_scan_fig28_tunis_court.py`; `.blend`, `.glb` and
`preview.png` regenerated from the same camera, composition, dimensions
unchanged. New totals: **10,508 triangles / 227 objects**.

- **Palette:** the original build passed sRGB-looking values straight into
  Blender's linear Base Color socket, lifting every colour about a gamma
  step (deep red rendered pastel pink, indigo sky blue, hide brown beige).
  Colours are now specified in sRGB and converted to linear in `mat()`,
  and the values themselves were deepened/desaturated: carpets, fascia
  panels and the overhead swag in deep reds (swag border bands now a dark
  maroon, darker than the field), textiles in indigo/ochre/muted cream
  (no sky blue, no pink), counter fronts darker striped, floor and hide
  darker and warmer. Colours remain interpretive — the source is a B/W
  engraving (see Colour caveat above).
- **Figures:** the two standing visitors were bare capsule mannequins.
  They now have period silhouettes at the same low-poly level: trouser
  legs and shoes below the knee, a long coat with a skirt flaring from
  waist to knee, a tapered torso widening to shoulders, and a simple
  faceless head with a brim-and-crown hat form (replacing the flat cap
  puck). Stylised, no likenesses, as before.
- **Animal hide:** drape profile rebuilt with smoothstep interpolation
  between control heights on a denser grid (26 × 14, was 18 × 10), so the
  kinks that read as folded card are gone; material darkened to a mid/dark
  leather brown with a darker edge tone. The raised "fan flap" cone at
  the head end was removed and replaced with a low rolled fold lying
  across the hide's width at the crest, reading as a folded hide edge.
- **Alcove 1 density:** added a second staggered row of three smaller
  straw hats on the back wall and three more small counter vessels
  (copper bottle, pottery jar, brass cup) in the gaps between the
  existing pieces.
- The regenerated `preview.png` was viewed and checked after the fix:
  the court now reads as rich, muted bazaar textiles; the figures read
  as long-coated, hatted men; the hide reads as a smooth dark drape
  with a folded edge. No pastel toy-block colours remain.
