# DEPARTURES — Sydenham Crystal Palace, state SY-EARLY (c.1856)
Grades: B = book (1856 Guide text/figures), R = repo research (registered plan 0205 / section 0212 / park map 0591), I = inference, U = unresolved.
Axes: +X north, -X south (railway end); +Y west/Parade front, -Y east/garden front; z=0 main floor. Units ft (F=0.3048 m).

## Scale / registration (R)
- Plan 0205 (5669x2763 px, De la Motte, no scale bar): end walls x=477/5119 px = 1,608 ft (B) -> 2.887 px/ft; centre x=2798, nave CL y=735. Grid autocorrelation 66-70 px ≈ 24 ft confirms. Scripts: scripts/plan_lines.py, plan_period.py, plan_crop.py; params in scripts/params.py.
- Section 0212 ≈4.33 px/ft: tiers 22/42/62.6 ft; bands W->garden 24,24,48,24,72(nave),24,48,48 = 312 ft (B general width). Nave centred.
- Park map 0591 ≈5.19 ft/px: upper terrace ~100 ft, lower terrace ~300 ft deep.

## Departures / guesses
| Item | Model | Grade | Note |
|---|---|---|---|
| Length 1608, general width 312, greatest width 384 | exact | B | p.35 |
| Nave crown 110'3", CT crown 174'3", basement 23'7" | exact | B | p.35 |
| Nave vault semicircular, span 72, spring 74.25 | | I | section shape reads semicircular |
| Central transept span 120 ft | 120 | U | plan inner column lines read 104 ft; 16 ft diff ≈ 8 ft advanced columns each side (p.35) — unresolved |
| CT projections 24 ft west / 48 ft garden (=384) | | I | split of the 72 ft excess is inferred from plan |
| Side transepts at ±528 ft, span 72, crown = nave | | R/I | plan lines -529/+523; crown height I |
| North transept as separate collection | SY_north_transept__lost1866 | B/R | destroyed by fire 1866 — hide for post-1866 states |
| 24 ft garden recesses at transept ends | | B | p.31; recess form I |
| Crossing towers 24 ft sq to spring+12 | | I | p.33 "low square towers"; size/height I |
| Gallery floor 22.92 ft reused from HP practice | | I | not HP geometry; only the tier number |
| Paired columns advanced 8 ft every 72 ft | | B | p.35 |
| Floor as solid boarded slab (no ½" gaps) | | I | p.35 gives boards 1.5" w/ ½" gaps — not modelled |
| West front timber dado 6 ft | | B/U | p.35 "portion panelled with wood"; extent U |
| Basement front, Paxton tunnel 24 ft | | B/I | p.34; position under bands I |
| Wings 36 ft wide, centres ±860, from y=-100 running 574 ft garden-ward | | R/B/I | width from plan 31-37 ft; heights/roof I |
| Wing roof arched, level 2nd tier; lower storey at -BD-10 | | I | |
| Railway colonnade 720 ft straight in -Y from south wing | SY54_railway_colonnade | B length / U route | dated 1854 (I) |
| Brunel water towers h=284 ft, 12-sided, at x=±(HALF+120), y=60 | SY56_water_towers__dated | U | height, plan form & position U; dated 1855-56 (U) — hide for SY54 |
| Fountain basins (4) r=34 | SY56_fountains_basins__dated | U | positions from 0591 approx; date ~1856 U |
| Upper terrace 100 ft, lower 300 ft, drop 20 ft, 10-step flight | | R/U | drop U |
| Ground slope 1:10 beyond terraces; distant flat ground | | U | |
| Nave planting tubs/trees every 72 ft | | I | placeholder for guide-described planting; positions I |
| Paint colours (grey iron) | | U | Owen Jones scheme not yet applied |
| No subway (1865) modelled | | B (state rule) | SY-EARLY must not show subway |

## Strict self-review r03 (judgment calls logged per Prof. Bear: no questions, decide and log)
- MISS (major): central transept garden projection modelled as full-height glazed side walls on free poles -> reads as a tall greenhouse standing proud. Photo 0074/0007 show the projection stepped in tiers with the great arch set into the facade. Fix next round: step the projection walls (22/42/62 ft) and bring the arch screen to the facade line.
- MISS: lower-terrace great basins / Grand Fountain layout from 0591 not modelled (only 4 small placeholder basins); terrace balustrade/statue rhythm coarse.
- MISS: basement/terrace plinth is a blank wall; real garden front shows arched basement openings and steps.
- MISS: colour scheme (Owen Jones) not applied; iron is neutral grey (U).
- MISS: nave interior lacks courts, statuary, fountains; trees are placeholder spheres (I).
- Judgment call: kept 120 ft CT span (common figure) over 104 ft plan read; logged U.

## Rounds r04–r06 (Prof. Bear steering: no questions — decide, log, iterate)
Grades: B = book/guide, R = repo research (plan/map/photo measured), I = inference, U = unresolved.

| Call | Where | Grade | Note |
|---|---|---|---|
| **BUG (major, r01–r03):** column/girder meshes were never finalised, so r01–r03 had NO main-frame columns or girders | build.py `frame` MBs | — | fixed r04 (`for _mb in frame.values(): _mb.done()`); every r01–r03 render/score is affected |
| CT garden front rebuilt as 3 stepped glazed tiers (22/42/62 ft bands, each with its own ridge-and-furrow roof); vault set into the facade, no free-standing poles | SY_central_transept | R/I | tiers R (0212, 0074); 8 ft step depth I |
| Nave + wings read as multi-tier steps (bands 156/132/108/60/36) | SY_main_* | R | section 0212 |
| Basement/upper-terrace front: round-arched arcade, stair flights at CT and wings | SY_basement_garden_front | I | arch form, bay count and stair positions I (0074/0007 read) |
| Balustrade 3.5 ft, statues on pedestals every 48 ft, ~8 ft figures | SY_terraces_* | I | scale I; positions I |
| Owen Jones colour: red/blue/yellow banded iron as toggle (`OJ_TOGGLE` value node in `iron_painted_OJ`; `scripts/set_palette.py -- 0|1 out.blend`) | materials | **U** | proportions/placement of red, blue, yellow unresolved; exterior shown pale (I) |
| Exterior iron pale stone-grey (`iron_exterior_pale`) | facade, transept & wings frames | I | r04 striped exterior read as black poles against 0074 |
| Boarded nave floor (procedural boards running E–W) | main_floor | I | board direction I |
| Nave beds/tubs x-positions from plan 0205 detection (checks/plan_nave_beds.json) | nave placeholders | R | species, heights I |
| Nave/transept statue + group/basin placeholders at 26 marks detected on plan 0205 (`scripts/plan_nave_objects.py` → checks/plan_nave_objects_filtered.json: dark blobs 3–16 ft, fill ≥0.4, deduped 8 ft); ≥8 ft marks = low basin + group block, smaller = statue | SY_nave_planting_statuary__placeholders | R pos / I form | replaced r04's regular 72 ft statue rhythm (I). FLAGGED PLACEHOLDERS |
| Crystal Fountain at the crossing withdrawn | — | U | plan 0205 shows no mark at the crossing; its 1856 location unresolved |
| Park profile `zs(y)` (terraces then 1:10 fall) | SY56_park_* | U | levels unresolved |
| Upper terrace 180 ft deep | SY_terraces | R | 1857 map scale |
| Fountain/basin positions from 1857 park map (registration mdx/mdy, 4.28 ft/px) | SY56_park_fountains_cascades__dated | R | |
| S basins r=45 ft (map ≈107 ft across) | same | R | r04 had r=34, too small |
| Basin shapes (round/oval), cascades, temples | same | I | |
| Fountains working by c.1856 | same | U | Grand Fountain system opened 1856 (U on dates/extent) — hide for SY54 |
| Park trees: 70 broadleaf placeholders, random (seed 1857), avoiding axis/basins | SY_park_trees__placeholders | I | density, species, placing all I |
| Section render: true ortho Workbench cut on column line x=−276 (slice −282..−270), garden on the right like 0212 | scripts/section_render.py | R/I | |
| Plan overlay now a plan cut (z 880–899.5 m clip) not the roof silhouette | scripts/plan_overlay.py | — | method |
| CAM_compare_0074 / CAM_compare_0007 solved from tower/transept image fractions at 35 mm; 0007 is elevated ~30 ft above lower terrace | cameras | I | |
| r05.blend kept as first built; the in-place r05 revision (placeholders + trees) became r06 with the 0007 camera re-aim | rounds/ | — | interim kept off-repo |

## Self-review r06
- Better: stepped CT front and tiered nave read against 0074; the arched basement arcade reads; section vs 0212 matches bands, vault and column rhythm; plan cut aligns with 0205.
- MISS: no diagonal tower bracing (0212's braced towers flanking the vault); vault rib thin; basement level not in the section; ground flat in section.
- MISS: placeholder statuary/fountains/trees are blocks and blobs; terrace basins plain rings (0074 shows ornate basins).
- MISS: water towers simplified (no tapered body/lantern); upper-terrace grass slopes shown as walls.
- U: Owen Jones colour placement; park levels; fountain dates; Crystal Fountain position.
