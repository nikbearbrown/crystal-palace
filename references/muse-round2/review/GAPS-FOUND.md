# Muse round 2 — GAPS FOUND

Collection round for the Crystal Palace film: missing scene images (Section A), Sydenham plans (Section B, highest priority), and better versions noted (Section C). Everything below is on branch `muse-round2`, written only under `references/muse-round2/`. Hyde Park 1851 and Sydenham 1854–1936 are kept strictly apart throughout; a file is Sydenham unless its line says Hyde Park.

## Summary

**Start-here checks.** `references/muse-drive/review/REVIEW.md` exists and was read in full (including "Corrections that matter" and "What to keep separate" — both are respected below). `references/muse-drive/data/manifest.csv` exists (8,860 records); round 2's `manifest.csv` uses its exact column set (`title, local_path, section, source_pages, original_url, width, height, bytes, mime, license, license_url, description, status`). First-round images actually found under `references/muse-drive/images/`: **1,398 blobs** (1,395 with image extensions; 3 are truncated long Rijksmuseum filenames) — the brief's figure of 1,398 checks out. The dimensions file exists at `references/muse-drive/review/dimensions-from-1856-guide.json` (Sydenham and Hyde Park figures from printed p.35 of the 1856 guide). **`scenes.json` and `TIMELINE.md` were NOT found anywhere in the repository tree (3,198 entries searched) — there is no `youtube/` directory.** Scene IDs below therefore follow the S-numbers in the round-2 brief itself; if the scene list lives outside the repo, the mapping should be checked against it.

**Found.** 123 files downloaded, 381.9 MB total, every file under the 50 MB cap, round total well under the 1 GB cap. The single biggest win: **the 1856 guide is now complete** — the 73 Commons page scans round 1 lacked (everything after printed p.125) are downloaded, including the "Plan of Palace and Park" fold-out and the book's last page (printed p.197). Also found: an opening-year (1854) ground plan of palace and gardens printed in the Illustrated London News; Samuel Phillips's 1854 guide's annexed routes map, frontispiece and title page; a second contemporary source for the Sydenham dimensions (Phillips 1854) whose figures **do not match** the 1856 guide's — see Contradictions; the Punch page (13 July 1850) in which the name was actually coined; the ILN fire engraving and report for the 1866 north-transept fire; Delamotte / Negretti & Zambra photographs of the Sydenham building, the water towers and Hawkins's studio; period material for the dinosaurs, the Iguanodon dinner, the FA Cup finals, prices and fares, and the winter-garden campaign.

**Not found in any whitelisted open source searched by this pass** (full detail in "Scenes with nothing" below): period images of Fox Henderson's Smethwick works and Chance Brothers' glassworks (S15/S19); a Sydenham/Penge map earlier than the palace (S44); Brunel's water-tower drawings (S51); photographs of the 1940/1941 tower demolitions (S83); a period image of the Crystal Palace subway (S87, modern conservation photographs only); an 1851 printed admission tariff page (S34, 1854 fares page found instead). **Three of these gaps (S15, S19, S34) were filled by the parallel pass on this branch — see the note immediately below.**

**Three biggest surprises.**
1. **The two best contemporary dimension sources disagree.** Phillips's 1854 guide gives the Sydenham central transept as 168 ft to the top of the louvre and the nave arch crown as 104 ft; the 1856 guide's table gives 174 ft 3 in and 110 ft 3 in. The 168 ft figure matches the "~168 ft" that appears in later retellings — so the long-running transept-height conflict is not modern sloppiness; it starts with the Crystal Palace Company's own guides. Reported in Contradictions, not resolved.
2. **Phillips's 1854 guide has no building plan at all** — only a routes map. The best opening-year plan of the building itself turned up not in a guide but in a newspaper: the ILN's "Ground Plan of the Crystal Palace and Gardens at Sydenham", 17 June 1854.
3. **The name "Crystal Palace" was not coined by a cartoon.** The item is a prose letter in Punch (13 July 1850) written by Douglas Jerrold in the persona of "Mrs Amelia Mouser", describing a dream of "a palace of very crystal" — a week after Paxton's design was first published and before it was accepted.

Confidence key: **High** = the file is what the scene asks for, dated and licensed from source metadata and (where marked) visually verified. **Medium** = right subject, but small, loosely dated, or identified from catalogue text rather than inspection. **Low** = nearest available stand-in.

## A note on this branch — two collection passes

While this pass was being assembled, a **second, parallel Muse collection pass** was committing files one by one to this same branch (`muse-round2`) under different filenames. Nothing has been overwritten: the branch holds both sets. The parallel set (45 files at the time this note was written, still growing) is strong exactly where this pass was weak — it includes the V&A's 1851 season ticket No. 1 signed by Prince Albert (S34), the 1851 Official Catalogue's flooring and tariff pages (S25, S34), Fox, Henderson's 1849 bowstring-girder proof paper (S15), a Chance Brothers flint-glass disc of 1851 (S19), ILN construction reporting of 14 Dec 1850 (S13), a Phillips Alhambra court plan and Routledge dimension pages (Section B), and the Punch cartoon page (p.22) that follows the Mouser letter (S37). This pass's own `manifest.csv` covers only this pass's 123 files; the two manifests and reviews should be merged by whoever closes the round. Where the parallel files change a verdict below, the section says so.

## Section B — Sydenham plans (highest priority)

### B1 — The complete 1856 guide
**Found, complete.** Round 1 held 117 of the guide's 190 Commons page scans, ending at printed p.125. Round 2 downloads the remaining **73 pages** (`images/B1-guide1856-p<id>.jpg`, Polona / National Library of Poland scan via Wikimedia Commons, public domain; author Samuel Phillips; Crystal Palace Library, 1856; 197 pp. + 2 maps per the Polish catalogue record — the description confirms the brief's "197 pages plus two maps"). Identified pages include printed p.172 (Telescope Gallery), printed p.197 (Final Summary — the last page), and plates: Screen of the Kings and Queens of England; the Temple of Aboo Simbel; the Stone Arcade; View of Great Transept; and **The Secondary Island** (Hawkins's islands — cross-filed under S52 in the scene notes). One of the guide's two maps is among them: the **Plan of Palace and Park** (see plans table). The second map is believed to be the building ground plan already in round 1 (gallery 0205); the two sets should be collated on paper copies before the film locks its plan references. Confidence: **High** (visually verified).

### B2 — 1854 opening-year plans and handbooks
- **ILN ground plan, 17 June 1854** — `images/B2-iln-1854-ground-plan-palace-gardens.jpg`. "Ground Plan of the Crystal Palace and Gardens at Sydenham", printed p.581 of the opening report: the whole building (north transept present, wings, colonnade) plus the gardens layout. Public domain (ILN 1854, via Internet Archive). Confidence: **High** (visually verified).
- **Phillips, *Guide to the Crystal Palace and Park* (1854)** — the opening-year handbook by Samuel Phillips, "Illustrated by P. H. Delamotte". Downloaded: title page (`images/B2-phillips1854-title-page.jpg`), frontispiece view (`images/B2-phillips1854-frontispiece.jpg`), annexed **routes map** (`images/B2-phillips1854-routes-map.jpg`), the fares page (under S34) and the dimensions page (under B5). Note: this guide contains **no building ground plan** — the annexed map shows routes from London only. Scan: Internet Archive `guidetocrystalpa00phil_0` (Getty Research Institute copy). Public domain. Confidence: **High**.
- **Routledge's *Guide to the Crystal Palace and Park at Sydenham* (1854)** — located on IA (`routledgesguidet00grou`) and text-checked; it corroborates Phillips's 68 ft springing height but no plan page was extracted this round. Noted for a future pass.

### B3 — Grounds, terraces, fountains, geological islands
- **Plan of Palace and Park (1856 guide fold-out)** — `images/B1-guide1856-p147900658.jpg` (2,9xx px wide; full resolution in file). Keyed plan of the entire site: palace and wings, terraces, gardens, the two lakes, geological islands (lower left), the railway and station, roads to Sydenham and Dulwich. Public domain. Confidence: **High** (visually verified).
- **ILN 1854 ground plan** (above) also shows the gardens as laid out for the opening. Confidence: **High**.
- **The Secondary Island plate (1856 guide)** shows the islands as the guide presented them. Confidence: **High**.
- Round 1 already holds an 1857 park plan and the 1854 Delamotte photographs of the Water Temple; no separate 1854–57 terrace/fountain engineering plan was found in the whitelisted sources.

### B4 — Railway arrival; north transept before/after the 1866 fire
- Railway arrival: the **1856 Plan of Palace and Park** and the **ILN 1854 plan** both draw the colonnade, wings and the London & Brighton Railway; Phillips's routes map shows the rail approach from London. Round 1's 1856-guide pp.29–30 (gallery 0208–0209) describe the colonnade arrival in text. Confidence: **High** for the plan evidence.
- North transept for marking the 1866 loss: the **ILN 1854 plan** and the **1856 Plan of Palace and Park** both show the building **with** its north transept (pre-fire state). A post-fire plan (showing the shortened building) was **not found** in the whitelisted sources this round — the later guides and OS editions that would show it are not openly digitised in the places searched. The ILN fire engraving (S67) shows what was lost.

### B5 — A second dated source for the heights
**Found: Samuel Phillips's guide (1854), "Account of the building"** — page downloaded as `images/B5-phillips1854-dimensions-page.jpg`. Phillips gives, for Sydenham: main building 1,608 ft long (agrees with 1856), wings 574 ft each, colonnade 720 ft; nave 72 ft wide, arch springing 68 ft, **crown of arch 104 ft**; central transept 384 × 120 ft, **168 ft from floor to top of louvre**, 108 ft to the springing, **208 ft from the garden front to the top of the louvre**. The 1856 guide's p.35 table (round 1, gallery 0214; JSON in round 1) gives instead: nave height 110 ft 3 in, transept height 174 ft 3 in, transept from basement 197 ft 10 in. The two sources agree on lengths and disagree on every height — see Contradictions. Routledge's 1854 guide repeats the 68 ft springing, a partial third witness. Confidence: **High** that both texts say what is reported here (Phillips page visually verified; figures read from the book's own text).

## Section A — Scene gaps

### S03 — Chatsworth: Great Conservatory and the great lily
1. `images/S03-lily-chatsworth-iln-1849.jpg` — ILN, 17 Nov 1849: the Victoria regia in flower at Chatsworth, the period image of Paxton's lily house triumph. Public domain. 1409×949. Confidence: **High**.
2. `images/S03-victoria-regia-fitch-1851.jpg` — Walter Hood Fitch's 1851 lithograph of the expanded flower, 5955×4307. Public domain. Confidence: **High**.
3. `images/S03-chatsworth-great-conservatory-19c.jpg` — the Great Conservatory in a 19th-century photograph (attr. Charles Latham). Public domain but small (1035×611). Confidence: **Medium**. No period interior engraving of the conservatory was found in the whitelisted sources.

### S04 — Britain about 1850: industry and its other face
1. `images/S04-opening-liverpool-manchester-railway-1830.jpg` — Isaac Shaw's print of the opening of the Liverpool & Manchester Railway, 1830 (Yale Center for British Art, CC0). Confidence: **High**.
2. `images/S04-murray-mills-manchester-baines-1835.png` — A. & G. Murray's Manchester cotton mills from Baines (1835). Public domain; small (711×487). Confidence: **Medium**.
3. `images/S04-court-for-king-cholera-1852.jpg` — John Leech, "A Court for King Cholera", Punch 1852: the poverty image — a crowded poor London court. CC BY 4.0 (Wellcome Collection). 3755×2806. Confidence: **High**.

### S05 — Portraits and the road to 1849
1. `images/S05-prince-albert-1848.jpg` — Prince Albert, portrait dated 1848. Public domain. Confidence: **High**.
2. `images/S05-henry-cole-portrait.jpg` — Henry Cole. Public domain but only 227×332 — a place-holder; the frontispiece portrait in Vol. I of *Fifty Years of Public Work of Sir Henry Cole* (IA `cu31924098820628` is Vol. II) is the better version to extract. Confidence: **Low** (size only).
3. `images/S05-paxton-portrait-oakley-c1850.jpg` — Joseph Paxton by Octavius Oakley, c.1850. Public domain. Confidence: **High**.
4. `images/S05-society-of-arts-adelphi.jpg` — the Society of Arts building, John Street, Adelphi (19th-century engraving). Public domain; small (460×620). Confidence: **Medium**.
5. `images/S05-paris-1849-exposition-building.jpg` and `images/S05-paris-1849-exposition-entrance.jpg` — the **French** 1849 exposition building on the Champs-Élysées (the predecessor London answered), prints of 1849. Public domain. Confidence: **High**. Note: a plate of this same building sits in round 1 mislabelled among Crystal Palace plans (REVIEW.md correction 4) — it belongs to this scene, as the comparison, not to the London building.

### S13 — Hyde Park, summer 1850: the first works (Hyde Park building)
From Berlyn & Fowler, *The Crystal Palace, its Architectural History and Constructive Marvels* (1851) — the contemporary construction account, written from inside the works (IA `crystalpalaceits00berl`, public domain; this scan is modest resolution, ~1000 px pages):
1. `images/S13-berlyn-1851-frame-erection-plate.jpg` — iron frame bays under erection with derrick crane. Confidence: **Medium-High**.
2. `images/S13-berlyn-1851-works-view-plate.jpg` — view along the building under construction with workmen. Confidence: **Medium-High**.
3. `images/S13-berlyn-1851-hyde-park-ground-plan.jpg` — the book's general ground plan plate of the Hyde Park building (useful cross-check against the Downes plates in round 1). Confidence: **Medium**.
Round 1 already holds ILN 1850 site coverage; Berlyn is the strongest single construction source found.

### S15 / S19 — Smethwick: Fox Henderson's works and Chance Brothers' glassworks
This pass found **no period view of either works** in the sources it searched (see "Scenes with nothing") — **but the parallel pass on this branch found the documentary core of both scenes**: `images/S15-fox-henderson-bowstring-proof-1849.jpg` and `images/S15-fox-henderson-bowstring-title-1849.jpg` (Fox, Henderson's 1849 bowstring-girder proof — the girder system proved for the building), and `images/S19-chance-flint-glass-disc-1851.jpg` with `images/S19-iln-1852-chance-reference.jpg` (Chance Brothers' glass for the palace). Rank those first for the two scenes; what neither pass found is a period *view of the works buildings themselves*. Modern CC photographs of the surviving Chance works in Smethwick exist on Commons and were left undownloaded by this pass as they are not period evidence.

### S25 — The 1851 timber floor with the gaps between the boards (Hyde Park building)
1. `images/S25-berlyn-1851-floor-description.jpg` — Berlyn (1851), the description page: the ground floor "is laid with an interval of half an inch between the boards, to allow the passage of dust" (the gallery floor, by contrast, had iron tongues between the boards). This is the contemporary written evidence the scene asks for. Public domain. Confidence: **High** (text read and verified).
2. `images/S25-berlyn-1851-gallery-floor-test.jpg` — Berlyn engravings: "Testing the Gallery Floor" (a floor bay load-tested by workmen) and the boiler house. Confidence: **Medium-High**.
3. Sydenham cross-check: Phillips 1854 (the B5 dimensions page) describes the Sydenham floor the same way — boards 1½ in thick "with half-inch openings between them", "as in the old building". No drawing that isolates the slatted floor itself was found; the Downes plates in round 1 show the floor structure in section.
4. Parallel pass, same branch: `images/S25-01-official-catalogue-1851-introduction-p62-flooring.jpg` and `images/S25-02-…-p63-flooring-conclusion.jpg` — the 1851 Official Catalogue introduction's own flooring account, the natural companion to Berlyn above.

### S34 — What it cost to get in: tariffs, shilling days, tickets
**Best items are the parallel pass's** (already on this branch): `images/S34-01-va-season-ticket-no1-signed-albert-1851.jpg` (the V&A's season ticket No. 1, signed by Prince Albert) with its case exterior, and the 1851 Official Catalogue introduction pages on season-ticket prices and the shilling-days tariff (`images/S34-03-…jpg`, `images/S34-04-…jpg`). From this pass:
1. `images/S34-phillips1854-fares-page.jpg` — Phillips (1854), "Conveyance by Rail and Road from London": Brighton Railway return fares to the Palace including admission on most days — 2s 6d first class, 2s second, 1s 6d third — with season-ticket arrangements. Public domain. Confidence: **High** (visually verified).
2. Round 1 already holds the 1856 guide's refreshment tariff pages (gallery 0208–0209) and the Routledge 1851 guide scans (visitor context).

### S37 — Punch gives the building its name
1. `images/S37-punch-1850-07-13-mouser-page21.jpg` — Punch, Vol. XIX, p.21 (issue of 13 July 1850): Douglas Jerrold writing as "Mrs Amelia Mouser" describes her dream of the exhibition housed in "a palace of very crystal" — the coinage itself, a week after Paxton's design was published and before it was accepted. Public domain (IA `sim_punch_1850_19_0`). Confidence: **High** (passage located in the volume text and the page downloaded).
2. `images/S37-punch-1850-08-24-glass-houses-page81.jpg` — Punch, Vol. XIX, p.81 (24 Aug 1850): "Glass Houses of Parliament", the open letter to Paxton that kept the glass-palace idea in circulation all summer. Public domain. Confidence: **High**.
Corrective note: the naming item is a prose letter, not a cartoon; later retellings that credit "a Punch cartoon" are wrong about the form, though right about the magazine and the month.

### S41 — The winter garden: Paxton's plan for the afterlife (Hyde Park building)
1. `images/S41-medical-mans-plea-winter-garden-1851.jpg` — opening page of *A Medical Man's Plea for a Winter Garden in the Crystal Palace* (1851; RCP Edinburgh copy via IA `b28042517`): a campaign pamphlet for keeping the building as a winter garden, summarising Paxton's own proposal to dispose the interior "into an Arcadia of his own imagining". Public domain. Confidence: **High** as evidence of the 1851–52 campaign. Paxton's own pamphlet (*What is to become of the Crystal Palace?*, 1851) exists in print; no openly licensed scan of its pages was extracted this round.

### S44 — Sydenham and Norwood before the palace
**Nothing pre-1852 found** — see "Scenes with nothing". What round 2 does add for the site story: the 1854 routes map (B2) and the 1856 Plan of Palace and Park (B3), and round 1 holds an 1857 park plan. The 1840s mapping of Penge Common (parish tithe maps, c.1843) is held by London Metropolitan Archives and is not openly digitised in the sources searched; no Ordnance Survey coverage of the area predates the palace (the first OS surveys here are 1860s, post-palace).

### S45 / S46 / S47 — Taking it down, moving it, building it again (1852)
1. `images/S45-removal-pamphlet-title.jpg` — title page of *The Removal of the Crystal Palace* (Houlston and Stoneman; V&A National Art Library copy, IA `EX.1851.161RemovalOfTheCrystalPalace`): the printed debate over removal and Sunday opening, 1851–52. Public domain. Confidence: **High** as a document of the removal fight; it is an argument pamphlet, not a dismantling record.
2. The Sydenham rebuilding itself is covered by the Delamotte construction photographs under S57 (1853–54) and the 1853 Negretti & Zambra interior. ILN dismantling engravings of 1852 exist in the bound volumes on IA but were not isolated this round; the 1854 Crystal Palace Company prospectus was not found in the whitelisted sources. Round 1 found none either — the gap is narrowed (pamphlet + rebuilding photographs) but the 1852 taking-down itself remains unillustrated here.

### S51 — Brunel's two water towers (Sydenham)
1. `images/S51-south-tower-water-temple-1854.jpg` — south transept and the south water tower from the Water Temple, Delamotte / Negretti & Zambra, 1854. Public domain. Confidence: **High**.
2. `images/S51-north-tower-south-wing-1854.jpg` — centre transept and the north water tower from the south wing, 1854. Public domain. Confidence: **High**. Together these do the scene's "towers against the building for height" work: both towers were over 280 ft high and 46 ft in diameter (Historic England list entry 1469984 for the surviving south-tower base).
**Not found:** Brunel's drawings for the towers. No openly licensed copy exists in the whitelisted sources; the drawings live in the Brunel collections (Brunel Museum / Brunel Institute, Bristol). Attribution note for the film: the towers were designed by Brunel and built by Fox, Henderson & Co. in 1854–56, replacing a first pair of towers (1853, under the company's engineer Charles Wild) that were demolished as inadequate — sources that credit "Brunel's towers" without that history are compressing it.

### S52 — The prehistoric islands in period (Sydenham)
1. `images/S52-hawkins-studio-delamotte-1853.jpg` — Hawkins's Sydenham studio with the models under construction, photographed by Delamotte, 1853. Public domain. 3166×4134. Confidence: **High**.
2. `images/S52-dinosaurs-engraving-1854.jpg` — period engraving of the dinosaurs on their islands, 1854. Public domain; small (960×525). Confidence: **Medium-High**.
3. `images/S52-gartenlaube-1854-p106.jpg` and `images/S52-gartenlaube-1854-p107.jpg` — Die Gartenlaube's 1854 two-page spread on the geological islands. Public domain. Confidence: **Medium-High**.
4. Cross-reference: the 1856 guide's own **Secondary Island plate** (`images/B1-guide1856-p147900764.jpg`) — the islands as the Company's guide presented them in 1856. Confidence: **High**.
All period (1853–56); no modern photographs are offered for this scene.

### S53 — The dinner inside the Iguanodon, 31 December 1853 (Sydenham)
1. `images/S53-iguanodon-dinner-woodcut-1854.jpg` — the well-known woodcut of the banquet inside the Iguanodon mould: twenty-one guests, Hawkins at the head of the table inside the beast. Commons dates the print 1854; the dinner itself was New Year's Eve, 31 Dec 1853 (see Contradictions on the dating). Public domain. 1287×831. Confidence: **High**.
2. Context: the Hawkins studio photograph (S52) shows the same model under construction. No second, independent period record of the dinner (invitation card, menu, press drawing) was found in the whitelisted sources; the ILN's own report was text-only.

### S55 — The Sydenham opening, 10 June 1854
1. `images/S55-iln-1854-06-17-opening-arrival-p582.jpg` — ILN, 17 June 1854, p.582: "Opening of the Crystal Palace — Arrival of Her Majesty", engraving of the Queen's arrival for the 10 June ceremony, with the report text. Public domain. Confidence: **High** (visually verified).
2. `images/S55-iln-1854-06-17-opening-article.jpg` — the ILN opening article page, with the opening medal engraving. Public domain. Confidence: **High**.
3. `images/S55-state-visit-1855.jpg` — the palace ceremony photograph of April **1855** (Napoleon III, Queen Victoria, Empress Eugenie, Prince Albert). Included because it is the famous "royal group at Sydenham" photograph — but it is the French state visit a year later, **not** the opening; do not caption it as 1854. Public domain. Confidence: **High** (as an 1855 image).
Science Museum Group holds a large opening engraving ("The New Crystal Palace at Sydenham") under CC BY-NC-SA 4.0 — non-commercial terms; noted, not downloaded (see Section C).

### S57 — The rebuilt palace in its first years (Sydenham, 1850s)
1. `images/S57-progress-delamotte-met-109624.jpg` and `images/S57-progress-delamotte-met-109625.jpg` — Delamotte / Negretti construction photographs, 1854 (Met Museum, CC0, ~3900 px). Confidence: **High**.
2. `images/S57-interior-negretti-zambra-1853.jpg` — interior under construction, stereoscopic daguerreotype published by Negretti & Zambra, dated 1853 (Rijksmuseum, CC0). Confidence: **High**.
3. `images/S57-general-view-water-temple-1854.jpg` — general view from the Water Temple, Delamotte, 1854. Public domain. Confidence: **High**.
4. `images/S57-upper-gallery-delamotte-1852-54.jpg` — along the upper gallery, Delamotte, dated 1852–54 (Rijksmuseum, CC0). Confidence: **High**.
5. `images/S57-interior-stereo-1855-75.jpg` — stereoscopic interior, c.1855–75 (Rijksmuseum, CC0) — later than the ideal 1850s window at its far end; ranked last for that reason. Confidence: **Medium**.
Plus the two tower views under S51 (both Delamotte / Negretti & Zambra, 1854).

### S67 — The fire that took the north transept, 30 December 1866 (Sydenham)
1. `images/S67-iln-1867-01-05-fire-engraving.jpg` — ILN, 5 Jan 1867: engraving of the fire's aftermath — the burnt north transept interior seen from the transept, trees standing in the ruins. Public domain. Confidence: **High** (visually verified).
2. `images/S67-iln-1867-01-05-fire-report.jpg` — the same issue's full report, "Fire at the Crystal Palace". Public domain. Confidence: **High**.
Mark the loss on the pre-fire plans in B4; the building was never rebuilt to its full length afterwards.

### S70 — Cup finals at the Palace ground, 1895–1914 (Sydenham)
1. `images/S70-fa-cup-final-1913-programme.jpg` — programme cover of the 1913 final (Aston Villa v Sunderland), the final the scene singles out. Public domain. Confidence: **High**.
2. `images/S70-aston-villa-1913-postcard.jpg` — postcard of the Aston Villa cup-winning team, 1913 (Rotary Photographic Co.). Public domain. Confidence: **High**.
3. `images/S70-fa-cup-final-1901.jpg` — the 1901 final at the Palace ground, Tottenham v Sheffield United before 114,815. Public domain; small (504×336). Confidence: **Medium**.

### S83 — The towers come down, 1940/1941 (Sydenham)
**Nothing found** — see "Scenes with nothing". For the record: the north tower was demolished with high explosives on 16 April 1941 (it fell across the aquarium site); the south tower, close to houses, was taken down floor by floor in 1940–41 (Historic England, list entry 1469984; Lambeth planning heritage statements). Photographs of the 1941 demolition exist — a Surrey Archaeological Society bulletin (No. 321, 1998) reproduces the explosion photograph credited to Lambeth Archives — but no openly licensed copy is in the whitelisted sources. The south tower's base survives and is Grade II listed.

### S87 — The Crystal Palace subway (Sydenham)
1. `images/S87-subway-interior-2023.jpg` — the subway's vaulted interior during conservation/open days, 2023 (CC BY-SA 4.0, Doyle of London). Confidence: **High** as a conservation photograph.
No 1860s photograph or plan of the subway was found in the whitelisted sources; Historic England's listing material (the subway is Grade II*) is the authoritative modern record. The subway was built in 1865 to link the high-level station to the palace.

### S89 — The National Sports Centre, 1960s (Sydenham) — optional scene
1. `images/S89-national-sports-centre-2024.jpg` — the 1964 building photographed in 2024 (CC BY-SA 4.0). Confidence: **Medium** — right building, wrong decade; 1960s photography of the centre (e.g. John Maltby's) sits in the Historic England Archive and is not openly licensed in the sources searched.

## Sydenham plans table

| Plan / section | Year shown | Good for | Where / resolution |
|---|---|---|---|
| Plan of Palace and Park — fold-out in the 1856 guide | 1856 | Grounds, terraces, lakes, geological islands, railway and station, whole-site routes | `images/B1-guide1856-p147900658.jpg` (this round); ~2,950 px wide |
| Ground Plan of the Crystal Palace and Gardens — ILN | 1854 (opening) | Building footprint incl. north transept, wings, colonnade; gardens as opened; route/arrival | `images/B2-iln-1854-ground-plan-palace-gardens.jpg`; 4,113×5,936 |
| Annexed routes map — Phillips's guide | 1854 | Routes from London by rail and road; fares context (with S34 page) | `images/B2-phillips1854-routes-map.jpg`; ~2,100 px |
| Ground plan of the building — 1856 guide (round 1, gallery 0205) | 1856 | Room-by-room route through the building | Round 1; 5,669×2,763 |
| Transverse section — 1856 guide (round 1, gallery 0212) | 1856 | Heights as drawn in 1856 (compare B5 texts) | Round 1 |
| Court plans (Egyptian 0226, Alhambra 0246) — 1856 guide (round 1) | 1856 | Individual court layouts | Round 1 |
| Dimensions table, printed p.35 — 1856 guide (round 1, gallery 0214) | 1856 | Heights/lengths source #1 (JSON: `references/muse-drive/review/dimensions-from-1856-guide.json`) | Round 1 |
| "Account of the building" dimensions — Phillips's guide | 1854 | Heights/lengths source #2 — DISAGREES with 1856 on heights (see Contradictions) | `images/B5-phillips1854-dimensions-page.jpg`; ~2,100 px |
| General ground plan plate — Berlyn (Hyde Park building, NOT Sydenham) | 1851 | Hyde Park footprint cross-check only — never use for Sydenham | `images/S13-berlyn-1851-hyde-park-ground-plan.jpg` |
| Park plan (round 1, main-article set) | 1857 | Grounds a year after the guide | Round 1 |

No post-1866 plan (showing the shortened, north-transept-less building) and no pre-1852 site map were found in the whitelisted sources.

## Scenes with nothing (and where was searched)

- **S15 / S19 — a period VIEW of the Smethwick and Spon Lane works buildings.** Searched by this pass: Wikimedia Commons (text + categories), Internet Archive (Berlyn and Tallis texts read; no plates of either works), Wellcome. The parallel pass found the girder-proof and glass-disc documents (see S15/S19 section), but a period view of either works itself remains unfound in the open sources; the ILN's 1851 Smethwick coverage is the likeliest print source and is not openly digitised at plate quality.
- **S44 — Sydenham/Norwood before the palace.** Searched: Commons (map categories and text), IA map texts. Nothing dated before 1852 was found openly. The c.1843 Penge tithe map is at London Metropolitan Archives (not openly digitised); the first OS mapping of the area is 1860s, after the palace.
- **S51 (drawings only) — Brunel's tower drawings.** Searched: Commons, IA, Brunel Museum site. Drawings are held in the Brunel collections in Bristol; no open copy. The photographic half of the scene is fully covered (S51 above).
- **S83 — Tower demolitions 1940/1941.** Searched: Commons, IA, Historic England (list entry confirms dates and method; its archive photographs are not openly licensed), Surrey Archaeological Society bulletin (reproduces the 1941 explosion photo, © Lambeth Archives). Nothing openly licensed found.
- **S87 (period only) — the subway in the 1860s.** Searched: Commons, IA, Historic England. Only modern conservation photography is openly available (downloaded); no period photograph or plan found.
- **S41 (Paxton's own pamphlet pages).** The campaign pamphlet evidence is downloaded; Paxton's *What is to become of the Crystal Palace?* (1851) was located in print catalogues but no open scan was extracted this round.

## Contradictions (reported, not fixed)

1. **Sydenham heights — the Company's own guides disagree.** 1856 guide, printed p.35: nave height 110 ft 3 in; transept height 174 ft 3 in; transept from basement 197 ft 10 in. Phillips, 1854: nave arch crown 104 ft (springing 68 ft); central transept 168 ft to the top of the louvre, 108 ft to the springing, 208 ft from the garden front. Lengths agree exactly (1,608 ft; 384 ft transept). Both are contemporary, official-adjacent sources; the difference is partly datum (floor vs garden front vs basement) and partly — for the louvre figures, 168 vs 174 ft 3 in — unexplained. The film should either show both or pick one and say which. (The often-quoted "108 ft" for a transept turns out to be Phillips's Sydenham *springing* height — a plausible origin for several later confusions, including the Hyde Park figures flagged in round 1's REVIEW.)
2. **Opening date.** The documented opening is 10 June 1854 (Phillips's preface; ILN report of 17 June 1854). At least one later heritage text (Surrey Archaeological Society bulletin, 1998) says the palace "opened on June 18th 1854" — wrong, but in circulation.
3. **The Iguanodon dinner's image is dated 1854; the dinner was 31 Dec 1853.** The woodcut (S53) is a print *of* the event published the following year; captions should date the event 1853 and the print 1854.
4. **The 1855 state-visit photograph is not the opening.** The Napoleon III / Queen Victoria group (S55, item 3) is April 1855. It is routinely captioned elsewhere as the 1854 opening; it is not.
5. **"Crystal Palace Park – 1857.jpg" (Commons, also in round 1's orbit)** carries an upload date (2014) where a depicted date should be, and no source note; "1857" rests on the title alone. Use with care.
6. **Tower credit.** "Brunel's towers" compresses a two-step history: a first pair of towers (1853, company's engineer Charles Wild) was demolished as inadequate; Brunel's replacement pair was built 1854–56 by Fox, Henderson & Co. (Historic England, list entry 1469984).
7. **Round-1 wrong-building files (from REVIEW.md, restated because S05 now touches them):** the French 1849 exposition building, the Berlin Kroll Wintergarten and the unexecuted committee/Turner designs sit in round 1's plan folders. Round 2's two 1849 Paris prints (S05) are that same French building — wanted there as the predecessor, never as the London palace.

## Section C — Better versions noted, not downloaded

- **Crystal Palace from the air, c.1935** — ETH-Bibliothek photographs by Walter Mittelholzer (Commons, public domain, TIFF ~46.9 MB each): superb late views of the whole Sydenham site a year before the fire. Under the 50 MB cap but three near-identical frames; left for a decision on which single frame the film wants.
- **Crystal Palace, 1886** — Hallwyl Museum photograph (Commons, public domain, TIFF 45.9 MB): a fine garden-front view; a smaller Commons JPG derivative exists if wanted.
- **Henry Cole portrait** — the frontispiece of *Fifty Years of Public Work*, Vol. I (1884) would replace the 227×332 place-holder (S05).
- **The New Crystal Palace at Sydenham (opening engraving)** — Science Museum Group, CC BY-NC-SA 4.0: non-commercial terms make it unusable for most film purposes; recorded so nobody re-hunts it as "the missing opening picture" — the ILN engravings under S55 are public domain.
- **Negretti & Zambra / Delamotte stereoviews (Rijksmuseum, CC0)** — round 2 took five; the museum's Crystal Palace series runs to dozens more (sculpture courts, vestibules, nave statues) if later scenes need interiors.
- **Routledge's 1854 guide** — full text on IA; a plan-hunt through its plates is the obvious next pass if a third 1854 source is wanted.

## Round totals

This pass: 123 files in `references/muse-round2/images/` (104 via Wikimedia Commons, 19 page images via the Internet Archive), 381.9 MB in total; largest single file 14.1 MB; every file under the 50 MB cap; all licences public domain or CC0/CC BY/CC BY-SA as recorded per file in `manifest.csv`. SHA-256 for every file is in the manifest's description field. The parallel pass's files (45+ at writing) sit alongside under their own filenames; branch totals are therefore higher than the figures above and the two manifests should be merged when the round is closed. Nothing was written outside `references/muse-round2/`; nothing was merged to main.
