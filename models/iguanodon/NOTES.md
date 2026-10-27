# NOTES — Iguanodon (Hawkins's Sydenham dinosaur, as it survives)

Prop for the Crystal Palace film: the Sydenham grounds (CP043/CP047)
and the present-day park. Candidate #40 in `models/CANDIDATES.md`.

## What it is

One of Benjamin Waterhouse Hawkins's two surviving concrete
Iguanodons in Crystal Palace Park — specifically the **foreground
animal** of the reference photograph: the sprawled, low browsing
individual, belly near the ground, head raised, near foreleg lifted
and gripping the reddish conifer trunk it is pulling at, heavy tail
dragging on the ground behind. It stands on a simple low earth mound
(the park ground), with the trunk included because the pose is
unreadable without it.

**The anatomy is Hawkins's 1854 reconstruction, deliberately.** The
barrel body on four columnar legs and the conical spike on the nose —
the animal's thumb, misplaced there by Hawkins and Owen — are the
historical artefact. Nothing has been "corrected" toward the modern
bipedal, tail-up Iguanodon; a modern animal would be a different prop.

The second, standing Iguanodon (visible behind it in the photograph,
on its rock) is **not** modelled — one animal only, as briefed.

## Sources

- `refs/Iguanodon_Crystal_Palace.jpg` — the collection's only view of
  the dinosaurs: a modern colour photograph, front three-quarter.
  Repo path `references/muse-drive/images/main-article/Iguanodon_Crystal_Palace.jpg`;
  manifest entry "File:Iguanodon Crystal Palace.jpg", Wikimedia
  Commons, **CC BY-SA 2.0** ("Iguanodon at Crystal Palace. Benjamin
  Waterhouse Hawkins's Iguanodon statues.").
- No period image of the finished animal exists in the collection;
  the 1853 model-room material (ILN) is used in the sibling prop
  `models/hawkins-mould-and-table/`, whose mould is this animal's
  other half, so to speak — the dinner of 31 Dec 1853 was eaten
  inside it.

## Dimensions and their provenance

- **Overall length 30 ft (9.14 m) — DOCUMENTED for the animal as
  built**: ILN, 5 Nov 1853, on the clay model in Hawkins's model
  room: "thirty feet long and eleven feet high" (quoted in
  `models/hawkins-mould-and-table/NOTES.md`). Adopted as the scale
  anchor for this build.
- The model as built measures **9.28 m snout-to-tail-tip in plan**
  (about +1.5% on the adopted figure — the spine arc, with the neck
  raised, is a little longer), body barrel 1.90 m wide, back at
  2.21 m, **2.80 m high at the horn tip**.
- The ILN's "eleven feet high" (3.35 m) belongs to the standing
  clay model / standing pose and does **not** transfer to this
  reclining individual; the 2.80 m here is a consequence of the
  pose, not a measurement.
- Base slab: 12.6 × 7.2 m of park earth, a display convenience, not
  a documented object.

## Measured / seen vs guessed

**Seen in the photograph (one front ¾ view) and followed:** the
sprawled pose itself; belly low between the legs; head carried high
and turned slightly toward the viewer; mouth slightly open with a
fringe of small pale teeth along the seam; the nasal spike; small
eyes high on the skull; the near foreleg raised with long claws
curled round the reddish trunk; the far foreleg planted as a column
under the shoulder; the near hind leg crouched with the broad foot
flat and three blunt toes forward; the tail thick at the base,
tapering, lying flat on the ground; the pale sage green-grey of the
survivors' current paint.

**Guessed / inferred (no source shows them):** the whole far side,
the back and the underside (built symmetric-plausible); every
absolute dimension except the adopted ILN length; limb thicknesses,
which read slimmer here than the photograph's very massive legs;
the head's fine structure (schematic brow, nostrils placed by
analogy); the trunk's buried foot and broken top.

**Surface:** the survivors are armoured in large overlapping scales.
Here that is a procedural Voronoi-bump + noise mottle in the .blend
materials only — the **.glb carries flat base colour and roughness**,
so the scale read is lost in the GLB and at close range generally.
Treat this as a scene-distance prop.

## Stats

- 20 objects, **9,864 triangles** (counted three ways: build log,
  re-opened .blend, parsed .glb — all agree).
- `.blend` 1.07 MB, `.glb` 0.25 MB. Units: metres. Origin at base
  centre (ground level under the body's midpoint). Head toward +X,
  the animal's left (the photographed side) toward +Y.
- Build: `scripts/build_iguanodon.py` (procedural bpy lofts —
  body/tail/neck one loft, head and jaw separate lofts, legs as
  Catmull-Rom tubes, teeth/claws as merged cones). Renders:
  `scripts/render_views.py`, one fixed neutral-grey rig; the
  photomatch view approximates the photograph's viewpoint and
  `scripts/make_compare.py` composes `renders/compare.png`.

## Known inaccuracies

- Head is the weakest part: long-faced and domed in the right spirit,
  but the face is a stylisation — Hawkins's head has a heavier brow
  and a more broken silhouette than these smooth lofts give.
- Legs are slimmer and smoother than the massively wrinkled concrete
  originals; no skin folds are modelled.
- The gripping hand is a simplified mass behind the trunk; only the
  claw curl reads, as in the photograph it mostly does — but the
  real hand is larger and more fingered.
- The photomatch camera is an approximation; the compare image is a
  proportions check, not a registration.
- Three silhouette rounds were run against the photograph (head
  reduced and lengthened after round 1; gripping arm rebuilt and
  trunk shortened after round 2; jaw lifted for the final).
