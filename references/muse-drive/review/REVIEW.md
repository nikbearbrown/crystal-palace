# Crystal Palace research review

Prepared for **Nik Bear Brown**, 24 October 2026. Scope: **both Hyde Park in 1851 and Sydenham from 1854, including the move and rebuilding**.

[Open the offline research gallery](index.html) · [Model and film recommendations](MODEL-AND-FILM-PLAN.md) · [76-reference shortlist](shortlist.csv) · [Download audit](audit-summary.json)

## What is now available

The live Muse Drive research collection has been copied into this folder without changing the Drive originals. All **1,398 image/page files** match the live manifest's downloaded records and the Drive inventory. They total **2,109,175,319 bytes**. With the original README, 11 data files, three scraper source files and three original JP2 archives, the mirror contains **1,416 source files / 2,434,899,457 bytes**. Generated thumbnails, contact sheets, catalogue, OCR and this review are additional.

Every downloaded source file has a recorded SHA-256 and matches its Drive byte count. Raster image structure checks, SVG XML parsing, JSON parsing and ZIP CRC checks passed. There is one exact duplicate image pair, the two differently spelled `Destroyed/Destoyed_1936` files; both were retained to preserve source paths. Other visually similar reproductions are not necessarily byte duplicates.

All image/page files were screened through **35 contact sheets**. Selected plans, the 1856 dimension table and visitor details were examined at larger size. **40 selected pages/images** also have machine OCR; key passages were reviewed, but the OCR is not a checked transcription of every word. This is a collection-wide visual/metadata triage, not a claim to have read every book page or independently authenticated every caption. The two SVGs are interface icons and use placeholder thumbnails.

| Live image folder | Files | Reconstruction value |
|---|---:|---|
| `commons` | 345 | The hidden strength: 117 partial scans of the 1856 Sydenham guide, photographs, coloured prints and construction illustrations. Also substantial irrelevant material. |
| `main-article` | 31 | Useful overview, 1857 park plan, 1851 interiors, later history; includes two interface icons. |
| `downes-1852-working-drawings` | 209 | 187 page scans and 22 larger re-exports. Use the project's existing 28 original plates as the geometric authority. |
| `routledge-1851-guide` | 272 | Exhibit zoning plan, descriptions, visitor context, index; also advertisements and scan targets. |
| `tallis-history-v1` | 232 | Interior engravings, sculpture and decorative objects, historical text. |
| `tallis-history-v4` | 172 | Interior and object engravings, machinery and decorative details. |
| `new-york-crystal-palace` | 114 | Comparative history only; a separate building, excluded from London geometry. |
| `architectuul-crystal-palace` | 11 | Mixed-period visual leads, including a grounds map described as 1862. |
| `iln-1850` | 9 | Early designs, press illustrations and text; includes an unbuilt committee proposal. |
| `va-paxton-sketches` | 3 | Reproductions/context for Paxton's concept sheet, not three independent designs. |

The manifest contains **8,860 records**, but only 1,398 downloaded images: 7,380 records were skipped for the collector's budget, 56 for media type, and 26 for size. The empty `linked/` folder is consistent with that. The existing README's 32 main-article / 340 Commons breakdown is stale; the live inventory is 31 / 345. Its “529 drawings” figure is a keyword count, not a count of useful drawings.

## Most useful discoveries

**Hyde Park geometry:** the original Downes folio remains the strongest source. Its printed plans, sections and component details support a modular build with separate columns, girders, timber roof work, gutters, glazing, galleries and stairs. Existing [measurement notes](../../downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md) distinguish printed dimensions from measured checks and document OCR fraction errors.

**Hyde Park exhibit layout:** Routledge scan `p0007`, gallery **0726**, shows ground-floor and gallery zoning, national displays, machinery, refreshment areas and the central fountain. Pair this with Downes Plate I/II rather than treating an exhibit diagram as a survey. The Talbot-associated 1851 photographs and opposite nave views (**0169, 0170, 0177, 0181, 0184**) provide useful camera-matching evidence. Tallis and coloured exhibition prints provide object density, clothing, flags, foliage and decoration, with artistic interpretation kept visible.

**Sydenham floor plan:** gallery **0205**, `Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg`, is a **5,669 × 2,763** plan with named courts, objects, entrances, north/south wings and garden connections. The same guide includes a transverse section (**0212**) and court plans, including Egyptian and Alhambra layouts (**0226, 0246**). It is more useful for the rebuilt interiors than a general exterior photograph. The downloaded 117-image sequence is incomplete, ending at printed p.125; its bibliographic metadata describes a 197-page book with two maps, which are not both established as present.

**Direct before/after dimensions:** printed p.35, gallery **0214**, compares the two buildings. The values below were read from the image, not accepted from OCR. They are one contemporary source's reported measurements, requiring agreement with the correct plan and datum before serving as final model controls.

| Dimension | Hyde Park, reported in the 1856 guide | Sydenham, reported in the 1856 guide |
|---|---:|---:|
| Main building length | 1,848 ft | 1,608 ft |
| General width | 408 ft | 312 ft |
| Greatest width | 456 ft | 384 ft |
| Nave height above ground floor | 64 ft 9 in | 110 ft 3 in |
| Transept height above ground floor | 102 ft 2 in | 174 ft 3 in |

The Sydenham table separately gives **197 ft 10 in from the basement** for the central transept. Do not mix this with ground-floor height. Wing and colonnade lengths are separate from main-building length. The [JSON transcription](dimensions-from-1856-guide.json) includes metre conversions, source ID and qualification; it is a starting dataset, not an already validated model.

**The move:** the 1856 guide introduction, printed p.20 (**0198**), describes removal and dates the raising of the first Sydenham column to 5 August 1852. Printed pp.31–35 (**0210–0214**) describe the new roof, three transepts, site slope, basement and construction. Pages 33–34 claim reuse of the old materials except roof glass and transept-roof framing. Retain that as the guide's retrospective institutional claim; it is not an itemized inventory of surviving parts. The narrative is promotional and its paragraph ordering should not be mistaken for a precise chronological log.

**Film details beyond architecture:** printed pp.29–30 (**0208–0209**) describe arrival through the railway colonnade and contain a refreshment tariff with dining locations. These support an arrival shot, signs, menus, service spaces and everyday activity. The construction illustrations (**0174, 0330, 0332–0333, 0336–0338**) show glazing equipment, manufacturing, lifting ribs and floor testing. They establish illustrative construction methods; they do not document the exact sequence of the 1852–54 move.

## Corrections that matter for the model

1. **The Downes plate numbers are not interchangeable.** Muse's 22 large exports were selected by scan width and renamed sequentially. After 08, many numbers diverge from the printed folio. Printed IX, X, XX, XXa, XXIII and XXIV are absent from that large-export subset, although their ordinary page scans are present. The project's original 28 identified plates include them. See the complete [crosswalk](DOWNES-CROSSWALK.md). Keep filenames unchanged and translate the labels explicitly.
2. **Muse's `crystal-palace-facts.md` mixes or oversimplifies dimensions.** Its 128/168-foot height description should not become Hyde Park geometry. Its rectangular 77 × 19-module description obscures the distinction between the 408-foot main width and the 48-foot north addition over only part of the length. Use the source plans and record the datum for every height. The claim that 1,851 feet arose by confusing the year with the length is unsupported; do not repeat that explanation. The existing Downes notes instead distinguish column-centre dimensions from approximate overall length.
3. **A publication year is not the depicted year.** Dickinson plates published in 1854 can depict the Great Exhibition of 1851. The filename `Kristallpalast_Sydenham_1851_aussen.png` (**0598**) depicts Sydenham despite “1851” in its name. Its source description explicitly identifies the relocated building.
4. **Some convincing plans are for other buildings or rejected proposals.** `The_Crystal_Palace_page_16.jpg` (**0322**) is the French 1849 exhibition; page20a (**0323**) is Kroll's Wintergarten in Berlin; page22 (**0324**) is the committee design; page_xb (**0340**) is the Turner proposal. `iln-1850_04.jpg` (**0569**) is also a committee proposal. Gallery **0186** is described as an unexecuted design. Gallery **0128** has a questionable Hyde Park caption relative to its appearance and remains excluded from accepted geometry pending identification.
5. **The V&A files do not establish a separate acceptance telegram.** The images show concept-sheet reproductions and an album/context page. The collector's caption should be checked against the museum object record before the film tells a telegram story.
6. **Sydenham is not one frozen state.** The 1856 guide, 1857 park map, claimed 1862 map, later events, 1911 additions, wartime uses and 1936 ruins need distinct date labels. Modern terraces can inform surviving fabric, but not opening-day planting or finishes.

These corrections are separate from the preserved original Muse files. The catalogue's broad phase tags are editorial screening aids, not verified dates for every image. Book collections retain volume-level tags even on blanks or advertisements.

## What to keep separate

The converted [`crystal-palace-full.blend`](../../../crystal-palace-full.blend) is a usable native asset with packed maps, but its multiple vaulted masses and terraced setting resemble Sydenham. That is a visual inference, not a proven identification or dimensional validation. Do not use it to stand in for the 1851 building. The existing [Claude course model](../../../course-models/crystal-palace-1851-claude/README.md) is a separate, incomplete Hyde Park reconstruction grounded in Downes. The research now supports independent development of both, linked by a documented reuse/rebuilding sequence.

No Blender scene was changed during this research pass. The existing Blender-only model cleanup remains in effect. No FBX, MAX, DWG, 3DS or GLB was downloaded back into the project.

## Source preservation and omissions

- Original Drive source: [Muse collection](https://drive.google.com/drive/folders/1AjxbrohOVLdUEr50j3NQwci0TR0vrFM_). The complete recursive [Drive inventory](drive-inventory.json) includes files not mirrored.
- Mirrored all live images, data and scraper source files; scraper code was preserved, not executed.
- Downloaded the three full-resolution JP2 ZIPs for Tallis volumes 1 and 4 and Routledge's guide. They passed archive CRC checks. Downes' original ZIP already exists at `references/downes-1852/source-scans/jp2.zip`, so it was not duplicated. The New York original ZIP was inventoried but omitted; its 114 JPEG pages are available as comparative context.
- The three `research-muse/` bundles are older/redundant snapshots, not the live folder layout. The metadata and main-article bundles were inspected in temporary staging; the Commons bundle exceeded the connector's raw-file size limit. The live Commons images were downloaded individually instead. Those snapshot ZIPs were not added to the project.
- Original non-Blender model files and redundant `maps.zip` were skipped. Nothing was deleted from Drive. Low-value image hits remain in the mirror but are clearly separated in the catalogue so they cannot silently become geometric evidence.

## Attribution and publication

Per-file source record, Drive link, collector license field and SHA-256 are retained in the gallery/catalogue. Source metadata is not the same as verified attribution: the manifest does not consistently name the image creator, and some descriptions are truncated. Check the source's complete credit and terms when an image enters the final film. Do not treat the collector's “all pre-1929” sentence as blanket clearance for every reproduction or jurisdiction.

The museum overview [V&A: The Great Exhibition of 1851](https://www.vam.ac.uk/articles/the-great-exhibition-of-1851) is useful corroboration for the first exhibition. [Historic England's Crystal Palace Park entry](https://historicengland.org.uk/listing/the-list/list-entry/1000373) anchors the move and developing landscape. [Royal Collection's account of the 1855 royal visit](https://www.rct.uk/collection/stories/prince-albert-his-life-and-legacy/the-royal-and-imperial-visit-to-the-crystal-palace) helps distinguish the rebuilt cultural attraction. These were consulted as contextual checks, not substitutes for measured drawings.

A further lead, [Science Museum Group's “The New Crystal Palace at Sydenham”](https://collection.sciencemuseumgroup.org.uk/objects/co67641/engraving-the-new-crystal-palace-at-sydenham), includes an anticipated opening inscription and a museum date field. Record both rather than treating it as an as-built survey. Its displayed image terms are CC BY-NC-SA 4.0, illustrating why source-level reuse checks matter. This external lead was not downloaded into the Muse mirror.
