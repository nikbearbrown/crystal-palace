# hp-osler-crystal-fountain

The **Osler crystal fountain** — F. & C. Osler's "Large fountain, in
cut crystal glass", the centrepiece of the Hyde Park transept at the
intersection of the Main Avenue, as exhibited in **1851**. Scenes
**CP021, CP022, CP023**. Wave 2, item 7 of
`models/SCENE-BUILD-PLAN.md`, built to the research spike report
(`build/osler-spike-report.md`, verdict BUILDABLE-FAITHFUL), §5. See
`refs/REFERENCES.md` for the sources. **Hyde Park 1851 only** — the
post-1854 Sydenham re-erection (in a goldfish pool) is a different
installation and is not blended in; the fountain was destroyed in
the 1936 fire.

**Datum:** z = 0 is the basin waterline, i.e. the surrounding floor
level; the basin shell extends 0.20 m below it (pool depth), and the
spout top is at z = 8.23 m. Origin at the centre of the basin. All
geometry is rotationally symmetric about the axis, as in the plate.
All objects are world-space geometry with identity transforms (unit
scale throughout).

## Dimensions

**Published (primary source)**

| Part | Value | Source |
|---|---|---|
| Overall height, waterline → top of glass spout | **27 ft = 8.23 m** | *Official Descriptive and Illustrated Catalogue* (1851), Class XXIV, exhibit No. 20, F. & C. Osler — the exhibitor's own entry; corroborated by Christie's lot 6387468, Johnston Collection (8.25 m), *History of London*, Birmingham Post |
| Basin diameter | **24 ft = 7.32 m** | Birmingham Post / Free Library article; matches the building's 24 ft module. Adopted over the plate's ≈26–27 ft photo ratio — see the conflict note in the spike report §4. **Tolerance ±10%.** |
| Weight (context only) | 4 tons / 4,000 kg | Johnston Collection; Birmingham article |

**Measured from the Ferrier plate** (spike report §4: fractions of
the 8.23 m height, ±5% per level, ±10% per diameter; plate =
`refs/osler-ferrier-plate.jpg`, RCIN 2800080)

| Element | Height above waterline | Diameter |
|---|---|---|
| Plinth drum top (stem cage begins) | 1.06 m | drum Ø 2.30 m |
| Tier-1 dome underside / cage junction | 3.02 m | — |
| Tier-1 dome rim | 3.25 m | dome Ø 2.84 m |
| Tier-1 top bowl rim | 4.19 m | bowl Ø 2.25 m |
| Tier-2 dome rim | 5.73 m | dome Ø 1.25 m |
| Tier-2 top bowl rim | 6.23 m | bowl Ø 0.99 m |
| Top of glass spout | 8.23 m | — |

Tier 2's dome underside (5.63 m) and crown (5.90 m) are scaled from
tier 1's proportions (the plate fixes its two rims, not its
underside). The basin rim height (+0.10/+0.13 m), pool floor
(−0.10 m) and the two centre steps (top step at the waterline) are
read from the plate's shallow floor pool and the Talbot transept
view; no dimensioned source gives them.

## What was NOT modelled / omissions

- **The water plume is excluded** — it is water, not object (spike
  §5.9). The basin carries a still water surface at the waterline.
  If a "playing" state is ever wanted, the plume should be a
  separate transparent add-on, clearly labelled.
- **Internal iron armature and the silvered water tube** — the glass
  shafts were built up around iron bars "so completely embedded in
  the glass as to be invisible", and water rose through a silvered
  tube hidden inside the central column (Birmingham / Free Library
  article). Documented construction, invisible in reality, **not
  modelled**.
- **The drum's inscription is not lettered.** The plate shows a
  horizontal inscription band around the drum, only partly legible
  ("…LONDON"). The model carries the band as a blank frosted-glass
  ring; the text must not be completed by invention (spike §6.5).
- The Official Catalogue's own illustration plate ("represented in
  the accompanying Plate") was not separately viewed by the spike;
  the measured image is the *Reports by the Juries* plate of the
  same fountain (spike §3, honest gaps).

## Inferred — the spike report §6, verbatim

> ## 6. What remains inferred (must appear in the model's NOTES.md)
>
> 1. Every per-tier diameter and level is a **photo-derived fraction** of
>    the catalogue height (±5–10%), not a dimensioned drawing.
> 2. Basin Ø: published 24 ft adopted over the photo's ≈26–27 ft reading;
>    ±10% flagged (§4).
> 3. Basin material and construction: undocumented in sources found.
> 4. Stem-cage rod count (8–12) and the branching cluster's arm geometry:
>    approximate readings of an 1851 salt print.
> 5. Cut-glass pattern: generic period fluting/faceting, not a traced
>    Osler pattern; the drum's inscription is only partly legible and
>    must not be completed by invention.
> 6. Internal structure (iron core, silvered tube): documented in text,
>    invisible, not modelled.

Build choices made inside those inferences: stem cage = **12 rods**
(the top of the 8–12 range, matching the plate's dense read);
branching cluster = 6 curving arms with cups at 4.30–5.09 m; basin
modelled as a dark stone/metal-rimmed pool; centre steps pale stone;
the fluted flare at the cage base is junction ornament read from
the plate.

## Materials / rendering

- **Cut crystal glass** (drum, bowls, domes, stems, rods, cups):
  Principled BSDF, **full transmission (weight 1.0), IOR 1.52**,
  roughness 0.055 (fine stems/nozzle 0.035; the blank inscription
  band is frosted at 0.28). No transmission compromise was needed —
  the glass is true transmission glass, not a transparent-mix fake.
  The *cutting* is geometry: radial flutes are modulated into the
  lathe profiles and the fluted parts are flat-shaded, so the facets
  catch the light as cut glass does. Generic period fluting, not a
  traced Osler pattern (§6.5).
- **Basin water:** a still, dark, low-roughness reflective surface
  at the waterline — a pool at rest, not a simulation.
- **Basin and steps:** plain stone (dark rim/floor, pale steps),
  inferred material (§6.3).
- Studio renders: neutral grey world and backdrop as on the other
  props, sun + area lights, plus four emissive softbox planes that
  are hidden from the camera but visible to glossy/transmission
  rays — they supply the bright streaks without which transmission
  glass reads as grey plastic against a grey backdrop. Glass
  objects do not cast shadows (Cycles would otherwise give them
  solid black shadows; the basin carries the contact shadow).
- Cycles CPU, **192 samples** with OpenImageDenoise, transmission
  bounces 12 — the delivered renders are the script's output at
  `OSLER_SAMPLES=192` (script default 256).

## Triangle counts

Recounted from the saved files three ways — build log, re-opened
.blend, and parsing the exported .glb — all agree:

- `Model`: **67 objects, 30,424 triangles**; z range −0.200 to
  **8.230 m** (spout top exactly at the catalogue height); basin
  Ø 7.32 m. Under the 50k ceiling of `MUSE-PROMPT.md` §2.
- The .glb parses back at 67 meshes / 30,424 triangles and carries
  `KHR_materials_transmission` on all three glass materials.
- `.blend` re-opens with collections `Model` and `RenderSetup`.

## QC

- All three renders viewed against the Ferrier plate. The
  silhouette — shallow floor pool, ornate drum, rod cage, fluted
  dome-and-bowl pair, candelabrum cluster, smaller tier pair, tall
  lacy upper stem — matches the plate and the Talbot view from the
  opposite end of the transept.
- The glass was checked specifically for the failure mode the plan
  warns against ("a solid crystal blob"): at test renders it reads
  as transparent, refracting cut glass with facet sparkle, not
  white plastic — the fluted tier-1 bowl and the rod cage are the
  clearest reads.
- Two defects found in test renders and fixed in the script: the
  first three-quarter camera sat too high and close (the fountain
  read squat and the finite backdrop's edge crossed the frame) —
  camera lowered and pulled back, backdrop enlarged; and the
  front/side orthographic cameras cropped the fountain top and
  bottom, because Blender's `ortho_scale` is the *horizontal*
  extent at this aspect — scale corrected 9.4 → 11.6.
- The plinth drum reads fainter in the flat orthographic views than
  in the plate (in the plate it is backlit and dense with cutting);
  its flutes were deepened once (0.010 → 0.018 m) and it reads
  correctly in the three-quarter view. Recorded here rather than
  chased further: the geometry is the measured geometry.
