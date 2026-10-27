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
  - Changes: REF_talbot raised to 24 ft at the gallery-rail sightline (C06, the 30 ft pull-back is blocked by ELM_NORTH2's crown); fountain scaled to ~27 ft; statue proxies at x = +/-14 and the curved iron railing; grey roof glass; RL02 render-time override of Claude's PART_RoofUnit MAT_Glass with GT_Glass (his file never saved; `CLAUDE_ROOF_OVERRIDE slots 1` in the log).
  - Self-score r07: 7.8/10.
    - Good: Talbot composition now reads (railing foreground, fountain on axis, elm behind, statues lining the nave edge); Owen set unchanged and stable.
    - Misses: the fountain is now too near/large in the Talbot frame (the photo puts it ~60 ft further south); the south end fan still reads light, not as the dark radiating lunette; REV_combo still clips the roofs to white on BOTH halves (an exposure problem in this transept scene, not a material seam: the r06/r07 roof pixels are both 249-255); no exhibits or plants under the galleries.
- Next (r08): move the REF_talbot camera north ~40 ft along the axis (or a 35 mm with a lower target) so the fountain sits at mid-ground; darken the lunette sash bars and add the radial fan glazing bars; give REV_combo its own exposure (-0.6 like the exterior EX10) so the seam check is meaningful; exhibit and plant proxies under the galleries.
