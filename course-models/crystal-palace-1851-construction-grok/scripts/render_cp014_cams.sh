#!/usr/bin/env bash
# CP014 cams CANDIDATE 2026-11-11 (DEPARTURES KD14-KD16; no verdict, NOT live). Builds rounds/candidates/k01_cp014cams.blend
# from the LIVE k01 (md5 2c1e3235..., never written) with scripts/cand_cp014_cams_20261111.py, then renders every CP014 shot
# before (live k01) and after (candidate), ONE camera per Blender session (same session composition before and after),
# look v1 era 1850 / tod studio, 24 spp, 1280x720 (whole: 720x1280 portrait via its res prop).
# Before exposures = the live recipes: whole -0.13 (render_cp014_plate_live.sh), roof/gutter/base the look exposure (0.40).
# After exposures re-matched to the before mean luma (env EXP_<CAM>).
#   scripts/render_cp014_cams.sh [samples=24] [outdir=renders/candidates/cp014_cams_20261111]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; S=${1:-24}; R=${2:-renders/candidates/cp014_cams_20261111}
[[ $(md5sum < rounds/k01.blend | cut -c1-8) == 2c1e3235 ]] || { echo "live k01 md5 mismatch"; exit 3; }
"$B" -b rounds/k01.blend -P scripts/cand_cp014_cams_20261111.py -- --out rounds/candidates/k01_cp014cams.blend 2>&1 | grep -E "KD1|LABELS_OUT|SAVED|Error|Traceback"
declare -A EB=([whole]=-0.13 [roof]=0.40 [gutter]=0.40 [base]=0.40)
declare -A EA=([whole]=${EXP_WHOLE:--0.13} [roof]=${EXP_ROOF:-0.40} [gutter]=${EXP_GUTTER:-0.42} [base]=${EXP_BASE:-0.30})
for c in whole roof gutter base; do
  cam=CP014_drain_${c}_start
  [[ "${SKIP_BEFORE:-0}" == 1 ]] || "$B" -b rounds/k01.blend -P scripts/render_views.py -- --cams $cam --outdir "$R/before" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 --exposure "${EB[$c]}" 2>&1 | grep -E "WROTE|Error" || true
  "$B" -b rounds/candidates/k01_cp014cams.blend -P scripts/render_views.py -- --cams $cam --outdir "$R/after" --res 1280x720 --samples "$S" --era 1850 --tod studio --threads 8 --exposure "${EA[$c]}" 2>&1 | grep -E "WROTE|Error" || true
done
md5sum rounds/k01.blend rounds/candidates/k01_cp014cams.blend
