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
