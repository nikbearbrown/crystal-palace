"""usage: python3 compare_sheet.py <render.png> <ref.jpg> <out.jpg> <title>"""
import sys
from PIL import Image, ImageDraw
r, ref, out, title = sys.argv[1:5]
A = Image.open(r).convert('RGB'); Bm = Image.open(ref).convert('RGB'); H = 900
A = A.resize((int(A.width*H/A.height), H)); Bm = Bm.resize((int(Bm.width*H/Bm.height), H))
S = Image.new('RGB', (A.width+Bm.width+20, H+50), 'white'); S.paste(Bm, (0, 50)); S.paste(A, (Bm.width+20, 50))
d = ImageDraw.Draw(S); d.text((10, 15), f'{title}   LEFT: period reference  {ref.split("/")[-1]}   RIGHT: model {r.split("/")[-1]}', fill='black')
S.save(out, quality=88); print('saved', out)
