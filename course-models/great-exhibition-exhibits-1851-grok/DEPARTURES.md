# DEPARTURES — hero exhibits (Grok Bot)
Grades: **A** = documented, **B** = derived from a surviving object / close analogue, **C** = staged for camera, **I** = interpretive.

| id | grade | departure / judgment call | why |
|---|---|---|---|
| EX01 | — | CP024 machine = **Nasmyth steam hammer** (Official Catalogue Class 6 no. 236), not Applegath's vertical press | A surviving c.1851–56 Nasmyth hammer (Smithsonian NMAH) gives real proportions; the ram's blow reads instantly on camera; Applegath's press survives only in engravings and its many-cylinder drum would be invented detail. |
| EX02 | B | Koh-i-Noor sized 1.55 × 1.30 × 0.68 in → ~186 ct by volume (3.52 g/cm³), pre-recut Mughal form (flat table, irregular facets), IOR 2.417 | 186 1/16 ct is the documented 1851 weight; exact pre-1852 geometry is from the later plaster casts/descriptions, so facet layout is approximate. |
| EX03 | I | Gilded "bird-cage" (32 bars, bell dome, gilt crown), glass bell over the stone, velvet stand, draped Chubb iron safe as pedestal, brass rail R 6.5 ft, policeman | From ILN 17 & 31 May 1851 and the Illustrated Exhibitor ("great parrot-cage", stone lowered into a safe at night). No measured drawing survives: bar count, radius and crown are interpretive. |
| EX04 | I | Osler candelabrum arm layout (8 lower + 6 upper + 1 top = 15 lights), festoon drops | Catalogue gives height 8 ft, 15 lights, prism shaft >3 ft only; arm arrangement follows Osler's general 1850s style. The originals (a pair, the Queen's) stood in the Central North Gallery — only one is built, on the preview dais. |
| EX05 | B | Hammer frame: base 14 × 6 ft, ~19 ft, raked double standards, separate anvil, entablature + cylinder | NMAH example proportions; the exhibited 1851 machine's own dimensions not found. Sole-plate arrangement interpretive. |
| EX06 | C | Stroke 3.5 ft; blow cycle lift 14 / hold 4 / fall 6 frames, 4 blows per 96 | Staged for a readable loop; real hammers ran faster/slower by valve setting. |
| EX07 | I | Dark green-grey machine paint | No colour record for the exhibit. |
| EX08 | C | No hot forging piece on the anvil (cold dies) | Exhibit machinery in the Hall was mostly shown running without work; avoids inventing glow/fire. |
| EX09 | C | Showroom stand (boards, Paxton column lines, Osler dais, crimson drape behind Osler) is a **preview stand only**, not a location claim | Assets ship standalone; the drape lets cut glass read against something other than sky. |
| EX10 | B | July crimson enclosure with gas jets around the Koh-i-Noor (ILN mid-1851) | e02 builds the July state: 8 crimson panels (south door open), 6 gas jets on swan-necks aimed at the stone, diamond emission warmed. Enclosure radius 3.4 ft (inside the 6.5 ft brass rail). Form interpretive — written accounts only. |
| EX11 | C | Placement test: Koh-i-Noor (96,0, main avenue east of the transept) + Osler (108,-22) in the transept r10 east block-outs (x ≤ 144); hammer at (-456,4) in Claude's west nave | Test only, to prove the assets drop in. Real 1851 locations differ (Koh-i-Noor near the transept in the main avenue; Osler in the gallery; the hammer in the NW machinery court) — not modelled in either host. Clash check reports intersecting host objects; `--hide-clash` hides only loose crowd figures standing in the footprint at render time (4 for the Koh-i-Noor); props/statues/machines are never hidden, so spots were chosen clear of them (K43 statue at x 120, locomotive at x 72–84). `--clear-sightlines` also hides loose crowd figures within 2.5 ft of a camera→asset sightline (the r10 avenue crowd is dense). Hosts are never saved (md5 checked before/after). |
| EX12 | C | CP024_ram pulled back 15 → 25 ft, EX_osler pulled back to 28 ft; ram rendered at f015 (top of lift) and f025 (on the die) | Preview showed a confusing tight crop and a cut-off candelabrum foot. |
| EX13 | C | Steam puffs (translucent emissive spheres) keyed to each of 4 ram impact frames on exhaust + anvil | Staged for a readable blow; not a measured exhaust volume. |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| EX20 | Crystal glass sparkle (coat + faint emission); 6-sided prism drops and festoon cones | Osler candelabrum flat glass | B |

## Look — crystal-palace-look v1 (2026-10-27)
Shared grade from `/workspace/crystal-palace-survey/look/` (AgX Medium High Contrast, Nishita-family MULTIPLE_SCATTERING sky + haze, era white-balance, mid-grey exposure table, glass/white-iron albedo ceilings). Render scripts import via `cpl_look.py` and call `apply_look` before rendering. Hero tiles re-rendered lean (24 spp, 1280×720). See `look/README.md` for Sydenham adoption.

## CP025 Koh (2026-10-27)
| ID | Topic | Call |
|---|---|---|
| EX_KOH_V1 | Prior CANDIDATE (ribbons + tight july crop): diamond invisible; grey pole (OSL_shaft_prisms) down cage; ribbons read as messy curved bars | **REJECT** (user). Live e02 untouched. |
| EX_KOH_V2 | KEEP `e02_koh_v2` promoted into live `rounds/e02.blend`: drop gilt ribbons; hide OSL_shaft_prisms + KOH_gas_pipes; three-wall crimson backdrop (N/E/W + roof, south open); reframe CP025_july_start 50 mm / eye 5.25 ft / no roll, whole birdcage on plinth | **KEEP** (user 2026-10-27). Promoted live. |
| EX_KOH_SPARKLE | Live (v2 promote): diamond emission Fac 0.25 / str 1.8 + warm/cool points. Stronger polish candidate `e02_koh_sparkle`: Fac 0.42 / str 4.5 + spark 55 W | **Cheat**. **REJECT** (user 2026-10-27) — no visible difference; keep v2 live. |
| EX_KOH_SCALE | Rose-cut diamond screen scale **3.5×** true ~1.55×1.3×0.68 in so facets read at 50 mm / ~10.5 ft | **Cheat** (candidate v2). |
| EX_KOH_COUNTER | Muse `glass-topped-display-counter` (~12 ft unit) vs ~7 ft July tent | **Skip** — does not fit without scaling. |

## 2026-10-27 hero call + next hero
| ID | Topic | Call |
|---|---|---|
| EX_KOH_KEEP | Koh-i-Noor v2 CP025 | **KEEP** — promote `e02_koh_v2` → live `e02`. Whole cage reads on plinth. |
| EX_KOH_SPARKLE2 | Stronger sparkle polish | **REJECT** (user) — no visible difference vs live v2. Pair `REJECTED_CP025_koh_sparkle_july_start_pair.png`. |
| EX_ORGAN | Willis 1851 / Gray & Davison | **Skip** — storyboard organ is CP045 (Sydenham 1857 music), not an HP blend shot. |
| EX_GATES | Coalbrookdale gates | **Skip** — no storyboard shot features them. |
| EX_HAM_MODEL | Nasmyth hammer CP024 MODEL enrich | **KEEP** (user): A-frame + cylinder + steam pipe read as Nasmyth. Promoted `e02_hammer` → live `e02` (`scripts/promote_hammer_live.py`). |
| EX_HAM_SETTING | Outdoor showroom / sea-blue horizon / lone truss around hammer | **Wrong** — CP024 is inside 1851 Machinery Court. |
| EX_HAM_COURT | Machinery Court setting around KEEP hammer | **CANDIDATE** `e02_hammer_court`: cast-iron columns, gallery+girders, glazed ridge-and-furrow roof, boarded floor, neighbour machine block-outs; pale daylit world (no Nishita sea); `interior_machinery`; CP024_ram_start raised/backed so top reads against gallery/roof. Pair `CANDIDATE_CP024_hammer_court_ram_start_pair.png`. Claude west nave not appended this pass. |

## 2026-11-01 Muse reference intake (CANDIDATES, no call made)
| ID | Topic | Departure / note |
|---|---|---|
| EX_MUSE_HAM_SRC | Source disagreement | Muse: 1851 Ferrier photo RCIN 2800024, height assumed 5.00 m ±30%. Ours: NMAH surviving c.1851–56 hammer, ~19 ft (5.79 m), base 14×6 ft. |
| EX_MUSE_HAM_DIM | Dimensions | Height 5.79 (ours) vs 4.98 m (Muse; ours within Muse's band). Frame width 4.43 vs 3.61 m; depth 1.83 vs 1.55 m; Muse throat 0.67 m. |
| EX_MUSE_HAM_FORM | Standards | Muse standards built as a V (wider at top) because of a rotation-sign error (build script ~l.146); Muse's NOTES and the photo say A-form. Left uncorrected (their folder is read-only). |
| EX_MUSE_HAM_MOTION | Motion | Muse Tup static at mid-stroke, single-acting; ours animated blow cycle + steam puffs (EX13). |
| EX_MUSE_DRESS_PLACE | Machinery Court dressing | 1851 portable engines and seed drills stood with agricultural implements (Class IX), not in machinery-in-motion; placing them beside the hammer is a dressing departure. Vacuum sugar apparatus is plausible for the machinery area. |
| EX_MCD_PLACARD | Machinery Court dressing (KEEP 2026-11-02) | Stand placards carry generic Official Catalogue class headings (CLASS V. Machines for direct use; CLASS VI. Manufacturing machines and tools), not exhibitor names; board size/lettering inferred from fig-29/fig-48 scans (dressing refs, not measurements). |
| EX_MCD_SHAFT | Machinery Court dressing | Overhead line shafts at 15.5 ft (param `--shaft-z`), drop hangers and column brackets, pulley sizes all inferred from fig-29 (Hibbert, Platt); no measured 1851 shafting layout for these stands. |
| EX_MCD_BELT | Machinery Court dressing | Belt from the engine block-out's added flywheel to the south shaft, and shaft-to-press/lathe belts, are dressing assumptions: the block-outs are generic, not identified 1851 exhibits. |
| EX_MCD_RAIL | Machinery Court dressing | Turned stanchion rails with rope on green cloth with crimson kerb (rope colours from fig-30 De la Rue); the boiler block-out is railed as an exhibit. Rails skip posts near columns. |
| EX_MCD_PEOPLE | Machinery Court dressing | 7 attendants/visitors baked from vendored people_lib (HBM, `cpl_people` tag removed so render-time swap ignores them) beside the older low-poly VIS figures — style mismatch; lady's head reads bare from behind at close range. |
| EX_MCD_SCOPE | Machinery Court dressing | fig-48 (Garrett & Son) used only for stand/placard treatment, not for its agricultural subject matter; figs 43/54/74 (generated patches) not used. Hyde Park 1851 only. |

## 2026-11-02 CP024 Machinery Court dressing KEEP (parent viewed all pairs)
| ID | Topic | Departure / note |
|---|---|---|
| EX_MCD_KEEP | Status | EX_MCD_PLACARD/SHAFT/BELT/RAIL/PEOPLE/SCOPE now apply to LIVE e02 (CP024 approach_start, approach_end, ram_start). Promoted by `scripts/promote_machinery_live.py`; old live `rounds/e02.blend.pre_machinery_keep`. |
| EX_MCD_PLACARD_NUDGE | Boiler placard position | Boiler CLASS V placard moved 1.0 ft east along the rail front (`--boiler-placard-dx 1.0`) purely for framing, so it clears the left edge of CP024_approach_start. No source fixes placard positions; still 1 ft outside the rope rail. |


## 2026-11-09 CP025 exhibit-court scan props (KEEP 2026-11-09: live e02 = byte copy of reviewed candidate e02_scanprops)
Sources: origin/main e88ee17 `scan-models/blend/` (Tripo H3.1 image-to-3D from single 1851 prints; ~1.4 M tris; estimated scale; read with `git show` into scratch, never checked out or edited). Our cleaned copies: `assets/scanprops/*_hp1851.blend` (`scripts/prep_scanprops.py`). All tagged `cp_era=HP1851`, `cp_state="Hyde Park 1851"`. Dressing only, never evidence against Downes/Fox Henderson dimensions.
| ID | Topic | Departure / note |
|---|---|---|
| EX_SCN_MESH | All three props | Generated meshes, not surveyed objects: unseen sides invented by the generator; decimated (collapse) 1.40–1.46 M → 58.8 k tris each; floating crumbs < 3 cm removed (slave 1,184 faces, cabinet 963, vase 8,347); larger loose islands kept; not retopologised, not watertight; textures downsized 2048 → 1024. |
| EX_SCN_FIG-52 | Greek Slave scale | Scaled to 1.655 m (×1.003): the 1851 exhibit was Powers' first marble (Raby Castle), 165.5 × 53.5 cm (Di Bello 2016, n.3); Wikipedia lists 165.7 cm for the Yale version. The scan's 1.65 m stands. Height includes the round base carved with the statue. |
| EX_SCN_FIG-52_SETTING | Greek Slave setting | Turned drum pedestal 0.80 m with a gilt revolving disc, four gilt posts and a crimson valance/tester canopy (2.1 m square, 3.9 m high) after the SAAM account ("rotating pedestal under a lavish red canopy"); pedestal and canopy shape and size are interpretive. Marble colour: the generated grey albedo is remapped to warm statuary white (luminance × 1.55 → ramp), ORM metal/roughness unhooked. |
| EX_SCN_FIG-52_PLACE | Greek Slave position | In 1851 it stood in the United States section (east nave); here it stands ~4 m west of the Koh-i-Noor enclosure so it reads in CP025_visitors_start/_end. Compression of the plan, not the catalogue position. |
| EX_SCN_FIG-54 | Elkington jewel cabinet scale | Scaled ×0.954 to the Royal Collection height (RCIN 1562, 97 × 132 × 81 cm, H × W × D) → 0.97 × 1.34 × 0.91 m; scan said max 1.40 m. Width within 1.5 cm; depth ~10 cm deep (invented back). Portraits are generated paintings, not the Thorburn miniatures; fig-54 used a repaired scan. |
| EX_SCN_FIG-54_PLACE | Cabinet position + stand | Catalogue: Her Majesty's no. 140, Main Avenue West, listed beside the Koh-i-Noor, so near the Koh is right in spirit; exact spot, the crimson-clothed stand (1.62 × 1.12 × 0.78 m) and the brass/rope rail are inferred. No glass case shown (unknown). |
| EX_SCN_VASE | Watherston & Brogden vase scale | Scaled ×0.381 to 0.457 m (18 in), from a secondary summary of the 1851 account (gold, 95 oz, "largest gold cup ever manufactured in this country"); the 18 in figure is NOT verified against the Art-Journal/Wyatt plate text — verify. Scan said 1.20 m, which is far too big for a 95 oz gold cup. |
| EX_SCN_VASE_COLOUR | Vase material | The generated albedo is grey (from a monochrome engraving); remapped to gold (luminance → dark-to-bright gold ramp, metallic 1.0, roughness 0.28). Enamel colours and the jewels described in 1851 are not modelled. Figure groups on the model follow the engraving (single statue on the cover), not the written description (Britannia/Scotia/Hibernia group). |
| EX_SCN_VASE_PLACE | Vase position + pedestal | Square pedestal 0.95 m with crimson cushion, no glass case (the real vase would almost certainly have been cased); position in the open court is a dressing choice. |
| EX_SCN_LAYOUT | Layout positions (scene metres) | Greek Slave group at (−3.6, 1.7) W of the Koh-i-Noor enclosure; Elkington cabinet stand at (1.2, −6.2) (moved in t4 so it no longer blocks the lit Osler plinth); W&B vase pedestal at (6.2, −8.6) in the open EX_lineup court. All three are framing choices for CP025_visitors_start/_end and EX_lineup_start, not catalogue positions. |
| EX_SCN_DECIMATE | Decimation budget | 58,799 / 58,800 / 58,799 tris (≈4 % of the generated 1.40–1.46 M); fine carving on the Greek Slave's chain/drapery and the cabinet's ormolu is softened; acceptable at the CP025/EX_lineup framing distances, not for close-ups. |
| EX_SCN_KEEP | Status | Parent viewed CANDIDATE pairs CP025_visitors_start, CP025_visitors_end, EX_lineup_start and KEPT all three (2026-11-09). Live `rounds/e02.blend` is a byte copy of `rounds/candidates/e02_scanprops.blend` (md5 fce122da…; not rebuilt; SCN_* objects still carry `candidate=e02_scanprops` and the text block is still `CREDIT_SCN_CAND`). Old live → `rounds/e02.blend.pre_scanprops_keep` (untracked, md5 a26776f5…). Known misses: cabinet reads very dark / near-silhouette in EX_lineup_start; Greek Slave small and dim in CP025 wides; vase height 18 in unverified. |
| EX_SCN_SCOPE | Era | Hyde Park 1851 only; nothing Sydenham. CP024 (Machinery Court) not dressed: none of the three props belongs there. |
