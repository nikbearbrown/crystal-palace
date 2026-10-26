# Una and the Lion — build notes

John Bell's sculpture group as displayed at Sydenham: Una seated sidesaddle
on a walking lion, the group on its rocky base atop a tall black display
plinth. Candidate #1 in `../CANDIDATES.md`. Sydenham state (the courts as
photographed in the 1850s–60s).

## Sources

| Source | Licence |
|---|---|
| Stereograph, Crystal Palace, John Bell's Una and the Lion — MET DP700246 — `references/muse-drive/images/commons/-Stereograph,_Crystal_Palace,_John_Bell's_Una_and_the_Lion-_MET_DP700246.jpg` (copy in `refs/`) | CC0 (Metropolitan Museum of Art via Wikimedia Commons, per `references/muse-drive/data/manifest.csv`) |

That is the **only** usable view in the collection. The companion file
DP700247 is the card's green verso, not a second view, and was not used.
The stereograph's two eyes give two close three-quarter views from the
group's display front (the lion's left side); both were used — the
silhouette, pose and drapery were traced from them. **No front-on,
rear or right-side view survives in the collection**, so everything the
stereograph cannot see is inference (below).

## Dimensions and where they came from

Overall (final build, measured from the .blend): **3.256 m high ×
2.450 m long × 0.976 m deep**; origin at the centre of the plinth foot.
Sculpture group above the plinth: **2.16 m**. Plinth: **1.10 m high**,
foot 2.45 × 0.98 m, top slab 2.44 × 0.97 m. Rock base ≈ 0.2 m thick,
its top at ≈ 1.32 m. Lion's back ≈ 1.03 m above the rock. **33,888
triangles.**

These are **photo-derived ratios hung on one stated assumption, not
survey measurements**:

- Points picked on the stereograph give plinth height ÷ group height
  ≈ 0.51–0.53, group length ≈ 0.94 × plinth length, and Una's seated
  height (seat to crown) ≈ 0.40 × group height.
- The absolute anchor is Una herself, taken as a **life-size seated
  figure** (seat to crown 0.86 m). That yields the 2.16 m group and
  1.10 m plinth above. Sensitivity: if Bell's group was somewhat over
  life-size, every absolute figure scales up together; the proportions
  stand either way.
- Cross-check: the plinth is the same black ebonised family as
  `../display-plinth/` (0.90 m for a standing statue; that model's notes
  document taller and lower/wider court variants). A 1.10 m plinth for
  a large group sits inside that documented family range. Its plan size
  comes from the photograph relative to the group; the photograph is a
  three-quarter view, so **depth is the least certain dimension
  (±15%)**.

## Measured / seen in the photograph

- Una sits **sidesaddle on the lion's left flank**, well back over the
  mid-back, legs together, knees bent, shins hanging, feet pointed and
  dangling clear of the base.
- Her **left arm reaches forward**, hand resting on the mane; her right
  arm is bent across her waist **cradling a spray of lilies**.
- The lion walks in a pace gait — near foreleg reaching far forward,
  far foreleg planted back under the chest — with its **head bowed low**,
  muzzle close above the base, mouth slightly open.
- A **huge mane** frames the head and covers the shoulders and chest.
- **Drapery**: a cloth under her seat spills down the near flank in long
  folds and pools forward on the rock; a second folded panel hangs over
  the lion's shoulder beside the mane.
- A **floral garland** swags across the rump, with a small cluster at
  its top (possibly a bird — see below).
- The **tail** hangs down the rear and its tuft lies forward on the rock.
- The sculpture stands on a **rough, irregular rocky slab** that
  overhangs the plinth unevenly.
- The plinth is a tall, straight black block. Its face carries painted
  white lettering (legible, reversed in the glass stereograph: "UNA AND
  THE LION / JOHN BELL", with the rock edge inscribed "UNA or PURITY").

## Guessed / inferred (flagged, not presented as fact)

- **The whole far side and back are unseen.** The far legs are placed by
  normal quadruped gait logic (pace), the far flank and the fall of
  drapery behind her seat by symmetry with the seen side. Treat the
  lion's right-side (+Y) geometry as a plausible completion, not
  evidence.
- **Face and hands are schematic** — smooth masses with a nose ridge and
  brow, no carved features; the photograph itself shows her features
  only softly at this size.
- **Hair** is a smooth swept-back mass with a low knot, as photographed;
  no strand detail.
- **The mane's carved locks** are far deeper and more directional in
  the marble than this model's noise-displaced surface — the model's
  mane reads smoother and rounder than the original (weakest point,
  see below).
- **The garland's top cluster** is modelled as a small schematic
  bird-like form; at the photograph's resolution it cannot be confirmed
  as a bird.
- **Label**: following the display-plinth family convention, the label
  zone is a shallow unlettered plate. The photograph shows painted
  lettering; no text is modelled.
- **Plinth mouldings**: the stepped foot and thin cap follow the court
  family; the photograph shows the shaft clearly but the foot is in
  shadow, so the moulding profile is family inference.
- **Finish**: white marble for the group (the original is marble; the
  hand-coloured print reads near-white), greyer rough stone for the
  rock slab, satin black for the ebonised plinth — all interpretations
  of a monochrome/sepia source.

## Build

Procedural Blender 4.2, profile-first (script in `scripts/`): the side
silhouette was traced from the stereograph and each mass lofted with
rounded cross-sections — lion body, legs, Una's torso, limbs and neck —
with displaced-sphere masses for the mane, haunches, head and rock, and
folded ribbon sheets for the drapery. Five build rounds were run against
the photograph (orientation/mirror correction, mane and face
integration, gait and drapery fixes). Renders use the house neutral-grey
rig; `renders/compare.png` pairs the stereograph with a render from a
matched viewpoint.

**Weakest points, honestly**: the mane (too smooth and spherical versus
Bell's deeply locked carving) and the lion's face, which is a schematic
assembly sitting slightly proud of the mane rather than carved within
it. From the display front at film distance the profile — Una's seated
pose, the reaching arm, the bowed head, the pooling drapery — matches
the photograph well; from the far side the model is an informed guess
and should be used accordingly.
