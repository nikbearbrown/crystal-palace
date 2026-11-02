# scan-fig47-dinner-time — Muse version

**This is the Muse version** of this model (ships as `scan-fig47-dinner-time-muse`).

## Source
- Figure 47, "Dinner-Time at the Crystal Palace", *Punch*, 5 July 1851.
- Source image: `fig-47_dinner-time-crystal-palace-punch-1851.png` (catalogue scan IMG_6444).
- The original print has a stepped silhouette (the statue rises above the crowd block);
  the vignette follows that composition. One view only.

## Subject modelled
A composed vignette (~7 m wide):
- Central **standing Shakespeare statue** (~2.3 m) in Elizabethan dress on a tall, dark,
  stepped plinth (~1.5 m), one leg crossed in front of the other as drawn, one hand resting
  toward a book on its support post, laurel spray hinted at the base.
- The plinth's inscription tablet is modelled as a **blank tablet**. The motto in the print
  reads "ONE TOUCH OF NATURE MAKES THE WHOLE WORLD KIN" — recorded here, not carved into
  the model.
- Working families picnicking around the plinth base: a mother nursing a baby at centre,
  a woman reclining against the plinth step with a girl beside her, a standing man in a top
  hat pouring from a bottle, seated women and children with wicker baskets, a cloth bundle,
  and a small boy seen from behind.
- Background crowd silhouettes (heads and shoulders rising behind the plinth on both sides).

## Treatment of the source's caricature
The *Punch* original exaggerates its figures satirically. Per the batch rule the composition
is followed **without caricature exaggeration**: all people are dignified, stylised simplified
figures in period dress, with no facial features and no likenesses.

## Scale
- **Estimated.** Set from the seated/standing figures (adults ~1.7 m). The statue is taken as
  roughly 1.35× life size, consistent with its dominance over the crowd in the print.
  Vignette footprint 7.6 × 4.6 m.

## Assumptions and interpretation
- The statue is an **abstracted monumental figure** (blank surfaces, no carved detail, no
  facial features); a sculptor pass would be needed for hero quality.
- The nursing mother is represented by a seated figure holding a wrapped bundle; the pose is
  suggested, not anatomically detailed.
- Baskets are plain wicker forms; no food items are individually modelled beyond the bottle
  and bundles.
- Rear faces of the plinth and statue, and everything outside the print's stepped frame,
  are interpretation.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 5,816 triangles.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, portrait-format
  frontal view comparable to the print), re-runnable `build_scan_fig47.py`.

## Manual-review items
- Whether to add the motto as real geometry/text texture on the tablet in a later pass.
- Sculptor pass for the Shakespeare figure if it is ever used closer than mid-shot.
