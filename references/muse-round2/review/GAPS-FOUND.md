# Muse round 2 — gaps found: missing scene images and Sydenham plans

## Summary

**Start-here checks.** `references/muse-drive/review/REVIEW.md` — present, read
(including "Corrections that matter" and "What to keep separate").
`references/muse-drive/data/manifest.csv` — present; this round's manifest uses
its exact columns, with three columns appended (`creator`, `date_made`,
`sha256`) because the brief requires provenance the round-1 columns have no
field for; the shared columns merge cleanly. Round-1 images under
`references/muse-drive/` — **1,398 found**, as the brief states (the repo
README and `MUSE-PROMPT.md` both say 1,393; see Contradictions).
`youtube/claude-liam-crystal-palace-story-walk/scenes.json` and `TIMELINE.md` —
**not in this repository** (no `youtube/` folder among its 3,152 files). This
round was worked from the brief's own scene table; Bear later supplied the
v001 storyboard (CP001–CP076) in chat, so each scene below also carries its
CP crosswalk. `dimensions-from-1856-guide.json` — found at
`references/muse-drive/review/dimensions-from-1856-guide.json`.

**What was found.** 95 manifest rows: **89 files downloaded (203 MB**, under
the round's 1 GB cap; largest single file 14.4 MB, none over 50 MB) plus
**6 URL-only records** (licence-restricted or oversize sources, recorded with
URLs). Every scene in the brief has at least one usable candidate except the
honest gaps listed below. The Sydenham plans (section B) came in strongly:
the 1856 guide's second map, Phillips's 1854 foldout ground plan, an 1854
grounds foldout, a post-fire plan of 1878, and a two-source heights
cross-check. The dismantling scenes S45–S47, blank in round 1, now have a
contemporary paper trail.

**What could not be found** (details and full search logs per scene below):
any image of the Hyde Park building actually being taken down, or any record
of how the parts were transported; a genuinely pre-1852 map of the
Sydenham/Norwood ridge; Paxton's own winter-garden pamphlet as an open scan;
a period view of Fox, Henderson's London Works; an openly licensed
photograph of either water tower's demolition; any 1960s National Sports
Centre image under an open licence; a drawn 1854 section of the Sydenham
building; Brunel's tower drawings under an open licence.

**The three biggest surprises.**
1. **The 1856 guide's Sydenham dimensions are the outlier.** Two independent
   1854 sources (Phillips's official handbook; Routledge/MacDermott) agree
   with each other and with the drawn arch geometry — nave crown 104 ft,
   central transept 168 ft — against the 1856 table's 110 ft 3 in /
   174 ft 3 in (round 1's dimensions JSON). A consistent ~6 ft shift on
   both figures; unresolved, and the model should not treat the 1856
   figures as settled.
2. **The Punch item that named the palace is not a cartoon.** It is Douglas
   Jerrold's prose letter ("Mrs Amelia Mouser") in *Punch*, 13 July 1850,
   p.21 — "a palace of very crystal" inside a dream description. The page is
   now held and the dating pinned from the issue itself.
3. **The towers cannot appear in an 1854 view.** Brunel's water towers were
   begun in August 1854 and operational only on 2 June 1856; the great
   fountains first played 18 June 1856. The well-known "Inaugurated
   10th June 1854" lithograph shows both complete — it is promotional
   anticipation, and the Delamotte tower views Commons dates "1854"
   cannot be 1854 photographs of finished towers.

Manifest: `references/muse-round2/manifest.csv` (95 rows). Files:
`references/muse-round2/images/`. Nothing outside `references/muse-round2/`
was added, edited, moved or deleted.

---

## A. Scenes

### S03 — Chatsworth: Great Conservatory and lily house → CP003, CP004
1. **Latham photograph of the Great Conservatory exterior** (19th c.,
   undated; PD; `images/S03-great-conservatory-chatsworth-19c-photo.jpg`,
   1035×611). The only period photograph found; small. Confidence: high.
2. **Underside of a Victoria regia leaf, William Sharp chromolithograph,
   1854** (CC BY-SA 4.0 — this Commons copy is a modern Rawpixel
   enhancement; `images/S03-victoria-regia-leaf-underside-sharp-1854.jpg`,
   2500×2000). The rib structure in full detail; crop the modern caption
   band before use. Confidence: high.
3. **"The Gigantic Waterlily in Flower at Chatsworth", ILN, 17 Nov 1849**
   (PD; `images/S03-gigantic-waterlily-in-flower-chatsworth-iln-1849.jpg`).
   The first flowering, in Paxton's lily house. Confidence: high.
4. **Victoria Regia House, exterior and interior engravings, Berlyn &
   Fowler 1851** (PD; `images/S03-victoria-regia-house-chatsworth-1851.jpg`,
   `images/S03-victoria-regia-house-interior-chatsworth-1851.jpg`).
   Catalogued in round 1 as skipped-budget — never actually downloaded
   until now. Confidence: high.
No interior view of the Great Conservatory exists on Commons; the Met's
CC0 "Chatsworth Conservatory" drawing was left out — its subject could not
be verified.

### S04 — Britain around 1850: industry and its cost → CP002
1. **Britannia Bridge tube floated into place, Hawkins lithograph, 1850**
   (PD; `images/S04-britannia-bridge-tube-floating-1850.jpg`, 6862×5531).
   Heavy railway engineering in the scene's own year. Confidence: high.
2. **"A Court for King Cholera", Leech, *Punch*, 25 Sept 1852** — the
   balance image (CC BY 4.0, Wellcome;
   `images/S04-court-for-king-cholera-leech-1852.jpg`, 3755×2806).
   Confidence: high.
3. **Manchester from Kersal Moor, Wyld, 1852** (PD;
   `images/S04-manchester-from-kersal-moor-wyld-1852.jpg`, 1000×656 —
   best open copy is small; filename says "(1857)", the painting is 1852).
   Confidence: high.
4. **Rain, Steam and Speed, Turner, 1844** (PD;
   `images/S04-rain-steam-and-speed-turner-1844.jpg`). Dated honestly:
   1844, an artwork, not a document of 1850. Confidence: high as the
   railway-age image.
5. **Cotton-mule factory floor, Ure, 1835** (PD;
   `images/S04-cotton-mule-spinning-1835.jpg`). Fifteen years early;
   nothing closer to 1850 of comparable clarity exists in the allowed
   sources (no British factory photograph of c.1850 was found anywhere).
   Confidence: medium-high.

### S05 — Portraits, the Society of Arts, Paris 1849 → CP005 (CP007 context)
1. **Henry Cole, portrait print captioned "executive commissioner", 1852**
   (PD, National Library of Wales;
   `images/S05-henry-cole-executive-commissioner-1852.jpg`). Confidence: high.
2. **Joseph Paxton, attributed to Ellerby, c.1843** (PD;
   `images/S05-joseph-paxton-ellerby-1843.jpg`, 2497×3307 — the
   highest-resolution period Paxton portrait found; the c.1850 Oakley
   portrait exists only at 577×754). Confidence: high.
3. **Prince Albert after Winterhalter, c.1845–50** (PD, Royal Collection;
   `images/S05-prince-albert-after-winterhalter-c1850.jpg`). Confidence: high.
4. **Paris 1849 exhibition building, bird's-eye engraving, Champin/
   Quartley** (CC0, Musée Carnavalet;
   `images/S05-paris-1849-exhibition-birdseye-carnavalet.jpg`, 3000×2525).
   **Better version** — see section C. Confidence: high.
5. **Society of Arts at the Adelphi, Microcosm of London plate, 1810**
   (PD; `images/S05-society-of-arts-adelphi-microcosm-1810.jpg`). The
   institution and rooms are right; the image is 40 years early — no
   1840s–50s image of the Society in session was found. Confidence:
   medium-high, date flagged.

### S13 — Hyde Park, summer 1850: the site as work began → CP006, CP010, CP016, CP017
1. **"Raising the Ribs of the Transept Roof", ILN full-page plate,
   14 Dec 1850** (PD; `images/S13-iln-1850-12-14-raising-transept-ribs.jpg`,
   4088×6168). The rib pair going up over the enclosed elm. Confidence:
   high — but December 1850, works at full stretch, **not** the summer
   start; the notes refuse to back-date it.
2. **ILN p.452, same issue: Prince Albert's visit to the works + moving a
   pair of transept ribs** (PD;
   `images/S13-iln-1850-12-14-visit-of-prince-albert-to-works.jpg`).
   Confidence: high.
3. **ILN p.454 construction account** (PD;
   `images/S13-iln-1850-12-14-construction-account.jpg`) — contemporary
   text: 24 ft column bays, three tiers — independently consistent with
   Downes. A document page, included for citation.
4. **Competition site plan of the empty site, 1850** (PD;
   `images/S13-site-drawing-great-exhibition-competition-1850.jpg`).
   Confidence: medium (Dutch-lettered continental impression; a diagram,
   not a survey).
**Nothing usable for the first works themselves:** no image of hoardings,
setting-out, trenching or foundations in summer/autumn 1850 exists in the
allowed sources. ILN issues of 21 Sept, 19 Oct, 2 Nov, 23 Nov 1850 were
checked on IA — design articles and progress text only, no site-works
plate before 14 December. Photography of the site begins with the
finished building in 1851.

### S25 — The gapped timber floor → CP013, CP020
**Solved from the primary source.**
1. **Official Catalogue (1851), Introduction pp.62–63** (PD;
   `images/S25-catalogue-1851-introduction-p62.jpg`,
   `images/S25-catalogue-1851-introduction-p63.jpg`). Quoting Paxton's own
   account: boards **1½ in thick laid ½ in apart**, dust falling through
   the interstices, washed water "disappears between the openings";
   joist/sleeper sizes and the 772,784 sq ft ground-floor area.
   Confidence: very high — the description the film's claim rests on.
No Downes plate shows the ground-floor boarding (the folio is ironwork
and glazing). Round 1's "Testing the Gallery Floor" is the *gallery*
floor — a different floor; do not use it for this claim.

### S34 — The 1851 admission tariff and shilling days → CP026, CP044
1. **Season Ticket No. 1 in its case, signed "Albert"** — V&A O1439451,
   two photographs (© V&A photographs; object PD; non-commercial terms —
   confirm before commercial use;
   `images/S34-va-season-ticket-no1-in-case.jpg`,
   `images/S34-va-season-ticket-case-exterior.jpg`). Confidence: very high.
2. **Official Catalogue p.28** (PD; `images/S34-catalogue-1851-introduction-p28.jpg`):
   season tickets **£3 3s gentleman / £2 2s lady**; £1 days, 5s day; 1s
   from day 22; Sundays closed.
3. **Official Catalogue p.29** (PD; `images/S34-catalogue-1851-introduction-p29.jpg`):
   the tariff in force from day 22 — **Mon–Thu 1s, Fri 2s 6d, Sat 5s**;
   "No change will be given at the doors." The definitive shilling-days
   page. Confidence: very high.

### S37 — The Punch naming item → (reference; no direct CP scene)
**Solved, with the premise corrected.** The naming item is **not a
cartoon**: it is Douglas Jerrold's prose letter as "Mrs Amelia Mouser",
*Punch* vol. XIX, **13 July 1850, printed p.21** (PD;
`images/S37-punch-1850-07-13-mouser-letter-p21.jpg`, visually verified):
a dream of walking in "**a palace of very crystal**". The page gives the
descriptive phrase, not yet the capitalised proper name; the rival
Thackeray attribution has no page evidence.
The same issue's p.22 holds a genuine Punch cartoon (a palm-house design
"humbly submitted" to Prince Albert; `images/S37-punch-1850-07-13-cartoon-p22.jpg`)
— included for the visual, explicitly **not** the naming item.

### S41 — Paxton's winter-garden plan, 1851–52 → CP030
1. **A Medical Man's Plea for a Winter Garden in the Crystal Palace
   (1851), pp.3 and 10** (PD, Wellcome/MHL;
   `images/S41-medical-mans-plea-winter-garden-p3.jpg`,
   `images/S41-medical-mans-plea-winter-garden-p10.jpg`). Builds expressly
   on Paxton's proposal ("Addition to the arguments of Denarius and
   Mr. Paxton in favour of a Winter Garden in London"). Confidence: high.
2. **The Crystal Palace and its Contents (1852), p.51** (PD;
   `images/S41-crystal-palace-and-contents-1852-p51.jpg`): the Kingsland
   public meeting resolving to petition Parliament to preserve the palace
   "as a winter garden". Confidence: high.
3. **Routledge's Sydenham guide (1854), p.11** (PD;
   `images/S41-routledge-1854-removal-chapter-p11.jpg`): retrospective of
   the whole retention debate, name-checking the "Denarius" pamphlet.
   Corroboration, not an 1851 artefact. Confidence: high.
**Not found:** Paxton's own *What is to Become of the Crystal Palace?*
(1851) as an open scan — exhaustive IA searches logged in the manifest
notes; a copy is at the Royal Collection (RCIN 6006621), not openly
downloadable. The often-cited "ILN 5 July 1851 p.11" winter-garden image
could not be verified — the IA copy of that issue does not contain it.

### S44 — The Sydenham/Norwood ridge before the palace → CP033
**Honest gap.** No genuinely pre-palace (1840s–1852) map of the ridge
exists in any allowed open source: Commons categories and searches,
Wyld's *Environs* 1840 (auction copies only), Penge Place sale particulars
(no open scan), Ordnance Survey (the ridge is outside the 1848–51 London
town-plan coverage; county series is 1860s). Delivered as the sanctioned
fallback:
1. **Phillips 1854, Delamotte folding route map** (PD;
   `images/S44-phillips-1854-route-map.jpg`) — the ridge country and the
   site on the hilltop. Caveat: it shows the site *with* the palace
   (1854); it evidences ridge geography, not the pre-1852 landscape.
2. **Phillips 1854, "The Site" page** (PD;
   `images/S44-phillips-1854-the-site-page.jpg`) — the contemporary
   verbal fixing of the site's topography.

### S15 — Fox, Henderson & Co.'s London Works, Smethwick → CP011
**No period view of the works exists in any allowed open source**
(Commons incl. Smethwick categories, IA, SMG all searched). Delivered
instead the firm's own dated documents from the works:
1. **Bow-string Bridge Ribs (1849), title page** (PD;
   `images/S15-fox-henderson-bowstring-title-1849.jpg`) — published from
   the "London Works, near Birmingham".
2. **The same pamphlet, p.16** (PD;
   `images/S15-fox-henderson-bowstring-proof-1849.jpg`) — the public
   proof trial of a rib at the works, 6 Sept 1849, observed by Cowper
   and Rankine. Confidence: high as documents of the firm; not pictures
   of the premises.

### S19 — Chance Brothers' glassworks → CP011
1. **Salt-print photograph of Chance's great flint-glass disc, 1851**
   (CC0, Rijksmuseum; `images/S19-chance-flint-glass-disc-1851.jpg`,
   4900×5760). The works' most famous product as exhibited. Confidence: high.
2. **ILN, 17 April 1852, p.301** (PD;
   `images/S19-iln-1852-chance-reference.jpg`) — names L. Chance,
   "the manufacturer of the glass for the Crystal Palace", and his "two
   gigantic manufactories".
3. **URL-only:** the ILN's own engravings of Chance's manufactory,
   21 Dec 1850 — they exist (the 1852 page cites them) but IA holds that
   issue only as a loan-restricted scan; no openly downloadable copy
   found. Commons/SMG hold only modern photographs and glass samples.

### S45 — The decision, the debate, the sale → CP030, CP031
Round 1 found nothing here. The contemporary paper trail now:
1. **Phillips 1854, Introduction pp.13 and 15** (PD;
   `images/S45-phillips-1854-history-leaf18.jpg`,
   `images/S45-phillips-1854-history-leaf20.jpg`) — the official
   commission on the building's future; Leech's rescue scheme; the
   Company's formation and prospectus (£500,000 in 100,000 £5 shares).
2. **ILN, 1 May 1852, p.335** (PD;
   `images/S45-iln-1852-sale-70000-report.jpg`) — after the Commons vote,
   sale to private parties at **£70,000** conditionally accepted;
   "the work of removal will commence on the 11th of May".
3. **The Removal of the Crystal Palace (penny pamphlet, 1852), title
   and p.1** (PD; `images/S45-removal-pamphlet-1852-title.jpg`,
   `images/S45-removal-pamphlet-1852-page1.jpg`) — quotes the Commons
   debate of 29 April 1852. A Sabbatarian argument about the removal
   debate — **not** an official or contractor's record, and round 1's
   catalogue entry for it should not be cited as one.
4. **ILN, 28 Feb 1852, p.175** (PD;
   `images/S45-iln-1852-feb-auction-demolition-report.jpg`) — Fox &
   Henderson's auction catalogue leads the paper to infer demolition
   "already in progress". **That inference was wrong** (see
   Contradictions); the document itself is genuine.

### S46 — The transfer, the company, the site → CP032
1. **ILN, 15 May 1852, p.391** (PD;
   `images/S46-iln-1852-05-15-transfer-report-p391.jpg`) — the transfer
   executed in the Transept on 13 May: price paid, possession delivered;
   the purchasers' 150-acre Sydenham plans. Confidence: high.
2. **ILN, 22 May 1852, p.406** (PD;
   `images/S46-iln-1852-company-advertisement.jpg`) — the Company's own
   advertisement: in effect its prospectus notice (capital, directors,
   Paxton/Jones/Wyatt, Fox Henderson as re-erection contractors).
3. **ILN, 5 June 1852, p.441** (PD;
   `images/S46-iln-1852-06-05-sydenham-site-sketch.jpg`) — "Sketch on
   the proposed site of the Crystal Palace, Sydenham": the wooded Penge
   Place grounds before re-erection.
**Transport: nothing found.** No searched source describes wagons,
carts or trains carrying the parts. Phillips says only that Fox &
Henderson were instructed "to convey the palace". The storyboard's
two-site cut for CP032 is the honest treatment; the mechanics of the
move are undocumented in open sources.

### S47 — Re-erection begins → CP032, CP033
1. **Phillips 1854, Introduction p.17** (PD;
   `images/S47-phillips-1854-history-leaf22.jpg`) — "The first column
   of the new structure was raised by Mr. Laing… on the 5th August,
   1852." (Removal from Hyde Park began in May; August is the
   *re-erection* start — modern summaries that date dismantling to
   August conflate the two.)
2. **Negretti & Zambra stereoscopic interior, dated 1853** (CC0;
   `images/S47-sydenham-interior-stereo-1853.jpg`) — the building under
   fit-out before opening. Museum dating; treat as the publisher's date.

### S51 — The two water towers → CP042, CP062, CP064
1. **Delamotte, south tower from the Water Temple** (PD;
   `images/S51-delamotte-south-tower-from-water-temple.jpg`) — the
   tower clear of the transept roofline: the height-against-building
   evidence the scene wants. **Dating caveat:** Commons dates these
   views 1854, but Brunel's towers were begun Aug 1854 and operational
   2 June 1856 (Historic England) — recorded as c.1854–1856; do not
   caption them 1854.
2. **Delamotte, north tower from the south wing** (PD;
   `images/S51-delamotte-north-tower-from-south-wing.jpg`). Same caveat.
3. **Garden-front photograph, Rijksmuseum, dated 1878–1890** (CC0;
   `images/S51-garden-front-tower-height-comparison.jpg`, 2500×1676) —
   the clearest tower-vs-nave height comparison, a generation later.
**No openly licensed Brunel drawing of the towers exists** in the
permitted sources (ICE holds material without an open licence). Tower
facts for the script: 86 m / 282–284 ft, 12 cast-iron columns on a
concrete ring (Historic England) — note the sources disagree on the
foot figure (282 / 284; ILN 1941 says 280).

### S52 — The prehistoric islands in the 1850s (period views only) → CP034, CP043, CP067, CP074
1. **Wellcome V0013783, coloured print** (CC BY 4.0;
   `images/S52-wellcome-palace-and-geological-islands.jpg`, 3392×2301) —
   the palace and terraces with Hawkins's models on the islands in the
   foreground; the only true "models in their landscape as built" view
   found. Wellcome dates the print "later than 1854?"; content confidence
   high, exact print date medium.
2. **Owen, Geology and Inhabitants of the Ancient World (1854), p.20 —
   Megalosaurus** (PD; `images/S52-owen-1854-megalosaurus-p20.jpg`) —
   the official handbook's woodcut of the restoration as built.
3. **Same volume, p.36 — Labyrinthodon** (PD;
   `images/S52-owen-1854-labyrinthodon-p36.jpg`).
Already in round 1 (not re-downloaded): the ILN 31 Dec 1853 model-room
engraving (models under construction), held as a Smithsonian 1900
reproduction. **Trap avoided:** Commons's "Iguanodon Model 1–6 (1854)"
files are modern photographs of a 1/12-scale model — excluded.

### S53 — The dinner inside the Iguanodon, 31 Dec 1853 → CP034
1. **ILN, 7 January 1854, p.22, full page** (PD;
   `images/S53-iln-1854-01-07-iguanodon-dinner-page.jpg`, 4113×5936) —
   the engraving **and** the report (the pterodactyl-wing invitation;
   Owen at the head of the table). The primary record every later
   account derives from. Confidence: certain. (Hawkins's own letter
   misdates this report "July 7 1854" — it is 7 January.)
2. **The same woodcut, tighter** (PD;
   `images/S53-iln-iguanodon-dinner-woodcut.jpg`) — catalogued in
   round 1 but never downloaded. Confidence: certain.
Hawkins's own sketch of the dinner (BL Add MS 50150) was logged, not
copied — no open licence for the manuscript image could be verified.
The dinner was in the *mould*, as the storyboard's CP034 has it.

### S55 — Opening of the Sydenham palace, 10 June 1854 → CP035
1. **Delamotte photograph of the opening ceremony in the centre
   transept** (CC0, Met DP109644;
   `images/S55-delamotte-opening-ceremony-1854.jpg`, 3101×3912). The
   event itself. (The Met's title says "Reopening… Reconstructed" —
   1854 was the first Sydenham opening; the 1920 reopening is a
   different event with different photographs.) Confidence: certain.
2. **Souvenir lithograph, "Inaugurated by Her Majesty 10th June 1854"**
   (CC BY-NC-SA 4.0, Science Museum Group;
   `images/S55-smg-inauguration-lithograph-1854.jpg`). A document of
   the opening, but **partly anticipatory as a depiction**: it shows
   both towers complete and the fountains playing — neither true until
   June 1856. The NC licence is recorded in the manifest.

### S57 — Sydenham in the 1850s → CP036–CP041, CP045
1. **Delamotte, the planted nave, 1854** (CC0, Met DP109633;
   `images/S57-delamotte-planted-nave-1854.jpg`, 2651×3976). The
   definitive 1850s nave interior. Confidence: certain.
2. **Delamotte, sculpture gallery, 1854** (CC0, Met DP109630;
   `images/S57-delamotte-sculpture-gallery-1854.jpg`) — statues in
   rows during installation.
3. **Bedford/Delamotte, Roman Court, 1854** (CC0, BL;
   `images/S57-roman-court-1854.jpg`) — a Fine Arts court as opened.
4. **Delamotte, general view from the Water Temple, 1854** (PD;
   `images/S57-delamotte-general-view-water-temple-1854.jpg`, 928×706 —
   low resolution is its only weakness).
5. **Negretti & Zambra stereo interior, dated 1853** (CC0;
   `images/S57-negretti-zambra-interior-1853.jpg`) — the earliest
   interior photograph found; fitting-out, not the finished interior,
   and captioned here as such.
Kept out deliberately: the Rijksmuseum "Stereoscopic Illustrations"
series that sounds 1850s is dated by the museum c.1870–1890.

### S67 — The fire of 30 December 1866 → CP047, CP048
1. **ILN, 12 January 1867, full-page engraving of the ruins** (PD;
   `images/S67-iln-1867-01-12-fire-ruins-engraving.jpg`, 4136×5904) —
   the Abu Simbel colossi amid twisted girders and rubble. The best
   picture of the destruction. Confidence: certain.
2. **Same issue, p.42** (PD; `images/S67-iln-1867-01-12-fire-account-p42.jpg`) —
   the contemporary account page, with a small plan diagram of the
   damaged part.
3. **URL-only (2):** Historic England OP04456 and BB92/15895 — genuine
   post-fire photographs (twisted metal; snow on damaged court walls),
   no open licence found; recorded, not downloaded.
Note: the fire was 30 **December 1866**; most print coverage is
January 1867, and some secondary sources (Citizendium) drift it into
1867 outright.

### S70 — FA Cup finals at the Crystal Palace → CP050, CP055
All public domain:
1. **1905 final panorama** (`images/S70-fa-cup-final-1905-panorama.jpg`,
   2157×760) — round-1 catalogue entry, first download.
2. **1913 final programme cover** (`images/S70-fa-cup-final-1913-programme.jpg`) —
   Aston Villa v Sunderland, 19 April 1913.
3. **1901 final photograph** (`images/S70-fa-cup-final-1901-photo.jpg`).
4. **1899 final illustration** (`images/S70-fa-cup-final-1899-illustration.jpg`).
5. **1906 fans photograph** (`images/S70-fa-cup-final-1906-fans.jpg`).
**No open-licence photograph of the 1913 match itself exists** in the
allowed sources — only the programme; agency photographs are
commercial and were excluded per the rules.

### S83 — Demolition of the water towers, 1940–41 → CP064
**No openly licensed demolition photograph was found** (Commons, the
round-1 manifest, and two IWM collections searches — IWM returned only
its 1920–24 gallery material). What the record now establishes:
- **South tower: dismantled in sections, autumn 1940** (near houses).
- **North tower: blown up by the Royal Engineers, 16 April 1941.**
  A photograph of that demolition exists in the Surrey Archaeological
  Society Bulletin 321 (Ted Coles) — **URL-only**, licence not stated.
- The ILN's April 1941 photo feature "The Crystal Palace North Tower
  to Go" survives only in the commercial ILN/Mary Evans archive —
  URL-only. Historic England list entry 1469984 is the official
  reference — URL-only.
- Downloaded: **the surviving south-tower base, photographed 2022**
  (CC BY-SA 4.0; `images/S83-south-water-tower-base-2022.jpg`) — the
  present-day evidence for CP062/CP064 treatments.
Some web retellings reverse the towers' order or claim the south tower
fell "shortly after the 1936 fire" — contradicted by the SAS account
and the Historic England listing.

### S87 — The Crystal Palace subway → CP046, CP065, CP071
1. **OS 25-inch plan of High Level station, 1895** (PD;
   `images/S87-os-plan-high-level-station-1895.png`) — shows the
   subway under the Parade; round-1 entry, first download.
2. **ILN engraving of the new High Level station, 30 Sept 1865** (PD;
   `images/S87-high-level-station-iln-1865.jpg`) — the station the
   subway served. **No Victorian image of the subway itself exists**
   in the sources.
3. **Conservation photographs:** interior 2016, pre-restoration (CC
   BY-SA 4.0; `images/S87-subway-interior-2016.jpg`); east courtyard
   during restoration, 2023 (CC BY-SA 4.0;
   `images/S87-subway-east-courtyard-2023.jpg`); restored interior,
   Jan 2025 (CC BY-SA 2.0; `images/S87-subway-restored-interior-2025.jpg`).
   These date the PARK-NOW scenes (CP071) honestly: the subway's
   present state is *restored 2023–24*, and access is not continuous.

### S89 — National Sports Centre, 1960s → CP066
**Nothing usable.** Commons and the round-1 catalogue hold only modern
photographs of the 1964 building; no 1960s image under an open licence
was found. The scene was optional in the brief; the storyboard keeps
it (CP066, book-covered), so this stays an open evidence gap — period
photographs exist in architectural-press and Historic England holdings
but not under terms the brief allows.

---

## B. The Sydenham plans

| Plan / section | Year it shows | Good for | Resolution |
|---|---|---|---|
| 1856 guide, ground plan (round 1, gallery 0205) | 1856 | Route drawing; courts; entrances | 5,669 × 2,763 |
| **1856 guide, "Plan of Palace and Park"** (round 2, `S56-plan-1856-guide-palace-and-park.jpg`) | 1856 (state of 1854–56) | **Best single route base**: building + terraces + fountains + lakes + geological islands on one dated sheet; key names the Railway Colonnade | 2,760 × 3,976 |
| 1856 guide, transverse section (round 1, gallery 0212) | 1856 | Heights; section | (round 1) |
| **Phillips 1854, foldout ground plan** (round 2, `S56-plan-1854-phillips-ground-plan.jpg`) | **1854, as opened** | Route drawing with the fullest key (courts 1–29, statues A–Z); **fire marking** (north transept + north wing present); station entrance | 4,227 × 2,169 |
| **Phillips 1854, routes-to-the-palace map** (round 2) | 1854 | Railway-arrival context (the journey across south London) | 2,528 × 2,032 |
| **Phillips 1854, "View of Building from the North"** (round 2, `S66-view-1854-phillips-building-from-north.jpg`) | 1854 | The north end **before** the fire — pairs with the post-fire plan | 2,127 × 3,220 |
| **Phillips 1854, Alhambra court plan** (round 2) | 1854 | Court plan, opening-year state (cf. round 1's 1856 printing, 0246) | 2,127 × 3,220 |
| **Routledge 1854, grounds foldout** (round 2, `S62-plan-1854-routledge-grounds-terraces-islands.jpg`) | 1854 (some features "not completed" — as projected, flagged) | Grounds/terraces/fountains; the clearest 1854 layout of the geological islands, animals keyed | 2,407 × 1,734 |
| **Grounds map, c.1862** (round 2, `S62-plan-1862-crystal-palace-grounds-map.jpg`) | c.1862 | Grounds in neighbourhood context; mid-life park state. Round 1 catalogued it but never downloaded it (0 bytes) | 2,020 × 2,896 |
| **1878 official guide, ground plan** (round 2, `S66-plan-1878-guide-ground-plan-post-fire.jpg`) | **1878, post-fire** | **Fire marking (the after-state)**: north transept gone, "Tropical End"/Orangery; the only plan labelling **both** railway entrances (High Level 1865 + Brighton low-level) | 1,571 × 2,611 |
| 1856 guide, Screen of Kings and Queens elevation (round 2) | 1856 | Interior elevation detail | 2,960 × 2,080 |
| Dimension evidence pages: Phillips 1854 p.28; Routledge 1854 pp.25–26, p.125 (round 2) | 1854 | **Heights cross-check** (below) | 2,127 × 3,220 / 1,753 × 3,134 / 1,839 × 3,124 |

**The complete 1856 guide:** not on the Internet Archive at all. The
complete book (197 pp. + 2 maps) is the Polona scan mirrored in the
Commons category. Round 1's 117 files end at printed p.125; all 73
remaining pages were triaged this round — almost entirely text. Their
only drawn matter is the "Plan of Palace and Park" and the Screen
elevation, both downloaded. The guide's court plans all sit in the part
round 1 already has. No higher-resolution copy of the 5,669 × 2,763
ground plan exists (that *is* the full Polona scan).

**Heights cross-check** (the brief asked for a second source; two were
found, and they agree with each other):

| Quantity | 1856 guide table (round-1 JSON) | Phillips 1854, p.28 | Routledge 1854, pp.25–26, 125 |
|---|---|---|---|
| Nave above ground floor | 110 ft 3 in | **104 ft** to crown (springs 68 ft + 36 ft radius) | crown **104 ft** implied by same geometry |
| Central transept above ground floor | 174 ft 3 in | **168 ft** to top of louvre (springs 108 ft) | crown **168 ft 3½ in**; 176 ft 7½ in incl. open louvre |
| From below | 197 ft 10 in "from the basement" | 208 ft from the garden front | 200 ft 2½ in from garden-front ground (basement floor 23 ft 7 in deep) |

The 1854 pair are independent of each other (official handbook vs.
commercial rival) and internally consistent with the drawn geometry
(springing + radius). The 1856 table runs ~6 ft higher on both headline
figures — a consistent shift suggesting a different datum, but no 1856
text states one, so it is **unresolved**: 104 ft / 168 ft are the
drawing-supported figures. The "from below" figures are
datum-incomparable and should only ever be quoted with their datum.
Phillips 1854 is also internally inconsistent (his p.24 "44 ft higher
than Hyde Park's nave" matches neither his own 104 ft nor the 1856
figure) — promotional rounding is at work in all three books.

**Documented plan gaps:** no drawn **1854 section** exists in Phillips,
Routledge or the 1854 Expositor (the only Sydenham section remains
round 1's 1856 one); no post-fire plan earlier than **1878**; no
standalone railway-arrival plan sheet (arrival is covered inside the
plans above, plus Phillips's colonnade dimensions in text: 720 × 17 ×
18 ft); the 1857 park plan's Commons original is only 1,483 × 1,896 —
no better version exists. One further observation from the guide's
late pages: by 1856 the north transept was already partitioned from
the nave by "a gigantic curtain" (p.148, the Tropical End) — the 1856
state is not a fully open three-transept interior.

---

## C. Better versions of pictures already collected

- **Paris 1849 building (S05):** round 1's file (gallery 0322) is only
  a *plan* of the 1849 building. The Carnavalet bird's-eye engraving
  (CC0, 3000 × 2525) is the pictorial version — downloaded as
  `S05-paris-1849-exhibition-birdseye-carnavalet.jpg`. Keep both.
- **Actually-downloaded at last:** several round-1 records were
  catalogue entries with status skipped-budget (0 bytes) that a title
  list makes look collected. This round downloaded them for the first
  time: the Chatsworth Victoria Regia House engravings (S03), the
  c.1862 grounds map (B), the 1905 FA Cup panorama and the 1895 OS
  station plan (S70/S87), and the ILN Iguanodon-dinner woodcut (S53).
- **Checked, no better version exists:** the 1856 ground plan
  (5,669 × 2,763 is the full Polona scan; no IA copy) and the 1857
  park plan (Commons original 1,483 × 1,896, identical to round 1's).

---

## Scenes with nothing usable — and where we searched

| Gap | Searched |
|---|---|
| First-works images, Hyde Park, summer 1850 (S13) | Commons (construction/foundations queries); ILN Sept–Nov 1850 issues on IA read for plates |
| Transport of the parts, Hyde Park → Sydenham (S46) | ILN vol. 20 (1852) full-text index of all 515 leaves, 57 palace hits read; Phillips 1854 introduction; Company prospectus searches on IA. ILN vol. 21 (Jul–Dec 1852) exists only as loan-restricted scans — the dismantling's later stages could not be checked in an open copy |
| Any image of the building being taken down (S45) | Same ILN trawl; Commons; no dismantling image exists in the open sources |
| Pre-1852 map of the Sydenham ridge (S44) | Commons map categories/searches; Wyld 1840 (commercial only); Penge Place sale particulars (no open scan); OS coverage (town plans don't reach the ridge; county series 1860s) |
| Paxton's own winter-garden pamphlet (S41) | IA title/creator/phrase searches, all fruitless; Royal Collection copy not openly downloadable |
| Period view of Fox, Henderson's works (S15) | Commons (Smethwick categories), IA, SMG |
| Chance's manufactory engravings, ILN 21 Dec 1850 (S19) | IA holds the issue loan-restricted only; open DLI ILN set lacks vol. 17 |
| Brunel tower drawings (S51) | Commons, SMG, Wellcome, V&A via search; ICE holds material, no open licence |
| 1913 FA Cup Final match photograph (S70) | Commons and open collections; only the programme is open — match photography is agency/commercial |
| Water-tower demolition photographs (S83) | Commons, round-1 manifest, two IWM collections searches (1920–24 material only); SAS Bulletin photo and ILN 1941 feature recorded URL-only |
| 1960s National Sports Centre images (S89) | Commons, round-1 catalogue — modern photographs only |
| Drawn 1854 Sydenham section (B) | Phillips 1854 (all plate leaves), Routledge 1854, the 1854 Expositor |
| Post-fire plan before 1878 (B) | IA guide/handbook search 1860–1885 |

---

## Contradictions with the existing collection and scene list (reported, not fixed)

1. **Sydenham heights.** The 1856 table behind
   `dimensions-from-1856-guide.json` (nave 110 ft 3 in; transept
   174 ft 3 in) is contradicted by two independent 1854 sources and by
   the drawn arch geometry (104 ft / 168 ft). See section B.
2. **Image count.** Repo README and `MUSE-PROMPT.md` say the round-1
   collection has 1,393 images; the repo actually holds **1,398**
   (REVIEW.md agrees with 1,398).
3. **The Punch premise.** The brief's S37 (and popular accounts) call
   the naming item a cartoon; it is Jerrold's prose letter, 13 July
   1850, p.21. The phrase on the page is "a palace of very crystal",
   not yet the proper name. The rival Thackeray attribution has no
   page evidence.
4. **Floor boards.** Modern summaries give board *widths* (22 cm /
   9 in) with a ~½ in gap, disagreeing with each other. The 1851
   Catalogue quoting Paxton gives board **thickness** 1½ in and a
   ½-inch gap, no width. Use the primary figures (CP013/CP020).
5. **Season tickets.** Secondary sources flatten the price to "two
   guineas"; the Catalogue gives £3 3s (gentleman) / £2 2s (lady).
   One modern summary claims 1s admission "on Sundays" — the
   Exhibition was closed on Sundays (Catalogue p.28).
6. **"Demolition already in progress", Feb 1852.** The ILN inferred it
   from an auction catalogue; the building was in fact sold intact in
   May 1852 and re-erected. Any script line dating demolition to
   February 1852 would be wrong (CP031).
7. **Removal vs re-erection dates.** Removal was announced to begin
   11 May 1852; the first Sydenham column was raised 5 Aug 1852.
   Summaries dating the *dismantling* to August conflate the two
   (CP031/CP033).
8. **The removal pamphlet's date.** IA metadata says 1851; the title
   page reads 1852 and the text quotes the 29 April 1852 Commons
   debate. It is also a Sabbatarian pamphlet about the debate — round
   1's catalogue record carries bookseller subject headings and should
   not be cited as an official removal record.
9. **Tower demolition order and method.** South tower: dismantled in
   sections, autumn 1940. North tower: blown up, 16 April 1941. Web
   retellings that reverse this, or date the south tower "shortly
   after the 1936 fire", are contradicted by the SAS account and the
   Historic England listing (CP064). Tower height is variously 280 ft
   (ILN 1941), 282 ft, 284 ft, 86 m — unresolved.
10. **Towers and fountains "1854".** Commons dates the Delamotte tower
    views 1854 and the SMG inauguration lithograph shows the finished
    towers and playing fountains on 10 June 1854; the towers were
    operational 2 June 1856 and the fountains first played 18 June
    1856 (CP035/CP042 must exclude both from opening views).
11. **Routledge's "Central Dome".** A Routledge passage giving a
    160–170 ft "Central Dome" describes the **rejected 1850 Building
    Committee design**, not Sydenham. Routledge also reverses the Hyde
    Park widths (456/408); the 1856 assignment (408 general / 456
    greatest) stands.
12. **Fire-date drift.** The north-transept fire was 30 Dec 1866;
    some secondary sources place it "in 1867" because the print
    coverage is January 1867 (CP047's date stands).
13. **Met title wording.** DP109644's "Reopening of the Reconstructed
    Crystal Palace" describes the **1854 first opening** at Sydenham;
    the 1920 reopening is a different event (some of its photographs
    are in round 1).
14. **Catalogued ≠ collected.** Round 1's manifest lists items (the
    Chatsworth lily-house engravings, the c.1862 grounds map, the
    1905 panorama, the 1895 OS plan) with status skipped-budget —
    present as records, absent as files until this round. Any future
    audit should count `status = downloaded` rows only.
