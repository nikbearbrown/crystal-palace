# Seed drill (Great Exhibition, 1851)

A horse-drawn seed drill of the type exhibited in the agricultural section at
Hyde Park in 1851: a lidded seed box spanning between two large spoked driving
wheels, a row of eleven hanging coulters with seed tubes and lifting chains
beneath it, and a drawbar running forward to a small two-wheeled fore-carriage
with a steering T-handle. Set dressing for the agricultural / machinery scenes
(CP024/CP025).

## Sources

Both references are mounted calotypes by Henry Fox Talbot from his 1852
presentation report on the Great Exhibition (public domain; see the repo
manifest, `references/muse-drive/data/manifest.csv`):

- `refs/talbot-agricultural-implements-1.jpg` — plate captioned "GARRETT AND
  SONS". The drill is at the left of the frame, seen from the rear-left: the
  seed-box end panel with the maker's medallion, the row of seed cups along the
  box, the coulter bar with its chains, and the fore-carriage wheels at the far
  end of the drawbar. (The portable steam engine centre-frame and the
  cultivator at the right are separate exhibits and are **not** modelled.)
  Repo path: `references/muse-drive/images/commons/Great_Exhibition,_Agricutlural_Implements,_HF_Talbot,_1851.jpg`
- `refs/talbot-agricultural-implements-2.jpg` — plate captioned "HORNSBY AND
  SONS". The drill is at the right of the frame, seen from the front-right:
  both driving wheels, the two lidded compartments of the seed box, the
  coulters hanging between the wheels, and the fore-carriage with its steering
  post and T-handle.
  Repo path: `references/muse-drive/images/commons/Great_Exhibition,_Agricutlural_Implements_2,_HF_Talbot,_1851.jpg`

**One machine or two?** The plates are captioned to two different makers and
show two different portable engines, so the two drills may be two makers'
machines of the same standard type rather than one exhibit photographed twice.
The shared layout is identical in every resolvable particular (wheel size and
spoke count, box form and lids, coulter row, fore-carriage), so this model is a
synthesis of the type as the two plates jointly document it — not a portrait of
one serial-numbered machine. The maker's medallion visible on the Garrett
machine's box end is represented as a plain brass boss; no lettering is
invented.

## Dimensions

Overall: 2.11 m wide × 4.32 m long (over the fore-carriage) × 1.61 m high
(the top of the raised lift lever). Model: 173 objects, 6,800 triangles.

No dimensioned drawing of either drill exists in the collection, so every
absolute dimension comes from the scale chain below; proportions between parts
were measured on the photographs and are firmer (±5%) than the absolute scale
(±10%).

| Part | Value | Basis |
|---|---|---|
| Driving wheels | Ø 1.40 m, 12 spokes | Spoke count seen in both plates. Diameter adopted from period practice for this drill class (driving wheels of 4 ft 6 in – 5 ft were standard) and checked against the engines in the same frames (boiler proportions of the portables). |
| Fore-carriage wheels | Ø 0.66 m, 6 spokes | Measured ratio to the driving wheel ≈ 0.47–0.50 in both plates; spoke count seen in plate 2. |
| Wheel track | 1.94 m between centres | Measured: wheels stand just outside the box ends in both plates. |
| Seed box | 1.84 × 0.52 m, bottom 0.88 m, top 1.30 m, lid ridge 1.42 m | Measured ratios to the wheel (box top ≈ 0.94 × wheel Ø; box length ≈ 1.31 × wheel Ø). Two lidded compartments per plate 2. |
| Coulters | 11, at 0.16 m pitch | Count: 9–10 seed cups resolve along the box in plate 1 and 10–12 shoes in plate 2; 11 adopted at the standard ~7 in row spacing of the type. Shoes rest at ground level (working position, as photographed). |
| Coulter bar | 0.47 m above ground | Measured from plate 1 (bar hangs at ≈ ⅓ wheel Ø). |
| Drawbar | ≈ 1.7 m from frame to fore-carriage | Measured from plate 2 (drawbar + fore-carriage ≈ 1.5 × wheel Ø beyond the box). |

## Measured / seen vs guessed

**Seen in the photographs and modelled as seen:** 12-spoke driving wheels and
6-spoke fore wheels; the seed box spanning between the wheels with a two-part
sloped lid and panelled faces; the row of seed cups along the box; coulters
hanging in a row beneath the box on a transverse bar, each with a chain rising
to the box; seed tubes behind the coulter shanks; the long drawbar to a
two-wheeled fore-carriage with a vertical steering post, top T-handle and a
draught hook below; the lift lever rising behind the box (plate 1); the
circular maker's medallion on the box end (plate 1).

**Inferred or schematic (not resolved in the photographs):**
- The wheel-to-feed drive: a gear ring inside the right wheel and an end gear
  on the metering shaft under the box are shown, but the intermediate gearing
  is hidden in both plates and is represented schematically only.
- The feed mechanism inside the box is not visible in either plate; the model
  carries only the external cups, the metering shaft and its feed discs.
- Coulter shoe profile (a flat triangular point) follows the type; individual
  shoes are too small in the plates to trace.
- Chain runs are drawn as sagging two-segment links per coulter — the plates
  show chains hanging at every coulter but not their exact anchor points.
- Timber/iron material split (wooden wheel spokes and felloes, wooden frame
  rails and shafts, iron tyres, bar and coulters) follows period practice; the
  calotypes are monochrome, so all colours — including the dark green paint —
  are period-typical inference, not observation.
- Absolute scale (±10%, chain above). If a dimensioned catalogue entry for
  either maker's 1851 drill surfaces, rescale uniformly from the wheel.

## Files

- `seed-drill.blend` / `seed-drill.glb` — origin at the centre of the ground
  footprint, ground at z = 0, machine built in metres, scale applied.
- `renders/` — front, side and three-quarter views on the fixed grey rig,
  plus `rear-three-quarter.png` and `plate2-angle.png` (the two photograph
  angles) and the two side-by-side compare sheets (`compare-plate1.jpg`,
  `compare-plate2.jpg`).
- `scripts/build_seed_drill.py` — the procedural build (the script is the
  source of truth); `scripts/render_seed_drill.py` — the render rig.
