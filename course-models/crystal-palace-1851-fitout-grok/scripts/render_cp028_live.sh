#!/usr/bin/env bash
# CP028 LIVE (KEEP 2026-11-02: louvre drive v2, FT51-FT54). Renders live rounds/h03.blend -> renders/h03/CP028_louvre_start.png
# with the exact settings of the v2 candidate (1280x720, 48 spp, --keep-lighting, --no-people), so the live frame is
# pixel-identical to renders/candidates/cp028_drive_v2_20261102/after/CP028_louvre_start.png.
#   scripts/render_cp028_live.sh [--rebuild]
# --rebuild regenerates live h03 from the pre-promotion h03 pinned at fitout commit 7b25192 by running
# scripts/polish_cp028_drive_v2_cand.py on it (the same script that built the KEEP candidate).
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
BASE_COMMIT=7b25192
REL=course-models/crystal-palace-1851-fitout-grok/rounds/h03.blend
if [[ "${1:-}" == "--rebuild" ]]; then
  TMP=$(mktemp -d)
  git show "$BASE_COMMIT:$REL" > "$TMP/h03_pre_cp028_drive.blend"
  "$B" -b -P scripts/polish_cp028_drive_v2_cand.py -- --src "$TMP/h03_pre_cp028_drive.blend" --out "$TMP/h03.blend"
  mv "$TMP/h03.blend" rounds/h03.blend
  rm -rf "$TMP"
fi
"$B" -b rounds/h03.blend -P scripts/render_views.py -- --cams CP028_louvre_start --res 1280x720 --samples 48 --no-people --keep-lighting --outdir renders/h03
echo "done: renders/h03/CP028_louvre_start.png"
