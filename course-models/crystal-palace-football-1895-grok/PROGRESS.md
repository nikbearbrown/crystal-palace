# PROGRESS — G-FOOTBALL

## fb01 / fb01_1895 (2026-10-27)
- Append Sydenham r13 read-only; drop N transept / waterworks / Muse; clear south-basin water; sink park_slope over drained pitch (FB02).
- Pitch 110×70 m at (−158, −598, −47.5); natural bank + pavilion/stand; GN crowd.
- **1913** `rounds/fb01.blend`: crowd_1913=121000, 16.5 MB, checks **22/22**.
- **1895** `rounds/fb01_1895.blend`: crowd_1895≈7873, 14.8 MB, checks **22/22**.
- Finals: `renders/fb01/` (CP055), `renders/fb01_1895/` (CP050).

## fb02 (2026-10-27): quality pass — denser heroes, turf/bank
- 36 hero figures near bank/pavilion/pitch cams (FT=0.3048); darker turf/bank albedo; turf strip.
- DEPARTURES FB04. Renders/fb02/.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## CP050 CANDIDATE 2026-11-16: FA Cup Final 20 April 1895 (not live, no verdict)
- `rounds/candidates/fb02_1895_cp050cup.blend` on live `rounds/fb02_1895.blend` (d8b263c0, unchanged); D-FB-CP050-01..10.
- Box crowd -> 42,560 people_lib 1890s spectators; goals onto the 70 m lines (the pitch is now within the 1891 law); 1892 markings; nets; 22 players (Villa v WBA), referee, 2 linesmen, ball.
- Live recipe both sides (render_views.py, file exposure 0.0, no people swap), 1920x1080 48 spp: `renders/candidates/cp050_cupfinal_20261116/`.
- Hero CP050_bank luma 226.16 -> 219.73; side effect CP050_pavilion 223.13 -> 162.72. Checks 20/20 (`checks/cp050_cupfinal_checks.json`); rebuild renders with max diff 0.
- CP050 row and live renders unchanged; nothing routed.

## 2026-11-16 CP050 FA Cup Final 1895 KEEP (scoped, live) — DEPARTURES D-FB-CP050-11
- Parent viewed the pairs: KEEP for `CP050_bank_1895_start` only. Side effect REJECTED: `CP050_pavilion_1895_start` (luma 223 -> 163, a wall of backs blocks the pitch); stays on `rounds/fb02_1895.blend` (d8b263c0, unchanged). CP055 1913 cams stay on `rounds/fb02.blend`.
- Live round `rounds/fb04_1895_cp050cup.blend` = byte copy of `rounds/candidates/fb02_1895_cp050cup.blend` (md5 27e0525d2e97bc2c37da9af9f61c40a4). (fb03/fb03b_1895 = reverted set_v18 attempt, not used.)
- Routing `scripts/football_live_heroes.json` (new): CP050_bank_1895_start -> fb04_1895_cp050cup; CP050_pavilion -> fb02_1895; CP055 cams -> fb02.
- Render `scripts/render_cp050_cup_live.sh [--rebuild] [outdir=renders/fb04_1895]` (render_views.py, file exposure 0.0, no people swap, 1920x1080, 48 spp; --rebuild regenerates from fb02_1895 into a temp blend, never overwrites fb04).
- Live hero `renders/fb04_1895/CP050_bank_1895_start.png` (luma 219.73). Live = candidate after: max diff 0. --rebuild vs live: max diff 0. Pre-keep hero `renders/fb02_1895/CP050_bank_1895_start.png` stays as the pre-KEEP frame.
- Checks `checks/cp050_keep_checks_fb04.txt` + `checks/cp050_keep_diffs_fb04.json`; 27 pre-existing blends/PNGs md5-unchanged. Tag `pre_cp050cup_keep` (local). Not pushed.
