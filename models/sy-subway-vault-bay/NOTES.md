# NOTES — High Level subway brick-vault bay

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 9).
Scenes: CP046 (1860s — the second railway threshold: the vaulted
subway under Crystal Palace Parade linking the High Level station to
the Palace), CP065 (1954 — High Level closes, the subway loses its
transport role), CP071 (present day — the surviving enclosed space).
**1860s Sydenham fabric only.** The subway opened on 23 December
1865, four months after the High Level station; it must never be
placed in the 1854 palace, and it is not the lower (1852) station's
arrival of CP036.

## What it is

ONE repeatable bay of the subway, built to tile. The Historic
England listing describes the interior as three parallel rows of
five octagonal columns carrying circular fan vaults; this prop is
the square module of that grid: one full octagonal cream-brick
column (square stone plinth, brick base drum with a stone ovolo
ring, moulded stone capital with a scalloped band and flaring bell),
the fan vault that springs from it — a patterned red-and-cream
brick soffit rising to the bay midlines, with ovolo-profile stone
ribs along the groins (diagonals) and along the bay edges
(perimeter arches) — quarter-roundels with concentric polychrome
rings and dark gas-fitting centres at the four corners (they
complete into full roundels when bays tile), and one square of the
alternating-stone floor. Origin at the base centre of the column,
floor top z = 0. Units: metres. Blender 4.5.3.

Tiling: place copies on a 3.35 m square grid. Edge ribs are inset
half a rib width inside each bay edge, so tiled neighbours pair
into one full rib instead of z-fighting. `renders/
tiled-three-quarter.png` shows a 3 × 2 tiling (three bays along
the hall, with the adjoining row) — roundels complete, fans meet
along the groin ribs, and the scalloped rhythm of the real ceiling
reads correctly.

## Sources used (see `refs/REFERENCES.md` for the full table)

- `refs/S87-subway-restored-interior-2025.jpg` — **primary source.**
  The subway after the 2023–24 restoration (CC BY-SA 2.0). Every
  photo-derived dimension below was measured on this photograph:
  brick courses counted, proportions taken against the piers and
  the vault pattern.
- `refs/S87-subway-interior-2016.jpg` — pre-restoration interior
  with visitors (CC BY-SA 4.0): human scale cross-check.
- `refs/S87-subway-east-courtyard-2023.jpg` — the courtyard end of
  the same vault system in daylight (CC BY-SA 4.0).
- `refs/S87-os-plan-high-level-station-1895.png` — layout context
  (PD). `refs/S87-high-level-station-iln-1865.jpg` — the station it
  served (PD, context only).
- Historic England list entry 1385457 (construction facts: column
  grid 3 × 5, materials, capitals, base mouldings, fan vaults,
  roundels, gas fitting) and the Friends of Crystal Palace Subway
  leaflet (vault thickness ~30 cm). Quoted/summarised in
  `refs/REFERENCES.md`.

## Dimensions — published vs photo-measured vs estimated

**No dimension of this building was available to me as a measured
survey figure.** Except where marked *published*, every number is a
**photo-derived estimate** from the 2025/2016 photographs, derived
as stated. Treat the set as ±10 % — it is internally consistent
(three independent reads converge, see below), but it is not a
survey.

| Part | Value | Status |
|---|---|---|
| Bay pitch (column centres, square) | 3.35 m | **Photo-estimated:** the fan radius (column centre → cell centre) counts ≈ 31 brick courses on the 2025 ceiling photographs; at the 0.075 m course gauge that is 2.32 m, and pitch = radius × √2 ≈ 3.29–3.35 m. Cross-check: gives a clear aisle of pitch − column ≈ 2.6 m, matching the two-people-abreast width against the columns in the 2016 photograph |
| Column, across flats | 0.73 m | **Photo-estimated:** one shaft face (a stretcher length + joints ≈ 0.30 m) → flats = face ÷ tan(22.5°) |
| Brick course gauge | 0.075 m (3 in) | **Assumed** — standard imperial gauging for 65 mm bricks; all course-count dimensions inherit this assumption |
| Shaft height (brick) | 2.55 m | **Photo-counted:** ≈ 34 courses, base ring to capital, on the lit pier in the 2025 photograph |
| Floor → springing | 3.51 m | Sum of the parts below; cross-check: capitals sit at ≈ 2× a visitor's height in the 2016 photograph (2 × 1.7 m ≈ 3.4 m) |
| Plinth | 1.02 m sq × 0.20 m high, stone | **Photo-proportioned** |
| Base drum (brick, wider) | 0.82 m flats × 0.16 m | **Photo-proportioned** (listing: brick bases with ovolo stone mouldings) |
| Base ring (stone ovolo) | 0.12 m high, to Ø ≈ 1.01 m | **Photo-proportioned** |
| Capital: scalloped band 0.14 m + bell/rings 0.34 m | 0.48 m total, flaring to Ø ≈ 1.08 m | **Photo-proportioned** from the 2025 pier close-ups |
| Vault crown (roundel plane) | 5.01 m (rise 1.50 m above springing) | **Photo-estimated:** rise ≈ 0.45 × pitch read off the 2016 view along the hall; end-arch crown ≈ 2.5 × the visitor standing in it |
| Perimeter arch crown (bay-edge midpoint) | 4.66 m (rise 1.15 m) | **Photo-estimated** from the fan geometry in the 2025 views |
| Roundel diameter | 1.15 m (≈ 0.34 × pitch) | **Photo-proportioned** on the near-plan ceiling views |
| Gas-fitting centre | Ø 0.45 m, dark | **Photo-proportioned** (listing: central cast-iron gas light fitting) |
| Stone rib width / projection | 0.15 m / 0.05 m proud | **Photo-proportioned** (listing: ovolo-moulded stone) |
| Vault thickness | 0.30 m | **Published** — Friends of CP Subway: "little more than 30 cm thick at the top of the arch" |
| Column grid of the real hall | 3 rows × 5 columns + wall responds | **Published** — Historic England listing (context for the tiling, not modelled) |
| Floor | stone slabs, diamond layout, two alternating tones | **Published** (listing: "paved floors in alternating stone") + photographed |

## The pattern

As photographed and as the listing puts it: "circular fan vaults
in red and cream brick laid to form diamonds." What the camera
actually shows, and what the model reproduces: on each fan the
brick courses run in concentric arcs around the capital; the
colour divides into **stepped diagonal bands** — roughly nine
courses wide, alternating red and cream, stepping one course at a
time across each quadrant of the fan — so that where four fans
meet, the bands compose the large diamond figures the listing
names. At the fan's foot there is a red ring course above the
capital. Between the fans sit the pale stone ribs; at each cell
centre a roundel of concentric red/cream rings with one diapered
(checker) ring and a dark centre where the gas fitting hangs.
The band sequence is **read from the photographs, not surveyed** —
the exact band phase on any given fan is an interpretation, and
on the steep fan foot the texture's plan-projected courses render
slightly wider-spaced than the real surface-laid courses.

All brick/stone appearance is **procedural**: the textures are
painted by the build script itself (numpy) from the dimension
constants — concentric fan courses with per-brick tonal jitter for
the vault, stretcher bond for the shaft, diamond slabs for the
floor. No photographic texture is used anywhere.

## What was NOT modelled / known inaccuracies

- **One interior bay only** — per the build plan. The real hall's
  wall responds (half-octagonal piers against oblong wall piers),
  side walls (cream brick with a red border, per the listing), end
  walls and their segmental arches, the glass-roofed vestibule and
  the stairs at the east end, and the courtyard at the west end
  are all outside this prop. A dressed scene needs a separate
  wall/end kit.
- **The gas light fitting** is represented only by its dark
  roundel centre; the hanging iron fitting itself is not modelled
  (it reads at a scale this bay doesn't resolve, and its exact
  form isn't legible in the references).
- **The capital's scalloped band** is a lathe with a shallow
  8-fold radial ripple standing in for carved scallops; the real
  carving is hand-cut and irregular.
- **Stone ribs** use a simplified ovolo (gabled) profile swept
  along the groin/edge curves; the real ribs are moulded stone
  with a true ovolo section.
- **Condition is neutral.** The bay is clean 1865 fabric: CP065's
  quieter 1954 state and CP071's restored present day are dressing
  and lighting differences (the 2016 photograph shows the
  pre-restoration grime the film may want as a texture pass), not
  different geometry. The air-raid-shelter phase (porcelain channel
  in the floor, per the listing) is not included.
- **Colours** are matched by eye to the 2025 restored photographs
  under gallery lighting; the restored brick is vivid, and 1865
  gaslight would have read it darker and warmer.
- Bay pitch and heights are estimates (±10 %, see table). If a
  measured survey of the subway is later added to the repo, the
  constants at the top of the build script are the single place
  to correct.

## QC (2026-10-26)

- Evidence files hash-verified against the round-2 manifest
  before use (all five S87 files MATCH).
- First build's renders were viewed against the 2025 photograph
  and showed five defects, fixed in the shipped build:
  (1) cameras framed out the crown and the floor — reframed;
  (2) the red brick rendered salmon-pale and the stone almost
  white under the first lighting — palette deepened, light
  energies and exposure reduced; (3) mortar joints read too wide
  and light — narrowed and darkened; (4) the capital's scallop
  ripple read as a ruffle — shallowed; (5) the vault's cut edge
  (solidify shell) wore the patterned texture stretched over it —
  the shell now takes a plain dark structural material, so the
  0.30 m thickness reads as structure; (6) the pattern's colour
  bands at first reset along the cardinal directions, seaming
  every fan down its middle — the band phase is offset 45°, so
  the resets fall on the groins under the diagonal ribs and the
  bands run continuous across the bay edges, as the photographs
  show from fan to fan.
- The tiled render was checked bay-to-bay: columns land on the
  3.35 m grid, quarter-roundels complete into full roundels with
  unbroken rings, paired edge ribs merge into single ribs, and
  no texture seams show at the bay boundaries.
- Counts: **17 objects, 20,112 triangles** (build log, evaluated
  with the vault's solidify applied) — under the ~50,000 triangle
  prop budget. World bounding box 3.35 × 3.35 m plan, 5.31 m to
  the top of the vault shell (soffit crown 5.01 m + 0.30 m
  thickness).
- The `.blend` contains two collections: `Model` (exported to
  the `.glb`) and `RenderSetup` (ground plane, lights, cameras;
  not exported). All model meshes are world-space geometry with
  unit scale; the generated textures are packed into the `.blend`
  and embedded in the `.glb`.

## Files

- `build_sy_subway_vault_bay.py` — re-runnable build script
  (bpy); all dimensions are named constants at the top, grouped
  into published / photo-measured / photo-proportioned.
- `sy-subway-vault-bay.blend` — model + render setup.
- `sy-subway-vault-bay.glb` — `Model` collection only (the
  brick-node-free materials export with their generated textures;
  the stone's procedural bump does not survive glTF and reads
  flat there).
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, 960 × 720. A square bay's front and side
  elevations are the same view by symmetry; the three-quarter is
  taken low, from the bay's diagonal, like the conservation
  photographs.
- `renders/tiled-three-quarter.png` — the bay tiled 3 × 2,
  proving the repeat.
- `textures/` — the four script-generated textures (vault brick,
  cream brick, foot ring, floor stone), also packed in the .blend.
- `refs/` — the five S87 reference images used, and
  `REFERENCES.md`.
