# Standard display plinth — build notes

The black ebonised pedestal that stands under the sculpture in every
Sydenham court: the single most-repeated piece of furniture in the courts,
and the base the statue candidates in `../CANDIDATES.md` sit on. Candidate
#35. Sydenham state (the courts as photographed in the 1850s–60s).

## Sources (all CC0)

Copies in `refs/`; originals in the repo:

| Source | Licence |
|---|---|
| Greek & Roman sculpture court stereograph, RP-F-2012-96-327 — `references/muse-drive/images/commons/Beelden_in_de_Griekse_en_Romeinse_zaal_in_Crystal_Palace_in_Sydenham_Crystal_Palace._101._Statues_in_the_Greek_and_Roman_sculpture_court._(titel_op_object),_RP-F-2012-96-327.jpg` | CC0 (Rijksmuseum via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) |
| Cain and his Children stereograph, RP-F-2012-96-336 — `references/muse-drive/images/commons/Beeld_Cain_en_zijn_kinderen_door_Antoine_Etex_in_de_beeldengalerie_van_het_Crystal_Palace_te_Sydenham_Crystal_Palace_Sculpture_Gallery._239_Cain._By_A._Etex._(titel_op_object),_RP-` | CC0 |
| Hercules in the nave stereograph, RP-F-2012-96-329 — `references/muse-drive/images/commons/Standbeeld_in_het_middendeel_van_Crystal_Palace_in_Sydenham_Crystal_Palace._Statue_in_the_Nave._(titel_op_object),_RP-F-2012-96-329.jpg` | CC0 |

The Aristides plinth in the Greek & Roman court view is the measured
subject — it is the closest, clearest instance, seen front and side at
reading distance.

## Dimensions and where they came from

Overall: **0.90 m high × 0.90 m wide (foot) × 0.65 m deep (foot)**; top slab
0.84 × 0.59 m. Origin at base centre; built in metres, scale applied.

These are **photo-derived ratios, not survey measurements**. Points were
picked on the Aristides stereograph (statue head, feet, plinth top, plinth
foot; the same picks on the Minerva bust beside it):

- Plinth height ÷ statue height in frame = **0.454**. Taking the statue
  (the Aristides/Aeschines) as the full-size ~2.0 m cast of the Naples
  figure gives 0.91 m → modelled as **0.90 m**. Sensitivity: if the cast
  were 1.8 m, the plinth would be ~0.82 m. The 0.90 m figure carries that
  assumption.
- Base moulding zone = ~21% of plinth height in frame → 0.185 m here.
- Front width ≈ 0.93 × height; depth ≈ 0.65 × width (side face of the same
  plinth, de-foreshortened) → 0.84 m top width, 0.59 m top depth.

## Measured / seen in the photographs

- A **stepped base moulding**: a bottom slab, a small step in, then a steep
  chamfer rising to the shaft. The light catches it identically on the
  Aristides and Minerva pedestals.
- A **straight, untapered shaft** — no taper is visible in either clear
  view, so none is modelled.
- **White painted lettering high on the front face** — catalogue number,
  title and origin in three lines ("320 / ARISTIDES OR AESCHINES / FROM
  NAPLES"; "328 / MINERVA / FROM MUNICH"; "317 / HERCULES REPOSING").
- The statues stand on their **own white marble base slabs**, which sit on
  the plinth and are *not* part of this prop.
- The Hercules base in the nave is the same black family, largely hidden by
  planting.

## Guessed / inferred (flagged, not presented as fact)

- **Label plate:** the photographs show painted lettering, quite possibly
  directly on the face. The model renders the label zone as a shallow
  (8 mm) recessed, unlettered plate — an interpretation so the zone reads
  at film distance without inventing text. No lettering is modelled.
- **Cap profile:** in every view the top is covered by the statue's own
  slab. A thin stepped cap and slightly overhanging top slab are inferred
  from the rim visible at the Minerva pedestal's top edge.
- **Back and underside** are unseen in all references; modelled as plain
  continuations of the shaft and foot.
- **Finish:** ebonised (black-stained) wood with a satin sheen. The
  sources are sepia albumen prints, so the exact black value and gloss are
  an interpretation.
- **One size is a simplification.** Heights in the courts were matched to
  the exhibit: in the same photograph the Minerva *bust* pedestal stands
  ~1.6× taller (≈1.5 m, same ratio method); group bases are lower and
  wider, and the Cain group's base has a sloped shoulder and a small label
  low on the front. This model is the standing-statue standard only; the
  variants are documented here but not modelled.

## Build

Procedural Blender 4.2 (script in `scripts/`): a rectangular loft through
the moulding profile, boolean-cut label recess, two materials (ebonised
wood, label plate). **96 triangles.** Renders use one fixed neutral-grey
rig for all views; `renders/compare.png` sets the reference crop beside
the three-quarter render.
