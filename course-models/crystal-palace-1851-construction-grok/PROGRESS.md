# PROGRESS: Hyde Park 1851 construction set (CP010-CP016), Grok Bot

Branch `grok-construction-1851` (worktree /workspace/crystal-palace-construction), folder
`course-models/crystal-palace-1851-construction-grok/`. Commit locally only.

- Build: `blender -b -P scripts/build_construction.py -- --out rounds/cNN.blend` (from this folder)
- Checks: `blender -b rounds/cNN.blend -P scripts/check_construction.py -- --out checks/cNN/checks.md`
- Renders: `bash scripts/render_round.sh cNN 1280x720 48` (CP015 louvre at frames 1 and 48; CP014 section portrait)
- Compare: `python3 scripts/compare_sheets.py cNN`

## c01
- **c01 (2026-10-26):**
  - The full HP-BUILD site on the 24 ft grid, east half.
  - Zone A: foundations in 5 states (pegged, dug, poured, base set, backfilled) with D17 pads and D16 base plates.
  - Zone B: erection, with columns up to the first lift and girders by tier; a sheer-leg hoist in bay 540-564; scaffold towers.
  - Zone C: the complete frame with the roof in states (glazed, half, bars, gutters, canvas); 4 glazing wagons with 8 workers; floor boards, then bare joists.
  - Also: the louvre bay animation, the offsite yard and the drainage cutaway.
  - Checks 20/20. Renders in renders/c01.
  - Review: iron, concrete and planks read beige-white in full sun; the wagons read as white crates; CP014_gutter looked into the cutaway backdrop.
- **c02 (2026-10-26):**
  - Darker primer iron, exposure -2.4, darker concrete, planks and timber (CN12/CN13).
  - Open timber wagon frames (CN21).
  - CP014_gutter moved on site with water in the gutters (CN20).
  - Checks 20/20 (checks/c02). Renders in renders/c02; compare sheets in compare/c02_*.jpg.

- **c03 (2026-10-26):**
  - models/ comparison with Muse's parts on origin/main adb0d2c (CN22–CN26).
  - Sash bars now 27 per slope at 10.29 in centres, with 3 strong 2½ in bars (CN23). Was 29 bars at 9.93 in, narrower than a 10 in pane.
  - Floor joists 7 × 2½ in at 2 ft centres (CN22).
  - 20 packing crates appended from Muse's hp-crate-and-display-case and credited to Muse (CN24).
  - Timber hoarding with a gate on the south side (CN25).
  - Checks 22/22 (checks/c03; new K21 credited props, K22 hoarding). Renders in renders/c03; compare sheets in compare/c03_*.jpg.

## Self-score c03: 7.0/10
**Good:**
- The roof bars now satisfy the pane arithmetic.
- The site gains stock (crates at the glazing bays, the gate road and the louvre bays) and an enclosure, which shows in the aerial and through the louvre wall.

**Misses:**
- Still no seated glazier or pane being slid in, no carts or horses, and no spoil heaps scaled to the pits.
- The CP014 section has not been reframed.
- The Muse crate is an open slatted exhibit crate, not a closed glass crate, and its pale timber reads a little light against our darkened site palette.
- The strong bars sit up to 3½ in off the 4/12/20 ft marks.

## Next (c04)
- Glazier poses with a pane at about 30 degrees.
- Carts and horse stand-ins at the gate.
- Spoil heaps scaled to the pit volume.
- CP014 reframed.
- Closed crate variant: a lid board on a copy in our file, not in models/.
- Darken Muse's crate timber by a render-time override if needed.

## Self-score c02: 6.8/10
**Good:**
- One continuous site reads as the progression from pegs to pits, pads, base pieces, columns, girders, bars, glass and canvas, all on Claude's grid with D16/D17 numbers.
- The CP012 sheer legs, CP014 gutter water and CP016 wagons give the film its working moments.
- The louvre bay animates.

**Misses:**
- The worker stand-ins are crude: faceted heads, no tools in hand, all in one pose family. Some read large in the 50 mm close views.
- The wagon has no canvas cover option and no glass panes being slid in. The 0174 engraving's glazier sits on the gutter with a pane at an angle; we show standing figures.
- The site is too clean. No spoil heaps beside the pits beyond the small mounds, no carts, horses or timber hoarding (the 1850 site was enclosed by a hoarding), no stacked glass crates on the ground.
- The CP014 section is legible but plain: the drain run and pad are small at the bottom of the frame.
- The CP015 blinds/louvre shots use the 1851 canvas on an 1850 frame (CN09), as staging.
- The roof sash bars read cream; their 1850 colour is unknown.

## Next (c03)
- Seated and kneeling glazier poses, with a pane held at about 30 degrees, as in 0174.
- Timber hoarding around the site, horse-and-cart stand-ins, glass crates and girder stacks on site.
- Spoil heaps scaled to the pit volume.
- CP014 section reframed with a larger lower half.
