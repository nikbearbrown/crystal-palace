# PROGRESS — crystal-palace-move-1852-grok

## Checkpoint m01 (2026-10-26)
- Built `rounds/m01.blend` (scripts/build_move.py; 358 objects, ~7.8 MB).
- D-checks `checks/m01_checks.json`: **25/25 pass** (K1–K8 joint, cameras eye 5.25/lens/no roll, F1–F2 figures, M1 distance, M2 no route, S1–S3).
- Final renders `renders/m01/` (1920×1080, 96 spp) + `contact_sheet_m01.jpg`.
- Self-score 7/10. Misses: KJ_exploded cluttered/too close; Muse elms read cyan-lollipop; ARR slope reads only subtly; locator Thames is very schematic.

## Checkpoint m02 (2026-10-26)
- Move fix 1 only (Professor Bear): KJ_exploded pulled back, N girder + oak keys hidden per-camera (MV12).
- `rounds/m02.blend`; D-checks `checks/m02_checks.json`: **25/25 pass**.
- Final renders `renders/m02/` (1920×1080, 96 spp) + contact sheet (`scripts/render_m02.sh`, detached).

## Next
1. ~~KJ_exploded pull back, hide second girder~~ (m02 done).
2. Elm leaf tint (warmer, less cyan) on appended Muse elms.
3. ARR: steeper grade + a stake line to make the slope read.

## Backlog (parked by Professor Bear, diminishing returns)
- r11 (transept polish), x07 (exterior polish), d04 (dismantle polish).

## m03 — CP068 legacy today (2026-10-27)
- Built `rounds/m03_legacy.blend` via `scripts/build_legacy_today.py` (reuse `parts1851` K-JOINT + single bay).
- Cams: `CP068_park`, `CP068_kit`, `CP068_bay` (appended to `route/camera_route.json`).
- Renders: `renders/m03/CP068_{park,kit,bay}_start.png` (28 spp, 1280×720).
- D-checks: `checks/m03_checks.json` **11/11**.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP032; lib 3.1

## people v3.2 2026-10-27
- people v3.2: revert CP032

## 2026-11-02 CP032 departure hands (CANDIDATE, no verdict)
- `scripts/candidate_cp032_people.py` builds sibling `rounds/candidates/m02_cp032people.blend` from live m02: 7 STAFF_* stand-ins → people_lib v3.4 hero figures `DEP_HAND_NN_<role>` (untagged so the render-time swap leaves them), dark fustian dress, black-coated clerk. DEPARTURES MV15.
- `bash scripts/render_cp032_people.sh [DIR]` rebuilds the candidate and renders before/after at identical settings (1920×1080, 24 spp); `scripts/make_cp032_people_pairs.py` writes `look/pairs_geo/CANDIDATE_CP032_people_{before,after,pair,detail_pair}.png`. Mean luma 180.95 → 179.11 (darker clothing; settings identical).
- Known flaws: A-pose arms still a little splayed; workmen's hands carry the trouser slot (read as dark gloves); hero boots are tubes over bare feet (visible only close up); low-poly caps. Live m02 and renders/m02 untouched.

## 2026-11-02 CP032 departure hands KEEP (live m02)
- Parent reviewed `CANDIDATE_CP032_people_*` and kept it; pairs renamed `look/pairs_geo/KEEP_CP032_people_*`. DEPARTURES MV15 → KEEP.
- Live `rounds/m02.blend` now carries the seven `DEP_HAND_*` figures (STAFF_00..06 removed; STAFF_07..11 at ARR untouched): `candidate_cp032_people.py --live` applied in place to the pre-KEEP m02 (pinned at 9cb8eb5). The script is idempotent (no-op when the hands are already in) and prints `CP032_HANDS_IN_PLACE True|False`.
- Live render `renders/m02/CP032_departure_start.png` (1920×1080, 24 spp, look exposure; same settings as the KEEP candidate, identical to `KEEP_CP032_people_after.png`, max diff 0).
- Reproduce: `scripts/render_cp032_live.sh [--rebuild]` (--rebuild regenerates live m02 from 9cb8eb5 + the CP032 script); pixel-identical (max diff 0) both ways. Depends on this folder's `people_lib.py` (render-time swap) staying as it is.
- Round: `scripts/build_m02.sh [OUT]` = `build_move.py` + CP032 re-apply + assert `CP032_HANDS_IN_PLACE True` (tested on a throwaway round). build_move.py has grown since m02 was frozen (adds CP068 region), so a fresh round is not pixel-identical to live m02.
- Stale: `renders/m02/CP032_departure_end.jpg` (6 of the 7 hands in frame; still shows the stand-ins), the old 96-spp `renders/m02/CP032_departure_start.jpg` (superseded by the .png), and `renders/m02/contact_sheet_m02.jpg`. The other m02 renders (KJ_*, CP032_arrival_*, CP032_locator_start) don't see the hands and are current.

## 2026-11-02 CP032 housekeeping: stale m02 files refreshed from live m02
- `scripts/render_cp032_stale.sh` (from live `rounds/m02.blend`, unchanged; same settings as the live start: render_shots.py, 1920x1080, 24 spp, look exposure) rewrote `renders/m02/CP032_departure_end.jpg` (fresh render, people_lib 3.4 swap, DEP_HAND_* workmen + clerk), `renders/m02/CP032_departure_start.jpg` and `renders/m02_png/CP032_departure_start.{png,jpg}` (from the live start PNG), and `renders/m02/contact_sheet_m02.jpg` (sheet.py layout over the m02 JPEGs only).
- Checks: the live start re-rendered pixel-identically (diff bbox None) before the refresh; CP032_departure_end rendered in its own session twice, pixel-identical. Rendered after the start camera in one session it gives a different people swap, so the script renders it alone.
- Still showing the old style: CP032_arrival_start/end (Sydenham arrival) keep boxy stand-in figures; not part of the MV15 KEEP. In the new departure_end the left foreground workman (close-up skip) has a blocky boot.
- Uncommitted `scripts/people_lib.py` working-tree edit (people 3.3 statue exclusion, dated 2026-10-27, not mine) left untouched and uncommitted.

## 2026-11-02 CP032 arrival hands (CANDIDATE, no verdict; DEPARTURES MV16)
- `scripts/candidate_cp032_arrival.py` builds sibling `rounds/candidates/m02_cp032arrival.blend` from live m02: the 5 Sydenham arrival stand-ins STAFF_07..11 → people_lib v3.4 hero figures `ARR_HAND_NN_<role>` (3 workmen, 1 navvy, clerk as 1850s gentleman), same xy/heading, feet ray-dropped onto the sloping ARR ground, MV15 fustian / black frock coat / hand-slot fix.
- Checks: `scripts/check_cp032_arrival.py` → `checks/m02_cp032arrival_checks.json` 6/6 (count, feet |dz|<1 cm, heights 1.66–1.80 m, core clear of ARR parts, DEP hands untouched, no Hyde Park objects in ARR).
- `bash scripts/render_cp032_arrival.sh [DIR]` rebuilds the candidate and renders before (live m02) / after for CP032_arrival_start and CP032_arrival_end, each camera in its own session (render_shots.py, 1920x1080, 24 spp, look exposure); `scripts/make_cp032_arrival_pairs.py` writes `look/pairs_geo/CANDIDATE_CP032_arrival_{start,end}_{before,after,pair}.png`. Mean luma start 189.24 → 187.98, end 184.73 → 183.45 (darker clothing; settings identical).
- Known flaws: same as MV15 (A-pose arms, low-poly caps on bald-looking heads, tight trousers); the 'working' pose mimes with empty hands; the clerk's frock-coat skirt reads as a flat black slab from the front; feet placed by a single centre ray, so on the 1-in-14 slope one boot can sit ~2 cm off. Not touched: the near foreground clay is blown to near-white under look v1 in both before and after (the whole lower third of both frames), and the stale `renders/m02/CP032_arrival_*.jpg` are pre-look 96-spp renders.
- If KEEP: add a `--live` mode (as candidate_cp032_people.py) and a render_cp032_arrival_live.sh, re-apply in build_m02.sh, re-render renders/m02/CP032_arrival_{start,end} and the contact sheet.

## 2026-11-02 CP032 arrival hands KEEP (live m02; DEPARTURES MV16)
- Parent reviewed `CANDIDATE_CP032_arrival_{start,end}_*` and kept both; survey pairs renamed `KEEP_CP032_arrival_*` with labels fixed.
- Live `rounds/m02.blend` now carries the five `ARR_HAND_*` figures (STAFF_07..11 removed): `candidate_cp032_arrival.py --live` applied in place (idempotent: a second run prints "already applied" and does not save; always prints `CP032_ARR_HANDS_IN_PLACE`). Pre-promotion m02 = move 8bfed03 (backup `/workspace/backups/m02_pre_arrival/m02.blend`).
- Departure figures unchanged: the seven `DEP_HAND_*` vertex/material/transform hashes are identical before and after. The live object set equals the candidate blend's.
- Live renders `renders/m02/CP032_arrival_start.png`, `renders/m02/CP032_arrival_end.png` (render_shots.py, 1920x1080, 24 spp, look exposure, one Blender session per camera). `scripts/render_cp032_arrival_live.sh [--rebuild]` reproduces both pixel-identically (diff bbox None vs the candidate afters / `KEEP_CP032_arrival_*_after.png`) from the live blend and after `--rebuild` (m02 @ 8bfed03 + arrival --live).
- Refreshed from the live PNGs (`scripts/refresh_cp032_arrival_files.sh`): `renders/m02/CP032_arrival_{start,end}.jpg`, `renders/m02_png/CP032_arrival_start.{png,jpg}`, `renders/m02/contact_sheet_m02.jpg`.
- `render_cp032_live.sh --rebuild` now also applies the arrival script; `build_m02.sh` re-applies arrival and asserts it.
- Caveat: with the arrival change, re-rendering CP032_departure_start from live m02 differs from the stored KEEP frame at noise level only (max 11/255, mean 0.01; the swap count changed 5 -> 1). The stored departure renders were left as they are.
- Next open weakness: the near foreground clay/ground is blown to near-white under look v1 (the lower third of both arrival frames).
- `scripts/people_lib.py` uncommitted working-tree edit (3.3 statue exclusion) left untouched and uncommitted.

## 2026-11-02 CP032 arrival near-foreground ground (CANDIDATE, no verdict; DEPARTURES MV17)
- Cause (ray probe, not a clay problem): look v1 drops its 2 km `CPL_HorizonGround` disk at z −0.02 m (the min top of the flat K/DEP grounds in the same blend). The Sydenham yard slopes down to the west, so under the arrival cameras the clay is 0.3–0.5 m lower and the flat, shadowless, near-white disk covered the lower third of both frames.
- `scripts/candidate_cp032_foreground.py` builds sibling `rounds/candidates/m02_cp032fg.blend` from live m02: `grok_states` hides `CPL_HorizonGround` for `CP032_arrival*` cameras only, and ARR_CLAY (not the spoil heaps) gets `GT_SydenhamClayYard` (trodden grey-brown clay, darker wet patches, fine bump). Checks `checks/m02_cp032fg_checks.json` pass (same objects, identical transforms, only ARR_CLAY's material slot changed).
- `bash scripts/render_cp032_foreground.sh [DIR]` rebuilds the candidate and renders before (live m02) / after for CP032_arrival_start and _end, each camera in its own session (render_shots.py, 1920x1080, 24 spp, look exposure). The before frames are pixel-identical to live `renders/m02/CP032_arrival_*.png`. `scripts/make_cp032_foreground_pairs.py` writes `look/pairs_geo/CANDIDATE_CP032_foreground_{start,end}_{before,after,pair}.png`; afters copied to `renders/candidates/cp032_fg_20261102/`. Mean luma start 187.98 → 160.55 (lower 40%: 226.65 → 170.31), end 183.45 → 159.02 (lower 40%: 218.50 → 170.25). Pixels above the ground also shift slightly (the white disk was bouncing light up into the scene).
- Known misses: the near yard now reads as earth with cast shadows, but it is still an empty, smooth plane. There are no cart ruts from the wagon, no stones, planks, puddles or tools, and the noise reads as soft blotches rather than trodden clay at 1:1. The pink spoil heap behind the girder (still GT_SydenhamClay) no longer matches the yard. The sash-bar bundles at the bottom left of the start frame are still the brightest thing in the foreground.
- Follow-up for the look library (not edited here): `_ensure_horizon_ground` should take the terrain under the active camera, not the min over every region in a multi-region blend.
- Live m02, renders/m02 and `scripts/people_lib.py` (an uncommitted 3.3 working-tree edit that is not mine) left untouched.
