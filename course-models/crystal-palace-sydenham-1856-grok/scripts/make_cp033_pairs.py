"""CP033 slope CANDIDATE pairs: luma table for every camera of the round + matched-exposure pairs for the hero and every
camera whose image changed. Writes /workspace/crystal-palace-survey/look/pairs_geo/CANDIDATE_CP033_slope_* (before/after png,
side-by-side pair jpg) and renders/candidates/cp033_slope_20261116/luma.tsv.   usage: python3 scripts/make_cp033_pairs.py"""
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '..', 'renders', 'candidates', 'cp033_slope_20261116')
OUT = '/workspace/crystal-palace-survey/look/pairs_geo'; HERO = 'CAM_CP033_slope_up_35mm'
def luma(a): return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception: font = ImageFont.load_default()
rows = []
for f in sorted(os.listdir(os.path.join(R, 'after'))):
    cam = f[:-4]; bp = os.path.join(R, 'before', f); ap = os.path.join(R, 'after', f)
    if not os.path.exists(bp): continue
    b = np.asarray(Image.open(bp).convert('RGB')).astype(float); a = np.asarray(Image.open(ap).convert('RGB')).astype(float)
    d = np.abs(a - b); changed = (d.max(axis=2) > 8).mean() * 100
    rows.append((cam, luma(b), luma(a), d.max(), d.mean(), changed))
with open(os.path.join(R, 'luma.tsv'), 'w') as fh:
    fh.write('camera\tluma_before\tluma_after\tmax_diff\tmean_diff\tpct_pixels_changed_gt8\n')
    for r in rows: fh.write('%s\t%.2f\t%.2f\t%d\t%.3f\t%.2f\n' % r)
for r in rows: print('%-42s %7.2f -> %7.2f  max %3d mean %6.3f  changed %5.2f%%' % r)
def pair(cam, tag):
    b = Image.open(os.path.join(R, 'before', cam + '.png')).convert('RGB'); a = Image.open(os.path.join(R, 'after', cam + '.png')).convert('RGB')
    b.save(os.path.join(OUT, tag + '_before.png')); a.save(os.path.join(OUT, tag + '_after.png'))
    W, H = b.size; s = Image.new('RGB', (W * 2 + 12, H + 44), (20, 20, 20)); s.paste(b, (0, 44)); s.paste(a, (W + 12, 44))
    dr = ImageDraw.Draw(s); dr.text((10, 8), 'BEFORE live build53-r18b  ' + cam, fill=(230, 230, 230), font=font)
    dr.text((W + 22, 8), 'AFTER CANDIDATE cp033slope (not live)', fill=(255, 200, 120), font=font)
    s.save(os.path.join(OUT, tag + '_pair.jpg'), quality=92); return tag
made = []
for (cam, lb, la, mx, mn, ch) in rows:
    if cam == HERO: made.append(pair(cam, 'CANDIDATE_CP033_slope_up'))
    elif mx > 0: made.append(pair(cam, 'CANDIDATE_CP033_slope_sidefx_' + cam[4:]))
print('PAIRS', made)
