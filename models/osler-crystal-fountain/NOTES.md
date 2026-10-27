# Osler Crystal Fountain — NOTES

## What this is

The Crystal Fountain by F. & C. Osler of Birmingham — the glass fountain that
stood at the centre of the Hyde Park transept for the Great Exhibition of
1851, and the film's centrepiece prop (storyboard **CP021, CP022**). The
build is the fountain **in its playing state**: the full tiered glass
structure rising from its circular basin, with static translucent water
sheets and jets (see "Water" below). Origin at the centre of the basin
floor, real-world metres, Z up.

**Total height: 8.23 m (27 ft). Basin diameter, defined by this build:
7.2 m (R 3.6 m)** — see the two sections below; both numbers matter to
other builds.

## Sources used

All four references named for candidate #12, copied into `refs/`:

- **Wellcome engraving — governs the build.**
  `references/muse-drive/images/commons/Catalogue_of_the_great_exhibition_Wellcome_L0022578.jpg`
  ("View of the Transept and Crystal Fountain", from the *Catalogue of the
  Great Exhibition*; manifest licence **CC BY 4.0**,
  https://creativecommons.org/licenses/by/4.0; 1724 × 1170 px). The only
  full-height, near-frontal, detail-legible view: tier sequence, fluted and
  scalloped dishes, the Gothic arcade under the great dish, both rings of
  pointed pinnacles, the drum's panel blocks, buttress fins and shell
  cartouche, and the stacked-cup finial all come from this plate.
- **Opening-day engraving — silhouette cross-check.**
  `references/muse-drive/images/commons/Great_Exhibition_fountain_1851.jpg`
  ("The Transept of the Crystal Palace on the 1st of May"; **public
  domain**; 677 × 595 px). Confirms the overall silhouette and tier order.
  Its drum ornament is drawn as statuette-like figures and its mid-tier as
  a leafy crown; the Wellcome plate's sharper reading (pinnacle/panel ring,
  fluted bowl) is followed instead.
- **Nash lithograph — distant confirmation only.**
  `references/muse-drive/images/commons/The_Transept_(BM_1917,1208.2277).jpg`
  (Dickinson's *Comprehensive Pictures*, plate 4; **public domain**;
  2500 × 1907 px). The fountain is small and distant: a low wide dish and
  a tall column of falling water. Confirms the playing silhouette; no
  detail taken from it.
- **MET photograph — NOT the 1851 fountain's building.**
  `references/muse-drive/images/commons/View_of_Transept,_Looking_South_MET_DP238264.jpg`
  (Metropolitan Museum of Art; **CC0**; 2788 × 3863 px). This is the
  **Sydenham** transept: a tiered fountain of the same family playing
  behind the panelled basin railing (modelled separately as
  `fountain-basin-railing`). Used only as a form comparison in
  `renders/compare-met.jpg`; **no dimension or detail was taken from it**,
  and it must not be captioned as the 1851 original.

## Height — verification of the documented 27 ft

- The documented figure for the fountain is **27 ft**. Within this project
  it is carried in the architectural-data compilation made for the film
  ("the 27 ft (8 m) tall Crystal Fountain"). The project book
  (`crystal/crystal.md`) says the fountain "rose more than 20 feet" —
  consistent, but less precise.
- Checked against the guide material as instructed:
  `references/muse-drive/review/dimensions-from-1856-guide.json` holds
  **building dimensions only** (11 entries, from the 1856 guide's printed
  comparison table, p.35) — it contains **no fountain dimension**, so
  nothing in it contradicts 27 ft; it simply does not cover the fountain.
- Proportion check: scaling the Wellcome plate's internal ratios (below)
  with H = 27 ft gives stage sizes that sit comfortably against the
  plate's gallery and statuary scale; no internal contradiction found.
- **Adopted: 27 ft = 8.2296 m**, basin floor to finial tip. Status:
  documented (secondary sources), not measured from a period drawing —
  no dimensioned drawing of the fountain exists in the references.

## Basin diameter — DEFINED here as 7.2 m

No period source in the references dimensions the basin; the Routledge
1851 guide plan marks the fountain with a symbol only. The diameter is
therefore fixed by this build from the governing engraving:

- Wellcome plate: basin Ø / fountain height ≈ **0.79–0.89** depending on
  how the crowd-occluded left rim tip is read → **6.5–7.3 m** at
  H = 8.23 m. Adopted midpoint: **Ø 7.2 m (R 3.6 m)**.
- The opening-day engraving implies a smaller basin (≈ 5.3–6.4 m);
  engraver variance between the two plates is recorded, not resolved —
  the Wellcome reading governs.
- **Consequence for `fountain-basin-railing`:** that build's quadrant was
  modelled at an inferred **R 3.5 m** from the same Wellcome plate. To
  ring this basin (rim centreline R ≈ 3.43 m, outer edge R 3.62 m) the
  railing arc should be **re-radiussed from R 3.5 m to R 3.6 m**.

## Dimensions — measured proportions vs adopted values

Stage heights are the Wellcome plate's proportions (fractions of total
height, measured from the plate) applied to 27 ft; diameters likewise.
Engraver tolerance is roughly ±10% throughout.

| Element | z (m) | Ø (m) | Basis |
|---|---|---|---|
| Basin rim (top) | 0.375 | **7.20** (defined) | plate ratio, see above |
| Basin water surface | 0.29 | 6.52 | rim inner |
| Steps (2) | 0 → 0.44 | 2.52 / 2.22 | plate proportion |
| Base drum | 0.44 – 1.58 | 1.85–2.0 | plate proportion |
| Base pinnacles (8) | 1.12 – 2.00 | ring R 0.80 | plate: tips ≈ ¼ height |
| Arcade (8 columns + pointed arches) | 1.58 – 3.05 | ring R 0.80 | plate proportion |
| Great dish (rim) | 3.62 | 2.86 | plate: rim ≈ 0.44 × H |
| Wide fluted bowl (rim) | 4.44 | 1.85 | plate proportion |
| Middle drum (fluted bulb) | 4.05 – 5.23 | 1.03 | plate proportion |
| Middle pinnacles (6) | 4.05 – 5.04 | ring R 0.58 | plate proportion |
| Small dish (rim) | 5.47 | 0.86 | plate proportion |
| Flower cup (rim) | 5.82 | 0.69 | plate proportion |
| Spike cups (5, stacked) | 6.02 – 7.78 | 0.31 → 0.16 | plate proportion |
| Finial tip | **8.2296** | — | **27 ft, documented** |
| Mesh | **33,292 triangles, 89 objects** | bbox 7.23 × 7.23 × 8.23 m | final build stats |

## What was seen vs what was guessed

**Seen in the references, and modelled:**

- The full tier sequence: stepped base, ornamented drum, open Gothic
  arcade, great shallow dish, fluted bowl, fluted drum, small dish,
  flower cup, stacked-cup spike.
- Fluted undersides and scalloped (pie-crust) rims on the dishes; a wavy
  rim on the wide bowl.
- Two rings of tall pointed glass pinnacles — around the base drum and
  around the middle drum.
- Panel blocks and sloped buttress fins around the drum base; a scallop
  shell cartouche on the drum face.
- Water playing: a bell-shaped sheet falling from the spike tip, sheets
  spilling from each dish rim, and arcing jets from the middle drum into
  the wide bowl.

**Guessed or interpreted (not traceable to a source):**

- **Pinnacle counts** (8 base, 6 middle): the plate shows the front arc
  only; counts are inferred for rotational symmetry. The fountain was a
  lathe-turned exhibition piece, so full rotational symmetry is assumed
  throughout — the unseen back is the front, rotated.
- The arcade's pointed-arch profile (two-centred, centres offset 0.12 m)
  and the shell cartouches' exact form (schematic fluted discs; 4 placed).
- **Materials split:** the fountain proper is modelled entirely in glass
  (period accounts describe it as a glass fountain). The **basin rim and
  steps are modelled in pale stone** — an interpretation: in both
  engravings the basin reads as a plain solid ring distinct from the
  glasswork. No source in the references states the basin's material.
- The drum's internal structure and any metal armature, valves or pipework
  (invisible in every view) are not modelled.
- Absolute dimensions other than height and basin diameter are
  plate-proportions, ±~10%, as tabled.

## Water

The playing state is shown with **static translucent forms**, not a fluid
simulation: a bell sheet from the spike, spill sheets under the small
dish, wide bowl and great dish, and six arcing jets from the middle drum.
Fine radial fluting on the sheets is a rendering device so they read as
falling water rather than glass tubes. If a shot needs the fountain at
rest, hide the six objects named `Water*` — the structure is complete
without them.

## Known inaccuracies

- The two 1851 engravings disagree with each other (basin size, drum
  ornament, mid-tier form). The Wellcome plate governs; the disagreements
  are recorded above rather than averaged away.
- Engravers idealise: flute and scallop counts on the dishes are regular
  (24 / 16 / 12) where the originals were hand-finished.
- Glass renders through Blender's transmission model; the .glb export
  approximates those materials and will look flatter in other renderers.
- The fountain's glass in 1851 was famously almost colourless; the model
  carries a very slight green tint so the forms read against a grey
  backdrop at scene distance.

## Build

- `scripts/build_osler_fountain.py` — fully procedural bpy (Blender 4.2,
  headless). Height and basin radius are parameters at the top of the
  file; every stage is a lathe profile or an instanced repeat.
- `scripts/render_rig.py` — the fixed neutral-grey studio rig used for
  `renders/` (Cycles; emissive softboxes with camera visibility off give
  the glass something to refract). It opens the saved .blend and does
  not modify it.
- `scripts/make_compare.py` — builds the two comparison images.
- Renders: `front.png`, `side.png`, `three-quarter.png` (all from the
  one rig), `compare-wellcome.jpg` (Wellcome engraving crop left, front
  render right), `compare-met.jpg` (MET **Sydenham** photograph crop
  left, three-quarter render right — form comparison only).
- Built over four rounds: structure and proportions from the plate (r1),
  water transparency and framing (r2), sheet streaking, fin construction
  and basin water (r3), dish rim weight and middle-pinnacle placement
  (r4, final renders).
