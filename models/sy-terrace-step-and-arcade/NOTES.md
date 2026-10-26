# NOTES — Sydenham terrace step flight + arcaded parapet (balustrade)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 14).
Scenes: CP042 (the landscape performs — terrace descent, balustrade
stop; working window c.1856–57 per round 2's fountain date fix),
CP073 (the steps and the sphinxes — present-day terrace, same prop
family in modern condition). **Sydenham only — nothing Hyde Park.**

## Relationship to the version already on main

`models/sy-terrace-step-and-arcade/` already exists on main,
built by the parallel stream: a 6-step flight with **square
balusters**, every dimension explicitly guessed, no surveyed or
photographic dimension used (its NOTES.md says so). This build is
the evidence-derived counterpart, staged separately for the
parent audit: it replaces the guessed square balusters with the
**pierced arcaded parapet the sources actually describe**, and
derives its dimensions from the terrace photographs as set out
below. The two should not be merged blindly; if only one ships,
this is the one whose form is evidenced.

## What it is

One repeatable module of the Sydenham upper-terrace edge: a flight
of **4 solid stone steps** (5.0 m wide) climbing to a truncated
top landing, **raked arcaded cheeks** on both sides of the flight,
a square **pier** at each side of the flight foot, and one **level
parapet bay** standing on the landing — base band, pierced plate
of 15 narrow round-headed arch openings, coping, and a pilaster
at the bay's start end. Origin at the base centre of the flight's
footprint (bottom step front, ground level), ground z = 0. Units:
metres. Blender 4.5.3.

**The decisive evidence.** The brief called for "balusters", but
the terrace balustrade is not a baluster rail. Historic England
list entry 1064352 (the terraces, Grade II) describes the
balustrade as "of similar pattern of **narrow round-headed
arches**" to the niche arcade of the terrace wall below it, with
the wall's pilasters "carried up into the balustrade above…
topped by vases or statues". The photographs agree: the parapet
is a pierced stone arcade (see `refs/crop-upper-terrace-parapet.png`),
and the stair cheeks carry the same narrow arches raked along
the slope (`refs/crop-upper-terrace-stair-cheek.png`). This prop
models that pierced parapet. No turned baluster appears anywhere
in it, deliberately.

## Sources used (see `refs/REFERENCES.md` for the full table)

- `refs/CPupperterraces02.jpg` — **primary source** (late 1980s,
  CC BY-SA 3.0). Upper Terrace centre: parapet, pilasters, stair
  with raked arcaded cheeks. Arch openings counted on it; height
  ratios proportioned from it.
- `refs/S57-01_delamotte_general-view_water-temple_1854.jpg` —
  Delamotte, 1854 (PD): the terraces as opened, arcaded fronts
  and parapet already present; a fountain-basin stair with
  balustrade cheeks and piers in the foreground. Confirms the
  pattern is 1854 fabric.
- `refs/2005-03-30_-_London_-_Crystal_Palace_-_Stairs_and_BBC_Radio_Tower_4887765272.jpg`
  — the great central staircase, 2005 (CC BY 2.0): step
  proportions read from its foreground flight.
- `refs/Crystal_Palace_Park,_terrace_-_geograph.org.uk_-_3424917.jpg`
  — on the Upper Terrace (CC BY-SA 2.0): coping width and the
  corbelled parapet on the garden face.
- `refs/CPupperterraces01.jpg` — 1993 (CC BY-SA 3.0): terrace
  levels and the Italian Gardens side.
- The 1854 Routledge grounds plan and the 1878 post-fire plan
  (both PD, round 2) — layout context only; **no dimension was
  taken from any plan**.
- Historic England list entry 1064352 — the published description
  quoted in `refs/REFERENCES.md`.

## Dimensions — published vs photo-counted vs photo-estimated

**No surveyed dimension of the terraces was available.** Except
where marked *published*, every number is a photo-derived
estimate, derived as stated; treat the set as ±10–15 %.

| Part | Value | Status |
|---|---|---|
| Parapet form: pierced arcade of narrow round-headed arches; pilasters carried up, topped by vases/statues | — | **Published** — list entry 1064352 (vases/statues NOT modelled) |
| Arch openings per pilaster bay | 15 | **Photo-counted** on CPupperterraces02: 89 openings counted across 6 bays (≈15/bay) |
| Parapet total height | 1.05 m | **Photo-proportioned**: parapet band ≈ 0.35 × the niche-arch height below it on the same front; consistent with a standard parapet |
| Arch opening | 0.19 m wide × 0.55 m high, semicircular head | **Photo-proportioned** from the counted density (15 per bay) and the band height |
| Arch pitch along bay | 0.30 m | Derived from the count over the adopted bay length |
| Bay length (pilaster pitch) | 5.00 m | **Modelling choice** for tiling, set so 15 arches at 0.30 m pitch + end margins fill the bay; the facade's niche groups (3 + pilaster) support a ~5 m rhythm but no bay was measured directly |
| Pierced plate thickness | 0.20 m | **Photo-proportioned** (openings' reveals in the 1980s/2005 views) |
| Base band / coping | 0.25 m / 0.12 m, coping 0.30 m thick | **Photo-proportioned** (geograph view along the coping) |
| Pilaster | 0.55 m wide × 0.30 m thick, cap slab +0.08 m | **Photo-proportioned** |
| Step rise | 0.15 m (6 in) | **Photo-estimated**: consistent across the 2005 staircase view, the 1916 Quarter-deck painting and the 1980s views; the period standard |
| Step going | 0.70 m | **Photo-estimated — the weakest number (±0.15 m).** Read from the foreground flight of the 2005 photograph (deep ceremonial treads, roughly 4–5 × the rise after allowing for foreshortening); the real central stair's treads vary by flight |
| Steps per module / flight width | 4 / 5.00 m | **Modelling choice**: one parapet bay wide; tiles sideways and up the slope (below) |
| Cheek plate | 0.24 m thick; 9 openings of 0.19 × 0.62 m stepping with the slope | **Photo-counted/proportioned** from the stair-cheek enlargement (openings upright, bottoms following the raked base band) |
| Pier at flight foot | 0.55 m square, 1.05 m + 0.10 m cap | **Photo-proportioned** ( CPupperterraces02 stair foot; Delamotte basin stair) |
| Landing depth | 1.50 m | **Modelling choice** — truncated; real landings run deeper |

## Tiling

- **Up the slope:** repeat the flight group (steps + cheeks) at
  Δy = −2.80 m, Δz = +0.60 m per module. Cheek segments butt at
  the segment joints; each segment's top end levels beside its
  landing exactly as the base module's does.
- **Sideways:** the flight is one bay (5.0 m) wide; repeat at
  Δx = ±5.0 m for wider stairs (the real central staircase is
  many bays wide). Cheeks of adjacent modules coincide at the
  shared edge — hide one of the pair.
- **Parapet:** repeat the bay at Δx = ±5.0 m; each bay carries
  its pilaster at its start end, so pilasters land on every bay
  joint, as the listing describes. `renders/tiled-three-quarter.png`
  shows the flight tiled ×3 up the slope and the parapet run
  extended sideways on its landing slabs.

## Period caveats — read before dressing a scene

- The terraces **survive**, but the photographs mix periods: the
  fabric was extensively repaired in the early 1980s, the statues
  and urns were sold in 1957, and the lower gardens were levelled
  in 1961–62. The model follows the **1854 pattern**, which is
  independently confirmed by Delamotte's 1854 view and by the
  list description; the modern photographs were used only for
  the proportions of the surviving stone pattern, never for
  condition or ornament.
- The pilasters were "topped by vases or statues" (listing).
  The cap slabs are modelled **empty**: vases, statues and the
  sphinxes that flank some flights are separate props (and the
  figurative ones are sculptor work, not procedural).
- Upper and lower terraces share the pattern; this module is
  generic to both and **asserts no specific terrace level**,
  consistent with the build plan.
- CP042's state (c.1856–57): terraces complete, fountains
  playing from June 1856 — this prop does not include or imply
  the fountains (item 15, separately gated). CP073's present-day
  state is a dressing/condition difference, not different
  geometry.

## What was NOT modelled / known inaccuracies

- **The terrace wall itself** — the round-headed niche arcade
  below the parapet, its pilasters and semi-domed niches are the
  terrace's main elevation and a separate, larger build; this
  prop is the step flight + parapet module that sits on and in
  front of it.
- **Vases, statues, sphinxes** on the pilaster/pier caps (sold
  1957; several sphinxes survive) — not modelled, see above.
- **Parapet returns** at the landing sides: the landing's side
  edges are open in this module; scene builders run a parapet
  bay along them where a return is needed. The stair cheek's top
  end levels beside the landing to meet such a return.
- **Mid landings / two-flight stairs**: the photographed stairs
  often run in two flights with a mid landing (see the cheek
  crop). The module is a single flight; a mid landing is
  assembled from the landing slab + parapet bay when tiling.
- Arch heads are 7-segment faceted arcs (at 0.19 m wide the
  facets are below film resolution); pierced plates are flat
  stone — the real parapet's arches have moulded reveals.
- Stone appearance is **procedural**: one texture painted by the
  build script (numpy mottling, no photographic texture). The
  real stone is weathered and lichen-stained in the modern
  views; 1850s condition would have been cleaner. Colour is a
  neutral warm grey matched by eye.

## QC (2026-10-26)

- Three build rounds; every render viewed against
  CPupperterraces02 and the Delamotte view.
- Round 1 defects, all fixed: (1) the parapet bay was placed at
  ground level **inside** the landing slab (its base band buried,
  arches cut at the sill) — the bay now stands on the landing
  (+0.60 m); (2) the pierced plates came out at **twice** their
  intended thickness — Blender curve `extrude` extends both
  ways, so the script now sets half the target thickness;
  (3) the stone texture's bump pass smeared vertical streaks
  down the piers — bump removed, texture contrast halved.
- Round 2 defect: in the front/side ortho renders the cheeks'
  buried feet showed **through** the ground plane as floating
  slabs. Diagnosis: with a near ortho camera, rays to geometry
  buried below the plane pass under the plane's surface *behind
  the camera plane*, so the plane never occludes them. Fixed by
  moving the ortho cameras far back (framing is unaffected in
  ortho) and reducing the burial to 0.45 m.
- Known residual: in the three-quarter view the shadowed ground
  seen through the parapet openings reads as small dark wedges
  at the openings' bases — the shadow core of a real pierced
  parapet reads the same way in the photographs; a dim back
  fill light was added to keep it off pure black.
- Counts, verified three ways (build log, re-opened `.blend`,
  parsed `.glb` — all agree): **12 objects, 1,728 triangles** —
  far under the ~50,000 triangle prop budget. World bounding
  box X −3.10…2.97 m (pilaster cap to pier cap), Y −4.35…0.45 m,
  Z −0.38…1.80 m (cheek feet buried 0.38 m for slope seating;
  highest point the raked cheek coping at the top nosing,
  0.07 m above the level parapet's cap line — the mitre
  difference where a raked coping meets a level one).
- The `.blend` contains two collections: `Model` (exported to
  the `.glb`) and `RenderSetup` (ground plane, lights, cameras;
  not exported). All model meshes are world-space geometry with
  unit scale; the generated stone texture is packed into the
  `.blend` and embedded in the `.glb`.

## Files

- `build_sy_terrace_step_and_arcade.py` — re-runnable build
  script (bpy); all dimensions are named constants at the top,
  grouped into published / photo-counted / photo-proportioned /
  photo-estimated.
- `sy-terrace-step-and-arcade.blend` — model + render setup.
- `sy-terrace-step-and-arcade.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 960 × 720. Front is the
  garden-side elevation (the CP042 viewpoint); side is the cheek
  profile; three-quarter from the garden side above.
- `renders/tiled-three-quarter.png` — the module tiled: flight
  ×3 up the slope, parapet run extended sideways — proving the
  repeat in both directions.
- `textures/stone.png` — the script-generated stone texture,
  also packed in the .blend.
- `refs/` — the reference images used, two enlargements, and
  `REFERENCES.md`.
