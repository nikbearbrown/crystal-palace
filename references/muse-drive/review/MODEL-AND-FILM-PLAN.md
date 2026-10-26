# Two buildings, the move, and the rebuilding

For Nik Bear Brown. This is an evidence-based production recommendation, not a completed film or a revised Blender model. Start with the [gallery](index.html) and [research review](REVIEW.md).

## Recommended model structure

Use separate native Blender scenes for `Hyde Park 1851` and `Sydenham 1854`, with an assembly scene for transition shots. Shared component libraries may connect the scenes, but similarity alone does not establish that an individual modeled component was physically reused. Keep proposed, measured and inferred geometry identifiable in object/collection metadata.

| Priority | Work | Evidence | Check before calling it faithful |
|---|---|---|---|
| 1 | Calibrate the Hyde Park skeleton and complete its missing extent | Original Downes plates I–VIII; existing control dimensions and Claude model | Footprint including north addition, 24-ft column grid, tier widths/heights, gallery voids and transept silhouette; compare camera-matched views to sources |
| 1 | Establish Sydenham footprint, roof and basement independently | 1856 plan 0205, section 0212, text 0210/0213, dimensions 0214 | Main building vs wings, one-to-three transept change, arched nave, ground-floor vs basement datum; don't uniformly scale the current mesh and assume completion |
| 1 | Audit the converted Blender model against the Sydenham evidence | Existing full-resolution scene plus dated exterior photographs 0074/0598 | Identify missing/extra bays and wings, choose a dated state, validate axes and scale before materials |
| 2 | Build editable repeated structural components | Downes VIII–XIV, XVIII–XXa, XXVII; plate crosswalk | Distinguish cast/wrought iron, timber, glass, gutters and mechanical louvers; keep repeated components instanced where practical |
| 2 | Reconstruct Hyde Park exhibition zoning | Routledge plan 0726; photographs 0169/0170/0181/0184 | Place national displays, machinery, central fountain and circulation against the plan, keeping the elms in the transept |
| 2 | Reconstruct selected Sydenham courts | 1856 plan 0205, court plans 0226/0246, Assyrian/Italian/Alhambra references 0012/0061/0108 | Treat the historical courts as a different exhibition programme from 1851; choose a limited set for detailed camera coverage |
| 2 | Add terrain, terraces and circulation | 1857 map 0591; later map 0008; source-dated photographs; modern remains as secondary checks | Separate topography from later planting, towers, paths, basins and alterations; establish which elements existed on the chosen date |
| 3 | Refine materials and dressing | Coloured prints 0312/0349/0584, photographs and component drawings | Do not assume that “metal” objects should shade as bare metal if painted; test glass thickness, roof transmission, framing and interior visibility under plausible daylight |
| 3 | Populate film-specific details | Tallis engravings, machinery 0316/1293, railway arrival 0208, tariff 0209 | Read object captions and time-specific placement; stage only what cameras require |

The [1856 dimension dataset](dimensions-from-1856-guide.json) preserves the printed values, metre conversion and datum. Its measurements are source statements, not independently validated mesh controls. Keep the existing Downes measurement work and the original source plates as the geometric reference for Hyde Park.

## Suggested film sequence

| Beat | Visual action | Starting evidence | Evidence boundary |
|---|---|---|---|
| 1. A temporary building takes shape | Paxton concept sheet leads into the modular grid; close-up of joint, gutter and glazing | 1395; Downes VIII–XIV | The sketch is conceptual; later construction details should not appear as if already on that sheet |
| 2. Hyde Park, 1851 | Exterior reveal, entry under the transept, tree canopy, fountain and crowded national exhibits | Downes elevations; 0726; 0181; 0312; 0584 | Mark renderings as reconstructions; paintings supply interpretive colour rather than exact measured finishes |
| 3. Dismantling and departure | Empty exhibition, selected modules disassembled, components moving between the two sites | 1856 introduction 0195/0198; component drawings | No verified complete transport route, manifest or day-by-day dismantling order in this review. Use a schematic site-to-site transition or clearly labeled inferred staging |
| 4. Rebuilding on a hill | New foundations and basement appear; reused component language develops into a larger, taller roof system and three transepts | 0210–0214; 0205 | Construction illustrations 0174/0336/0337 show methods at Hyde Park; they do not prove identical Sydenham equipment or sequence. Do not morph the two shells as if unchanged |
| 5. Sydenham opens | Approach via railway connection; reveal the courts and elevated garden frontage | 0208; 0205; court sources; dated early exterior evidence | Separate June 1854 opening from later completed landscaping. If a 1856 or 1857 state is shown, title it accordingly |
| 6. A new purpose | Contrast industrial exhibition with art, education and leisure; end on the two plans side by side | 1856 guide and source-matched models | A later-history epilogue is optional; keep 1911, wartime uses and 1936 destruction outside the opening-day reconstruction |

Do not fix film duration until the narration and selected story are approved for production. When film production is requested, use the existing `brutalist.art` toolkit and its current Blender/film skill, with the required project-owned reel, beat sheet, narration and verification workflow.

## Remaining evidence gaps, in order

1. **Opening-date Sydenham drawings and photographs:** the 1856 guide is strong early evidence, but not proof every illustrated element was complete in June 1854. Obtain dated as-built elevations/sections and resolve the construction state of towers, fountains, terraces and wings.
2. **The actual move:** locate contracts, dismantling records, transport accounts and construction photographs. The existing retrospective guide supports the event and a first-column date; it does not supply an audited reuse percentage or route.
3. **Survey alignment and terrain:** georeference the selected period's maps, establish north and level datums, and distinguish surviving terrace fabric from later interventions.
4. **Finishes:** corroborate paint placement, timber finish, glazing appearance and court colours with contemporary accounts and multiple images. Avoid sampling aged paper as literal material colour.
5. **Image credits:** complete author, institution, object number, source URL and required attribution for the actual film selections; keep the collector's rights labels as leads until checked.

## Next concrete milestone

Produce matched orthographic and perspective comparisons for **two calibrated shells**, with a separate list of measured, inferred and unresolved features. Then build the relocation sequence from shared modules and explicitly new Sydenham elements. This gives the film a defensible visual foundation before expensive detail and animation work.
