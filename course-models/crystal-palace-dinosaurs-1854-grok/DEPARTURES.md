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

## r05 CANDIDATE (dinosaurs only; trees/water = r03 KEEP)

- **D-DINO-02 I** Both park Iguanodon slots use Muse `models/iguanodon` (append-only).
  Recumbent = original sprawl pose; standing slot = mirrored re-posed copy of the same
  Muse animal (not an upright quadruped). Logged because a convincing procedural standing
  build was not achievable after r04 rejection. Credit: Muse package on main.
- CP043b reframed 50 mm / eye ~1.65 m as Muse-iguanodon hero; lake/island edge behind.
- Megalosaurus / Hylaeosaurus / plesiosaurs / ichthyosaurs: stone/sage Voronoi paint only
  (r03 meshes). Trees and `lake_water_still` untouched.
- CP043b cam: north of Muse looking south so lake/island edge is behind; 50 mm, eye ~1.85 m; shift_y −0.06 to reduce empty foreground grass. Full Muse length kept in frame.
- Muse `IguanodonHide` weathered in-cand toward stone-grey/sage (Voronoi dirt + mix); Muse mesh untouched (append-only).

## r05b KEEP / promote (2026-10-27) — CP043 + CP043b

Judge: CP043 r05 KEEP (modest gain, far figures more animal) — promote.
CP043b r05 KEEP with fixes — Muse Iguanodon reads as Hawkins sculpture; then promote.

Fixes before promote (CP043b + shared scene cleanup):
- Removed stray brown diagonal trunk/stick behind Muse head (parkland bark / prior CycadTrunk support).
- Removed floating grey hook at far-left edge (`shore_rocks_and_bases` left-edge verts; `plesiosaur_3` relocated off-frame).
- CP043b camera: NW of Muse, looking south so lake waterline / island edge reads behind the body; 50 mm; eye ~2.5 m; shift_y +0.08; full Muse in frame; less empty grass-shadow foreground.
- Trees/water (`lake_water_still`) still r03b KEEP (untouched).

Live: `rounds/dinosaurs-1854-r05.blend` (= fixed r05b-cand).
Pairs: `compare/r05b_cand/pair_CP043.jpg`, `pair_CP043b.jpg`, `pair_CP043_vs_r03.jpg`.
Renders: `renders/r05b_cand/`.

## r06 CANDIDATE CP034b dinner (2026-11-13; not live, no verdict) — D-DN-26..D-DN-33
Source: ILN 7 Jan 1854 woodcut (`refs/ILN1854_dinner_in_the_iguanodon_PD.jpg`) + period accounts. All in `DN53_iguanodon_dinner__31Dec1853` (dated 31 Dec 1853); new objects `DN53c_*`.
| # | Item | Model | Source / reasoning | Grade |
|---|------|-------|--------------------|-------|
| D-DN-26 | Marquee enclosed by boarded hoarding (back + both ends) 0-21 ft, 68 x 44 ft footprint of the existing canopy; front (camera side) left open | boards 0.72 ft, three rails | Print shows boarded walls behind the mould under the tent; height and footprint are by eye / reuse of the r01 canopy | I |
| D-DN-27 | Red/cream striped valance 21-26 ft under the canopy springing | 1.5 ft stripes | Print: striped tent cloth; colours as r01 marquee mats (U) | I/U |
| D-DN-28 | 21 diners seated inside the mould, 10 a side + Owen at the head, bare-headed, chest/head above the rim; ~1.4 ft elbow room each | seated figures | 21 diners and Owen at the head (accounts, R); bare heads and seated-in-mould view (print, R); elbow room is forced by the 10 m statue mould (statue size R, interior I) | R/I |
| D-DN-29 | Mould floor and table rebuilt inside the measured interior (per-1-ft slice), table 1.7 ft wide at the rim 10.2 ft | | Old plank poked out of the narrow neck as a floating bench (geometry bug). Table width I | I |
| D-DN-30 | Name boards lettered BUCKLAND, CUVIER, OWEN, MANTELL on the back wall at 18.2 ft (were blank at 22-24.5 ft, out of frame) | ovals 9.2 x 2.8 ft | Print shows these four names R; heights/positions I (in the print Buckland is on the left wall) | R/I |
| D-DN-31 | Chandelier lowered to 16.5 ft, 10 gas globes, warm point light 1500 W | | Print: chandelier over the table R (form I); evening gaslight D-DN-24 R | I |
| D-DN-32 | Evergreen festoons on the back wall and over the table; folding screen behind Owen's end at x +16 | | Print: garland strung over the diners and a folding screen behind the head of the table R; sizes I | I |
| D-DN-33 | Three waiters with trays on the deck (aprons) | | Print: waiters carrying dishes on the deck and stairs R; dress I | I |
Not changed: mould mesh (still the statue body cut flat at 10 ft; no head/eye, the print shows the head intact), daylight sun + marquee glow (D-21 unchanged), camera.
