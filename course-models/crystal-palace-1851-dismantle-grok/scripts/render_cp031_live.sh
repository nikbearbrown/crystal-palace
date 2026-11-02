#!/usr/bin/env bash
# CP031 LIVE (KEEP 2026-11-02: dressed striker DM24 + maul-face nudge DM25). Renders live rounds/d04_dismantle.blend ->
#   renders/d04/CP031_key_strike_start.png, renders/d04/CP031_lateral_start.png (+ renders/d04/CP031_lateral_start_dusk.png)
# with the exact settings of the KEEP candidate (render_cp031_strike.sh: x05 host, 1280x720, 24 spp, look exposure),
# so a re-run reproduces the live frames pixel-identically.
#   scripts/render_cp031_live.sh [--rebuild]
# --rebuild regenerates live d04_dismantle.blend from the pre-promotion d04 pinned at dismantle commit 7b7171a by running
# scripts/candidate_cp031_strike.py on it with --contact-dy 0.10 (the KEEP candidate script + the face-on-key nudge).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=7b7171a
REL=course-models/crystal-palace-1851-dismantle-grok/rounds/d04_dismantle.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/d04_pre_cp031.blend"
  "$B" -b "$TMP/d04_pre_cp031.blend" -P scripts/candidate_cp031_strike.py -- --contact-dy 0.10 --out "$TMP/d04_dismantle.blend" | grep CP031_INFO
  mv "$TMP/d04_dismantle.blend" rounds/d04_dismantle.blend
  rm -rf "$TMP"
fi
X=../crystal-palace-1851-exterior-grok/rounds/x05.blend
CL=../crystal-palace-1851-claude/crystal-palace-1851.blend
for c in CP031_key_strike_start CP031_lateral_start; do
  "$B" -b "$X" -P scripts/render_dismantle.py -- --dismantle rounds/d04_dismantle.blend --state dismantle --cams "$c" \
    --outdir renders/d04 --res 1280x720 --samples 24 --claude "$CL" | grep -E "WROTE|Error" || true
done
"$B" -b "$X" -P scripts/render_dismantle.py -- --dismantle rounds/d04_dismantle.blend --state dismantle --dusk \
  --cams CP031_lateral_start --outdir renders/d04 --res 1280x720 --samples 24 --claude "$CL" | grep -E "WROTE|Error" || true
echo "done: renders/d04/CP031_key_strike_start.png renders/d04/CP031_lateral_start.png renders/d04/CP031_lateral_start_dusk.png"
