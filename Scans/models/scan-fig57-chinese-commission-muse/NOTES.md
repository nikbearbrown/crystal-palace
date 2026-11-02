# scan-fig57-chinese-commission — Muse version

**This is the Muse version** of this model (ships as `scan-fig57-chinese-commission-muse`).

## Source and historical context
- Figure 57, satirical frontispiece to Henry Sutherland Edwards, *An Authentic Account of
  the Chinese Commission, which was sent to report on the Great Exhibition* (1851),
  discussed in the source book as an example of British **Orientalist caricature**
  (catalogue scan IMG_6438; original has rounded top corners).
- One view only (a hand-coloured frontispiece).

## Treatment — read this first
The source is a satirical frontispiece whose figures are caricatured. Per the batch rule
the model preserves the **composition** — a Chinese commission disembarking — with all
figures rendered as dignified, neutral stylised silhouettes in period dress: no facial
features, no caricature exaggeration. Period dress elements that are clothing, not
caricature (the long robe, the wide conical hat, the sash) are retained as dress.
The tall staff is a **plain pole with a finial**: the print's inscribed banner is NOT
reproduced — no lettering and no pseudo-script anywhere in the model.

## Subject modelled
- Centre: the commission's official in a long red robe with two plain trim bands and a
  sash, wide conical hat, carrying the tall staff, stepping onto a **gangplank** over
  water at a stone quay.
- Attendant (left rear) carrying the commission's great **kettle** — big rounded vessel
  with lid, knob, spout and swing handle — at his side.
- Attendant (right rear) with a large banded **hamper chest** on his back and a rolled
  scroll on top.
- A fourth attendant at the left edge (cropped by the frame, as in the print) holding a
  red **parasol** over the party.
- Backdrop set-dressing, as drawn: distant green hills, a three-tier **pagoda**, and a
  **junk** with a plain battened sail on the water behind the quay. Water strip in front.

## Scale
- **Estimated**, set from the figures (official 1.82 m; attendants ~1.7 m). Vignette
  footprint ~6.4 × 5.7 m; staff 3.5 m. The backdrop elements are deliberately compressed
  flat set-dressing, following the print's shallow stage-like space — not true scale.

## Assumptions and interpretation
- The print is a shoreside embarkation scene; the quay/water split and plank angle follow
  the drawing. Everything behind the figures is a flat backdrop by design.
- The kettle and hamper are modelled from their drawn silhouettes; their far sides and
  exact construction are interpretation.
- Robe colour follows the print's red; trim bands and sash are plain dress detail.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 6,144 triangles.
- Files: `.blend`, `.glb` (verified glTF), `preview.png` (Cycles, 48 samples + denoise,
  portrait-format frontal view comparable to the print), re-runnable
  `build_scan_fig57.py` with its in-folder `vignette_common.py` helper.
- QC note: an early draft rendered the robe's trim bands as free-standing rings (a torus
  orientation error); they were rebuilt as hugging sleeve-cylinders and the camera was
  pulled back so the parasol attendant is in frame.

## Manual-review items
- A parallel builder's separate package for this entry exists at
  `scan-fig57-chinese-commission-frontispiece/` — the parent should ship only one.
- The parasol attendant is half-cropped at the frame edge, as in the print; widen the
  composition if he is ever needed whole.
- Sensitivity review recommended before any public use, given the source.
