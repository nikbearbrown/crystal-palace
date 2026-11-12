# DEPARTURES: HP-FITOUT (CP018-CP020) and HP51 (CP026-CP029), Grok Bot

Grades:
- A: printed or measured.
- B: strong inference from a period source or image.
- C: staging judgement for the film.

## Fit-out (state `fitout`, round f01)
| id | decision | evidence | grade |
|---|---|---|---|
| FT01 | No exhibits are installed. Muse's exhibit set, the dressing plinths and the counters are all held back, and check_dims asserts they are absent. | Exhibits arrived from Feb 1851; the storyboard shows "cases arriving" | B |
| FT02 | Osler's crystal fountain is absent. It was erected only in spring 1851. | Osler fountain installation dates | B |
| FT03 | Priming coat is a pale stone (0.58/0.55/0.49). The darker oxide used on site (CN12) was covered before the Owen Jones colours went on. | Owen Jones scheme over a light ground; exact colour not printed | C |
| FT04 | Paint goes on top-down. A paint_cut height splits each half-painted member (colour above, primer below). 479 members painted, 8 half, 313 primer; the south-west bays stay primer. | Owen Jones 1850-51; front placement is staging | C |
| FT05 | Two ladders and six hanging cradles with 14 painters, plus a paint shop (trestle, kegs, a man grinding). Cradle rigging is simplified to ropes from the girders. | ILN fit-out engravings show cradles and ladders; rig details not printed | B |
| FT06 | The south doors are opened as three pairs of 3 ft leaves swung 90 deg inward (`open_south_doors`). The leaf division is inferred. | Downes shows the doors; leaf division not printed | C |
| FT07 | A horse dray waits outside and hand trucks bring cases through the doors to stacks. | Contemporary accounts of exhibits arriving | B |
| FT08 | Crates are appended from Muse `hp-crate-and-display-case`, with Grok board sheathing on some (credit Muse). | reuse | - |
| FT09 | East nave floor x 84-132 is left unboarded. Muse `hp-floor-boards` tiles (joists and sleepers) are appended, 18 tiles, with 32 loose boards being laid. | Paxton 1850 (9 x 1.5 in boards, 1/2 in gaps); Muse | B |
| FT10 | Board gaps are 1/2 in so sweepings fall through. | Paxton's lecture (as reported) | B |
| FT11 | Paxton's sweeping machine (a wheeled frame of brooms on a shaft) follows the water hand-engine on the boarded nave. It is **planned/proposed** per Paxton's Society of Arts lecture of 13 Nov 1850; Petroski notes its use is unconfirmed, so it is shown "on trial". The form is reconstructed. | Paxton, SoA Nov 1850; Petroski | C |
| FT12 | Camera CP020_floor/gaps stands over the unboarded patch (joists and earth). The floor-hit check allows the patch, and the eye stays at 5.25 ft over floor level. | camera grammar | C |
| FT13 | Muse exhibits are skipped in the fitout state only. hp51 and closing load them. | scope | - |
| FT14 | Cameras moved for clearance: dray to (-32,-262) because it was inside the waiting dray; paint to x -22 because of the elm trunk; gaps to (126,24) because of the board stack. | check_state 1 ft clearance | - |

## HP51 daily life (state `hp51`, round h01)
| id | decision | evidence | grade |
|---|---|---|---|
| FT20 | Shilling-day re-dress: 78% of the crowd (531 of 660) is swapped to working dress (fustian, smock, velveteen, cotton prints, shawls, bonnets). | Shilling days from 26 May 1851; Mayhew's "1851"; Punch images | B |
| FT21 | Children and family groups are added to the working-class wardrobes. | ILN shilling-day images | B |
| FT22 | Turnstiles: four 4-arm iron and brass turnstiles in five railed lanes at the south entrance (y -193). The layout is interpretive. | Turnstiles counted visitors in 1851; layout not printed | C |
| FT23 | Two pay boxes at x +/-12.6 with money-takers. Shilling days were pay-at-door. | 1851 admission regulations | B |
| FT24 | Three police (Metropolitan uniform, top hat) and attendants in green livery. The livery colour is inferred. | Police were present in 1851; livery colour not confirmed | C |
| FT25 | Six visitors on the K-STAIR gallery stair flights (x 96 +/- 7.75), with z following the flight pitch. | Grok K-STAIR | B |
| FT26 | Muse `hp-louvre-and-blind` compartments (3) replace the tier-1 louvres on the north end wall at x 12-36 (only WLOUV_NE1 is hidden). Muse's closed copy and `.001` duplicates are filtered out (credit Muse). | Downes Plate XXI | B |
| FT27 | An attendant works the louvres by rope from the floor. The exact gear (cords, rods, wheels) is inferred. | Downes describes louvres worked by attendants; gear simplified | C |
| FT28 | Three attendants water the elms and plants with cans, with spare cans and wet patches. | accounts of daily maintenance | C |
| FT29 | South doors are open as in FT06. A gravel apron with a queue of about 140 figures, 4 abreast, outside. | staging | C |

## Closing (state `closing`, round c01)
| id | decision | evidence | grade |
|---|---|---|---|
| FT30 | The date is the closing ceremony of 15 Oct 1851. The public closing was 11 Oct. | Official closing accounts | A |
| FT31 | The dais is placed north of the transept crossing (x -22..22, y 30..58). Its exact position is inferred. | ILN closing engraving shows a dais under the transept | B |
| FT32 | Prince Albert appears as an unnamed stand-in figure (`DAIS_ALBERT_standin`), not a likeness, among 26 commissioners. | policy: no likeness | C |
| FT33 | Ceremony crowd of 620 floor and 260 gallery figures, all facing the dais. The real attendance was ~53,000 that week. | staging density | C |
| FT34 | Autumn tint is applied to the elm leaf colour ramp. | October | B |
| FT35 | The sun is lowered 18 deg and warmed for October. | season | B |
| FT36 | The fountain stays in place for the closing. | It stood until dismantling | B |
| FT37 | The closing gallery camera moved to the west gallery because the elm canopy blocked the east view. | clearance | - |
| FT38 | Sunlit exteriors (CP019_dray, CP026_shilling_ext) are re-rendered at render-time exposure -0.7 because the wall boards blew out white. This is a review override only; the .blend is unchanged. | render review | C |
| FT39 | **Pale exterior boards** (f02/h02/c02): GT_Timber Base Color (0.54, 0.495, 0.42) and GT_Boarding (0.45, 0.40, 0.325) — weathered painted deal instead of new white board, so sunlit exteriors (CP019, CP026) stop blowing out. | Review: boards read as white sheets even at exposure −0.7. | B |
| FT40 | **CP029 gallery foreground filter** (c02): drop CROWD_* persons within 18 ft in front of the gallery cam at (−39.5, −44) on the gallery floor (z ≈ 22.92). Dais shot unchanged. | Review: a spectator filled the left foreground of CP029_gallery. | B |
| FT41 | **CP028 louvre camera tilt** (h02): pos (24, 156, 5.25) → look (24, 203, 15), 50 mm. The Muse louvre band sits at z ≈ 16.67 ft; the previous look left it low in frame. | Review: louvres were under-framed. | B |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| FT41 | GT_Timber/GT_Boarding base albedo darkened in build_transept + state_common (Boarding ≈0.24/0.20/0.15) — material not exposure | Sunlit boards still pale after FT39 | B |
| FT42 | Fountain hanging drops → hexagonal tapered prisms; glass_solid mix 0.22 for sparkle | Osler glass read as smooth cylinders | B |
| FT43 | New `--state opening` (CP021/CP022): May ceremony dais + fountain cams; spring sun, no autumn leaf tint | Gap: opening day / landmark of glass | B |
| FT44 | New `--state empty` (CP030): strip dressing/exhibits; packing crates + sparse packers; pale winter sun | Gap: palace without exhibition | B |
| FT45 | New `--state dismantle` (CP031): shores, girder/sash/column stacks, hero joint with pins withdrawn, sky-open bay | Gap: undoing the assembly | B |
| FT46 | empty/dismantle dims: DRESS_* / PROPS_muse fail by design (no HP51 dressing); state checks 19/19 and 15/15 | Expected for stripped states | A |

## Look — crystal-palace-look v1 (2026-10-27)
Shared grade from `/workspace/crystal-palace-survey/look/` (AgX Medium High Contrast, Nishita-family MULTIPLE_SCATTERING sky + haze, era white-balance, mid-grey exposure table, glass/white-iron albedo ceilings). Render scripts import via `cpl_look.py` and call `apply_look` before rendering. Hero tiles re-rendered lean (24 spp, 1280×720). See `look/README.md` for Sydenham adoption.

## Muse kit compare pointer (2026-10-27)
See construction-grok `DEPARTURES.md` MK01–MK05 (lattice girder, Paxton gutter, gallery rail, S25 floor gaps). Floor gaps already logged FT09/FT10 — confirmed match to muse-round2 S25 (½ in, ground floor only).

## KEEP CP022 Osler (2026-10-27) — Muse fountain live
| ID | Topic | Call |
|---|---|---|
| FT50 | Muse `osler-crystal-fountain` promoted to live o01 (CP021/CP022); also r11 for CP023. Lathe `FOUNTAIN_*` hidden. | **KEEP.** Credit: Muse (Wellcome). See CREDITS.md. |

## CANDIDATE CP028 louvre drive (2026-11-02) — h03_cp028_drive, live h03 unchanged
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT51 | **One cord, one pulley per 216 ft run.** Compartments x=16 ft and x=32 ft (LOUVRE_MUSE_0/2) now instance `CP028_Louvre_Intermediate`: Muse compartment without pulley Q, rope R, worm P/worm-wheel O, centre rod N, forks, bearing S and cleat; a copy of Muse's crank U / rod N' / bearing S' station put at the compartment centre (x −0.914 m local). Centre compartment x=24 ft keeps the full Muse pulley/worm station and LOUVRE_ROPE. | Downes/Cowper 1852, LOUVRES (Plate XXVII): one wheel O drives "a length of 108 ft on each side" via 1 in shafting T, intermediate louvres by cranks U and rods N'. Live h03 showed three pulleys in 24 ft. Exact positions of driving stations along the north wall are not recorded; x=24 ft is kept because the floor attendant's rope is there. | B |
| FT52 | Continuous 1 in shafting T (CP028_SHAFTING_T) x=12.05–35.95 ft at Muse local y −0.218 m, z +0.19 m (world y 61.855 m, z 5.272 m). | Same text: shafting runs the length; live showed three 7.3 ft stubs with gaps. | B |
| FT53 | Stray closed-state blind pieces (BlindLath_±1, BlindSeam_±1, Muse model_closed leftovers at local x 2.7–5.1 m) unlinked from the in-blend Muse collection copy. Muse's own folder untouched. | Cleanup: they sat in the neighbouring compartment. | A |
| FT54 | **v1, REJECTED 2026-11-02 (oiler read as floating beside the steps); superseded by FT54 v2.** **Staging:** second attendant (ATTEND_OILER, ATTEND mesh + arm copy) on a 14 ft pair of deal steps (CP028_STEPS, top 4.30 m, standing tread 3.65 m, side-on to the wall so the back legs clear the boarding) oiling bearing S' at x=16 ft with a zinc oil feeder; hand 0.16 m from the bearing. | Storyboard CP028 "daily work behind the spectacle". No source shows this man; oiling shafting bearings is ordinary 1850s maintenance. | C |
| FT54 v2 | **KEEP 2026-11-02, live in `rounds/h03.blend` (with FT51–FT53).** **Staging (`polish_cp028_drive_v2_cand.py`):** ATTEND_OILER stands ON a 14 ft pair of deal steps (CP028_STEPS, top 4.30 m, 14 rises of 0.307 m, 74 deg front, side-on to the wall, back legs 0.19 m clear of the boarding), facing up the steps and turned 10 deg toward the wall (camera sees his right side). Lower foot on tread 12 (3.69 m), right foot on tread 13 (3.99 m; shin sheared up/forward, thigh hidden in the coat), body between the stiles, top cap at thigh height (0.60 m above the lower foot) just in front of his coat. Hand 0.15 m short of bearing S' at x=16 ft (z 5.24 vs 5.27 m), zinc feeder spout to the bearing. Own mesh copy: pale moleskin trousers below the coat hem and dark boots, for legibility against the boarding. | Storyboard CP028 "daily work behind the spectacle". No source shows this man; pale moleskin/duck trousers were ordinary 1850s labourers' wear. | C |

## CANDIDATE CP026 shilling entrance (2026-11-10) — h03_cp026shilling, live h03 unchanged (md5 df1e46cf)
State: HP51, a shilling day in the later 1851 season (Hyde Park only; nothing Sydenham). Script `scripts/cand_cp026_shilling_20261110.py`.
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT55 | **Shilling-day figures.** 140 QUEUE_/QUEUE_LANE_ + 4 ENTERING_ figures and the 3 constables are replaced by modelled 1851 dress (`scripts/cp026_figures.py`; `scripts/c26_figures_base.py` = copy of our site-grok `c9_figures_v2.py`, CC0 HBM heads from the survey people vendor bases): 12 men (fustian, cord, velveteen, moleskin, blue cloth jackets; smock-frocks; a few best black/grey frock coats with top hats; caps and wideawakes), 10 women (print/stuff/merino dresses over petticoats to the ground, folded shawls pointed at the back, straw or black bonnets), 3 boys, 3 girls, constables in blue tail-coat and top hat. Each new object sits exactly on its old figure (kept, `hide_render`) so the people_lib v3.1 render-time swap of everyone else keeps its LOD order. Heights men 1.63–1.81 m + hat, women 1.54–1.63 m, children 1.18–1.35 m. | Storyboard CP026 "visitors present tickets and pass into the hall; excursion groups arrive behind them"; FT21 working dress. No source shows these people; dress is ordinary 1851 working-class wear (pre-crinoline skirts, shawls, bonnets). Women have no modelled arms (inside the shawl). | C |
| FT56 | **Apron gravel.** HP_APRON flat 0.50 albedo → rolled buff hoggin: 3 m mottling, 25 cm mottling, pebble Voronoi bump, dark grit specks, darker trodden band ~2.5 m either side of the queue line. Mean albedo ≈0.40. | No source for the 1851 apron surface; Hyde Park drives and paths were gravel. Live read as a white slab. | C |
| FT57 | **South-end boarding.** Copy of GT_Boarding on WALLF_SE1_* and SOUTH_DOORS_OPEN only: vertical boards 9 in wide (estimated) with pale joints and a joint bump, ±10 % per-board tone, grain, a broken splash/boot-dirt band to ~1.2 ft at the foot. Base albedo unchanged (FT41). | Downes Plate IV (south elevation) draws the ground-tier panels and arched heads with vertical boarding; board width not dimensioned. | B (vertical boarding) / C (9 in, dirt) |
| FT59 | **South-entrance pedestals.** SOUTH_PEDESTALS (two plain 5×5×7 ft boxes, no source, read as a pale block beside the doorway) hidden; replaced by Downes pedestal a5 round the feet of COL_END_X±012_Y-204: octagonal cast iron, flats to the cardinal points, plinth 5.4 in @20.2 in AF, cyma to 11.9 in, shaft 40.9 in, torus 14.1 in, band 13.5 in, top 57.0 in = 4 ft 9 in (printed), bell to 60.8 in, countersunk screw heads; painted as GT_Iron. Profile numbers taken from Muse's `models/south-entrance-pedestals/NOTES.md` plate metrology (read-only, nothing copied). | Downes pp. 38–39, Plate XXVI figs 26–27, Plate IV. Plate IV shows pedestals under every 8 ft detached column of the transept front with three steps; only the two columns our model has at ±12 ft get them; the steps and the 8 ft column rhythm are not built (open miss). | A (pedestal) / C (placement on the 24 ft-grid columns) |
| FT58 | (withdrawn) pay-box retint: the pay boxes stand inside the wall line (y = −195 ft) and are not in frame. | — | — |

## KEEP CP026 environment-only polish (2026-11-10) — live in rounds/h03.blend (md5 0a1da8f2; pre-keep pinned rounds/h03.blend.pre_cp026env_keep, md5 df1e46cf)
Script `scripts/cand_cp026_env_20261110.py` (rebuild: `scripts/render_cp026_live.sh --rebuild`). Hyde Park 1851 only.
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT55 | **REJECTED 2026-11-10, not live.** The shilling-day figures read as armless pastel cones from behind; the live people_lib v3.1 queue, lane, entering figures and constables stay exactly as before. | Parent verdict | — |
| FT56 | **KEEP, live.** Apron gravel as described above. | as above | C |
| FT56b | **KEEP, live.** The trodden band now follows the real queue line (bends to +x south of y = −250 ft; the shilling script had the sign reversed) and is a little darker (×0.66 vs ×0.70) so it shows between the figures. | Staging so the queue's wear reads; no source | C |
| FT57 | **KEEP, live.** South-end vertical boarding as described above (also visible far off in CP026_turnstiles and CP027_stair_foot). | Downes Plate IV | B / C |
| FT59 | **KEEP, live.** Downes pedestal a5 at COL_END_X±012_Y-204; SOUTH_PEDESTALS hidden (it also no longer blocks the doorway in CP026_turnstiles and CP027_stair_foot). | Downes pp. 38–39, Pl. XXVI figs 26–27, Pl. IV | A / C |

## KEEP CP020 nave (2026-11-11) — f03_cp020nave, KEPT 2026-11-11 and live in f03 (18d4107f -> 3e80da59; pre-keep pinned rounds/f03.blend.pre_cp020nave_keep)
State: HP-FITOUT, Jan-Apr 1851 (Hyde Park only; nothing Sydenham). Script `scripts/cand_cp020_nave_20261111.py`; same rules as the transept folder's KEEP envelope v2 (`apply_envelope_v2.py`, ENV2-02..10), mirrored west. Checks `checks/cp020_nave_checks.json` 15/15, dims 40/40 (`checks/cp020_nave_dims.md`), state 48/48 (`checks/cp020_nave_state.md`).
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT60 | **Nave tier-3 strip** for x 60..132 and -60..-132: columns on y = ±36 (col_62), 72 ft light trusses (truss72) on every column line, ridge-and-furrow roof units over \|y\| < 60 at 62 ft 2 in, glazed tier-3 clerestory bays at y = ±60, nave-front railings at y = ±36. The f03 transept model left this strip to a nave model, so CP020 looked into open sky and a column-less nave. | Downes 24 ft grid, nave 72 ft, girder tops 22'2"/42'2"/62'2" (D11a-c); ENV2-02 | B |
| FT61 | **West nave, full three-tier section** x -132..-924: tiers at \|y\| ≤ 60 / ≤ 132 / ≤ 204 (120 / 264 / 408 ft), girders between every column pair, tier-1/2/3 roof units, tier-2 glazed clerestory at y = ±132, boarded ground tier at y = ±204, galleries (9 in timber slabs at 22 ft 11 in) over the aisles \|y\| 36..60 and 108..132 with railings on y = ±36, ±60, ±108. No gallery girders under the slabs beyond the tier-1 girders, no stairs, no exhibits, no people, no paint shop in the west block. | SURVEY: length 1,848 ft, tier widths 408/264/120; ENV2-05 simplifications | B / C |
| FT62 | **West end at x = -924** (half of 1,848 ft between end column centres, transept taken as the middle): boarded ground-tier bays, glazed tier-2/3 bays, end-screen columns at (-924, ±12). No doors, no entrance or Downes end elevation detail; seen only as a pale band at the vanishing point. | C02 / ENV2-04 pattern; end elevation not modelled | C |
| FT63 | **Floor boards** continued x -924.5..-144, y ±204 (GT_FloorBoards, object at the origin so the board pattern runs on; top = live floor top, check N11). The west nave is shown boarded; only the FT09 east patch is still being laid. | FT09-FT10; reuse | C |
| FT64 | The west arm's x = -132 tier-2 side walls for \|y\| < 132 (18 objects WALL/WALLF/WLOUV_A-1...) hidden, not deleted: they would stand inside the building once the west block exists. | ENV2-06 mirrored | B |
| FT65 | New ironwork uses the part meshes' own painted materials (GT_IronColumn_OJ / GT_IronGirder_OJ); the west nave is shown painted, not part-primed. Roof units keep the arm-roof orientation (ridge along x), not checked against a Downes nave roof plate (as ENV2-03). | Paint progress in the west nave Jan-Apr 1851 not documented here | C |
| FT66 | **Render recipe.** The live CP020 PNG (Oct 27 06:46, people v3.3 pass) reproduces only with people_lib 3.3 (survey d19449b; `scripts/render_views_ppl33.py`), `--keep-lighting`, 24 spp and exposure **-1.768** (found by search: max diff 1/255, luma 128.75 vs 128.76; the blend's own exposure is -0.7 and gives luma 164). Candidate after uses the identical recipe. | Matched before/after | — |

## CANDIDATE CP022 envelope (2026-11-11) — o01_cp022envelope, NOT live, no verdict (live rounds/o01.blend unchanged, md5 4776f618)
State: HP51 OPENING, 1 May 1851 (Hyde Park only; nothing Sydenham). Script `scripts/cand_cp022_envelope_20261111.py` = the KEPT CP020 nave rules (`scripts/cand_cp020_nave_20261111.py`, FT60-FT65) applied unchanged to o01 (same transept part library and pre-CP020 block layout), plus the FT71 gallery-figure fix. Checks `checks/cp022_envelope_checks.json` 17/17, dims 37/37 (`checks/cp022_envelope_dims.md`, same 37/37 as live o01), state 26/26 (`checks/cp022_envelope_state_state.md`, same as live o01).
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT67 | (= FT60) Nave tier-3 strip for x 60..132 and -60..-132 in o01: col_62 on y = ±36, truss72 on every column line, tier-3 roof units over \|y\| < 60 at 62 ft 2 in, glazed tier-3 clerestory at y = ±60, nave-front railings at y = ±36. | Downes 24 ft grid, nave 72 ft, girder tops 22'2"/42'2"/62'2" (D11a-c); CP020 KEEP | B |
| FT68 | (= FT61/FT62) West nave, full three-tier section x -132..-924 (120 / 264 / 408 ft tiers), girders, roof units, tier-2 clerestory, boarded ground tier, gallery slabs over the aisles \|y\| 36..60 and 108..132 with railings; west end at x = -924 with end-screen columns at (-924, ±12). 542 columns, 1,869 girders, 39 trusses, 1,773 roof units, 243 wall bays, 210 railings. The live CP022 frame showed the west side gallery standing against open sky because o01 stops at x = -132. | SURVEY: length 1,848 ft, tier widths 408/264/120; CP020 KEEP; end elevation not modelled | B / C |
| FT69 | (= FT63) Floor boards continued x -924.5..-144, y ±204 (copy of the o01 FLOOR_BOARDS material; top = live floor top, check N11). | FT63 reuse | C |
| FT70 | (= FT64) The x = -132 tier-2 side walls for \|y\| < 132 (18 objects WALL/WALLF/WLOUV_A-1…) hidden, not deleted. | ENV2-06 mirrored | B |
| FT71 | **Floating gallery visitors.** 46 gallery-level crowd figures (CROWD_OPG_*, z 22 ft 11 in) whose feet are not over any gallery deck (GAL_* or C22_GAL_*, 0.5 ft inset) hidden, not deleted. In CP022 they stood in mid-air over the nave/transept crossing at x ≈ -43 ft, y 12..36 ft (no gallery crosses there), legs dangling. 334 gallery figures remain. | Staging bug (spawn rectangle ran over the crossing); no source needed | — |
| FT72 | The new west block is empty: no exhibits, visitors, banners or Owen Jones stripe check beyond the part meshes' own paint, though the nave was full on 1 May 1851. It is only seen at distance beyond the transept galleries in CP022. | Judgement call; dressing the west nave is out of scope for a one-scene pass | C |
| FT73 | **Render recipe.** render_views.py with people_lib 3.3 (survey d19449b) via `scripts/render_views_ppl33.py`, `--keep-lighting` (blend exposure -0.7, AgX MHC), 1280x720, 48 spp. Re-rendering live o01 this way matches the stored live CP022 PNG in structure and luma (146.72 vs 146.75) but not every person (max 246, mean 2.13: people_lib variant differences), so before = live o01 re-rendered with the identical recipe, not the stored PNG. | Matched before/after | — |

## CANDIDATE CP027 east nave (2026-11-12) — h01_cp027east, NOT live, no verdict (live rounds/h01.blend unchanged, md5 73c09039)
State: HP51, exhibition open, summer 1851 (Hyde Park only; nothing Sydenham). Script `scripts/cand_cp027_east_20261112.py` = the KEPT CP020 nave rules (FT60-FT65; reused for CP022 FT67-FT70) mirrored to the EAST on h01's own part library. Live CP027_stair_foot_start looks due south from (103.7, -50) ft, so frame-left is due east, where h01 stopped at x = +132 ft: the ground tier showed a green lawn and open hazy sky under the side gallery. Checks `checks/cp027_east_checks.json` 17/17, dims 39/39 (`checks/cp027_east_dims.json`, run on a copy under /workspace/tmp/cp027/dimsrun because check_dims reads ../route), state 38/38 (`checks/cp027_east_state.json`, incl. >= 1 ft camera clearance; live h01 also 38/38).
| ID | Departure / change | Source / reason | Grade |
|---|---|---|---|
| FT74 | (= FT60/FT67, east half) Nave tier-3 strip for x 60..132 in h01: col_62 on y = ±36, truss72 on every column line, tier-3 roof units over \|y\| < 60 at 62 ft 2 in, glazed tier-3 clerestory at y = ±60, nave-front railings at y = ±36. | Downes 24 ft grid, nave 72 ft, girder tops 22'2"/42'2"/62'2" (D11a-c); CP020 KEEP | B |
| FT75 | (= FT61/FT62 mirrored) East nave, full three-tier section x 132..924 (120 / 264 / 408 ft tiers), girders, roof units, tier-2 clerestory, boarded ground tier at y = ±204, gallery slabs over the aisles \|y\| 36..60 and 108..132 with railings; east end at x = +924 with end-screen columns at (924, ±12). 536 columns, 1,833 girders, 36 trusses, 1,728 roof units, 237 wall bays, 204 railings. East end = half of 1,848 ft with the transept at the middle (FT62 convention; the real transept was close to, not exactly at, the middle). No east-end elevation detail (it is beyond the frame). | SURVEY: length 1,848 ft, tier widths 408/264/120; CP020 KEEP | B / C |
| FT76 | (= FT63 mirrored) Floor boards continued x 144..924.5, y ±204 (FLOOR_BOARDS material; top = live floor top, check N11). | FT63 reuse | C |
| FT77 | (= FT64 mirrored) The x = +132 tier-2 side walls for \|y\| < 132 (18 objects WALL/WALLF/WLOUV_A+1…) hidden, not deleted. The \|y\| > 132 ones stay (clerestory above the tier-1 roof). | ENV2-06 mirrored | B |
| FT78 | No figures hidden. The FT71 floating-figure test finds 0 gallery-level crowd figures off a deck in h01 (report only, N14), and no figure stands inside a new column (N12). Hiding nothing keeps the people_lib variant order, so the stair visitors are dealt the same on both sides of the pair. | CP021 side-effect lesson (people reshuffle) | B |
| FT79 | The new east block is empty: no exhibits, visitors, banners or stall dressing, though the east nave (foreign side) was full in 1851. In CP027 it is seen through the side-gallery columns at 30-300 ft. | Judgement call; dressing the east nave is out of scope for a one-scene pass (as FT72) | C |
| FT80 | **Render recipe.** render_views.py with people_lib v3.1 via `scripts/render_views_ppl31.py` (the lib of the live CP027 PNG, people v3.1 keep b12c425), shared look `--era 1851` (tod interior_daylit; exposure set by the look, identical both sides), CP027_stair_foot_start at 1920x1080, 48 spp; side-effect cam CP027_gallery_rail_start 1280x720, 24 spp. Before = live h01 re-rendered with the same recipe (the stored Oct 27 PNG is 1280x720 and its stair visitors came from an earlier people_lib draw). `scripts/render_cp027_east.sh`. | Same-recipe pairs (CP020/CP022 lesson) | — |
