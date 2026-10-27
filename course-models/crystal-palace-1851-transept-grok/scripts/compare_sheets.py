"""Side-by-side compare sheets: reference (left) vs matched fixed-camera render (right).
python3 scripts/compare_sheets.py rNN"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
R = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
REF = os.path.join(ROOT, "..", "..", "references")
MD = os.path.join(REF, "muse-drive", "images")
PL = os.path.join(REF, "downes-1852", "source-scans", "plates")
pairs = [
    ("talbot", os.path.join(MD, "commons", "Great_Exhibition,_Transept_looking_south,_HF_Talbot,_1851.jpg"), "REF_talbot_start", "Talbot 1851, transept looking south"),
    ("absolon", os.path.join(MD, "commons", "John_Absolon,_The_Transept_from_the_South_Gallery,_The_Great_Exhibition_of_1851.jpg"), "REF_absolon_start", "Absolon, the transept from the south gallery"),
    ("elm_north", os.path.join(MD, "main-article", "Crystal_Palace_Great_Exhibition_tree_1851.png"), "REF_elm_north_start", "Empty transept and elm, looking north (1851)"),
    ("plate_IV", os.path.join(PL, "plate-004.jpg"), "PLATE_IV_south_ortho_start", "Downes Plate IV, south elevation (drawing is shortened)"),
    ("plate_VII", os.path.join(PL, "plate-007.jpg"), "PLATE_IV_south_ortho_start", "Downes Plate VII, transept end elevation/section"),
]
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except OSError:
    font = ImageFont.load_default()
os.makedirs(os.path.join(ROOT, "compare"), exist_ok=True)
H = 800
for key, ref, cam, title in pairs:
    rp = os.path.join(ROOT, "renders", R, cam + ".png")
    if not (os.path.exists(ref) and os.path.exists(rp)): print("skip", key); continue
    a = Image.open(ref).convert("RGB"); b = Image.open(rp).convert("RGB")
    a = a.resize((int(a.width * H / a.height), H)); b = b.resize((int(b.width * H / b.height), H))
    sheet = Image.new("RGB", (a.width + b.width + 30, H + 50), "white")
    sheet.paste(a, (10, 40)); sheet.paste(b, (a.width + 20, 40))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "REFERENCE: " + title, fill="black", font=font)
    d.text((a.width + 20, 8), f"GROK {R}: camera {cam}", fill="black", font=font)
    out = os.path.join(ROOT, "compare", f"{R}_{key}.jpg"); sheet.save(out, quality=88); print("wrote", out)
