# Egyptian Court colossi — build notes

**What it is.** The pair of colossal seated pharaoh statues (Abu Simbel type —
Ramesses the Great) that fronted the Egyptian Court at the Sydenham Crystal
Palace, facing the nave, on their shared pedestal. Film state: **SY-EARLY,
c.1856**; storyboard scene **CP038**. Built by Muse from the repo's own
reference collection, per `MUSE-PROMPT.md` §2.

## Sources used

| Source (repo path) | What was taken from it | Licence |
|---|---|---|
| `references/image-leads/uxqanywewcl.jpg` (copy in `refs/`) | The only photograph of the pair in the collection: frontal view from the nave. All proportions, the pedestal front, and every visible detail come from this image, measured against a grid overlay. | **Not recorded in the repo** for this lead image (it appears in neither `references/muse-drive/data/manifest.csv` nor the review `catalogue.json`). Copyright status unverified here — check before reuse outside the course. |
| `references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900414).jpg` and `...(147900416/417/418/420).jpg` — 1856 *General Guide Book*, Egyptian Court chapter, printed pp. 46–50 | p.47: ground plan of the Egyptian Court; p.50: the statement that "the gigantic figures in the northern transept" are the size of the sitting figures of the original temple of Aboo Simbel, "and the smaller ones around, his mother, wife, and daughter". p.48's engraving ("The Gigantic Figures of Rameses the Great") shows *standing* figures — a different feature, not used for this model. | Public domain (per `references/muse-drive/review/shortlist.csv`) |
| `references/muse-drive/review/dimensions-from-1856-guide.json` | Checked: it records building dimensions only (lengths, nave/transept heights). **No dimension for the colossi exists there or elsewhere in the repo that I could find.** | — |
| `models/CANDIDATES.md` (candidate #9) | The brief for this prop. | — |

No other view of the colossi exists in the downloaded collection: a manifest-wide
search for Egyptian Court / colossi / Abu Simbel material returned only this
photograph and the guide pages above.

## Dimensions — and where each number comes from

- **Statue height 20.0 m** (plinth top to crown top) — **INFERRED, but
  corroborated.** No repo source states a figure. Two independent lines agree:
  (1) the 1856 guide, p.50, states the northern-transept figures are *the size
  of* the original Abu Simbel sitting figures; (2) measuring the photograph:
  statue height = 7.1 × the height of the doorway in the pedestal front, and
  that doorway (width:height ≈ 0.81, a grand double doorway) at 2.8 m gives
  19.9 m. Built at 20.0 m.
- **Pedestal 5.9 m high × 17.2 m wide** — ratio to statue height measured from
  the photograph (0.296 and 0.86 respectively). **Pedestal depth 9.8 m —
  GUESSED** (front elevation only; enough to contain the throne depth plus a
  margin behind).
- **Statue internal proportions** — measured from the photograph with a grid
  overlay: chin at 0.76 H, beard bottom 0.61 H, waist 0.47 H, knee top 0.38 H,
  knee spread 0.33 H, nemes width 0.29 H.
- **Statue depth ≈ 7.7 m** (back slab to toe tips) — **INFERRED** from the
  Abu Simbel seated type; no side elevation survives in the collection.
- **Small figures 2.8 m (between the legs) / 4.7 m (sides and centre)** —
  measured height ratios from the photograph.
- Whole model: 17.7 m wide × 10.3 m deep × 26.35 m high (incl. pedestal
  cornice overhang). Origin at the centre of the pedestal base; metres;
  scale applied.

## Seen in the photograph vs guessed

**Seen (modelled as shown):** the pair side by side, nearly touching, on one
shared pedestal and plinth; tall rounded crown over a striped nemes whose
wings fall to the shoulders; prominent ears; long, broad, horizontally banded
false beard reaching the chest; broad collar; oval cartouche medallion on the
chest; cartouche plates on both upper arms; arms vertical, forearms resting
on the thighs, hands flat on the knees with separated fingers; shendyt kilt;
feet with separated toes; five small standing figures (one between each
statue's legs, one at each outer side, one between the pair — the guide's
"mother, wife, and daughter" group, though which is which is not identifiable);
pedestal front with a plain upper band, a row of small square openings, a
lower band of vertical slots, and a central doorway interrupting the pattern.

**Guessed / inferred (no source in the collection shows it):** everything
about the sides and back — throne depth and side profile, the recessed panel
on each throne side (its border follows the sliver visible at the statues'
outer edges in the photograph; the panel is deliberately left blank), the
back of the nemes, the kilt's side form, the pedestal's sides and back
(modelled plain), and the doorway's interior (the pale board inside it is a
conjectural reading of a light rectangle in the photograph).

## Known inaccuracies

- This is a **stylised block construction** (procedural boxes, frustums and
  lathes), not a sculpt. Faces are schematic — brow bar, nose wedge, almond
  eye plates — and there is **no carved detail and no hieroglyphic text
  anywhere, deliberately**: the sources do not let me read any inscription,
  so none was invented.
- The Sydenham figures were **painted** reproductions; the model is a fairly
  uniform sandstone. The photograph suggests paler hands and feet, kept here
  as a slightly lighter stone; full polychromy is not attempted.
- The crown's frontlet is simplified to a uraeus and disc; in the photograph
  it looks more elaborate than this resolution can settle.
- The small figures are generic robed standing figures; their dress and
  headgear are not legible in the photograph.
- Depths are the softest numbers here (see above). If a side elevation or a
  stated height for the Sydenham pair ever surfaces, the model should be
  re-proportioned against it.

## Build

Blender 4.2, fully procedural bpy — `scripts/build_colossi.py` rebuilds the
model, saves the `.blend`, exports the `.glb`, and renders the three views
with one fixed lighting rig (Eevee, neutral grey backdrop).
**Meshes: 286. Triangles: 30,232** (within the prompt's ~50k prop budget).
Overall size 17.7 × 10.3 × 26.35 m.
