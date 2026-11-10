#!/usr/bin/env bash
# CP026 env KEEP regression (2026-11-10): pre-keep h03 (rounds/h03.blend.pre_cp026env_keep) vs live h03, other h03 cams -> /workspace/tmp/cp026keep/{pre,live}. Same recipe both sides.
set -euo pipefail
cd /workspace/crystal-palace-fitout/course-models/crystal-palace-1851-fitout-grok
B=/workspace/blender5/blender; R=/workspace/tmp/cp026keep
for side in pre live; do
  f=rounds/h03.blend; [[ $side == pre ]] && f=rounds/h03.blend.pre_cp026env_keep
  mkdir -p $R/$side
  "$B" -b $f -P scripts/render_views_ppl31.py -- --cams CP026_turnstiles_start --res 1280x720 --samples 24 --era 1851 --tod exterior_midday --threads 8 --exposure -0.7 --outdir $R/$side
  "$B" -b $f -P scripts/render_views_ppl31.py -- --cams CP027_gallery_rail_start,CP027_stair_foot_start,CP028_watering_start --res 1280x720 --samples 24 --era 1851 --threads 8 --outdir $R/$side
  "$B" -b $f -P scripts/render_views.py -- --cams CP028_louvre_start --res 1280x720 --samples 48 --no-people --keep-lighting --outdir $R/$side
  echo "REGRESS_SIDE_DONE $side"
done
echo REGRESS_DONE
