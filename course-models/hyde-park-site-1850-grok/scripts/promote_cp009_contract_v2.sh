#!/usr/bin/env bash
# KEEP CP009 contract v2 (2026-11-09): promote the reviewed CANDIDATE v2 to the live rounds/s02.blend.
# Default: copies the reviewed candidate rounds/candidates/s02_cp009contract_v2.blend (md5 4b36e87a...) to live and tags
# ST_C9_GROUND_WORN with cpl_not_ground (render_shots.py look path ignores it in the horizon-ground scan). This is pixel-
# identical to the reviewed v2 after renders (max diff 0). --rebuild instead regenerates it (scene-equivalent, but Cycles
# lands +-1..3 levels on <0.1% of pixels vs the reviewed afters):
# rebuilds live s02 from the pre-KEEP s02 (md5 0a987ca7..., = git 870ad81:rounds/s02.blend, kept untracked at
# rounds/s02.blend.pre_cp009v2_keep) with scripts/cand_cp009_contract_v2_20261109.py (figures scripts/c9_figures_v2.py),
# then re-renders the live CP009 frames into renders/s02_png at the v2 exposures (start 0.29, end 0.06; other s02 shots keep
# the scene exposure -0.4), 1920x1080, 96 spp, authored lighting kept, --no-people -- identical settings to the v2 after renders.
#   scripts/promote_cp009_contract_v2.sh [--no-build|--rebuild] [samples=96] [outdir=renders/s02_png]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; PRE=rounds/s02.blend.pre_cp009v2_keep
CAND=rounds/candidates/s02_cp009contract_v2.blend
BUILD=copy; [ "${1:-}" = "--no-build" ] && { BUILD=0; shift; }; [ "${1:-}" = "--rebuild" ] && { BUILD=1; shift; }
S=${1:-96}; R=${2:-renders/s02_png}
ES=${EXP_START:-0.29}; EE=${EXP_END:-0.06}
if [ "$BUILD" = copy ]; then
  [ "$(md5sum "$CAND" | cut -c1-8)" = 4b36e87a ] || { echo "candidate v2 md5 mismatch" >&2; exit 1; }
  cp -p "$CAND" rounds/s02.blend
  "$B" -b rounds/s02.blend --python-expr 'import bpy; bpy.data.objects["ST_C9_GROUND_WORN"]["cpl_not_ground"] = True; bpy.ops.wm.save_mainfile(); print("CP009C SAVED rounds/s02.blend (candidate v2 + cpl_not_ground)")' 2>&1 | grep -E "SAVED|Error|Traceback"
  rm -f rounds/s02.blend1; md5sum rounds/s02.blend
fi
if [ "$BUILD" = 1 ]; then
  if [ ! -f "$PRE" ]; then
    if [ "$(md5sum rounds/s02.blend | cut -c1-8)" = 0a987ca7 ]; then cp -p rounds/s02.blend "$PRE"
    else git show 870ad81:course-models/hyde-park-site-1850-grok/rounds/s02.blend > "$PRE"; fi
  fi
  [ "$(md5sum "$PRE" | cut -c1-8)" = 0a987ca7 ] || { echo "pre-KEEP s02 md5 mismatch" >&2; exit 1; }
  "$B" -b "$PRE" -P scripts/cand_cp009_contract_v2_20261109.py -- --out rounds/s02.blend 2>&1 | grep -E "PERSON|SAVED|Error|Traceback"
  md5sum rounds/s02.blend
fi
for CE in CP009_start:$ES CP009_end:$EE; do
  "$B" -b rounds/s02.blend -P scripts/render_shots.py -- --cams "${CE%%:*}" --out "$R" \
    --samples "$S" --pct 100 --keep-lighting --no-people --exposure "${CE##*:}" 2>&1 | grep -E "RENDERED|Error" || true
done
python3 - "$R" <<'PY'
import sys; from PIL import Image
for k in ("start", "end"):
    p = f"{sys.argv[1]}/CP009_{k}"; Image.open(p + ".png").convert("RGB").save(p + ".jpg", quality=92); print("JPG", p + ".jpg")
PY
