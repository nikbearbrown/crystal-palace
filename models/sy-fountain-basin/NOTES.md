# NOTES — Great Fountain basin, Sydenham grounds

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 15).
Scene: CP042 (the landscape performs, c.1856–57 — selected fountains
operating below the terraces). **Sydenham grounds only.** This is not
the Hyde Park Osler Crystal Fountain (an indoor glass fountain of
1851, a different prop and a different research problem), and it is
not the Sydenham "Large Circular Fountain" either (see below).

## The date gate (read this before placing the prop)

The Sydenham great fountains **first played on 18 June 1856**, and
Brunel's water towers that fed them were operational only from
2 June 1856 (Historic England, via round-2 review). The June 1854
inauguration lithograph that shows the fountains playing is a
promotional anticipation, not a record. So this basin, in its
operating state, belongs to **c.1856–57 and later only** — it must
never appear in a June 1854 opening state. The plan's gate on item 15
is answered by this date: CP042's c.1856–57 window is supported.

## What it is

ONE of the pair of great fountain basins that flank the Grand Centre
Walk below the cascades — key "MM, Basins of large fountains" on the
1856 guide's Plan of Palace and Park. This is the **west basin**,
built in the orientation the plan draws it: a central scalloped
medallion (the widest part, bulging south), a narrower arm running
west to a rounded scalloped terminus, and a shorter arm running east
that ends flat against the central walk. Mirror it E–W for the east
basin of the pair. Origin at the centre of the medallion, ground
level (apron) z = 0. Units: metres. Blender 4.5.3.

Construction: the outline is a radial function — max of the
medallion ellipse, the two arm rectangles and the west cap circle,
with a 14-lobe scallop modulation that fades out on the arms — and
the rim is swept around it: outer apron band, rolled stone coping,
inner wall, basin floor. The water is a separate object,
`WaterDisc` (a still disc at the waterline; hide it for a drained
basin). The low centre plinth and nozzle boss are separate objects
(`CentrePlinth`, `CentreBoss`). Everything else is one mesh,
`Basin`.

## Which fountain — and which it is not

The grounds held several distinct waterworks, and the sources were
checked against each other before choosing:

- **The great basins (MM) — this prop.** Two huge shaped basins on
  the central axis below the cascades. Chosen because they are the
  best-evidenced basin in the collection: drawn to a readable
  outline on two plans (1856 guide; Routledge 1854) and photographed
  playing in 1886 and in the Italian Garden album view.
- **The "Large Circular Fountain" (H)** on the same axis, nearer the
  palace — a plain circular basin with a ring of jets around a
  central Water Temple (photographed close in the 1878–90
  garden-front view, `refs/photo-garden-front-circular-fountain-1878-90.jpg`).
  NOT this prop: different plan-form, and its centrepiece is a
  building/sculpture, outside this prop's remit.
- **The terrace fountains (R, S)** in the Italian Garden on the
  Upper Terrace — smaller scalloped basins, several visible in the
  album photograph. Same rim language, different (smaller) basins;
  not modelled here.
- **The cascades (LL) and their temples (JJ)** feed the great
  basins from the terrace; they are separate landscape structures,
  not part of this prop.

## Sources used (see `refs/REFERENCES.md` for the full table)

- `refs/plan-1856-guide-palace-and-park.jpg` — shape, key, layout.
- `refs/plan-1854-routledge-grounds.jpg` — outline corroboration
  (as projected; some features marked not completed).
- `refs/plan-1862-grounds-map.jpg` — absolute scale (see below).
- `refs/photo-italian-garden-fountains-album.jpg` — rim form and
  height, jet arrangement (single tall central jet).
- `refs/photo-great-fountains-playing-1886.jpg` — the pair playing;
  lobed outline and central jet confirmed for the great basins.
- `refs/photo-garden-front-circular-fountain-1878-90.jpg` — the
  circular fountain H (differentiation; rim-profile cross-check).
- `refs/plan-1878-guide-post-fire.jpg` — layout persistence.

## Dimensions — plan-measured vs photo-estimated vs inferred

**No dimensioned drawing of this basin exists in the collection**
(round-2 review §B3 found no 1854–57 fountain engineering plan).
Every absolute number below is an estimate, derived as stated.

### The scale conflict (why two numbers exist, and which was used)

Measured on the 1856 guide foldout against the palace block drawn
on the same sheet (1,608 ft = 490.1 m, the length both guides
agree on), one basin comes out ≈ **249 m long** — but the foldout
is a pictorial key plan, and its garden features are drawn large
for legibility. Measured the same way on the c.1862 surveyed
grounds map (6 in to 1 mile), the basin is ≈ **138 m E–W × 83 m
N–S**. The 1862 figure is adopted: it is the surveyed source, and
it passes the sanity check the 1856 figure fails — two 249 m
basins plus the central walk would span more than the palace
front itself, while two 138 m basins sit comfortably inside the
terrace width. Treat even the adopted size as **±20 %**.

| Part | Value | Status |
|---|---|---|
| Water outline, overall E–W | 138 m | **Plan-ratio estimate:** 1862 map, basin ÷ palace = 160/567 against palace 490.1 m. (1856 foldout would give 249 m — rejected, see above.) |
| Water outline, overall N-S (at medallion) | 79 m (+ scallops ≈ 81 m) | **Plan-ratio estimate:** 1862 map ratio 96/567 tempered by the 1856 plan's internal proportion (medallion N-S ÷ basin length = 270/498 = 0.54) |
| Medallion | 57 m E-W × 79 m N-S | **Plan-measured proportions** (1856 foldout: 206 × 270 px of the basin's 498 px length), scaled to the adopted length |
| Arms | 32 m wide (N-S); west arm to a rounded end, east arm flat at the walk | **Plan-measured proportions** (1856 foldout: arm width ≈ 115/498 of basin length; ends as drawn) |
| Scallops | 14 lobes around the medallion, ±4 % of local radius | **Counted/estimated** on the 1856 and Routledge plans (the engravers differ in detail; the count is a reading, not a survey) |
| Apron (surround band) | 4.3 m wide, top ≈ +0.48 m | **Plan band + photo check** — the hatched surround on the 1856 plan, width read against the central walk in the album photograph |
| Coping top | +0.86 m above surrounding ground | **Photo-estimated:** the rim reads at about knee-to-thigh height against the figures and balustrades in the photographs; no dimensioned source |
| Waterline | +0.55 m (0.31 m below coping top) | **Photo-estimated** freeboard, matched to the rim read in the circular-fountain photograph |
| Basin floor | −1.05 m | **Guessed.** No source shows the basin empty or in section. A working depth only. |
| Centre plinth / boss | Ø 11 m plinth to +0.40 m; Ø 3.6 m boss to +0.66 m | **Inferred.** Every photograph shows the centre hidden by the jet's foam. Included, small and mostly submerged, so a scene has a physical jet origin; it asserts nothing about the real nozzle arrangement. |

Plan-internal checks that do hold: on the 1856 foldout the two arms
are symmetric about the medallion (144 px west, 148 px east), the
medallion's centre sits on the basin's centreline, and the pair of
basins is mirror-symmetric about the central walk — the model
keeps all three.

## What was NOT modelled / known inaccuracies

- **No water in motion.** No jets, no spray, no flow — per the
  build plan ("basin only, no invented flow rate"). The photographs
  show one tall central jet and (1886 view) a ring of smaller jets;
  recreating them is a scene/render task, and their cost in water
  and engine hours is the scene's point — this prop must not make
  the spectacle look free or permanent.
- **The twin basin.** Only the west basin is built; mirror for the
  pair. The cascades, their temples, the central walk and the
  terrace works that frame the basins are landscape/shell work,
  not this prop.
- **Rim ornaments omitted.** The photographs show urns/vases at
  intervals on the rim and statues on pedestals at the basin
  corners. The urns belong to a garden-ornament prop; the statues
  are figurative sculpture (sculptor work per the plan) and are
  deliberately absent.
- **The outline is a reading, not a tracing.** The radial-function
  outline reproduces the plans' medallion-and-arms form and
  proportions, but the engravers' exact scallop rhythm (and the
  small bays along the arms on the Routledge sheet) is simplified
  to a single 14-lobe modulation on the medallion.
- **Materials are flat procedural colours** (pale stone rim, dark
  underwater interior, still-water disc). No photographic texture;
  the real basins' stone/lead tones vary and weather — a texture
  pass is scene dressing.
- **Condition is neutral, as-built.** No algae lines, no later
  alterations, no drained/ruined state.

## QC (2026-10-26)

- Evidence read directly: both plans' basin outlines measured by
  visual grounding on full-resolution crops (palace end walls,
  basin tips, medallion extremes, reservoir circle as a control);
  the 1856-vs-1862 scale conflict found by that measurement is
  documented above rather than averaged away.
- First build audited from the saved `.blend`: object set,
  collections and bounding boxes verified (water 138.6 × 81.2 m,
  coping top z = 0.86, floor z = −1.05). A top (plan) QC render was
  compared against the 1856 plan crop; two defects found and fixed
  in the shipped build: (1) the scallops were too shallow to read
  as the plans' lobed medallion — amplitude raised; (2) the west
  arm ended flat — the plan draws a rounded scalloped terminus
  there (only the east, walk-side end is flat), so a cap circle
  was added. Elevation cameras were also lowered (30 m → 12 m) so
  the front/side renders read as elevations of a very flat prop
  rather than near-plan views.
- Counts: **4 objects, 19,768 triangles** (Basin 18,000; WaterDisc
  1,200; CentrePlinth 284; CentreBoss 284), verified on the
  evaluated meshes of the saved `.blend` — well under the ~50,000
  triangle prop budget.
- The `.blend` contains two collections: `Model` (exported to the
  `.glb`) and `RenderSetup` (ground plane, sun, cameras; not
  exported). All model geometry is world-space with unit scale;
  origin at the medallion centre, ground level.

## Files

- `build_sy_fountain_basin.py` — re-runnable build script (bpy);
  all dimensions are named constants at the top, grouped into
  plan-measured / photo-estimated / inferred.
- `sy-fountain-basin.blend` — model + render setup.
- `sy-fountain-basin.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` — neutral
  grey backdrop, 960 × 720. Front is the south elevation (the
  garden side, medallion bulge toward the viewer); side is the
  view along the arm axis from the west; three-quarter is an
  elevated view from the south-west, like the period photographs.
  The prop is 138 m wide and 0.86 m tall: the elevations are
  honestly thin, and the plan-form carries in the three-quarter.
- `refs/` — the plans and photographs used, a working crop of the
  1856 plan's basin pair, and `REFERENCES.md`.
