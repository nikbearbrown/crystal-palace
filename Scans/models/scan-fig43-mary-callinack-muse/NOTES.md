# NOTES — scan-fig43-mary-callinack (Muse version)

**Source:** fig-43_mary-callinack-penzance-1851.png — engraved seated
portrait of Mary Callinack of Penzance, Illustrated London News,
25 October 1851 (catalog fig. 43, IMG_6447).

## Subject
A stylised seated elderly woman on a plain wooden side chair: large
dark bonnet, checked shawl over the bodice, long skirt with a pale
apron front, arms folded with hands clasped in the lap, head bowed,
shoes just visible below the skirt. The figure is a mannequin-like
record of pose and dress: **no facial features and no likeness are
modelled**, per the batch rule for figures.

## Scale
Seated group ≈ 1.48 m to the bonnet crown; the seated figure is in
the ~1.4 m seated-height class per the brief. **Estimated** — the
engraving carries no dimension; proportions follow the image and
ordinary chair dimensions (seat height 0.45 m).

## Repair caveat (important)
The scan's left edge is a modern generated background patch, and the
tear in the original reaches the outline of the dress (catalog repair
record: ~11% of pixels changed, background only). **That strip is
treated as non-evidence.** Where the dress outline is lost at the
left, the skirt is continued as a plain, smooth bell — the plainest
period interpretation — and no detail has been invented there. The
model therefore does not reproduce any feature that exists only in
the repaired area.

## Assumptions / interpretation
- Single three-quarter engraved view: the chair is mostly hidden
  behind the sitter in the original; the chair shown (seat, legs,
  two back rails) is the plainest period side-chair interpretation.
- The shawl's check is suggested by one diagonal wrap band only;
  the engraving's woven check pattern is not reproduced as texture.
  Her white hair shows as a band at the bonnet's opening.
- Colours are conventional period tones read from a monochrome
  engraving (dark bonnet, mid-tone dress, pale apron).
- The bowed head angle and clasped hands follow the engraving.

## Build
- `scan-fig43-mary-callinack.blend` / `.glb` — Model collection only
  in the GLB; metres, origin at base centre, scale applied.
- Triangles: **4,876**, 27 objects — verified from the saved .blend
  (no unapplied scale; world bbox 0.91 × 0.98 × 1.49 m).
- Preview: renders/preview.png — front-left three-quarter, comparable
  to the engraving.

## QC
- Preview checked against the engraving: bonnet mass with the bowed
  face sitting in its opening, white hair band, shawl wrap band,
  folded arms with clasped hands, pale apron front over the skirt
  bell, chair rails behind, shoe toes at the hem. The build took
  several preview iterations: the apron first z-fought against the
  skirt (rebuilt as a uniformly proud partial shell), and the bonnet
  crown — first a closed lathe that swallowed the face — was rebuilt
  as an open-front shell with a solid cap and interior plug so the
  face reads in the opening. Residuals at this stylisation level: a
  small dark tab at the bonnet's front rim (reads as a bonnet bow)
  and a hairline shadow sliver at the opening's far edge.
