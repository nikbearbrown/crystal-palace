#!/usr/bin/env bash
# CP020 nave KEEP regression (2026-11-11): pre-keep pin vs live f03, same live recipes both sides (scripts/render_f03_others_live.sh)
# -> /workspace/tmp/cp020keep/fin/{pre,live}; numbers in checks/cp020_nave_keep_regression.json
set -euo pipefail
cd "$(dirname "$0")/.."
scripts/render_f03_others_live.sh rounds/f03.blend.pre_cp020nave_keep /workspace/tmp/cp020keep/fin/pre
scripts/render_f03_others_live.sh rounds/f03.blend /workspace/tmp/cp020keep/fin/live
echo CP020_KEEP_REGRESS_DONE
