# Notes and history: walking the Crystal Palace, 1851

## Summary (read first)

**What.** Bear's general notes and history section for the game: what the 1851 interior held, who came, what they paid, what it sounded and looked like, and a set of design pushbacks. Pasted 2026-10-17 as "parts of notes", kept here nearly as written.

**Why it is here.** It is the starting point for the research agents (`AGENTS.md`) and the source of ideas for the GDD. It is **not evidence.** Nothing below has a citation, and no sentence has been checked against a primary source.

**What I found checking it against the project.**
1. Every factual claim here is `[UNVERIFIED]` and goes into the agents' queue (table at the end).
2. **One point conflicts with a decision.** Section 8 point 3 ("pick a day") praises a shilling Tuesday and a five-shilling Saturday. Q-01 is decided as **opening day, 1 May 1851**. The notes say shilling days began in late May, so the cheap-crowd variants cannot be 1 May. The ticket tiers are still useful as later days. Whether 1 May was open only to season-ticket holders is a fact for agent A3 to confirm, not something this file asserts.
3. **A number to reconcile with the building pack.** The notes give the transept vault as 108 ft. Our pack has a 74 ft 4 in vault diameter, and "108 ft" appears there only as the louvre run (D22, on no plate). The two may both be true (a height and a span) but the pack has not measured a 108 ft height. The building session owns this; do not change either side from here.
4. The notes' nave width of 72 ft agrees with the pack's 72 ft avenue; the 24 ft grid and 1,848 ft length are the pack's verified figures. The notes' "about 1,850 ft" and "64 ft" roof are unverified here.

---

## The core problem

The iron frame isn't the experience. What overwhelmed people in 1851 was density: more than 100,000 objects, sometimes over 100,000 visitors in a day, steam machinery running, colored ironwork, red hangings, heat, and a strange soft light coming through a glass roof. Charlotte Brontë, after visiting in June 1851, called it "vast, strange, new, and impossible to describe."

The renders show the skeleton going up, and it looks accurate. A first-person player walking through that frame empty will feel like they're in a beautifully lit parking structure. The real design questions are what fills the building, and what the player does in it.

## 1. Where the player is

The building was laid out on a 24-foot grid. The main avenue, the nave, ran east–west, about 72 feet wide and about 1,850 feet long, open to the roof at roughly 64 feet. On either side, the side aisles stepped down in tiers. Galleries ran along the upper level, reached by staircases. Halfway along, the transept crossed the nave north–south under a 108-foot barrel vault built to enclose full-grown elm trees.

The **west half held Britain and its colonies**, and the **east half held foreign nations**. So `west01` is the home side: British machinery, manufactures, the India court, Pugin's Medieval Court.

**Scale is a design decision, not a detail.** At a real walking pace, the nave alone takes six to seven minutes end to end, before galleries or side courts. Real visitors came back on several days. Queen Victoria went dozens of times. A realistic-scale game needs a reason to keep walking every hundred meters or so.

## 2. Arrival

Most visitors entered from the south, straight into the transept. What they paid depended on the day. After late May, Monday to Thursday cost a shilling and drew packed crowds of working people, many arriving on excursion trains (Thomas Cook built his business partly on these). Fridays cost two shillings and sixpence. Saturdays cost five shillings and drew a quieter, fashionable crowd.

Many visitors bought the *Official Catalogue*, which numbered every exhibit by class and location: the period's map, guidebook and checklist in one.

The first view was the set piece: the transept vault with living elms beneath the glass. At the crossing stands the **Crystal Fountain** by F. & C. Osler: 27 feet of cut glass, around four tons of it. Sculpture surrounds it, along with the cast-iron **Coalbrookdale Gates**. Sparrows nested in the trees. The story that the Duke of Wellington solved the bird problem with "Sparrowhawks, ma'am" is probably a legend, but a good ambient audio line.

The fountain was the meeting point and main landmark, visible down the nave from far away: the wayfinding anchor.

## 3. Walking west: the British half

Sculpture and large showpieces lined the nave. The side aisles and galleries were divided into courts by class and region, using partitions, display stands and hanging fabric.

| Exhibit | What the player experiences | Game use |
|---|---|---|
| **Machinery in Motion** (north-west) | Steam piped from an outside boiler house drove power looms, spinning machines, Applegath's vertical printing press, De La Rue's envelope-folding machine. Locomotives, Nasmyth's steam hammer, and the hydraulic press that lifted the Britannia Bridge tubes were also shown. Loud, smelling of oil and steam. | The noisiest zone, an audio landmark you hear before you see it |
| **Medieval Court** (A. W. N. Pugin) | Gothic Revival church furnishings, metalwork, stained glass in a dimmer, enclosed space | A quiet, sacred-feeling room inside a machine age |
| **India court** (East India Company) | A stuffed elephant with a howdah, Indian textiles and jewelry, the carved ivory throne from Travancore | A scale surprise; an imperial-politics thread if wanted |
| **The Koh-i-Noor** | Dull inside its gilded cage in daylight; moved to a darkened booth lit by gas jets to make it sparkle | A queue and a letdown |
| **The Tempest Prognosticator** | George Merryweather's storm-warning device: twelve leeches in jars ringing a bell | An oddity reward for explorers |
| **British manufactures** | Sheffield cutlery, Minton ceramics, Osler and Chance glass, textiles, raw materials, minerals | Set-dressing mass |

Outside the west end stood Marochetti's equestrian statue of Richard the Lionheart, a natural endpoint for a west-wing walk.

## 4. The east half, for when you build it

The **United States** section sat at the far east end. *Punch* mocked how sparse it looked early on, before it won respect with McCormick's reaper, Colt revolvers, Goodyear's india-rubber goods, and Alfred Hobbs's "unpickable" lock with a cash challenge. Hiram Powers's *Greek Slave* was among the most-viewed sculptures.

**France** showed Sèvres porcelain, Gobelins tapestries and Lyons silks. **Russia's** goods arrived late, including enormous malachite doors and vases. The **Zollverein** section had August Kiss's *Amazon Attacked by a Panther*.

## 5. The galleries

Climbing to the galleries gave the defining view: down the nave over crowds, fabric and sculpture toward the fountain and transept. Most period color lithographs are drawn from roughly that spot. Lighter goods such as textiles and small manufactures were displayed up there. For the game, the gallery is the reveal and the orientation point.

## 6. What visitors actually did

They navigated with the catalogue, hunting for specific exhibits or their own town's manufacturers. They watched machines run for long stretches. They queued for the Koh-i-Noor. They ate and drank: Schweppes held the refreshment contract, alcohol was banned, and buns, ices and soft drinks sold in enormous quantities. They paid a penny for George Jennings's flush toilets, the first public ones, and over 800,000 people did so.

They also watched each other. Classes mixed and foreigners walked the aisles. There had been widespread fear of riots and revolutionaries, and the crowds turned out orderly. Then visitors sat down, exhausted, and came back another day.

## 7. The sensory layer the model doesn't have yet

**Color is the biggest single correction.** The renders are cream and white. The real interior followed Owen Jones's color scheme: columns and girders in narrow bands of red, yellow and blue separated by white, with red cloth hung from the galleries. Contemporaries described the effect as shimmering, blending into a soft haze over distance. (The building handoff records the scheme as pale blue ironwork with yellow and red; the two descriptions differ and need one primary source.)

**Light should be softer.** In summer, calico was stretched across the roof to cut heat and glare, so the interior light was diffuse.

**Heat was real.** A greenhouse in summer; louvred vents at the base of the walls were the main defense.

**Sound changes with distance.** Machinery clatter in the north-west, the fountain's splash at the crossing, pipe organs being demonstrated, a multilingual crowd murmur.

**The floor** was wooden boards laid with small gaps so dust could be swept through: hollow footstep audio.

**Crowds** wore top hats, bonnets and wide skirts, with Metropolitan Police among them.

**Time of day:** as far as Bear's notes know, the building had no general artificial lighting and closed in the evening. A night level would be ahistorical unless deliberately a dream.

## 8. Design pushback

1. **Density over structural completeness.** Build a library of repeatable display units (glass cases, stalls, pedestals, textile drapes) and instance them heavily. Save hand-built detail for six to ten hero exhibits.
2. **The model shows false sightlines.** Side aisles were subdivided into courts by partitions and hangings, so long views ran only down the nave, along the transept and from the galleries. That gives natural rooms, natural occlusion, and reveals that land harder.
3. **Pick a day.** The ticket tiers give built-in variants without new geometry: a quiet five-shilling Saturday or a packed, loud shilling Tuesday. *(Conflicts with decided Q-01 for the first playable; the tiers become later days. See the summary.)*
4. **Decide on scale now.** Compress the building, speed up the walk, or commit to true scale with pacing landmarks. The fountain and transept vault should be visible from as much of the nave as possible.
5. **Consider the catalogue as the interface.** A catalogue held in hand works as a diegetic map, quest log and encyclopedia, and gives "what do they do" an answer: find things.
6. **`west01` needs the transept eventually.** The vault and fountain should be in view, even as a low-detail placeholder, before judging how the west wing feels.

## Reference lineage (leads, not yet checked)

- Dickinson, *Comprehensive Pictures of the Great Exhibition of 1851* (1854): colour lithographs after Nash, Haghe, Roberts; interior colour, hangings, crowds, placement.
- Downes, *The Building Erected in Hyde Park for the Great Exhibition* (1852): the measured drawings behind the building model.
- *Official Descriptive and Illustrated Catalogue* (1851): classes, numbers, locations.
- Owen Jones's 1850 lecture to the RIBA on the decoration.
- *Illustrated London News*, 1851.
- John Tallis, *History and Description of the Crystal Palace* (1852): a tour-ordered contemporary walkthrough.
- Modern histories (secondary, leads only): Colquhoun, *A Thing in Disguise*; Leapman, *The World for a Shilling*; Auerbach, *The Great Exhibition of 1851*.

---

## Claims to check (queue for the agents)

Each row is a claim in the notes above with no citation yet. Candidate claims go to `research/inbox/<agent>/`, never straight to `data/claims/`.

| # | Claim | Agent | Note |
|---|---|---|---|
| N-01 | Brontë's June 1851 quote | A2 | Quote exactly from her letter; mind the <15-word rule |
| N-02 | More than 100,000 objects; more than 100,000 visitors in a day | A1, A3 | Count per day from the Commissioners' tables |
| N-03 | Ticket prices by weekday after late May; start date of shilling days | A3 | Needed to place days relative to 1 May |
| N-04 | Who could enter on 1 May and at what price | A3 | Directly serves decided Q-01; not asserted in this file |
| N-05 | Nave about 1,850 ft by 72 ft, roof about 64 ft; transept 108 ft | building session | Reconcile with the pack's measured figures; not an agent job |
| N-06 | West half British and colonies, east half foreign | A1, A6 | Confirm with the Catalogue plan |
| N-07 | Crystal Fountain: Osler, 27 ft, about four tons | A1 | |
| N-08 | Coalbrookdale Gates, Pugin Medieval Court, India court, Travancore throne, stuffed elephant | A1 | Positions via A6 only |
| N-09 | Koh-i-Noor moved to a darkened gas-lit booth | A1, A2 | |
| N-10 | Machinery in Motion, steam from an outside boiler house, listed machines | A1, A5 | |
| N-11 | Merryweather's Tempest Prognosticator with twelve leeches | A1 | |
| N-12 | US section contents (McCormick, Colt, Goodyear, Hobbs lock, Greek Slave) | A1 | East half, later |
| N-13 | Schweppes contract, no alcohol, Jennings toilets, 800,000+ users at a penny | A3, A5 | |
| N-14 | Calico under the roof for shade | A5 | |
| N-15 | Owen Jones colour scheme and red hangings | A5, building session | Reconcile "pale blue" vs "red, yellow, blue bands" |
| N-16 | Wooden floor with gaps | building session, A5 | The model has a plain 6 in slab: a departure already in the ledger |
| N-17 | Sparrows in the trees; the Wellington "Sparrowhawks" line | A2 | Likely legend; tier `unknown` or `inferred` |
| N-18 | Marochetti's Richard the Lionheart outside the west end | A1, A6 | |
| N-19 | Building closed in the evening, no general artificial lighting | A3, A5 | Limits any night-time mode |
| N-20 | Most visitors entered from the south into the transept | A6, A2 | |
| N-21 | Queen Victoria visited dozens of times | A2 | Royal Archives published extracts |
