# Sydenham garden fountain basin — NOTES

## What this is

The great **lower fountain basin** of the Sydenham gardens: the wide,
lobed pool in the foreground of both reference photographs, lying on the
garden axis below the Italian terraces, modelled in its **display state**
— stone rim, basin walls and floor, the water surface at its playing
level, and the jets as static display forms (one tall central jet, a ring
of eight, a ring of sixteen, and a small jet at each lobe).

The basin **alone**. The campana urns that stand on the rim in the
photographs are candidate #16, the statues on pedestals around the lawn
are other candidates, and the **upper basin** near the terraces is a
separate piece of scene dressing — none of them are in this folder.

Film context: storyboard **CP042** (terraces and fountains, c.1856–57
working window). This is a **Sydenham** object (post-1854). It must never
be placed in a Hyde Park scene.

## Sources used

- **Primary — plan-form and jet pattern:**
  `references/muse-drive/images/commons/Crystal_Palace_Park_-_fountains_in_1886.jpg`
  (photograph, 640 × 471 px; manifest licence **public domain**). Elevated
  view looking across the lower basin toward the upper fountains: the
  lobed outline and the ringed jet pattern read from above. Copied into
  `refs/`.
- **Primary — rim, water level, jet heights, garden setting:**
  `references/muse-drive/images/commons/Exterieur_van_Crystal_Palace_in_Sydenham_met_tuinen_en_fonteinen,_RP-F-F01134-AL.jpg`
  (albumen photograph, 4108 × 3236 px, Rijksmuseum object RP-F-F01134-AL;
  manifest licence **CC0**,
  http://creativecommons.org/publicdomain/zero/1.0/deed.en). The
  foreground basin fills the lower frame: scalloped rim, urns on the rim,
  a thicket of small jets around one very tall central jet. The manifest's
  museum record lists the maker as anonymous and dates the print
  ca. 1880–1910; the view is the one the candidates list attributes to
  Delamotte. Copied into `refs/`.
- **Checked, no basin dimension found:**
  `references/muse-drive/review/dimensions-from-1856-guide.json` gives
  building dimensions only (Sydenham frontage 1,608 ft / 490.1 m — used
  below only as a sanity bound); the 1856 guide's ground plan (gallery
  0205) is the palace **interior** — the gardens are off-plan, marked only
  "Entrance from the Gardens"; `REVIEW.md` and `MODEL-AND-FILM-PLAN.md`
  discuss the terraces and waterworks but print no basin size.

## Dimensions — measured vs inferred

**No measured dimension for this basin exists in the references.** Every
absolute size below is **inferred** from the two photographs and carries
roughly **±20%** uncertainty. The method: bench lengths (~1.8 m) and the
life-size statues on pedestals visible at the basin's own depth in the
Delamotte view set a pixel scale of ~32–48 px/m across the basin's depth;
applied to the basin's ~1,290 px span that brackets 27–40 m before
correcting for the oblique view, which lengthens the true span. The 1886
view gives the same order against its figures and paths. The adopted size
sits in the upper part of that bracket because the foreground statue —
the nearest anchor — is closer to the camera than the basin, so its scale
understates the basin least. Treat the whole model as re-scalable: every
size is a parameter at the top of the build script.

| Dimension | Value | Basis |
|---|---|---|
| Overall outline (rim centreline) | **40.0 × 27.0 m** (ratio 1.48) | **Inferred** (method above). Ratio read from the 1886 near-plan view (~1.4) and the Delamotte view after allowing for foreshortening. |
| Overall incl. ground apron | 42.5 × 29.1 m | The outline plus the modelled apron margin (bounding box of the stone mesh). |
| Lobes around the outline | **14** | **Read approximately** from both photographs — the edge resolves ~12–16 scallops; 14 adopted and the outline idealised as a true ellipse with even lobes. |
| Lobe amplitude | ±0.9 m | Read from the depth of the scallops relative to the outline in the 1886 view. |
| Coping (rim) top above ground | 0.56 m | **Inferred.** Both photographs show a low kerb barely rising above the lawn; no figure stands at the rim at a readable depth. |
| Coping width | ~0.5 m (roll profile) | **Guessed profile** — see below. |
| Water level | 0.16 m below coping top (z = 0.40) | Read from the Delamotte view: water sits just under the rim, bright against it. |
| Basin floor | z = −0.55 m (water depth ~0.95 m) | **Guessed** — the floor is never visible. |
| Central jet height | **20.0 m** | **Inferred.** Jet-to-basin-width ratio in the photographs is ~0.5 (1886) to ~0.9 including spray (Delamotte); 0.5 × width adopted. |
| Lesser jets | 8 × 7.5 m at 0.17 of the half-extents; 16 × 3.4 m at 0.40; 14 × 2.1 m at the lobes (0.78) | **Pattern read, counts approximate.** The photographs show a dense thicket of small jets (~30+ visible) around the centre and small jets toward the rim; the exact historic nozzle layout is not resolvable at 640 px. |
| Mesh | **12,632 triangles**, 3 prop meshes (+ studio ground in the .blend only) | Stone 4,704; water 224; jets 7,704. Origin at basin centre, ground at z = 0, real-world metres, scale applied. |

## What was seen vs what was guessed

**Seen in the photographs, and modelled:**

- A wide, shallow basin whose plan is an elongated oval **ringed with
  semicircular lobes** — the outline is the clearest fact in either
  photograph (1886, from above).
- A low, pale rim/coping, with the water surface bright and just below it.
- One dominant central jet, far taller than any other, rising from the
  middle of the pool with a broad white splash at its base.
- A ringed pattern of many smaller vertical jets, densest around the
  centre, with small jets out toward the lobes.
- The basin sits in open lawn on the garden axis; gravel paths and the
  terrace stairs frame it (context only — not modelled).

**Guessed or interpreted (not traceable from the photographs):**

- The **rim profile**. At the distance of both photographs the coping is
  a pale band a few pixels high. The model uses a simple rolled stone
  coping on a plain wall with a narrow ground apron — a plausible period
  kerb, **not** a read profile.
- Every absolute dimension (table above).
- The basin floor and its depth — never visible under playing water.
- The jets as smooth lathed solids with foam domes and landing skirts.
  Real jets are broken, moving water; these are **display forms** that
  hold the photographed heights and positions, nothing more.
- The water as a single flat, still surface at the playing level.

## Known inaccuracies / open questions

- **The outline is idealised.** The real basin's lobes vary and its long
  sides are unlikely to be a perfect ellipse; the photographs cannot
  resolve the plan to better than the ±1 lobe / ±20% size stated here. If
  the 1856 guide's fold-out **Plan of Palace and Park** (located by the
  round-2 collection on branch `muse-round2`) is measured, the outline
  parameters at the top of the build script should be re-fit to it.
- **Date state.** The photographs show the basin decades after the
  gardens opened (1886; the album print is dated ca. 1880–1910 in the
  museum record). The basin's form is the 1850s layout, but finishes,
  planting and the rim urns changed over the years; the model is the
  basin as photographed, captioned to CP042's c.1856–57 window only as
  the same structure in an earlier state.
- The **upper basin** (visible in both photographs, with its own ring of
  tall jets) is not modelled here; a full fountain-garden scene needs it
  as a companion piece, probably reusing this script with different
  parameters.
- The rim urns (candidate #16) stand directly on the rim in the
  photographs; when that candidate is built, its pedestals should land on
  this coping (crown at z = 0.56, centreline radius as parameterised).

## Build

- `scripts/build_garden_fountain_basin.py` — fully procedural bpy
  (Blender 4.2, headless). All dimensions are parameters at the top of
  the file. The stone (rim, walls, floor) is one profile swept along the
  lobed outline; jets are lathed display forms merged into one mesh.
- `scripts/render_rig.py` — the fixed neutral-grey studio rig used for
  `renders/` (Cycles; EEVEE hangs in this VM). It opens the saved .blend
  and does not modify the geometry. The studio ground disc is part of
  the rig and is **excluded from the .glb**.
- Renders: `front.png` (from the gardens, −Y), `side.png` (from +X),
  `three-quarter.png`, `elevated-three-quarter.png` (the money view,
  approximating the 1886 photograph), and `compare.jpg` (the 1886
  photograph at left, the elevated render at right).
- Built over three rounds: plan-form, rim and jet layout from the
  photographs (r1); jets rebuilt as columns with landing skirts after
  round 1 read as thin spikes (r2); shadows removed from the water
  cluster and foam plates domed after round 2 rendered a dark,
  shadow-pooled centre (r3).
