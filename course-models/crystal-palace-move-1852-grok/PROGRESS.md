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
