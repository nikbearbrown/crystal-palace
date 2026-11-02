# scan-fig59-exhibition-and-foreigners-broadside — Muse version

**This is the Muse version** of this model (ships as `scan-fig59-exhibition-and-foreigners-broadside-muse`).

## Source
- Figure 59, "The Exhibition and Foreigners" — illustrated song broadside, printed and
  published by E. Hodges, Seven Dials, London, 1851.
- Source image: `fig-59_the-exhibition-and-foreigners-broadsheet.png` (catalogue scan IMG_6436).
- The image is the sheet itself (a photographed page with irregular, torn edges retained on a
  rectangular canvas). One view only.

## Subject modelled
The broadside as a physical object, pasted up on a weathered wooden hoarding:
- The sheet, 1.55 m wide × 2.00 m tall, with a gentle paste billow and the bottom edge
  curling away from the board, as a photographed/pasted sheet behaves.
- Its printed layout reproduced as **blank tonal blocks only — no lettering anywhere**:
  - the bold headline as a solid dark ink band with rules above the vignettes;
  - the three caricature head vignettes under the headline, as abstract ink-silhouette
    head-and-hat masses (turban with crest, top hat, feathered bonnet) inside ruled panels;
  - the publisher's imprint as a plain strip;
  - the two verse columns as rows of fine print-line strips with a centre rule;
  - the circular library stamp at lower right as a plain blue ring (blank centre).
- Context props at the foot of the hoarding: the bill-sticker's paste bucket and brush.
- The hoarding: two posts with feet, two rails, nine vertical weathered boards.

## Treatment of the source
The original is a xenophobic song sheet whose verses and caricature heads mock the foreign
visitors of 1851. The model preserves the **sheet as an artefact** — its format, layout and
physical presence — while the caricature heads are reduced to neutral silhouette masses and
all text is omitted. Nothing of the wording is reproduced or paraphrased in the model.

## Scale
- **Estimated.** Real song broadsides of this publisher were roughly 0.5 × 0.7 m; per the
  batch brief the sheet is modelled at display scale, 1.55 × 2.00 m, so the artefact reads
  at film distance. Hoarding ~2.35 m tall. If a true-to-life sheet is ever needed, scale the
  Sheet and its layout blocks by ~0.35.

## Assumptions and interpretation
- The scan shows the sheet flat against a page; mounting it on a hoarding with a paste
  bucket and brush is presentation context, not evidence from the image.
- Head vignettes are abstract silhouettes: no facial features, no attempt at the original
  caricatures' features.
- The torn/irregular edges of the photographed sheet are suggested only by softened top
  corners and the bottom curl; the sheet outline is kept rectangular.
- The back of the sheet and hoarding are plain interpretation.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 5,496 triangles, 113 objects.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, near-frontal view
  comparable to the source's straight-on presentation), re-runnable `build_scan_fig59_broadside.py`.
- QC: first render had the library stamp edge-on (ring not rotated into the sheet plane)
  and the verse lines too proud, reading as louvres; both fixed and re-rendered.

## Manual-review items
- If the broadside is ever shown in close-up, the layout blocks would need replacing with
  a scanned-texture approach — as built it is a mid-distance artefact.
- The headline is a solid ink band; the real sheet's headline is lettering. Deliberate
  under the no-lettering rule, but worth a human decision if the sheet is ever a hero prop.
