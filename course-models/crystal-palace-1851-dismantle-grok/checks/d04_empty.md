# d04_empty checks: 32/32

| id | check | target | measured | pass |
|---|---|---|---|---|
| K01 | CP030_empty_walk_start lens | 28 | 28.0 | PASS |
| K02 | CP030_empty_walk_start no roll (camera X axis z) | 0 | -0.0 | PASS |
| K03 | CP030_empty_walk_start eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP030_empty_walk_start clearance to nearest visible mesh (ft) | >= 3 | 5.27 (EGRAVEL_APRON) | PASS |
| K01 | CP030_empty_walk_end lens | 28 | 28.0 | PASS |
| K02 | CP030_empty_walk_end no roll (camera X axis z) | 0 | 0.0 | PASS |
| K03 | CP030_empty_walk_end eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP030_empty_walk_end clearance to nearest visible mesh (ft) | >= 3 | 5.27 (EGRAVEL_APRON) | PASS |
| K05 | CP030_empty_walk move length (m) | <= 10 m | 7.54 | PASS |
| K01 | CP030_empty_aisle_start lens | 35 | 35.0 | PASS |
| K02 | CP030_empty_aisle_start no roll (camera X axis z) | 0 | 0.0 | PASS |
| K03 | CP030_empty_aisle_start eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP030_empty_aisle_start clearance to nearest visible mesh (ft) | >= 3 | 4.14 (COL_X+060_Y-036) | PASS |
| K01 | REV_dismantle_aerial_start lens | 35 | 35.0 | PASS |
| K02 | REV_dismantle_aerial_start no roll (camera X axis z) | 0 | 0.0 | PASS |
| K06 | rounds/d03_empty.blend size (MB) | < 90 | 18.1 | PASS |
| K06 | rounds/d03_dismantle.blend size (MB) | < 90 | 18.2 | PASS |
| K06 | rounds/d04_dismantle.blend size (MB) | < 90 | 18.1 | PASS |
| K06 | rounds/d04_empty.blend size (MB) | < 90 | 18.1 | PASS |
| K07 | no Sydenham-named data (Hyde Park 1851 only) | 0 | 0 | PASS |
| K08 | HP51 dressing 'crowd' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'banners' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'sculpture' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'textiles' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'machinery' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'planters' visible | 0 | 0 | PASS |
| K09 | Muse plinths and benches cleared | 0 | 0 | PASS |
| K10 | Muse crates present and credited | > 0, credited | 64, credited=True | PASS |
| K11 | EMPTY: half the vitrines kept (dust-sheeted) | 24 | 24 | PASS |
| K12 | EMPTY: dust sheets | present | True | PASS |
| K13 | EMPTY: packing cases at the machinery footprints | >= 8 | 18 | PASS |
| K21 | floor seam: exterior boards above transept boards where they overlap (ft) | 0.01-0.05 | 0.03 | PASS |
