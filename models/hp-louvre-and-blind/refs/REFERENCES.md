# REFERENCES — hp-louvre-and-blind

All evidence is from the repository `nikbearbrown/crystal-palace`
itself (per `MUSE-PROMPT.md` §2: use only what is already in
`references/`). Hyde Park 1851 only.

## Primary source — copied into this folder

- `plate-027.jpg` — Downes (Charles Downes / E. A. Cowper text),
  *The Building Erected in Hyde Park for the Great Exhibition of the
  Industry of All Nations, 1851* (John Weale, April 1852), **Plate
  XXVII, "Details of machinery for moving louvres"**.
  Repo path: `references/downes-1852/source-scans/plates/plate-027.jpg`
  (branch `main`). Public domain (1852 publication).
  This single plate is the design source for the whole mechanism:
  - **Fig. 1** — vertical section through the louvre bank at the upper
    part of a tier: five S-curved blades E, pivot pins, hoop-iron
    links L, bars M, connecting rod N, worm-wheel O, endless screw P,
    rope pulley Q with rope R, sill/wall plate K. Solid lines =
    closed; dashed lines = open.
  - **Fig. 2** — internal elevation: the bank, the two bars M with
    block *a* and rod N at the centre, the large spoked rope pulley Q
    in front of the bank, shafting T T running both ways.
  - **Figs. 3–5** — the ⅜ in blade pivot pin (Fig. 4: 2 9/16 in long,
    ⅜ in rivet holes).
  - **Figs. 6–9** — the two-piece bearing S (Fig. 8 plan: halves 1 in,
    centre 1½ in; Fig. 9 sectional plan lettered "Shafting 1 inch
    dia. T").
  - **Figs. 10–14** — intermediate bearing S¹ (base 3 in printed;
    shaft centre 3¾ in above the sill, printed Fig. 10), crank U
    (Fig. 13: shaft hole 1 1/16 in, pin hole 9/16 in), connecting rod
    N′ (Fig. 14: ⅜ in, eye 9/16 in).
  - **Fig. 12** — double bearing S² (base 7⅜ in printed) at shafting
    junctions. (Not modelled — see NOTES.)
  - **Figs. 15–17** — single/double bearings of the *lower* (ground
    floor) louvre shafting; **Figs. 18–22** — the lower louvres'
    mitre-wheel hand drive. (Different apparatus from the upper-tier
    rope drive modelled here — see NOTES.)
  - The plate's own scale bar (12 in) was used for measurement:
    70.8 px/in on the repo scan, cross-checked against the printed
    5½ in dimension in Fig. 1 (390 px measured).
- Crops of the same plate, made for this build (derivatives of the
  file above): `plate-027-fig1-section.jpg`,
  `plate-027-fig1-blade-detail.jpg`, `plate-027-fig2-elevation.jpg`,
  `plate-027-figs10-12-bearings.jpg`.

## Text sources — repo files, quoted in `downes-louvres-and-canvas-text.txt`

- `references/downes-1852/crystal-palace-1851/text/downes-1852-ocr-fulltext.txt`
  (branch `main`) — the Downes/Cowper prose:
  - **"LOUVRES" chapter, printed pp. 39–40** — the mechanism described
    part by part (quoted in full in the extract file): louvres of
    galvanized sheet iron; ⅜ in pin riveted to the end of each louvre;
    hoop iron L, 1 in wide, bent to an eye; wooden pins through two
    wooden bars M M; block *a*; connecting rod N; worm-wheel O and
    endless screw P; pulley Q with endless cord/rope R; bearing S in
    two pieces on wall plate K with wooden cleat *c*; shafting T T,
    1 in, "a length of 108 ft on each side of the wheel is thus set in
    motion simultaneously"; intermediate bearings S′ with cranks U
    working the bars of the intermediate louvres.
  - **Introduction, printed p. 7** — "several thousand [feet] of
    louvres, made of galvanized sheet-iron plates corrugated in an
    S form, which not only gives great stiffness to the plates, but
    also forms a good joint between the louvres."
  - **"OUTER WALLS", printed p. 32** — the ground-floor wall has eight
    louvres below the boarding and **five louvres** above the
    wall-plate; the upper tiers likewise have five louvres above the
    windows. (This fixes the five-blade bank modelled here.)
  - **Plate XXII description, printed p. 33** — the louvre case
    "consists of two jambs and a head, all 5½ in. wide and ⅞ in.
    thick", a ⅜ in lining concealing the case, and a strip of wood
    2½ in wide by ⅜ in thick "against which the lower louvre-board
    shuts"; wall-plate 10 in wide.
  - **"MISCELLANEOUS DETAILS", printed p. 44** — the building's only
    canvas in Downes: "The roof was covered with canvas, to reduce
    the light and heat in the interior of the building. The canvas
    was nailed to the ridges and allowed to hang down between them.
    It was in two breadths, with the seam in the centre…" — the
    source of the blind's two-breadth/centre-seam construction. It
    describes the *roof* canvas, not a blind on this unit; see the
    blind note in NOTES.md.
  - OCR warning (from CONTROL-DIMENSIONS.md): the OCR misreads
    fractions; every fraction used in the model was read off the
    printed plate or the plate's printed dimensions, not the OCR.

## Controls

- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md`
  (branch `main`) — **D22**: "Louvre run moved by one wheel: 108 ft
  each side — Plate XXVII — text. No plate shows this: Plate XXVII
  draws the louvre mechanism at detail scale (1 ft bar). Printed
  page 53 confirms the figure." The model's shafting is therefore
  cut at the unit's ends and the truncation is stated in NOTES.md.

## Checked, not used

- `references/muse-drive/review/catalogue.json` item 0347,
  "Cross section of louvre-blade" (`images/commons/The_Crystal_Palace_section_7.png`)
  — a 36 × 53 px thumbnail; too small to measure. Not used.
- The 1851 Official Catalogue material in the repo (Introduction
  pages collected in round 2 for the floor description) contains no
  louvre or blind description usable for this prop.
- 1851 interior photographs (0169/0170/0177/0181/0184 in
  `references/muse-drive/images/`) show the louvre banks only as
  distant horizontal bands above the wall boarding; consistent with
  Plate XXVII but adding no measurable detail. Appearance check only.
