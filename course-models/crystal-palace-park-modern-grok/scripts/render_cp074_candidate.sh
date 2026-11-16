#!/usr/bin/env bash
# CP074 Geological Court present-day CANDIDATE (2026-11-16, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp074_candidate.sh [--no-build]
# before = rounds/parknow-r01.blend (md5 fb640758, unchanged) = the blend the live hero renders/r01_parknow_CAM_CP074_dinosaurs_35mm.png
#          was rendered from (PNG 'File' metadata; the manifest/COVERAGE say r02, which does NOT reproduce it);
# after  = rounds/candidates/parknow-r01_cp074geocourt.blend.
# Recipe = the live hero recipe: survey look/apply_render.py (look v1.1, present / exterior_afternoon, exposure -0.8, --no-people),
# one camera per Blender session, both sides identical; at 1280x720 24 spp it reproduces the live hero at max diff 0 (step 0);
# pairs at 1920x1080, 48 spp.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; LOOK=/workspace/crystal-palace-survey/look/apply_render.py
LIVE=rounds/parknow-r01.blend; CAND=rounds/candidates/parknow-r01_cp074geocourt.blend
OUT=renders/candidates/cp074_geocourt_20261116; LOG=/workspace/logs/cp074_geocourt_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == fb640758 ]] || { echo "live r01 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp074_geocourt.py 2>&1 | grep -E "CP074_CANDIDATE_SAVED|Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
# step 0: live recipe reproduces the live hero
if [[ ! -s $OUT/live_repro_1280x720_24spp.png ]]; then
  "$B" -b $LIVE -P $LOOK -- --cam CAM_CP074_dinosaurs_35mm --out $OUT/live_repro_1280x720_24spp.png --scene-id CP074 --era present --tod exterior_afternoon --spp 24 --res 1280x720 --no-people >> $LOG 2>&1
fi
python3 - "$OUT/live_repro_1280x720_24spp.png" renders/r01_parknow_CAM_CP074_dinosaurs_35mm.png <<'PY' | tee -a $LOG
import sys, numpy as np
from PIL import Image
a, b = (np.asarray(Image.open(p).convert("RGB")).astype(int) for p in sys.argv[1:3])
print("LIVE_REPRO max diff", int(abs(a - b).max()))
PY
CAMS="CAM_CP074_dinosaurs_35mm:CP074 CAM_CP074_iguanodon_50mm:CP074 CAM_CP075_layered_nsc_35mm:CP075 CAM_CP066_nsc_wide_35mm:CP066 CAM_CP072_footprint_35mm:CP072"
for side in before after; do
  BL=$([[ $side == before ]] && echo $LIVE || echo $CAND)
  for spec in $CAMS; do
    IFS=: read cam sid <<<"$spec"; png="$OUT/$side/$cam.png"
    [[ -s "$png" ]] && { echo "skip $png" >> $LOG; continue; }
    echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
    "$B" -b $BL -P $LOOK -- --cam $cam --out "$png.tmp.png" --scene-id $sid --era present --tod exterior_afternoon --spp 48 --res 1920x1080 --no-people >> $LOG 2>&1 && mv "$png.tmp.png" "$png"
  done
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
