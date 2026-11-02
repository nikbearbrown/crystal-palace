#!/usr/bin/env bash
# CP031 stale-view refresh (2026-11-02). Renders the d04 dismantle views that still showed the r09 stand-in striker
# (CP031_joint_detail_start, CP031_lateral_end, REV_dismantle_aerial_start, + CP031_lateral_end dusk) with the exact
# settings of the live CP031 frames (render_cp031_live.sh: x05 host, 1280x720, 24 spp, look exposure).
#   scripts/render_cp031_stale.sh                -> live rounds/d04_dismantle.blend into renders/d04
#   scripts/render_cp031_stale.sh --before DIR   -> pre-CP031 d04 pinned at dismantle 7b7171a into DIR (for pairs)
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BLEND=rounds/d04_dismantle.blend; OUT=renders/d04; TMP=""
if [[ "${1:-}" == "--before" ]]; then
  OUT=${2:?outdir}; TMP=$(mktemp -d)
  git show "7b7171a:course-models/crystal-palace-1851-dismantle-grok/rounds/d04_dismantle.blend" > "$TMP/d04_pre_cp031.blend"
  BLEND="$TMP/d04_pre_cp031.blend"
fi
mkdir -p "$OUT"
X=../crystal-palace-1851-exterior-grok/rounds/x05.blend
CL=../crystal-palace-1851-claude/crystal-palace-1851.blend
for c in CP031_joint_detail_start CP031_lateral_end REV_dismantle_aerial_start; do
  "$B" -b "$X" -P scripts/render_dismantle.py -- --dismantle "$BLEND" --state dismantle --cams "$c" \
    --outdir "$OUT" --res 1280x720 --samples 24 --claude "$CL" | grep -E "WROTE|Error" || true
done
"$B" -b "$X" -P scripts/render_dismantle.py -- --dismantle "$BLEND" --state dismantle --dusk \
  --cams CP031_lateral_end --outdir "$OUT" --res 1280x720 --samples 24 --claude "$CL" | grep -E "WROTE|Error" || true
[[ -n "$TMP" ]] && rm -rf "$TMP"
echo "done: $OUT"
