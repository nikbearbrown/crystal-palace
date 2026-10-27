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
