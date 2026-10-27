# construction checks c07.blend

| id | result | check | detail |
|---|---|---|---|
| K01 | PASS | columns on Claude's 24 ft grid (x = -924 + 24 i ft) | 464 columns, 0 off grid |
| K02 | PASS | no columns in the 72 ft nave | 0 |
| K03 | PASS | fixed girder tops at 22'2" / 42'2" / 62'2" | 1110 girders, 0 bad |
| K04 | PASS | CP012 hoisted girder below its seat and under the sheer-leg apex | girder top 15.0 ft, apex 36.0 ft |
| K05 | PASS | D16 base plates from the Plate VIII printed set 2x1 .. 3x2 ft | 120 base pieces; sizes [(2.0, 1.0), (2.0, 1.5), (3.0, 1.5), (3.0, 2.0)] |
| K06 | PASS | D17 pads: thickness 1.25-3.48 ft, width 1.58-3.72 ft, top 1.2-2.1 ft below floor | 368 pads, 0 out of range |
| K07 | PASS | D17 trend: pads deeper under the inner (heavier) columns |  |
| K08 | PASS | base piece socket 3 3/4 in above floor (Plate VIII Fig. 1) | socket top 3.75-3.75 in |
| K09 | PASS | no bare column on grass/earth: standing columns only where bases are backfilled (x <= 708) | 0 |
| K10 | PASS | glazing wagons: wheels in the gutters, 8 ft gauge, deck over one ridge | 4 wagons, wheel spread 8.26-8.26 ft (outer faces) |
| K11 | PASS | sash bars at 10-10 3/4 in centres (> 10 in pane width; Plate XII 10 1/2 in) + 3 strong bars per 24 ft | 27 bars per slope per unit, 10.29 in centres |
| K21 | PASS | props appended from models/ are credited to their maker | 20 Muse crates |
| K22 | PASS | site hoarding ~8 ft high, south of the works (y < -290 ft) | 1 hoarding objects |
| K12 | PASS | worker stand-ins 5'4"-5'10" (standing) | 70 workers; standing heights 5.67-5.67 ft |
| K13 | PASS | lenses 28/35/50 mm on 36 mm sensor | 21 cameras |
| K14 | PASS | no roll | 0 |
| K15 | PASS | eye height 1.6 m (5.25 ft) above ground or the work-platform deck the camera stands on | all on ground or deck |
| K16 | PASS | camera clearance >= 1 ft from every object (never inside scaffold, girders, columns) | all clear |
| K17 | PASS | OFFSITE yard and detail sit >= 2000 ft from the building (never read as Hyde Park site) |  |
| K18 | PASS | CP014 section labelled | 7 labels |
| K19 | PASS | CP015 louvre opens/closes over frames 1-96 | 11 animated blades |
| K20 | PASS | Hyde Park 1851 only, no Sydenham content |  |
| K23 | PASS | spoil heaps sized to their pits (heap + carted = 1.25 x pit volume) | 86 heaps, 22976 of 26120 ft3 bulked on site (88 %) |
| K24 | PASS | carts and draught horses at the gate, standing on the ground | 5 carts, 5 horses |
| K25 | PASS | glaziers handle 49 x 10 in panes, held at ~30 deg | 8 panes, 4 held at 30 deg |
| K26 | PASS | closed crate variant built on Muse's frame in our file, credited | 12 closed crates |
| K27 | PASS | CP010 field spans the whole site (pegs -924..924 ft), north strip present, states progress pegged > dug > poured > base west to east | pegs x -924..924; field {'positions': 680, 'scale_markers': 14, 'pegged': 112, 'dug': 264, 'poured': 216, 'base': 88, 'pits_open': 568, 'heaps': 554, 'heaps_skipped': 14}; pads {'base': 88, 'poured': 216}; 32 north-strip pads |
| K28 | PASS | no columns stand in the foundation field (x < -36 ft) | 0 |
| K29 | PASS | CP012 horse haul: sheer-leg fall led through a ground snatch block to a horse on the ground | horse 26.0 ft from block |
| K30 | PASS | CP012 gin pole: upper-tier column hanging above its seat and below the pole head | column 24.6-43.0 ft, head 50 ft |
| K31 | PASS | CP013_layers sees more than one roof layer (glazed / bars / gutter) | {"gutter": 7, "glazed": 70, "bars": 42, "half": 26} |
| K32 | PASS | CP010 scale markers: a standing figure every 96 ft, clear of pits/heaps/props, most visible from CP010_extent | 14 markers x -708..540, gaps [96.0], clashes [], head visible 12/14 |

32/32 pass
