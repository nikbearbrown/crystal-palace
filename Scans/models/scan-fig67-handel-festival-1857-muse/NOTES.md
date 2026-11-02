# scan-fig67-handel-festival-1857 — Muse version

**This is the Muse version** of this model (ships as `scan-fig67-handel-festival-1857-muse`).

## Source
- Figure 67, "The Great Handel Festival at the Crystal Palace", *Illustrated London News*,
  27 June 1857 (engraving after a photograph by Negretti and Zambra).
- Source image: `fig-67_handel-festival-sydenham-crystal-palace-1857.png` (catalogue scan IMG_6431).
- This is the **Sydenham** (re-erected) palace's central transept, 1857 — not the 1851
  Hyde Park building. One view only.

## Subject modelled
The festival performance as a composed vignette (~18 m wide):
- **Organ front** at the rear centre — an original build in the visual language of an 1850s
  exhibition organ: dark case, three towers of gilt pipes with flats between, scallop-shell
  motif over the centre tower, gallery below. (Built fresh for this image; not a copy of
  any other prop.)
- **Massed choir** on raked timber tiers flanking and below the organ (~180 instanced
  standing silhouettes).
- **Orchestra** on the front platform: two arcs of seated players with music desks, four
  standing soloists, and the **conductor** on a podium at the centre with raised arms and
  baton, as drawn.
- **Iron side galleries** (columns, deck, rail, lattice bracing) as simplified frame hints
  at both edges, two **draped swags** overhead, and potted trees at the sides — all as in
  the engraving.
- **Audience**: three seated foreground blocks separated by two aisles, plus standing
  figures at the rear (~230 instanced seated silhouettes).

## Scale
- **Estimated** from the figures (adults ~1.7 m). Organ front ~6.4 m wide × ~6.8 m tall;
  vignette footprint 20 × 15 m. The real 1857 festival forces numbered in the thousands;
  the model's crowd is a representative massing at the engraving's composition, not a count.

## Assumptions and interpretation
- All performers and audience are **instanced stylised silhouettes** (four low-poly
  prototypes: standing man/woman, seated man/woman) — no likenesses, no individual
  characterisation. Choir dress is generalised dark/white; the engraving's surplices are
  only broadly suggested.
- Instruments are **not** individually modelled (desks and seated poses imply the
  orchestra); a few string-player silhouettes could be added in a later pass.
- The galleries and swags are partial frame hints at the vignette's edges, following the
  engraving's cropping; the full transept structure is out of scope.
- Rear and side faces of the organ case are plain interpretation.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 42,800 triangles.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, elevated view from
  behind the audience, comparable to the engraving), re-runnable
  `build_scan_fig67.py`.

## Manual-review items
- Organ pipe layout is generic 1850s exhibition style; the actual 1857 Sydenham organ
  (Gray & Davison) could be researched if a hero organ is needed.
- Crowd density is impressionistic; increasing instance counts is trivial in the script.
