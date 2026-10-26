# NOTES — Alhambra Court ornament panel

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 11).
Scene: CP041 (the Alhambra Court — geometric ornament and colour,
50 mm insert on one surface).
**Sydenham 1854 only** — no Hyde Park evidence is used in this model.

## The interpretation caveat (read first)

**This is Owen Jones's Victorian interpretation of Nasrid ornament,
not the Alhambra itself and not a neutral copy of it.** Jones designed
the Alhambra Court (opened 1854) and directed its colour scheme; the
1856 guide records that the court was built from "specimens of the
original casts of ornaments of the Alhambra, brought by Mr. Owen Jones
from Spain" and that "the patterns on the walls and ceilings [were]
taken from other portions of the Alhambra" (p.70) — i.e. even in 1854
the court's walls were a Victorian composite of motifs from different
parts of the Spanish palace, executed in painted plaster in south
London. This prop continues that chain honestly: its patterns are read
from the court's own two surviving views in the collection, and every
step away from those views is flagged below. It must not be presented
— in the film or in these notes — as a direct record of the Nasrid
Alhambra.

## What it is

One repeatable wall panel ("bay unit") of the court, plus a narrow
companion strip, composed as they are used together:

- **The panel** (3.60 × 3.60 m): a flat surface asset for court
  dressing, layered exactly as the court's walls are layered in the
  evidence, bottom to top: plain skirting; a **diamond-lattice tile
  dado**; a **zigzag dentil band**; a dark **inscription-style band**;
  a **sebka field** — a diamond net of shallow blue ribs with a small
  painted palmette in each diamond; a **roundel frieze**; a stepped
  cornice. The sebka net, roundel rings, zone ledges and cornice are
  real (shallow) geometry; the rest of the pattern is painted texture
  with a matching bump map, which is what CP041's surface insert
  needs.
- **The medallion strip** (0.56 × 3.60 m): the entrance piers' stacked
  **quatrefoil medallions** on a fine star-diaper ground, as a
  separate object so scene builders can set it at bay divisions and
  door/window framing, as the court's entrance screen uses it.

Origin at the base centre of the *panel*; the strip stands abutting
its left edge in the file (centre x = −2.08 m) as the default bay
arrangement. Units: metres. Blender 4.5.3. The unit tiles
horizontally: panel + strip repeat at a 4.16 m pitch with no pattern
break (see `renders/tiled-front.png`).

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- Coloured print "Entrance to the Alhambra Court" (round-1 catalogue
  0108, the plan's "image lead 0108") — the court's only view in the
  collection; composition and colour register.
- 1856 guide p.66, woodcut of the same view — the pattern source
  (medallions, inscription bands, zigzag band, diamond dado, sebka
  upper walls; and in its interior view, the roundel frieze and the
  same dado inside the Court of the Lions).
- 1856 guide p.67, "Ground Plan of the Alhambra" (catalogue 0246) —
  court layout only.
- 1856 guide pp.68–70, court text — "rich arabesque work in coloured
  stucco"; walls "covered with diaper work, consisting of
  inscriptions in Arabic character, of conventional representation
  of flowers and of flowing decoration"; court 75 ft long; Court of
  the Lions arches full-size; patterns taken from other parts of the
  Alhambra; Jones's casts.

**Evidence limitation, stated plainly:** the task brief allowed the
panel to be built from Owen Jones's published Alhambra ornament
plates if the court views proved too distant. The views were *not*
too distant (the p.66 woodcut is the same view as the coloured print,
at full resolution, and its patterns are legible) — and Jones's
plates are in any case **not in this collection** (searched: the
*Grammar of Ornament* appears only as a skipped-budget manifest
entry; his *Alhambra* volumes and his 1854 court handbook are absent).
Per MUSE-PROMPT §2 nothing was copied from outside the repo. Every
motif below is therefore read from the court's own views; where a
motif is read at the limit of the engraving, that is said.

## Dimensions — measured vs derived vs adopted

| Part | Value | Status |
|---|---|---|
| Panel width × height | 3.60 × 3.60 m | **Adopted** (see below) |
| Dado zone height (incl. zigzag + inscription bands) | 0.86 m of 3.60 m = 23.9% | **Derived** from a **measured** ratio: on the p.66 woodcut (visual grounding) the dado top sits at 24.7% of the entrance wall's height (floor y=731, zigzag band y=607, wall top y=228, in 0–1000 image units) |
| Skirting | 0.12 m | Adopted (plain base in both views) |
| Dado field | 0.12–0.86 m | Derived (as above) |
| Dado diamonds | 0.36 wide × 0.185 m high | **Proportioned** from the woodcut (diamonds read 2:1, light lattice on dark — see crop) |
| Zigzag band | 0.86–0.98 m | **From the woodcut** (dark triangles on light, directly above the dado) |
| Inscription-style band | 0.98–1.16 m | **From the woodcut** (a dark band with light script caps the dado zone on the piers) — but see "not modelled" for its content |
| Sebka field | 1.16–3.10 m | **From the views** (the upper walls' diamond diaper) |
| Sebka diamonds | 0.45 wide × 0.485 m high | **Proportioned** from the woodcut's upper-wall diaper; chosen so 8 × 4 diamonds divide the field exactly |
| Roundel frieze | 3.10–3.43 m; roundels Ø 0.27 m | **From the woodcut's interior view** (the band of circles above the Court of the Lions arches) |
| Cornice | 3.43–3.60 m | Adopted plain stepped cap |
| Slab thickness | 0.12 m | Adopted (a dressing panel, not a wall build-up) |
| Medallion strip width | 0.56 m | **Derived**: measured on the woodcut, the pier ornament strip is 0.154 × the wall height; 0.154 × 3.60 m = 0.554 m |
| Medallions | 7 stacked, pitch 0.514 m | **Counted/proportioned** from the pier crop (≈5½ medallions over the upper zone; 7 over the full panel height at the measured pitch ratio) |

**The adopted overall size (the weakest numbers in this prop):** no
dimensioned drawing of any Alhambra Court wall or panel exists in the
collection, and neither view carries a scale. What the sources fix is
*proportion* (the measured ratios above) and *context*: the court was
75 ft long (guide p.68), its Court of the Lions arches were full-size
(p.69), and it stood in the building's side-aisle zone (the Egyptian
prop's derivation gives a 24 ft aisle module). The 3.60 m square is
adopted as a dressing height inside that context — tall enough to
carry the measured layering at human scale (dado top at 0.98 m ≈
waist height, as the views show against their figures), square so the
sebka net divides exactly. **Treat the panel's absolute size as
±25%**; its internal proportions are the evidenced part.

## Pattern — how each motif was read

- **Diamond-lattice dado.** Direct from the p.66 woodcut (entrance
  piers) and confirmed inside the court (the wall behind the lions
  fountain): dark diamonds separated by light diagonal lattice lines,
  tiny light dots at crossings. This is the tile dado (azulejos) of
  the original rendered in the court's painted plaster.
- **Zigzag dentil band.** Direct from the woodcut: a single row of
  dark triangles on a light ground capping the dado.
- **Inscription-style band.** The woodcut shows a true inscription
  band (cursive Arabic) here and flanking the medallions. **The band
  in this prop is abstract interlaced knot-blocks, not letterforms**
  — decorative geometry in the band's place and colours. No text was
  copied or invented; the film must not present this band as writing.
  (Same convention as the Egyptian prop's procedural glyph marks.)
- **Sebka field.** The upper walls of the entrance view are a diamond
  net diaper with a small floral motif in each diamond (clearest in
  the coloured print's spandrel crop); the interior pier panels show
  the same net finer, with dots. Modelled as shallow geometry ribs
  (16 mm proud — cast-plaster relief in Jones's manner) over a
  painted palmette per diamond.
- **Roundel frieze.** Direct from the woodcut's interior view: a row
  of circles with flower centres running above the arches. Painted,
  with a shallow blue ring in geometry over each roundel.
- **Quatrefoil medallions.** Direct from the entrance piers: a
  vertical chain of four-lobed medallions, each filled with symmetric
  arabesque scrollwork, on a fine star-diaper ground, framed by
  inscription bands. Here the fill is a procedural symmetric
  arabesque (star, palmettes, scroll curls) in the medallion's
  colours — the engraving's scrollwork is legible as a *type*, not
  traceable line-for-line at this resolution, and is not claimed to
  be a tracing.

## Paint and polychromy

- **Attested** (coloured print 0108, the only colour source): warm
  gold/cream stucco grounds; inscription bands very dark blue-black
  with light script; dado diamonds dark with light lattice lines;
  the whole court reads gold-dominant with dark accents.
- **Interpretive, labelled as such** (Jones's published primary
  scheme for the court — blue, red and gold — applied in his manner,
  as with the Egyptian prop's palette): the sebka ribs and roundel
  rings in deep blue; palmette accents alternating red/blue/green;
  the dado diamonds glazed deep teal-blue-green with gold dots;
  medallion fills dark blue with red/gold/green arabesque. The print
  is small and hand-coloured, so no specific colour here is claimed
  as measured; if a future source (e.g. Jones's handbook, not in the
  collection) gives the court's exact scheme, repaint from it.

## What was NOT modelled / known inaccuracies

- **No arches, columns, muqarnas or room geometry** — per the build
  note, one panel, not a court. The entrance arch and its stalactite
  intrados (prominent in both views) are a different prop.
- **No real inscriptions** — see the band note above. The court's
  Arabic inscriptions are replaced by abstract knotwork everywhere
  in this prop, deliberately.
- **Relief is shallow and regular.** Jones's court ornament was
  cast plaster, crisp but hand-finished; this prop's ribs are
  machine-regular, and the painted patterns are flat with bump only.
  At CP041's intended insert distance this reads correctly; it will
  not pass as hand-carved stucco in extreme close-up.
- **The back and edges are plain** (a dressing panel; the slab's
  sides are unornamented stucco colour).
- **No weathering or later states**: the prop is the court as opened
  in 1854.

## QC (2026-10-26)

- Views read at full resolution; the two measured ratios (dado
  fraction, strip width fraction) taken by visual grounding on the
  p.66 woodcut, values in the table above. Texture patterns were
  proofed as images against the woodcut crops before building (the
  dado's first proof pasted its lattice in the wrong colour and was
  corrected; the medallions' first proof was too wide and too empty
  and was redrawn denser and narrower).
- **First build defect (caught by pixel audit, fixed):** the sebka
  net rendered pure black in the front view although its material
  was mid-blue and the same material rendered blue on a test cube.
  Isolation (material swaps, object-hiding, re-aimed sun, rebuilt
  mesh — all still black) traced it to the net's construction: the
  first script drew **every net edge twice**, as exactly coincident
  cube pairs joined into one mesh; the coincident pairs self-shadow
  in Cycles and crush to black (boundary edges, drawn once, rendered
  blue — the tell). The shipped build generates each edge **once**
  (128 segments) as a single bmesh with identity transform; a pixel
  audit of the new front render counts 2,594 blue rib pixels against
  85 dark (first build: 2,233 dark, ~0 blue).
- A VM/service restart killed the first corrected build during its
  fourth render; front/side/three-quarter (already written from the
  identical scene code) were kept and the tiled render was completed
  by `scripts/resume_tiled.py`, a variant of the build script with
  the scene construction byte-identical and only that render enabled.
- Counts, verified three ways (build log, re-opening the saved
  `.blend`, parsing the exported `.glb` — all agree): **14 objects,
  3,964 triangles** — well under the ~50,000 triangle prop budget.
  World bounding box: 4.16 m wide (strip −2.36 m to panel edge
  +1.80 m) × 0.15 m deep (ribs proud of the 0.12 m slab) × 3.60 m
  high. All four textures are packed in the `.blend` and embedded in
  the `.glb`.
- The `.blend` contains three collections: `Model` (exported),
  `RenderSetup` (ground, lights, cameras; not exported) and
  `TiledSetup` (two render-only copies of the unit used for
  `renders/tiled-front.png`; not exported).

## Files

- `scripts/build_sy_alhambra_ornament_panel.py` — the re-runnable
  bpy build script; dimensions are named constants at the top,
  grouped by evidence status.
- `scripts/make_textures.py` — procedural painted textures (system
  python3 + PIL; run before the build script).
- `scripts/resume_tiled.py` — the resume variant described in QC.
- `textures/` — panel front/bump and strip front/bump PNGs.
- `sy-alhambra-ornament-panel.blend` — model + render setup.
- `sy-alhambra-ornament-panel.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` — neutral
  grey backdrop, same lighting, 1024 × 768; `renders/tiled-front.png`
  (1600 × 1000) shows three bay units repeated. Front shows the bay
  unit (strip + panel); side is the panel's thin edge; three-quarter
  is the CP041 establishing view.
- `refs/` — the two court views, the guide plan and text pages, six
  enlarged crops, and `REFERENCES.md`.

Staged locally for review; not yet pushed to the repo.
