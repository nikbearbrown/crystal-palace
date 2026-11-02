#!/bin/bash
# 2026-11-02 CP023 START floor-detail CANDIDATE (not live). Rebuilds the candidate blend from the live r11_envelope_v2.blend
# (unchanged) and renders it at live CP023 settings. Variant A = floor detail only; variant B adds --shift-y 0.035.
set -e
cd "$(dirname "$0")/.."
B=${BLENDER:-/workspace/blender5/blender}
OUT=renders/candidates/cp023_floor_20261102
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/apply_cp023_floor.py
COMMON="--cams CP023_into_nave_start --res 1280x720 --samples 64 --threads 8 --exposure -0.9 --cp023-boots"
$B -b rounds/candidates/r11_envelope_v2_cp023floor.blend -P scripts/render_views.py -- $COMMON --outdir $OUT/full
$B -b rounds/candidates/r11_envelope_v2_cp023floor.blend -P scripts/render_views.py -- $COMMON --shift-y 0.035 --outdir $OUT/full_shift
python3 scripts/cp023_floor_pairs.py
