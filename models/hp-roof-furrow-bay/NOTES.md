# NOTES — Hyde Park roof glazing panel: timber sash bars + glass

Prop for the Crystal Palace film. **Hyde Park 1851 building only** — no
Sydenham evidence is used in this model. Scenes: CP013 (iron, glass —
and timber), CP016 (glazing at construction speed).

## What it is

One repeatable unit of the 1851 ridge-and-furrow roof: **one complete
furrow across a full 24 ft bay** — two glass slopes at 2½ to 1 between a
central timber ridge piece and two timber Paxton gutters at 8 ft pitch,
carrying 27 timber sash bars and 28 panes per slope. The unit repeats
along the building (bays) and across it (furrows). Origin at the base
centre: x = 0 on the ridge centreline, y = 0 at mid-bay, z = 0 at the
underside of the gutters. Units: metres. Blender 4.2+.

Overall: 2.583 m across (101.7 in) × 7.315 m long (24 ft) × 0.654 m
high (25.7 in to the ridge crest).

## Sources used (all already in the repo)

- `references/downes-1852/source-scans/plates/plate-012.jpg` — Downes
  Plate XII, "Glass roof and Paxton gutters": Fig. 1 (roof section,
  8 ft / 4 ft printed), Fig. 3 (gutter elevation, bar-notch chain),
  Fig. 10 (enlarged gutter / bar / ridge sections). Primary source.
- `references/downes-1852/source-scans/plates/plate-013.jpg` — Plate
  XIII, main gutters (gutter fall figure only).
- `references/downes-1852/source-scans/plates/plate-014.jpg`,
  `plate-018.jpg` — Plates XIV / XVIII, consulted (gallery details;
  transept-vault sash bars — a different, curved construction).
- `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` —
  controls D06, D09.
- `references/downes-1852/crystal-palace-1851/text/downes-1852-ocr-fulltext.txt`
  — Cowper's text: glass and sash-bar passages.
- Interior photographs 0169 / 0184 (Talbot and LCCN general views) as
  appearance checks — see `refs/REFERENCES.md`.

## Dimensions — measured/printed vs guessed

| Part | Value | Status |
|---|---|---|
| Panel length | 24 ft (7.315 m) | Control D06, plate-checked + printed on Plate X/XII |
| Gutter pitch (ridge-to-ridge) | 8 ft (2.438 m) | Control D09, plate-checked on Plates VI, XII; Fig. 1 prints "8′ 0″" |
| Half-pitch (ridge CL to gutter CL) | 4 ft (1.219 m) | Printed on Plate XII Fig. 1 ("4′ 0″") |
| Glass slope | 2½ to 1 (21.8°); rise 19.2 in per half-pitch | Printed on Plate XII Fig. 10 ("Inclination 2½ to 1") and text p.15 (printed-page check; the OCR layer's "24 to 1" is a known misread) |
| Glass pane | 49 in long × 10 in wide nominal | Text p.15: sheets cut into panes "49 in. long and 10 in. wide". Modelled centre-to-centre of bars (10½ in typical), length exactly 49 in — its ends land inside the ridge piece and at the gutter cheek, as Fig. 10 draws |
| Glass thickness | 0.08 in (≈2 mm) | Derived: text gives weight 16 oz per sq ft, not a thickness; the text's thickness fraction is garbled in the OCR copy and was not read off the printed page. Marked derived, not printed |
| Bar centres along the bay | 5¼ in end margins; 10½ in typical; 11¼ in flanking strong bars | Printed chain on Plate XII Fig. 3; the model's 27 positions per slope reproduce the chain exactly (it sums to 288 in) |
| Ordinary sash bar | 1 in wide × 1⅜ in deep overall | Printed on Plate XII Fig. 10 section and stated in the text |
| Bar top profile | Central rib ⅜ in wide; glass grooves/shoulders each side | Plate XII Fig. 10 section (⅜ in figures) + text: bars "furnished with a groove on each side … to receive the glass" |
| Strong bars | 2½ in wide; **three in every 24 ft**, at 4 ft, 12 ft, 20 ft | Width printed (Fig. 10 section) and text ("Three stronger bars are introduced in every 24 ft., their width being 2½ in."); positions from the wide notches in Fig. 3 — at the centres of the three 8 ft gutter-pitch modules |
| Strong bar depth | 1⅞ in overall (modelled) | **Interpreted.** The plate section also carries 2⅜ in and 15⁄16 in figures whose referents are not fully legible; 1⅞ in is the reading used. See "known inaccuracies" |
| Ridge piece | 3 in wide at base | Printed on Plate XII Fig. 10 ("3″"). Depth 3.55 in and the crest profile are proportional estimates from the drawing — not dimensioned on the plate |
| Paxton gutter | Base 5 in wide; channel 2½ in deep; overall depth 6 in | Base and channel printed on Fig. 10 (5″; 1¼ + 1¼ in). The 6 in is the plate's right-hand dimension, taken as overall depth (see inaccuracies). Cheek width at top (5.7 in) and the side condensation grooves are drawn profiles, scaled proportionally |
| Paint colour | Pale warm off-white painted timber | Interpretive: the roof reads pale and fine-latticed in the 1851 interior photographs (0169/0170/0177/0181/0184). The exact 1851 paint colour is NOT verified. Timber was painted, not bare |

## What was NOT modelled / known inaccuracies

- **Gutter fall omitted.** The real gutters were cambered/fell toward
  their outlets (Plate XIII Fig. 5: fall ⅝ in in 8 ft; the text notes
  the ridge is "cambered like the gutters"). The panel is modelled
  level so the unit repeats cleanly; over one 24 ft length the real
  fall is ≈1⅞ in.
- **Strong-bar depth** is the least certain figure on the model (see
  table). Its width, count and positions are printed/text-stated; only
  the depth is an interpreted reading.
- **Gutter profile detail** (cheek flare, condensation-groove shape,
  channel curve) is traced proportionally from Fig. 10, not
  dimensioned; the printed anchors are the 5 in base, the 2½ in
  channel depth and the 6 in overall dimension.
- **Bar feet and glass ends** are housed into the gutter notches and
  the ridge piece (hidden overlaps of well under an inch), following
  Fig. 10's line work, where the glass runs past the bar ends into the
  ridge groove and down to the gutter cheek. The small glazing clips
  drawn at the pane ends in Figs. 2/10 are not modelled.
- **Putty** in the bar grooves (the text's glazing method) is not
  modelled as a separate material.
- No trusses, main gutters, louvres or structure below the Paxton
  gutters — this is the glazing panel alone, as the build plan scopes
  it. The gutter's cast-iron support struts and tie rods (Plate XII
  Figs. 7–9) belong to the truss props, not this panel.
- Glass is modelled as flat panes of uniform thickness with clean
  edges; the real cylinder sheet glass was wavy and varied.

## Relationship to other models

Independent prop built from the plates, in the same series as
`hyde-park-column-tier1`. Not copied from
`course-models/crystal-palace-1851-claude/` or `blender-deliverables/`.
Its bay length (24 ft) and gutter pitch (8 ft) are the building's
primary module (controls D06/D09), so it registers with the column
prop's 24 ft bay and with any shell built to the same controls.

## QC (2026-10-26)

- All three renders were viewed against Plate XII: the front
  (section) view shows the two 2½-to-1 slopes, the ridge piece and
  both gutter channels in the Fig. 1 arrangement; the side elevation
  shows the 27-bar rhythm with the three wider strong bars at 4 ft,
  12 ft and 20 ft; the three-quarter view shows the pane/bar lattice
  reading pale and fine, as in the Talbot interior photographs.
- First render pass defects, both fixed and re-rendered: (1) the
  backdrop was a thin box whose edge drew a black horizon line across
  all three views — replaced with a single large plane; (2) the
  backdrop box was accidentally included in the first `.glb` export
  (selection side-effect of creating it) — export now deselects
  everything before selecting the Model collection, and the exported
  `.glb` was re-checked to contain only panel objects.
- Counts from the built model: 113 objects (2 gutters, 1 ridge,
  54 sash bars, 56 panes), **2,388 triangles** — well under the
  ~50,000-triangle prop budget. Overall size 2.583 × 7.315 ×
  0.654 m as tabled above.
- The `.blend` opens in Blender 4.5.3 and the script re-runs
  end-to-end (factory reset → build → save → export → renders).

## Files

- `hp-roof-furrow-bay.blend` — collection `Model` plus a
  `RenderSetup` collection (backdrop, lights, cameras; not exported).
- `hp-roof-furrow-bay.glb` — `Model` collection only.
- `build_hp_roof_furrow_bay.py` — the re-runnable build script.
- `renders/front.png`, `side.png`, `three-quarter.png` — neutral grey
  backdrop, same lighting, 960×640.
- `refs/` — the four Downes plates, two interior photographs, three
  Plate XII detail crops, and `REFERENCES.md`.

## Relationship to hp-glazing-and-sash-panel

This prop was built in parallel with `models/hp-glazing-and-sash-panel/`
(shipped by the other Muse stream) and is NOT a replacement for it.
That prop is one flat row of panes (5 panes, no gutters or ridge — its
NOTES leaves gutters/ridge to "separate scene-builder work"). This prop
is the complete furrow across a full 24 ft bay: both slopes, the timber
ridge piece and both Paxton gutters, with the sash-bar chain taken from
Plate XII Fig. 3. Use the row prop for repeated glazing runs; use this
bay where the gutter/ridge construction itself is the subject
(CP013, CP014, CP016).
