"""Detect planting-bed blobs along the nave edges of plan 0205 -> JSON list of x_ft per side (R, registered 2.887 px/ft).
usage: python3 plan_nave_beds.py out.json"""
import sys, json, numpy as np
from PIL import Image
sys.path.insert(0, __file__.rsplit('/',1)[0]); from params import PLAN_PX_PER_FT as S, PLAN_X0, PLAN_Y0
im = np.asarray(Image.open('/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg').convert('L')).astype(float)
res = {}
for side, (y0, y1) in (('west', (565, 615)), ('garden', (815, 855))):
    band = (im[y0:y1, :] < 110).mean(axis=0)
    k = np.convolve(band, np.ones(9)/9, 'same'); on = k > 0.18
    runs = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            if j - i >= 25 and 480 < i < 5110: runs.append(((i+j)/2 - PLAN_X0)/S)
            i = j
        else: i += 1
    res[side] = [round(x, 1) for x in runs]
json.dump(res, open(sys.argv[1], 'w'), indent=1); print({k: len(v) for k, v in res.items()}, res)
