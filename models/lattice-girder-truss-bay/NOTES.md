# Lattice girder / truss bay — notes

One 24 ft (7.315 m) structural bay of the Hyde Park 1851 building, as two
alternative members stacked for comparison — **not** an as-built assembly:
the cast-iron lattice girder below, one bay of the wrought-iron roof truss
above it (0.30 m display gap between them), and short column stubs under
the girder ends as end conditions only. This is the repeating frame unit
the interior views are made of; it complements `hyde-park-column-tier1/`
(column + girder stub) with the full spanning members.

## Sources (all in `refs/`, all public domain)

- `plate-010.jpg` — Downes (1852), PL. 10 "Wood Trusses and Cast Iron
  Girders". Fig. 3 (cast-iron girders under roof) is the girder's source.
  Downes plates: PD (published 1850s; scans via Internet Archive / McGill).
- `plate-011.jpg` — Downes, PL. 11 "Wrought Iron Trusses for Roof".
  Fig. I (48 ft truss under glass roof) is the truss's source.
- `section_1.png` … `section_7.png` — Wikimedia Commons section details
  (PD, per `references/muse-drive/data/manifest.csv`): cross-sections of
  the girder-truss top rail (single bar; composite), bottom rail
  (composite), extra-strong girder top rail, gallery-girder flange/rail,
  gallery-girder upright, and a louvre blade. They confirm the chords are
  composite rails built from bars and angles, as modelled.

## What was built

**A. Cast-iron lattice girder (PL. 10 Fig. 3)** — 24 ft span between column
centres; T-section top chord; inverted-T bottom chord with the wider
flange; X-lattice web in three 8 ft panels; square end posts C;
cruciform section verticals B at the third points (the plate's enlarged
section b.b). The two bars of each X pass one another at slightly offset
depths, as cast lattice bars do — they are not welded through each other.

**B. Wrought-iron roof-truss bay (PL. 11 Fig. I)** — one 24 ft length
(three 8 ft panels) of the 48 ft truss: top chord a pair of angle irons,
bottom chord a pair of flat bars, X diagonals in flat bars, cruciform
cast-iron standards *d* at the intermediate panel points, T-section end
standards, and the 1⅛ in joint pins shown in the plate's end detail.

**C. Column stubs** — 0.45 m cruciform stubs with base plates under the
girder ends, purely to give the girder its bearing condition.

## Dimensions — measured / printed vs inferred

Printed on the plates (read at full resolution):

- Span 24 ft 0 in, column centre to centre — both plates. Model: 7.315 m.
- Girder depth: the dimension chain at Fig. 3's right end prints
  3 ft 1¼ in as its main depth figure; PL. 8 prints a 3 ft girder depth
  (see `hyde-park-column-tier1/NOTES.md`). Model overall depth 0.965 m
  (3 ft 2 in), consistent with the plate-measured overall ≈ 3 ft 1½ in.
- Truss member sizes, PL. 11 Fig. I: top chord two angle irons
  4 in × 2 in × ¼ in; bottom chord two bars 4½ in × ¼ in; diagonals
  bar 4 in × ⅞ in and wood 3½ in × ⅞ in; standards at 8 ft 0 in centres;
  joint bolts 1⅛ in diameter. Modelled at those sizes.
- Truss depth: no overall depth is printed legibly on Fig. I; measured
  on the plate calibrated by its printed 48 ft length — ≈ 5 ft 6 in.
  Model: 1.676 m, plate-measured, ± ~3 in.

Inferred (flagged, not documented):

- Girder flange widths (top 0.23 m, bottom 0.30 m), flange thickness
  (0.028 m), web-bar width (0.14 m) and thickness (0.022 m) — read from
  the elevation's proportions and the enlarged section glyphs, which are
  drawn without a usable scale in the copies held here.
- Truss diagonal thickness (both diagonals modelled as 0.022 m iron
  bars; the plate makes one of each pair a 3½ in × ⅞ in wood bar — the
  pairing is recorded here but not material-distinguished in the model).
- End-standard and column-stub sections (0.28 m cruciform stub) follow
  the PL. 11 standard details at reading size, not from printed figures.
- Paint: a single dark grey-green iron colour for both members; the
  plates give no colour information in these figures.

## Known inaccuracies

- The two members never stood stacked as shown; in the building the
  girders carry floors and roofs at different levels. The stack is a
  comparison exhibit for the film's component library.
- Only one 24 ft bay of the 48 ft truss is modelled (half the truss);
  the full truss is two such bays meeting at a centre standard.
- Rivets and joint plates are omitted except the panel-point pins;
  chord splices are not modelled.
- The girder's chord sections are simplified T forms of the composite
  rails the section glyphs show.

## Build

Procedural Blender (bpy), script in `scripts/build_lattice_girder_truss_bay.py`;
renders on the fixed neutral-grey rig in `scripts/render_rig.py`.
50 objects, 856 triangles. Metres, origin at base centre (underside of
the column stubs), scale applied. Overall bounding box 7.735 × 0.42 ×
3.391 m — the 7.735 m includes the column-stub base plates, which
overhang the 7.315 m span between column centres by 0.21 m at each end.
Renders: `front.png` (elevation), `side.png` (end view), `three-quarter.png`,
plus `compare-plate10-fig3.jpg` and `compare-plate11-figI.jpg` setting the
front render against the two plate elevations.
