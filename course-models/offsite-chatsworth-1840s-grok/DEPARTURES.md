# DEPARTURES — O-CHATS (CP003, CP004) Chatsworth

| id | decision | why | grade |
|---|---|---|---|
| CH01 | Great Stove as 277×123×67 ft arched laminated-timber rib hall (23 ribs), ridge-and-furrow glazing, dwarf brick wall, central path | Paxton's Great Conservatory (Great Stove) at Chatsworth, 1836–40; demolished 1920. Dimensions from contemporary accounts. | A |
| CH02 | Lily house 61×49 ft with ~33 ft circular tank, ridge-and-furrow on hollow iron columns, offset to x=200 ft in the same .blend | Victoria regia house 1849–50; tank size from contemporary reports of the giant waterlily display. | A |
| CH03 | Victoria regia pads (~4–5 ft) with upturned rims; radial + concentric underside ribs | Leaf morphology from botanical plates; ribs are the structural lesson Paxton took to the Crystal Palace roof. | A |
| CH04 | Turned-over leaf on a trestle for the underside + CP004_learning shot linking leaf ribs to the roof | Staging: CP004 "learning to repeat". A leaf was exhibited this way. | B |
| CH05 | Tropical planting as simplified palms + underplanting boxes (not a full botanical inventory) | Staging density for an interior view. | C |
| CH06 | Stove walk ledge at 4.05 ft — cameras at eye 5.25 over that surface (z=9.3) | The dwarf wall raises the floor; eye grammar is over the standing surface. | B |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| CH03 | Warmer glass/iron (iron 0.07, paint cream 0.62/0.55/0.42, glass tint mix 0.14); world strength 0.28 + haze; lily fill AREA + leaf emit; exposure −0.15 | Review: bleached studio look; lily pads underlit | B |

## Look — crystal-palace-look v1 (2026-10-27)
Shared grade from `/workspace/crystal-palace-survey/look/` (AgX Medium High Contrast, Nishita-family MULTIPLE_SCATTERING sky + haze, era white-balance, mid-grey exposure table, glass/white-iron albedo ceilings). Render scripts import via `cpl_look.py` and call `apply_look` before rendering. Hero tiles re-rendered lean (24 spp, 1280×720). See `look/README.md` for Sydenham adoption.

## CP004 lily house CANDIDATE 2026-11-16 (Grok; not live, no verdict) — `rounds/candidates/ch02_cp004lily.blend`
State: Victoria regia house, Chatsworth, **spring 1850** (completed house; 1849-50). Sources: Gardeners' Chronicle 1850 description as summarised in thegardenhistory.blog (14 Jul 2018, "Joseph, Victoria and the amazing leaf") and WIT Trans. Built Env. DN100071 "Victoria regia's bequest to modern architecture" (plan 61 x 49 ft [alt. 62 x 54], tank 33 ft [alt. 40], 37 in masonry base, 30 low-level openings, 8 corner ponds, 4 small water wheels); Chadwick (8 hollow cast-iron columns doubling as drainpipes).

| id | decision | why | grade |
|---|---|---|---|
| CH07 | Columns cut from 14 (12 ft grid; 4 standing in the tank water, 4 more just outside the coping at r 17.0 ft) to **8 hollow cast-iron columns**, two rows of 4 at y = ±19.5 ft, x = ±7.5 / ±22.5 ft, all clear of the tank (nearest r = 20.9 ft) | Chadwick: "no support other than 8 hollow cast iron columns". Count is sourced; the 2 x 4 layout is inferred (no measured plan seen) | B (count A, layout I) |
| CH08 | Base raised/lowered to **37 in** masonry + 3 in stone sill (was 3.5 ft brick dwarf wall); 30 low-level vent grilles on its inner face (9 per long wall, 6 per short wall) | DN100071: base 37 in, 30 low-level openings. Spacing inferred (even) | A (spacing I) |
| CH09 | Walls rebuilt as **one repeated iron-and-glass module**: 4 ft bays (15 long, 12 short), 3 sash bars per bay (1 ft panes), sill/transom (9.5 ft)/head rails, cream paint, eaves 16.0 ft. Was: no wall glazing at all above the dwarf wall | "He repeated the simple iron and glass module that formed its walls" (Gardeners' Chronicle via blog). Bay size, pane width, transom and eaves height inferred | B |
| CH10 | Roof rebuilt over the **full plan** (old ridges stopped 6.5 ft short of each side wall): flat ridge-and-furrow, 8 bays of 7.625 ft across the 61 ft length, ridges + furrows running across the 49 ft depth, ridge 1.55 ft above gutter (≈1:2.5), sash bars ~1 ft, timber Paxton gutters on two lattice girder lines over the column rows, gutters trussed with an iron rod + 2 struts per span | Ridge-and-furrow is sourced; the 8 ft Crystal Palace module and the trussed gutter are the Crystal Palace pattern used as a stand-in. The 39 ft gutter span over the tank is long for a timber gutter: flagged | I |
| CH11 | Tank rebuilt as a true circle: **33 ft** water diameter, stone coping 2.55 ft, water at 2.05 ft (was 32 box segments, coping blocks with gaps, water disc r 16.1) | Tank 33 ft (Gardeners' Chronicle [10]); coping profile inferred | A (profile I) |
| CH12 | Tank water: new **dark still water** material (CP4_TankWater, no emission) instead of the live CH_Water (emissive cyan "pool" look). Live CH_Water not edited (still used by nothing visible in the candidate lily house) | The emission was a lighting cheat from ch02 ("lit lily pads"); a heated tank of soil-bedded water reads dark and reflective | B |
| CH13 | Victoria leaves rebuilt: **one plant**, 19 leaves 3.6-5.1 ft across in rings round the crown, lying on the water, low upturned rim 0.13 ft (red outer face), drainage notch facing the crown, faint quilted veins; 2 young red leaves (rim 0.08 ft) by the crown; 2 flowers (white first-night, pink second-night). Old pads were radius 3.8-5.2 ft (= **7.6-10.4 ft leaves**: radius used as diameter, CH03 says 4-5 ft) and floated 0.56-0.85 ft above the water | Leaves 4 ft 5 in by 15 Oct 1849, "five feet" quoted (DN100071; OSCOV). One plant in 1849-50. Leaf count / arrangement inferred | B |
| CH14 | 8 small **corner tanks** (2 per corner) with Nymphaea pads + flowers, Nelumbium leaves on stalks, a Pontederia clump | DN100071: 8 smaller ponds in the corners with Nymphaea, Nelumbium, Pontederia. Tank sizes (≈6 x 4-7 ft) and planting inferred | B (sizes I) |
| CH15 | The turned-over leaf on its trestle stands in the tank water (live CH04). Not moved; tagged `only_cams = CP004_lily_underside,CP004_learning` (existing render_views mechanism) so it is not drawn in the hero. The 4 lily-house figures stood in/on the tank (live): moved to the far walk (y 18-18.6 ft) | Physical clash in the hero; scoped fix only. The two detail cams still show the trestle in the water (pre-existing) | C (staging) |
| CH16 | Lawn + gravel apron (7 ft) round the lily house outside the glass, x 100-300 ft (object `CP4_outside_turf_apron`); tagged only_cams for the 3 CP004 cams, and deliberately not named lawn/grass/gravel so the shared look does not re-tint/re-height its CPL_HorizonGround for every camera (first build did: CP003 stove horizon +10 luma) | The new glazed walls look out; live had a void beyond. Planting outside not modelled | C |

Not modelled: the 4 small water wheels (no dimensions found), heating pipes in the base, roof ventilation gear, internal shading. No dimension change made to the Great Stove (CP003).
