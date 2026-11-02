# scan-fig69-fire-1936 — Muse version

**Muse version** (ships as `scan-fig69-fire-1936-muse`).

## Subject
Night photograph of the Crystal Palace fire (catalog fig. 69, scan IMG_6429): the burning Sydenham palace seen from the park side. Modelled as a night vignette following the photograph's layout: the transept's arched end at screen-left with clustered stylised flames inside the arch against a glowing end wall, the nave's barrel roof and glowing arcaded side wall receding to the right, Brunel's south water tower standing intact and fire-lit at centre-right, a turntable ladder raised at screen-right with a water jet directed at the building and three firemen silhouettes at its base, a lit lamp post, foreground park railings with a gate, and a bare winter tree at screen-left.

## Date caveat (from the catalog)
The printed caption reads "The fire, 20 November 1936"; the catalog flags this date as **transcribed as printed and not independently verified**. The Crystal Palace fire is historically dated **30 November 1936**. The model follows the photograph, not the caption date.

## Scale
Vignette ~26 m wide (building excerpt); water tower ~15 m as modelled. **Scale estimated** — the real transept and tower were far larger; this is a compressed excerpt of the photographed composition, not a measured reconstruction.

## Assumptions / interpretation
- Flames are deliberately abstract: layered emissive-orange cones clustered inside the transept, along the nave wall top and at ground level — a tasteful stylisation, not a fire simulation. Smoke is suggested by a few dark translucent volumes above the roof.
- The photograph is monochrome and dominated by glare; colours (ember orange glow, near-black night) are interpretive.
- Only one viewpoint exists: rear and side elevations of the excerpt are plain interpretation; the building continues beyond the frame in reality.
- The water jet is a single translucent tapered stream, as the photograph shows one jet clearly.

## Technical
- Triangles: **9,204**. Blender 4.5.3, metres, origin at base centre, scale applied.
- Files: `scan-fig69-fire-1936.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, night view comparable to the photograph), re-runnable `build_scan_fig69_fire_1936.py`.

## QC
Preview checked against the photograph over four iterations: camera pulled back to compose the whole vignette; flame clusters rebuilt twice (oversized roof flames that read as floating bells were replaced by interior/ground/wall-top clusters on visible bases); fire-light levels rebalanced so the ironwork silhouettes against the glow and the tower reads as fire-lit, as in the photograph. Handedness verified: transept screen-left, ladder screen-right.
- Fix round (exposure/framing, audit-driven): the first shipped preview was too dark to audit — over half the frame was pure black and the tower/nave were barely readable. Lighting/framing only, no geometry change (triangles unchanged at 9,204): world background and backdrop lifted from near-black to very dark grey, ground tone warmed/lifted, fire point lights roughly doubled (main 1200→2400, nave 650→1300, tower 650→1100), cool moon fill 0.25→0.55, view exposure +0.3, and the camera moved closer with a slightly longer lens so the vignette fills the frame. Flames and the glowing end wall remain the brightest elements; every element named above (transept arch + mullions, flame clusters, nave ribs and glowing wall, tower with windows/belt/arcaded top, ladder + water jet, three firemen, lamp post, railings + gate, bare tree, smoke) is now identifiable in the preview while the night mood is kept.

## Manual-review items
- Flame shapes are cone abstractions; for hero shots replace with volumetrics or sprite flames.
- The excerpt's proportions are compressed relative to the real building — do not use for dimensional reference.
