# PROGRESS — hyde-park-site-1850-grok (branch grok-site-1850)

## Checkpoint s01 (2026-10-26)
- `scripts/build_site.py` → `rounds/s01.blend` (~35 MB): terrain, footpaths, Rotten Row, drive, 6 elms (3 exact transept), 183 park trees (summer/winter pairs), survey line/pegs/chain/poles/theodolite/staff, survey party + visitors + riders, CP007 committee model, CP008 design-study overlay, CP009 hoarding/stack/drawing table/engineer.
- Per-camera states via `grok_states` (CP006 winter, CP007 model, CP008 overlay, CP009 stacks).
- Preview fixes: overlay emission 6→1.6 (read white, now amber); label moved into the 28 mm frame; engineer and theodolite surveyor moved off table/tripod (F1); handed sheet moved to engineer's reach.
- D-checks `checks/s01_checks.json`: **25/25 pass**.
- Final renders `renders/s01/` (1920×1080, 96 spp), contact sheet.
- Self-score 7/10. Misses: background park trees are lollipop clumps; CP009 columns stand upright in a row (reads more "display" than "stack"); CP009_start foreman cuts the left edge as a dark block; CP006 winter trees bare-generic; Rotten Row riders are simplified horse+rider meshes, barely visible in any shot.

## Checkpoint s02 (2026-10-26)
- Site fix 1 only (Professor Bear): CP009 dray with a column being unloaded, horse, carter; workman_1 moved off the CP009_end sightline; CP009_end retargeted onto the horizontal columns on bearers.
- `rounds/s02.blend`; D-checks `checks/s02_checks.json`: **25/25 pass** (first build failed F1 carter vs dray by 0.05 ft; carter moved 0.7 ft south).
- Final renders `renders/s02/` (1920×1080, 96 spp) + contact sheet (`scripts/render_s02.sh`, detached).

## Next
1. ~~CP009 columns on bearers + cart~~ (s02 done).
2. Replace lollipop park trees with Muse/elm-card trees for the near 300 ft.
3. CP006: add frost/low sun haze; a few walkers on the footpath.
4. CP008: fade-in variant (overlay alpha ramp) for the edit.

## Backlog (parked by Professor Bear — diminishing returns)
- r11 transept polish, x07 exterior polish, d04 dismantle polish (HP-BUILD/transept/dismantle branches unchanged).

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP006/009; lib 3.1

## people v3.2 2026-10-27
- people v3.2: revert CP006/009

## s02 w02 (2026-10-27)
KEEP CP007: committee study model glass ridge roofs + drafting tools (compass/ink/quill/weight). Best path → `CP007_start` (end cam is tree insert, near-identity). Pair `look/pairs_geo/CP007_start_pair.png`.

## CP009 geo polish CANDIDATE "contract" (2026-11-04, NOT live — awaiting review)
`scripts/cand_cp009_contract_20261104.py` on live `rounds/s02.blend` (unchanged, md5 0a987ca7) → `rounds/candidates/s02_cp009contract.blend`; render `scripts/render_cp009_contract.sh` (1920×1080, 96 spp, --keep-lighting --no-people, exposure 0.68 / 0.22 luma-matched). Pairs `scripts/cand_cp009_contract_pairs.py` → survey `look/pairs_geo/CANDIDATE_CP009_contract_{start,end}_*`. DEPARTURES SD28–SD31. Luma start 123.52 → 123.21, end 120.44 → 120.29. Self-score 5/10.

## CP009 contract CANDIDATE v2 (2026-11-09, NOT live — awaiting review; v1 REJECTED)
v1 verdict: table, ground and hoarding better; people v3.4 figures regressed (bald grey heads, lost top hat/period dress, bare-foot read); after slightly washed. v2: `scripts/cand_cp009_contract_v2_20261109.py` on live `rounds/s02.blend` (unchanged, md5 0a987ca7) → `rounds/candidates/s02_cp009contract_v2.blend`; keeps SD28–SD30, withdraws SD31, new figures `scripts/c9_figures_v2.py` (SD32: HBM head + hair, modelled 1850 dress, top hat / wideawakes / caps that sit on the head, coats, waistcoats, neckwear, moleskin/cord trousers, laced boots), paler warmer deal (SD33), primer and earth albedo lifted (SD34). Render `scripts/render_cp009_contract_v2.sh` (1920×1080, 96 spp, --keep-lighting --no-people, exposure 0.29 / 0.06). Pairs `scripts/cand_cp009_contract_v2_pairs.py` → survey `look/pairs_geo/CANDIDATE_CP009_contract_v2_{start,end}_*`. Luma start 123.55 → 123.27, end 120.47 → 120.18. Self-score 6/10. Misses: start frame has less contrast than live (std 52 vs 71: no white table/figure), deal still reads cream-grey under the cool sky, mitten hands, generic faces with dark eye sockets, trodden earth a little mottled/dusty, hero workman stands stiffly.

## CP009 contract v2 KEEP → live s02 (2026-11-09)
Parent viewed the v2 pairs and KEPT them (1850-dress figures with hats/coats/boots, planked deal table, trodden earth; exposure matched). Promoted with `scripts/promote_cp009_contract_v2.sh`: copies the reviewed candidate `rounds/candidates/s02_cp009contract_v2.blend` (md5 4b36e87a, scene-identical to a rebuild from the pre-KEEP s02 0a987ca7 / git 870ad81) to live `rounds/s02.blend` (md5 → ab2d25d4) and tags `ST_C9_GROUND_WORN` with `cpl_not_ground`; re-renders live `renders/s02_png/CP009_{start,end}.png/.jpg` (1920×1080, 96 spp, --keep-lighting --no-people, exposure 0.29 / 0.06). `--rebuild` regenerates from pre-KEEP instead (scene-equivalent but ±1–3 levels on <0.1 % of pixels vs the reviewed afters, so the copy is the default).
Fixes carried: `c9_figures_v2.palette` skin tone used salted `hash(tag)` (drifted per process) → pinned SKIN_PIN table + crc32 fallback; `render_shots.py` look path hides `cpl_not_ground` objects from `crystal_palace_look`'s horizon-ground scan (the worn patch had lifted CPL_HorizonGround to 0.26 m — a pale disk over CP006–CP008).
Checks: live CP009 start/end vs KEEP afters max 0 / 0; keep-lighting regressions CP006–CP008 (7 shots, 32 spp 50 %) max 0; look path CP006–CP008 max 0,0,0,1,3,1,1 (≤152 px of 518k, pre-KEEP re-render noise floor 0; visible objects/transforms/materials/lights identical, pale-ground bug gone by eye). Self-score 6/10.

## CP006 polish CANDIDATE "winterpark" (2026-11-09, NOT live — awaiting review)
Why CP006: weakest phase-2 beat on a visual pass of the live renders not polished in the last week ("grass, paths and mature trees; surveyors mark a limited line" read as lollipop trees on a flat green with one blocky figure at the edge and the survey party out of frame).
`scripts/cand_cp006_winterpark_20261109.py` on live `rounds/s02.blend` (unchanged, md5 ab2d25d4) → `rounds/candidates/s02_cp006park.blend`. CP006-only: new objects W6_-prefixed and base-hidden; grok_states CP006 now shows W6_ and hides G_PARK*, PATH_SOUTH_FOOT, SVP_, SV_TOOL, CPL_HorizonGround; TR_W_ (CP006-only) trees re-meshed. DEPARTURES SD35–SD42.
Render `scripts/render_cp006_winterpark.sh [--no-build]` (1920×1080, 96 spp, --no-people; start --keep-lighting exposure 0.14, end look v1.1 exposure -0.50; each the recipe that reproduces its live frame, luma-matched). Log `/workspace/logs/cp006_winterpark_render.log`, ends `CP006_WINTERPARK_DONE`.
Pairs `python3 scripts/cand_cp006_winterpark_pairs.py` → survey `look/pairs_geo/CANDIDATE_CP006_winterpark_{start,end}_{before,after,pair}.png`.
Resume: if the after PNGs exist but no pairs, run the pairs script; if no after PNGs, rerun the render script with --no-build (candidate .blend kept). Then commit site (grok-site-1850) + survey (pairs) locally; no push, no promotion.

## CP006 winterpark KEEP → live s02 (2026-11-09)
Parent viewed the CANDIDATE pairs (survey 28230d6) and KEPT start and end: bare winter crowns replace the lollipop trees, the five-figure 1850 survey party is in frame, the pale slab is gone, exposure matched. Promoted with `scripts/promote_cp006_winterpark.sh`: byte copy of reviewed candidate `rounds/candidates/s02_cp006park.blend` (md5 fc771aba) over live `rounds/s02.blend` (ab2d25d4 → fc771aba; old live kept untracked at `rounds/s02.blend.pre_cp006park_keep`). Live `renders/s02_png/CP006_{start,end}.png/.jpg` re-rendered (1920×1080, 96 spp, --no-people; start keep-lighting 0.14, end look v1.1 -0.50).
Checks: live CP006 start/end vs KEEP afters max 0 / 0; live CP009 full-res at live recipe vs renders/s02_png max 0; pre-KEEP vs live CP007–CP009 (7 shots, 32 spp 50 %) keep-lighting and look paths all max 0. Self-score 6/10.
Remaining misses: start/end colour mismatch, blue-grey start grass, knee-cropped survey party on the end frame, stiff figures.
