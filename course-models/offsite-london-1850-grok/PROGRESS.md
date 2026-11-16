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

## ln03 w03 fix (2026-10-27) — CP069 exposure + RAH-as-itself + London planes
- User rejected w02 after (washed/overexposed, pale brick/dome, cone trees, grey-dash windows).
- Fix: authored exposure ~−0.18 (street mean luminance ≈ before 0.73); BrickDeep (0.16,0.045,0.028) + grit; buff terracotta + dark mosaic frieze; darker DomeIronGlass + thick iron ribs; regular arched dark-glazed bays with iron frames (Kit.quad, no AABB dashes); rounded broadleaf London planes (14 icosphere lobes + leaf noise, exterior park-tree grammar).
- Keep-lighting 1280×720 / 32 spp. Strict keep-better by eye: **KEEP** CP069.

## ln03 w04 (2026-10-27)
KEEP CP069 street+rah: London planes with trunk/branches + small leaf clusters + darker underside; arched windows as near-black glazing with sash bars; exposure matched to before. Pairs in survey `look/pairs_geo/`.

## CP002 polish CANDIDATE (2026-11-16) — not live, no verdict
- `scripts/build_cp002_street.py` opens live `rounds/ln02.blend` (unchanged) and saves `rounds/candidates/ln03_cp002.blend`. It replaces the INDUSTRY set with an 1850 London railway lane: an L&G-pattern viaduct (20 ft c/c, 18 ft span, 22 ft crown) with arches let as workshops, smithy, stable and store; setts, flags and kerbs; gas lamps; two horse drays; a Jenny Lind-type train; a continuous terrace; a 5-storey mill and chimneys; volumetric smoke and thin smog; 17 modelled 1850 figures (`scripts/cp002_figures.py`). The CP005 room is untouched (except the fireplace swap fix, D-LN-CP002-12). DEPARTURES D-LN-CP002-01..12. check_set 29/29 (`checks/ln03_cp002_CANDIDATE_checks.md`).
- Renders: `scripts/render_cp002_candidate.py` uses the live recipe: enhance + `--keep-lighting`, era 1840s, 1280×720, 28 spp, exposure −0.10 on both sides. Pairs are built by `scripts/make_cp002_pairs.py` into `renders/candidates/cp002_20261116/` (hero CP002_lane, plus side effects CP002_terrace, CP002_factory, CP005_room, CP005_table).

## 2026-11-16 CP002 1850 railway lane KEEP (scoped, live) — DEPARTURES D-LN-CP002-13
- The lead viewed the pairs. KEEP: `CP002_lane_start` (hero) and `CP002_factory_start`. REJECTED: `CP002_terrace_start` (exposure not matched, luma 37 -> 92) and `CP005_table_start` (a stray pale figure enters top right). `CP005_room_start`: no change. These three stay on `rounds/ln02.blend` (md5 56e47151da2b529d220fd8d80b62caa6, unchanged).
- Live round `rounds/ln04_cp002lane.blend` = byte copy of `rounds/candidates/ln03_cp002.blend` (md5 33262e1fb94f1540dd2e7c60ab856051).
- Routing `scripts/london_live_heroes.json` (new): CP002_lane_start + CP002_factory_start -> ln04_cp002lane; CP002_terrace + CP005 cams -> ln02; CP069 cams -> ln03_southken.
- Render `scripts/render_cp002_lane_live.sh [--rebuild] [outdir=renders/ln04_cp002lane]` (render_cp002_candidate.py: enhance + render_views.py --keep-lighting, era 1840s, exposure -0.10, 1280x720, 28 spp, one camera per session; --rebuild regenerates from ln02 into a temp blend and never overwrites ln04).
- Live heroes `renders/ln04_cp002lane/CP002_lane_start.png` (8657f41c5d96fd7dde7c8219cc0aaf5f) and `CP002_factory_start.png` (b854abed087e0c6a8b5229e452e7d7c9) = the candidate after PNGs (byte copies). A fresh render through the live script from ln04 matches them at max diff 0 (0 px differ) for both cams. Pre-keep heroes `renders/ln02/CP002_{lane,factory}_start.png` stay in place as the pre-KEEP frames.
- `--rebuild` vs live: **not exactly 0**. CP002_lane max 14, mean 0.0019, 3,790 of 921,600 px > 0, 4 px > 8. CP002_factory max 1, 206 px > 0. Cause: `build_cp002_street.py` is not byte-deterministic in face order. Two rebuilds have the same vertices (max delta 0.0), the same face sets and the same material indices, but the face index order differs in 20 meshes (LN2_Folk_00..16, LN2_Horse_6, LN2_Horse_92, LN2_Train), and the order also changes between two rebuilds. That changes Cycles BVH sampling and causes noise-level differences. The content is identical. The live blend is the frozen byte copy, so live renders are reproducible at max 0.
- Checks `checks/cp002_keep_checks_ln04.txt` + `checks/cp002_keep_diffs_ln04.json`. All 25 pre-existing blends/PNGs/JPGs outside renders/candidates are md5-unchanged. Pairs renamed KEEP_/REJECTED_/NOTE_ (pairs.json updated). Tag `pre_cp002lane_keep` (local). Not pushed.
- Note: survey `look/batch_mat_keeplight.py` still hard-codes ln02 -> renders/ln02/CP002_lane_start.png (the pre-keep frame). Use `render_cp002_lane_live.sh` for the live CP002 lane hero.

## 2026-11-16 CP005 planning room CANDIDATE (not live, no verdict) — DEPARTURES D-LN-CP005-01..10
- `scripts/build_cp005_room.py` opens live `rounds/ln02.blend` (md5 56e47151, unchanged) and saves `rounds/candidates/ln03_cp005.blend`. It replaces the PLANNING_ROOM set and its 5 figures with these: real 6-over-6 street windows with shutters and curtains, plus a first-floor view of a London stock-brick terrace across a 58 ft street; the bookcase moved off the camera; drab paper, a dado, a cornice and a carpet; a mahogany and baize table with chairs; a door; a London wall map; a chimneypiece; a gasolier; 1849-50 plans with no Crystal Palace drawings (`scripts/make_cp005_textures.py` -> `textures/cp005_*.png`); sample manufactured goods; and 5 modelled bareheaded gentlemen. check_set 29/29 (`checks/ln03_cp005_CANDIDATE_checks.md`).
- Renders: `scripts/render_cp005_candidate.py` uses the live CP005 recipe (survey look/batch_mat_keeplight.py: enhance + `--keep-lighting`, era 1850, 1280x720, 28 spp, exposure -0.10). CP002_terrace uses `--era 1840s`. Pairs are built by `scripts/make_cp005_pairs.py` into `renders/candidates/cp005_20261116/`. Hero CP005_room luma 109.47 (live PNG) / 112.44 (ln02 re-rendered today) -> 108.35. Side effects: CP005_table luma 215.22 -> 142.07 (content change); CP002_terrace no change (mean abs diff 0.37).
