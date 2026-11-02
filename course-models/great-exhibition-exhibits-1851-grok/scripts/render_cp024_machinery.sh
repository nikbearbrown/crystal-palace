#!/bin/bash
# LIVE CP024 Machinery Court (KEEP 2026-11-02: stand dressing on approach_start, approach_end, ram_start;
# parent viewed all three pairs). Renders ONLY the three CP024 shots from live rounds/e02.blend:
#   renders/e02/CP024_approach_start.png, CP024_approach_end.png  (frame 1, look v1 exposure)
#   renders/e02/CP024_ram_start_f025.png                          (frame 25, --exposure 0.3 per-shot cheat)
# 28 spp, 1920x1080 (scene 100%), people swap on (MCD_* figures are baked and untagged, so swap ignores them).
# usage: scripts/render_cp024_machinery.sh [--rebuild] [SAMPLES=28] [OUTDIR=renders/e02]
#   --rebuild: rebuild live from the pre-KEEP base first:
#     rounds/e02.blend.pre_machinery_keep (restored from git 5c4b55d if missing)
#       -> scripts/polish_machinery_dress.py -> rounds/candidates/e02_machinery_dress.blend
#       -> scripts/promote_machinery_live.py -> rounds/e02.blend
set -e
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
RB=0; if [ "$1" = "--rebuild" ]; then RB=1; shift; fi
S=${1:-28}; O=${2:-renders/e02}
if [ $RB = 1 ]; then
  BK=rounds/e02.blend.pre_machinery_keep
  [ -f $BK ] || git show 5c4b55d:course-models/great-exhibition-exhibits-1851-grok/rounds/e02.blend > $BK
  [ "$(md5sum $BK | cut -d' ' -f1)" = ae5355a50db7ae718ddfbde4078b36cf ] || { echo "BAD BASE $BK"; exit 1; }
  $B -b -P scripts/polish_machinery_dress.py -- --base $BK --out rounds/candidates/e02_machinery_dress.blend
  $B -b -P scripts/promote_machinery_live.py
fi
$B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O --samples $S --pct 100 --frame 1 --cams CP024_approach_start,CP024_approach_end
$B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O --samples $S --pct 100 --frame 25 --suffix _f025 --exposure 0.3 --cams CP024_ram_start
echo CP024_MACHINERY_LIVE_DONE
