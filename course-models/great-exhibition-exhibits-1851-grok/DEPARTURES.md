# DEPARTURES — hero exhibits (Grok Bot)
Grades: **A** = documented, **B** = derived from a surviving object / close analogue, **C** = staged for camera, **I** = interpretive.

| id | grade | departure / judgment call | why |
|---|---|---|---|
| EX01 | — | CP024 machine = **Nasmyth steam hammer** (Official Catalogue Class 6 no. 236), not Applegath's vertical press | A surviving c.1851–56 Nasmyth hammer (Smithsonian NMAH) gives real proportions; the ram's blow reads instantly on camera; Applegath's press survives only in engravings and its many-cylinder drum would be invented detail. |
| EX02 | B | Koh-i-Noor sized 1.55 × 1.30 × 0.68 in → ~186 ct by volume (3.52 g/cm³), pre-recut Mughal form (flat table, irregular facets), IOR 2.417 | 186 1/16 ct is the documented 1851 weight; exact pre-1852 geometry is from the later plaster casts/descriptions, so facet layout is approximate. |
| EX03 | I | Gilded "bird-cage" (32 bars, bell dome, gilt crown), glass bell over the stone, velvet stand, draped Chubb iron safe as pedestal, brass rail R 6.5 ft, policeman | From ILN 17 & 31 May 1851 and the Illustrated Exhibitor ("great parrot-cage", stone lowered into a safe at night). No measured drawing survives: bar count, radius and crown are interpretive. |
| EX04 | I | Osler candelabrum arm layout (8 lower + 6 upper + 1 top = 15 lights), festoon drops | Catalogue gives height 8 ft, 15 lights, prism shaft >3 ft only; arm arrangement follows Osler's general 1850s style. The originals (a pair, the Queen's) stood in the Central North Gallery — only one is built, on the preview dais. |
| EX05 | B | Hammer frame: base 14 × 6 ft, ~19 ft, raked double standards, separate anvil, entablature + cylinder | NMAH example proportions; the exhibited 1851 machine's own dimensions not found. Sole-plate arrangement interpretive. |
| EX06 | C | Stroke 3.5 ft; blow cycle lift 14 / hold 4 / fall 6 frames, 4 blows per 96 | Staged for a readable loop; real hammers ran faster/slower by valve setting. |
| EX07 | I | Dark green-grey machine paint | No colour record for the exhibit. |
| EX08 | C | No hot forging piece on the anvil (cold dies) | Exhibit machinery in the Hall was mostly shown running without work; avoids inventing glow/fire. |
| EX09 | C | Showroom stand (boards, Paxton column lines, Osler dais, crimson drape behind Osler) is a **preview stand only**, not a location claim | Assets ship standalone; the drape lets cut glass read against something other than sky. |
| EX10 | — | July crimson enclosure with gas jets around the Koh-i-Noor (added after complaints it did not sparkle) **not built** | e01 shows the May/June cage state. Proposed as a variant. The tiny, dull look of the stone in CP025_case is therefore period-correct (visitors complained of it). |
| EX11 | C | Placement test: Koh-i-Noor (96,0, main avenue east of the transept) + Osler (108,-22) in the transept r10 east block-outs (x ≤ 144); hammer at (-456,4) in Claude's west nave | Test only, to prove the assets drop in. Real 1851 locations differ (Koh-i-Noor near the transept in the main avenue; Osler in the gallery; the hammer in the NW machinery court) — not modelled in either host. Clash check reports intersecting host objects; `--hide-clash` hides only loose crowd figures standing in the footprint at render time (4 for the Koh-i-Noor); props/statues/machines are never hidden, so spots were chosen clear of them (K43 statue at x 120, locomotive at x 72–84). `--clear-sightlines` also hides loose crowd figures within 2.5 ft of a camera→asset sightline (the r10 avenue crowd is dense). Hosts are never saved (md5 checked before/after). |
| EX12 | C | CP024_ram pulled back 15 → 25 ft, EX_osler pulled back to 28 ft; ram rendered at f015 (top of lift) and f025 (on the die) | Preview showed a confusing tight crop and a cut-off candelabrum foot. |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| EX20 | Crystal glass sparkle (coat + faint emission); 6-sided prism drops and festoon cones | Osler candelabrum flat glass | B |
