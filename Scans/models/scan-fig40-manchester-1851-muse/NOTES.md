# scan-fig40-manchester-1851 — Muse version

**Muse version** — built by Muse for the Crystal Palace film project (Scans batch 6).

## Subject
George Cruikshank, "Manchester in 1851" — the satirical companion to
"London in 1851": Manchester's streets stand empty because the whole town
has gone to the Great Exhibition. Reference:
`fig-40_george-cruikshank-manchester-1851.png` (scan IMG_6449) and its
catalog description — "Satirical view of deserted Manchester streets as
residents travel to the exhibition."

## What is modelled
A composed street section ~25 m long, following the engraving:
- Terraced brick frontages on both sides (ten buildings in five converging
  rows), 3–4 storeys with pitched roofs and chimneys, sash-window grids,
  stone sills.
- Ground-floor shopfronts with fascia boards and hanging signs on the near
  rows; poster boards pasted on the plainer frontages further down.
- Cobbled carriageway with raised pavements, converging and narrowing into
  the distance, closed by silhouette blocks, a mill chimney and a church
  spire.
- Five cast-iron street lamps.
- Emptiness is the subject: the street is deserted. The print shows at most
  a tiny seated figure far down the right-hand pavement; one small seated
  figure on a crate is included there, and nothing else moves.

## Scale
Estimated. Buildings are modelled at plausible Manchester terrace scale:
frontages ~5.4 m wide, 9–13.5 m tall, street narrowing from ~11 m to ~8.5 m
between facades, lamps 3.9 m. The engraving's perspective is exaggerated
for effect; the model regularises it into a buildable street.

## Assumptions / interpretation (not confirmed by the single view)
- This is a satirical print, not a survey: no specific Manchester street is
  identified, and none is claimed. Building heights, window counts and the
  degree of convergence are interpretive.
- The many placards and shop signs in the print carry jokes ("Gone to the
  Great Exhibition" etc.). **No lettering is modelled** — signs and posters
  are blank boards, so the gag must be re-added in production if wanted.
- Rear elevations, roof details beyond the ridge line, and the far end of
  the street are invented period-typical forms.
- The single seated figure is stylised, with no likeness intended; its
  presence follows the tiny figure visible in the print.

## Files / QC
- `scan-fig40-manchester-1851.blend` (metres, origin at base centre of the
  street section, scale applied), `.glb` export, `preview.png` from a
  viewpoint comparable to the engraving (looking down the street).
- Triangles: 7,764 (budget < 50k).
- QC: procedural build; each building is one joined mesh; grouped under a
  single Model collection. Companion piece to `scan-fig41-london-1851`.

QC note (final): preview art-directed over three passes — joined builders
needed root parts (buildings/lamps were sinking by half their first part's
height), the camera was raised to the print's elevated viewpoint, and the
segmented road (which rendered with dark bands at every joint) was rebuilt
as continuous narrowing ribbons for road and pavements. The far block's top
edge is broken with rooftop blocks so the mill chimney and spire read
against the sky as in the print.
