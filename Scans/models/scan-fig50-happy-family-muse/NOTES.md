# NOTES — scan-fig50-happy-family (Muse version)

## Subject

John Tenniel, **"The Happy Family in Hyde Park"** (*Punch*, 19 July 1851) —
catalog figure 50 — modelled as a stage vignette **as drawn**: the nations
of the world penned together inside a tall two-tier **barred cage** beneath
the Crystal Palace transept **fan window**, dancing in pairs, while large
foreground **spectators** watch from outside the bars. (The batch brief's
guess of families picnicking on grass is not what the image shows; the
image governed, per the standing rule.)

Contents: cage front 8.4 m wide × 4.3 m high (posts, three rails, ~35
vertical bars, short barred side returns, pale interior backdrop); ten
dancers in five pairs on a raised upper step and eight dancers in four
pairs on the cage floor, in varied dress silhouettes (top hat, turban,
cap, shako, conical hat; women in bonnets); the semicircular fan window
above (radial spokes, concentric inner arc, hub, translucent glazing,
radius 3.9 m, sill at 4.35 m) with a blank pennant flag at each top corner;
eight foreground spectators including the top-hatted gentleman with a cane,
the man pointing into the cage with a thin pointer, two children, and the
woman in a tiered flounced dress at right.

This is the Muse version of the model for this catalog entry; it ships as
`scan-fig50-happy-family-muse`.

## Scale — ESTIMATED

- **Basis:** foreground adult figures taken as period-average heights
  (1.64–1.78 m). Cage, fan window and dancers are sized in proportion to
  them as drawn; the dancers are deliberately smaller than the spectators,
  as in the print's perspective.
- Resulting dimensions: vignette ground 9.6 × 6.4 m; pool of key heights —
  cage top rail 4.3 m, fan hub 4.35 m, fan top ≈ 8.25 m, flag tops ≈ 5.85 m.
- No dimension is confirmed by a measured source; treat all as estimated.

## Assumptions and interpretations

- **Single view:** one engraved cartoon. Backs and unseen sides of the
  cage, fan window and all figures are reasonable interpretations, never
  confirmed fact. The cage's side returns are short (the print shows the
  enclosure nearly front-on); its depth is a staging choice.
- **No caricature, no likenesses:** Tenniel's national types are rendered
  as dignified stylised figures distinguished only by dress silhouettes
  and hat forms — no facial features, no exaggerated anatomy, no ethnic
  markers beyond period clothing shapes.
- The print's cage holds more figures than are modelled (a churning mass
  in two tiers); 18 dancers in 9 pairs are a deliberate reduction.
- The two pennants are **blank** (the print leaves them effectively
  plain; no devices are invented) and the printed caption is not
  reproduced anywhere.
- The fan glazing is a translucent half-disc; in the print it is hatched
  glass through which trees are vaguely visible — the trees are not
  modelled.

## Build / technical

- Script: `build_scan_fig50_happy_family.py` (+ shared `vignette_common.py`
  helper copied into the package) — re-runnable, Blender 4.5.3, `bpy` only:
  `blender -b --python build_scan_fig50_happy_family.py`. It regenerates
  the .blend, .glb and `preview.png` and prints the triangle count.
- Units: metres. Origin at base centre (ground centre, z = 0 at ground
  top). Scale applied on all meshes. Material colours are authored in
  sRGB and converted to linear in the helper, as required.
- **Triangle count: 36,552** (evaluated count from the exported .glb;
  290 mesh objects).
- Preview: `preview.png`, Cycles CPU, 48 samples + denoise, 880 × 1100
  (portrait, matching the print), neutral grey background, frontal view
  comparable to the reference.

## QC

- Preview viewed against the reference before finishing (three build
  iterations). Final view matches the print's arrangement: fan window
  crowning the cage, two tiers of dancing pairs behind the bars, big
  spectators across the foreground.
- Defects found and fixed along the way: (1) dancers on the upper tier
  lost their hat brims/peaks when lifted onto the step (only
  group-parented parts moved); a first fix that lifted every created
  object then **double-moved** the parented parts (dancers ended up
  standing on the fan window) — the shipped script lifts only parentless
  objects (the group empty, which carries its children, plus loose hat
  parts), verified in the final preview; (2) the right-hand spectator's
  flounce rings were too wide and floated around her skirt (radii
  reduced to the skirt profile and the figure moved fully into frame).
  An earlier superseded draft also had an opaque full-disc "glass" that
  washed out the dancers; the glass is now a translucent semicircle
  only. The two pennant flags are in the model but fall just outside
  the preview's frame.
- **Folder note (parallel-build collision):** another builder worked
  this same folder concurrently with a smaller 5.6 m-cage variant.
  Their notes are preserved as `NOTES-variant-a.md`; an earlier copy of
  these notes was preserved by them as `NOTES-variant-b.md`. The
  `.blend` / `.glb` / `preview.png` now in this folder are the build
  described in THIS file (36,552 triangles, 8.4 m cage — final render
  completed after the variant build), produced by
  `build_scan_fig50_happy_family.py`.
- Remaining known nits: dancers' raised arms are plain tapered struts, as
  throughout this batch's figure style; the pointer in the right-hand
  spectator's hand is a thin rod held at waist height.

## Manual-review items

1. Dancer count is a reduction of the print's crowd — check the cage
   still reads as full at film distance.
2. The cage depth / side returns are invented staging (single view).
3. Overall scale rests on estimated figure heights; the real transept
   end was far larger — this is a ~9.6 m stage vignette, not the building.
