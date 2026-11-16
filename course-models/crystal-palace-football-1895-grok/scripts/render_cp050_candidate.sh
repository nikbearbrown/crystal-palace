#!/usr/bin/env bash
# CP050 Cup Final 20 Apr 1895 CANDIDATE (2026-11-16, no verdict): build + before/after renders, resumable per PNG.
#   scripts/render_cp050_candidate.sh [--no-build]
# before = live rounds/fb02_1895.blend (md5 d8b263c0, unchanged); after = rounds/candidates/fb02_1895_cp050cup.blend.
# Recipe = the live CP050 hero recipe (scripts/render_round.sh -> scripts/render_views.py, no --era / no people swap,
# exposure from the file = 0.0, AgX Medium High Contrast, lights/world untouched), one camera per Blender session, both
# sides identical, 1920x1080, 48 spp. At 1280x720 / 48 spp this recipe reproduces the live hero
# renders/fb02_1895/CP050_bank_1895_start.png exactly (max diff 0).
# Side-effect cam = CP050_pavilion_1895_start (the only other route camera in this round; the CP055 1913 cams in this
# file are not live — CP055 renders from rounds/fb02.blend, untouched).
set -uo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
LIVE=rounds/fb02_1895.blend; CAND=rounds/candidates/fb02_1895_cp050cup.blend
OUT=renders/candidates/cp050_cupfinal_20261116; LOG=/workspace/logs/cp050_cupfinal_render.log
mkdir -p "$OUT/before" "$OUT/after" /workspace/logs
[[ $(md5sum < $LIVE | cut -c1-8) == d8b263c0 ]] || { echo "live fb02_1895 md5 mismatch" | tee -a $LOG; exit 3; }
if [[ "${1:-}" != "--no-build" ]]; then
  "$B" -b $LIVE -P scripts/candidate_cp050_cupfinal1895.py -- --out $CAND 2>&1 | grep -E "CP050|Error|Traceback" | cut -c1-300 | tee -a $LOG
fi
[[ -f $CAND ]] || { echo "no candidate" | tee -a $LOG; exit 3; }
CAMS="CP050_bank_1895_start CP050_pavilion_1895_start"
for side in before after; do
  BL=$([[ $side == before ]] && echo $LIVE || echo $CAND)
  for cam in $CAMS; do
    png="$OUT/$side/$cam.png"
    [[ -s "$png" ]] && { echo "skip $png" >> $LOG; continue; }
    echo "$(date -u +%FT%TZ) render $side $cam" >> $LOG
    tmpd=$(mktemp -d)
    "$B" -b $BL -P scripts/render_views.py -- --cams $cam --res 1920x1080 --samples 48 --threads 8 --outdir $tmpd >> $LOG 2>&1 && mv "$tmpd/$cam.png" "$png"
    rm -rf "$tmpd"
  done
done
( cd $OUT && md5sum before/*.png after/*.png > md5.txt ); md5sum $LIVE $CAND >> $OUT/md5.txt
echo "$(date -u +%FT%TZ) DONE" | tee -a $LOG; touch $OUT/DONE
