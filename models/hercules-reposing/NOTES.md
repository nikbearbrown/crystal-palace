# Hercules Reposing — build notes

The **Farnese Hercules cast in the Sydenham nave** — the weary hero
leaning on his club, the Nemean lion skin sheeted over it — as
photographed among the nave planting. Candidate #4 in
`../CANDIDATES.md`. Sydenham state only (the stereograph is dated
c.1870–c.1890 in the manifest). Film scenes CP044 family. The statue
is modelled **on its pale integral base slab and on a dark court
pedestal**, as photographed; the pedestal alone is also available as
`../display-plinth/` (candidate #35) and `../sy-classical-cast-base/`.

## Orientation — read before placing

- the figure's front (chest, toes) faces **−Y**; his left — the club
  and lion-skin side — is **+X**;
- renders: `front.png` = the documented view (−Y); `side.png` = from
  his left (+X, the club side, **inferred** — never photographed);
  `three-quarter.png` from (+X, −Y); `photomatch.png` approximates
  the stereograph's own viewpoint and `compare.jpg` sets it beside
  the photograph.

## Sources

Copies in `refs/`; originals in the repo:

| Source | Licence |
|---|---|
| Nave stereograph, RP-F-2012-96-329 — `references/muse-drive/images/commons/Standbeeld_in_het_middendeel_van_Crystal_Palace_in_Sydenham_Crystal_Palace._Statue_in_the_Nave._(titel_op_object),_RP-F-2012-96-329.jpg` (Rijksmuseum via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`; 3,259 × 1,669 px, anonymous albumen stereo pair, c.1870–c.1890) | CC0 |

One source only: a stereo pair, both halves frontal. **The side, the
back and all depths were never photographed in this collection** —
everything off the frontal plane is inference from the Farnese type
(see below). The printed caption under the photograph ("…HERCULES
REPOSING…") identifies the subject; the pedestal's own label is not
legible in the photograph, so the model's label plate is left blank.

## Dimensions and where they came from

Overall assembly: **3.14 m high**; footprint 1.64 × 0.94 m (pedestal
foot). Origin at base centre; built in metres, scale applied.
**36,424 triangles**, 5 objects (figure, lion skin, slab, pedestal,
label plate).

**Ratios are measured from the photograph; the absolute scale is the
shared inferred anchor** used by the sibling Sydenham figure builds,
so all the nave/court casts agree in a scene:

- Figure (soles to crown) = **2.00 m adopted** — the heroic-cast
  convention of `../aristides-statue/` (whose 2.00 m also anchors
  `../display-plinth/`'s 0.90 m plinth and `../krater-vase/`'s
  1.30 m). No dimensioned source for this cast exists in the
  collection; carry ±15–20% on every absolute figure dimension.
- Landmarks were picked on the stereograph at native resolution,
  with the slab located by a brightness scan of a vertical strip
  (slab band y ≈ 1,265–1,395 px; figure crown ≈ y 200, soles at the
  slab top): slab thickness ÷ figure = **0.122** → **0.24 m**;
  slab width ÷ figure ≈ 0.6–0.8 across the two halves → **1.45 m**
  wide, 0.80 m deep (depth inferred).
- Figure proportions (fractions of figure height, from the photo):
  shoulder width 0.33; chest max 0.57 wide at 0.80 height; belly
  forward of the chest plane; head + beard ≈ 0.12; club top at
  0.67 (forearm rests on it); lion skin hangs 0.67 → 0.02, flaring
  from 0.21 to 0.60 wide; the left shin crosses **in front of** the
  right — the photograph's shin X.
- Pedestal: **0.90 m adopted** from the documented Sydenham
  standing-statue pedestal family (`../display-plinth/`,
  `../sy-classical-cast-base/`), widened to 1.64 × 0.94 m to carry
  the slab. The photograph shows only its top ≳0.38 m before
  foliage and the frame edge intervene — the height is a family
  adoption, **not** a measurement of this pedestal.

## Measured / seen in the photograph

- The pose: head bowed, shoulders rolled, torso slumped onto the
  club at his left; right arm hanging at his side, hand low at the
  thigh; legs crossed at the shin, left in front.
- The lion skin as a broad hanging sheet over the club, widening
  downward and ending just above the slab; the lion's head and two
  paws at the top, by the hand.
- The club itself is almost wholly hidden behind the skin — only
  its knob shows at the top, under the forearm.
- The pale, chunky rectangular base slab, wider than the figure
  group, on a dark pedestal lost below in foliage/shadow.
- Uniform pale cast tone over figure, club and skin alike (modelled
  in one plaster material).

## Guessed / inferred

- **All depths, the side and the back** — from the Farnese type:
  torso depth, the back's musculature, the skin sheet's thickness
  and rear face, and how the sheet wraps the club.
- The club's knotty shaft (conventional; it is hidden in the photo).
- The right hand: modelled hanging at the thigh as the photograph
  reads. In the Naples Farnese original that hand, behind the back,
  holds the apples of the Hesperides — not resolvable in the
  stereograph and not modelled.
- Pedestal height (family adoption, above) and slab depth.
- Face, hair and beard are schematic masses with noise-displaced
  surfaces; fingers and toes are not articulated.

## Known inaccuracies

- The chest still reads as two pec masses over a separate belly;
  the photograph's torso is a single broader barrel. The massing
  and silhouette are right; the internal modelling is simplified.
- The lion-skin sheet is too regular — straighter edges and a
  narrower ground flare than the photograph's ragged drape — and
  its fold pattern is procedural noise, not observed folds.
- The head is the weakest element: bowed and bearded in the right
  place, but the features are a schematic read of a soft photograph.
- If the cast was not the ~2.0 m heroic size, the whole assembly
  scales with the anchor (see the sensitivity note in
  `../display-plinth/NOTES.md`).

## Build

Procedural Blender 4.2 (`scripts/build_hercules_reposing.py`):
chained-ellipsoid lofts and masses posed on the photograph's
frontal landmarks, voxel-remeshed at 0.021 m (figure) and 0.018 m
(lion skin) for a carved read; pedestal and slab are rectangular
lofts. Three frontal-composition rounds were run against the
photograph (belly integration, head sunk between the shoulders,
shin cross deepened, club moved behind the skin sheet).
`scripts/make_compare.py` builds `renders/compare.jpg`. Renders use
one fixed neutral-grey rig (Cycles, Filmic, −0.2 exposure).
