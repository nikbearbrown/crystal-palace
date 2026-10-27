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
