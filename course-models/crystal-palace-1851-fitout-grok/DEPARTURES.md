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
| FT54 v2 | **Staging (CANDIDATE, `polish_cp028_drive_v2_cand.py`):** ATTEND_OILER stands ON a 14 ft pair of deal steps (CP028_STEPS, top 4.30 m, 14 rises of 0.307 m, 74 deg front, side-on to the wall, back legs 0.19 m clear of the boarding), facing up the steps and turned 10 deg toward the wall (camera sees his right side). Lower foot on tread 12 (3.69 m), right foot on tread 13 (3.99 m; shin sheared up/forward, thigh hidden in the coat), body between the stiles, top cap at thigh height (0.60 m above the lower foot) just in front of his coat. Hand 0.15 m short of bearing S' at x=16 ft (z 5.24 vs 5.27 m), zinc feeder spout to the bearing. Own mesh copy: pale moleskin trousers below the coat hem and dark boots, for legibility against the boarding. | Storyboard CP028 "daily work behind the spectacle". No source shows this man; pale moleskin/duck trousers were ordinary 1850s labourers' wear. | C |
