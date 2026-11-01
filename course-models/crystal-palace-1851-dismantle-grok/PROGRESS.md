# PROGRESS: HP-EMPTY / HP-DISMANTLE (Grok)

Branch grok-dismantle-1851, from transept r09 (0b64c06) plus a merge of exterior x05 (65bd396). Worktree /workspace/crystal-palace-dismantle. Local commits only.

## d01: in progress (checkpoint)
- Scripts: build_dismantle.py, zones.py, render_dismantle.py, check_dismantle.py, build_round.sh, render_round.sh. Route: CP030_empty_walk, CP030_empty_aisle, CP031_joint_detail, CP031_lateral, REV_dismantle_aerial.
- First checks: empty 29/29; dismantle 32/34. After the fixes: empty 29/29, dismantle 34/34 (checks/d01_*). The deck was enlarged to 186–195 × −152…−145, and the striker moved to frame left.
  - The joint-detail eye was 1.0 ft under a tier-1 roof unit, so the deck was lowered from 15.5 to 13.5 ft.
  - The lateral track was 14.6 m, so it was shortened to 9.75 m.
- The lowered girder is canted 15° by the tag lines so it clears the column shafts.

## d02 — 2026-10-26 (final for this pass)
- Cameras: CP030 walk end and aisle reframed (DM12). Rebuilt rounds/d02_empty.blend and d02_dismantle.blend; d01 blends dropped from the tree (still in history at e8d96a2).
- Checks: checks/d02_empty 29/29, checks/d02_dismantle 34/34.
- Renders: renders/d02 (7 frames, 1280x720, 48 spp; two CP030 frames re-rendered, the rest carried over from d01 unchanged). d01 frames kept for comparison.
- Self-score: 7.4/10.
- Misses: CP031_joint_detail and REV aerial overexposed, so the joint keys and wedges don't read; the lowered girder is white on a white wall in lateral_start and reads weakly; porters toy-like up close (walk end); a black floor seam line crosses the nave in walk end; ironwork is plain white, not Owen Jones colours; the stacks are illustrative, not counted from a source.
- Next d03: view exposure -0.6 to -0.8 for the DISMANTLE cams; a darker or red-lead primed tone on the lowered girder; a 50 mm close-up of the key and wedge being struck; find and remove the floor seam; a few more porters and a cart in EMPTY at mid-distance; a CP031 dusk variant.

## d03 — checkpoint 2026-10-26 22:25 (render running)
- Done in scripts: per-shot view exposure from the route (DISMANTLE interiors -1.3 = x05 default -0.7; aerial -1.1; DM14); lowered and stacked girders in red-lead primer (DM13); new CP031_key_strike 50 mm close-up from the scaffold deck (trestle stage, smith with a raised maul at the half-driven key, mate with a drift; DM17); floor seam fixed at render time (transept floor 9 mm under the exterior boards; DM15); EMPTY gets a horse trolley loading cases at mid distance plus 3 carries, a sack truck and 7 more porters; CP031 dusk variant (sun 5 deg WSW, warm; DM16); figure facing fixed (DM18).
- Checks: d03_empty 30/30, d03_dismantle 41/41 (new K21 floor seam, K22 red lead, K23 striker reach).

## d03 — FINAL (2026-10-26)
- Renders: renders/d03/ (10 frames at 1280x720, plus _contact_d03.jpg). Checks: d03_empty 30/30, d03_dismantle 41/41.
- Done:
  - Dismantle cameras get a -0.7 offset (the CP031 cameras end up at -1.3/-1.1).
  - The removed girder is in red-lead primer.
  - New 50 mm CP031_key_strike close-up.
  - Floor seam fixed.
  - More porters, plus a mid-distance trolley/cart.
  - CP031 dusk variants (lateral start/end).
- Self-score: 7.5/10.
- Misses:
  - The key-strike frame is still bright on the white ironwork, and the sledge/maul reads as a stick.
  - The figures are blocky.
  - The horse sits half-hidden behind the girder in lateral_end.
  - The dusk sky is still daylight-blue through the roof, so the dusk is only a sun-angle change.
- Next d04:
  - Warm dusk world colour.
  - Add a maul head and an arm pose.
  - Move the horse clear of the girder.
  - Use the r10 figure styles (frock coats, caps) for the workmen.

## Backlog (parked 2026-10-26)
- d04 parked by Professor Bear's instruction: polish rounds now give diminishing returns; work moved to unbuilt sets (HP-SITE, MOVE+K-JOINT).
- Parked d04 items: warm dusk world colour; maul head/arm pose; horse clear of girder; r10 figure styles for workmen.

## d04 (2026-10-27): warm dusk, maul head/pose, horse clear, r10 workmen styles
- Parked d04 backlog cleared.
- Build: `rounds/d04_empty.blend`, `rounds/d04_dismantle.blend`. Checks: empty 32/32, dismantle 43/43.
- Lean renders: `renders/d04` — CP031_key_strike, CP031_lateral (+ dusk), CP030_empty_walk (24 spp).

## look-v1 (2026-10-27)
- Wired `scripts/cpl_look.py` → shared `crystal-palace-survey/look/crystal_palace_look.py`.
- `apply_look` in render script; lean re-render of COVERAGE hero cams.

## Repo hygiene

never git init inside a grok folder; commit from the worktree root

## 2026-11-01 HP interior envelope REJECT (CP030)
- Envelope candidate `rounds/candidates/d04_envelope.blend` on CP030_empty_aisle reviewed: washed out, loses glass, tree and depth vs live. REJECT; live d04 unchanged. Candidate files left in `rounds/candidates/` for reference.
