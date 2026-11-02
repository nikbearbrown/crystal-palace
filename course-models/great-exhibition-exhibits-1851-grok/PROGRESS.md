# PROGRESS — hero exhibits (Grok Bot)

## e01 — 2026-10-26/27 (branch grok-exhibits-1851, local commits only)
- Built three standalone asset collections: `EXH_KOHINOOR` (CP025), `EXH_OSLER_CANDELABRUM` (CP025 luxury), `EXH_NASMYTH_HAMMER` (CP024, animated ram).
- Preview showroom stand + 8 cameras (eye 5.25 ft, no roll, 35/50 mm). Placement helper `place_exhibits.py` + `place_test.sh` (east block-outs via transept r10, west nave via Claude's model appended read-only at render time).
- D-checks: **19/19** (`checks/e01/checks.md`).
- Preview fixes: exposure (-0.2 → -2.0), asset collections excluded from view layer (double render), visitors off camera axes, diamond enlarged to 186 ct, hammer base 15.1 → 14.5 ft, piston rod inside cylinder, Osler/ram cameras pulled back, crimson drape behind Osler, hammer label moved off the ram sightline.
- Placement test: clash preflight clear for all three spots after moving Koh-i-Noor off the K43 statue and Osler off the locomotive; host md5 identical before/after.
- Renders: `renders/e01/` (1280x720, 48 samples) + `renders/e01/placement/`.

### Self-score e01: 7/10
Misses: the stone itself is a few pixels in CP025_case (period-correct, but a 50 mm detail cannot make it read — needs a macro/insert proposal); Osler glass is a simple transparent shader (no dispersion/caustics, prisms read as rods); hammer is massing-level (no valve-gear linkage detail, no forging, no engine-man action); figures are the shared low-poly kit; showroom is a stand, not a court.

### Next
1. EX10 variant: July crimson enclosure with gas jets (ILN 1851) as a switchable state.
2. Koh-i-Noor insert camera (ask for an 85/100 mm exception or a 50 mm inside-the-rail "attendant's view").
3. Osler: second candelabrum of the pair, faceted prisms with dispersion; place in the Central North Gallery once a gallery host exists.
4. Hammer: valve-gear linkage, steam puffs on the exhaust per blow, red-hot billet variant; place in the NW machinery court block-out.
5. Applegath vertical press as the second CP024 machine.

## e02 (2026-10-27): Osler glass faceted prisms + sparkle
- glass(sparkle=True) Coat/Emission; 6-sided prism drops. DEPARTURES EX20. Checks 19/19.

## e02 remainder (2026-10-27): July crimson Koh-i-Noor + steam on hammer blows
- Parked e02 remainder cleared.
- July enclosure: crimson panels, 6 gas jets, diamond emit (EX10 B). Steam puffs on ram impacts (EX13 C).
- Route: `CP025_july`; lean renders include `CP025_july_start.png`, `CP024_ram_start_f025.png`.
- Checks: 19/19. COVERAGE best paths → july / ram_f025.

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## people/material 2026-10-27
- people v3.1 keep CP024; revert CP025; lib 3.1

## people v3.2 2026-10-27
- people v3.2: revert CP024

## Hero CANDIDATE CP025 Koh (2026-10-27)
- Audit: Koh-i-Noor diamond 42-vert icosphere vs CP025 close-up screen time — second crudest hero.
- CANDIDATE: `scripts/polish_koh_cand.py` rebuilds pre-1852 Mughal/rose-cut diamond (170v/336f hard facets) + gilt ribbon/bead-ring cage enrich → `rounds/candidates/e02_koh.blend` + `renders/candidates/CP025_july_start.png` (--keep-lighting). Live e02 untouched.
- Pair: survey `look/pairs_geo/CANDIDATE_CP025_koh_july_start_pair.png`.
- Muse `cut-glass-chandelier` / `glass-topped-display-counter` noted for CP019/CP025 dressing but not in CP025_july frame; not appended this pass.

## CP025 Koh REJECT v1 → CANDIDATE v2 (2026-10-27)
- User REJECT: ribbons messy; diamond invisible; pole/crop.
- New candidate `rounds/candidates/e02_koh_v2.blend`: no ribbons; hide OSL_shaft_prisms; reframe CP025_july_start (50 mm, eye 5.25 ft, no roll, whole cage); emission + point-light sparkle (EX_KOH_SPARKLE); Muse counter skipped (EX_KOH_COUNTER).

## 2026-10-27 Koh CP025
- REJECT ribbons candidate. New CANDIDATE e02_koh_v2: no ribbons, open south, reframe 50 mm/5.25 ft, sparkle cheat (EX_KOH_*). Muse counter skipped.

## 2026-10-27 hero KEEP + next hero
- **KEEP** Koh-i-Noor v2 → promoted live `rounds/e02.blend` (`scripts/promote_koh_live.py`). Pair keep-record: survey `look/pairs_geo/CANDIDATE_CP025_koh_v2_july_start_pair.png`.
- Sparkle polish **CANDIDATE** (clearly brighter stone): `rounds/candidates/e02_koh_sparkle.blend` + `renders/candidates/CP025_july_start_sparkle.png`. Pair: `CANDIDATE_CP025_koh_sparkle_july_start_pair.png`. Live unchanged.
- Organ/gates gate: Willis/Gray&Davison organ only in storyboard CP045 (Sydenham); Coalbrookdale gates not in storyboard → skip.
- Next-crudest HP hero by screen time: **Nasmyth hammer CP024 CANDIDATE** `rounds/candidates/e02_hammer.blend` + `renders/candidates/CP024_ram_start.png` (`scripts/polish_hammer_cand.py`). Pair: `CANDIDATE_CP024_hammer_ram_start_pair.png`.

## 2026-10-27 Koh sparkle REJECT + hammer court CANDIDATE
- **REJECT** Koh sparkle — no visible difference; keep v2 live. Pair → `REJECTED_CP025_koh_sparkle_july_start_pair.png`.
- **KEEP** Nasmyth hammer MODEL → promoted live `rounds/e02.blend` (`scripts/promote_hammer_live.py`).
- Setting wrong (outdoor sea horizon): **CANDIDATE** Machinery Court `rounds/candidates/e02_hammer_court.blend` + `renders/candidates/CP024_ram_start.png` (`scripts/polish_hammer_court.py`). Pair: survey `look/pairs_geo/CANDIDATE_CP024_hammer_court_ram_start_pair.png`.
- HP interior sea-horizon audit (report only): see commit message / agent report.

## 2026-11-01 HP interior envelope KEEP
- Today's re-renders of the envelope candidate were reviewed pair by pair.
- KEEP envelope for CP024_approach, CP025_visitors, EX_lineup.
- CP024_ram: v1 wide reframe REJECTED; v2 restores the live close camera inside the envelope (+0.3 exposure in `render_round.sh`) → KEEP.
- Promoted `rounds/candidates/e02_envelope_v2.blend` → live `rounds/e02.blend` (backup `rounds/e02.blend.pre_envelope_keep`).
- Departure: CP024 ram exposure is a per-shot cheat (+1.0 stop over the CP021-matched interior_daylit) because the hammer is backlit by the bright end wall.

## 2026-11-01 reference intake CANDIDATES (Muse, origin/main a62ba2e) — not promoted, no keep/revert call
Live `rounds/e02.blend` untouched (md5 ae5355a5…). Script `scripts/intake_muse_1101.py` (opens live e02, saves candidate only).
Renders: 28 spp, 1280×720; CP024_ram_start at frame 25 with `--exposure 0.3` (existing per-shot cheat). Fresh live baseline rendered with identical settings into `renders/candidates/live_20261101/` (renders/e02 predates the envelope KEEP).
- **e02_muse_hammer** (`rounds/candidates/e02_muse_hammer.blend`): our HAM_* hammer hidden (barrier + label kept); Muse `hp-working-machine-exhibit` appended unmodified as `EXH_MUSE_NASMYTH_HAMMER` at the same spot; text block `CREDIT_MUSE_INTAKE_1101`.
  Renders `renders/candidates/CP024_{approach_start,ram_start_f025}_muse_hammer.png`.
  Pairs `/workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP024_muse_hammer_{ram_start,approach_start}_pair.jpg`.
  Comparison: Muse is NOT clearly better — its standards splay outward as a V (rotation sign bug; its own notes/photo say A-frame), material reads pale grey, Tup is static (single-acting, no blow cycle). Built anyway as the requested candidate for judging.
- **e02_muse_dressing** (`rounds/candidates/e02_muse_dressing.blend`): boiler/engine/lathe block-outs hidden; Muse `vacuum-sugar-apparatus` at the boiler spot, `portable-steam-engine` at the engine spot (rot 200°), `seed-drill` at the lathe spot (rot 90°); press block-out kept.
  Renders `renders/candidates/CP024_{approach_start,ram_start_f025}_muse_dressing.png`.
  Pairs `…/pairs_geo/CANDIDATE_CP024_muse_dressing_{approach_start,ram_start}_pair.jpg`. Copper vacuum pan is cut by the left frame edge in approach_start; ram_start shows essentially no change.
- Departures logged in DEPARTURES.md (EX_MUSE_*).

## 2026-11-01 Muse intake: Grok Bot review
- All Muse intake candidates REJECTED after viewing the pairs (see survey look/pairs_geo/README.md). Live blends unchanged; candidate files kept for reference.

## 2026-11-02 CP024 Machinery Court stand dressing — CANDIDATE (not promoted, no keep/revert call)
Live `rounds/e02.blend` untouched (md5 ae5355a5… checked by the render script). Not a repeat of the rejected Muse hammer/dressing intake: hammer and block-outs unmodified; only stand dressing added.
- Script `scripts/polish_machinery_dress.py` (parametric: `--shaft-z`, `--no-people/--no-shafts/--no-rails/--no-placards`) → `rounds/candidates/e02_machinery_dress.blend`, collection `MCD_MACHINERY_DRESS_1851`, text block `CREDIT_MCD_CAND`.
- Adds per block-out stand (boiler, engine, press, lathe): green floor cloth + crimson kerb, turned stanchion rails with sagging rope, Catalogue class placards; north + south line shafts with hangers/brackets, pulleys and flat belts to press, lathe and an engine flywheel; 7 baked people_lib attendants/visitors in period dress. Refs: scans fig-21/29/30/48 (dressing/colour only).
- `scripts/render_machinery_cand.sh` rebuilds from live and renders before (live) and after with identical settings (28 spp, approach f1, ram f25 `--exposure 0.3`) into `renders/candidates/machinery_20261102/{before,after}/` and copies pairs to survey `look/pairs_geo/CANDIDATE_CP024_machinery_{approach_start,approach_end,ram_start_f025}_{before,after}.png`.
- Self-score 6/10. Approach_start reads most like fig-29 (flywheel+belt, rails, placards). Misses: ram_start change is mostly background (pale north shaft line behind hammer, pulley at left edge, CLASS VI board) — the hammer foreground is unchanged; placard sub-lines illegible at film res; boiler placard large and edge-cut in approach_start; attendants small/dark in wide shots and HBM style differs from VIS figures; block-outs still grey boxes, so the dressing frames placeholders; after frames ~5% darker in mean (added dark iron, same lighting).
- Departures EX_MCD_* in DEPARTURES.md.

## 2026-11-02 CP024 Machinery Court stand dressing — KEEP (promoted live)
Parent viewed all three pairs: KEEP for approach_start, approach_end and ram_start (approach shots clearly richer; ram mildly better, nothing harmful).
- Pre-promotion polish: boiler CLASS V placard nudged 1.0 ft east (new params `--boiler-placard-dx` default 1.0, `--boiler-placard-yaw` default 0 in `scripts/polish_machinery_dress.py`). In CP024_approach_start its left edge moves from 22 px to ~70 px (1920 px frame); it is off-frame in approach_end and ram_start. Kept (nothing worse; post now sits in front of the black stanchion, rope passes behind the board).
- `polish_machinery_dress.py` gained `--base` (default `rounds/e02.blend.pre_machinery_keep` when present) so rebuilds never re-dress an already dressed live.
- Old live backed up to `rounds/e02.blend.pre_machinery_keep` (untracked, md5 ae5355a5…, == git 5c4b55d e02). `scripts/promote_machinery_live.py` retags `MCD_*` candidate → keep (24 objects), renames the credit to `CREDIT_MCD_KEEP`, saves live `rounds/e02.blend`.
- Live CP024 renders (28 spp, 1920×1080): `renders/e02/CP024_approach_start.png`, `renders/e02/CP024_approach_end.png`, `renders/e02/CP024_ram_start_f025.png` (frame 25, +0.3 exposure cheat). `scripts/render_cp024_machinery.sh [--rebuild]` reproduces all three pixel-identically, from live and when rebuilding from the pre-KEEP e02 (tested 2026-11-02). Live approach_end / ram differ from the reviewed candidate after frames only by Cycles noise (max 11/255) from the off-frame placard move.
- `render_machinery_cand.sh` kept as the candidate record; its BEFORE side now renders the pre-KEEP base.
- renders/e02 jpgs and the other e02 pngs predate the envelope KEEP; only the three CP024 pngs above are current.
- Remaining misses: grey block-outs still placeholders; placard sub-lines illegible at film res; attendants small/dark in wides, people_lib style vs older VIS figures; ram_start change mostly background (pale north shaft line, pulley at left edge); frames ~5% darker in mean.

