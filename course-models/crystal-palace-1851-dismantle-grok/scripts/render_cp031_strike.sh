#!/usr/bin/env bash
# CANDIDATE CP031 key strike (2026-11-02, no verdict). Rebuilds the sibling candidate blend from the live
# rounds/d04_dismantle.blend (never overwritten) and renders both CP031 strike cams at 1280x720, 24 spp, look exposure.
#   scripts/render_cp031_strike.sh [--rebuild] [outdir]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
REBUILD=0; [[ "${1:-}" == "--rebuild" ]] && { REBUILD=1; shift; }
OUT=${1:-renders/candidates/cp031_strike_20261102}
CAND=rounds/candidates/d04_cp031strike.blend
if [[ $REBUILD == 1 || ! -f $CAND ]]; then
  "$B" -b rounds/d04_dismantle.blend -P scripts/candidate_cp031_strike.py -- --out "$CAND" | grep CP031_INFO
fi
for c in CP031_key_strike_start CP031_lateral_start; do
  "$B" -b ../crystal-palace-1851-exterior-grok/rounds/x05.blend -P scripts/render_dismantle.py -- \
    --dismantle "$CAND" --state dismantle --cams "$c" --outdir "$OUT" --res 1280x720 --samples 24 \
    --claude ../crystal-palace-1851-claude/crystal-palace-1851.blend | grep -E "WROTE|Error" || true
done
