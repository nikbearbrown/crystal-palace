# NOTES — Hawkins's Iguanodon mould + dinner table

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 5, item 22).
Scene: CP034 (making extinct animals visible — the dinner inside the
mould, Sydenham, 31 December 1853). Sydenham-side story, 1853–54
workshop. **This is a workshop artefact, not a dinosaur.** The finished
Iguanodon is sculptor work and is deliberately NOT modelled anywhere
in this package; what is modelled is the hollow piece-mould the dinner
was held in, the staging built around it, and the table set inside it.

## What it is

One `.blend`, two named model collections (a third, `RenderSetup`,
holds ground/lights/cameras and is excluded from the `.glb`):

**`Mould`**
- `Mould_BodySection` + `Mould_TailSection` — the open **ventral
  (lower-half) mould** of the Iguanodon, as a lofted trough shell:
  plaster/compo read, reinforcing flange rib along the rim, iron
  hoops. The sections are **open-ended, as piece moulds are** — the
  cavity runs continuously through the flanged joints; only the
  shell's end-grain band closes each section face. The two sections
  meet at `Mould_JointFlange` with iron bolt bosses
  (`Mould_JointBolts`); `Mould_NeckFlange` and `Mould_TailFlange`
  frame the outer ends (the unmodelled head section adjoined at the
  neck flange).
- `Mould_IronHoop_1..4` — iron hoops around the body section.
- `Mould_Cradle` — the timber cradle: cross sills, longitudinal
  baulks, packing blocks, stepped blocks rising under the tail.
- `Mould_SparePlanks` — two planks stored under the staging
  (workshop dressing, from the model-room engraving).

**`Table`**
- `Table_Platform` — staging decks along both sides of the mould
  (top at 0.95 m), with posts and joists; `Table_StairsRails` — the
  five-step stair at the head end and the deck handrails.
- `Table_DinnerTable` + `Table_Cloth` — the long dinner table inside
  the cavity, standing on the mould floor, with a plain cloth.
- `Table_Benches` — two benches inside the mould flanking the table,
  and two on the side decks (overflow seating — see below).
- `Table_Candlesticks` — three plain brass candlesticks on the table:
  the abstract suggestion of the dinner lighting, nothing more.
- `Table_TrestleStool` — a workshop trestle stool beside the platform.

Origin at the base centre of the set (centre of the mould's length,
floor level). Units: metres. Blender 4.5.3. All objects have identity
scale (scale applied by construction).

## The historical facts the prop rests on

- **The dinner.** New Year's Eve, **31 December 1853**, in Hawkins's
  model-room at Sydenham. The ILN report (7 Jan 1854, p.22 — refs/2)
  is explicit that the dinner was **in the mould**: "In the mould of
  this colossal work of art … Mr. Hawkins conceived the idea of
  bringing together those great names…". **One-and-twenty guests**;
  **Professor Owen sat at the head of the table, in the head of the
  animal**, with Prof. E. Forbes, Joseph Prestwich, John Gould and
  the Crystal Palace Company's directors and officers. (An earlier
  summary in the round-2 review said Hawkins sat at the head; the ILN
  page itself says Owen — the ILN is followed here.) Secondary
  accounts (Owen/Rudwick) add that seven of the party overflowed onto
  **a platform raised to the same level just outside** the mould;
  modern retellings divide the 21 differently (11–14 inside). This
  set allows both readings: benches inside, benches on the decks.
- **The invitation** (described in the ILN report; the card itself is
  not in the repo — see refs/REFERENCES.md) was written on the wing of
  a Pterodactyle spread before an etching of the Iguanodon with its
  "socially-loaded stomach".
- **The animal's size** (hence the mould's): ILN, 5 Nov 1853, on the
  clay model in the same room — the Iguanodon "thirty feet long and
  eleven feet high" (9.14 m × 3.35 m).
- **The mould case's look**: the model-room engraving (ILN 31 Dec
  1853 — refs/3) shows the Iguanodon's body rising from a plain
  panelled case ≈1.9 m to the rim against a standing workman, in a
  timber workshop of trestles, baulks and blocks.
- **Construction of the finished models** (Hawkins, lecture 27 May
  1854): iron columns, brick and tile rubble, cement — "100 feet of
  iron hooping" among it. The dinner's staging (Earth Magazine /
  History Press retellings of the reports): steps up to a platform
  built around the model, a striped tent above, chandelier and
  candelabra, banners naming Buckland, Cuvier, Owen and Mantell.
  **The tent, banners and chandelier are scene dressing and are NOT
  part of this prop**; only the platform, steps and table are.

## Dimensions — what is measured, derived, estimated

No dimensioned drawing of the mould survives in the collection. The
chain of reasoning is stated, not hidden:

| Part | Value | Status |
|---|---|---|
| Animal overall length (mould plan length) | 9.14 m (30 ft) | **Printed** — ILN 5 Nov 1853 |
| Animal overall height | 3.35 m (11 ft) | **Printed** — ILN 5 Nov 1853 |
| Mould overall length (this model) | 8.80 m incl. end flanges | Derived — mould sections for torso + tail; the head mould section is separate and not modelled (below), so the set is ≈0.35 m shorter than the whole-animal figure |
| Mould rim height | 1.86–1.94 m | **Measured from the engraving** — case rim ≈1.9 m against the workman in refs/3; consistent with the dinner woodcut's platform/rim/guest geometry |
| Cavity (inner) width, torso | 1.68–1.82 m | Derived — torso depth of a 30 ft Hawkins Iguanodon read from refs/5 proportions; must seat a table + two bench rows, as the woodcut shows |
| Cavity floor height | 0.60 m | Estimated — shell on a 0.45 m cradle; the dinner geometry (bench seat 1.05 m, table top 1.39 m, heads above the 1.9 m rim) is internally consistent with the woodcut |
| Platform deck height | 0.95 m | Estimated from the woodcut — deck a little above the workman's waist, rim ≈0.95 m above deck, five steps up |
| Dinner table | 4.40 × 1.02 m, top 1.39 m | Estimated — sized to the cavity and to the woodcut's table, which spans most of the torso with diners both sides |
| Wall/flange/bolt sizes, cradle scantlings | 0.05–0.24 m | **Guessed** — period-plausible workshop sizes; no source |

Overall footprint of the set (measured from the exported `.glb`):
10.42 m × 4.18 m (platform + stairs), height 1.96 m (an iron hoop
standing over the 1.94 m rim).

## What is abstracted or omitted — and why

- **The head mould section is not modelled.** Owen sat "in the head",
  so a head section existed; but no source shows it as a separate
  workshop object, and any head-shaped shell would read on screen as
  a dinosaur head — exactly what this prop must not become. The body
  mould ends at a flat neck section face (`Mould_NeckFlange`), which
  is also how a piece-mould section honestly presents. Flagged here
  so the scene builder knows the head-end is a documented absence,
  not an oversight.
- **The upper (dorsal) half mould is not modelled.** The dinner could
  only have happened in the open lower half; the upper half's
  workshop state (hoisted? stored?) is unevidenced.
- **Leg mould sections are not modelled** — not visible in either
  period image; the case rests in its cradle as the engraving shows.
- **The table is a suggestion, not a reconstruction**: plain table,
  cloth, benches, three candlesticks. No food, no place settings, no
  glassware, no people (SCENE-BUILD-PLAN: no prop stages a person or
  a performance). The famous eight-course menu is a document, not a
  prop.
- **No tent, no name banners, no chandelier** — room dressing for the
  scene builder, per the plan's split between prop and environment.
- The shell's outer surface is a smooth lofted form. A real piece-
  mould's exterior would be rougher and more irregular; the interior
  carried the animal's surface in negative (scales and all) — that
  sculptural detail is sculptor territory and is not faked here.

## Triangle count and files

- Triangles: **2,504** (budget <50k). Objects: 19 model objects —
  12 in `Mould`, 7 in `Table`.
- `hawkins-mould-and-table.blend` / `.glb` (Mould + Table only),
  `build_hawkins_mould_and_table.py` (re-runnable build script),
  `renders/` front (profile, head at left as in the woodcut), side
  (head-end elevation), three-quarter, mould-interior (looking into
  the open mould at the set table). Cycles CPU, 960×720, neutral grey.

## QC

- Renders eyeballed against refs/1 and refs/3: rim height, platform
  and stair arrangement, and the table-inside-trough read all match
  the woodcut's geometry; the case reads as a plain workshop mould,
  not as an animal.
- **Defect found and fixed during build (v1 → v2):** the first loft
  ring placed its flange "step" points inside the line of the outer
  wall, so the cross-section loop crossed itself at the rim; combined
  with a loft winding that pointed the wall normals into the
  material, the section end faces and the tail interior rendered
  black. Diagnosed from the polygon normals in the saved file (outer
  wall +Y where −Y was required; cavity floor −Z where +Z was
  required). Fix: the ring was redrawn so the flange is a rib whose
  root points lie exactly on the wall line (21-point ring, no
  self-intersection) and the loft winding was reversed. All four
  views re-rendered clean; normals re-verified in the file.
- GLB re-import check: **passed** — fresh-scene import returns the
  same 19 named objects and 2,504 triangles as the `.blend`, bbox
  10.42 × 4.18 × 1.96 m with z-min at 0.00 (an early stringer length
  dipped 0.09 m under the floor; shortened and re-verified).
- One clarification the renders forced: the section end "caps" in
  the loft are the shell's end-grain band only — the sections are
  open through the joints, which is how the dinner view down the
  trough (renders/side.png) works and how piece moulds actually
  assemble.
- Known weakness: every dimension below the printed 30 ft / 11 ft is
  a reasoned estimate (table above). If a dimensioned Hawkins
  workshop source surfaces, this prop's NOTES and the plan should be
  updated together.
