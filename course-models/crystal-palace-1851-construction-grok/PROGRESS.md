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

- **c04 (2026-10-26):**
  - Spoil heaps sized to their pits: 86 heaps, 88% of the bulked spoil on site, the rest carted (CN27).
  - Glaziers with panes held at 30°, plus a pane sliding up the bars at each wagon (CN28).
  - 4 tip carts with draught horses and carters at and near the gate (CN29).
  - Closed crate variant on Muse's frame; darker crate timber in our copy (CN30).
  - CP014 section reframed (CN31).
  - Checks 26/26 (checks/c04; new K23 heaps, K24 carts, K25 panes, K26 closed crates). Renders in renders/c04.

- **c05 (2026-10-26/27) — HP-PHASES (CP010, CP012, CP013, CP016):**
  - CP010 "small foundations, immense extent": foundation field over the whole site extent (pegs x −924..924 ft), 680 positions in work order pegged → dug → poured → base, 554 spoil heaps; new CP010_extent eye-level camera (CN32, CN33).
  - CP012 bay-by-bay rise: horse haul through a snatch block at the shear legs, crab winch kept as standby; guyed gin pole raising an upper-tier column; CP012_bay end camera (CN34, CN35, CN37).
  - CP013 iron + glass + timber layering: new CP013_layers 28 mm camera along the roof states (CN36).
  - CP016 K-WAGON: follow-end camera on the glazing wagon with its glaziers (CN37).
  - Field spoil cart off the CP010 axis; K24 exempts the hauling horse; new checks K27–K31 (CN38).
  - Checks **31/31** (checks/c05). Renders in renders/c05 (1280x720, 48 samples) + contact_sheet_c05.jpg.

## Self-score c05: 7.4/10
**Good:**
- CP013_layers is the strongest frame of the set: gutters, bare bars, half and fully glazed bays receding in one 28 mm look.
- CP010_foundations now reads the repeated pits/heaps marching to the horizon; CP012 has a working horse at the tackle and a second lifting method.

**Misses:**
- CP010_extent still reads "big field" more than "immense": the eye-level horizon flattens 1848 ft; no high or long-lens comparison frame.
- Horses remain white metaball stand-ins with no harness or collar; the CP012 haul horse is partly masked by a worker.
- Heaps are smooth frustums; panes still faint against the sky at 50 mm.
- CP016 wagons read as clusters of figures; the wagon wheels on the gutter are hidden.

## Next (c06)
- CP010: second extent frame from a ladder/hoarding top (eye-height rule exception to log) or stagger figures as scale markers every 96 ft.
- Harness + collar on the horses; darker coat colours.
- Heap displacement; pane edge band; wagon wheel close-up in CP016_end.

## Self-score c04: 7.3/10
**Good:**
- CP010 now reads as a dug site: the heaps match the pit volumes, with a cart taking the surplus.
- The gate has traffic. The section is legible top to bottom.

**Misses:**
- The heaps are smooth frustums, with no clods or tool marks.
- The horses are soft metaball forms, with no harness or collar.
- The panes are hard to see at 50 mm against the sky (thin glass).
- The CP012 cart sits just outside the 28 mm frame.

## Next (c05)
- Harness and collars. Rough heap displacement.
- CP012 camera yaw 5° left to catch the crate cart.
- Pane edges catching light (a putty or edge band).

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

## c06-lite (2026-10-27): CP010 scale view only (the rest of c06 is parked as backlog)
- CN39: 14 scale-marker figures every 96 ft along the CP010_extent view; eye height unchanged.
- Checks 32/32 (new K32: spacing 96 ft, no clashes, 12/14 heads visible from the camera).
- Renders: renders/c06/CP010_extent_start.png and CP010_extent_end.png (1280x720, 48 spp).
- Backlog (parked, not started): the remaining c06 list above.

## k01 (2026-10-27): K-DRAIN CP014 labelled cutaway
- KD01–KD06: ridge → Paxton gutter → box gutter → hollow column → base pipe → drain; studio diagrams + live details.
- Checks: see checks/k01_checks.md.
- Renders: renders/k01/CP014_drain_{whole,roof,gutter,base}_start.png.

## c07 (2026-10-27): horse harness + darker coats
- Bay/grey coats darkened; harness straps (bridle/breast/girth/traces) GT_HorseHarness. DEPARTURES CN35.

## c06 (2026-10-27): rough spoil, pane edge catchlights, CP016 wheel close-up
- Build: `rounds/c06.blend`. Checks: 32/32.
- Lean renders: `renders/c06` — CP010_foundations, CP016_trolley, CP016_wheels (24 spp).

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP012; lib 3.1

## people v3.2 2026-10-27
- people v3.2: revert CP012 (exposure regression)

## c09 (2026-10-27)
KEEP CP015: hanging canvas flaps, thicker louvre blades, plank grooves/battens, canvas rolls on floor; exposure match (gain~1.27). Source c04 → c09 via `polish_cp015_c09.py`. Pair `look/pairs_geo/CP015_blinds_start_pair.png`.

## CP015 REVERT + CP014 CANDIDATE (2026-10-27)
- **CP015:** REVERT c09 (canvas flaps read as mid-air brown slabs). Live remains `rounds/c04.blend` / `renders/c04/CP015_blinds_start.png`. Rejected pair: survey `look/pairs_geo/REJECTED_CP015_blinds_start_pair.png`.
- **CP014 CANDIDATE:** `scripts/polish_cp014_cand.py` → `rounds/candidates/k01_cp014.blend` + `renders/candidates/CP014_drain_whole_start.png`. Live `k01` untouched. Pair: survey `look/pairs_geo/CANDIDATE_CP014_drain_whole_start_pair.png`.

## Muse Paxton gutter CANDIDATE (2026-10-27)
- Adopt Muse `paxton-gutter` into K-DRAIN as candidate `k01_gutter` (MK03b). Girder depth (MK01) and gallery rail height (MK04) logged as departures only.

## 2026-10-27 Muse gutter
- CANDIDATE k01_gutter: adopt Muse Paxton gutter (MK03b). MK01 girder depth + MK04 rail height remain departures.

## 2026-10-27 Muse gutter REJECT
- **REJECT** Muse Paxton gutter adopt (MK03b / `k01_gutter`): red teaching-point gutter end disappeared; stray pale beam bottom-left. Keep live KD03. Pair: survey `look/pairs_geo/REJECTED_CP014_gutter_muse_pair.png`.
- Muse 10½ in sash-bar / gutter notch pitch logged as **departure note only** (MK03c) — do not retarget live this round.

## 2026-11-02 CP016_wheels reframe CANDIDATE: executor notes (not a verdict)
- Why: in the live c06 CP016_wheels_start, an octagonal KSCAF_ROOFEDGE standard (x 328, y -208) sits 4.3 ft from the lens at frame centre, and the wagon is cut off at the top. You can't see the wheels at all.
- Script: scripts/cand_cp016_wheels_20261102.py loads rounds/c06.blend (unchanged, md5 e461f024b79c…) and saves rounds/candidates/c06_cp016wheels.blend. Use that blend for CP016_wheels ONLY.
  - Start camera (332,-212,29.25) aimed at (328.6,-196.1,22.8), 50 mm; end camera (332,-210.5,29.25) aimed at (328.4,-196.1,22.6). Both stand in the bay between standards on the 24 ft deck.
  - The glazing_wagon wheels get the existing GT_CartTyre material (iron), so they read dark against the timber (CN43).
  - Hidden for this shot: KWORKER_013/014/027_CP016 (under the people_lib 3.4 close-up gate they would be grey proxies) and KPANE_SLIDING_0 / KPANE_HELD_0 (the panes they hold, which would float without them). The men stay in CP016_trolley.
  - Tried and rejected: an 85 mm lens (wheels still unreadable, more proxies), people gate off (bald base-mesh men; render_views change reverted), and aiming at x 326 (pushes the wagon into a corner).
- Renders: renders/candidates/cp016_wheels_20261102/CP016_wheels_{start,end}.png, 1280x720, 48 spp. Log: /workspace/logs/construction_cp016wheels_full_20261102.log.
- Pairs: look/pairs_geo/CANDIDATE_CP016_wheels_reframe_pair.png (live start vs candidate start) and CANDIDATE_CP016_wheels_reframe_startend.png (candidate start vs end; there's no live end).
- Honest read: the whole wagon now sits on its gutters with no pole in frame. The dark wheels show only faintly at the lower corners, because the axle bearer and gutter hide most of them. The deck is empty with no glaziers, and the bottom ~40% of the frame is foreground glazing bars. It's legible but not yet a "wheels" shot.
- Resume: if the renders are missing, run blender -b rounds/c06.blend -P scripts/cand_cp016_wheels_20261102.py, then blender -b rounds/candidates/c06_cp016wheels.blend -P scripts/render_views.py -- --cams CP016_wheels_start,CP016_wheels_end --outdir renders/candidates/cp016_wheels_20261102 --res 1280x720 --samples 48, then python3 scripts/cand_cp016_wheels_pairs.py. Awaiting the parent's keep/revert decision. Do NOT promote.

## 2026-11-02 CP016_wheels reframe: KEEP (parent viewed the pair), promoted
- Verdict: KEEP for start and end. Removing the scaffold pole and showing the whole wagon on its gutters is clearly better than live c06.
- Live CP016_wheels start/end: `renders/candidates/cp016_wheels_20261102/CP016_wheels_{start,end}.png`, from `rounds/candidates/c06_cp016wheels.blend` (CP016_wheels only). Re-render: `scripts/render_cp016_wheels.sh` (rebuilds the blend from rounds/c06.blend if it's missing). route/camera_route.json now holds the reframed cameras. DEPARTURES CN43 → KEEP. Survey pairs renamed `KEEP_CP016_wheels_reframe_{pair,startend}.png`; COVERAGE CP016 row updated.
- Follow-ups (open): (1) the wheels are still barely visible (axle bearer and gutter hide them); (2) the wagon deck is empty, with no glaziers (the wagon_0 men are hidden in this shot); (3) the bottom ~40% of the frame is foreground glazing bars.

## 2026-11-02 CP016_wheels v2: CANDIDATE (not promoted, waiting for the parent's verdict)
- Script `scripts/cand_cp016_wheels_v2_20261102.py` (flags `--stub-axles --glaziers --swap-workers --cam front32 [--out]`), loading `rounds/candidates/c06_cp016wheels.blend`.
- Blends: `rounds/candidates/c06_cp016wheels_v2.blend` (all fixes) and `c06_cp016wheels_v2_noglaziers.blend` (no deck glaziers).
- Renders: `renders/candidates/cp016_wheels_v2_20261102/` and `renders/candidates/cp016_wheels_v2_noglaziers_20261102/` (1280x720, 48 spp).
- Pairs (survey look/pairs_geo): `CANDIDATE_CP016_wheels_v2_{start,end}_pair.png` and `CANDIDATE_CP016_wheels_v2_noglaziers_{start,end}_pair.png`, built by `scripts/cand_cp016_wheels_v2_pairs.py`.
- Tried and dropped: keep/kneel/kneel_low/front/front_kneel cameras (the wheels stayed hidden behind the bearer at every angle, so the geometry needed the stub-axle fix); 40 mm (cut off the glaziers' heads); the seated glazier pose (people_lib seated loses the smock shell in close-up); glaziers at rz 180 (facing away).
- Honest notes: the wheels now read clearly and the foreground glazing bars drop from ~40% to ~20% of the frame. The people_lib 3.4 workmen are weak in close-up: a muscular base mesh, a pale smock that reads as bare skin, a tiny cap, and boots that look like cuffs over bare feet. The no-glaziers variant isolates the camera and wheels fix.
- Resume: `B=/workspace/blender5/blender; $B -b rounds/candidates/c06_cp016wheels.blend -P scripts/cand_cp016_wheels_v2_20261102.py -- --stub-axles --glaziers --swap-workers --cam front32 && $B -b rounds/candidates/c06_cp016wheels_v2.blend -P scripts/render_views.py -- --cams CP016_wheels_start,CP016_wheels_end --outdir renders/candidates/cp016_wheels_v2_20261102 --res 1280x720 --samples 48`
