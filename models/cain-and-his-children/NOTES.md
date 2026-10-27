# Cain and his Children — Antoine Étex (Sydenham sculpture gallery)

The intertwined figure group catalogued in the Sydenham sculpture
gallery as "239 Cain. By A. Etex.": Cain seated in the centre on a rocky
mound, head bowed, with four children disposed around him — a standing
boy at his right hand, a crouched child in front of him, a larger
crouching figure at his left with an infant sheltered against it.
Candidate #3 in `../CANDIDATES.md`. Sydenham state (the sculpture
gallery as photographed, c.1870–1890).

## Sources

Copy in `refs/`; original in the repo:

| Source | Licence |
|---|---|
| Stereo pair of the group in the sculpture gallery, Rijksmuseum RP-F-2012-96-336 (photographer anonymous, albumen print, dated c.1870–c.1890 by the museum) — `references/muse-drive/images/commons/Beeld_Cain_en_zijn_kinderen_door_Antoine_Etex_in_de_beeldengalerie_van_het_Crystal_Palace_te_Sydenham_Crystal_Palace_Sculpture_Gallery._239_Cain._By_A._Etex._(titel_op_object),_RP-` (filename truncated in the repo, no extension; bytes are JPEG) | CC0 (Rijksmuseum via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) |

This is the **only view of the group in the collection, and it is
frontal**. Everything about depth, the sides and the back is inference
(see below). The display-base form follows the plinth family's
documentation in `../display-plinth/NOTES.md`, which records from the
same stereograph that group bases are lower and wider than the standing
-statue standard, with a sloped shoulder and a small label low on the
front.

## Dimensions and where they came from

Overall (including the display base): **2.12 m wide × 1.36 m deep ×
1.62 m high**. Origin at base centre; built in metres, scale applied.
The figure group above the base is 1.46 m high; Cain's crown is the
highest point. Display base: 2.12 × 1.36 m, 0.16 m high.

These are **photo-derived estimates, not measurements of the object**.
No dimensioned source for the group exists in the collection. The size
was set by treating the Sydenham cast as a heroic, over-life-size
gallery group on the same basis the plinth build used for its
neighbouring casts (the Aristides taken as the ~2.0 m cast of the
Naples figure): Cain's seated proportions were built to a
standing-equivalent of ~2.2 m, and the group's width-to-height ratio
(≈1.14 for figures + rock, de-foreshortened) was taken from the
stereograph. Within the frame, the boy's crown sits at Cain's shoulder
(checked against the photograph across five build rounds). Carry an
uncertainty of roughly **±15%** on all absolute dimensions.

**48,216 triangles**, 14 objects: five figures, the pelt, the rock
mound, the display base and its label plate, three un-remeshed hair
masses.

## Measured / seen in the photograph

- The **frontal composition and silhouette**, which the model tracks:
  Cain seated high at the centre-back on the rock, torso hunched,
  head bowed so the face is shadowed under shaggy hair; both of his
  thighs project forward and both shins hang near-vertical at the
  front, feet planted on the rock's front slope.
- The **standing boy** at Cain's right (viewer's left): body in
  contrapposto against Cain's side, head turned up toward Cain's face,
  near hand resting on Cain's right knee, far leg trailing diagonally
  behind; his crown reaches Cain's shoulder. Shoulder-length hair.
- The **crouched central child** directly in front of Cain between his
  knees, largely occluded: a prominent bowed curly head, one small foot
  planted at the rock's front edge.
- The **larger crouching figure** at Cain's left (viewer's right), seen
  from the back three-quarter: smooth arched back, one leg extended
  forward along the rock with the foot at its edge, one arm raised so
  Cain's left hand clasps it, the other arm supporting on the rock.
- The **infant** tucked between the central child and that figure: a
  round head resting against the figure's side, small curled body.
- The **shaggy animal pelt** hanging between Cain's knees over the
  rock (the dark textured mass at the centre of the photograph).
- The **rocky integral base**: a low, wide craggy mound, wider than it
  is deep, with sloped shoulders, on which all figures sit or stand.
- A neighbouring exhibit's dark pedestal at the frame's left edge is
  **not** part of this group and is not modelled.

## Guessed / inferred (flagged, not presented as fact)

- **Depth and the entire back.** No side or rear view exists in the
  collection. Depths of all figures, the mound's rear profile and the
  way the children connect behind Cain are sculptural inference from
  the frontal masses (symmetry and plausibility), nothing more.
- **Figure count and identities.** Five human forms are legible in the
  photograph and five are modelled (Cain + four children). The larger
  right-hand figure may be Cain's wife rather than a child — the
  gallery catalogue title says only "Cain"; the model does not assert
  an identity for it.
- **The intertwining.** At this stylisation level the figures are
  chained, voxel-remeshed masses that overlap as the photograph shows;
  hands, faces and the exact interlock of limbs are schematic. Cain's
  right arm passes behind the boy as the photograph suggests but its
  hand placement on his knee is an interpretation; the clasped hands
  at Cain's left are placed where the photograph shows the two hands
  meeting, without modelled fingers.
- **The display base** below the rock is only marginally visible in
  the stereograph — the group appears to stand almost at floor level.
  The low, wide ebonised base with sloped shoulder is built from the
  plinth build's documentation of this base family; the shallow
  unlettered label plate low on its front is an interpretation, as on
  the standard plinth (no lettering is modelled or invented).
- **Finish.** The cast is rendered as warm-white marble/plaster; the
  source is a sepia albumen print, so surface tone and the pelt's
  darker brown are interpretations. Hair masses are kept out of the
  voxel remesh so their displaced, shaggy surfaces survive — a
  stylisation device, not a claim about the carving.

## Build

Procedural Blender 4.2 (script in `scripts/`): each figure is chained
ellipsoids and spine lofts posed against the photograph, joined and
voxel-remeshed (0.026 m) for a carved read; the rock is displaced masses
similarly remeshed with a normal-direction crag pass. Five frontal
composition rounds were run against the stereograph (see
`renders/compare.png`, which sets the reference beside the model's
matching viewpoint). Renders use one fixed neutral-grey rig for all
views. Weakest aspects, in order: the unseen back and depth (pure
inference), the muddled centre where three children and the pelt
overlap (the photograph itself barely resolves it), and the schematic
hands and faces.
