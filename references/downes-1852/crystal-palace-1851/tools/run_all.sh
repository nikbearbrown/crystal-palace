#!/bin/bash
# Re-run every plate measurement and write the output, with the versions and plate checksums, to
# tools/output/run-<date>.txt. Usage: bash tools/run_all.sh   (from anywhere)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLATES="$HERE/../../source-scans/plates"
OUT="$HERE/output"
mkdir -p "$OUT"
FILE="$OUT/run-$(date +%Y-%m-%d).txt"
{
  echo "# Crystal Palace plate measurements, run $(date '+%Y-%m-%d %H:%M')"
  python3 -I -c "import sys,numpy,cv2,PIL; print('python', sys.version.split()[0], '| numpy', numpy.__version__, '| opencv', cv2.__version__, '| Pillow', PIL.__version__)"
  echo "# plate checksums (sha256, first 16)"
  for p in 001 006 010 015 018 020; do
    printf '%s  ' "plate-$p.jpg"; shasum -a 256 "$PLATES/plate-$p.jpg" | cut -c1-16
  done
  for s in measure_plate_vi measure_plate_i measure_plate_x measure_plate_xv measure_plate_xviii measure_plate_xx; do
    echo
    echo "## $s.py"
    python3 -I "$HERE/$s.py" 2>&1
    echo "(exit $?)"
  done
} | tee "$FILE"
echo
echo "written to $FILE"
