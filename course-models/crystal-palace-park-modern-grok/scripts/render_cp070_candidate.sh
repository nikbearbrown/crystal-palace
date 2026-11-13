#!/usr/bin/env bash
# CP070 station CANDIDATE (2026-11-13, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp070_candidate.sh [--no-build]
# before = live rounds/parknow-r02.blend (md5 48fc01ec, unchanged); after = rounds/candidates/parknow-r02_cp070station.blend.
# Recipe per camera = its live recipe (scripts/render_cp076_look.py, look v1.1 present / exterior_afternoon, exposure from the
# look (-0.8)), one camera per Blender session, both sides identical, at 1920x1080, 48 spp:
#   CP070 x2 + CP067: pk_grass_plateau shown (scripts/live_plateau_show.py) = how dud-fix v4 rendered the live heroes;
#   CP075: clipper hidden (saved state) = live hero recipe. Each recipe reproduces its live 1280x720/32 spp hero at max diff 0.
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/parknow-r02.blend; CAND=rounds/candidates/parknow-r02_cp070station.blend
OUT=renders/candidates/cp070_station_20261113; LOG=/workspace/logs/cp070_station_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == 48fc01ec ]] || { echo "live r02 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp070_station.py -- --out $CAND 2>&1 | grep -E "CP070_CANDIDATE_SAVED|Error|Traceback" | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
CAMS="CAM_CP070_begin_walk_35mm:CP070:show CAM_CP070_park_entry_35mm:CP070:show CAM_CP075_layered_nsc_35mm:CP075:hide CAM_CP067_dino_conservation_35mm:CP067:show"
for side in before after; do
  BL=$([[ $side == before ]] && echo $LIVE || echo $CAND)
  for spec in $CAMS; do
    IFS=: read cam sid pl <<<"$spec"; png="$OUT/$side/$cam.png"
    [[ -s "$png" ]] && { echo "skip $png" >> $LOG; continue; }
    X=(); [[ $pl == show ]] && X=(-P scripts/live_plateau_show.py)
    echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
    "$B" -b $BL "${X[@]}" -P scripts/render_cp076_look.py -- "$png.tmp.png" $cam $sid none 1920x1080 48 >> $LOG 2>&1 && mv "$png.tmp.png" "$png"
  done
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
