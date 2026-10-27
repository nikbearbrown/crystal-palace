| id | check | target | tol | measured | pass |
|---|---|---|---|---|---|
| D19a | 72 ft truss, face-to-face extent across the nave (Y) | 71.2 | 0.4 | 71.45 | PASS |
| D19b | 72 ft truss depth (Z) | 6.0 | 0.1 | 6.0 | PASS |
| D20 | main rib A extrados diameter (X extent) | 74.3333 | 0.70% | 74.3333 | PASS |
| D21 | main rib A radius (extrados, the 37 ft the ribs are 'cut to') | 37.0 | 0.70% | 37.1667 | PASS |
| D21i | main rib A depth (extrados - intrados) | 1.5 | 0.02 | 1.5 | PASS |
| T01 | vault crown (rib extrados top) above floor | 102.1667 | 1.0 | 102.1667 | PASS |
| T02 | transept (vault) length, end rib to end rib | 408.0 | 0.5 | 408.0 | PASS |
| T05 | main rib A pitch (on the 24 ft columns) | 24.0 | 0.01 | 24.0 | PASS |
| T06 | main ribs carried on the strong 72 ft trusses at y = +-12 ft | 2 | 0 | 2 | PASS |
| G01 | columns on Claude's 24 ft grid (max off-grid error) | 0.0 | 0.01 | 0.0 | PASS |
| G02 | transept clear width between column lines | 72.0 | 0.01 | 72.0 | PASS |
| D11a | tier-1 girder top | 22.1667 | 0.05 | 22.1667 | PASS |
| D11b | tier-2 girder top | 42.1667 | 0.05 | 42.1667 | PASS |
| D11c | tier-3 girder top | 62.1667 | 0.05 | 62.1667 | PASS |
| D12 | gallery floor top | 22.9167 | 0.05 | 22.9167 | PASS |
| T03 | south cross gallery depth (Plate II '48.0') | 48.0 | 0.1 | 48.0 | PASS |
| T04 | north cross gallery depth | 24.0 | 0.1 | 24.0 | PASS |
| D13 | column outside diameter (shaft) | 8.0 | 0.1 | 8.0 | PASS |
| D14 | column shaft top (bottom of the first connecting piece) | 18.9792 | 0.05 | 18.9792 | PASS |
| E01_ELM_NORTH2_LEAVES | ELM_NORTH2_LEAVES: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| E01_ELM_NORTH2_WOOD | ELM_NORTH2_WOOD: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| E01_ELM_NORTH_LEAVES | ELM_NORTH_LEAVES: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| E01_ELM_NORTH_WOOD | ELM_NORTH_WOOD: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| E01_ELM_SOUTH_LEAVES | ELM_SOUTH_LEAVES: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| E01_ELM_SOUTH_WOOD | ELM_SOUTH_WOOD: min clearance to vault intrados / 72 ft column lines (>= 3 ft) | 3.0 | 0 | 3.0 | PASS |
| F01 | Osler fountain glass body height above the floor | 27.0 | 0.5 | 27.0 | PASS |
| G03 | arm gallery floor top | 22.9167 | 0.05 | 22.9167 | PASS |
| S01 | avenue stair landing top | 11.4583 | 0.05 | 11.4583 | PASS |
| S02 | avenue staircases: one per avenue void (N, S) in the stair bay of each arm | 4 | 0 | 4 | PASS |
| CAM_CP031_joint_start | camera: >=1 ft from any branch/leaf, no roll, eye 1.6 m on walks |  |  | {'branch_clearance_ft': 77.47, 'roll_rad': 0.0, 'z_m': 1.6} | PASS |
| CAM_CP031_stacks_start | camera: >=1 ft from any branch/leaf, no roll, eye 1.6 m on walks |  |  | {'branch_clearance_ft': 49.28, 'roll_rad': 0.0, 'z_m': 1.6} | PASS |
| PROPS_muse | appended models/ props credited to their maker (Muse); no camera within 3 ft of a prop |  |  | {'props': 0, 'nearest_camera_ft': 1000000000.0} | FAIL |
| DRESS_cam | no interior camera inside or within 3 ft of a dressing object (statues, machines, crowd, planters, textiles) |  |  | {'nearest_ft': 1000000000.0, 'camera': '', 'object': ''} | PASS |
| DRESS_plinths | no empty display plinth: one bust per Muse plinth |  |  | {'plinths': 0, 'busts': 0} | FAIL |
| DRESS_counts | HP51 dressing present (crowd >= 250, sculpture, machinery >= 6, banners, textiles) |  |  | {} | FAIL |
