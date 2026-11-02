# NOTES — scan-fig04-royal-commissioners (Muse version)

**Source:** fig-04_royal-commissioners-great-exhibition-1851.png —
Henry Windham Phillips, "The Royal Commissioners for the Great
Exhibition of 1851" (catalog fig. 4, IMG_6420).

## Subject
A group vignette: 13 stylised gentlemen in 1851 dress (dark frock
coats, pale waistcoats, white shirts, cravats) gathered around a long
mahogany table bearing the exhibition plans — large and medium plan
sheets, a rolled plan, loose papers and a pair of dividers. Six are
seated (one writing; the white-haired commissioner on the near side,
back to the viewer, holding the rolled plan; Prince Albert on the far
side facing the viewer in the painting's ornate high-back chair,
hands on the large plan sheet), seven stand behind. All figures are mannequin-like records of
pose and dress: **no facial features and no individual likenesses
are modelled** — the painting's sitters are identifiable people, and
this model deliberately does not attempt portraits. Side whiskers on
two figures are period dress detail, not likeness.

## Scale
Figures ≈ 1.70–1.78 m standing; table 3.5 × 1.15 m at 0.76 m high.
**Estimated** throughout — the painting carries no dimensions; sizes
follow ordinary period furniture and figure proportions.

## Assumptions / interpretation
- The painting shows 14 heads; the group is built with 13 figures —
  the half-hidden seated figure behind the writing commissioner is
  merged into the group rather than modelled as a separate partial
  figure. **Manual-review item** if an exact head-count is wanted.
- Poses are simplified to a small set of arm gestures read from the
  painting (writing, pointing at the plan, holding a roll, hands on
  the plan sheet, clasped hands, arms at rest).
- The painted room (dark panelling, a portico glimpse) is reduced to
  a plain backdrop wall with two pilasters — room dressing kept
  minimal as briefed; the painting's landscape backdrop is omitted.
- The fringed upholstery of the painted chairs is simplified to
  plain upholstered backs; only the central ornate chair keeps
  finials.
- Colours are conventional: the reproduction is monochrome, so coat,
  waistcoat and mahogany tones are period-typical choices.

## Build
- `scan-fig04-royal-commissioners.blend` / `.glb` — Model collection
  only in the GLB; metres, origin at base centre, scale applied.
- Figures are parametric (shared builder function in the build
  script), each a separate named group of meshes for editability.
- Triangles: **29,720**, 279 objects — verified from the saved .blend
  (no unapplied scale; world bbox 5.60 × 3.37 × 3.00 m including the
  backdrop wall).
- Preview: renders/preview.png — frontal wide shot, comparable to
  the painting.

## QC
- Preview checked against the painting: table group reads, plan
  sheets and dividers on the table, standing row behind, Albert on
  the far side in the ornate chair, the white-haired commissioner in
  the near-side foreground as in the painting. First-pass defects
  (waistcoat/shirt ellipsoids poking through the coats as irregular
  white patches; Albert's chair back hiding him from the camera)
  were found in the first preview and rebuilt — waistcoats are now
  clean arc shells and the seating arrangement follows the painting.
