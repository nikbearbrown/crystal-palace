# NOTES — scan-fig51-peace (Muse version)

## Subject

**"Peace! — A Sketch from the Crystal Palace"** (*Punch*, 5 July 1851) —
catalog figure 51 — modelled as a stage vignette **as drawn**: a single
**cannon** on its two-wheeled carriage (barrel pointing right, ground
trail, stack of round shot beside it) displayed under a **scalloped
canopy**, attended by **two tall soldiers** in shakos, while a crowd of
**bonneted schoolgirls in aprons** and their chaperone look on — the
"Great Peace Festival" exhibiting the instruments of war. (The batch
brief's guess of armour on stands is not in the image; there are no
armour stands.)

The girls mostly stand with their **backs to the viewer** facing the
cannon, as drawn — their aprons are on the far side; the two girls at the
left edge turn outward, as in the print, and show their aprons.

This is the Muse version of the model for this catalog entry; it ships as
`scan-fig51-peace-muse`.

## Scale — ESTIMATED

- **Basis:** the soldiers taken as ~1.88–1.90 m (they tower over the
  crowd as drawn). Cannon ~2.9 m overall (barrel 2.5 m, wheels 1.08 m
  diameter — plausible period field-piece proportions, not measured from
  a named gun). Girls 1.06–1.52 m by age, chaperone 1.70 m.
- Resulting dimensions: canopy 6.3 m wide, posts 3.6 m, roof at ~3.7 m;
  vignette ground 8.0 × 5.0 m.
- No dimension is confirmed by a measured source; treat all as estimated.

## Assumptions and interpretations

- **Single view:** one engraved cartoon. The far side of the cannon
  carriage, the canopy's rear, and the fronts of the back-turned girls
  are reasonable interpretations, never confirmed fact.
- **No likenesses / no caricature:** all figures are faceless stylised
  forms; the soldiers' and girls' dress follows the print's silhouettes
  only.
- The two small faces the print floats in the background behind the
  cannon are engraver's shorthand for more onlookers. They are **not**
  modelled as free-standing heads (an earlier draft did this and it read
  as floating heads in 3D; removed).
- The canopy backdrop is a plain draped panel (blank); the print's
  sketchy booth interior is not elaborated. No lettering anywhere.

## Build / technical

- Script: `build_scan_fig51_peace.py` (+ shared `vignette_common.py`
  helper copied into the package) — re-runnable, Blender 4.5.3, `bpy`
  only: `blender -b --python build_scan_fig51_peace.py`. It regenerates
  the .blend, .glb and `preview.png` and prints the triangle count.
- Units: metres. Origin at base centre (ground centre, z = 0 at ground
  top). Scale applied on all meshes. Material colours are authored in
  sRGB and converted to linear in the helper, as required.
- **Triangle count: 23,560** (count printed by the build over all mesh
  objects).
- Preview: `preview.png`, Cycles CPU, 48 samples + denoise, 1024 × 768,
  neutral grey background, frontal view comparable to the reference.

## QC

- Preview viewed against the reference before finishing. The cannon,
  canopy valance, soldiers and crowd arrangement match the print; heads
  are correctly seated on all figures (the batch-wide floating-head
  defect of earlier drafts is absent — verified figure by figure in the
  preview).
- Remaining known nits: the left soldier's lowered arm hangs as a plain
  strut close to his side; the chaperone at the right edge is partly
  cropped by the preview frame, as figures are in the print itself; the
  girls' bonnets read as pale head-wraps at preview distance (their brim
  tori are subtle from behind).

## Manual-review items

1. Cannon proportions are generic period field-piece estimates — no
   specific exhibited gun is identified in the source.
2. Crowd count (11 girls + chaperone) is a slight reduction of the
   print's crowd; check it still reads as a school party.
3. Overall scale rests on estimated figure heights.

- **Folder note (parallel-build collision):** another builder worked
  this same folder concurrently. Their notes are preserved as
  `NOTES-variant-a.md`; an earlier copy of these notes was preserved by
  them as `NOTES-variant-b.md`. The `.blend` / `.glb` / `preview.png`
  now in this folder are the build described in THIS file (23,560
  triangles, produced by `build_scan_fig51_peace.py`).
