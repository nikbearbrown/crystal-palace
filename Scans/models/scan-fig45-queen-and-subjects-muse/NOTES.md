# NOTES — scan-fig45-queen-and-subjects (Muse version)

## Subject

The Punch cartoon **"The Queen and her subjects"** (*Punch*, 3 May 1851) — the print's own caption reads "Her Majesty, as She Appeared on the First of May, Surrounded by 'Horrible Conspirators and Assassins'" — modelled as a stage vignette: the **Queen** (deep teal crinoline, crimson sash, small crown) and **Prince Albert** (dark court dress, crimson sash, sword) at centre, the young **Princess** in white holding toward her mother and the **Prince** in jacket and kilt at his father's side; at right an elderly **courtier** in white hair bows deeply, leaning on a long staff; behind the party, a packed crowd of bonneted women with three top hats waved in the air and one tossed hat; above them all, an exhibition **gallery** — posts, diagonal braces, deck and railing — with a second row of onlookers and two small blank pennants.

This is the Muse version of the model for this catalog entry; it ships as `scan-fig45-queen-and-subjects-muse`.

## Scale — ESTIMATED

- **Basis:** the adult figures in the cartoon, taken as period-average heights. Modelled: Albert ≈ 1.78 m, the Queen ≈ 1.58 m (she was short; the print keeps her near Albert's shoulder), Princess ≈ 1.24 m, Prince ≈ 1.14 m, courtier ≈ 1.72 m.
- Resulting key dimensions: floor vignette 7.6 m × 4.2 m; gallery deck at 2.63 m, railing top ≈ 3.17 m, pennant tops ≈ 3.9 m.
- No dimension is confirmed by a measured source; treat all as estimated.

## Assumptions and interpretations

- **Single view:** the reference is one engraved cartoon. Backs and unseen sides of all figures and of the gallery are reasonable interpretations, never confirmed fact.
- **No likenesses:** the royal party are identified by dress, sashes, the small crown and the family grouping only. All figures are faceless stylised forms; the Queen's sash is worn as drawn (a plain crimson band, no order insignia), and the Prince's kilt is a plain dark-green skirt cone (no tartan pattern).
- **Crowd reduction:** the print's crowd is a solid mass of faces. The model uses ten simplified full figures in two rows plus nine busts on the gallery — a deliberate reduction, flagged here.
- The waved hats are held on raised arms rising from the crowd, and one hat hangs mid-air as drawn (it is a static part of the model).
- The gallery structure (posts, X-braces, deck, balustrade) is simplified from the print's upper band; the pennants are blank — no devices.
- The courtier's bow (about 52°) and his staff follow the print; his white fur collar is suggested by a pale ring at the neck.

## Build / technical

- Script: `build_scan_fig45_queen_and_subjects.py` (re-runnable, Blender 4.5.3, `bpy` only).
- Units: metres. Origin at base centre (floor centre, z = 0 at walking surface). Scale applied on all meshes.
- **Triangle count: 29,200** (evaluated count printed by the build; under the 50k budget — an earlier draft at 56,576 was rebuilt with simplified background crowd figures and lighter sphere tessellation).
- Preview: `preview.png`, Cycles CPU, 800 × 1024 (portrait, matching the print), neutral grey background, frontal view of the royal party with crowd and gallery behind, comparable to the reference.

## QC

- Preview viewed against the reference before finishing (three build iterations): the final view matches the print's arrangement — royal party centre (Queen crowned in teal with crimson sash, Albert beside her, Princess in white, Prince in his kilt), the white-haired courtier bowing deeply at right with his staff planted before him, two rows of bonneted crowd women behind with hats waved and one hat tossed in the air, and the railed gallery with its second row of onlookers and two blank pennants above. Defects found in earlier iterations and fixed: the first build exceeded the triangle budget (56,576) and was rebuilt with simplified crowd figures (28,696–29,200); Albert and the Prince were given dark hair caps (bare skin heads read as bald); the waved hats were lowered so they read as hats on raised arms rather than on poles; the tossed hat was moved in front of the gallery; the courtier was brought fully into frame with his staff beside his hands. Remaining known nits: the sashes read as strong vertical bands rather than pronounced diagonals at preview scale; the waved hats' arms are plain struts, as throughout this batch's figure style.

## Manual-review items

1. Royal-party identification rests on dress and grouping alone (no likenesses by design); confirm this reads acceptably.
2. Crowd density is a reduction of the print's massed faces — check it still reads as an adoring crowd at film distance.
3. Overall scale rests on estimated figure heights — no measured source exists in the catalog entry.
