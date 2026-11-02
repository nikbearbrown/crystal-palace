# scan-fig70-fire-remains — Muse version

**Muse version** (ships as `scan-fig70-fire-remains-muse`).

## Subject
Daylight photograph of the Crystal Palace remains after the 1936 fire (catalog fig. 70, scan IMG_6429). Modelled as a wreckage vignette following the photograph: a rubble field of flattened mounds, angular chunks, scattered twisted beams and bent plates in the foreground; charred standing columns (one tall pale column with its capital at screen-left foreground); a leaning girder ramp at centre; a skeletal iron framework with two tall masts at mid-right; bent collapsed arch ribs at screen-right; the surviving transept barrel-vault skeleton at back-left with a dark hollow far end; and Brunel's north water tower standing intact in the centre background — **the tower is visible in this photograph**, so it is included.

## Scale
Vignette ~24 m wide. **Scale estimated** — a compressed excerpt of a much larger ruin field; column and tower heights are proportioned from the photograph, not measured.

## Assumptions / interpretation
- Somber grey palette throughout, matching the monochrome photograph; rust tints on some ironwork are a restrained interpretation (the photograph gives no colour).
- Rubble is procedural (randomised mounds, chunks and beams, seed-fixed) — it evokes the debris field; it does not reproduce individual pieces of wreckage.
- The vault skeleton repeats five ribs as an excerpt of the barrel; the real ruin continued well beyond the frame.
- Single viewpoint: the arrangement behind the foreground wreckage is interpretation.

## Technical
- Triangles: **18,132**. Blender 4.5.3, metres, origin at base centre, scale applied.
- Files: `scan-fig70-fire-remains.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, view across the wreckage comparable to the photograph), re-runnable `build_scan_fig70_fire_remains.py`.

## QC
Preview checked against the photograph over three iterations: camera widened so the whole composition (vault left, tower centre, frame right, rubble foreground) reads as in the photograph; rubble rebuilt from smooth uniform mounds into a mixed angular debris field; an early "distant tree line" of blobs was removed as unconvincing (the photograph's background is plain haze); ground plane extended so the wreckage runs to the frame edges.

## Manual-review items
- Individual twisted-girder shapes are generic; a hero foreground would need hand-modelled wreckage.
- The dark far-end panel of the vault is a flat tonal device for the photograph's dark hollow.
