#!/bin/bash
# detached final render of every m02 camera (1920x1080, 96 samples); log in /workspace/logs/move_render_m02.log
cd "$(dirname "$0")/.."
/workspace/blender5/blender -b rounds/m02.blend -P scripts/render_shots.py -- --out renders/m02 --samples 96 --pct 100 \
  && python3 /workspace/tmp/sheet.py renders/m02 renders/m02/contact_sheet_m02.jpg && echo RENDER_M02_DONE
