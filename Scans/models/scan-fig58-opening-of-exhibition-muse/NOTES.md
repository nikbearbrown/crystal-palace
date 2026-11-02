# scan-fig58-opening-of-exhibition — Muse version

**This is the Muse version** of this model (ships as `scan-fig58-opening-of-exhibition-muse`).

## Source
- Figure 58, H. C. Selous, "The Opening of the Great Exhibition" (1851–2), V&A.
- Source image: `fig-58_opening-great-exhibition-hc-selous-1851.png` (catalogue scan IMG_6437).
- Catalogue note: the right edge of the painting is clipped by the source photograph; the
  vignette is composed inside the visible field. One view only.

## Subject modelled
The opening ceremony of 1 May 1851 as a composed vignette (~15 m wide):
- Central **royal dais**: three carpeted steps, two throne chairs, and the crimson-and-gold
  **canopy** on four slender gilt columns with scalloped valance and hanging back drapes.
- The **royal party and officials** as a stylised group on the dais: a queen figure in a dark
  crinoline dress with a blue sash band, a prince figure in dark court dress with sash, two
  royal children, a white-robed cleric, an official with a gilt staff, courtiers and
  child attendants at the canopy sides. **No likenesses** — all figures are generic
  period-dress silhouettes.
- **Crowd**: rows of stylised spectators (crinoline dresses, bonnets, top hats) flanking the
  central red-carpet aisle, with larger foreground backs at the lower corners as painted.
- Backdrop: a simplified **transept arch** on two columns, four hanging banners in abstract
  colours (no arms or lettering invented), the **Osler crystal fountain** hinted at the right
  (tiered glass form), and the great **elm** hinted at the left.

## Scale
- **Estimated** from the figures (adults ~1.7 m). Dais platform 7.4 m wide; canopy top ~4.9 m;
  backdrop arch spans ~12.8 m with its crown at ~10 m — a compressed backdrop, not a
  full-size transept (the real transept vault was far larger; see assumptions).

## Assumptions and interpretation
- The backdrop arch is a **stage-flat vignette element**: the painting itself compresses the
  transept, and the model follows the painting's compression rather than true building scale.
- Placement and dress colours of the royal party follow the painting's arrangement broadly;
  individual identities beyond the two central figures are not asserted.
- Banners are plain coloured cloth; the painting's heraldic detail is deliberately not
  reproduced or invented.
- The fountain is a "hint" (tiered silhouette in pale glass material), matching its
  half-hidden position at the painting's right edge.
- Everything behind the dais plane and outside the frame is interpretation.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- Crowd figures are linked duplicates of three low-poly prototypes (man / woman / child).
- 20,784 triangles.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, elevated frontal
  view comparable to the painting), re-runnable `build_scan_fig58.py`.

## Manual-review items
- A full architectural transept backdrop exists in other Crystal Palace assets; this
  vignette's compressed arch is intentional and should not be swapped silently.
- Heraldic banners and court-dress detail would need a dedicated research pass.
