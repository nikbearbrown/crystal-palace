"""CP040 English Mediaeval Court CANDIDATE pairs: luma.tsv + side-by-side jpgs (before | after) in renders/candidates/cp040_mediaeval_20261118/pairs/.
usage: python3 scripts/make_cp040_mediaeval_pairs.py"""
import os, glob
import numpy as np
from PIL import Image, ImageDraw
D = 'renders/candidates/cp040_mediaeval_20261118'; os.makedirs(f'{D}/pairs', exist_ok=True)
W = np.array([0.2126, 0.7152, 0.0722])
rows = ['set\tcamera\tluma_before\tluma_after\tmax_diff\tpct_px_changed_gt8']
def pair(tag, b, a, out):
    A = np.asarray(Image.open(b).convert('RGB')).astype(float); B = np.asarray(Image.open(a).convert('RGB')).astype(float)
    d = np.abs(A - B); rows.append(f'{tag}\t{os.path.basename(b)[:-4]}\t{(A@W).mean():.2f}\t{(B@W).mean():.2f}\t{int(d.max())}\t{100*(d.max(2)>8).mean():.2f}')
    ia, ib = Image.open(b).convert('RGB'), Image.open(a).convert('RGB'); w, h = ia.size
    S = Image.new('RGB', (w * 2 + 8, h), (255, 255, 255)); S.paste(ia, (0, 0)); S.paste(ib, (w + 8, 0))
    dr = ImageDraw.Draw(S); dr.text((12, 10), 'BEFORE (live)', fill=(255, 0, 0)); dr.text((w + 20, 10), 'AFTER (CANDIDATE, no verdict)', fill=(255, 0, 0))
    S.save(out, quality=90)
for s in ('.', '1920x1080_48spp'):
    for b in sorted(glob.glob(f'{D}/{s}/before/*.png')):
        a = b.replace('/before/', '/after/')
        if os.path.exists(a): pair('live_1280x720_24spp' if s == '.' else s, b, a, f"{D}/pairs/CANDIDATE_CP040_mediaeval_hero_{'live_1280x720_24spp' if s == '.' else s}_pair.jpg")
for b in sorted(glob.glob(f'{D}/sidefx_before/*.png')):
    a = b.replace('sidefx_before', 'sidefx_after')
    if os.path.exists(a): pair('sidefx_1280x720_48spp_keeplight', b, a, f'{D}/pairs/CANDIDATE_CP040_mediaeval_sidefx_{os.path.basename(b)[4:-4]}_pair.jpg')
open(f'{D}/luma.tsv', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
