# scan-fig72-brompton-boilers — Muse version

**Muse version** (ships as `scan-fig72-brompton-boilers-muse`).

## Subject — and a brief/image discrepancy
Catalog fig. 72 (scan IMG_6427): the *Illustrated London News* coloured view of 24 May 1862 captioned "The 'Brompton Boilers'. South Kensington Exhibition, 1862."

**The image governs.** Although the nickname and the batch brief suggested corrugated-iron sheds, the view itself shows the **1862 International Exhibition building** in South Kensington: a very long brick frontage of round-arched bays with projecting entrance pavilions, a large glazed dome rising behind the right-hand pavilion and a smaller glazed dome at the left, plain red flags along the roofline, and horse-drawn carriages, riders and pedestrians on the open ground in front. That is what is modelled here — an excerpt of the frontage (~68 m as framed), not the whole building and not corrugated sheds.

## Scale
Arcade wall 11 m high; large dome ~8.2 m radius on a ~14 m springing; excerpt frontage ~68 m. **Scale estimated** from the figures/carriages in the print; the real building was several times longer than the excerpt.

## Assumptions / interpretation
- The print is a single three-quarter view: the model is a frontage excerpt with a shallow return; depth, rear elevations and roof construction are interpretation.
- Domes are stylised: ribbed glass caps (glass clamped at the springing) on brick rotunda drums set back behind the front pavilions, as the print shows them rising behind the front block.
- Flags are plain red rectangles — the print's flags carry no readable device at this size and none was invented.
- Traffic is stylised: simplified horse/carriage/figure masses in the batch's house style; no lettering anywhere.

## Technical
- Triangles: **29,652**. Blender 4.5.3, metres, origin at base centre, scale applied.
- Files: `scan-fig72-brompton-boilers.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, three-quarter view comparable to the print), re-runnable `build_scan_fig72_brompton_boilers.py`.

## QC
Preview checked against the print over three iterations: framing widened so both domes and the arcade read as in the print (big dome screen-right, small dome screen-left — handedness verified); the large dome's glass was clamped to a cap and its drum set back so it rises behind the front pavilion instead of bulging in front of it; brick warmed toward the hand-coloured print; plaza extended to the frame edges.

## Manual-review items
- Horses are distant-traffic silhouettes; not suitable for close-ups.
- Dome rib pattern is a regular stylisation of the print's diagonal glazing lattice.
- The discrepancy between the "Brompton Boilers" nickname/brief and the building actually shown should be kept with the asset so nobody re-labels this as the corrugated sheds.
