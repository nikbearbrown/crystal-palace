# NOTES — Hyde Park glazing and sash panel

Prop for the Crystal Palace film. Hyde Park 1851 building only — no
Sydenham evidence is used in this model.

## What it is

One row of roof glass in timber sash bars: 5 panes between 6 sash
bars, with an end rail at each end (along-slope ends). The panel lies
flat in its roof plane. Origin at the centre of its bottom face
(z = 0 at the bottom of the sash bars). A scene builder rotates it
into the roof slope; the prop itself does not assert a slope angle.
Units: metres. Blender 4.2+.

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-012.jpg` —
  Downes Plate XII, "Glass roof and Paxton gutters", Fig. 1
  "Section of Roof": ridge (G), slopes (F), Paxton gutter (A/B),
  8 ft gutter-to-gutter pitch, 24 ft bay. The bottom detail of the
  same plate repeats sash-bar spacing as 10½ in. See `refs/` for a
  crop of Fig. 1.
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md`
  — printed-page check: glass length 49 inches (p.15).

## Dimensions — measured/printed vs guessed

| Part | Value | Status |
|---|---|---|
| Sash-bar centres | 10½ in (0.267 m) apart | Read off Plate XII bottom detail (repeated 10½ in; 11¼ in at the ends of that detail — the panel uses the repeated 10½ in spacing throughout) |
| Glass length (along slope) | 49 in (1.245 m) | Printed p.15 |
| Roof pitch | 8 ft gutter-to-gutter | Printed on Plate XII Fig. 1 (context, not a panel dimension) |
| Bay | 24 ft | Printed on Plate XII Fig. 1 (context) |
| Panel overall | 1.364 m wide × 1.245 m long | Derived: 5 × 10½ in + one bar width, by 49 in |
| Sash-bar section | 30 mm wide × 60 mm deep | Guessed — not dimensioned in the controls; the plate section (F) shows a thin bar, no printed section size was found |
| End-rail width | 60 mm (along slope) | Guessed |
| Glass thickness | 4 mm | Guessed |
| Glass visible width | 10½ in minus bar width ≈ 237 mm | Derived from spacing minus guessed bar width |
| Timber colour | Mid brown (0.45, 0.30, 0.18) | Interpretive — timber sash bars in the plate are uncoloured linework; no 1851 timber finish is verified here |
| Glass material | Pale blue-grey, 45% opacity in renders | Render stand-in for glass; in the .blend the panes are a translucent material, not a physical glass simulation |

## What was NOT modelled / known inaccuracies

- No Paxton gutter (A/B), ridge (G), truss or glazing trolley —
  this is the sash panel alone; gutters and ridge are separate
  scene-builder work.
- Only one pane length along the slope. The real roof had
  successive panes along each slope; this panel is one row, to be
  repeated along the slope by the scene builder.
- No putty, clips or fixings at pane edges.
- No dirt, breakage or variation between panes — all five panes
  are identical, which the real roof was not after months of use.

## Relationship to other models

Independent prop from the plates, like `hyde-park-column-tier1/`.
It is NOT copied from `course-models/crystal-palace-1851-claude/`
or from `blender-deliverables/`. It pairs with the column prop:
columns and girders carry the frame, this panel closes the roof
between gutters.

## Files

- `hp-glazing-and-sash-panel.blend` — model collection `Model`
  plus a `RenderSetup` collection (backdrop, lights, cameras;
  not exported).
- `hp-glazing-and-sash-panel.glb` — `Model` collection only.
- `renders/front.png` (top view: panel face), `side.png`
  (edge view: thickness and bars), `three-quarter.png` —
  neutral grey backdrop, same lighting, 1080×1440.
- `refs/` — Plate XII Fig. 1 crop and a full reference list.
