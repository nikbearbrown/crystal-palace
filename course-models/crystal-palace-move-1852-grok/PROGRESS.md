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

## 2026-11-02 CP032 arrival near-foreground KEEP (live m02; DEPARTURES MV17)
- Parent reviewed `CANDIDATE_CP032_foreground_{start,end}_*` and kept both; survey pairs renamed `KEEP_CP032_foreground_*` with labels relabelled KEEP.
- Live `rounds/m02.blend` now carries the fix: `candidate_cp032_foreground.py --live` applied in place (grok_states `CP032_arrival` hides `CPL_HorizonGround`; ARR_CLAY -> `GT_SydenhamClayYard`; spoil heaps keep GT_SydenhamClay). Idempotent: a second run prints "already applied" and does not save; always prints `CP032_FG_IN_PLACE`. Pre-promotion m02 = move d9a9501 (backup `/workspace/backups/m02_pre_fg/m02.blend`).
- Live renders `renders/m02/CP032_arrival_{start,end}.png` from new `scripts/render_cp032_foreground_live.sh [--rebuild]` (render_shots.py, 1920x1080, 24 spp, look exposure, one Blender session per camera). Pixel-identical to the candidate afters / `KEEP_CP032_foreground_*_after.png` (max diff 0, 0 px differ) both from the live blend and after `--rebuild` (m02 @ d9a9501 + foreground --live).
- Refreshed from the live PNGs (`scripts/refresh_cp032_arrival_files.sh`): `renders/m02/CP032_arrival_{start,end}.jpg`, `renders/m02_png/CP032_arrival_start.{png,jpg}`, `renders/m02/contact_sheet_m02.jpg`.
- `build_m02.sh` re-applies the foreground fix and asserts `CP032_FG_IN_PLACE True` (hook tested on a copy of the pre-MV17 m02). `render_cp032_live.sh --rebuild` and `render_cp032_arrival_live.sh --rebuild` now also apply it, so neither rebuild drops MV17.
- Departure frames: CP032_departure_start rendered from live m02 differs from the pre-MV17 m02 render by noise only (max 3/255) and from the stored KEEP frame by the known MV16 noise (max 11/255). Stored departure renders left as they are.
- Next open weaknesses (arrival frames): the near yard is an empty, smooth plane (no cart ruts, stones, planks, puddles or tools); the pink spoil heap (GT_SydenhamClay) no longer matches the grey-brown yard; the sash-bar bundles bottom-left of the start frame are the brightest thing in the foreground.
- Look library follow-up (not edited): `_ensure_horizon_ground` places the disk at min(ground tops) - 0.02 m over all regions, so other multi-level / multi-region blends may have the same cut-through slab; audit later.
- `scripts/people_lib.py` uncommitted working-tree edit (3.3 statue exclusion) left untouched and uncommitted.

## 2026-11-02 CP032 arrival yard dressing (CANDIDATE, no verdict; DEPARTURES MV18)
- `scripts/candidate_cp032_yard.py` builds sibling `rounds/candidates/m02_cp032yard.blend` from live m02 (b19926f): cart ruts (wagon + two older tracks, 5 ft gauge, ray-conformed ribbons with wet grooves fading into the clay), rut and yard puddles, 320 stones/clods, deal walking boards + baulk, an elm navvy barrow with a shovel, a pick; the yard material `GT_SydenhamClayYard` rebuilt in place (darker trodden clay, wet patches, clods, grit); the spoil heaps get `GT_SydenhamSpoil1852` (grey-brown fresh-dug clay/gravel instead of pink) and subsurf/displace lumps; the arrival sash-bar bundles get weathered painted-deal materials with visible bar ends (departure bundles unchanged). All new objects are `ARR_YD_*` in ARR_SYDENHAM_1852.
- Checks `scripts/check_cp032_yard.py` → `checks/m02_cp032yard_checks.json` PASS: object set = live + 6 ARR_YD_* objects; every existing transform and mesh identical; slot changes only ARR_SPOIL and ARR_BARS_GUTTERS; modifier changes only ARR_SPOIL `CP032Y_*`; no dressing vertex over any ARR_HAND_* foot box; every free piece's lowest point within 6 cm of the clay (stones sink up to 5.7 cm, by design).
- `bash scripts/render_cp032_yard.sh [DIR]` rebuilds the candidate and renders before (live m02) / after for CP032_arrival_start and _end, each camera in its own session (render_shots.py, 1920x1080, 24 spp, look exposure). The before frames are pixel-identical to live `renders/m02/CP032_arrival_*.png` (getbbox of difference = None). `scripts/make_cp032_yard_pairs.py` writes `look/pairs_geo/CANDIDATE_CP032_yard_{start,end}_{before,after,pair}.png`; afters copied to `renders/candidates/cp032_yard_20261102/`. Mean luma start 160.55 → 149.92 (lower 40%: 170.31 → 149.06), end 159.02 → 150.30 (lower 40%: 170.25 → 151.87); sash-bar bundle region in the start frame (x 76–366, y 640–750) 177.0 → 99.6.
- Self-score 6/10. Known misses: the ruts are overlay ribbons, not real depressions, so they read as soft dark wheel bands rather than cut grooves; puddles are small, and the yard puddle by the barrow reads as a pale sliver; the stone scatter is fairly even confetti; the bar-end grid is too regular, like tiles; the oak bearers under the bundles (GT_OakBearer, shared) are still pale beige blocks; the yard is still soft at 1:1 and darker overall (mean luma −9 to −11); the spoil heaps are barely visible in either frame, so the palette fix hardly shows; arrival bundles are now dirtier than the same bundles in the departure frames.
- Promote if kept: `/workspace/blender5/blender -b rounds/m02.blend -P scripts/candidate_cp032_yard.py -- --live` (then a live render script and a build_m02.sh hook, not written until a KEEP).
- Live m02, renders/m02 and `scripts/people_lib.py` (an uncommitted 3.3 working-tree edit that is not mine) left untouched.

## 2026-11-02 CP032 arrival yard dressing KEEP (live m02; DEPARTURES MV18)
- Parent reviewed `CANDIDATE_CP032_yard_{start,end}_*` and kept both (the yard reads as worked ground; the bar bundles no longer glare); survey pairs renamed `KEEP_CP032_yard_*` with labels relabelled KEEP (`look/relabel_keep_cp032_yard.py`, verified against the original labels first).
- Live `rounds/m02.blend` now carries MV18: `candidate_cp032_yard.py --live` applied in place (ARR_YD_RUTS/PUDDLES/STONES/BOARDS/BARROW/TOOLS; GT_SydenhamClayYard rebuilt; ARR_SPOIL -> GT_SydenhamSpoil1852 + lumps; ARR_BARS_GUTTERS -> GT_SashBarWeathered / GT_GutterTimberWeathered). Idempotent: a second run prints "CP032_YARD already applied; nothing changed" and does not save (md5 unchanged); always prints `CP032_YARD_IN_PLACE`. Pre-promotion m02 = move b19926f (backup `/workspace/backups/m02_pre_yard/m02.blend`).
- Live renders `renders/m02/CP032_arrival_{start,end}.png` from new `scripts/render_cp032_yard_live.sh [--rebuild]` (render_shots.py, 1920x1080, 24 spp, look exposure, one Blender session per camera). Pixel-identical to the candidate afters `renders/candidates/cp032_yard_20261102/*` = `KEEP_CP032_yard_*_after.png` (max diff 0, 0 px differ) from the live blend and after `--rebuild` (m02 @ b19926f + yard --live).
- Hooks: `build_m02.sh` re-applies MV17 then MV18 and asserts `CP032_YARD_IN_PLACE True` (tested: full build to a scratch copy, BUILD_DONE, exit 0; a re-run on it says already applied). `render_cp032_live.sh --rebuild`, `render_cp032_arrival_live.sh --rebuild` and `render_cp032_foreground_live.sh --rebuild` now apply MV18 after MV17 with the same assert; all three rebuilds tested, and the arrival frames from each rebuilt blend are pixel-identical to the KEEP afters (max 0). The `KEEP_CP032_foreground_*_after.png` frames (MV17) now predate MV18 and no longer equal the live arrival renders.
- Refreshed from the live PNGs (`scripts/refresh_cp032_arrival_files.sh`): `renders/m02/CP032_arrival_{start,end}.jpg`, `renders/m02_png/CP032_arrival_start.{png,jpg}`, `renders/m02/contact_sheet_m02.jpg`.
- Departure spot-check (scratch renders, stored files untouched): CP032_departure_start from live m02 vs the pre-MV18 m02 max 10/255, mean 0.0003, 1500 px (25 px > 1/255); CP032_departure_end max 4/255, mean 0.0003, 1605 px (11 px > 1/255); scattered Cycles noise only. Stored `renders/m02/CP032_departure_start.png` left as is (still the known MV16 noise variant, max 11/255).
- Next open weaknesses (arrival frames): the background tree line is faceted low-poly "lollipop" trees in a flat lime field, the biggest non-period element at a glance in both frames; then the pale beige oak bearers and plain timber crates, ruts that read as flat dark bands rather than cut grooves, and the hatless workman's bald-looking head.
- `scripts/people_lib.py` uncommitted working-tree edit (3.3 statue exclusion) left untouched and uncommitted.

## 2026-11-02 CP032 arrival parkland oaks, meadow, timber, workmen hats (CANDIDATE, no verdict; DEPARTURES MV19)
- `scripts/candidate_cp032_trees.py` builds sibling `rounds/candidates/m02_cp032trees.blend` from live m02 (d1711db, MV18 live). The 83 ARR_OAK_* / ARR_OAK_EDGE_* trees behind the yard swap their mesh data from the 4 low-poly lollipop meshes (cone and icosphere balls) to 8 parametric open-grown oaks (2 per old height, 6.8k–12.3k leaf cards each, bark `GT_OakBark1852`, attribute-driven `GT_OakLeaf1852`). Transforms are unchanged, crown tops are within 5 cm of the old tops, and crowns are 0.85 x the height. ARR_GRASS gets `GT_SydenhamMeadow1852` (rough olive pasture with patch, swathe, tussock and straw-fleck variation). The arrival bearers and bundle bearers get `GT_OakBearerWeathered1852`. ARR_CRATE_0/1 instance an ARR-only copy of Muse's crate collection with weathered materials (Muse's collection and files untouched). The 4 arrival workmen get fitted felt wideawake hats and back/side hair (`ARR_HD_*`), and their flat people_lib cap disc is hidden by an object-linked transparent slot. The clerk keeps his top hat. DEP_* (Hyde Park 1851) objects and materials are unchanged, and so is the wagon.
- Checks `scripts/check_cp032_trees.py` → `checks/m02_cp032trees_checks.json` PASS:
  - object set = live + 8 ARR_HD_* + 20 ARR_SY_* crate copies;
  - no transform changes;
  - mesh changes only on ARR_OAK_*;
  - slot changes only on the listed ARR objects;
  - instance changes only on ARR_CRATE_0/1;
  - no DEP object touched;
  - each hat is centred on its skull (0 mm off axis), with its base 9–10 cm below the head top and its top 5 cm above.
  - Oak polys (sum over objects, instanced data): 60,756 → 450,538.
- `bash scripts/render_cp032_trees.sh [DIR]` renders before (live m02) and after for CP032_arrival_start and _end. It uses render_shots.py at 1920x1080, 24 spp and look exposure, with each camera in its own session. The before frames are pixel-identical to live `renders/m02/CP032_arrival_*.png` (max diff 0). `scripts/make_cp032_trees_pairs.py` writes `look/pairs_geo/CANDIDATE_CP032_trees_{start,end}_{before,after,pair}.png`, and the afters are copied to `renders/candidates/cp032_trees_20261102/`. Mean luma: start 149.92 → 139.63 (lower 40%: 149.06 → 146.69); end 150.30 → 139.44 (lower 40%: 151.87 → 150.47).
- Self-score 6/10. Known misses:
  - The trees now read as broadleaf parkland trees, but at 1:1 the leaf cards show as spotty confetti at the crown edges.
  - All 83 trees are one species and habit from 8 meshes, in a fairly even row, with a too-uniform dark value and no aerial-perspective falloff on the far ones.
  - The trunks read a little cool and dark.
  - The meadow variation is still faint at this distance; it reads mostly as a flat olive plane.
  - The hats are simple turned shapes, and the hair is barely visible from these angles.
  - The bearer and crate timber is now grey-brown, but the bearers are still plain cuboids.
  - The cart ruts (flat bands) were not touched.
  - Frames are about 10 luma darker overall, mainly from the darker tree band.
- Promote if kept: `/workspace/blender5/blender -b rounds/m02.blend -P scripts/candidate_cp032_trees.py -- --live`. The live render script and the build_m02.sh hook are not written until a KEEP.
- Live m02, renders/m02 and `scripts/people_lib.py` (an uncommitted working-tree edit that is not mine) were left untouched.

## 2026-11-02/03 CP032 arrival parkland oaks, meadow, timber, workmen hats KEEP (live m02; DEPARTURES MV19)
- Parent reviewed `CANDIDATE_CP032_trees_{start,end}_*` and kept both; survey pairs renamed `KEEP_CP032_trees_*` with labels relabelled KEEP (`look/relabel_keep_cp032_trees.py`; checked that the original labels rebuild the old pair files exactly and the new pairs differ only in the label strip, y 0–30).
- Live `rounds/m02.blend` now carries MV19: `candidate_cp032_trees.py --live` applied in place (83 ARR_OAK* swapped to 8 parametric open-grown oaks; ARR_GRASS -> GT_SydenhamMeadow1852; weathered ARR bearers + ARR-only weathered copy of Muse's crate collection; ARR_HD_HAT felt hats + hair on the 4 arrival workmen). Idempotent: a second run prints "CP032_TREES already applied; nothing changed" and does not save; always prints `CP032_TREES_IN_PLACE`. Pre-promotion m02 = move d1711db (backup `/workspace/backups/m02_pre_trees/m02.blend`).
- Live renders `renders/m02/CP032_arrival_{start,end}.png` from new `scripts/render_cp032_trees_live.sh [--rebuild]` (render_shots.py, 1920x1080, 24 spp, look exposure, one Blender session per camera). Pixel-identical to the candidate afters `renders/candidates/cp032_trees_20261102/*` = `KEEP_CP032_trees_*_after.png` (max diff 0, 0 px differ) from the live blend and after `--rebuild` (m02 @ d1711db + trees --live).
- Hooks: `build_m02.sh` re-applies MV17, MV18, then MV19 and asserts `CP032_TREES_IN_PLACE True` (tested: full build to a scratch copy, BUILD_DONE, exit 0; a re-run on it says already applied). `render_cp032_live.sh`, `render_cp032_arrival_live.sh`, `render_cp032_foreground_live.sh` and `render_cp032_yard_live.sh --rebuild` now apply MV19 after MV18 with the same assert; all four rebuilds tested, and the arrival frames from each rebuilt blend are pixel-identical to the KEEP afters (max 0). The `KEEP_CP032_yard_*_after.png` frames (MV18) now predate MV19.
- Refreshed from the live PNGs (`scripts/refresh_cp032_arrival_files.sh`): `renders/m02/CP032_arrival_{start,end}.jpg`, `renders/m02_png/CP032_arrival_start.{png,jpg}`, `renders/m02/contact_sheet_m02.jpg`.
- Departure spot-check (scratch renders from the pre-MV19 and live m02, same settings; stored files untouched): CP032_departure_start max 16/255, mean 0.016, 78k px (1,343 px > 1/255); CP032_departure_end max 21/255, mean 0.016, 81k px (1,198 px > 1/255); mean luma unchanged (176.60 vs 176.59). The differences are scattered Cycles noise, concentrated in the Hyde Park foliage (the scene BVH changed); no Sydenham object shows in the departure frames (MV07: Hyde Park and Sydenham never blended). `render_cp032_live.sh --rebuild` rewrites `renders/m02/CP032_departure_start.png`; that rewrite was reverted, so the stored file is still the known MV16 noise variant.
- Next open weaknesses (arrival frames): confetti-like leaf-card crown edges at 1:1; one even row of trees of a single habit, with uniform dark value and no aerial haze or falloff on the far ones; the meadow is faint and reads as a flat olive plane; the bearers are still plain box cuboids; the ruts are still flat dark bands rather than cut grooves; frames are about 10 luma darker than before MV19 (mostly the darker tree band; lower 40% within ~2). Also seen: the ironwork (column, girder, pipes) is a flat saturated toy blue with no paint wear, and the figures are grey mannequins with pale faces. (The Hyde Park departure frames still have the low-poly lollipop trees; that is a separate DEP job.)
- `scripts/people_lib.py`: the uncommitted working-tree diff is the Oct 27 v3.2 -> v3.3 statue/plinth exclusion and is not part of MV19 (hats and hair are made by `candidate_cp032_trees.py` itself). It is not used at render time either: `cpl_people.py` falls back to the survey `people/people_lib.py` v3.4 (renders log `PEOPLE 3.4`). Left uncommitted in the working tree as before; backup at `/workspace/backups/people_lib_v3.3_uncommitted_20261027.patch`.
