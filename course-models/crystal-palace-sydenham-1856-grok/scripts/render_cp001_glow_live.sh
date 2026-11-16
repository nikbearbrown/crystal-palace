#!/usr/bin/env bash
# SYDENHAM r18 1936 LIVE hero: CP001 prologue_distant 35mm ONLY, from rounds/sydenham-1936-r19_cp001glow.blend =
# CP001 glow on the hill KEEP (2026-11-16, parent viewed the pairs; DEPARTURES D-SY-CP001-01..12).
# 1936-r19_cp001glow (md5 a348d548...) is a byte copy of the approved candidate rounds/candidates/sydenham-1936-r18b_cp001glow.blend,
# i.e. scripts/candidate_cp001_glow.py applied to live rounds/sydenham-1936-r18b.blend (md5 66edd7cd..., pinned by tag
# pre_cp001glow_keep). 1936-r18b is NOT changed; the candidate's 18 side-effect cameras in that round (night world, CP038/CP041/
# CP047/CP048/CP057-CP062/CP064/CP072/CP073 views) were REJECTED / not routed and stay on their current live rounds.
# Only CAM_CP001_prologue_distant_35mm renders from 1936-r19_cp001glow (manifest: scripts/sydenham_live_heroes.json).
# Recipe = the approved candidate "after" recipe (scripts/render_cp001_candidate.sh = the live CP001 hero recipe):
#   render.py, NO_PEOPLE=1, KEEP_LIGHTING=1 (blend exposure Filmic -1.0 EV), 1280x720, 48 spp, one camera per Blender session.
#   scripts/render_cp001_glow_live.sh [--rebuild] [outdir=renders/r18]
# --rebuild regenerates the round from 1936-r18b (md5-checked) into a TEMP blend and renders from that (1936-r19_cp001glow never overwritten).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
ROUND=rounds/sydenham-1936-r19_cp001glow.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/sydenham-1936-r18b.blend | cut -c1-8) == 66edd7cd ]] || { echo "1936-r18b md5 mismatch (expected 66edd7cd)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  env -u CP001_NOSAVE "$B" -b rounds/sydenham-1936-r18b.blend -P scripts/candidate_cp001_glow.py -- "$TMP/sydenham-1936-r19_cp001glow.blend" 2>&1 | grep -E "CP001 (SAVED|BUILT)|Error|Traceback" || true
  [[ -f "$TMP/sydenham-1936-r19_cp001glow.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1936-r19_cp001glow.blend"
fi
OUT=${1:-renders/r18}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY36_prologue_glow__30Nov1936_c1945"); print("CP001_GLOW_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP001_GLOW_IN_PLACE" || true)
echo "$CHK"; grep -q "CP001_GLOW_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP001 glow KEEP"; exit 3; }
export NO_PEOPLE=1 KEEP_LIGHTING=1 RES=1280x720 THREADS=8
for CAM in CAM_CP001_prologue_distant_35mm; do
  "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r18_1936glow 100 48 "$CAM" 2>&1 | grep -E "KEEP_LIGHTING|PEOPLE_ADOPT|RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r18_1936glow_CAM_CP001_prologue_distant_35mm.png"
