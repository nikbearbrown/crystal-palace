#!/usr/bin/env bash
# CP009 "contract" CANDIDATE 2026-11-04 (DEPARTURES SD28-SD31; NOT live, awaiting review). Builds
# rounds/candidates/s02_cp009contract.blend from the live rounds/s02.blend (never written) via
# scripts/cand_cp009_contract_20261104.py, then renders CP009_start/_end at the live s02 settings (1920x1080, 96 spp,
# authored lighting kept, --no-people because the figures are fixed people_lib v3.4 builds) with exposure re-matched to
# the live renders/s02_png mean luma (start 123.55, end 120.47 at 960x540 grey).
#   scripts/render_cp009_contract.sh [samples=96] [outdir=renders/candidates/cp009_contract_20261104/after]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
S=${1:-96}; R=${2:-renders/candidates/cp009_contract_20261104/after}
ES=${EXP_START:-0.68}; EE=${EXP_END:-0.22}
mkdir -p rounds/candidates
"$B" -b rounds/s02.blend -P scripts/cand_cp009_contract_20261104.py -- --out rounds/candidates/s02_cp009contract.blend 2>&1 | grep -E "PERSON|SAVED|Error|Traceback"
for CE in CP009_start:$ES CP009_end:$EE; do
  "$B" -b rounds/candidates/s02_cp009contract.blend -P scripts/render_shots.py -- --cams "${CE%%:*}" --out "$R" \
    --samples "$S" --pct 100 --keep-lighting --no-people --exposure "${CE##*:}" 2>&1 | grep -E "RENDERED|Error" || true
done
