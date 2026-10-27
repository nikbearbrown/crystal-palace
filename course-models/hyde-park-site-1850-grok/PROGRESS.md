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
