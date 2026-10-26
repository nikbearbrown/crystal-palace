# SAVE-STATE — Crystal Palace 1851 model session
_Updated 2026-10-18 after extending the west-half build to 888 ft._

## State

- **Current model file:** `/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851/model/crystal-palace-west-03_v001.blend`
- **Built:** lines 0:37 (west end to 888 ft, the transept west face), 7,757 parts
- **Regression hashes (all verified):**
  - 4:5 = 31d28a05cb53a430 (308 parts)
  - 0:6 = baa9ab74096de122 (1328 parts)
  - 0:12 = ede6c112ab6a9a58 (2580 parts)
  - 0:37 = af709609ae4364c6 (7757 parts)
- **Gate:** 25 gated controls PASS, 0 FAIL (D25, D26, D29 fixed with name-scoped selectors after multi-stair-bay expansion); 4 text-only reported; D28/D34 show large `info` measurements (not gated; will need name-scoping if ever promoted to gated)
- **Departures ledger:** `DEPARTURES-LEDGER.md`, 28 rows; rows 24–28 cover the extended plan
- **Review renders:** `model/previews/west03_v001_{section,iso,nave,gallery}.png`; 4 views in 61 s at 32 samples
- **Plate reading:** `tools/measure_plate_ii.py` records the full horizontal dim chain (west wall to east wall, 1848 ft); all readings plate-printed or plate-checked
- **Not built:** transept and vault, walls/louvres, north strip, west entrance and end wall, 6 east-half staircases, glazing, colour, east half of building
- **Next step (HANDOFF §1 complete):** Transept and vault (Plates XVIII, XX, XXIV–XXVI: 72 ft trusses, 74 ft 4 in vault ribs); controls D19a, D19b, D20 exist in controls.json and are skipped until those parts exist
