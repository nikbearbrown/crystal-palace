# PROGRESS — SY-EARLY c.1856
- r01: shell built (scripts/build.py). Preview renders washed out.
- r02: darker albedos, exposure, cameras retargeted, nave planting placeholders.
- r03: sphere trees; full renders renders/r03_*.png; self-score 5/10 (later found: no columns/girders — frame bug).
- r04: frame bug fixed; stepped CT front; tiered nave/wings; basement arcade + stairs; terraces/balustrade/statues; Owen Jones toggle; boarded floor; palms/trees; park fountains set (SY56_park_fountains_cascades__dated); ortho section; compare/r04_section_vs_0212.jpg.
- r05: pale exterior iron; S basins r=45 (map); 0074/0007 cameras re-solved; ortho_scale fix.
- r06: nave/transept placeholders from plan 0205 detection (26 marks), crossing Crystal Fountain withdrawn (U), 70 park trees, 0007 elevated camera. 259 objects / 154k faces / 2.0 MB. 12/12 dimension checks PASS (checks/r06_dimension_check.txt).
- r06 outputs: renders/r06final_*.png (1920x1080, 128 spp), compare/r06_vs_0074.jpg, compare/r06_vs_0007.jpg, compare/r06_section_vs_0212.jpg, compare/r06_plan_overlay.jpg.
- r07 (rebuild: SY_NO_COURTS=1 blender -b -P scripts/build.py -- rounds/sydenham-1856-r07.blend): ribbed vault + arched bands, tower bracing, octagonal Brunel towers with lantern, grass banks, ornate basins + jets, 1857 park paths/beds, 0007 cam re-aim, ground slope + basement piers + cut floor in section. 271k faces / 5.1 MB. Dimension checks in checks/r07_dimension_check.txt.
- r07 outputs: renders/r07final_*.png (0074 128 spp; others 32–64 spp), compare/r07_vs_0074.jpg, r07_vs_0007.jpg, r07_section_vs_0212.jpg, r07_plan_overlay.jpg.
- r08: courts (scripts/courts.py, exec'd at end of build.py unless SY_NO_COURTS) — Egyptian 0226 + Alhambra 0246 as dated collections, court voids in the main frame, Egyptian annex through the Parade wall. 288.8k faces / 5.6 MB. renders/r08final_*.
- r08b: Alhambra spandrel strips welded (black-seam fix), arcade-walk ceiling, 0108 camera from the Hall of Justice through the central arch. 12/12 dimension PASS (checks/r08b_dimension_check.txt). compare/r08b_plan_overlay.jpg, compare/r08b_courts_on_plan0205.jpg, compare/r08_alhambra_vs_0108.jpg (from r08b render). renders/r08bfinal_* (48 spp; 0108 portrait RES=1080x1371).
- Render resolution override: RES=WxH env var for scripts/render.py.
- Commands:
  - Rebuild: /workspace/blender5/blender -b -P scripts/build.py -- rounds/<name>.blend
  - Render: blender -b rounds/X.blend -P scripts/render.py -- renders <tag> <pct> <spp> <cams...>
  - Section: blender -b rounds/X.blend -P scripts/section_render.py -- compare/<tag>.png
  - Overlay: blender -b rounds/X.blend -P scripts/plan_overlay.py -- compare/<tag>; python3 scripts/plan_composite.py compare/<tag>.raw.png compare/<tag>.jpg
  - Palette: blender -b rounds/X.blend -P scripts/set_palette.py -- 0|1 out.blend
  - Plan marks: python3 scripts/plan_nave_objects.py checks/plan_nave_objects.json
  - Checks: blender -b rounds/X.blend -P checks/dimension_check.py -- checks/<tag>.txt
- NOT pushed. Branch grok-sydenham-1856, local commits only.
- Next states: courts (0226/0246) → post-1866 without North Transept → 1936 fire → ruins/towers.
- r09 (20:35): appended Muse colossi (vendored, unmodified) into SY56_north_transept_colossi_muse__lost1866 at the garden end of the north transept; 12/12 PASS; final render renders/r09final_CAM_north_transept_colossi_35mm.png
- r10 START (20:45): brief = Alhambra detail pass (relief stucco via shader displacement, zellige dado, slender paired columns, cusped stilted/muqarnas arches, lions, planting, muted colour); Egyptian lotus capitals + relief/hieroglyph bands, warmer; colossi cam headroom; Egyptian entry frame 1; SY-POST66 state (env SY_STATE=POST66 + merged scenes) with CP047/CP048 matched before/after pairs. Evidence for post-1866: Historic England blog (north transept never rebuilt; North Nave, Alhambra, Byzantine restored), crystal.dircon chronology ("whole of the north end ... except part of a low narrow wing"), Aerofilms EPW021373 1928 ("truncated north end") — scratch copy /workspace/syd_scratch/post66/ (not committed: licence).

## r10 (milestones)
- Fixed an infinite loop in `hang()` (rr guard) that had hung the build.
- r10a/r10b: Alhambra detail pass (relief shader, stilted cusped arches + muqarnas soffits, paired slender columns, dado, Lions fountain, planting, muted colour) + Egyptian lotus capitals/relief bands; colossi headroom and Egyptian entry frame fixed.
- r10b: spandrel black slits fixed (tessellated spandrel faces). `rounds/sydenham-1856-r10b.blend` 588 obj / 460k faces; `checks/r10b_dimension_check.txt` 12/12 PASS.
- SY-POST66: `SY_STATE=POST66 blender -b -P scripts/build.py -- rounds/sydenham-post66-r10.blend` → 295 obj / 432k faces; `checks/post66_r10_dimension_check.txt` 12/12 PASS (north transept ABSENT = pass in POST66).
- Renders: `renders/r10final_*`, `renders/post66r10_*` (CP047/CP048 identical settings 50%/40 spp); compare sheets in `compare/r10_*`.

## r11 (milestones) — SY-1936 / FIRE / AFTER / RUINS
- r11 START (21:30): brief = SY-1936 pre-fire + fire/aftermath variant, SY-RUINS (terraces, sphinxes, stairs, foundations, towers dated), matched storyboard cameras + before/after sheets; optional Alhambra lace + brighter 0108.
- New `scripts/states.py` (exec'd at end of build.py). SY_STATE → root collection:
  EARLY `SY-EARLY_c1856` | POST66 `SY-POST66_c1868` | 1936 `SY-1936_Nov1936_preFire` | FIRE `SY-1936FIRE_30Nov1936_night` | AFTER `SY-1936AFTER_Dec1936_morning` | RUINS `SY-RUINS_c1937-40` | RUINS41 `SY-RUINS_post1941`.
- All states: terrace sphinxes (6) + side flights (x=±528) in `SY54_terrace_sphinxes_and_side_flights__1854_extant`. 1936/FIRE/AFTER: Baird mast on south tower. FIRE: central transept deleted → collapse pile + glowing debris, volumetric flames (SY_FLAME, default 1.5), 19 smoke objects, night world. AFTER: shell removed, 2600-member collapsed ironwork field, north fragment, smoulder, low east sun + haze. RUINS: footing pads, towers in dated sub-collections (south: dismantled autumn 1940–1941; north: demolished 16 Apr 1941). RUINS41: tower bases only.
- Build: `SY_STATE=<S> blender -b -P scripts/build.py -- rounds/sydenham-<s>-r11.blend` (1856, 1936, 1936fire, 1936after, ruins, ruins41; all < 10 MB).
- Checks (state-aware `checks/dimension_check.py`): `checks/r11_<s>.txt` — 0 FAIL in all six (1856 19 PASS, 1936 20, fire 18, after 12, ruins 13, ruins41 9).
- Renders: `renders/r11_<state>_<cam>.png` 960×540, 32 spp.
- 22:15 r11b: `rounds/sydenham-1856-r11b.blend` built with Alhambra geometry lace (SY_LACE=1 default, courts.py arch_screen: 3 staggered rows of faceted lozenge studs following the arch outline, both faces). render.py accepts EXPO=<ev> per-render exposure override.
- 22:37 r11 renders complete (`renders/r11_*`, 31 PNG) and matched compare sheets: `compare/r11_CP057_states.jpg` (1936/FIRE/AFTER/RUINS), `r11_CP061_1936_vs_fire.jpg`, `r11_CP062_1936_fire_after.jpg` (+post-1941), `r11_CP001_1936_vs_fire.jpg`, `r11_CP064_skyline_states.jpg` (5 states), `r11_CP072_after_vs_ruins.jpg`, `r11_CP073_1856_vs_ruins.jpg`, `r11_CP059_1936_vs_fire.jpg`. Same cam/res/spp per sheet (960×540, 32 spp). Sheets: `python3 scripts/state_sheet.py out.jpg "title" 2 "label=path" ...`.
- In progress: r11b flames (one soft-masked emissive volume object per tongue, no hard cone silhouettes) → `rounds/sydenham-1936fire-r11b.blend`.
- 23:20 r11b DONE. FIRE flames → emissive surface tongues (facing-ratio core × stretched world noise × per-vertex `hfac` tip fade); per-object volume flames tried and abandoned (too slow). `rounds/sydenham-1936fire-r11b.blend` (SY_STATE=FIRE; `SY_FLAMEVOL=1` = r11 look). `checks/r11b_1936fire.txt` 0 FAIL. Renders `renders/r11b_1936fire_*` (6 cams); sheets `compare/r11b_CP057_states.jpg`, `r11b_CP061/CP059/CP001_1936_vs_fire.jpg`, `r11b_CP062_1936_fire_after.jpg` (supersede the r11 fire sheets).
- r11b Alhambra: geometry lace (`SY_LACE`, default on) in `rounds/sydenham-1856-r11b.blend`, `checks/r11b_1856.txt` 0 FAIL; 0108 at +0.2 EV: `RES=1080x1350 EXPO=0.2 blender -b rounds/sydenham-1856-r11b.blend -P scripts/render.py -- renders r11b_expo+0.2 100 64 CAM_compare_0108_alhambra` → `compare/r11b_alhambra_lace_vs_0108.jpg` (also −0.3 EV render kept).
- Next (not started): sphinx sculpt (currently ellipsoid blobs, I); AFTER stump colour reads timber; fire appliances/crowds MISS.

## r12 (23:00–) — sphinx, charred stumps, PPL-20C 1936 dressing
- `scripts/sculpt.py`: the metaball sphinx (recumbent lion body, nemes hull, plinth) replaces the ellipsoid blobs. `scripts/states.py` uses it for all 6 terrace sphinxes and adds the `iron_charred_black_1936` material for AFTER stumps and wreckage.
- `scripts/dress36.py` (exec'd from states.py for 1936/FIRE/AFTER):
  - LFB pumps (`pump_parade_00…`) and turntable ladders (`TL_*`, `TL_ladder_*`);
  - firemen, canvas hoses and water jets;
  - 1930s crowds (`crowd36_*`) and police lines on the Parade and terraces;
  - cameras CP058 and CP060.
- Rounds `rounds/sydenham-{1856,1936,1936fire,1936after,ruins}-r12.blend`, all under 16 MB. RUINS41 is unchanged since r11.
- Checks `checks/r12_*.txt` all have 0 FAIL:
  - fire 23 PASS;
  - after 16;
  - 1936 21;
  - ruins 14;
  - 1856 20.
  New r12 checks cover sphinx head height, pump/TL counts, pump length, police and crowd presence, and the charred material.
- Renders `renders/r12_<state>_<cam>.png` at 960×540 and 32 spp, run detached by `/workspace/syd_scratch/render_r12.sh`.
- 23:57 resume: r12b chain (CP058 camera moved inside the cordon, y 217) running detached: FIRE + 1936 rebuilt (0 FAIL), AFTER in progress. Dino branch clean at e1d59bb.
- r12b DONE: CP058 camera moved to (-310, 217) inside the cordon (press position, graded I). Rebuilt FIRE/1936/AFTER r12; checks 23/0, 21/0, 16/0. CP058 re-rendered for all three; compare/r12_CP058_1936_fire_after.jpg regenerated. r12 milestone committed locally (no push).

## r13 (00:05–) — CP045 Handel Festival 1857, Fine Arts courts II, CP042 waterworks running
- New `SY_STATE=CONCERT57` (root `SY-CONCERT57_HandelFestival_Jun1857`; the EARLY building with the north transept): `scripts/concert57.py` (orchestra amphitheatre, Gray & Davison organ, Costa rostrum, royal box, 2,424 performers, ~10,900 audience) + `scripts/people57.py` (Victorian-dress GN figures; 7 ft clear zone round cameras).
- `scripts/courts2.py` (EARLY + CONCERT57): Pompeian house, Greek/Roman segment, Mediaeval Court with Rochester door and stained glass; Muse props appended from `vendor/muse-*` (CREDIT.md per prop; unused una/fountain-basin copies dropped).
- `scripts/waterworks.py` (EARLY): fountains running (`SY56_waterworks_running__18Jun1856`), cascades, 2,417 visitors, CP042 cameras.
- Rounds `rounds/sydenham-1856-r13.blend` (18.4 MB) and `rounds/sydenham-concert57-r13.blend` (15.1 MB).
- Checks: `checks/r13_1856.txt` 25 PASS / 0 FAIL; `checks/r13_concert57.txt` 28 PASS / 0 FAIL (new: performer count, audience, organ/rostrum/royal box, dated tiers, orchestra width, the three courts, waterworks dated + visitors). `dimension_check.py` POST66 now excludes CONCERT57 (north transept present).
- Previews in `/workspace/syd_scratch/r13/` (c57b_sheet, e13a_sheet, b_sheet). Finals rendering detached at 1280×720/32 spp → `renders/r13_*` via `/workspace/syd_scratch/r13/render_r13.sh`.
- 01:04 r13 finals DONE: 18 renders `renders/r13_{concert57,1856}_*.png` (1280×720, 32 spp; Pompeian atrium/wall at +1.5 EV, presentation only). Sheets: `compare/r13_CP045_concert57.jpg`, `compare/r13_CP039_CP040_courts.jpg`, `compare/r13_CP042_waterworks.jpg`.
- Best: CP045 floor aisle 28 mm (organ, orchestra tiers, choir, audience) and CP042 terrace basin 35 mm (plume, veil, rim jets).
- Known misses for r14: gallery-level diagonal bracing crosses the CP045 gallery cameras and the CP040 Mediaeval Court view (pick new positions); the cascade reads as white steps more than water; Greek interior under-lit; Graces/Farnese not framed by any camera yet; the waterworks INFO line reports jet top vs main floor (64 ft), not jet height above the water.

## r14 (01:04–) — r14 fixes + SY-BUILD / SY54 / G-STATION / SY-LATE / SY-WAR
- Quick fixes: gallery + Mediaeval cameras moved off braces; Graces/Farnese 50 mm cams; Greek fill lights; jet-height check measures above water.
- New states via `scripts/eras.py` + `scripts/station.py`:
  - BUILD53 `SY-BUILD_c1853_construction` (CP033)
  - OPEN54 `SY54_OpeningDay_10Jun1854` (CP035) + Low Level station/covered way (CP036)
  - LATE11 `SY-LATE_FestivalOfEmpire_1911` (CP049–53)
  - WAR `SY-WAR_HMS_CrystalPalace_c1915` (CP056)
- people57: navvy / courtier / queen / yeoman / Edwardian / rating templates (indices after conductor unchanged).
- Rounds (all < 20 MB, no `.blend1`, no push):
  - `rounds/sydenham-build53-r14.blend` (2.4 MB)
  - `rounds/sydenham-open54-r14.blend` (14.7 MB)
  - `rounds/sydenham-1856-r14.blend` (18.4 MB)
  - `rounds/sydenham-concert57-r14.blend` (15.1 MB)
  - `rounds/sydenham-late11-r14.blend` (13.4 MB)
  - `rounds/sydenham-war-r14.blend` (13.3 MB)
- Checks `checks/r14_*.txt` all 0 FAIL: BUILD53 13P, OPEN54 27P, EARLY 29P, CONCERT57 30P, LATE11 25P, WAR 24P.
- Renders 1280×720 / 32 spp detached via `/workspace/syd_scratch/r14/render_r14.sh` → `renders/r14_*`.
- Renders DONE: 26 PNG at 1280×720 / 32 spp → `renders/r14_{build53,open54,1856,concert57,late11,war}_*.png`.
- Sheets: `compare/r14_CP033_build53.jpg`, `r14_CP035_opening.jpg`, `r14_CP036_station.jpg`, `r14_CP040_courts_fix.jpg`, `r14_CP045_concert_fix.jpg`, `r14_CP049_CP053_late.jpg`, `r14_CP056_war.jpg`.
- Best: CP035 procession nave 28 mm (opening crowds, yeomen, banners, vault) and CP036 platform arrival 28 mm (station shed, train, visitors).
- Misses: 1913 national purchase not modelled; pavilion forms U; All-Red Route path I; White Ensign is banded approximation; BUILD53 outdoor dressing reads thin from some cams (tramway/spoil present on slope-up); opening crowd ~8k of ~40k; cascade look still from r13.
- Local commit ee5b670 (rounds + scripts + BUILD53 renders); renders/sheets follow-up commit. NOT pushed.

## r15 (2026-10-27) — SY60 + SY-CLEARANCE; park-modern spun out
- `SY_STATE=SY60` → High Level station + patterned brick subway under the Parade (CP046). Round `sydenham-sy60-r15.blend` (~9 MB). Check `r15_sy60.txt` 0 FAIL.
- `SY_STATE=CLEARANCE` → late-1930s scrap gangs, cranes, lorries on the RUINS plateau (CP063). Round `sydenham-clearance-r15.blend` (~5.6 MB). Check `r15_clearance.txt` 0 FAIL.
- Park modern work moved to branch `grok-park-modern` / folder `crystal-palace-park-modern-grok` (PARK54/PARK60/PARK-NOW).
- NOT pushed.

## r15b checkpoint (2026-10-27 02:14 UTC)
- Rebuilt SY60 + CLEARANCE after subway lights + approach cam fix.
- Checks: r15_sy60 / r15_clearance — 0 FAIL.
- Renders: r15_sy60 CP046 ×4, r15_clearance CP063 ×4 (re-render).

## Checkpoint crystal-palace-sydenham-1856-grok quality round
- Patched scripts for quality pass; rebuilds pending lean hero renders.

## r16 (2026-10-27) — quality + coverage fill
- EARLY `sydenham-1856-r16.blend` (~18.5 MB): waterworks + CP037/CP044 coverage.
- LATE11 `sydenham-late11-r16.blend` (~13.5 MB): CP051/052/054.
- OPEN54 `sydenham-open54-r16.blend` (~15 MB): densified crowds ~38k.
- Lean heroes 1280×720 / 28 spp → `renders/r16/r16_CAM_CP{037,042,044,035,051,052,054}_*.png`.
- Soft cam-block hints: none on park; 7 ft clear zone kept.
- Local commit. NOT pushed.

## r17 WEAK→OK quality (in progress 2026-10-27 03:46 UTC)
- Targets: CP058/062/063/064 (AFTER/RUINS/CLEARANCE).
- Cam/dress: denser AFTER pumps; elevated tower cams; clearance crane FG scrap; horizon_fill berm + Nishita aerosol (kill blue band).
- Rounds: sydenham-{1936after,ruins,clearance}-r17.blend. Lean heroes r17*/r17d*/r17i*.
- NOT pushed.

## r17j checkpoint (2026-10-27 04:00 UTC)
- Horizon: taller stepped berms + heavier Nishita aerosol on RUINS/CLEARANCE (no shared look preset).
- Rebuild+lean re-render CP062/063/064 in flight.
- CP058 r17i kept (crowd+tower+appliances).
- NOT pushed.

## r17 WEAK→OK done (2026-10-27 04:22 UTC)
- CP058/062/063/064 promoted ≥7 (pixel judgment). Heroes r17i/r17q. Horizon haze card; no shared look preset. Local commit. NOT pushed.

## 2026-11-01 reference intake CANDIDATES (Muse, origin/main a62ba2e) — not promoted, no keep/revert call
Live `rounds/sydenham-1856-r16.blend` untouched (md5 1b984fb6…). Script `scripts/intake_muse_1101.py` → `rounds/candidates/sydenham-1856-r16-muse-courts.blend`.
Vendored unmodified: `vendor/muse-alhambra-lion-fountain/` (+ `textures/fascia_band.png`, packed into the candidate), `vendor/muse-assyrian-lamassu/` (CREDIT.md each).
- **CP041 lion fountain**: grok `al_lions` + `al_lions_jet` hidden; Muse fountain instanced at their centre (161.04, 25.60 m, floor 0.09 m) in `SY56_alhambra_lion_fountain_muse__dated_c1856` (cp_state SY-EARLY_c1856). Court water kept.
  Pairs `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP041_muse_lion_fountain_{alhambra_hold,alhambra_entry}_pair.jpg`.
  Muse fountain is much larger than ours (3.6 m footprint vs 2.2 m) and dominates the hold shot; its lions read as rounded/cartoon-like at this distance.
- **CP037 lamassu**: 4 Muse lamassu on the Nineveh Court nave facade per plan 0205 no. 27 (x 683/696 and 722/735 ft, y 60.5 ft, heads toward the entrance at x ≈ 709 ft), in `SY54_court_nineveh_lamassu_muse__1854_lost1866` (opened 1854, lost in the Dec 1866 north-end fire).
  The Nineveh Court architecture is NOT modelled, so the bulls stand free in the north nave.
  `CAM_CP037_taller_nave_28mm` shows NO visible change (it looks up into the vault, ~250 m away): pair `…/CANDIDATE_CP037_muse_lamassu_taller_nave_pair.jpg`.
  Added candidate camera `CAM_CP037_nineveh_facade_28mm` (eye 1.6 m, no roll) to make them judgeable: pair `…/CANDIDATE_CP037_muse_lamassu_nineveh_facade_pair.jpg`. Before = live r16 + that camera only (temp blend outside the repo).
- Renders: 1280×720, 28 spp, blend lighting, no people env. Live `renders/candidates/live_20261101/r16live_*.png`, candidate `renders/candidates/muse_courts_*.png`.
- COVERAGE oddity: CP041 is listed against `sydenham-clearance-r15.blend` / `r08bfinal_…insert_spandrel_50mm.png`, but the CP041 Alhambra cameras live in EARLY r16.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## 2026-11-01 Muse intake: Grok Bot review
- All Muse intake candidates REJECTED after viewing the pairs (see survey look/pairs_geo/README.md). Live blends unchanged; candidate files kept for reference.

## 2026-11-13 CP044 railway-entrance admission CANDIDATE — not live, no verdict
Resume notes: /workspace/tmp/cp044/PROGRESS.md. Live `rounds/sydenham-1856-r16.blend` untouched (1b984fb6).
- Why CP044: weakest live frame on the Sydenham contact sheets — the nave "pay desks" sit inside the palm-garden tubs (ray probe: PLACEHOLDER_nave_tubs, black-faced slab), two dark stand-ins, no gate or family; storyboard wants a family at an admission point (no tariff) + staff tending plants / repairing glazing.
- Script `scripts/candidate_cp044_railway_entrance.py` (on live r16) -> `rounds/candidates/sydenham-1856-r16_cp044gate.blend` (70f5ef98). Dated collection `SY56_railway_entrance_admission__c1856`.
  Plan 0205 "ENTRANCE FROM RAILWAY STATION" cross at the end of the South Wing (98 x 48 ft arms, 48 ft neck/stub, glazed), the wing staircase drawn just north of it (side flights, landing, central flight to an upper floor at zb+18), admission barrier with 3 cast-iron turnstiles, closed centre gate, 2 oak pay boxes with blank fascia boards, collector's desk; family of four at the left turnstile (backs to lens), money-taker, collector, 10 visitors, glazier on a ladder with a pane, gardener with a can, 10 orange tubs. DEPARTURES D-SY-CP044-01..18.
  CAM_CP044_pay_desks_35mm MOVED (reframe) to the entrance; new CAM_CP044_maintenance_50mm. Old nave desks left in place.
- Render chain `scripts/render_cp044_candidate.sh` (live recipe render.py PEOPLE_ERA=1850s SEED=81, 1920x1080 48 spp, both sides) -> `renders/candidates/cp044_gate_20261113/` (md5.txt). Before-side helper `scripts/cp044_link_cams.py` (candidate cameras into live r16, in memory).
- Mean luma: pay_desks live 58.08 -> 139.11 (reframe; same-camera before 198.91 = empty glazed wing end); maintenance same-camera 200.35 -> 153.34; side effect CP064_skyline (r16 only) 207.46 -> 207.45.
- Side effects: visibility test over all r16 cameras -> only CAM_CP064_skyline_50mm sees the change (live CP064 hero is on ruins-r17, so no live effect); CP037/CP041/CP042 r16 heroes: none. Rebuild from script = candidate, max diff 0 over all 48 cams (320x180).
- Live hero note: the r16 CP044 hero (Oct 27, people v3.1) no longer re-renders byte-exact (people_lib now v3.4: mean diff 0.51), so the "before" is the current recipe.

## 2026-11-13 16:30 UTC — CP063 clearance CANDIDATE (in progress, no verdict)
- Scene picked: CP063 "Reassembly is no longer an option" (weakest remaining: crane_lift hero reads as giant orange crates + cone men).
- Live round untouched: `rounds/sydenham-clearance-r17.blend` (md5 055ef338). Candidate script `scripts/candidate_cp063_scrap_clearance.py` -> `rounds/candidates/sydenham-clearance-r17_cp063scrap.blend`.
- Renders: `scripts/render_cp063_candidate.sh` (resumable per PNG) -> `renders/candidates/cp063_scrap_20261113/{before,after}`; log `/workspace/logs/cp063_scrap_render.log`.
- Departures D-SY-CP063-01.. in DEPARTURES.md. Do not promote; parent views the pairs.
- 16:25 UTC: candidate built `rounds/candidates/sydenham-clearance-r17_cp063scrap.blend` (md5 5ec53dd9); dated collection `SY37_clearance_scrap_sorting_remnant__1937`; 56 rust boxes + 28 cone stand-ins hidden (not deleted). Last standing central-transept bay (x=-60, y 36..60; 8 in x 18'11 3/4" columns, 3 x 23'3 1/4" trellis girder) racked 9 deg, 2 ropes to 9 haulers; sorted column/girder stacks on bearers, broken girder heap, cullet/ash/rib heaps, 42 low plateau piles; 17 people_lib 1930s men (nearest ~44 ft). DEPARTURES D-SY-CP063-01..10.
- Renders done (1920x1080 48 spp, render.py, blend lighting, NO_PEOPLE both sides; md5.txt): luma crane_lift 135.71->133.66 (33.6 % px changed); side effects scrap_gang 157.57->157.64 (2.4 %), clearance_perimeter 168.34->168.35 (0.03 %), terrace_edge 150.79->150.79 (none, max diff 1).
- Frustum test: no other live hero renders from clearance-r17 (CP062/CP064 live on ruins-r17, CP001/CP072 elsewhere), so side effects are limited to the 4 CP063 cams. Rebuild from script = candidate, max diff 0 (4 cams, 320x180).
- Survey pairs `look/pairs_geo/CANDIDATE_CP063_*`. COVERAGE CP063 row unchanged. NOT promoted, no verdict. Untracked s67c files in this folder are not mine; left alone.

## 2026-11-13 16:35 UTC — CP063 clearance KEEP (scoped promotion, in progress)
- Verdict (parent viewed the pairs): KEEP for CAM_CP063_crane_lift_50mm only; side effects scrap_gang, clearance_perimeter, terrace_edge REJECTED (stay on live `rounds/sydenham-clearance-r17.blend`, 055ef338, unchanged).
- Tag `pre_cp063scrap_keep` (local only). `rounds/sydenham-clearance-r18_cp063.blend` = byte copy of the candidate (md5 5ec53dd9ce456a7cb2ae22533dcf4f23).
- Routed only CAM_CP063_crane_lift_50mm in `scripts/sydenham_live_heroes.json`; live recipe `scripts/render_cp063_scrap_live.sh` (render.py, NO_PEOPLE=1, blend lighting, 1920x1080 48 spp) -> `renders/r18/r18_clearance_CAM_CP063_crane_lift_50mm.png`.
- Background chain (nohup): live render log `/workspace/logs/cp063_keep_live.log`, then `--rebuild /workspace/tmp/cp063_keep_rebuild` log `/workspace/logs/cp063_keep_rebuild.log` (ends ALLDONE). Baseline md5s of rounds/heroes: `/workspace/tmp/cp063_keep_baseline_md5.txt`.
- 16:50 UTC DONE: live hero `renders/r18/r18_clearance_CAM_CP063_crane_lift_50mm.png` (1920x1080) pixel-identical to candidate after (max diff 0); `--rebuild` from clearance-r17 (CP063 SAVED, 27 objects in `SY37_clearance_scrap_sorting_remnant__1937`) max diff 0. All 237 baseline md5s (rounds/*.blend, renders/*.png, renders/r16, renders/r18) unchanged incl. clearance-r17 055ef338 and r18_cp044 70f5ef98; pre-keep hero `renders/r17q_clearance_CAM_CP063_crane_lift_50mm.png` kept.

## 2026-11-13 18:15 UTC — CP056 RND nave drill CANDIDATE (in progress, no verdict)
- Scene picked: CP056 "From excursionists to recruits" (weakest remaining: the nave_drill_gallery hero is 27 % one placeholder tree blob + a block of cone ratings with orange poles).
- Live round untouched: `rounds/sydenham-war-r14.blend` (md5 718c4b3d). Candidate script `scripts/candidate_cp056_rnd_nave_drill.py` -> `rounds/candidates/sydenham-war-r14_cp056rnd.blend`.
- Renders: `scripts/render_cp056_candidate.sh` (resumable per PNG) -> `renders/candidates/cp056_rnd_20261113/{before,after}`; log `/workspace/logs/cp056_rnd_render.log`. Resume notes `/workspace/tmp/cp056/PROGRESS.md`. Tag pre_cp056rnd_cand (local).
- Departures D-SY-CP056-01.. in DEPARTURES.md. Do not promote; parent views the pairs.
- 18:35 UTC candidate `rounds/candidates/sydenham-war-r14_cp056rnd.blend` (md5 0a431fc8); dated collection `SY15_rnd_depot_nave_drill_mess__1915`. 49 nave planting placeholders + nave statues hidden (not deleted); 160 r14 nave cone points removed from a copy of the ppl15 mesh; 9 squads (223 people_lib `1890s_sailor` figures incl. PO + LS each, no rifles), canvas mess screens on the garden-side aisle (x -330..-90, every third bay open), 22 mess tables + forms, 6-man mess party. DEPARTURES D-SY-CP056-01..09.
- Renders done (1920x1080 48 spp, render.py, blend lighting, NO_PEOPLE both sides; md5.txt): luma nave_drill_gallery 72.16->83.05 (45.5 % px changed); side effects CP059_nave_fire 57.34->63.90 (war-r14 only; live CP059 hero is on 1936fire-r11b), nave_interior_28mm 55.26->61.17 (utility cam), ext_elevated_overview 194.30->194.30 (0.17 % px, through-glass speckle), CP056 terrace_drill 201.71->201.68 (0.08 % px, through-glass), CP056 ranks 161.43->161.43 (none, max diff 2).
- Frustum/occlusion test /workspace/tmp/cp056/vis.py over all 31 war-r14 cams; section_cut_x-300 / plan_overlay_top / compare_0108 also see it (diagnostic cams, not rendered). Rebuild from script = candidate, max diff 0 (6 cams, 320x180). Edge/size check: no figure cut by the hero frame, max 10.6 % frame height, nearest ~88 ft.
- Survey pairs `look/pairs_geo/CANDIDATE_CP056_*`. COVERAGE CP056 row unchanged. NOT promoted, no verdict. Untracked s67c files left alone.

## 2026-11-13 18:40 UTC — CP056 RND nave drill KEEP (scoped promotion)
- Verdict (parent viewed the pairs): KEEP for CAM_CP056_nave_drill_gallery_28mm only (placeholder tree gone, squads read clearly, matched lighting). Side effects CP059_nave_fire (war round), nave_interior_28mm (utility), ext_elevated_overview, CP056 terrace_drill, CP056 ranks REJECTED / not routed (stay on live `rounds/sydenham-war-r14.blend`, 718c4b3d, unchanged).
- Tag `pre_cp056rnd_keep` (local only). `rounds/sydenham-war-r15_cp056.blend` = byte copy of the candidate (md5 0a431fc86bfe047d66277e53d24f4233, cmp identical).
- Routed only CAM_CP056_nave_drill_gallery_28mm in `scripts/sydenham_live_heroes.json`; live recipe `scripts/render_cp056_rnd_live.sh` (render.py, NO_PEOPLE=1, blend lighting, 1920x1080 48 spp; checks collection `SY15_rnd_depot_nave_drill_mess__1915`, 234 objects) -> `renders/r18/r18_war_CAM_CP056_nave_drill_gallery_28mm.png`.
- Logs `/workspace/logs/cp056_keep_live.log`, `/workspace/logs/cp056_keep_rebuild.log` (ALLDONE). Baseline md5s `/workspace/tmp/cp056_keep_baseline_md5.txt` (244 files: rounds/*.blend + renders/**/*.png excl. candidates and untracked s67c dirs).
- DONE: live hero (1920x1080) pixel-identical to candidate after (max diff 0); `--rebuild` from war-r14 (CP056 SAVED) max diff 0. All 244 baseline md5s unchanged (incl. war-r14 718c4b3d, r18_cp044 70f5ef98, clearance-r18_cp063 5ec53dd9); only new files are the round and the hero. Pre-keep hero `renders/r14_war_CAM_CP056_nave_drill_gallery_28mm.png` kept. Survey COVERAGE CP056 row -> war-r15_cp056 / r18 hero (fixes the old clearance-r15 round mismatch). s67c files, pyc change left alone.

## 2026-11-13 20:05 UTC — CP060 hose crews CANDIDATE (not live, no verdict)
- Scene: CP060 "Water cannot save the whole building" (30 Nov 1936, SY36 external fire response), camera `CAM_CP060_crowd_watching_35mm` (not moved).
- Weakness picked: the COVERAGE hero `renders/r12_1936_CAM_CP060_crowd_watching_35mm.png` is the pre-fire DAYLIGHT 1936 round (intact palace, flat green ground, no fire, no firemen); the fire-state render of the same camera (`rounds/sydenham-1936fire-r12.blend`) is a wall of dark lathe-crowd backs in the foreground with no hose, crew or jet readable. The COVERAGE row also lists `rounds/sydenham-clearance-r15.blend`, not the round the hero came from.
- Candidate `rounds/candidates/sydenham-1936fire-r12_cp060hose.blend` (md5 dccd2c62ea85f2aa742d364507a9a67a) = `scripts/candidate_cp060_hose_crews.py` on fire-r12 (33102f4b, unchanged). Dated collection `SY36_parade_hose_crews__30Nov1936`: 34 `crowd36_parade` blocks in the CP060 frustum < 330 ft and `police_line_parade` hidden (not deleted, prop `cp060_hidden_by_candidate`); wet Parade plane with noise puddles reflecting the fire; 3 branch crews of 3 people_lib v3.4 `1930s_fireman` (~101-124 ft from the lens) + hose runner + officer; 3 charged 2 3/4 in hoses running from below the frame to the branches, 4 slack lines; brass branches; jets as core stream + widening spray, 70-85 ft throw, falling short of the burning front (low pressure). Flames NOT changed (still r11b cone tongues).
- DEPARTURES D-SY-CP060-01..08. Rebuild from the script is deterministic (object/curve/mesh hash identical, /workspace/tmp/cp060/hash.py).
- Renders `scripts/render_cp060_candidate.sh` (render.py, NO_PEOPLE=1, blend lighting fire-r12 Filmic -0.5 EV, 1920x1080 48 spp, same camera both sides) -> `renders/candidates/cp060_hose_20261113/{before,after,livehero}/` + md5.txt. Hero luma 39.02 -> 45.44 (23.8 % px changed). `livehero/` = the COVERAGE daylight state (1936-r12, -1.0 EV) at the same res/spp, context only, NOT exposure-matched (luma 177.11).
- Side-effect cams (frustum test; occluded garden-side cams not rendered): CP058 parade_appliances and CP061 transept_collapse on fire-r12. No live hero renders from fire-r12 (CP058 live = 1936after-r17, CP059/CP061 live = 1936fire-r11b), so no live hero changes.
- Survey pairs `look/pairs_geo/CANDIDATE_CP060_*`. COVERAGE CP060 row unchanged. NOT promoted. Untracked s67c files and the pyc change left alone.
- 22:21 UTC render chain DONE (`renders/candidates/cp060_hose_20261113/DONE`, md5.txt): luma CP060 crowd_watching 39.02->45.46 (25.9 % px >2); side effects (fire-r12 only) CP058 parade_appliances 36.69->42.72 (38.7 % px), CP061 transept_collapse 63.55->63.56 (0.2 % px).

## 2026-11-13 22:15 UTC — CP060 hose crews KEEP (scoped promotion)
- Verdict (parent viewed the hero pair `look/pairs_geo/CANDIDATE_CP060_hose_crews_crowd_watching_*`): KEEP for CAM_CP060_crowd_watching_35mm ONLY. Side effects CP058 parade_appliances and CP061 transept_collapse (fire-r12 views) REJECTED / not routed; they stay on their current live rounds (CP058 `rounds/sydenham-1936after-r17.blend`, CP061 `rounds/sydenham-1936fire-r11b.blend`). `rounds/sydenham-1936fire-r12.blend` (33102f4b) unchanged.
- Tag `pre_cp060hose_keep` (local only, on the CANDIDATE commit fffbbd3). `rounds/sydenham-1936fire-r13_cp060.blend` = byte copy of the candidate (md5 dccd2c62ea85f2aa742d364507a9a67a, cmp identical).
- Routed only CAM_CP060_crowd_watching_35mm in `scripts/sydenham_live_heroes.json`; live recipe `scripts/render_cp060_hose_live.sh` (render.py, NO_PEOPLE=1, blend lighting fire-r12 Filmic -0.5 EV = candidate exposure, 1920x1080 48 spp; checks collection `SY36_parade_hose_crews__30Nov1936`, 28 objects) -> `renders/r18/r18_fire_CAM_CP060_crowd_watching_35mm.png`.
- Logs `/workspace/logs/cp060_keep_live.log`, `/workspace/logs/cp060_keep_rebuild.log` (ALLDONE). Baseline md5s `/workspace/tmp/cp060_keep_baseline_md5.txt` (246 files: rounds/*.blend + renders/**/*.png excl. candidates and untracked s67c dirs).
- DONE: live hero (1920x1080) pixel-identical to candidate after (max diff 0); `--rebuild` from fire-r12 (CP060 BUILT crews 3 men 11 hoses 7 jets 3; SAVED) max diff 0. All 246 baseline md5s unchanged (incl. fire-r12 33102f4b, 1936after-r17, 1936fire-r11b, war-r15_cp056 0a431fc8); only new files are the round and the hero. Pre-keep hero `renders/r12_1936_CAM_CP060_crowd_watching_35mm.png` (pre-fire daylight) kept. Survey COVERAGE CP060 row -> 1936fire-r13_cp060 / r18 hero (fixes the old clearance-r15 round mismatch). The candidate render chain finished incl. the CP061 'after' side effect (22:21 UTC). s67c files, pyc change left alone.

## 2026-11-14 00:50 UTC — CP051 1903 SMMT motor show CANDIDATE (not live, no verdict)
- Chosen: CP051 electric nave (r16 hero had no exhibit: blob placeholder tree over the right third, palm-trunk placeholder 13 ft from the lens, gold 'tech cabinet' boxes, a stray cone-skirt figure 11 ft from the lens from duplicated crowd points). Storyboard asks for a dated electrical/motor exhibit.
- `scripts/candidate_cp051_motor_show.py` on live `rounds/sydenham-late11-r16.blend` (3ce48caf, unchanged) -> `rounds/candidates/sydenham-late11-r16_cp051motor.blend` (579800c4). Collection `SY03_smmt_motor_show_nave__1903` (30 Jan - 7 Feb 1903, Grace's Guide): 18 stands on 9 west-nave bays with blank name boards, 35 generic 1903 vehicles (19 tonneaux, 11 voiturettes, 5 bare chassis), 66 people_lib figures (1890s stand-in), nearest ~70 ft. Hidden (not deleted): 19 west-nave planting placeholders, 1911/1913 flags, r16 cabinets (mesh copy). 44 stray duplicated nave points removed from mesh copies of the 3 LATE11 crowds. Cameras not moved. DEPARTURES D-SY-CP051-01..10.
- Renders `scripts/render_cp051_candidate.sh` (render.py, NO_PEOPLE=1, blend lighting Filmic -1.0 EV, 1920x1080 48 spp, same camera both sides) -> `renders/candidates/cp051_motor_20261114/{before,after}/` + md5.txt. Hero luma 68.71 -> 71.83 (43.2 % px changed).
- Side effects (late11-r16 views; NOT for routing): CP052 scaffold_reglaze 150.03->150.00 (1.3 % px, stands faint through glass), CP054 plymouth_rescue 188.56->193.24 (1913 flags gone: REJECT), CP049 worn_garden_front 172.53->174.76 (flags gone: REJECT), nave_interior 62.78->69.64, CP059_nave_fire (late11 round, no live hero) 62.53->69.42.
- Rebuild from the script into /workspace/tmp/cp051/rebuild.blend: CP051 render max diff 0 (blend bytes differ by save metadata only). 254 baseline md5s (rounds/*.blend + renders/**/*.png excl. candidates) unchanged. `scripts/sydenham_live_heroes.json` not edited. Suggested tag on KEEP: pre_cp051motor_keep. Untracked s67c files and the pyc change left alone.

## 2026-11-14 02:05 UTC — CP051 1903 SMMT motor show KEEP (scoped promotion)
- Verdict (parent viewed the hero pair `look/pairs_geo/CANDIDATE_CP051_*`): KEEP for CAM_CP051_electric_nave_28mm ONLY. Side effects CP052 scaffold_reglaze, CP054 plymouth_rescue and CP049 worn_garden_front (1911/1913 flags hidden), nave_interior and CP059_nave_fire (late11 round) REJECTED / not routed; they stay on `rounds/sydenham-late11-r16.blend` (3ce48caf, unchanged; live CP059 hero stays on its 1936fire round).
- Tag `pre_cp051motor_keep` (local only, on the CANDIDATE commit 12af85d). `rounds/sydenham-late11-r17_cp051.blend` = byte copy of the candidate (md5 579800c4f5515f6a5710b306b04b108f, cmp identical).
- Routed only CAM_CP051_electric_nave_28mm in `scripts/sydenham_live_heroes.json`; live recipe `scripts/render_cp051_motor_live.sh` (render.py, NO_PEOPLE=1, blend lighting late11-r16 Filmic -1.0 EV = candidate exposure, 1920x1080 48 spp; checks collection `SY03_smmt_motor_show_nave__1903`, 86 objects) -> `renders/r18/r18_late11_CAM_CP051_electric_nave_28mm.png`.
- Logs `/workspace/logs/cp051_keep_live.log` (LIVEDONE), `/workspace/logs/cp051_keep_rebuild.log` (ALLDONE). Baseline md5s `/workspace/tmp/cp051_keep_baseline_md5.txt` (248 files: rounds/*.blend + renders/**/*.png excl. candidates and untracked s67c dirs).
- DONE: live hero (1920x1080) pixel-identical to candidate after (max diff 0); `--rebuild` from late11-r16 (CP051 BUILT people 66; SAVED) max diff 0. All 248 baseline md5s unchanged (incl. late11-r16 3ce48caf, 1936fire-r13_cp060 dccd2c62, war-r15_cp056 0a431fc8); only new files are the round and the hero. Pre-keep hero `renders/r16/r16_CAM_CP051_electric_nave_28mm.png` kept. Survey COVERAGE CP051 row -> late11-r17_cp051 / r18 hero. s67c files, pyc change left alone.

## 2026-11-16 ~11:55 UTC — CP001 glow on the hill CANDIDATE (not live, no verdict)
- `scripts/candidate_cp001_glow.py` on live `rounds/sydenham-1936-r18b.blend` (66edd7cd, unchanged; the blend the live hero `renders/r18_1936_CAM_CP001_prologue_distant_35mm.png` was rendered from) -> `rounds/candidates/sydenham-1936-r18b_cp001glow.blend` (md5 a348d5481c61c8aa9fade71ff39b463a). Dated collection `SY36_prologue_glow__30Nov1936_c1945` (30 Nov 1936 c.7:45 pm, pre-collapse): night world + faint east moonlight, 126 emissive flame tongues + 9 interior lights inside the central transept / south nave (glass intact, collapse withheld), 20-puff smoke column leaning SE, 64 people_lib 1930s spectators; lost-1866 north transept stub and south-basin silt plane hidden (not deleted). Camera not moved, exposure unchanged (Filmic -1.0 EV). DEPARTURES D-SY-CP001-01..11.
- Renders `scripts/render_cp001_candidate.sh` (render.py, NO_PEOPLE=1, KEEP_LIGHTING=1, 1280x720 = live hero resolution, 48 spp, same camera both sides) -> `renders/candidates/cp001_glow_20261116/{before,after}/` (19 cams) + md5.txt + DONE. Hero luma (Rec.709) 206.52 -> 18.12.
- Side effects (1936-r18b views; none has a live hero on that round; NOT for routing): every other camera in the round turns night (e.g. CP062 211.67->22.16, CP064 211.71->19.13, CP057 191.89->48.91, CP059 74.05->160.44, CP072 noise).
- Built by the failed 09:54 run, left uncommitted; committed now on the parent's verdict. Untracked s67c files and people_lib edits left alone.

## 2026-11-16 ~12:15 UTC — CP001 glow on the hill KEEP (scoped promotion)
- Verdict (parent viewed the hero pair `look/pairs_geo/CANDIDATE_CP001_*`): KEEP for CAM_CP001_prologue_distant_35mm ONLY. The 18 other 1936-r18b cameras in the pair folder (whole round turns night) REJECTED / not routed; they stay on their current live rounds; `rounds/sydenham-1936-r18b.blend` (66edd7cd) unchanged.
- Tags (local only): `pre_cp001glow_cand` on 84e7ee7, `pre_cp001glow_keep` on the CANDIDATE commit aeeb6ef. `rounds/sydenham-1936-r19_cp001glow.blend` = byte copy of the candidate (md5 a348d5481c61c8aa9fade71ff39b463a, cmp identical).
- Routed only CAM_CP001_prologue_distant_35mm in `scripts/sydenham_live_heroes.json`; live recipe `scripts/render_cp001_glow_live.sh` (render.py, NO_PEOPLE=1, KEEP_LIGHTING=1, Filmic -1.0 EV = candidate exposure, 1280x720 48 spp; checks collection `SY36_prologue_glow__30Nov1936_c1945`, 94 objects) -> `renders/r18/r18_1936glow_CAM_CP001_prologue_distant_35mm.png` (md5 6d177a3f27a02fc76e235efd77fb3d31).
- Logs `/workspace/logs/cp001_keep_live.log` (LIVEDONE), `/workspace/logs/cp001_keep_rebuild.log` (ALLDONE). Baseline md5s `/workspace/tmp/cp001_keep/baseline_md5.txt` (400 tracked .blend/.png before the candidate commit).
- DONE: live hero pixel-identical to candidate after (max diff 0); `--rebuild` from 1936-r18b (CP001 BUILT tongues 126 lights 9 smoke 20 spectators 64; SAVED) max diff 0. All 439 tracked .blend/.png (400 baseline md5s + the 39 committed candidate files) unchanged; only new files are the round and the hero. Pre-keep hero `renders/r18_1936_CAM_CP001_prologue_distant_35mm.png` kept. Survey COVERAGE CP001 row -> 1936-r19_cp001glow / r18 hero. s67c files and people_lib edits left alone.

## 2026-11-16 ~22:40 UTC — CP033 slope works CANDIDATE (not live, no verdict)
- `scripts/candidate_cp033_slope.py` on live `rounds/sydenham-build53-r18b.blend` (dc579904, unchanged; the blend the live hero `renders/r18_build53_CAM_CP033_slope_up_35mm.png` was rendered from — before re-render pixel-identical, max diff 0) -> `rounds/candidates/sydenham-build53-r18b_cp033slope.blend` (md5 ebb75f7025abaa56359505c2f2452775). Dated collection `SY53_slope_works__autumn1853` (387 objects): works-ground overlay in the CAM_CP033 frustum (worked clay, cart tracks, wet patches, pasture remnants), centre cone heap replaced by grounded tip heaps + plank runs, 368 pv57 navvy points in the frustum re-placed as 336 people_lib 1850s navvies/workmen (+24 new: foreground gang with shovels/picks, barrows, 3 horse tip carts + carters, surveyor + staff man, masons), navvy dress recoloured, lower-terrace garden-front wall under construction for x 40-238 m (brick piers/alcoves, scaffolds, 2 shear-legs), placeholder tree 38 -> elm. Originals hidden, not deleted. Camera not moved, exposure unchanged (Filmic -1.0 EV). DEPARTURES D-SY-CP033-01..10.
- Renders `scripts/render_cp033_candidate.sh` (render.py, NO_PEOPLE=1, KEEP_LIGHTING=1, 1280x720 = live hero recipe, 48 spp, same camera both sides) -> `renders/candidates/cp033_slope_20261116/{before,after}/` (all 33 round cams) + md5.txt + luma.tsv + DONE. Hero luma (Rec.709) 202.00 -> 184.70 (42.6 % of pixels changed > 8 levels).
- Side effects (build53-r18b views; only CP033_slope_up is live from this round; NOT for routing): every cam changes a little because the people_lib figures replace pv57 points also inside the building (erectors) — largest: compare_0007 208.85->206.55 and ext_elevated_overview 197.52->194.97 (the overlay shows as a frustum-shaped dark patch), CP038 egyptian_hold 201.19->201.25 (near-lens figure swapped), CP038 entry 196.28->195.89, CP057 196.34->195.93, terrace_cut 208.96->208.51 (shear-legs on the horizon); the rest < 1.2 % pixels. Pairs for all in `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP033_slope_*` (`scripts/make_cp033_pairs.py`).
- Rebuild check: a second `candidate_cp033_slope.py` run from build53-r18b renders the hero pixel-identical to the candidate after (max diff 0).
- Untracked s67c fire-ruins candidate files left alone.
