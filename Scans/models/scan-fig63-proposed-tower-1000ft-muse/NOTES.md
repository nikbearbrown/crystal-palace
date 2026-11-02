# scan-fig63-proposed-tower-1000ft — Muse version

**This is the Muse version** of this model (ships as `scan-fig63-proposed-tower-1000ft-muse`).

## Source
- Figure 63, "Design for the Conversion of the Exhibition-Building into a Tower 1000 Feet
  High", by Mr C. Burton, architect (engraving, 1851).
- Source image: `fig-63_crystal-palace-conversion-tower-design.png` (catalogue scan IMG_6433).
- The print shows the tower in parkland with paths and tiny visitors. One view only.

## Subject modelled
The drawing modelled as architecture, presented as an architect's display model:
- **Scale: design scale, model at 1:100.** The design's stated height is 1000 ft
  (304.8 m); the model tower stands **3.048 m** — a 10 ft model of a 1000 ft design.
- From the ground up, following the engraving's tiers:
  - the Crystal Palace itself as the base — glazed nave block with lower side wings and
    the great transept front: an arch-topped glazed panel with frame ring, transom,
    mullions and a dark central door, with the barrel vault rising behind it;
  - a broad multi-storey block (floor ledges + mullions), with two small turrets with
    pyramidal caps at its top corners;
  - a mid tower carrying the design's large circular window (ring, dark glass, cross bars);
  - the long slim shaft: six stacked segments stepping slightly inward, each with its
    floor ledge and mullions;
  - a cap block and small lantern, a flagpole and a plain red flag (blank, no device).
- Presentation: landscaped plinth on a wooden baseboard — lawn, the print's cross paths
  and main approach, six model trees, two 1:100 visitors (~17 mm) on the path, and two
  **blank** annotation boards on easels at the front corners (ruled lines only, no text).

## Scale basis
- Stated in the print itself: 1000 feet. Tier proportions (palace base ≈ 13% of height,
  broad block to ≈ 42%, oculus tier to ≈ 59%, shaft to ≈ 93%) were measured off the
  engraving's own proportions and are **interpretation of a drawing**, not of a building —
  the tower was never built.

## Assumptions and interpretation
- The engraving is an elevation; depths are inferred by analogy with the palace's real
  proportions and kept shallower than widths, as presentation models usually are.
- Floor counts within tiers follow the engraving's banding rhythm, simplified; the real
  print's storeys are more numerous and finer.
- The palace base's glazing is a flat pale glass material with frame bars — a model's
  shorthand for the iron-and-glass original.
- The rear elevation is plain banded repetition of the front's tiers.
- The tiny visitors and trees are scale devices from the print, not surveyed content.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 5,784 triangles, 152 objects.
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, portrait-format
  three-quarter view from the front, comparable to the engraving), re-runnable
  `build_scan_fig63_tower.py`.
- QC: the first render's transept read as a floating pale disc (the barrel vault's end
  cap, proud of the facade). The vault was sunk behind the facade and the front rebuilt
  as a flush glazed arch; re-rendered twice until the arch read correctly.

## Manual-review items
- If a full-height version is ever needed, the same script's tier heights can be scaled
  ×100 — but the ledge/mullion shorthand is a model's language and would need real
  storey design at 1:1.
- The engraving's base shows more of the palace's side ranges than the model's compact
  wings; widen the baseboard and wings if the base becomes the focus.
