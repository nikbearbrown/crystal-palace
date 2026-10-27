# NOTES — Post-1866 north-end closure dressing

Prop for the Crystal Palace film (SCENE-BUILD-PLAN Wave 4,
item 16). Scenes: CP048 (the missing transept stays missing —
the north end permanently altered, loss and surviving structure
readable in one view; the fire itself is CP047). **Sydenham
only, post-1866 state.** Nothing here may be placed in the
1854–66 palace, and nothing here is 1936: the 1936 ruin is a
separate prop (item 17, `sy36-ruin-fragment`) with a different
job.

## What it is

A variant/condition set of three elements, each in its own
collection in the `.blend`, composed as delivered around one
24 ft structural bay at the burn line:

- **`DamagedBay`** — the fire-damaged end bay: two columns and
  the girder between them (heat-sagged, blackened), the
  skeletal end-wall framing in the bay plane (light rails and
  diagonal flats in two tiers, every pane of glass gone), two
  kinked roof stubs, heat-drooped bars, hanging sash bars, a
  fallen girder length, and a patch of the palace's open-
  boarded floor running from scorched (south) to deep-charred
  and burnt away (north-east corner), with fallen charred
  joists. The east column leans ~2° at its head toward the
  burn. This is a *fragment at the edge of the destruction*,
  not a model of the ruins as a whole.
- **`ClosureScreen`** — the closure across the nave at the
  burn line: a double-boarded timber screen one bay wide and
  6.60 m high, framed on posts and rails, boarded both faces,
  diagonal-braced on the nave face, one board replaced. See
  "Evidence status" — this element is a **reconstruction**.
- **`Shoring`** — timber shoring to the damaged bay: two dead
  shores under the sagging girder (cross-braced), a waling
  across the end frame's burn face with two raking shores
  from the north, and one raking shore against the leaning
  east column. See "Evidence status".

Origin at the base centre of the damaged bay (between its
columns), finished floor level z = 0. Units: metres.
Blender 4.5.3.

## The state line (1866 → 1878)

- **30 Dec 1866** — fire destroys the north transept and the
  northern end of the palace (ILN, 12 Jan 1867: ruins
  engraving + account; its plan diagram tints the destroyed
  extent). Round 2 established the date firmly; some
  secondary sources drift it into 1867.
- **1867 onward** — the palace reopens without the transept;
  the surviving building is closed at the burn line. The
  form of that closure is **not pictured in any source in
  this collection** (build-plan evidence gate 6, still open).
- **1878** — the official guide's ground plan (the earliest
  post-fire plan found) shows the end state: transept
  absent, the building terminating at a straight line, its
  northern rooms in use as the "Tropical End", Aquarium
  corridor and Orangery beyond.
- A precedent the film can lean on: by **1856** the north
  transept was already partitioned from the nave by "a
  gigantic curtain" (1856 guide, p.148, the Tropical End) —
  this end of the palace had been screened off before.

## Sources used (see `refs/REFERENCES.md` for the full table)

- ILN 12 Jan 1867 ruins engraving — primary visual source
  for the damaged bay (frame skeleton, drooped bars, fallen
  members, glass wholly gone).
- ILN 12 Jan 1867 p.42 — account + tinted-extent plan
  diagram (the state line).
- 1878 official guide ground plan — the after-state and the
  closure line's position.
- Phillips 1854, view from the north — the same end before
  the fire (pairing view; context only).
- Downes 1852 dimension controls via `hyde-park-column-
  tier1` — the structural sizes of the bay.
- Paxton's printed floor figures via `hp-floor-boards` —
  the floor patch's member sizes.

## Dimensions — documented vs plate-read vs reconstructed

| Part | Value | Status |
|---|---|---|
| Bay width (column centres) | 24 ft (7.315 m) | **Documented** — the palace's structural module |
| Column | 10 in OD (0.254 m); floor collar 6 in; intermediate collars ~2 m / ~4 m | **Documented** (bore/flange per Plate VIII via the column prop); collar positions proportional, inferred there |
| Girder | 3 ft 0 in deep (0.914 m), soffit 19 ft 2 in (5.842 m), flanges 0.30 × 0.05 m | **Documented** (Plate VIII / controls D10–D11); flange width as the column prop |
| Floor | boards 1½ in thick × 9 in wide, ½ in gaps; joists 7 × 2½ in | **Printed** (Catalogue pp.62–63); board width inferred in `hp-floor-boards` |
| End-frame rails / braces | 0.14 m rails, 0.11 × 0.025 m diagonal flats, mid rail at half the girder line | **Plate-read** — scaled from the ILN skeleton's proportions; no dimensioned source exists for the end framing |
| Girder heat sag | 0.17 m at mid-span | **Guessed** — modest, in the spirit of the plates (the engraving's damage is mostly in the roof bars, not the main girder) |
| East column lean | 0.3° / 1.1° / 2.3° by segment, ≈ 0.14 m at the head, toward the burn | **Guessed** — kept small; the engraving's standing frame is plumb, so the lean is a dressing choice at the burn edge, flagged here so it is never quoted as evidence |
| Drooped bars | Ø 0.032 m tubes, droop to ≈ 3.6–3.9 m | **Plate-read form, guessed sizes** — the engraving's most distinctive read |
| Closure screen | 7.315 m wide (one bay) × 6.60 m high; posts 0.15 m sq; rails at 0.10–0.25 / 3.28–3.43 / header 6.42–6.60 m; boards 0.228 × 0.025 m both faces | **Reconstruction** — period-typical double-boarded timber partition sized to the bay; no dimension of the real screen is known |
| Shoring | dead-shore posts 0.22 m sq; raking baulks 0.24 × 0.20 m at ≈ 60°; soles, caps, wedges, waling 0.14 × 0.18 m | **Reconstruction** — standard period shoring practice, sized to meet the (documented) girder soffit, sag included |

## Evidence status, element by element

- **DamagedBay — evidenced in kind, estimated in degree.**
  That the end frame stood as a glassless, blackened
  skeleton of columns, rails and cross-bracing, with roof
  bars heat-drooped and members fallen across the floor, is
  exactly what the ILN engraving shows, and the sizes of its
  main members are the documented palace sizes. The *degree*
  of damage in any one bay (sag 0.17 m, lean ≈ 2°, which
  boards burnt away) is chosen dressing, stated above —
  the engraving's transept was destroyed wholesale; this
  fragment is the survivable edge of that destruction, which
  is what CP048 photographs.
- **ClosureScreen — RECONSTRUCTION, flagged.** No image or
  description of the actual post-fire screen was found in
  the collection (the two genuine post-fire photographs are
  unlicensed and were not used). What is modelled is a
  plain, double-boarded, ledged-and-braced timber partition
  of period-typical construction, sized to the documented
  bay — the least-inventive closure a Victorian works
  department would build. The 1856 "gigantic curtain" is a
  documented precedent for screening this end, but it was
  canvas and a decade earlier; it is **not** what is
  modelled, and the screen must not be captioned as the
  documented 1867 screen. If evidence for the real closure
  reaches the repo, this element is the one to replace.
  The screen is also only the ground tier: the real end
  treatment rose beyond one storey, and scene builders
  should stack/extend the module rather than treat 6.60 m
  as the closure's full height.
- **Shoring — RECONSTRUCTION, flagged.** No shoring is
  visible in the 1867 images consulted (the engraving shows
  workmen clearing, not shores). Dead shores under a sagging
  girder and raking shores to a leaning column are the
  standard period response and are what a scene of the
  secured ruin needs; sizes follow carpentry practice, not
  a Crystal Palace source. Treat as plausible dressing.

## What was NOT modelled / known inaccuracies

- **The Egyptian Court colossi** that dominate the ILN
  engraving — figurative sculpture is sculptor work, never
  procedural in this project. Their absence also removes
  the engraving's scale anchor; the bay's scale rests on
  the documented dimensions instead.
- **The ruins as a whole** — the twisted transept interior,
  rubble fields and the destroyed courts are outside this
  prop; CP047's fire and CP048's wide shots need scene
  work, not a bigger fragment.
- **No glass at all** — deliberately: the engraving shows
  the frame wholly stripped. A few surviving panes would be
  invention.
- **No smoke, flame, snow or workmen** — condition/season/
  population are scene dressing. (The unlicensed Historic
  England photographs show snow on the ruins; noted here
  only as a pointer for the scene builders.)
- Char and scorch are **procedural** (noise-driven node
  materials); there is no photographic texture anywhere in
  the prop. In the `.glb` the noise variation does not
  survive export — the char reads as flat near-black there;
  the `.blend` is the reference version.
- The girder is the column prop's plate-girder reading
  (flanges + web). The ILN skeleton's bands look lighter,
  more like lattice; where the two conflict, the documented
  plate evidence was preferred for the main member and the
  engraving's lightness was given to the end framing.
- Floor patch underside sits at grade (−0.038 m): the
  patch's joists are not modelled except as fallen pieces,
  and the boards run one way only, as a remnant — it is
  not a second floor-system prop (that is `hp-floor-boards`).

## QC (2026-10-26)

- Evidence files verified against the round-2 manifest
  (all four PD; licences recorded in REFERENCES.md).
- **First builds — three real defects, all fixed and
  re-rendered.** (1) The side render came out rolled 90°:
  the camera helper aimed with a bare `rotation_difference`,
  which leaves the roll arbitrary — front happened to land
  upright, side did not. Cameras now use a proper look-at
  with world-up. (2) The front render showed black squares
  on the screen's header band and a black diamond at the
  diagonal braces' crossing: post faces and rail faces were
  exactly coplanar (z-fighting), as were the two braces'
  side faces where they crossed. Rails/header are now
  recessed 6 mm behind the post faces and cut flush with
  them. (3) The first brace fix — offsetting the second
  brace in Y to lap the crossing — buried it in the board
  layer and it vanished from the front render; the shipped
  detail is carpentry instead: one brace continuous, the
  other butted to it with a short gap at the crossing. The
  dead-shore X-brace pair is lapped (no board layer behind
  it there). The coplanar trap was checked across the rest
  of the set (girder segment joints are end-to-end, not
  coplanar-faced; floor boards are separated by their
  printed gaps; the end frame's X pairs are Y-offset).
- Renders were viewed against the ILN engraving: frame
  skeleton read, droop curves, glasslessness and the
  scorched→charred floor gradient all check; the lean reads
  as damage, not as a modelling error, at ≈ 2°.
- Counts: **221 objects, 3,588 triangles** — verified
  three ways (build log, independent parse of the exported
  `.glb`, and a re-opened `.blend`): DamagedBay 125 objects
  / 2,436 tris, Shoring 23 / 276, ClosureScreen 73 / 876.
  Far under the ~50,000 triangle prop budget. World
  bounding box 10.60 × 7.43 m plan (shore feet included),
  8.29 m to the rafter-stub tips.
- The `.blend` contains the three model collections
  (`DamagedBay`, `Shoring`, `ClosureScreen`) plus
  `RenderSetup` (ground, lights, cameras; not exported).
  All model objects are world-space geometry with unit
  scale (transforms applied before save/export). The `.glb`
  exports the three model collections only.

## Files

- `build_sy_post66_closure.py` — re-runnable build script
  (bpy); all dimensions are named constants at the top,
  grouped documented / plate-read / reconstruction /
  dressing.
- `sy-post66-closure.blend` — model + render setup.
- `sy-post66-closure.glb` — the three model collections.
- `renders/front.png` (from the nave side — the closure
  screen with the damaged bay's stubs above it), `side.png`
  (profile: screen, bay, raking shores), `three-quarter.png`,
  `damaged-bay.png` (close view of the bay from the burn
  side). Neutral grey backdrop, 960 × 720, Cycles with
  denoising at 48 samples (the finish the Wave 3 court's
  renders shipped with; the shared build VM was heavily
  contended — the script's default 128-sample pass upgrades
  them without any geometry change).
- `refs/` — the four reference images used, one derived
  crop, and `REFERENCES.md`.
