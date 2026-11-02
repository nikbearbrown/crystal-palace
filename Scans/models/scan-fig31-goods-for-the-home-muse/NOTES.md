# NOTES — scan-fig31-goods-for-the-home (Muse version)

## Subject

Catalog figure 31, "Goods for the home": a colour exhibition view of a
decorative-furnishings stand at the Great Exhibition of 1851 — ornate
furnishings, cabinets, chairs, trays and visitors. The model is the
composed display group as seen in the view, on its platform. This is
the Muse version of this catalog entry. No areas of the source image
are repaired (catalog repair method: "None; geometric extraction
only"), so no part of the model rests on repaired evidence.

## What is modelled

- **Setting** — low raised platform (5.6 × 2.5 m, 0.18 m high) with a
  red carpet and gilt front trim; pale boarded floor in front; brown
  display wall behind (2.9 m high) with cornice, skirting and side
  posts; a folded deep-red curtain at the right (image right).
- **Centre** — highly ornate upright piano in black lacquer: gilt
  stringing, three gilt-framed coloured inlay panels with simplified
  floral dots (papier-mâché style), pierced/carved top rail suggested
  by a row of gilt knobs plus two finials, keyboard block with white
  keys and a black-key strip, candle sconces, turned front legs,
  castors, pedal lyre with two brass pedals, and a music desk holding
  a **blank** sheet of music (no notation). Round-topped piano stool
  in front (red upholstered seat, turned column, three feet). Two low
  dark cabinets with dark lacquer, gilt-framed doors, candlesticks
  and small vases flank the piano at the back. (Panel colours as
  corrected in Fix Round 1 — see QC.)
- **Right (image right)** — the tall **hooded porter's chair**: gilt
  frame and side wings, parametrically curved hood shell in gilt with
  a deep-buttoned orange-red upholstered inner back (buttons as a
  small grid of dark studs), red seat cushion and arm pads, gilt arm
  knobs and crest. In front of it a small ornate side chair (dark
  carved wood, dark upholstered seat, a small **blank** card on the
  seat). Beside them a tall gilt pedestal urn (tripod stand, baluster
  vase with two handles). Large round trays/plaques: one hanging on
  the wall, two leaning at the right edge, with gilt rims.
- **Left/back (image left)** — three flat display boards on the wall
  carrying door furniture: rows of simplified brass knobs on stems,
  finger plates with knobs, and escutcheons with keyhole dots
  (36 fittings in total). Above them a large diagonal carved dark
  panel (stair-rail-like) with a row of balusters and a lower rail.
  At far left a metal firescreen/fireback panel (dark iron/bronze)
  whose raised scene is simplified to a few gilt/dark relief bumps.
  A low front table carries a leaning round silver tray, a small
  dark lidded box and a small dark vessel (as corrected in Fix
  Round 1 — see QC).
- **Visitors** — stylised simplified figures, no likenesses, no facial
  features: a couple left of the piano (image left) standing looking
  toward the goods — woman in blue bodice, white full skirt, cream
  shawl and yellow bonnet (total height ~1.62 m); man in black
  tailcoat with tails, grey trousers, white shirt front, black top
  hat, holding a cane (total height ~1.75 m).

## Scale — ESTIMATED, and its basis

No dimension is printed anywhere for this stand. Scale is **estimated**
from the two anchors visible in the view itself:

- an upright piano of this period stands about **1.30 m** high to the
  top of the case — the model's piano case and lid top out at 1.29 m
  above the platform (the decorative top rail and finials rise above
  that, as they do in the view);
- the visitors are given ordinary adult heights, **1.62 m** (woman)
  and **1.75 m** (man, before his top hat) — consistent with their
  size against the piano in the view.

Everything else is proportioned from those two anchors as seen in the
view: hooded chair overall ~1.98 m high (its signature tall hood —
roughly 1.5× the piano height, as drawn), pedestal urn ~1.35 m,
side chair ~0.91 m, piano stool ~0.48 m, display boards 1.30 m tall,
hanging tray Ø 0.68 m. Treat all of these as ±15–20 % estimates.
Units: metres. Origin at the base centre of the platform, at floor
level. Scale is applied in the exported files.

## Assumptions and interpretations

- **Single view.** Only the fronts and the image-left/image-right
  sides are evidenced. Backs (piano back, chair backs, cabinet backs,
  the wall boards' fixings) are a reasonable period interpretation —
  plain, undecorated — and are **not** confirmed.
- **No readable text.** The view carries trade signs above the stand;
  both sign boards on the wall are modelled **blank**, the sheet music
  is blank, and the card on the side chair is blank. This omission is
  deliberate.
- The piano's floral inlay is reduced to coloured panels with dot
  flowers; the real papier-mâché panels are far more detailed. The
  pierced top rail is suggested, not carved through.
- The firescreen's raised pictorial scene is simplified to relief
  bumps; the diagonal panel's carving is not reproduced beyond its
  balusters and rails.
- Deep buttoning on the hooded chair is shown only on the inner back,
  as a stud grid; the seat and arm pads are plain.
- The curtain is a regular sine-fold sheet — a stand-in for draped
  fabric.
- Only the one couple specified by the view's main grouping is
  modelled; smaller background figures visible deeper in the original
  view are omitted.
- Materials follow the colour view: black lacquer, carved dark wood,
  gilt/brass, orange-red and dark-green upholstery, red carpet and
  curtain, pale floor boards. All materials are flat colours with
  metallic/roughness variation — no textures.

## Files and counts

- `build_scan_fig31_goods_for_the_home.py` — re-runnable build script
  (Blender 4.5.3, `bpy`; builds, saves, exports and renders).
- `scan-fig31-goods-for-the-home.blend` — 305 objects.
- `scan-fig31-goods-for-the-home.glb` — same scene, modifiers applied.
- `preview.png` — Cycles CPU, 960 × 720, neutral grey background.
- `refs/` — copy of the source image + `REFERENCES.md`.
- **Triangle count: 15,364** in the stored .blend geometry;
  **18,148** in the exported GLB (bevel modifiers applied on export,
  counted from the GLB index accessors). Both are well under the
  50k budget. (Counts updated in Fix Round 1, below; original build
  was 14,292 / 16,980.)

## QC

- The preview was viewed and compared with the reference: piano centre
  with keyboard, inlay panels and stool facing the camera; hooded
  chair at image right with its tall gilt hood, red interior and the
  side chair in front; pedestal urn and trays at the right edge;
  door-furniture boards, diagonal panel and firescreen at image left;
  couple at image left of the piano (woman: blue/white/yellow; man:
  black tailcoat and top hat); red-carpeted platform, pale boards in
  front, brown wall and red curtain behind. An earlier render had the
  group mirrored and the piano front facing the wall; both were
  corrected and the preview re-rendered before finishing.
- Re-running the build script reproduces the .blend, .glb and preview
  (the shipped preview was rendered from the final .blend at 24
  samples with denoising because the build machine was heavily loaded;
  the script itself renders at 32 samples — same camera, lights and
  engine).
- No text, lettering or notation appears anywhere in the model.

### Fix Round 1 (parent audit, 2026-11-01) — all fixes made in the build script and re-rendered from the same camera

Composition/layout were passed by the audit and were not moved.
The five findings, and what changed:

1. **Piano inlay (was bright teal/pink with polka dots, toy-like).**
   Panel grounds changed to deep green-black (`inlay_teal`
   0.015/0.045/0.035) and deep burgundy (`inlay_floral_red`
   0.20/0.035/0.04); floral dots halved in size (0.028 → 0.014 m)
   and recoloured to muted rose / cream / sage plus gilt; the lower
   front panel gained a gilt frame over a burgundy ground. The case
   now reads black-and-gilt overall, as in the reference.
2. **Hooded chair (was a pale boxy canopy over a cream chair).**
   Frame/base changed from dark wood to gilt; hood shell recoloured
   to a deeper gilt (0.62/0.38/0.09, less metallic wash-out) and its
   arc extended at both ends (245° → −35°) so it curves down and
   encloses the sitter; new hanging side-cheek panels follow the arc
   down each side; side wings lengthened/lowered. Interior
   upholstery deepened to a deep orange-red (0.46/0.085/0.018) on the
   inner back (extended to follow the full arc), seat and arm pads;
   the dark-stud button grid is retained.
3. **Male figure (was a dark cylinder with a top hat — chess-pawn
   read).** Rebuilt at the same low-poly level as a lathe-profile
   torso (flared tailcoat skirt → narrow waist → chest → shoulders,
   elliptical cross-section), with trousered legs now visible below
   the coat, lengthened coat tails behind, and arms angled down /
   slightly forward to suggested hands. Still faceless/stylised.
   The woman was left as passed, with one optional tweak: her
   bodice is now a slight taper (narrow waist) instead of a cylinder.
4. **Teal cabinets flanking the piano.** Door panels changed from
   bright teal to a near-black dark lacquer (`cabinet_door_dark`)
   behind a gilt frame; the remaining teal-material users (piano
   grounds, the leaning tray at the right edge) are the deep
   green-black of item 1, so no bright teal blocks remain.
5. **Far-left table goods (grey disc + pink block were unclear).**
   Replaced with a round silver tray with a gilt rim leaning up at
   the back of the table, one small dark-wood lidded box, and one
   small dark iron vessel, per the left-edge goods in the reference.

Rebuilt .blend / .glb / preview.png by re-running
`build_scan_fig31_goods_for_the_home.py`; the new preview was viewed
against the reference: piano black-and-gilt with muted inlay, hooded
chair gilt and enclosing with a deep red interior glimpse, the man
reads as a tailcoated figure with legs and arms, no teal or pink
blocks remain, and the left table carries a legible tray, box and
vessel. New counts: 305 objects, 15,364 tris (.blend) / 18,148 tris
(GLB) — still well under the 50k budget. Manual-review items 1 and 2
above are correspondingly improved but still apply at close-up
range. Not pushed to GitHub (staged package only).

## Manual-review items

1. Hood silhouette: the parametric hood reads slightly "canopy-like"
   from some angles; check against the reference's more enclosed,
   egg-like hood before use in close-up.
2. Piano inlay panels are stylised (dots on coloured grounds) — not
   suitable for a close-up without rework.
3. The couple faces the stand (backs three-quarter to a front camera
   in some framings) and is featureless by design; check the chosen
   film framing accepts back/three-quarter figures.
4. All dimensions are estimates from the piano/figure anchors
   (±15–20 %); do not quote them as measured.
5. The firescreen relief and the diagonal panel carving are
   placeholders at viewing distance only.
