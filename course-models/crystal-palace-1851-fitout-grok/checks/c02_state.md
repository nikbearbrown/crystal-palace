# state checks: closing -- 15/15 pass

| id | check | target | measured | pass |
|---|---|---|---|---|
| CP029_dais_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP029_dais_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP029_dais_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP029_dais_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP029_dais_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| CP029_gallery_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP029_gallery_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 22.92 | 22.92 | PASS |
| CP029_gallery_start.roll | no roll (camera x-axis horizontal) | 0 | 0.0 | PASS |
| CP029_gallery_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 28 | 28.0 | PASS |
| CP029_gallery_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 4.17 | PASS |
| C.dais | dais, canopy and chair of state |  |  | PASS |
| C.crowd | ceremony crowd >= 500 floor + 150 gallery (added to the hp51 dressing) |  | [620, 260] | PASS |
| C.leaf | autumn leaf tint applied |  | autumn tint | PASS |
| C.dais_people | commissioners on the dais |  | 27 | PASS |
| FILE.size | round .blend under 90 MB | < 90 MB | 22.6 | PASS |
