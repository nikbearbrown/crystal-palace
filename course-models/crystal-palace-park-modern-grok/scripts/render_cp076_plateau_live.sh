#!/usr/bin/env bash
# CP076 LIVE heroes (both cams) from rounds/parknow-r21_cp076.blend = CP076 plateau KEEP (2026-11-11, parent viewed the pairs;
# DEPARTURES D-PM-26..31). parknow-r21_cp076.blend (md5 bc62d275...) is a byte-copy of the candidate
# rounds/candidates/parknow-r02_cp076plateau.blend, i.e. scripts/candidate_cp076_plateau.py applied to live
# rounds/parknow-r02.blend (md5 48fc01ec..., pinned by tag pre_cp076plateau_keep). parknow-r02.blend is NOT changed and
# still serves CP067/CP070/CP072/CP074/CP075 (plateau side effects on CP070/CP072/CP075 were REJECTED). Only the CP076 cams
# render from r21 (manifest: scripts/parknow_live_heroes.json).
# Recipe = scripts/render_cp076_look.py (dud-fix v4: look v1.1 present/exterior_afternoon, 1280x720, 32 spp, exposure -0.8),
# one camera per Blender session.
#   scripts/render_cp076_plateau_live.sh [--rebuild] [outdir=renders]
# --rebuild regenerates rounds/parknow-r21_cp076.blend from parknow-r02.blend (md5-checked) with candidate_cp076_plateau.py.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
CHECK='import bpy; n=sum(1 for o in bpy.data.objects if "cp076_now" in o.keys()); print("CP076_PLATEAU_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/parknow-r02.blend | cut -c1-8) == 48fc01ec ]] || { echo "parknow-r02.blend md5 mismatch (expected 48fc01ec)"; exit 3; }
  TMP=$(mktemp -d)
  "$B" -b rounds/parknow-r02.blend -P scripts/candidate_cp076_plateau.py -- --out "$TMP/parknow-r21_cp076.blend" 2>&1 | grep -E "CP076_CANDIDATE_SAVED|Error|Traceback" || true
  [[ -f "$TMP/parknow-r21_cp076.blend" ]] || { echo "rebuild failed"; rm -rf "$TMP"; exit 3; }
  mv "$TMP/parknow-r21_cp076.blend" rounds/parknow-r21_cp076.blend; rm -rf "$TMP"
  git checkout -- checks/cp076_plateau_candidate.json 2>/dev/null || true   # candidate script rewrites its log; keep the committed one
fi
OUT=${1:-renders}
CHK=$("$B" -b rounds/parknow-r21_cp076.blend --python-expr "$CHECK" 2>&1 | grep -E "CP076_PLATEAU_IN_PLACE" || true)
echo "$CHK"; grep -q "CP076_PLATEAU_IN_PLACE True" <<<"$CHK" || { echo "parknow-r21_cp076.blend does not carry the CP076 plateau KEEP (run with --rebuild)"; exit 3; }
for CAM in CAM_CP076_empty_plateau_35mm CAM_CP076_hold_35mm; do
  "$B" -b rounds/parknow-r21_cp076.blend -P scripts/render_cp076_look.py -- "$OUT/r21_parknow_${CAM}.png" "$CAM" CP076 -0.8 2>&1 | grep -E "RENDERED|Error|Traceback" || true
done
echo "done: $OUT/r21_parknow_CAM_CP076_{empty_plateau,hold}_35mm.png"
