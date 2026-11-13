#!/bin/bash
set -u
B=/workspace/blender5/blender; D=/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok; T=/workspace/tmp/cp034bkeep
CAM=CAM_CP034b_iguanodon_dinner_28mm
cd $D
[ -f $T/ALL_DONE ] && { echo already done; exit 0; }
[ -f $T/md5_before.txt ] || md5sum rounds/dinosaurs-1854-r05.blend rounds/dinosaurs-1854-r02.blend rounds/dinosaurs-1854-r01.blend renders/r01/*.png renders/r02/*.png renders/r05_cand/*.png renders/r05b_cand/*.png > $T/md5_before.txt
[ -f rounds/dinosaurs-1854-r06.blend ] || cp -p rounds/dinosaurs-1854-r06-cand.blend rounds/dinosaurs-1854-r06.blend
m=$(md5sum < rounds/dinosaurs-1854-r06.blend | cut -c1-32); [ $m = 2707897bac47a2349517394dbf5e038f ] || { echo BAD_MD5 $m; exit 1; }
echo "- $(date -u +%H:%M) r06.blend ok $m" >> $T/PROGRESS.md
if [ ! -f renders/r06/r06_$CAM.png ]; then
  $B -b rounds/dinosaurs-1854-r06.blend -P scripts/render.py -- renders/r06.tmp r06 100 48 $CAM && mkdir -p renders/r06 && mv renders/r06.tmp/r06_$CAM.png renders/r06/ && rmdir renders/r06.tmp || exit 1
  echo "- $(date -u +%H:%M) live PNG rendered" >> $T/PROGRESS.md
fi
if [ ! -f $T/r06_rebuild.blend ]; then
  sed -e "s#^OUT = .*#OUT = '$T/r06_rebuild.blend'#" scripts/cand_cp034b_dinner_20261113.py > $T/rebuild_script.py
  diff scripts/cand_cp034b_dinner_20261113.py $T/rebuild_script.py > $T/rebuild_script.diff
  $B -b -P $T/rebuild_script.py || exit 1
  echo "- $(date -u +%H:%M) rebuild blend done" >> $T/PROGRESS.md
fi
if [ ! -f $T/rebuild/rebuild_$CAM.png ]; then
  $B -b $T/r06_rebuild.blend -P scripts/render.py -- $T/rebuild rebuild 100 48 $CAM || exit 1
  echo "- $(date -u +%H:%M) rebuild PNG rendered" >> $T/PROGRESS.md
fi
{ python3 $T/cmp.py renders/r06/r06_$CAM.png $T/rebuild/rebuild_$CAM.png
  python3 $T/cmp.py renders/r06/r06_$CAM.png renders/candidates/cp034b_dinner_20261113/after/after_$CAM.png; } > $T/compare.txt
cat $T/compare.txt
md5sum rounds/dinosaurs-1854-r05.blend rounds/dinosaurs-1854-r02.blend rounds/dinosaurs-1854-r01.blend renders/r01/*.png renders/r02/*.png renders/r05_cand/*.png renders/r05b_cand/*.png > $T/md5_after.txt
diff $T/md5_before.txt $T/md5_after.txt && echo MD5_UNCHANGED > $T/md5_cmp.txt || echo MD5_CHANGED > $T/md5_cmp.txt
md5sum rounds/dinosaurs-1854-r06.blend rounds/dinosaurs-1854-r06-cand.blend renders/r06/*.png $T/r06_rebuild.blend > $T/md5_r06.txt
echo "- $(date -u +%H:%M) compare + md5 done: $(cat $T/md5_cmp.txt)" >> $T/PROGRESS.md
date -u > $T/ALL_DONE; echo ALL_DONE
