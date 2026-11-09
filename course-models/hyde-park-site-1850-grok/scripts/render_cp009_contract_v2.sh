#!/usr/bin/env bash
# CP009 "contract" CANDIDATE v2 2026-11-09 (DEPARTURES SD28-SD30 kept, SD31 withdrawn, SD32-SD34; NOT live, awaiting review).
# Builds rounds/candidates/s02_cp009contract_v2.blend from the live rounds/s02.blend (never written) via
# scripts/cand_cp009_contract_v2_20261109.py (figures: scripts/c9_figures_v2.py), then renders CP009_start/_end at the live
# s02 settings (1920x1080, 96 spp, authored lighting kept, --no-people) with exposure matched to live renders/s02_png mean
# luma (start 123.55, end 120.47 at 960x540 grey). Live exposure is -0.4; v2 needs only +0.69 / +0.46 stop (v1 needed +1.08 / +0.62).
#   scripts/render_cp009_contract_v2.sh [samples=96] [outdir=renders/candidates/cp009_contract_v2_20261109/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-96}; R=${2:-renders/candidates/cp009_contract_v2_20261109/after}
ES=${EXP_START:-0.29}; EE=${EXP_END:-0.06}
mkdir -p rounds/candidates
"$B" -b rounds/s02.blend -P scripts/cand_cp009_contract_v2_20261109.py -- --out rounds/candidates/s02_cp009contract_v2.blend 2>&1 | grep -E "PERSON|SAVED|Error|Traceback"
for CE in CP009_start:$ES CP009_end:$EE; do
  "$B" -b rounds/candidates/s02_cp009contract_v2.blend -P scripts/render_shots.py -- --cams "${CE%%:*}" --out "$R" \
    --samples "$S" --pct 100 --keep-lighting --no-people --exposure "${CE##*:}" 2>&1 | grep -E "RENDERED|Error" || true
done
