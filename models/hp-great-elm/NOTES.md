# NOTES — hp-great-elm: procedural elm tree (GENERIC)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 1, item 5).
Scenes: CP008 (build around the trees), CP017 (the park remains
inside — elms under the transept vault), CP022 (trees behind the
fountain). **Hyde Park 1851 building only** — the transept elms were
Hyde Park trees enclosed by the 1851 building; no Sydenham evidence
is used in this model.

## This tree is generic — read this first

**This is a generic procedural elm, not a portrait of any specific
tree.** The transept views (see `refs/REFERENCES.md`) show the elms
only at a distance, in a group, or silhouetted against the end
window; they cannot capture an individual elm, and no prop built
from them could honestly claim to be one. What the model takes from
the evidence is the *kind* of tree and its approximate proportions:
a mature English elm (*Ulmus procera*) with a tall straight bole, a
high fork, and the broad vase/fountain crown of the species, in full
summer leaf.

**Canopy / roof clearance is unresolved in the storyboard.** The
height below is a plausible mature-elm estimate derived from one
photograph's proportions (see next section). **This prop must not
be used to "prove" transept clearance** — it does not establish
that the real elms cleared, touched, or were cut back under the
102 ft 2 in vault. If a scene's argument turns on clearance, that
argument needs other evidence, not this tree.

Origin at base centre, ground at z = 0 (root flare buried 5 cm).
Units: metres. Blender 4.2+ (built with 4.5.3).

## Dimensions — estimated vs inferred

| Part | Value | Status |
|---|---|---|
| Total height | 22.0 m (72 ft) | **Estimated from a photograph** — see below |
| Crown width (spread) | ≈ 18.5 m (61 ft) | **Inferred** — see below |
| Crown base (lowest foliage) | ≈ 8.8 m | Modelled from the views (foliage begins around/above gallery height) |
| Bole top | 7.8 m; scaffold limbs leave the trunk at 5.9–7.8 m | Modelling interpretation of the fork zone |
| Trunk diameter at base | ≈ 2.0 m (radius 0.98 m), flaring to ≈ 2.6 m at the ground | **Guessed** — plausible for a mature park elm; no source measures the transept elms' girth |
| Seasonal state | Full summer leaf | From the views (Talbot calotype; Nash lithograph) |

**The height estimate.** In Talbot's 1851 calotype "View of
transept, looking south" (`refs/`), the great elm stands at the far
end of the transept at the same depth plane as the great end
window, whose arch crown is the transept vault crown: 102 ft 2 in
(31.16 m) above the floor (1856 guide table, Hyde Park building —
the figure the storyboard uses). Measured on the image (normalised
coordinates, checked by visual grounding): window arch crown
y = 135, elm canopy top y = 218, floor at the tree y = 424. So the
elm's height ≈ (424 − 218) / (424 − 135) × 31.16 m = **22.2 m**,
built as 22.0 m. The same measure gives the visible fork at
≈ 11.8 m — the point where the silhouette's trunk divides; in the
model the limbs leave the bole lower (5.9–7.8 m) and separate
visibly through the crown's lower half, which is how the layered
limbs read in the photograph. Treat all of this as ±10–15%:
perspective, the plate's soft focus, and the assumption that the
tree stands exactly at the end-wall plane all push the figure
around. It is an estimate for a generic tree, and that is all the
scene needs — CP008/CP017/CP022 show elms as the park surviving
inside the building, not as surveyed specimens.

**The spread.** The photograph's canopy spans x = 248–597
(normalised) against the end wall, but there is no clean horizontal
yardstick at that plane (the apparent width exceeds what the
72 ft transept would allow if read naively — the tree stands in
front of the wall, and neighbouring elms overlap it). 18.5 m is
chosen as a mature-elm spread that (a) matches the photograph's
broad fan, whose crown is much wider than the crown is deep, and
(b) fits inside the 72 ft (21.9 m) transept with room at the
galleries. **Inferred, not measured.**

## How it is built (technique)

Re-runnable script `build_hp_great_elm.py`, seeded
(`random.Random(1851)`) — re-runs produce the same tree; changing
the seed gives a sibling tree for groupings.

- **Bark structure, one merged mesh (4,432 triangles).** The trunk
  and branches are tapered tube runs along arched polylines,
  generated ring by ring and concatenated. The trunk is fluted
  (5 broad grooves, amplitude fading with height — elm boles are
  fluted and burr-knotted) with a flared, buttressed base. Six
  scaffold limbs (five + a central leader) leave the bole steeply
  (18–34° from vertical — the vase form) and arch outward; each
  recurses twice more (limbs → branches → twigs, ~140 branches in
  all), a few outer twigs drooping, as elm sprays do. Elm bark is
  deeply fissured in reality; here that is suggested by the
  fluting and radius noise only — **no photo textures** (rule:
  nothing from outside the repo), and the bark material is a flat
  grey-brown.
- **Foliage, instanced clusters (41,280 triangles instanced).**
  Sixteen reusable cluster meshes (12 outer, 4 dark interior),
  each an 80-triangle icosphere displaced by smooth noise plus
  per-vertex jitter, flattened and stretched — crumpled leafy
  lumps, flat-shaded so the facets read as leaf breakup at film
  distance. 516 instances share those 16 meshes and differ only
  by position and rotation (scale is exactly 1.0; size variety is
  baked into the variants), so the prop is **instancing-friendly**:
  a scene can place many copies cheaply, and the .blend keeps the
  shared mesh data. Placement is art-directed, not random fill:
  an outer shell and mid layer following a fan-shaped crown
  profile (widest at 17–19 m, lobed outline), a top cap, a hanging
  skirt at the lower edge, dark interior fill for depth, and
  clusters hung along the outer branches and twig tips so the
  foliage sits on the limb structure instead of floating above it.
- **Materials:** four flat colours (bark, two leaf greens, one
  deep interior green), roughness 1.0. No textures, no alpha —
  the canopy is solid geometry and reads clean against the sky
  and the glazing at film distance.

**Triangle count: 45,712 total** (instanced count, printed by the
build script) — inside the ~50k prop budget. Objects: 517
(1 bark mesh + 516 foliage instances). File sizes: .blend 1.5 MB,
.glb 0.31 MB (17 meshes — the 16 cluster variants + bark — over
517 nodes).

## What was seen vs what was guessed

- **Seen in the refs:** tall clear bole; high fork; long limbs
  radiating up and out, visible through the lower crown; foliage
  layered along the limbs; crown a broad fan, widest high, top
  gently domed; crown top well below the vault crown; full leaf.
- **Estimated:** total height 22.0 m (method above).
- **Inferred/guessed:** crown width 18.5 m; trunk girth; the exact
  limb pattern (procedural, species-typical, not traced); bark
  colour and the three foliage greens (period views are a
  photograph's sepia and a lithograph's hand colour — the greens
  are a modern plausible summer elm, nothing more); crown depth,
  which the model makes ≈ crown width (a radially symmetric fan),
  whereas any real elm differs front-to-back.

## QC

Built and rendered three times before this version. Round 1
(smooth-shaded, large clusters) read as balloons on a pole —
rejected. Round 2 fixed the silhouette (fan profile, limbs
carrying foliage) but placed 762 clusters = over the triangle
budget — rejected on count. This version: flat-shaded, smaller
clusters in two layers plus interior fill, cluster cap enforced
in code, twig tips capped with foliage so bare twigs don't read
as wires. All three renders were viewed: the fan silhouette,
clear bole and forking limbs read as an elm against the Talbot
view from front, side and three-quarter. Remaining known
weaknesses, stated plainly: a handful of outer twigs still read
as thin lines at 960 px (at film distance, inside a transept,
they read as sprays); the trunk's bark is smooth-toned — its
fissuring is only in the geometry's fluting; the crown is
slightly more regular than a real elm's. None of these is
visible at the distances CP008/CP017/CP022 use the tree.

Renders use the same studio setup as the other Wave-1 props
(neutral grey backdrop and world, sun + area fill, Cycles CPU,
960×720; front/side orthographic, three-quarter perspective).
