# scan-fig61-at-the-opera — Muse version

**This is the Muse version** of this model (ships as `scan-fig61-at-the-opera-muse`).

## Source
- Figure 61, "The Opera", *Punch*, 1851 — catalogued under the theme "Crossing boundaries:
  dressing and undressing".
- Source image: `fig-61_the-opera-crossing-boundaries-cartoon.png` (catalogue scan IMG_6434).
- **Note on the brief:** the batch brief guessed an opera-box interior. The image itself is
  a standing reception in a grand salon — a long table down the middle, a chandelier, an
  arched opening at the back, and a receiving line of guests in wildly varied national and
  evening dress. The model follows the image, not the guess. One view only.

## Subject modelled
A salon vignette ~7.6 m wide × 3.3 m high:
- The room: panelled back wall with pilasters, cornice and skirting; a central arched
  opening (dark room beyond, with one dim figure standing in it); boarded floor.
- A long cloth-covered table down the centre (gold trim line, low brass centrepiece bowl,
  two candlesticks) and a brass chandelier above it — stem, ring, six candle arms, small
  crystal drops.
- The receiving line, arranged as drawn:
  - far side: two men in tailcoats (one with a cream waistcoat), a woman in a pink
    crinoline with burgundy bodice, a third man, plus background guest busts;
  - left end: a man in a fur-trimmed cloak with a tall conical hat, and a woman in a pale
    crinoline with a black bodice;
  - centre, facing the viewer: the principal figure in a patterned cloak with a feathered
    headdress, holding a long staff with a gilt knob;
  - right of centre: a man in a turban with a round hand-fan, a woman in a white crinoline
    with a blue bodice, and a girl in a short pink dress;
  - far right: a guardsman in a bearskin and red coat with gold epaulettes and a white
    cross-belt, and a woman entirely in white with a veiled head.

## Treatment of the source
The cartoon's comedy is the jostling of national costumes at a fashionable reception.
The model keeps the **composition and the costumes as dress silhouettes** — cloak, turban,
feathers, bearskin, veil, crinolines — with every figure a dignified stylised form: no
facial features, no likenesses, no caricature exaggeration of any person or nation.
All heads use the same neutral tone as every other batch figure.

## Scale
- **Estimated** from the figures (adults 1.62–1.82 m). Table 3.85 m long; ceiling line
  3.3 m; chandelier ring at ~2.4 m.

## Assumptions and interpretation
- The room is a shallow stage slice: side and rear construction beyond the drawn view is
  not modelled.
- The principal figure's exact identity/nation is not stated in the model; the patterned
  cloak is two plain tones and the headdress three upright plumes — the drawing's
  silhouette, not an ethnographic claim.
- The dark area above the arch (a transom-like panel) follows the engraving's dark
  rectangle behind the chandelier.
- Tableware beyond the centrepiece and candlesticks is not individually modelled.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 45,240 triangles, ~290 objects (the most figure-heavy model in the batch; still under
  the 50k cap).
- Files: `.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, frontal view
  comparable to the cartoon), re-runnable `build_scan_fig61_opera.py`.
- QC: first render had the principal figure's cloak panel misplaced at thigh height, the
  chandelier cropped by the frame, and the veiled woman out of shot; panel moved to the
  torso, camera pulled back and raised, chandelier drops reduced — package re-rendered.

## Manual-review items
- Figure count could be trimmed (background busts merged) if the 45k triangle count is
  a problem for a target engine.
- The principal figure's headdress plumes read as plain white blades at distance; a
  sculptor pass could give them feather barbs if he is ever a hero figure.
