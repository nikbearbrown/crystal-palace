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

## x04 (2026-10-26)
- **Changes**
  - Darker end-screen glass. Flagstaffs on the cresting. EXT_SE_34 and EXT_NE_strip moved about 40% closer (EX23). Park trees.
  - **Roof seam with Claude** (EX24/EX26): at render time, and in the assembly .blend saved here, his appended roof units take our roof glass.
    - First x04 pass: the override applied, but his 2-poly roof mesh has no usable UVs. Our UV-driven sash-bar mask therefore painted his whole roof as bar, an opaque cream sheet.
    - Fix: a copy, GT_RoofGlassExt_CL, drives the bars from object coordinates in feet. The seam is closed in REF_aerial_SE (`compare/x04_seam_before_after.jpg`).
    - Claude's file was only read, never saved.
  - **HP1851 complete** (EX25): `assembly/HP1851_complete.blend` is 20.6 MB and self-contained (appended, not linked).
    - Contents: Claude's west frame, the Grok transept r07 and this exterior, with 31 cameras and 12 film-order markers over frames 1-1152.
    - Rebuilt after EX26; its roof mesh carries GT_RoofGlassExt_CL.
    - Test frame 1000 (OPEN_gallery) renders correctly from the assembly.
- Checks 29/29 (checks/x04). Renders are in renders/x04, compare sheets in compare/x04_*.jpg.

## Self-score x04: 7.2/10
**Good:**
- The seam between west and east roofs is gone from the air: one roof glass over 1848 ft.
- The east end and transept read together in the eye-height views.
- One film scene now holds the whole 1851 building and the camera route.

**Misses:**
- Claude's roofs are flat 2-poly sheets. From low angles they read smoother than our ridge-and-furrow units.
- EXT_SE_34 is still about 45% lawn. The building needs to sit lower in frame, or the camera should stand on Rotten Row with trees in the foreground.
- The south wall reads very pale and flat in full sun. The boarding and louvre bands need more value contrast.
- No people, carriages or railings in the park.
- REV_combo in the transept scene still clips the roofs (exposure 0 there), so the seam check uses the x04 aerial.

## Next (x05)
- Render-time ridge-and-furrow proxy for Claude's roof units: an instanced copy of our roof unit, placed only in our combined/assembly scenes.
- EXT_SE_34 reframed. Wall value contrast. Railings and a few carriages on Rotten Row.

## x05 (checks 31/31 in checks/x05; renders renders/x05 at 1280x720, 48 spp, with transept r09; compare/x05_*.jpg)
**Changes:**
- Render-time furrow roofs across Claude's units and ours (EX27; `FURROW_SWAP objects 2179`).
- ROOFGLASS tuning.
- combine `show_with_claude`.
- CP023_into_nave_full, the authoritative CP023 walk on the combined scene with the r09 HP51 dressing.

**Self-score x05: 8.1/10**

**Good:**
- The interior east nave now reads as one ridge-and-furrow roof receding to the east end.
- CP023 shows the dressed nave (locomotive, statuary, banners, crowd) with real nave columns.

**Misses:**
- EXT_SE_34 is still lawn-heavy.
- The south-wall value contrast is unchanged.
- There are no park people or carriages.
- The PLATE_IV ortho is still dominated by the Rotten Row tree line, as in x04.

## Next (x06)
- Reframe EXT_SE_34.
- Wall value contrast.
- Railings and carriages on Rotten Row.
