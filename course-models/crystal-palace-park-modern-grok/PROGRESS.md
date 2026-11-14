# PROGRESS — crystal-palace-park-modern-grok

## r01 (2026-10-27)
- Branch `grok-park-modern` worktree at `/workspace/crystal-palace-park-modern`.
- Folder `course-models/crystal-palace-park-modern-grok/`.
- States: PARK54 (CP065), PARK60 (CP066), PARK-NOW (CP067–076).
- Appends Sydenham ruins41 + dinosaurs-1854 read-only.
- Rounds: `park54-r01.blend` (~2.0 MB), `park60-r01.blend` (~2.0 MB), `parknow-r01.blend` (~6.7 MB). All < 90 MB; no GLB/`.blend1`.
- Checks: `checks/r01_*.txt` — 0 FAIL each.
- Inferences logged in DEPARTURES.md and `*_info.json`.
- NOT pushed. Local commits only.

## r01b checkpoint (2026-10-27 02:14 UTC)
- PARK54 / PARK60 / PARK-NOW rebuilt: dino translate D-PM-08, camera purge, subway lights, cam fixes.
- Checks: r01_park54 / park60 / parknow — 0 FAIL.
- No OS/LiDAR in workspace (D-PM-01).

## Checkpoint crystal-palace-park-modern-grok quality round
- Patched scripts for quality pass; rebuilds pending lean hero renders.

## r02 (2026-10-27) — PARK-NOW quality + CP067/CP070
- `parknow-r02.blend` (~6.8 MB): richer grass/stone/NSC mats, trees, visitor silhouettes, CP067/CP070 cams.
- Lean heroes → `renders/r02/r02_CAM_CP{067,070,066,071,072,074,076}_*.png`.
- Soft cam-block: []. Local commit. NOT pushed.

## r17 WEAK→OK quality (in progress 2026-10-27 03:46 UTC)
- Targets: CP065/066/073 (PARK54/PARK60/PARKNOW).
- CP065 cam off gate → subway vault; CP066 NSC raised above park_slope + red track emit + SW 3/4 cam; CP073 mid-sphinx aim + warm stone; horizon berms.
- Rounds: park{54,60,now}-r17.blend. NOT pushed.

## r17k checkpoint (2026-10-27 04:00 UTC)
- CP065: sealed subway bulkhead at SUB_Z (was looking under street-level gate → distant ground).
- CP066/073: taller E/W/S berms + more aerosol (no shared look preset).
- Rebuild+lean re-render in flight.
- NOT pushed.

## r17 WEAK→OK done (2026-10-27 04:22 UTC)
- CP065/066/073 promoted ≥7. Heroes r17k. Subway seal + stadium track + sphinx framing. Local commit. NOT pushed.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## CP076 plateau CANDIDATE (2026-11-11 Grok; candidate only, no verdict)
- Scene: CP076 "Turn back toward the empty site" (closing shot). Live hero `renders/r01_parknow_CAM_CP076_empty_plateau_35mm.png` re-rendered from live `rounds/parknow-r02.blend` with `scripts/render_cp076_look.py` (dud-fix v4 recipe): max diff 0, so the before is the live frame.
- Weaknesses fixed: lollipop trees and stick visitors floating 7-34 m in the sky above the arcade (hidden dud-fix plateau); no upper-terrace ground; no present-day landmark.
- Candidate `rounds/candidates/parknow-r02_cp076plateau.blend` (`scripts/candidate_cp076_plateau.py`, DEPARTURES D-PM-26..31): trimmed Upper Palace Terrace grass, grounded trees/visitors, parametric trees + embankment scrub, 1956 transmitter lattice.
- Renders `renders/candidates/cp076_plateau_20261111/{before,after}_<cam>.png`, one camera per Blender session for both sides, exposure -0.8 both. Luma CP076 199.49 -> 187.22 (hold cam identical). Side effects: CP070 210.29 -> 208.10, CP072 194.87 -> 180.25 (foundations now under grass), CP073 191.44 -> 183.00, CP075 201.77 -> 200.56. Unchanged (noise only, max <= 10, <= 1 px > 8): CP066 nsc_wide, CP067, CP071, CP074.
- Pairs: survey `look/pairs_geo/CANDIDATE_CP076_plateau_start_{before,after,pair,detail_pair}.png`, `CANDIDATE_CP076_plateau_sidefx_{CP070,CP072,CP073,CP075}_{before,after,pair}.png` (`scripts/make_cp076_pairs.py`).
- Candidate md5 bc62d275 (compressed; rebuild is deterministic, object signature checked twice). Live `rounds/parknow-r02.blend` untouched (md5 48fc01ec). Not promoted; NOT pushed.

## CP076 plateau KEEP, scoped promotion (2026-11-11 Grok; parent viewed the pairs)
- Verdict: KEEP for CP076 (hero + hold cam). REJECT for the side effects on CP070 (loses the foundation-edge reading), CP072 (the footprint shot loses its foundations) and CP075 (new tree cuts the right edge). Those keep their current live heroes and blends.
- Scoped: new live blend `rounds/parknow-r21_cp076.blend` (md5 bc62d275d5d82e2c47d4ccbf03e4c6dd, byte copy of the candidate), used ONLY by the CP076 cams. `rounds/parknow-r02.blend` unchanged (md5 48fc01ec) and still serves CP067/070/072/074/075. Pre-KEEP state pinned by local tag `pre_cp076plateau_keep` (= 7d8d7cf).
- Manifest `scripts/parknow_live_heroes.json` (camera -> blend -> hero). Live render `scripts/render_cp076_plateau_live.sh [--rebuild] [outdir]` (dud-fix v4 recipe, exposure -0.8, one cam per session).
- Live heroes: `renders/r21_parknow_CAM_CP076_empty_plateau_35mm.png`, `renders/r21_parknow_CAM_CP076_hold_35mm.png`. Max diff 0 vs candidate afters. `--rebuild` regenerates r21 from parknow-r02 (md5-checked) and renders max diff 0 on both cams (rebuilt blend md5 differs only by save-time packing; the committed byte copy was kept). The old `renders/r01_parknow_CAM_CP076_empty_plateau_35mm.png` is now the pre-KEEP frame (left as is).
- Regression: CP066 (r17k stadium, r01/r02 nsc_wide), CP067, CP070, CP071 (r20), CP072, CP073 (r17k), CP074, CP075 live heroes byte-unchanged (md5); every pre-existing blend byte-unchanged.
- CP073 KEEP ON HOLD (not promoted): the live CP073 hero is `renders/r17k_parknow_CAM_CP073_sphinx_steps_50mm.png` from `rounds/parknow-r17.blend` (r17 along-terrace cam, 35 mm, 1920x1080, D-PM-19), but the candidate pair's "before" was the r02 50 mm cam, a different shot. True comparison for a fresh verdict: survey `look/pairs_geo/CANDIDATE_CP073_truelive_trio.png` (live r17k | candidate r02 cam | candidate with the live r17 cam, `renders/candidates/cp076_plateau_20261111/after_CAM_CP073_r17cam_35mm.png`). If kept, add CP073 to the r21 manifest and the live script.
- NOT pushed.

## CP073 KEEP on r21 with the live camera (2026-11-11 Grok; parent viewed the true trio)
- Verdict: KEEP option 3 of `look/pairs_geo/CANDIDATE_CP073_truelive_trio.png` (survey): the live r17 camera rendered on `rounds/parknow-r21_cp076.blend`. The green plateau ceiling is gone, clear sky, real arches, grounded trees. REJECT option 2 (the r02 50 mm cam, a different shot).
- CP073 now renders from r21 (md5 bc62d275, unchanged) with the exact live r17 `CAM_CP073_sphinx_steps_50mm` transform + 35 mm lens copied in-session from `rounds/parknow-r17.blend` (md5 a4d2ed90, checked) by `scripts/cp073_r17cam.py`; no blend is modified. Recipe `scripts/render_cp076_look.py` (look v1.1 present/exterior_afternoon, 1280x720, 32 spp, exposure -0.8), its own Blender session.
- Live hero: `renders/r21_parknow_CAM_CP073_sphinx_steps_50mm.png` (1280x720, luma 189.34; the r17k hero was 1920x1080, luma 165.51). Max diff 0 vs the trio's third render `renders/candidates/cp076_plateau_20261111/after_CAM_CP073_r17cam_35mm.png`. The old `renders/r17k_parknow_CAM_CP073_sphinx_steps_50mm.png` stays in place as the pre-KEEP frame.
- Manifest `scripts/parknow_live_heroes.json`: CP073 -> r21 (camera_from parknow-r17). `scripts/render_cp076_plateau_live.sh [--rebuild] [outdir]` now renders CP076 x2 + CP073.
- Regression: every other live hero and every blend byte-unchanged (47-file md5 list); CP076 x2 re-rendered max diff 0. `--rebuild` (to a scratch outdir) reproduces all three r21 heroes at max diff 0 (rebuilt blend md5 differs only by save-time packing; the committed byte copy was restored). Pre-KEEP pinned by local tag `pre_cp073_keep` (= 90223ae).
- NOT pushed.

## CP073 live hero back to 1080p (2026-11-11 Grok)
- Fix: the CP073 KEEP hero had dropped to 1280x720 (CP076 recipe default). Re-rendered at 1920x1080 for the film's 1080p delivery, same camera (live r17 cam on `rounds/parknow-r21_cp076.blend`, md5 bc62d275 unchanged), same look (present / exterior_afternoon), exposure -0.8.
- Samples: 24 spp = what the pre-KEEP r17k CP073 hero was actually rendered with (its PNG metadata `cycles.ViewLayer.samples` = 24; the r17 blend's scene setting is 48, overridden at render time by the lean r17k pass). Adaptive sampling 0.01 + OpenImageDenoise as before. A 48 spp test render differed from 24 spp by mean 0.42/255 with no visible difference.
- `scripts/render_cp076_look.py` takes optional `[WxH] [SAMPLES]` args (defaults 1280x720 / 32 spp unchanged). `scripts/render_cp076_plateau_live.sh` passes `1920x1080 24` for CP073 only; manifest CP073 entry records `resolution` 1920x1080, `samples` 24. CP076 cams unchanged (1280x720, 32 spp).
- Hero `renders/r21_parknow_CAM_CP073_sphinx_steps_50mm.png` replaced: 1920x1080, md5 1f53a8ac845d1d668cd3e7993ad543a9, mean luma 189.15 (720p version 189.34). Viewed: same content and framing as the 720p frame, sharper, no new noise or artifacts (downscaled to 720p: mean abs diff 1.1/255, only on edges).
- Live script reproduces all three r21 heroes at max diff 0; `--rebuild` (scratch outdir) reproduces all three at max diff 0 (rebuilt blend differs only by save-time packing; the committed byte copy bc62d275 was restored). Every other hero and blend byte-unchanged (70-file md5 list, only the CP073 hero changed).
- NOT pushed.

## CP070 Low Level station CANDIDATE (2026-11-13 Grok; candidate only, no verdict, NOT live)
- Why CP070: on the contact sheets of all live heroes outside the polished list it read worst: a third of the frame is a blank light-grey Parade road slab, the middle is the flat emissive footprint overlay with stick figures, haze, no station. It also contradicts the storyboard (visitor emerges from the SURVIVING station, establish the sign, walk 8 m to the park entrance; next-shot caption forbids implying subway adjacency) because the live cams stand at the former High Level site beside the subway.
- Live recipe found and reproduced at max diff 0: CP070 (both cams) and CP067 were rendered by dud-fix v4 BEFORE it hid `pk_grass_plateau` for CP075/CP076 and saved r02, so their live recipe = r02 + plateau shown (`scripts/live_plateau_show.py`) + `scripts/render_cp076_look.py` (exp -0.8 from the look). CP075 = saved state (hidden). NB the CP076 candidate's "CP070 side effect" before-frame (brick basement sides) was therefore not the live CP070 frame (green sides).
- Candidate `rounds/candidates/parknow-r02_cp070station.blend` (md5 22ee900f) by `scripts/candidate_cp070_station.py` from live r02 (48fc01ec, unchanged); DEPARTURES D-PM-33..41. Both CP070 cams MOVED (reframe) to the Low Level station (HE 1064353 NGR -> model (-260.0, -407.1) via the D-PM-31 grid).
- Renders `scripts/render_cp070_candidate.sh` -> `renders/candidates/cp070_station_20261113/{before,after}/` (1920x1080 48 spp, live recipe per cam, one cam per session, md5.txt, DONE). Pairs `python3 scripts/make_cp070_pairs.py` -> survey `look/pairs_geo/CANDIDATE_CP070_*`; numbers `checks/cp070_station_pairs.json`.
- Luma: CP070 begin_walk 212.14 -> 148.44; CP070 park_entry 212.14 -> 142.46; side effects CP075 201.62 -> 201.16 (station roof on far right horizon + replaced trees), CP067 165.80 -> 165.81 (one 9x10 px patch at the right edge).
- Checks: `checks/check_cp070_station.py` 13/13 (scope/state/grounding/walk 8.00 m/35 mm), `checks/check_cp070_station_dims.py` 13/13, `checks/dimension_check.py` on the candidate 11 PASS identical to live r02.
- Pre-candidate tag `pre_cp070station_cand` (= 0b1ecf3, local). Not done: promotion, manifest change, COVERAGE row change, any live PNG. NOT pushed.

## CP070 Low Level station KEEP, scoped promotion (2026-11-13 Grok; parent viewed the pairs)
- Verdict: KEEP for both CP070 cams (begin_walk, park_entry); the reframe is accepted (the old frame was an empty road slab). REJECT the CP075 and CP067 side effects: they stay on live parknow-r02.
- Scoped: new live blend `rounds/parknow-r22_cp070.blend` (md5 22ee900ffa91caa7494c0e8c4f2a35fc, byte copy of the approved candidate `rounds/candidates/parknow-r02_cp070station.blend`), used ONLY by CAM_CP070_begin_walk_35mm and CAM_CP070_park_entry_35mm. `rounds/parknow-r02.blend` unchanged (48fc01ec) and still serves CP067/072/074/075. Pre-KEEP state pinned by local tag `pre_cp070station_keep` (= 7c17249).
- Manifest `scripts/parknow_live_heroes.json` (CP070 x2 -> r22; `not_promoted_cp070_station` lists CP075/CP067). Live render `scripts/render_cp070_station_live.sh [--rebuild] [outdir]` (plateau shown + render_cp076_look.py CP070, exposure -0.8, 1920x1080, 48 spp, one cam per session); `--rebuild` builds from r02 into a temp blend and never overwrites r22.
- Live heroes: `renders/r22_parknow_CAM_CP070_begin_walk_35mm.png` (2267ba17), `renders/r22_parknow_CAM_CP070_park_entry_35mm.png` (c1e222e4). Rebuild from script max diff 0 on both; live = candidate after max diff 0 on both (`checks/cp070_keep_diffs_r22.json`). Pre-KEEP frames `renders/r02/r02_CAM_CP070_*.png` left in place.
- Checks on r22: `check_cp070_station.py` 13/13 (`checks/cp070_keep_checks_r22.json`), dims 13/13 (`checks/cp070_keep_dims_r22.json`), `dimension_check.py` 11 PASS identical to the candidate/live r02 (`checks/cp070_keep_dimcheck_r22.txt`).
- Regression: parknow-r02.blend and all renders/r02/*.png + renders/r01_*.png md5-unchanged; every pre-existing blend byte-unchanged.
- NOT pushed.

## CP066 NSC 1964-67 CANDIDATE (2026-11-14 Grok; candidate only, no verdict, NOT live)
- Why CP066: on contact sheets of every live hero outside the polished list (excluded CP006/009/011/013/014/018/021/022/023/026/027/029/031/032/034/044/051/056/060/063/070/073/076) it read worst at a glance: the "stadium" is four white boxes with flat pure-black tops round a square pink ring, a lit box for the sports hall, floodlight sticks. It is also the wrong shape for its date: in 1964-67 the NSC had ONE seated stand (West Stand); the Jubilee Stand opposite is 1977.
- Live recipe found and reproduced at max diff 0: `scripts/render_cp076_look.py` with scene id CP066 (look v1.1 present / exterior_afternoon, exposure -0.8) on `rounds/park60-r17.blend` at 1280x720 24 spp reproduces the live hero `renders/r17k_park60_CAM_CP066_nsc_stadium_35mm.png` (md5 9bad831f; the look v1.1 keep-better re-render of ed66c02) at max diff 0. Pairs use the same recipe at 1920x1080 48 spp both sides (before downscaled to 720p vs the live hero: mean abs diff 1.09/255, i.e. resolution/sample noise only).
- Candidate `rounds/candidates/park60-r17_cp066nsc64.blend` (md5 19af4411de9b598499c1f9ffe04c021b) by `scripts/candidate_cp066_nsc64.py` from live park60-r17 (9ea1c796, unchanged); DEPARTURES D-PM-42..49, dated May 1964 - May 1968: 440 yd cinder oval (8 x 4 ft lanes, chalk lines, kerb, infield, jump pit), 1964 West Stand (34 bench rows on concrete treads, sickle wrap 30.6 deg into each bend, cantilevered canopy over the straight), open east terracing + grass banks, arena floor dropped onto the terrain (-43.1, was a slab at -40), sports centre rebuilt at 1.75 acres (plinth, fully glazed upper storey, A-frame gables, vent tower; moved +27 m in x to clear the banks), re-grounded floodlight masts with lamp heads (r17 lights untouched), 14 athletes + 88 spectators. 24 r17 block-out meshes hidden (hide_render only). Camera NOT moved.
- Renders `scripts/render_cp066_candidate.sh` -> `renders/candidates/cp066_nsc64_20261114/{before,after}/` (md5.txt, DONE). Pairs `python3 scripts/make_cp066_pairs.py` -> survey `look/pairs_geo/CANDIDATE_CP066_*`; numbers `checks/cp066_nsc64_pairs.json`.
- Luma (hero, 1920x1080 48 spp): 167.02 -> 195.41 (the black box tops are gone; the frame is brighter overall). Side effects (other cams stored in park60-r17; NONE is a live hero): CP066 nsc_wide 169.30 -> 176.20 (now looks across the back of the West Stand + canopy columns instead of into a pink box); CP066 nsc_hall 32.17 -> 0.08 (this cam at (40, -520, -40) was already inside the old bank box and showed mostly black; it is now buried in the +x-bend terrace, fully black); park60 CP065 hl_closed 183.79 -> 183.79 (0 px > 8, no pair); park60 CP065 subway_threshold 91.54 -> 91.50 (40 px > 8, noise; CP065's live hero is on park54-r17 anyway).
- Checks: `checks/check_cp066_nsc64.py` 20/20 (no live object removed/moved, only tagged objects added, cameras + all lights unchanged, only the 24 nsc_ block-outs hidden, scene look/exposure/res/spp unchanged, masts grounded, no terrain through the arena floor, 440 yd lap, 8 x 4 ft lanes, 1.75 acres, ~10,400 seats, canopy clearance, no 1977 east stand).
- Pre-candidate tag `pre_cp066nsc_cand` (local). Not done: promotion, manifest change, COVERAGE row change, any live PNG. NOT pushed.
