"""CP034b dinner CANDIDATE pairs (2026-11-13) -> survey look/pairs_geo/CANDIDATE_CP034b_* + checks/cp034b_dinner_pairs.json"""
from PIL import Image, ImageDraw, ImageStat, ImageChops
import json, os
D = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
R = f'{D}/renders/candidates/cp034b_dinner_20261113'; S = '/workspace/crystal-palace-survey/look/pairs_geo'
HERO = f'{D}/renders/r01/r01_CAM_CP034b_iguanodon_dinner_28mm.png'
out = {'date': '2026-11-13', 'recipe': 'scripts/render.py 100% 48 spp 1920x1080, before = rounds/dinosaurs-1854-r05.blend (live), after = rounds/dinosaurs-1854-r06-cand.blend'}
def luma(im): return round(ImageStat.Stat(im.convert('L')).mean[0], 2)
def pair(cam, tag, ref=None):
    b = Image.open(f'{R}/before/before_{cam}.png').convert('RGB'); a = Image.open(f'{R}/after/after_{cam}.png').convert('RGB')
    b.save(f'{S}/CANDIDATE_{tag}_before.png'); a.save(f'{S}/CANDIDATE_{tag}_after.png')
    W, H = 960, 540; tiles = [('BEFORE live r05', b), ('AFTER candidate r06 (CANDIDATE, no verdict)', a)]
    if ref: tiles.append(('ILN 7 Jan 1854 woodcut (PD)', ref))
    sh = Image.new('RGB', (W * len(tiles), H + 28), 'black'); d = ImageDraw.Draw(sh)
    for i, (lab, im) in enumerate(tiles):
        t = im.copy(); t.thumbnail((W, H)); sh.paste(t, (i * W + (W - t.width) // 2, 28 + (H - t.height) // 2)); d.text((i * W + 6, 8), lab, fill='yellow')
    sh.save(f'{S}/CANDIDATE_{tag}_pair.png')
    diff = ImageChops.difference(a, b).convert('L'); bb = diff.point(lambda v: 255 if v > 12 else 0).getbbox()
    frac = sum(1 for v in diff.getdata() if v > 12) / (a.width * a.height)
    out[tag] = {'before_luma': luma(b), 'after_luma': luma(a), 'changed_px_frac_gt12': round(frac, 4), 'changed_bbox': bb}
ref = Image.open(f'{D}/refs/ILN1854_dinner_in_the_iguanodon_PD.jpg').convert('RGB')
pair('CAM_CP034b_iguanodon_dinner_28mm', 'CP034b_iguanodon_dinner', ref)
pair('CAM_CP034_hawkins_studio_28mm', 'CP034b_sidefx_CP034_hawkins_studio')
h = Image.open(HERO).convert('RGB'); b = Image.open(f'{R}/before/before_CAM_CP034b_iguanodon_dinner_28mm.png').convert('RGB').resize(h.size)
out['before_vs_hero_r01_png'] = {'hero_size': h.size, 'hero_luma': luma(h), 'mean_abs_diff': round(ImageStat.Stat(ImageChops.difference(h, b).convert('L')).mean[0], 2)}
json.dump(out, open(f'{D}/checks/cp034b_dinner_pairs.json', 'w'), indent=1); print(json.dumps(out, indent=1))
