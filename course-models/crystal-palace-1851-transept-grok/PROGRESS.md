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
