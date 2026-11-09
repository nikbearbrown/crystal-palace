#!/bin/bash
# KEEP CP025 exhibit-court scan props (2026-11-09; parent viewed all three pairs: CP025_visitors_start,
# CP025_visitors_end, EX_lineup_start). Live rounds/e02.blend is a BYTE COPY of the reviewed
# rounds/candidates/e02_scanprops.blend (md5 fce122dabf730ae76b47d3cacf6d36b7; not rebuilt, objects keep
# their candidate=e02_scanprops tag). Old live -> rounds/e02.blend.pre_scanprops_keep (untracked).
# 1) live renders of the three KEEP shots -> $O/live/, compared with $O/after/ (must be max diff 0)
# 2) regression: old live vs new live on the other e02 shots -> $O/regress_old/, $O/regress_new/
# usage: scripts/render_scanprops_live.sh [SAMPLES=28]
set -e
S=${1:-28}; B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
O=renders/candidates/scanprops_20261109
OLD=rounds/e02.blend.pre_scanprops_keep
[ -f $O/live/EX_lineup_start.png ] && [ "$FORCE" != 1 ] || \
  $B -b rounds/e02.blend -P scripts/render_shots.py -- --out $O/live --samples $S --pct 100 --frame 1 --cams CP025_visitors_start,CP025_visitors_end,EX_lineup_start
for side in old new; do
  if [ $side = old ]; then BL=$OLD; else BL=rounds/e02.blend; fi
  [ -f $O/regress_$side/CP024_ram_start_f025.png ] && [ "$FORCE" != 1 ] && { echo "skip $side"; continue; }
  $B -b $BL -P scripts/render_shots.py -- --out $O/regress_$side --samples $S --pct 100 --frame 1 --cams EX_osler_start,CP024_approach_start,CP024_approach_end,CP025_july_start,CP025_case_start
  $B -b $BL -P scripts/render_shots.py -- --out $O/regress_$side --samples $S --pct 100 --frame 25 --suffix _f025 --exposure 0.3 --cams CP024_ram_start
done
echo SCANPROPS_LIVE_DONE
