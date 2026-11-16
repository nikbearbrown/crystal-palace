# DEPARTURES — O-INDUSTRY + O-ROOM (London 1850)

| id | decision | why | grade |
|---|---|---|---|
| LN01 | Representative c.1850 railway lane: 8-arch brick viaduct, train, factory with 3 chimneys + smoke, 12 terraced fronts | CP002 mood board — industry that made the Palace possible. Composite, not a single documented street. | B |
| LN02 | Smoke as stacked translucent cylinders; haze via Nishita air/dust density | Staging for a sooty sky without a full volumetric sim. | C |
| LN03 | Planning room (28×22×12 ft Georgian) with commission table, chairs, fireplace, bookshelf | CP005: 1849–50 planning. Room is interpretive. | B |
| LN04 | Plan sheets as PIL-generated textures (nave plan, south elevation, gutter detail, OJ colour board), packed into the .blend | Readable stand-ins for Fox & Henderson / Paxton drawings. | C |
| LN05 | Samples on the table: glass pane, sash-bar length, short hollow column section | The three materials of the Palace. | A |
| LN06 | Industry at origin, room at x=300 ft in one .blend | Same pattern as Chatsworth (two sets, one file). | B |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| LN02 | Darker brick/soot/slate albedos; soot rear wall + brick wing walls inside each viaduct arch | Black arch voids; peachy brick | B |
| LN03 | Denser loco smoke plume (7 translucent stacks); dimmer hazy world | Train smoke thin/absent | B |
| LN04 | CP069 South Kensington ‘today’ block-out (`ln03_southken`): Exhibition Road + RAH dome amphitheatre + three museum front blocks (V&A / Science / NHM massing). **OPTIONAL** — real footage may replace | C | storyboard OFFSITE South Ken; institutional legacy of 1851 profits, not a claim every museum was built by the exhibition |
| LN05 | CP069 lean 28-sample / 1280×720; RAH is faceted ellipse rings not a surveyed survey | D | box busy; block-out only |

## Look — crystal-palace-look v1 (2026-10-27)
Shared grade from `/workspace/crystal-palace-survey/look/` (AgX Medium High Contrast, Nishita-family MULTIPLE_SCATTERING sky + haze, era white-balance, mid-grey exposure table, glass/white-iron albedo ceilings). Render scripts import via `cpl_look.py` and call `apply_look` before rendering. Hero tiles re-rendered lean (24 spp, 1280×720). See `look/README.md` for Sydenham adoption.

## ln03 w02 polish (2026-10-27)

| ID | Change | Why | Grade |
|---|---|---|---|
| LN06 | RAH: mosaic frieze strip, arched window recesses + iron mullions (3 floors × 36), SW iron balcony rail, glazed lantern ring + radial dome ribs | Prior massing was blank peach cylinder + faceted dome | C |
| LN07 | Museum blocks: iron window frames on street façades | Blank stone slabs | C |
| LN08 | Street: iron rails, lamps, bollards; multi-lobe tree canopies + iron tree-guard cages | Bare road / single-cone trees | C |

## ln03 w03 fix (2026-10-27)

| ID | Change | Why | Grade |
|---|---|---|---|
| LN09 | Exposure held ~−0.18; world strength 0.18 / sun 1.8 so street mean luminance tracks before (~0.73) | w02 after washed (mean ~0.90) | C |
| LN10 | RAH materials: deep BrickDeep, TerracottaBuff band, MosaicFrieze under cornice, darker DomeIronGlass + thick ribs; arched Kit.quad glazing + iron frames | Read as Royal Albert Hall, not blank peach cylinder / grey dashes | C |
| LN11 | Street trees: London-plane icosphere multi-lobe canopies + leaf noise (not tapered cones) | Cones read as low-poly placeholders | C |

## CP002 polish CANDIDATE 2026-11-16 — `rounds/candidates/ln03_cp002.blend` (NOT live; lead reviews pairs)
Built by `scripts/build_cp002_street.py` on top of live `rounds/ln02.blend` (unchanged). Camera `CP002_lane_start` not moved. Dated state: London, c.1850 — a representative railway lane, not a documented street; no named firm, factory or railway company. Hyde Park and Sydenham are not blended in. Sources: Historic England list entry 1253151 (L&G viaduct, Deptford–North Kent Jn: grey brick, arches 20 ft centre to centre, 22 ft high, parapets ~4 ft 6 in); Railway Wonders of the World, "London's First Railways" (878 arches, mostly 18 ft span, 22 ft high); Victorian Web via silverfoxstudios (851 semicircular arches; arches let as workshops and stores).

| ID | Change | Why / source | Grade |
|---|---|---|---|
| D-LN-CP002-01 | Viaduct rebuilt to the London & Greenwich pattern: semicircular arches 20 ft c/c, 18 ft clear span, 22 ft to crown (springing 13 ft), stone imposts + plinths, two-ring gauged-brick voussoirs, stone string course at 24 ft, brick parapets to 28.5 ft + coping, 17 bays (x −110…230 ft), end abutment; ballast + two tracks inside. Was 8 bays at 16 ft c/c with tall elliptical rings that read as pointed/Gothic, 28 ft deck. **Width kept at 12 ft** (L&G ~25 ft) so the CP002_factory / CP002_terrace eyes stay outside the masonry; the deck width cannot be seen from CP002_lane. | HE 1253151; RWW. | B |
| D-LN-CP002-02 | Arches let as workshops (timber-boarded screens, ledged-and-braced double doors, strap hinges, small-pane windows, boarded tympana with fanlights), a smithy (open front, dark interior, glowing hearth, hood, anvil, cart wheels at the door), a stable (half doors) and a brick-infilled store; three bays left open as through passages to the terrace lane. Sign boards are blank. | L&G arches were let commercially from the start. Arrangement interpretive. | B/I |
| D-LN-CP002-03 | Procedural materials: London stock brick coursed from world position (9 × 3 in brick + ⅜ in joint), soot streaks running down from the coping, ground-level grime, per-brick scatter, mortar bump; gauged red arch rings; granite setts (~4 × 9 in) with mud in the joints; York-stone flags; granite kerbs; tarred / painted boarding. | Replaces flat peach brick and a beige mud plane. Texture-free, not photographic. | C |
| D-LN-CP002-04 | Street: 34 ft setted carriageway between a 4 ft pavement against the viaduct and a far pavement; the CP002_lane eye now stands in the carriageway (5.25 ft over the setts, so check_set's eye-height rule still passes, 29/29). North lane: setts + terrace pavement. | Representative 1850 London street section. | B |
| D-LN-CP002-05 | 11 cast-iron gas-lamp columns (~9 ft to the ladder bar, square tapered glazed lanterns, ~12.5 ft overall), unlit (daytime; faint warm glass). | Standard London column lamp of the period; spacing representative. | B |
| D-LN-CP002-06 | Horse traffic: two ~16-hand draught horses (ellipsoid/tube bodies, collar + hames, bridle with blinkers, traces, breeching) in four-wheel drays loaded with barrels. The near dray is half-turned toward the camera. | "Horse traffic" brief; anatomy is a stand-in, not a measured horse. | C |
| D-LN-CP002-07 | Train: an 1847–50 2-2-2 express engine of Jenny Lind type (6 ft single drivers with splashers, 4 ft carrying wheels, tall chimney, brass haycock firebox + dome, **no cab, weatherboard only**), a four-wheel tender, four three-compartment four-wheel carriages, luggage under tarpaulin on the first roof; generic dark green / brown, no company livery. Moved along the viaduct so the engine shows over the parapet in CP002_lane (top right). | Period-correct for 1850; cabs came later. | B/I |
| D-LN-CP002-08 | Terrace rebuilt as a continuous two-up two-down row (13 houses, 14 ft frontage, 19 ft eaves, pitched slate roofs, party-wall stacks with pots, 6-over-6 sashes with sills and gauged lintels, panelled doors with fanlights, stone steps); the old block was 12 detached boxes with 2 ft gaps that crossed the factory. Factory replaced by a 5-storey, 62 ft brick mill with iron-framed small-pane windows on all faces, engine/boiler house, and 6 tapering chimneys 105–160 ft (two near, four on the skyline), plus 17 massing blocks as a distant town and a warehouse closing the north-lane view. | Typical c.1850 mill and chimney heights; not a named works. | B |
| D-LN-CP002-09 | People: 17 modelled 1850 street figures, using `scripts/cp002_figures.py` (vendored from Grok's KEEP'd CP009 builder `c9_figures_v2.py`) plus a new `build_woman()` (fitted bodice, full ankle-length skirt over petticoats — **no crinoline cage, which dates from 1856** — shawl crossed at the front, coal-scuttle bonnet or shawl hood, apron, basket). The cast: a gentleman in frock coat and top hat, clerks, navvies, coal-heavers, a costermonger with a barrow, a carter in a smock-frock at the horse's head, and women. The names avoid people_lib's figure prefixes, so the render-time v3.4 swap leaves them alone (it skips close-ups anyway, leaving any proxy as a lathe doll). | "Period-dressed people". Faces are generic, hands are mittens, poses are stiff. | C |
| D-LN-CP002-10 | The ln02 world, sun and exposure (−0.10, AgX Medium High Contrast) are **unchanged** and both sides use the same render recipe (enhance_offsite_materials + render_views `--keep-lighting`, era 1840s, 1280×720, 28 spp). Under this light a 0.3 albedo renders near-white (the live peach viaduct), so the new surface albedos are scaled (×0.63) to read as sooted stock brick and tarred timber. Result: CP002_lane luma 151.2 → ~135 (≈ −11%): the after is a little darker on purpose, and the exposure is identical. | Matched-exposure pair. | C |
| D-LN-CP002-11 | Volumetric coal smoke from the mill and skyline chimneys and the house stacks; loco steam trails back over the carriage roofs; a thin warm-grey smog volume (0.0028 m⁻¹) over the industry set only (x ≤ 268 ft; the CP005 room at 286–314 ft is outside it). The smog ignores shadow rays, so the authored sunlight is not dimmed. | Smoky 1850 air. Most plumes sit above the CP002_lane frame (the camera looks at the viaduct face); they show in the factory/terrace views. | C |
| D-LN-CP002-12 | `LN_Fireplace` (CP005 room) tagged `part_kind=ornament` in the candidate only. people_lib's name rule (`_FIRE`) was swapping it at render time for a 1930s fireman who stood at the object's origin (0,0,0), i.e. inside a CP002 viaduct arch. In the live ln02 pipeline the room fireplace is also lost the same way; it is out of shot in CP005_room/table, and those renders are unchanged apart from people-swap noise. | Bug fix needed for the new open arch. | A |
