# NOTES — Renaissance arch fragment (Italian/Renaissance Court loggia bay)

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 3, item 13 —
the second of the item's pair of court fragments; the Gothic
fragment, `sy-gothic-arch-fragment`, is the first).
Scenes: CP038 / CP040 (a dressing module for the Renaissance Court,
not a room).
**Sydenham 1854 only** — no Hyde Park evidence is used in this model.

## The interpretation caveat (read first)

**This is a Victorian reproduction, not Renaissance building.** The
Italian (Renaissance) Court was one of the Fine Arts Courts built at
Sydenham in 1854 under the direction of Matthew Digby Wyatt — a
didactic, plaster-and-timber arrangement of copies after Renaissance
originals, made in south London. The 1856 guide is explicit about the
assemblage: the court's nave entrance is "a restored copy of a
portion of the Hôtel Bourgtheroulde, at Rouen", and its back wall is
a gathering of copied exhibits — compositions from the Certosa di
Pavia, doors by Jean Goujon, a doorway from the Doria Palace, the
monument of Ilaria di Caretto. The loggia arcade modelled here is the
court's own architecture as photographed, not a documented
Renaissance prototype — **the guide names no prototype for the
arcade itself** in the pages consulted (pp.95–99), so the bay is
modelled from the photograph and must not be presented in the film
as an Italian Renaissance building.

## What it is

One repeatable bay of the court's loggia arcade, spanning
**pier-centre to pier-centre**: a semicircular arch on piers, each
pier carrying an applied **Ionic pilaster** whose capital — necking,
echinus flare, bolster and a pair of volutes — rises well past the
arch springing to a full **entablature** (two-fascia architrave,
carved frieze, cornice) with a plain panelled **attic course** above
(the base of the upper gallery wall). Moulded **impost blocks** mark
the springings; a **patera roundel** (ring + boss) sits in each
spandrel flanking the pilaster at capital height; the pilaster
shafts carry a shallow panel frame. That is the stack the
stereograph of the court shows, bay after bay.

The end piers are **half piers carrying half pilasters**, cut at
the module edges (x = ±1.90 m): copies placed side by side at the
3.80 m pitch compose full piers with full Ionic pilasters (both
volutes, the full bolster), and the entablature bands continue
(verified in the tiled render — see QC). A single module also
stands alone as a clean cut fragment.

Origin at the base centre of the bay's footprint, ground z = 0.
Units: metres. Blender 4.5.3.

## Sources used (all already in the repo — see `refs/REFERENCES.md`)

- The **stereograph of the Italian Court** (round-1 collection,
  `CrystalPalaceItalianCourt.jpg`) — the form source: the loggia
  arcade with its round arches, Ionic pilasters, carved frieze and
  gallery above; the Gaillon fountain (the big tazza) centre-
  foreground and a Medici tomb — Michelangelo's Lorenzo with the
  reclining figures — standing against the arcade.
- 1856 guide, "THE RENAISSANCE COURT" (pp.95–99): p.97 identifies
  the space ("In the centre of the Court we find a fountain of the
  Renaissance period, from the Château de Gaillon" — the fountain
  in the stereograph) and the loggia ("in the lunettes under the
  ceiling of the small loggia, or gallery, portraits of twelve of
  the most celebrated patrons of art"); p.98 gives the court's
  ground plan; p.99 describes the back wall's assemblage.
- Detail readings from enlarged crops of the stereograph's left
  eye (copies in `refs/`): the capitals are **Ionic** — volutes
  and bolster are legible at 6× — the arches spring from moulded
  impost blocks set well below the capitals; the archivolt is a
  wide flat fascia with a raised outer roll whose crown dies just
  under the architrave; roundels flank each pilaster at capital
  height; the frieze is carved rinceaux with medallions (legible
  as carving, not stroke-legible); the pilaster shafts carry a
  shallow panel frame; walls and pilasters read mid-tone against
  paler mouldings, capitals and frieze relief (tonal reading
  only — colour is unattested, see Paint).

**Evidence vs the plan's assumption:** as with the Gothic half,
item 13 said period reference images were "still required". For
this court the collection holds a good stereograph of the arcade
itself plus the guide's plan and text — but **no drawn elevation
or section of the arcade** (the guide's one Renaissance Court
woodcut, p.95, is the court's nave entrance screen, a different
element — see REFERENCES.md). No Delamotte photograph of this
court exists in the collection.

## Dimensions — measured vs derived vs inferred

No dimension is printed in any source used. Proportions are
measured on the stereograph's left eye by visual grounding;
perspective is corrected with the arch itself (apparent span /
2 × rise = 0.970 foreshortening). Absolute size is an estimate
(chain below), ±20%.

| Part | Value | Status |
|---|---|---|
| Bay width, pier centre to pier centre | 3.80 m | **Estimated** (chain below; measured 3.81 m) |
| Total height (top of attic course) | 7.17 m | Build-up of the parts below |
| Arch span / bay pitch | 0.76 | **Measured** (0.744 apparent, ÷ 0.970) |
| Arch span (intrados) | 2.90 m (R 1.45 m) | From the measured ratio + bay width |
| Arch springing | z 3.72 m | **Measured** 3.75 m, adopted 3.72 |
| Impost block and cap | z 3.42–3.72 m | **Proportioned** from the crops |
| Arch crown (intrados) | z 5.17 m | Springing + radius (measured 5.14 m) |
| Pier width / pilaster width | 0.90 m / 0.50 m → 0.435 m (tapered) | **Measured** ratio (pilaster/pitch ≈ 0.13) + build |
| Ionic capital (necking to abacus top) | z 5.10–5.50 m | **Proportioned** from the crops |
| Spandrel roundels | Ø 0.34 m at (±1.45 m, z 5.24 m) | **Proportioned** from the crops |
| Architrave (two fasciae) | z 5.50–5.85 m | Stack adjusted ≤ 0.1 m so the archivolt crown dies just under it, as photographed (measured frieze bottom 5.75 m) |
| Frieze | z 5.85–6.42 m | **Proportioned** from the stereograph |
| Cornice (bedmould, corona, crown) | z 6.42–6.87 m | **Measured** top ≈ 6.77–6.87 m |
| Attic course | z 6.87–7.17 m (cut) | **Inferred** — the gallery wall continues past the frame of every source |
| Wall depth | 0.60 m (front y −0.30, back +0.30); overall depth 0.75 m incl. the cornice crown's projection | **Inferred** — the sources are a photograph and a plan; no section exists |

**The absolute-size chain:** (1) the Medici tomb standing against
the arcade in the stereograph carries the cast of Michelangelo's
Lorenzo de' Medici, whose seated height is 1.78 m; (2) the cast
measures ≈ 294 px in the left eye → ≈ 165 px/m at the tomb's
depth; (3) the tomb stands against the loggia, so its depth is
close to the arcade's (the residual depth difference is folded
into the uncertainty); (4) at that scale the bay pitch measures
3.81 m and the span 2.91 m — adopted 3.80 m / 2.90 m. Every link
is an estimate; **±20% on absolute size would not surprise**.
The *proportions* rest on the measured ratios.

## Paint and polychromy

**No source in the collection gives this court's colour scheme**
for the arcade. The stereograph attests tones only: walls and
pilaster shafts mid-tone, the mouldings, capitals, archivolt,
roundels and frieze relief paler. The prop therefore ships in
those two tones, labelled interpretive, with no invented
polychromy. If a colour source for the court reaches the repo,
repainting is a material change only.

## Scope — the Gothic half of item 13

SCENE-BUILD-PLAN item 13 is a *pair*: this Renaissance fragment
and the Gothic fragment (`sy-gothic-arch-fragment`, shipped),
"designed to be shot separately". This package builds the
**Renaissance fragment only**, as briefed. The two fragments
assert no adjacency and no hierarchy of civilisations, per the
plan.

## What was NOT modelled / known inaccuracies

- **The exhibits are not architecture.** The Gaillon fountain and
  the Medici tomb that identify the space in the stereograph are
  exhibits standing in the court, not part of the bay; they are
  not modelled here (the fountain is the subject of its own
  evidence problem elsewhere in the plan; figurative sculpture —
  the tomb's Lorenzo and reclining figures — is never modelled
  procedurally in this project).
- **The loggia interior.** The gallery behind/above the arcade —
  its lunettes with the twelve patrons' portraits (guide p.97),
  its ceiling and back wall — is not modelled; the prop is the
  arcade screen only, with a plain attic course cut at z 7.17 m.
- **The nave entrance screen** (guide p.95 woodcut: segmental
  arches, dense carving, the Bourgtheroulde copy) is a different
  element of the same court and is not part of this bay.
- **The frieze relief is a simplified stand-in.** The photograph's
  carved rinceaux — scrolling stems with medallions and masks —
  is legible as carving but not stroke-legible; the model ties a
  centre medallion, ring scrolls, leaves and small discs along a
  running stem. In close-up it will not pass as carving; it reads
  correctly at CP038/CP040 distance.
- **The Ionic capitals are simplified.** Volutes are stepped
  discs and the echinus a straight flare; the photograph's carved
  detail (egg-and-dart, volute spirals) is not reproduced.
- **The back** is the plain reverse of the wall and entablature;
  no source shows the arcade's back face, and no rear detail is
  invented.
- **Depth/thickness** of wall and pier is inferred (no section
  source); the front projections follow the photograph.
- No weathering, damage or later state: the court as opened in
  1854.

## QC (2026-10-26/27)

- Sources read at full resolution; proportions taken by visual
  grounding on enlarged crops of the stereograph's left eye
  (values in the table), with the arch itself as the perspective
  reference.
- Two build/render rounds, every render viewed against the
  stereograph. Rev 1 defects, all fixed in rev 2:
  (1) **cameras cropped the attic course** — pulled back (front/
  side to 17 m, target z 3.45);
  (2) **the archivolt's prominence was inverted** — rev 1's fascia
  stood prouder than its roll; the photograph shows the outer
  roll as the strongest line, so the roll now fronts at −0.38 m
  against the fascia's −0.35 m;
  (3) **the frieze relief floated as separate motifs** — a thin
  running stem at frieze centre height now ties medallion,
  scrolls, leaves and discs into the vine the photograph shows;
  (4) **black faces on the module's cut planes** — the base band,
  two lines in the entablature and a notch at the impost rendered
  near-black. Chased properly: signed volumes all positive;
  an emission-override render was clean; the blacks persisted
  under sun-only and fill-only lighting and without the ground;
  and an isolation render proved the mechanism — the base boxes
  alone render pale, but with the pier present the overlapped
  band goes black. Rev 1's pier box ran through the base steps
  and the pilaster was embedded in the pier front, so pairs of
  *exposed* faces shared the cut plane exactly (coincident
  coplanar faces of interpenetrating solids). Rev 2 partitions
  the cut-plane stack so parts butt instead of interpenetrating
  across the plane: the pier starts above its base steps, the
  base steps are split front/rear around the plinth, pilaster
  parts butt the pier's front plane, the bolster and frame rails
  stop a few mm short of the edge, and the frieze beads/stem are
  front strips stopping 4 mm short. The cut faces now render
  clean. One small dark dash remains at each impost on the cut
  face — the archivolt drop's shaded underside where it dies
  into the impost, a real moulding surface, left as found.
- Tiling verified: three modules side by side compose full piers
  with full Ionic pilasters (volute pairs, shared bases), and the
  architrave, frieze stem and cornice run continuously
  (`renders/tiled-three-quarter.png`).
- **Tiled-proof shading defect, found in review and fixed
  (2026-10-27).** The first tiled render showed the MIDDLE bay —
  the original module — shading markedly darker than the flanking
  copies (in the worst render near-black across its large faces),
  with two black dots at its volutes. The module itself is clean:
  the single-bay renders are unaffected; all 75 meshes have
  positive signed volume and unit scale; and the build script
  placed straight translated copies at ±3.80 m — **no mirrored or
  negative-scale instance exists anywhere** (the mirroring
  hypothesis was tested and disproven). Controlled renders
  isolated the trigger empirically: the defect appears only when
  the saved file's ORIGINAL objects are rendered together with
  visible duplicates of themselves. Copies rendered alone (linked
  or full) shade uniformly, and the originals render cleanly the
  moment the copies are hidden. The mechanism inside Cycles was
  not identified and is not claimed; it is an artefact of the
  originals-plus-duplicates combination in this file, not a
  defect of the model's geometry, normals or materials. **Fix:**
  the tiled proof is now composed from three full copies at
  −3.80 / 0 / +3.80 m with the originals removed from the proof
  scene (in memory only), rendered with the saved RenderSetup rig
  (Sun 3.0, Area fill 500) and the tiled camera; all three bays
  now shade uniformly (frieze-band means ≈ 175 / 184 / 184 across
  the bays — the residual gradient is the studio fill's ordinary
  falloff), the joins compose full piers with volute pairs, and
  the entablature runs continuously. The build script's tiled
  block now uses the same copies-only method. The shipped
  `.blend` and `.glb` are byte-identical to before the fix
  (md5 `79bc6cfbe6ab5c658044dd61685e1845` /
  `c1d7e8a6accf97885e8b93f9067a6873`); the prop itself never
  carried the defect.
- Counts, verified two ways (re-opening the saved `.blend` and
  parsing the exported `.glb` — both agree): **75 objects,
  3,916 triangles** — well under the ~50,000 triangle prop
  budget. World bounding box: 3.80 m wide × 0.75 m deep
  (cornice crown projection) × 7.17 m high. All meshes have
  positive signed volume; no flipped faces remain.
- The `.blend` contains two collections: `Model` (exported) and
  `RenderSetup` (ground plane, lights, cameras; not exported).
  Meshes are world-space geometry with unit scale throughout.

## Files

- `scripts/build_sy_renaissance_arch_fragment.py` — re-runnable
  bpy build script; dimensions are named constants at the top,
  grouped by evidence status.
- `sy-renaissance-arch-fragment.blend` — model + render setup.
- `sy-renaissance-arch-fragment.glb` — `Model` collection only.
- `renders/front.png`, `side.png`, `three-quarter.png` —
  neutral grey backdrop, same lighting, 1024 × 768. Front is the
  bay elevation; side shows the entablature stepping and the cut
  plane; three-quarter is the dressing view.
  `renders/tiled-three-quarter.png` shows three bays composed.
- `refs/` — the stereograph, the four guide pages consulted, the
  vestibule photograph, three enlarged crops, and
  `REFERENCES.md`.

Staged locally for review; not yet pushed to the repo.
