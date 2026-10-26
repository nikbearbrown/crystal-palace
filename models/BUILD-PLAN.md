# Build plan — what Muse will build for the Crystal Palace film

Derived from **storyboard v001** (76 scenes, CP001–CP076; 3,541 words; central
estimate 31:35) and `models/CANDIDATES.md` (40 prop candidates). The storyboard
is a planning draft, not an approved edit; this plan organises the *asset work*
it implies. It authorises no narration, render or publication.

Working rules carried into every build:

- **State separation is absolute.** Hyde Park 1851 and Sydenham 1854–1936 are
  different buildings. Every environment below is built as its own dated state;
  no era is produced by re-dressing another era's shell.
- **Props are drawn in random order** from the CANDIDATES pool (Bear's
  amendment — other bots build from the same pool). Environments are built in
  dependency order, because shells must exist before they can be dressed.
- Props follow MUSE-PROMPT §2: `models/<slug>/` with .blend, .glb, renders,
  refs, NOTES.md separating *measured/seen* from *guessed*.
- Anything the storyboard flags **U** (unresolved) is listed as an evidence
  gate, not built as fact.

## 1. Where things stand today (honest baseline)

- **Hyde Park frame (course model, not Muse's to edit):** 37 of 77 bays —
  the west half, 888 ft — an unfinished frame. Missing per the departures
  ledger: envelope and glazing detail, the central transept and its vault,
  colour, exhibits, site/terrain, finished floors and stairs.
- **`crystal-palace-full.blend`:** visually resembles Sydenham; identification
  and dimensions unvalidated. Not treated as a verified model of either
  building.
- **References:** 1,398 collected images + Downes 1852 working drawings +
  1856-guide plans. Round 2 (in progress, branch `muse-round2`) is hunting
  the missing Sydenham plans and scene images.
- **Props built:** none yet. First random draw is under way (§5).

## 2. The component library — build once, reuse in every state

The structural system is the film's recurring explanation (CP068), so these
parts come first. All are in the CANDIDATES pool with Downes plates as sources.

| Component | Candidate | Scenes that need it |
|---|---|---|
| Cast-iron column with base, brackets, capital connections | #18 | CP010, CP012, everywhere |
| Lattice girder / truss bay (24 ft module) | #21 | CP012, CP068 |
| Paxton gutter + hollow-column drainage section | #22 | CP014 |
| Gallery lattice railing + newel post | #19 | CP018, CP027, CP037 |
| Gallery staircase | #23 | CP027 |
| Louvre-vent operating machinery + canvas shades | #24 | CP015, CP028 |
| Glazing wagon / trolley | #31 | CP016 |
| Timber sash bars; floor boards with cleaning gaps | (Downes XII–XIV) | CP013, CP020 |
| Foundation pad + column base set | (Downes VIII) | CP010 |
| Cast-iron standards A–D (transept ribs/standards) | #25 | CP008, CP017 |

Colour is a *variant*, not an afterthought: Owen Jones's painted scheme
(CP018) needs paint-study materials kept separate from the bare-iron
construction states.

## 3. Environments by state family

### Hyde Park

- **HP-SITE** (CP006–CP009) — park terrain, paths, the great elms, survey
  lines and markers; the unbuilt committee scheme as a small *table model*
  (CP007), never as a built palace.
- **HP-BUILD** (CP010–CP017) — phased construction: foundation pads, rising
  bays, component stacks, work platforms, rigging and crews; the transept
  rising around living elms (CP017 — the single biggest missing piece of the
  existing frame).
- **HP-FITOUT** (CP018–CP020) — painted frame, crates and exhibit install,
  floor boards, entrance/service fit-out.
- **HP51** (CP021–CP029) — the dressed exhibition: nave avenues, Osler
  fountain centrepiece, machinery court, luxury/Indian displays, galleries,
  entrances and ticketing. Plus its two later states: **HP-EMPTY** (CP030,
  packing) and **HP-DISMANTLE** (CP031, supported joints being undone).
- **MOVE** (CP032) — two staging areas and a schematic two-site locator.
  Explicitly *not* a continuous transport route.

### Offsite contexts (small, bounded sets)

- Industrial Britain lane (CP002); Chatsworth glasshouse interior + rib
  detail (CP003–CP004); London planning room (CP005); factory/workshop for
  parallel manufacture (CP011); South Kensington street view (CP069).

### Sydenham — each era its own build

- **SY-BUILD** (CP033–CP034) — sloped ridge terrain, terrace earthworks,
  three-transept frame rising; Hawkins's workshop with the Iguanodon mould.
- **SY54** (CP035) — opening state, entrance only, bounded by 1854 evidence.
  *Gate:* the 1856 guide does not prove June-1854 completion; towers,
  fountains and wings stay out until dated evidence supports them.
- **SY-EARLY c.1856** (CP036–CP044) — the largest Sydenham build: railway
  approach + colonnade, nave with planting and sculpture, Egyptian Court,
  Greek & Roman courts, Assyrian Court, medieval/Renaissance courts,
  Alhambra Court, terraces and fountains, geological islands.
- **SY57** (CP045) — central transept as concert hall: organ, choir and
  orchestra staging, audience seating.
- **SY60** (CP046) — High Level station approach and the brick-vaulted
  subway, kept distinct from the CP036 low-level arrival.
- **SY66 / SY-POST66** (CP047–CP048) — pre- and post-fire north end as
  separate shells; the missing transept stays missing in every later state.
- **SY-LATE** (CP049–CP052) — event dressing (flower/animal shows,
  fireworks night), technology exhibits, maintenance states; **SY95**
  football ground (CP050) and **SY13** cup-final crowd state (CP055);
  **SY11/SY13** entrance states (CP053–CP054).
- **SY-WAR** (CP056) — naval training adaptation. *Gate:* omit the HMS
  Victory numeral — the sources conflict (V vs VI).
- **SY-INTERWAR** (CP057) → **SY36** (CP001, CP058–CP062) — dated fabric,
  fire states and the morning-after ruin with both towers standing.
- **SY-CLEARANCE / SY-TOWER-REMOVAL** (CP063–CP064) — staged clearing;
  before/after skylines for each tower's removal. *Gate:* individual tower
  dates/reasons need their own records.

### The park after the palace

- **PARK54** (CP065) — High Level station closing state + subway threshold;
  the surviving low-level station is a *different* asset and stays open.
- **PARK60** (CP066) — National Sports Centre in the 1960s landscape.
- **PARK-CONSERVATION** (CP067) — dinosaur conservation state.
- **PARK-NOW** (CP070–CP076) — the modern walk: surviving station, subway
  today, empty plateau, terraces with sphinxes, dinosaurs today, layered
  landscape. *Gate:* present-day access/condition must be surveyed, not
  assumed; an accurately registered Sydenham outline overlay is its own
  piece of work (CP072/CP076) — never the Hyde Park grid.

## 4. Court dressing sets (SY-EARLY)

Each court is a limited set plus its signature props from the pool:

- **Egyptian Court** (CP038): the colossi pair (#9, building now), painted
  columns, pylon base.
- **Greek & Roman courts** (CP039): Una and the Lion (#1), Andromeda (#2),
  Aristides/Aeschines (#6), Minerva bust (#7), Farnese Hercules (#4),
  Farnese Bull (#10), Three Graces (#5) — all on the standard display
  plinth (#35).
- **Assyrian Court** (CP039–CP040): lamassu bulls (#8).
- **Alhambra Court** (CP041): lion fountain (#14), geometric ornament set.
- **Sculpture gallery** (CP034/CP039): Cain and his Children (#3).
- **Nave and terraces**: Osler fountain (#12 — HP51 centre *and* the
  Sydenham nave's own state), garden fountain basin (#13), fountain-basin
  railing (#20), garden urn (#16), krater vase (#17), terrace balustrade
  and arcade (#39), park bench (#38), south-entrance pedestals (#26).

## 5. Prop pool mapped to scenes — random draw order

| Candidate | Serves scenes |
|---|---|
| #9 Egyptian Court colossi — **drawn first, building now** | CP038 |
| #12 Osler Crystal Fountain | CP021–CP022, CP037 |
| #15 The great elm | CP006, CP008, CP017 |
| #40 Iguanodon (and Hawkins mould state) | CP034, CP043, CP067, CP074 |
| #18/#21/#22 components | §2 library |
| #19 railing, #23 staircase | CP027, CP037 |
| #24 louvre machinery, #31 glazing wagon | CP015, CP016 |
| #27 Crampton locomotive "Folkestone" | CP024 (machinery court) |
| #28 vacuum sugar apparatus, #29 portable steam engine, #30 seed drill, #34 moving machinery | CP024 |
| #32 cut-glass chandelier, #33 exhibition carriage | CP019, CP025 dressing |
| #35 display plinth, #37 glass-topped display case | all courts, CP019–CP025 |
| #36 Great Exhibition medal | CP025 detail insert |
| #1–#8, #10, #11 statues/busts | CP037–CP040, CP073 (#11 as it survives) |
| #13, #14, #16, #17, #20, #26, #38, #39 garden set | CP042, CP070–CP076 |

**Not in the pool yet — needs candidates of its own:** the concert organ
(CP045), football stands and kit (CP050/CP055), 1936 fire appliances
(CP060), naval training dressing (CP056), period vehicles (CP051/CP057),
the subway's patterned brickwork set (CP046/CP071), terrace sphinxes
(CP073 — the references hold only the empty base), and all human figures:
crowds, crews, visitors and period dress are a dressing problem of their
own, flagged in nearly every scene.

## 6. Build sequence

1. **Phase A — component library** (§2). Everything else stands on it.
2. **Phase B — Hyde Park states** in story order: SITE → BUILD → FITOUT →
   HP51 → EMPTY → DISMANTLE, completing the transept the existing frame
   lacks. (The course-model frame is a starting reference, not an input to
   edit — Muse's environments are built fresh in `models/`.)
3. **Phase C — Sydenham states** in story order: BUILD → 54 → EARLY → 57 →
   60 → POST66 → LATE/95/13 → WAR → INTERWAR → 36 → RUINS → CLEARANCE →
   TOWER-REMOVAL. Shells shared *within* Sydenham only, each era a dated
   variant.
4. **Phase D — park and modern states**, plus the offsite context sets.
5. **Props throughout**, drawn at random from the pool (§5), each landing
   in `models/<slug>/` ready to dress whichever state needs it.

## 7. Evidence gates (do not build as fact until resolved)

- **Transept heights conflict — corrected 2026-10-26 (round 2):**
  the book rounds to ~108 ft / ~168 ft. The 1856-guide table
  (ground-floor datum) gives Sydenham nave 110 ft 3 in and central
  transept 174 ft 3 in, and 197 ft 10 in from the basement; the
  102 ft 2 in figure in the review table is the Hyde Park transept,
  not a Sydenham height (an earlier wording here conflated the two
  columns of that table). Round 2's cross-check
  (references/muse-round2/review/GAPS-FOUND.md) found two
  independent 1854 sources agreeing on the drawing-supported pair —
  nave crown 104 ft, central transept 168 ft — against the 1856
  table; the ~6 ft difference is unresolved. Resolve endpoints and
  datums before either shell is dimensioned; where a height is
  unavoidable, use 104 ft / 168 ft with datums stated.
- **Court adjacency and routes** (CP036–CP041): must be plotted from the
  1856 plan before interiors are laid out; unresolved adjacencies get
  labelled location cuts in the film, and no fabricated doors in the models.
- **1854 completion state** (CP035, CP042): fountains, towers and wings
  enter only with dated evidence.
- **Subway and modern park** (CP046, CP065, CP070–CP076): need surveys and
  current-condition checks; the plan asserts nothing about present access.
- **The Greek Slave and the Koh-i-Noor** have no usable references in the
  collection (CP025 handles the diamond as a case detail for this reason);
  if round 2 finds evidence, they join the pool then.

## 8. What this plan is not

Not a render instruction, not an approved edit, and not a promise that the
listed assets exist. It is the working map from the storyboard's 76 scenes
to the models Muse will build, in the order and under the rules above.
