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
