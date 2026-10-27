# state checks: dismantle -- 15/15 pass

| id | check | target | measured | pass |
|---|---|---|---|---|
| CP031_joint_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP031_joint_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP031_joint_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP031_joint_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 50 | 50.0 | PASS |
| CP031_joint_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| CP031_stacks_start.eye | eye height over its floor plane (gallery 22.92 / floor 0) | 5.25 ft | 5.25 | PASS |
| CP031_stacks_start.floorhit | surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed) | 0.0 | 0.01 | PASS |
| CP031_stacks_start.roll | no roll (camera x-axis horizontal) | 0 | -0.0 | PASS |
| CP031_stacks_start.lens | lens in grammar (28 interior / 35 approach / 50 detail) | 35 | 35.0 | PASS |
| CP031_stacks_start.clear | clearance to nearest mesh (82-ray sphere) | >= 1 ft | 5.24 | PASS |
| D.shores | temporary shores |  | 6 | PASS |
| D.stacks | component stacks |  | 5 | PASS |
| D.joint | hero joint present |  | hero end-plate with pins withdrawn | PASS |
| D.crew | dismantling crew |  | 8 | PASS |
| FILE.size | round .blend under 90 MB | < 90 MB | 17.6 | PASS |
