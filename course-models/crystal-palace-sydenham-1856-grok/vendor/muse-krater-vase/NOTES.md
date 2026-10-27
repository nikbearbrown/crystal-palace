# Classical krater vase on pedestal — build notes

One of the pair of large relief kraters in the **Greek & Roman sculpture
court, Sydenham**, modelled on the **centre krater** of the pair — the one
instance in the photograph that is fully visible together with its
pedestal. Candidate #17 in `../CANDIDATES.md`. Sydenham state only (the
courts as photographed; the stereograph is dated c.1870–c.1890 in the
manifest). It stands on the court's standard black plinth in the
photograph; that plinth is a separate model (`../display-plinth/`,
candidate #35) and is **not** part of this one.

## Sources

Copies in `refs/`; originals in the repo:

| Source | Licence |
|---|---|
| Greek & Roman sculpture court stereograph, RP-F-2012-96-327 — `references/muse-drive/images/commons/Beelden_in_de_Griekse_en_Romeinse_zaal_in_Crystal_Palace_in_Sydenham_Crystal_Palace._101._Statues_in_the_Greek_and_Roman_sculpture_court._(titel_op_object),_RP-F-2012-96-327.jpg` (Rijksmuseum via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) | CC0 |
| "View of Transept, Looking South", MET DP238264 — `references/muse-drive/images/commons/View_of_Transept,_Looking_South_MET_DP238264.jpg` — used only to document the variant urn described below, **not** modelled | CC0 |

## Dimensions and where they came from

Overall: **krater 0.87 m high, rim Ø 0.54 m; carved pedestal 0.43 m high,
0.43 m shaft width; whole assembly 1.30 m**. Origin at base centre; built
in metres, scale applied. 42,816 triangles.

**Ratios are measured from the photograph; the absolute scale is
inferred.** Landmarks were picked on the centre krater in the stereograph
at native resolution (grid overlay on the left half of the stereo pair):

- Krater height ÷ rim diameter = **1.62** (370 px ÷ 228 px).
- Carved pedestal height ÷ rim diameter = **0.79**; pedestal shaft width
  ÷ rim diameter = **0.79**; cap, base and top-slab width ≈ **0.85**.
- Profile along the krater (fractions of its height, from the foot):
  foot and knopped stem 0–0.26; rounded lower bowl rising to a pinched
  groove at 0.41; figured relief band 0.44–0.91; flared rim 0.93–1.00.

Absolute scale: the assembly (krater + carved pedestal) spans 550 px in
the same frame as the Aristides statue (1,345 px), which the
display-plinth build from this same photograph takes as the ~2.0 m
full-size cast. Correcting for the krater standing one court row further
from the camera (distance ratio ≈ 1.5, estimated from the floor positions
of the two plinths) gives an assembly of ≈ **1.30 m**, hence rim Ø 0.54 m
and krater height 0.87 m. Sensitivity: a distance ratio of 1.3–1.8 moves
the assembly to 1.13–1.56 m, so read all absolute dimensions as **±20%**.
The ratios above are much firmer than the absolute size.

## Measured / seen in the photograph

- A **bell (campana) krater**: flaring rim, a deep upper body carrying a
  **figured relief band** between two grooves, a rounded lower bowl, and
  a short stem with a cushion knop above a spreading foot, standing on a
  flat square slab.
- A **square carved pedestal** under it: relief-figured panel faces, a
  moulded cap and a moulded base. (The dark plinth below it is the
  standard court plinth — see above.)
- White cast material, reading the same as the marble/plaster statues
  around it. The model uses one plaster material throughout, with the
  relief figures given a very slightly deeper tone of the same material
  purely so the schematic carving stays legible in flat renders.

## Guessed / inferred — not seen

- **Handles.** No handle is legibly resolved on either krater in the
  stereograph (small protrusions at rim level on the centre krater are
  consistent with volute tops, no more). Volute handles are modelled
  because the brief for this candidate specifies the bell/volute krater
  type; treat them as **inferred from the type**, not photographed.
- **The relief figures are schematic.** The photograph shows a figured
  frieze — standing draped figures — but no individual pose, attribute or
  count is legible. The model repeats one schematic draped figure ten
  times around the band (fluted robe, arms at the sides, diagonal sash).
  It is a placeholder for "figured relief", not a reconstruction of the
  actual carving. The pedestal panels get the same schematic figures,
  three to a face; only the front face is visible in the photograph, so
  the side and back panels are assumed similar.
- **Pedestal depth** is taken as equal to its width (square); only the
  front and part of one side are visible.
- **Interior** depth of the bowl is a plausible lathe continuation, not
  observed.
- **Foot detail** (knop profile) is at the resolution limit of the
  photograph and partly hidden by the foreground statue.

## Documented variant — NOT built

The MET transept photograph (Hyde Park, 1851; copy in `refs/`) shows a
different urn in its left foreground: a **dark ornamental urn** with
flamboyant leaf/acanthus crest handles on a turned foot, standing on a
**plain cylindrical pedestal** beside the fountain railing. Different
type, different material reading, different building (Hyde Park, not
Sydenham). Recorded here so nobody mistakes it for this krater; it is a
separate candidate if ever wanted.

## Also not built

The second krater of the stereograph pair (right of frame, half hidden by
the Aristides statue and the Minerva plinth) differs from the centre one
in its lower body — a gadrooned bowl and a tall fluted foot, with no
carved pedestal visible. Only the centre type is modelled here.

## Build

Blender 4.2, fully procedural (`scripts/build_krater.py`): lathed body
profile, ten schematic relief figures, two volute handles, lofted square
pedestal with moulded cap/base and relief panels on all four faces.
Four build/render rounds against the reference; renders on one fixed
neutral-grey rig (`renders/front.png`, `side.png`, `three-quarter.png`,
plus `compare.png` against the photograph).
