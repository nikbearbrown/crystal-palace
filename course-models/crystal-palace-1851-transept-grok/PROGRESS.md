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
