# Glazing wagon — NOTES

Hyde Park 1851 **construction only** (film scenes CP010/CP013). The glaziers'
"glazing waggon": the movable platform designed by Charles Fox (of
Fox, Henderson & Co., the building's contractors) that ran along the roof
gutters of the Crystal Palace, letting its crew lay the ridge-and-furrow roof
panes at a much higher rate than scaffolding allowed. **Wagon only — the crew
is not modelled** (people are not props).

## Source

- `references/muse-drive/images/commons/Glazing_waggon.png` — engraving,
  three-quarter view of the wagon on the roof with its crew of four.
  **Public domain** (repo manifest: Wikimedia Commons, "Public domain";
  manifest description: *'A "glazing waggon" — a movable platform designed by
  Charles Fox for the Crystal Palace building, allowing glass panes to be
  installed at a much higher rate than previously.'*) Copied into `refs/`.
- This is the **only** view of the wagon in the collection. No dimensioned
  drawing of it exists in the references.

## What the engraving shows (seen)

- A rectangular boarded platform; the planks run lengthwise.
- A deep side beam along each long edge, carrying a visible row of bolt heads.
- **Four** arched hoops of thin iron rod over the platform, roughly evenly
  spaced, springing at deck level along both side edges, their crowns roughly
  level with a near-straight run at the top (read here as a crown bar tying
  the hoops together).
- A raised end board (upstand with a ledge strip) at the near end of the deck.
- The wagon sits on the glazed roof at the foot of the slope it is glazing;
  the ridge-and-furrow slope runs away below/in front of it.
- The wheels are **almost entirely hidden** behind the roof slope — only the
  under-frame line and small fittings below the side beam can be seen.

## Dimensions — all inferred (no measured source)

| Item | Value | Basis |
|---|---|---|
| Deck | 3.66 × 2.44 m (12 × 8 ft) | Width adopted as one ridge-and-furrow slope module: the roof's furrow pitch, built up from the printed sash-bar centres of 10½ in and 49 in panes (Downes Pl. XII — see `hp-glazing-and-sash-panel/` and `hp-roof-furrow-bay/`). Length from crew scale: a prone glazier (≈1.6 m) spans about 45% of the deck in the engraving. |
| Deck top height | 0.60 m | Shallow timber underframe over 0.30 m wheels, matching the low stance in the engraving. |
| Hoops | 4 no., span 2.44 m, rise 1.50 m, rod Ø 32 mm | Count and span seen; rise scaled from the seated crew (seated figure ≈ 0.9 m above deck; crown ≈ 1.65× that). Profile is a smooth ellipse. |
| Crown bar | Ø 26 mm | Read from the level crown run in the engraving. |
| Wheels | Ø 0.30 m, gauge 1.98 m, wheelbase 2.80 m | **Conjectural** — see below. |
| End upstand | 0.26 m above deck | Scaled against the seated figure beside it. |

**Wheel-gauge reasoning.** The wagon ran in/along Paxton's gutter at the foot
of each roof slope. The gutter's own profile is not dimensioned anywhere in
the references, and the engraving hides the wheels, so the running gear is
the weakest part of this model: plain dished disc wheels of 0.30 m (a
plausible minimum for a loaded timber platform of this size) on a 1.98 m
gauge, inset under the frame so the wheel lines track within the wagon's
footprint along the gutter line, each with a shallow inner flange. Treat the
whole undercarriage as period-plausible inference, not observation.

## Measured vs guessed

- **Seen:** hoop count (4), lengthwise plank deck, deep side beams with a row
  of bolt heads, end upstand at the drawn end, hoops springing at deck level,
  level crown run, low stance on the roof.
- **Guessed:** every absolute dimension (chain in the table above), the wheel
  design, diameter and gauge, the underframe and axle arrangement, plank
  count (7), bolt count and spacing (6 per side, echoing the engraving's
  row), hoop rod and crown bar diameters, and the plain far end (barely
  visible in the engraving; no upstand is modelled there).

## Known inaccuracies

- Wheels and flanges are conjectural — hidden in the only surviving view.
- Hoop profile is a smooth ellipse; the engraving's bows may have a flatter
  crown where they meet the crown bar.
- Modelled level on flat ground; in use the wagon sat at gutter level on the
  roof, beside the slope being glazed.
- No glass panes, tools or crew are included. (The hoops are often described
  as protecting the pane load, but no stacked panes are legibly shown in the
  engraving, so none are modelled.)

## Build

Procedural Blender Python (`scripts/build_glazing_wagon.py`), Blender 4.2,
real-world metres, origin at base centre, scale applied. 65 objects,
**5,716 triangles** (evaluated count; matches the shipped .glb).
Renders on one fixed neutral-grey rig (`scripts/render_glazing_wagon.py`);
`renders/compare-engraving.jpg` sets the three-quarter render beside the
engraving.
