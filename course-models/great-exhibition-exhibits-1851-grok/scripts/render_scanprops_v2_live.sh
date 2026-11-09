#!/bin/bash
# KEEP CP025 scan props v2 (2026-11-09; parent viewed all three pairs: CP025_visitors_start,
# CP025_visitors_end, EX_lineup_start). Live rounds/e02.blend is a BYTE COPY of the reviewed
# rounds/candidates/e02_scanprops_v2.blend (md5 f75234f3ce35fca0053e2a2e33d73e2f; not rebuilt).
# Old live (fce122da, KEEP 68cfae5) -> rounds/e02.blend.pre_scanprops_v2_keep (untracked).
# 1) live renders of the five candidate shots (same camera order as render_scanprops_v2_cand.sh)
#    -> $O/live/, compared with $O/after/ (expect Cycles run-to-run floor, max ~1/255)
# 2) regression: the other e02 shots on new live -> $O/regress_new/, compared with old-live renders
#    renders/candidates/scanprops_20261109/regress_new/ (rendered from fce122da, same settings/order)
# usage: scripts/render_scanprops_v2_live.sh [SAMPLES=28]   (FORCE=1 to redo)
set -e
S=${1:-28}; B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
O=renders/candidates/scanprops_v2_20261109
[ "$(md5sum rounds/e02.blend | cut -d' ' -f1)" = f75234f3ce35fca0053e2a2e33d73e2f ] || { echo "live e02 is not the v2 KEEP"; exit 1; }
[ -f $O/live/CP025_case_start.png ] && [ "$FORCE" != 1 ] || \
  $B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O/live --samples $S --pct 100 --frame 1 --cams CP025_visitors_start,CP025_visitors_end,EX_lineup_start,CP025_july_start,CP025_case_start
if [ ! -f $O/regress_new/CP024_ram_start_f025.png ] || [ "$FORCE" = 1 ]; then
  $B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O/regress_new --samples $S --pct 100 --frame 1 --cams EX_osler_start,CP024_approach_start,CP024_approach_end,CP025_july_start,CP025_case_start
  $B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O/regress_new --samples $S --pct 100 --frame 25 --suffix _f025 --exposure 0.3 --cams CP024_ram_start
fi
echo SCANPROPS_V2_LIVE_DONE
