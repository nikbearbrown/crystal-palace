# scan-fig44-agricultural-workers-sculpture — Muse version

**This is the Muse version** of this model (ships as `scan-fig44-agricultural-workers-sculpture-muse`).

## Source
- Figure 44, "Agricultural workers at the Great Exhibition", *Illustrated London News*, 19 July 1851.
- Source image: `fig-44_agricultural-workers-great-exhibition-1851.png` (catalogue scan IMG_6447).
- One frontal view only; the unseen backs/sides of all elements are interpretation.

## Subject modelled
A composed vignette (~8 m wide) of the engraving's frontal group: rural visitors standing
among the sculpture exhibits. Principal elements:
- The large standing **dog statue** on a tall rectangular plinth (right of centre), with cap
  slab, base moulding and a blank label plate.
- A second plinth at the left rear carrying only the lower legs and a drapery edge of a
  standing human statue — exactly as much as the engraving shows; the figure is not completed.
- An ornate lamp/candelabrum silhouette at the centre rear and one vague statue mass at the
  far right rear, both kept as background dressing as in the print.
- Seventeen stylised visitors (men in smocks, caps, bowlers and top hats; women in bonnets
  and shawls; three children), two walking sticks and a basket/bundle at the group's feet.

## Important source discrepancy
The catalogue description says the group stands "among sculpture exhibits, including a
**lion**". The image itself unambiguously shows a large long-eared **dog** (a Landseer-type
mastiff/retriever statue). The image was followed, not the caption text; flagged here and
for the manifest as a manual-review item.

## Scale
- **Estimated.** No dimension is given in the source. Figure heights 1.6–1.78 m set the scale;
  the dog statue is modelled ~2.4 m long overall on a 1.5 m plinth, matching its monumental
  size relative to the crowd in the engraving. Vignette footprint 9.0 × 5.6 m.

## Assumptions and interpretation
- All people are **stylised simplified figures in period-dress silhouettes** — interpretive,
  with no facial features and no likenesses. Poses are generalised standing poses; the
  engraving's individual gestures are only broadly suggested.
- The dog statue is an **abstracted monumental mass** (body, legs, head, muzzle, drop ears,
  tail) with blank, uncarved surfaces: fine sculptural detail is deferred to a sculptor pass.
- The plinth label plate is left blank; no lettering is invented.
- Depth arrangement (crowd in one shallow rank, plinths behind) follows the engraving's
  compressed staging; real gallery spacing is not claimed.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 8,064 triangles, ~180 objects.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, frontal view
  comparable to the engraving), re-runnable `build_scan_fig44.py`.

## QC
- Preview compared against the reference: dog faces left as drawn; crowd reads as a single
  frontal rank; plinths and label plate visible behind the group. First render's framing
  (cropped edges, dog facing the wrong way, lamp reading as a solid mushroom) was fixed and
  re-rendered.
- Fix round (2026-11-01): male figures rebuilt — the original stacked-box torsos on stick
  legs were replaced with tapered smock/coat body masses reaching near the ground, a shoulder
  frustum into the head, and short boot hints, matching the women's figure language and the
  batch standard (cf. fig67). Count, positions, scene and other elements unchanged;
  .blend/.glb/preview regenerated (triangles 7,264 → 8,064) and the new preview verified.

## Manual-review items
- Catalogue "lion" vs image "dog" discrepancy (above).
- Sculptor pass needed for the dog and the partial statue if hero quality is wanted.
- The partial statue's identity and the lamp's exact form are not determinable from this view.
