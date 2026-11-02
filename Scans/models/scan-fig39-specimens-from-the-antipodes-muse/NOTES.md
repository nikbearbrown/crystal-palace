# NOTES — scan-fig39-specimens-from-the-antipodes (Muse version)

## Subject

The Punch cartoon **"Specimens from Mr. Punch's Industrial Exhibition of 1850 (To be improved in 1851)"** (*Punch*, 13 April 1851), modelled as a stage vignette: a row of three arched, glass-fronted display alcoves against a dark interior wall, each holding a working person exhibited like a museum specimen — a seated **needlewoman** sewing (left), a bent elderly **labourer** in a pointed nightcap working with a flail-like hand tool (centre), and a **shoemaker** seated on the floor of his case at a low bench with shoe forms (right). A blank placard hangs in each case. In front of the cases stand two top-hatted gentlemen viewers: one tall and thin, hand raised to his chin, and one portly, with a cream waistcoat, watch chain and cane.

This is the Muse version of the model for this catalog entry; it ships as `scan-fig39-specimens-from-the-antipodes-muse`. (The slug preserves the batch's working name; the catalog and the image itself title the cartoon "Specimens from Mr. Punch's Industrial Exhibition" — see refs/REFERENCES.md.)

## Scale — ESTIMATED

- **Basis:** the figures in the cartoon, taken as period-average heights. Modelled: tall gentleman ≈ 1.85 m (plus top hat), portly gentleman ≈ 1.70 m, labourer ≈ 1.66 m.
- Resulting key dimensions: each alcove ≈ 2.06 m wide, ≈ 2.9 m to the arch crown, ≈ 0.9 m deep; overall vignette 7.2 m × 3.4 m.
- No dimension is confirmed by a measured source; treat all as estimated.

## Assumptions and interpretations

- **Single view:** the reference is one engraved cartoon. Case backs/interiors beyond the front view and all unseen sides are reasonable interpretations, never confirmed fact.
- **Blank placards:** the print lettered each case ("An industrious needle-woman", "A labourer aged 75", "A distressed shoemaker", "A sweater"). No lettering is reproduced anywhere in the model; the placards are blank boards and the satire is carried by the glass cases themselves.
- **No caricature exaggeration:** the workers are dignified stylised figures — faceless, simplified period dress (smock, nightcap, shirtsleeves) — and the gentlemen keep only the drawn contrast of build.
- The print shows the cases as curved glass alcoves; the model approximates them with a flat arched glass front plus glazed side returns.
- The labourer's tool is read as a flail-type hand tool, as drawn; the shoemaker's bench forms are generic shoe lasts.
- The dark back wall stands for the print's hatched interior; no other room architecture is shown or modelled.

## Build / technical

- Script: `build_scan_fig39_specimens_from_the_antipodes.py` (re-runnable, Blender 4.5.3, `bpy` only).
- Units: metres. Origin at base centre (floor centre, z = 0 at walking surface). Scale applied on all meshes.
- **Triangle count: 13,280** (evaluated count printed by the build; well under the 50k budget).
- Preview: `preview.png`, Cycles CPU, 960 × 760, neutral grey background, frontal three-quarter view of the three cases with the two gentlemen in front, comparable to the reference.

## QC

- Preview viewed against the reference before finishing (two build iterations): the final view shows the three arched glass cases in a row with blank placards, the needlewoman sewing at left, the nightcapped labourer bent at centre, the shoemaker at his bench at right, and the two gentlemen standing before the cases, as drawn. Defects found in the first iteration and fixed: the arch fronts were first built as solid panels that hid the interiors entirely — rebuilt as open frames (jambs plus arc segments) over clearer glass; the labourer and shoemaker were moved deeper into their cases so hands and tools stay behind the glass; dim warm lights were added inside the cases so the workers read through the glass. Remaining known nits: the case glass renders slightly milky, softening the interiors (acceptable — it reads as glass); the shoemaker sits low and small in his case, as he does in the print.

## Manual-review items

1. Case-label texts are deliberately blank (no-lettering rule); confirm the vignette still reads as the "Specimens" satire without them.
2. The labourer's exact tool and the shoemaker's posture are interpretive readings of the engraving.
3. Overall scale rests on estimated figure heights — no measured source exists in the catalog entry; the catalog also flags this entry as review-recommended because its book caption is partly outside the source photograph.
