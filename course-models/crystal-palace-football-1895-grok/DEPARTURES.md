# DEPARTURES — G-FOOTBALL (CP050, CP055)

| id | decision | why | grade |
|---|---|---|---|
| FB01 | Append Sydenham shell from `sydenham-1856-r13.blend` read-only (link=False); never edit the Sydenham folder | Reuse the park palace on the skyline. | A |
| FB02 | Drop north transept (lost 1866), waterworks sprays, Muse court props, and south-basin water near the pitch | 1895/1913 state; pitch sits in the drained south basin. | A |
| FB03 | Pitch ~110×70 m at centre (−158, −598, −47.5); natural bank on −y rising ~12 m; pavilion/stand on +y | Crystal Palace FC ground in the park; bank is the famous "natural terrace". | A |
| FB04 | Crowd as point-cloud + Geometry Nodes Instance-on-Points (low-poly variants). 1913 ≈ 120k at ~3.8/m²; 1895 quieter (~20k). Camera clear holes. | 1913 Cup Final attendance ~120,000; GN keeps the .blend manageable. | B |
| FB05 | Eye 1.6 m over the local bank/pitch surface (metres file); lenses 35 bank / 28 pitch-side | Camera grammar adapted to metres Sydenham space. | B |
| FB06 | Build flag `--state 1895|1913` (default 1913 for the Cup Final hero shot) | Two story beats, one script. | B |
| FB07 | Sink `park_slope` −20 m over the south basin; clear basin water/stone/sprays by bound-box centre (not origin) | Sydenham park_slope lids the basin at ~−45.9 above the pitch; origin-based delete missed world-baked meshes. | B |
| FB08 | check_set skips non-route (Sydenham) cameras and FB_Var/Crowd hits; 1895 state zeros crowd_1913 min | Appended shell otherwise fails eye/roll matching. | B |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| FB04 | 36 hero figures near bank/pavilion/pitch cams; darker turf/bank albedo; turf strip on pitch | Sparse near-camera figures; flat green | B |

## People library v3.1 adopt (2026-10-27) — football crowds

| Shot | Era | Verdict | Note |
|---|---|---|---|
| CP050 bank 1895 | 1890s Victorian | REVERT | mid-ground stand reads darker/muddier vs before; grade otherwise OK |
| CP055 bank 1913 | 1910s→1890s stand-in | REVERT | overall grade brighter/washed; pavilion band darker |

### Departures
- 1913 uses 1890s bustle/boater stand-in (same as Sydenham late11) — no true 1910s day-dress set in v3.1.
- Crinoline hem capped ~0.9–1.0 m; lighter mid-tone skirts (shared survey `people_lib.py`).
- Heroes left at pre-adopt PNGs after keep-better revert.

## People library v3.3 adopt (2026-10-27) — football crowds

Retry of v3.1-reverted CP050/CP055 with people_lib 3.3 + `--keep-lighting`. Honest keep-better by viewing:

| Shot | Era | Verdict | Note |
|---|---|---|---|
| CP050 bank 1895 | 1890s | REVERT | pale/stony foreground vs varied before; stand muddier |
| CP055 bank 1913 | 1910s | REVERT | pale/ghostly bank + washout ~1.12×; contrast lost |

Heroes left at pre-adopt PNGs. Pairs under `people_v33/previews/`.

## People library v3.4 — close-up gate (2026-10-27)

Synced people_lib 3.4 (`CLOSE_UP_FRAME_FRAC`). No football keeps this round (CP050/055 already reverted).
