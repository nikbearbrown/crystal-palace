# Farnese Bull group — build notes

> **⚠ LOOSE INTERPRETATION — MASSING ONLY.** This is the weakest-evidence
> model in the collection and must never be cited as a documented
> reconstruction. The single reference photograph shows the group small,
> distant and from behind; almost everything below the silhouette is
> convention taken from the famous antique type, not observation.
> Candidate #10 in `../CANDIDATES.md` (feasibility: **Low** — "recognisable
> massing only… expect a loose interpretation, flagged as such").

The cast of the Farnese Bull as it stood as the centrepiece of the Greek
& Roman Sculpture Court at Sydenham, in the court state photographed by
Philip Henry Delamotte in the 1850s. Sydenham state only — this group was
not at Hyde Park in 1851.

## Sources

Copy in `refs/`; original in the repo:

| Source | Licence |
|---|---|
| Album page "Assyrian Court, Facade Towards the Nave; Elevated View of Assyrian Court; Greek and Roman Sculpture Court; The Three Graces", MET DP323102 — `references/muse-drive/images/commons/-Assyrian_Court,_Facade_Towards_the_Nave;_Elevated_View_of_Assyrian_Court;_Greek_and_Roman_Sculpture_Court;_The_Three_Graces-_MET_DP323102.jpg` (copied to `refs/album-DP323102.jpg`; the bottom-left photograph, cropped to `refs/greek-and-roman-court-crop.jpg`, is the one that shows this group) | CC0 (MET via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) |

That is the **only** view of the group in the whole reference collection —
the manifest was searched for any other Farnese Bull image and none
exists. No source outside the repo was used, per MUSE-PROMPT.md.

## What the photograph actually shows (measured / seen)

- The group stands **centre-frame in the court, on a low, dark,
  rectangular platform** with a stepped/moulded top edge, roughly square
  in plan. (The benches and low protective railing around the platform in
  the photograph are court furniture and are **not** modelled.)
- The group sits on an **irregular rocky mount** that fills most of the
  platform top.
- The **bull rears on the mount**: hindquarters low at the rear, body
  rising diagonally, forelegs raised clear of the rock, head high. The
  rearing diagonal and the raised forelegs are the clearest forms in the
  photograph.
- A **tall draped standing woman** (Antiope) stands at the rear of the
  group; her draped back and the diagonal sash across it are legible.
- A **draped man** stands at the rear-right, seen from behind.
- Figures cluster at the bull's front and sides, and small forms
  (children/animals) sit at the base. Individual poses are **not**
  resolvable at this distance.
- The camera viewpoint is **elevated and from the rear-left** — the
  photograph shows the group's back, not its display front. The model is
  therefore arranged with its canonical front facing the opposite way,
  and `renders/photomatch.png` approximates the photograph's viewpoint
  for comparison.

## Dimensions and where they came from

**All dimensions are estimates.** Final model: **5,268
triangles**; overall **3.60 m wide × 3.10 m deep × 3.34 m
high** (bounding box), origin at base centre, floor at z = 0.

- **Platform 3.60 × 3.10 m, 0.43 m high** — proportioned from the
  photograph against the court's standard black display plinths (0.90 m
  high, see `../display-plinth/NOTES.md`; group bases there are noted as
  "lower and wider" than the standing-statue standard). The platform's
  width is ≈ 4× a statue plinth's height in frame, de-foreshortened;
  its height ≈ 0.45–0.5× a plinth's. Both ratios carry the photograph's
  perspective error.
- **Group above platform ≈ 2.91 m** (as built) — scaled so the standing figures read
  life-size (~1.72 m) against the same plinth yardstick, then checked
  against the antique type: the Naples original of the Farnese Bull is
  ~3.70 m high including its own base, so a full-size cast on a low
  platform should stand roughly 3.3–3.7 m overall. The model lands at
  the low end of that range; treat ±0.3 m as the honest uncertainty.

## Arrangement — convention, NOT observation

The figure arrangement follows the **canonical composition of the
Farnese Bull type** (the Hellenistic group known from the Naples
original), because the photograph cannot resolve it:

- bull rearing at the centre on the rocky mount;
- **Zethus** at the front-left, gripping the bull's lowered foreleg;
- **Amphion** at the front-right, one hand up to the bull's jaw, the
  other dragging **Dirce** by the hair;
- **Dirce** kneeling in the front-centre foreground, one arm raised;
- **Antiope** standing draped at the rear-left with a thyrsus staff;
- two children, a small goat, a seated dog and the sacrificial basket
  (cista) disposed at the base, as the type prescribes.

## Guessed / inferred (flagged, not presented as fact)

- Every figure's pose, gesture and exact placement (convention, above).
- The bull's head carriage, horns, tail and leg positions in detail —
  only the rearing diagonal and raised forelegs are observed.
- The rocky mount's exact shape; the model uses noise-displaced masses
  with angular crag shards to match the photograph's craggy texture at
  film distance.
- The platform's stepped cap profile — the photograph shows a moulded
  top edge but not its section.
- Material finish: pale plaster/stone for the cast, darker rock, near-
  black ebonised timber platform (the court's standard finish). The
  source is a sepia albumen print, so all colour is interpretation.
- The model's "front" is the type's canonical front; how the cast was
  actually oriented in the court is not recorded in the collection.

## Build

Procedural Blender 4.2 (script in `scripts/`): lofted body and figure
masses, noise-displaced rock, three materials. Renders use one fixed
neutral-grey rig for all views; `renders/compare.png` (built by
`scripts/make_compare.py`) sets the reference crop beside the
photomatch render.
