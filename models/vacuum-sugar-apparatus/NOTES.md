# Vacuum sugar apparatus (copper vacuum pan) — candidate #28

Hyde Park 1851, machinery / process section (film scene CP024). The great
spherical copper vacuum pan photographed by Henry Fox Talbot: polished
spherical pan on a riveted girdle ring, dome neck with a swan-neck vapour
pipe arching to a vertical condenser column, and a thicket of brass valves,
taps and gauge glasses at working height.

## Sources

- `refs/Great_Exhibition,_Vacuum_Sugar_Apparatus,_HF_Talbot,_1851.jpg` —
  the ONLY reference: frontal calotype photograph, Henry Fox Talbot, 1851,
  from Talbot's presentation report (Spicer Brothers / W. Clowes & Sons,
  1852). **Public domain** (manifest: "Public domain"). Copied into `refs/`.
- No other view of this apparatus exists in the collection: no side, rear or
  detail image. Everything not visible in this one frontal photograph is
  marked inferred below.

## Dimensions and provenance

All **proportions were measured off the photograph** (1501 × 2059 px; the
sphere spans ≈ 1000 px, two-thirds of the frame width):

| Part | Model | Photo measurement |
|---|---|---|
| Pan (sphere) diameter | 2.20 m | 1000 px — the unit all else is scaled from |
| Overall height (arch crown) | 4.13 m | ≈ 1.88 × sphere Ø |
| Sphere centre height | 1.42 m | bottom lost in floor shadow; sphere completed geometrically |
| Girdle ring | z 0.72–0.89 m, Ø ≈ 2.03 m | ring at 79% of sphere height from its top |
| Dome neck | Ø 0.40 m, top flange Ø 0.55 m at z 3.29 m | neck Ø = 0.18 sphere Ø |
| Swan-neck pipe | Ø 0.26 m, legs 1.05 m apart | tube = 0.115 sphere Ø, legs = 0.48 sphere Ø |
| Condenser column | Ø 0.38 m, top flange z 3.10 m | column Ø = 0.17 sphere Ø |
| Twin standpipe cluster (front left) | 1.89 m overall | ≈ 0.80 sphere Ø at the adopted scale (photo ≈ 0.71–0.80) |
| Overall footprint incl. fittings | ≈ 2.9 × 1.9 m | tap tip to valve stack |

**Absolute scale is ADOPTED, not documented (± ~15%).** The photograph
contains no person, no legible dimension and no scaleable fitting of known
size. The chain: working vacuum pans of the period were prestige pieces of
roughly 6–8 ft pan diameter, and the hand-worked valve stands in the
foreground fix the human scale of the fittings; a 2.20 m (7 ft 3 in) pan
reconciles both. If a documented size for this exhibit surfaces, the model
rescales uniformly — every internal proportion is photo-measured.

## Measured / seen vs guessed

**Seen in the photograph and modelled from it:** the sphere and its polished
read (the palace roof reflects in the copper, confirming the form); the
riveted girdle ring low on the sphere; the dome neck with its stepped base,
bolted top flange and maker's plate (the plate's lettering is **illegible**
in the photograph and is left blank — no text invented); the swan-neck's
clean inverted-U; the condenser column with bolted top flange, side lever
and front gauge glass; two ball-capped fittings on the front shoulder; the
tall graduated gauge glass on the right shoulder; a small round boss on the
right flank; the twin standpipes with their bolted manifold, twin valve
bonnets, elbow and lever; the draw-off tap at the left with cross handle,
curved spout and bulbous pendant; the centre discharge valve with its long
hanging operating rod; the slim valve stand front-right; and the three-valve
stack at the far right with its horizontal connector pipe from the pan.

**Inferred (not visible in the photograph):**
- Everything below the girdle ring is in deep shadow. The four curved
  bracket feet and their pads are a period-plausible support, **invented**;
  the sphere's underside is completed as a sphere because nothing else is
  geometrically sensible.
- The condenser column disappears behind the pan at shoulder height. Its
  reducer, downcomer and offset drop leg below that point are **inferred**
  plumbing, arranged to clear the sphere.
- The **rear of the apparatus is wholly unseen**. No fittings have been
  invented for the back; the sphere, ring, neck and arch are rotational or
  planar forms whose backs follow from their fronts.
- Fitting positions on the shoulder (ball valves, gauge glass, flank boss)
  are placed from their positions in the single frontal view; their
  front-to-back placement carries the usual single-view uncertainty.

## Build

- Procedural bpy (Blender 4.2), script in `scripts/`; renders on one fixed
  neutral-grey studio rig (`front` = the documented view; `compare` is the
  same rig in a portrait frame echoing the photograph).
- **27,740 triangles, 154 objects.** Real-world metres, origin at base
  centre (floor, under the pan axis), scale applied.
- Materials: polished copper / copper pipe / brass / cast iron / steel /
  gauge glass. The .blend's copper is tuned for Cycles scene lighting; the
  .glb carries the same flat PBR colours (its polished read depends on the
  scene environment, as with all the metal props in this folder).

## Known inaccuracies

- Absolute scale ± ~15% (see above); proportions ± ~5%.
- The dome neck's stepped base is slightly more "wedding-cake" than the
  photograph's smoother flare.
- Small fittings (valve bonnets, handles) are resolved only as far as the
  calotype resolves them; their internal detail is schematic.
- The support brackets and the condenser's lower plumbing are inventions
  in shadow/hidden regions, as flagged — treat them as dressing, not
  evidence.
