# PROGRESS: Hyde Park 1851 construction set (CP010-CP016), Grok Bot

Branch `grok-construction-1851` (worktree /workspace/crystal-palace-construction), folder
`course-models/crystal-palace-1851-construction-grok/`. Commit locally only.

- Build: `blender -b -P scripts/build_construction.py -- --out rounds/cNN.blend` (from this folder)
- Checks: `blender -b rounds/cNN.blend -P scripts/check_construction.py -- --out checks/cNN/checks.md`
- Renders: `bash scripts/render_round.sh cNN 1280x720 48` (CP015 louvre at frames 1 and 48; CP014 section portrait)
- Compare: `python3 scripts/compare_sheets.py cNN`

## c01
