#!/usr/bin/env bash
# KEEP CP006 winterpark (2026-11-09): promote the reviewed CANDIDATE to the live rounds/s02.blend.
# Byte-copies the reviewed candidate rounds/candidates/s02_cp006park.blend (md5 fc771aba..., built from live ab2d25d4 by
# scripts/cand_cp006_winterpark_20261109.py, site da068d0) over live rounds/s02.blend -- no rebuild, so live is the exact file
# whose after renders were reviewed. The pre-KEEP live is kept untracked at rounds/s02.blend.pre_cp006park_keep (md5 ab2d25d4,
# = git 367ae93:rounds/s02.blend). Then re-renders live CP006 into renders/s02_png with the candidate recipes
# (1920x1080, 96 spp, --no-people; start --keep-lighting exposure 0.14, end look v1.1 path exposure -0.50).
#   scripts/promote_cp006_winterpark.sh [--no-copy] [samples=96] [outdir=renders/s02_png]
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; PRE=rounds/s02.blend.pre_cp006park_keep; CAND=rounds/candidates/s02_cp006park.blend
COPY=1; [ "${1:-}" = "--no-copy" ] && { COPY=0; shift; }
S=${1:-96}; R=${2:-renders/s02_png}
ES=${EXP_START:-0.14}; EE=${EXP_END:--0.50}
if [ "$COPY" = 1 ]; then
  [ "$(md5sum "$CAND" | cut -c1-8)" = fc771aba ] || { echo "candidate md5 mismatch" >&2; exit 1; }
  if [ ! -f "$PRE" ]; then
    [ "$(md5sum rounds/s02.blend | cut -c1-8)" = ab2d25d4 ] || { echo "live s02 is not ab2d25d4; refusing" >&2; exit 1; }
    cp -p rounds/s02.blend "$PRE"
  fi
  cp -p "$CAND" rounds/s02.blend; md5sum rounds/s02.blend
fi
"$B" -b rounds/s02.blend -P scripts/render_shots.py -- --cams CP006_start --out "$R" --samples "$S" --pct 100 --keep-lighting --no-people --exposure "$ES" 2>&1 | grep -E "RENDERED|Error" || true
"$B" -b rounds/s02.blend -P scripts/render_shots.py -- --cams CP006_end --out "$R" --samples "$S" --pct 100 --no-people --exposure "$EE" 2>&1 | grep -E "RENDERED|Error" || true
python3 - "$R" <<'PY'
import sys; from PIL import Image
for k in ("start", "end"):
    p = f"{sys.argv[1]}/CP006_{k}"; Image.open(p + ".png").convert("RGB").save(p + ".jpg", quality=92); print("JPG", p + ".jpg")
PY
echo CP006_PROMOTE_DONE
