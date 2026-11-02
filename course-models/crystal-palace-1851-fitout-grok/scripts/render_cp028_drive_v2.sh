#!/usr/bin/env bash
# CP028 louvre-drive CANDIDATE v2 (FT54 restaged; v1 REJECTED): before (live h03) / after (rounds/candidates/h03_cp028_drive_v2.blend).
# Same camera, same settings: 1280x720, 48 spp, --keep-lighting (authored h03 exposure -0.7; this is
# what reproduces the live renders/h03/CP028_louvre_start.png, mean diff ~1.5/255), --no-people.
#   scripts/render_cp028_drive_v2.sh [--rebuild]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
OUT=renders/candidates/cp028_drive_v2_20261102
mkdir -p "$OUT/before" "$OUT/after"
if [[ "${1:-}" == "--rebuild" || ! -f rounds/candidates/h03_cp028_drive_v2.blend ]]; then
  "$B" -b -P scripts/polish_cp028_drive_v2_cand.py -- --src rounds/h03.blend --out rounds/candidates/h03_cp028_drive_v2.blend
fi
ARGS=(--cams CP028_louvre_start --res 1280x720 --samples 48 --no-people --keep-lighting)
"$B" -b rounds/h03.blend -P scripts/render_views.py -- "${ARGS[@]}" --outdir "$OUT/before"
"$B" -b rounds/candidates/h03_cp028_drive_v2.blend -P scripts/render_views.py -- "${ARGS[@]}" --outdir "$OUT/after"
echo "done: $OUT/{before,after}/CP028_louvre_start.png"
