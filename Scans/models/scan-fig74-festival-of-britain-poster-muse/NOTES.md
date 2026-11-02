# NOTES — scan-fig74-festival-of-britain-poster (Muse version)

**Subject.** The official Festival of Britain poster, 1951 (Abram Games
design), as reproduced in fig-74 of the Scans catalog. Modelled as a
physical poster sheet pinned on a plain mounting board, with the printed
design rebuilt as bold flat shapes. This package is the Muse version of
the subject, built for the Crystal Palace film project.

**What was modelled** (all design elements as flat raised shapes on the
blue sheet, laid out as printed):
- Deep-blue poster sheet (1.00 × 1.50 m) on a simple board.
- Blank pale blocks at top left and right where the years "1851" and
  "1951" are printed — the numerals are lettering and are NOT reproduced.
- Two sagging strings of red/white/blue pennant bunting across the top.
- The Festival emblem abstracted: red compass star, pale disc, and the
  Britannia profile head as a flat silhouette facing left, as printed
  (no facial detail; it is a graphic motif, not a portrait).
- The red-and-white striped banner element printed at the left of the map.
- A pale silhouette map of Britain, drawn from simplified coastal
  lon/lat points.
- The dark navy bottom band carrying two blank pale strips where the
  title "FESTIVAL OF BRITAIN" and the dates "MAY 3 – SEPTEMBER 30" are
  printed — lettering NOT reproduced, bands left blank deliberately.

**Scale.** Sheet 1.00 × 1.50 m — a standard large poster format,
ESTIMATED from the design's known format class; the scan carries no scale
reference.

**Assumptions and unseen sides.**
- The poster is modelled flat on a board; the original's paper texture,
  print registration and exact colour values are approximated.
- REPAIR NOTE: this scan has a repaired area — a narrow strip of blue
  sea/background along the torn right edge (modern infill, ~0.9% of
  pixels, per catalog.json). That strip is plain background in the design;
  the model treats it as ordinary blue ground and does NOT use the
  repaired pixels as evidence for any design detail.
- The emblem is a deliberate abstraction: in the original, the Britannia
  head carries striped/flag detail in the hair, which is simplified away
  here; the map outline is a simplified coastline, not a cartographic
  reproduction.

**Counts / QC.** 1,648 triangles (Model collection, evaluated). Preview
rendered near-frontally, comparable to the flat reference reproduction,
neutral grey backdrop, Cycles CPU, 48 samples + denoise. QC fixes during
the build: the first preview mirrored the design (the +Y camera shows
world +X on the left) — all design coordinates are now defined in image
space and negated into world space, verified against the reference (1851
block left, banner left of the map, Britannia facing left); a coplanar
overlap between the map and banner caused z-fighting artifacts — the
banner was shifted clear and given more relief.

**Files.** `scan-fig74-festival-of-britain-poster.blend`,
`scan-fig74-festival-of-britain-poster.glb`, `preview.png`,
`build_scan_fig74_festival_poster.py` (re-runnable).

**Manual review.** Recommended: (1) emblem treatment is abstract — swap
in a textured print if the poster is ever seen at close range; (2) poster
sheet dimensions are an estimated format, not measured from the scan.
