# Exterior checks x01: 29/29 pass

| id | check | target | measured | tol | pass | source |
|---|---|---|---|---|---|---|
| D01 | building length, end wall to end wall (column centrelines) | 1848.0 | 1848.0 | 1.0 | PASS | Downes D01, Plate I/IV: 1848 ft |
| D02a | tier-1 width between its outer side walls | 408 | 408.0 | 0.5 | PASS | Downes D02 / Plate III: 408 / 264 / 120 ft |
| D02aL | tier-1 side walls reach the end walls (x extent of wall-bay centres + 24) | 1848.0 | 1848.0 | 1.0 | PASS | tiers all 1848 ft long |
| D02b | tier-2 width between its outer side walls | 264 | 264.0 | 0.5 | PASS | Downes D02 / Plate III: 408 / 264 / 120 ft |
| D02bL | tier-2 side walls reach the end walls (x extent of wall-bay centres + 24) | 1848.0 | 1848.0 | 1.0 | PASS | tiers all 1848 ft long |
| D02c | tier-3 width between its outer side walls | 120 | 120.0 | 0.5 | PASS | Downes D02 / Plate III: 408 / 264 / 120 ft |
| D02cL | tier-3 side walls reach the end walls (x extent of wall-bay centres + 24) | 1848.0 | 1848.0 | 1.0 | PASS | tiers all 1848 ft long |
| D05a | north strip length (x extent of its north wall) | 936.0 | 936.4166 | 1.0 | PASS | CONTROL-DIMENSIONS D05 |
| D05b | north strip depth beyond the 408 ft block | 48.0 | 48.2083 | 0.6 | PASS | D05: 48 ft |
| D05c | north strip start x (216 ft west of the transept centre-line chain) | -708.0 | -708.2083 | 0.6 | PASS | north chain 216 + 936 + 696 |
| G01 | every column on Claude's 24 ft grid (max off-grid, ft) | 0.0 | 0.0 | 0.01 | PASS | x=-924+24i, y=-204+24j |
| G02 | no exterior column west of line 40 except the north strip | 0 | 0 | 0 | PASS | complementary to Claude (x <= -36) |
| G03 | no duplicate column positions | 614 | 614 | 0 | PASS |  |
| G04 | no column inside the 72 ft nave (|y| < 36) | 0 | 0 | 0 | PASS | Plate VI; EX02 |
| D11a | tier-1 girder top | 22.1667 | 22.1667 | 0.05 | PASS | controls D11 |
| D11b | tier-2 girder top | 42.1667 | 42.1667 | 0.05 | PASS | controls D11 |
| D11c | tier-3 girder top | 62.1667 | 62.1667 | 0.05 | PASS | controls D11 |
| D12 | east gallery floor top | 22.9167 | 22.9167 | 0.05 | PASS | controls D12 |
| W01 | full-height posts per 24 ft wall bay (iron-column ends + 2 timber posts at 8 ft, Plate XXI) | 4 | 4 | 0 | PASS | Plate XXI |
| E01 | east end wall incl. top louvre band reaches the tier-3 girder underside | 59.1667 | 58.9708 | 0.6 | PASS | Plate V |
| E02 | east end entrance doors (centre 3 bays + outer 2) | 5 | 5 | 0 | PASS | Plate V |
| S01 | east-half avenue staircases (mirrors of Claude's stair bays 8/17/26, N and S) | 6 | 6 | 0 | PASS | Plate II; Claude STAIR_BAYS |
| C_EXT_east_end_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.02 | 0.5 | PASS | storyboard v001 |
| C_EXT_int_east_nave_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.02 | 0.5 | PASS | storyboard v001 |
| C_EXT_NE_strip_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.02 | 0.5 | PASS | storyboard v001 |
| C_EXT_SE_34_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.02 | 0.5 | PASS | storyboard v001 |
| C_PLATE_IV_full_south_ortho_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.0 | 0.5 | PASS | storyboard v001 |
| C_PLATE_V_east_ortho_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.0 | 0.5 | PASS | storyboard v001 |
| C_REF_aerial_SE_start | camera: no roll (deg) + eye-height error (cm) unless review/ortho | 0.0 | 0.0 | 0.5 | PASS | storyboard v001 |
