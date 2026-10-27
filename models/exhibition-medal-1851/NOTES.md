# Great Exhibition medal, 1851 — build notes

The white-metal souvenir medal struck for the Great Exhibition: the
Crystal Palace on one face, the building's vital statistics in sixteen
lines of lettering on the other. Candidate #36 in `../CANDIDATES.md`.
A detail-insert prop — the storyboard's CP025 (the Koh-i-Noor / luxury
displays scene) is where a 39 mm object earns a close camera.

## Sources

Copies in `refs/`; originals in the repo:

| Source | Licence |
|---|---|
| Obverse photograph — `references/muse-drive/images/main-article/1851_Medal_Crystal_Palace_World_Expo_London,_obverse.jpg` | CC BY-SA 3.0 (per `references/muse-drive/data/manifest.csv`) |
| Reverse photograph — `references/muse-drive/images/main-article/1851_Medal_Crystal_Palace_World_Expo_London,_reverse.jpg` | CC BY-SA 3.0 |

**Share-alike:** both photographs are CC BY-SA 3.0, and this model's
relief is derived from them, so the model should be treated as a
derivative work under the same share-alike terms — keep the attribution
and the licence with it wherever it travels.

The manifest entry is also the dimension source: *"White metal,
d. = 39 mm"* — the object's own catalogue description, not an estimate.

**Documented sibling, not built:** the 1854 Crystal Palace medallion
(`references/muse-drive/images/commons/1854-CrystalPalaceMedallion.jpg`,
CC BY-SA 3.0) shows both faces of the Sydenham medal. It is a separate
object for a separate state; it is recorded here so nobody mistakes it
for this one.

## Dimensions and where they came from

- **Diameter 39.0 mm — documented** (manifest, above). Modelled exactly.
- **Overall thickness 3.10 mm — inferred.** No edge photograph exists in
  the collection. The thickness is a period-typical struck-medal figure
  chosen to match the chunky raised rim the face photographs show: a
  2.10 mm field thickness with the rim crests standing 0.50 mm proud of
  each field. Treat the third digit as decoration; the honest statement
  is "about 3 mm, unverified".
- Relief height above the field: up to ~0.31 mm (obverse legend),
  ~0.19 mm (reverse lettering) — scaled to read like the photographs,
  not measured from the object.

## What the faces carry (all read off the photographs at 2× zoom)

**Obverse.** Curved legend in two arcs — "THE BUILDING AT LONDON, FOR
THE" / "INTERNATIONAL EXHIBITION" — over "1851". Below, the building in
low relief: the long glazed nave with its floor bands and glazing
divisions, the barrel-vaulted transept with its little flag, the great
tree at the right end, and a speckled ground strip with tiny figures.
An exergue band carries the signatures the die itself carries:
"J. PAXTON ESQ. ARCHT." (left) and "ALLEN & MOORE F." (right — the
Birmingham makers). In the bottom segment, two winged putti flank a
crowned oval medallion with the conjoined busts of Victoria and Albert;
the left putto holds a palm frond, the right a caduceus, with a floral
cluster beside the crown.

**Reverse.** Sixteen lines, transcribed exactly as struck, including
the die's own claims and its own error ("cubic" for area):

> THE MATERIALS ARE / IRON AND GLASS, / IN SHAPE / A PARALLELOGRAM, /
> 1848 FT LONG BY 408 FT BROAD, / AND 66 FT HIGH; / IT IS CROSSED
> MIDWAY BY / A TRANSEPT 108 FT HIGH, / ON THE NORTH SIDE IS AN /
> ADDITIONAL 936 FT IN LENGTH / BY 48 FT IN BREADTH; / TOTAL AREA OF
> SPACE / 855,560 CUBIC FT; / OR NEARLY 21 ACRES; / ESTIMATED VALUE /
> £150,000.

These are the medal's 1851 publicity figures, reproduced because they
are what the object says — not endorsed as measurements (the storyboard
flags the transept heights as contested; see the 1856-guide review).

## Measured / seen versus guessed

**Seen in the photographs and followed:** the 39 mm diameter (via the
manifest); both designs in full — every word of both faces, the
building's composition (nave, transept position, tree at the right,
ground strip, exergue band and signatures), the putti/medallion/crown
arrangement, and the bold raised rim with a rounded crest on each face.

**Guessed / inferred, flagged as such:**

- **Thickness and rim profile** — no edge view exists; ~3 mm and the
  rim section are period-typical inference (above).
- **Edge treatment** — plain and slightly rounded, inferred from the
  rim's appearance at the faces' edges; no reeding is visible, so none
  is modelled.
- **Die alignment** — both faces are modelled upright relative to each
  other (medallic alignment). The photographs do not establish the
  original's alignment.
- **The pictorial relief is an interpretation, not a tracing.** The
  heightmaps (`scripts/make_heightmaps.py`) redraw the photographs'
  masses — building, tree, figures — as simplified shapes; the putti in
  particular are schematic masses with suggested wings and attributes,
  not sculpted figures. Fine die detail (the busts' features, foliage,
  the crowd) is below what the model attempts.
- **Letterforms** are a modern serif (DejaVu Serif Bold, condensed
  ~20% to match the die's narrow punches), not a facsimile of the
  original letter punches. The die's small raised "T" in "FT" is
  rendered as ordinary "FT".
- **Material** — white metal rendered as a pale, softly polished metal;
  the exact alloy and finish of the original are not recorded in the
  collection.

## Build

- One mesh, 39,168 triangles: two polar grids (192 sectors) displaced
  from the drawn heightmaps, joined by the edge band; bump maps from
  the same heightmaps carry the micro-detail (lettering strokes) the
  grid cannot. Origin at base centre (the disc stands on its rim,
  centre 19.5 mm up); real-world scale; scale applied.
- `scripts/build_exhibition_medal.py` rebuilds everything (it runs
  `scripts/make_heightmaps.py` output from `work/`); the saved .blend
  includes the grey studio rig used for `renders/`.
