# Crampton locomotive "Folkestone" — notes

**Subject.** South Eastern Railway 4-2-0 Crampton patent locomotive
No. 136 "Folkestone", built by Robert Stephenson & Co., Newcastle
(works no. 787), 1851, and exhibited in the moving-machinery court of
the Great Exhibition, Hyde Park (film scene CP024). The nameplate was
cast with the single-E spelling **FOLKSTONE**; the model keeps it, as
photographed.

## Source

One reference only, copied into `refs/`:

- `refs/Great_Exhibition_No_136_Folkstone_by_HF_Talbot_1851.jpg` —
  Henry Fox Talbot calotype, dead-level side elevation of the engine
  as exhibited (public domain; repo manifest: "Mounted Calotype
  depicting South Eastern Railway 4-2-0 Crampton locomotive no 136
  'Folkstone' at the Great Exhibition of 1851", from Talbot's
  presentation report, 1852).

It is a single view. The front is partly hidden behind a building
column; the far side, the top and everything between the frames is
not seen at all.

## Dimensions

Published for this engine (Stephenson works list for the SER
Cramptons; cylinders 15 × 22 in, weight 26 long tons 5 cwt):

- Driving wheels **6 ft = 1.8288 m**
- Bogie wheels **3 ft 6 in = 1.0668 m**

These two anchor the scale. All other proportions were measured on
the calotype at **4.303 mm/px** (driver read vertically, hub centre
to rail contact = 425 px; the horizontal width is inflated by the
far driving wheel showing through the spokes, so it was not used).
Cross-check: the crank-pin offset measured on the photograph is
0.28 m, matching half the published 22 in stroke.

Photo-measured (metres, u = from front buffer-beam face):

| Feature | Value |
|---|---|
| Length over frames | 7.62 |
| Length over buffers | 8.30 |
| Wheelbase, axle 1 → driver | 5.18 |
| Bogie axle spacing | 1.36 |
| Boiler barrel diameter | 1.12 |
| Boiler centre above rail | 2.02 |
| Chimney top above rail | 4.04 |
| Rear stack top above rail | 3.58 |
| Footplate height | 1.28 |
| Nameplate (oval) | 0.93 × 0.47 |
| Maker's plate (oval) | 0.86 × 0.55 |
| Leaf spring span / peak | 1.14 / 1.79 |

Model: **22,964 triangles**, 173 objects, overall 8.30 × 2.64 × 4.04 m
(the Y extent is set by the access steps; z = 0 is rail level, origin
at base centre, front of engine toward −X).

## The plates

Both plates' lettering is legible in the calotype and is transcribed,
not invented. Nameplate: "FOLKSTONE / 1851". Maker's plate:
"STEPHENSON & Co ENGINEERS NEWCASTLE" (rim), "SOUTH EASTERN RAILWAY /
LONDON TO PARIS / FOLKSTONE & BOULOGNE / & DOVOR & CALAIS" (lines),
"CRAMPTON PATENTEE" (rim) — "DOVOR" is as it appears in the calotype
crop. The textures are legibility redraws in a period serif
(`scripts/make_textures.py`), applied as decals on the barrel and
splasher panel; they are not facsimiles of the castings' letterforms.

## Seen vs inferred

**Seen in the calotype (near side):** tall chimney with flared cap;
long low boiler with handrail and bands; nameplate; feed clack and
pipe on the barrel side; the large laminated leaf spring over the
bogie; deep plate frames with scalloped arches and rivet rows;
axleboxes and the rod linking the bogie axleboxes; the intermediate
crankshaft boss and the polished outside coupling rod to the driving
wheel's crank pin; the splasher panel with painted lining and the
maker's plate; the backhead silhouettes (whistle finial, tall column,
lever, ring handle); the polished bell-based casing at the rear of
the boiler with its neck and flared lip.

**Inferred (flagged, not observed):**

- The far side is mirrored throughout, including both plates.
- All widths come from period practice and the standard gauge:
  wheels at ±0.78 m inside outside frames at ±0.94 m, footplate
  2.44 m wide, firebox wrapper 1.50 m wide.
- The inside cylinders, crossheads and main rods are not visible in
  the photograph. They follow the published arrangement for these
  engines — inside cylinders driving an intermediate crankshaft in
  front of the firebox, the crankshaft coupled to the driving wheels
  by the outside rods that *are* visible — but their exact form here
  is a reconstruction.
- Rear buffer beam and buffers (the rear of the engine is in shadow).
- The exact layout of the backhead fittings; the items are seen, their
  arrangement is approximated. The hanging chain visible in the
  photograph is omitted.
- The leaf spring is duplicated to the far side (one spring is seen,
  outboard of the near frame).
- Splasher top cover, ashpan form, front drain pipes duplicated to
  both sides (one is seen).

## Known inaccuracies

- Single-view build: the smokebox front is largely occluded in the
  source, so the door, dart and cross handle are conventional readings
  of what the crop shows.
- The firebox wrapper top is a squashed-sphere approximation of a
  rounded wrapper.
- The rear polished casing is modelled by form only; its function is
  not asserted.
- The motion is a static pose (crank pins forward and slightly down,
  as photographed), not a working simulation.
- The leaf spring's nine leaves are nested at 15.5 mm pitch and read
  as one mass at a distance; the calotype's ribbed read is stronger.
- Finish is near-black throughout, following the calotype's tonal
  read; the engine's exhibition livery (likely lined) cannot be
  recovered from a monochrome plate.

## Files

- `crampton-locomotive-folkestone.blend` / `.glb` — the model
  (textures packed).
- `scripts/build_crampton_locomotive_folkestone.py` — procedural build.
- `scripts/render_views.py` — the shared neutral-grey rig (side view
  from −Y so the engine's front falls on the left, as in the calotype;
  `photomatch.png` uses a long lens to approximate the elevation).
- `scripts/make_compare.py` — stacks `photomatch.png` against the
  calotype crop in `renders/compare.png`.
- `scripts/make_textures.py` — plate texture redraws.
- `textures/` — the three plate/panel textures used by the build.
