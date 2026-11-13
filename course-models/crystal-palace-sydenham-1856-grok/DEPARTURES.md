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
| r08b: arcade-walk ceiling at ATOP between the Lions colonnade and pier row B | courts | I | 0108 shows a ceiled arcade |
| r08b: CAM_compare_0108_alhambra re-solved from the Hall of Justice through the central row-B arch | cameras | I | engraving viewpoint inferred |

## Self-review r08/r08b
- Better: both courts sit on their plan-0205 footprints (overlay); Egyptian hall of papyrus columns with OJ banding reads as a set at 1.6 m eye; Alhambra arcades, Lions fountain and the 0108 arch-framed view work as a composition.
- MISS: no muqarnas/stalactite work, no carved stucco relief (pattern is procedural diaper only); Divans dome missing; lions and colossi are massing blocks; cypresses are cones; Lions court shows the palace iron roof overhead (correct for Sydenham but the engraving idealises sky).
- MISS: CP038 entry frame 1 is dominated by the plain door jambs of the ~4 ft door; nave-front screen walls lack painted relief.
- U: court heights, colour placement, column treatment inside the court voids.

## r09 — Abu Simbel colossi appended from Muse (models/egyptian-court-colossi, origin/main 90e62cc)
Credit: **Muse** built the colossi (`models/egyptian-court-colossi/`, commit 90e62cc "models: add Egyptian Court colossi (Muse)"). Inspected read-only after `git fetch`; the .blend is vendored unmodified at `vendor/muse-egyptian-court-colossi/` (see CREDIT.md) and appended at build time by `scripts/courts.py` (`bpy.data.libraries.load`, link=False) into the dated collection `SY56_north_transept_colossi_muse__lost1866` (child of `SY_north_transept__lost1866`). `models/` was not edited. Muse's mesh and materials are used as delivered (286 objects + 1 root empty, units already metres, scale 1).

Soundness/dating check: stylised block build, clean, metre units, origin at the centre of the pedestal base; maker's notes date it SY-EARLY c.1856 (CP038) and cite Guide 1856 p.50 "the gigantic figures in the northern transept". Accepted. Maker flags the lead photo licence as unverified; that carries over.

| Item | Where | Grade | Note |
|---|---|---|---|
| Colossi located in the **north transept**, not inside the Egyptian Court footprint | courts.py r09 | R | Guide 1856 p.50 (per Muse notes); plan 0226 shows no colossi inside the court |
| Garden (−Y) end of the north transept, back 2 ft off the recessed end wall (y −130 ft), centred on the transept axis x 528, facing +Y toward the nave | courts.py r09 | I | which end is not fixed by my sources; the Parade half of the transept bay (x 492–564) is taken by the plan-0205-traced Alhambra Court, so only the garden end is clear |
| Figure height 20.0 m (65.6 ft), pedestal 5.9 m; overall 86.5 ft as modelled | Muse | U | Muse took the Abu Simbel originals' height; the Sydenham casts' true height not checked by me against a period source |
| Fit under the vault: overall 86.5 ft at ±29 ft off-axis vs vault intrados 95.6 ft there (spring 74.25 + √(36²−29²)) | check | — | ~9 ft clearance; width 58 ft inside the 72 ft span |
| Sandstone colouring (Muse) kept; no Owen Jones polychromy added | Muse | U | period colouring of the casts not researched |

**Dimension comparison with plan 0226 (Egyptian Court):** modelled court is x 180–276 (96 ft) by y 60–184 (124 ft incl. annex), with heights held ≤ 21.5 ft under the 22.17 ft tier. Muse's pair is 58 ft wide × 34.6 ft deep × 86.5 ft high — 60% of the court's width, 4× its permitted height; it cannot stand inside 0226 under the aisle tiers, and 0226 draws nothing of that size. 0226's "Model of the Abo Simbel Tomb" (plan 0205 item 12A) is therefore kept as my small 9 ft annex model (U), and the full-size colossi go where the Guide puts them: the full-height north transept. Both lost together with the north transept in the 1866 fire, hence the `__lost1866` suffix.

## r10 — Alhambra / Egyptian detail pass (judged against engraving 0108)
| Item | Where | Grade | Note |
|---|---|---|---|
| Polka-dot diaper replaced by procedural 8-point star / interlace relief (shader bump in `ornament.py`, not true displacement) | al_relief_mat | I / U | motifs are generic Nasrid-type geometry, not traced from Jones' plates (U); bump not displacement, so silhouettes stay flat (I) |
| Stilted cusped arches with soffit muqarnas tiers + alfiz frame | `arch_screen` | I | 0108 R for the stilted/cusped form; muqarnas depth and tier count I |
| Slender paired marble columns (paired at the colonnade corners and the central bays), ring-annulet shafts, cubic capitals | Lions colonnade | I | pairing rhythm read from 0108 only at the visible bays; the rest I |
| Arcade ceiling (ATOP) at 19.5 ft | courts | I | |
| Zellige tile dado, ivory mouldings; colour muted toward 0108's tonal values (OJ hues kept but desaturated) | materials | I | |
| Lion fountain: 12 lions with blob-built bodies, 12-sided basin + upper bowl | courts | R arrangement / I form | |
| Hanging planting over the arcade cornice | courts | I | 0108 shows creepers; species/extent U |
| r10b fix: spandrel faces tessellated as one outline per side (the r08 vertical strips backtracked along the cusped profile → coplanar flipped faces → black slits) | `arch_screen` | — | geometry fix only |
| Egyptian: lotus-bud / open-papyrus capitals, relief bands with generic hieroglyph and figure registers (bump), warmer sandstone + OJ polychromy | Egyptian court | I / U | capital types per 0226 hall I; glyph content generic U |
| Colossi camera: target raised / fl kept at 35 mm so heads and crowns clear the frame | cameras | I | |
| Egyptian entry frame 1 moved back to frame through the lotus portal, not the plain jambs | cameras | I | |
| Muqarnas *domes* (Hall of Two Sisters / Divans) still not modelled | — | MISS | |

## SY-POST66 (c.1868) — toggle `SY_STATE=POST66`, collection `SY-POST66_c1868`
Evidence: north-transept fire 30 Dec 1866. Crystal Palace Park Trust: the north nave was rebuilt over ~2 years, **the north transept never rebuilt**; 1928 aerial (Historic England EPW021373, scratch-viewed, licence – not committed) shows a continuous nave running to an arched north end with no transept; crystal.dircon notes the colossi survived the fire but were not re-erected in the transept; Historic England blog: the Alhambra Court was restored after the fire. No post-fire elevation drawing found.
| Item | Grade | Note |
|---|---|---|
| North transept (x 492–564) removed; that bay infilled with standard nave bays | R removal / I infill identical to standard bays | aerial shows a continuous ridge, bay detail not legible |
| North end wall + lunette gable kept as in 1856 | I / R | aerial shows an arched end; detail I |
| North wing length shortened to 240 ft | U | not measured from a source |
| Colossi removed | I | they survived the fire; later fate U |
| North garden stairs removed with the transept | I | |
| Alhambra kept (restored); its wall lowered to 21.4 ft to sit under the aisle roof now the transept vault is gone; transept-floor void kept for the court | I | |
| CP047 (north end from the upper terrace, 35 mm) and CP048 (terrace walk 7 m + hold, 35 mm) — identical camera objects in both states for the matched before/after pair | cameras | I | storyboard viewpoints I |

## r11 — later states from one script: `SY_STATE=1936 | FIRE | AFTER | RUINS | RUINS41` (`scripts/states.py`, exec'd at the end of `build.py`)
Root collections: `SY-1936_Nov1936_preFire`, `SY-1936FIRE_30Nov1936_night`, `SY-1936AFTER_Dec1936_morning`, `SY-RUINS_c1937-40`, `SY-RUINS_post1941`. All later states start from the POST66 build (no north transept, R), so 1866 losses carry through.
Sources used: Wikipedia "The Crystal Palace" (fire 30 Nov 1936; towers survived; "a section of the north end of the main nave" left standing; site cleared); London Fire Brigade history page (start near the centre, high wind, timber floors, iron frame buckled/collapsed in sequence); Historic England listing text as quoted by Inside Croydon (fountains long out of use; Baird's TV mast on the South Tower from 1933; South Tower taken down autumn 1940); ADS/Archaeology Data Service grey-lit (South Tower "end of 1941"); Crystal Palace Park Trust (six sphinxes in pairs at the heads of three granite flights; repainted red 2016 "as they had been until the end of the 19th century"); ArtUK SE19_JK_S106 (sphinx H 180 × D 480 cm, 1854); refs in `references/muse-drive/images/`: 0592 fire photograph, 0587/0588 aerials "destroyed 1936", CPsphinxsteps02, CPupperterraces01-04 (the surviving arcaded basement wall).

| Item | State(s) | Grade | Note |
|---|---|---|---|
| Six sphinxes, in pairs at the heads of three flights between the terraces | all | R count/arrangement | Park Trust |
| Sphinx size 15.8 × 5.9 ft body on a 7.6 × 18.8 × 3 ft plinth | all | R body (ArtUK 480 × 180 cm) / I plinth | check PASS 15.80 vs 15.75 ft |
| Sphinx form (Tanis type, built from ellipsoids + nemes boxes) | all | I | procedural; not traced from photos |
| Sphinxes face the garden (−Y) | all | I | |
| Sphinx colour: terracotta red to c.1900, weathered grey concrete in 1936+ | EARLY/POST66 vs later | R red early (Park Trust) / I weathered colour | |
| Side flights at the side-transept axes x = ±528, 28 ft wide, 10 steps, cheek walls; upper balustrade opened there | all | I | positions of the outer two "great steps" not measured; on axis by analogy with the central flight |
| Fountains dry, jets removed, basins dry silt | 1936+ | R out of use / I which basins and their state | the football ground / motor-racing use of the basin area is NOT modelled (MISS) |
| Courts and interiors kept as in POST66 | 1936/FIRE | I | 1936 interior state (exhibitions, organ, etc.) not researched (MISS) |
| Baird lattice mast on the South Tower lantern, 50 ft | 1936/FIRE/AFTER | R existence / U form and height | |
| FIRE: whole central transept (shell + vault) removed and replaced by a collapse pile (≈520 twisted members, 35 % glowing) + 7 falling ribs | FIRE | R collapse / I pile form and timing | storyboard beat CP061 |
| FIRE: flames as emissive blackbody volumes (≈490 cones), strongest around the centre and south nave, spreading north | FIRE | R that it spread from near the centre in high wind / I-U distribution at this instant | |
| FIRE: smoke column as 19 noise-masked volume puffs leaning north-east, low orange underglow | FIRE | I form / U wind direction | |
| FIRE: night sky, faint moonlight | FIRE | R night (fire c.20:00–) / U moon | |
| Fire appliances, crowds, hoses, searchlights | FIRE/AFTER | MISS | |
| AFTER: shell gone; ≈2600 kinked/twisted members + ≈170 column stumps over the footprint; scorched ground plane | AFTER | R wreck field (0587/0588) / I density and heights | |
| AFTER: north-end standing fragment (4 bays of frame to the tier heights, part of the end rib) | AFTER | R that a north-end section stood / I extent | |
| AFTER: basement garden-front arcade, garden stairs, terraces, railway colonnade, both towers standing | AFTER | R wall/towers (photos, Wikipedia) / U colonnade condition | |
| AFTER: December morning, low east sun, smoke haze, thin smouldering volumes | AFTER | I | |
| RUINS: wreckage cleared (Thos. W. Ward), plateau rubble/grass, column footing pads on the 24 ft grid (70 % kept) | RUINS/RUINS41 | R clearance / I pads and surface | |
| RUINS: basement arcade wall + stairs kept as the terrace wall | RUINS/RUINS41 | R (survives today, CPupperterraces01-04) | |
| RUINS: towers in dated sub-collections `SY-RUINS_south_water_tower__dismantled_autumn1940-1941`, `SY-RUINS_north_water_tower__demolished_16Apr1941` | RUINS | R that both went in WWII / **date conflict on the South Tower: HE autumn 1940 vs ADS end of 1941 vs Wikipedia "shortly after the fire"** — collection name carries the range | the official reason (landmark for bombers) is commonly told, U |
| RUINS41: both towers removed, brick bases kept | RUINS41 | R (south base excavated 1985) / I north base | |
| Railway colonnade kept in all later states | 1936–RUINS41 | U | its demolition date not researched |
| Storyboard cameras CP001, CP057, CP059, CP061, CP062, CP064, CP072, CP073 created in every state (identical objects → matched pairs) | all | I positions | 36 mm sensor, 1.6 m eye, no roll; 28 interior / 35 exterior / 50 detail |

### r11b polish
| Change | State | Grade | Note |
|---|---|---|---|
| FIRE flames re-done as emissive *surface* tongues: opacity = facing-ratio core × stretched world noise × per-vertex height fade (`hfac` attribute), blackbody 1150–2300 K. Replaces r11 volume cones that read as solid spikes. `SY_FLAMEVOL=1` restores r11 volumes | FIRE | I (look, not physics) | per-tongue volume objects tried and abandoned: 600 volume objects did not finish one 60 % frame in 24 min |
| Alhambra arch outlines: real-geometry "sebka" lace, 3 staggered rows of faceted lozenge studs following each arch profile on both faces (`SY_LACE`, default on) | EARLY/POST66 | I (pattern) / R that the arch outlines carried dense pierced/relief lace (0108) | stud size 0.32–0.52 × 0.2–0.3 ft, 0.12 ft proud; not a copy of any specific Owen Jones panel |
| 0108 comparison exposure raised from −1.0 to −0.3 EV (`EXPO` env in render.py, per render only) | EARLY | — | presentation only; scene file exposure unchanged |

### r12 — sphinx sculpt, charred stumps, PPL-20C 1936 dressing (`scripts/sculpt.py`, `scripts/dress36.py`)
| Change | State | Grade | Note |
|---|---|---|---|
| Terrace sphinxes: metaball recumbent lion body (forepaws out, haunch, tail), nemes headdress hull with lappets, human face, on a moulded plinth. Size from the ArtUK record (H 180 × D 480 cm); D-check: head > 5 ft above the plinth | all | R size / I form (from photos of the surviving sphinxes) | face and nemes stripes are simplified; colour is the existing terracotta-ish stone paint (U) |
| AFTER column stumps: 0.8 ft charred iron with dark oxide/soot material `iron_charred_black_1936`, also on the collapsed ironwork field | AFTER | I colour / R that the wreck was blackened iron (photos) | replaces the timber-looking r11 colour |
| LFB appliances: pump-escape/pump block-outs about 25 ft long (D-check 25 ± 3 ft) and turntable ladders (TL) with extended ladders, in 1930s red, along the Parade and lower terrace. FIRE has ≥ 10 pumps and ≥ 3 TL (D-check) | FIRE/AFTER | R attendance (89 appliances, 438 firemen, LFB/Wikipedia) / I forms and positions | 15 pumps + 4 TL modelled — a representative subset of the 89 |
| Firemen figures (dark tunics, helmets), canvas hoses (2¾ in) laid across the Parade to the building, water jets | FIRE/AFTER | I | helmet colour U (brass vs. cork-black) |
| Crowds: 1930s-dress stand-ins (overcoats, hats; HP executor's `figures.py` approach, read-only, credited) on the Parade and the upper and lower terraces behind police lines; daytime visitors in the 1936 state | 1936/FIRE/AFTER | R that huge crowds watched (c. 100,000 reported) / I density and positions | |
| Police lines (constables in helmets, roped) on the Parade and the lower and upper terraces | FIRE/AFTER | I | |
| New storyboard cameras CP058 (behind the police line over the appliances, Parade) and CP060 (crowd watching), in all states | all | I positions | 36 mm, 1.6 m eye, no roll, 35 mm |

### r13 — CP045 Handel Festival 1857, Fine Arts courts II (CP039/CP040), CP042 waterworks running
New scripts: `scripts/people57.py` (Victorian-dress figure templates, GN-instanced; clear zone of 7 ft round every camera), `scripts/concert57.py` (state `SY_STATE=CONCERT57`, root `SY-CONCERT57_HandelFestival_Jun1857`), `scripts/courts2.py` (EARLY + CONCERT57), `scripts/waterworks.py` (EARLY). Muse props appended unmodified from `vendor/muse-*` (each has CREDIT.md with the origin/main commit); `models/` not edited.
| ID | Change | State | Grade | Note |
|---|---|---|---|---|
| D-R13-C1 | Great Handel Festival 15–19 June 1857 in the central transept, collection `SY57_HandelFestival_15-19Jun1857__dated` | CONCERT57 | R (date, place) | Times / Grove "Handel Festival"; the 1857 festival was the Commemoration rehearsal for 1859 |
| D-R13-C2 | Orchestra amphitheatre: 28 stepped segmental tiers (rise 1.5 ft, tread 3.4 ft) from 4.5 ft to ~46 ft, filling the north half of the transept, 216 ft wide, in stained deal with red baize risers | CONCERT57 | R that a huge raked orchestra filled one end of the transept (prints); dimensions I | ground galleries and girders cut away inside the orchestra (ORCH_VOIDS) — I |
| D-R13-C3 | Orchestra on the **north** side facing south | CONCERT57 | I | prints conflict with a Trove report placing the royal box opposite; chosen so the royal box sits on the south gallery across the transept |
| D-R13-C4 | Great organ (Gray & Davison, 1857) at the top/back of the orchestra: four pipe towers, three flats, gilt pipes, swell box, console | CONCERT57 | R existence/builder; form, size I | ORGAN_FRONT x 158, 54 ft wide, case base ~39 ft |
| D-R13-C5 | Performers: 2,000 chorus + 396 band = 2,396 target; model seats 2,424 (+1.2 %), band at 2.7 ft pitch on the lower 8 rows, chorus 2.05 ft; women's voices lower and at the sides | CONCERT57 | R numbers / I layout / U voice placement | D-check 2396 ± 15 % |
| D-R13-C6 | Conductor Michael Costa on a raised rostrum at the orchestra front (form only, no likeness) | CONCERT57 | R that Costa conducted / I rostrum | |
| D-R13-C7 | Audience ≈ 10,900 figures: benches on the transept floor and the south nave, standing along the gallery fronts and transept sides; royal box on the south gallery with canopy and velvet parapet | CONCERT57 | R attendance 11,000–17,000/day; I positions; U count per area | tubs/plan objects removed from the floor for the seating (I) |
| D-R13-C8 | CP045 cameras: floor aisle 28 mm (hero), two gallery-front 28 mm, organ-gallery reverse 28 mm, conductor 50 mm | CONCERT57 | I | 36 mm sensor, 1.6 m eye, no roll |
| D-R13-F1 | Pompeian Court as a house (atrium with impluvium and compluvium, tablinum, peristyle with garden and basin, cartibulum) at x −562..−494, y 62..154, walls 20 ft; Fourth-Style red/black/yellow panels with vignettes | EARLY/CONCERT57 | R type and parts (Scharf/Digby Wyatt 1854 handbook); plan size I; paint scheme I (not copied from a specific wall) | collection `SY54_court_pompeian__dated` |
| D-R13-F2 | Greek and Roman courts as a segment on the nave front at y 60: Doric front (x 288–360) with painted triglyph frieze, meander and antefixes; Roman Corinthian front (x 384–480); iron columns encased by the orders | EARLY/CONCERT57 | R that the courts fronted the nave with orders (Delamotte); intercolumniation tied to the 24 ft grid (I) | collection `SY54_court_greek_roman__dated` |
| D-R13-F3 | Muse props in the Greek/Roman courts: Three Graces, Farnese Bull, display plinths + kraters, classical cast bases | EARLY/CONCERT57 | R that these casts were shown (1854 guide); positions I | credit: Muse (vendor/*/CREDIT.md) |
| D-R13-F4 | Mediaeval Court at x 392–490, y −116..−46, walls 30 ft, encaustic tile floor; 11 Muse gothic arch bays on the nave front, 7-bay inner screen at x 456 (English vs German parts) | EARLY/CONCERT57 | R court and its subdivisions (Digby Wyatt); layout I | open to the roof: gallery cut away over the court (GAL_VOIDS13), I |
| D-R13-F5 | Rochester (cathedral west) door cast: five orders, chevron, tympanum with mandorla | EARLY/CONCERT57 | R that a cast of the Rochester doorway stood in the court; form I (simplified) | |
| D-R13-F6 | Stained glass: lancets with roundels, a rose (r 5.5 ft) and German lancets, emissive Voronoi glass with leading | EARLY/CONCERT57 | R that stained glass was shown; designs I | |
| D-R13-F7 | Tomb effigy and font in the English part | EARLY/CONCERT57 | I | |
| D-R13-F8 | Visitors in Victorian dress in all three courts | EARLY/CONCERT57 | I | |
| D-R13-W1 | Waterworks **running**, collection `SY56_waterworks_running__18Jun1856` (first full display 18 June 1856, Queen present) | EARLY | R date | static basins/towers from r05–r07 unchanged underneath |
| D-R13-W2 | Terrace basins: 64 ft centre plume with crown, falling veil (28 arcs), spray cloud, 24 rim jets arching inward, overflow foam | EARLY | R type (photo 0120: tall centre plume + ring jets); heights and counts I | |
| D-R13-W3 | Great lower basins: 200 ft centre plume each, inner ellipse of 24 plumes 55–70 ft, 40 rim jets | EARLY | period claim "up to 250 ft" R as a claim; modelled 200 ft I; counts I | |
| D-R13-W4 | H basin 120 ft plume + 32 rim jets; R fountains 40 ft + 12 | EARLY | I | |
| D-R13-W5 | Cascades running: white-water sheets over each of 16 steps, foam at the foot, three outfall spouts at each temple | EARLY | R that the cascades ran from the water temples (1857 map, prints); form I | |
| D-R13-W6 | Water as mesh (tapered columns, parabolic bar arcs, tetrahedral droplets) with a semi-opaque emissive white "spray" material | EARLY | I (look, not physics) | particles not used, so files stay small |
| D-R13-W7 | 2,420 visitors round the basins, terrace balustrades and walks | EARLY | U numbers / I positions | |
| D-R13-W8 | CP042 cameras: terrace basin 35 mm (hero), head of the centre flight 35 mm, great basins 35 mm, cascade 50 mm | EARLY | I | |

### r14 — camera/lighting/jet fixes; SY-BUILD (CP033), SY54 opening (CP035), G-STATION (CP036), SY-LATE (CP049–54), SY-WAR (CP056)
New scripts: `scripts/eras.py` (BUILD53 / OPEN54 / LATE11 / WAR dressing), `scripts/station.py` (Low Level station + covered way, exec'd from eras OPEN54). `scripts/people57.py` gains navvy / court / queen / yeoman / Edwardian / rating templates. `scripts/build.py` ROOTS + POST66 / GAL_VOIDS13 / exec wiring. `checks/dimension_check.py` state-aware for SY-BUILD / SY54 (and ROOT match for `SY54_*`).
| ID | Change | State | Grade | Note |
|---|---|---|---|---|
| D-R14-F1 | CP045 gallery cameras moved out of the braced tower stacks: (−98, ±40, GF+EYE) looking at (110, ∓12, 30) | CONCERT57 | I | braces occupy x ±60–84 central and x 468–492 north |
| D-R14-F2 | CP040 Mediaeval Court camera moved to (452, −50, EYE) looking at (398, −96, 13) | EARLY/OPEN54 | I | was blocked by a diagonal brace |
| D-R14-F3 | New CP040 cameras on the Three Graces (336, 94 → 336, 120) and Farnese Bull (424, 86 → 432, 120), 50 mm | EARLY/OPEN54 | I | Muse casts already placed in r13 |
| D-R14-F4 | Greek/Roman interior brightened: two area fills `court_fill_greekroman` (size 90×86 ft, energy 9000) over the court | EARLY/OPEN54 | I | r13 under-lit |
| D-R14-F5 | Jet-height check now measures spray-vertex max−min z above water at each great-basin centre (`great_centres_ft` custom prop), target 200 ± 20 ft | EARLY | — | was reporting jet top vs main floor |
| D-R14-B1 | Erection front c. autumn 1853: glazing complete to x=−350; frame to tier 3 to x=+150; to tier 1 to x=+450; basement only beyond; central transept kept whole; north wing not begun; south wing frame kept | BUILD53 | U | no single dated elevation of the rising frame; Paxton park works 1852–54 R |
| D-R14-B2 | Ground recoloured raw clay; meadow for y < −1300; terraces stone clipped for x > 40 | BUILD53 | I | |
| D-R14-B3 | Earth wedges with cut faces, 22 spoil heaps, 3 tramways (sleepers/rails/tip wagons), horses and carts | BUILD53 | I | tramways typical of the works; route I |
| D-R14-B4 | Timber scaffolding round the transept (x ±72/96), shear-legs, column/girder stacks, huts; 737+ navvies/erectors | BUILD53 | I form / U numbers | workforce claim ~6,400 R(claim); modelled subset |
| D-R14-B5 | CP033 cameras: slope-up 35 mm, terrace-cut 35 mm, frame-rising 35 mm, transept-ribs 28 mm | BUILD53 | I | |
| D-R14-O1 | Dais + throne + canopy at x −46..−14 facing **north** to the choir stand (x 70..172); crimson cloth and gilt | OPEN54 | U orientation | ILN 17 Jun 1854 shows a dais in the transept; facing chosen so the procession approaches from the south nave |
| D-R14-O2 | Opening-day figures: ~6,080 inside (royal party, yeomen, procession, nave lining, stands, choir/band, galleries) + 1,796 terrace; ~40,000 present R(press) | OPEN54 | R attendance / I–U density | modelled subset |
| D-R14-O3 | Roof flags of many nations along the nave + Royal-Standard-ish at the central-transept crown; gallery banners | OPEN54 | I | engravings show a line of flags |
| D-R14-O4 | Water towers ABSENT (built 1855–56); park fountains/cascades and terrace jets not playing | OPEN54 | R towers/fountains dates; U terrace-fountain state on the day | |
| D-R14-O5 | CP035 cameras: transept gallery 28 mm, procession nave 28 mm, dais 50 mm, garden-front flags 35 mm | OPEN54 | I | |
| D-R14-S1 | Old flat colonnade killed; glazed covered way rebuilt bay-by-bay following `gzp`, ≤ 6 ft drop/bay, steps, glass sides, pitched glass roof, brick dado; length 720 ft, drop ~65 ft | OPEN54 | I (was floating ~70 ft above the park at its south end in r01–r13) | guide 720 ft B |
| D-R14-S2 | Low Level station: shed x −1130..−650, y −1350..−1440; two glazed pitched spans; 3 platforms, 2 tracks, tank engine + 9 carriages; collection `SY54_LowLevel_station_and_covered_way__1854` | OPEN54 | R that the station opened 10 Jun 1854 / U plan and form | |
| D-R14-S3 | CP036 cameras: platform arrival 28 mm, covered way 28 mm, station exterior 35 mm; 969 arriving visitors | OPEN54 | I | |
| D-R14-L1 | Wear: transparent BSDF darkened ×0.62; 3.5 % of panes swapped to zinc-board material | LATE11/WAR | I | |
| D-R14-L2 | Festival of Empire 1911: replica pavilions Canada (−520, −1300), Australia (520, −1300), South Africa (−300, −1560), New Zealand (300, −1560); All-Red Route elliptical rail loop (r 760×300 at y −1420) with cars | LATE11 | R festival / All-Red Route existed; sites and forms I/U | 1913 national purchase not modelled (MISS) |
| D-R14-L3 | CP049 worn garden front 35 mm; CP053 festival 35 mm + pavilions wide 35 mm; Edwardian crowd ~5k | LATE11 | I | |
| D-R14-W1 | HMS Crystal Palace: White Ensign approx. (banded) on the transept + mast/yard on the terrace at (0, −250); 8 companies of 6×16 ratings on the upper terrace + nave/lower-terrace squads (1,164 figures) | WAR | R that the RND depot trained here (~125,000 men claim); formations I/U; ensign I | |
| D-R14-W2 | CP056 cameras: terrace drill 35 mm, nave drill gallery 28 mm, ranks 50 mm | WAR | I | |

## r15 — SY60 High Level/subway (CP046) + SY-CLEARANCE (CP063)

### D-R15-S* High Level station and subway (SY60, c.1865)
- **D-R15-S1 U/I** Station/subway layout: no measured High Level plans or vault surveys in the repo (BUILD-PLAN gap). Placed on the Parade (+Y) side beyond y≈200 ft: shed x=-220..220, y=300..400; booking hall y=260..300; subway under Parade y=190..268, width 18 ft, floor z=-14 ft, vault crown z=-2 ft. Parade road deck at z=+4 ft. Grades: existence of HL station (opened 1 Aug 1865, LCDR) and brick-vaulted subway under Crystal Palace Parade **R**; dimensions/placement **I/U**.
- **D-R15-S2 I** Patterned vault: cream ground with red/black geometric bands via object-space shader (Byzantine/Italianate look of the surviving subway in period/modern photos **R** existence; exact motif **U**).
- **D-R15-S3 I** Two-span glazed shed, three platforms, two roads — form parallel to Low Level stand-in; do **not** confuse with CP036 Low Level (garden/−Y side, 1854).
- **D-R15-S4 U** Passenger counts (200 modelled) and dress (Victorian people57 templates).
- **D-R15-S5 B** North transept still present (1865 is pre-30 Dec 1866 fire).

### D-R15-C* Clearance (SY-CLEARANCE, late 1930s)
- **D-R15-C1 I** Dresses the RUINS cleared-plateau state (footing pads, terraces, sphinxes, both Brunel towers still standing — towers removed 1940–41 **R**).
- **D-R15-C2 U/I** Three lattice mobile cranes, six 1930s tipper lorries, 63 scrap-gang workers, scrap piles and twisted beams — no dated clearance photo set in repo; plant/forms stand-ins.
- **D-R15-C3 I** Intact terrace edge kept as the CP063 visual anchor (storyboard).

## r15 follow-up (CP046 lighting / approach)
- **D-R15-S-LIGHT I**: subway AREA lights along vault (cream tungsten); sun alone left CP046 black underground.
- **D-R15-S-CAM I**: `CAM_CP046_hl_approach_28mm` moved to Parade looking north at booking/shed (was inside shed facing S wall).
- **D-R15-S-EXIT I**: subway exit lookat retargeted toward palace GF emergence.

## r16 quality (2026-10-27)
- D-R16-O1 R: OPEN54 densified toward ~40k via people() instancing (nave/galleries/terrace/park lawn)
- D-R16-W1 I: cascade sheets thicker + vertical spray ribbons; FOAM/WSP higher transmission/emission
- D-R16-W2 I: CAM_CP042_cascade_50mm side-on mid-cascade (was look-through to palace/pool)
- D-R16-P1 I: people57 taller top hats, broader frock coats, wider crinolines; hero ring outside 7 ft clear zone

## r16 coverage + quality (2026-10-27)
- **D-R16-C1 I** `scripts/coverage_cams.py`: EARLY CP037 taller nave cam; CP044 pay desks / guidebook stall / refreshment counter + clerks (south aisle placement U).
- **D-R16-C2 I** LATE11 CP051 electric pendant fittings + warm POINT lights + tech cabinets; CP052 scaffold towers + reglazing gang on garden-front glazing; CP054 1913 Plymouth rescue flags + terrace crowd (~2200).
- **D-R16-C3 R** OPEN54 densify: people 20983 + terrace 8118 + park 9117 (~38k toward 40k storyboard).
- **D-R16-W3 I** Cascade water materials already boosted in waterworks.py (transmission/emission); side-on CP042 cascade hero.

## r17 WEAK→OK ( 2026-10-27 04:22 UTC )
- **D-R17-C1 I** CP058 denser AFTER pumps + cam along pump line (`dress36.py`); hero `r17i_after_CAM_CP058_*`.
- **D-R17-C2 I** CP062/064 elevated cams (absolute Z) + horizon grass/haze fill (`states.py` r17q); heroes `r17q_ruins_*`.
- **D-R17-C3 I** CP063 lowered lookat among scrap + yellow crane FG (`clearance.py`); hero `r17q_clearance_*`.
- **D-R17-W1 I** Nishita hard blue band: aerosol bump + sky-matched haze card (shared look preset NOT adopted).

## People library v3.1 adopt (2026-10-27) — Sydenham crowds

Adopt `/workspace/crystal-palace-survey/people/` v3.1 into Sydenham crowd shots via `adopt_people_v31` (PPL57 templates + merged `crowd36_`/`lfb_`/`police_line_` blocks). Keep-better before/after; revert darker/emptier or broken; preserve each scene’s prior lighting/grade.

| Shot | Era dress | Verdict | Note |
|---|---|---|---|
| CP035 open54 gallery | 1850s | REVERT | after darker vs before |
| CP036 covered way | 1850s | REVERT | mesh corruption / clay |
| CP037 taller nave | 1850s | REVERT | no crowd gain; washout |
| CP044 pay desks | 1850s | KEEP | Victorian frock/top-hat; grade matched |
| CP045 concert57 | 1850s | REVERT | after much darker |
| CP049 late11 garden | 1910s→1890s stand-in | REVERT | floating heads / broken hats |
| CP051 late11 nave | 1910s→1890s stand-in | REVERT | foreground double-face glitch |
| CP054 late11 terrace | 1910s→1890s stand-in | KEEP | light 0.9–1.0 m hems, ~40% women, grade held |
| CP058 1936 parade | 1930s | KEEP | shorter coats/trilbies; mats fixed; grade held |
| CP060 1936after crowd | 1930s | KEEP | denser 1930s dress; light mid-tones; grade held |

### Dress / library departures
- **1911 (late11):** no dedicated 1910s garment set — `ERA_ROLES["1910s"]` maps to 1890s gentleman/lady (bustle + boater). Logged; CP049/051 reverted on geometry, CP054 kept with this stand-in.
- **1936:** `_build_person` lady branch now prefers `is_1930` (mid-calf coat, no crinoline) before Victorian paths; men get trousers + mid-thigh coat + trilby. Merged-block rebuild assigns materials **before** `bmesh.to_mesh` (else all faces clamp to skin/clay).
- **Crinoline hem:** reduced from ~1.2 m to **0.9–1.0 m** diameter (`hem_rx, hem_ry = 0.47, 0.42`); skirt albedos lightened to mid-tones so crowds don’t read as dark blobs (HP steering).
- **Mix:** template names already ~40% women; merged blocks use `lady` fraction **0.42**.
- **Lighting rule:** any after with mean luminance < 0.97× before, or visually darker/emptier grade, is reverted (CP035/045/050/055 among others).

Verdicts: `people_v31/verdicts_v31_crowds.json`. Previews: `people_v31/previews/CP*_v31_before_after.jpg`.

## People library v3.3 adopt (2026-10-27) — Sydenham crowds

Canonical `people_lib` PEOPLE_VERSION **3.3** under `/workspace/crystal-palace-survey/people/` (vendored into `scripts/people_lib.py`). Drop bare `FIGURE` match; exclude statues/sculptures/plinth/pedestal; never turn `CastBase_*` / `FIG_*` sandstone facade / PanelFigure into people. `--keep-lighting` preserves authored sun/world/exposure (no look override). CP058 1930s coats: darker mid-tone `_COATS_1930`, paint coats before hand-skin, thicker coat shells; `_sex_for` endswith(`_f`) so `1930s_fireman` stays male.

Honest keep-better by viewing each before/after pair (not lum alone):

| Shot | Era | Verdict | Note |
|---|---|---|---|
| CP035 open54 gallery | 1850s | KEEP | white clay placeholders → mid-tone crowd; grade held |
| CP036 covered way | 1850s | REVERT | broken multi-arm/sunk meshes; washout ~1.95× |
| CP037 taller nave | 1850s | REVERT | washout ~1.49×; no people gain in frame |
| CP045 concert gallery | 1850s | REVERT | darker/emptier (~0.82×); mid-stand thinner |
| CP049 garden front | 1910s | KEEP | articulated crowd; lum ~1.00 exact hold |
| CP051 electric nave | 1910s | REVERT | double-head artifact; washout ~1.26× |
| CP058 1936 parade | 1930s | KEEP | coats/bodices darker mid-tones + normal skin; bare shoulders fixed |

Prior v3.1 KEPT still held: CP044, CP054, CP060 (not re-batched this round).
Pairs: `people_v33/previews/CP*_pair.jpg`. Verdicts: `people_v33/verdicts_v33_crowds.json`.

## People library v3.4 — close-up gate; CP058/035/049 revert (2026-10-27)

Eye review of v3.3 KEPT tiles: CP058 AFTER has large bald pale HBM faces, tiny perched hats, bare torsos (uncanny). CP049 same class of floating hats / bald close faces. CP035 has a too-large foreground figure at the left edge. **All three reverted** to pre-adopt heroes.

`people_lib` PEOPLE_VERSION **3.4**: `CLOSE_UP_FRAME_FRAC = 0.08` — if a person-height figure at an object would fill more than ~8% of the frame height, `swap_scene_people` / merged crowd blocks / FB_Hero adopt **keep the previous mesh** (or leave empty). Never base-mesh close-ups without hair, a sized hat, and a clothed torso.

Cumulative Sydenham people KEEP still held from v3.1: **CP044, CP054, CP060**.

## set_v18 build / park establish (2026-10-27)

### CP033 BUILD53 slope (`CAM_CP033_slope_up_35mm`)
- **D-R18-B1 I** Clay/meadow rematted with noise+bump (`build53_clay_r18`, `build53_meadow_r18`); spoil extras, timber baulks, tram sleepers, iron girder stock, cut-face benches, low scaffold decks.
- **D-R18-B2 I** Dress Z snapped to `park_slope`/`terrain` BVH after first pass floated decks (r18 → r18b).
- **D-R18-B3 R** BUILD53 dated: water towers / fountains / courts still absent (eras.py kill list unchanged).
- Hero: `renders/r18_build53_CAM_CP033_slope_up_35mm.png` from `rounds/sydenham-build53-r18b.blend`. KEEP (modest) vs r14 flat clay.

### CP001 1936 prologue (`CAM_CP001_prologue_distant_35mm`)
- **D-R18-P1 I** Park trees: bark/leaf noise mats + 3 secondary canopy icospheres per crown; grass/gravel noise; central-walk kerbs.
- **D-R18-P2 R** Water towers remain visible (1936 pre-fire dated). Heavy foreground asphalt strip from first pass removed in r18b (dominated frame).
- Hero: `renders/r18_1936_CAM_CP001_prologue_distant_35mm.png` from `rounds/sydenham-1936-r18b.blend`. KEEP vs r12 schematic trees.

## S67 CANDIDATE — CP047 / CP048 (1866–67 north-transept fire scar)

Evidence: muse-round2 S67 (ILN 1867-01-05 fire engraving/report; ILN 1867-01-12 ruins of north
transept with Abu Simbel colossi amid warped iron; ground plan tinted fire extent).

| Change | Class | Note |
| --- | --- | --- |
| Removed leftover `frame_SY_north_transept__lost1866` stub that survived into post66-r10 | R | POST66 must not keep north-transept fabric (aerial / Park Trust) |
| Scorched ground pad + warped iron remnants + rubble on former N-transept footprint (x≈150–172) | I | density/heights I; pose language from S67 engraving (curved girders) |
| Charred blanking faces on N/S of former bay | I | temporary/fire-scarred cut, not a rebuilt elevation drawing |
| Soot-darkened materials on adjacent nave iron in fire zone | I | adjacent fabric sooted, not rebuilt |
| Colossi not re-placed in POST66 | R | crystal.dircon: survived fire but not re-erected in the transept; S67 shows them in the *immediate* ruins only |

Blend: `rounds/sydenham-post66-s67-cand.blend`. Live starts untouched. Matched BEFORE remains EARLY r10final/r16 CP047/CP048.

## S67b CANDIDATE — CP047 / CP048 (1866–67 N-transept fire, EARLY ruins)

Prior S67 POST66 fire-scar cand (**REJECT** as fire shots): intact palace look; no readable fire damage.
White-slab removal in CP048 foreground KEPT in live `sydenham-post66-r10.blend`.

New candidate from EARLY (destroyed in-place), framed on the north end:

| Change | Class | Note |
| --- | --- | --- |
| Kill N-transept vault glass / walls / roofs; leave gap where transept stood | R | ILN ruins + 12 Jan 1867 fire-extent plan |
| Twisted / fallen iron ribs + charred collapsed wing fabric | I | pose language from ILN ruins engraving |
| Rubble, blackened / broken glazing, smoke stains on adjacent fabric + colossi soot | I | density I |
| Cameras on north end (CP047 north_end, CP048 terrace_hold) | R | fire must read at a glance |
| Grey overcast winter sky (Jan 1867) replaces clear blue | I | **dated-state departure**, logged |

Blend: `rounds/sydenham-s67b-fire-cand.blend` (script `scripts/install_s67b_fire_ruins_cand.py`).
Before: `renders/s67b_before/` (EARLY + same cam poses). After: `renders/s67b_cand/`.
Pairs: `compare/s67b_cand/pair_CP047.jpg`, `pair_CP048.jpg`.

## 2026-11-01 Muse intake CANDIDATE (`rounds/candidates/sydenham-1856-r16-muse-courts.blend`)
| Item | Grade | Note |
|---|---|---|
| Muse lion fountain replaces grok al_lions; 3.6 m vs 2.2 m footprint | I | Muse sizes ±15% (Owen Jones print, guide 1856 pp.66-69); scale disagreement unresolved |
| Lamassu x4 on Nineveh facade, plan 0205 no. 27 | R/I | x/y read off the gridded plan (±5 ft); orientation along the facade, heads to the entrance is **I** |
| Nineveh Court building not modelled; bulls free-standing | I | dated SY54 to lost 1866 |
| Extra camera CAM_CP037_nineveh_facade_28mm | R | storyboard CP037 cam cannot see the Nineveh facade |

## 2026-11-13 CP044 railway-entrance admission CANDIDATE (`rounds/candidates/sydenham-1856-r16_cp044gate.blend`, script `scripts/candidate_cp044_railway_entrance.py`) — not live, no verdict
Dated collection `SY56_railway_entrance_admission__c1856` (cp_state SY-EARLY_c1856). Live `rounds/sydenham-1856-r16.blend` untouched (1b984fb6).
Dimension check against plan 0205 (`/workspace/crystal-palace-workshop/models/sy-egyptian-column-pair/refs/guide-1856-ground-plan-0205.jpg`, full-res px, 2.887 px/ft):

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP044-01 | "ENTRANCE FROM RAILWAY STATION" cross at the end of the South Wing | R | plan 0205 label + outline | cross built at the modelled wing end | — |
| D-SY-CP044-02 | Cross arms width | R | 282 px = 97.7 ft | 98 ft | +0.3 ft |
| D-SY-CP044-03 | Arm depth (N-S) | R | 139 px = 48.1 ft | 48 ft (y -601..-649) | -0.1 ft |
| D-SY-CP044-04 | Neck/stub width | R | 138 px = 47.8 ft | 48 ft | +0.2 ft |
| D-SY-CP044-05 | Neck 23.6 ft / stub 24.6 ft long | R | 68 / 71 px | 23 / 25 ft | ±0.6 ft |
| D-SY-CP044-06 | Cross position | R/I | plan registration puts the stub end at y = -663 ft | -674 ft (= WING_Y0 - WING_LEN, guide 574 ft) | **11 ft south**: tied to the modelled wing end, not re-registered |
| D-SY-CP044-07 | Wing width in the plan neck | R | 92 px = 31.9 ft | 36 ft (existing WING_W) | +4 ft, inherited, not changed |
| D-SY-CP044-08 | Entrance walls glazed, 24 ft high, flat glazed roofs; 8 ft mullions, sill/transom/plate | I | plan shows dotted (glazed/columned) walls; height not evidenced | 24 ft | U height |
| D-SY-CP044-09 | Colonnade arrives through the west arm's south wall; 12 ft doorway in the stub | I | colonnade route already U in build.py | opening 24 ft at the colonnade axis | — |
| D-SY-CP044-10 | Admission barrier across the neck, 3 turnstiles, closed centre gate, 2 pay boxes, collector's desk | I | inferred: the Company took money at the doors and published daily attendance counts; no fittings drawing in the repo | timber dado 3 ft 6 in, turnstiles 4-arm cast iron | fittings designed, not copied; **no Hyde Park part reused** |
| D-SY-CP044-11 | Pay-box fascia boards left blank (no tariff, no lettering) | B | storyboard CP044: no fabricated tariff, no single price for the whole period | blank green board, gilt lines | — |
| D-SY-CP044-12 | Orange trees in square tubs in the arms and along the wing | I | company plants (narration); orange trees in tubs are an inference for the wing | 10 tubs | U species/placement |
| D-SY-CP044-13 | Glazier on a deal ladder offering up a pane; gardener with a zinc can | U | storyboard asks for staff tending plants and repairing glazing | people_lib v3.4 workmen | staged, not documented |
| D-SY-CP044-14 | Family of four + 9 other visitors + collector (company police uniform) + money-taker | U | storyboard "a family reaches an admission point" | people_lib v3.4, baked meshes (not template-swapped), backs to the lens | — |
| D-SY-CP044-15 | Wing south glazing faces split at the cross; boarded floor laid over the entrance and the wing to y = -300 ft | I | wing interior floor finish not evidenced | boards_gapped | — |
| D-SY-CP044-17 | Wing staircase just north of the entrance (plan 0205: two 8 ft side flights 21.8 ft long either side of a 7 ft spine, 7.6 x 22.5 ft landing, 8.7 ft central flight 20 ft long) | R | plan px 23/20/63/22/65/25/58 | as measured, shifted -11 ft with the cross | — |
| D-SY-CP044-18 | Stair rise and direction: side flights up northward to the landing (+9 ft), central flight up to an upper wing floor at zb+18 (-15.6 ft, the existing frame band) | I | plan shows treads, not levels; guide: 3 storeys in the South Wing | upper floor boards y -505..-100 ft with a balustrade at the stair head | U floor extent |
| D-SY-CP044-16 | CAM_CP044_pay_desks_35mm moved from the nave palm garden (x -380 ft) to the entrance (x -865, y -636 ft, eye 1.6 m); new CAM_CP044_maintenance_50mm | R | storyboard: hold family at the gate, cut to 50 mm maintenance | reframe — the old nave desks are left in place (sit inside the palm-garden tubs, unchanged) | camera move |

## 2026-11-13 CP063 clearance CANDIDATE (`rounds/candidates/sydenham-clearance-r17_cp063scrap.blend`, script `scripts/candidate_cp063_scrap_clearance.py`) — not live, no verdict
Dated collection `SY37_clearance_scrap_sorting_remnant__1937` (cp_state SY-CLEARANCE_1937). Live `rounds/sydenham-clearance-r17.blend` untouched (055ef338). Cameras not moved.
Sources: Crystal Palace Foundation "Disaster strikes, 1936" (by 1937 most of the ironwork removed by W. Ward & Co. Ltd, scrap merchants); Getty/Hulton 886658878, Fox Photos (Becker), 15 Jul 1937 (Buckland helps workmen pull down the last of the ironwork in the central transept after a controlled explosion); UMD World's Fair Treasury umd:1014 (amateur snapshots of the Thos. W. Ward dismantling: frame still standing, men hauling rubble, "mostly done by hand and not with machinery"). Member sizes: survey SURVEY.md (Downes 1852) and params.py.
Dimension check: column 8 in dia (R) -> model 0.667 ft; column top 18'11 3/4" (R) -> 18.98 ft; girder 3 ft deep (R) -> 3.0 ft; girder 23'3 1/4" (R) -> 23.27 ft; bay 24 ft (R, params BAY) -> remnant columns at y 36/60 (COL_Y) = 24 ft; central transept span 120 ft (I/U, params CT_SPAN) -> remnant on x = -60.

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP063-01 | r15/r17 solid "rust box" scrap piles (`clearance_scrap_piles`, `clearance_crane_fg_scrap`) hidden, not deleted | I | Ward were scrap merchants: scrap is cut members, not crates | 56 boxes hidden (prop `cp063_hidden_by_candidate`) | — |
| D-SY-CP063-02 | Last standing bay of the central-transept frame: 2 columns + one 3 ft trellis girder, racked 9 deg by the haul | R/I | Getty 15 Jul 1937: last ironwork in the central transept pulled down by workmen | x = -60, y 36..60; columns 8 in x 18.98 ft; girder 3 x 23.27 ft | lean angle, exact bay and blast damage I |
| D-SY-CP063-03 | Snapped second-tier column stub above the connection; the bay's other girder lying across its footing | U | photo shows twisted/fallen members; no bay-level record | 4.2 ft stub; girder on the ground | — |
| D-SY-CP063-04 | Two manila ropes from the girder head to a gang of 9 hauling | R/I | Getty 15 Jul 1937 (hand pull-down); UMD "mostly by hand" | 2 falls, ~1 in rope, men 3.3 ft apart, hands at ~1.1 m | rope count/size I |
| D-SY-CP063-05 | Sorted scrap: cut column lengths stacked on timber bearers (some snapped short); 6 girders laid flat on bearers; broken girder halves on a heap near the hook | I | merchants sort by kind before carting (inference); sizes R as above | stack 7-6-5-4 at (-41, 63); girder stack at (-47, 44) | layout/counts U |
| D-SY-CP063-06 | Cullet (broken/fused glass) and ash-rubble heaps; a heap of curved wrought rib segments from the transept vault | I | fire destroyed the glazing; vault ribs (UMD photo) | 3 cullet + 4 ash mounds; 7 rib arcs R = 60 ft | form U |
| D-SY-CP063-07 | Each old plateau box pile replaced at the same seeded position by a low ash mound + 3-5 cut members | I | as -01 | 42 piles | — |
| D-SY-CP063-08 | 28 cone stand-ins of the crane gang hidden; 17 people_lib v3.4 `1930s_man` baked meshes (9 haulers + 8 sorting/standing) | U | storyboard: workers secure debris and remove damaged members | nearest ~44 ft from CAM_CP063_crane_lift_50mm, backs or profiles only (close-up gate) | dress is the 1930s town-man stand-in, not documented work clothes |
| D-SY-CP063-09 | Fire-scaled cast iron reads near-black with a little rust bloom (was orange-brown) | I | after a fire, before weathering | `cp063_fire_scaled_cast_iron` 0.075/0.060/0.050 | colour U |
| D-SY-CP063-10 | Yellow mobile crane (D-R15-C2) kept although the UMD note says the work was mostly by hand | U | UMD umd:1014 | unchanged | out of scope for this candidate; flagged |
