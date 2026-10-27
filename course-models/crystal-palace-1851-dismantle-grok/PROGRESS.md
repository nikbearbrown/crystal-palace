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
