# PROGRESS — O-LONDON

## ln01 (2026-10-27)
- O-INDUSTRY (CP002) viaduct / factory / terraces + O-ROOM (CP005) commissioners' planning room with plan textures.
- Checks: **29/29** (`checks/ln01_checks.md`).
- Finals 1280×720 / 48 spp: `renders/ln01/` (5 shots).
- Previews: `renders/ln01_prev/`.

## ln02 (2026-10-27): quality pass — brick/soot/slate, arch fills, train smoke
- Darker brick/soot/slate; soot rear + brick wing walls in arches; denser loco smoke; gloomier world.
- DEPARTURES LN02–LN03. Checks pass; renders/ln02/.

## ln03 — CP069 South Ken today (2026-10-27)
- Built `rounds/ln03_southken.blend` via `scripts/build_southken_today.py`.
- Cams: `CP069_street`, `CP069_rah`, `CP069_museums` (appended to route).
- Renders: `renders/ln03/` (lean). Logged **optional** in DEPARTURES LN04.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- material grit pass keep-better CP002/005/069; people_lib 3.1 vendored

## ln03 w02 polish (2026-10-27) — CP069 set geometry
- Rebuilt `rounds/ln03_southken.blend`: RAH frieze band, window ring + iron mullions, iron balcony, glazed lantern + dome ribs; museum iron frames; street rails/lamps/bollards; multi-lobe trees + iron tree guards.
- Keep-lighting lean 1280×720 / 28 spp: `renders/ln03/CP069_street_start.png`, `CP069_rah_start.png`.
- Honest pair keep-better: **KEEP** CP069 (geometry/dressing visibly better than prior block-out).
