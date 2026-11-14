#!/usr/bin/env bash
# CP066 NSC 1964-67 CANDIDATE (2026-11-14, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp066_candidate.sh [--no-build]
# before = live rounds/park60-r17.blend (md5 9ea1c796, unchanged); after = rounds/candidates/park60-r17_cp066nsc64.blend.
# Recipe = the live CP066 hero recipe: scripts/render_cp076_look.py with scene id CP066 (look v1.1 present /
# exterior_afternoon, exposure from the look = -0.8), one camera per Blender session, both sides identical, 1920x1080, 48 spp.
# (The live hero renders/r17k_park60_CAM_CP066_nsc_stadium_35mm.png is 1280x720 / 24 spp; this recipe at 1280x720 24
#  reproduces it at max diff 0.) Side-effect cams = every other camera stored in park60-r17 (none of them is a live hero).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/park60-r17.blend; CAND=rounds/candidates/park60-r17_cp066nsc64.blend
OUT=renders/candidates/cp066_nsc64_20261114; LOG=/workspace/logs/cp066_nsc64_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == 9ea1c796 ]] || { echo "live park60-r17 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp066_nsc64.py -- --out $CAND 2>&1 | grep -E "CP066_CANDIDATE_SAVED|Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
CAMS="CAM_CP066_nsc_stadium_35mm CAM_CP066_nsc_wide_35mm CAM_CP066_nsc_hall_35mm CAM_CP065_hl_closed_35mm CAM_CP065_subway_threshold_35mm"
for side in before after; do
  BL=$([[ $side == before ]] && echo $LIVE || echo $CAND)
  for cam in $CAMS; do
    png="$OUT/$side/$cam.png"
    [[ -s "$png" ]] && { echo "skip $png" >> $LOG; continue; }
    echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
    "$B" -b $BL -P scripts/render_cp076_look.py -- "$png.tmp.png" $cam CP066 none 1920x1080 48 >> $LOG 2>&1 && mv "$png.tmp.png" "$png"
  done
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
