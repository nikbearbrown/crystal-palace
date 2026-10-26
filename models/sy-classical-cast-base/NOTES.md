# NOTES — classical court cast pedestal (figure + bust variants)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 12).
Scenes: CP039 (antiquity in colour — coloured detail beside
sculpture); the module is the standard cast base for the whole
Sydenham classical-court sequence.
**Sydenham 1854 only** — no Hyde Park evidence is used in this
model, and no figurative sculpture is modelled: this prop is the
empty base a separately sourced cast stands on.

## What it is

The standard display pedestal of the Greek and Roman Sculpture
Court, as photographed by Delamotte (1854–55) and still in place
in the later stereo views: a plain, very dark, square-section box
pedestal whose only moulding is at the floor — a low projecting
foot step and a concave cove sweeping up to the die. The top is a
plain flat square: **there is no cap moulding**. In the photographs
each cast stands on its own light-coloured plinth slab, which
overhangs the die slightly and supplies the "cap" read; that slab
belongs to the cast, not to this prop, and is not modelled. The
prop's top face is a single clean bedding plane at full height so
scene builders can stand a cast (with or without its own slab) on
it.

Two variants of the one family are supplied, because the court
used both throughout:

- `CastBase_Figure` — the standing-figure pedestal, 0.91 m high,
  die 0.61 m square (the Aristides / Posidonius type).
- `CastBase_Bust` — the bust pedestal, 1.30 m high, die 0.46 m
  square (the Minerva type; the Greek Court's portrait-gallery
  busts of the Greek Poets stood on such pedestals).

Origin at the base centre of the pair's footprint, ground z = 0.
Units: metres. Blender 4.5.3.

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- Delamotte album, "Greek and Roman Sculpture Court" (MET
  DP323102, CC0) — the type in rows across the court; heights
  cross-checked against the figures and busts on them.
- Stereo "101. Statues in the Greek and Roman sculpture court"
  (Rijksmuseum RP-F-2012-96-327, CC0) — eye-level profile source;
  the Aristides and Minerva crops are the measured evidence.
  (Dated c.1870–90, but it shows the same court and the identical
  pedestal family as Delamotte's 1850s view.)
- 1856 guide p.55, "The Greek Court" (public domain) — court
  contents and the bust portrait gallery; its blue/red/yellow/gold
  colouring describes the court architecture, not the pedestals.

**Evidence limitation, stated plainly:** no dimensioned drawing of
these pedestals exists in the collection, and the 1856 guide never
describes them. Every absolute size below is derived from the
photographs against the casts on them, and carries the stated
uncertainty. The *profile* (step, cove, plain die, plain top) is
directly seen at eye level in the stereo view and is not in doubt.

## A correction to the expected profile

The build brief expected "base moulding, die, cap moulding". The
eye-level photograph contradicts the third element: both the
Aristides and the Minerva pedestals end in a plain square top
edge, and the light slab visible above it is the cast's own
plinth, a separate piece belonging to each statue (it is numbered
"324" in the photograph, the pedestal "325"). The model follows
the photograph, not the brief: base moulding and die only, flat
top. Nothing has been added to make the profile look more
"classical" than the evidence shows.

## Dimensions — measured vs derived

Measured on the stereo crops by visual grounding (bounding boxes
and corner points on the Aristides and Minerva pedestals):

| Quantity | Value | Status |
|---|---|---|
| Figure pedestal height ÷ statue height | 0.468 | **Measured** (Aristides: statue 564 units, pedestal 264, same view) |
| Bust pedestal height ÷ bust height (incl. socle) | 1.48 | **Measured** (Minerva: bust 277 units, pedestal 410) |
| Base moulding share of total height | ≈ 0.15–0.20 | **Measured** (corner points, both pedestals) |
| Die plan | square | **Seen** (Delamotte elevated view; both crops) |
| Foot-step projection beyond die face | ≈ 30–40 mm | **Read** from the crops (modelled 38 mm) |

Adopted sizes (derived from the ratios against life-size casts;
period casts of standing figures were life-size, and the guide's
numbering identifies the yardstick statues):

| Part | Value | Status |
|---|---|---|
| Figure pedestal, total height | 0.91 m (≈ 3 ft) | **Derived**: 0.468 × ~1.95 m cast; ±0.06 m |
| Figure pedestal, die | 0.61 m square (≈ 2 ft) | **Derived** from the crops' width/height read at the measured viewing angle; ±0.05 m |
| Bust pedestal, total height | 1.30 m | **Derived**: 1.48 × ~0.88 m bust + socle; ±0.08 m |
| Bust pedestal, die | 0.46 m square (≈ 1 ft 6 in) | **Derived**, same method; ±0.06 m |
| Base moulding height | 0.15 m (foot step 0.055 + cove 0.095) | From the measured share above; the same moulding serves both variants, as in the photographs |

The proportions rest on the two measured ratios; the absolute
sizes are the weak numbers (the yardstick casts' exact heights are
not printed in the collection) and are flagged accordingly. If a
scene needs the pedestals a few centimetres taller or shorter,
the evidence cannot refute it — but do not change the *ratios*
between die, base and height, which are the photographed facts.

## Paint and material

The pedestals print near-black in both photographic sources, in
sunlit and shaded views alike — a very dark painted finish, most
probably painted timber (the cheap, standard exhibition material;
nothing in the views suggests stone). **The hue is not recorded**
and no colour source for the pedestals exists in the collection:
the model uses a warm black-brown at satin roughness and makes no
colour claim beyond "very dark". This is separate from the
classical courts' architecture, whose polychromy the 1856 guide
attests (blue, red, yellow, gold) and which the storyboard in any
case flags as scene-level, not a property of this prop.

## The painted labels (omitted)

In the photographs every pedestal carries its catalogue number
and title painted in light letters high on the die's front face —
"325 / ARISTIDES OR AESCHINES / FROM NAPLES", "328 / MINERVA /
FROM MUNICH", "7 / ANDROMEDA / JOHN BELL". They are **omitted**:
this project does not fabricate inscription text, and a correct
label differs per cast in any case. Scene builders who need the
label should add the specific cast's real number and title as a
decal; the die's upper front face is where it belongs.

## Variants seen in the views, NOT built

- **Round drum pedestals** under urns and tazze (Delamotte
  elevated view: a large urn at the left edge and a tazza in the
  foreground centre, both on dark cylindrical drums, the tazza's
  drum shorter and wider). Same dark finish, different plan.
- **Low wide platform** under large groups (the Farnese Bull in
  the centre of the Delamotte view stands on a broad low dark
  platform with benches around it).
- **Low plain dark block** under historic carved bases (the Three
  Graces monument's own Renaissance base stands on one,
  ~0.35–0.45 m high). The carved base itself is part of that
  artwork and is sculptor work, not this prop.
- **Low nave pedestals** for modern sculpture among the planting
  (John Bell's Andromeda, ~0.5–0.6 m; the Farnese Hercules
  similarly), labelled like the court pedestals but lower — a
  nave, not a classical-court, context.
- **The later Sculpture Gallery pedestal** (Cain stereo,
  c.1870–90): light-coloured, panelled, with full cap and base
  mouldings. A different, later furniture type — recorded here so
  it is not mistaken for the 1854 court standard, and not built.

## What was NOT modelled / known inaccuracies

- **No cast, statue or bust** — deliberately; figurative
  sculpture is sculptor work in this project, never procedural.
- **The casts' own plinth slabs** — the light slabs seen on top
  of every pedestal in the photographs belong to the casts.
  This prop's bedding plane is the die's full top face; a cast
  placed on it should bring its own slab, overhanging ~40 mm
  as photographed.
- **The painted labels** (see above).
- **Construction** — the real pedestals are hollow timber boxes;
  the model is a solid loft of the same outside profile. Panel
  joints, if any, are invisible in the photographs and are not
  represented.
- **The cove profile** is a smooth concave sweep fitted to the
  photographs; the original moulding plane's exact curve (and
  whether it carried a small fillet at its head, as the Minerva
  crop hints) cannot be resolved at the photographs' resolution.
- No weathering, scuffs or later-state condition: the prop is
  the court as opened in 1854.

## QC (2026-10-26)

- Photographs read at full resolution from the collection files;
  both ratios (0.468 and 1.48) and the base-moulding share taken
  by visual grounding on enlarged crops of the Aristides and
  Minerva pedestals, values and method in the table above.
- First build's renders were inspected: the geometry and profile
  were right, but the cameras framed the pair too small, and the
  foot step read weakly against the Aristides photograph.
  Fixed and re-rendered: cameras moved in (6.8 m → 4.4 m), foot
  projection 30 → 38 mm, foot-step height 50 → 55 mm, paint
  darkened slightly. (An apparent taper of the dies in the first
  front render was checked at native resolution and is an
  off-axis perspective effect of the small preview, not
  geometry: the loft rings are constant-width, and the saved
  bounding box confirms it.)
- Final renders compared against the stereo crops: step + cove
  base, plain straight die, flat square top, very dark satin
  finish — all as photographed. Side render is end-on: the bust
  pedestal (nearer the side camera) occludes the figure
  pedestal, as with the Egyptian column pair prop.
- Counts, verified three ways (build log, re-opening the saved
  `.blend`, and parsing the exported `.glb` — all agree):
  **2 objects, 136 triangles** (68 per pedestal) — far under the
  ~50,000 triangle prop budget, as expected for a box pedestal.
  World bounding box: 1.956 m wide (footprint centred on the
  origin: x −0.978…+0.978) × 0.686 m deep × 1.30 m high
  (the bust variant's height).
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground plane, lights, cameras; not exported).
  Meshes are world-space geometry with identity transforms —
  unit scale, no rotation, everywhere.

## Files

- `build_sy_classical_cast_base.py` — re-runnable build script
  (bpy); dimensions are named constants at the top, grouped by
  evidence status.
- `sy-classical-cast-base.blend` — model + render setup.
- `sy-classical-cast-base.glb` — `Model` collection only
  (`CastBase_Figure`, `CastBase_Bust`).
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 1024 × 768. Front shows
  both variants side by side; side is end-on (bust pedestal in
  front); three-quarter is the CP039 dressing view.
- `refs/` — the Delamotte album page, the sculpture-court
  stereo card, four measurement crops, the Three Graces and
  Andromeda views, the Cain stereo (rejected variant), the 1856
  guide's Greek Court page, and `REFERENCES.md`.

Staged locally for review; not yet pushed to the repo.
