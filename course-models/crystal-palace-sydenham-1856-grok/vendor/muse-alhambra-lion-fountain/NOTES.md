# NOTES — Alhambra Court lion fountain

Prop for the Crystal Palace film, scene **CP041** (the Alhambra Court).
**Sydenham 1854 only** — the Alhambra Court did not exist at Hyde Park.
Built by Muse (candidate #14 in `models/CANDIDATES.md`).

## What it is

The Fountain of the Lions at the centre of Owen Jones's Alhambra Court:
a dodecagonal basin carried on the backs of twelve standing lions,
a central column rising from the basin to a smaller fluted upper basin
with a jet, and the court's low stepped plinth. All water (basin and
upper-basin surfaces, the jet, eight overflow arcs from the upper bowl,
and the twelve lion-mouth spouts) sits in a **`Water` collection** /
`Water_*` objects so the scene builder can hide it as one set.

Origin at the base centre; units metres; scale applied.
42 objects, **32,348 triangles** (evaluated, lions counted ×12).
Stone footprint 3.60 m (step ring); overall scene extent 3.73 × 3.73 m
(the extra 0.13 m is the mouth spouts landing at the step's edge);
height 2.30 m to the nozzle, 2.78 m including the water jet.

## Sources used (all already in this repo — see `refs/`)

- **Coloured print, "Entrance to the Alhambra Court"** by Owen Jones
  (`references/muse-drive/images/commons/Crystal_Palace_Alhambra_Court.jpg`;
  manifest: **Public domain**). The fountain stands centre-left, seen
  through the entrance arch: standing lions with strongly ribbed
  manes spouting water from their mouths, a polygonal basin with a
  patterned fascia carried above them, an upper fluted drum and a
  tall sheet-like jet.
- **1856 guide, p.66** — woodcut of the same entrance view
  (`models/sy-alhambra-ornament-panel/refs/guide-1856-p66-entrance-woodcut.jpg`;
  the guide is public domain). Clearer than the print for structure:
  upper bowl on a stem with water falling in arcs into the main basin,
  the basin's moulded rim and fascia, lions in a row beneath it,
  mouth spouts falling to a low channel at the platform edge.
- **1856 guide, p.67** — "Ground Plan of the Alhambra": the fountain
  drawn as a many-sided polygon at the centre of the Court of the
  Lions, inside an octagonal ring path (the path is court paving and
  is *not* part of this prop).
- **1856 guide, pp.68–69** — text: "Entering through the central
  archway, we see before us **the fountain supported by the lions**
  that give name to the court"; "This court is **75 feet long**, just
  two-thirds the length of the original; the columns are as high as
  the columns of the Court of Lions itself, and the arches … of the
  actual size of the original arches"; and "Round the basin of the
  fountain is an **Arabic poem**" (p.69).

## Dimensions — what is measured, what is estimated

No dimensioned drawing or photograph of this fountain survives in the
collection (the print is 453 × 575 px with the fountain ~100 px wide).
The size is therefore an **estimate built as a chain**, stated so it
can be corrected if a dimensioned source surfaces:

1. **Court length 75 ft = 22.86 m** — printed in the 1856 guide (p.68).
2. **Basin diameter ≈ 2.6–2.7 m** — on the p.67 plan the fountain
   polygon measures ≈ 0.115 of the Court of the Lions' length
   (read off the plan image; ±15% at the plan's engraving tolerance).
   Adopted: **2.70 m across vertices / 2.61 m across flats**.
3. **Heights as fractions of basin diameter**, read off the p.66
   woodcut cross-checked against the coloured print: lion back at
   0.39 × Ø, basin rim at 0.49 × Ø (1.31 m), upper-bowl rim at
   0.80 × Ø (2.16 m), jet top ≈ 1.03 × Ø (2.78 m as modelled).
4. **The lions**: length 1.00 m nose-to-tail-base, 0.82 m to the back,
   ~1.00 m to the head top — scaled from their height in the views
   relative to the basin (they must reach the basin underside, which
   the guide's "supported by the lions" and both views require).

Everything else (plinth 3.30 m Ø / step 3.60 m Ø, column profile,
upper-basin Ø 1.15 m) follows the same view proportions. Treat all
absolute sizes as **±15%**.

## Modelling choices and known inaccuracies

- **The lions stand; they do not crouch or recline.** The CANDIDATES
  note called them "simple recumbent forms" and the guide quotes the
  basin poem's "Lions crouching", but both views in the collection
  show the Sydenham lions **standing on four legs, heads up**, in the
  Granada disposition. The model follows the views.
- **Twelve lions** — one under each basin side. Only the front arc
  (3–4 lions) is visible in either view; the count is an inference
  from the dodecagonal basin and the reproduced original's
  disposition, not a count from a Sydenham image.
- **The lion sculpt is deliberately schematic**: blocky masses,
  columnar legs, a mane of five horizontal ribs (the one surface
  trait both prints insist on), simple muzzle/ears/eyes, mouth slot,
  tail up the rear flank. Faces, paws and musculature are **not**
  resolved by the sources and are not invented beyond this.
- **Basin fascia**: the guide says the original basin carries an
  Arabic poem; the Sydenham print shows a patterned band but no
  legible characters. The band is therefore an **abstract stepped
  knot-block pattern** (procedural texture, `textures/fascia_band.png`),
  *not* letterforms — the same convention as
  `sy-alhambra-ornament-panel/` in this repo.
- **The upper basin** follows the print's fluted-drum reading
  (12 flutes) under a shallow bowl; the woodcut shows a plainer bowl
  on a stem. The two views disagree in emphasis (the print also makes
  the jet much taller); the model takes the woodcut's proportions
  with the print's fluting, and the jet at the woodcut's height.
- **Water is a display state, not evidence of flow rates**: arcs are
  placed where the views draw them (upper bowl → main basin; lions'
  mouths → step edge). Cross-sections are uniform tubes.
- **Colours** are the pale warm stone of the prints under a neutral
  studio rig; the court's actual paint scheme for the fountain is not
  recorded in the collection, and the lions may have been painted —
  no colour is asserted beyond "pale in both views".
- The plan's **octagonal ring path** around the fountain is court
  paving and is left to the court environment build, not this prop.

## Files

- `alhambra-lion-fountain.blend` / `.glb` — the model (Water in its
  own collection).
- `scripts/build_alhambra_lion_fountain.py` — the build (source of truth).
- `scripts/make_textures.py` — the fascia band texture.
- `scripts/render_rig.py` — the fixed neutral-grey studio rig.
- `scripts/make_compare.py` — builds `renders/compare.jpg`.
- `renders/` — front / side / three-quarter + print comparison.
- `refs/` — the coloured print and the enlarged measurement crops;
  the 1856 guide pages are listed in `refs/REFERENCES.md` (canonical
  copies live in `sy-alhambra-ornament-panel/refs/`).
