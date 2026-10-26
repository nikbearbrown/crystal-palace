# Scene-based build plan — Muse's `models/` queue

Derived from the Crystal Palace film storyboard / executive sequence
v001 (26 October 2026): **76 scenes, CP001–CP076, 3,541 words,
central planning estimate 31:35**.

This plan is a build queue for `models/` only. It is **not** an approval
of the storyboard, not a render instruction, and not a claim that any
shell or scene below already exists. The storyboard itself is marked
planning only; after narration is recorded and approved, timings and
camera must be retimed to speech.

Scope rule (from `MUSE-PROMPT.md`): I build **individual objects,
components and dressing props** in `models/<slug>/` — `.blend`
(Blender 4.2+, metres, origin at base centre, scale applied), `.glb`,
front / side / 3-4 renders on a neutral grey backdrop, `refs/` list,
and `NOTES.md` stating what was measured, what was seen, and what was
guessed. I do **not** build full palace shells in `models/`, and I do
not edit anything outside `models/`.

Full shells are other work: the Hyde Park west-half frame lives in
`course-models/crystal-palace-1851-claude/` (37 of 77 bays, unfinished
— no transept, envelope, glazing detail, colour or exhibits yet), and
the large native scene in `blender-deliverables/` resembles Sydenham
only by visual inference and must never stand in for 1851
(see `references/muse-drive/review/REVIEW.md`, "What to keep separate").
My props are designed to plug into those shells and into future
Sydenham shells, not to replace them.

## Separation rule — read before building anything

Hyde Park 1851 and Sydenham 1854–1936 are **two different buildings**.
Never scale Hyde Park geometry into Sydenham, never reuse a Hyde Park
prop as Sydenham evidence, and never carry an intact North Transept
past CP047. Each prop is tagged HP or SY, and each NOTES.md names its
building and date state. Sydenham itself is not one frozen state:
CP035 (June 1854 opening) must exclude towers, fountains and wings
that are only evidenced later; CP042's waterworks state is
c.1856–1857, not June 1854; CP048 onward is post-1866.

Do not conflate scene IDs: this plan uses the v001 CP001–CP076 IDs.
The earlier 94-scene outline's S01–S94 IDs are independent.

## Build order — why this sequence

1. **Structural kit first.** One column, one bay and one joint unlock
   the largest block of scenes (construction, systems, exhibition,
   dismantling, and the CP068 engineering-explanation beat). A prop
   that only serves one scene waits behind a prop that serves ten.
2. **Centrepiece second, after a research spike.** The Osler fountain
   anchors CP021–CP023, but it is currently under-referenced — no
   dimensioned detail set was found in the manifest grep. Research
   before geometry, not geometry before research.
3. **Sydenham dressing third.** Court props are freestanding modules,
   because the storyboard itself flags court adjacency as unresolved.
   No prop assumes two courts are next door to each other.
4. **Ruin / present-day variants last.** They reuse earlier props in
   damaged or modern states, so they are cheap only after the intact
   props exist.

Per-prop budget (from `MUSE-PROMPT.md`): under ~50,000 triangles,
no file over 90 MB, no `.zip`. Every prop gets the same QC: renders
viewed against its reference, triangle count recorded, `.glb`
checked to export, `.blend` checked to open in Blender 4.2+.

---

## Wave 0 — in progress

### 0. `hyde-park-column-tier1` — HP tier-1 iron column + girder stub
- **Scenes:** CP010 (foundations / column positions), CP012 (one bay,
  then the next), CP014 (rain / hollow-column drainage explanation),
  CP017 (transept context), CP023 (nave colonnade), CP031
  (dismantling — the same joint, undone), CP068 (engineering
  explanation / structural bay study).
- **Status:** Built and QC-passed 2026-10-26. `.blend` (1.1 MB)
  and `.glb` (140 KB) exist; 21 objects, 2,560 triangles, height
  6.756 m. First renders came out blank grey (camera
  `rotation_quaternion` set while still in XYZ euler mode);
  fixed and re-rendered from the saved `.blend`, and all three
  re-renders were viewed: column, floor collar, collar rings,
  capital flange/bolts and triangular girder stub all visible.
  Girder top-flange/web gap is the stated Fig. 12 simplification
  (see NOTES.md QC section).
- **Evidence:** Downes Plate VIII (`references/downes-1852/
  source-scans/plates/plate-008.jpg`), Figs. 3/12/13; controls D06
  (24 ft bay), D10 (3 ft girder), D11 (22 ft 2 in girder top).
  Full dimension table, including what is nominal or inferred, is
  in `hyde-park-column-tier1/NOTES.md`.
- **Claimed in:** `models/CANDIDATES.md` row 1.

## Wave 1 — Hyde Park structural and fitout kit

These are the props that turn the column from a single object into
a usable bay, interior and exhibition.

### 1. `hp-glazing-and-sash-panel` — timber sash bars + glass panel
- **Status:** Built and QC-passed 2026-10-26. 5 panes between 6
  sash bars, 1.364 × 1.245 m, 13 objects, 156 triangles; renders
  viewed (face, edge, three-quarter). Bar centres 10½ in (Plate
  XII), glass length 49 in (printed p.15); bar section and glass
  thickness guessed — see `hp-glazing-and-sash-panel/NOTES.md`.
- **Scenes:** CP013 (iron, glass — and timber), CP016 (glazing at
  construction speed), CP052 (glazier repair, Sydenham-era reuse of
  the *technique*, not the HP panel as SY evidence).
- **Evidence to use:** Downes plates XII–XIV / XVIII; 1851 interior
  photographs 0169/0170/0177/0181/0184 as appearance checks.
- **Build note:** One repeatable panel, not a whole roof. Timber
  sash is explicit — no all-metal roof depiction.

### 2. `hp-floor-boards` — open-boarded floor section
- **Status:** Built and QC-passed 2026-10-26 by the parallel
  Muse stream (not this builder — a duplicate staging of mine
  with guessed dimensions was deliberately NOT pushed, because
  theirs is better evidenced). 15 boards, 7 joists, 2 sleepers,
  24 objects, 288 triangles, section 16 × 12 ft. Boards 1½ in
  thick, ½ in gaps, joists 7 × 2½ in, sleepers 13 × 3¼ in at
  8 ft — all printed in the Official Catalogue (1851) p.62;
  board width (9 in) and joist spacing (2 ft) inferred and
  labelled. See `hp-floor-boards/NOTES.md` on main.
- **Scenes:** CP020 (preparing for feet and crowds — narrow spaces
  between boards for cleaning), CP028 (daily work / cleaning).
- **Evidence to use:** Downes floor evidence; storyboard CP020 flag
  (current course-model floor slab cannot stand in for these boards).
- **Build note:** A short section with gaps, not a full floor slab.

### 3. `hp-gallery-stair` — stair flight + gallery rail section
- **Status:** Taken by the parallel Muse stream (CANDIDATES.md
  row 9, 2026-10-26) — do NOT duplicate. A local stair script
  and NOTES draft exist in this builder's workspace but must
  not be pushed while the row is taken.
- **Scenes:** CP027 (another level of visitors — stair shown from
  the bottom, explicit cut to landing, never floating through a
  floor), CP023 (nave / gallery context).
- **Evidence to use:** Downes plates II / XV–XVII. Existing course-
  model stairs are a starting point for dimensions only, not a copy
  — their details are flagged simplified/inferred in the storyboard.
- **Build note:** One flight + rail + landing edge. Well-hole edges
  stay unmodelled until confirmed.

### 4. `hp-louvre-and-blind` — opening louvre + canvas blind unit
- **Status:** Taken by the parallel Muse stream (CANDIDATES.md
  row 10, 2026-10-26) — do NOT duplicate.
- **Scenes:** CP015 (keeping a glass hall habitable — shading and
  ventilation), CP028 (shading / ventilation as daily work).
- **Evidence to use:** Downes plate XXVII.
- **Build note:** Mechanism shown open and closed in renders
  (two states of the same prop, not two props).

### 5. `hp-great-elm` — procedural elm tree, instancing-friendly
- **Scenes:** CP008 (build around the trees), CP017 (the park
  remains inside — elms under the transept vault), CP022 (trees
  behind the fountain).
- **Evidence to use:** Transept interior views in
  `references/muse-drive/images/commons/` and `main-article/`.
- **Build note:** Generic, clearly labelled as such. These views
  cannot capture a specific elm, so no prop claims to be a named
  individual tree. Canopy / roof clearance is unresolved in the
  storyboard — the prop ships at a plausible mature height with
  that uncertainty stated in NOTES.md, and must not be used to
  "prove" transept clearance.

### 6. `hp-crate-and-display-case` — packing crate + exhibition vitrine
- **Scenes:** CP019 (the world arrives in cases), CP024 (machinery
  section dressing — case/barrier, not the machine itself),
  CP025 (jewel case — case only, no invented diamond sparkle or
  case design), CP030 (packing crates replace exhibits).
- **Evidence to use:** Dickinson plates in
  `references/muse-drive/images/commons/` (e.g. plate XXIV, cases
  of goods, CC0); Routledge zoning plan 0726 for *where* cases
  sat, not for their dimensions.
- **Build note:** Sizes are guessed, not dimensioned — NOTES.md
  must say so. Do not populate every court with generic modern
  museum cases; this is one period-style case, reused sparingly.

## Wave 2 — Hyde Park centrepiece (research spike first)

### 7. `osler-crystal-fountain` — Osler fountain, Hyde Park transept
- **Scenes:** CP021 (doors open — fountain establishes scale),
  CP022 (a landmark made of glass — the film's central navigation
  object), CP023 (nave walk starts with fountain behind).
- **Status:** Open in CANDIDATES.md row 2. **Not started, and not
  to be started from geometry guesses.**
- **Evidence found so far (leads, not a dimension set):** Wellcome
  transept view `Catalogue_of_the_great_exhibition_Wellcome_
  L0022578.jpg` (CC BY 4.0); two British Museum transept views
  (public domain); `Great_Exhibition_fountain_1851.jpg`
  (677×595, public domain).
- **Research spike before building:** hunt a dedicated dimensioned
  or multi-angle detail set (fountain-maker records, Tallis /
  Dickinson plates, 1851 photographs 0185/0181). If none is found,
  the prop ships as an explicitly interpretive tier/basin study
  with every inferred tier marked — or it stays unbuilt and CP022
  is flagged as blocked. A guessed fountain presented as faithful
  would be worse than no fountain.
- **Build note:** Glass material study, not a solid crystal blob.
  Placement (transept centre) is a scene-layout decision for the
  shell builder, not a property of this prop.

### 8. `hp-working-machine-exhibit` — ONE documented working exhibit
- **Scenes:** CP024 (machines at work — one machine operating,
  one evidenced moving component in 50 mm insert).
- **Status:** Blocked on selection. The storyboard requires choosing
  and researching one actual exhibit before animation. Leads
  named: Muse 0316/1293.
- **Build note:** Do not build a generic "Victorian machine".
  If no single exhibit can be documented, this slot stays empty
  and CP024 is flagged — the film must not invent a functioning
  engine assembly.

## Wave 3 — Sydenham dressing (separate evidence, freestanding modules)

### 9. `sy-subway-vault-bay` — High Level subway brick-vault bay
- **Scenes:** CP046 (a second railway threshold — 1860s High Level
  subway, distinct from CP036's earlier arrival), CP065 (1954 —
  subway loses its transport role, High Level closes, lower station
  survives), CP071 (present-day walk — the surviving enclosed
  space, brick columns and patterned vaults).
- **Evidence to use:** Period station/subway layout and measured
  vault references — still needed; storyboard flags actual
  station-to-entry geometry as unplotted. Modern subway imagery
  is secondary evidence for the present-day state only.
- **Build note:** One repeatable vault bay (brick columns +
  patterned vault), so the same prop serves 1860s, 1954 and
  present-day states with different dressing / condition. Never
  confuse with the lower station, and never place it in 1854.

### 10. `sy-egyptian-column-pair` — Egyptian Court column pair
- **Scenes:** CP038 (Egypt, interpreted in South London).
- **Evidence to use:** Court plan 0226 and dated views; 1856 guide
  plan 0205 for court position only.
- **Build note:** Painted columns + capital detail. NOTES.md must
  state these are Victorian reproductions/interpretations, not
  originals and not a neutral account of an entire culture.

### 11. `sy-alhambra-ornament-panel` — Alhambra Court ornament panel
- **Scenes:** CP041 (the Alhambra Court — geometric ornament and
  colour, 50 mm insert on one surface).
- **Evidence to use:** Alhambra plan 0246 and image lead 0108.
- **Build note:** One panel, not a whole court. Geometry and
  colours must be verified against sources; do not fill gaps
  from an unrelated Islamic building.

### 12. `sy-classical-cast-base` — classical court cast plinth + base
- **Scenes:** CP039 (antiquity in colour — coloured detail beside
  sculpture and a Victorian visitor guide).
- **Evidence to use:** Classical court plans and decoration
  references (to be selected per court; specific polychromy is
  flagged unverified in the storyboard).
- **Build note:** Plinth and base only. **No figurative sculpture
  is modelled here** — see "Not building" below.

### 13. `sy-gothic-arch-fragment` — medieval / Renaissance fragment pair
- **Scenes:** CP040 (walking through arranged history — Gothic
  detail and Renaissance fragment in two separately established
  court spaces, explicit cut between them, never a morph).
- **Evidence to use:** Court positions from 0205; specific period
  reference images still required.
- **Build note:** Two small fragments as one prop set, designed
  to be shot separately. Literal court sequence is unconfirmed
  in the storyboard — the props do not assert adjacency or a
  hierarchy of civilisations.

### 14. `sy-terrace-step-and-balustrade` — terrace step + balustrade section
- **Scenes:** CP042 (the landscape performs — terrace descent,
  balustrade stop), CP073 (the steps and the sphinxes — present-
  day terrace, same prop family in modern condition).
- **Evidence to use:** 1857 map 0591; terrace / basin references;
  modern terrace survey for the present-day state.
- **Build note:** One step flight + balustrade length, reusable
  up and down the slope. Fountains themselves are a separate,
  later decision (see below) — this prop does not imply the
  full waterworks were running.

### 15. `sy-fountain-basin` — terrace fountain basin (research-gated)
- **Scenes:** CP042 (selected fountains operating below, towers
  only in a date-supported state).
- **Status:** Gated on the CP042 working-date question
  (c.1856–1857 needs completion records; if the selected
  waterworks state is later, the scene moves after CP045).
- **Build note:** Basin only, no invented flow rate, no claim of
  continuous full operation. Operating cost is the scene's point;
  the prop must not make the spectacle look free.

## Wave 4 — Later states, ruin and present-day variants

These are variants and condition states, not new buildings. Each
reuses a Wave 0–3 prop family so the change reads as change.

### 16. `sy-post66-closure` — post-1866 north-end closure dressing
- **Scenes:** CP048 (the missing transept stays missing — north
  end permanently altered, loss and surviving structure both
  readable in one view).
- **Build note:** Closure wall / altered-end dressing as a
  variant set. Exact closure-wall form is flagged as requiring
  evidence in the storyboard — do not just delete one symmetrical
  block and call it done.

### 17. `sy36-ruin-fragment` — twisted / collapsed iron fragment
- **Scenes:** CP062 (morning between the towers — twisted remains
  on the ridge, towers standing beyond the missing roof), CP063
  (clearance — debris secured, damaged members removed).
- **Build note:** A damaged variant of column/girder geometry,
  explicitly labelled ruin. It must never be reused as an intact
  component, and CP062 must not use a fully cleared plateau for
  the morning after.

### 18. `sy-tower-study` — water-tower massing study (shell-builder aid)
- **Scenes:** CP042 (towers only in a date-supported state),
  CP062 (towers survive the fire), CP064 (skyline loses its last
  markers — before/after by explicit time cuts, no speculative
  demolition blast).
- **Build note:** Massing study only, in `models/` as a scale
  reference for the shell builder. Tower demolition dates and
  causes need individual records (storyboard flag) — this prop
  asserts no demolition narrative.

### 19. `park-now-plateau-marker` — present-day plateau / outline aid
- **Scenes:** CP072 (read the missing footprint — dated Sydenham
  outline overlaid briefly, explicitly interpretive, camera fixed
  for comparison), CP076 (turn back toward the empty site —
  outline appears briefly and fades while the camera is still).
- **Build note:** A flat outline / marker set for the overlay,
  not a building. Registration is future work (storyboard:
  georeferenced Sydenham plan + modern survey required; label
  approximate until independently aligned). Never put a Hyde Park
  grid on Sydenham terrain.

## Wave 5 — Offsite and contextual props

Small, clearly-labelled interpretive props. None of these is a
palace component, and none pretends to be a surveyed room.

### 20. `chatsworth-glasshouse-rib-bay` — glasshouse rib bay
- **Scenes:** CP003 (a gardener's workshop — glasshouse interior,
  plants and structure sharing the frame), CP004 (learning to
  repeat — repeated glass and ribs receding, 50 mm detail on two
  matching components).
- **Build note:** One rib bay, labelled illustrative, not a literal
  surveyed Chatsworth room. The lily-leaf inspiration anecdote is
  omitted by the storyboard — do not build a lily-leaf "origin"
  prop for it.

### 21. `committee-brick-model` — miniature unbuilt-proposal model
- **Scenes:** CP007 (the answer that would not work — small
  volumetric model of the committee scheme on a worktable,
  captioned "Unbuilt committee proposal", never a built palace).
- **Evidence to use:** Muse 0324/0569 committee proposal leads.
- **Build note:** Deliberately miniature and tabletop-scale.
  French 1849 and New York exhibition plans are NOT London
  geometry and must not be used as references for this model.

### 22. `hawkins-mould-and-table` — Iguanodon mould shell + set table
- **Scenes:** CP034 (making extinct animals visible — dinner
  inside the mould, 1853–31 December 1853).
- **Evidence to use:** Dinner illustration and workshop evidence
  — still needed. Exact guests, seating and mould construction
  are unverified in the storyboard.
- **Build note:** Mould shell + table only. No completed live
  dinosaur is implied, and no dialogue is staged by a prop.

### 23. `sy-concert-organ-front` — central-transept organ front
- **Scenes:** CP045 (music fills the transept — choir, orchestra
  and audience in the central transept, organ anchors the space).
- **Status:** Gated on dated image leads 0032/0057/0595 and a
  checked festival configuration. No performer count is asserted.
- **Build note:** Organ front / case only, not a full concert-hall
  interior.

---

## Scene-by-scene coverage map

"Prop" = a prop from this plan. "Shell / environment" = work for a
shell or environment builder, not `models/`. "—" = no new prop
needed (narration, caption, cut, or existing asset suffices).

| Scenes | Passage | What this plan supplies | Left to shell / environment builders |
|---|---|---|---|
| CP001 | 1936 prologue | 17 ruin fragment (reference for silhouette dressing) | SY36 shell, skyline, crowd silhouettes, fire refs 0592/0587/0588 |
| CP002 | Industrial Britain | — (representative place, not a prop) | New contextual environment: railway-side lane, factory, housing |
| CP003–CP004 | Chatsworth | 20 glasshouse rib bay | Chatsworth plans, planting, glasshouse interior environment |
| CP005 | Planning room | — (table dressing is generic) | Planning-room dressing; no fabricated document wording legible |
| CP006 | Hyde Park site | — | 1850 site terrain, trees, survey props (ref lead Muse 0318) |
| CP007 | Unbuilt proposal | 21 committee brick model (miniature) | Park view behind the table |
| CP008 | Build around trees | 5 elm (with 0 column as vault context) | Transept vault study overlay, elm canopy clearance |
| CP009 | Proposal → contract | 0 column (joint as the repeated component) | Component stacks, drawings, worktable, site |
| CP010–CP012 | Foundations / bays | 0 column; 1 sash panel (bay dressing) | Foundation pads/bases (Downes VIII, D16/D17), rigging, crews |
| CP013–CP016 | Materials / systems | 1 sash panel; 4 louvre/blind | Roof, gutters, hollow-column drainage demo, glazing trolley |
| CP017–CP018 | Transept / colour | 5 elm; 0 column (paint study) | Transept vault + glazing, Owen Jones paint study (refs 0312/0349) |
| CP019–CP020 | Fitout | 6 crate + case; 2 floor boards | Exhibit installation, entrance aisle, service plan |
| CP021–CP023 | Opening / nave | 7 fountain (research-gated); 0 column; 5 elm | HP51 complete interior, ceremony placement (refs 0583/0603/0150) |
| CP024 | Machines | 8 one machine (selection-blocked); 6 case/barrier | Machinery-section environment |
| CP025 | Luxury / empire | 6 case only | Jewellery / Indian display area, provenance text |
| CP026–CP028 | Crowds / galleries / daily work | 3 stair + rail; 4 louvre/blind; 2 floor boards | Entrance, ticket desk, crowd dress, evening daylight look |
| CP029–CP031 | Closing / empty / dismantle | 6 crates; 0 column (joint undone) | HP empty + dismantling states, temporary support gear |
| CP032 | Across London | — (two staging stacks are set dressing) | Departure / receiving staging areas, schematic locator |
| CP033 | New building on slope | — (shell, not a prop) | Independent SY shell + terrain, 1856 plan 0205, section 0212, dims 0214 |
| CP034 | Extinct animals | 22 mould + table | Dinosaur workshop environment, Hawkins sculptures (see below) |
| CP035 | Second opening | — (opening-state entrance is shell work) | SY54 entrance + ceremony evidence, separate SY54 collection |
| CP036 | Railway arrival | 9 subway bay is **not** for this scene — CP036 is the earlier arrival | Station approach + colonnade (1856 guide 0208/0209, plan 0205) |
| CP037 | Taller interior | 10–13 court props (see below) as dressing | SY nave interior, plants, sculpture, court entrances |
| CP038–CP041 | Courts | 10 Egyptian columns; 11 Alhambra panel; 12 classical base; 13 Gothic/Renaissance fragments | Full court interiors, court plans 0226/0246, dated views |
| CP042 | Terraces / water | 14 terrace step + balustrade; 15 basin (date-gated); 18 tower study | Terraces, basins, water system, 1857 map 0591 |
| CP043 | Deep time | — (sculptures are sculptor work, see below) | Geological islands, lakeside path, Hawkins sculptures in period appearance |
| CP044 | Costs / access | — (gate + service dressing is generic) | Gate, service area, gardener / repair props |
| CP045 | Music | 23 organ front (date-gated) | Central-transept concert layout, choir / orchestra / audience |
| CP046 | Second railway threshold | 9 subway vault bay | High Level station approach, vault route |
| CP047–CP048 | 1866 loss | 16 post-66 closure dressing | SY pre/post-1866 shells, loss boundary |
| CP049 | New reasons to return | — (event dressing is per-event, not a standing prop) | Flower / animal-show dressing, night exterior + lighting |
| CP050 | Sport takes grounds | — | Football ground + stand plan, crowd / kit refs (1895) |
| CP051 | Modernity inside ageing building | — (exhibit is per-exhibit, not a standing prop) | One dated electrical / motor exhibit, older hall |
| CP052 | Repair never finishes | 1 sash panel (repair context) | Glazier / painter assets, weathered fabric |
| CP053–CP054 | Company fails / rescue | — (entrance is shell work) | 1911 / 1913 entrance states, rescue records |
| CP055 | 1913 Cup Final crowd | — | 1913 ground / crowd photographs, attendance record |
| CP056 | War naval use | — | Wartime hall adaptation, uniforms (refs 0317/0601); HMS Victory numeral omitted until verified |
| CP057 | Interwar revival | — | Interwar entrance / event refs, dated vehicles + clothing |
| CP058–CP061 | 1936 fire | 17 ruin fragment (aftermath ref only) | SY36 shell, fire progression, appliances, crowd viewpoints |
| CP062–CP064 | Ruins / clearance / towers | 17 ruin fragment; 18 tower study | Ruins photographs, debris staging, tower-removal records |
| CP065 | Railway changes | 9 subway vault bay (quieter state) | 1954 station / subway records, separate high/low station assets |
| CP066 | Sports Centre 1960s | — | National Sports Centre plans / photographs, landscape change |
| CP067 | Conservation | — (sculpture surface is sculptor / conservation work) | Conservation records, current sculpture condition |
| CP068 | Method outlives building | 0 column (analytical bay study, captioned as such) | Park view, component study environment |
| CP069 | South Kensington legacy | — | Street-level South Kensington context, chronology |
| CP070–CP076 | Surviving walk | 9 subway bay (CP071); 14 terrace step (CP073); 19 plateau marker (CP072/CP076) | Current station, park survey, terrace + sphinx survey, dinosaur viewpoints, layered-landscape survey |

## What I am deliberately NOT building in `models/`

- **Full Hyde Park or Sydenham shells.** Those are shell-builder
  work, with dated plans as the authority. A prop that pretends to
  be a shell would hide the storyboard's biggest honest gap: the
  documented HP model is an unfinished west-half frame, and no
  verified dated Sydenham model exists yet.
- **Figurative sculpture as procedural primitives:** Greek Slave,
  Una and the Lion, Three Graces (CP025/CP039 context), Hawkins
  dinosaurs (CP034/CP043/CP067/CP074) and terrace sphinxes (CP073).
  These need a sculptor. My plan supplies their bases, plinths,
  moulds and settings — never a blobby "statue" that would
  misrepresent the work. CANDIDATES.md row 6 stays open for a
  sculptor.
- **People, crowds, vehicles, trains and animals.** Crowds, workmen
  and staff are interpretive staging for the scene builders;
  no prop in this plan stages a person, a performance or a
  historical individual.
- **Furniture, lamps, benches and railings as a bulk set.** The
  manifest grep found no Palace-specific multi-angle set for
  these. If a later reference hunt isolates one Palace lamp,
  bench or railing run, it joins Wave 1 as a single named prop —
  it does not arrive as an invented generic set.
- **A "Sydenham column" by rescaling the Hyde Park column.**
  Sydenham proportions, datums and colour (pale blue ironwork,
  yellow, red per MODEL-AND-FILM-PLAN.md) are different evidence.
  Any future Sydenham column is a new prop from Sydenham plates,
  not a scaled copy.

## Coordination with other builders

- Claim before building: add a row to `models/CANDIDATES.md`
  (or extend it) and mark it Taken. Do not duplicate a taken row.
- One prop at a time, top-down from this plan, unless a research
  gate blocks the top item — then work the next ungated item and
  leave the gated item flagged, not fudged.
- After each prop: update `models/README.md` with name, thumbnail
  (three-quarter render), triangle count and accuracy note;
  commit **only** `models/` paths; push via the Git Data API on
  current main (other bots are pushing concurrently — retry on
  ref move, never force-push, never `git add .`).
- If a reference hunt changes a prop's evidence (e.g. the Osler
  dimension set turns up, or a court plan contradicts a panel),
  update that prop's NOTES.md and this plan together — do not
  leave a built prop and a stale plan disagreeing.

## Open evidence gates (things that can still change this plan)

1. Osler fountain dimension set (Wave 2, item 7).
2. One documented working machine for CP024 (Wave 2, item 8).
3. Egyptian / Alhambra / classical / Gothic court geometry and
   colours (Wave 3, items 10–13).
4. Subway vault measurements and station-to-entry geometry
   (Wave 3, item 9).
5. CP042 waterworks completion date (Wave 3, item 15).
6. Post-1866 closure-wall form (Wave 4, item 16).
7. Tower demolition dates / causes, individually (Wave 4, item 18).
8. Transept vault geometry — CORRECTED 2026-10-26 (round 2): the
   1856 guide table (ground-floor datum) gives Sydenham nave
   110 ft 3 in and central transept 174 ft 3 in, and 197 ft 10 in
   from the basement; the 102 ft 2 in figure in the review table is
   the HYDE PARK transept, not a Sydenham height (an earlier wording
   of this gate conflated the two columns of that table). Round 2's
   cross-check (references/muse-round2/review/GAPS-FOUND.md) found
   two independent 1854 sources agreeing on the drawing-supported
   pair — nave crown 104 ft, central transept 168 ft — against the
   1856 table; the ~6 ft difference is unresolved (a possible datum
   shift that no source states). No prop in this plan narrates or
   models a precise Sydenham height without naming its datum and
   endpoint; where a height is unavoidable, use 104 ft / 168 ft
   and say so.
9. A sculptor for dinosaurs, sphinxes and named statuary.

## Status at writing (26 October 2026)

- Wave 0 in progress, not complete (see above).
- Waves 1–5 are a queue, not built work. No prop beyond Wave 0
  is claimed, started or promised for a date.
- The storyboard's "ready" counts from the earlier 94-scene
  outline are not carried over as validation, per the storyboard
  itself.
