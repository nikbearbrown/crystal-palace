#!/usr/bin/env bash
# PARK-NOW r23 LIVE hero: CAM_CP074_dinosaurs_35mm ONLY, from rounds/parknow-r23_cp074.blend = CP074 Geological Court
# present-day KEEP (2026-11-16, parent viewed the pairs; DEPARTURES D-PM-50..57). parknow-r23_cp074.blend (md5 2e9ad6a6...)
# is a byte-copy of the approved candidate rounds/candidates/parknow-r01_cp074geocourt.blend, i.e.
# scripts/candidate_cp074_geocourt.py applied to rounds/parknow-r01.blend (md5 fb640758..., the blend the pre-keep hero
# renders/r01_parknow_CAM_CP074_dinosaurs_35mm.png was actually rendered from; pinned by tag pre_cp074_keep).
# parknow-r01.blend and parknow-r02.blend are NOT changed; the side effects (CP074 iguanodon_50mm, CP075 layered_nsc,
# CP066 nsc_wide, CP072 footprint) were REJECTED and are not routed to r23.
# Recipe = the approved candidate "after" recipe: survey look/apply_render.py (look v1.1, present / exterior_afternoon,
# exposure -0.8, --no-people), 1920x1080 (film 1080p delivery), 48 spp, one camera per Blender session.
# The pre-KEEP frame renders/r01_parknow_CAM_CP074_dinosaurs_35mm.png stays in place.
#   scripts/render_cp074_geocourt_live.sh [--rebuild] [outdir=renders]
# --rebuild regenerates the round from parknow-r01.blend (md5-checked) with candidate_cp074_geocourt.py into a TEMP blend
# and renders from that (rounds/parknow-r23_cp074.blend is never overwritten), so outdir PNGs can be diffed against the live hero.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; LOOK=/workspace/crystal-palace-survey/look/apply_render.py
ROUND=rounds/parknow-r23_cp074.blend; TMP=""
CHECK='import bpy; n=sum(1 for o in bpy.data.objects if "cp074_now" in o.keys()); print("CP074_NOW_IN_PLACE", n > 0, n)'
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  [[ $(md5sum < rounds/parknow-r01.blend | cut -c1-8) == fb640758 ]] || { echo "parknow-r01.blend md5 mismatch (expected fb640758)"; exit 3; }
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  "$B" -b rounds/parknow-r01.blend -P scripts/candidate_cp074_geocourt.py -- --out "$TMP/parknow-r23_cp074.blend" 2>&1 | grep -E "CP074_CANDIDATE_SAVED|Error|Traceback" || true
  [[ -f "$TMP/parknow-r23_cp074.blend" ]] || { echo "rebuild failed"; exit 3; }
  git checkout -- checks/cp074_geocourt_candidate.json 2>/dev/null || true   # candidate script rewrites its log; keep the committed one
  ROUND="$TMP/parknow-r23_cp074.blend"
fi
OUT=${1:-renders}; mkdir -p "$OUT"
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP074_NOW_IN_PLACE" || true)
echo "$CHK"; grep -q "CP074_NOW_IN_PLACE True" <<<"$CHK" || { echo "$ROUND does not carry the CP074 KEEP"; exit 3; }
CAM=CAM_CP074_dinosaurs_35mm
"$B" -b "$ROUND" -P "$LOOK" -- --cam $CAM --out "$OUT/r23_parknow_${CAM}.png" --scene-id CP074 --era present --tod exterior_afternoon --spp 48 --res 1920x1080 --no-people 2>&1 | grep -E "RENDERED|Saved|Error|Traceback" || true
echo "done: $OUT/r23_parknow_${CAM}.png"
