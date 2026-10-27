# NOTES — central-transept concert organ front (Gray & Davison, 1857)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 5,
item 23). Scenes: the central-transept concert sequence (plan
coverage map: CP045; storyboard v001 concert passages CP050 /
CP055). **Sydenham only** — no Hyde Park evidence is used.

## Gate verdict: OPEN — built

Item 23 was gated on the round-1 leads 0032 / 0057 / 0595
resolving to the organ's actual form, plus a checked festival
configuration. Both tests are met (see `refs/REFERENCES.md`):

- **0057** (albumen stereo photograph, c.1860–c.1880,
  Rijksmuseum RP-F-2012-96-339) and **0595** (Negretti & Zambra
  photograph of a Handel Festival, c.1899) show the same front,
  from different distances and decades: four round pipe towers,
  three flats between/beside them, a pediment cluster of short
  pipes over the centre flat, a cartouche impost band, and a
  panelled base with oval medallions around a central console
  recess. The form was stable for the whole festival era.
- **0032** (engraving captioned "A SKETCH AT THE HANDEL FESTIVAL
  IN THE CRYSTAL PALACE") checks the festival configuration —
  massed orchestra/choir banks before the organ — though the
  organ itself is out of frame.
- A **dimensioned contemporary source** exists: *The Engineer*,
  2 June 1882, gives the instrument's footprint in print
  (40 ft wide) and a full section plate (p.400).

## What it is

The pipe front / case front ONLY, as the plan specifies: a
12.19 m-wide decorated screen of gilded front pipes in four
towers and five flats over a panelled wooden case, with the
central console recess left empty. **No console, keyboards,
mechanism, interior pipework or blowing apparatus is modelled**
— the detached console visible in the photographs is a separate
object and is deliberately excluded; the recess reads as the
dark opening it stood in front of. Scene builders dress the
platform, choir and orchestra in front of it (lead 0032). The
recess itself is represented by a near-black inset panel in the
base front — the dark void the console stood against — not by a
modelled cavity or any part of the console.

Origin at the base centre of the footprint, ground z = 0.
Units: metres. Blender 4.5.3.

## Dimensions — evidence status

| Dimension | Value | Status |
|---|---|---|
| Overall width | **12.19 m (40 ft)** | PRINTED — *The Engineer* 1882: platform "40 ft wide", "space occupied by the instrument is 40 ft wide by 24 ft deep" |
| Overall height | **8.15 m** (±10%) | MEASURED ratio from 0595 (visual grounding: front height/width = 0.668) applied to the printed width |
| Tower positions | centres ±1.90 m, ±4.35 m | MEASURED fractions of the front width in 0595, symmetrised |
| Tower drum Ø | 1.26 m | MEASURED ratio in 0595 |
| Zone heights | base 2.55 m; impost band 0.60 m; pipe sill 3.15 m; tower tops 7.80 m | MEASURED fractions of the photographed front |
| Depth (footprint) | 1.62 m | **NOMINAL** — front-module depth only. The instrument itself occupied 24 ft (7.32 m) of depth; that depth, and everything behind the front pipes, is NOT modelled |
| Largest real pipe | 32 ft wooden (pedal) | PRINTED (*Engineer*) — internal, not part of the front; recorded here so nobody "corrects" the front pipes to 32 ft |

## Pipe counts — as drawn vs modelled

Counts read from 0595 (front rank only; towers are semicircular
clusters, so a tower's full rank is more than its visible front
arc):

| Field | As drawn (visible) | Modelled |
|---|---|---|
| Each tower | ~7 across the front arc | 7 |
| Intermediate flats | ~9–11 | 9 each |
| Centre flat | ~19–21 | 19 |
| Side bays | ~7 | 7 each |
| Pediment cluster | ~11 | 11 |
| **Total front pipes** | **~110** | **110** |

## Modelled as seen

- Four towers with cornice rings and the small crenellated
  blocks that crown them in both photographs.
- Centre flat pipe tops in a shallow inverted V, and the
  triangular pediment cluster of short pipes above it (0595).
- Impost band with horizontal oval cartouches over each bay;
  the centre cartouche is a plain plaque — in 0595 it appears
  to carry lettering (plausibly "HANDEL") that cannot be read
  reliably, so no lettering is modelled.
- Base: six tall panels with raised oval medallions (the
  photographs' medallions carry figural ornament; modelled as
  plain gilt ovals — simplification, flagged), slim panels
  flanking the console recess, canopy slab over the recess.
- Dark mouth slots on every front pipe at the photographed
  mouth height; horizontal mouth rails across the flats.

## Inferred / simplified (flagged honestly)

- **Pipe decoration bands:** in both photographs the tower
  pipes carry dark patterned (diapered) bands at roughly 55%
  and 80% of their length. The bands are modelled as plain
  dark gilt-bronze rings at those positions; the diaper
  *pattern itself* is not recoverable from monochrome
  photographs and is not invented.
- **Gilding:** front pipes are modelled gilt (bright metallic
  gold). In the photographs they read light against the dark
  case with dark bands; gilding is the documented finish for
  this front's decorated pipes, but the exact tone is a
  rendering choice, not a measurement.
- **Case colour:** dark wood, from the photographs' tonal read.
- **Heights of individual flat pipes** follow the photographed
  top lines (arch / inverted-V) as smooth profiles; individual
  pipe lengths were not counted pipe-by-pipe beyond the centre
  flat's profile.
- The 1882 rebuild (82 stops, 4,394 pipes, carillon) changed
  the interior; the front photographed before (0057) and after
  (0595) is the same arrangement, so the model represents the
  festival-era front c.1857–1926 without distinguishing rebuild
  states.

## QC

- Objects: 332. Triangles: **9,856** (limit 50,000).
- World bounding box: x −6.095…+6.095 (12.19 m), y −0.845…+0.770
  (1.62 m), z 0…8.150 (8.15 m). All object scales 1.0 (applied);
  origin at base centre.
- Renders checked against 0595: four-tower rhythm, centre
  pediment, cartouche band and medallion base all read in the
  front view; the side view confirms this is a front module —
  do not place it where its shallow back is a featured surface
  without set dressing behind it.
