# Crystal Palace film — build plan (draft, 2026-10-26)

Status: draft plan, not a render instruction, not an approved edit.
Governing scene list for building: **CP001–CP076, storyboard v001**
(3,541 words, central estimate 31:35 at 140 wpm plus 342 s of holds;
range 28:33–34:02 at 125–155 wpm). The S01–S94 story-walk list is the
research inventory behind this plan, mapped to CP scenes in
`GAPS-FOUND.md` (appendix) and in `SCENE-ASSET-SHEET.md` in this folder.
If the S list is ever made governing instead, the mapping already exists;
nothing in this plan depends on a scene number alone — every build unit
is tied to a dated, sourced visual.

Source of narration: the v001 voiceover (3,541 words). No narration is
rewritten in this plan, and no new audio is generated until the
voiceover text is approved for recording. Timing is planning only until
a recorded voiceover exists.

## Hard rules carried into the build (from REVIEW.md and GAPS-FOUND.md)

- Hyde Park 1851 and Sydenham 1854–1936 are **two different buildings**.
  Never blend them in one image, one caption, or one 3D shot.
- **No Sydenham 3D.** There is no verified dated Sydenham model.
  Sydenham is built from plans, photographs, engravings, and cards only.
- Hyde Park 3D is the existing west-half iron frame only: 37 of 77 bays,
  888 ft of the west half, unfinished frame — missing envelope, glazing
  detail, transept, colour, exhibits, site work. It is labelled as a
  partial reconstruction wherever it appears. It is not finished, and
  this plan does not promise to finish it.
- A publication year is not the depicted year. Every caption states the
  date the work was **made**, the building it shows, and the source.
- New York Crystal Palace and Kroll Wintergarten (Berlin) are out.
- Licence unclear means unclear (two V&A Delamotte photographs, V&A
  season ticket, Historic England Archive leads). Nothing licence-unclear
  goes into a rendered cut until its terms are confirmed.
- No 3D files, no .zip files, no file over 50 MB in this round's folder.
  Work is on branch `muse-round2` only; never main, never merge,
  never force-push.

## What is being built, in one paragraph

A book-led walkthrough film, 76 short scenes, built as: (1) a scene
asset sheet tying every passage to a verified visual, (2) a three-state
plan sequence for the Sydenham route (pre-fire 1856, 1866 fire extent,
post-fire Ordnance Survey), (3) Hyde Park 3D inserts only where the
partial frame honestly serves the scene, (4) text cards where no honest
visual exists, and (5) a watchable narrated slate cut for review — no
4K final, no publication, until Bear has seen the slate cut.

## Build units (the same for every scene)

Each scene is built as one unit: primary visual, backup visual or card,
on-screen label (building, date made, source), narration beat from the
v001 voiceover, and a hold. A scene is "built" only when its visual is
in the repo (round 1, round 2, or the parallel writer's additions once
they are inventoried), its caption is written from its manifest row,
and its licence is open or confirmed. A scene with a card instead of a
visual is still a built scene — the card says what is missing and why,
it does not fake a picture.

## Passage build table

| Passage | Scenes | Build approach | Assets ready | Gaps / fallbacks |
|---|---|---|---|---|
| Prologue / context | CP001–CP004 | Still images, slow holds. Britain 1850 panorama + cholera balance image; Chatsworth lily plates for the Paxton origin | S04 panorama, King Cholera 1852; S03 ILN 1849 lily, Hooker/Fitch 1851 plates, Latham conservatory photo (later photo, captioned as such) | CP004 omits the lily-leaf anecdote on purpose — do not reintroduce it from the S03 files |
| Proposal | CP005–CP009 | Portraits + Paris 1849 views + cards. Portraits are available but CP005 says no likeness is required, so portraits are optional dressing, not load-bearing | S05 Albert (1840/1845/1848), Paxton (c.1843/c.1850/1865), Cole 1852 (lead), Society of Arts 1809; Paris QB.726/QB.727 (CC0, print dates unknown, captioned as unknown) | S15 Fox, Henderson works: **no image — card**. Do not substitute a Chance photograph (different firm) |
| Building the glass hall | CP010–CP020 | Hyde Park partial frame + Downes plates (round 1) + description pages. No finished-building render is promised | Downes 1852 plates (round 1); S25 Wyatt + Ackermann floor pages (½ in gaps, ground floor only); S19 Chance flint-glass disc 1851 (artefact, not works view) | S13 first-works view: **no construction image — elm context image + card**. First column 26 Sep 1850 is a secondary-source date anchor, not an image |
| Great Exhibition | CP021–CP029 | Routledge/Tallis (round 1) + shilling-day etchings | S34 Cruikshank "Going In"/"Coming Out" 1 Jul 1851, first shilling day 26 May 1851 | Visits ≠ visitors (6m+ visits, CP029); V&A season ticket is licence-unclear, not in the cut |
| Move / rebuilding | CP030–CP035 | Winter-garden pages + dismantling page + ridge maps + dinosaur engravings + opening spread | S41 Haden 1851 + Dilke 1855; S45–S47 ILN 30 Oct 1852 p.360 (one page serves all three); S44 Greenwood maps 1822–1829 (not Ordnance Survey); S52/S53 dinosaur material; S55 ILN 1 Jul 1854 opening spread | S44 site plan of Penge Common itself: **not found — ridge maps + card**. Paxton's own pamphlet not found as a downloadable copy (Royal Collection lead only) |
| Early Sydenham | CP036–CP046 | **Route plans first, photographs second.** No Sydenham 3D anywhere in this passage | S57 Negretti & Zambra Rijksmuseum interiors (1854 Egyptian Court lead; 1853 interior, year by museum dating); S51 Delamotte tower views (date 1854–1859, not 1854); S55 Delamotte opening photo; S87 1895 High Level plan + 1908 station photo | S51 Brunel tower drawing: **not found under an open licence — photographs + card**. S52 completed-islands photograph: **not found — engravings + card** |
| Damage / adaptation | CP047–CP057 | Fire plan + FA Cup programmes/panorama + cards for unverified items | S67 ILN 12 Jan 1867 ruins engraving + tinted fire-extent ground plan; S70 1905 panorama, 1899 illustration, 1904/1913 programmes | S70 1913 match photograph: **not found — programme + 1905 panorama, never presented as a 1913 photo**. CP056 HMS Victory V/VI: **omitted until verified** |
| Final fire | CP058–CP062 | 1936 material only, from round 1 / later inventory. **Never** an 1851 Downes section for a 1936 Sydenham fire | To be inventoried from round 1 before this passage is built (see Phase 1 check) | Ignition not established; no minute-by-minute spread; Churchill quotation omitted; "more than 90 years" not used (90th anniversary of 30 Nov 1936 had not occurred as of 26 Oct 2026) |
| Landscape after | CP063–CP067 | Post-fire plans + surviving bases + modern photographs, all labelled by date | OS Surrey Sheet 008 crop 1871–1882 (post-fire footprint, both railway lines); S83 tower bases 2002; S87 subway interior 2023 / entrance 2010 (conservation-era, labelled as such) | S89 National Sports Centre: **no 1960s photo — see decision note below**. No standalone post-1866 building plan (OS crop is the closest; it is a district sheet, not a palace plan) |
| Legacy | CP068–CP069 | Cards + surviving material, no invented scenes | Tower dates (autumn 1940 / 16 Apr 1941, Historic England 1469984) for CP064-adjacent legacy beats | IWM palace occupation, detailed Baird TV work, detailed Festival of Empire: **not narrated in the transcript — do not claim them as book scenes** |
| Surviving walk | CP070–CP076 | Present-day photographs + georeferenced plan, all labelled present-day | S87 subway modern photos; S44 ridge maps for CP072; S52/S53 surviving models (CP074) | Present-day access / subway opening / restoration status **not verified** (CP070–CP071) — captions state what is shown, not access status |

## The route build (highest priority, built first after the asset sheet)

The Sydenham route (S56–S66 in the research list) is built as a
**three-state plan sequence**, not one blended plan:

1. **Pre-fire state:** 1856 guide ground plan (round 1, Muse 0205,
   5669×2763) inside the building, plus 1856 Plan of Palace and Park
   (round 2, 2760×3976) for grounds, terraces, fountains, islands,
   railway colonnade and low-level station. This is the best
   route-drawing plan in the collection.
2. **1866 loss marked:** ILN 12 January 1867 p.42 ground plan, tinted
   portion = extent of the fire. The route line stops at the lost north
   transept; it does not draw through it as if intact.
3. **Post-fire state:** Ordnance Survey Surrey Sheet 008 crop
   (round 2, 2200×1900, 1871–1882) — post-fire footprint, both railway
   lines, High Level station and colonnade, terraces and fountains.
   Labelled as a district sheet crop, not a palace plan.

Supporting route plates, in the same sequence and never mixed into one
image: 1856 transverse section (round 1, 0212), 1856 court plans
(Egyptian 0226, Alhambra 0246), 1856 Secondary Island plate (round 2),
1854 Phillips railway routes map (round 2, leaf 6 — dashed railway was
proposed, not built; scan rotated, rotate clockwise to read), 1857
grounds plan (round 1), 1895 High Level plan (round 2, S87, low
resolution, station only), Festival of Empire 1911 map (round 1, grounds
in 1911). Dating guardrail: no 1854–1857 plan can show both railway
lines (High Level opened 1 August 1865); any plan showing both is 1865
or later.

Heights on the route plates and in narration state their datum every
time: 1854 Phillips guides give nave 104 ft / central transept 168 ft;
1856 guide gives 110 ft 3 in / 174 ft 3 in from ground floor — both gaps
exactly 6 ft 3 in, a datum difference, not rival measurements. The book's
rounded ~108 ft / ~168 ft is neither figure. 384 ft is two different
measures (1856 greatest width; 1854 central transept length) — never
equated. "82 years" = Sydenham; "85 years" = 1851–1936 overall; neither
is the age of one unchanged building.

## Phases (in order, no phase skipped)

- **Phase 0 — this plan.** Draft, for the record. Building proceeds
  from it without waiting for a second approval.
- **Phase 1 — asset sheet + caption set.** One row per CP passage
  (and per S scene where the mapping is 1:1): file path, date made,
  building shown, licence, caption line. Includes the inventory check
  for the final-fire passage (CP058–CP062) from round 1, and the
  parallel writer's additions to `muse-round2` once they settle —
  inventoried, not assumed. Licence-unclear items stay out of the cut.
- **Phase 2 — route plates.** The three-state plan sequence above,
  as labelled stills first. No animated route line is drawn until the
  court order of the route is defined from the 1856 plans; a route
  line drawn over the wrong court order would be a invented fact.
- **Phase 3 — Hyde Park inserts.** Partial-frame shots only, labelled
  partial, cut against Downes plates for the envelope and glazing the
  model lacks. No Sydenham 3D is built in any phase.
- **Phase 4 — assembly.** Scenes in CP order, narration beats from
  v001, holds per the v001 timing (342 s total holds), cards where
  the asset sheet says card. Output: a watchable narrated slate cut
  for review.
- **Phase 5 — review stop.** Slate cut delivered, building stops for
  Bear's verdict. No 4K final, no publication, no title/description
  changes on any public channel, until he has seen it.

## Decisions already made in this plan (not questions)

- CP001–CP076 governs the build; S01–S94 is the research inventory.
- Sydenham is plans/photographs/cards only; Hyde Park frame is partial
  and labelled as such.
- Cards are honest build units, not placeholders to be hidden: S13
  construction, S15 works, S44 site plan, S51 Brunel drawing, S52
  completed islands, S70 1913 photo, S83 demolition photo, S87
  19th-century subway interior, S89 1960s photo, post-1866 building
  plan — each gets a card or a labelled substitute, never a
  wrong-building or wrong-date picture.
- S89 note: the round-2 brief called it optional; v001 treats the
  National Sports Centre as a book-covered core scene (CP066). This
  plan builds it as a core scene with a card (no 1960s photo found;
  modern 2024 Commons photo is a "building today" fallback only, never
  captioned as 1960s) — the core/optional label does not change the
  visual, only whether the scene can be cut.
- S37 note: no Punch-naming scene was identified in v001. The Jerrold
  Mouser page (Punch vol. XIX, p.21, "a palace of very crystal") is
  built as a standalone naming beat and flagged as an omission from
  v001, not silently dropped and not forced into a CP number it does
  not have.
