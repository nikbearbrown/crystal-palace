# NOTES — scan-fig71-blotting-book (Muse version)

**Subject.** Crystal Palace souvenir blotting-book cover, as photographed in
fig-71 of the Scans catalog: a desk blotting book whose cover is inset with a
painted-glass view of the Palace over silver foil, surrounded by gold vine
ornament (original in the Museum of London, per the catalog caption). This
package is the Muse version of the subject, built for the Crystal Palace
film project.

**What was modelled**
- The closed book as a low slab: cream page block beneath a dark leather
  cover board (the reference shows the decorated cover face only).
- On the cover: a thin red pinstripe inset border; a gilt vine border —
  stem loop with spiral curls at the corners and edge midpoints and small
  leaf shapes along it (procedural, simplified from the dense painted vine
  in the photograph).
- Central panel in a gilt frame: dark blue-green "painted glass" ground
  with the Palace as a flat silver-foil silhouette (stepped nave wings and
  arched transept, as in the painted view), gilt tracery lines and arch
  arcs on the silhouette, and the two great elms enclosed in the transept
  as dark silhouette shapes in front of it.

**Scale.** Desk scale, ESTIMATED: cover 0.35 × 0.26 m, overall thickness
~0.015 m. The photograph carries no scale reference; the size is a typical
blotting-book format and all internal proportions follow the image.

**Assumptions and unseen sides.**
- Only the cover face is visible in the source. The page block, underside
  and spine are plain interpretation; the real object's edges are slightly
  rounded/irregular (noted in the catalog) and are modelled as a clean
  rectangle.
- The painted palace view is deliberately abstracted to flat shapes; the
  original is a detailed miniature painting under glass.
- The gilt vine is a simplified procedural motif, not a tracing of the
  painted ornament.

**Counts / QC.** 10,360 triangles (Model collection, evaluated). Preview
rendered from above at an angle comparable to the reference photograph,
neutral grey backdrop, Cycles CPU, 48 samples + denoise. QC fixes during
the build: the panel design initially read upside-down from the first
camera side (camera moved to the −Y side so the palace reads upright), and
the vine leaves were scattered by a transform-apply pitfall (object
origins baked to the world origin) — rebuilt with plain object transforms
and re-verified in the final preview.

**Files.** `scan-fig71-blotting-book.blend`, `scan-fig71-blotting-book.glb`,
`preview.png`, `build_scan_fig71_blotting_book.py` (re-runnable).

**Manual review.** Recommended: (1) scale is estimated — check against the
Museum of London object's published dimensions before hero use; (2) the
painted-glass palace is an abstraction — a texture-based treatment would
be needed for close-ups.
