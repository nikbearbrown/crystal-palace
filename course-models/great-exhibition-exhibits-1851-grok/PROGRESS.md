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


## 2026-11-09 CP025 exhibit-court scan props — CANDIDATE built, then KEEP (see below)
Candidate stage: live `rounds/e02.blend` untouched (md5 a26776f5…, checked by the render script). Hyde Park 1851 only. CP024 not dressed (none of these props belongs in the Machinery Court).
- Props: origin/main e88ee17 `scan-models/blend/{fig-52_greek-slave, fig-54_elkington-jewel-cabinet, unnumbered_watherston-brogden-vase}.blend` read with `git show` into scratch `/workspace/tmp/cp025scan/src` (no checkout of main, scan-models/ never edited). `scripts/prep_scanprops.py` strips floating crumbs, decimates 1.40–1.46 M → 58,799/58,800/58,799 tris, rescales to catalogued heights (slave 1.655 m ×1.003; cabinet 0.97 m ×0.954; vase 0.457 m ×0.381), turns the print view to −Y, packs 1024 px textures → `assets/scanprops/*_hp1851.blend` (tagged `cp_state="Hyde Park 1851"`).
- `scripts/polish_scanprops_cand.py` (parametric: `--slave/--cabinet/--vase X,Y,YAW`, `--no-canopy`, `--no-rails`, `--marble-gain`, `--gold-gain`, pedestal/stand/canopy heights) opens live e02 read-only → `rounds/candidates/e02_scanprops.blend`, collection `SCN_SCANPROPS_HP1851`, credit `CREDIT_SCN_CAND`.
  - Greek Slave on a turned revolving pedestal (0.80 m) under a crimson canopy with gilt posts, brass/rope rail, at (−3.6, 1.7) W of the Koh enclosure (seen in CP025_visitors_start/_end). Marble albedo remapped to statuary white.
  - Elkington jewel cabinet on a crimson-clothed stand (0.78 m) with rail at (1.2, −6.2); W&B vase (gold remap) on a 0.95 m pedestal at (6.2, −8.6); both seen in EX_lineup_start.
- `scripts/render_scanprops_cand.sh` renders before (live) / after at render_round settings (28 spp, 1920×1080, frame 1, look v1 interior_daylit, people swap) into `renders/candidates/scanprops_20261109/{before,after}/`; `scripts/pair_luma.py` writes luma (whole frame + outside the prop mask) and labelled pairs. Pairs: survey `look/pairs_geo/CANDIDATE_{CP025_visitors_start,CP025_visitors_end,EX_lineup_start}_scanprops_{before,after,pair}.png`. CP025_july/case rendered as regressions only (noise-level change).
- Departures EX_SCN_* in DEPARTURES.md.

### KEEP 2026-11-09 (parent viewed all three pairs)
- Verdict: KEEP CP025_visitors_start, CP025_visitors_end, EX_lineup_start. Greek Slave under its red canopy behind the Koh-i-Noor cage reads and is period-correct; the Elkington cabinet and W&B vase dress the previously empty EX_lineup court. Exposure matched (whole-frame luma 25.07→24.75, 19.92→19.75, 56.01→53.26; parent's masked figures 26.33→26.04, 21.49→21.32, 56.75→54.19).
- Promotion: `cp rounds/candidates/e02_scanprops.blend rounds/e02.blend` (byte copy, NOT rebuilt). Live md5 a26776f5be0a9ec7fb0657033ef6a0de → fce122dabf730ae76b47d3cacf6d36b7. Old live → `rounds/e02.blend.pre_scanprops_keep` (untracked). SCN_* objects keep their `candidate=e02_scanprops` tag (no retag, to keep the file byte-identical to what was reviewed).
- `scripts/render_scanprops_live.sh` re-renders the three KEEP shots from live into `renders/candidates/scanprops_20261109/live/` and the other e02 shots from old and new live into `regress_old/`, `regress_new/` (untracked).
- Live vs candidate afters: max diff **1/255** on 37 / 44 / 56 pixels (not 0). Control: re-rendering the same candidate file gives max 1 on 47–58 px, so this is Cycles run-to-run noise on this box, not a content change; the files are byte-identical (`live_vs_after.txt`).
- Regression (old live vs new live, `regress.txt`): EX_osler_start max 15, CP024_approach_start 9, approach_end 7, ram_start_f025 9, CP025_july_start 21, CP025_case_start 23. Mean |diff| ≤ 0.11, luma within 0.4 %; the >12 pixels are speckle on the gilt cage highlights (indirect light from the new props/canopy). No visible change, but not pixel-identical. Note: CP025_july also depends on render order (people-swap state carries between cameras): the same old live gave max 7 against the 06:22 render.
- `renders/e02/`: CP025_visitors_start/_end and EX_lineup_start now = live/; CP025_july_start, CP025_case_start, EX_osler_start = regress_new/. CP024 PNGs left as the 2026-11-02 renders; `render_cp024_machinery.sh` now reproduces them only to noise (max ≤ 9), not pixel-identically.
- Misses: Elkington cabinet very dark, near-silhouette in EX_lineup_start; Greek Slave small and dim in the CP025 wides; vase height (18 in) unverified; generated meshes (unseen sides invented); vase uncased.

## 2026-11-09 CP025 scan props v2 — CANDIDATE built and rendered (not live, no verdict)
Goal (BUILD-PLAN CP025 row): lift Elkington cabinet out of silhouette; Greek Slave larger/brighter read under canopy (check height); verify W&B vase height + log; glass case on vase if sources show one; match exposure to live renders/e02.
Base: live rounds/e02.blend (md5 fce122da, = KEEP 68cfae5), opened read-only. Output: rounds/candidates/e02_scanprops_v2.blend. Renders: renders/candidates/scanprops_v2_20261109/{before,after}/. Pairs: survey look/pairs_geo/CANDIDATE_<shot>_scanprops_v2_{before,after,pair}.png.
- [10:05 UTC] started: reading sources + scene.
- [10:55 UTC] scripts/polish_scanprops_v2_cand.py written + tuned on quick renders (t1–t5 in /workspace/tmp/cp025v2). Light-linked fills (no floor pools). Next/resume: `scripts/render_scanprops_v2_cand.sh` (skips sides already rendered; FORCE=1 to redo), then commit worktree + survey pairs.
- [11:20 UTC] DONE. `scripts/render_scanprops_v2_cand.sh` built `rounds/candidates/e02_scanprops_v2.blend` (md5 f75234f3…) from live e02 (md5 fce122da, unchanged after the run) and rendered before (live) / after, 28 spp, 1920×1080, frame 1, same camera order both sides (the people swap depends on the order) into `renders/candidates/scanprops_v2_20261109/{before,after}/`. Before frames == renders/e02 live pngs within 1/255.
  - Changes: Greek Slave (position unchanged, true 1.655 m kept) gets a dark crimson velvet back curtain ("dark velvet niche", 1851 visitor's letter) + a light-linked 40 W fill under the tester, marble gain 1.8; Elkington cabinet retinted after the RCT photo (gilt/silvered electrotype, blue enamel: value ×2.2, metallic 0.35) + light-linked 200 W front-roof fill (cabinet only) and 50 W (stand only); W&B vase gold gain 2.6 + light-linked 60 W fill. No glass case (no source shows one). Departures EX_SCN2_*.
  - Luma (whole frame / outside the changed-pixel mask): visitors_start 24.74→24.57 (−0.69%) / 24.70→24.71 (+0.06%); visitors_end 19.75→19.50 (−1.26%) / 18.80→18.80 (−0.03%); EX_lineup_start 53.47→54.96 (+2.79%, the lit cabinet is the point) / 52.24→52.59 (+0.68%). Regressions CP025_july/case: +0.21% / +0.08%, ~1.3k px of noise speckle on the cage bars (sampling changes with the extra lights), no visible change.
  - Pairs: survey `look/pairs_geo/CANDIDATE_{CP025_visitors_start,CP025_visitors_end,EX_lineup_start}_scanprops_v2_{before,after,pair}.png`.
  - Heights: Greek Slave 165.5 cm (Raby, Di Bello) / 165.7 cm (Yale MAVCOR) — kept; W&B vase: no printed height in Official Catalogue vol. 2 (Class 23 no. 105, South Central Gallery), Art-Journal cat. p. 281 or Wyatt pl. LXVI; 95 oz 22 ct ≈ 166 cm³ → 18 in gives ≈0.57 mm mean wall, plausible (13½–19 in range for 1.0–0.5 mm); kept 0.457 m, still unverified.
  - Self-score 6/10. Misses: Greek Slave still partly hidden (legs/plinth) by the visitor in CP025_visitors_start and is no bigger in frame (camera-limited); all three lifts are light-linked fill cheats; cabinet tones come from the generated texture (a little orange, caryatids near white), stand still a dark block; vase is tiny at 16.7 m and its height remains a plausibility estimate; vase not in its catalogue gallery position.
  - Promotion (if KEPT later): byte-copy `rounds/candidates/e02_scanprops_v2.blend` → `rounds/e02.blend` after backing up live to `rounds/e02.blend.pre_scanprops_v2_keep`; NOT done here.

## 2026-11-09 CP025 scan props v2 — KEEP (promoted live)
Parent viewed all three v2 pairs (CP025_visitors_start, CP025_visitors_end, EX_lineup_start) and KEPT them: cabinet reads gilded instead of a black block, Greek Slave reads white against the crimson curtain, exposure matched outside the changes.
- Old live (md5 fce122da, KEEP 68cfae5) → `rounds/e02.blend.pre_scanprops_v2_keep` (untracked). Live `rounds/e02.blend` = byte copy of the reviewed `rounds/candidates/e02_scanprops_v2.blend` (md5 f75234f3ce35fca0053e2a2e33d73e2f; no rebuild).
- `scripts/render_scanprops_v2_live.sh` (28 spp, 1920×1080, same camera order as the candidate script) → `renders/candidates/scanprops_v2_20261109/live/` and `regress_new/`.
- Live vs candidate afters (`live_vs_after.txt`): max 1/255 on all five shots (47–127 px), luma identical to 2 dp = Cycles run-to-run floor.
- Regressions (`regress.txt`, old-live renders `scanprops_20261109/regress_new/` from fce122da vs new live): EX_osler max 34, CP024_approach_start/_end max 39/41, CP024_ram_f025 max 52, CP025_july/case max 130/98; luma within 0.2% everywhere (mean |diff| 1.1–2.0). Viewed the densest-diff crops: no visible change; the differences are edge/highlight noise across the whole frame (the extra light-linked lights change Cycles light sampling), larger than the v1 regression (max 7–23) but noise only.
- `renders/e02/` CP025_visitors_start/_end, EX_lineup_start, CP025_july/case and EX_osler_start updated to the new live renders. renders/e02 CP024 pngs NOT updated: they now differ from a fresh live render by the noise above (`render_cp024_machinery.sh` is no longer pixel-identical against the new live).

