# Muse round 2 — GAPS FOUND (merged draft)

**Status: DRAFT, local only (stage 21, 2026-10-26). Not pushed, not committed,
not merged to any branch.** This document is a NEW document. It does not
overwrite either of the two reviews it merges, and neither review, neither
manifest, the stage-9 draft, nor the stage-20 v1 manifest was edited to
produce it. Both source reviews are preserved: my review
(`final/references/muse-round2/review/GAPS-FOUND.md`, 1,133 lines, 71 files)
and the branch review (`build/fold/branch-gaps-found.md`, fetched read-only
from branch `muse-round2` head `80680bf30485c72656c49744688756ffc7b2d8a7`
in stage 18, 322 lines, covering 211 files).

**Base and method.** This draft takes the branch review as its base, per the
stage-18 recommendation: the branch review is already the merged record of
two parallel collection passes on the branch (Pass A: 89 files, 203 MB,
95-row manifest with 6 URL-only rows; Pass B: 123 files, 381.9 MB), and it
is fuller than my review on most scenes. My review's material is carried
over scene by scene below (the 28 mine-only claims from the stage-18
comparison are integrated, and a checklist of them follows the scene
sections so the carry-over can be audited). Scene sections cite filenames
as kept in the merged manifest v1 (`build/fold/MERGED-MANIFEST-V1.csv`,
244 rows, 238 unique file contents, 608,308,900 bytes); a filename cited
here is a v1 kept filename, and its v1 `local_path` is
`references/muse-round2/images/<filename>` (URL-only rows carry no file).
Where a source review cited a name that v1 drops as an alias, this draft
gives the kept filename and notes the alias name once, in the scene
section; the full 44-row alias table is `build/fold/ALIAS-TABLE.csv`
(38 shared-content branch names kept under my filenames, plus 6
branch-internal duplicate names).

**Provenance, stated honestly.** v1's SHA-256 values for the 167
branch-only contents were recomputed locally in stage 17 (167/167 match
the branch manifest's embedded claims), and v1's `what_it_shows` for those
contents comes from stage-19 visual verification of contact sheets
(high 147, medium 20, low 0). Creator and date_made for branch rows are
still carried verbatim from branch-manifest description prose: the 156
embedded creator values were NOT checked per row for the
author-vs-image-maker ambiguity (guide authors such as Samuel Phillips are
often recorded as creator for guide page scans), 13 rows have no creator
at all, and date_made values were NOT normalised or checked against
depicted dates. Do not cite a branch row's creator or date_made from this
draft as locally verified. Licence names are copied verbatim from the
source manifests; licence URLs in v1 are the canonical URL for the stated
standard licence where the source left the field blank, and blank where
the licence is not a standard licence. Nothing in this draft upgrades a
licence. The V&A-terms and licence-unclear position is stated explicitly
in its own section below and applies to every scene section.

**The two buildings, kept apart.** Hyde Park 1851 and Sydenham 1854–1936
are two different buildings throughout. A file is Sydenham unless its line
says Hyde Park. A publication year is not the depicted year. The New York
Crystal Palace and the Kroll Wintergarten (Berlin) are left out. No
Sydenham 3D is claimed or used anywhere in this review.

## Summary

**Start-here checks.** `references/muse-drive/review/REVIEW.md` exists and
was read in full by both source passes, including "Corrections that
matter" and "What to keep separate". `references/muse-drive/data/manifest.csv`
exists (8,860 records). First-round images under
`references/muse-drive/images/`: **1,398** (the branch review adds that 3
are truncated long Rijksmuseum filenames, so 1,395 carry image
extensions). The repo README's "1,393 images" figure is stale against
that count (see Contradictions, C11). The dimensions file exists at
`references/muse-drive/review/dimensions-from-1856-guide.json` (Sydenham
and Hyde Park figures from printed p.35 of the 1856 guide).
**`youtube/claude-liam-crystal-palace-story-walk/scenes.json` and
`TIMELINE.md` were NOT found anywhere in the repository tree; there is no
`youtube/` directory.** Scene IDs below therefore follow the S-numbers
in the round-2 brief. A separate storyboard draft, v001 (76 scenes,
CP001–CP076, 3,541 words, planning only), was received during round 2;
its CP IDs are independent of the S IDs, and the crosswalk appendix maps
the two lists.

**Found (merged set).** 238 unique file contents, 608,308,900 bytes
(~580.1 MiB), every file under the 50 MB cap, the round as a whole well
under the 1 GB cap. The single biggest win: **the 1856 guide is now
complete** — the 73 Commons page scans round 1 lacked (everything after
printed p.125) are in the set, including the "Plan of Palace and Park"
fold-out and the book's last page (printed p.197). Also found: an
opening-year (1854) ground plan of palace and gardens in the Illustrated
London News; Samuel Phillips's 1854 guide's annexed routes map,
frontispiece and title page; a second and a third contemporary source
for the Sydenham dimensions (Phillips 1854, Routledge 1854) whose figures
**do not match** the 1856 guide's — see Contradictions; the Punch page
(13 July 1850) in which the name was coined; the ILN fire engravings and
reports for the 1866 north-transept fire; Delamotte / Negretti & Zambra
photographs of the Sydenham building, the water towers and Hawkins's
studio; the ILN 30 October 1852 p.360 dismantling page the first-round
review said had not been found; the 1878 official guide's post-fire
ground plan; and period material for the dinosaurs, the Iguanodon
dinner, the FA Cup finals, prices and fares, and the winter-garden
campaign.

**Not found in any whitelisted open source searched by any pass** (full
detail in "Scenes with nothing usable" below): a period view of Fox,
Henderson's Smethwick works (S15); a period view of Chance Brothers'
glassworks buildings (S19); a Sydenham/Penge map earlier than the palace
(S44, site plan itself); Brunel's water-tower drawings (S51); photographs
of the 1940/1941 tower demolitions (S83); a period image of the Crystal
Palace subway (S87, modern conservation photographs only); a 1960s
National Sports Centre photograph (S89); a summer-1850 Hyde Park
first-works view (S13 — December 1850 works views only); a period
photograph of the completed prehistoric islands as a whole (S52); a 1913
FA Cup final match photograph (S70); an 1851 printed admission tariff
page as a file (S34 — the tariff is now evidenced by Catalogue pages,
and the V&A season tickets are held under V&A terms, see below).

**The four biggest surprises.**

1. **The dismantling evidence the first-round review said had not been
   found, was found — in one page.** The Illustrated London News of
   30 October 1852, p.360, carries "The last of the old Crystal Palace
   in Hyde Park" with engravings of the interior before removal and of
   the cleared site, and states the last column and girder had been
   "carried away in Mr. Younghusband's vans" to Sydenham. One file
   serves S45, S46 and S47.
2. **The heights disagreement starts with the Crystal Palace Company's
   own guides — and the gap is constant.** Phillips's 1854 guide gives
   the Sydenham central transept as 168 ft to the top of the louvre and
   the nave arch crown as 104 ft; the 1856 guide's table gives
   174 ft 3 in and 110 ft 3 in. Both gaps are exactly 6 ft 3 in. Routledge's
   1854 guide agrees with Phillips (104 ft; 168 ft 3½ in to the crown).
   The 168 ft figure matches the "~168 ft" in later retellings — so the
   long-running transept-height conflict is not modern sloppiness. Whether
   the constant gap is a datum difference is **suspected but unproven**:
   no 1856 text states a datum (see Contradictions, C1, disposition D4).
   The same trap recurs as a number: 384 ft is both the 1856 guide's
   greatest width and the 1854 text's central transept length — two
   different measures, same number.
3. **The brief's "Punch cartoon" is not a cartoon, and the name arrived
   as a phrase before it was a proper name.** The naming item is Douglas
   Jerrold's Mouser prose piece in Punch vol. XIX, p.21 (13 July 1850),
   describing a dream of "a palace of very crystal" — a week after
   Paxton's design was first published and before it was accepted. The
   same issue's p.22 holds a genuine Punch cartoon (a palm-house design
   "humbly submitted" to Prince Albert) that is explicitly NOT the
   naming item. A competing first-use date (2 November 1850) is in
   circulation and was not verified page by page.
4. **The 1854 plan question is genuinely unsettled, and the 1856 guide
   is now complete.** Phillips's 1854 guide as examined on IA
   (`guidetocrystalpa00phil_0`, Getty copy) contains no building ground
   plan — only a routes map — yet the merged set holds a fold-out
   ground plan attributed to Phillips 1854 (see Section B and
   Contradictions, C8, disposition D2). Do not cite that plan as
   "Phillips 1854" without the caveat. Separately, the 1856 guide's
   completion is now a fact of the set: all 73 skipped pages are held,
   and no additional folded map was found among them (stage-19 viewing).

Confidence key (as in both source reviews): **High** = the file is what
the scene asks for, dated and licensed from source metadata and (where
marked) visually verified. **Medium** = right subject, but small, loosely
dated, or identified from catalogue text rather than inspection.
**Low** = nearest available stand-in. Stage-19 viewing confidence
(high/medium) is recorded per branch row in v1's
`what_it_shows_confidence` column; my rows carry `my-manifest`.

## A note on the passes — three collections, one merged record

The branch review already merged two parallel passes (Pass A: 89 files,
203 MB, 95-row manifest with 6 URL-only rows; Pass B: 123 files,
381.9 MB) that used the same paperwork filenames, so Pass B's commit
overwrote Pass A's paperwork files at those paths. No image was lost:
both image sets are complete on the branch, Pass A's original manifest
and review survive in branch history (commits `5846260c` and `670cfe83`),
and the branch's merged manifest (217 rows in round 1's exact 13 columns,
with Pass A's creator/date_made/sha256 folded into `description` prose)
is the branch side of the stage-9 reconciliation. My review is a third,
independent pass (71 files, 104,375,188 bytes, 17-column manifest).
Stage 9 reconciled the three passes by content (git blob SHA, never
filename): 238 unique contents — 26 shared by my pass and the branch,
45 mine-only, 167 branch-only — plus 6 URL-only rows. Sixteen sources
were collected under two or three different filenames (twice by Pass A
itself in two cases); v1 keeps one filename per content, and the
44-row alias table preserves every dropped name with its section tag.
Build stages after both reviews then verified parts of the set against
original sources: stage 10 re-downloaded the S13, post-1866-plan and
S15 items from IA and visually verified them; stage 17 recomputed
SHA-256 locally for all 167 branch-only contents (167/167 match); stage
19 viewed all 167 branch-only contents via contact sheets and wrote
`what_it_shows` from what was seen. Where a build finding corrects a
source review, this draft says so and cites the stage; it does not
silently rewrite the source review's wording.

## Section B — Sydenham plans (highest priority)

### B1 — The complete 1856 guide
**Found, complete.** Round 1 held 117 of the guide's 190 Commons page
scans, ending at printed p.125. The merged set holds the remaining
73 pages (`B1-guide1856-p<id>.jpg`, Polona / National Library of Poland
scan via Wikimedia Commons, public domain; author Samuel Phillips;
Crystal Palace Library, 1856; 197 pp. + 2 maps per the Polish catalogue
record). Identified pages include printed p.172 (Telescope Gallery),
printed p.197 (Final Summary — the last page), and plates: Screen of
the Kings and Queens of England; the Temple of Aboo Simbel; the Stone
Arcade; View of Great Transept; and **The Secondary Island** (Hawkins's
islands — cross-filed under S52). One of the guide's two maps is among
them: the **Plan of Palace and Park** (see plans table). The second map
is believed to be the building ground plan already in round 1 (gallery
0205); the two sets should be collated on paper copies before the film
locks its plan references. Stage-19 viewing of the 70-file guide run
found it overwhelmingly text pages; the illustrated pages are the yak,
Cromwell statue, Screen of Kings and Queens elevation, Aboo Simbel
temple, transverse gallery interior, park/terrace engravings, Stone
Arcade, Labyrinthodon, Pterodactyl, and cherry trees plates. **No
additional folded map was found among them.** Confidence: **High**
(visually verified).

### B2 — 1854 opening-year plans and handbooks
- **ILN ground plan, 17 June 1854** — `B2-iln-1854-ground-plan-palace-gardens.jpg`.
  "Ground Plan of the Crystal Palace and Gardens at Sydenham", printed
  p.581 of the opening report: the whole building (north transept
  present, wings, colonnade) plus the gardens layout. Public domain
  (ILN 1854, via Internet Archive). Confidence: **High** (visually
  verified).
- **Phillips, *Guide to the Crystal Palace and Park* (1854)** — the
  opening-year handbook by Samuel Phillips, "Illustrated by P. H.
  Delamotte". Held: title page (`B2-phillips1854-title-page.jpg`),
  frontispiece view (`B2-phillips1854-frontispiece.jpg`, also filed
  under the alias `S66-view-1854-phillips-building-from-north.jpg`),
  annexed **routes map** (`1854-phillips-guide-railway-routes-map-leaf6.jpg`,
  aliases `B2-phillips1854-routes-map.jpg`,
  `PLAN-1854-phillips-routes-to-palace-map.jpg`,
  `S44-01-phillips-guide-1854-route-map-to-the-crystal-palace.jpg`),
  the fares page (under S34) and the dimensions page (under B5). Note:
  this guide as examined on IA contains **no building ground plan** —
  the annexed map shows routes from London only. Scan: Internet
  Archive `guidetocrystalpa00phil_0` (Getty Research Institute copy).
  Public domain. Confidence: **High**.
- **Fold-out ground plan attributed to Phillips 1854 — ATTRIBUTION
  DISPUTED, see Contradictions C8 (D2).** `S56-plan-1854-phillips-ground-plan.jpg`
  (4,227×2,169, key of courts 1–29 and statues A–Z), together with a
  Phillips Alhambra court plan (`PLAN-1854-phillips-alhambra-court-plan.jpg`).
  Stage 19 viewed the fold-out plan: **it IS a whole-building ground
  plan** with keyed courts, south wing entrance from the station, and
  north wing. That narrows D2 but does not close it: the mine-side
  finding was about the Delamotte-scan 1854 guides examined in round 2,
  and this file's source edition was not re-established in stage 19.
  Do not cite the plan as "Phillips 1854" without noting this.
- **Routledge's *Guide to the Crystal Palace and Park at Sydenham*
  (1854)** — located on IA (`routledgesguidet00grou`) and text-checked;
  it corroborates Phillips's 68 ft springing height, and its dimensions
  pages are held as files (under B5). No plan page was extracted from
  Routledge beyond the grounds fold-out below.

### B3 — Grounds, terraces, fountains, geological islands
- **Plan of Palace and Park (1856 guide fold-out)** —
  `1856-guide-147900658.jpg` (2,760×3,976; aliases
  `B1-guide1856-p147900658.jpg`, `S56-plan-1856-guide-palace-and-park.jpg`).
  Keyed plan of the entire site: palace and wings, terraces, gardens,
  the two lakes, geological islands (lower left), the railway and
  station, roads to Sydenham and Dulwich. Public domain. Confidence:
  **High** (visually verified). **Best route-drawing plan in the set.**
- **ILN 1854 ground plan** (above) also shows the gardens as laid out
  for the opening. Confidence: **High**.
- **The Secondary Island plate (1856 guide)** —
  `1856-guide-147900764.jpg` (2,976×1,902) — the islands as the guide
  presented them. Confidence: **High**.
- **Grounds fold-out, Routledge's guide (1854)** —
  `S62-plan-1854-routledge-grounds-terraces-islands.jpg` (2,407×1,734) —
  terraces, fountains, lakes, geological islands keyed; some features
  marked "not completed" — as projected, flagged in the source.
- **Grounds/neighbourhood map, c.1862** —
  `S62-plan-1862-crystal-palace-grounds-map.jpg` (2,020×2,896) — grounds
  in their neighbourhood context; mid-life park state. Round 1
  catalogued it but never downloaded it.
- Round 1 already holds an 1857 park plan and the 1854 Delamotte
  photographs of the Water Temple; no separate 1854–57 terrace/fountain
  engineering plan was found in the whitelisted sources.

### B4 — Railway arrival; north transept before/after the 1866 fire
- Railway arrival: the **1856 Plan of Palace and Park** and the **ILN
  1854 plan** both draw the colonnade, wings and the London & Brighton
  Railway; Phillips's routes map shows the rail approach from London.
  Round 1's 1856-guide pp.29–30 (gallery 0208–0209) describe the
  colonnade arrival in text. Confidence: **High** for the plan
  evidence. No standalone railway-arrival plan sheet exists (arrival is
  covered inside the plans above, plus Phillips's colonnade dimensions
  in text: 720 × 17 × 18 ft).
- North transept for marking the 1866 loss: the **ILN 1854 plan** and
  the **1856 Plan of Palace and Park** both show the building **with**
  its north transept (pre-fire state). A post-fire plan **was found**
  by the branch pass — the **1878 official guide's ground plan**
  (`S66-plan-1878-guide-ground-plan-post-fire.jpg`, 1,571×2,611),
  showing the shortened building with the north transept gone
  (Tropical End/Orangery) and both railway entrances labelled. No
  post-fire plan earlier than 1878 was found by any pass. The ILN fire
  engraving (S67) shows what was lost, and the ILN 12 January 1867
  p.42 plan marks the fire's extent directly.
- Dating guardrail: the 1856 plan and the 1854 map show ONLY the
  low-level railway (opened June 1854, 720 ft colonnade to the south
  wing). The High Level station opened 1 August 1865, so no 1854–1857
  plan can show both lines. Any plan showing both must be dated 1865
  or later. The OS Surrey Sheet 008 crop (below) is the surveyed
  sheet that does show both lines.

### B5 — Dated sources for the heights
**Three sources, two positions.** Phillips's guide (1854), "Account of
the building" — `B5-phillips1854-dimensions-page.jpg`: main building
1,608 ft long (agrees with 1856), wings 574 ft each, colonnade 720 ft;
nave 72 ft wide, arch springing 68 ft, **crown of arch 104 ft**; central
transept 384 × 120 ft, **168 ft from floor to top of louvre**, 108 ft to
the springing, **208 ft from the garden front to the top of the
louvre**. The 1856 guide's p.35 table (round 1, gallery 0214; JSON in
round 1) gives instead: nave height 110 ft 3 in, transept height
174 ft 3 in, transept from basement 197 ft 10 in. Routledge's 1854 guide
(pp.25–26 and p.125; `PLAN-1854-routledge-dimensions-p25.jpg`,
`PLAN-1854-routledge-dimensions-p26.jpg`,
`PLAN-1854-routledge-transept-height-p125.jpg`) gives the same arch
geometry as Phillips: nave crown **104 ft** by the same
springing-plus-radius reckoning, and central transept **168 ft 3½ in**
to the crown (176 ft 7½ in including the open louvre; 200 ft 2½ in from
garden-front ground, the basement floor lying 23 ft 7 in deep). The two
independent 1854 sources agree with each other and with the drawn
geometry, and the 1856 table runs a consistent ~6 ft higher on both
headline figures — a different datum is suspected, but no 1856 text
states one, so the conflict stays **unresolved** (C1, D4). Phillips is
internally inconsistent (his p.24 claim of a nave "44 ft higher" than
Hyde Park's matches neither his own 104 ft nor the 1856 figure) —
promotional rounding is at work in all three books. The 1854 text's
claim that the Sydenham nave crown (104 ft) is "just the height of the
transept at the old building" is a Hyde Park figure to keep separate
from Sydenham heights. **384 ft trap:** the 1856 table's "greatest
width 384 ft" (building width) and the 1854 text's "central transept
384 ft long" are the same number for two different measures — do not
equate them.

## Sydenham plans table (merged)

Round-1 files deliberately not re-downloaded are marked R1; their
resolutions are as reported in round 1. All other rows are v1 contents.

| Plan / section | Year it shows | Good for | Where / resolution |
|---|---|---|---|
| 1856 guide ground plan, Muse 0205 / `147900384` (R1) | 1856, pre-fire, three transepts | Route drawing inside the building, court layout | Round 1; 5,669 × 2,763 |
| Plan of Palace and Park — fold-out in the 1856 guide | 1856 | Grounds, terraces, lakes, geological islands, railway and station, whole-site routes | `1856-guide-147900658.jpg`; 2,760 × 3,976 |
| Ground Plan of the Crystal Palace and Gardens — ILN | 1854 (opening) | Building footprint incl. north transept, wings, colonnade; gardens as opened; route/arrival | `B2-iln-1854-ground-plan-palace-gardens.jpg`; 4,113 × 5,936 |
| Annexed routes map — Phillips's guide | 1854 | Routes from London by rail and road; fares context (with S34 page). Dashed West End & Crystal Palace Railway was proposed, not built. Scan rotated 90°; rotate clockwise to read | `1854-phillips-guide-railway-routes-map-leaf6.jpg`; 2,528 × 2,032 |
| Transverse section — 1856 guide (R1, gallery 0212) | 1856 | Heights as drawn in 1856 (compare B5 texts) | Round 1 |
| Court plans (Egyptian 0226, Alhambra 0246) — 1856 guide (R1) | 1856 | Individual court layouts | Round 1 |
| Dimensions table, printed p.35 — 1856 guide (R1, gallery 0214) | 1856 | Heights/lengths source #1 | Round 1 |
| "Account of the building" dimensions — Phillips's guide | 1854 | Heights/lengths source #2 — DISAGREES with 1856 on heights (C1) | `B5-phillips1854-dimensions-page.jpg`; ~2,100 px |
| Dimensions pages — Routledge's guide, pp.25–26 and p.125 | 1854 | Heights/lengths source #3 — agrees with Phillips against the 1856 table (C1) | `PLAN-1854-routledge-dimensions-p25.jpg`, `PLAN-1854-routledge-dimensions-p26.jpg`, `PLAN-1854-routledge-transept-height-p125.jpg` |
| General ground plan plate — Berlyn (Hyde Park building, NOT Sydenham) | 1851 | Hyde Park footprint cross-check only — never use for Sydenham | `S13-berlyn-1851-hyde-park-ground-plan.jpg` |
| Park plan (R1, main-article set) | 1857 | Grounds a year after the guide. "1857" rests on the Commons title alone; the file carries a 2014 upload date and no source note (C5) | Round 1; 1,483 × 1,896 |
| Fold-out ground plan — attributed to Phillips's guide (**attribution disputed**, C8/D2) | 1854, as opened | Route drawing with the fullest key (courts 1–29, statues A–Z); fire marking (north transept and north wing present); station entrance | `S56-plan-1854-phillips-ground-plan.jpg`; 4,227 × 2,169 |
| Grounds fold-out — Routledge's guide | 1854 (some features marked "not completed" — as projected) | Grounds, terraces, fountains and lakes; the clearest 1854 layout of the geological islands, animals keyed | `S62-plan-1854-routledge-grounds-terraces-islands.jpg`; 2,407 × 1,734 |
| Alhambra Court plan — attributed to Phillips's guide | 1854 | The court in its opening-year state (cf. round 1's 1856 printing) | `PLAN-1854-phillips-alhambra-court-plan.jpg` |
| "View of Building from the North" — Phillips frontispiece plate | 1854 | The north end **before** the fire — pairs with the 1878 post-fire plan | `B2-phillips1854-frontispiece.jpg`; 2,127 × 3,220 (alias `S66-view-1854-phillips-building-from-north.jpg`) |
| Map of the Crystal Palace grounds and neighbourhood | c.1862 | Grounds in their neighbourhood context; mid-life park state | `S62-plan-1862-crystal-palace-grounds-map.jpg`; 2,020 × 2,896 |
| Ground plan — official guide | **1878, post-fire** | Fire marking, the after-state: north transept gone, "Tropical End"/Orangery; the only plan labelling **both** railway entrances (High Level 1865 and the Brighton low-level line) | `S66-plan-1878-guide-ground-plan-post-fire.jpg`; 1,571 × 2,611 |
| Ordnance Survey Surrey Sheet 008 crop, Crystal Palace area | 1871–1882, post-fire | Post-fire footprint, terraces and fountains, High Level station and colonnade, Low Level line — the closest found to a both-lines plan on a surveyed sheet (district sheet, not a palace plan) | `os-surrey-sheet008-crystal-palace-area-1871-1882-crop.jpg`; 2,200 × 1,900 (crop of the 10,742 × 7,139 full sheet, pixels 4200,4400 to 6400,6300) |
| Ground plan marking the 1866 fire's extent, ILN 12 January 1867 p.42 | 1866 fire, published 1867 | Marking the 1866 loss on a contemporary plan; court index included | `s67-ground-plan-fire-extent-iln-1867-01-12-p42.jpg`; 2,068 × 2,952 |
| View of Great Transept, 1856 guide | 1856 | Transept elevation context (view, not dimensioned); terraces/fountains foreground | `1856-guide-147900716.jpg`; 2,946 × 2,127 |
| The Secondary Island, 1856 guide | 1856 | Geological islands: numbered key of Secondary island models | `1856-guide-147900764.jpg`; 2,976 × 1,902 |
| Festival of Empire 1911 Map (R1) | 1911, post-fire | Grounds in 1911: post-fire footprint, aquarium / North Tower Gardens area, Festival buildings | Round 1; 897 × 1,024 |

One post-1866 plan was found (1878, above); none earlier than 1878, and
no pre-1852 site map, was found in the whitelisted sources. Further
plan-level findings: no drawn **1854 section** exists in Phillips,
Routledge or the 1854 *Expositor* (the only Sydenham section remains
round 1's 1856 one); by 1856 the north transept was already partitioned
from the nave by "a gigantic curtain" (1856 guide, p.148 — the Tropical
End), so the 1856 state is not a fully open three-transept interior.
**Checked and rejected as Sydenham plans (so nobody re-searches them):**
`Crystal Palace - plan.jpg` on Commons is the HYDE PARK 1851 exhibition
plan — not Sydenham; `Crystal.Palace.Paxton.Plan.jpg` is Paxton Hyde Park
front/rear views; V&A Paxton sketches are Hyde Park 1850–51 designs;
Science Museum Group holds 1854 Sydenham views only, no plan (a "Plan of
the Crystal Palace and grounds, Sydenham" attributed to SMG on a
commercial print site was NOT downloaded — pursue it through SMG
directly and check the licence there if wanted); *The Builder*,
28 June 1856, Grand Fountain Basins plan was cited in later literature
but the journal volume was not extracted; the May 1864 map sold by the
Crystal Palace Foundation shop is commercial (excluded) and predates the
fire anyway.

## Section A — Scene gaps (merged, ranked best first within each scene)

### S03 — Chatsworth: Great Conservatory and the great lily
1. `victoria-regia-iln-1849.jpg` — ILN, 17 Nov 1849: the Victoria regia
   in flower at Chatsworth, the period image of Paxton's lily-house
   triumph (aliases `S03-lily-chatsworth-iln-1849.jpg`,
   `S03-gigantic-waterlily-in-flower-chatsworth-iln-1849.jpg`). Public
   domain, 1,409×949. Confidence: **High**.
2. `chatsworth-great-conservatory-19th-century.jpg` — the Great
   Conservatory in a 19th-century photograph (attr. Charles Latham),
   1,035×611 (aliases `S03-great-conservatory-chatsworth-19c-photo.jpg`,
   `S03-chatsworth-great-conservatory-19c.jpg`). Public domain.
   **High** that it depicts the conservatory, **medium** on period:
   exact year unknown, a later photograph of the same building, not an
   1836–1840 view. Do not caption it as contemporary with construction.
3. `hooker-victoria-regia-1851.jpg` — Hooker and Fitch *Victoria regia*
   plates, 1851 folio, 2,151×1,588. **High**.
4. `victoria-regia-entire-plant-1851.jpg` — Fitch plate 1, "Entire plant
   reduced", 1851, 760×584. **High** for the whole plant, leaf and flower.
5. `victoria-regia-expanded-flower-1851.jpg` — Fitch plate 3, "Expanded
   flower", 1851, 5,955×4,307 (alias `S03-victoria-regia-fitch-1851.jpg`).
   **High** for the flower; it does not show the leaf ribs — use it for
   the flower, not the leaf.
6. `S03-victoria-regia-house-chatsworth-1851.jpg` and
   `S03-victoria-regia-house-interior-chatsworth-1851.jpg` — Berlyn &
   Fowler 1851 engravings of the **Victoria Regia House** at Chatsworth,
   exterior and interior. Catalogued in round 1 but never actually
   downloaded until this round (branch Contradiction 20, carried as C20).
7. `S03-victoria-regia-leaf-underside-sharp-1854.jpg` — underside of a
   Victoria regia leaf, William Sharp chromolithograph, 1854, CC BY-SA
   4.0; this Commons copy is a modern Rawpixel enhancement — crop the
   modern caption band before use.
Not downloaded on purpose: modern Victoria amazonica photographs; a
Chatsworth lily-house interior was not isolated beyond item 6's interior
engraving. A Met CC0 "Chatsworth Conservatory" drawing was left out
because its subject could not be verified. No period interior engraving
of the Great Conservatory itself was found.

### S04 — Britain about 1850: industry and its other face
Balance image first, by design. The scene has no satisfactory c.1850
railway engraving; the dated items below are flagged honestly.
1. `king-cholera-1852.jpg` — John Leech, "A Court for King Cholera",
   Punch 1852 (aliases `S04-court-for-king-cholera-1852.jpg`,
   `S04-court-for-king-cholera-leech-1852.jpg`): the poverty image — a
   crowded poor London court. CC BY 4.0 (Wellcome), 3,755×2,806.
   Confidence: **High**.
2. `iln-panorama-london-thames-1845-1850.jpg` — ILN panorama of London
   and the Thames, 1845–1850, Public domain, 4,001×2,961. **High** for
   London around 1850.
3. `S04-britannia-bridge-tube-floating-1850.jpg` — Britannia Bridge tube
   floated into place, Hawkins lithograph, 1850, 6,862×5,531 — heavy
   railway engineering in the scene's own year. **High**.
4. `S04-manchester-from-kersal-moor-wyld-1852.jpg` — Manchester from
   Kersal Moor, Wyld, 1852, 1,000×656; the filename's "(1857)" is wrong
   — the painting is 1852.
5. `S04-opening-liverpool-manchester-railway-1830.jpg` — Isaac Shaw's
   print of the opening of the Liverpool & Manchester Railway, 1830
   (Yale Center for British Art, CC0). **High** as a railway document,
   dated 1830.
6. `S04-murray-mills-manchester-baines-1835.png` — A. & G. Murray's
   Manchester cotton mills from Baines (1835). Public domain, small
   (711×487). **Medium**.
7. `power-loom-weaving-wellcome.jpg` — Power-loom weaving, Wellcome,
   CC BY 4.0, 1,636×1,194, date **unknown** (no date in Commons metadata;
   Wellcome API returned none). **Medium**: unmistakably a power-loom
   mill scene, but do not caption it as an 1850s view until the Wellcome
   object record is checked.
8. `rainhill-bridge-bury-1831.jpg` — Rainhill Bridge, Bury's Liverpool
   and Manchester Railway, 1831, Public domain, 1,024×817. **Medium**
   for railway industry in general, **low** for "around 1850". Date
   trap: several Bury plates are titled 1831 but dated 1833 in Commons
   metadata; Rainhill is 1831 in both.
9. `S04-cotton-mule-spinning-1835.jpg` — cotton-mule factory floor,
   Ure, 1835 — fifteen years early; nothing closer to 1850 of comparable
   clarity exists in the allowed sources, and no British factory
   photograph of c.1850 was found anywhere.
10. `S04-rain-steam-and-speed-turner-1844.jpg` — *Rain, Steam and
    Speed*, Turner, 1844 — dated honestly as an artwork of 1844, not a
    document of 1850.
11. `coalbrookdale-by-night-1801.jpg` — Loutherbourg, Coalbrookdale by
    Night, 1801, Public domain, 1,207×770. **Medium** for industry,
    **low** for 1850 — it is 1801, fifty years early. Included only as
    the iconic ironworks-at-night image, flagged; never caption it as
    an 1850s view.
Searched: Commons, Wellcome API, round-1 manifest. Great Western Railway
engraving searches returned mostly 1881–1934 material. A further pass
could try ILN 1851 railway pages, Science Museum Group, and
Euston/Paddington 1850s views.

### S05 — Portraits, Society of Arts, 1849 Paris building
**Prince Albert:** `prince-albert-partridge-1840.jpg` (Partridge, 1840,
**high**); `prince-albert-1848.jpg` (1848, artist unnamed, **high** as a
likeness, medium on attribution; alias `S05-prince-albert-1848.jpg`);
`prince-albert-winterhalter-1845.jpg` (Winterhalter, Royal Collection
RCIN 404129, 1845, **high**); `S05-prince-albert-after-winterhalter-c1850.jpg`
(after Winterhalter, c.1845–50, Royal Collection). A lower-resolution
Winterhalter 1850 portrait (RCIN 402327) exists and was not downloaded.
**Joseph Paxton:** `paxton-oakley-c1850.jpg` (Oakley, c.1850, **high**,
alias `S05-paxton-portrait-oakley-c1850.jpg`);
`paxton-ellerby-c1843.jpg` (attributed to Ellerby, c.1843, 2,497×3,307,
**high** as a likeness, attribution flagged "attributed to",
highest-resolution Paxton portrait in the set; alias
`S05-joseph-paxton-ellerby-1843.jpg`); `paxton-iln-1865.jpg` (ILN, 1865,
**high** as a likeness, lower as a period portrait).
**Henry Cole:** `henry-cole-1852.jpg` ("Portrait of Henry Cole Esqr.,
executive commissioner", 1852, **high**; alias
`S05-henry-cole-executive-commissioner-1852.jpg`); backup
`henry-cole-vanity-fair-1871.jpg` (Pellegrini, Vanity Fair, 1871,
**high** as a likeness, **low** as a period portrait); placeholder
`S05-henry-cole-portrait.jpg` (227×332, **low**, size only — creator
blank in v1). The frontispiece portrait in Vol. I of *Fifty Years of
Public Work of Sir Henry Cole* is the better version to extract
(Section C).
**Society of Arts:** `society-of-arts-adelphi-1809.jpg` (Microcosm of
London Plate 71, Rowlandson and Pugin, July 1809, **high** — the
Society's own Adelphi rooms; the institution is the same as in 1850
even though the print is 1809); `S05-society-of-arts-adelphi-microcosm-1810.jpg`
(the 2,764×2,144 colour version dated 1810 — see C29/D6: keep the two
versions distinct, do not collapse them to one date);
`society-of-arts-distributing-awards.jpg` (18th-century engraving,
date broad 18th–19th century, **medium**);
`S05-society-of-arts-adelphi.jpg` (19th-century engraving, small
460×620, **medium**, creator blank in v1).
**1849 Paris exhibition building (the building itself, not a Crystal
Palace):** `paris-1849-birds-eye-qb726.jpg` (Paris Musées QB.726,
Quartley after Champin, CC0, **high** that it shows the 1849 Paris
buildings; print date unknown in Commons metadata — recorded as
unknown, not assumed 1849);
`paris-1849-horticulture-court-qb727.jpg` (Paris Musées QB.727, Bertrand
after Freeman, CC0, same date caveat, **high**);
`S05-paris-1849-exhibition-birdseye-carnavalet.jpg` (bird's-eye
engraving by Champin/Quartley, Musée Carnavalet, CC0, 3,000×2,525 — the
pictorial version of the plan held in round 1);
`S05-paris-1849-exposition-building.jpg` and
`S05-paris-1849-exposition-entrance.jpg` (prints of 1849, creator blank
in v1). Caption all of them as Paris, never as London. Note: a plate of
this same building sits in round 1 mislabelled among Crystal Palace
plans (REVIEW.md correction 4) — it belongs to this scene, as the
comparison, not to the London building.

### S13 — Hyde Park, summer 1850: the site as work began (Hyde Park building)
**CLOSED as a construction-view scene by the branch contents, with a
dating caveat — my review's "site context only" is superseded.** The
merged set holds December 1850 works views, not the summer start.
For the first works themselves — hoardings, setting-out, trenching,
foundations — no usable image was found: the parallel pass checked the
ILN issues of 21 Sept, 19 Oct, 2 Nov and 23 Nov 1850 on IA (design
articles and progress text only, no site-works plate before
14 December), and photography of the site begins with the finished
building in 1851.
1. `S13-iln-1850-12-14-raising-transept-ribs.jpg` — ILN, 14 Dec 1850,
   full-page plate "RAISING THE RIBS OF THE TRANSEPT ROOF" (p.453):
   a paired transept rib hoisted over the enclosed elm tree at the
   Hyde Park works. 4,088×6,168. **High** (stage 10 re-downloaded from
   IA and visually verified: Hyde Park construction, not Sydenham,
   not a design).
2. `S13-berlyn-1851-frame-erection-plate.jpg` — Berlyn & Fowler 1851,
   "General View of the Works in Progress": iron frame bays under
   erection with derrick crane, workmen, horse (landscape plate on a
   portrait page — rotate 90° to view). **High** (stage 10 visually
   verified).
3. `S13-iln-1850-12-14-visit-of-prince-albert-to-works.jpg` — ILN,
   14 Dec 1850, p.452: Prince Albert's visit to the works, with a pair
   of transept ribs being moved.
4. `S13-iln-1850-12-14-construction-account.jpg` — ILN, 14 Dec 1850,
   p.454, the construction account — contemporary text (24 ft column
   bays, three tiers) independently consistent with the Downes plates;
   included as a citation document.
5. `S13-berlyn-1851-hyde-park-ground-plan.jpg` — Berlyn's general
   ground plan plate of the Hyde Park building (useful cross-check
   against the Downes plates in round 1). **Medium**.
6. `S13-site-drawing-great-exhibition-competition-1850.jpg` — a
   competition site plan of the empty site, 1850 (a Dutch-lettered
   continental impression; a diagram, not a survey). **Medium**.
7. `elm-hyde-park-bm.jpg` — "Elm, in Hyde Park", tinted lithograph,
   British Museum, Edward Hassell, dated between 1837 and 1852,
   1,757×2,500. **Low–medium** for S13: Hyde Park with its old elms,
   the trees the design famously had to spare, but not the site as
   work began and not a construction view. Use only as "Hyde Park
   before the building" context, with its date range stated.
**FLAGGED — do not use as a construction view:**
`S13-berlyn-1851-works-view-plate.jpg` — the branch review describes
it as a "view along the building under construction with workmen".
Build stage 10 downloaded it from its IA source (Berlyn leaf 59) and
visually verified it as "View of Glass Roof from the Lead Flat" — a
completed, fully glazed roof with men on the lead flat, not frame
erection and not a construction view. Stage 19 confirmed this from the
merged set's copy (v1 `what_it_shows`, high confidence). It is Hyde
Park 1851 (not a wrong-building file), but it fails the S13
construction test. It remains available at its IA source if a
roof/finishing beat ever wants it. **The branch description prose for
this file still says the old wording in v1's `description` column;
v1's `what_it_shows` says the corrected wording. The merged review
follows `what_it_shows`.**
Date anchor (from a secondary source, not an image): the first iron
column was fixed 26 September 1850. Excluded leads: "Sappers and miners
working on the site" (after Gilbert) found only on Bridgeman Images
(commercial, excluded); ILN 6 July 1850 Paxton design engraving (a
design, not the site; Yale Library record, reuse terms unverified, not
downloaded).

### S15 / S19 — Smethwick: Fox, Henderson's works and Chance Brothers' glassworks
**S15 — documented, NOT closed as a works view.** No period view of
either works building was found in any allowed source. What the merged
set holds is the firm's own documentary core, and it must never be
captioned as a works view or photograph:
`S15-fox-henderson-bowstring-title-1849.jpg` — title page of Fox,
Henderson & Co.'s 1849 bowstring-girder proof pamphlet, imprint
"LONDON WORKS, NEAR BIRMINGHAM. MDCCCXLIX." (date visually verified
on the page itself, stage 10); `S15-fox-henderson-bowstring-proof-1849.jpg`
— printed p.16: proof trial of 6 September (1849), deflections observed
independently by E. A. Cowper and W. J. M. Rankine of Edinburgh. Both
Public domain (stage 10, from IA originals). The pamphlet proves the
firm's bow-string iron ribs by public load test two years before the
palace frame; it shows neither the works nor the works buildings.
Context for a card/text beat: the firm, formerly Brannah, Fox and Co.,
built the Crystal Palace's iron structure in 1851 at its London Works,
Smethwick, employing at peak around 2,000 people; the company closed in
1856 and the site was later Chamberlain and Nettlefold's, cleared in
2014 for the Midland Metropolitan University Hospital. **Do not
substitute a Chance Brothers works photograph for this scene — that is
a different firm.**
**S19 — four files plus a reference page, but no 1850s working view of
the works.**
1. `s19-chance-flint-glass-disc-1851.jpg` — Rijksmuseum RP-F-F25213-AG,
   CC0, 4,900×5,760 (alias `S19-chance-flint-glass-disc-1851.jpg`).
   **High** that it is Chance Brothers glass exhibited at the 1851
   Great Exhibition — but it is a product sample (a flint-glass disc
   for an astronomical telescope), not a view of the works. Best
   period artefact.
2. `S19-iln-1852-chance-reference.jpg` — ILN, 17 April 1852, p.301,
   naming L. Chance as "the manufacturer of the glass for the Crystal
   Palace" with his "two gigantic manufactories". **Medium**: stage-19
   viewing found the Chance connection **not legible at thumbnail
   scale** — do not cite it as confirmed Chance evidence on this stage
   alone.
3. `s19-chance-glassworks-canalside-2007.jpg` — photograph by Oosoom,
   16 June 2007, CC BY-SA 3.0, 2,592×1,636. **High** for the surviving
   works site at Spon Lane, Smethwick; surviving fabric, not an 1850s
   working view.
4. `s19-chance-seven-storey-warehouse-2022.jpg` — photograph by Oliver
   Mills, 22 February 2022, CC BY-SA 2.0, 1,200×1,600. **High** for the
   surviving Seven Storey Warehouse; same modern-date caveat.
5. `s19-chance-catalogue-plate.jpg` — plate from an unidentified Chance
   Brothers trade catalogue of ornamental glass designs, Public domain,
   date c.1900s (uncertain — Commons date given only as "1900s",
   flagged, not narrowed). **Medium**: the firm's trade output, not
   the works, and its date is imprecise.
URL-only: the ILN's own engravings of Chance's manufactory, 21 Dec
1850, are known to exist (the 1852 page cites them) but IA holds that
issue only as a loan-restricted scan, and the open DLI ILN set lacks
vol. 17 — no openly downloadable copy was found. Context: Chance
Brothers, founded 1824 when Robert Lucas Chance bought the British
Crown Glass Company at Spon Lane, Smethwick, supplied the glass for
the 1851 building; Historic England listing 1021387 records over
956,000 sq ft supplied, plus a further 750,000 sq ft when the building
was later moved. That area figure and the round-1 figure of 293,000
panes are different units, not a contradiction (C28).

### S25 — The 1851 timber floor with the gaps between the boards (Hyde Park building)
No drawing of the gaps themselves was found; the scene is carried by
contemporary description pages, which agree on the figure that
matters: boards 1½ in thick, laid half an inch apart, so dust fell
through. Gaps are ground floor only: galleries were close-boarded.
1. `S25_wyatt-1851-the-flooring-half-inch-apart.jpg` — Wyatt, "On the
   construction of the building for the Exhibition", p.10, "The
   Flooring" (ICE paper, 1851), 2,760×4,921. Cleanest single page:
   heading, figures and purpose in one paragraph. Joists 7×2½ in on
   sleepers 13×3½ in at 8 ft. **High**.
2. `S25_ackermann-1851-paxton-floor-boards-half-inch-apart.jpg` —
   Ackermann, "The Palace of Industry", p.39, Paxton quoted,
   3,495×4,516. Boards 9 in broad, 1½ in thick, half an inch apart, on
   sleeper joists 9×3 in at 4 ft; dust "falls into the vacuity below";
   also the watering-then-sweeping routine. Best for Paxton's own
   voice. Use with Wyatt, not instead of it, because the joist/sleeper
   figures differ (C12).
3. `S25-01-official-catalogue-1851-introduction-p62-flooring.jpg` and
   `S25-02-official-catalogue-1851-introduction-p63-flooring-conclusion.jpg`
   — the 1851 Official Catalogue introduction's own flooring account,
   the natural companion to Wyatt/Ackermann.
4. `S25-berlyn-1851-floor-description.jpg` — Berlyn (1851), the
   description page: the ground floor "is laid with an interval of half
   an inch between the boards, to allow the passage of dust" (the
   gallery floor, by contrast, had iron tongues between the boards).
   **High** (text read and verified).
5. `S25-berlyn-1851-gallery-floor-test.jpg` — Berlyn engravings:
   "Testing the Gallery Floor" (a floor bay load-tested by workmen)
   and the boiler house. **Medium-High**. Caution: this shows the
   **gallery** floor — a different floor from the ground floor whose
   gapped boards this scene is about. No Downes plate shows the
   ground-floor boarding (the folio is ironwork and glazing), and
   round 1's "Testing the Gallery Floor" must not be used as evidence
   for the ground-floor claim; the Catalogue pages above carry it.
Already collected, not re-downloaded: Downes (1852), "open boarding of
the floor" (IA leaf 13) — text only, no gap dimension; it corroborates,
it does not carry the scene alone. Do not use modern summaries giving
3/8 in or ~1 cm; use ½ in and cite Wyatt/Paxton (C12).

### S34 — What it cost to get in: tariffs, shilling days, tickets
Tariff evidence and shilling-day evidence are different things; the
merged set now holds both, with the licence split stated plainly.
**Tariff (Catalogue pages, open licence):**
`S34-03-official-catalogue-1851-introduction-p28-season-ticket-prices.jpg`
and `S34-04-official-catalogue-1851-introduction-p29-shilling-days-tariff.jpg`
— season tickets **£3 3s (gentleman) / £2 2s (lady)**; then £1 days and
a 5s day; from day 22 the printed tariff ran **Mon–Thu 1s, Fri 2s 6d,
Sat 5s** — "No change will be given at the doors" — with **Sundays
closed** (Catalogue introduction pp.28–29). Secondary sources flatten
the season price to "two guineas" and one modern summary claims 1s
admission "on Sundays" — both wrong (C13).
**Shilling-day pictures (open licence):**
`s34-first-shilling-day-going-in-1851.jpg` (SMG 1991-100/7, 1,536×992)
and `s34-first-shilling-day-coming-out-1851.jpg` (SMG 1991-100/8,
1,536×1,046) — George Cruikshank etchings, Science Museum Group,
CC BY-NC-SA 4.0, published by D. Bogue 1 July 1851, both **high** for
the shilling day itself. The first shilling day was 26 May 1851: the
V&A's record for the season ticket states the exhibition ran 1 May to
15 October 1851, tickets cost 5 shillings for the first four weeks,
and "on 26 May, the price was dropped to one shilling".
**Fares (1854, context):** `S34-phillips1854-fares-page.jpg` — Phillips
(1854), "Conveyance by Rail and Road from London": Brighton Railway
return fares to the Palace including admission on most days — 2s 6d
first class, 2s second, 1s 6d third — with season-ticket arrangements.
Public domain. **High** (visually verified).
**Season tickets — V&A TERMS, not open licences (see licence section).**
`S34-01-va-season-ticket-no1-signed-albert-1851.jpg` (the V&A's season
ticket No. 1, signed by Prince Albert) with its case exterior
(`S34-02-va-season-ticket-case-exterior-1851.jpg`) — downloaded under
V&A non-commercial terms. The object itself is public domain; the
photographs carry non-commercial terms — confirm before commercial
use, and do not present them as openly licensed. A different ticket —
season ticket No. 21810 in the name of Mary Ann Frodsham (V&A object
O121261, accession E.47-1937, pink card) — was recorded licence-unclear
and NOT downloaded (V&A image copyright "© Victoria and Albert
Museum, London", no open licence stated; IIIF image
`https://framemark.vam.ac.uk/collections/2006AX7799/full/full/0/default.jpg`,
description page
`https://collections.vam.ac.uk/item/O121261/ticket-unknown/`). The two
tickets are different objects, not conflicting claims about one ticket;
the merged position on both is in the licence section below. Round 1
already holds the 1856 guide's refreshment tariff pages (gallery
0208–0209) and the Routledge 1851 guide scans (visitor context). An ILN
image of shilling-week visitors (19 July 1851) exists only through a
commercial picture library — not an allowed source.

### S37 — Punch gives the building its name
**Correction to the brief: it is not a cartoon, it is a text piece.**
Two distinct scans of the same page are held (different bytes, both
kept contents):
`S37_punch-1850-vol19-p21-mouser-palace-of-very-crystal.jpg` — Punch,
vol. XIX, p.21 (IA `sim_punch_1850_19`, leaf 24), 3,000×4,056; and
`S37-punch-1850-07-13-mouser-page21.jpg` — the same page from IA
`sim_punch_1850_19_0` (alias `S37-01-punch-1850-07-13-p21-mouser-palace-of-very-crystal.jpg`
maps to my scan). Douglas Jerrold writing as "Amelia Mouser", "A Bit
of My Mind, Bit the Eleventh: Mrs. Mouser suggests a domestic
improvement as regards the Exhibition of 1851". The dream passage,
verified on the page image, calls the Exhibition "a palace of very
crystal, the sky looking through every bit of the roof". The page does
carry a cartoon at its head ("There, Baby dear, look at the pretty
Soldiers!") — that cartoon has nothing to do with the Crystal Palace.
**High** for the piece. Date caveat: the scan page itself bears no
issue date (only "Vol. XIX", p.21). 13 July 1850 is the date given by
secondary sources, and p.21 sits early in the July–December volume,
consistent with the second issue — do not present the date as printed
on the page. **Attribution conflict, preserved not resolved:** other
sources (citing Terry Strieter 1999, and the BBC) credit the Punch
issue of 2 November 1850 with bestowing the name. That issue was not
checked page-by-page here, and the 13 July piece already contains the
"palace of very crystal" image, so the 2 November claim may describe
the name's later currency rather than first use. A further unverified
secondary note says the term occurs seven times in the 13 July issue
itself. The film should not claim a single cartoon, or a single
first-use date, without resolving this (C22). Nuances carried from the
branch pass: the p.21 page gives the descriptive phrase "a palace of
very crystal", **not yet the capitalised proper name**; and the rival
Thackeray attribution has no page evidence.
Supporting pages: `S37-punch-1850-08-24-glass-houses-page81.jpg` —
Punch, Vol. XIX, p.81 (24 Aug 1850): "Glass Houses of Parliament", the
open letter to Paxton that kept the glass-palace idea in circulation
all summer. Public domain. **High**.
`S37-02-punch-1850-07-13-p22-cartoon-hyde-park-building-design.jpg` —
the same issue's p.22 holds a genuine Punch **cartoon** — a palm-house
design "humbly submitted" to Prince Albert — included for the visual,
explicitly **not** the naming item. Round-1 manifest check: 15 "Punch"
hits, none of them the p.21 page. No CP scene for the naming item was
identified in storyboard v001 (flagged omission in the crosswalk
appendix); the film build carries it as a standalone beat.

### S41 — The winter garden: Paxton's plan for the afterlife (Hyde Park building)
1. `S41_haden-1851-paxton-winter-garden-arcadia.jpg` — Haden, "A medical
   man's plea for a winter garden in the Crystal Palace", p.1, 1851,
   CC Public Domain Mark 1.0, 2,175×3,658. **High**: a contemporary
   (1851) witness naming Paxton's plan directly — Paxton had "disposed
   its vast interior into an Arcadia of his own imagining". Best S41
   page after the pamphlet itself. The branch pass's Haden p.3 file
   (`S41-01-medical-mans-plea-1851-p3-addition-to-paxton.jpg`) and its
   opening-page file (`S41-medical-mans-plea-winter-garden-1851.jpg`)
   are byte-identical to this p.1 content and are kept under this
   filename as aliases — they add no new page; do not cite them as
   separate Haden pages.
2. `S41_haden-1851-medical-mans-plea-winter-garden-title.jpg` — Haden
   title page, 1851, CC Public Domain Mark 1.0, 2,100×3,533. **High**
   for identification. Title page is anonymous; the Haden attribution
   is the cataloguer's, so the manifest creator field is left empty.
3. `S41-02-medical-mans-plea-1851-p10-london-childs-plea.jpg` — Haden
   p.10 ("London child's plea").
4. `S41_dilke-catalogue-paxton-winter-park-and-garden-entry.jpg` —
   Dilke, "Catalogue of a collection of works on the Exhibition of
   1851", p.112, 1855, Public domain, 2,732×3,640. **Medium-high**: a
   retrospective record (catalogue 1855, pamphlet 1851) quoting
   Paxton's "Winter Park and Garden under glass". The same page lists
   Cruikshank's satire and Gambardella's "remain on its present site"
   letter — useful for showing the debate, not just Paxton's side.
5. `S41-03-crystal-palace-and-its-contents-1852-p51-preservation-of-the-crystal-palace.jpg`
   — *The Crystal Palace and its Contents* (1852), p.51: the Kingsland
   public meeting resolving to petition Parliament to preserve the
   palace "as a winter garden". **High**.
6. `S41-04-routledges-guide-to-sydenham-1854-p11-removal-of-the-exhibition-building.jpg`
   — Routledge's Sydenham guide (1854), p.11: a retrospective of the
   whole retention debate, name-checking the "Denarius" pamphlet;
   corroboration, not an 1851 artefact.
Not downloaded — Paxton's pamphlet itself ("What is to *become* of the
Crystal Palace?", Bradbury & Evans, 1851): no Internet Archive copy
found by title, author or full-text search. Bibliographic copies exist
at the Royal Collection (RCIN 6004649, 16 pp; RCIN 6006621, 24 pp) —
Royal Collection is not in the allowed-source list for this round, so
these are leads only. Page-count differences (Dilke: 15 pp, 1s edition;
"Another Edition" 16 pp; RCT 16 and 24 pp) are edition/binding
differences — do not pick one as "the" pamphlet length (C15).
**Title trap:** Paxton = "What is to *become* of…"; Cruikshank's satire
= "What is to be *done* with…" (14 etched proposals). A modern paper
swaps them. **Dating trap:** the winter-garden plan is a Hyde Park plan
(1851). The Sydenham rebuilding is a different outcome; do not present
the pamphlet as a Sydenham plan. Other leads, not downloaded:
Greville's "Answer to 'What is to become of the Crystal Palace?'"
(1851, "Pull it down, we say"); Hansard, Lords, 11 July 1851, and
Commons, 29 April 1852 (Parliamentary record, outside the strict
allowed list). The often-cited "ILN 5 July 1851 p.11" winter-garden
image could not be verified — the IA copy of that issue does not
contain it.

### S44 — Period maps of the Sydenham/Norwood ridge before the palace
**No site-specific plan of Penge Common / the chosen site was found in
an allowed source.** What was found is genuine pre-palace mapping of
the ridge. The scene can be carried with a ridge map plus narration;
it cannot honestly be carried with a pre-1854 "site plan".
1. `S44_greenwood-surrey-ridge-norwood-sydenham-crop.jpg` — Greenwood
   Surrey map, ridge crop at full JP2 resolution, 2,177×1,650,
   CC BY-NC-SA 3.0 (David Rumsey Map Collection, Stanford Libraries).
   **Medium**: shows the Norwood ridge country (Dulwich, Streatham,
   Sydenham Hill, Lewisham, Bromley, Croydon), but at county-map scale
   the site zone is small and Penge Common itself is not labelled.
   Ridge context, not a site plan.
2. `S44_greenwood-surrey-county-map-1822-1829-overview.jpg` — C. & J.
   Greenwood, "Map of the county of Surrey. From an actual survey made
   in the years 1822 & 1823 … Published July 4th. 1829" (atlas issue
   1834), 1,536×1,163, CC BY-NC-SA 3.0. **Medium**, establishing
   overview; the crop above is the legible detail. The survey date
   (1822–1823) is the date made, not the publication date (1829).
3. `S44-02-phillips-guide-1854-the-site-page.jpg` — Phillips 1854,
   "The Site" page: the contemporary verbal fixing of the site's
   topography. The routes map (kept under B-plans, alias
   `S44-01-phillips-guide-1854-route-map-to-the-crystal-palace.jpg`)
   shows the site *with* the palace — it evidences ridge geography,
   not the pre-1852 landscape.
Do not caption the Greenwood maps as Ordnance Survey: **no pre-palace
Ordnance Survey sheet was found** (C25). Every OS sheet found that
shows the palace area postdates it (1863–1872, 1886; Commons OS Surrey
sheets are 1871–1882). Places searched and rejected as "before": NLS
Ordnance Survey Six-inch Surrey Sheet XIV (surveyed 1867–1868,
published 1872 — later state only; NLS's map service returned a bot
check from this VM, so no NLS sheet could be downloaded at all); "Map
of Sydenham, Lewisham, c.1865" (OS 1863–1870, later state); Bacon 1886
(later, commercial dealer, excluded); 1864 Helsham Jones ordnance plan
(later, commercial dealer, excluded); Greenwood "Map of London" sheets
5–6 (1824–1826 survey — sheet 5 reaches Peckham, sheet 6 is Greenwich;
neither reaches Sydenham); Greenwood Kent map (survey 1819–1820 — its
JP2 would not decode to a usable image in this session; follow-up lead,
Kent side of the border); Rocque 1774 and OS Old Series 1-inch (no
downloadable open copy showing Penge/Sydenham found); Penge tithe maps
(county archives / The National Archives, not open downloads); Wyld's
*Environs* 1840 (auction copies only); Penge Place sale particulars
(no open scan); the ridge lies outside the 1848–51 OS London town-plan
coverage and the county series is 1860s. Round-1 manifest check: 18
"Ordnance" hits are Imperial War Museum gallery photographs, not maps.
Boundary note: the site sits on the Surrey–Kent border (Penge Common,
Sydenham Hill), so no single county map centres it — say "the ridge
above Penge" rather than pointing at a single labelled plot. If the
film needs a site outline, it must be drawn over a later plan and
labelled as such.

### S45, S46, S47 — Taking it down, moving it, building it again (1852)
**The dismantling page (my review's headline find, ranked first):**
`s45-47-old-crystal-palace-hyde-park-iln-1852-10-30-p360.jpg` —
Illustrated London News, 30 October 1852 (vol. 21, issue 587), printed
p.360, Public domain, 2,016×2,976, from IA
`sim_illustrated-london-news_1852-10-30_21_587`, leaf 15. **High**. The
page carries the article "The last of the old Crystal Palace in Hyde
Park" and two engravings: an oval "Fountain in the north transept" (the
interior before removal) and, below it, "Site of the transept,
north-east" — the cleared site with stacked material, workmen and a
fire. The article states the last column and the last girder had "been
carried away in Mr. Younghusband's vans" to Sydenham, and that only the
trees, the gigantic blocks of coal and the columns of granite remained
to be sold. The first Sydenham column date of 5 August 1852 from the
1856 guide is consistent with a site cleared by 30 October 1852. One
manifest row, section S45; S46 and S47 reference the same file.
**Dating trap:** the 1852 ILN page's "Fountain in the north transept"
engraving shows the Hyde Park interior before removal and must not be
used as a Sydenham interior.
**The paper trail (branch pass, in chronological order):**
`S45-iln-1852-feb-auction-demolition-report.jpg` — ILN, 28 Feb 1852,
p.175: the paper inferred from Fox & Henderson's auction catalogue
that demolition was "already in progress"; **that inference was wrong**
(C14). `S45-iln-1852-sale-70000-report.jpg` — ILN, 1 May 1852, p.335:
after the Commons vote, the sale to private parties at **£70,000**
conditionally accepted; "the work of removal will commence on the 11th
of May". `S46-iln-1852-05-15-transfer-report-p391.jpg` — ILN, 15 May
1852, p.391: the transfer executed in the Transept on 13 May: price
paid, possession delivered, and the purchasers' 150-acre Sydenham
plans. `S46-iln-1852-company-advertisement.jpg` — ILN, 22 May 1852,
p.406: the Company's own advertisement — in effect its prospectus
notice (capital, directors, Paxton/Jones/Wyatt, Fox Henderson as
re-erection contractors). `S46-iln-1852-06-05-sydenham-site-sketch.jpg`
— ILN, 5 June 1852, p.441: "Sketch on the proposed site of the Crystal
Palace, Sydenham": the wooded Penge Place grounds before re-erection.
`S45-phillips-1854-history-leaf18.jpg` and
`S45-phillips-1854-history-leaf20.jpg` — Phillips 1854, Introduction
pp.13 and 15: the official commission on the building's future,
Leech's rescue scheme, and the Company's formation and prospectus
(£500,000 in 100,000 £5 shares). `S47-phillips-1854-history-leaf22.jpg`
— Phillips 1854, Introduction p.17: "The first column of the new
structure was raised by Mr. Laing… on the 5th August, 1852": removal
began in May; August is the *re-erection* start, and modern summaries
that date the dismantling to August conflate the two.
**The removal pamphlet — read the alias warning:**
`S45-removal-pamphlet-1852-title.jpg` — the actual title page of *The
Removal of the Crystal Palace* (Houlston and Stoneman; V&A National Art
Library copy, IA `EX.1851.161RemovalOfTheCrystalPalace`): the printed
debate over removal and Sunday opening, 1851–52. Public domain.
**High** as a document of the removal fight; it is an argument
pamphlet, not a dismantling record. `S45-removal-pamphlet-1852-page1.jpg`
— the pamphlet's p.1, quoting the Commons debate of 29 April 1852; a
Sabbatarian argument about the debate, **not** an official or
contractor's record (C15). **Alias warning:** the branch row
`images/S45-removal-pamphlet-title.jpg` (section S45-47) is NAMED
"title" but holds page-1 text content, byte-identical to the page-1
file above (stage-19 mismatch, high confidence). The alias table
preserves that row with mismatch=yes; the v1 content row for that
content is the page-1 file. Do not cite the alias row as a title page.
IA metadata dates the pamphlet to 1851; its title page reads 1852 and
its text quotes the Commons debate of 29 April 1852 (C15).
**Still missing:** no image of the building actually being taken down
was isolated by any pass (ILN dismantling engravings of 1852 exist in
the bound volumes on IA but were not isolated beyond the p.360 page
above; ILN vol. 21, Jul–Dec 1852, exists only as loan-restricted scans,
so the dismantling's later stages could not be checked in an open
copy). On **transport** no pass found anything: no searched source
describes wagons, carts or trains carrying the parts — Phillips says
only that Fox & Henderson were instructed "to convey the palace". The
1853 Negretti & Zambra interior (S57) also serves this passage — the
building under fit-out before opening; museum dating, treated as the
publisher's date. The Crystal Palace Company prospectus of 18 May 1852
(£500,000 capital in 100,000 £5 shares) was not found as a scanned
item on Internet Archive under that title — the 1855 shareholders'
letter (`1855PalaceShareholders`) is a later document and does not
evidence the 1852 move. The £120,000 figure sometimes quoted for the
Fox, Henderson move contract (from a secondary blog) is **unverified**,
not contradicted — the contemporary ILN article confirms
Younghusband's vans but states no price (C28).

### S51 — Brunel's two water towers (Sydenham)
Two photographs, both Public domain, both **high** for content (a
Brunel tower against the building) and **low** for the Commons "1854"
date (see below). No Brunel water-tower **drawing** was found under an
open licence.
1. `s51-south-transept-south-tower-water-temple.jpg` — Delamotte /
   Negretti & Zambra, "South Transept & South Tower" (handwritten
   caption), 950×850 (aliases
   `S51-01_delamotte_south-transept-south-tower_water-temple_1854.jpg`,
   `S51-south-tower-water-temple-1854.jpg`). The slender Brunel tower
   stands at the left, clearly rising above the south transept
   roofline, Water Temple fountains in the foreground. Date recorded
   as 1854–1859 in my manifest; the branch pass records c.1854–1856
   (C23/D5 — reconciled range below).
2. `s51-centre-transept-north-tower-south-wing.jpg` — Delamotte,
   "Centre Transept & North Tower from South Wing", 960×841 (aliases
   `S51-02_delamotte_centre-transept-north-tower_south-wing_1854.jpg`,
   `S51-north-tower-south-wing-1854.jpg`). Same composition from the
   other end: north tower above the centre transept, fountains in the
   foreground. Same date warning.
3. `S51-03_exterior_fountain-water-tower_RP-F-F01212-16-1.jpg` —
   garden-front photograph, Rijksmuseum, dated 1878–1890, CC0,
   2,500×1,676 — the clearest tower-against-nave height comparison, a
   generation later.
Together these do the scene's "towers against the building for height"
work. **Dating rule (both reviews agree on substance):** the towers
were designed by Brunel and built by Fox, Henderson & Co. in 1854–56,
replacing a first pair of towers (1853, under the company's engineer
Charles Wild) that were demolished as inadequate (C6) — sources that
credit "Brunel's towers" without that history are compressing it.
Brunel's pair was begun in August 1854 and operational only on
2 June 1856 (Historic England), and the great fountains first played
18 June 1856 — so the Delamotte views at items 1–2, dated "1854" by
Commons, cannot be 1854 photographs of finished towers. **No view
dated 10 June 1854 can show the finished Brunel towers** — any S51
image used beside S55 opening material must carry its later date.
**Reconciled date range (C23/D5):** record the two Delamotte views as
c.1854–1856 (branch parallel range), with the note that my manifest's
1854–1859 upper end is not supported by any dated evidence in the set;
both reviews agree on the substance (not 1854; a finished tower with
working fountains cannot predate June 1856). Tower figures: 86 m /
282–284 ft, 12 cast-iron columns on a concrete ring (Historic England)
— against "over 280 ft and 46 ft in diameter" in my review; the foot
figure varies by source (280 / 282 / 284), see C17. Cross-reference,
already in round 1, not re-downloaded: Delamotte "General view from
Water Temple" — same series, also shows a tower; the two new files are
its companions, not replacements. Leads, not downloads: Historic
England Archive Anerley Road water-tower view CC97/00546 and York &
Son stereo view of the South Tower CC97/00770 (1870–1900) — Historic
England's image service was unavailable at the time of searching; a
1925 Alamy photograph was rejected (commercial source).

### S52 — Prehistoric islands in the 1850s, as built (not modern photographs)
No period **photograph** of the completed islands as a whole was
located in the allowed sources.
1. `S52-01_sydenham-palace_prehistoric-creatures-foreground_wellcome-V0013783.jpg`
   — Wellcome V0013783, coloured print, CC BY 4.0, 3,392×2,301 — the
   palace and terraces with Hawkins's models on the islands in the
   foreground: the only true "models in their landscape as built" view
   any pass found. Wellcome dates the print "later than 1854?", so
   content confidence is high but the exact print date is medium.
   Creator blank in v1.
2. `s52-geology-inhabitants-ancient-world-05.jpg` — Engraving from
   Owen's *Geology and Inhabitants of the Ancient World* (1854),
   illustrated by Hawkins, 800×517. **High**: a period view of the
   islands as built, in a book published the year the palace opened —
   palace across the lake, dinosaur models on the island in the
   foreground.
3. `S52-02_owen-1854_megalosaurus-restoration_p20.jpg` and
   `S52-03_owen-1854_labyrinthodon-restoration_p36.jpg` — Owen (1854),
   the official handbook: Megalosaurus (p.20) and Labyrinthodon (p.36)
   — the restorations as built, as the handbook presented them.
4. `S52-dinosaurs-engraving-1854.jpg` — period engraving of the
   dinosaurs on their islands, 1854. Public domain; small (960×525).
   **Medium-High**. Creator blank in v1.
5. `S52-gartenlaube-1854-p106.jpg` and `S52-gartenlaube-1854-p107.jpg`
   — Die Gartenlaube's 1854 two-page spread on the geological islands.
   Public domain. **Medium-High**.
6. `s52-sydenham-studio-1853-1920px.jpg` — Hawkins's Sydenham workshop,
   1853, 1,920×2,507 (1920px derivative; the 14.8 MB original was not
   needed). **High** for the models as built/in construction;
   **medium** for attribution details (Commons metadata alone).
   **Cataloguing correction (C24/D1, confirmed by stage 19):** Commons
   attributes it to Delamotte as a photograph, but visually it is an
   **engraving, not a photograph** — do not caption it as a photograph.
7. `S52-hawkins-studio-delamotte-1853.jpg` — the branch pass's file of
   the same workshop subject (3,166×4,134), described in the branch
   review as "photographed by Delamotte, 1853". Stage-19 viewing of
   the merged set's copy confirms the correction: what is actually
   seen is an **engraving** (cross-hatched line work throughout, same
   workshop family as the two Gartenlaube engravings on the same
   sheet), not a photographic image. Delamotte authorship alone cannot
   be confirmed or refuted from the image. **The merged review follows
   the engraving reading; the branch review's "photographed by
   Delamotte" wording is not carried forward for this file.**
8. `s52-concept-drawing-dinosaurs-1854.jpg` — Hawkins's 1854 concept
   drawing, 960×571. **Medium**: Hawkins's own period design for the
   islands, but a concept drawing, not a view of the finished islands;
   rank it behind the Owen plate for any "as built" claim.
Cross-reference: the 1856 guide's own **Secondary Island plate**
(`1856-guide-147900764.jpg`) — the islands as the Company's guide
presented them in 1856. **High**. Crossover (filed under S55): the
Paxton souvenir print also shows the lake, islands and dinosaur models
in a panoramic palace view. Rejected: a 2021 photograph of a Hawkins
Iguanodon plaster in Paris (modern photograph, wrong location); the
modern Iguanodon photograph already in round 1 does not satisfy this
scene; Commons's "Iguanodon Model 1–6 (1854)" files are modern
photographs of a 1/12-scale model — excluded. Already in round 1 (not
re-downloaded): the ILN 31 Dec 1853 model-room engraving of the models
under construction, held as a Smithsonian 1900 reproduction.

### S53 — Dinner inside the Iguanodon, 31 December 1853
Two files, both Public domain, both **high** for content. Date the
work 1854-01-07 (ILN issue); the dinner depicted was 1853-12-31 — do
not date the work itself to 31 December 1853 (C3).
1. `s53-iln-1854-01-07-p22-dinner.jpg` — Full page 22 of the
   Illustrated London News, vol. 24 no. 662, 7 January 1854 (IA
   `sim_illustrated-london-news_1854-01-07_24_662`, leaf 21),
   4,113×5,936 (alias `S53-02_iln-1854-01-07_p22_dinner-page.jpg`).
   Engraving captioned "DINNER IN THE IGUANODON MODEL, AT THE CRYSTAL
   PALACE, SYDENHAM": guests inside the Iguanodon's body, waiters on
   the stairs, banners BUCKLAND, CUVIER, OWEN, MANTELL. Article on the
   same page: Hawkins "had one-and-twenty guests around him in the
   body of the Iguanodon on Saturday last; at the head of whom...
   sat Professor Owen". This is the primary published record — use it
   first. **Disposition D3: the merged review follows this page —
   Owen at the head, engraving and report together.** The branch
   review's base text (Hawkins at the head; ILN coverage text-only) is
   superseded by its own parallel addition and by this page, and is
   not carried forward.
2. `s53-iguanodon-dinner-woodcut.jpg` — Cropped Commons copy of the
   same ILN engraving, 1,287×831 (aliases
   `S53-iguanodon-dinner-woodcut-1854.jpg`,
   `S53-01_iguanodon-dinner_ILN-woodcut_1854.jpg`). Cleaner, closer
   crop of the diners, but a secondary copy without page context;
   rank behind the full ILN page.
Other records checked, not downloaded: Hawkins's own sketch of the
dinner (British Library Add MS 50150, f.225 — no digitised copy found
for download; Hawkins's own later letter misdates the ILN report
"July 7 1854" — it is 7 January); ILN model-room engraving of
31 December 1853 (vol. 23, issue 661, p.600 — context for the models,
not the dinner). The dinner was in the *mould*, as the storyboard's
CP034 has it. Secondary pages (Cain, Geological Society, BL blogs)
were used only to confirm date and guest count (21 guests, Owen at
the head); they are not download sources.

### S55 — Opening of the Sydenham palace, 10 June 1854
Dating discipline: ILN issues are dated by issue, ceremony by
10 June 1854; the souvenir print predates the opening and is not an
opening-day record.
1. `s55-iln-1854-07-01-p618-opening-left.jpg` and
   `s55-iln-1854-07-01-p619-opening-right.jpg` — The two halves of the
   ILN double-page opening engraving, 1 July 1854 (IA
   `sim_illustrated-london-news_1854-07-01_24_690`, leaves 7–8,
   printed pp.618–619), each 4,120×5,936, Public domain. Left: royal
   party on the dais ("OPENING OF THE CRYSTAL P..."); right: crowd
   inside the palace ("...PALACE, AT SYDENHAM"). **High**. The two
   files must be joined for display. Article on p.620 confirms: "the
   impressive ceremony of the Opening of the Crystal Palace, on June
   10, by her Majesty, in person."
2. `S55-iln-1854-06-17-opening-arrival-p582.jpg` — ILN, 17 June 1854,
   p.582: "Opening of the Crystal Palace — Arrival of Her Majesty",
   engraving of the Queen's arrival for the 10 June ceremony, with the
   report text. Public domain. **High** (visually verified).
3. `S55-iln-1854-06-17-opening-article.jpg` — the ILN opening article
   page, with the opening medal engraving. Public domain. **High**.
4. `s55-queen-victoria-reopening-delamotte-1854.jpg` — Delamotte
   photograph, Metropolitan Museum (DP109644), CC0, 3,101×3,912 (alias
   `S55-01_delamotte_opening-ceremony_MET-DP109644.jpg`). Royal party
   on the dais, vast choir and orchestra filling the transept.
   **High** for the ceremony; **medium** for the exact day (Met title
   plus a matching Historic England caption, not a date inscribed on
   the print). **Wording trap (C19):** the Met title calls it the
   "Reopening of the Reconstructed Crystal Palace" — "reopening"
   because the palace had first opened at Hyde Park in 1851; at
   Sydenham this was the opening of the reconstructed building. Do not
   let "reopening" imply a second Sydenham opening, and do not confuse
   it with the 1920 reopening (a different event, some of whose
   photographs are in round 1).
5. `s55-smg-paxton-print-1854-large.jpg` — Science Museum Group
   co8020384, official souvenir print designed by Paxton, Day & Son,
   published 25 May 1854, CC BY-NC-SA 4.0, 1,536×930. **High** as
   opening-era context; **low** as evidence for anything on 10 June
   itself — it predates the opening by over two weeks and shows water
   towers and fountains that were not yet operational.
6. `S55-02_smg_lithograph_inaugurated-10-june-1854.jpg` — Science
   Museum Group lithograph "The New Crystal Palace at Sydenham",
   CC BY-NC-SA 4.0 — the non-commercial term stands, so it is usable
   only under those terms. As a depiction it is **partly
   anticipatory**: it shows both towers complete and the fountains
   playing, neither true until June 1856. (The branch base text's note
   that this lithograph was "noted, not downloaded" is superseded by
   its parallel pass, which downloaded it; the usability note is
   unchanged.)
7. `S55-state-visit-1855.jpg` — the palace ceremony photograph of
   April **1855** (Napoleon III, Queen Victoria, Empress Eugenie,
   Prince Albert). Included because it is the famous "royal group at
   Sydenham" photograph — but it is the French state visit a year
   later, **not** the opening; do not caption it as 1854. Public
   domain. **High** (as an 1855 image). Creator blank in v1.
Not downloaded: Historic England Archive albumen print AL0327/009/02
(possibly Delamotte, Queen Victoria at the opening) — identified from
a secondary article, but Historic England's image service was
unavailable, so no download route or licence could be established.
The Met Delamotte photograph above is the substitute. Opening-date
correction (C2): a Surrey Archaeological Society bulletin (1998)
saying the palace "opened on June 18th 1854" is wrong; the opening was
10 June 1854.

### S57 — Sydenham interior and exterior in the 1850s, with dates
Ranked best first. The two V&A photographs carry licence **unclear**
— confirm V&A terms before film use (see licence section). Exterior
coverage for this scene comes from the S51 tower photographs (garden
front from the fountains) and the S55 Paxton panorama; no separate
garden-front photograph was added, to avoid duplicating the S51 views.
1. `s57-negretti-zambra-egyptian-court-1854-rijks.jpg` — Negretti &
   Zambra stereoscopic photograph of the Egyptian Court interior,
   Rijksmuseum RP-F-F04697, CC0, 4,562×2,402. **High**: a dated
   Negretti & Zambra court interior, exactly what the scene asked
   for — colossal seated pharaoh figures, painted columns,
   hieroglyphic decoration. (Round 1: `skipped-budget`.)
2. `s57-negretti-zambra-interior-1853-rijks.jpg` — Negretti & Zambra
   stereoscopic interior, Rijksmuseum RP-F-F14420, CC0, 3,926×1,954
   (aliases `S57-interior-negretti-zambra-1853.jpg`,
   `S57-05_negretti-zambra_interior-stereo_RP-F-F14420_1853.jpg`, and
   the cross-section alias `S47-sydenham-interior-stereo-1853.jpg`).
   **High** for a Negretti & Zambra Sydenham interior; **medium**
   for the exact year (museum dating, not an inscribed date) —
   classical statues, fountain basin, iron-and-glass roof, with a
   still-unfinished look consistent with pre-opening fitting-out in
   1853. (Round 1: `skipped-budget`.) The branch pass captions it as
   the building **under fit-out**, not the finished interior.
3. `S57-03_delamotte_nave-interior_MET-DP109633.jpg` — Delamotte, the
   planted nave, 1854 (Met DP109633, CC0, 2,651×3,976) — the definitive
   1850s nave interior.
4. `S57-04_delamotte_sculpture-gallery_MET-DP109630.jpg` — Delamotte,
   sculpture gallery, 1854 (Met DP109630, CC0) — statues in rows
   during installation.
5. `S57-progress-delamotte-met-109624.jpg` and
   `S57-progress-delamotte-met-109625.jpg` — Delamotte / Negretti
   construction photographs, 1854 (Met Museum, CC0, ~3,900 px).
   **High**.
6. `S57-01_delamotte_general-view_water-temple_1854.jpg` — general view
   from the Water Temple, Delamotte, 1854 (alias
   `S57-general-view-water-temple-1854.jpg`). Public domain. **High**.
7. `S57-upper-gallery-delamotte-1852-54.jpg` — along the upper gallery,
   Delamotte, dated 1852–54 (Rijksmuseum, CC0). **High**.
8. `s57-roman-court-plate-viii-1854.jpg` — "Roman Court from the Nave",
   plate viii of *Views of the Crystal Palace and Park, Sydenham*
   (1854), tinted lithograph by Francis Bedford after a Delamotte
   photograph, CC0, 1,575×1,225 (alias
   `S57-02_roman-court_views-1854_plate-viii_BL.jpg`). **High** for
   the Roman Court interior in 1854; note it is a lithograph after a
   photograph, not the photograph itself.
9. `s57-delamotte-great-nave-1854-va.jpg` — V&A O128434, Delamotte
   albumen print, "The Great Nave, Crystal Palace", 1854,
   1,500×2,000. **High** on the V&A description (vaulted glass roof,
   galleries, plants, fountain along the nave). Licence: **unclear**
   — the V&A record carries only "© Victoria and Albert Museum,
   London"; no CC licence is stated.
10. `s57-delamotte-interior-fountain-transept-1854-va.jpg` — V&A
    O85633, Delamotte albumen print, "Interior view: Crystal Palace",
    1854, 2,000×1,641. **High** on the V&A description (this file was
    not visually inspected frame by frame, unlike the Great Nave).
    Licence: **unclear**, same as above.
11. `S57-interior-stereo-1855-75.jpg` — stereoscopic interior,
    c.1855–75 (Rijksmuseum, CC0) — later than the ideal 1850s window
    at its far end; ranked last for that reason. **Medium**. Creator
    blank in v1. **Dating dispute (C10):** the Rijksmuseum
    "Stereoscopic Illustrations" series that sounds 1850s is dated by
    the museum **c.1870–1890** and was deliberately kept out by the
    branch pass — which sits uneasily with this file's "c.1855–75";
    treat the later stereo dating as disputed. The dispute does not
    touch items 1–2 above, which are individually dated.
Leads checked, not downloaded: British Library Delamotte prints
Tab.442.a.5(7)–(10) (BL catalogue flags the related construction set
as not digitised); National Gallery of Victoria Negretti & Zambra
1859 stereographs (NGV download/licence terms not established, NGV not
explicitly in the allowed-source list — now redundant given the two
Rijksmuseum CC0 stereographs); Science Museum Group Carrick
lithographs co67636/co67639 (no licence line found on the co67639
object page — record licence as unclear if picked up later); SMU
"Stereoscopic Illustrations of the Crystal Palace, at Sydenham"
(metadata "ca. 1850" predates the 1852–1854 rebuild, Flickr Commons
"No restrictions" rather than a clean CC licence, content unverified);
two Rijksmuseum stereographs dated ca. 1870–1890 (outside the 1850s
scope). The museum's Crystal Palace stereoview series runs to dozens
more (sculpture courts, vestibules, nave statues) if later scenes need
interiors (Section C).

### S67 — Fire that destroyed the north transept, 30 December 1866 (Sydenham)
This is the Sydenham palace, not Hyde Park — the fire was at Sydenham,
thirty years after the move. Fire-date drift: the fire was
30 December 1866; most print coverage is January 1867, and some
secondary sources drift it into 1867 outright (C18).
1. `S67-iln-1867-01-05-fire-engraving.jpg` — ILN, 5 Jan 1867:
   engraving of the fire's aftermath — the burnt north transept
   interior seen from the transept, trees standing in the ruins.
   Public domain. **High** (visually verified).
2. `S67-iln-1867-01-05-fire-report.jpg` — the same issue's full
   report, "Fire at the Crystal Palace". Public domain. **High**.
3. `s67-ruins-north-transept-iln-1867-01-12-p28.jpg` — ILN, 12 Jan
   1867, printed p.28, IA leaf 3, 2,068×2,952. Full-page engraving
   captioned "Ruins of the north transept of the Crystal Palace
   destroyed by the late fire": twisted iron frame and the surviving
   Abu Simbel (Rameses) figures. Public domain. **High**.
4. `S67-01_iln-1867-01-12_ruins-abu-simbel_north-transept.jpg` — ILN,
   12 January 1867, full-page engraving of the ruins (4,136×5,904) —
   the Abu Simbel colossi amid twisted girders and rubble; the best
   picture of the destruction in the set.
5. `s67-ground-plan-fire-extent-iln-1867-01-12-p42.jpg` — ILN,
   12 Jan 1867, printed p.42, IA leaf 17, 2,068×2,952. Article "The
   great fire at the Crystal Palace" beside a "Ground plan of the
   Crystal Palace" whose caption states the tinted portion indicates
   the extent of the destruction by the fire, with an index of the
   courts (Sheffield, Bohemian, French, Alhambra, Egyptian, Greek,
   Roman, Italian, Renaissance, Mediaeval, Byzantine, and others).
   This plan is also directly useful to Section B. The article
   describes the fire beginning at the north-east angle of the
   lecture-room/class-room area and spreading through the Alhambra
   and Egyptian courts, and notes the two Rameses figures were each
   60 ft high. Public domain. **High**.
6. `S67-02_iln-1867-01-12_p42_fire-account-plan.jpg` — the same
   issue's p.42: the contemporary account page, with a small plan
   diagram of the damaged part (a distinct file from item 5's plan
   page).
Mark the loss on the pre-fire plans in Section B; the building was
never rebuilt to its full length afterwards. Not downloaded (licence
unclear, URL-only rows in v1): Historic England Archive photographs
OP04456 (twisted metal with Abu Simbel figures in the distance) and
BB92/15895 (stereoscopic interior with snow on damaged court walls),
both © Historic England Archive with no open licence stated. They
corroborate the ILN engraving but add nothing it does not already
show. **Dating trap:** a commercial library catalogues the ILN 1867
engraving as "Ruins of the North Transept … 19th century" with no
building named — it must be labelled Sydenham (1866 fire), never Hyde
Park, and never dated 1851.

### S70 — FA Cup final at the Crystal Palace, 1895–1914 (1913 especially)
**No 1913 match photograph exists in the allowed sources** — the only
1913 pictorial material found was commercial (PicClick/eBay, Getty)
and was not used. The 1913 programme below is a 1913 artefact, not a
match photograph; do not present it as one.
1. `s70-1913-fa-cup-final-programme.jpg` — Programme, Aston Villa v
   Sunderland, 1913, 975×1,368 (alias
   `S70-fa-cup-final-1913-programme.jpg` — collected by both branch
   passes under the same filename, byte-identical, so it appears once
   in v1). **High** that it is a 1913-final artefact at Crystal
   Palace; **low** as a picture of the match itself (programme cover).
2. `S70-aston-villa-1913-postcard.jpg` — postcard of the Aston Villa
   cup-winning team, 1913 (Rotary Photographic Co.). Public domain.
   **High**.
3. `s70-1905-fa-cup-final-panorama.jpg` — Panoramic photograph of the
   stadium crowd, 15 April 1905, 2,157×760 (alias
   `S70-fa-cup-final-1905-panorama.jpg`). **High** — a genuine period
   match photograph at the Crystal Palace stadium, the best actual
   match image in the set. (Round 1: `skipped-budget`.)
4. `S70-fa-cup-final-1901-photo.jpg` — the 1901 final at the Palace
   ground, Tottenham v Sheffield United before 114,815. Public
   domain; small (504×336). **Medium** (alias
   `S70-fa-cup-final-1901.jpg`; creator blank in v1).
5. `s70-1899-fa-cup-final-illustration.jpg` — Illustration of the 1899
   final (Sheffield United v Derby County), 1899, 964×531 (alias
   `S70-fa-cup-final-1899-illustration.jpg`). **High** for the event,
   **medium** as a depiction (illustration, not photograph).
6. `s70-1904-fa-cup-final-programme.jpg` — Programme, 1904, 820×1,122.
   **High** for the event; a programme, not a match photograph.
7. `S70-fa-cup-final-1906-fans.jpg` — 1906 FA Cup fans photograph.
   Creator blank in v1.
Places searched for a 1913 match photograph: Wikimedia Commons (title
and category searches, including "1913 FA Cup Final" — no such
category exists), Internet Archive. The 1913 final itself (Aston Villa
1–0 Sunderland, attendance 120,028) is confirmed from the finals
record, but that does not make the programme a match photograph. The
120,028 figure is a rounded source claim; keep it as reported, not as
a verified count.

### S83 — Demolition of the two water towers, 1940 and 1941
**No photograph of either demolition was found in any allowed source.**
What follows is the nearest honest evidence: the towers standing, and
what survives. A 1928 photograph of the north tower before demolition
exists only through a commercial print site — not an allowed source,
not downloaded.
1. `s51-south-transept-south-tower-water-temple.jpg` — Delamotte /
   Negretti & Zambra, south tower against the south transept (filed
   under S51; cross-referenced here, not duplicated). **High** for
   the tower's height against the building, which the brief also asked
   for; **low** for the demolition itself — it predates it by
   86 years. See S51 for the date warning.
2. `s83-south-water-tower-base-2002.jpg` — Remaining base of the south
   tower, 2002, CC BY-SA 3.0 (Fonzy), 500×336. **High** for what
   survives; **low** for the demolition event.
3. `s83-north-water-tower-base-2002.jpg` — Remaining base of the north
   tower, 2002, CC BY-SA 3.0 (Fonzy), 500×337. Same confidence as
   above.
4. `S83-south-water-tower-base-2022.jpg` — surviving south-tower base,
   photographed 2022, CC BY-SA 4.0, as the present-day evidence.
   Stage-19 viewing confirms: a 2022 photo of the overgrown surviving
   base, not a demolition photo.
Dates (Historic England listing 1469984, base of the southern water
tower): south tower dismantled in sections during **autumn 1940**
(proximity of housing and the former engineering school buildings
ruled out explosives); north tower demolished with explosives by the
Royal Engineers on **16 April 1941**. The listing also records the
towers built 1854–1856 by Fox, Henderson and Company to Isambard
Kingdom Brunel's designs, 86 m tall, demolished 1940–1941; the south
tower carried John Logie Baird's television antenna from 1933. If the
existing collection or scene list repeats "taken down shortly after
the 1936 fire" for the south tower, correct it to autumn 1940 (C21).
Some web retellings reverse the towers' order, or claim the south
tower fell "shortly after the 1936 fire" — contradicted by the SAS
account and the Historic England listing. Places searched: Wikimedia
Commons, Internet Archive, Historic England listing and archive
catalogue (archive photographs are © Historic England Archive with no
open licence stated, so none was downloaded), two IWM collections
searches (IWM returned only its 1920–24 gallery material). URL-only
rows in v1: the Surrey Archaeological Society Bulletin 321 (July
1998) photograph of the 1941 explosion (© Lambeth Archives), the ILN's
April 1941 photo feature ("The Crystal Palace North Tower to Go",
commercial archive — not reused), and the Historic England list entry
1469984 itself.

### S87 — Crystal Palace subway (built in the 1860s)
No 19th-century engraving of the subway interior was found in allowed
sources; the historic evidence here is the plan and the station
photograph, plus clearly-labelled modern conservation photographs.
1. `s87-high-level-station-plan-1895.png` — Ordnance Survey plan,
   1895, Public domain, 544×840 (low resolution; alias
   `S87-os-plan-high-level-station-1895.png`). **High**: shows the
   High Level station, its sidings and turntable, and the surviving
   subway beneath Crystal Palace Parade — the best plan evidence in
   the set, directly usable for a route/arrival drawing. (Round 1:
   `skipped-budget`.)
2. `S87-high-level-station-iln-1865.jpg` — ILN engraving of the new
   High Level station, 30 Sept 1865 — the station the subway served;
   the subway itself is underground and not visible in it.
3. `s87-high-level-station-1908.jpg` — Photograph of the High Level
   station, 1908, Public domain, 598×361. **High** for the station the
   subway served; the subway itself is underground and not visible in
   it. (Round 1: `linked`.)
4. `s87-subway-entrance-2010.jpg` — Photograph by Malc McDonald,
   17 October 2010, CC BY-SA 2.0, 640×480. **High** for the subway
   entrance approach; modern, not historic.
5. `s87-subway-interior-2023.jpg` — Photograph by Doyle of London,
   15 September 2023, CC BY-SA 4.0, 1,920×1,438. **High** for the
   subway's present restored interior (Byzantine-style vaulting, red
   and cream brick, chequered floors). Label it as a conservation-era
   photograph, not a historic one: the subway was restored and
   reopened in the 2020s.
6. `S87-subway-interior-2023.jpg` — the branch pass's 2023 interior
   (a distinct file from item 5 above; both are kept contents).
7. `S87-subway-interior-2016.jpg` — interior in 2016, pre-restoration,
   CC BY-SA 4.0.
8. `S87-subway-east-courtyard-2023.jpg` — east courtyard during
   restoration, 2023, CC BY-SA 4.0.
9. `S87-subway-restored-interior-2025.jpg` — restored interior,
   January 2025, CC BY-SA 2.0.
Together with item 5 these date the present-day scenes honestly: the
subway's present state is *restored 2023–24*, and access is not
continuous. Context (not downloaded, for the caption): subway built
1865 to link the High Level Station (opened 1 August 1865, Charles
Barry Jr.'s design) to the palace; Grade II listed 1972, upgraded to
Grade II* 2018. Historic England Archive items DP232790/DP232791
(interiors) and DP487647 (oblique aerial of the restored entrance)
exist but are © Historic England Archive with no open licence stated
— not downloaded, licence unclear. Both reviews agree: **no Victorian
image of the subway itself exists** in the sources searched.

### S89 — National Sports Centre, 1960s
**Nothing usable as a 1960s photograph.** No period (1960s) photograph
was found in any allowed source. Places searched: Wikimedia Commons
(modern geograph photographs of the centre exist, all 2010s–2020s),
Internet Archive, the round-1 catalogue. The only 1960s-period material
found was commercial/rights-managed: a Getty/Hulton Archive Aerofilms
aerial dated 1964 and an Alamy Allan Cash 1964 indoor sports hall
photograph — not allowed sources, not downloaded.
`S89-national-sports-centre-2024.jpg` — the 1964 building photographed
in 2024, CC BY-SA 4.0. **Medium** — right building, wrong decade.
Stage-19 viewing confirms: a 2024 aerial photo of the sports centre,
not a 1960s photo. If the scene can carry a "the building today" beat,
that file is the fallback; it is not a 1960s image and must not be
captioned as one. **Contradiction with the round-2 brief:** the brief
labelled this scene optional, but storyboard v001 treats the National
Sports Centre as a book-covered core scene (CP066), not optional. If
v001 governs, S89 needs a different solution than the optional label
suggests (see crosswalk appendix). Period photographs exist in
architectural-press and Historic England holdings, but not under terms
the brief allows.

## Scenes with nothing usable

These scenes have no file in the merged set that satisfies the scene
as asked. The fallback choice (card or text beat) can now be made with
open eyes; places searched are in the scene sections above.

- **S15 — Fox, Henderson & Co.'s works at Smethwick.** Nothing in any
  allowed source (Commons, Internet Archive, Historic England, Science
  Museum Group, V&A). The 1849 bowstring pamphlet pages document the
  firm and its product; they do not show the works. Do not substitute
  a Chance Brothers photograph — different firm. Fallback: card/text
  beat.
- **S89 — National Sports Centre, 1960s.** No period photograph in any
  allowed source; only commercial 1964 material (Getty/Hulton
  Aerofilms aerial, Alamy indoor hall). The 2024 photograph is a
  "building today" fallback only, deliberately labelled as such.
  Fallback: card/text beat, or the modern-photo beat labelled as such
  — subject to the v001 core-vs-optional conflict (CP066).

**Partial gaps inside otherwise-covered scenes** (fallback or
captioning decisions needed, not whole-scene failures):

- S13: December 1850 works views only; no summer-1850 first-works view
  (hoardings, setting-out, trenching, foundations).
- S44: ridge/county maps only; no pre-1854 plan of the chosen site
  itself (Penge Common).
- S51: photographs only; no Brunel water-tower drawing under an open
  licence.
- S52: engravings and a workshop engraving only; no period photograph
  of the completed islands as a whole.
- S70: programmes and earlier finals only; no 1913 match photograph.
- S83: towers standing and surviving bases only; no demolition
  photograph.
- S87: plan and station photograph plus modern conservation
  photographs only; no 19th-century subway-interior engraving.
- S19: product sample, a reference page and modern surviving-fabric
  photographs only; no 1850s working view of the glassworks.
- S34: tariff pages (open licence) and shilling-day etchings (open
  licence) held; the tariff evidence in ticket form (V&A season
  tickets) is under V&A terms, not an open licence.
- S41: contemporary witness pages and a retrospective catalogue entry
  only; Paxton's own pamphlet was not found as a downloadable copy on
  an allowed source.
- Section B: no standalone post-1866 building plan earlier than 1878;
  no drawn 1854 Sydenham section; no standalone both-lines palace plan
  (closest: the OS Surrey Sheet 008 crop, a district sheet).

## What this draft carries over from my review (audit checklist)

The stage-18 comparison listed 28 mine-only claims. All 28 are
integrated above, at the sections noted; this checklist exists so the
carry-over can be checked without re-reading both source reviews.

1. Greenwood Surrey maps (S44) — ridge crop + county overview, with
   the never-caption-as-Ordnance-Survey warning.
2. Wyatt ICE flooring paper p.10 + Ackermann Paxton flooring quote
   p.39 (S25), including the differing joist/sleeper figures.
3. Cruikshank shilling-day etchings "Going In" / "Coming Out" (S34).
4. Dilke catalogue p.112 winter-garden entry (S41).
5. ILN 30 October 1852 p.360 dismantling page (S45/S46/S47).
6. ILN 1 July 1854 opening double-page spread, pp.618–619 (S55), two
   files that must be joined for display.
7. V&A Delamotte photographs, licence-unclear (S57), excluded from
   film use pending V&A terms confirmation.
8. 1904 FA Cup final programme (S70).
9. 1908 High Level station photograph + 2010 subway entrance
   photograph (S87).
10. 2002 north water-tower base photograph (S83).
11. Ordnance Survey Surrey Sheet 008 crop, 1871–1882 (Section B),
    with full-sheet crop coordinates.
12. Festival of Empire 1911 Map row (Section B, round 1).
13. ILN 1867 p.42 fire-extent plan as a plans-table row (Section B).
14. Hawkins 1854 concept drawing for the islands (S52) + the
    cataloguing correction that the "Sydenham studio" image is an
    engraving, not a Delamotte photograph (C24/D1).
15. S05 specifics: Partridge 1840 Albert portrait; Winterhalter 1845
    (RCIN 404129); Vanity Fair 1871 Cole caricature; Society
    distributing-awards engraving; Paris Musées QB.726/QB.727 files.
16. S03 specifics: Fitch plate 1 "Entire plant reduced" (1851) + the
    Hooker and Fitch folio plates (2,151×1,588).
17. S04 specifics: ILN London/Thames panorama 1845–1850; Wellcome
    power-loom weaving plate (date unknown, recorded as unknown);
    Loutherbourg Coalbrookdale by Night 1801 (flagged 50 years early).
18. S13 specifics: Hassell elm lithograph (British Museum, dated
    1837–1852) as Hyde Park context, the first-iron-column date anchor
    (26 September 1850, secondary source), and the excluded-leads list
    (Bridgeman "Sappers and miners", Yale ILN 6 July 1850 design
    engraving with unverified reuse terms).
19. V&A season ticket No. 21810 in the name of Mary Ann Frodsham
    (E.47-1937), recorded licence-unclear and not downloaded, with its
    IIIF URL and description page (S34). Different ticket from the
    branch's No. 1 Albert ticket.
20. S19 modern-site specifics: 2007 canalside works photograph, 2022
    Seven Storey Warehouse photograph, c.1900s Chance catalogue plate,
    and the firm-history context (founded 1824, ~2,000 peak employees
    at Smethwick, closed 1856, site cleared 2014 for the Midland
    Metropolitan University Hospital).
21. The 1,398 breakdown by round-1 section (commons 345, main-article
    31, Downes 209, Routledge 272, Tallis v1 232, v4 172, New York 114,
    Architectuul 11, ILN-1850 9, V&A Paxton 3) + the 1,398 thumbnails
    note + the 17-column manifest design + assembly notes (two
    SHA-256 dedupes, group-A dimension corrections on 22 of 23 rows,
    OS crop provenance).
22. The full v001 crosswalk appendix (see below) — the branch review's
    inline CP references do not substitute for a scene-by-scene CP↔S
    map, and the S37 omission flag and S89 core-vs-optional
    contradiction belong in the merged review.
23. The S89 modern-fallback policy: the 2024 Commons photograph noted
    as a "building today" fallback but deliberately labelled as such,
    with the commercial leads named (Getty/Hulton Aerofilms 1964,
    Alamy Allan Cash 1964).
24. S67 article detail: fire began at the north-east angle of the
    lecture/class-room area, spread through the Alhambra and Egyptian
    courts, Rameses figures each 60 ft high.
25. S53 secondary-record checks (not downloaded): Hawkins's dinner
    sketch (BL Add MS 50150, f.225) and the ILN 31 Dec 1853 model-room
    engraving (vol. 23, issue 661, p.600) as context.
26. S41 leads (not downloaded): Greville's "Answer to 'What is to
    become of the Crystal Palace?'" and Hansard (Lords 11 July 1851;
    Commons 29 April 1852), flagged as outside the strict
    allowed-source list.
27. Section B rejected-plans list: *The Builder* 28 June 1856 Grand
    Fountain Basins plan (not extracted), May 1864 commercial district
    map (excluded), ILN August 1852 proposal-plan follow-up (14 Aug
    issue has no ground-plan caption), 1911 auction catalogue landscape
    leaves sampled (photographs, not plans), and the NLS/OS
    viewer-served sheets flagged as a browser/viewer task.
28. Heights extras: the 1854 text's claim that the Sydenham nave crown
    (104 ft) is "just the height of the transept at the old building"
    (a Hyde Park figure to keep separate), and the 1911 auction
    catalogue repeat figures (wings 574 ft each; 2,756 ft with wings;
    3,476 ft with the 720 ft colonnade; water towers 284 ft to the top
    ornaments; aquarium inaugurated 1872, ~400×70 ft, 38 tanks).

## Claims in the existing collection or scene list that new sources contradict

Reported, not fixed. Nothing in this draft was edited outside
`build/fold/`. Count: the branch review's 20 numbered items plus my
review's 12 numbered items = 32; five direct overlaps were merged
(heights, reopening wording, pamphlet date/character, round-1 count,
floor figures), and two review-vs-review differences that appear in
neither numbered list were added (tower-photo date range, Microcosm
plate versions), giving **29 items (C1–C29)**. The stage-18 estimate of
"roughly 23" undercounted because it treated several unnumbered text
conflicts as overlaps; the item-by-item count here is the auditable
one. Dispositions D1–D6 from the stage-18 comparison are applied where
marked.

**C1. Sydenham heights — the Company's own guides disagree.
[Disposition D4: carried with the branch qualifier, not as a settled
datum.]** 1856 guide, printed p.35: nave height 110 ft 3 in; transept
height 174 ft 3 in; transept from basement 197 ft 10 in. Phillips,
1854: nave arch crown 104 ft (springing 68 ft); central transept
168 ft to the top of the louvre, 108 ft to the springing, 208 ft from
the garden front. Routledge 1854 agrees with Phillips (104 ft;
168 ft 3½ in to the crown). Lengths agree exactly (1,608 ft; 384 ft
transept). My review reads the constant 6 ft 3 in gap on both headline
figures as pointing to a datum difference (1854 "floor" vs 1856
"ground floor"). The branch review withholds that reading as unproven:
the difference is "partly datum... and partly — for the louvre
figures, 168 vs 174 ft 3 in — unexplained", and no 1856 text states a
datum. **Merged position: state the datum with every height, give
both figures with their sources, and do not present the datum reading
as established.** (The often-quoted "108 ft" for a transept turns out
to be Phillips's Sydenham *springing* height — a plausible origin for
several later confusions, including the Hyde Park figures flagged in
round 1's REVIEW. The book's rounded transept heights, roughly
108 ft / 168 ft per storyboard v001, are neither the 1854 nor the 1856
figures — resolve endpoints and datums before narrating precise
heights. And 384 ft must not be equated across its two uses: 1856
greatest width vs 1854 central transept length.)
**C2. Opening date.** The documented opening is 10 June 1854
(Phillips's preface; ILN report of 17 June 1854). At least one later
heritage text (Surrey Archaeological Society bulletin, 1998) says the
palace "opened on June 18th 1854" — wrong, but in circulation.
**C3. The Iguanodon dinner's image is dated 1854; the dinner was
31 Dec 1853.** The woodcut (S53) is a print *of* the event published
the following year; captions should date the event 1853 and the print
1854.
**C4. The 1855 state-visit photograph is not the opening.** The
Napoleon III / Queen Victoria group (S55) is April 1855. It is
routinely captioned elsewhere as the 1854 opening; it is not.
**C5. "Crystal Palace Park – 1857.jpg" (Commons, also in round 1's
orbit)** carries an upload date (2014) where a depicted date should
be, and no source note; "1857" rests on the title alone. Use with
care.
**C6. Tower credit.** "Brunel's towers" compresses a two-step history:
a first pair of towers (1853, company's engineer Charles Wild) was
demolished as inadequate; Brunel's replacement pair was built
1854–56 by Fox, Henderson & Co. (Historic England, list entry
1469984).
**C7. Round-1 wrong-building files (from REVIEW.md, restated because
S05 now touches them):** the French 1849 exposition building, the
Berlin Kroll Wintergarten and the unexecuted committee/Turner designs
sit in round 1's plan folders. Round 2's 1849 Paris prints (S05) are
that same French building — wanted there as the predecessor, never as
the London palace.
**C8. Phillips 1854: plan or no plan. [Disposition D2: kept flagged
UNRESOLVED, narrowed by stage 19.]** The branch base position
(examined IA scan `guidetocrystalpa00phil_0`, Getty copy) found **no
building ground plan** in Phillips's guide. The branch parallel pass
downloaded a fold-out ground plan attributed to Phillips 1854, with a
full court key. Stage 19 viewed that plan (`S56-plan-1854-phillips-ground-plan.jpg`):
it **is** a whole-building ground plan with keyed courts, south wing
entrance from the station, and north wing — so the branch attribution
has a real file behind it. But the mine-side finding was about the
Delamotte-scan 1854 guides examined in round 2, and this file's source
edition was not re-established in stage 19. Possibly different
printings of the guide, possibly a misattribution — unresolved; both
statements stand, and the plan should not be cited as "Phillips 1854"
without the caveat. The same caveat applies to the Phillips Alhambra
court plan.
**C9. The Iguanodon dinner: who sat at the head of the table, and
what the ILN printed. [Disposition D3: resolved toward my review and
the branch parallel pass.]** The branch base text puts **Hawkins** at
the head of the table and reports the ILN's own coverage as a
text-only report, with no second period record found. The branch
parallel addition and my review agree: the ILN page itself
(7 Jan 1854, p.22, held in the set) carries engraving **and** report
together, and puts **Owen** at the head of the table. **The merged
review follows Owen and the full page, and drops the branch base
text's two statements.**
**C10. The Rijksmuseum stereo dating.** The later stereoscopic
interior at S57 (`S57-interior-stereo-1855-75.jpg`) is dated
c.1855–75 in my review; the branch pass reports that the museum dates
its "Stereoscopic Illustrations" series **c.1870–1890** and kept that
series out on that basis. (The 1853 Negretti & Zambra stereo, S57
item 2, is individually dated and not part of this dispute.) Treat
the later stereo dating as disputed.
**C11. Round-1 image count.** The repo README and `MUSE-PROMPT.md`
say the round-1 collection has **1,393** images; the repo actually
holds **1,398** (REVIEW.md agrees with 1,398, as do both passes'
counts; the branch review adds that 3 are truncated long Rijksmuseum
filenames). The README's "32 main-article / 340 Commons" breakdown is
also stale: live inventory is 31 / 345.
**C12. Floor-board figures.** Modern summaries give board *widths*
(22 cm / 9 in) with a ~½ in gap, disagreeing with each other, and some
give 3/8 in or ~1 cm for the gap. The 1851 Catalogue, quoting Paxton,
gives board **thickness** 1½ in and a ½-inch gap, and no width; Wyatt
1851 agrees on ½ in. Use the primary figures, and note the gaps are
ground floor only — galleries were close-boarded (any caption
implying the whole building had gapped floors is wrong). The
joist/sleeper figures differ between Wyatt (7×2½ in on 13×3½ in
sleepers at 8 ft) and Paxton via Ackermann (9×3 in at 4 ft) — cite
both, do not harmonise them.
**C13. Season-ticket and shilling-day flattening.** Secondary sources
flatten the season-ticket price to "two guineas" (the Catalogue gives
£3 3s gentleman / £2 2s lady), and one modern summary claims 1s
admission "on Sundays" — the Exhibition was closed on Sundays
(Catalogue p.28).
**C14. "Demolition already in progress" (ILN, 28 Feb 1852).** An
inference from an auction catalogue; the building was in fact sold
intact in May 1852 and re-erected. Any script line dating demolition
to February 1852 would be wrong. Removal was announced to begin on
11 May 1852 and the first Sydenham column was raised on 5 Aug 1852 —
summaries that date the *dismantling* to August conflate removal with
re-erection.
**C15. The removal pamphlet's date and character.** IA metadata dates
*The Removal of the Crystal Palace* to 1851; its title page reads
1852 and its text quotes the Commons debate of 29 April 1852. It is
also a Sabbatarian argument pamphlet about that debate — round 1's
catalogue record for it carries bookseller subject headings and
should not be cited as an official removal record. Paxton =
"What is to *become* of the Crystal Palace?"; Cruikshank = "What is
to be *done* with the Crystal Palace?" (satire). A modern paper swaps
them. Page counts (15 / 16 / 24 pp) are edition/binding differences,
not one correct count.
**C16. Routledge's "Central Dome".** A Routledge passage giving a
160–170 ft "Central Dome" describes the **rejected 1850 Building
Committee design**, not Sydenham. Routledge also reverses the Hyde
Park widths (456/408); the 1856 assignment (408 ft general / 456 ft
greatest) stands.
**C17. Tower height figures.** 280 ft (ILN, 1941), 282 ft, 284 ft and
86 m all circulate for the same pair of towers (Historic England
gives 86 m, on 12 cast-iron columns over a concrete ring). The
demolition order and method are settled (C21); the headline height is
not.
**C18. Fire-date drift.** The north-transept fire was 30 December
1866; some secondary sources place it "in 1867" because the print
coverage is January 1867.
**C19. Met title wording.** DP109644's title, "Reopening of the
Reconstructed Crystal Palace", describes the **1854 first opening**
at Sydenham; the 1920 reopening is a different event (some of its
photographs are in round 1). My review's gloss ("reopening" refers to
the 1851 Hyde Park opening) and the branch review's warning are
compatible warnings about one ambiguous word; the merged position is
the one stated at S55: Sydenham 1854 was the opening of the
reconstructed building.
**C20. Catalogued ≠ collected.** Round 1's manifest lists items — the
Chatsworth lily-house engravings, the c.1862 grounds map, the 1905 FA
Cup panorama, the 1895 OS station plan, the ILN Iguanodon-dinner
woodcut — with status *skipped-budget*: present as records, absent as
files until this round downloaded them. Any future audit should count
`status = downloaded` rows only.
**C21. Water-tower demolition dates.** Some web summaries say the
south tower was "taken down shortly after the 1936 fire". Historic
England listing 1469984 dates it precisely otherwise: south tower
dismantled in sections during **autumn 1940**, north tower blown up
**16 April 1941** (by the Royal Engineers). The branch base text's
"1940–41" for the south tower is the parallel pass's "autumn 1940"
refined, not contradicted; the demolition method (south in sections,
north by explosives) is agreed by both reviews.
**C22. The "Punch cartoon".** The brief's S37 framing is wrong: the
naming item is Jerrold's Mouser text piece, not a cartoon, and the
first-use date is contested (13 July 1850 vs 2 November 1850).
Correct any caption calling it "the Punch cartoon" or asserting a
single first-use date. The p.21 page gives the descriptive phrase "a
palace of very crystal", not yet the capitalised proper name.
**C23. Delamotte water-tower photographs dated "1854". [Disposition
D5: reconciled range.]** Commons metadata dates the two S51
photographs 1854, but Historic England listing 1469984 gives the
towers built 1854–1856 with fountains turned on 18 June 1856. A
photograph showing a finished tower with fountains in full flow cannot
date from 1854. My manifest records 1854–1859; the branch pass records
c.1854–1856 and warns against captioning them 1854. **Merged range:
c.1854–1856**, with the note that my manifest's 1854–1859 upper end
is not supported by any dated evidence in the set. Both reviews agree
on the substance (not 1854). Any existing caption dating these views
to 1854, or using them as 10 June 1854 opening-day evidence, is wrong.
**C24. "Sydenham studio" as a Delamotte photograph. [Disposition D1:
corrected by stage-19 visual verification.]** The image catalogued as
a Delamotte photograph of Hawkins's workshop is visually an engraving
(stage 19: cross-hatched line work throughout, same workshop family as
the two Gartenlaube engravings). Any caption calling it a photograph
is wrong. Delamotte authorship alone cannot be confirmed or refuted
from the image. The branch review's "photographed by Delamotte, 1853"
wording is not carried forward for this file.
**C25. Greenwood maps as Ordnance Survey.** The pre-palace maps in
the set are Greenwood county maps (survey 1822–1823), not Ordnance
Survey. Any caption calling them Ordnance Survey is wrong; no
pre-palace OS sheet was found.
**C26. The "1,851 ft = year" explanation.** The 1911 auction catalogue
text repeats the claim that the Hyde Park building's length "was to
be 1,851 feet — which corresponded with the year of its opening". Per
the round-1 review, that explanation is unsupported and must not be
repeated as fact.
**C27. Historic England Archive caption error (secondary).** A
Historic England Archive item description (as returned in search)
says the palace was "designed for the Great Exhibition in 1851 and in
1864 was moved from Hyde Park to Sydenham" — 1864 is wrong; the move
and rebuild were 1852–1854. Treat HE archive captions as unchecked
where they give dates.
**C28. No contradiction found where one might be expected.** Chance
glass figures (293,000 panes, round 1, vs over 956,000 sq ft plus
750,000 sq ft on the move, Historic England listing 1021387) are
different units, not conflicting figures. The £120,000 figure sometimes
quoted for the Fox, Henderson move contract (from a secondary blog)
is **unverified**, not contradicted — the contemporary ILN article
confirms Younghusband's vans but states no price, so the figure should
stay flagged, not asserted.
**C29. Society of Arts Microcosm plate: July 1809 vs 1810. [Disposition
D6: two versions kept distinct.]** My review: Microcosm Plate 71, July
1809, 2,400×2,024 version; a 2,764×2,144 colour version dated 1810
noted in Section C, not substituted. The branch parallel addition:
Microcosm plate, **1810**. These may be two printings/versions of the
same plate rather than a dating error; the merged review keeps the
two versions distinct instead of collapsing them to one date.

**Not contradictions (recorded to prevent false merges).**
- *S34 season tickets:* my Frodsham No. 21810 (unclear, not
  downloaded) and the branch's Albert No. 1 (downloaded, V&A
  non-commercial terms) are **different tickets**, not conflicting
  claims about one ticket. The policy difference is real, though —
  see the licence section.
- *S89 fallback:* my review deliberately did not download the 2024
  photograph; the branch downloaded it. Same evidence conclusion (no
  1960s photo), different staging policy — not a factual conflict.
- *S57 stereo dating:* branch Contradiction 10 (series c.1870–1890)
  does not touch my individually dated 1853/1854 stereographs, which
  the branch agrees are individually dated (see C10).
- *Tower demolition method:* both reviews agree (south in sections
  autumn 1940; north explosives 16 April 1941); the branch base text's
  "1940–41" is a refinement, not a contradiction (see C21).
- *1856 guide "2 maps":* my review (ground plan 384 + Plan of Palace
  and Park 658 as the most plausible reading) and the branch review
  (second map "believed to be" the ground plan 0205) agree.
- *S55 "reopening":* see C19 — compatible warnings about one
  ambiguous word.

## Build-verified corrections (not review-vs-review)

These come from build stages after both reviews were written. They are
not counted in C1–C29, and they correct the source reviews' wording
where the build checked the file itself.

- **Berlyn leaf 59 (S13).** The branch review describes
  `S13-berlyn-1851-works-view-plate.jpg` as a "view along the
  building under construction with workmen". Build stage 10 downloaded
  it from its IA source (Berlyn leaf 59) and visually verified it as
  "View of Glass Roof from the Lead Flat" — a completed, fully glazed
  roof with men on the lead flat, not frame erection and not a
  construction view. Stage 19 confirmed this from the merged set's
  copy. **Do not carry the branch description forward for this file;
  do not caption it as a construction view.** The file itself remains
  available at its IA source if a roof/finishing beat ever wants it.
- **S45 "title" alias row.** The branch row
  `images/S45-removal-pamphlet-title.jpg` (section S45-47) is NAMED
  "title" but holds page-1 text content, byte-identical to
  `S45-removal-pamphlet-1852-page1.jpg` (stage-19 mismatch, high
  confidence). The alias table preserves that row with mismatch=yes;
  the v1 content row for that content is the page-1 file. The actual
  title page is the separate S45-row file
  (`S45-removal-pamphlet-1852-title.jpg`). Do not cite the alias row
  as a title page.
- **S13 construction view and post-1866 plan — closed in the build.**
  Build stage 10 closed both gaps from branch contents re-downloaded
  from original sources and visually verified: ILN 14 Dec 1850
  "Raising the Ribs" + Berlyn frame-erection plate (S13), and the 1878
  guide ground plan (standalone post-1866 plan). My review's
  statements that S13 has "site context only" and that "no standalone
  building plan was found" are therefore superseded, while the branch
  review already contained both items. This draft records them as
  closed, citing stage 10, not as open gaps.
- **S15 — documented, not closed.** Build stage 10 documented S15
  with the 1849 bowstring pamphlet pages (the branch's S15 documents)
  but did not close the works-photograph gap: neither file shows the
  works. This draft keeps S15-works-photograph open and describes the
  pamphlet pages exactly as stage 10 captions them (pamphlet/proof
  pages, not a works view or photograph).

## Section C — Better versions noted, not substituted

No original in `references/muse-drive/` was replaced (round-2 rules
forbid it, and nothing outside `references/muse-round2/` was touched).
The following better versions were found and are noted here for a
future decision; the round-2 files themselves are first downloads, not
replacements.

- **Society of Arts, Adelphi (S05):** the downloaded Microcosm of
  London Plate 71 is the 2,400×2,024 July 1809 version. A 2,764×2,144
  colour version dated 1810 exists on Commons ("Microcosm of London
  Plate 071 - Society for the Encouragement of Arts, Adelphi
  (colour).jpg"). It was not substituted at assembly; swap it in only
  if the colour version is wanted (see C29 — keep the two versions
  distinct).
- **Crystal Palace from the air, c.1935** — ETH-Bibliothek photographs
  by Walter Mittelholzer (Commons, public domain, TIFF ~46.9 MB
  each): superb late views of the whole Sydenham site a year before
  the fire. Under the 50 MB cap but three near-identical frames; left
  for a decision on which single frame the film wants.
- **Crystal Palace, 1886** — Hallwyl Museum photograph (Commons,
  public domain, TIFF 45.9 MB): a fine garden-front view; a smaller
  Commons JPG derivative exists if wanted.
- **Henry Cole portrait** — the frontispiece of *Fifty Years of
  Public Work*, Vol. I (1884) would replace the 227×332 place-holder
  (`S05-henry-cole-portrait.jpg`).
- **The New Crystal Palace at Sydenham (opening engraving)** —
  Science Museum Group, CC BY-NC-SA 4.0: non-commercial terms make it
  unusable for most film purposes; recorded so nobody re-hunts it as
  "the missing opening picture" — the ILN engravings under S55 are
  public domain. (Note: the branch parallel pass did download this
  lithograph as `S55-02_smg_lithograph_inaugurated-10-june-1854.jpg`;
  the non-commercial term stands.)
- **Negretti & Zambra / Delamotte stereoviews (Rijksmuseum, CC0)** —
  this round took five; the museum's Crystal Palace series runs to
  dozens more (sculpture courts, vestibules, nave statues) if later
  scenes need interiors.
- **Routledge's 1854 guide** — full text on IA; a plan-hunt through
  its plates is the obvious next pass if a third 1854 source is wanted.
- **Paris 1849 building** — round 1's file (gallery 0322) is only a
  *plan* of the 1849 building. The Carnavalet bird's-eye engraving
  (CC0, 3,000×2,525) is the pictorial version and is held in the set
  (`S05-paris-1849-exhibition-birdseye-carnavalet.jpg`). Keep both.
- **Checked — no better version exists** — the 1856 ground plan
  (5,669×2,763 *is* the full Polona scan, and the complete guide is not
  on the Internet Archive at all) and the 1857 park plan (Commons
  original 1,483×1,896, identical to round 1's copy).
- **De-duplication, not better versions:** the Delamotte south-tower
  view and the 1895 High Level plan each arrived twice (once per
  research group, byte-identical by SHA-256). One copy of each was
  kept; the dropped copies are recorded in the assembly notes, not as
  "better versions". The full duplicate record is the 44-row alias
  table: 16 sources collected under two or three filenames on the
  branch, plus the shared-content names kept under my filenames.

## Licence-unclear and V&A-terms position (explicit, applies to the whole draft)

Nothing in this draft upgrades a licence. The merged set contains
four categories that must not be treated as openly licensed film
material without further confirmation:

1. **My V&A Delamotte photographs (S57), licence unclear, OUT of the
   film cut:** `s57-delamotte-great-nave-1854-va.jpg` (V&A O128434)
   and `s57-delamotte-interior-fountain-transept-1854-va.jpg` (V&A
   O85633). The V&A records carry only "© Victoria and Albert Museum,
   London"; no CC licence is stated. Confirm V&A terms before any film
   use; do not treat a museum object record as an open licence.
2. **Branch V&A season-ticket photographs (S34), V&A non-commercial
   terms, NOT an open licence:**
   `S34-01-va-season-ticket-no1-signed-albert-1851.jpg` and
   `S34-02-va-season-ticket-case-exterior-1851.jpg`. The object itself
   is public domain; the photographs carry non-commercial terms.
   Confirm before commercial use. Their v1 licence URLs are the V&A
   collection URLs kept verbatim, not an open-licence URL.
3. **My V&A Frodsham season ticket (S34), licence unclear, NOT
   downloaded:** object O121261 (accession E.47-1937), No. 21810 in the
   name of Mary Ann Frodsham. A different ticket from item 2's Albert
   No. 1. Recorded with its IIIF URL and description page (see S34);
   do not download or use it until V&A terms are confirmed.
4. **Historic England Archive leads, licence unclear, NOT downloaded:**
   tower views (CC97/00546, CC97/00770), 1866-fire photographs
   (OP04456, BB92/15895, URL-only rows in v1), subway interiors
   (DP232790/DP232791, DP487647), and the 1920s–30s material named in
   the scene sections. © Historic England Archive, no open licence
   stated.
5. **URL-only rows with non-open licences (v1, no file held):** two
   `unclear` rows, one loan-restricted row (ILN 21 Dec 1850 Chance
   manufactory engravings — IA scan loan-restricted), one not-stated
   row (© Surrey Archaeological Society bulletin 321), one commercial
   row (ILN April 1941 photo feature, ILN / Mary Evans Picture
   Library — not reused), one © Historic England website-content row
   (list entry 1469984, a record, not an image).
6. **Non-commercial CC licences held as files (usable only under
   those terms):** the Cruikshank shilling-day etchings and the SMG
   Paxton print and SMG lithograph (CC BY-NC-SA 4.0), the Greenwood
   maps (CC BY-NC-SA 3.0), the Sharp leaf-underside (CC BY-SA 4.0),
   and the conservation photographs under CC BY-SA versions as
   recorded per file. Check each file's licence before film use; the
   set does not re-licence anything.
**Consistency rule for the merged set:** the V&A-terms position above
applies to items 1–3 alike. My review's "unclear, excluded" treatment
and the branch review's "downloaded under V&A terms" treatment describe
different objects under different handling, not a single policy — the
merged policy is: V&A photographs are not open-licence material, and
none of items 1–3 enters a film cut until V&A terms are confirmed in
writing for that use.

## Appendix — Storyboard v001 crosswalk (CP001–CP076 vs S-scenes)

During round 2 a separate storyboard draft, v001 (76 scenes,
CP001–CP076, 3,541 words, central estimate 31:35, planning only), and
its executive scene sequence were received. They live on Bear's Mac at
`books/the-crystal-palace/crystal/` (not in this repo, which has no
`youtube/` folder), and their CP IDs are independent of the S IDs used
above (the draft says so itself). This appendix maps the merged
collection to the CP scenes so the same files serve both lists; it
does not re-scope round 2.

- S03 Chatsworth → CP003, CP004 (note: CP004 omits the lily-leaf
  inspiration anecdote on purpose — do not reintroduce it from the
  S03 files).
- S04 Britain 1850 → CP002.
- S05 portraits / 1849 Paris → CP005 (note: CP005 says no portrait
  likeness required — differs from the S05 ask; the portraits
  collected here are available if the film wants them).
- S13 Hyde Park 1850 works → CP006, CP008, CP010.
- S15/S19 Fox, Henderson / Chance → CP009, CP011 (S15 gap stands in
  both lists).
- S25 timber floor → CP013, CP020.
- S37 Punch naming → no CP scene identified in v001 (flagged
  omission).
- S41 winter-garden plan → CP030.
- S44 Sydenham ridge maps → CP033, CP072 (georeferenced Sydenham
  plan).
- S45/S46/S47 dismantling + move → CP031, CP032, CP063.
- S51 water towers → CP042, CP062, CP064.
- S52/S53 dinosaurs + Iguanodon dinner → CP034, CP043, CP067, CP074.
- S55 Sydenham opening → CP035.
- S57 Sydenham interiors → CP037–CP041 (incl. Egyptian court plan
  0226, Alhambra plan 0246, round 1).
- S67 1866 fire → CP047, CP048.
- S70 FA Cup → CP050, CP055 (1913 Aston Villa v Sunderland).
- S83 tower demolition → CP064 (CP064 itself says tower dates and
  reasons need individual records rather than one simple shared
  explanation — consistent with the autumn 1940 / 16 April 1941
  correction above).
- S87 subway → CP046 (1860s High Level), CP065 (1954 closure), CP071
  (present day).
- S89 National Sports Centre → CP066 — **contradiction with the
  round-2 brief**: v001 says the National Sports Centre is a
  book-covered core scene, NOT optional. If v001 governs, S89 needs a
  different solution than the optional label suggests.
- Other v001 cautions carried forward: 1913 attendance is a rounded
  source claim; visits are distinct from individual visitors (CP029);
  HMS Victory V/VI designation conflicts — omit until verified
  (CP056); 1936 ignition not established, Churchill quotation omitted,
  do not use an 1851 Downes section for the 1936 Sydenham fire;
  "82 years" = Sydenham, "85 years" = 1851–1936 overall, neither the
  age of one unchanged building; as of 26 October 2026 the 90th
  anniversary of 30 November 1936 has not yet occurred, so "more than
  90 years" is not used; present-day access / subway opening /
  restoration status not verified (CP070–CP071); Imperial War Museum
  palace occupation, detailed Baird television work and detailed
  Festival of Empire account are NOT narrated in the transcript — do
  not claim them as book scenes. Course model status cited in v001:
  37 of 77 Hyde Park bays, 888 ft of the west half, unfinished frame.

## Manifest and assembly notes (merged)

- File: `build/fold/MERGED-MANIFEST-V1.csv` (244 rows + header,
  20 columns) — this draft's companion manifest. Columns, in order:
  `title, local_path, section, source_pages, original_url, width,
  height, bytes, mime, license, license_url, description, status,
  creator, date_made, sha256, what_it_shows, source_sets,
  provenance_status, what_it_shows_confidence`. The first twelve
  columns are exactly the round-1 manifest's columns, in the same
  order, so the lists can merge; `creator, date_made, sha256,
  what_it_shows` are appended because round 1 has no creator,
  date-made or SHA-256 columns and the brief requires them;
  `source_sets` and `provenance_status` are draft-only, and
  `what_it_shows_confidence` is v1-only.
- Row counts: 244 = 71 my rows (45 mine-only + 26 shared, `source_sets`
  mine/both) + 167 branch-only file rows + 6 URL-only rows. Unique
  file contents: 238 (distinct non-blank SHA-256 values). File bytes
  (duplicates counted once): 608,308,900 (~580.1 MiB).
- `provenance_status` is kept verbatim from the stage-9 draft
  (COMPLETE 71, PARTIAL 167, URL-ONLY 6), with an explicit warning:
  PARTIAL no longer means "SHA/what_it_shows missing" — both are now
  filled for all 167 branch rows (stage 17 SHA, stage 19 viewing). It
  now means "remaining gaps listed under Still missing". A finalising
  stage should re-derive the status vocabulary explicitly rather than
  leaving PARTIAL to mean two different things across stages.
- `source_pages` is the description page (Commons file page, IA item
  page, museum object page); `original_url` is the direct file URL
  downloaded from. For the OS crop, `original_url` is the full-sheet
  original; the committed file is the crop described in `description`
  (full-sheet pixels 4200,4400 to 6400,6300).
- `date_made` is the date the WORK was made, not publication or upload
  date. Where it is a range, a circa, or unknown, it is recorded as
  such — never narrowed by guessing. Branch date_made values were NOT
  verified in stages 17–20 (see Still missing).
- `sha256` was computed on the committed file and, for branch-only
  contents, recomputed locally in stage 17 (167/167 match the branch
  manifest's embedded claims); `bytes`, `width` and `height` are the
  committed files' actual values. My review's group-A staging
  width/height values were corrected at assembly (22 of 23 rows
  recorded thumbnail sizes); bytes and SHA-256 needed no correction.
- Section labels were NOT remapped in v1 (see
  `build/fold/SECTION-LABEL-MAP.md`: 20 branch labels identical to my
  labels, mapped 1:1; 17 unmapped with reasons, not forced — including
  the guide/source groupings B1-guide1856, B2-iln1854, B2-phillips1854,
  B5-heights, four PLAN labels, multi-scene tags S45-47 and S56-S66
  route plan, and scene labels with no my-manifest counterpart: S15,
  S46, S47, S62 grounds, S66 north/post-fire, S89). My `B-plans`
  label has no branch counterpart.
- No file in the merged set is over 50 MB; no 3D file of any kind and
  no .zip file was downloaded. Nothing outside `references/muse-round2/`
  was added, edited, moved or deleted in round 2, and nothing outside
  `build/fold/` was written by the folding stages. In particular,
  nothing in `references/muse-drive/`, `blender-deliverables/`,
  `course-models/`, `crystal/`, `models/` or `youtube/` was touched.

## Still missing before this draft and v1 could replace either review or manifest

1. Creator for 13 rows (listed by name in
   `build/fold/MERGED-MANIFEST-V1-NOTES.md`: 11 branch-only file rows
   + 2 URL-only Historic England Archive rows) — plus a per-row source
   check for the 156 embedded branch creator values before they are
   treated as image creators (author-vs-image-maker ambiguity).
2. date_made verification for all 173 branch rows: values are carried
   verbatim from branch description prose, including imprecise values
   and guide publication years, and were NOT normalised or checked
   against depicted dates.
3. Licence-terms confirmation for non-open-licence rows: my 2 V&A
   Delamotte rows, the 2 branch V&A-terms ticket rows, and the URL-only
   unclear/not-stated/commercial/© Historic England/loan-restricted
   rows (see the licence section above).
4. A provenance_status re-derivation (see the PARTIAL warning above).
5. A final head re-check immediately before any commit, and a single
   new commit on `muse-round2` (never force-push) — no commit was made
   in any folding stage.

## Round totals

My pass: 71 files in `references/muse-round2/images/`,
104,375,188 bytes (~99.5 MiB); largest single file 14.7 MB (Fitch
expanded-flower plate). Branch passes: Pass B 123 files, 381.9 MB;
Pass A 89 files, 203 MB; merged branch totals 211 image files,
585.1 MB (the passes overlap on exactly one filename — the 1913 FA
Cup programme, byte-identical in both — and on sixteen further sources
held under two or three different filenames); 217 manifest rows (211
downloaded + 6 URL-only). **Merged totals: 238 unique file contents,
608,308,900 bytes; v1 rows 244 (238 file rows + 6 URL-only); the
round as a whole is under the 1 GB cap.** All licences are public
domain or CC0 / CC BY / CC BY-SA / CC BY-NC-SA as recorded per file
in v1, except the licence-unclear and V&A-terms rows listed in the
licence section, which are not open-licence material. Nothing was
written outside `references/muse-round2/` in round 2, and nothing
outside `build/fold/` in the folding stages; nothing was merged to
main.
