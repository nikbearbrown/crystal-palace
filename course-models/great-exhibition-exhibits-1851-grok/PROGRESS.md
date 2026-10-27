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
