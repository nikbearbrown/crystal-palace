#!/usr/bin/env bash
# CP014 cams CANDIDATE 2026-11-11 (DEPARTURES KD14-KD16). KEEP 2026-11-11, now LIVE (see scripts/render_cp014_cams_live.sh).
# Builds rounds/candidates/k01_cp014cams.blend from the PRE-KEEP k01 (md5 2c1e3235..., committed at 4f7da40; never from the
# promoted live k01, which already carries KD14_*: the script asserts "candidate already applied") with
# scripts/cand_cp014_cams_20261111.py, then renders every CP014 shot before (pre-KEEP k01) and after (candidate),
# ONE camera per Blender session (same session composition before and after),
# look v1 era 1850 / tod studio, 24 spp, 1280x720 (whole: 720x1280 portrait via its res prop).
# Before exposures = the pre-KEEP live recipes: whole -0.13 (render_cp014_plate_live.sh), roof/gutter/base the look exposure (0.40).
# After exposures re-matched to the before mean luma (env EXP_<CAM>).
#   scripts/render_cp014_cams.sh [samples=24] [outdir=renders/candidates/cp014_cams_20261111]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; S=${1:-24}; R=${2:-renders/candidates/cp014_cams_20261111}
BASE=$(mktemp --suffix=.blend); trap 'rm -f "$BASE"' EXIT
git show 4f7da40:course-models/crystal-palace-1851-construction-grok/rounds/k01.blend > "$BASE"
[[ $(md5sum < "$BASE" | cut -c1-8) == 2c1e3235 ]] || { echo "pre-KEEP k01 md5 mismatch"; exit 3; }
CHK=$("$B" -b "$BASE" --python-expr 'import bpy; print("KD14_PRESENT", any(o.name.startswith("KD14_") for o in bpy.data.objects))' 2>&1 | grep KD14_PRESENT || true)
grep -q "KD14_PRESENT False" <<<"$CHK" || { echo "base already carries KD14 (candidate already applied): $CHK"; exit 3; }
"$B" -b "$BASE" -P scripts/cand_cp014_cams_20261111.py -- --out rounds/candidates/k01_cp014cams.blend 2>&1 | grep -E "KD1|LABELS_OUT|SAVED|Error|Traceback"
declare -A EB=([whole]=-0.13 [roof]=0.40 [gutter]=0.40 [base]=0.40)
declare -A EA=([whole]=${EXP_WHOLE:--0.13} [roof]=${EXP_ROOF:-0.40} [gutter]=${EXP_GUTTER:-0.42} [base]=${EXP_BASE:-0.30})
for c in whole roof gutter base; do
  cam=CP014_drain_${c}_start
  [[ "${SKIP_BEFORE:-0}" == 1 ]] || "$B" -b "$BASE" -P scripts/render_views.py -- --cams $cam --outdir "$R/before" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 --exposure "${EB[$c]}" 2>&1 | grep -E "WROTE|Error" || true
  "$B" -b rounds/candidates/k01_cp014cams.blend -P scripts/render_views.py -- --cams $cam --outdir "$R/after" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 --exposure "${EA[$c]}" 2>&1 | grep -E "WROTE|Error" || true
done
md5sum "$BASE" rounds/k01.blend rounds/candidates/k01_cp014cams.blend
