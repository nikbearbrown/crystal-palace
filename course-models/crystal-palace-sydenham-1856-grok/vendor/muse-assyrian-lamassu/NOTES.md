# Assyrian human-headed bull (lamassu) — Nineveh Court, Sydenham

A single lamassu of the row that lined the façade of the Assyrian (Nineveh) Court
towards the nave at the Crystal Palace, Sydenham (film scene CP037). The Sydenham
figures were plaster casts/reconstructions of the Khorsabad (Dur-Sharrukin)
originals, made under the direction of A. H. Layard for the Nineveh Court
(opened 1854). Stylised architectural sculpture, built procedurally in Blender
4.2 (`scripts/build_lamassu.py`); no sculpting, no external assets.

## Sources

- **Album sheet, four Delamotte photographs** — repo path
  `references/muse-drive/images/commons/-Assyrian_Court,_Facade_Towards_the_Nave;_Elevated_View_of_Assyrian_Court;_Greek_and_Roman_Sculpture_Court;_The_Three_Graces-_MET_DP323102.jpg`
  (copied into `refs/`). Manifest licence: **CC0** (public domain);
  photographs by Philip Henry Delamotte, c. 1854–1855.
  Only the **top-left** photograph ("Assyrian Court. Façade towards the Nave")
  shows the bulls: a row of at least four, seen from front-left at slight
  elevation, plus standing attendant figures and the court arch. The other
  three photographs (elevated nave view, Greek & Roman Court, Three Graces)
  do not show the bulls and were not used for the model.
- No measured drawing of the casts exists in the repo references; all
  dimensions below are photo-derived estimates, chained as described.

## Dimensions and how they were got

Pixel measurements on the façade photograph (nearest bull vs. the painted
attendant figure visible in the court archway, and vs. the arch opening):

- Painted attendant figure ≈ 330 px tall; arch opening ≈ 585 px;
  nearest bull (hooves → crown top) ≈ 593 px; its plinth ≈ 27 px.
- Chain: taking the painted attendant as a life-size figure of **1.7 m** gives
  an arch opening of ≈ 3.0 m and a bull height of **≈ 3.05 m**; plinth ≈ 0.15 m.
  Both the figure and the arch are on/near the façade plane, so perspective
  error is second-order; overall uncertainty **±0.3 m** on the height.
- **Adopted:** statue 3.05 m tall above a 0.15 m plinth (total 3.20 m);
  body (chest front → rump) 2.91 m; body width 0.80 m; back height 2.12 m.
- Proportions (legs ≈ 0.37 of height, body depth ≈ 0.31, crown ≈ 0.15,
  wing tip ≈ 0.33 above the back) measured as pixel fractions of the nearest
  bull's height in the same photograph.

## What was measured / seen in the photograph

- Row of slab-sided, high-relief-style bulls standing on low individual
  plinth slabs against the façade.
- Human head in profile: tall tiered cylindrical crown with a ribbed top rim,
  a band carrying two rows of dots (rosettes), and a diadem band below.
- Long rectangular beard of tight curl rows hanging down the chest front;
  curled hair masses at the sides of the head; small bovine ears.
- One raised wing per side lying flat over the back: long, low, sweeping back,
  its primaries carved as long near-parallel lines; a covert band of scales at
  the wing root.
- Rows of overlapping scallop scales covering the shoulder and the hindquarter,
  and an apron of scales down the chest front.
- Four legs with cloven hooves and a carved ring above each hoof; a ribbed
  band under the front of the belly; tail hanging behind the hind legs with a
  tuft at the end.

## What is inferred / guessed

- **Absolute scale** — chained from the painted attendant as above; no
  dimensioned source. If the attendant painting is not life-size, the whole
  model scales proportionally (it is built parametrically).
- **Far side and back** — never photographed; mirrored from the visible side.
  The casts were made to be seen from the nave, so the wall side was probably
  plainer than this model's finished far side.
- **Five legs?** The Khorsabad originals famously carry five legs (two seen
  from the front, four in profile). In the Delamotte photograph the leg count
  of the casts **cannot be resolved** — the visible hooves are consistent with
  four legs with the far pair offset, but a fifth leg cannot be ruled out.
  Modelled with **four**; treat the question as open.
- **Horns** — a horn-like curve at the crown base of the middle bull could not
  be resolved (it may be the ear and hair). Horns **omitted** rather than
  guessed.
- **Inscription band** — the originals carry a cuneiform band between the
  legs. The band is modelled (a shallow panel on each flank under the belly)
  but left **plain**: no cuneiform text was invented.
- **Colour** — the casts were painted; the model is a single stone grey (with
  a darker grey only to articulate hair/beard/hooves in renders). No
  polychromy is asserted.
- Crown dot/rib counts, scale counts, feather counts are regularised readings
  of a partly illegible carved pattern, not counts from the object.
- The head is an idealised Assyrian-type face assembled from primitives; the
  photograph's profile was matched for proportions, not portrait detail.

## Files

- `assyrian-lamassu.blend` / `.glb` — the model (origin at base centre,
  metres, scale applied; plinth included as part of the prop).
- `renders/` — front, side (the figure's left, the photographed side),
  three-quarter, photo-match and a side-by-side `compare.jpg`, all on the
  fixed neutral-grey rig in `scripts/render.py`.
- `refs/` — the album sheet used.
- `scripts/` — `build_lamassu.py` (build + stats + export),
  `render.py` (rig), `make_compare.py` (compare sheet).

## Stats

- Triangles: 40,192 · Objects: 102
- Bounding box: 3.770 × 1.320 × 3.202 m (length × width × height, incl. plinth;
  the plinth and its step set the length/width — the statue itself is
  3.50 × 0.99 × 3.05 m, nose to tail)
