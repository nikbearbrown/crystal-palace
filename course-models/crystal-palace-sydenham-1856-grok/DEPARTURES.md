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
- MISS (after finals): CAM_compare_0007 is still too low/level — the photo looks down over the terraces and Grand Fountain; ours shows flat lawn. Park paths/flower beds absent. The CT central stair and stair cheeks are plain blocks (no flights/landings articulation). In the straight CT view the stepped tiers read only as horizontal bands (correct frontally, but the front still looks boxy).

## r07 — shell polish (built with SY_NO_COURTS=1, so no court voids)
| Departure / guess | Where | Grade | Note |
|---|---|---|---|
| Vault: dense lattice ribs + deep arched rib bands, hood 8 ft deep at the vault end (no flat glazed slab) | SY_central_transept | R/I | band presence R (0074); rib count/depth I |
| Tower bracing: X-braces in the braced stacks flanking the vault, every tier; extra `transverse_bracing_72ft` object (hideable) | frame | R/I | presence R (section 0212); frequency I |
| Brunel water towers: 8-sided, tiered storeys, open lantern top | SY_water_towers | R/I | form R (0074 distant tower); storey count, taper I. Note 0007 shows a thicker, more cylindrical body — MISS (proportions) |
| Grass banks 40 ft deep between terraces (slopes, not walls), kerb, stepped stair cheeks with pedestals + urns | SY_terraces_* | I | bank depth/angle I; 0074 shows banks |
| Ground under palace: `gz(y)` falls from -1.5 ft (Parade side y=156) to basement level -23.58 ft by y=-84; brick basement piers on the grid where ground drops >2.5 ft | ground_under_palace, basement_piers | R/I | slope R (0212 shows the hill); profile linear I; pier form I |
| Main floor 1.5 ft deep, built per 24 ft bay so the cut shows it | main_floor | I | |
| Section camera moved to x=-300 (slice -306..-294) | scripts/section_render.py | — | method |
| Ornate basins: lobed rim + steps + coping + bead, two-tier centre fountain, main jet + 8 rim jets, 4 urns (S r45 jet 26; R r20 jet 25; H r77 12 lobes jet 60) | SY56_park_fountains_cascades__dated | R pos / I form | basin outlines from 1857 map (R); lobing, tazza, urns I; jet heights U |
| Jets as soft transmissive cones (`fountain_jet_spray`) | same | I | stand-ins for water; hide for SY54 |
| Park paths, rings, rosette gardens, serpentine perimeter walks, parterre borders, flower beds digitised from the 1857 map (`SY56_park_paths_beds__dated`) | park | R/I | layout R (map registration 4.28 ft/px); widths and bed planting I; bed dates U |
| CAM_compare_0007 re-solved: eye at lower terrace +30 ft, looking down to the H basin; tower ≈-21°, transept ≈+8° | cameras | I | photo was likely taken from a raised point (U) |

## Self-review r07
- Better: vault end now reads as a ribbed arch, not a slab; braced stacks and slope/basement in the section match 0212 closely; basins and paths give the 0074/0007 foreground its structure.
- MISS: in 0007 the model camera still sits a little low and right; the photo's foreground is the terrace balustrade/steps — ours is the H basin. Tower body too slender/spire-like vs 0007.
- MISS: jets read as white cones; beds are flat discs (no planting height); the terrace balustrade in 0074 is heavier.
- MISS: CT vault in 0074 is more transparent and warmer; our glazing still reads blue-white.

## r08 — Egyptian (0226) and Alhambra (0246) courts, scripts/courts.py
REVIEW.md checks: #3 (a publication year is not the depicted year) — 0226/0246 are taken from the 1856 Guide, so the courts are dated "as in the 1856 Guide" (collections `SY56_court_*__dated`), not "as built 1854"; #6 (Sydenham is not one frozen state) — courts are separate dated collections and hideable. REVIEW.md has no court-specific corrections.
| Departure / guess | Where | Grade | Note |
|---|---|---|---|
| Court footprints and internal layout digitised from guide plans 0226 (3.875 px/ft) and 0246 (5.833 px/ft), registered to plan 0205 court positions | both court collections | R | scale bars read off the plan pages |
| Egyptian court x 180–276, y 60 (nave front) → 184; Museum/Abu Simbel annex breaks the Parade wall (wall_y split at x 180–248.4) | build.py, courts | R/I | projection beyond the wall R (0226); annex roof outside the shell I |
| Court voids: main-frame columns, X- and Y-girders and gallery floors inside x 180–276 / y 60–156 omitted | build.py `COURT_VOIDS` | **U** | the real iron columns stood inside/behind the court walls; how they were hidden is unresolved |
| Egyptian heights held ≤ 21 ft (wall top 20, cornice to ~21.5) under the 22.17 ft tier | courts | I | 0226 has no heights |
| Karnak hall: two rows of 8 papyrus-bell columns, architraves; lower façade 8 columns with Ptolemaic screen walls, centre bay open | courts | R plan / I elevation | column count R, diameters/heights I |
| Abu Simbel model: 4 seated colossi, 9 ft scale | courts | **U** | scale unresolved; massing blocks only |
| Amenoph colossi at the CT edge facing the transept; Osiride pillars as massing | courts | R pos / U form | |
| Beni Hassan tomb front with 16-sided proto-Doric shafts | courts | R pos / I form | |
| Nave-front doorways x 219.7–223.5, 238.6–242.4, 257.5–261.5 (≈4 ft) | courts | R | widths read off 0226 |
| Egyptian colour: blue/red/yellow/green banding on sandstone (dado red, frieze bands, papyrus capitals striped) | Egyptian materials | I | Owen Jones/Bonomi scheme documented in general; band layout I, hues U |
| Alhambra placed x 492–564 (3 ft shift from 0205 read so end walls take the transept columns) | courts | I | |
| Alhambra reduced scale: columns 9 ft, springing 11 ft, crown 14.5 ft, wall 24 ft | courts | I | Sydenham court known as reduced reproduction; numbers I |
| Court of Lions 12×7 colonnade, cusped stilted arcades, 4 planted beds, cross paths, Lions fountain (12 lions, 12-sided bowl) | courts | R plan / I elevation | 0108 engraving R for arch + fountain arrangement |
| Abencerrages fountain, Divans 8-column ring, Cast Room partition | courts | R plan | Divans dome NOT modelled (MISS) |
| Alhambra colour: Owen Jones blue/red/gold diaper on stucco, zellige checker dado, gilt capitals | Alhambra materials | I | Jones' scheme documented (external), patterns procedural (not his drawings): **colour placement I, motifs U** |
| Muqarnas (stalactite) arches and ceilings replaced by cusped arch outlines | courts | — | MISS (0108 shows deep muqarnas) |
| CP038 / CP041 cameras: 28 mm, 1.6 m eye, 6 m (19.7 ft) push-in over frames 1–120 + hold; CP041 50 mm spandrel insert; CAM_compare_0108_alhambra portrait (RES=1080x1371) | cameras | I | storyboard paths I |
