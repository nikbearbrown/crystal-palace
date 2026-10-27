# PROGRESS: HP-FITOUT + HP51 (Grok Bot)

Branch `grok-fitout-1851` (worktree /workspace/crystal-palace-fitout). Local commits only; no push; Professor Bear reviews first.

- **f01 (2026-10-27), fitout state (CP018-CP020):**
  - Paint: 479 painted, 8 half, 313 primer. 14 painters, 2 ladders, 6 cradles.
  - Doors open, with a dray and trucks.
  - Floor: 18 Muse floor tiles and 32 loose boards; sweeper and hand-engine.
  - Checks: D 40/40, state 48/48. 8 renders.
- **h01 (2026-10-27), hp51 state (CP026-CP028):**
  - Shilling crowd 531/660 re-dressed. 4 turnstiles, 2 pay boxes, 3 police, queue of 140.
  - 6 stair visitors. 3 Muse louvres with a rope attendant. 3 watering attendants.
  - Checks: D 39/39, state 38/38. 6 renders.
- **c01 (2026-10-27), closing state (CP029):**
  - Dais, canopy, chair, 27 dais figures; 620 floor and 260 gallery spectators.
  - Autumn elms and an October sun.
  - Checks: D 35/35, state 15/15. 2 renders.
- **Exposure fix:** CP019_dray and CP026_shilling_ext re-rendered at exposure -0.7 (FT38).
- **Open / next:**
  - The CP028 louvre shot frames the wall below the Muse louvres: tilt it up or use 35 mm.
  - The CP029 gallery shot has a spectator in the left foreground: add a cam_conflict filter on gallery spawns.
  - Half-painted columns read faintly: make the paint cut a sharper band and add drips and drop cloths.
  - The CP019 doors shot needs more crates in transit.

## f02 / h02 / c02 (2026-10-27): quick fixes 1, 2, 4
- FT39 pale exterior timber/boarding tone; FT40 CP029 gallery foreground filter; FT41 CP028 louvre camera tilt.
- Parked as backlog: sharper half-paint bands with drips; workshop belts and shavings / shop lighting / loading-door view (fitout next 3 and 5).
- Checks: f02 40/40 dims + 48/48 state; h02 39/39 + 38/38; c02 35/35 + 15/15.
- Renders: renders/f02/CP019_dray_start; renders/h02/CP026_shilling_ext_start, CP028_louvre_start; renders/c02/CP029_gallery_start, CP029_dais_start.

## f03 / h03 / o01 (2026-10-27): quality + opening gap fill
- FT41 darker boarding albedo (material not exposure); FT42 hex fountain prisms + glass_solid sparkle; FT43 `--state opening` (CP021/CP022).
- Horse harness + darker coats in fitout. Checks: f03 40/40 + 48/48.
- Renders: f03/, h03/, o01/.

## em01 / dm01 (2026-10-27): HP-EMPTY + HP-DISMANTLE gap fill
- empty (CP030): crates replace exhibits.
- dismantle (CP031): shores, stacks, joint hero.
- DEPARTURES FT44–FT45.
- Checks: em01 state 19/19; dm01 state 15/15 (dims DRESS fails expected).
- Renders: renders/em01/CP030_*; renders/dm01/CP031_*.
