"""Detect free-standing dark marks (statues/fountain basins/pedestals) in the open nave strip and central transept
of plan 0205 -> checks/plan_nave_objects.json (model ft, R). usage: python3 plan_nave_objects.py out.json"""
import sys, json, numpy as np
from collections import deque
from PIL import Image
sys.path.insert(0, __file__.rsplit('/',1)[0]); from params import PLAN_PX_PER_FT as S, PLAN_X0, PLAN_Y0
im = np.asarray(Image.open('/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg').convert('L')).astype(float)
def px(x, y): return int(PLAN_X0 + x*S), int(PLAN_Y0 - y*S)
zones = [('nave', -790, 790, -21, 21), ('transept', -56, 56, -150, 150)]
seen = set(); out = []
for name, x0, x1, y0, y1 in zones:
    ax, ay = px(x0, y1); bx, by = px(x1, y0)
    sub = im[ay:by, ax:bx] < 100
    lab = np.zeros(sub.shape, bool)
    for (i, j) in zip(*np.nonzero(sub)):
        if lab[i, j]: continue
        q = deque([(i, j)]); lab[i, j] = True; pts = []
        while q:
            a, b = q.popleft(); pts.append((a, b))
            for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                c, d = a+da, b+db
                if 0 <= c < sub.shape[0] and 0 <= d < sub.shape[1] and sub[c, d] and not lab[c, d]:
                    lab[c, d] = True; q.append((c, d))
        P = np.array(pts); h = (P[:,0].max()-P[:,0].min()+1)/S; w = (P[:,1].max()-P[:,1].min()+1)/S
        if not (2.5 <= max(h, w) <= 16 and len(pts) > 12): continue   # skip text strokes/columns(<2.5 ft) and large beds
        cy = (P[:,0].mean()+ay); cx = (P[:,1].mean()+ax)
        x = round((cx-PLAN_X0)/S, 1); y = round(-(cy-PLAN_Y0)/S, 1)
        key = (round(x/4), round(y/4))
        if key in seen: continue
        seen.add(key); out.append({'zone': name, 'x': x, 'y': y, 'w': round(w,1), 'd': round(h,1), 'fill': round(len(pts)/(h*w*S*S),2)})
json.dump(out, open(sys.argv[1], 'w'), indent=0); print(len(out)); [print(o) for o in out]
