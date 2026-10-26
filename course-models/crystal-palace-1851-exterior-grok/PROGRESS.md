# PROGRESS: Hyde Park 1851 exterior completion (Grok Bot)

Branch `grok-exterior-1851`, a local worktree at /workspace/crystal-palace-exterior. Nothing is pushed. Blender 5.1.2.

**Scope:** what completes the 1851 exterior around Claude's west frame (x <= -36 ft, collection MODEL) and the Grok transept (|x| <= 132 ft):
- the east half: lines x = 36..924 ft, with columns, girders, 72 ft nave trusses, ridge-and-furrow roofs, galleries and 6 stairs;
- the north strip: x -708..228, y 204..252;
- side walls on all three tiers along the full 1848 ft;
- the east and west end walls, with the Plate V doors, cresting and fascia.

Claude's frame is used as-is: metres, origin at the crossing, X east, Y north. His folder is never edited; his .blend is only appended at render time.

**Build:**
`cd scripts && blender -b -P build_exterior.py -- --out ../rounds/xNN.blend --milestones ../rounds`

**Checks:**
`blender -b rounds/xNN.blend -P scripts/check_dims.py -- --out checks/xNN`

**Renders:**
`bash scripts/render_round.sh xNN 1280x720 48 [transept.blend]` renders a combo of Claude, the transept r06 and this model.

**Compare:**
`python3 scripts/compare_sheets.py xNN` writes Plate V, Plate IV and the bird's-eye view sheets.

## Log
- x01: first full build, 6236 parts, 614 columns, 1962 roof units, 6 stairs. Checks 29/29. Renders in renders/x01.
  - The combo ground plane rendered black because two coplanar planes overlapped (fixed by EX16).
  - The roofs read as white slabs.
  - The Plate V ortho looked through the glazed end into the transept's full-width vault.
- x02: 7 doors on the east end (Plate V: the centre 3, the bays at y = +-120, the outer 2). The EXT_SE_34 camera was moved closer. Checks 29/29.
- x03: the Plate V review camera is cut at x = 700 ft (EX18), and the exterior roofs have their own greyer glass (EX19). Checks 29/29. Renders in renders/x03; compare sheets in compare/x03_*.jpg.

## Self-score x03: 6.5/10
**Good:**
- The stepped 408/264/120 ft east end reads in both the ortho and the eye-height perspective, with the Plate V proportions, door bays and cresting line.
- The full 1848 ft building joins Claude's west half and the transept vault without gaps or duplicate columns (G01-G04).
- The interior east nave vista to the transept reads, with galleries and stairs.
- The roofs now read as ridge-and-furrow glass from the air.

**Misses:**
- Claude's west-half roofs still read white next to my grey east roofs. That is his material and I can't edit it, so the seam shows in the aerial view.
- The end-wall glazing is too transparent and too pale. Plate V draws the arched panels dark and dense; the model loses them against the sky.
- The eye-height views (EXT_SE_34, EXT_NE_strip) are half lawn, with the building small in frame.
- There are no ventilation louvre shadows or tarpaulins (EX13), no flagstaffs along the roof, no park trees or Rotten Row context, and no boundary railings.
- The gravel apron is a flat placeholder (EX17, grade D).

## Next (x04)
- Darker end-screen glass and bars, matching the transept r06 fix, plus the arched-panel pattern of Plate V.
- Flagstaffs on the tier-3 cresting (bird's-eye view).
- Move EXT_SE_34 and EXT_NE_strip about 40% closer and lower the look target, so the building fills the upper half.
- Park trees: reuse the transept elm generator at low density, south of Rotten Row and on the Kensington side.
- Propose (not do) a shared roof-glass material to Claude through Professor Bear.
