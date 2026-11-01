#!/bin/bash
# 2026-11-01 envelope full-camera check: live r11 vs candidate r11_envelope, same lean settings.
# Live: plain pipeline (no per-shot table) = live output. Candidate: --shot-exposure (CP023 -2.2).
# usage: scripts/render_envelope_check.sh [SAMPLES] [THREADS]   (never saves any .blend)
S=${1:-28}; T=${2:-4}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
CAMS=REV_int_up_start,CP017_park_inside_end,REV_ext34_start,REV_south_start,PLATE_IV_south_ortho_start,REF_talbot_start,REF_absolon_start,REF_elm_north_start,CP017_park_inside_start,CP008_build_around_end,OPEN_gallery_start,DET_fountain_start,CP023_into_nave_start,CP023_into_nave_end,CP008_build_around_start
O=renders/candidates/envelope_check_20261101
$B -b rounds/r11.blend -P scripts/render_views.py -- --cams $CAMS --portrait REF_talbot_start --outdir $O/live --res 1280x720 --samples $S --threads $T > /workspace/logs/transept_envcheck_live.log 2>&1 &
$B -b rounds/candidates/r11_envelope.blend -P scripts/render_views.py -- --cams $CAMS --portrait REF_talbot_start --outdir $O/candidate --res 1280x720 --samples $S --threads $T --shot-exposure > /workspace/logs/transept_envcheck_cand.log 2>&1 &
wait
echo ENVCHECK_DONE
