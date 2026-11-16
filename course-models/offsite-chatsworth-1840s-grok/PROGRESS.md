# PROGRESS — O-CHATS

## ch01 (2026-10-27)
- Great Stove interior (CP003) + Victoria lily house with pads and underside rib (CP004).
- Underside cam moved off tank to pos_ft [20,4,5.25] (eye over path).
- Checks: **27/27** (`checks/ch01_checks.md`).
- Finals 1280×720 / 48 spp: `renders/ch01/` (5 shots).
- Previews: `renders/ch01_prev/`.

## ch02 (2026-10-27): quality pass — warmer glass/iron, lit lily pads
- Warmer darker iron/paint; glass tint; world strength 0.28 + haze; lily AREA fill + leaf emit; exposure −0.15.
- DEPARTURES CH03. Checks pass; renders/ch02/.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- material paint/iron/brick grit keep-better CP003/004; people_lib 3.1 vendored

## 2026-11-16 CP004 lily house CANDIDATE — executor notes (not a verdict, NOT live; DEPARTURES CH07-CH16)
- Why CP004: on a contact sheet of every live hero outside the recent-polish list it read worst with a clear fix: a bright cyan "swimming pool" under open sky, lily pads hovering on stilts (the turned-over leaf's trestle standing in the water), dark iron columns standing in the tank, no wall glazing and no roof in frame, so the storyboard beat ("repeated glass and supporting ribs ... above planting") did not read.
- Base: live `rounds/ch02.blend` (md5 59eca5d7, never written). COVERAGE hero `renders/ch02/CP004_lily_tank_start.png` (1280x720, 28 spp, 2026-10-27 material pass via survey `look/batch_material_london_chatsworth.py`, people v3.1). Current recipe (render_views.py, look v1 1840s / exterior_midday, people v3.4) at 1280x720 28 spp reproduces it except one off-frame figure shadow at bottom right: max diff 114, mean 0.58, 7955 px > 8. So "before" = live ch02 rendered with the same recipe as "after".
- Script `scripts/candidate_cp004_lilyhouse.py` (live ch02 -> `rounds/candidates/ch02_cp004lily.blend`; refuses to overwrite ch02 or run twice). Only adds CP4_ objects in a new collection `CP4_LILY_HOUSE_1850` (child of LILY_HOUSE), hides 14 superseded lily meshes (not deleted), tags trestle + underside leaf only_cams, moves the 4 lily-house figures to the far walk. Cameras, world, sun, fill light, exposure and all live materials unchanged.
- Render `scripts/render_cp004_candidate.sh [--no-build]` (resumable per PNG; log /workspace/logs/cp004_lilyhouse_render.log; DONE + md5.txt) -> `renders/candidates/cp004_lilyhouse_20261116/{before,after}/` for all 5 cams, 1920x1080 48 spp.
- Pairs `python3 scripts/make_cp004_pairs.py` -> survey `look/pairs_geo/CANDIDATE_CP004_lily_house_tank_*` (+ `_detail_pair`) and `CANDIDATE_CP004_sidefx_*`; numbers `checks/cp004_lilyhouse_pairs.json`.
- Checks: `checks/dump_state_cp004.py` on both blends + `python3 checks/check_cp004_lilyhouse.py` -> `checks/cp004_lilyhouse_checks.json`.
- Build bytes are not deterministic (blend timestamps), geometry is: a rebuild gives a different md5 but the same dump.
- Not done: promotion, KEEP, routing, COVERAGE row change, any live PNG. ch02 and renders/ch02 unchanged. Tag `pre_cp004lily_cand` (local). NOT pushed.
- Gotcha found on the way (fixed in the script, documented in CH16): the first build named the outside turf `CP4_lawn_apron_outside`; the shared look's `_ensure_horizon_ground()` re-tints/re-heights CPL_HorizonGround from any object named lawn/grass/gravel/soil/..., so the CP003 stove horizon went +10 luma. Renamed to `CP4_outside_turf_apron` (+ only_cams for the CP004 cams); CP003 then differs from live by noise only. The check `SCOPE.look_horizon_keywords` guards it.
- Result (2026-11-16 02:3x UTC): candidate `rounds/candidates/ch02_cp004lily.blend` md5 bdccb859ffeaee63d5a8788d251f6abb (live ch02 59eca5d7 unchanged). Checks 18/18. Luma (1920x1080 48 spp, same recipe both sides): hero CP004_lily_tank 184.04 -> 120.21; side effects CP004_learning 180.65 -> 130.77, CP004_lily_underside 169.23 -> 108.71 (trestle leaf still stands in the water there, pre-existing), CP003 stove_nave 191.87 -> 191.87 (mean diff 0.056, noise) and stove_rib 195.97 -> 195.98 (mean 0.06, noise). Survey pairs written; no verdict.
- Correction: the live lily house had 14 columns (build info lily_columns = 14), not 20 as the candidate commit message says; DEPARTURES CH07 and the script docstring are fixed (docstring only, geometry unchanged).
