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
