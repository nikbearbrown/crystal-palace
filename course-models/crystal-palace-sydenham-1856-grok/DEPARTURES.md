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

## 2026-11-13 CP056 RND nave drill CANDIDATE (`rounds/candidates/sydenham-war-r14_cp056rnd.blend`, script `scripts/candidate_cp056_rnd_nave_drill.py`) — not live, no verdict
Dated collection `SY15_rnd_depot_nave_drill_mess__1915` (cp_state SY-WAR_1915). Live `rounds/sydenham-war-r14.blend` untouched (718c4b3d). Cameras not moved.
Sources: "Hygienic Conditions at the Crystal Palace", *The Hospital*, 1915 (PMC5229154: ground floor "cleared of its statuary, goods stalls, and other impedimenta, is used for drill, instruction classes"; meals in spaces made "by screening off wide spaces on the outskirts of the vast nave"; 6,578 officers and men in residence); *The Southern Reporter*, 25 Nov 1915, quoted at royalnavaldivision.info/crystalpalace.htm ("In wet weather 10,000 men can be drilled and physically trained on the main floor"; RND recruits "formed into squads of twenty to thirty men", each "commanded by a Petty Officer, assisted by a Leading Seaman"); Rev. John Carter, "H.M.S. Crystal Palace", *Wesleyan Magazine* 1916 ("all the men begin their service in blue-jacket uniform"; meals in "mess decks"). Exterior references 0317 (Lavery 1916, quarter-deck walk) and 0601 (Lavery 1917, terrace muster) are outdoor and not used for this interior frame.
Dimension check: nave 72 ft between column lines (R, params NAVE_SPAN) -> screens on y = -37 (1 ft behind the -36 line); bay 24 ft (R, params BAY) -> screen panels 22 ft between 24 ft bays; squad size 20-30 (R) -> 22-24 men + PO + LS; gallery floor 22.92 ft (I, params) -> screens 8 ft stay below the gallery.

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP056-01 | Nave planting placeholders (all `PLACEHOLDER_nave_tree_*`, `PLACEHOLDER_nave_palm_*`, `PLACEHOLDER_nave_tubs`) hidden, not deleted, for the WAR state | I | The Hospital 1915: floor cleared of "statuary, goods stalls, and other impedimenta" for drill | 49 objects hidden (48 tree/palm crown, frond and trunk objects + tubs; prop `cp056_hidden_by_candidate`) | whether the planted beds/trees were removed is inferred from "other impedimenta" and the 10,000-man drill floor |
| D-SY-CP056-02 | `PLACEHOLDER_nave_statues` (central transept groups) hidden | R | The Hospital 1915: "cleared of its statuary" | hidden; fixed basins kept | basins kept (U: masonry, not "impedimenta") |
| D-SY-CP056-03 | r14 nave cone squads (160 points, D-R14-W1 "wet-weather drill, I") removed from `ppl15_rnd_ratings`; terrace / lower-terrace points unchanged | R/I | Southern Reporter 1915: wet-weather drill on the main floor (R) | 160 of 1,164 points removed (mesh copied to `ppl15_rnd_ratings_cp056`) | — |
| D-SY-CP056-04 | 9 squads of people_lib v3.4 `1890s_sailor` baked meshes: 6 halted in two ranks (10-12 files), 3 marching in column of threes; each with a Petty Officer (out front / alongside) and a Leading Seaman (flank / rear) | R/U | squads of 20-30 under a PO + LS (R) | 20-24 men + PO + LS per squad, 223 figures in all; ~27 in per file, ranks 3.5 ft, column rows 3 ft (I) | formations, positions and number of squads on the floor U; no rifles or drill equipment (storyboard flag); no totals shown |
| D-SY-CP056-05 | Blue-jacket rig (navy jumper, dark cap) for all ratings incl. PO/LS; no badges | R/I | Carter 1916: all begin in blue-jacket uniform | people_lib `1890s_sailor` (CPL3_navy) | people_lib has no 1910s-specific naval rig; PO rate badges and cap tallies not modelled (U) |
| D-SY-CP056-06 | Mess space screened off along the garden-side aisle: canvas-on-deal screens 8 ft high, 22 ft panels on the 24 ft bays from x -330 to -90, every third bay open | R/I | The Hospital 1915: meals in spaces screened off on the outskirts of the nave (R) | 7 screened + 4 open bays | side (garden aisle), x extent, height, material and openings I |
| D-SY-CP056-07 | Mess tables behind the screens: 2 per bay, scrubbed deal 2.5 x 20 ft at 2.45 ft, forms either side, white enamel mugs | I | Carter 1916 "mess decks"; Southern Reporter: seating for 9,800 | 22 tables, 44 forms | table type/size I; seating count not modelled |
| D-SY-CP056-08 | Mess party of 6 (5 seated, 1 walking) at one table behind an open bay | U | — | x -201..-190 | — |
| D-SY-CP056-09 | Hammocks / sleeping arrangements not modelled | U | Carter 1916: men sleep in hammocks; location not given (The Hospital: men lodged largely in the 1911 Festival of Empire buildings) | none | flagged, out of scope |

## CP060 hose crews (2026-11-13, CANDIDATE -> scoped KEEP) — SY36 external fire response, 30 Nov 1936
**Status 2026-11-13 KEEP (parent viewed the pairs) for CAM_CP060_crowd_watching_35mm ONLY**: live from `rounds/sydenham-1936fire-r13_cp060.blend` (dccd2c62, byte copy of the candidate) via `scripts/sydenham_live_heroes.json`, hero `renders/r18/r18_fire_CAM_CP060_crowd_watching_35mm.png`. D-SY-CP060-01..08 below now apply to that live hero. Side effects on CAM_CP058_parade_appliances_35mm (incl. the D-SY-CP060-02 police-line removal) and CAM_CP061_transept_collapse_35mm REJECTED / not routed (they stay on 1936after-r17 / 1936fire-r11b); fire-r12 (33102f4b) unchanged.
Candidate `rounds/candidates/sydenham-1936fire-r12_cp060hose.blend` = `scripts/candidate_cp060_hose_crews.py` on `rounds/sydenham-1936fire-r12.blend` (33102f4b, unchanged). Dated collection `SY36_parade_hose_crews__30Nov1936` (cp_state SY36-FIRE_30Nov1936). Cameras not moved. Hyde Park content not touched.
Sources: storyboard CP060 (firefighters work hoses outside; clear exterior perimeter; follow a hose toward a crew); Science Museum Group co8223615 (Daily Herald, E. G. Malindine, 30 Nov 1936: firemen at the fire; 88 engines, 483 firefighters); Manchester Guardian 1 Dec 1936 (archive repr. 2021: "miles of wriggling hosepipes ... muddy streets"); London Walks, *Today in London History* 30 Nov (water pressure difficulty from the height of the Palace; molten glass "forcing the firemen back").
Dimension check: hose 2 3/4 in LFB delivery (R) -> charged bevel radius 0.115 ft; Parade wall line y = 156 (build.py) and road surface z = -0.5 (dress36.py); figure heights people_lib 5'4"-5'10" (I); jet reach 70-85 ft, peak 16-21 ft above the nozzle line (I, chosen short to show the pressure problem); branch 2.5 ft (I).

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP060-01 | 34 `crowd36_parade` blocks inside the CAM_CP060 frustum within 330 ft hidden (not deleted, prop `cp060_hidden_by_candidate`) | I | storyboard CP060: clear exterior perimeter; spectators belong to CP061 | 34 of the Parade crowd blocks hidden | the r12 crowd band (y 236-300) stood where the hose crews now work; the Guardian puts crowds in the streets, so a crowd-free Parade forecourt is I |
| D-SY-CP060-02 | `police_line_parade` (one object, 120 constables along y = 224) hidden | I | 3,000 police controlled the crowds (London Walks, R) | hidden for the whole Parade | with the crowd gone in frame the line policed nothing; side effect on the fire-r12 CP058 view (no live hero on fire-r12) |
| D-SY-CP060-03 | Wet Parade: one plane x -560..-60, y 158..345 at z -0.47, noise puddles (rough 0.04) in trodden mud (rough 0.62) | R/I | Guardian 1936: "slopped about in the muddy streets" (R) | puddle/mud split ~40/60 | puddle layout, extent and mud colour I |
| D-SY-CP060-04 | 3 branch crews of 3 people_lib v3.4 `1930s_fireman` ('hauling' pose), ~101-124 ft from the lens, 85-115 ft off the Parade wall | R/I | firemen with hoses (Daily Herald 30 Nov 1936, R); stand-off forced by molten glass (R) | 9 men + hose runner + officer = 11 | crew size, positions and stand-off distance I; people_lib firemen wear the workman smock palette (not navy LFB tunics) and a generic helmet, not the 1936 LFB pattern (U) — reads only as silhouettes at night |
| D-SY-CP060-05 | Charged 2 3/4 in canvas hoses from each branch back across the road to below the frame (pumps behind the lens), plus 4 slack flat lines | R/I | LFB 2 3/4 in delivery (R); "miles of wriggling hosepipes" (R) | 3 charged + 4 slack (0.07 ft) | routes I; the pumps feeding them are assumed behind the camera on the Parade (I) |
| D-SY-CP060-06 | Branch pipes 2.5 ft brass; jets as core stream (solid ~60 % of the throw) + widening spray, reach 70-85 ft, falling short of the burning front | I | low water pressure (R) | 3 jets | the throw length is an illustrative choice, not a measured pressure/reach (B/U per storyboard flag) |
| D-SY-CP060-07 | Hose runner walking the middle line, officer pointing at the cordon edge | U | — | 2 people_lib firemen | — |
| D-SY-CP060-08 | Cone flames (dress r11b emissive tongues) NOT changed | — | — | unchanged | still read as hard cones; out of scope for this one-scene candidate |

## CP051 1903 SMMT motor show in the nave (2026-11-14, CANDIDATE -> scoped KEEP) — SY-LATE, 30 Jan - 7 Feb 1903
**Status 2026-11-14 KEEP (parent viewed the pairs) for CAM_CP051_electric_nave_28mm ONLY**: live from `rounds/sydenham-late11-r17_cp051.blend` (579800c4, byte copy of the candidate) via `scripts/sydenham_live_heroes.json`, hero `renders/r18/r18_late11_CAM_CP051_electric_nave_28mm.png`. D-SY-CP051-01..10 below now apply to that live hero. Side effects on CAM_CP052_scaffold_reglaze_35mm, CAM_CP054_plymouth_rescue_35mm and CAM_CP049_worn_garden_front_35mm (incl. the hidden 1911/1913 flags), CAM_nave_interior_28mm and CAM_CP059_nave_fire_28mm (late11 round) REJECTED / not routed (they stay on late11-r16); late11-r16 (3ce48caf) unchanged.
Candidate `rounds/candidates/sydenham-late11-r16_cp051motor.blend` = `scripts/candidate_cp051_motor_show.py` on `rounds/sydenham-late11-r16.blend` (3ce48caf, unchanged). Dated collection `SY03_smmt_motor_show_nave__1903` (cp_state `SY-LATE_1903-01-30..1903-02-07_SMMT_motor_show`). Cameras not moved. Hyde Park content not touched.
Why CP051: the r16 hero (`renders/r16/r16_CAM_CP051_electric_nave_28mm.png`) showed no exhibit at all — a blob placeholder tree filling the right third, a palm-trunk placeholder 13 ft from the lens as a brown slab at the right edge, gold 'tech cabinet' boxes, and a cone-skirt figure standing in the foreground (stray crowd points); the storyboard asks for "a researched electrical or motor exhibit" in the old hall with "one dated exhibit".
Sources: Grace's Guide, *1903 Motor Show (SMMT January)* (Crystal Palace, 30 Jan - 7 Feb 1903; sections Petrol Cars / Steam Cars / Electromobiles / Chassis; stands numbered, some in the courts e.g. Stand 3a Greek Court; Sunbeam 12 h.p. 4-cyl, Fiat 16/20/30 h.p. 4-cyl, Traveller two/three-seat voiturettes, Toledo steam cars); Grace's Guide, *Motor Show Early History* (1903: "over 530 cars; of these about 440 were complete and 68 chassis"); britainbycar.co.uk, *The Crystal Palace Motor Car Shows* (shows "amid the courts and permanent attractions", 1896 and 1902-1906; 1903 the first SMMT show); SMMT history page (first SMMT exhibition at Crystal Palace, January 1903). Storyboard CP051 (electrical displays and later motor vehicles; date one exhibit).
Dimension check: nave 72 ft between column lines, bays 24 ft (params.py, R); stands y +-13..+-33.5 leave a 26 ft central gangway and clear the column line at 36 (I); tonneau wheelbase 7 ft 6 in, track 4 ft 5 in, wheels 33/34 in (I, typical 12-16 h.p. 1903); voiturette wheelbase 5 ft 9 in, 28 in wheels (I); people_lib figures 5'0"-6'0".

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP051-01 | State dated to the first SMMT motor show, 30 Jan - 7 Feb 1903, on the LATE11 fabric | R/I | Grace's Guide 1903 Motor Show (R) | cp_state on the collection | the round's fabric (wear, pendants, scaffold) is the r16 1911 build reused for 1903 (I); later-dated pieces in this view hidden (D-05) |
| D-SY-CP051-02 | 18 exhibitor stands on 9 west-nave bays (x -258..-42), both sides of a 26 ft gangway: 5 in deal platform + crimson/green baize, white turned-post front rail with crimson rope and an opening | I | stands numbered in the catalogue (R); layout in the nave not documented here (the catalogue plan was not consulted, U) | 18 stands | positions, sizes, colours I; which courts/nave bays the 1903 show actually used is U |
| D-SY-CP051-03 | Name boards at the back of each stand on two posts (2.2 x <=18 ft, dark green with gilt lines) left BLANK | I | exhibitor names in Grace's Guide (R) | no lettering | deliberately blank: no maker, stand number or price is invented or assigned to a position |
| D-SY-CP051-04 | 35 vehicles: generic rear-entrance tonneaux (4-cyl 12-16 h.p. class), two-seat voiturettes, and bare 4-cyl chassis with exposed chain drive | R/I | petrol cars, voiturettes and 68 chassis shown (R) | 19 tonneaux / 11 voiturettes / 5 chassis | forms are generic 1903 types, not a specific make (storyboard asks for one actual dated exhibit: still U); steam cars and electromobiles (R present) not modelled; brass radiators, oil side lamps, acetylene head lamp, artillery wheels, RHD |
| D-SY-CP051-05 | Pale grey tyres | I | pre-carbon-black natural rubber tyres read grey/white in period photos (I) | rgb 0.40 | tone I |
| D-SY-CP051-06 | Hidden (not deleted): 19 west-nave planting placeholder objects (blob-tree / palm trunks + crowns, x -420..-30, incl. the palm trunk 13 ft from the lens), and the r16 gold tech-cabinet boxes (64 verts with z < 9 ft removed from a mesh copy `cov_electric_fittings_cp051`; pendants and warm lights unchanged) | I | stands occupied the floor (I) | placeholders hidden, prop `cp051_hidden_by_candidate` | whether the nave planting stayed in place during the 1903 show is U; the r16 cabinets had no source |
| D-SY-CP051-07 | Hidden: 1911 Festival of Empire flagpoles/flags and 1913 Plymouth rescue poles/flags (they read through the glazing; later dates than 1903) | R | dated collections in this round (R) | 8 objects hidden | side effect on the 1911/1913 views of this round (CP049, CP054 etc.) — candidate is for CAM_CP051 only |
| D-SY-CP051-08 | Stray nave-interior points removed (x -360..-30, |y| < 40) from mesh copies of `ppl11_festival_crowd` (12), `ppl11_reglazing_gang` (16), `ppl13_plymouth_rescue_crowd` (16): the same points were duplicated across all three objects (overlapping figures = the people v3.1/v3.3 'double-face' note), some floating at z 57 ft inside the nave span, one 11 ft from the lens | R (bug) | — | 44 points removed | none — these were build artefacts |
| D-SY-CP051-09 | 46 visitors on the gangway + 8 in the garden-side aisle (people_lib v3.4 1890s_gentleman / 1890s_lady as the 1900s stand-in, as CP054) and 12 stand attendants on the platforms; nearest ~70 ft | U/I | — | 66 figures | 1890s dress for 1903 (no 1900s garment set, logged as for LATE11); the lady skirts read as plain bells; no winter overcoats although the show was in Jan/Feb |
| D-SY-CP051-10 | Electrical side of the beat (storyboard 'electrical displays') carried only by the existing r16 pendant fittings | I | — | unchanged | no researched electrical exhibit added |

## CP001 glow on the hill (2026-11-16, CANDIDATE -> scoped KEEP) — SY36 30 Nov 1936, evening, before the collapse
**Status 2026-11-16 KEEP (parent viewed the pairs) for CAM_CP001_prologue_distant_35mm ONLY**: live from `rounds/sydenham-1936-r19_cp001glow.blend` (a348d548, byte copy of the candidate) via `scripts/sydenham_live_heroes.json`, hero `renders/r18/r18_1936glow_CAM_CP001_prologue_distant_35mm.png` (1280x720, 48 spp). D-SY-CP001-01..11 below now apply to that live hero (D-SY-CP001-12 logs the KEEP). Side effects on the 18 other cameras of the 1936-r18b round (CP038 egyptian hold/entry, CP041 alhambra hold/entry/insert_spandrel, CP047 north_end, CP048 terrace hold/walk, CP057 1936_lower_terrace, CP058 parade_appliances, CP059 nave_fire, CP060 crowd_watching, CP061 transept_collapse, CP062 morning_between_towers, CP064 skyline, CP072 footprint, CP073 steps/sphinx_steps: the whole round turns night) REJECTED / not routed; they stay on their current live rounds; 1936-r18b (66edd7cd) unchanged. Pre-keep hero `renders/r18_1936_CAM_CP001_prologue_distant_35mm.png` kept.
Candidate `rounds/candidates/sydenham-1936-r18b_cp001glow.blend` = `scripts/candidate_cp001_glow.py` on `rounds/sydenham-1936-r18b.blend` (66edd7cd, unchanged; the blend the live hero `renders/r18_1936_CAM_CP001_prologue_distant_35mm.png` was rendered from: PNG metadata File/Camera, 48 spp, 1280x720; re-render max diff 0). Dated collection `SY36_prologue_glow__30Nov1936_c1945` (cp_state SY36-1936_30Nov1936_evening_precollapse). Camera `CAM_CP001_prologue_distant_35mm` NOT moved; exposure NOT changed (Filmic, -1.0 EV). Hyde Park content not touched; no state blended (the 1936 round only gains dated evening content; FIRE-round collapse content is not used).
Problem in the live hero: flat midday sun on an intact palace with an empty park (storyboard: "30 November 1936, evening — an orange glow reveals part of the palace silhouette beyond spectators; withhold the collapse"); the 1866-lost north-transept frame stub standing; the lens 0.28 m (0.9 ft) above the dry-silt plane of the south great basin, which filled the lower ~40 % of the frame as a flat beige expanse.
Sources: storyboard CP001; Crystal Palace Foundation, "Disaster strikes, 1936" (Buckland saw a red glow c.7 pm; small fire in the office area in the centre transept; first brigade call 7:59 pm, first engine 8:03); London Walks, *Today (November 30) in London History* (wind "freshly from the northwest"; fire "starting in the front of the transept, was blown right through it to the back and also down through the southwest wing"; sky "resembled a brilliant sunset"; "flames and glowing smoke-clouds rose to an altitude double the height of the two great terminal towers"); Wikipedia "Crystal Palace" (fire section: red glow, women's cloakroom, 100,000 came to Sydenham Hill to watch); Corinthian-Casuals FC "Former Grounds" (Corinthian FC at Crystal Palace 1922-36); football round FB02/FB03 (pitch in the drained south basin, centre x -518 ft, y -1962 ft).
Dimension check (model vs source): central transept 118 ft wide (x ±59 ft) vs 120 ft cited (U, params CT_SPAN); transept crown 174-177 ft (params CT_CROWN); water towers 285 ft vs 284 ft (U); south great basin 761 x 420 ft from the 1857 park map (R, earlier row); lens eye 5.2 ft over the park grass (states.py EYE) — before the candidate it was 0.9 ft over the silt plane / 2.8 ft over the basin floor stone; spectators 5'1"-6'2" (people_lib); smoke column base 180 ft, puff tops beyond the frame (> 600 ft at the palace distance) vs "double the tower height" ≈ 570 ft (R as a claim).

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP001-01 | Time state: 30 Nov 1936 c.7:45 pm — fire inside the central transept and the south half of the nave, glazing and vault intact (collapse withheld) | R/I | fire seen c.7 pm, first call 7:59 pm (CPF, R); storyboard: withhold the collapse | one instant, pre-collapse | the exact minute and the extent of fire at it are I (no record of the spread per minute) |
| D-SY-CP001-02 | Night world: sky gradient (zenith RGB 0.0045/0.0055/0.014, warm horizon 0.040/0.020/0.012 for London + fire skyglow); Filmic -1.0 EV kept | I | "the sky over Sydenham resembled a brilliant sunset" (R, as a description) | world shader replaced in the candidate only | skyglow colour/strength I; every other camera in this round turns night as well (side effects, none live on 1936-r18b) |
| D-SY-CP001-03 | Moonlight: the round's sun light reused at 0.035, bluish (0.62/0.72/1.0), from the east 18 deg above the horizon (behind the ridge) | R/U | moon c.16.5 days old on 30 Nov 1936 (waning gibbous, rises in the east early evening; computed from the mean synodic month, R) | energy/altitude | strength and altitude U; clouds not modelled (weather U) |
| D-SY-CP001-04 | 126 emissive flame tongues (blackbody 2300 K base -> 1300 K tip): 46 in the central-transept front office area (x ±56 ft, y -190..+98 ft), 70 down the south half of the nave to x -490 ft, 10 across the crossing to x +148 ft; heights 5-66 ft; all inside the glass | R/I | fire start in the centre transept office area (CPF, R); spread from the front of the transept to the back and down the south-west wing on a NW wind (London Walks, R) | tongues on floor (75 %) and gallery level (25 %) | count, heights and positions I; nothing breaks through the vault (storyboard) |
| D-SY-CP001-05 | 9 interior point lights (RGB 1.0/0.42/0.12 ≈ 1800 K), 0.08-0.6 MW each, 2.93 MW in all; one at 230 ft lights the smoke base | I | — | — | light power tuned by eye so the frame reads at the unchanged -1.0 EV; the park grass is fire-lit more than a real 2,150 ft throw would give |
| D-SY-CP001-06 | Smoke column: 20 volume puffs (density 0.018-0.030 /m with noise), base 180 ft, leaning south-east (-x, +y) downwind, underside emission fading with height | R/I | wind freshly from the NW (London Walks, R); smoke clouds to twice tower height (R, as a claim) | lean ~45 deg in plan, column leaves the frame top | form, density and lean angle I. NB the FIRE rounds (fire-r11b/r12, states.py) lean their smoke north-east (+x, +y, "wind U"); this candidate follows the NW-wind source and does not touch those rounds |
| D-SY-CP001-07 | `frame_SY_north_transept__lost1866` (x +492..+564 ft) hidden, not deleted (`cp001_hidden_by_candidate`) | R | north transept burnt 30 Dec 1866, never rebuilt; storyboard CP001 "keep North Transept absent" | hidden | the stub stood in every 1936 view of this round (also hidden there by the candidate: side effect) |
| D-SY-CP001-08 | South great basin drained: mesh copies `park_basins_water_cp001` (2 faces dropped: the south-basin silt polygon, 27,463 m2, and the lowest south cascade-channel silt step, 7 x 11 m, at its north-east corner) and `park_basins_stone_cp001` (77 faces dropped: basin floor + centre tazza/urns within 115 ft of the basin centre); originals hidden, not deleted; the r18 park grass (`park_slope`, `park_grass_r18`) is the ground, 5.2 ft below the lens | R/I | ground in the drained south basin from 1895 (football FB02, R); Corinthian FC home ground 1922-36 (R) | rim walls and coping kept; north basin untouched | MISS: the football pitch, markings, stands and pavilion of the 1936 ground are not modelled (pitch centre lies left of the frame); whether the basin rim survived round the ground in 1936 U |
| D-SY-CP001-09 | 64 spectators (people_lib v3.4, era 1930s: 60 % `1930s_man`, 40 % `1930s_woman`; 86 % standing, 8 % walking, 6 % pointing), 28.5-460 ft from the lens on the park grass, each turned toward the centre transept ±200 ft; no figure within 98 ft of the lens in a 22 %-wide window in front of the transept | R/I | 100,000 came to Sydenham Hill to watch (Wikipedia, R) | 64 figures | positions I; crowds are documented in the streets and on the Parade — spectators inside the lower park at night is I (whether the grounds were open U) |
| D-SY-CP001-10 | people_lib 1930s day-coat palette used unchanged at night | U | — | — | they read as silhouettes; hats/coats not checked against 1936 photographs |
| D-SY-CP001-11 | Camera and exposure unchanged | — | — | `CAM_CP001_prologue_distant_35mm`, Filmic -1.0 EV | the storyboard's 6 m walk toward the ridge is not animated (stills only) |
| D-SY-CP001-12 | Scoped KEEP 2026-11-16: only CAM_CP001_prologue_distant_35mm routed to `rounds/sydenham-1936-r19_cp001glow.blend` (byte copy of the candidate, md5 a348d548); live hero = candidate after (max diff 0), `--rebuild` from 1936-r18b max diff 0 | — | parent verdict | 1 camera routed | the night world, hidden north-transept stub and drained south basin exist only in the r19 round; the 18 other 1936-r18b views keep their own live rounds (Sydenham and Hyde Park states not blended) |

## CP033 slope works (2026-11-16, CANDIDATE -> scoped KEEP) — SY-BUILD c. autumn 1853, the park slope below the terraces
**Status 2026-11-16 KEEP (parent viewed the pairs) for CAM_CP033_slope_up_35mm ONLY**: live from `rounds/sydenham-build53-r19_cp033slope.blend` (ebb75f70, byte copy of the candidate) via `scripts/sydenham_live_heroes.json`, hero `renders/r19_cp033slope/r19_build53slope_CAM_CP033_slope_up_35mm.png` (1280x720, 48 spp, luma 184.70). D-SY-CP033-01..10 below now apply to that live hero (D-SY-CP033-11 logs the KEEP). Side effects on the 32 other cameras of the build53-r18b round NOT promoted: REJECTED (>0.5 % of pixels changed) CP033 terrace_cut / transept_ribs, CP038 egyptian_entry / egyptian_hold (near-lens figure swapped), CP057 1936_lower_terrace, CP059 nave_fire, compare_0007 and ext_elevated_overview (frustum-shaped works-ground wedge), compare_0074, nave_interior, CP073 sphinx_steps, central_transept_straight; NOTE (noise level) the other 20. All stay on their current live rounds; build53-r18b (dc579904) unchanged. Pre-keep hero `renders/r18_build53_CAM_CP033_slope_up_35mm.png` kept.
Candidate `rounds/candidates/sydenham-build53-r18b_cp033slope.blend` = `scripts/candidate_cp033_slope.py` on live `rounds/sydenham-build53-r18b.blend` (dc579904, unchanged; the blend the live hero `renders/r18_build53_CAM_CP033_slope_up_35mm.png` was rendered from — re-render with the live recipe 1280x720 / 48 spp / KEEP_LIGHTING / NO_PEOPLE is pixel-identical, max diff 0). Dated collection `SY53_slope_works__autumn1853` (cp_state SY-BUILD_c1853_slope_works, 387 objects). Camera `CAM_CP033_slope_up_35mm` NOT moved; sun/world/exposure NOT changed (Filmic, -1.0 EV). No Hyde Park 1851 content used; the BUILD53 erection front (D-R14-B1) is unchanged.
Problem in the live hero: the lower half of the frame is one flat uniform beige plane (the slope does not read); the only spoil heap in frame is a squat 24-sided cone (x 55, y -219 m) whose downhill rim floats above the slope (dark lip); the pv57 navvy instances read as white-headed posts/signposts; a placeholder sphere-tree floats at the right edge; nothing on the lower-terrace line for x > 40 m (terraces_stone is clipped there), so the terrace front reads only on the left.
Sources: storyboard CP033 (terrace earthworks and a raised platform support a new frame; worksite edge on the slope); *Guide to the Crystal Palace and Park* (1854), "The Terraces" (upper terrace 1576 x 48 ft, terrace wall of Bath stone; central flight and Grand Central Walk 96 ft; lower terrace 1664 ft long between the wings, 512 ft wide); Journal of Horticulture/Gardeners' Chronicle report on the new palace (c.1853: "about 1000 labourers ... levelling the ground, and forming basins"; a raised terrace walk 48 ft broad over a grass slope 50 ft wide); P. H. Delamotte, *Photographic Views of the Progress of the Crystal Palace, Sydenham* (1855): no. 6 "Grounds looking towards Penge, Aug. 1852", no. 7 "Commencement of terraces, Aug. 1852", "Workmen in the grounds", "The Terrace Front, with Mortar Machine", "Scaffolding for the erection of the great ribs in the Centre Transept"; Crystal Palace Foundation history pt 2 (1,608 ft long, three transepts, barrel-vaulted nave, central transept 168 ft).
Dimension check (model vs source): main building x ±245.2 m = 1609 ft vs 1,608 ft (R, OK); central transept crown 176 ft (vault ribs top 53.6 m) vs 168 ft CPF / 174-175 ft guides (U, unchanged); lens eye 2.82 m = 9.2 ft above `park_slope` (existing camera, not moved — reads as a slightly raised viewpoint, e.g. off a cart or bank); figures 5'0"-5'10" (people_lib v3.4, nearest 18.8 m); horses ~16 hands (5 ft 4 in at withers, 2.48 m to ear tips); tip-cart wheels 5 ft, body 6 ft x 4 ft 6 in; elm 62 ft, crown spread ~51 ft; slope gradient in frame 1:12.5 (4.6°, model terrain, unchanged).

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP033-01 | Works ground in the CAM_CP033 frustum: polar-grid overlay `cp033_slope_works_ground` (65,755 faces, 7-150 m from the lens, y < -196.2 m) 2-12 cm above `park_slope` (never below it; dips 4 cm under existing r18 dress pieces so sleepers/baulks/puddles keep their look); worked London-clay browns (albedo ~0.07-0.15, dry earth low specular), two wheel-rutted cart tracks, 4 small wet patches, remnant rough pasture patches away from the workings | I | ~1000 labourers levelling the slope (R, c.1853); London Clay slope below the Bagshot/Claygate-capped ridge (R, BGS general) | colours, track routes, pasture extent I | `park_slope` itself and its r18 material unchanged; the overlay ends at the frustum (other cams see its edges — side effect) |
| D-SY-CP033-02 | Centre cone heap (earth_spoil_heaps_cuttings island at x 55, y -219 m, 40.6 m across, 6.4 m) dropped from a mesh COPY (`earth_spoil_heaps_cuttings_cp033`, 14 faces dropped; original hidden, not deleted) and replaced by an irregular grounded tip heap (~34 x 20 m, 4.2 m, base sunk 0.5 m, steeper tipping face) + a 14 x 9 m second tip, two diagonal plank barrow runs on trestles | R-typical / I | barrow-and-plank earthworks (Delamotte 1852-53) | shapes, sizes, positions I | the other 23 r14 spoil cones are unchanged (none is in the CP033 frame) |
| D-SY-CP033-03 | pv57 navvy instance points inside the CAM_CP033 frustum (<= 430 m; 368 points) dropped from a mesh COPY `ppl53_navvies_erectors_cp033` (original hidden, not deleted; 369 points outside the frustum kept) and re-placed at the same spots (336 after de-duplicating overlapping points < 0.9 m) as people_lib v3.4 `1850s_navvy` / `1850s_workman` (workman for y > -112 m, i.e. erectors at the building), random working/hauling/standing/walking poses, mid LOD < 140 m, crowd LOD beyond | R numbers (claim) / I positions | ~6,400 workforce claim (D-R14-B4); ~1000 on ground works | 336 + 24 new = 360 people_lib figures in the round | the ppl53 points included duplicates (the people v3.1 'double-face' issue); poses are people_lib generic, not dug-in |
| D-SY-CP033-04 | Navvy dress: the people_lib smock materials (albedo 0.35-0.48) on these 360 figures only are copied and recoloured to worn drab/canvas, faded blue flannel, fustian brown and one rust (174 slots, 6 colours) | R-typical / I | navvies' canvas/flannel shirts, moleskin, velveteen (Coleman, *The Railway Navvies*) | colours I | people_lib itself not edited; other rounds unaffected |
| D-SY-CP033-05 | Foreground bank cutting at 21-29 m (centre-left): 7 navvies (shovels and picks held in front, simple props), a 15.6 m clay berm thrown up-slope of a shallow darkened cut, 2 barrows (one loaded) + a barrow man | R-typical / I | Delamotte 'Workmen in the grounds' | positions, tools I | tools are not hand-attached (float slightly at some poses); cut depth 10 cm (shown by colour, overlay never goes below park_slope) |
| D-SY-CP033-06 | Three horse-drawn two-wheeled tip carts with carters (28 m near loading with 3 navvies shovelling; 64 m climbing; 114 m at the heap); horse = port of the CP002 LN2 draught horse (~16 hands, bay/black) | R-typical / I | horse earth-carts in park works (Delamotte; R-typical) | 3 teams | cart and horse geometry is simple (no traces/chains), no driver on the shafts |
| D-SY-CP033-07 | Surveyor (people_lib 1850s gentleman) at a dumpy level on a tripod at 19 m, staff man with a red/white 14 ft levelling staff at 47 m; 8 red/white ranging poles (8 ft) along the slope | I | — | — | slope cue; positions I |
| D-SY-CP033-08 | Lower-terrace garden-front wall under construction for x 40-238 m on the line y -195.6 m (where BUILD53 had nothing): brick piers on 24 ft bays, part-turned shallow alcove arches + alcove back walls to x ~80 m, then courses falling to 1.3 ft at the north end; pole scaffolds, brick stacks, mortar boards; two shear-legs (33-36 ft) lifting Bath-stone coping blocks; 8 masons/labourers | R (alcoved garden-front wall 1,896 ft) / U progress / I form | lower-terrace garden-front wall formed into alcoves, 1,896 ft (R); terrace wall of Bath stone (R, upper terrace) | stock brick with Bath-stone coping blocks; max 9.8 ft above the park | **the model terrain is flush at this line (park_slope and terrace_gravel both z -13.6 m), so the wall stands FREE above the ground instead of retaining the lower terrace (U)**; bay spacing, height and the north-wards progress gradient are I |
| D-SY-CP033-09 | Placeholder tree 38 (sphere crown, 52 m from the lens, right edge) hidden (not deleted) and replaced at the same trunk by an elm (CP032 `trees.py` build_elm recipe vendored in the script; 62 ft, 77,250 leaf cards, olive leaves with first autumn yellowing) | I | Penge Place park trees retained in the new park (I) | 1 tree | other 69 placeholder trees unchanged |
| D-SY-CP033-10 | Not changed / noted: camera, exposure, the BUILD53 frame/erection front, water towers absent (D-R18-B3 R). Existing terrain departures left as they are: upper terrace (y -100..-48 m) 171 ft deep vs 48 ft walk + 50 ft grass slope (R); lower terrace (y -194..-100 m) 308 ft vs 512 ft (R); Grand Central Walk 80 ft vs 96 ft (R) | — | see sources | — | **the north transept (x 150-172 m) falls just outside this frame (27.8° right of the lens axis vs 27.2° half-FOV), so the storyboard's "three transept positions are distinguishable" is still not met in CAM_CP033_slope_up_35mm** |
| D-SY-CP033-11 | Scoped KEEP 2026-11-16: only CAM_CP033_slope_up_35mm routed to `rounds/sydenham-build53-r19_cp033slope.blend` (byte copy of the candidate, md5 ebb75f70); live hero = candidate after (max diff 0), `--rebuild` from build53-r18b max diff 0 | — | parent verdict | 1 camera routed | the works ground, re-placed navvies, tip carts, garden-front wall works and elm exist only in the r19 round; the 32 other build53-r18b views keep their own live rounds (no state blended) |

## CP035 royal dais (2026-11-17, CANDIDATE -> scoped KEEP) — SY54 opening day, 10 June 1854, central transept
**Status 2026-11-17 KEEP (parent viewed the pairs) for CAM_CP035_transept_gallery_28mm ONLY**: live from `rounds/sydenham-open54-r17_cp035dais.blend` (09cd4606, byte copy of the candidate) via `scripts/sydenham_live_heroes.json`, hero `renders/r17_cp035dais/r17_open54dais_CAM_CP035_transept_gallery_28mm.png` (1280x720, 28 spp r16 lean-hero recipe, luma 100.44). D-SY-CP035-01..12 below now apply to that live hero (D-SY-CP035-13 logs the KEEP). Side effects on the other 46 cameras of the open54-r16 round NOT promoted: CAM_CP035_dais_50mm REJECTED by the parent (74.28 -> 56.56, the new dais is hidden behind close royal-party / court figures); REJECTED (>0.5 % of pixels changed) CP035 procession_nave, CP038 egyptian_hold, CP040 greek_roman_fronts / mediaeval_front; NOTE noise-level the other 13 judged cams; the 28 cams whose pairs were still rendering at KEEP time not judged and not promoted. All stay on their current live rounds; `rounds/sydenham-open54-r16.blend` (683b1bc9) unchanged; pre-keep hero `renders/r16/r16_CAM_CP035_transept_gallery_28mm.png` kept.
Candidate `rounds/candidates/sydenham-open54-r16_cp035dais.blend` = `scripts/install_cp035_royal_dais.py` on live `rounds/sydenham-open54-r16.blend` (683b1bc9, unchanged; the blend the live hero `renders/r16/r16_CAM_CP035_transept_gallery_28mm.png` was rendered from — re-render with the live recipe 1280x720 / **28 spp** / NO_PEOPLE / blend lighting is pixel-identical, max diff 0). Dated collection `SY54_royal_dais__10Jun1854` (cp_state SY54_opening_royal_dais__10Jun1854, 61 objects). Camera `CAM_CP035_transept_gallery_28mm` NOT moved; sun/world/exposure NOT changed (Filmic, -1.0 EV). No Hyde Park 1851 content used; nothing from later Sydenham states (no water towers, no fountains, no Handel orchestra).
Problem in the live hero: the dais is a crude red box with a flat red 'roof' over its west half and a red block 'throne' at the WEST end facing the orchestra (D-R14-O1, U); the royal party is a handful of pv57 cone figures mixed with nave-lining crowd points standing ON the dais; the gallery the camera stands on has no front railing (crowds stand at a 23 ft drop); six pv57 'hero silhouette' points (people57 r16 adds 4 per camera to EVERY crowd carrier) are stacked 2.9 m from the lens and read as one huge pale blob at the left edge.
Sources: ETH-Bibliothek e-rara vol. III pp. [216]-[217] (19th-century history, e-rara pagetext 12187846/12187847; account of the opening: 'In the centre of the building a dais was erected for her Majesty and the royal party, with vases full of the choicest flowers'; the party = the Queen, Prince Albert, the Prince of Wales, Prince Alfred, the Princess Royal, Princess Alice, the King of Portugal and the Duke of Oporto; 'the members of the government were arranged on one side, and the foreign ambassadors, in their rich costumes, on the other, together with the directors and officers of the Crystal Palace in court dress'; orchestra of 'not less than 1,500 performers' under Costa; 'rows upon rows of crimson benches'); *Household Narrative of Current Events* 1854 p. 136 (Laing 'advanced to the foot of the throne'; the Queen 'descended from the throne, leaning on the arm of Prince Albert'); Queen Victoria's journal, 10 June 1854 ('we Ladies in very elegant morning dresses, & the Gentlemen, in uniform'; 'Immediately behind us rose the enormous Orchestra, of nearly 2000 performers'; 'When Paxton came up the steps of the dais'); ILN 17 June 1854 (dais in the transept, D-R14-O1). No source found gives dais dimensions, a canopy or colours.
Dimension check (model vs source): `checks/cp035_dais_candidate_OPEN54.txt` 27/27 PASS (unchanged building: length 1,608 ft, transept span 120 ft, crown 174 ft 3 in, no water towers / fountains, dais + flags + choir present, dated collection). Dais 32 x 44 ft x 3 ft (r14 footprint kept, U); flight 3 x 1 ft risers, 20 ft wide; haut-pas 8 x 16 ft, +1 ft; chair of state seat 1 ft 4 in, back 5 ft 6 in; canopy tester 15 ft above the dais (21.8 ft above the floor, top of crown); carpet runner 12 x 30 ft; gallery railing 3 ft 6 in on the 22 ft 11 in gallery floor (z 6.99 m; upper tier 13.10 m); figures (people_lib v3.4, incl. hats): the Queen 5 ft 2 in (Victoria c. 4 ft 11 in, R), Albert 6 ft 4 in with hat (c. 5 ft 10 in, R), children 4 ft 1 in - 5 ft 0 in (ages 9-13, R), men 5 ft 10 in - 6 ft 2 in with hats. Nearest new figure to the hero lens 8.1 m; the Queen 27.8 m.

| ID | Item | Grade | Source value | Model value | Departure |
|---|---|---|---|---|---|
| D-SY-CP035-01 | Old dais `open54_dais` + `open54_dais_gilt` hidden (not deleted) and rebuilt as `cp035_royal_dais` on the same footprint (x -46..-14 ft, y +-22 ft, 3 ft): crimson cloth with velvet sheen, carpet top, 6 in gilt band + bullion fringe on all four fascias | R existence / U size / I form | 'a dais was erected' in the centre of the building (R) | 32 x 44 x 3 ft | size and colour not in any source found (kept from r14) |
| D-SY-CP035-02 | Orientation reversed: chair of state on an 8 x 16 ft haut-pas at the EAST end facing WEST, flight of steps on the WEST front — the orchestra/choir stand (x 70..172 ft) is now behind the Queen | R | QV journal: 'Immediately behind us rose the enormous Orchestra' | throne x -18 ft facing -x | supersedes D-R14-O1 ('facing north to the choir stand') for this candidate only; the procession still approaches from the west nave |
| D-SY-CP035-03 | Chair of state (gilt frame, crimson upholstery, arms, crown cresting) + footstool; small canopy over the throne only: 4 turned gilt posts, crimson tester 9 x 16 ft with scalloped gilt-fringed valance, dossal behind the chair, gilt crown on top | R throne / U canopy / I form | 'foot of the throne', 'descended from the throne' (R) | canopy top 21.8 ft | **no source found mentions a canopy**; kept (smaller than r14's 24 x 28 ft roof) as the convention of 1851; may be removed |
| D-SY-CP035-04 | Three-riser carpeted flight (20 ft wide) with gilt nosings; crimson carpet runner 12 x 30 ft westward from the flight; low (2 ft 6 in) gilt rails along the north/south dais edges and the west front either side of the flight | I | 'came up the steps of the dais' (R steps) | — | runner length/width, rails I |
| D-SY-CP035-05 | Six flower vases on pedestals (2 west dais corners, 2 flanking the flight on the floor, 2 flanking the haut-pas): stone pedestal, gilt tazza, foliage mound with ~150 mixed blooms each | R / I | 'vases full of the choicest flowers' (R) | 6 vases | count, form, colours I; the two east-corner vases were dropped (2.8 m from the CAM_CP035_dais_50mm lens) |
| D-SY-CP035-06 | 186 pv57 points on/at the dais and on the carpet approach (the r14 royal party + yeomen points and the east ends of the nave-lining rows) dropped from mesh COPIES (`*_cp035`) of the PPL57 crowd carriers (7 carriers, originals hidden, not deleted) | — | — | — | carriers re-instanced with the same GN group (`PPL57_instance_people`) and attributes |
| D-SY-CP035-07 | Royal party as people_lib v3.4 figures (hero LOD) on the haut-pas / dais front: the Queen (lilac 'morning dress', I), Prince Albert (scarlet uniform coat, I), King of Portugal and Duke of Oporto (dark blue uniforms, I), Prince of Wales and Prince Alfred, Princess Royal and Princess Alice, 4 ladies of the household | R people / I dress, positions | party named (R); 'Ladies in very elegant morning dresses, & the Gentlemen, in uniform' (R) | 12 figures | the gentlemen keep people_lib top hats (U: hats would be off before the Queen; no uniform hats in people_lib); faces are generic |
| D-SY-CP035-08 | Government ministers in court dress (black, 12 figures, two ranks, north side) and foreign ambassadors in coloured gold-trimmed uniforms (12 figures, south side) on the dais edges facing the centre line; 4 directors in court dress at the dais front; Samuel Laing on the flight with the address (vellum roll) | R / I | 'government on one side, ambassadors ... on the other ... directors in court dress'; Laing 'advanced to the foot of the throne' (R) | 29 figures | uniform colours I; the address roll floats at hand height (not hand-attached) |
| D-SY-CP035-09 | 14 yeomen of the guard (people_lib 1850s_soldier, scarlet coat/breeches, gold trim) either side of the flight and along the dais sides on the floor, facing out | I | yeomen at state occasions (R-typical) | 14 | Tudor bonnets/partisans not modelled (black hat) |
| D-SY-CP035-10 | Gallery-front railings `cp035_gallery_front_railings` on every free nave/transept edge of the existing gallery floors (both tiers; 63 runs, 2,045 m): 3 ft 6 in, mahogany cap over an iron top rail, bottom rail, stanchions every 8 ft, open diamond lattice of flat bars, painted the frame's Owen Jones blue (iron_painted_OJ base colour) | R-typical / I | gallery railings at Sydenham (R existence, photographs); form I | 3 ft 6 in | lattice pattern and colour I; outer-wall edges and building ends left without rail |
| D-SY-CP035-11 | 62 pv57 gallery points within 9 m of the hero lens dropped (incl. the 6 stacked 'hero silhouettes' 2.9 m from it); 1,218 gallery-front points that would stand in the new railing pushed 0.45 m back onto the floor (same mesh copies); 3 people_lib spectators at the rail 8.1-11.0 m from the lens | I | — | — | the r16 lens 'hero silhouettes' stay at every other camera of the round |
| D-SY-CP035-12 | Not changed / noted: camera, exposure, the choir stand and transept seating stands, flags/banners, the nave crowds beyond the dais, the 'crimson benches' (R) — transept-floor crowds still stand; people_lib itself not edited | — | 'rows upon rows of crimson benches' (R) | — | benches would be the next CP035 step; **hero luma falls 109.27 -> 100.44 at the live 28 spp (109.24 -> 100.40 at 48 spp; content, not grade): the pale near-lens blob and pale cone figures are gone and the railing crosses the frame** |
| D-SY-CP035-13 | Scoped KEEP 2026-11-17: only CAM_CP035_transept_gallery_28mm routed to `rounds/sydenham-open54-r17_cp035dais.blend` (byte copy of the candidate, md5 09cd4606); live hero = candidate after_28spp (max diff 0), `--rebuild` from open54-r16 max diff 0 | — | parent verdict | 1 camera routed | the rebuilt dais, royal party / court figures, gallery railings and near-lens point removal exist only in the r17 round; CAM_CP035_dais_50mm (dais hidden behind close figures) REJECTED and the other open54-r16 views keep their own live rounds (no state blended) |
