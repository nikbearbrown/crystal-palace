#!/usr/bin/env bash
# PARK60 r18 LIVE hero: CAM_CP066_nsc_stadium_35mm ONLY, from rounds/park60-r18_cp066.blend = CP066 NSC 1964-67 KEEP
# (2026-11-16, parent viewed the pairs; DEPARTURES D-PM-42..49). park60-r18_cp066.blend (md5 19af4411...) is a byte-copy of the
# approved candidate rounds/candidates/park60-r17_cp066nsc64.blend, i.e. scripts/candidate_cp066_nsc64.py applied to live
# rounds/park60-r17.blend (md5 9ea1c796..., pinned by tag pre_cp066nsc_keep). park60-r17.blend is NOT changed; the side effects
# (CP066 nsc_wide, CP066 nsc_hall, park60 CP065 hl_closed + subway_threshold) were REJECTED and are not routed to r18.
# Recipe = the approved candidate "after" recipe = the live CP066 recipe: scripts/render_cp076_look.py, scene id CP066
# (look v1.1 present / exterior_afternoon, exposure from the look = -0.8), 1920x1080 (film 1080p delivery), 48 spp,
# one camera per Blender session. The pre-KEEP frame renders/r17k_park60_CAM_CP066_nsc_stadium_35mm.png stays in place.
#   scripts/render_cp066_nsc_live.sh [--rebuild] [outdir=renders]
# --rebuild regenerates the round from park60-r17.blend (md5-checked) with candidate_cp066_nsc64.py into a TEMP blend and
# renders from that (rounds/park60-r18_cp066.blend is never overwritten), so outdir PNGs can be diffed against the live hero.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/park60-r18_cp066.blend; TMP=""
CHECK='import bpy; n=sum(1 for o in bpy.data.objects if "cp066_nsc" in o.keys()); print("CP066_NSC_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/park60-r17.blend | cut -c1-8) == 9ea1c796 ]] || { echo "park60-r17.blend md5 mismatch (expected 9ea1c796)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/park60-r17.blend -P scripts/candidate_cp066_nsc64.py -- --out "$TMP/park60-r18_cp066.blend" 2>&1 | grep -E "CP066_CANDIDATE_SAVED|Error|Traceback" || true
  [[ -f "$TMP/park60-r18_cp066.blend" ]] || { echo "rebuild failed"; exit 3; }
  git checkout -- checks/cp066_nsc64_candidate.json 2>/dev/null || true   # candidate script rewrites its log; keep the committed one
  ROUND="$TMP/park60-r18_cp066.blend"
fi
OUT=${1:-renders}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP066_NSC_IN_PLACE" || true)
echo "$CHK"; grep -q "CP066_NSC_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP066 NSC KEEP"; exit 3; }
CAM=CAM_CP066_nsc_stadium_35mm
"$B" -b "$ROUND" -P scripts/render_cp076_look.py -- "$OUT/r18_park60_${CAM}.png" "$CAM" CP066 none 1920x1080 48 2>&1 | grep -E "RENDERED|Error|Traceback" || true
echo "done: $OUT/r18_park60_${CAM}.png"
