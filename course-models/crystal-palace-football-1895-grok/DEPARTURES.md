# DEPARTURES — G-FOOTBALL (CP050, CP055)

| id | decision | why | grade |
|---|---|---|---|
| FB01 | Append Sydenham shell from `sydenham-1856-r13.blend` read-only (link=False); never edit the Sydenham folder | Reuse the park palace on the skyline. | A |
| FB02 | Drop north transept (lost 1866), waterworks sprays, Muse court props, and south-basin water near the pitch | 1895/1913 state; pitch sits in the drained south basin. | A |
| FB03 | Pitch ~110×70 m at centre (−158, −598, −47.5); natural bank on −y rising ~12 m; pavilion/stand on +y | Crystal Palace FC ground in the park; bank is the famous "natural terrace". | A |
| FB04 | Crowd as point-cloud + Geometry Nodes Instance-on-Points (low-poly variants). 1913 ≈ 120k at ~3.8/m²; 1895 quieter (~20k). Camera clear holes. | 1913 Cup Final attendance ~120,000; GN keeps the .blend manageable. | B |
| FB05 | Eye 1.6 m over the local bank/pitch surface (metres file); lenses 35 bank / 28 pitch-side | Camera grammar adapted to metres Sydenham space. | B |
| FB06 | Build flag `--state 1895|1913` (default 1913 for the Cup Final hero shot) | Two story beats, one script. | B |
| FB07 | Sink `park_slope` −20 m over the south basin; clear basin water/stone/sprays by bound-box centre (not origin) | Sydenham park_slope lids the basin at ~−45.9 above the pitch; origin-based delete missed world-baked meshes. | B |
| FB08 | check_set skips non-route (Sydenham) cameras and FB_Var/Crowd hits; 1895 state zeros crowd_1913 min | Appended shell otherwise fails eye/roll matching. | B |

## Quality pass 2026-10-27

| ID | Change | Why | Grade |
|---|---|---|---|
| FB04 | 36 hero figures near bank/pavilion/pitch cams; darker turf/bank albedo; turf strip on pitch | Sparse near-camera figures; flat green | B |

## People library v3.1 adopt (2026-10-27) — football crowds

| Shot | Era | Verdict | Note |
|---|---|---|---|
| CP050 bank 1895 | 1890s Victorian | REVERT | mid-ground stand reads darker/muddier vs before; grade otherwise OK |
| CP055 bank 1913 | 1910s→1890s stand-in | REVERT | overall grade brighter/washed; pavilion band darker |

### Departures
- 1913 uses 1890s bustle/boater stand-in (same as Sydenham late11) — no true 1910s day-dress set in v3.1.
- Crinoline hem capped ~0.9–1.0 m; lighter mid-tone skirts (shared survey `people_lib.py`).
- Heroes left at pre-adopt PNGs after keep-better revert.

## People library v3.3 adopt (2026-10-27) — football crowds

Retry of v3.1-reverted CP050/CP055 with people_lib 3.3 + `--keep-lighting`. Honest keep-better by viewing:

| Shot | Era | Verdict | Note |
|---|---|---|---|
| CP050 bank 1895 | 1890s | REVERT | pale/stony foreground vs varied before; stand muddier |
| CP055 bank 1913 | 1910s | REVERT | pale/ghostly bank + washout ~1.12×; contrast lost |

Heroes left at pre-adopt PNGs. Pairs under `people_v33/previews/`.

## People library v3.4 — close-up gate (2026-10-27)

Synced people_lib 3.4 (`CLOSE_UP_FRAME_FRAC`). No football keeps this round (CP050/055 already reverted).

## set_v18 CP050 bank set attempt (2026-10-27)

- **D-FB-01 I** CP050 pitch/bank/boards/goal mats rebuilt (fb03 → fb03b: thin chalk stripes, bank mottling, stand roof). `KEEP_LIGHTING` (exposure 0). Pair `set_v18/previews/CP050_set_fb02_vs_fb03.jpg`. **REVERT by eye** — AFTER washed terrain/trees toward clay beige; not clearly better. Best remains `renders/fb02_1895/CP050_bank_1895_start.png`.

## CP050 FA Cup Final 20 April 1895 CANDIDATE (2026-11-16, not live, no verdict)

On live `rounds/fb02_1895.blend` (d8b263c0, unchanged) -> `rounds/candidates/fb02_1895_cp050cup.blend` by
`scripts/candidate_cp050_cupfinal1895.py`; renders `scripts/render_cp050_candidate.sh`; pairs `scripts/make_cp050_pairs.py`;
checks `checks/check_cp050_cupfinal.py` (20/20). Cameras not moved; lights, world and exposure untouched. Placeholders hidden, never deleted.

| ID | Decision | Source / why | Grade |
|---|---|---|---|
| D-FB-CP050-01 | State = Saturday 20 April 1895, first FA Cup Final at Crystal Palace: Aston Villa 1 West Bromwich Albion 0, attendance 42,560, referee John Lewis, "a beautiful spring day"; collection `FB95_cup_final__1895-04-20`. Never mixed with the 1913 state (CP055 stays on `fb02.blend`). | Wikipedia "1895 FA Cup final" (RSSSF; Gibbons 2001 p. 268 for the weather). | A |
| D-FB-CP050-02 | Goals moved from the 110 m lines to the 70 m lines (x = CX +- 55): the fb01 pitch was 70 m long x 110 m wide (110 m = 120 yd is over the 100 yd maximum breadth; 70 m = 77 yd is under the 100 yd minimum length). Now 120.3 x 76.6 yd, inside the 1891 Law 1 limits; the natural bank and pavilion become touchline stands, as in Cup Final photographs. fb01 `FB_Post_*`/`FB_Bar_*` hidden. Exact Crystal Palace pitch size not found. | IFAB 1891 Law 1 (englandfootballonline.com IFAB1891): length 100-200 yd, breadth 50-100 yd. | B (size I) |
| D-FB-CP050-03 | Goals 8 yd x 8 ft (7.315 x 2.438 m), square posts 5 in, white paint; Brodie-type nets, 1.8 m deep at the ground and 0.9 m at the bar, translucent cord material. | 1891 Law 1 (8 yd apart, bar 8 ft); goal nets first used at the 1892 FA Cup Final (thepfsa.co.uk "Football Pitch & Ball Dimensions"); 5 in maximum only written in 1902 (IFAB 1902 minutes); paint colour and net depth I. | B |
| D-FB-CP050-04 | Markings per the 1892 plan: 12 yd line across the full width, 6 yd quarter-circles from each post joined by a straight line 6 yd out, existing 10 yd centre circle kept; fb01 `FB_Halfway` (drawn along the long axis) hidden, and no halfway line drawn (it enters the Law only in 1902). Four corner flags, 5 ft staffs, red flags. 1 yd corner-kick arcs not drawn (sub-pixel here). | IFAB Llandudno 13 Jun 1892 (playupliverpool.com 14 Jun 1892: plan shows "the twelve yards line (the eighteen yards line being abolished), the six yards radius at each goal-post, and the corner kicks radius"); 1891 law (centre mark + 10 yd circle); nachspielzeiten.de Law 1 chronology (halfway line 1902; flags 1863, 5 ft staff 1902); flag colour I. | B |
| D-FB-CP050-05 | Kits: Aston Villa claret jersey with light-blue sleeves (the neck band is not modelled); West Bromwich Albion blue-and-white vertical stripes (5.5 cm painted bands, navy shade); both teams white knickerbockers, dark stockings, black boots. | historicalkits.co.uk Aston Villa (claret + contrasting light-blue sleeves, regular first choice from 1894) and "History of Football Kits part 2" (WBA early adopters of vertical stripes, c.1885; white or dark-blue knickerbockers usual). Stripe width, stocking colours I. | B |
| D-FB-CP050-06 | 22 players in two 2-3-5 shapes, Villa attacking the east goal a few seconds into a move; ball 0.222 m (27-28 in circumference) at the Villa inside-right. Bodies are people_lib v3.4 `today_casual_m` HBM meshes repainted by height band (no modelled kit); the library's arms-out "walking" pose is used as running. | 1891 Law 1 (ball 27-28 in); formation and moment I. | I |
| D-FB-CP050-07 | Officials: referee (object named for John Lewis) in dark jacket and trousers on the field; two club linesmen with hand flags on the touchlines (umpires became linesmen in 1891). | Wikipedia 1895 final (referee); thepfsa.co.uk (referee on the field, linesmen instead of umpires); dress I. | B |
| D-FB-CP050-08 | Crowd figures: 25 people_lib v3.4 1890s mid-LOD variants: 11 cap men (`1850s_workman` base with the smock recoloured as a dark sack coat: the stand-in for the working man's jacket and flat cap), 10 boater men (`1890s_gentleman`, frock with tails), 2 top hats (`1850s_gentleman`), 2 women (`1890s_lady`, bustle + boater); about 44/40/8/8 %. On copies of the meshes only: hats lowered 4.5-6 cm so they sit over the cranium (v3.4 perches them on the crown), scalp and nape painted as hair, and the rust-pink waistcoat trim on men turned into dark cloth (it showed as a jagged band above the coat from behind). people_lib itself is not edited. | Crowd photographs of Crystal Palace finals c.1895-1905 show mostly men in caps, bowlers and boaters (I: proportions; no bowler mesh in the library, so caps and boaters stand in). | I |
| D-FB-CP050-09 | 42,532 GN instances + 28 swapped heroes = 42,560, the official attendance: natural bank 24,900 plus a top-up of 214 (north rail had only 886 of its 1,100 places), end banks 5,000 each, behind the goal lines 2,232, north touchline rail 886, stand 3,700, pavilion floor 600. Jittered grid 0.55-0.62 m (about 3 per m2), every point raycast onto the actual bank/stand/apron mesh (the fb01 banks have downward face normals, so the test uses abs(n.z)), facing the play (+-0.35 rad), scale 0.96-1.04. Clear wedges: CP050 bank lens 9 m at +-50 degrees (plus 1.5 m round the eye); pavilion lens 6 m. fb01 `FB_Crowd_1895` (7,873 three-box blocks) hidden. | Attendance from D-FB-CP050-01. The split between banks is I: no 1895 ground plan has been found yet (BUILD-PLAN still lists "Football ground plan, 1895 and 1913" as a gap). | B (split I) |
| D-FB-CP050-10 | The 20 bank and 8 pavilion heroes (1851 lathe crinolines and frock coats) get people_lib 1890s variant meshes at the same positions and are turned to face the play (they faced -y, so the bank ones looked into the CP050 lens and the pavilion ones away from the pitch). The 8 `FB_Hero_pitch_*` visitors standing on the pitch during the match are hidden. | Period dress (1851 crinolines are wrong for 1895); spectators off the field of play. | B |

Not changed (known, out of scope): two suns (FB_Sun 2.6 + the appended Sydenham `sun` 2.2) with AgX wash dark wool to pale grey at exposure 0; fb01 pavilion and stand are box massing; the 1854 railway colonnade on the left skyline reads pink and elevated (Sydenham append, read-only).
