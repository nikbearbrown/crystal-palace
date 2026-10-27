# Garden urn on pedestal — NOTES

## What this is

The **tall campana garden urn on its square pedestal** that recurs all
over the Sydenham gardens: along the paths, around the fountain basins
and on the terrace parapet piers. Modelled as a lathe-turned campana
(bell) urn — flared rim, smooth bell body with shallow gadrooning on the
lower bell, a knopped stem and a spreading foot — standing on a stepped
square stone pedestal (plinth, die, cap). An empty soil bed is modelled
just inside the mouth; the planting itself is scene dressing, not part
of the prop.

Film context: Sydenham gardens/terraces dressing (storyboard **CP042**,
**CP073**). This is a **Sydenham** object (post-1854). It must never be
placed in a Hyde Park scene.

This is the prop the `garden-fountain-basin` build deliberately left
out: its NOTES record "the campana urns that stand on the rim in the
photographs are candidate #16" — this folder is that candidate.

## Sources used

- **Primary — silhouette family, pedestal form, garden setting:**
  `references/muse-drive/images/commons/Exterieur_van_Crystal_Palace_in_Sydenham_met_tuinen_en_fonteinen,_RP-F-F01134-AL.jpg`
  (albumen photograph, 4108 × 3236 px, Rijksmuseum object RP-F-F01134-AL;
  manifest licence **CC0**). The candidates list attributes this view to
  Delamotte; the museum record lists the maker as anonymous,
  ca. 1880–1910. Tall white campana vases on square pedestals stand in
  the mid-ground around the upper basin and along the paths; smaller
  urns ring the foreground basin. Copied into `refs/`.
- **Secondary — exterior/terrace context:**
  `references/muse-drive/images/commons/Exterieur_van_Crystal_Palace_in_Londen,_op_de_voorgrond_een_fontein,_links_een_watertoren_Chrystal_Palace_(titel_op_object),_RP-F-F01212-16-1.jpg`
  (albumen photograph, 2500 × 1676 px, Rijksmuseum object RP-F-F01212-16-1,
  dated 1878–1890; manifest licence **CC0**). The upper fountain basin,
  terraces and their parapet ornaments. Copied into `refs/`.
- **Anchor dimensions borrowed from sibling props:** the terrace
  parapet height of **1.05 m** from `models/sy-terrace-step-and-arcade`
  (photo-proportioned) and the bench length ~1.8 m used by
  `models/garden-fountain-basin` and `models/park-bench`.

**No single urn is shown close in either photograph**, and no
dimensioned source for any Sydenham garden urn exists in the
references. Everything below is silhouette-true and size-inferred.

## Dimensions — measured vs inferred

| Dimension | Value | Basis |
|---|---|---|
| Total height | **1.79 m** | **Inferred (±~20%).** In the Delamotte view the mid-ground urns stand at the same lawn depth as life-size statues on pedestals (~1.7 m figure on ~1.15 m pedestal) and ~1.8 m benches; pixel heights put the urn-and-pedestal total a little below the statue-and-pedestal total, in a ~1.6–2.0 m band. 1.79 m adopted. |
| Pedestal height | 0.98 m | **Inferred.** Pixel ratio pedestal : urn ≈ 1.2 : 1 in the mid-ground examples (the pedestal reads slightly taller than the vase it carries). |
| Pedestal footprint | 0.67 × 0.67 m (plinth); die 0.51 × 0.51 m | **Inferred.** Square pedestal read from the photographs; widths proportioned from the die's height/width ratio in the mid-ground examples (the vase pedestals read slimmer than the statue pedestals beside them). Steps (scotia, cove, cap) are the standard Victorian pedestal sequence, not individually resolved in the photographs. |
| Urn height | 0.81 m | **Inferred** (ratio above). |
| Urn rim diameter | 0.69 m | **Inferred.** Rim diameter : urn height ≈ 0.85 read from the mid-ground silhouettes — a wide-mouthed campana, not a narrow vase. |
| Urn foot diameter | 0.39 m | Proportioned from the silhouette; the foot is partly hidden behind pedestal caps in every view. |
| Gadrooning | 16 shallow lobes, lower bell only | **Interpreted.** The mid-ground bells show vertical shading consistent with gadrooning/fluting on the lower body; at the photographs' distance it cannot be counted. The upper bell is smooth in the model, as it reads in the photographs. |
| Mesh | **4,148 triangles**, 8 prop objects (+ studio in .blend only) | Lathe urn 3,456; soil disc 192; pedestal boxes ~500. Origin at base centre, ground at z = 0, real-world metres, scale applied. |

## What was seen vs what was guessed

**Seen in the photographs, and modelled:**

- A wide-mouthed **campana silhouette**: flared lip, bell body curving
  continuously down to a narrow stem, a knop/collar on the stem, and a
  spreading foot.
- A **square pedestal** with a stepped base and a cap wider than the
  die, of pale (white-painted or light stone) finish — the urns read
  bright white against the lawns in both views.
- The type **recurs at several sizes** in the gardens (see below).

**Guessed / inferred, and flagged:**

- **All absolute dimensions** (chain stated above, ±~20%). The model is
  re-scalable: every size is a parameter at the top of the build script.
- The pedestal's individual moulding steps, the urn's foot profile, the
  inner bowl depth and the soil level — none is resolved at the
  photographs' distance.
- The gadroon count (16) and its restriction to the lower bell.
- **No handles are modelled**: no handle is resolvable on any urn in
  either photograph. If the originals had lug handles, they are below
  the resolution of the surviving views.

## The other urn family in the same photographs — not modelled

The foreground basin of the Delamotte view and the rim of
`garden-fountain-basin` carry a **second, smaller type**: a low, wide
tazza-like planter (broad shallow bowl, short stem, low square base),
mostly shown planted with dark foliage. It is a different prop from the
tall campana modelled here; the two should not be substituted for each
other at the basin rim. The urns visible on the terrace parapet piers
in the background are the campana type at a smaller scale — this model
scaled to ~0.75× is the closest available stand-in, and that use is an
inference, not a measurement.

## Build / renders

- `scripts/build_garden_urn.py` (procedural bpy, Blender 4.2): lathe urn
  with parametric gadrooning, stacked pedestal, fixed neutral-grey
  studio rig, GLB export. Build/render rounds: r1 silhouette, r2
  wider/shorter bell + deeper gadrooning, r3 pedestal slimmed toward
  the mid-ground examples, final exposure correction.
- Renders are **Cycles CPU** on the same grey rig the other Muse props
  use: this VM's EEVEE/EGL stack hangs headless (the same failure the
  `glass-topped-display-counter` build recorded), so light energies
  were re-balanced for Cycles. The .blend and .glb are engine-neutral.
- `renders/compare.jpg` sets the three-quarter render beside a cropped
  region of the Delamotte photograph (mid-ground urns and statue,
  centre-right) — the silhouette family, not a photomatch: no
  photograph shows the urn from this angle at this size.
