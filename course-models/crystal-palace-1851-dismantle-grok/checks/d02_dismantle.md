# d02_dismantle checks: 34/34

| id | check | target | measured | pass |
|---|---|---|---|---|
| K01 | CP031_joint_detail_start lens | 50 | 50.0 | PASS |
| K02 | CP031_joint_detail_start no roll (camera X axis z) | 0 | -0.0 | PASS |
| K03 | CP031_joint_detail_start eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP031_joint_detail_start clearance to nearest visible mesh (ft) | >= 3 | 3.00 (EROOF1_t1-1_+192_-144) | PASS |
| K01 | CP031_lateral_start lens | 35 | 35.0 | PASS |
| K02 | CP031_lateral_start no roll (camera X axis z) | 0 | -0.0 | PASS |
| K03 | CP031_lateral_start eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP031_lateral_start clearance to nearest visible mesh (ft) | >= 3 | 5.24 (EFLOOR_BOARDS) | PASS |
| K01 | CP031_lateral_end lens | 35 | 35.0 | PASS |
| K02 | CP031_lateral_end no roll (camera X axis z) | 0 | 0.0 | PASS |
| K03 | CP031_lateral_end eye height above standing surface (ft) | 5.25 | 5.25 | PASS |
| K04 | CP031_lateral_end clearance to nearest visible mesh (ft) | >= 3 | 5.24 (EFLOOR_BOARDS) | PASS |
| K05 | CP031_lateral move length (m) | <= 10 m | 9.75 | PASS |
| K01 | REV_dismantle_aerial_start lens | 35 | 35.0 | PASS |
| K02 | REV_dismantle_aerial_start no roll (camera X axis z) | 0 | 0.0 | PASS |
| K06 | rounds/d02_empty.blend size (MB) | < 90 | 17.6 | PASS |
| K06 | rounds/d02_dismantle.blend size (MB) | < 90 | 18.1 | PASS |
| K07 | no Sydenham-named data (Hyde Park 1851 only) | 0 | 0 | PASS |
| K08 | HP51 dressing 'crowd' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'banners' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'sculpture' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'textiles' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'machinery' visible | 0 | 0 | PASS |
| K08 | HP51 dressing 'planters' visible | 0 | 0 | PASS |
| K09 | Muse plinths and benches cleared | 0 | 0 | PASS |
| K10 | Muse crates present and credited | > 0, credited | 12, credited=True | PASS |
| K11 | DISMANTLE: all vitrines gone | 0 | 0 | PASS |
| K14 | home girder hidden while lowered | all hidden | [True] | PASS |
| K15 | lowered girder between floor and its seat (ft) | 0 < z < 19.17 | 7.00-10.00 | PASS |
| K16 | lowered girder clear of its columns (x, ft) | 156.4 < x < 179.6 (column faces) | 156.60-179.40 | PASS |
| K17 | shores bear on the neighbour girder (top vs girder soffit, ft) | 19.17 +/- 0.15 | 19.17 | PASS |
| K18 | sheer-leg head above the girder line (ft) | > 22.17 + 10 | 38.13 | PASS |
| K19 | zone R stripped / zone G glass-off units | > 0 / > 0 | 9 / 108 | PASS |
| K20 | joint keys at the column head (ft from joint) | < 3 | 0.55 | PASS |
