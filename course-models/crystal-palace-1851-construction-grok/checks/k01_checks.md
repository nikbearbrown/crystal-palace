# checks: K-DRAIN k01 -- 19/19 pass

| id | check | target | measured | pass |
|---|---|---|---|---|
| CP014_drain_base_start.eye | eye 5.25 ft over the surface below (KD_Ground) | 5.25 ft | 5.25 | PASS |
| CP014_drain_base_start.roll | no roll | 0 | -0.0 | PASS |
| CP014_drain_base_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) and = route | 50 | 50.0 | PASS |
| CP014_drain_base_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.25 | PASS |
| CP014_drain_gutter_start.eye | eye 5.25 ft over the surface below (KD_Scaffold_board) | 5.25 ft | 5.25 | PASS |
| CP014_drain_gutter_start.roll | no roll | 0 | -0.0 | PASS |
| CP014_drain_gutter_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) and = route | 50 | 50.0 | PASS |
| CP014_drain_gutter_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 2.81 | PASS |
| CP014_drain_roof_start.diagram | diagram camera (labelled cutaway; eye grammar n/a), no roll |  | ORTHO | PASS |
| CP014_drain_whole_start.diagram | diagram camera (labelled cutaway; eye grammar n/a), no roll |  | ORTHO | PASS |
| KD.water | water strips along the whole path | >= 6 | 6 | PASS |
| KD.arrows | flow arrows | >= 8 | 13 | PASS |
| KD.labels | 3D text labels (whole + roof diagrams) | >= 12 | 21 | PASS |
| KD.paxton | Paxton gutters with rain channel + 2 condensation grooves | >= 2 | 2 | PASS |
| KD.sash | sash bars (10 in spacing) carrying condensation grooves | >= 40 | 64 | PASS |
| KD.path | water path falls monotonically ridge -> sewer (z never rises) | >= 1 | 1 | PASS |
| KD.column | hollow column shown cut (inner bore visible) | >= 1 | 1 | PASS |
| KD.figure | scale figure at the column foot | >= 1 | 1 | PASS |
| FILE.size | round .blend under 90 MB | < 90 MB | 0.2 | PASS |
