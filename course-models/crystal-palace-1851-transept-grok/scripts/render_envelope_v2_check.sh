#!/bin/bash
# 2026-11-01 envelope v2 full-camera check: same 15 cameras / settings as render_envelope_check.sh.
#   live      = rounds/r11.blend (look default exposure)
#   candidate = rounds/candidates/r11_envelope_v2.blend with --shot-exposure (CP023 at -2.2)
#   keep_cp023 = rounds/candidates/r11_envelope.blend CP023 start/end with --shot-exposure (the current KEEP, "before" for CP023)
#   candidate_noshot = v2 CP023 start/end WITHOUT --shot-exposure (reference only: -2.2 was tuned for v1's extra lights)
S=${1:-28}; T=${2:-4}
B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
CAMS=REV_int_up_start,CP017_park_inside_end,REV_ext34_start,REV_south_start,PLATE_IV_south_ortho_start,REF_talbot_start,REF_absolon_start,REF_elm_north_start,CP017_park_inside_start,CP008_build_around_end,OPEN_gallery_start,DET_fountain_start,CP023_into_nave_start,CP023_into_nave_end,CP008_build_around_start
C23=CP023_into_nave_start,CP023_into_nave_end
O=renders/candidates/envelope_v2_20261101
$B -b rounds/r11.blend -P scripts/render_views.py -- --cams $CAMS --portrait REF_talbot_start --outdir $O/live --res 1280x720 --samples $S --threads $T > /workspace/logs/transept_envv2_live.log 2>&1 &
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $CAMS --portrait REF_talbot_start --outdir $O/candidate --res 1280x720 --samples $S --threads $T --shot-exposure > /workspace/logs/transept_envv2_cand.log 2>&1 &
wait
$B -b rounds/candidates/r11_envelope.blend -P scripts/render_views.py -- --cams $C23 --outdir $O/keep_cp023 --res 1280x720 --samples $S --threads $T --shot-exposure > /workspace/logs/transept_envv2_keep.log 2>&1 &
$B -b rounds/candidates/r11_envelope_v2.blend -P scripts/render_views.py -- --cams $C23 --outdir $O/candidate_noshot --res 1280x720 --samples $S --threads $T > /workspace/logs/transept_envv2_noshot.log 2>&1 &
wait; echo ENVV2CHECK_DONE
