# exhibit checks e02.blend

| id | result | check | detail |
|---|---|---|---|
| E01 | PASS | three asset collections present | missing [] |
| E02 | PASS | each asset carries title, status, credit and sources | [] |
| E03 | PASS | instance-ready: origin at floor centre (min z ~0, footprint centred), instance offset 0 | {"EXH_KOHINOOR": [0.0, 0.0, 0.0], "EXH_OSLER_CANDELABRUM": [0.0, 0.0, 0.0], "EXH_NASMYTH_HAMMER": [0.0, 0.0, -0.29]} |
| E04 | PASS | preview stand uses collection instances (same path as placement elsewhere) | 3 instances |
| E05 | PASS | collections marked as Blender assets | [True, True, True] |
| E06 | PASS | Koh-i-Noor sized for ~186 ct (pre-1852 cut) at diamond density 3.52 g/cm3 | 1.55 x 1.3 x 0.68 in -> ~186 ct |
| E07 | PASS | stone under the glass dome, inside the gilded bars, crown on the apex | cage z 3.09-7.38, crown top 8.27 ft |
| E08 | PASS | Koh-i-Noor visitors stay outside the rail | 8 visitors near, [] |
| E09 | PASS | Osler candelabrum: 8 ft high, 15 lights, prism shaft over 3 ft (Official Catalogue) | h 8.00 ft, 15 lights, shaft 3.38 ft |
| E10 | PASS | Nasmyth hammer at the NMAH proportions: base ~14 x 6 ft, ~19 ft high | 14.5 x 6.0 x 19.0 ft |
| E11 | PASS | ram animated: strikes the lower die (never through it), 3.5 ft stroke, repeated blows | z 2.95-6.45 ft |
| E12 | PASS | piston rod stays inside the cylinder through the stroke | rod top 14.40-17.90 ft vs cylinder 13.85-18.0 |
| E13 | PASS | anvil block separate from the standards (own foundation) | anvil x -2.1..2.1 |
| E14 | PASS | cameras at 5.25 ft eye height | 8 cams, bad [] |
| E15 | PASS | no roll | [] |
| E16 | PASS | lenses 28/35/50 only | {"CP024_approach_end": 35.0, "CP024_approach_start": 35.0, "CP024_ram_start": 50.0, "CP025_case_start": 50.0, "CP025_visitors_end": 35.0, "CP025_visitors_start": 35.0, "EX_lineup_start": 35.0, "EX_osler_start": 50.0} |
| E17 | PASS | cameras at least 1 ft from any mesh | [] |
| E18 | PASS | Hyde Park 1851 only, no Sydenham content |  |
| E19 | PASS | file under 90 MB | 0.7 MB |

19/19 pass
