# NOTES — Park-now plateau marker: present-day Upper Terrace edge section

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 4, item 19).
Scenes: CP072 / CP076 (the surviving walk — the modern park reads
the missing palace from what survives), CP068–76 generally.
**Present day ONLY — nothing in this prop is 1854 dressing.**

## Relationship to the version already on main

The plan's item 19 records a `park-now-terrace-edge` already
built on main by the parallel stream: a **flat footprint-outline
overlay aid** (1,608 × 384 ft outline strips + posts, 120
triangles, for the CP072/CP076 overlay shots). This build is a
different object for the same scenes: the **physical surviving
terrace edge** the walk actually passes — wall, parapet, empty
plinths, plateau surfaces — at architectural scale. The two are
complements, not duplicates (outline overlay vs. standing
fabric), but they share the plan slug; the parent should resolve
the folder name at push time rather than overwrite either.

## What it is

One composed 35 m section of the Upper Terrace edge as it stands
today in Crystal Palace Park, centred on origin at garden ground
level (z = 0), plateau surface at z = 3.80:

- **Terrace retaining wall** — plinth band, a front plate pierced
  by **21 round-headed niches in groups of 3** between pilasters
  (the published rhythm, Historic England 1064352), a two-step
  corbelled cornice, and a solid back block. Niches are blind
  recesses 0.40 m deep with semicircular heads (the listing's
  "semi-circular semi-domed niches"; the conch is read as the
  arch-profile reveal at this scale).
- **Pierced arcaded parapet** on the wall top — dimensions
  **reused unchanged** from the shipped terrace module
  `models/sy-terrace-step-and-arcade/`: 15 narrow round-headed
  openings per 5.00 m bay, base band, coping, pilasters carried up
  with cap slabs standing **empty** (the vases/statues that topped
  them were sold in 1957).
- **Empty statue plinths** (×4) on the plateau gravel behind the
  parapet — plain stone pedestals, nothing on them.
- **Sphinx-less bases** (×2) at the section's south end — plain
  two-course rectangular blocks, the form photographed at the
  sphinx steps (`refs/CPsphinxsteps02.jpg`). **The sphinxes
  themselves are NOT modelled** — figurative sculpture is
  sculptor work in this project; several sphinxes survive on the
  terrace and belong to a separate prop.
- **Surfaces** — gravel forecourt at the wall foot and a gravel
  strip behind the parapet on the plateau (both photographed),
  grass bank beyond the forecourt and grass plateau beyond the
  gravel (both photographed).
- **Modern wire-mesh fence** on posts just behind the parapet —
  a present-day addition, photographed in the geograph view and
  included as such (posts, two rails, alpha-grid mesh).

Origin at the base centre of the section; units metres;
Blender 4.5.3. All materials procedural (script-painted textures;
no photographic textures).

## Sources used (see `refs/REFERENCES.md` for the full table)

- `refs/CPupperterraces02.jpg` (late 1980s, CC BY-SA 3.0) —
  primary elevation: niche groups, pilasters, parapet, gravel
  forecourt, wall/parapet height ratio.
- `refs/Crystal_Palace_Park,_terrace_-_geograph.org.uk_-_3424917.jpg`
  (CC BY-SA 2.0) — on the plateau: coping + corbelled garden face,
  gravel path behind the parapet, the modern mesh fence, grass
  beyond.
- `refs/CPupperterraces01.jpg` (1993), `CPupperterraces04.jpg`
  (late 1980s) — terrace levels, grass surfaces, pedestal form,
  grass bank at the north end, surviving sphinx in the distance.
- `refs/CPsphinxsteps02.jpg` (late 1980s) — the sphinx-less
  two-course plinth.
- Historic England list entry 1064352 — the published niche /
  pilaster / parapet description (quoted in REFERENCES.md).
- `models/sy-terrace-step-and-arcade/NOTES.md` — the reused
  dimension set and its evidence table.

## Dimensions — reused vs photo-counted vs photo-proportioned

**No surveyed dimension of the terraces was available to either
build.** Treat the set as ±10–15 %.

| Part | Value | Status |
|---|---|---|
| Parapet: 15 openings/bay, opening 0.19 × 0.55 m, pitch 0.30 m, plate 0.20 m, base band 0.25 m, coping 0.12 m, total 1.05 m; pilaster 0.55 m; bay 5.00 m | — | **Reused** from `sy-terrace-step-and-arcade` (published form + photo-counted there) |
| Niches per bay | 3 (21 in the section) | **Published** (listing: "groups of 3") + **photo-counted** on CPupperterraces02 (grounding count: 3 between every pair of parapet pilasters) |
| Wall height, garden ground → plateau | 3.80 m | **Photo-proportioned**: parapet (1.05 m, reused) ≈ 0.22 of the total elevation on CPupperterraces02 → total ≈ 4.85 m incl. parapet |
| Niche opening | 1.00 m wide × 2.95 m high, semicircular head, 0.40 m recess | **Photo-proportioned**: pitch 1.50 m from the counted 3-per-bay rhythm over the 5.00 m bay; height from the terrace module's parapet ≈ 0.35 × niche-arch proportion |
| Wall plinth band / cornice | 0.35 m / two steps 0.25 + 0.25 m, corbelled to 0.07 m | **Photo-proportioned** (cornice corbelling seen in the geograph view along the coping) |
| Wall thickness | 0.90 m | **Modelling choice** — retaining body; only the front 0.40 m (recess depth) is evidenced by the niche reveals |
| Section length | 35.00 m (7 bays; 35.6 m incl. end pilasters) | **Modelling choice** — a composed section in the brief's 30–40 m range |
| Gravel strip on plateau / grass beyond | 4.0 m / 8.0 m | **Photo-proportioned** from the geograph view (wide gravel path, grass behind) — depths truncated for a prop |
| Gravel forecourt / grass bank | 5.0 m / 4.5 m | **Photo-proportioned** (1980s views: gravel at the centre, grass bank at the north end — combined in one composed section) |
| Statue plinths | 1.00 m sq die, 1.08 m overall, on the gravel at y = 2.35 | **Estimated** — form from the square pedestals photographed in the park (CPupperterraces01 urns); positions composed, not a surveyed row |
| Sphinx-less bases | 3.60 × 1.50 m, two courses of 0.45 m | **Photo-proportioned** from CPsphinxsteps02 against its vegetation/block courses — the weakest sizes in the prop (±20 %) |
| Mesh fence | posts at 2.50 m, 1.10 m high, at y = 1.30 | **Photo-proportioned** from the geograph view; wire gauge/mesh size illustrative |

## What was NOT modelled / known inaccuracies

- **The sphinxes and any statue or vase** — plinths and caps
  stand empty by design (sculptor work; also the present-day
  truth for the caps since the 1957 sale).
- **Stairs** — flights pierce the terrace at intervals (visible
  in the primary photograph); this section is a plain wall run
  between flights. The shipped step module covers the flights.
- **Trees and planting** — the photographs show heavy tree cover
  behind and above the terrace; vegetation is scene dressing,
  not this prop.
- **The lower terrace** and the full plateau (the real terrace
  runs the palace's full ~500 m frontage; this is a 35 m
  composed section asserting no specific bay of it).
- Niche semi-domes are the arch-profile reveal of a 0.40 m plate,
  not modelled conches; arch heads are 7-segment faceted arcs
  (below film resolution at 1.0 m wide).
- Stone is one procedural texture, evenly weathered; the real
  wall varies (1980s repairs, staining, localised damage) far
  more than a single prop should assert.
- The fence mesh is an alpha-grid texture (~25 mm cells); at
  close range it will not hold up as woven wire — it is a
  mid-distance read, as photographed.

## QC (2026-10-27)

- Two build rounds; every render viewed against
  CPupperterraces02 and the geograph plateau view.
- Round 1 defect, caught by the script's own bbox audit
  (Z max 5.70 vs the designed 4.93): the wall pilasters and the
  plinth band stood at **twice** their intended offset. Cause:
  the shared `box()` helper bakes the passed location into the
  mesh (identity object transforms); two places in this script
  additionally re-assigned `.location`, applying the offset a
  second time. Fixed by removing the re-assignments (and a
  warning comment left in the script). The same audit explains
  the round-1 side render's black notch at the wall foot — the
  shadow gap under the raised pilaster — gone in round 2.
- Round 2 also toned the grass dry-patch layer (round 1 read as
  regular mowing stripes) and dimmed the garden-side fill so the
  niche recesses keep some depth.
- Known residual: in the three-quarter view the shadowed recess
  floors read as dark wedges at the niche bases — the same read
  as the shadow cores in the terrace photographs (the step
  module's NOTES record the identical phenomenon at the parapet
  openings); accepted.
- Counts, verified three ways (build log, re-opened `.blend`
  bbox audit, parsed `.glb` — all agree): **20 objects,
  6,662 triangles** — far under the ~50,000 triangle prop
  budget. World bounding box X −17.85…17.85 m, Y −9.50…12.90 m,
  Z −0.17…4.93 m (highest point the empty pilaster cap slabs).
- The `.blend` contains two collections: `Model` (exported to
  the `.glb`) and `RenderSetup` (ground plane, lights, cameras;
  not exported). All model meshes are world-space geometry with
  unit scale; the generated textures are packed into the `.blend`
  and embedded in the `.glb`.

## Files

- `build_park_now_terrace_edge.py` — re-runnable build script
  (bpy); all dimensions are named constants at the top, grouped
  reused / counted / proportioned / estimated.
- `park-now-terrace-edge.blend` — model + render setup.
- `park-now-terrace-edge.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 960 × 720. Front is the
  garden-side elevation (the CPupperterraces02 viewpoint); side
  is the section profile (forecourt / wall / plateau); three-
  quarter from the garden side above.
- `textures/` — the script-generated stone, gravel, grass and
  fence-mesh textures, also packed in the .blend.
- `refs/` — the reference images used, one enlargement, and
  `REFERENCES.md`.
