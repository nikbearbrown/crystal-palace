#!/usr/bin/env bash
# FOOTBALL fb04 LIVE hero: CP050_bank_1895_start ONLY, from rounds/fb04_1895_cp050cup.blend = CP050 FA Cup Final
# 20 April 1895 KEEP (2026-11-16, parent viewed the pairs; DEPARTURES D-FB-CP050-01..11). fb04_1895_cp050cup.blend
# (md5 27e0525d...) is a byte-copy of the approved candidate rounds/candidates/fb02_1895_cp050cup.blend, i.e.
# scripts/candidate_cp050_cupfinal1895.py applied to live rounds/fb02_1895.blend (md5 d8b263c0..., pinned by tag
# pre_cp050cup_keep). fb02_1895.blend is NOT changed; the side effect CP050_pavilion_1895_start was REJECTED and is not
# routed to fb04 (scripts/football_live_heroes.json). (fb03/fb03b_1895 were the reverted set_v18 attempt, not used.)
# Recipe = the approved candidate "after" recipe: scripts/render_views.py, no --era / no people swap, file exposure 0.0,
# 1920x1080 (film 1080p delivery), 48 spp, 8 threads, one camera per Blender session.
# The pre-KEEP frame renders/fb02_1895/CP050_bank_1895_start.png stays in place.
#   scripts/render_cp050_cup_live.sh [--rebuild] [outdir=renders/fb04_1895]
# --rebuild regenerates the round from fb02_1895.blend (md5-checked) with candidate_cp050_cupfinal1895.py into a TEMP
# blend and renders from that (rounds/fb04_1895_cp050cup.blend is never overwritten), so outdir PNGs can be diffed
# against the live hero.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/fb04_1895_cp050cup.blend; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
CHECK='import bpy; c=bpy.data.collections.get("FB95_cup_final__1895-04-20"); print("CP050_CUP_IN_PLACE", c is not None and len(c.all_objects) > 0, len(c.all_objects) if c else 0)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/fb02_1895.blend | cut -c1-8) == d8b263c0 ]] || { echo "fb02_1895.blend md5 mismatch (expected d8b263c0)"; exit 3; }
  "$B" -b rounds/fb02_1895.blend -P scripts/candidate_cp050_cupfinal1895.py -- --out "$TMP/fb04_1895_cp050cup.blend" 2>&1 | grep -E "CP050_CANDIDATE_SAVED|Error|Traceback" | cut -c1-200 || true
  [[ -f "$TMP/fb04_1895_cp050cup.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/fb04_1895_cp050cup.blend"
else
  [[ $(md5sum < "$ROUND" | cut -c1-8) == 27e0525d ]] || { echo "$ROUND md5 mismatch (expected 27e0525d)"; exit 3; }
fi
OUT=${1:-renders/fb04_1895}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP050_CUP_IN_PLACE" || true)
echo "$CHK"; grep -q "CP050_CUP_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP050 Cup Final KEEP"; exit 3; }
CAM=CP050_bank_1895_start
mkdir -p "$TMP/r"
"$B" -b "$ROUND" -P scripts/render_views.py -- --cams $CAM --res 1920x1080 --samples 48 --threads 8 --outdir "$TMP/r" > "$TMP/render.log" 2>&1 || { tail -20 "$TMP/render.log"; exit 3; }
mv "$TMP/r/$CAM.png" "$OUT/$CAM.png"
echo "done: $OUT/$CAM.png"
