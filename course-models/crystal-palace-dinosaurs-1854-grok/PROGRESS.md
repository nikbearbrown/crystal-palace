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
