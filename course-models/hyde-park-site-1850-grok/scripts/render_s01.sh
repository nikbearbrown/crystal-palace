#!/bin/bash
# detached final render of every s01 camera (1920x1080, 96 samples); log in /workspace/logs/site_render_s01.log
cd "$(dirname "$0")/.."
/workspace/blender5/blender -b rounds/s01.blend -P scripts/render_shots.py -- --out renders/s01 --samples 96 --pct 100 \
  && python3 /workspace/tmp/sheet.py renders/s01 renders/s01/contact_sheet_s01.jpg && echo RENDER_S01_DONE
