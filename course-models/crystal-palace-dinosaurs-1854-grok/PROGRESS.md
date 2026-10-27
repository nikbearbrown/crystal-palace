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
