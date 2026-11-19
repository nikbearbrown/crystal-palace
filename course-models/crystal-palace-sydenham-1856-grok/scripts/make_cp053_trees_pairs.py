"""CP053 lower-park trees in leaf (summer 1911) CANDIDATE pairs: luma.tsv + side-by-side jpgs (before | after) in renders/candidates/cp053_trees_20261119/pairs/.
usage: python3 scripts/make_cp053_trees_pairs.py"""
import os, glob
import numpy as np
from PIL import Image, ImageDraw
D = 'renders/candidates/cp053_trees_20261119'; os.makedirs(f'{D}/pairs', exist_ok=True)
W = np.array([0.2126, 0.7152, 0.0722])
rows = ['set\tcamera\tluma_before\tluma_after\tmax_diff\tpct_px_changed_gt8']
def pair(tag, b, a, out):
    A = np.asarray(Image.open(b).convert('RGB')).astype(float); B = np.asarray(Image.open(a).convert('RGB')).astype(float)
    d = np.abs(A - B); rows.append(f'{tag}\t{os.path.basename(b)[:-4]}\t{(A@W).mean():.2f}\t{(B@W).mean():.2f}\t{int(d.max())}\t{100*(d.max(2)>8).mean():.2f}')
    if out is None: return
    ia, ib = Image.open(b).convert('RGB'), Image.open(a).convert('RGB'); w, h = ia.size
    S = Image.new('RGB', (w * 2 + 8, h), (255, 255, 255)); S.paste(ia, (0, 0)); S.paste(ib, (w + 8, 0))
    dr = ImageDraw.Draw(S); dr.text((12, 10), 'BEFORE (live)', fill=(255, 0, 0)); dr.text((w + 20, 10), 'AFTER (CANDIDATE, no verdict)', fill=(255, 0, 0))
    S.save(out, quality=90)
for b in sorted(glob.glob(f'{D}/before/*.png')):
    a = b.replace('/before/', '/after/')
    if os.path.exists(a): pair('live_1280x720_24spp_lookv1.1', b, a, f'{D}/pairs/CANDIDATE_CP053_trees_hero_live_1280x720_24spp_pair.jpg')
    r = b.replace('/before/', '/rebuild/')
    if os.path.exists(r) and os.path.exists(a): pair('rebuild_vs_after', a, r, None)
live = 'renders/r14_late11_CAM_CP053_empire_pavilions_wide_35mm.png'
for b in sorted(glob.glob(f'{D}/before/*.png')): pair('live_hero_vs_before', live, b, None)
for b in sorted(glob.glob(f'{D}/sidefx_before/*.png')):
    a = b.replace('sidefx_before', 'sidefx_after')
    if os.path.exists(a): pair('sidefx_1280x720_48spp_keeplight', b, a, f'{D}/pairs/CANDIDATE_CP053_trees_sidefx_{os.path.basename(b)[4:-4]}_pair.jpg')
open(f'{D}/luma.tsv', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
