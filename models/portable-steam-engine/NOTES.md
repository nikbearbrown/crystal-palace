# Portable steam engine — Garrett & Sons, Great Exhibition 1851

Candidate #29 in `models/CANDIDATES.md`. Hyde Park 1851, agricultural
section (film dressing for CP024/CP025). The engine is modelled as the
**Garrett** machine; the Hornsby engine in the companion photograph is
documented below but not built, and the threshing machine attached to
it is not built either.

## Sources

Both references are calotypes by Henry Fox Talbot from his presentation
report on the Great Exhibition (Spicer Brothers / W. Clowes & Sons,
1852), copied into `refs/`:

- `refs/garrett-side.jpg` — repo path
  `references/muse-drive/images/commons/Great_Exhibition,_Agricutlural_Implements,_HF_Talbot,_1851.jpg`
  (the filename carries the source's own "Agricutlural" spelling).
  Side aspect of the Garrett engine, outdoors, printed caption
  "GARRETT AND SONS". **Public domain** per the repo manifest.
- `refs/hornsby-opposite.jpg` — repo path
  `references/muse-drive/images/commons/Great_Exhibition,_Agricutlural_Implements_2,_HF_Talbot,_1851.jpg`.
  The Hornsby engine from the opposite aspect, threshing machine
  attached, caption "HORNSBY AND SONS". **Public domain** per the
  repo manifest.

No dimensioned drawing of either engine exists in the references;
everything below is measured on the photographs or inferred.

## What the Garrett photograph shows (measured)

The plate is a near-side elevation but yawed roughly 25°, so
horizontal extents were corrected ×1.10 and all primary proportions
were taken from **vertical** extents, which yaw does not compress.
Measured on a grid overlay of the Garrett calotype (ground line =
wheel contact):

- Layout, firebox end → smokebox end: backhead plate with a cluster
  of small fittings (fire door, gauge cocks, handwheel, hanging
  lever, copper pipe runs); rectangular firebox wrapper below the
  barrel; a horizontal **cylinder on top of the boiler at the firebox
  end**; a large steam dome with a banded base and flared cap rising
  behind the cylinder's rear half; whistle pipe; a tall thin
  safety-valve/gauge column; a flyball governor at mid-boiler with a
  thin drive belt running forward; a long connecting rod along the
  boiler top to a **crankshaft carried over the smokebox end**; the
  **flywheel on the far side** of the crankshaft; tall chimney (two
  brass bands, flared base and cap) over the smokebox; a slender
  vertical feed-pump rod down the smokebox front face.
- Four road wheels in two pairs of **different** sizes: the pair
  under the smokebox end is the larger (Ø 158 units against the
  barrel's 100), the pair under the firebox end smaller (Ø 121).
  Spokes counted: 14 on the large wheels, 12 on the small, 6 on the
  flywheel. A long tie rod links the axles along the side; a drawbar
  leaves the firebox end toward the seed drill in the photograph.
- Flywheel Ø ≈ 1.90 × barrel Ø, its centre a little above the
  barrel's top line; rim bottom ≈ 1.1 m above ground.

## Dimensions and their provenance

**Absolute scale is inferred, by this chain:** proportions were
measured on the calotype as above; the scale was then anchored on the
large road wheel at **1.45 m (4 ft 9 in)**, a standard period size for
the carrying wheels of a mid-size portable. Every other dimension
follows from the measured ratios. Nothing here is a documented Garrett
dimension.

| Part | Model value | Basis |
|---|---|---|
| Boiler barrel | Ø 0.92 m, centreline 1.47 m above ground | measured ratios (Ø = 100 grid units; centre 160 units above ground) |
| Overall length (body) | 3.30 m; 4.65 m overall footprint incl. drawbar and the flywheel's overhang past the smokebox | measured, yaw-corrected |
| Overall height | 4.26 m to chimney top | measured (463 units) |
| Wheelbase | 2.33 m | measured between hub centres |
| Large road wheels | Ø 1.45 m, 14 spokes | **scale anchor**; spokes counted |
| Small road wheels | Ø 1.12 m, 12 spokes | measured ratio 1.30; spokes counted |
| Flywheel | Ø 1.75 m, 6 spokes, far side | measured ratio 1.90 × barrel Ø |
| Chimney | Ø 0.30 m, top 4.26 m | measured |
| Steam dome | Ø 0.54 m base, top ≈ 2.51 m | measured |
| Cylinder | Ø 0.34 m × 0.86 m, on boiler top | measured position; bore class inferred |
| Track (wheel centres) | 1.76–1.80 m | **guessed** — no end view survives; period practice |

## Measured vs guessed

- **Measured/seen** (Garrett calotype): the whole layout above; both
  wheel sizes and spoke counts; flywheel size, side and position;
  dome, governor, chimney form and banding; the long top connecting
  rod; the backhead fitting cluster (individual functions of the
  smallest fittings are read approximately).
- **Inferred**: absolute scale (chain above); all widths across the
  machine (track, tyre widths 0.13/0.11 m, firebox wrapper width
  1.04 m) — no front or rear elevation of the Garrett engine survives;
  crank pin pose (one frozen position); valve-rod and eccentric
  routing along the top; the governor belt as a single straight run;
  the turntable disc under the firebox-end axle; drawbar length.
- **Colour**: the calotypes are monochrome. The model uses black
  japan with brass barrel bands, dome and chimney bands — a period
  convention, **not** a recorded Garrett livery.

## The Hornsby engine (not built) — differences observed

From `refs/hornsby-opposite.jpg`, which shows the opposite aspect:

- The big/small wheel arrangement is **reversed**: Hornsby's large
  pair stands under the firebox end, the small pair under the
  smokebox/chimney end — the layout that later became standard.
- The flywheel is on the **camera side** and sits further back along
  the boiler, roughly over the wheelbase middle.
- The boiler is visibly **lagged** (ribbed wooden staves under brass
  bands); Garrett's barrel reads smooth and plain-banded.
- The firebox end carries a tall rounded-top vertical casing with a
  small brass dome, quite different from Garrett's barrel dome with
  its flared cap.
- Hornsby's chimney is shorter and stouter, with a plain flared lip
  and no bands.
- The Hornsby is photographed with a threshing machine coupled at
  its left (smokebox end); per the brief it is documented here only
  and deliberately not modelled.

## Known inaccuracies

- The motion work (valve rod, eccentric, governor drive) is a
  simplified reading of lines on the calotype, not a reconstruction
  of Garrett's actual gear; small backhead fittings are approximate.
- Wheel dish is only hinted (hub offset); spokes are straight
  rectangular-section, where the originals are shaped.
- The smokebox door dart is modelled as a simple cross handle.
- Widths across the machine are the weakest numbers in the model
  (see track, above).

## Build

Procedural bpy, Blender 4.2, script `scripts/build_portable_steam_engine.py`;
renders on the fixed neutral-grey rig, `scripts/render_views.py`;
`renders/compare.png` pairs the photomatch (taken from the
calotype's own ~25° angle) with the reference crop.
**18,800 triangles, 150 objects.** Origin at base centre (ground,
mid-length of the body), real-world metres, scale applied.
