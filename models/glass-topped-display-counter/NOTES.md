# NOTES — Glass-topped display counter (nave counter run unit), 1851

Prop for the Crystal Palace film. Candidate #37 in `models/CANDIDATES.md`.
Scenes: CP019 / CP025 (Hyde Park 1851 nave and court dressing). Hyde Park
1851 building only.

## What it is

ONE unit of the standard low exhibition counter that ran in long lengths
along the nave and through the courts: a slab-sided timber carcase with
applied frame-and-panel faces (three panels to the long faces, one to each
end), a recessed plinth, a capping band, and a flat glazed top in timber
sash framing (three panes) over a dark cloth display bed. Units butt end
to end to form a run; `renders/run-three-quarter.png` shows three units
tiled. The saved `.blend` / `.glb` contain the single unit only.

This is **not** the table/desk case on turned legs with a hipped glazed
lid already in the repo as `hp-crate-and-display-case/` — that is a
different, freestanding piece of furniture. No low carcase counter existed
in the repo before this build (checked the full tree on main).

## Sources

- `refs/talbot-eastern-nave.jpg` — H. F. Talbot, *View of Eastern Nave*,
  1851 (repo path `references/muse-drive/images/commons/Great_Exhibition,_View_of_Eastern_Nave_by_HF_Talbot,_1851.jpg`;
  manifest licence: Public domain). The long dark counter runs with goods
  piled on top are visible along both sides of the nave.
- `refs/dickinson-plate-xxiv.jpg` — Dickinson's *Comprehensive Pictures*,
  plate XXIV, the Cotton court, 1854 (repo path
  `references/muse-drive/images/commons/Cotton,_carriages,_etc_-_Dickinson's_comprehensive_pictures_of_the_Great_Exhibition_(1854)_vol_2,_plate_XXIV_-_BL.jpg`;
  manifest licence: CC0). Long counters in the middle distance, one with
  folded cotton goods on top; figures alongside give the scale.

Both images show the counters only in wide views, exactly as the
candidate's feasibility note warned: the form class (long, low,
slab-sided, waist height, flat top) is all they support. No single named
counter is, or could be, reconstructed from them.

## Dimensions — all INFERRED

No dimensioned source for exhibition counters exists in the collection.
Every figure below is an inference and is labelled as such:

| Dimension | Value | Basis |
|---|---|---|
| Unit length | 3.658 m (12 ft) | Half the Palace's documented 24 ft structural bay, so two units tile per bay — a plausible joinery module for furniture that had to fill bays; the runs in Talbot's view are continuous over many bays. **Guessed.** |
| Depth | 0.762 m (2 ft 6 in) | Period counter practice; consistent with the proportions of the runs against the nave columns in Talbot's view. **Guessed.** |
| Overall height | 0.940 m | In Dickinson's plate the counter tops sit at about hip-to-waist height on the standing figures beside them (~1.65–1.75 m people) → top ≈ 0.9–1.0 m. Midpoint adopted. **Estimated from the plate, ±~0.05 m.** |
| Plinth 0.102 m, carcase 0.736 m, capping 0.026 m, glazed top 0.076 m | — | Apportioning of the total height by eye from the views. **Guessed.** |
| Display bed | dark green cloth | Counters in Dickinson's plate are draped/lined dark; a cloth bed under the glass is the conservative reading. **Inferred.** |

## Measured / seen vs guessed

- **Seen:** the form class — long low slab-sided runs, flat tops, dark
  finish (near-black in Talbot's photograph, dark grey-green in
  Dickinson's plate; the model uses a dark stain between the two),
  counter height against figures, goods displayed on top of the counters
  (i.e. the tops were working surfaces, glazed display counters being
  the standard fitting this candidate names).
- **Guessed:** every absolute dimension; the panel count and panel
  treatment (counters at this distance show no joinery detail in either
  image — applied frame-and-panel is standard period counter work, not
  observed detail); the sash framing and three-pane division of the
  glazed top; the cloth bed colour; end panelling (ends are never seen
  in the views; when units are tiled into a run the end panels are
  hidden anyway).

## Build

- Procedural bpy script: `scripts/build_glass_topped_display_counter.py`
  (Blender 4.2, headless). Real-world metres, origin at base centre,
  all transforms applied. 41 mesh objects, **492 triangles**.
- Renders on one fixed neutral-grey rig (grey world + ground plane, same
  sun/fill for every view): `front.png`, `side.png`, `three-quarter.png`,
  plus `run-three-quarter.png` (three units tiled) and `compare.png`
  (three-quarter render beside a crop of the Talbot view; composed by
  `scripts/make_compare.py`). Disclosure: the three main views are EEVEE
  renders from the build script; the supplementary run view was rendered
  later from the saved `.blend` with Cycles CPU (`scripts/render_run.py`)
  after this VM session lost its EGL stack — same geometry, cameras and
  lights, slightly different shading.
- Three build rounds: (1) first pass — panel faces were coplanar with
  the carcase core and z-fought (striped moiré in renders); (2) core
  inset 12 mm, panelling rebuilt with no coplanar faces, boxed backdrop
  replaced by a uniform grey world (its unlit edge showed black in the
  3/4 view); (3) timber darkened toward the near-black of Talbot's
  counters. Final stats re-checked against this file and the README row.

## Known inaccuracies

- This is a *type* model, not a portrait of any individual counter:
  exhibitors' fittings varied, and neither reference resolves one
  counter's joinery.
- The glazed top is an interpretation of the candidate's "glass-topped"
  specification; in Talbot's view the tops cannot be resolved well
  enough to prove glazing on the nave runs specifically (goods sit on
  top of them), so the glass should be read as the standard fitting,
  not as observed fact.
- Colour is a compromise between a monochrome photograph taken in
  shade and a hand-coloured plate.
