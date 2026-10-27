# NOTES — hp-working-machine-exhibit: Nasmyth steam hammer, Great Exhibition 1851

**Prop:** Wave 2, item 8 — the ONE working machine exhibit for CP024.
**Staging:** `~/workspace/crystal-palace-film/build/hp-working-machine-exhibit/`
(not pushed to GitHub; parent audits and pushes). **Blender 4.5.3,
metres, origin at base centre, scale applied.**

## What this is — and the narrow claim only

Nasmyth & Co (J. Nasmyth, Patricroft, Manchester) exhibited a steam
hammer at the Great Exhibition, Hyde Park, 1851: *Official Descriptive
and Illustrated Catalogue*, **Class VI, No. 236**, Council Medal.
That is the only historical claim this prop makes. Steam-hammer
priority is **contested** (Bourdon/Schneider, Le Creusot 1840; the
Science Museum's text for its full-size hammer states Nasmyth "did
not invent the steam hammer, nor was he the first to build one") —
never "inventor of the steam hammer" anywhere in this package.

## Spike verdict (see SPIKE.md for full reasoning)

- **Form: ESTABLISHED** from the exhibit's own photograph, Ferrier,
  RCIN 2800024 (*Reports by the Juries*, Vol. II), inscribed
  "J. Nasmyth's patent" / "J. Nasmyth & Co Engineers, Manchester".
- **Exhibit identity: ESTABLISHED** (Catalogue Class VI, No. 236;
  jury report "(236)"; Council Medal).
- **Exhibit dimension: NOT FOUND.** The Catalogue Class VI entry
  was checked as the decisive open source and gives no dimension,
  weight or fall. No dimension for the 1851 exhibit itself was found
  in the catalogue, jury report, or press/biographical coverage.
- **Absolute scale: ASSUMED / UNCONFIRMED.** The build adopts a
  nominal overall height **H = 5.00 m** purely as a modelling
  assumption applied to the photograph's own proportions, flagged
  with an indicative **±30% (3.5–6.5 m)**. Scene placement must not
  treat the height as established.
- **SMG co46218 is NOT a dimension source** (spike guardrail
  correction, 2026-10-27): it is a 1:4 model of the FIRST hammer
  (1839 design / 1842 patent), not of the 1851 exhibit, and its
  record as read gives no model measurements to scale from. It is
  used for **mechanism evidence only**. The IMechE 1:8 model is
  likewise excluded (Patricroft works machine, 1847 self-acting
  improvement — a later form).
- **Absence of a dimension is never permission to borrow one.**
  See "Figures NOT used" below.

## Adopted dimensions (status per dimension)

H = 5.00 m nominal. Fractions are of H, measured from the Ferrier
photograph (RCIN 2800024, 807 × 1024 px + 3× tup/anvil crop;
±3% levels, ±5% widths).

| Dimension | Value | Status |
|---|---|---|
| Overall height (floor → top of lifting eye) | 5.00 m | ASSUMED, UNCONFIRMED ±30% |
| Overall width across feet | 3.61 m | PHOTO-MEASURED (0.722 H) |
| Overall depth (sole plates) | 1.55 m | INFERRED ±30% |
| Cylinder barrel Ø | 0.48 m | PHOTO-MEASURED (0.096 H) |
| Cylinder barrel, z-range | 3.18 → 4.67 m | PHOTO-MEASURED (0.636–0.934 H) |
| Cylinder covers/flanges/eye | to 5.00 m | PHOTO-MEASURED |
| Standards top bearing (cylinder seat) | 3.18 m | PHOTO-MEASURED |
| Clear throat between guides | 0.67 m | PHOTO-MEASURED (0.134 H) |
| Standard foot width (each, X) | ≈0.88 m | PHOTO-ESTIMATED |
| Standard depth (Y, at base) | ≈0.88 m | INFERRED ±30% |
| Anvil working face height | 0.59 m | PHOTO-MEASURED (0.118 H) |
| Anvil foundation block top | 0.35 m | PHOTO-MEASURED (0.070 H) |
| Tup: die + main block height | 0.22 + 0.57 m | PHOTO-MEASURED |
| Tup block width | 0.67 m | PHOTO-MEASURED (≈ throat) |
| Tup depth (Y) | 0.67 m | INFERRED (square-ish block) |
| Piston rod Ø | 0.12 m | PHOTO-ESTIMATED |
| Tup rest position (die bottom) | 0.64 m | PHOTO-MEASURED (0.128 H) |
| Tup modelled travel (animatable) | 1.30 m above rest | INFERRED from guide/cylinder clearances |
| Valve chest | ≈0.54 × 0.64 m, front of cylinder, offset left | PHOTO-MEASURED/ESTIMATED |
| Hand lever length (projects left) | ≈0.98 m | PHOTO-ESTIMATED |

Modelled top of the lifting eye is 4.98 m (torus geometry); the
nominal 5.00 m is the design height, not a measured value.

## Mechanism (as evidenced)

Single-acting, direct-action (SMG pattern description for co46218,
consistent with the exhibit photograph): the tup is connected to
the piston of the vertical steam cylinder and guided between two
standards. Steam admitted **below** the piston lifts the tup; the
valve then lets it **fall by gravity** onto the work. Double-acting
(steam above the piston) was a later improvement — the build is
single-acting. The slide valve sits in the bolted chest on the
cylinder's front, worked by the hand lever (original hand-gear
control). Wilson's 1843 self-acting regulating device (small
overhead cylinder, levers, vertical motion rod, low handwheel) is
included in **simplified form, flagged as pattern-evidence** —
the photograph shows the overhead gear, motion rod and handwheel,
but their exact geometry is not dimensioned from the photo.

## The moving component (CP024 animation)

- Object **`Tup`** (die + main block + piston rod + blank plate,
  one joined object) is the only moving part.
- Shipped at **mid-stroke**: object location z = 0, die bottom
  1.29 m above the floor.
- **Rest:** location z = −0.65 m (die bottom 0.64 m, ≈0.05 m above
  the anvil face — as photographed).
- **Full raise:** location z = +0.65 m (die bottom 1.94 m).
- **Modelled travel: 1.30 m.** Animators move `Tup` in Z only;
  at full raise the block top (2.73 m) stays clear of the cylinder
  underside (3.18 m) and the rod stays engaged.
- `renders/tup-raised.png` shows the Tup at full raise, proving
  the moving component. The `.blend` and `.glb` ship with the Tup
  at mid-stroke.

## Figures NOT used (borrowed-dimension traps)

- **30 cwt / 4 ft fall**: the Patricroft works demonstration hammer
  built after the June 1842 patent (Nasmyth, *Autobiography*) —
  not the exhibit.
- **5 tons / 5 ft fall**: the next order, Rushton & Eckersley of
  Bolton — not the exhibit.
- **4-ton pile driver; 50-cwt Admiralty order; surviving full-size
  SMG hammer co46229** ("a small version") — all different machines.
- **Later double-frame hammers; the 1847 self-acting patent form**
  (IMechE 1:8 model) — not the 1851 exhibit's evidence.

## Egg stunt — NOT staged, NOT claimed

Unresolved secondary-source conflict: the *Autobiography* attaches
the egg passages to the Patricroft hammer and to a Devonport
Dockyard demonstration (2½-ton hammer, before the Lords of the
Admiralty); a Science Museum blog relocates an egg demo to the
1851 Exhibition. CP024 shows **generic tup motion only**. The
catalogue's 1851 editorial note claims only the *capability* of
graduating the blow to egg-shell force. No egg, wineglass or anvil
prop is included, and no caption may claim the stunt happened at
the Exhibition.

## Maker's plates — BLANK

The photograph shows plates reading "J NASMYTH & Co / ENGINEERS /
MANCHESTER" (right standard) and "J NASMYTH'S / PATENT" (tup
block). The build carries **blank plate boxes only** — no
inscription is modelled or textured, so nothing is invented. If a
later pass adds text, it must match the photograph's wording, not
an invented variant.

## Files

- `SPIKE.md` — gate document (revised 2026-10-27 under the spike
  guardrail corrections).
- `build_hp_working_machine_exhibit.py` — re-runnable build +
  render script (Blender 4.5.3, Cycles CPU, 960 × 960 px).
- `hp-working-machine-exhibit.blend`, `hp-working-machine-exhibit.glb`
  (Tup preserved as its own object).
- `renders/front.png`, `renders/side.png`,
  `renders/three-quarter.png`, `renders/tup-raised.png` (neutral grey).
- `refs/REFERENCES.md` + copies of the photo/model/lead images used.

## QC

- Reopened `.blend` and `.glb` after build: **31 mesh objects**
  (excluding the render ground plane), **`Tup` present as its own
  object** at location z = 0 (mid-stroke), bounding box ≈
  3.61 m (X) × 1.55 m (Y) × 4.98 m (Z), origin at base centre.
- **Triangle count: 4,368** (well under the ~50k budget).
- Renders viewed before delivery: front, side, three-quarter and
  tup-raised all read as the photographed machine (A-form
  standards, cylinder on top, tup between guides, anvil below).
  One defect found in first-pass QC — the small Wilson cylinder
  floated beside the top cover with a visible gap — was fixed
  (moved into contact with the barrel) and the set re-rendered.
- Known limitations (not defects): depth dimensions are inferred
  (front photograph only); the Wilson gear is simplified
  pattern-evidence; the absolute height is an unconfirmed nominal
  assumption (±30%); the side elevation naturally hides the tup
  behind the near standard, as a real side view would.
