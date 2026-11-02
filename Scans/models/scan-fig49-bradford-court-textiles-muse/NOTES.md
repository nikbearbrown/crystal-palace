# NOTES — scan-fig49-bradford-court-textiles (Muse version)

## Subject

Bradford Court textile display at the Great Exhibition of 1851 (Crystal
Palace, Hyde Park), from catalog figure 49 — "Bradford Court: exhibits for
women"; "Colour interior of Bradford Court showing striped fabrics, textile
cabinets, women and a child." A composed section of the court, ~6 m wide,
modelled from the single colour view in `refs/`:

- **Centre (signature element):** tall lengths of boldly striped fabric
  hanging in soft folds from a canopy frame on brass posts with finials,
  over a dark plinth. The stripes are a procedural texture generated in the
  build script — vertical bands of varied width in red, blue, yellow,
  green, pink and white, matching the hangings in the image. The cloth is a
  subdivided grid mesh displaced into gentle folds that deepen toward the
  hem (no cloth simulation). Two broad panels, a third backing panel, and
  one short striped length draped over the plinth front.
- **Left:** freestanding timber display kiosk — polished mid-brown frame,
  panelled base with two circular motifs on the front, glazed upper storey,
  shallow roof, and an oval pediment crest (gold rim, blue centre) on a
  stepped base. Inside: fabrics draped at the back, cloth piled in mounds
  and folded stacks in many colours on a shelf.
- **Right:** display counter in dark mahogany with a glass top sloping
  toward the viewer, framed in dark wood bars, with cloth mounds and a
  white cloth roll inside; behind it a second glazed cabinet holding two
  draped cloths (sage and grey) and a simplified gold crest plaque.
- **Setting:** pale boarded floor only. The Crystal Palace roof, trusses
  and columns in the background of the image are **not** modelled (per
  brief). One plain deep-red hanging banner is included **blank** — the
  original banners carry lettering; all text is omitted.
- **Figures (stylised, simplified, no likenesses):** two women (~1.62 m) in
  bonnets and white shawls over full skirts, with green neck ribbons,
  standing beside the left end of the counter; a child (~0.98 m) beside
  them in a red coat, white stockings and a straw hat, holding a thin
  stick — as shown in the image.

## Scale

- **ESTIMATED.** No dimension is given in the source. Basis: the women in
  the image are taken as ~1.6 m tall; every other element is sized in
  proportion to them as drawn (kiosk ≈ 2.05 m wide × ≈ 2.9 m to the crest
  top; striped hangings ≈ 2.2 m drop from a 2.95 m canopy; counter base
  ≈ 0.9 m high; floor section 6.6 × 4.2 m). Treat all dimensions as
  approximate (±20 %).
- Units: metres. Origin at base centre (floor centre, z = 0 at floor top).
  Scale applied on all mesh objects.

## Assumptions / interpretations

- **Single view.** Only the front three-quarter view in the image is
  evidence. Backs and unseen sides (kiosk rear, cabinet rear, the reverse
  of the hangings) are reasonable period interpretations, **not**
  confirmed fact: the kiosk rear is plain framed glazing/panelling like
  its sides, and the hangings would read the same from behind.
- The composed section compresses the court: in the image the right-hand
  cabinet sits further back; it is brought into the ~6 m section so the
  whole group reads as one asset.
- The kiosk crest in the image is an oval armorial plaque with carved
  scrollwork; it is simplified here to a gold-rimmed blue oval on a
  stepped base with two scroll knobs — the arms themselves are not
  reproduced. The gold plaque in the rear cabinet likewise simplifies a
  heraldic crest hanging between draped cloths.
- Fabrics inside the kiosk and counter are represented by draped back
  cloths, rounded cloth mounds and folded stacks in period colours; the
  image's individually folded and fringed pieces are not itemised.
- The women's skirt colours (green-toned and pale) follow the two figures
  in the image; faces are featureless — no likenesses are attempted.
- The banner is blank by design (lettering omitted), and the small dark
  name boards visible in the image on the kiosk, plinth and counter are
  omitted rather than given invented text.

## Build / files

- `build_scan_fig49_bradford_court_textiles.py` — re-runnable bpy script
  (Blender 4.5.3): `blender --background --python
  build_scan_fig49_bradford_court_textiles.py`. It regenerates the .blend,
  the .glb and `preview.png`, and prints the triangle count. Both image
  textures (striped fabric, floor boards) are generated procedurally in
  the script and packed into the .blend.
- `scan-fig49-bradford-court-textiles.blend` / `.glb` — 183 mesh objects
  (111 originally; +72 fold-welt segments from fix round 1, see QC).
- `preview.png` — Cycles CPU, 32 samples with denoising, 960 × 720,
  neutral grey background, three-quarter view from front-right (kiosk
  left, striped hangings centre, counter and figures right), comparable
  to the reference view.
- `refs/` — copy of the source image + `REFERENCES.md`.

## Triangle count

**23,648 triangles** (script count over all mesh objects) — under the
50k budget. (17,088 before fix round 1; the increase is the higher-
resolution cloth-pile meshes and their fold welts.)

## QC

- Preview viewed against the reference before finishing: composition,
  stripe palette and figure placement checked; a first render was
  rejected and fixed (lighting overexposure washing the timber to pink,
  women intersecting the counter volume, kiosk crest motif orientation).
- Known simplifications for manual review:
  1. Cloth folds are a regular sine displacement — softer and more
     regular than real worsted hangings; acceptable at this scale but
     the first thing to improve with a cloth sim if the asset is promoted.
  2. The kiosk interior reads through glass that is modelled as a single
     transparent pane per face; reflections are minimal.
  3. The rear cabinet is only partly visible in the preview (behind the
     counter, as in the reference) — check it in the .blend if its detail
     level matters.
  4. Figure hands/faces are not modelled; shawl points and bonnet brims
     are stylised cones/tori.

- **Fix round 1 (parent audit — fabric piles only; scene not rebuilt):**
  1. *Colour.* The piled/draped kiosk fabrics and the counter cloths
     rendered as pastel blobs (baby blue, pink, cream). Cause found in
     the script: the fabric colours were authored as display (sRGB)
     values but fed straight into Blender's linear Base Color socket,
     lifting them ~a gamma step, and several palette entries were
     pastel to begin with. Fix, in the build script only: a proper
     sRGB→linear conversion (`srgb_to_linear`, applied via
     `mat(..., srgb=True)` to the pile/drape fabrics only — all other
     materials untouched) and a richer, saturated palette matching the
     reference cloths — bottle green, deep teal-green, burgundy,
     crimson, plum purple, deep mauve, navy, ochre, russet, olive —
     with a single cream-wool entry kept for the light cloths in the
     reference. Verified by eye against the reference: the kiosk piles
     now read green / plum / teal and the counter cloths mauve /
     burgundy / ochre instead of the previous macaron pastels (they
     still sit behind the modelled glass, which hazes them slightly,
     as in the reference view).
  2. *Form.* The kiosk piles read as smooth stones/eggs. Each cloth
     mound (kiosk piles and, by the same helper, the counter cloths)
     now has cheap fold cues, no cloth sim: light noise displacement
     on a higher-resolution mound mesh, three shallow crease grooves
     carved across the upper surface, and three low ridge welts along
     the same fold lines — segmented thin boxes in a darker shade of
     the pile's own fabric, following the dome so they read as folded
     cloth edges at preview distance. Verified in the regenerated
     preview: the fold bands are visible on the counter cloths and,
     through the glass, on the kiosk piles.
  3. Regenerated `.blend` / `.glb` / `preview.png` from the edited
     script with the same camera; nothing else in the scene changed.
     New count: **23,648 triangles** (was 17,088), 183 mesh objects —
     still under the 50k budget.
