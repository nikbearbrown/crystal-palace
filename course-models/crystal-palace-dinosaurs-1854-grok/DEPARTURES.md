# DEPARTURES — Crystal Palace dinosaurs, 1854 (grok)

Grades: **B** = built from a measured plan or drawing; **R** = from a published reference figure (cited); **I** = inferred from photographs/prints, by proportion or by analogy; **U** = unknown, placeholder for a guess.

Units in the scripts are feet. Coordinates: +X runs east along the lake, +Y is north, Z is up, and water level is 0.

| # | Item | Model | Source / reasoning | Grade |
|---|------|-------|--------------------|-------|
| 1 | Iguanodon statue size | 35.8 ft L × 8.8 ft above ground | cpdinosaurs.org: statue c. 10 m long and 2.7 m high. D-check passes within ±10 % / ±1 ft | R |
| 2 | Megalosaurus statue size | 34.8 ft L × 10.8 ft | Historic England / cpdinosaurs: c. 10 m × 3.5 m. D-check passes | R |
| 3 | Iguanodon form (quadruped, nose horn, low dorsal frill) | sculpted | Surviving statues (photos). Owen/Mantell placed the thumb spike on the nose (Wikipedia, McCarthy & Gilbert 1994) | I (form) / R (horn) |
| 4 | Recumbent second Iguanodon | 7.0 ft high | Surviving statue photos | I |
| 5 | Megalosaurus open jaw, quadruped | sculpted | Owen's 1854 quadruped interpretation (Wikipedia). Jaw gape and tooth count are I | I |
| 6 | Hylaeosaurus size (24.4 ft / 7.4 m) and dorsal spine row | sculpted | Wikipedia notes the iguana-like form with spines along the back. Size is by eye from photos | I |
| 7 | Ichthyosaurs: 3, basking at the waterline, sclerotic rings | 3 | cpdinosaurs.org: "three models basking on either side of a small island". Wikipedia confirms the exposed scleral rings | R (count) / I (poses) |
| 8 | Plesiosaurs: 3, two with flexible necks | 3 | cpdinosaurs.org: three species. Wikipedia: "two of them have implausibly-flexible necks" | R (count) / I (poses) |
| 9 | Megatherium clasping a tree, upright, short tapir-like trunk | 14.3 ft | Wikipedia (the model hugged a live tree and had a tapir-like snout). Height is I | R (pose) / I (size) |
| 10 | Irish elk group: 2 stags, 1 standing doe, 1 reclining doe | 4 | Wikipedia: "Hawkins built four Megaloceros sculptures, two male and two female". cpdinosaurs.org: reclining doe. The "fawn" is a misidentified Anoplotherium, so it is **not** modelled | R |
| 11 | Elk antler span 12.3 ft (3.7 m) | | Real Megaloceros spans reach about 3.5–3.6 m (cpdinosaurs) | I |
| 12 | Omitted 1854 figures: Labyrinthodons, Dicynodons, Pterodactyls, Mosasaurus, Teleosaurus, Palaeotherium, Anoplotherium, etc. | not built | Scope is limited to the brief's species list | U (omission) |
| 13 | Lake shape and island layout (lake 880 × 236 ft ellipse; secondary island 380 × 164 ft; tertiary island 200 × 132 ft) | heightfield | Shaped by eye from the modern park layout and the 1854 guide plan. No measured survey was used | I |
| 14 | Statue positions and headings | | Arranged from the arrangement visible in modern photos | I |
| 15 | 1854 paint colours (Iguanodon olive-grey, Megalosaurus brown, etc.) | | No surviving colour record was consulted. Hand-coloured prints vary | U |
| 16 | Planting (trees, rocks), fence | generic | Placeholders | I |
| 17 | Geological strata cliff (box layers at x ≈ 455) | simplified | The real strata illustration (coal measures, limestone, etc.) is only blocked out here | I |
| 18 | CP043b/c cameras stand in a boat on the lake (eye 1.6 m above water) | | The banks are too far away for a 50 mm detail. Boating on the lake is plausible but not verified for 1854 | I |
| 19 | Hawkins' Sydenham studio shed (king-post trusses, scaffold, clay Iguanodon) | | ILN 1853 print (PD, `refs/`) gives the arrangement. Dimensions are by eye | I |
| 20 | Dinner in the Iguanodon, 31 Dec 1853: open mould on a raised deck, striped marquee, name boards, chandelier, 21 guests, Owen at the head | | ILN 7 Jan 1854 woodcut (PD, Commons "Crystal palace iguanodon.jpg"). 21 diners (Wikipedia/period accounts); Owen seated in the head (accounts) | R (event, guest count) / I (layout) |
| 21 | Dinner lit as daylight | | The real dinner was an evening event under gaslight. The daylight sun is left on for legibility, with a warm marquee glow added | I/U |
| 22 | Raised press gallery for the CP034b camera | 12 ft | Needed to reproduce the print's raised viewpoint while keeping the 1.6 m eye height above a floor | I |
| 23 | Mould cut height (upper half removed above 6.0 ft local), boarded inner floor, table at the rim | | The print shows diners at the rim level. Construction details are I | I |
| 24 | Studio/dinner sets placed off-site (x = 2000 / 3000) on a grass yard | | Separate dated collections per the rules; not geographic | I |
| 25 | Figures (workmen, guests): metaball stand-ins after the HP executor's `figures.py` approach (read-only reference, credited) | | Generic 1850s dress | I |

## r02 quality (2026-10-27)
- D-DN-22 U/I: brighter Hawkins cement paints + stronger scale bump (hand-coloured prints / 2002 restoration notes)
- D-DN-23 I: CP043b reframed from S-bank walk (was boat-level; bank filled lower third)
- D-DN-24 R: New Year dinner evening gas/oil lamps (warm POINT); guests top-hatted for silhouette

## r02b (2026-10-27)
- Dinner evening override in hero render (world 0.015, sun 0.02); marquee/chandelier glow already in build.
- CP043b further back/higher from S-bank (build.py).

## set_v18 CP043 lake islands (2026-10-27)

- **D-DINO-01 I** CP043 grass/rock/bank/foliage + Hawkins paint mats rebuilt with high-contrast object-space noise + bump; lake water transmission/roughness tightened for sharper reflections. `KEEP_LIGHTING` (exposure −1.4). Hero `renders/r03/r03_CAM_CP043_lake_islands_35mm.png` from `rounds/dinosaurs-1854-r03b.blend`. KEEP by eye vs r01 flat turf / soft water.

## Queued next (after dinosaurs hero keep calls) — muse-round2 refs

- **S67** (muse-round2): ILN ruins of the 1866–67 north transept fire +
  fire-extent plan dated 12 Jan 1867 → set rounds for **CP047** and **CP048**.
- **S87** (muse-round2): 1895 plan + 1908 view of the High Level station
  → set rounds for **CP046** and **CP065**.
