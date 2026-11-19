#!/usr/bin/env bash
# CP059 nave planting burning, night of 30 Nov 1936 KEEP (2026-11-19, D-SY-CP059-01..08): live hero recipe for
#   CAM_CP059_nave_fire_28mm ONLY.
# Round = rounds/sydenham-1936fire-r11b_cp059planting.blend (byte copy of the approved candidate
#   rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend, md5 6dc0707e; candidate commit 1f183d1).
# Recipe = the verified live CP059 hero recipe (r11b_1936fire): RES=960x540 scripts/render.py -- <dir> <tag> 100 32 <cam>
#   (blend's own Filmic -0.5 EV, no people, no look pass; EXPO/KEEP_LIGHTING/NO_PEOPLE/PEOPLE_ERA/THREADS unset).
#   scripts/render_cp059_planting_live.sh [--rebuild] [outdir=renders/r11b_cp059planting]
# --rebuild regenerates the round from rounds/sydenham-1936fire-r11b.blend AS COMMITTED IN 9aff52a (md5 62396fca, extracted from
#   git to a TEMP dir) into a TEMP blend and renders from that (r11b_cp059planting never overwritten).
# Every other camera keeps its current live round (side effects NOT promoted: CAM_CP061_transept_collapse_35mm,
#   CAM_nave_interior_28mm, CAM_section_cut_x-300, CAM_plan_overlay_top, CAM_central_transept_straight,
#   CAM_ext_elevated_overview, CAM_CP001_prologue_distant_35mm stay on their current live rounds).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REL=course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-1936fire-r11b.blend
ROUND=rounds/sydenham-1936fire-r11b_cp059planting.blend; TMP=""
if [[ "${1:-}" == "--rebuild" ]]; then
  shift
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  git show 9aff52a:$REL > "$TMP/1936fire-r11b_9aff52a.blend"
  [[ $(md5sum < "$TMP/1936fire-r11b_9aff52a.blend" | cut -c1-8) == 62396fca ]] || { echo "1936fire-r11b@9aff52a md5 mismatch (expected 62396fca)"; exit 3; }
  env -u CP059_NOSAVE "$B" -b "$TMP/1936fire-r11b_9aff52a.blend" -P scripts/candidate_cp059_burning_planting.py -- "$TMP/sydenham-1936fire-r11b_cp059planting.blend" 2>&1 | grep -E "CP059 |Error|Traceback" || true
  [[ -f "$TMP/sydenham-1936fire-r11b_cp059planting.blend" ]] || { echo "rebuild failed"; exit 3; }
  ROUND="$TMP/sydenham-1936fire-r11b_cp059planting.blend"
fi
OUT=${1:-renders/r11b_cp059planting}; mkdir -p "$OUT"
CHECK='import bpy; c=bpy.data.collections.get("SY36_nave_planting_burning__30Nov1936"); print("CP059_PLANTING_IN_PLACE", c is not None, len(c.all_objects) if c else 0)'
CHK=$("$B" -b "$ROUND" --python-expr "$CHECK" 2>&1 | grep -E "CP059_PLANTING_IN_PLACE" || true)
echo "$CHK"; grep -q "CP059_PLANTING_IN_PLACE True 4" <<<"$CHK" || { echo "$ROUND does not carry the CP059 planting KEEP"; exit 3; }
for CAM in CAM_CP059_nave_fire_28mm; do
  ( unset EXPO KEEP_LIGHTING NO_PEOPLE PEOPLE_ERA PEOPLE_SEED THREADS
    RES=960x540 "$B" -b "$ROUND" -P scripts/render.py -- "$OUT" r11b_1936fireplanting 100 32 "$CAM" 2>&1 | grep -E "Error|Traceback|Saved|RENDERED" || true )
done
echo "done: $OUT/r11b_1936fireplanting_CAM_CP059_nave_fire_28mm.png"
