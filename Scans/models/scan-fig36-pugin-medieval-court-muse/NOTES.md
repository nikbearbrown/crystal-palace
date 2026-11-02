# NOTES — scan-fig36-pugin-medieval-court (Muse version)

## Subject

A composed single bay (~7 m wide) of **Pugin's Medieval Court** at the Great Exhibition of 1851, modelled from the fig-36 colour view: a red-and-gold draped canopy/tester over an altar-like display on a raised red-carpeted platform at centre; a pale stone Gothic screen with a statue niche and a black candelabrum at left; a pale pierced Gothic screen at right against dark blue wall panels and red hangings; a hanging gilt corona; and a pyramid-topped glass display case with silver/gilt plate in the right foreground, with three stylised visitors in period dress.

This is the Muse version of the model for this catalog entry.

## Scale — ESTIMATED

- **Basis:** the visitor figures in the colour view, taken as ~1.65–1.75 m tall. All exhibit heights were proportioned against them.
- Modelled figures: women ≈ 1.65 m (head top), man ≈ 1.75 m body / ≈ 1.88 m including top hat.
- Resulting key dimensions: bay floor 7.4 m wide × 5.2 m deep; canopy tester top ≈ 3.32 m above the platform (platform top 0.22 m); left screen ≈ 3.35 m to cornice / ≈ 3.9 m to pinnacle tips; right pierced screen ≈ 3.3 m / ≈ 3.75 m to finial tips; corona ring Ø ≈ 1.04 m hung with its ring at ≈ 3.30 m; glass case table top 0.78 m, glass apex ≈ 1.63 m.
- No dimension is confirmed by a measured source; treat all as estimated to roughly ±15%.

## Assumptions and interpretations

- **Single view:** the reference is one colour view. Backs, tops and unseen sides of the canopy, screens and case are reasonable historical interpretations, never confirmed fact. The canopy is completed as a four-post tester with fabric on back and part-sides; the screens are given plain backs.
- **Statue (left niche):** the robed figure in the view reads as a Virgin-and-Child-like exhibit statue. It is modelled as a simplified stone form (cone robe, veil, small child form) — an exhibit object, not a devotional reconstruction; no face, no likeness, no attributes beyond the held child form.
- **Openwork (right screen):** the delicate pierced Gothic openwork of the view is approximated with solid pale panels carrying dark recessed quatrefoil discs and pointed-arch top lights, plus pinnacles/finials. It reads as pierced work at viewing distance but is not true through-cut tracery.
- **Fabric pattern:** the red hangings carry a procedural repeating sun/flower motif generated in the build script (gold discs with petal rings on deep red). It is a generic repeat suggesting the patterned fabric in the view — **no heraldry, no text, no inscriptions, no copied specific motif**.
- **Angel candlesticks:** the two small angel figures on the front prickets are simplified gilt forms (cone robe, head, two wing slabs).
- **Altar plate / case plate:** chalices, ewer, dishes and the clock in the glass case are simplified vessel forms (lathe-like stacks of cones/cylinders); the clock face is blank — no numerals or hands are inscribed.
- **Visitors:** three stylised simplified figures in period dress (tiered crinoline dress + white bonnet; top hat + tailcoat; burgundy crinoline + bonnet), no likenesses, no facial features. The burgundy-dress figure at right is an interpretation completing the visitor group visible at the edges of the view.
- **Corona chains** run to a single ceiling boss point above the ring, as hung in the view; no ceiling structure is modelled.
- **Floor** is a single dark-wood boarded slab with groove lines, extending beyond the exhibits as the court floor; the dark blue back wall is the court backdrop, not the Crystal Palace structure itself (the building's iron-and-glass shell is outside the scope of this composed bay).

## Build / technical

- Script: `build_scan_fig36_pugin_medieval_court.py` (re-runnable, Blender 4.5.3, `bpy` only).
- Units: metres. Origin at base centre (floor centre, z = 0 at floor underside / 0.03 at walking surface). Scale applied on all meshes.
- **Triangle count: 23,568** (evaluated count printed by the build; was 21,860 before Fix round 1, still well under the 50k budget).
- Preview: `preview.png`, Cycles CPU, 960 × 720, neutral grey background, three-quarter view from front-right with the canopy at centre, statue screen left and glass case right foreground, comparable to the reference view. (32 samples with adaptive sampling — the shared VM was heavily loaded by parallel batch builds.)

## QC

- Preview viewed against the reference before finishing (three build iterations): composition matches the view — draped red-gold canopy centre with altar, cross, plate and angel prickets; statue visible in its purple-draped niche in the left stone screen with the black candelabrum and flower table in front; corona with candles and chains top-left of centre; pierced pale screen right with the red hanging behind it; pyramid glass case with clock and plate in the right foreground; three visitors at plausible scale against the exhibits. Palette checked: deep red + gold fabric, dark blue wall with gilt panel frames, pale stone, dark wood floor, burgundy/cream/black period dress. Defects found in earlier iterations and fixed: back wall initially built flat (axis error), statue initially embedded in the solid screen block (screen rebuilt around an open niche), wall panel trims initially hid the blue panels (moved behind as gilt borders), burgundy dress and black coat initially rendered pink/grey (linear-space values deepened), candelabrum arms and case edges rebuilt as point-to-point struts, glass alpha reduced so the plate inside reads through the pyramid.
- **Fix round 1 (figures) — 2026-11-01:** figures-only fix per parent audit; scene, composition, palette, camera and all exhibits unchanged. (1) The man (centre, top hat) was a grey rectangular slab — rebuilt at the same low-poly level with a period silhouette: torso frustum tapering from broad shoulders to a narrow waist with a rounded shoulder cap, an elliptical coat-skirt frustum flaring from the waist to about the knee, slim tails behind, tapered trouser legs and shoes below the skirt, simple strut arms with small hands, white shirt front, faceless head and the original top hat kept (overall height unchanged, ≈1.88 m incl. hat). (2) Both women (cream left, burgundy right) were smooth cones — each dress rebuilt as 3 stepped tiers of stacked cone frustums, each upper tier stepping in but flaring out over the top of the tier below so the steps read as the tiered flounces that dominate the reference, plus a tapered bodice (waist 0.15 m → 0.105 m at the neck) with a small shoulder cap and the existing bonnet kept; still faceless/stylised, overall height unchanged (≈1.65 m). Changes were made in `woman()` / `man_tophat()` in the build script only; .blend, .glb and preview.png regenerated with the same camera. Preview re-viewed, including zoomed crops of all three figures: tiers read clearly on both dresses, the man's coat/waist/legs silhouette reads as period dress, and everything else in the frame is identical to the pre-fix preview. One defect found in the first fix render and corrected before finishing: the women's heads floated ~5 cm above the bodice (neck too short for the new bodice) — neck lengthened to overlap bodice and head, re-rendered and re-checked. Triangle count 21,860 → **23,568** (budget <50k).
- Files present: build script, .blend, .glb, preview.png, refs/ (source image copy + REFERENCES.md), NOTES.md.
- Not pushed to GitHub — staged locally only, per task instruction.

## Manual-review items

1. Statue simplification — confirm the abstract stone Virgin-and-Child form is acceptable as an exhibit statue.
2. Pierced-screen approximation — dark-disc openwork instead of true cut tracery; check it reads correctly at film distance.
3. Fabric motif density/colour against the reference hanging (procedural, adjustable via the script's tile size and mapping scale).
4. Overall bay width and canopy height rest on the estimated visitor-based scale — no measured source exists in the catalog entry.
5. The right-hand visitor in burgundy is partly an interpretation (edge-of-frame figure in the view).
