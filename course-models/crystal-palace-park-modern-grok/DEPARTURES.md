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
