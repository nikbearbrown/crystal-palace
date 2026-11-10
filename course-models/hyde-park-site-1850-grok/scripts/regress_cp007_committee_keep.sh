#!/usr/bin/env bash
# CP007 committee KEEP regressions (2026-11-10): render every other s02 camera from the promoted live rounds/s02.blend at the
# live recipes (1920x1080, 96 spp, --no-people) into $OUT/live, and CP008 (no renders/s02_png frames) also from the pre-KEEP
# backup rounds/s02.blend.pre_cp007committee_keep into $OUT/pre. Recipes: CP006_start KL 0.14, CP006_end look v1.1 -0.50,
# CP007_end + CP008_start/end/tilt KL scene exposure -0.4, CP009_start KL 0.29, CP009_end KL 0.06.
#   scripts/regress_cp007_committee_keep.sh [outdir=/workspace/tmp/cp007keep] [samples=96]
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; OUT=${1:-/workspace/tmp/cp007keep}; S=${2:-96}; PRE=rounds/s02.blend.pre_cp007committee_keep
r() { local f=$1 o=$2 c=$3; shift 3; "$B" -b "$f" -P scripts/render_shots.py -- --cams "$c" --out "$o" --samples "$S" --pct 100 --no-people "$@" 2>&1 | grep -E "RENDERED|Error|Traceback" || true; }
r rounds/s02.blend "$OUT/live" CP007_end,CP008_start,CP008_end,CP008_tilt --keep-lighting
r rounds/s02.blend "$OUT/live" CP006_start --keep-lighting --exposure 0.14
r rounds/s02.blend "$OUT/live" CP006_end --exposure -0.50
r rounds/s02.blend "$OUT/live" CP009_start --keep-lighting --exposure 0.29
r rounds/s02.blend "$OUT/live" CP009_end --keep-lighting --exposure 0.06
r "$PRE" "$OUT/pre" CP008_start,CP008_end,CP008_tilt --keep-lighting
echo CP007_REGRESS_DONE
