#!/usr/bin/env bash
# CHATSWORTH ch03 LIVE hero: CP004_lily_tank_start ONLY, from rounds/ch03_cp004lily.blend = CP004 lily house KEEP
# (2026-11-16, parent viewed the pairs; DEPARTURES CH07-CH17). ch03_cp004lily.blend (md5 bdccb859...) is a byte-copy of the
# approved candidate rounds/candidates/ch02_cp004lily.blend, i.e. scripts/candidate_cp004_lilyhouse.py applied to live
# rounds/ch02.blend (md5 59eca5d7..., pinned by tag pre_cp004lily_keep). ch02.blend is NOT changed; the side effects
# (CP004_learning, CP004_lily_underside; CP003 stove cams noise only) were REJECTED and are not routed to ch03
# (scripts/chatsworth_live_heroes.json).
# Recipe = the approved candidate "after" recipe: scripts/render_views.py, look v1 era 1840s / tod exterior_midday,
# 1920x1080 (film 1080p delivery), 48 spp, 8 threads, one camera per Blender session.
# The pre-KEEP frame renders/ch02/CP004_lily_tank_start.png stays in place.
#   scripts/render_cp004_lily_live.sh [--rebuild] [outdir=renders/ch03]
# --rebuild regenerates the round from ch02.blend (md5-checked) with candidate_cp004_lilyhouse.py into a TEMP blend and
# renders from that (rounds/ch03_cp004lily.blend is never overwritten), so outdir PNGs can be diffed against the live hero.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/ch03_cp004lily.blend; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
CHECK='import bpy; n=sum(1 for o in bpy.data.objects if o.name.startswith("CP4_")); print("CP004_LILY_IN_PLACE", "CP4_LILY_HOUSE_1850" in bpy.data.collections and n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/ch02.blend | cut -c1-8) == 59eca5d7 ]] || { echo "ch02.blend md5 mismatch (expected 59eca5d7)"; exit 3; }
  "$B" -b rounds/ch02.blend -P scripts/candidate_cp004_lilyhouse.py -- --out "$TMP/ch03_cp004lily.blend" 2>&1 | grep -E "CP004_CANDIDATE_SAVED|Error|Traceback" | cut -c1-200 || true
  [[ -f "$TMP/ch03_cp004lily.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/ch03_cp004lily.blend"
else
  [[ $(md5sum < "$ROUND" | cut -c1-8) == bdccb859 ]] || { echo "$ROUND md5 mismatch (expected bdccb859)"; exit 3; }
fi
OUT=${1:-renders/ch03}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP004_LILY_IN_PLACE" || true)
echo "$CHK"; grep -q "CP004_LILY_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP004 lily house KEEP"; exit 3; }
CAM=CP004_lily_tank_start
mkdir -p "$TMP/r"
"$B" -b "$ROUND" -P scripts/render_views.py -- --cams $CAM --res 1920x1080 --samples 48 --era 1840s --tod exterior_midday --threads 8 --outdir "$TMP/r" > "$TMP/render.log" 2>&1 || { tail -20 "$TMP/render.log"; exit 3; }
mv "$TMP/r/$CAM.png" "$OUT/$CAM.png"
echo "done: $OUT/$CAM.png"
