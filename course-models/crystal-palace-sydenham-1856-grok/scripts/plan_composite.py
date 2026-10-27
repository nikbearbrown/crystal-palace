import sys
from PIL import Image
SRC='/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg'
raw, out = sys.argv[1], sys.argv[2]
plan = Image.open(SRC).convert('RGBA'); ov = Image.open(raw).convert('RGBA').resize(plan.size)
r,g,b,a = ov.split(); a = a.point(lambda v: int(v*0.8)); ov.putalpha(a)
comp = Image.alpha_composite(plan, ov).convert('RGB'); comp.thumbnail((5669, 5669)); comp.save(out, quality=90); print('saved', out)
