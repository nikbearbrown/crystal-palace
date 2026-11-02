# scan-fig41-london-1851 — Muse version

**Muse version** — built by Muse for the Crystal Palace film project (Scans batch 6).

## Subject
George Cruikshank, "London in 1851" — Regent Circus (Piccadilly Circus)
crammed shoulder-to-shoulder with visitors to the Great Exhibition, the
crowded counterpart to the deserted "Manchester in 1851". Reference:
`fig-41_george-cruikshank-london-1851.png` (scan IMG_6449) and its catalog
description — "Crowded London street filled with exhibition visitors,
paired with the deserted Manchester scene."

## What is modelled
A composed circus vignette ~20 m across, following the engraving:
- Two curving stucco frontages (three angled segments each) with ground-floor
  shop arcades, fascia boards, first-floor balconies with railings, and three
  window floors above; silhouette blocks close the vista up the street.
- The great banner strung across the circus, sagging between the frontages,
  with laurel festoons at its ends and flags at the corners.
- Balconies filled with onlookers (stylised figures leaning on the rails).
- The street PACKED: 36 individually placed crowd figures in varied 1851
  dress (top hats, bonnets, shawls), three placard carriers, two hansom cabs
  with horses and drivers hemmed in by the crowd, and behind them a mass of
  160 instanced low-poly figure variants (tapered coat/skirt bodies with
  heads and top hats, caps, bonnets and shawls) filling the street and the
  vista, as the print does.
- Two street lamps on the foreground island.

## Scale
Estimated. Frontages ~13 m tall (four storeys over shops, matching the
print's proportions), circus opening ~15 m between facades, figures
1.5–1.78 m, cabs ~3.6 m long with horses. The print compresses a much larger
crowd into the frame; the model keeps the density readable rather than
literal.

## Assumptions / interpretation (not confirmed by the single view)
- The banner in the print carries a loyal inscription ("Peace & Good Will
  to All the World / God Save the Queen / Prince — Albert"). **No lettering
  is modelled** — the banner is blank cloth; text can be textured on in
  production.
- Shop names visible in the print (Swan & Edgar, etc.) are likewise not
  reproduced; fascias are blank.
- The crowd in the print numbers in the thousands and merges into texture;
  here it is 36 full figures plus 160 instanced simplified figure variants
  — a deliberate readability/performance choice, flagged for manual review
  if a denser crowd is wanted.
- Building backs, roof forms and the side streets are period-typical
  inventions; the curved plan of the circus is approximated with straight
  angled segments.
- All figures are stylised silhouettes — varied poses and dress, no
  likenesses, no individual caricature features from the print.

## Files / QC
- `scan-fig41-london-1851.blend` (metres, origin at base centre of the
  circus, scale applied), `.glb` export, `preview.png` from a viewpoint
  comparable to the engraving (elevated, looking into the circus).
- Triangles: 49,076 (budget < 50k).
- QC: procedural build; frontages, cabs and figures are joined single
  meshes under one Model collection. Companion piece to
  `scan-fig40-manchester-1851` — same street architecture language, opposite
  population.

QC note (final): preview art-directed over several passes. Two faults were
found and fixed: (1) joined builders needed root parts (cabs, horses and
frontage segments were sinking by their first part's height); (2) this
script's prim() creates size-2 cubes, so the frontage bodies were twice as
deep as the facade offset — the windows, columns and balconies were buried
inside the body volume and the buildings rendered as blank slabs; body
depth is now matched to the facade plane. The frontages were also rebuilt
on a quadrant arc (centre (0,-7), R 13.5 m) with facades aimed at the arc
centre, as the Regent Circus quadrant wraps around the viewer in the print,
and the camera moved inside the circus. Balcony figures stand on the
balcony slabs facing the street. Residual: the print's crowd is a solid
mass of hundreds — here 36 full figures + ~60 head-and-shoulder mass forms
suggest the density at vignette scale; Cruikshank's composite perspective
(giant foreground heads) is not reproduced. The banner's loyal inscription
is deliberately NOT modelled (blank cloth), as are all placard texts.

QC fix round (crowd rebuild): the original mid-ground and distant crowd
masses — bare cylinders with ball heads — read as fence posts, not people.
They were replaced by 160 instanced low-poly figure variants (four types —
top hat, cap, bonnet, shawl — in three colourways each, placed as
shared-mesh copies on staggered rows), packed shoulder-to-shoulder through
the street's middle band and down the vista, thinning at the frame edges
and routed around the cabs, placards and foreground figures. Triangle
count rose 41,132 → 49,076, still under the 50k budget. Preview
re-rendered at 48 samples + denoise from the same camera; the crowd now
reads as people at a glance.
