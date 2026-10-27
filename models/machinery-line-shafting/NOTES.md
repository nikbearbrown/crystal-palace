# Moving machinery — line-shafting run

**Film scene:** CP024 (machines at work, Hyde Park 1851 machinery court).
**Candidate:** #34 "Moving machinery display", built as its buildable core.
**Build stats (final):** 147 objects, **12,304 triangles**; overall
29.26 m long × ~1.8 m deep × ~4.6 m high. Blender 4.2, procedural bpy
(`scripts/build_machinery_line_shafting.py`).

## Interpretation — read this first

Candidate #34 is a *scene*, not a single object: Dickinson's plate XXI
shows the whole machinery court. This asset is therefore a **set piece**,
not a reconstruction of one documented machine. It models the court's
readable drive system — **an overhead line-shaft run**: floor standards
with plummer-block bearings carrying a main shaft, graduated pulleys, one
countershaft, and wide leather belts dropping to machine positions. That
shafting-and-belt system is what made the court's machines "move" in
1851, and it is the part of the plate's subject that can be built as one
coherent, reusable prop for CP024 dressing.

Stated openly, as required:

- The plate **documents the court** — its columns, roof, floor and named
  machines. It does **not** individually resolve the overhead shafting;
  the shafting arrangement here is period-typical practice, inferred, not
  traced from the plate.
- **No single machine in the plate is individually documented by this
  asset.** Whitworth's machine tools, Fairbairn's corn-mill, the
  wrought-iron crane, Garforth's rivetting machine, Johnson's
  wire-drawing machinery, Gardner's spinning machinery, Watkins's coining
  press and Appold's pump (the plate's own caption list) are **not**
  modelled.
- At each belt drop there is only a **plain floor machine base** — a
  plinth, two bearing pedestals, a short shaft and a pulley. No machine
  silhouettes were added, generic or otherwise.

## Source

- `refs/dickinson-plate-xxi-moving-machinery.jpg` — copy of
  `references/muse-drive/images/commons/Moving_Machinery_-_Dickinson's_comprehensive_pictures_of_the_Great_Exhibition_(1854)_vol_2,_plate_XXI_-_Royal_Coll.jpg`:
  Dickinson's *Comprehensive Pictures of the Great Exhibition* (1854),
  vol. 2, plate XXI, "Moving Machinery", view from Whitworth's stand.
  **Licence: Public domain** (per `references/muse-drive/data/manifest.csv`).
  What it shows: the machinery court interior — slender palace columns
  and lattice girders, boarded floor, heavy machine tools in the
  foreground (planing-machine beds, a large gear wheel, pedestal
  machines), dense machinery and visitors behind.

## Dimensions — provenance

| Dimension | Value | Basis |
|---|---|---|
| Bay spacing | 7.315 m (24 ft) | **Documented** building module of the palace (Downes plates / building documentation in this repo). |
| Number of bays / run length | 4 bays / 29.26 m | **Presentational choice** — a useful dressing length; the court's shafting ran far longer. |
| Main shaft centre height | 4.00 m | **Inferred** — period mill/exhibition practice (shafting above head and machine height, clear of visitors) read against the plate's proportions. Not measured from the plate. |
| Main shaft diameter | 90 mm (~3½ in) | **Inferred** — typical mid-19th-century line shafting. |
| Countershaft height / offset | 2.60 m / 1.15 m to one side | **Inferred** — typical countershaft placement below and beside the main shaft. |
| Pulley diameters | 0.45–0.90 m, graduated | **Inferred** — sized for varied belt speeds, as in period practice; the plate's machines show wheels of comparable spread. |
| Belt widths | 0.20–0.26 m | **Inferred** — wide single leather belts of the period. |
| Machine-base pulley height | 0.55 m | **Inferred** — low machine shaft line, consistent with the plate's floor machines. |
| Belt thickness / sag | 6 mm / ≤35 mm on the countershaft drive | Presentational. |

**Measured or seen in the reference:** the court's column spacing rhythm
(the basis for adopting the 24 ft module here), the boarded floor, the
general scale of the floor machines relative to visitors, and the fact of
dense belt-driven machinery. **Everything about the shafting itself is
inferred**, as stated above.

## Known inaccuracies and limits

- The shafting is carried on **floor standards**; in the building it may
  equally have been hung from the structure or carried on the machines'
  own framing in places. Floor standards were chosen because they are
  self-contained (the prop needs no palace shell to stand in) and are
  documented period practice — but they are a choice, not a finding.
- Pulleys are solid-web pattern; period pulleys were also commonly
  spoked or split. Belt runs are open belts throughout; no cross-belts,
  quarter-turn belts, fast-and-loose pulley pairs or belt shifters.
- No prime mover is included: the run is shown undriven, as dressing.
- The countershaft serves only two drops; a real court run served many
  more machines, at closer spacing.
- Materials (painted near-black iron, machined steel shaft, brown leather
  belts) are period-plausible, not sampled from the hand-coloured plate.

## Files

- `machinery-line-shafting.blend` / `.glb` — the model (metres, origin at
  base centre, transforms applied; render rig excluded from the GLB).
- `renders/` — `front.png` (full elevation), `side.png` (end view down
  the run), `three-quarter.png`, `compare.jpg` (plate vs model, with the
  interpretation caveat printed on it).
- `refs/` — the Dickinson plate used.
- `scripts/build_machinery_line_shafting.py` — the full build script.
