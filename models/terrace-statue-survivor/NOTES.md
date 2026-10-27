# NOTES — Terrace statue, surviving headless (present-day survivor)

Prop for the Crystal Palace film. Candidate #11 in `models/CANDIDATES.md`.
Scenes: the present-day park states (CP072 / CP076 family — the surviving
walk, alongside `park-now-terrace-edge/` and `park-now-plateau-marker/`).

**This is the statue as it survives today in Crystal Palace Park — NOT
the 1854 original.** The head and arms are lost in reality; nothing has
been restored, completed, or "improved". Do not dress it as an intact
Sydenham-era figure.

## What it is

One of the draped statues that stood on the pilasters of the Sydenham
Upper Terrace (Historic England list entry 1064352 describes the terrace
pilasters as "topped by vases or statues"), photographed in its present
weathered, headless state: a tall, columnar, fully draped standing
figure on its terrace pedestal — heavy vertical drapery folds from
shoulder to hem, a diagonal himation swag across the back, a hanging
drape flap on the back-right, a deep dark cavity in the figure's left
flank at chest/waist height, and one bare foot protruding at the front
of the hem. The pedestal is the stepped stone block the figure stands
on (top slab, recessed neck, main block, corbelled foot bands), sitting
at the parapet line; the terrace wall/parapet itself is the separate
`sy-terrace-step-and-arcade/` / `park-now-terrace-edge/` props.

Origin at base centre (bottom of pedestal), z = 0 at the parapet cap
line level. Units: metres. Blender 4.2. **22 objects, 14,984 triangles.**

## Sources used

- `refs/headless-statue-geograph-2436241.jpg` — the ONLY reference:
  "A headless statue 'surveys' Crystal Palace Park", Geograph image
  2436241, via Wikimedia Commons (`references/muse-drive/images/commons/
  A_headless_statue_'surveys'_Crystal_Palace_Park_-_geograph.org.uk_-
  2436241.jpg`; manifest row: 1280 × 960, **CC BY-SA 2.0**,
  https://creativecommons.org/licenses/by-sa/2.0). One modern colour
  photograph, **rear three-quarter view only**.
- Terrace module dimensions cross-checked against the shipped
  `models/sy-terrace-step-and-arcade/NOTES.md` (parapet 1.05 m,
  photo-proportioned from the same terrace photographs).

## Dimensions and their provenance

| Element | Value | Provenance |
|---|---|---|
| Figure height (plinth top to drape dome) | 3.00 m | **Adopted estimate** — see scale chain below, ±20% |
| Overall height (pedestal foot to dome) | 4.08 m | Figure + pedestal below |
| Pedestal height | 1.02 m | Photo-proportioned (see below) |
| Pedestal footprint (corbel foot) | 2.02 × 1.48 m | Photo-proportioned, ±20% |
| Figure hem width / depth | ~1.15 × 0.87 m | Photo-proportioned from the same ratios |
| Cavity (left flank) | ~0.35 wide × ~0.55 tall at z ≈ 1.9–2.5 m above plinth | **Seen** in the photograph; depth inferred |

**Scale chain (no dimensioned source exists for this statue):** in the
photograph the figure measures ≈ 440 px from plinth top to dome and the
pedestal block ≈ 135 px from plinth top to the parapet cap line — a
ratio of ≈ 3.3 : 1. Anchoring the pedestal to the terrace module's
parapet/pier scale (parapet 1.05 m, from the shipped terrace prop,
itself photo-proportioned) gives a pedestal of ≈ 0.9–1.0 m and hence a
figure of ≈ 3.0 m. Figure height 3.00 m was adopted on that basis;
**treat all absolute dimensions as ±20%**. All internal proportions
(height of the cavity, the fold roll, the shoulder mass, the hem
splay) were measured as fractions of figure height from the photograph
and are firmer than the absolute scale.

## Measured / seen vs guessed

**Seen in the photograph (rear three-quarter):**
- Columnar draped silhouette; floor-length drapery with deep vertical
  fluting, strongest in the bottom quarter; hem splaying and pooling
  slightly onto the plinth top.
- Domed drape mass where the head/neck would be — the figure ends at
  the shoulders in bunched, vertically streaked drapery. No head, no
  arm geometry anywhere: none survives.
- Diagonal swag of drapery across the back, descending from the
  figure's right shoulder toward the left hip, with a hanging pointed
  flap on the back-right.
- A large dark wedge-shaped cavity in the left flank at chest/waist
  height — modelled as a real dent in the loft with dark interior
  shells. (Whether it is a hollow in a cast figure or a lost drapery
  mass cannot be told from one photograph; the model records its
  outline and darkness, not a cause.)
- One bare foot protruding forward at the front of the hem.
- The pedestal's stepped profile: slab, recessed neck, plain block,
  corbelled bands at the foot.
- Weathered grey stone, green-grey staining — material colours sampled
  from the photograph's tones.

**Guessed / inferred (no evidence in the collection):**
- **The entire front of the figure.** Only a shallow diagonal groove,
  a slight chest swell and the protruding foot are modelled there —
  drapery-logic inference, deliberately kept quiet. No face, arms or
  attributes were invented (there is nothing to invent them from: the
  originals are lost).
- The right side, the back's exact fold pattern beyond the visible
  swag, the cavity's depth and interior, the second foot (a toe-tip
  hint only), and the pedestal's rear faces.
- The absolute scale (chain above) and the pedestal's width/depth
  ratio, foreshortened in the single view.

## Known inaccuracies

- Single-view reconstruction: everything the camera did not see is a
  plausible draped-figure reading, not a record. The compare render
  (`renders/compare-rear-three-quarter.png`) is against the one
  documented view; front/side renders are of inferred geometry.
- Folds are procedural fluting (13 + 27 harmonic ripple) — they give
  the photograph's heavy vertical rhythm, not its individual folds.
- The cavity is two dark shells in a sculpted dent: its ragged broken
  rim in reality is smoother here.
- The GLB carries flat base colours only; the procedural weathering
  (noise blotching/bump) lives in the .blend's materials and the
  Cycles renders.
- The figure's identity (which statue of the terrace series this is)
  is not asserted — the photograph's title does not name it and
  neither does this prop.
