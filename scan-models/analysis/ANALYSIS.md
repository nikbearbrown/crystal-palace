# Analysis: how well the 16 scan models match their reference images

Made 2026-11-03 with the `blender-analysis` skill. One reader's critique from the comparison sheets in `analysis/sheets/`, which put each reference crop beside the model rendered from a comparable angle, plus a view the reference never shows. It judges likeness to the picture only. It says nothing about how a model behaves in a game engine, which was not tested.

## Summary

Of 16 models, five reproduce their reference well (Greek Slave, Watherston and Brogden vase, Elkington jewel cabinet, tea service, obelisk shaft), five are good objects that need a fused background deleted or a part rebuilt (piano, canopy chair, urn stand, balloon-back chair, elephant), five are starting meshes only (boulder pile, balustrade, working-class home, tower, Centenary model), and one (Brompton Boilers) does not reproduce its reference. The deciding factor was not the object but the crop: every model cut out of a crowded or lit scene dragged part of the scene into the mesh.

| Group | Models |
|---|---|
| Reproduces its reference | greek-slave, watherston-brogden-vase, elkington-jewel-cabinet, tea-service, obelisk |
| Good object, contaminated by the scene around it (usable after cleanup) | inlaid-piano-and-stool, tufted-canopy-chair, gilt-urn-stand, balloon-back-chair, indian-elephant-howdah |
| Starting mesh only | boulder-pile, cast-iron-balustrade, model-working-class-home, tower-conversion-design, centenary-model |
| Does not reproduce its reference | brompton-boilers |

## Reading the verdicts

`matches`, `partly`, `does not`, or `cannot judge` (the reference does not show it). Every gap names its cause: **model** (the generator departed from the reference), **reference** (the picture cannot show it) or **comparison** (the comparison is unfair). A view the reference never shows is only described, never compared. Triangle counts are facts about the file; every model is about 1.4 million triangles and none is watertight, so the count says nothing about quality.

## Reproduces its reference

### fig-52_greek-slave

- **Reference:** `Scans/images/fig-52_hiram-powers-greek-slave-1843.png`, crop `whole image`, input `inputs/fig-52_greek-slave.png` (sha256 58184865d8b3…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19962-058c-7ab3-adea-d5773586b19a` (ledger). One image, no second view.
- **Model:** `glb/fig-52_greek-slave.glb` (sha256 c009fbfe07f1…), 1,458,679 triangles, 0.5347 x 1.65 x 0.5585 m as built, not watertight. Claimed scale: height = 1.65 m, general knowledge, not stated in the scan or catalog; verify.
- **Sheet:** `analysis/sheets/fig-52_greek-slave.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Contrapposto stance, head turn, the draped post and the round base all line up with the print. | — |
| Detail | matches | Hair knot, the chain at the wrists and the folds of the drapery are kept; the surface reads as marble. | — |
| Contamination | matches | No background or support from the dark studio plate came through. | — |
| Unseen sides | cannot judge | The back is anatomically coherent but invented; the print shows only the front. | reference |
| Scale | cannot judge | 1.65 m is an estimate for a life-size marble, not a measurement. | comparison |

**Good for as it stands:** an archival proxy for the statue's front, and a reasonable base for retopology.

**Next experiments:** (1) Check the 1.65 m against a catalogued height for the statue. (2) Retopologise before any engine use; 1.46 million triangles is not a game asset.

### unnumbered_watherston-brogden-vase

- **Reference:** `Scans/images/unnumbered_watherston-brogden-ornamental-vase.png`, crop `whole image`, input `inputs/unnumbered_watherston-brogden-vase.png` (sha256 7b0e8e86f996…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a1995d-c43f-7f30-8eec-d63fb8c3f824` (ledger). One image, no second view.
- **Model:** `glb/unnumbered_watherston-brogden-vase.glb` (sha256 c4410ae2bb0d…), 1,426,179 triangles, 0.4918 x 1.2 x 0.5484 m as built, not watertight. Claimed scale: height = 1.2 m, estimated.
- **Sheet:** `analysis/sheets/unnumbered_watherston-brogden-vase.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Statue on the lid, hexagonal drum, flared foot and pinnacles in the right order and proportion. | — |
| Detail and ornament | partly | Figure niches and the foot's seated figures are kept; fine ornament (swags, rope bands) is softened to bumps. | model |
| Parts | matches | All pinnacles and the four visible figure groups are present. | — |
| Unseen sides | cannot judge | The drum's far faces are invented; they continue the same figures plausibly. | reference |

**Good for as it stands:** an archival proxy for the front; the ornament is impressionistic.

**Next experiments:** (1) Compare the far faces against another engraving of the vase if one exists. (2) Re-render at a closer camera to judge how much ornament survived.

### fig-54_elkington-jewel-cabinet

- **Reference:** `Scans/images/fig-54_louis-gruner-elkington-jewel-cabinet-1851.png`, crop `whole image`, input `inputs/fig-54_elkington-jewel-cabinet.png` (sha256 bc77fe7f343c…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19962-2a62-7a22-aab0-96b1d78d86d4` (ledger). One image, no second view.
- **Model:** `glb/fig-54_elkington-jewel-cabinet.glb` (sha256 baa481215e3d…), 1,400,627 triangles, 0.9496 x 1.0168 x 1.4 m as built, not watertight. Claimed scale: max = 1.4 m, estimated.
- **Sheet:** `analysis/sheets/fig-54_elkington-jewel-cabinet.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Pagoda-style blue roof, projecting wings, lion finial and base all match. | — |
| Parts | matches | Two framed portraits, the central statuette, two caryatids and the enamel roundels are present. | — |
| Detail | partly | The finial group is simplified, and the portraits are only faint paintings: it is not the same pair of faces. | model |
| Surface and colour | matches | Gilt, silver and blue read correctly; the plate is coloured, so tone is indicative only. | comparison |
| Unseen sides | cannot judge | The back repeats the front composition with different portraits; that is invention. | reference |

**Good for as it stands:** an archival proxy for the front.

**Next experiments:** (1) Check the portraits against the catalogue description rather than the generated texture. (2) Remove the invented back panel if the model is shown from behind.

### fig-03_tea-service

- **Reference:** `Scans/images/fig-03_felix-summerly-tea-service-henry-cole-1846.png`, crop `whole image`, input `inputs/fig-03_tea-service.png` (sha256 17487d4f19a3…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a1995d-c720-7c70-8328-cde0c289adf6` (ledger). One image, no second view.
- **Model:** `glb/fig-03_tea-service.glb` (sha256 024832f5c417…), 1,400,242 triangles, 0.3765 x 0.4017 x 0.7 m as built, not watertight. Claimed scale: max = 0.7 m, estimated.
- **Sheet:** `analysis/sheets/fig-03_tea-service.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Parts | matches | All seven pieces are present and separate: bowl, jug, teapot, two cups, two saucers. | — |
| Detail | matches | The animal-head spout and lid knop on the teapot read correctly. | — |
| Layout | partly | The pieces sit loose on a floor instead of on the two shelves of the photograph. | model |
| Surface and colour | cannot judge | The photograph is monochrome, so the off-white is an assumption. | reference |
| Unseen sides | cannot judge | Cup interiors and saucer undersides are invented. | reference |

**Good for as it stands:** an archival proxy for the shapes; the arrangement is not the photograph's.

**Next experiments:** (1) Place the pieces on shelves in Blender if the arrangement matters. (2) Generate each piece separately for cleaner meshes.

### fig-24a_obelisk

- **Reference:** `Scans/images/fig-24_raw-materials-west-entrance-crystal-palace.png`, crop `[1239, 212, 1534, 1310]`, input `inputs/fig-24a_obelisk.png` (sha256 121c47baa534…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a14-a6e9-76b2-994b-2aa816441a61` (ledger). One image, no second view.
- **Model:** `glb/fig-24a_obelisk.glb` (sha256 5407e1d5531f…), 1,470,940 triangles, 2.0287 x 5.5 x 1.1206 m as built, not watertight. Claimed scale: height = 5.5 m, estimated.
- **Sheet:** `analysis/sheets/fig-24a_obelisk.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Tall tapered shaft with a broken top, the same taper and edge as the print. | — |
| Surface | matches | Weathered yellow stone with a vertical grain. | — |
| Base and ground | partly | A rough boulder stump is fused onto the foot; the print hides the real base behind boulders. | reference |
| Contamination | partly | A slab edge from the left of the crop shows at the foot of the model. | model |
| Scale | cannot judge | 5.5 m was set against standing visitors, which stand nearer the camera. | comparison |

**Good for as it stands:** an archival proxy for the shaft; the foot is invented.

**Next experiments:** (1) Crop the shaft only, above the boulders, and regenerate. (2) Check the height against the known obelisk if the exhibit is identified.

## Good object, contaminated by the scene around it (usable after cleanup)

### fig-31a_inlaid-piano-and-stool

- **Reference:** `Scans/images/fig-31_goods-for-home-decorative-furnishings.png`, crop `[835, 789, 1740, 1613]`, input `inputs/fig-31a_inlaid-piano-and-stool.png` (sha256 d1a4fb627895…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a16-bdda-7ca0-91d7-49682cdd0019` (ledger). One image, no second view.
- **Model:** `glb/fig-31a_inlaid-piano-and-stool.glb` (sha256 195ae6eb37a8…), 1,477,598 triangles, 1.2308 x 1.4 x 2.2882 m as built, not watertight. Claimed scale: height = 1.4 m, estimated.
- **Sheet:** `analysis/sheets/fig-31a_inlaid-piano-and-stool.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Parts | matches | Keyboard, music sheet, stool and scroll feet are present. | — |
| Detail and ornament | partly | The inlay on the case is simplified; the heavy ornament of the print is smoother. | model |
| Contamination | does not | The standing man from the crop edge is fused to the left of the piano as a full figure, with a slab behind him. | model |
| Proportion | partly | The case looks lower and wider than the print's tall upright, partly because of the fused slab. | model |
| Unseen sides | cannot judge | The back is a plain panelled box, invented. | reference |

**Good for as it stands:** usable after deleting the figure and the slab.

**Next experiments:** (1) Delete the man and the slab, then re-measure the piano against the 1.4 m estimate. (2) Regenerate from a crop that excludes the man.

### fig-31b_tufted-canopy-chair

- **Reference:** `Scans/images/fig-31_goods-for-home-decorative-furnishings.png`, crop `[1659, 302, 2378, 1044]`, input `inputs/fig-31b_tufted-canopy-chair.png` (sha256 e9a08bd1a306…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a16-de4e-7561-a6e1-0a25e549b9f4` (ledger). One image, no second view.
- **Model:** `glb/fig-31b_tufted-canopy-chair.glb` (sha256 213094107dca…), 1,492,212 triangles, 2.0157 x 1.5 x 1.3535 m as built, not watertight. Claimed scale: height = 1.5 m, estimated.
- **Sheet:** `analysis/sheets/fig-31b_tufted-canopy-chair.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | partly | The hooded, tufted chair with gilt edge reads, but the seat is shallow and the hood sweeps less than the print. | model |
| Detail | matches | Tufting, gilt trim and tassels are kept. | — |
| Contamination | does not | A curtain column and small props (a drum, a footstool) are fused beside and in front of the chair. | model |
| Unseen sides | does not | The back is a smooth blank shell. | reference |

**Good for as it stands:** usable after separating the chair from the curtain and props.

**Next experiments:** (1) Select the chair alone in Blender and delete the rest. (2) Regenerate from a crop with the curtain painted out.

### fig-31c_gilt-urn-stand

- **Reference:** `Scans/images/fig-31_goods-for-home-decorative-furnishings.png`, crop `[2065, 858, 2343, 1601]`, input `inputs/fig-31c_gilt-urn-stand.png` (sha256 356e083afc45…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a19-1451-76d2-b832-0dfdf7cc3640` (ledger). One image, no second view.
- **Model:** `glb/fig-31c_gilt-urn-stand.glb` (sha256 cd0eabceba4e…), 1,425,302 triangles, 0.7003 x 1.3 x 0.4866 m as built, not watertight. Claimed scale: height = 1.3 m, estimated.
- **Sheet:** `analysis/sheets/fig-31c_gilt-urn-stand.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Bell-topped urn on a flared three-footed pedestal with two bowls, as in the print. | — |
| Detail | matches | Gilt reliefs on the foot and the fluted bowls are kept. | — |
| Contamination | does not | A tall flat wall panel with chair details is fused behind the stand. | model |
| Unseen sides | does not | The back of the panel is a blank slab, so the object has no real back. | model |

**Good for as it stands:** a good front once the panel is deleted.

**Next experiments:** (1) Delete the fused panel in Blender and check what remains. (2) Regenerate from a crop with the background painted out.

### fig-31d_balloon-back-chair

- **Reference:** `Scans/images/fig-31_goods-for-home-decorative-furnishings.png`, crop `[1659, 1009, 2123, 1601]`, input `inputs/fig-31d_balloon-back-chair.png` (sha256 0067165b39e0…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a19-615a-76e3-861a-8223e9d96fb9` (ledger). One image, no second view.
- **Model:** `glb/fig-31d_balloon-back-chair.glb` (sha256 a8ddef5983bc…), 1,480,838 triangles, 0.6829 x 0.9 x 0.6625 m as built, not watertight. Claimed scale: height = 0.9 m, estimated.
- **Sheet:** `analysis/sheets/fig-31d_balloon-back-chair.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | Balloon back, shaped seat and cabriole legs match the print. | — |
| Parts | matches | The price card on the seat is carried over. | — |
| Contamination | does not | A flat backing board with part of a gilt frame is fused behind the chair. | model |
| Unseen sides | does not | The board's back is a blank brown slab. | model |

**Good for as it stands:** a good chair once the board is deleted.

**Next experiments:** (1) Delete the backing board and check the chair's rear legs. (2) Regenerate from a crop with the background painted out.

### fig-27_indian-elephant-howdah

- **Reference:** `Scans/images/fig-27_john-nash-indian-elephant-howdah.png`, crop `[680, 180, 1320, 1200]`, input `inputs/fig-27_indian-elephant-howdah.png` (sha256 ee186801686e…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a1995f-d7b5-7b61-97a7-0fa8a7776416` (ledger). One image, no second view.
- **Model:** `glb/fig-27_indian-elephant-howdah.glb` (sha256 4cdb21be1f78…), 1,485,910 triangles, 4.3404 x 5.0 x 3.4487 m as built, not watertight. Claimed scale: height = 5.0 m, estimated.
- **Sheet:** `analysis/sheets/fig-27_indian-elephant-howdah.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Parts | matches | Elephant, tusks, trunk, head cloth, tassels and the howdah platform are present. | — |
| Openness | does not | The howdah canopy is a solid helmet shape instead of an open arched canopy on slim pillars. | model |
| Contamination | does not | Two visitors from the crop are fused at the elephant's feet. | model |
| Detail | matches | The embroidered caparison and its cross panel are kept. | — |
| Unseen sides | cannot judge | The far side of the elephant and canopy are invented. | reference |

**Good for as it stands:** usable after rebuilding the canopy and removing the visitors.

**Next experiments:** (1) Rebuild the canopy by hand as an open frame. (2) Regenerate from a crop that cuts above the visitors.

## Starting mesh only

### fig-24b_boulder-pile

- **Reference:** `Scans/images/fig-24_raw-materials-west-entrance-crystal-palace.png`, crop `[791, 1192, 1569, 1652]`, input `inputs/fig-24b_boulder-pile.png` (sha256 5b9d719d8188…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a14-a90a-7ce0-9e30-f2d292272b16` (ledger). One image, no second view.
- **Model:** `glb/fig-24b_boulder-pile.glb` (sha256 7e4d5c5c8186…), 1,462,294 triangles, 3.4 x 1.5117 x 2.2354 m as built, not watertight. Claimed scale: max = 3.4 m, estimated.
- **Sheet:** `analysis/sheets/fig-24b_boulder-pile.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | partly | A heap of rough blocks, but boxier and flatter than the four big rounded boulders in the print. | model |
| Parts | does not | Block count and arrangement differ from the print. | model |
| Contamination | does not | A flat green slab and boxy slabs from the background are fused to the back of the heap. | model |
| Base and ground | does not | The heap stands on a flat brown disc. | model |

**Good for as it stands:** usable after deleting the slabs and the disc; not faithful to the arrangement.

**Next experiments:** (1) Delete the slabs and disc, then compare again. (2) Regenerate from a tighter crop of the pile alone.

### fig-31e_cast-iron-balustrade

- **Reference:** `Scans/images/fig-31_goods-for-home-decorative-furnishings.png`, crop `[673, 249, 1264, 835]`, input `inputs/fig-31e_cast-iron-balustrade.png` (sha256 de089b035dfe…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19a1b-478d-7592-acb3-70a01e387b5e` (ledger). One image, no second view.
- **Model:** `glb/fig-31e_cast-iron-balustrade.glb` (sha256 b5b4643034d8…), 1,438,604 triangles, 3.0 x 2.3804 x 2.233 m as built, not watertight. Claimed scale: max = 3.0 m, estimated.
- **Sheet:** `analysis/sheets/fig-31e_cast-iron-balustrade.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Detail and ornament | matches | The scrolled cartouche openwork on the diagonal front face is well kept. | — |
| Silhouette and proportion | does not | The model is a box: a wall block, a staircase wedge, a hat and gilt knobs are fused around a diagonal panel. | model |
| Scale | does not | The 3 m target is applied to the box, so the balustrade is smaller than stated. | model |
| Unseen sides | cannot judge | Thickness and back are invented. | reference |

**Good for as it stands:** the front face only; it needs manual isolation before any other use.

**Next experiments:** (1) Cut the diagonal panel out of the box in Blender. (2) The balustrade is a flat angled panel, which a single-image generator handles badly: model it by hand as a flat openwork panel.

### fig-33_model-working-class-home

- **Reference:** `Scans/images/fig-33_prince-albert-model-working-class-home-1851.png`, crop `whole image`, input `inputs/fig-33_model-working-class-home.png` (sha256 af37086a0f2f…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a1995f-f856-7b20-862a-edfc694d61f0` (ledger). One image, no second view.
- **Model:** `glb/fig-33_model-working-class-home.glb` (sha256 9c6b4d860841…), 1,389,300 triangles, 6.569 x 8.0 x 14.3959 m as built, not watertight. Claimed scale: height = 8.0 m, estimated.
- **Sheet:** `analysis/sheets/fig-33_model-working-class-home.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | partly | The facade with its central porch, gables and chimneys matches; the long side wings are plausible. | — |
| Contamination | does not | Flat grey cards float above the roof; visitors from the print are fused into the base. | model |
| Ground | partly | A raised stepped plinth appears where the print has a low wall and a gate. | model |
| Unseen sides | cannot judge | The rear and the sides are invented. | reference |

**Good for as it stands:** a starting mesh for the facade.

**Next experiments:** (1) Delete the floating cards and figures, then rebuild the base. (2) Regenerate with a second view of the building.

### fig-63_tower-conversion-design

- **Reference:** `Scans/images/fig-63_crystal-palace-conversion-tower-design.png`, crop `[0, 0, 1654, 2430]`, input `inputs/fig-63_tower-conversion-design.png` (sha256 a83214d6c836…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19964-37d8-7b51-9047-29ca442006a4` (ledger). One image, no second view.
- **Model:** `glb/fig-63_tower-conversion-design.glb` (sha256 4c9ed68a699d…), 1,473,281 triangles, 183.6856 x 304.8 x 130.3127 m as built, not watertight. Claimed scale: height = 304.8 m, printed design height of 1000 feet (catalog).
- **Sheet:** `analysis/sheets/fig-63_tower-conversion-design.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | matches | The shaft with its stacked tiers, clock stage and flag matches the engraving. | — |
| Detail | partly | Tier divisions are kept; the arched building at the foot is reduced to a small block. | model |
| Contamination | does not | The ground and trees are baked into a flat white slab at the base. | model |
| Scale | cannot judge | 304.8 m comes from the printed 1000 ft and is the one scale here with a basis. | comparison |

**Good for as it stands:** a starting mesh for the shaft, once the slab is deleted.

**Next experiments:** (1) Delete the slab and rebuild the base as the Crystal Palace nave end. (2) Check the tier count against the engraving.

### fig-73_centenary-model

- **Reference:** `Scans/images/fig-73_crystal-palace-centenary-model-festival-of-britain-1951.png`, crop `whole image`, input `inputs/fig-73_centenary-model.png` (sha256 361f46dd6a71…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19965-cf86-75c0-aa9c-ef29f3bfaa9d` (ledger). One image, no second view.
- **Model:** `glb/fig-73_centenary-model.glb` (sha256 3bf22ef82d73…), 1,397,789 triangles, 3.3984 x 2.1204 x 6.0 m as built, not watertight. Claimed scale: max = 6.0 m, estimated.
- **Sheet:** `analysis/sheets/fig-73_centenary-model.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | partly | A barrel-vault canopy over a raised platform with balustrade is the right idea. | — |
| Openness | does not | The glazed vault and the open ironwork come out solid and muddy. | model |
| Contamination | does not | Visitors are fused inside and an extra building mass sits behind. | model |
| Scale | cannot judge | The 6 m depth is an estimate; the dimensions are driven by the extra mass. | comparison |

**Good for as it stands:** a starting mesh for the vault and platform; not for the glazing.

**Next experiments:** (1) Rebuild the vault ribs and glazing by hand. (2) Regenerate from a crop without the visitors.

## Does not reproduce its reference

### fig-72_brompton-boilers

- **Reference:** `Scans/images/fig-72_brompton-boilers-south-kensington-exhibition-1862.png`, crop `whole image`, input `inputs/fig-72_brompton-boilers.png` (sha256 d036ca9d3004…).
- **Made by:** Tripo H3.1 through fal.ai, request `01a19964-d6a8-7082-a8d5-9776c6923a4c` (ledger). One image, no second view.
- **Model:** `glb/fig-72_brompton-boilers.glb` (sha256 b5851bc4cccd…), 1,405,977 triangles, 116.6901 x 53.8906 x 150.0 m as built, not watertight. Claimed scale: max = 150.0 m, estimated.
- **Sheet:** `analysis/sheets/fig-72_brompton-boilers.jpg`.

| Criterion | Verdict | What is visible | Cause |
|---|---|---|---|
| Silhouette and proportion | does not | A very long arcaded building collapses into a compact L-shaped mass. | reference |
| Parts | partly | Two domes and an arcaded front are present, but the dome count and the arcade rhythm differ. | model |
| Contamination | does not | A flat brown billboard slab is fused behind the domes. | model |
| Unseen sides | does not | The plan behind the facade is entirely invented. | reference |

**Good for as it stands:** not usable as a likeness; proportions are wrong.

**Next experiments:** (1) Build the facade by hand from the print's bay rhythm. (2) Do not feed an oblique view of a long building to a single-image generator.

## What the failures have in common

Every failure that cost likeness came from one of three causes. (1) The crop was not clean: walls, boards, curtains, figures and ground planes were fused into the mesh (fig 24b, 27, 31a-e, 33, 63, 72). (2) Open structure came out solid (the elephant canopy, the Centenary vault). (3) The reference could not support the claim: a long building seen at an angle (fig 72) and the back of every object. The successes (3, 52, 54, the vase, the obelisk shaft) were isolated objects against a plain or dark ground. So the cheapest improvement is upstream: paint the background out of the crop, or give the generator a second view, before generating. Triangle count and file size were no help: all 16 are about 1.4 million triangles and none is watertight.

## Limits

Judgments are the analyst's, read from rendered stills. Colour is not judged where the reference is a monochrome print or a hand-coloured plate. Hidden sides are called invention and are not scored. No likeness metric was computed: silhouette overlap and image similarity are unreliable across perspective, and the height-to-width ratios in `facts/` are a rough check only (a model with fused background or a different crop has a different ratio for reasons that are not the likeness).
