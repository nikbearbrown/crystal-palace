"""usage: python3 scripts/state_sheet.py <out.jpg> "<title>" <cols> "label=path" ...
Matched-camera state comparison sheet: identical camera objects rendered in each SY_STATE, labelled panels."""
import sys
from PIL import Image, ImageDraw, ImageFont
out, title, cols = sys.argv[1], sys.argv[2], int(sys.argv[3]); items = [a.split('=', 1) for a in sys.argv[4:]]
ims = [Image.open(p).convert('RGB') for _, p in items]; w, h = ims[0].size; LB = 50; TB = 60
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (w * cols, TB + rows * (h + LB)), (20, 20, 20)); d = ImageDraw.Draw(S)
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24); ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
d.text((14, 14), title, fill=(240, 240, 240), font=ft)
for i, ((lab, _), im) in enumerate(zip(items, ims)):
    x, y = (i % cols) * w, TB + (i // cols) * (h + LB)
    d.text((x + 12, y + 12), lab, fill=(235, 220, 170), font=fb); S.paste(im, (x, y + LB))
S.save(out, quality=90); print(out, S.size)
