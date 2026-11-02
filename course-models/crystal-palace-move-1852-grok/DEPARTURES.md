# DEPARTURES — MOVE + K-JOINT (CP032), Grok, round m01

Grades: **A** documented (Downes 1852 / dated source) · **B** documented in outline, detail inferred · **C** interpretive, period-plausible · **D** film/legibility adjustment, knowingly not historical.

| # | Decision | Grade | Why / source |
|---|---|---|---|
| MV01 | Hero joint dimensions (8 in column, 3 ft 4½ in connecting piece, 3 ft girder, 2×½ in snug groove, ¼ in end clearance) reused from Grok dismantle joint / parts1851.py | A | Downes 1852 Pl. VIII-type details; verified K1–K8 |
| MV02 | Joint shown on a trial-assembly stand, not in the building | D | lets a 50 mm camera stand at eye height 5.25 without being inside the structure |
| MV03 | Iron keys on the E girder, oak wedges variant on KJ_oak | B | both used; which at which joint is not recorded |
| MV04 | W girder drawn back 9 in ("exploded") to show the snug/U engagement | D | didactic; labelled as exploded state |
| MV05 | Paint: interpretive 1851 blue on Hyde Park parts | C | Owen Jones scheme is documented for the interior; exact tint inferred |
| MV06 | Departure stack: generic stripped frame bay behind, stacks of columns/girders/connecting pieces, crates | C | illustrative of the 1852 dismantling, not a surveyed layout |
| MV07 | Arrival (Sydenham) is a minimal generic staging area on a gentle slope, wooded edge, spoil cones | C | supported by ILN 5 Jun 1852 sketch (Muse S46, wooded with deer); no site survey used; Sydenham building NOT modelled (Hyde-Park-only rule) |
| MV08 | Locator: orthographic plane, two dots, Thames schematic, scale bar; **no route drawn** | D | camera-grammar exception (ortho insert); route unknown so not shown; HP–SY ≈ 6.98 mi straight line (M1) |
| MV09 | Sky sun disc off (Nishita disc fails silently in Blender 5.1); sun lamp carries direct light | D | technical |
| MV10 | Muse elm/props appended read-only with credit (Muse round-2 models); Claude/Codex folders untouched | — | reuse rule |
| MV11 | Figures: generic Grok PPL-1851 workmen/clerks; no named individuals | C | |
| MV12 | m02: KJ_exploded pulled back to (-3.3,-5.9,5.25 ft) looking at the W joint; north girder + its oak keys hidden for this camera only via `grok_states` (still in the scene for other shots) | C | camera fix only; joint geometry unchanged |
| MV13 | CP068 legacy-today: separate lean blend `m03_legacy` with K-JOINT kit + one 24 ft prefabricated bay on park grass under present-day daylight; analytical study plinth/pad, not a ruin or rebuild | B | storyboard asks PARK-NOW labelled model study; method, not archaeology |
| MV14 | CP068 materials: same Owen-Jones blue kit paint as m01; lean 28-sample / 1280×720 renders | D | box busy |
| MV15 | CANDIDATE (2026-11-02, no verdict) CP032 departure hands: the 7 boxy STAFF_* stand-ins replaced in a sibling blend `rounds/candidates/m02_cp032people.blend` by survey people_lib v3.4 hero figures (6 × 1850s_workman, STAFF_03 clerk → 1850s_gentleman), same xy and heading, feet on grass z=0; heights 1.66–1.83 m. Workmen's smocks/waistcoats dark matte fustian (CP012 values); clerk black wool frock coat + black silk hat; clerk's hands given the skin slot. A scripted arm-lowering pass was tried and dropped (tore sleeve shells). Live m02.blend untouched | C | 1852 workmen's dress per CP012 precedent (fustian/moleskin, not white); no named individuals; figure count and placement unchanged |

## Look — crystal-palace-look v1 (2026-10-27)
Shared grade from `/workspace/crystal-palace-survey/look/` (AgX Medium High Contrast, Nishita-family MULTIPLE_SCATTERING sky + haze, era white-balance, mid-grey exposure table, glass/white-iron albedo ceilings). Render scripts import via `cpl_look.py` and call `apply_look` before rendering. Hero tiles re-rendered lean (24 spp, 1280×720). See `look/README.md` for Sydenham adoption.
