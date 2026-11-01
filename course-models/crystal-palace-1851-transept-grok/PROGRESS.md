# PROGRESS: Hyde Park 1851 transept (Grok Bot)

Branch `grok-transept-1851` (local only, nothing pushed). Blender 5.1.2 at /workspace/blender5/blender.

## Decisions so far (r01)
- Axes and origin = Claude's frame: metres, origin at the nave/transept crossing, floor top z=0, X east along the length, Y north across the width. Line i of Claude's frame is at x = -924 + 24 i ft; his line 37 is x = -36 ft (transept west column line).
- Transept block built: |x| <= 132 ft, y -204..204 ft. Tier 3 (vault + lead flats) |x| <= 60; tier 2 arms 60..132 (Plate III cross-shaped plan above galleries).
- Vault springing z = 65.0 ft (Plate VII reads ~65.9 by eye), so the rib extrados crown = 65 + 37.17 = 102.17 ft = the 1856 guide's 102 ft 2 in.
- Main ribs A every 24 ft (on column rows, the two over the nave on the 72 ft trusses at y = +-12); intermediate ribs B every 8 ft (inferred).
- Galleries: Plate II: void runs y -156..180; 48 ft south cross gallery, 24 ft north cross gallery; 24 ft side strips |x| 36..60.
- Elms: 3, positions inferred from the Talbot south view and the empty-transept north photo.

## Log
- r01: frame, vault, glazing, end screens, galleries, elms v1 (blobby) -> checks 38/38. Renders in renders/r01 (960x540 previews).
- r02: elms rebuilt as branching tubes + leaf cards. CP017 end stop moved to (-26,-154), looking up at canopy + vault.
- r03: denser and wider elms, dark bark. Full render set (1280x720, 64 spp) launched detached: scripts/render_round.sh r03 -> /tmp/r03.log
- r04: elm branches clamped to the vault/column envelope (checks 38/38). Renders launched: /tmp/r04.log
- r04 renders done (1280x720, 48 spp). Compare sheets: compare/r04_*.jpg. Self-score r04: 6.5/10. Frame, vault and fan read; the elms read as umbrella pines; the Plate VII sheet is mis-framed; the combo has a dark band beyond the ground plane.
- r05: elm lower limbs (checks 38/38). Renders launched -> /tmp/r05.log. Script now has an 18,000 ft ground plane and a wider ortho (for r06).
- r05 renders and compare sheets done. Self-score r05: 7/10.
  - Good: the elms now read as broad-leaved park trees, the vault, fan and ridge-and-furrow read, and all 38 checks pass.
  - Misses:
    - The CP017 stop is too close: the canopy fills the frame, so the roof clearance is not readable.
    - The leaf cards are too large up close.
    - The fan glass washes out against the sky (the Talbot view shows a dark fan).
    - The Plate VII sheet is partial.
    - No fountain or exhibits.
    - Colours are neutral.
- Next (r06): move the CP017 end stop to about y=-162 and aim it at the canopy edge and the vault gap; halve the card size near the cameras; darken the end-screen glass and bars; build the Osler fountain; add the arm galleries.
- r06 (built from scripts/build_transept.py, checks 43/43 in checks/r06.md). Renders: renders/r06 (1280x720, 48 spp); Owen Jones toggle set in renders/r06/owen. Compare sheets: compare/r06_*.jpg.
  - Changes:
    - The CP017 end stop is pulled back, and the leaf cards near the cameras are smaller.
    - The end-screen glass and bars are darker.
    - The Osler crystal fountain is at the crossing: glass tiers on a basin kerb.
    - The arm galleries and stairs are in (Downes II/XV-XVII).
    - The ground-plane fix: REV_ext34 shows a continuous lawn.
    - A wider Plate IV/VII ortho.
    - The Owen Jones colour toggle (`--owen`), with blue, red and yellow stripes on the columns and girders (OJ01/OJ02).
  - Self-score r06: 7.5/10.
    - Good:
      - The fountain reads as glass and sits correctly under the crossing.
      - The CP017 stop now shows the floor, the gallery underside and the canopy together.
      - The combo with Claude's west frame and the exterior lawn is continuous.
      - The Owen colouring reads at gallery-rail scale.
  - Misses:
    - In the Talbot view the fan still does not read dark: the elm canopy hides most of it, and the reference camera is probably too low or too far north.
    - The fountain is too thin and too short against the Talbot one, which rises past the gallery rail.
    - There are no exhibits, statues, or the iron railing of the Talbot foreground.
    - The roofs read as white slabs from outside.
    - The overall contrast is low (no sepia or overcast grade).
- Next (r07):
  - Move REF_talbot back about 30 ft and up to the gallery-rail sightline. Scale the fountain to about 27 ft (the 1851 catalogue).
  - Add statue and railing proxies.
  - Make the outside roof glass less white (a grey glass and lead tint on the furrows), and grade the exposure.
- r07 (scripts/build_transept.py, checks 43/43). Renders: renders/r07 (1280x720, 48 spp), Owen set renders/r07/owen; compare sheets compare/r07_*.jpg. Note: the box restarted mid-round and wiped /tmp; the round was re-run, logs now in /workspace/logs.
  - Changes: REF_talbot raised to 24 ft at the gallery-rail sightline (C06, the 30 ft pull-back is blocked by ELM_NORTH2's crown); fountain scaled to ~27 ft; statue proxies at x = +/-14 and the curved iron railing; RL02 render-time override of Claude's PART_RoofUnit MAT_Glass with GT_Glass (his file never saved; `CLAUDE_ROOF_OVERRIDE slots 1` in the log).
  - Self-score r07: 7.8/10.
    - Good: Talbot composition now reads (railing foreground, fountain on axis, elm behind, statues lining the nave edge); Owen set unchanged and stable.
    - Misses: the fountain is now too near/large in the Talbot frame (the photo puts it ~60 ft further south); the south end fan still reads light, not as the dark radiating lunette; REV_combo still clips the roofs to white on BOTH halves. Part of this is exposure in the transept scene. Part is a real override bug (RL03, found in exterior x04): Claude's roof mesh has no UVs, so our UV sash-bar mask painted his whole sheet as bar. Fixed in render_views.py, and REV_combo was re-rendered as r07b with the exterior roof-glass recipe (RL04), so the roofs now read grey glass, but Claude's flat 2-poly sheets still look flat; no exhibits or plants under the galleries.
- Next (r08): move the REF_talbot camera north ~40 ft along the axis (or a 35 mm with a lower target) so the fountain sits at mid-ground; darken the lunette sash bars and add the radial fan glazing bars; give REV_combo its own exposure (-0.6 like the exterior EX10) so the seam check is meaningful; exhibit and plant proxies under the galleries.
- r08 (scripts/build_transept.py, checks 44/44 in checks/r08; new PROPS_muse check). Renders: renders/r08 (1280x720, 48 spp); compare sheets compare/r08_*.jpg. No Owen set this round.
  - Changes:
    - Exhibit proxies appended read-only from Muse's models/ on origin/main adb0d2c, credited to Muse on each collection and instance (MC03, MC08): 48 vitrines (hp-crate-and-display-case), paired per bay down both aisles under the galleries; 12 display plinths (display-plinth) on the aisle line; 4 benches (park-bench) in the transept.
    - REV_combo uses its own exposure (−0.6) and the exterior roof-glass recipe on both halves (RL04).
  - Self-score r08: 8.0/10.
    - Good: the aisles now read as an exhibition, with cases in rhythm with the bays. The combined review roofs read as glass, not white.
    - Misses:
      - The Talbot framing is unchanged (fountain still too near; C06 constraint).
      - The south lunette fan is still light.
      - Muse's ebonised plinths read as black boxes in CP017 and are empty.
      - There are no plants under the galleries.
      - Claude's roofs are still flat sheets in REV_combo.
- Next (r09):
  - A ridge-and-furrow proxy for the combined-review roofs, instanced from Muse's hp-roof-furrow-bay (credited).
  - Statue proxies on the Muse plinths, or plinths moved under our statues.
  - Darken the lunette bars.
  - A Talbot camera with a lower target.
  - Planter proxies.
- r09 (scripts/build_transept.py + new scripts/dressing.py, figures.py, furrow.py; checks/r09). Renders: renders/r09 (1280x720, 48 spp); compare sheets compare/r09_*.jpg.
  - Changes:
    - The mannequin statue placeholders are replaced by classical stand-ins from figures.py: draped standing figures, a seated figure, an equestrian group, the Amazon group and busts, all on moulded stone pedestals. Muse's empty plinths now carry busts and urns (ST03–ST09).
    - Exhibition dressing (dressing.py, everything tagged `dress_kind` so HP-EMPTY/DISMANTLE can strip it):
      - flags and banners hung from the galleries
      - hung carpets and textiles
      - machinery block-outs in the east nave (locomotive, steam, beam and marine engines, hydraulic press, power looms, reaper, printing machine)
      - sculpture groups
      - palm and orange-tree planters
      - 324 crowd stand-ins (CR01)
    - Darker lunette bars and end-screen glass (L02).
    - REF_talbot on the floor at eye height (C07).
    - CP023_into_nave camera (CP23).
    - The furrow roof module for the combined views (RL05, render scripts only).
    - figures.horse_group_mesh(base=...) param for reuse.
  - Self-score r09: 8.2/10.
    - Good: the aisles now read as a crowded show; Talbot reads with the fountain at mid-ground; the plinths are no longer empty black boxes.
    - Misses:
      - The planters read as green balls.
      - The figures are still low-poly and read as toy-like at close range.
      - The standalone CP023 shows open sky east of x 60 (by design; use the x05 combined render).
      - The lunette is darker but still not as black as in Talbot's photograph.
      - The crowd density is far below 1851.
- Next (r10): give the planters fronds/tub shapes; add more figure variety and a darker grade; move the machinery to the west/Claude zone if he agrees (proposal); refine the lunette.

## r10 — checkpoint (render running)
- Done:
  - Planters: PL02 fronded palms, PL03 orange-tree tubs.
  - Figures: F04 variety (frock coats, caps, shakos, shawls, boys, soldiers) and F05 scale jitter.
  - Crowd: F06 denser (floor 540, galleries 120).
  - Grade: G03 exposure -0.7.
  - Lunette: L03 darker and blacker, with 8 in radial bars.
  - MX02: machinery stays east.
- Build and checks: rounds/r10.blend, checks/r10 49/49. Render renders/r10 at 1280x720/48 is queued after d03.

## r10 — FINAL
- Renders: renders/r10 (15 frames plus _contact_r10.jpg). Compare sheets: compare/r10_*.jpg. Checks 49/49.
- Self-score: 7.5/10.
- Wins:
  - The palms now have fronds.
  - The crowd is denser and more varied: frock coats, shawls, children, redcoats.
  - The lunette reads dark, and the -0.7 grade gives the ironwork contrast.
- Misses:
  - The fountain glass still reads as chrome and steel rather than crystal.
  - The figures are still low-poly blocks.
  - The REF_talbot frame is too bright on the floor.
  - The orange tubs are small in frame.
- Next r11:
  - Fountain glass IOR/tint and caustic-free transmission.
  - Floor albedo down about 10%.
  - Figure heads and arms refined.
  - Gallery crowd up again.

## Backlog (parked 2026-10-26)
- r11 parked by Professor Bear's instruction: polish rounds now give diminishing returns; work moved to unbuilt sets (HP-SITE, MOVE+K-JOINT).
- Parked r11 items: fountain glass; floor albedo -10%; figure heads/arms; more gallery crowd.

## r11 (2026-10-27): fountain glass, darker floor, figure limbs, denser galleries
- Parked r11 backlog cleared in one round.
- Build: `rounds/r11.blend`. Checks: `checks/r11` 49/49.
- Dressing: floor crowd 540, gallery 180 (110+40+30).
- Lean renders: `renders/r11` (1280×720, 24 spp) — DET_fountain, OPEN_gallery, CP023_into_nave, CP017_park_inside.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP008/017/023; lib 3.1

## people v3.2 2026-10-27
- people v3.2 keep-lighting: keep CP023; revert CP008/017

## 2026-11-01 HP interior envelope (CP023) still CANDIDATE
- Oct 27 candidate `rounds/candidates/r11_envelope.blend` rendered blown out (scene exposure 0.4). Review renders at -1.6 and -2.2 (in /workspace/tmp/envjudge/cp023) read well: nave, galleries, OJ columns, locomotive, no sea horizon.
- Not promoted: the envelope changes all 14 transept cameras, including the exteriors, and the transept pipeline has no per-shot exposure yet. Next step: per-shot exposure (-2.2 for CP023) and a full-camera check before a keep call.

## 2026-11-01 envelope full-camera check (CANDIDATE pairs; no keep/revert call)
- Per-shot exposure added to `scripts/render_views.py`: table `SHOT_EXPOSURE` = {CP023_into_nave_start: -2.2, CP023_into_nave_end: -2.2}. Opt-in with `--shot-exposure`; without the flag every camera renders exactly as before, and cameras not in the table keep the look/scene/`--exposure` value. `render_round.sh` (live pipeline) unchanged and does not pass the flag. Pattern from the exhibits folder's per-shot `--exposure`.
- `scripts/render_envelope_check.sh`: 15 cameras (the 14 in render_round.sh + CP008_build_around_start) from live `rounds/r11.blend` (no table) and from `rounds/candidates/r11_envelope.blend` (`--shot-exposure`), both through apply_look interior_daylit, 1280x720, 28 spp, people v3.4, Blender 5.1.2 headless. Output `renders/candidates/envelope_check_20261101/{live,candidate}`. REV_combo not rendered (needs Claude's blend appended).
- Pairs (`scripts/envelope_pairs.py`): `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_<CP|REVIEW>_transept_envelope_<cam>_pair.jpg` (15). All CANDIDATE; nothing promoted.
- "Before" is a fresh live render with the current shared people library, so crowds differ from the committed renders/r11 PNGs (same crowd in both halves of each pair).
- What changed (executor notes, reviewer decides):
  - CP023 start/end: open sky east replaced by enclosed nave (glazed roof, blue/yellow ironwork, cream walls), not blown out at -2.2. Ironwork reads saturated yellow; walls flat cream.
  - Osler fountain (REF_elm_north, REV_int_up, DET_fountain, faint in REF_talbot): candidate fountain reads milky/ghost-pale, losing the dark cut-glass tiers. Cause: `brighten_host_glass()` matches any material with "glass" in its name, including the fountain glass (alpha <= 0.35, transmission >= 0.85). Regression.
  - Exteriors REV_ext34, REV_south: lawn gone (GROUND_PARK hidden) -> pale grey ground; REV_ext34 also shows the east-nave seal as a plain white box beside the transept. Regression. PLATE_IV ortho: glass slightly paler, otherwise near-identical.
  - CP008 start/end, CP017 start/end, REF_absolon, OPEN_gallery, REF_talbot: slightly brighter/paler glass and sky beyond, otherwise near-identical; REF_absolon/OPEN_gallery lose some depth in the far nave haze.
- Live blend md5s unchanged before/after (r11 0d083ae0e2bd09e2b64acdd2ec88e9fb, r10 a916795bca80185a0a576c24f41b9f40; candidate c579eb76785ab2bd6b88a157c648d56e unchanged too).

## 2026-11-01 envelope review: Grok Bot call
- KEEP for CP023 only (start and end): the enclosed nave replaces the open-sky eastward view; live source for CP023 is now `rounds/candidates/r11_envelope.blend` rendered with `--shot-exposure` (-2.2). `rounds/r11.blend` stays live for every other camera.
- REJECT for all other cameras: the fountain glass goes milky (`brighten_host_glass()` hits every "glass" material, including Osler's), exteriors lose the lawn (GROUND_PARK hidden) and show the east nave as a white box.
- Follow-up if the envelope is ever widened: exclude the fountain from the glass brighten, keep GROUND_PARK, and give the east-nave stub real glazing. Calm the saturated yellow ironwork in CP023.
- Pairs renamed KEEP_/REJECTED_ in survey look/pairs_geo.

## 2026-11-01 envelope v2 candidate + full-camera check (CANDIDATE pairs; no keep/revert call)
- New `scripts/apply_envelope_v2.py` builds `rounds/candidates/r11_envelope_v2.blend` from live `rounds/r11.blend` (Blender 5.1.2 headless, `--rig none`). DEPARTURES ENV2-01..10.
  1. Glass brighten skips the Osler fountain (MUSE_OSLER_* + FOUNTAIN_*), the case glass and the end-screen glass. Only GT_Glass and GT_RoofGlass are brightened.
  2. GROUND_PARK stays visible (no outdoor-leak hiding).
  3. No kit box or cream walls. The east nave is the transept's own part library on the Downes grid: tier-3 nave strip x 60..252 plus the full 3-tier section x 132..252, glazed clerestories, boarded ground tier, end screen at x=252 (a truncation), galleries, railings and floor. The x=132 arm walls that are now interior are hidden.
  4. New iron uses Owen Jones paint with per-object masks and a calmer yellow. Existing iron stays neutral.
- Check: `scripts/render_envelope_v2_check.sh`. The 15 cameras are rendered as in render_envelope_check.sh (apply_look interior_daylit, 1280x720, 28 spp, people v3.4), live r11 vs v2 with `--shot-exposure`. Also rendered: `keep_cp023/` (r11_envelope at -2.2, the CP023 "before") and `candidate_noshot/` (v2 CP023 at look exposure, reference only). Output `renders/candidates/envelope_v2_20261101/`.
- Pairs (`scripts/envelope_v2_pairs.py`): `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_<CP|REVIEW>_transept_envelope_v2_<cam>_pair.jpg` (15). All CANDIDATE; nothing promoted.
- Executor notes per camera (reviewer decides; mean-luma deltas are v2 minus before):
  - CP023 start/end (vs KEEP): real glazed nave, ridge-and-furrow roof, galleries, blue ironwork with thin yellow. No yellow wash and no cream walls. WORSE on exposure: much darker (luma 133 to 54, and 130 to 57). The KEEP's brightness came from v1's extra lights, so -2.2 is wrong for v2; even at look exposure (`candidate_noshot`) it is 85-87. The east end screen at x=252 closes the view after about 5 bays. Crowds differ between halves: the KEEP re-render and the noshot run show block stand-ins, the v2 main run shows v3.4 people (people-swap quirk in short runs, not investigated).
  - REV_ext34: lawn kept; the east block now reads as glazed stepped tiers on a boarded base instead of a white box. It also hides the open, see-through east side of live. Better than v1; different from live.
  - REV_south: near-identical to live; a thin sliver of the east block shows at the right edge.
  - PLATE_IV_south_ortho: near-identical; the new block's upper tiers appear faintly behind the right side (+1.9 luma).
  - DET_fountain: fountain keeps its dark cut-glass tiers (v1 milky regression fixed). WORSE overall: darker (-12.4 luma), with less sun on the floor and galleries beyond, because the new nave roof and walls close the open sky east of the crossing.
  - REF_elm_north: fountain dark tiers kept; darker (-7.0).
  - REV_int_up: fountain kept; slightly darker (-4.2).
  - REF_talbot: slightly darker floor and different sun patches (-5.8). End-screen lunette unchanged.
  - CP008 start/end, CP017 start/end, REF_absolon, OPEN_gallery: near-identical (within +-1.4 luma).
- md5 before/after unchanged: r11 0d083ae0e2bd09e2b64acdd2ec88e9fb, r10 a916795bca80185a0a576c24f41b9f40, r11_envelope c579eb76785ab2bd6b88a157c648d56e. v2 ce5db27df850982d8db63834ebd6fe19.

## 2026-11-01 envelope v2 review: Grok Bot call
- **CP023 start/end: KEEP v2.** The live source for CP023 is now `rounds/candidates/r11_envelope_v2.blend` (CP023 only), rendered by `scripts/render_cp023_v2.sh`. The candidate_noshot frame shows a real glazed nave in place of v1's yellow wash.
  - Exposure: `SHOT_EXPOSURE` in `render_views.py` is now keyed by blend. The old -2.2 applies only to `r11_envelope.blend` (v1, superseded); v2 has no entry. At the look exposure (-1.20), CP023 read dim next to CP021 (luma 129) and CP022 (147), at 83 start and 87 end. So it is rendered with a +0.3 lift, at **-0.9**: 93 start, 97 end, no clipping. This is logged as DEPARTURES ENV2-11.
  - People fix: people_lib 3.4's close-up gate (skip a figure if its projected height is more than 8% of the frame) caught 103 of the 104 visible CP023 figures, at a median of about 24% of frame. In a short run where CP023 is the first camera, they all stayed as the old block stand-ins. In the 14-camera runs, earlier wide cameras had already swapped them, so the outcome depended on render order. `render_views.py` now switches the gate off for CP023_into_nave_start/end (`SHOT_PEOPLE_GATE_OFF`, swapped around the call and restored afterwards). All 720 figures are swapped with CP023's own LOD ranking (log `skipped_close_up: 0 gate_off`). The shared people_lib is unchanged, and other cameras keep the gate. See DEPARTURES PPL-G01.
  - Renders, both 1280x720 at -0.9 with v3.4 people:
    - lean (28 spp): `renders/r11_envelope_v2/cp023_lean/`
    - full quality (render_round.sh live settings, 64 spp, 8 threads): `renders/r11_envelope_v2/cp023_full/CP023_into_nave_{start,end}.png`. This is the COVERAGE best path.
- **REV_ext34: KEEP v2.** The continuous glazed east nave is more truthful than live's open cut-away. Its current render is `renders/candidates/envelope_v2_20261101/candidate/REV_ext34_start.png` (28 spp). render_round.sh still renders every camera from r11 and was not changed.
- **REJECT v2 (stay on live r11):**
  - DET_fountain, REF_elm_north, REV_int_up, REF_talbot: darker, and the fountain fix isn't worth it there.
  - CP008 start/end, CP017 start/end, REF_absolon, OPEN_gallery, REV_south, PLATE_IV: no gain.
- Survey: pairs renamed KEEP_/REJECTED_ in `look/pairs_geo` (README line added), and COVERAGE CP023 updated.
- md5s unchanged: r11 0d083ae0e2bd09e2b64acdd2ec88e9fb, r10 a916795bca80185a0a576c24f41b9f40, r11_envelope c579eb76785ab2bd6b88a157c648d56e, v2 ce5db27df850982d8db63834ebd6fe19.

## 2026-11-01 CP023 crowd dressing CANDIDATE
- Resumed the stalled 12:50 UTC pass. `scripts/cp023_dressing.py` already had `people_patch`, which render_views.py calls (`pose_patch` is an old alias); the docstring now names it. No code fix was needed. It runs headless in Blender 5.1.2 with no errors. Rows are in DEPARTURES PPL-C01..C04.
- Live is not promoted. `scripts/render_cp023_v2.sh` now passes `--no-cp023-dressing`, so live CP023 re-renders unchanged. Candidate script: `scripts/render_cp023_dressing.sh [lean|full|both]` (r11_envelope_v2.blend, -0.9, gate off, dressing on).
- Renders in `renders/candidates/cp023_dressing_20261101/`:
  - lean (28 spp): `lean/`
  - full (64 spp, 1280x720, -0.9, 8 threads): `full/CP023_into_nave_{start,end}.png`
  - Logs: `/workspace/logs/transept_cp023_dress_{lean,full}.log` (`CP023_DRESS`, `CP023_DRESS_STATS`).
- Dress stats (identical in the lean and full runs):
  - start: 720 figures, 114 visible before; 17 flagged; 9 moved, 8 hidden (no spot, all gallery CROWD_GN at z 6.99), 1 near/off-frame hidden; 0 orphan hat parts; 106 visible after; pose_replaced 260.
  - end: 71 visible before; 14 flagged; 9 moved, 5 hidden (all gallery GN), 0 near hidden, 0 orphans; 66 visible after; pose_replaced 130.
- Pairs (before = live `renders/r11_envelope_v2/cp023_full`): `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP023_crowd_dressing_CP023_into_nave_{start,end}_pair.jpg` (`scripts/cp023_dressing_pairs.py`). CANDIDATE only; the keep/revert call is not made here.
- Executor notes (strict):
  - start: Fixed: no edge-cut or near-lens figures, so the looming bottom-left top hat, the kneeling foreground man and the half-figures at the frame edges are gone, and every visible figure stands. Bonnets read as hoods or hair from behind and in front. Hats: none floating. Boots: none detached, but men's boots are chunky stovepipe shells, clearly wider than the trouser leg, on the mid-ground men. Worse: the crowd now starts about 7 m out, so the bottom third of the frame is empty boards and the shot reads emptier and more staged, with three crinolines and a top-hatted man spaced evenly across the mid-ground. The upper galleries lost 8 figures. Pre-existing and not caused by dressing: a small pale block at the right frame edge (about x 1270, y 600) is in live too and is not a figure. Exposure unchanged (-0.9); mean luma 93.2 to 91.2 (content only).
  - end: Fixed: edge-cut figures, including the large half-lady on the right and the hatted man cut at the left edge, are gone, and all stand. Hats: none floating. Boots: the man standing at the locomotive plinth (right, pre-existing position) shows a doubled or stacked boot shell; other boots are attached but oversized. Mid-ground is denser and more even, with no foreground figures; the gallery lost 5. Exposure unchanged; luma 96.5 to 97.7.
- md5 before and after: r11 0d083ae0e2bd09e2b64acdd2ec88e9fb, r11_envelope_v2 ce5db27df850982d8db63834ebd6fe19 (unchanged). No .blend saved.

## 2026-11-01 CP023 crowd dressing review: Grok Bot call
- **KEEP for both CP023_into_nave_start and _end.** The cropped top hat at bottom-left, the kneeling foreground man (start), the large half-cut lady on the right (end) and the figures cut at the frame edges are gone. The frames now read as a calm walk into the nave. Exposure is unchanged (-0.9).
- Live CP023 is now `renders/candidates/cp023_dressing_20261101/full/CP023_into_nave_{start,end}.png`. `scripts/render_cp023_v2.sh` no longer passes `--no-cp023-dressing`, so re-renders come out dressed.
- Follow-ups, not blocking: the men's boots are oversized shells (people_lib 3.4), and the plinth man's boot is doubled (end). The bottom third of the frame is empty floor, and a few mid-distance figures could come in to about 4-5 m. A small pale block at the right edge (start, about x 1270, y 600) was in live too.
- Pairs renamed KEEP_ in survey look/pairs_geo.

## 2026-11-01 CP023 boots + foreground CANDIDATE (rendered 16:22 UTC; awaiting parent review, NOT kept)
- Goal: follow-ups from the crowd-dressing KEEP: (1) men's boots oversized, (2) empty lower third. CANDIDATE only; live CP023 (`render_cp023_v2.sh`, renders/candidates/cp023_dressing_20261101/full) must not change.
- Plan: opt-in flags in render_views.py (`--cp023-boots`, `--cp023-foreground`, `--save-blend-dir`) so live renders are byte-for-byte the same pipeline. Code in scripts/cp023_dressing.py (CP023 boot builder installed in people_patch; foreground() pre-swap placement). Driver: scripts/render_cp023_bootsfg.sh -> renders/candidates/cp023_bootsfg_20261101/{lean,full}; pairs via scripts/cp023_bootsfg_pairs.py -> survey look/pairs_geo/CANDIDATE_CP023_boots_foreground_*.png.
- Resume: if renders are missing, run `scripts/render_cp023_bootsfg.sh full` then `python3 scripts/cp023_bootsfg_pairs.py`.

### Result (16:30 UTC)
- The full run used `scripts/render_cp023_bootsfg.sh full`: r11_envelope_v2.blend, exposure -0.9 (the live CP023 exposure per ENV2-11), 1280x720, 64 spp, crowd dressing on, plus `--cp023-boots --cp023-foreground`. Log: /workspace/logs/transept_cp023_bootsfg_full.log.
- Renders: renders/candidates/cp023_bootsfg_20261101/{lean,full}/CP023_into_nave_{start,end}.png
- Sibling blend (baked dressed state, start camera, about 48 MB): rounds/candidates/r11_envelope_v2_CP023_into_nave_start.blend. The end-camera blend (about 51 MB) is left uncommitted on the box only. These blends are baked: do NOT re-render them through render_views (it would swap people again). Open them directly instead.
- Pairs: /workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP023_boots_foreground_CP023_into_nave_{start,end}_pair.png and *_lowerdetail_pair.png (bottom 45%). Script: scripts/cp023_bootsfg_pairs.py. Before = live cp023_dressing_20261101/full.
- Stats: FG start 6/6 placed (5.8-8.8 m), end 3/5 placed (6.7-7.5 m). Boots: 84 meshes, 22.0-28.5 x 8.0-9.6 cm. Luma start 91.2 -> 86.7, end 97.7 -> 93.9 (darker figures now cover bright floor).
- Departures: PPL-C05 (boots) and PPL-C06 (foreground).
- md5 unchanged: r11_envelope_v2.blend ce5db27df850982d8db63834ebd6fe19, r11.blend 0d083ae0e2bd09e2b64acdd2ec88e9fb. Live renders are untouched.
- Executor notes (not a verdict):
  - Start frame: the lower third is now mostly occupied.
  - Start frame: the six foreground figures all face away, which reads a bit like a queue.
  - Start frame: the bonnets on the back-facing ladies read as brown blobs at this size.
  - The bottom ~8-10% is still bare boards.
  - End frame: fuller, with men's boots visibly smaller.
  - The walking-pose front foot can still show a small lump (distant figures only).
