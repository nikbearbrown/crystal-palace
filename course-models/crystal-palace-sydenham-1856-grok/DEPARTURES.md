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
