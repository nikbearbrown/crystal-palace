# NOTES — Paxton gutter and main gutter

Prop for the Crystal Palace film. **Hyde Park 1851 building only** — no
Sydenham evidence is used in this model. Scenes: CP011 / CP015 (the
ridge-and-furrow roof and how it drains). Two related pieces in one folder,
in separate collections in the .blend:

- **Paxton_Gutter_24ft** — one full 24 ft bay length of Paxton's hollow
  timber roof gutter (Downes Plate XII).
- **Main_Gutter_24ft** — one 24 ft span length of the main gutter the
  Paxton gutters discharged into (Downes Plate XIII).

Both lengths run along X, side by side; origin at the base centre of the
pair, z = 0 at the underside of each piece. Units: metres. Blender 4.2+.
1,392 triangles total.

## Relationship to existing models

`hp-glazing-and-sash-panel/` is the sash panel only. `hp-roof-furrow-bay/`
contains a Paxton gutter **as one component of a complete roof bay**, its
profile traced proportionally from the same Fig. 10. This folder is the
standalone gutter prop: the same printed anchors, the gutter at full bay
length with its sash-bar notch chain, plus the Plate XIII **main gutter,
which no other model in the repo includes**. The glazing wagon
(`glazing-wagon/`) ran along these gutters.

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-012.jpg` — Downes
  Plate XII, "Glass roof and Paxton gutters": Fig. 10 (enlarged gutter
  section, printed dimensions), Fig. 3 (gutter elevation with the bar-notch
  chain), Fig. 1 (roof section: 8 ft gutter pitch, 49 in panes, 10½ in
  sash-bar centres — used as calibration cross-checks).
- `references/downes-1852/source-scans/plates/plate-013.jpg` — Plate XIII,
  "Main gutters": Fig. 2 (section at i.i, printed dimensions), Fig. 4
  (section at b.b), Fig. 5 (main gutter over 24 ft span, fall printed),
  Fig. 7 (Paxton gutter shoe bolted through the main gutter).
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` —
  controls D06 (24 ft primary unit) and D09 (8 ft gutter pitch), both
  plate-checked.

Downes (1852) is a period publication; the plates are public domain.

## Dimensions — measured/printed vs guessed

### Paxton gutter (Plate XII Fig. 10 + Fig. 3)

| Part | Value | Status |
|---|---|---|
| Length | 24 ft (7.315 m) | Control D06; Fig. 3 elevation is one bay |
| Overall depth | 6 in | **Printed** on Fig. 10 |
| Base width | 5 in | **Printed** on Fig. 10 |
| Channel width at top | 3 in | **Printed** on Fig. 10 |
| Channel depth | 3 in (solid 3 in below) | **Printed** segments on Fig. 10 (1¼ + 1¾ in) — see the discrepancy note in inaccuracies |
| Cheek width at top | ≈5.7 in | Traced proportionally from Fig. 10 (same reading as `hp-roof-furrow-bay/`) |
| Condensation groove | Concave side groove, top lip 3¼ in above base | Lip height **printed** on Fig. 10 (3¼ in); groove depth/shape traced proportionally |
| Bar notches | 27 housings per cheek; 5¼ in end margins, 10½ in centres, 11¼ in flanking strong bars at 4/12/20 ft; 1 in wide (2½ in at strong bars) | Chain **printed** on Fig. 3 and closes exactly (last margin 5¼ in); notch **depth ⅜ in inferred** |
| Colour | Pale warm off-white painted timber | Interpretive — as `hp-roof-furrow-bay/`: the roof reads pale in 1851 interior photographs; timber was painted, not bare |

Calibration cross-check: the same plate prints the 8 ft gutter pitch
(Fig. 1, "8′ 0″") and the 10½ in sash-bar centres / 49 in pane length used
by `hp-glazing-and-sash-panel/` and `hp-roof-furrow-bay/`; the profile
anchors above are the plate's own printed figures, not pixel scaling, so
no px/in calibration was needed for them. The proportional traces (cheek
flare, groove shape, channel curve) follow the sibling build's reading of
Fig. 10 for consistency between the two models.

### Main gutter (Plate XIII Figs. 2, 4, 5)

| Part | Value | Status |
|---|---|---|
| Length | 24 ft (7.315 m) | Fig. 5: "Main gutter over 24 feet span" |
| Bottom board E | 14 in wide × 2½ in thick | **Printed** on Fig. 2 ("1′ 2″", "2½″") |
| Side boards C / D | 1⅜ in thick, standing 6 in above E | **Printed** on Fig. 2 |
| Overall depth | 8½ in | **Printed** on Fig. 4; = 6 + 2½ in, consistent |
| Clear channel width | 5¼ in | **Printed** on Fig. 2 |
| Outside width at top | 8 in (= 5¼ + 2 × 1⅜) | **Printed** on Fig. 2; arithmetic closes |
| Fall | ⅜ in in 8 ft (1⅞ in over this length) | **Printed** on Fig. 5 — **modelled level**, see inaccuracies |
| Bolts | Ø ½ in, square nut below E | Pattern from Fig. 2; **spacing inferred** (ends + 4/12/20 ft module centres) |
| Cross-tie | One timber tie between the boards at mid-length | From Fig. 4 (section at b.b); its exact form at other points is not shown — one fitted, flagged |
| Colour | Plain mid timber | **Unverified** — the plate gives no colour; the main gutter sat high and largely unseen |

## What was NOT modelled / known inaccuracies

- **Falls omitted.** Both gutters are modelled level so the lengths repeat
  cleanly. The main gutter's printed fall is ⅜ in in 8 ft (Fig. 5); the
  Paxton gutters were likewise cambered/fell to their outlets. (The
  `hp-roof-furrow-bay/` notes quote the fall as ⅝ in; on Plate XIII Fig. 5
  the figure reads ⅜ in — flagged here so the two can be reconciled.)
- **Channel-depth fractions.** Fig. 10's two small vertical dimensions in
  the channel are read here as 1¼ + 1¾ in (3 in total), which also puts the
  U's bottom at half the 6 in section height, where the plate draws it.
  `hp-roof-furrow-bay/` read the same worn glyphs as 1¼ + 1¼ in (2½ in
  total), so the two models differ by ½ in of channel depth — flagged so
  the readings can be reconciled against the plate. The 6 in overall,
  5 in base, 3 in channel mouth and 3¼ in groove-lip figures are clear.
- **Ends are square-cut.** In the building the Paxton gutter ends met the
  cast-iron shoe over the main gutter (Plate XII Figs. 4–6, Plate XIII
  Figs. 6–7) and its cast-iron support struts (Plate XII Figs. 7–9);
  neither the shoe nor the struts are modelled here.
- **The sash rebate** where the glass and bar ends meet the cheek top
  (Fig. 10) is simplified to the notch housings; the small glazing clips
  drawn on the plate are not modelled.
- **Bolt spacing** on the main gutter is inferred; the plate sections show
  the bolt pattern, not its pitch. The Fig. 7 through-bolt that clamps a
  Paxton gutter shoe to the main gutter is part of that junction, not of
  either standalone length.
- Profile curves (channel U, condensation groove) are smooth interpolations
  through points traced from Fig. 10, anchored on the printed figures
  above; they are not dimensioned curves on the plate.

## Renders

One fixed neutral-grey studio rig (Cycles CPU — libEGL is unavailable on
the build VM, so Eevee could not be used): `front.png` (long elevation),
`side.png` (both end sections), `three-quarter.png`,
`end-section-paxton.png` and `end-section-main.png` (isolated close-ups),
`compare-paxton-section.jpg` and `compare-main-section.jpg` against the
plate sections. In the render copies only, the pair is lifted 55 mm so the
main gutter's under-board nuts clear the studio floor; the prop file
itself keeps z = 0 at the undersides.

## Build

Procedural Blender Python: `scripts/build_paxton_gutter.py` (profile
extrusion + notch-strip segments; boxes/cylinders for the main gutter),
`scripts/render_paxton_gutter.py`, `scripts/export_glb.py`,
`scripts/make_compare.py`. Real-world metres, origin at base centre,
scale applied.
