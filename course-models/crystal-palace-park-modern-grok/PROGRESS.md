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
