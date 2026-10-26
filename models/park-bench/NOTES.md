# Park bench (Sydenham gardens) — notes

**Read this first — how much of this model is evidence, and how much is not.**
The benches survive in the collection only as small silhouettes in one
photograph. That photograph gives **existence, placement and rough
silhouette only**. Nothing in it is large enough to measure: a bench end
occupies a few dozen pixels. The scrolled cast-iron end profile modelled
here is **period-typical inference, not measured from the photograph**,
and no dimension below was scaled from the photograph either. Treat this
prop as "a plausible mid-Victorian park bench standing where the photo
shows benches stood", not as a reconstruction of the actual Sydenham
foundry pattern.

## Source used

- `references/muse-drive/images/commons/Exterieur_van_Crystal_Palace_in_Sydenham_met_tuinen_en_fonteinen,_RP-F-F01134-AL.jpg`
  — view over the Sydenham lower gardens: fountain basins in play, the
  palace and a water tower behind. Copied into `refs/`.
  - Licence: **CC0** — http://creativecommons.org/publicdomain/zero/1.0/deed.en
    (per `references/muse-drive/data/manifest.csv`).
  - Rijksmuseum object RP-F-F01134-AL, albumen print, 4108 × 3236.
    `models/CANDIDATES.md` (rows #13, #38) cites it as a Delamotte
    photograph; the manifest's museum metadata records the photographer
    as anonymous and dates the print c.1880–c.1910. The discrepancy is
    noted, not resolved.

## What the photograph actually shows (seen)

- Benches placed along the garden walks: a row along the straight east
  walk, singles on the curved central walk — benches were standard
  furniture of the fountain gardens.
- One bench on the curved walk in near side-elevation: a **backed** bench
  with **two horizontal back members** — a top rail and a lower rail on
  uprights, with an open gap between them — over a single seat band, on
  dark supports.
- Benches on the east walk, seen from above and behind: pale (light-toned)
  horizontal seat/back surfaces with dark, narrow end supports; one
  further bench at the top of that view hints at a curved end profile,
  too small to read.

## What was guessed (inferred — not from the photograph)

- **The cast-iron end design in full**: flat-bar end frames with volute
  scrolls at the seat front, under the seat and at the top of the back
  post, an open frame under the seat, side stretchers and a longitudinal
  stretcher bar. This is the standard mid-Victorian cast-iron-ended bench
  type (the pattern sold by the big founders of the period), chosen
  because CANDIDATES #38 calls for a period cast-iron-ended bench. The
  real Sydenham pattern is unknown from this evidence.
- **Seat construction**: 4 slats. The photograph's seat reads as one band;
  the slat count cannot be resolved. (The two back rails *are* the count
  the photograph shows.)
- **Back uprights**: in the clearest silhouette the back reads as rails on
  simple posts. Here the posts are the rear members of the cast ends —
  the usual cast-iron-ended arrangement, but not proven by the photo.
- **Bolt heads** at the slat fixings: plausible construction detail, not
  visible in the source.
- **Colours**: the source is monochrome. Dark green-black painted iron
  and mid-brown timber are period convention, not evidence. The pale seat
  surfaces in the photograph may be sunlit timber, pale paint, or albumen
  glare; the model's timber is deliberately darker than that glare reads.

## Dimensions (all inferred/typical — none measured)

| Dimension | Value | Basis |
|---|---|---|
| Overall (model bounding box) | 1.92 × 0.65 × 0.89 m | as built |
| Slat length | 1.90 m | period-typical garden bench length (range ~1.8–2.0 m) |
| Seat height (top of slats) | 0.46 m | period-typical |
| Seat depth (slatted) | 0.46 m | period-typical |
| Back rake | 12° | period-typical comfort angle |

No dimension could be scaled from the photograph: no object of known size
stands in a measurable relation to any bench in it.

## Build

- Blender 4.2, fully procedural: `scripts/build_park_bench.py` builds the
  scene, saves the .blend, exports the .glb and renders all three views on
  one fixed neutral-grey rig (same sun/fill/backdrop for every view).
- 44 mesh objects, **5,132 triangles** (bench only; ground plane excluded).
- Real-world units (metres), origin at base centre, scale applied.
- Renders: `renders/front.png`, `renders/side.png`,
  `renders/three-quarter.png`; `renders/compare.jpg` pairs an upscaled
  crop of the photograph's clearest bench (a ~90 × 40 px silhouette) with
  the side render — the crop shows how little the source actually gives.

## Known inaccuracies

- The end profile is invented in period style; if the Sydenham benches
  were a specific founder's pattern, this is not it in any detail.
- Scrolls are generic volutes, not a copied ornament.
- If the real benches were timber-post benches rather than
  cast-iron-ended, the ends are wrong in kind, not just in detail (see
  "What was guessed").
- Paint colours are conjectural.
