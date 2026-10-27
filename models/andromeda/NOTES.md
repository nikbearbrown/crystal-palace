# NOTES — Andromeda, by John Bell (candidate #2)

John Bell's *Andromeda* — the standing nude figure chained by the
wrists to a rock — as photographed on its low inscribed pedestal.
Built for the Crystal Palace film. Candidate #2 in
`../CANDIDATES.md` (feasibility Medium–High: front fully documented
including the chain; side/back inferred).

## State / family — read this before use

The **sculpture** was a celebrated exhibit of the Great Exhibition,
**Hyde Park 1851**. The **photograph this model is built from shows
the Sydenham display**: Delamotte's view of the statue standing among
nave planting at the re-erected palace, on the low dark pedestal
inscribed for that installation. The statue itself is the same object
in both states; the pedestal in this model is the one in the
photograph (Sydenham). If a scene needs the 1851 Hyde Park pedestal,
that is not documented in the collection and is not this model.

## Sources

| Source | Licence |
|---|---|
| Photograph, "'ANDROMEDA' 'JOHN BELL' from *Sculptures of Andromeda, the Toilet of Atalanta, Corinna, and a Naiad*" — MET DP323119 (cropped) — `references/muse-drive/images/commons/_ANDROMEDA___JOHN_BELL__from_-Sculptures_of_Andromeda,_the_Toilet_of_Atalanta,_Corinna,_and_a_Naiad-_MET_DP323119_(cropped).jpg` (copy in `refs/`) | CC0 (Metropolitan Museum of Art via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) |

That is the **only view in the collection**: one full-length frontal
photograph. Everything the photograph cannot see — depths, the sides,
the back, the chained hands themselves — is inference, flagged below.
The same MET series promises companion sculptures (Atalanta, Corinna,
a Naiad) but no views of *this* figure from any other angle exist in
the repo.

## What the photograph shows (observed)

- Standing nude figure, weight on her **left leg** (viewer's right),
  that leg straight; her **right leg relaxed**, knee bent, shin
  near-vertical, the foot **pointed, toes resting on a raised lump of
  the rock** about 0.08 m above the standing foot's level.
- **Both arms pass behind her back**; only the upper arms and elbows
  show at her sides. The hands are hidden — the wrists are chained
  together behind her.
- **The chain**: from behind the back it comes around her right hip,
  hangs free a short way beside her right thigh, then runs diagonally
  across the fronts of the thighs, down the front of the standing
  shin, and is anchored on the rock beside the standing foot. Links
  are individually legible against the shin (~0.04 m long).
- Head **bowed deep**, chin tucked, face turned slightly to her right
  and downcast; hair a wavy/curled cap drawn back (a bun at the back
  is the standard Bell treatment and is inferred — see below).
- The figure stands on a **rough rocky mound**, wider than the stance,
  with a raised lump under the raised foot and a small knob at its
  left edge.
- The pedestal is a **plain dark square box** whose front is painted
  in white capitals: **"7 / ANDROMEDA / JOHN BELL"** — transcribed
  from the photograph, letter for letter (this is documentation, not
  invention; the texture is generated in `scripts/` from that
  transcription).

## Dimensions and where they came from

Overall (final build, from the .blend): **44,594 triangles**;
overall height **2.31 m** (pedestal 0.575 m incl. slab + rock ~0.10 m
+ figure 1.63 m); pedestal footprint 0.86 × 0.86 m (slab). The
figure is a single fused mesh of 28,208 triangles; the chain is
5,472, the rock 8,380.

These are **photo-derived ratios hung on stated anchors, not survey
measurements**:

- Landmark points were picked on the photograph (crown, chin,
  shoulder tips, waist, hips, knees, both foot contacts). As
  fractions of the figure's vertical extent: shoulders 0.175 wide,
  waist 0.117, hips 0.178; hip centre at 0.56 of height, knees at
  0.29, raised-toe contact 0.05 above the standing sole.
- The absolute anchor is the figure taken as **life size**: crown to
  standing sole **as posed** (head bowed) = **1.63 m** — the same
  convention as `../una-and-the-lion/` (Bell's other group in this
  repo, anchored on a life-size figure) and `../the-three-graces/`.
  Sensitivity: if Bell's figure was over life size, every absolute
  dimension scales up together; the proportions stand either way.
  The grounding points sit a few percent inside the silhouette, so
  widths carry a small (≈5%) erosion allowance for the voxel remesh;
  waist is modelled at 0.215 m against a raw ratio of ~0.19–0.20 m
  for that reason.
- **Pedestal height 0.55 m is ADOPTED** from `../sy-classical-cast-base/`'s
  notes, whose builder measured this same photograph's pedestal
  family ("low nave pedestals for modern sculpture … John Bell's
  Andromeda, ~0.5–0.6 m"). The pedestal's foot is below the
  photograph's frame, so its height cannot be measured from the
  photograph directly; its plan size is a photo ratio against the
  rock. The pedestal's base moulding (if any) is unseen and not
  modelled.

## Measured / seen vs inferred

**Seen in the photograph and modelled from it:** the pose and its
asymmetries (standing vs raised leg, toe contact +0.08 m), the
frontal proportions and silhouette, the arms-behind-back disposition,
the chain's whole frontal path and approximate link size, the bowed
and slightly turned head, the rock's frontal outline and raised lump,
the pedestal's form and its inscription.

**Inferred (no direct evidence):**

- **All depths** (torso, pelvis, limbs) — classical proportions
  judged against the frontal silhouette; the figure is at its least
  certain in profile.
- **The back in full**: buttocks, shoulder blades, the fall of the
  arms behind, and the hands themselves (two merged masses at the
  chain's shackle ring at sacrum height — the photograph shows no
  part of them).
- **The bun** at the back of the hair, and the hair's carved-curl
  surface (procedural noise; the photograph shows a wavy cap but does
  not resolve individual locks).
- **Face detail**: schematic — a nose wedge, no eyes, ears or mouth
  modelled. At the photograph's resolution the face is a downcast
  shadowed oval; this model stays at that level deliberately.
- The rock's depth, back and exact crag pattern (frontal outline and
  the raised lump are from the photograph; the rest is procedural).
- The pedestal's unseen base and back; slab overhang is a reading of
  the photograph's top edge line.

## Known inaccuracies

- The figure is **stylised**, in line with the other figure props in
  this repo (Una, the Graces, Cain): masses are fused lofts, not
  anatomy. The frontal disposition, relative heights and silhouette
  track the photograph; hands, feet and face are schematic.
- The raised foot reads slightly pendant in some lights — the pointed
  foot is an ellipsoid construction, and its toe contact on the lump
  is approximate (±0.02 m).
- The chain is a regular instanced link run along a fitted curve;
  the real chain sags and twists less uniformly, and its run *behind*
  the back (wrists to hip) is hidden in the photograph and therefore
  placed by the shortest plausible path.
- Colours: the photograph is monochrome. The figure is given a pale
  plaster/stone tone and the pedestal an ebonised near-black after
  the court's other documented pedestals; the statue's actual finish
  (marble or plaster) is not recorded in the collection.

## Build

Procedural bpy (Blender 4.2), no sculpting by hand: `scripts/build_andromeda.py`
(lofted torso/limbs, fused by voxel remesh; instanced torus-link
chain; value-noise rock; the inscription texture is drawn by the
script's companion PNG in `scripts/`). `scripts/render_andromeda.py`
is the fixed neutral-grey rig used for `renders/` (Cycles CPU — this
VM has no EGL for EEVEE). Renders: front (the documented view),
side, three-quarter, rear-quarter, and `compare.jpg` against the
photograph. Six build/render rounds were run against the photograph;
the last three concentrated on the frontal read (pelvis–thigh blend,
hip crease, arm placement, raised-foot contact).
