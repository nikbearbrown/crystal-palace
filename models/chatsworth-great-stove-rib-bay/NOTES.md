# chatsworth-great-stove-rib-bay — build notes

**What this is:** one full-width transverse rib bay — a structural slice —
of Paxton's **Great Stove (Great Conservatory) at Chatsworth, Derbyshire,
1836–40**: the curved laminated-timber arch ribs, cast-iron pillars,
ridge-and-furrow glazing and masonry base of the building that is the
direct ancestor of the Crystal Palace's construction system. An
ancestor-study prop for the Chatsworth passage of the film (scene CP005;
the build plan files the Chatsworth material under CP003–CP005).

**What this is NOT:** it is not the Crystal Palace — not Hyde Park 1851
and not Sydenham 1854 — and it must never be dressed as either. It is a
timber-and-iron glasshouse of the previous decade: no 8-ft Palace module
grid is claimed for it, no Palace iron column or Paxton gutter from the
1851 building is reused, and its profile (a tall elliptical central vessel
stepping down through two glazed side aisles to a stone plinth) is
Chatsworth's own. It is also not the Chatsworth Lily House (1849, the
Victoria Regia house) — a different, smaller building.

## Relationship to models/chatsworth-glasshouse-rib-bay/ (read first)

That package already occupies the plan's item-20 slug. It is a small
**illustrative** bay — semicircular arc, 6.0 m span, 3.0 m rise, 4.0 m
bay, every dimension guessed by its builder's own NOTES, no Chatsworth
figure sourced. This package is the evidence-derived counterpart: a
full-width slice at the Great Stove's printed real size (37.49 m wide,
20.42 m high), with the profile read from the period photograph. The two
are complements, not duplicates: keep the other as the lightweight
illustrative study; prefer this one wherever the Great Stove's actual
form and scale matter. First-to-main was not overwritten; this ships
under a distinct slug per project convention.

## Sources and scale derivation

Full citations in `refs/REFERENCES.md`. The section is dimensioned from
**period printed figures** (Morris, *Picturesque Views of Seats*,
pp. 49–52; *Black's Guide* 1864; Cokayne 1889 — all agreeing), and its
form is read from the **19th-century photograph** in the project
collection (round-2 `S03`). No published dimensioned section drawing of
the Great Stove was found in the collection or on the web, so the
derivation is: printed overall figures fix the section's control points;
the photograph fixes the curve family between them.

| Dimension | Value | Basis |
|---|---|---|
| Overall width | 123 ft = 37.490 m | **Printed** (Morris / Black's / Cokayne) |
| Central arch span | 70 ft = 21.336 m | **Printed** (same) |
| Crown height | 67 ft = 20.422 m | **Printed** (same) — adopted over the modern official figure, see Uncertainties |
| Pillar height = arch springing | 28 ft = 8.534 m | **Printed** (same) |
| Building length | 276 ft = 84.1 m | Printed, **not modelled** (one bay slice only) |
| Central rise above springing | 39 ft = 11.887 m | Derived: 67 − 28 ft |
| Aisle width, each side | 26.5 ft = 8.077 m | Derived: (123 − 70) / 2 ft |
| Central profile | half-ellipse, semi-span 10.668 m, semi-rise 11.887 m | **Photo-read form** through the printed control points: the photograph shows the curve steep at the springing and flattening across the crown — an ellipse, not the semicircle of the illustrative package and not a pointed/gothic curve |
| Side-aisle profile | quarter-ellipse, run 7.932 m, rise 5.90 m | Photo-read form between valley and wall line |
| Valley level (side roof top) | z = 7.90 m | Photo-proportioned against the printed springing/crown; **inferred** |
| Side glazing foot | z = 2.00 m | Photo-proportioned (top of the ventilator band); **inferred** |
| Stone plinth height | 1.05 m | Photo-proportioned; **inferred** |
| Bay width | 8 ft = 2.438 m | **Inferred** — not printed for the Stove. Paxton's ridge-and-furrow work was laid out on regular rib spacing and the photograph's rib density across the 276-ft length is consistent with a spacing of this order; stated as an assumption, not a measurement |
| Furrow pitch / amplitude | 0.406 m / 0.055 m | **Inferred** from the furrow striping density in the photograph |
| Rib section, central | 0.30 m deep × 0.15 m wide | **Guessed** — no Chatsworth source found; plausible for a laminated timber arch of this span |
| Side arch section | 0.20 × 0.11 m | **Guessed** |
| Pillar diameter | 0.25 m | **Guessed** — period sources say cast-iron pillars, no diameter printed |

## Rib construction

Per the standard account (see REFERENCES), the arched elements were
**laminated timber** — thin boards bent and built up into the curve —
carried on **cast-iron columns**, with the side arches buttressing the
central vessel over the flanking aisles. Modelled accordingly:

- **Central rib** at each end of the bay (y = ±1.219): five stacked
  lamination bands (5 × 0.06 m = the 0.30 m radial depth), each band a
  run of short segments following the ellipse, in three close painted
  tones so the layering reads as banding. The layers are *suggested*,
  not modelled plank-by-plank, per the brief.
- **Side arches**: single lighter sweeps on the same principle, carried
  down past the glazing foot to stone corbels on the plinth.
- **Pillars**: cast-iron, Ø 0.25 m (guessed), with base block and
  capital plate, at the printed 28-ft height; iron springing blocks at
  the rib feet; iron valley gutters where the central vessel meets the
  side roofs.
- **Purlins and glazing bars** run the bay length at the furrow ridges;
  the glass itself is a continuous mesh displaced in a triangular
  zigzag across the bay, so the ridge-and-furrow profile is real
  geometry following the rib curve on all three tiers, as the
  photograph shows.
- **Base**: rusticated stone plinth wall with one wide shallow-arched
  recess per bay per side (photo-read: the arches sit between piers at
  rib rhythm), and above it the **diagonal-lattice ventilator band**
  that the photograph shows at the foot of the side glazing, panelled
  between the rib feet.

Materials are read from a black-and-white photograph and period
practice, so all colours are **interpretive**: painted timber in pale
warm off-white (the structure reads pale in the photograph), ironwork
dark grey-green, stone warm grey, glass pale blue-grey at ~50 % opacity
as a render stand-in (the real house carried upwards of 70,000 sq ft of
sheet glass).

## What was NOT modelled

- **End walls and the curved (hipped) ends** of the building, including
  the classical pedimented end portico visible in the photograph — they
  belong to the ends, not to a rib bay.
- The **interior**: the carriage drive that famously ran through the
  centre of the house, planting, rockwork and the interior gallery —
  none of it is part of a structural bay slice.
- The **heating plant**: eight underground boilers, ~7 miles of
  hot-water pipe and the coal vaults (period sources) — below ground
  and outside the section.
- Individual glass panes and fixings beyond the furrow bars; laminated
  plank end-joints (banding only); eaves gutter and rainwater detail at
  the plinth line.
- Foundations below ground level.

## Uncertainties (for the audit)

1. **Crown height conflict.** Period sources agree on 67 ft (20.42 m),
   adopted here. Chatsworth's official modern page gives 19 m (≈ 62 ft)
   for the same building. Length and width agree across both (276 ft ≈
   84 m; 123 ft ≈ 37.5 m), so the discrepancy is height-only and
   unresolved; if the modern figure is preferred, the central ellipse's
   semi-rise drops from 11.887 m to ~10.5 m and nothing else changes.
2. **Profile family** is photo-read, not drawn from a published
   section: ellipse arcs through printed control points. A true
   dimensioned section of the Great Stove, if one surfaces, should
   replace the valley level, glazing foot and plinth height (all
   currently photo-proportioned) and confirm or correct the ellipse.
3. **Bay width, rib and pillar sections** are inferred/guessed as
   flagged in the table — no source for any of them was found.
4. One secondary web source prints the length as 227 ft against the
   period 276/277 ft — treated as a transcription error; length is not
   modelled in any case.

## QC

- Triangles: **10,836** (script count on the Model collection; GLB
  accessor count agrees). Limit ~50k — well under.
- Model bounding box (verified on the saved .blend): 37.91 (x) × 2.88
  (y) × 20.52 (z) m. The printed 123 ft width is carried on the glazing
  line (x = ±18.60 at the foot, ±18.75 at the springing line); the
  stone plinth faces stand ~0.2 m proud of it, and the pillar base
  blocks project to y = ±1.44, just beyond the bay faces. Crown:
  glazing 20.49 m against the printed 20.42 (67 ft), the difference
  being the furrow ridge stand-off. Origin at base centre of the bay
  slice, z = 0 at ground, nothing below ground. All object scales 1.0
  (transforms baked into the meshes before joining).
- GLB contains exactly the 12 Model meshes (7 joined part meshes,
  3 glass meshes, 2 arch-recess panels). The RenderSetup collection
  (ground, sun, fill, 3 cameras) is in the .blend only, not exported.
- Renders viewed by the builder: front reads as the published section —
  tall central ellipse on its pillars, side sweeps stepping down to the
  plinths; side shows the furrowed strip, valley gutter, ventilator
  lattice and plinth arch in elevation; three-quarter shows the full
  stepped section with real ridge-and-furrow geometry on all tiers.
  An earlier build round had systematically distorted joined parts
  (bounding box 38.9 × 2.9 × 22.0 m, parts below ground) — cause found
  (a transform-apply after joining baked the first part's scale into
  each joined mesh), fixed by baking each part's transform before
  joining, and re-verified against the numbers above.

## Files

- `build_chatsworth_great_stove_rib_bay.py` — re-runnable bpy build
  script (Blender 4.5.3): model, .blend, .glb, three renders.
- `chatsworth-great-stove-rib-bay.blend` / `.glb`
- `renders/front.png`, `renders/side.png`, `renders/three-quarter.png`
  (960×640, Cycles CPU, neutral grey)
- `refs/REFERENCES.md`, `refs/great-conservatory-19c-photo.jpg`,
  `refs/crop-end-profile.png`, `refs/crop-base-arches.png`
- `NOTES.md` — this file
