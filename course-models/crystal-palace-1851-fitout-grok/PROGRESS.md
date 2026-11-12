# PROGRESS: HP-FITOUT + HP51 (Grok Bot)

Branch `grok-fitout-1851` (worktree /workspace/crystal-palace-fitout). Local commits only; no push; Professor Bear reviews first.

- **f01 (2026-10-27), fitout state (CP018-CP020):**
  - Paint: 479 painted, 8 half, 313 primer. 14 painters, 2 ladders, 6 cradles.
  - Doors open, with a dray and trucks.
  - Floor: 18 Muse floor tiles and 32 loose boards; sweeper and hand-engine.
  - Checks: D 40/40, state 48/48. 8 renders.
- **h01 (2026-10-27), hp51 state (CP026-CP028):**
  - Shilling crowd 531/660 re-dressed. 4 turnstiles, 2 pay boxes, 3 police, queue of 140.
  - 6 stair visitors. 3 Muse louvres with a rope attendant. 3 watering attendants.
  - Checks: D 39/39, state 38/38. 6 renders.
- **c01 (2026-10-27), closing state (CP029):**
  - Dais, canopy, chair, 27 dais figures; 620 floor and 260 gallery spectators.
  - Autumn elms and an October sun.
  - Checks: D 35/35, state 15/15. 2 renders.
- **Exposure fix:** CP019_dray and CP026_shilling_ext re-rendered at exposure -0.7 (FT38).
- **Open / next:**
  - The CP028 louvre shot frames the wall below the Muse louvres: tilt it up or use 35 mm.
  - The CP029 gallery shot has a spectator in the left foreground: add a cam_conflict filter on gallery spawns.
  - Half-painted columns read faintly: make the paint cut a sharper band and add drips and drop cloths.
  - The CP019 doors shot needs more crates in transit.

## f02 / h02 / c02 (2026-10-27): quick fixes 1, 2, 4
- FT39 pale exterior timber/boarding tone; FT40 CP029 gallery foreground filter; FT41 CP028 louvre camera tilt.
- Parked as backlog: sharper half-paint bands with drips; workshop belts and shavings / shop lighting / loading-door view (fitout next 3 and 5).
- Checks: f02 40/40 dims + 48/48 state; h02 39/39 + 38/38; c02 35/35 + 15/15.
- Renders: renders/f02/CP019_dray_start; renders/h02/CP026_shilling_ext_start, CP028_louvre_start; renders/c02/CP029_gallery_start, CP029_dais_start.

## f03 / h03 / o01 (2026-10-27): quality + opening gap fill
- FT41 darker boarding albedo (material not exposure); FT42 hex fountain prisms + glass_solid sparkle; FT43 `--state opening` (CP021/CP022).
- Horse harness + darker coats in fitout. Checks: f03 40/40 + 48/48.
- Renders: f03/, h03/, o01/.

## em01 / dm01 (2026-10-27): HP-EMPTY + HP-DISMANTLE gap fill
- empty (CP030): crates replace exhibits.
- dismantle (CP031): shores, stacks, joint hero.
- DEPARTURES FT44–FT45.
- Checks: em01 state 19/19; dm01 state 15/15 (dims DRESS fails expected).
- Renders: renders/em01/CP030_*; renders/dm01/CP031_*.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP018-022/027; revert CP028; lib 3.1

## people v3.2 2026-10-27
- people v3.2 keep-lighting: keep CP020/CP021; revert CP018/019/022/027

## CP028 CANDIDATE (2026-10-27)
- **CP028 CANDIDATE:** `scripts/polish_cp028_cand.py` → `rounds/candidates/h03_cp028.blend` + `renders/candidates/CP028_louvre_start.png` (thick louvres/battens). Live `h03` untouched. Pair: survey `look/pairs_geo/CANDIDATE_CP028_louvre_start_pair.png`.

## Hero CANDIDATE CP022 Osler (2026-10-27)
- Audit: Osler fountain crudest vs screen time (CP022 hero; CP021/023 context) vs Muse articulated cut-glass.
- CANDIDATE: `scripts/polish_osler_cand.py` appends Muse `osler-crystal-fountain` (origin/main via models-main-ro; Wellcome-governed; credit on objects) → `rounds/candidates/o01_osler.blend` + `renders/candidates/CP022_fountain_start.png` (--keep-lighting). Live o01 / live render untouched.
- Pair: survey `look/pairs_geo/CANDIDATE_CP022_osler_fountain_start_pair.png`.
- CP014/CP028 candidates previously rejected by user; live left as-is (pairs renamed REJECTED_*).

## KEEP CP022 Osler live (2026-10-27)
- User KEEP on Muse append candidate. Promoted to live `rounds/o01.blend`; re-rendered CP021_doors/dais + CP022_fountain/crossing with `--keep-lighting`.
- Same append applied to transept `r11` for CP023 combine (exterior x07).
- CREDITS.md + DEPARTURES FT50.

## 2026-10-27 KEEP Osler
- Muse `osler-crystal-fountain` promoted live o01 (CP021/CP022 keep-lighting). CREDITS + DEPARTURES FT50. CP023 via r11.

## 2026-11-02 CANDIDATE CP028 louvre drive (live h03 untouched)
- `scripts/polish_cp028_drive_cand.py` → `rounds/candidates/h03_cp028_drive.blend` (FT51–FT54: one pulley Q + continuous shafting T, intermediate cranks at x=16/32 ft, stray blind laths removed, oiler on a pair of steps).
- `scripts/render_cp028_drive.sh [--rebuild]` → `renders/candidates/cp028_drive_20261102/{before,after}/CP028_louvre_start.png` (1280x720, 48 spp, --keep-lighting --no-people; the before is pixel-identical to live `renders/h03/CP028_louvre_start.png`).
- Survey pairs: `look/pairs_geo/CANDIDATE_CP028_drive_{before,after,pair,detail_pair}.png`. No verdict.
- **v1 REJECTED 2026-11-02** (parent viewed the pairs): the drive fix FT51–FT53 is right, but the oiler read as floating (steps' top at his waist, legs beside the steps, no foot on a tread). Survey pairs renamed `REJECTED_CP028_drive_v1_*`.

## 2026-11-02 CANDIDATE CP028 louvre drive v2 (FT54 restaged; live h03 untouched)
- `scripts/polish_cp028_drive_v2_cand.py` → `rounds/candidates/h03_cp028_drive_v2.blend`. FT51–FT53 code identical to v1; FT54 v2: oiler stands on treads 12/13 of the 14 ft steps, facing up them (turned 10 deg), top cap at thigh height, hand + feeder at bearing S' x=16 ft; pale trousers + dark boots on his own mesh copy.
- `scripts/render_cp028_drive_v2.sh [--rebuild]` → `renders/candidates/cp028_drive_v2_20261102/{before,after}/CP028_louvre_start.png` (camera, 1280x720, 48 spp, --keep-lighting --no-people identical to v1; before pixel-identical to live h03). Pixel-identical on rerun, including --rebuild.
- `scripts/make_cp028_drive_v2_pairs.py` → survey `look/pairs_geo/CANDIDATE_CP028_drive_v2_{before,after,pair,detail_pair}.png`. No verdict.

## 2026-11-02 KEEP CP028 louvre drive v2 (live h03)
- Parent verdict KEEP on v2 (oiler clearly stands on the steps; drive matches Downes; exposure matches). FT51–FT54 v2 now live in `rounds/h03.blend`.
- Live h03 rebuilt reproducibly: `scripts/render_cp028_live.sh --rebuild` takes the pre-promotion h03 pinned at fitout 7b25192, runs `scripts/polish_cp028_drive_v2_cand.py`, writes `rounds/h03.blend`, and renders `renders/h03/CP028_louvre_start.png` (1280x720, 48 spp, --keep-lighting --no-people). Pixel-identical (max diff 0) to `renders/candidates/cp028_drive_v2_20261102/after/CP028_louvre_start.png`, with and without --rebuild.
- CP028 has no end frame. The other h03 shot, CP026_shilling_ext_start, does not show this wall: an old-h03 vs new-h03 test render differs by at most 3/255 in 1006 pixels (bounce noise), so `renders/h03/CP026_shilling_ext_start.png` was not re-rendered.

## 2026-11-10 CP026_shilling_ext "shilling" CANDIDATE: executor notes (not a verdict, NOT live; DEPARTURES FT55-FT57, FT59)
- Why CP026: earliest unfinished phase is phase 1/2 Hyde Park; of the HP hero shots never geo-polished (CP013/14/17-22/26/27/29/30), CP026 was the weakest on a contact sheet of live renders: a white, textureless apron slab over a third of the frame, a flat beige wall, a pale 7 ft box (SOUTH_PEDESTALS, no source) beside the doorway, and a queue of people v3.1 mannequins.
- Sources: Downes Plate IV (south elevation: boarded, arched ground-tier panels; detached columns on pedestals with steps) and Plate XXVI figs 26-27 / pp. 38-39 (pedestal a5, 4 ft 9 in printed); profile numbers via Muse's models/south-entrance-pedestals NOTES (read-only). Plate IV crop kept in /workspace/tmp/cp026/ref only.
- Script scripts/cand_cp026_shilling_20261110.py on live rounds/h03.blend (unchanged, md5 df1e46cf311d2358891164a4d94178b5) -> rounds/candidates/h03_cp026shilling.blend (md5 e2a5472545696b3f613880a1bd8d1ed1). Figures scripts/cp026_figures.py + scripts/c26_figures_base.py (copy of site-grok c9_figures_v2.py).
- Live recipe reproduced exactly: render_views.py with people_lib v3.1 (survey 0dfacfa, the lib that made the live frame at b7069ee) via scripts/render_views_ppl31.py; 1280x720, 24 spp, look v1.1 1851 exterior_midday; re-render of live vs live PNG max 8, mean 0.0005. (Current people_lib 3.4 gives blocky figures, so a plain re-render is NOT the live frame.)
- Render scripts/render_cp026_shilling.sh [--no-build] -> renders/candidates/cp026_shilling_20261110/after/ (exposure -0.76 vs live -0.7). Luma 167.11 -> 167.63. Log /workspace/logs/cp026_shilling_render.log ends CP026_SHILLING_DONE.
- Pairs python3 scripts/cand_cp026_shilling_pairs.py -> survey look/pairs_geo/CANDIDATE_CP026_shilling_start_{before,after,pair,detail_pair}.png (before = live PNG).
- Checks scripts/check_cp026_shilling.py -> checks/cp026_shilling_checks.json: 15/15 (pedestal 57.0 in top / 60.8 in bell / 20.2 in plinth, on the floor; 147 replacements each on a hidden original; heights; no C26 figure caught by the v3.1 swap; apron/boarding materials).
- Self-score 5/10. Wins: apron reads as gravel (ground std 0.5 -> 6.4), the pale box is gone and Downes' octagonal pedestal stands at the column foot, south boarding reads vertical, women read as 1851 women (bonnets, folded shawls, skirts to the ground) and men have hats that sit, boots, coats.
- Misses: from behind under the hard midday sun the women read as pastel cones (no arms, flat skirts), and the queue looks smaller and less colourful than the bulky v3.1 crowd; men's coats read pale grey; no ticket action at the turnstiles is visible from this camera; Plate IV's 8 ft detached-column rhythm, three steps and panelled double doors are not built; gravel mottling is fine-grained and the trodden band is hidden under the queue; frame is still very bright overall (exposure matched to live).
- Not done: promotion, KEEP label, regression renders of the other h03 cams (CP026_turnstiles_start will change with the figures; CP027/CP028 should not, SOUTH_PEDESTALS is outside). Resume: if after PNG missing run scripts/render_cp026_shilling.sh --no-build, then the pairs script.

## 2026-11-10 KEEP CP026 environment-only polish (live h03; DEPARTURES FT56/FT56b, FT57, FT59; FT55 REJECTED)
- Parent verdict KEEP on the env-only candidate (viewed live renders/h03/CP026_shilling_ext_start.png vs renders/candidates/cp026_env_20261110/after/): gravel apron, vertical south boarding and the Downes pedestal replacing the pale 7 ft box are clearly better; same exposure -0.7; luma 167.11 -> 163.04 only from the darker ground; live people_lib v3.1 figures untouched. The earlier shilling candidate (FT55 figures read as armless pastel cones) is REJECTED; survey pairs renamed REJECTED_CP026_shilling_*.
- Candidate: scripts/cand_cp026_env_20261110.py (= shilling script minus FT55, plus FT56b trodden band on the real queue line) on live h03 -> rounds/candidates/h03_cp026env.blend (md5 d72ae4b3); scripts/render_cp026_env.sh; pairs scripts/cand_cp026_env_pairs.py -> survey look/pairs_geo/KEEP_CP026_env_start_{before,after,pair,detail_pair}.png (before = pre-keep live PNG).
- Pre-keep live h03 pinned as rounds/h03.blend.pre_cp026env_keep (md5 df1e46cf311d2358891164a4d94178b5, = h03 after the CP028 v2 KEEP).
- Live h03 rebuilt reproducibly: scripts/render_cp026_live.sh --rebuild runs cand_cp026_env_20261110.py on the pinned pre-keep h03, writes rounds/h03.blend (md5 0a1da8f271d50b3c02f878cd8f7d86e4; the blend md5 differs from the candidate file only by save metadata) and renders renders/h03/CP026_shilling_ext_start.png with the exact live recipe (render_views_ppl31.py, 1280x720, 24 spp, 1851 exterior_midday, exposure -0.7). Pixel-identical (max diff 0) to the candidate after PNG. Log /workspace/logs/cp026_env_promote.log.
- Regression scripts/regress_cp026_env_keep.sh (pre-keep vs live, same recipe both sides, /workspace/tmp/cp026keep/{pre,live}; numbers in checks/cp026_env_keep_regression.json): CP026_turnstiles_start max 201 / mean 4.77, changes only where the pale box was (now open to gravel/sky), the gravel apron outside and the boarding grain; CP027_stair_foot_start max 175 in 183 px, far south boarding now vertical and the right-edge doorway sliver open where the box stood; CP027_gallery_rail_start max 10 (23 px), CP028_watering_start max 5 (2 px), CP028_louvre_start max 19 (22 scattered px) = noise. Only CP026_shilling_ext_start and CP028_louvre_start have live renders/h03 frames; CP028 was not re-rendered (the pre-keep render is pixel-identical to the live PNG; the live delta is 22 px of noise). Rebuilding CP028 must now use scripts/render_cp028_live.sh WITHOUT --rebuild (its --rebuild would drop this KEEP).
- Open misses (unchanged): Plate IV's 8 ft detached-column rhythm, three steps and panelled double doors not built; no ticket action visible from CP026_shilling_ext; frame still bright; queue figures still the people v3.1 mannequins.

## 2026-11-11 CP020_floor_start "nave" CANDIDATE: executor notes (not a verdict, NOT live; DEPARTURES FT60-FT66)
- Why CP020: of the Hyde Park shots never geo-polished (CP008, CP013, CP014, CP017-CP021, CP027, CP029, CP030; CP026/CP007/CP010/CP015/CP006/CP025/CP009/CP011/CP032/CP012/CP031/CP028 avoided), CP020 was the weakest on a contact sheet of live renders: the left third of the frame runs out of the transept model past x = -144 onto open park with a flat sea-like horizon, and the nave over the camera has no roof (open sky top-left), so the floor-laying beat does not read as inside the building.
- Script scripts/cand_cp020_nave_20261111.py on live rounds/f03.blend (unchanged, md5 18d4107fd16aa3fc3b1a884203608325) -> rounds/candidates/f03_cp020nave.blend (md5 changes per save by metadata only; renders identical). 542 new columns, 1,869 girders, 39 trusses, 1,773 roof units, 243 wall bays, 210 railings, galleries + floor slab, 18 interior arm walls hidden; all linked meshes from f03's own part library.
- Render scripts/render_cp020_nave.sh [--no-build] [--before] [exposure] -> renders/candidates/cp020_nave_20261111/{after,before_rerender}/CP020_floor_start.png. Live recipe reproduced (FT66): before_rerender vs live PNG max 1, mean 0.05.
- Pairs python3 scripts/cand_cp020_nave_pairs.py -> survey look/pairs_geo/CANDIDATE_CP020_nave_start_{before,after,pair,detail_pair}.png (before = live PNG). Mean luma (Rec.709) 128.76 -> 106.36 at the same exposure -1.768.
- Checks: scripts/check_cp020_nave.py -> checks/cp020_nave_checks.json 15/15 (west end column line -924 ft = 1,848 ft mirrored; 24 ft steps; tier widths 408/264/120; nave 72 ft; girder tops 22'2"/42'2"/62'2"; floor top; no figure clash; no double columns); check_dims 40/40 and check_state 48/48 on the candidate (incl. >= 1 ft camera clearance for every f03 camera).
- Wins: the horizon and open park are gone; the frame now looks down a 1,848 ft glazed nave with column rows, galleries and a ridge-and-furrow roof overhead to a pale west end; figures and every existing object untouched.
- Misses / concerns: frame is darker (-22 luma) at matched exposure because the new nave roof shades the sunlit floor and the gallery undersides on the right; the far end is a bright white band; the people are still the v3.3 mannequins (the seated layer with legs out, cans); the near deal boards are still very pale; west nave shown fully painted and fully boarded (FT63/FT65 are judgement calls).
- Regression preview (not a live recipe): scripts/regress_cp020_nave.sh -> /workspace/tmp/cp020/regress/{live,cand} for CP018_paint/cradle, CP019_doors/dray (see survey README note). Not done: promotion, KEEP label.

## 2026-11-11 KEEP CP020 nave (live f03; DEPARTURES FT60-FT66)
- Parent verdict KEEP at 00:35 UTC (the floor-laying scene now reads as inside the building; darker at matched exposure -1.768, luma 128.76 -> 106.36, accepted).
- Live f03 = the approved candidate file copied in: rounds/f03.blend 18d4107f -> 3e80da59cf3bb3cf133d15edcc69e9 (= rounds/candidates/f03_cp020nave.blend). Pre-keep live pinned as rounds/f03.blend.pre_cp020nave_keep (md5 18d4107fd16aa3fc3b1a884203608325, = f03 as built Oct 27). The interrupted first attempt had left a --rebuild f03 (md5 8208a57c, save metadata); it was replaced by the candidate itself.
- scripts/render_cp020_live.sh [--rebuild] [--no-render] renders renders/f03/CP020_floor_start.png with the live recipe (people_lib 3.3 wrapper, --keep-lighting, 1280x720, 24 spp, exp -1.768): pixel-identical (max diff 0) to renders/candidates/cp020_nave_20261111/after/CP020_floor_start.png. --rebuild reruns cand_cp020_nave_20261111.py on the pinned pre-keep f03 (that script now refuses a source that already has C20_* objects). render_cp020_nave.sh / regress_cp020_nave.sh now use the pin, never live f03.
- Other f03 cams: scripts/render_f03_others_live.sh <blend> <outdir> recreates their historical recipes from git (cradle/dray: fitout da494a9 scripts, re-render of pre-keep = live PNG max 0; paint/doors: fitout 387a34c + people_lib 2.0 survey dab5204 + look survey 0008c1c, close but not exact, max 53/67 mean 2.3/1.2 from people placement). scripts/regress_cp020_nave_keep.sh = pre-keep vs live, same recipe both sides -> /workspace/tmp/cp020keep/fin/{pre,live}; numbers in checks/cp020_nave_keep_regression.json:
  - CP018_cradle_start max 203 / mean 37.8, luma 203.4 -> 177.1: open park horizon and sky behind the cradle become the nave (galleries, columns, roof). Expected but a large visible change, so the live PNG was NOT updated; pending reviewer (pair /workspace/tmp/cp020keep/regress_pairs/CP018_cradle_start_*).
  - CP018_paint_start max 192 / mean 11.7, luma 91.0 -> 85.2: far left sky/park and the far end become nave structure; roof shades the frame. NOT updated; pending reviewer (pair .../CP018_paint_start_*).
  - CP019_doors_start max 21 / mean 1.49 (1 px > 20): noise / slight bounce drop. Not re-rendered.
  - CP019_dray_start max 206 / mean 0.89 (13.5k px > 10, all inside the doorway): distant nave structure seen through the doors in place of park/sky; background-only, plainly expected, so renders/f03/CP019_dray_start.png was UPDATED from the live-side render (recipe exact).
- Why the first promotion stalled: it tried to reproduce the stored CP018_paint/CP019_doors PNGs pixel-exactly (several script snapshots: 387a34c, da494a9, people 2.0/3.1) before comparing, and those frames depend on people-swap order. Fix: pin the best recipe in a script and compare pre vs live under the SAME recipe; exact repro of the stored PNG is not needed for a regression check.
- Survey look/pairs_geo CANDIDATE_CP020_nave_start_* renamed KEEP_CP020_nave_start_*; COVERAGE CP020 row updated.

## 2026-11-11 CP022_fountain_start "envelope" CANDIDATE: executor notes (not a verdict, NOT live; DEPARTURES FT67-FT73)
- Why CP022: phase 1/2 Hyde Park first; of the HP heroes not on the avoid list (CP008, CP016, CP017, CP021-CP024, CP027, CP029, CP030), CP022 had the clearest at-a-glance miss on a contact sheet of live renders: the left third of "A landmark made of glass" is the west side gallery standing against open blue sky (o01 stops at x = -132 ft, no nave), and a row of gallery visitors floats in mid-air over the nave/transept crossing (x ~ -43, y 12..36 ft, no deck there), one with legs dangling.
- Script scripts/cand_cp022_envelope_20261111.py on live rounds/o01.blend (unchanged, md5 4776f6182fdfc758581eb79ce12d3345) -> rounds/candidates/o01_cp022envelope.blend. Uses the KEPT CP020 nave rules (FT60-FT65) unchanged + FT71 (46 floating gallery figures hidden). Refuses to write live o01 and refuses a source that already has C20_/C22_ objects. md5 changes per save by metadata only.
- Render scripts/render_cp022_envelope.sh [--no-build] [--no-before] -> renders/candidates/cp022_envelope_20261111/{before,after}/ for CP022_fountain_start (hero) + side-effect cams CP021_doors_start (CP021 hero), CP021_dais_start, CP022_crossing_start. Recipe FT73 (people_lib 3.3 wrapper, --keep-lighting, exp -0.7, 1280x720, 48 spp). Log /workspace/logs/cp022_envelope_render.log ends CP022_ENVELOPE_DONE.
- Pairs python3 scripts/cand_cp022_envelope_pairs.py -> survey look/pairs_geo/CANDIDATE_CP022_envelope_{before,after,pair,detail_pair}.png + CANDIDATE_CP022_envelope_sidefx_{CP021_doors,CP021_dais,CP022_crossing}_{before,after,pair}.png; numbers in checks/cp022_envelope_pairs.json.
- Checks: scripts/check_cp022_envelope.py -> checks/cp022_envelope_checks.json 17/17; check_dims 37/37 (run on a copy under /workspace/tmp/cp022/dimsrun because check_dims reads ../route from the blend's folder); check_state 26/26 (both identical to live o01).
- Status: see the "CP022 envelope status" line below (updated as steps finish).
- CP022 envelope status (2026-11-11 14:55 UTC): DONE as a CANDIDATE. Candidate blend md5 2cd47f234db677a644381c65dbe0c86a (untracked, like the other candidate blends; rebuild with scripts/render_cp022_envelope.sh). Live o01 unchanged (4776f618). Before CP022 re-render is deterministic (max 0 vs an earlier identical run).
  - Mean luma (Rec.709, exp -0.7 both sides): CP022_fountain_start 146.72 -> 135.96 (sky replaced by roofed nave structure); side effects CP021_doors_start 127.50 -> 123.64, CP021_dais_start 96.72 -> 87.95, CP022_crossing_start 135.55 -> 129.32.
  - Wins: the open-sky left third of CP022 is now the roofed, glazed west nave with galleries; the floating gallery visitors are gone (also in CP022_crossing).
  - Misses / concerns (executor, not a verdict): the left third is now a busy, pale white lattice with no people in the near side gallery and an empty west nave (FT72); every frame is darker at matched exposure; in CP021_dais (and slightly CP021_doors) the foreground people_lib figures are re-dealt (different clothes/colours) because hiding the 46 figures shifts the people_lib mesh-cache order, not because of a deliberate change; the fountain itself is untouched (still the dark chrome-looking Muse glass).
  - Not done: promotion, KEEP label, COVERAGE row change (only a CANDIDATE note added).

## 2026-11-12 00:15 UTC: CP022 envelope KEEP live (scoped)
- rounds/o02.blend (md5 2cd47f23 = approved candidate o01_cp022envelope.blend; FT67-FT73) is live ONLY for CP022_fountain_start (hero) and CP022_crossing_start, routed by scripts/fitout_live_heroes.json; recipe scripts/render_cp022_live.sh [--rebuild].
- renders/o02/ CP022 PNGs re-rendered; --rebuild check pixel-identical (max diff 0).
- rounds/o01.blend unchanged (4776f618); CP021 doors/dais stay on o01. Regression render of o01 with people v3.3 differs from the Oct 27 committed PNGs only by people_lib figure reshuffle (no geometry change); reviewed, not better, committed CP021 PNGs NOT updated.
- Pre-keep tag: pre_cp022envelope_keep. Local commit only, not pushed.

## 2026-11-12 CP027_stair_foot_start "east nave" CANDIDATE: executor notes (not a verdict, NOT live; DEPARTURES FT74-FT80)
- Why CP027: phase 1/2 Hyde Park first; of the HP heroes not on the avoid list (CP008, CP016, CP017, CP023, CP024, CP027, CP029, CP030), CP027 had the clearest at-a-glance miss on a contact sheet of live renders: the camera looks due south from the foot of the gallery stair at (103.7, -50) ft, so frame-left is due east, and h01 stops at x = +132 ft; the ground tier on the left third shows a flat green lawn and open hazy sky under the side gallery (the building has no east side).
- Script scripts/cand_cp027_east_20261112.py on live rounds/h01.blend (unchanged, md5 73c09039f67f61267b78ba2735ea81ce) -> rounds/candidates/h01_cp027east.blend (untracked like the other candidate blends; md5 changes per save by metadata only). = KEPT CP020 nave rules mirrored east: 536 columns, 1,833 girders, 36 trusses, 1,728 roof units, 237 wall bays, 204 railings, gallery slabs, floor; 18 x = +132 tier-2 walls hidden; no figure hidden. Refuses to write h01/h02/h03 and refuses a source with C20_/C22_/C27_ objects.
- Render scripts/render_cp027_east.sh [--no-build] [--no-before] (nohup; log /workspace/logs/cp027_east_render.log; done marker renders/candidates/cp027_east_20261112/DONE) -> renders/candidates/cp027_east_20261112/{before,after}/ : CP027_stair_foot_start 1920x1080 48 spp + side-effect CP027_gallery_rail_start 1280x720 24 spp; recipe FT80 (people_lib v3.1 wrapper, look --era 1851, same exposure both sides).
- Pairs python3 scripts/cand_cp027_east_pairs.py -> survey look/pairs_geo/CANDIDATE_CP027_{before,after,pair,detail_pair}.png + CANDIDATE_CP027_sidefx_gallery_rail_{before,after,pair}.png; numbers in checks/cp027_east_pairs.json.
- Checks: scripts/check_cp027_east.py -> checks/cp027_east_checks.json 17/17; check_dims 39/39 (checks/cp027_east_dims.json, run on a copy in /workspace/tmp/cp027/dimsrun); check_state 38/38 (checks/cp027_east_state.json; live h01 38/38).
- Resume: if DONE is missing, re-run `nohup scripts/render_cp027_east.sh --no-build &` (or with --no-before if before/ has both PNGs), then the pairs script.
- Not done: promotion, KEEP label, COVERAGE row change (only a CANDIDATE note). CP026/CP028 are live on h03, not h01, so no other hero is affected.

## 2026-11-12 08:15 UTC: CP027 east nave KEEP live (scoped)
- rounds/h04.blend (md5 cc938620 = approved candidate rounds/candidates/h01_cp027east.blend; FT74-FT80) is live ONLY for CP027_stair_foot_start (hero), routed by scripts/fitout_live_heroes.json; recipe scripts/render_cp027_live.sh [--rebuild].
- renders/h04/CP027_stair_foot_start.png = candidate after/ PNG (max diff 0); --rebuild check (/workspace/tmp/cp027keep, ALL_DONE 06:09) pixel-identical (max diff 0).
- rounds/h01.blend unchanged (73c09039); h01 PNGs byte-unchanged (md5 before = after). CP027_gallery_rail_start stays on h01 (side effect REJECTED: only darker, west lawn stays). Pre-keep hero stays in renders/h01/.
- Verdict (my own view of the pair): kept because the lawn and open sky left of the stair foot are replaced by the roofed east nave; frame is darker overall. Pre-keep tag: pre_cp027east_keep. Local commit only, not pushed.
- Note: the promotion chain restarted roughly every two hours (same pattern as CP022) before finishing; outputs were correct.

## 2026-11-12 CP029_dais_start "east nave" CANDIDATE: executor notes (not a verdict, NOT live; DEPARTURES FT81-FT87)
- Why CP029: phase 1/2 Hyde Park first; of the HP heroes not on the avoid list (CP008, CP013, CP016, CP017, CP024, CP029, CP030), CP029 had the clearest at-a-glance miss on a contact sheet of live renders: "The exhibition ends" looks east-north-east from (-27, -6) ft, c02 stops at x = +132 ft, so the right edge shows green lawn at floor level, the top-right open sky, and two gallery visitors stand on air against that sky.
- Script scripts/cand_cp029_east_20261112.py on live rounds/c02.blend (unchanged, md5 c0be5fff332040d906d148fb60c36f35) -> rounds/candidates/c02_cp029east.blend (md5 0651925dbe74cd2ea0cdb1df334a04fb; untracked like the other candidate blends; md5 changes per save by metadata only). = CP027 east-nave rules on c02 (536 columns, 1,833 girders, 36 trusses, 1,728 roof units, 237 wall bays, 204 railings, gallery slabs, floor; 18 x = +132 tier-2 walls hidden) + FT85: 36 floating gallery figures hidden. Refuses to write c01/c02/h0x and refuses a source with C20_/C22_/C27_/C29_ objects.
- Render scripts/render_cp029_east.sh [--no-build] [--no-before] (nohup; log /workspace/logs/cp029_east_render.log; done marker renders/candidates/cp029_east_20261112/DONE) -> renders/candidates/cp029_east_20261112/{before,after}/ : CP029_dais_start + side-effect CP029_gallery_start, both 1920x1080 48 spp; recipe FT87.
- Pairs python3 scripts/cand_cp029_east_pairs.py -> survey look/pairs_geo/CANDIDATE_CP029_{before,after,pair,detail_pair}.png + CANDIDATE_CP029_sidefx_gallery_{before,after,pair}.png; small side-by-sides /workspace/tmp/cp029/CP029_{dais,gallery}_start_pair_small.png; numbers in checks/cp029_east_pairs.json.
- Mean luma (Rec.709, same look/exposure both sides): CP029_dais_start 57.45 -> 50.52; CP029_gallery_start 72.63 -> 67.79.
- What changed (description, not a verdict): dais: top-right sky -> east-nave roof glazing and girders, right-edge lawn -> dim interior/boarding, the two figures on air above the gallery gone; the rest of the frame (dais, crowd, elm) shows only render noise/slightly darker light. Gallery (side effect): the row of visitors standing on air across the far crossing gone, the green lawn beyond -> east nave interior, and the group of large figures on air in the left foreground gone (the frame now looks down past the gallery end to the floor).
- Checks: scripts/check_cp029_east.py -> checks/cp029_east_checks.json 19/19; check_dims 35/35 (checks/cp029_east_dims.json, run on a copy in /workspace/tmp/cp029/dimsrun); check_state 15/15 (checks/cp029_east_state.json; live c02 35/35 + 15/15).
- Not done: promotion, KEEP label, COVERAGE row change (only a CANDIDATE note). No other storyboard hero renders from c02 (CP029 cams only).

## 2026-11-12 KEEP CP029 east nave (scoped, FT81-FT87)
- Verdict (viewed myself 10:55 UTC): KEEP for CP029_dais_start (hero) and the CP029_gallery_start side effect. Floating figures gone; lawn and open sky beyond the closing dais replaced by east-nave structure.
- Live: new rounds/c03.blend (md5 0651925d = approved candidate rounds/candidates/c02_cp029east.blend), routed in scripts/fitout_live_heroes.json; render via scripts/render_cp029_live.sh [--rebuild].
- Live renders renders/c03/CP029_{dais,gallery}_start.png (1920x1080, 48 spp, people v3.1, look era 1851). Rebuild from script (/workspace/tmp/cp029keep/c03_rebuild.blend) matches live, max pixel diff 0 on both.
- rounds/c02.blend unchanged (c0be5fff) and its renders/c02 PNGs unchanged (md5 before = after); they stay as pre-keep frames. Pre-keep tag pre_cp029east_keep.
