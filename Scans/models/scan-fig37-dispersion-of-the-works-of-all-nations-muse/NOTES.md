# NOTES — scan-fig37-dispersion-of-the-works-of-all-nations (Muse version)

## Subject

George Cruikshank's satirical print **"The Dispersion of the Works of All Nations from the Great Exhibition of 1851"**, modelled as a wide stage vignette: a simplified **Crystal Palace** at centre-back — glazed nave with arched windows and a shallow barrel-vault roof, a raised central **transept** with a great arch and its own vault, a tall tower and a chimney behind the roof, and a blank banner board across the roof front — with the exhibits scattering outward in every direction as drawn: a **locomotive** with tender, a **horse-drawn carriage**, a **boat** and a **two-masted ship** under sail, a **great fish**, a **polar bear**, a **globe** on its stand, a sofa, chair, table and chest of drawers, a **cannon**, a red-and-white striped **lighthouse**, a draped **statue** on a pedestal, a great gilt **urn**, barrels and crates — and twelve visitors streaming away among them, some carrying bundles and portmanteaus.

This is the Muse version of the model for this catalog entry; it ships as `scan-fig37-dispersion-of-the-works-of-all-nations-muse`.

## Scale — ESTIMATED

- **Basis:** the visitor figures, taken as ≈ 1.6–1.75 m. The print is a deliberate fantasy — its palace is barely larger than its exhibits — so the model follows the print's own relative scale rather than the real building's.
- Resulting key dimensions: stage 13.0 m × 7.0 m; palace block ≈ 8.8 m wide, transept arch crown ≈ 4.3 m, tower ≈ 7.0 m; locomotive ≈ 4.9 m over engine and tender; lighthouse ≈ 2.9 m.
- No dimension is confirmed by a measured source; treat all as estimated. This model must not be used as evidence for the real Crystal Palace's dimensions.

## Assumptions and interpretations

- **Single view:** the reference is one satirical engraving. Backs and unseen sides of every object are reasonable interpretations, never confirmed fact.
- **Flight on struts:** in the print the dispersing objects fly unsupported through the air. In the model the boat, ship, fish and urn are carried on slim dark display struts — a staging device so the composition stands as a physical model; it is not part of the depicted scene and is flagged here.
- **Blank banner:** the print letters its roof banner; the model's board is blank — no lettering anywhere.
- **Selection:** the print contains dozens of further objects, animals and figures in its margins. The model includes the large, legible items listed above; the smallest background clutter is omitted, and the crowd is reduced to twelve visitors.
- The palace is a deliberate miniature "hint" (flat glazed facade, two vault hints), not an architectural model of the building.
- The globe's continents are four abstract land patches, not a map; the statue is a simplified draped stone form; the polar bear and horse are simplified animal forms with no anatomical detail.

## Build / technical

- Script: `build_scan_fig37_dispersion_of_the_works_of_all_nations.py` (re-runnable, Blender 4.5.3, `bpy` only).
- Units: metres. Origin at base centre (floor centre, z = 0 at walking surface). Scale applied on all meshes.
- **Triangle count: 44,212** (evaluated count printed by the build; budget 50k).
- Preview: `preview.png`, Cycles CPU, 960 × 690, neutral grey background, frontal three-quarter view of the palace with the exhibits dispersing toward the viewer, comparable to the reference.

## QC

- Preview viewed against the reference before finishing (two build iterations): the final view matches the print's scheme — palace centre-back with glazed vaults, transept arch and blank roof banner, and the exhibits radiating outward (locomotive, carriage, boats, fish, globe, furniture, cannon, lighthouse, statue, urn, barrels, crates) with visitors streaming among them. Defects found in the first iteration and fixed: the locomotive's tender overhung the stage edge (train moved inboard); the tower was given a warmer, darker stone so it separates from the grey background; the carriage was turned slightly to present the horse more broadside. Remaining known nits: the glass vaults render milky and merge into one another (they read as a glasshouse mass rather than two distinct roofs); the horse reads weakly from the preview angle — its ellipsoid body merges visually with the cannon wheel behind it, though the full horse (neck, head, ears, legs, tail) is in the model; the polar bear is partly occluded by the locomotive from this angle.

## Manual-review items

1. The strut-supported "flight" is the model's largest departure from the print; confirm the staging device is acceptable, or re-pose the elevated pieces on the floor.
2. Exhibit selection omits the print's marginal clutter; check nothing essential to the gag is missing.
3. All dimensions are read from a satirical print and are estimated throughout — the catalog entry itself offers no measurements.
