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

## 2026-11-02 CP016_wheels v3: CANDIDATE (executor notes, not a verdict)
- Parent verdict on v2: the with-glaziers version is **REJECTED** (pairs renamed `REJECTED_CP016_wheels_v2_{start,end}_pair.png`). The no-glaziers version stays CANDIDATE; this pass fixes its far workmen only.
- Script: `scripts/cand_cp016_wheels_v3_20261102.py -- --hide KWORKER_028_CP016,KPANE_SLIDING_1 --repose KWORKER_029_CP016,KWORKER_030_CP016`. It loads `rounds/candidates/c06_cp016wheels_v2_noglaziers.blend` (left unchanged) and saves `rounds/candidates/c06_cp016wheels_v3.blend`, for CP016_wheels only. people_lib and other shots are not touched.
  - All 9 pre-swapped KWORKER_*_CP016 get a dark matte fustian smock, round-robin blue / grey / drab. The hero wagon_1 men are 015 (blue) and 016 (grey).
  - 028, the raised-arm gutter man, is hidden along with his sliding pane. 029 and 030 are reposed from pointing to working.
- Renders: `renders/candidates/cp016_wheels_v3_20261102/CP016_wheels_{start,end}.png` (same settings: 1280x720, 48 spp, render_views.py). Log: `/workspace/logs/construction_cp016wheels_v3_20261102.log`. Trial logs are try1–3 in the same folder.
- Pairs (survey look/pairs_geo): `CANDIDATE_CP016_wheels_v3_{start,end}_pair.png` (live KEEP reframe vs v3), made by `scripts/cand_cp016_wheels_v3_pairs.py`.
- Tried and dropped:
  - try1 (fustian + hide 028 only) left 028's pane lying alone in the gutter, and 029's `pointing` arm still looked odd.
  - try2 brown fustian on 016 read as a tanned bare muscular back in the end frame.
  - try3 drab on 016 read slightly "green muscle", so 016 moved to grey.
- Honest notes: the torsos now read as dark clothing, not skin, and no raised arm is left. At 2x crop the people_lib base mesh still shows bulky shoulders and back modelling through the smock, the heads are pale and bald-looking with small caps, and the wagon_1 hero (015) has his hand tucked into the smock front. At full frame they read as clothed workmen, but small and stiff. Nobody is visible on wagon_0's deck. That's expected now that the glaziers are rejected. The kneeling poses still stand (CN44 staging departure).
- Resume: `B=/workspace/blender5/blender; $B -b rounds/candidates/c06_cp016wheels_v2_noglaziers.blend -P scripts/cand_cp016_wheels_v3_20261102.py -- --hide KWORKER_028_CP016,KPANE_SLIDING_1 --repose KWORKER_029_CP016,KWORKER_030_CP016 && $B -b rounds/candidates/c06_cp016wheels_v3.blend -P scripts/render_views.py -- --cams CP016_wheels_start,CP016_wheels_end --outdir renders/candidates/cp016_wheels_v3_20261102 --res 1280x720 --samples 48 && python3 scripts/cand_cp016_wheels_v3_pairs.py`. Waiting for the parent's keep/revert decision. Do NOT promote.

## 2026-11-02 CP016_wheels v3: KEEP (parent viewed start + end pairs), promoted
- Verdict: KEEP for start and end. The wheels read clearly, the far workmen read as clothed at full frame, there is more depth, and no raised arm is left.
- Live CP016_wheels start/end: `renders/candidates/cp016_wheels_v3_20261102/CP016_wheels_{start,end}.png`, from `rounds/candidates/c06_cp016wheels_v3.blend` (CP016_wheels only). Re-render: `scripts/render_cp016_wheels.sh [samples] [outdir]`, which now renders v3 (rebuilding c06_cp016wheels → v2_noglaziers → v3 if the blends are missing). Check render at 48 spp to /tmp was pixel-identical to the v3 renders (start and end). Log: `/workspace/logs/construction_cp016wheels_v3_check_20261102.log`.
- route/camera_route.json CP016_wheels: 32 mm; start (333.5,-208.6,29.25)→(329.8,-194.5,25.4), end (330.5,-208.6,29.25)→(329.6,-194.5,25.4).
- DEPARTURES CN44 → KEEP (stub axles are inference, grade C; fustian colours inferred, grade C). Survey pairs: `KEEP_CP016_wheels_v3_{start,end}_pair.png`; v2 no-glaziers pairs → `SUPERSEDED_CP016_wheels_v2_noglaziers_{start,end}_pair.png`; v2 with-glaziers stay `REJECTED_`. COVERAGE CP016 row updated.
- Follow-ups (open): (1) wagon_0 deck is empty; repopulate it only once people_lib close-up clothing improves (the v2 deck glaziers read as bare-chested muscle men); (2) people_lib has no kneel pose, so the far workmen stand where the original staging had them kneeling; (3) at 2x crop the people_lib base mesh still shows bulky shoulders through the smock, pale bald-looking heads with small caps.

## 2026-11-02 02:10 UTC render_cp016_wheels.sh rebuild-from-c06 test: WORKS (executor, Grok Bot)
- Test: copied `scripts/`, `route/`, `checks/`, `CREDITS.md`, `DEPARTURES.md` and `rounds/c06.blend` (only; no candidate blends) to `/workspace/tmp/cp016_rebuild_test/` and ran `bash scripts/render_cp016_wheels.sh 48 /workspace/tmp/cp016_rebuild_test/out`. All three rebuild steps ran (c06 → c06_cp016wheels → c06_cp016wheels_v2_noglaziers → c06_cp016wheels_v3, each `SAVED`), then both cameras rendered. Exit 0. Log: `/workspace/logs/cp016_rebuild_test_20261102.log`.
- Result: start and end are **pixel-identical** to live `renders/candidates/cp016_wheels_v3_20261102/` (max diff 0). No script fix needed.
- Note: the v2 step's `--out` is relative (`rounds/candidates/...`); it works because the script `cd`s to the model folder first. Live blends untouched (md5 c06 e461f024…, v3 d5d1d242…).

## 2026-11-02 CP012_bay "One bay, then the next": CANDIDATE (executor, Grok Bot; not a verdict, not promoted)
- Why CP012: every COVERAGE row is OK, so the pick went by phase plus visible weakness. CP012 is the earliest-phase P1 shot (HP-PHASES phase 2, K-JOINT phase 1). Its storyboard action ("a crew connects one supported girder between columns; completed bays continue behind it") did not read in live c07: the hoisted girder KGIR_HOIST_X552_Y-180 hid behind the KSCAF_HEAD564 tower, a random `seated` people_lib pose gave a lounging foreground workman, pale smocks read as bare torsos and the haul horse was a white blob. CP021 (fitout o01, people v3.3 kept) already reads.
- State: Hyde Park, Nov–Dec 1850 erection (unchanged c07 site); nothing from Sydenham.
- Script: `scripts/cand_cp012_bay_20261102.py` loads `rounds/c07.blend` (left unchanged, md5 c6189435…) and saves `rounds/candidates/c07_cp012bay.blend` (CP012_bay only). Exact arguments are in `scripts/render_cp012_bay.sh`, which rebuilds the blend if it's missing and renders start at frame 1 and end at frame 96 (1280x720, 48 spp, render_views.py, `--no-people`).
  - Cameras `walk`, 28 mm, eye 5.25 ft, outside the south wall line: start (549,-219)→(551.5,-180,13.5), square-on to bay x540–564 on row y -180; end walks back and east to (566,-232)→(553,-180,15), outside the lifting zone. route/camera_route.json is NOT changed (live stays c07).
  - Girder animated: frame 1 top 19.0 ft (3 ft 2 in below its seat, on the sling); frame 96 seated, top 22 ft 2 in. Lifting ropes rebuilt as two keyed sets (`KROPES_CP012_LIFT_F001`, `KROPES_CP012_SEATED_F096`) plus `KROPES_CP012_STATIC` (fall to the snatch block, two guys); the original `KROPES` is hidden in this blend. KHAUL_ROPE is unchanged.
  - Head scaffolds KSCAF_HEAD540/564 moved 14 ft north (decks y -176..-170, 16 ft), so they stand behind the girder; deck men 008/009 go with them, facing the girder and camera.
  - People: 12 visible figures rebuilt with survey people_lib 3.4 `1850s_workman` in explicit poses (working / hauling / standing; never seated or pointing), smock and waist slots in local dark matte fustian (`CP012C_fustian_blue/grey/drab`, as CP016 v3). Hidden: KWORKER_005/006 (winch men; at 13–14 ft they were big close-up muscle-man figures) and KWORKER_062_CP010S (foreground, 28 ft). Moved: 007 (tag-line man) to (544,-166) behind the bay with the tag line to his hands; 064 to (559,-168).
  - Gate cart group (KCART_gate_crates, KHORSE_gate_crates, KWORKER_032_CARTS) shifted 30 ft west, out of the end frame. Haul horse KHORSE_haul uses the existing bay-coat mesh `horse_draught_bay`.
- Dimension checks: bay 24 ft (columns x540/x564 on row -180, col_22 22.35 ft); hoist girder mesh 23.52 ft; start top 19.0 < 22.17 seat (K04 holds) and apex 36 > 19 + 6; end top = 22.17 = fixed T1 girder tops. Scaffold decks 16 ft (unchanged).
- Renders: `renders/candidates/cp012_bay_20261102/CP012_bay_{start,end}.png`. Before-end reference (no live c07 end exists): `BEFORE_c07_rerender_CP012_bay_end.png` (c07.blend re-rendered 2026-11-02 with the current pipeline). Check render to /workspace/tmp/cp012/check is pixel-identical (log `/workspace/logs/cp012_bay_check_20261102.log`).
- Pairs (survey look/pairs_geo): `CANDIDATE_CP012_bay_{start,end}_pair.png`, made by `scripts/cand_cp012_bay_pairs.py`.
- Tried and dropped (scratch /workspace/tmp/cp012/try1–7): try1 square-on from (566,-221): girder lost against the bays behind, winch men huge in the foreground. try2 inside row -204: scaffolds and a back-facing bald-looking man dominate. try3 from 58 ft: girder lost again, white gate horse in the foreground. try4–6 near camera with the girder raised to read against sky: works, but foreground hauling men at 28–37 ft read as muscle men at 2x crop, so they were moved behind the bay or hidden (try7 = this candidate).
- Honest notes: the girder hanging on its sling between two column heads with men on the decks now reads at full frame; the end frame's seated girder is legible but less striking, and the front-row column (564,-204) stands close to its east end. The south sheer leg runs almost vertically through the centre of the start frame. Deck men are small (about 5% of frame height) but at 2x crop people_lib's bulky shoulders still show. The ground crew who'd do the hauling are mostly off frame (winch men hidden). No 50 mm joint insert in this pass (CP012 joint insert camera unchanged).
- Resume: `scripts/render_cp012_bay.sh && python3 scripts/cand_cp012_bay_pairs.py`. Waiting for the parent's keep/revert decision. Do NOT promote.
