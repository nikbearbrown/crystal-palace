# NOTES — scan-fig46-pound-and-a-shilling (Muse version)

## Subject

John Leech's Punch cartoon **"The Pound and the Shilling"** (*Punch*, 14 June 1851; the book caption reads "The classes and the masses"), modelled as a small stage vignette: at left, the "Pound" — a tall, portly gentleman in top hat and tailcoat, carpet bag at his feet and umbrella in hand, leaning forward with his hand out in greeting, his bonneted wife with a parasol beside him; at right, the "Shilling" — a rustic labourer in smock and wideawake hat, long staff in hand, leaning back in surprise, with his wife (bonnet, shawl and apron, baby in her arms) and their small daughter. Behind them, an exhibition column, a draped statue on a pedestal, and a row of onlookers' heads above a barrier and hoarding, as drawn.

This is the Muse version of the model for this catalog entry; it ships as `scan-fig46-pound-and-a-shilling-muse`.

## Scale — ESTIMATED

- **Basis:** the adult figures in the cartoon, taken as period-average heights. Modelled: gentleman ≈ 1.86 m (plus top hat), his wife ≈ 1.60 m, labourer ≈ 1.72 m, his wife ≈ 1.58 m, daughter ≈ 1.02 m.
- Resulting key dimensions: floor vignette 6.4 m × 3.6 m; column ≈ 3.6 m to capital (a partial column, cut at frame height as in the print); statue on pedestal ≈ 3.0 m overall.
- No dimension is confirmed by a measured source; treat all as estimated.

## Assumptions and interpretations

- **Single view:** the reference is one engraved cartoon. Backs and unseen sides of all figures and props are reasonable interpretations, never confirmed fact.
- **No caricature exaggeration:** the print's humour rests on the contrast between the two families. The figures keep the drawn contrast of build and dress (portly vs slight, tailcoat vs smock) but are dignified stylised forms — no facial features, no likenesses, no exaggerated features.
- **No lettering:** nothing in the scene carries text; the print's caption is not reproduced.
- The background crowd is reduced to five busts above a hoarding board, standing for the heads massed behind the barrier in the print.
- The statue on its pedestal is a simplified draped stone form (an exhibit), with no carved detail.
- The gentleman's greeting hand and the labourer's raised hand nearly meet at the centre — the drawn meeting point of the two groups is preserved, with a small gap as in the print.

## Build / technical

- Script: `build_scan_fig46_pound_and_a_shilling.py` (re-runnable, Blender 4.5.3, `bpy` only).
- Units: metres. Origin at base centre (floor centre, z = 0 at walking surface). Scale applied on all meshes.
- **Triangle count: 21,900** (evaluated count printed by the build; well under the 50k budget).
- Preview: `preview.png`, Cycles CPU, 800 × 1024 (portrait, matching the print), neutral grey background, frontal view of the two groups with the meeting of hands at centre, comparable to the reference.

## QC

- Preview viewed against the reference before finishing (three build iterations): the final framing holds all five principal figures — the portly gentleman centre-left with his hand out in greeting, carpet bag and folded umbrella at his side, his wife in lilac with parasol behind him; the labourer centre-right leaning on his long staff with one hand raised in surprise, his wife with shawl, apron and baby, and their daughter at far right; crowd busts above the hoarding and the draped statue behind, as drawn. Two defects were found and fixed during the iterations: (1) in the shared figure builder the men's torso group was missing its hip-height offset, burying heads and arms inside the coat skirt — fixed in the builder and all batch-8 models rebuilt; (2) the first framing cropped the outer figures — camera pulled back to the full group. Remaining known nits: the exhibition column at right is at the very edge of the preview frame, and the wife's parasol canopy passes behind the gentleman's hat from this angle (it is correctly placed over her own head in the model).

## Manual-review items

1. Figure proportions and the greeting gap are interpretive readings of a satirical drawing; check they read as intended at film distance.
2. The background crowd is a deliberate reduction (five busts) of the print's packed heads.
3. Overall scale rests on estimated figure heights — no measured source exists in the catalog entry.
