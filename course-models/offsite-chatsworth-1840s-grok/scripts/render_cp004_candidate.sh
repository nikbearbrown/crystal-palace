#!/usr/bin/env bash
# CP004 lily house CANDIDATE (2026-11-16, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp004_candidate.sh [--no-build]
# before = live rounds/ch02.blend (md5 59eca5d7, unchanged); after = rounds/candidates/ch02_cp004lily.blend.
# Recipe = the live CP004 hero recipe: scripts/render_views.py, look v1 era 1840s / tod exterior_midday (= era_for_scene /
# tod_for_scene CP004, as the 2026-10-27 material pass rendered the hero), exposure from the look, people swap on (v3.4 now;
# the hero was v3.1), one camera per Blender session, both sides identical, 1920x1080, 48 spp.
# At 1280x720 / 28 spp this recipe reproduces the live hero renders/ch02/CP004_lily_tank_start.png except one off-frame
# figure's shadow at bottom right (people v3.1 -> v3.4 placement): max diff 114, mean 0.58, 7955 px > 8.
# Side-effect cams = every other camera in ch02 (CP004 learning + underside share the lily house; CP003 stove cams check the
# outside lawn/apron added round the lily house).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/ch02.blend; CAND=rounds/candidates/ch02_cp004lily.blend
OUT=renders/candidates/cp004_lilyhouse_20261116; LOG=/workspace/logs/cp004_lilyhouse_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == 59eca5d7 ]] || { echo "live ch02 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp004_lilyhouse.py -- --out $CAND 2>&1 | grep -E "CP004_CANDIDATE_SAVED|Error|Traceback" | cut -c1-200 | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
CAMS="CP004_lily_tank_start CP004_learning_start CP004_lily_underside_start CP003_stove_nave_start CP003_stove_rib_start"
for side in before after; do
  BL=$([[ $side == before ]] && echo $LIVE || echo $CAND)
  for cam in $CAMS; do
    png="$OUT/$side/$cam.png"
    [[ -s "$png" ]] && { echo "skip $png" >> $LOG; continue; }
    echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
    tmpd=$(mktemp -d)
    "$B" -b $BL -P scripts/render_views.py -- --cams $cam --res 1920x1080 --samples 48 --era 1840s --tod exterior_midday --threads 8 --outdir $tmpd >> $LOG 2>&1 && mv "$tmpd/$cam.png" "$png"
    rm -rf "$tmpd"
  done
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
