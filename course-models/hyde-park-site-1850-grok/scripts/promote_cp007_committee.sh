#!/usr/bin/env bash
# KEEP CP007 committee (2026-11-10): promote the reviewed CANDIDATE to the live rounds/s02.blend.
# Byte-copies the reviewed candidate rounds/candidates/s02_cp007committee.blend (md5 cfadb9c7..., built from live fc771aba by
# scripts/cand_cp007_committee_20261110.py, site ed9045d) over live rounds/s02.blend -- no rebuild, so live is the exact file
# whose after render was reviewed (f/8 DOF on CP007_start kept, SD49). The pre-KEEP live is kept untracked at
# rounds/s02.blend.pre_cp007committee_keep (md5 fc771aba, = git 36f7f30:rounds/s02.blend). Then re-renders live CP007_start
# into renders/s02_png with the candidate recipe (1920x1080, 96 spp, --keep-lighting --no-people, exposure 0.85).
#   scripts/promote_cp007_committee.sh [--no-copy] [samples=96] [outdir=renders/s02_png]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; PRE=rounds/s02.blend.pre_cp007committee_keep; CAND=rounds/candidates/s02_cp007committee.blend
COPY=1; [ "${1:-}" = "--no-copy" ] && { COPY=0; shift; }
S=${1:-96}; R=${2:-renders/s02_png}
ES=${EXP_START:-0.85}
if [ "$COPY" = 1 ]; then
  [ "$(md5sum "$CAND" | cut -c1-8)" = cfadb9c7 ] || { echo "candidate md5 mismatch" >&2; exit 1; }
  if [ ! -f "$PRE" ]; then
    [ "$(md5sum rounds/s02.blend | cut -c1-8)" = fc771aba ] || { echo "live s02 is not fc771aba; refusing" >&2; exit 1; }
    cp -p rounds/s02.blend "$PRE"
  fi
  [ "$(md5sum "$PRE" | cut -c1-8)" = fc771aba ] || { echo "pre-KEEP backup md5 mismatch" >&2; exit 1; }
  cp -p "$CAND" rounds/s02.blend; md5sum rounds/s02.blend
fi
"$B" -b rounds/s02.blend -P scripts/render_shots.py -- --cams CP007_start --out "$R" --samples "$S" --pct 100 --keep-lighting --no-people --exposure "$ES" 2>&1 | grep -E "RENDERED|Error" || true
python3 - "$R" <<'PY'
import sys; from PIL import Image
p = f"{sys.argv[1]}/CP007_start"; Image.open(p + ".png").convert("RGB").save(p + ".jpg", quality=92); print("JPG", p + ".jpg")
PY
echo CP007_PROMOTE_DONE
