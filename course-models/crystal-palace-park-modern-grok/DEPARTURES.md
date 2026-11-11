# DEPARTURES — crystal-palace-park-modern-grok (branch grok-park-modern)

## D-PM-* (r01)
- **D-PM-01 I** Park levels reuse Sydenham ruins41 terrain. No OS OpenData / LiDAR tiles found in the workspace (searched 2026-10-27); log and proceed.
- **D-PM-02 I** High Level shed treated as demolished by the 1960s (PARK60/NOW show platform stubs only). Exact demolition date after the 1954 closure **U**.
- **D-PM-03 I** PARK-NOW subway shown in restored Open-House condition (cream/red patterned brick). Exact present-day finish **U**; not claimed always-open.
- **D-PM-04 I** PARK54 subway sealed/quiet after closure; gated booking-hall entrance.
- **D-PM-05 I/U** NSC athletics stadium + concrete sports hall block-outs at (−50, −550, −47) m near the former south-basin/football ground. NSC opened 1964 **R**; no plans in repo → forms **U**.
- **D-PM-06 I** Footprint overlay registered to the Sydenham model axes (not independently georeferenced to OS). Label approximate until a surveyed registration exists.
- **D-PM-07 R** Dinosaurs appended read-only from `dinosaurs-1854-r01.blend` (conserved survivors). Sydenham ruins41 shell appended read-only; this folder never edits those sources.
- **D-PM-08 U** PPL-NOW visitor counts and dress are stand-ins.

- **D-PM-09 I**: purged cameras that rode in on non-CAMERAS collections from ruins41 append (name collisions).
- **D-PM-10 I**: subway AREA lights for CP071; restored brighter than sealed PARK54/60.
- **D-PM-11 I**: CP072 footprint cam raised to elevated overview; CP074 retargeted after dino translate.

## r02 quality (2026-10-27)
- D-PM-12 I: PARK-NOW grass carpets + park trees (no OS tree survey; placement U)
- D-PM-13 I: noise grass / worn stone / NSC formwork concrete materials
- D-PM-14 I: visitor silhouettes with arms; hero figures just outside camera clear zone

## r02 coverage (2026-10-27)
- **D-PM-15 I** CP067 `CAM_CP067_dino_conservation_35mm` + interpretive board near conserved Hawkins cluster.
- **D-PM-16 R/I** CP070 aliased: `CAM_CP070_park_entry_35mm` + `CAM_CP070_begin_walk_35mm` (same pose; begin-the-walk beat).
- **D-PM-07 R** dino append path now `dinosaurs-1854-r02.blend`.

## r17 WEAK→OK ( 2026-10-27 04:22 UTC )
- **D-PM-17 I** CP065 sealed subway bulkhead at SUB_Z (`pk_subway_seal_N`) — street booking gate was above cam lookat.
- **D-PM-18 I** CP066 NSC CZ raised, basins hidden, TrackRed emit, SW 3/4 cam; hero `r17k_park60_*`.
- **D-PM-19 I** CP073 along-terrace cam + mid-warm sphinx stone; hero `r17k_parknow_*`.
- **D-PM-20 I** Horizon berms E/W/S + aerosol (no shared look preset).

## set_v18 CP071 subway dress (2026-10-27)

- **D-PM-21 I** CP071 Open-House subway: checkered floor tiles, cream brick noise walls, red brick columns with stone bases/capitals, dado + spring string courses, iron vault ribs, hanging lamp fixtures, wall poster boards, side handrail. Exact present-day finish still **U** (extends D-PM-03).
- **D-PM-22 I** Authored subway AREA lights + exposure (−0.8) held (`KEEP_LIGHTING`); no sun/world rewrite.
- Hero: `renders/r18_parknow_CAM_CP071_subway_interior_28mm.png` from `rounds/parknow-r18.blend`. KEEP by eye vs r01 graybox.

## set_v18 CP071 true subway vaults (2026-10-27)

- **D-PM-23 R** CP071 ceiling replaced with Muse `sy-subway-vault-bay` fan/groin vaults (refs S87-subway-restored-interior-2025 / S87-subway-interior-2016; HE 1385457). 3×6 octagonal cream-brick columns, polychrome red+cream brick soffits, stone ribs/capitals; vaults terminate in brick end wall. PARK-NOW dirt/wear on mats + dirty floor; modern AREA lamps (aimed at soffits) + LED uplights retained/adjusted. Terrain boolean-cut so park ground no longer caps the corridor. Cam nudged to aisle x=PITCH/2 so it is not inside a column. `KEEP_LIGHTING` (exposure −0.8; no sun/world rewrite).
- **D-PM-24 I** Hero `renders/r19_parknow_CAM_CP071_subway_interior_28mm.png` from `rounds/parknow-r19.blend`. KEEP by eye vs r18 flat olive slab + box ribs.

## set_v18 CP071 octagonal columns (2026-10-27)

- **D-PM-25 R** CP071 column shafts + base drums rebuilt as true flat-sided octagons (COL_FLATS 0.73 / BASE 0.82) with EdgeSplit + dark vertical corner arrises so the Byzantine-Italianate octagon reads at a glance. Vaults, polychrome soffits, dirt/wear, modern lamps, exposure −0.8 held. Hero `renders/r20_parknow_CAM_CP071_subway_interior_28mm.png` from `rounds/parknow-r20.blend`. KEEP by eye vs r19 cylindrical-looking shafts.

## CP076 plateau CANDIDATE (2026-11-11, Grok; candidate only, no verdict)
Candidate `rounds/candidates/parknow-r02_cp076plateau.blend` built from live `rounds/parknow-r02.blend` (unchanged) by `scripts/candidate_cp076_plateau.py`. PARK-NOW (present day) only.
- **D-PM-26 R/I** Upper Palace Terrace grass: `pk_grass_upper_palace_terrace` replaces the dud-fix v4 hidden `pk_grass_plateau` (which overhung the lower terrace to y -127.5 m), trimmed to the terrace/basement wall line y >= -47.9 m at the wall top (z 0.0, top 0.02). R: Crystal Palace Park Regeneration Plan (May 2017) App. B p.4-7: palace site infilled with spoil after 1936; Upper Palace Terrace at palace ground level, Lower Palace Terrace at basement level, ~8 m apart, upper terrace "rough grass with rows of semi-mature trees". I: the modelled wall is 7.2 m (z -7.2 -> 0.0), not 8 m; kept the ruins41 levels. The 1937-40 cleared foundations (`footprint_ground`) now sit under grass, which also changes CP072 (side effect, see pairs).
- **D-PM-27 I** Grounding: all 28 `pk_tree_*` (upper park) and every PPL-NOW visitor inside x +-340, y -215..215 m are dropped onto the highest render-visible ground under the foot (ray-cast; ignores trees, people, overlay, sphinxes, hidden objects). They floated up to 34 m (heroes 126-128/144-149 at z 13-26 m) and 7 m (trees on the hidden z 0 plateau over the z -7.2 terrace). Pre-existing duplicate heroes 144/147, 145/148, 146/149 left as they are.
- **D-PM-28 I** Trees: the icosphere "lollipop" meshes become parametric broadleaf trees (MV20 v2 generator vendored as `scripts/park_trees_now.py`, oak habit, H 11-17 m, leaf ramps x1.7 for the PARK-NOW look, no haze term, no blossom). Species U: the park stock is mixed oak, plane, lime, horse chestnut, sycamore (Regeneration Plan App. B; Crystal Palace Park Tree Trail); oak habit is a stand-in. Placement U (no tree survey; D-PM-12 positions kept).
- **D-PM-29 I** Seven trees that stood on the lower-terrace lawn (y -127.5..-47.9) moved up onto the spoil embankment / upper-terrace edge behind the wall (y -46..-30, same x). Historic England 1000373: the terraces are laid to grass; Regeneration Plan: the embankment between the two terraces is "covered by self-seeded scrub and trees". pk_tree_20 moved out of the terrace basin water (y -154.9 -> -132.0); pk_tree_11 off the Parade carriageway (y 65.1 -> 82.5).
- **D-PM-30 I** Scrub: 53 self-seeded scrub bushes (thorn habit, 2.5-5 m) in a broken band on the embankment top, y -47..-41 m, x +-240 m. Density and extent U.
- **D-PM-31 R/I** Crystal Palace transmitter (BBC 1956, now Arqiva), parametric lattice: 120 ft (36.6 m) square base, 12 diminishing panels to a 14.5 ft (4.4 m) square platform at 429 ft (130.8 m), lattice to 196 m main structure, UHF aerial cylinder to 219 m. R: Wikipedia "Crystal Palace transmitting station" (BICC design data, 219 m, aquarium site at the north end); thebigtower.com (196 m main structure, 219 m with UHF aerial). I: leg profile (concave, exponent 1.6), bracing pattern, member sizes and grey paint are by eye; upper-section taper is inferred. Position: OS grid refs subway TQ 33791 70972 (= model (0, 60)) and mast TQ 33947 71220 give model (289, 11) with the palace axis assumed at bearing 22.5 deg, within ~10 m of the modelled north water-tower base (281.6, 18.3), which fits the aquarium site; nudged to (308, 5) to clear that base (I, +-20 m). Base sits on `ground_under_palace` at z -4.37 (hidden behind trees and the wall in CP076).
- Unchanged: cameras, exposure (-0.8), world, look, sphinxes, terraces, people meshes. Side effect: the basement-arcade niches read darker in CP076 because the trimmed terrace grass now roofs the basement (they were lit from above through the missing plateau).

## CP076 plateau KEEP, scoped (2026-11-11)
- D-PM-26..31 are KEPT for CP076 only (both cams), carried by `rounds/parknow-r21_cp076.blend` (md5 bc62d275). They are NOT in `rounds/parknow-r02.blend` (md5 48fc01ec, unchanged), so CP067/CP070/CP072/CP074/CP075 stay as before.
- Rejected side effects (parent verdict 2026-11-11): CP072 footprint (the 1937-40 cleared foundations go under the D-PM-26 terrace grass, which is the point of the shot); CP070 begin walk (the foundation edge stops reading); CP075 layered NSC (a D-PM-28/29 tree cuts the right edge). These cams must never render from r21.
- CP073: held, not kept. Its live hero comes from parknow-r17 (D-PM-19 cam), and the viewed pair used the r02 cam. Waiting for a verdict on the true pair.
