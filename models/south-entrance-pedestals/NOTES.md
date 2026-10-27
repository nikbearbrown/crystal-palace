# South-entrance pedestals — NOTES

Candidate #26 from `models/CANDIDATES.md`. The two pedestals drawn on
Downes Plate XXVI for the entrance at the **south end of the Transept**,
Hyde Park 1851 (film scenes CP007/CP017). Both pedestal types the plate
details are in this one folder, as separate collections in the .blend:

- **Pedestal A (`a⁵`)** — the octagonal cast-iron pedestal of one of the
  *detached* columns at the entrance (Figs. 26–27), with a short stub of
  the column `a³` it carried.
- **Pedestal B (`B³`)** — the rectangular pedestal of one of the
  *semi-elliptical wooden* columns `B` (Figs. 28–30), with a short stub
  of the wooden column itself.

## Sources

- `refs/plate-026.jpg` — Downes (1852), Plate XXVI, "Details of ditto,
  and pedestals at south entrance" (repo path
  `references/downes-1852/source-scans/plates/plate-026.jpg`; public
  domain — the book is an 1852 Fox, Henderson & Co. publication, John
  Weale, London). Detail crops of the same plate in `refs/`:
  `fig26-pedestal-a-elevation.jpg`, `fig27-pedestal-a-plan.jpg`,
  `fig28-30-pedestal-b-details.jpg`.
- Downes' text, pp. 38–39 (repo OCR,
  `references/downes-1852/crystal-palace-1851/text/downes-1852-ocr-fulltext.txt`):
  *"Fig. 26 is an elevation of the pedestal of one of the detached columns
  at the entrance at the south end of the Transept. Fig. 27 is a sectional
  plan of the same at the line zz in Fig. 26. a³ is the cast-iron column.
  a⁵ is the pedestal of cast iron [⅜] in. thick, made in two pieces, and
  united by countersunk screws. Figs. 28 and 29 are parts of a side
  elevation of the pedestal of one of the semi-elliptical wooden columns
  B in Fig. 1, and Fig. 30 is a sectional plan of the same. A is the
  cast-iron column, and A⁵ its pedestal. B is the semi-elliptical wooden
  column, and B³ its pedestal. These pedestals are shown in the South
  Elevation, Plate IV."* (The OCR garbles the casing thickness; read here
  as ⅜ in., the standard thin casting of the building's ironwork.)

No other builder's model covers these pedestals (the repo's
`display-plinth/` and `sy-classical-cast-base/` are interior sculpture
plinths of a different family and place).

## Calibration (how the dimensions were got)

Pixel metrology on the plate scan (8,825 × 3,596 px), done for this build:

- **Figs. 26/27 (pedestal A):** the plate's own printed dimension
  **4′ 9″** is drawn from the pedestal's top line (the "level of top of
  pedestal / socket joint" datum, scan y = 329) to the floor line
  (y = 3,153): 2,824 px → **49.54 px/in**. The pedestal's total height is
  therefore exactly its printed 4 ft 9 in — the dimension measures the
  pedestal itself, not the shaft alone. All A heights below are the
  code-measured plate lines at this calibration.
- **Figs. 28–30 (pedestal B details):** the two printed dimensions in
  Fig. 29 measure 157 px (3¾ in.) and 184 px (4¼ in.) → **≈ 42.5 px/in**,
  a different (larger) drawing scale from Figs. 26/27, as usual on these
  plates. The plate's two engraved scale bars match neither figure group
  exactly and were not used.
- A's shaft width was checked two ways: the Fig. 26 elevation gives
  589 px across flats (front facet 243 px = 0.414 × across-flats, the
  exact regular-octagon ratio ✓); the Fig. 27 plan's casing ring measures
  ≈ 626 px. The 6 % disagreement is left as the stated tolerance; the
  elevation value (11.9 in.) is used for the shaft, the plan for the
  plinth (1,002 px across flats, confirmed by the elevation's own plinth
  facet geometry: front facet 415 px = 0.414 × 1,002 ✓).

## Pedestal A — dimensions (all plate-measured unless noted)

Total height **4 ft 9 in. = 1.448 m** (printed). Regular octagon in plan,
flats to the cardinal points (Fig. 27), casing of cast iron ⅜ in. thick
(text), made in two pieces with countersunk screws (screw heads modelled
on the front facet at the heights Fig. 26 draws them: bell, torus, three
down the shaft, one in the plinth).

| Part | Height | Width across flats |
|---|---|---|
| Plinth | 5.4 in. (0.137 m) | 20.2 in. (0.513 m) |
| Base flare (cyma) | 6.0 in. (0.152 m) | 14.0 in. at foot → 11.9 in. |
| Shaft | 40.9 in. (1.039 m) | 11.9 in. (0.302 m) |
| Torus (cushion) | 3.9 in. (0.100 m) | 14.1 in. max (0.359 m) |
| Band | 0.8 in. (0.020 m) | 13.5 in. (0.343 m) |
| **Pedestal top** | **57.0 in. (1.448 m)** | |
| Bell (socket of column a³) | 3.8 in. (0.095 m) | 13.5 in. → 11.9 in. |
| Column stub a³ | Ø 9.3 in. (0.236 m), from Fig. 27 plan | stub length 9 in. **adopted** — the plate is cut at its top edge |

## Pedestal B — dimensions (mixed provenance; read the flags)

Plan from Fig. 30 at 42.5 px/in: **23.0 in. wide (along the wall) ×
21.3 in. deep** (0.584 × 0.541 m). The figure's own dimension stack at
its front reads 3¾ in. + ½ in. + 1½ in. to the casing frame — the front
of the section is a framed construction; the model reads this as a
shallow framed panel on the shaft's front face (**interpretation**, the
projection is modelled at 0.2 in., not the full stack). Plinth 6.4 in.
tall (Fig. 29 at its calibrated scale; Fig. 29 also shows the pedestal's
fixing dowels dropping below floor level — not modelled, they are
sub-floor). Base flare and the cap (torus, band, bell) follow A's
profile heights — Figs. 28–29 are drawn at the same levels as Fig. 26's
cap and base, adjoining them on the plate. **Overall height adopted
equal to A: 4 ft 9 in.** — Figs. 28 and 29 are only *parts* of B's side
elevation (top and bottom); the shaft's middle is not drawn anywhere,
so B's shaft length is the residue of the adopted total, not a
measurement. Wooden column stub B: semi-ellipse 19.5 in. wide × 13.5 in.
projection from its flat (wall) back (Fig. 30, ±10 %); stub length
12 in. **adopted**. In the building, B stands against the cast-iron
column A (Fig. 30 shows both in one section); only B and its pedestal
are modelled here.

## In the file

- Origin at pedestal A's base centre, z = 0 at floor level, metres.
- Pedestal B is placed at (+1.05, +0.62) m — a display stagger so both
  pedestals read in the front and side renders. It is **not** a
  positional claim about the entrance; in the building the two types
  stood in the south transept front composition shown in Downes'
  Plate IV.
- Collections: `Pedestal_A_A5_octagonal`, `Pedestal_B_B3_rectangular`.
- 1,360 triangles total; .blend 4.2-compatible; build script in
  `scripts/` (renders are made by `scripts/render_views.py` from the
  saved .blend — in this VM EEVEE's GPU stack aborts, so the shipped
  renders are Cycles CPU at 96 samples; the .blend itself is
  engine-agnostic).

## Honest verdict

Pedestal A is a measured build: its height is the plate's own printed
dimension, its plan is confirmed by two independent octagon checks, and
its moulding divisions are the plate's lines. Its uncertainties are the
6 % plan-vs-elevation width tolerance, the cyma/torus curve shapes
(sampled from the drawn profiles, not dimensioned), and the column
stub's length (adopted; the real column continued to the gallery).
Pedestal B is a documented reconstruction, not a measured one: plan,
plinth and the 3¾/4¼ in. details are measured, but its total height is
adopted from A and its shaft middle is undrawn — treat B as correct in
plan and character, approximate in elevation. Paint colour is a neutral
grey stand-in for the building's painted ironwork; no period colour for
these pedestals is recorded in the references used.
