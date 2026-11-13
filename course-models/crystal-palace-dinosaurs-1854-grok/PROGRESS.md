# PROGRESS — crystal-palace-dinosaurs-1854-grok

## 2026-10-26 (late)
- Created the folder in worktree `/workspace/crystal-palace-dinosaurs` on branch `grok-dinosaurs-1854`. Commits are local only, nothing pushed.
- `scripts/hawkins.py`: species models for Iguanodon (standing and recumbent), Megalosaurus, Hylaeosaurus, Ichthyosaur, Plesiosaur, Megatherium (with tree and tapir trunk) and Irish elk (stag, doe, reclining doe).
- `scripts/build.py`: lake and islands heightfield, water, fence, planting, strata block, and the Hawkins studio set (1853). The Dinner in the Iguanodon set (31 Dec 1853) has an open mould, inner floor, table at the rim, 21 guests, a marquee and a raised gallery camera. There are five cameras.
- Preview iterations:
  - p1: exposure was too hot; fixed the lake width and the dinner guests buried in the mould.
  - p2: 50 mm details were too distant; dinner was viewed from the deck.
  - p3: boat-level detail cameras; raised print-like dinner view; added the 4th elk; dropped the misidentified "fawn".
- `checks/dimension_check.py` covers:
  - Iguanodon 10 m × 2.7 m;
  - Megalosaurus 10 m × 3.5 m;
  - Megatherium ≤ 6 m with its tree;
  - counts: Iguanodon 2, Ichthyosaur 3, Plesiosaur 3, Irish elk 4, plus 1 each of the others.
- Round r01 `rounds/dinosaurs-1854-r01.blend` (5.9 MB, 41 objects, 282k faces): **14 PASS / 0 FAIL** (`checks/r01.txt`).
- r01 1920×1080 renders are running detached into `renders/r01/`.

## Next
- Higher-fidelity heads (Megalosaurus snout, Iguanodon horn detail) and surface texture (scales, armour).
- Remaining 1854 genera (Labyrinthodon, Dicynodon, Pterodactyls, Mosasaurus, Teleosaurus, Palaeotherium, Anoplotherium).
- A gaslit evening version of the dinner.
- r01 renders done: `renders/r01/r01_CAM_*.png` (5 cams, 1920×1080, 40 spp). Contact sheet `compare/r01_contact.jpg`. Print compares: `compare/r01_CP034b_vs_ILN1854.jpg` and `compare/r01_CP034_vs_ILN1853.jpg`.
- Known misses for r01: statue colours are pale and uniform (U); CP043b has the island bank filling the lower frame; the studio scaffold is generic; diners are generic stand-ins without top hats or individual portraits.

## Checkpoint crystal-palace-dinosaurs-1854-grok quality round
- Patched scripts for quality pass; rebuilds pending lean hero renders.

## r02 (2026-10-27) — Hawkins paint + dinner evening + bank frame
- `dinosaurs-1854-r02.blend` (~5.7 MB).
- Lean heroes → `renders/r02/r02_CAM_CP{043,043b,034b}_*.png` (dinner evening avg ~140,121,94).
- Local commit. NOT pushed.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## 2026-11-13 CP034b "dinner in the Iguanodon" CANDIDATE r06 — executor notes (not a verdict, NOT live; DEPARTURES D-DN-26..33)
- Why CP034b: on a contact sheet of every live hero outside the recent-polish list it read worst: open ground plane and horizon with bare tent poles (no marquee), the front-row diners stood outside the mould wall with legs showing under the belly, and the inner floor plank poked out of the neck like a floating bench.
- Base: rounds/dinosaurs-1854-r05.blend (live round of this build, md5 f879da99, unchanged; its dinner set and lighting are identical to r01). COVERAGE lists r02 as the blend but renders/r01/r01_CAM_CP034b_iguanodon_dinner_28mm.png (1280x720, older render, darker sky) as the hero; r02 is the evening variant. The "before" here is r05 rendered with the same recipe as the "after", so it is brighter than the old r01 PNG (mean abs diff 39 at 1280x720) but shows the same geometry.
- Script scripts/cand_cp034b_dinner_20261113.py (live r05 -> rounds/dinosaurs-1854-r06-cand.blend; refuses to overwrite r05 or to run on a source with DN53c_ objects). Changes only inside DN53_iguanodon_dinner__31Dec1853: boarded marquee walls + striped valance + plank floor; 21 seated bare-headed diners inside the measured mould interior (old standing guests hidden, not deleted); old plank/table/legs/chandelier/blank boards removed from the combined deck mesh (islands logged) and rebuilt; lettered BUCKLAND/CUVIER/OWEN/MANTELL boards; lower chandelier with gas globes; festoons; folding screen past the tail end; three waiters with trays.
- Render scripts/render_cp034b_dinner.sh [--no-build] (resumable per PNG, nohup, log /workspace/logs/cp034b_dinner_render.log, DONE + md5.txt) -> renders/candidates/cp034b_dinner_20261113/{before,after}/ : CAM_CP034b hero + CAM_CP034 studio side effect, both 1920x1080 48 spp via scripts/render.py, no overrides, both sides.
- Pairs python3 scripts/cand_cp034b_dinner_pairs.py -> survey look/pairs_geo/CANDIDATE_CP034b_iguanodon_dinner_{before,after,pair}.png (pair has the ILN woodcut as a third tile) and CANDIDATE_CP034b_sidefx_CP034_hawkins_studio_{before,after,pair}.png; numbers checks/cp034b_dinner_pairs.json.
- Checks: checks/check_cp034b_dinner.py -> checks/cp034b_dinner_checks.json (dims vs print/accounts + scope/state vs live r05: nothing outside the dinner collection changed, all added objects DN53c_, nothing deleted, collections dated); checks/dimension_check.py on the candidate -> checks/cp034b_dinner_dims_r06cand.txt 13 PASS / 1 FAIL, identical to live r05 (the FAIL is the pre-existing park Iguanodon height, 9.89 vs 8.86 ft, not in this scene).
- Not done: promotion, KEEP, COVERAGE row change, any live PNG. r05 and its renders unchanged.
