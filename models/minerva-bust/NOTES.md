# Minerva bust — build notes

The helmeted bust the court lettering calls **"328 / MINERVA /
FROM MUNICH"**, Greek & Roman sculpture court, **Sydenham** — candidate
#7 in `../CANDIDATES.md`. Film scene CP036. Sydenham state only.

The bust is modelled **on its tall dark court pedestal**, as
photographed. The pedestal is the `CastBase_Bust` of
`../sy-classical-cast-base/`, reproduced here at that build's
published dimensions (pedestal 1.30 m, die 0.46 m square, foot step
and cove, plain flat top) so the two props agree if both are placed
in a scene; in this model the bust, socle and pedestal are separate
objects and the bust can be lifted off. The full-length figure in
the same photograph is `../aristides-statue/` (candidate #6).

## Orientation — read before placing

The photograph shows the bust from its **front-left three-quarter**,
hard against the right edge of the frame; the pedestal's lettered
face and the bust's front face the same way (the aisle). The model
keeps that relationship:

- the bust's anatomical front faces **−Y**;
- the head is **turned to its anatomical left (+X) and bowed**, as
  photographed — this is part of the object, not a rig pose. The
  turn (modelled at 45°) is estimated from the one view: it is the
  angle that makes the face read three-quarter from the
  photograph's own camera quadrant, and ±10° either way cannot be
  excluded;
- renders: `front.png` = the bust's front (−Y); `side.png` = its
  left profile (+X); `three-quarter.png` and `photomatch.png` are
  from the (+X, −Y) quadrant, close to the photograph's own
  viewpoint; `compare.jpg` sets the photomatch beside the
  stereograph crop.

## Sources

Copies in `refs/`; originals in the repo:

| Source | Licence |
|---|---|
| Greek & Roman sculpture court stereograph, RP-F-2012-96-327 — `references/muse-drive/images/commons/Beelden_in_de_Griekse_en_Romeinse_zaal_in_Crystal_Palace_in_Sydenham_Crystal_Palace._101._Statues_in_the_Greek_and_Roman_sculpture_court._(titel_op_object),_RP-F-2012-96-327.jpg` (Rijksmuseum via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) | CC0 |
| Enlarged crops of the same stereograph in `refs/` (bust; pedestal + socle) | CC0 |

One source only: a stereo pair (dated c.1870–c.1890 in the manifest)
whose **left half** shows the bust; the right half crops it almost
entirely behind the card mount. The bust's right side is cut off by
the frame edge in both halves.

## Dimensions and where they came from

Overall assembly **2.20 m high** as built; footprint 0.536 × 0.536 m
(the pedestal foot). Origin at base centre; built in metres, scale
applied. **24,044 triangles**, 11 objects.

**The absolute scale is the shared court chain, not a measurement of
this object.** No dimensioned source for the bust exists in the
collection.

- **Pedestal 1.30 m**, die 0.46 m square — adopted wholesale from
  `../sy-classical-cast-base/`, which derived the bust pedestal from
  its measured ratio against a life-size cast (its own uncertainty
  ±0.06–0.08 m). Foot step 0.055 m high projecting 38 mm, cove
  0.095 m, plain die, **no cap moulding** (the photograph contradicts
  one; see that build's notes).
- **Bust + socle 0.88 m** — from the cast-base build's ratio measured
  on *this* bust in *this* photograph: pedestal height ÷ bust height
  incl. socle = **1.48** (410 : 277 units) → 1.30 / 1.48 = 0.878 m.
- **Internal proportions** are my picks on the left stereo half at
  native resolution: crown → socle foot = 629 px = the 0.88 m above.
  Socle = 110 px → **0.15 m**; head, chin → helmet crown = 238 px →
  **0.33 m**, of which face (chin → brow) ≈ 120 px and helmet dome
  (brow → crown) ≈ 115 px — near-equal halves, which is why the dome
  is so tall. Read absolutes as **±10%**, the chain's own tolerance;
  the as-built assembly stands 15–20 mm over the nominal 2.18 m in
  the neck overlap, inside that tolerance.
- **Socle profile** read from the enlarged socle crop: trumpet flare
  under the bust, a projecting roll at ~60% of its height, a concave
  waist, a stepped foot. Foot Ø **0.23 m** from the crop's
  width : height (≈ 178 : 120 px). The socle's small painted number
  ("136", read on the crop) is **not** modelled — project practice is
  no fabricated lettering; the pedestal likewise carries the court
  family's recessed unlettered label plate, not the painted
  "328 / MINERVA / FROM MUNICH".
- **Bust width 0.50 m, depth 0.345 m** — the width is *not* fully
  measurable: the frame crops the bust's right side. The visible
  truncation spans ≈ 350 px (≈ 0.49 m) at the socle crop's scale;
  0.50 m adopted, consistent with the classical bust type. Depth is
  by type. Both flagged as the weak dimensions.

## Measured / seen in the photograph

- A female bust in a **tall, smooth Corinthian-type helmet**: the
  dome rises about as far above the brow as the face falls below it;
  a defined brow edge; cheek pieces hang beside the face; the head
  is turned to its left and inclined down, the face in shadow.
- **Hair escapes from under the helmet** in curl masses at both
  sides of the neck and the nape.
- A long, bare, forward-sloping neck.
- An **aegis high on the chest** — a rough, scaly-textured patch
  with a discernible **gorgoneion medallion** at its centre — and a
  thin trim/strap line descending from the neck toward it.
- **Bold, smooth pleats sweep diagonally** from her left shoulder
  across the chest (the himation), the single strongest drapery read
  in the frame.
- The bust truncates below the chest and stands on a **turned
  socle** (profile above) on the court's standard dark pedestal.

## Guessed / inferred — not seen

- **Everything the frame crops**: the bust's right shoulder and
  right side are completed by symmetry and the bust type.
- **The whole back** — never photographed: plain drapery mass, the
  helmet's neck guard and the nape hair are type inference.
- **The face is schematic** (brow ridge, shallow eye sockets, nose,
  mouth groove). In the photograph the face is washed out and turned
  away; no features beyond its profile line are actually legible,
  and none are invented here.
- **No crest is modelled.** The dome reads smooth in the
  stereograph; at this resolution a low crest-holder cannot be
  wholly excluded, but there is no evidence for a plume, so none is
  shown.
- The socle is modelled **round** (turned). Its crop shows a flat
  front face with the curved profile at the sides; a square-plan
  waisted socle cannot be entirely ruled out, but turned socles are
  the type and the silhouette curves are continuous.
- The aegis's scale texture is procedural noise; the gorgoneion's
  face is an abstract relief (two eye bumps, brow bar, nose wedge) —
  the photograph shows a face-like medallion whose features do not
  resolve.
- Materials are flat plaster / ebonised tones for the grey rig; the
  stereograph is a sepia albumen print, so exact tones are an
  interpretation.

## Build

Procedural bpy (Blender 4.2), scripts in `scripts/`; the torso is a
lofted profile with carved-fold displacement plus separate pleat
tubes, the socle a lathe, the head a displaced loft posed by a baked
rotation, the helmet a loft with cheek pieces and neck guard. Three
build/render rounds: round 1 established the forms (the pedestal
first read as a cylinder — rebuilt on a true rounded-rectangle
outline in round 2; the head sat too low — shoulders lowered and
the neck lengthened); rounds 3–4 calibrated the head's turn
against the photograph (32° read too frontal from the
photograph's quadrant; settled at 45°); round 5 corrected the
face : dome proportion to the measured near-equal halves (the
first build's face was a third too short). Renders are Cycles CPU
on the fixed grey rig in `scripts/render_rig.py` (Eevee cannot
initialise in this VM — no EGL).

**Weakest points, honestly:** the face (schematic, from a washed-out
source), the cropped right side and the bust's absolute width, and
the socle's plan. The three-quarter view — the one view the film can
check against the photograph — is the strong one.
