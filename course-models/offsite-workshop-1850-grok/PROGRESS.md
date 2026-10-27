# PROGRESS: O-WORKSHOP (CP011), Grok Bot

Branch `grok-workshop-1850` (worktree /workspace/crystal-palace-workshop). Commit locally only; no push.

- **w01 (2026-10-27):** first build.
  - Shed and partition, machine shop (engine, shaft, 2 sash-bar machines, gutter machine, 270 bars).
  - Glass house (furnace, stage and pits, 69 cylinders, kiln).
  - Siding (2 wagons, girder, 4 columns, shear legs) and 22 figures.
  - Preview fixes as in W13/W15/W16.
  - check_workshop 31/31. Renders: renders/w01 (1280x720, 48 spp).
- **Next:** add belts to each machine and shavings on the floor; split cylinders by the kiln; add an interior wagon view from the loading door; give the glass house a darker interior with more glory-hole bloom.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## w02 (2026-10-27) — belts, shavings, glass-house depth (CP011)
- Built `rounds/w02_workshop.blend` from `build_workshop.py`: drive belts on sash/gutter machines; floor shaving clumps; 6 split cylinders by kiln; stronger glory/kiln bloom; greener sheet glass; darker glass-house world (0.22).
- Route: added `CP011_loading` cam.
- `render_views.py`: `--keep-lighting` support.
- Keep-lighting lean: `renders/w02/CP011_shop_start.png`, `CP011_loading_start.png`.
- Honest pair keep-better: **KEEP** CP011 (belts + shavings + darker glass house read clearly).
