# The Three Graces — Sydenham, Greek & Roman Sculpture Court

A **stylised** model of the Three Graces group as it stood in the Crystal
Palace's Greek & Roman Sculpture Court at Sydenham, built for the Crystal
Palace film. Candidate #5 in `models/CANDIDATES.md` (feasibility Low–Medium:
"build only as a stylised group unless a closer view turns up"). No closer
view exists in the collection, so a stylised group is what this is — the
pedestal follows the photograph closely; the figures are an interpretation
at the limit of the evidence, and this file says plainly which is which.

## Source

One photograph only:

- `references/muse-drive/images/commons/-Assyrian_Court,_Facade_Towards_the_Nave;_Elevated_View_of_Assyrian_Court;_Greek_and_Roman_Sculpture_Court;_The_Three_Graces-_MET_DP323102.jpg`
  — an album sheet of four Delamotte photographs (Metropolitan Museum of
  Art, DP323102), **CC0**. "The Three Graces" is the bottom-right
  photograph, captioned so on the sheet. Copied into `refs/` with an
  enlarged crop of that quadrant (`refs/three-graces-crop.png`), which is
  what the model was actually built from.
- A search of the collection manifest for any other Graces view found
  nothing usable: the only other "Graces" hit is an unrelated Sèvres
  biscuit group (Venus crowned by the Graces), not downloaded and not
  this object.

## What the photograph shows (observed)

- Three standing female figures, close together and overlapping, on a
  **tall, heavily carved pedestal** in the court, seen from the front
  three-quarter. The figures are light-toned (a plaster cast, like the
  other court casts).
- The figures are **draped**, not nude: long garments fall from the
  shoulders to the feet. The composition reads as a front pair — one in
  near-profile facing into the group, one facing front-left and most
  prominent — with the third figure partly behind, her head and shoulder
  showing. At least one figure holds drapery at her side.
- The pedestal: a low, plain, dark square base block (about a quarter of
  the pedestal's height) with a small step; a carved body carrying a
  **Greek key (meander) band** near its bottom (with squared corner
  motifs), a large carved field with a central **cartouche and tablet**,
  festoon carving near the top, and corner uprights; a projecting moulded
  cap; and a plain slab on top carrying the group.

## Dimensions — all inferred, none measured

No dimension for this group or its pedestal survives in the references.
The model is scaled from the photograph's internal proportions on one
assumption: that the figures are life-size, as court casts generally
were.

| Element | Model | Basis |
|---|---|---|
| Figure height | 1.65 m | **Assumed** life size (unverified) |
| Pedestal total | 2.15 m | Photograph: pedestal ≈ 1.30 × figure height |
| Pedestal body | 0.94 m square | Photograph: body width ≈ 0.41 × pedestal height |
| Base block | 1.32 m square, 0.46 m high | Photograph proportions |
| Cap | 1.24 m square | Photograph proportions |
| Group width | ≈ 1.05 m | Photograph: ≈ 0.64 × figure height |
| **Total height** | **3.86 m** | Sum of the above |

If the cast was not life-size, the whole model scales with that error.
Do not quote any of these numbers as measured.

## Convention vs observation

- **From the photograph:** the pedestal's form and ornament programme
  (meander band, cartouche panel, swag, base block, cap), the group's
  massing and arrangement (front pair + one behind), the full-length
  drapery, the figures' relative sizes, hair drawn back (buns are the
  usual reading of what shows).
- **From classical convention, NOT verified by the photograph:** the
  exact arm links (arms resting across neighbours' shoulders — the
  photograph is too small and soft to confirm hands), the falls of
  drapery held in the outer hands, faces (left featureless), fingers,
  and all anatomy under the drapery. An earlier build used the famous
  Canova-style arrangement (centre figure's back turned, near-nude);
  the enlarged crop contradicts it for this cast, and the arrangement
  was rebuilt to match the photograph instead.
- **Inferred geometry:** all backs (of figures and pedestal — the
  pedestal's unseen faces are given the same treatment as the front),
  all depths, the rear figure's hidden arm and legs.

## Known inaccuracies

- Figures are smooth, mannequin-like stylisations: no facial features,
  musculature or individual drapery folds of the original. The gowns are
  regular lathe forms with procedural folds.
- The pedestal carving is *suggested*, not transcribed: the photograph
  shows denser scrollwork around the cartouche and possibly figural
  carving that cannot be resolved at this size; scroll rings and a swag
  stand in for it. Nothing specific (no inscription, no identifiable
  relief subject) was invented — the central tablet is left blank, as
  its lettering, if any, is illegible.
- The meander is a squared-spiral approximation of the key pattern, not
  a measured copy.

## Build

- Procedural Blender 4.2 (`scripts/build_three_graces.py`); figure bodies
  are primitive assemblies unified by voxel remesh; gowns are folded
  lathe meshes. Renders: `scripts/render_three_graces.py`, one fixed
  grey rig (front / side / three-quarter), plus `renders/compare.jpg`
  (reference crop beside the front render).
- **40,028 triangles**, real-world metres, origin at the base centre,
  scale applied.
- Files: `the-three-graces.blend`, `the-three-graces.glb`, `renders/`,
  `refs/`, `scripts/`, this file.
