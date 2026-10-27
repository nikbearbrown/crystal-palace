# state checks: fitout -- 48/48 pass

| id | check | target | measured | pass |
|---|---|---|---|---|
| CP018_cradle_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP018_cradle_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 22.92 | 22.92 | PASS |
| CP018_cradle_start.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP018_cradle_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 50 | 50.0 | PASS |
| CP018_cradle_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 4.17 | PASS |
| CP018_paint_end.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP018_paint_end.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP018_paint_end.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP018_paint_end.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP018_paint_end.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| CP018_paint_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP018_paint_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP018_paint_start.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP018_paint_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP018_paint_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| CP019_doors_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP019_doors_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP019_doors_start.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP019_doors_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP019_doors_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 4.38 | PASS |
| CP019_dray_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP019_dray_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.02 | PASS |
| CP019_dray_start.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP019_dray_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 35 | 35.0 | PASS |
| CP019_dray_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.23 | PASS |
| CP020_floor_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP020_floor_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | -0.12 | PASS |
| CP020_floor_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP020_floor_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP020_floor_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.37 | PASS |
| CP020_gaps_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP020_gaps_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | -0.12 | PASS |
| CP020_gaps_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP020_gaps_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 50 | 50.0 | PASS |
| CP020_gaps_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.37 | PASS |
| CP020_sweep_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP020_sweep_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP020_sweep_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP020_sweep_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 50 | 50.0 | PASS |
| CP020_sweep_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| FT.fountain | fountain absent (FT02) |  | removed (FT02) | PASS |
| FT.paint | painted, half-painted and primed members all present |  | {'painted': 479, 'half': 8, 'primer': 313} | PASS |
| FT.painters | painters on ladders and cradles |  | [14, 2, 6] | PASS |
| FT.crates | crates/cases arriving (dray, skids, trucks, stacks) |  | [13, 9, 12] | PASS |
| FT.floor | unboarded patch: Muse floor tiles + loose boards |  | [18, {'unboarded_patch_ft': [84.0, 132.0, -36.0, 36.0], 'loose_boards': 32}] | PASS |
| FT.sweep | sweeping machine + sprinkler hand-engine present |  | [True, True] | PASS |
| FT.exhibits | no exhibits installed (FT01) |  |  | PASS |
| FILE.size | round .blend under 90 MB | < 90 MB | 18.5 | PASS |
