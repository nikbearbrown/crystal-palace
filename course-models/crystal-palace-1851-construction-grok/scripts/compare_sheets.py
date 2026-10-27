"""Side-by-side compare sheets: reference (left) vs matched fixed-camera render (right).
python3 scripts/compare_sheets.py cNN"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
R = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
REF = os.path.join(ROOT, "..", "..", "references")
MD = os.path.join(REF, "muse-drive", "images")
PL = os.path.join(REF, "downes-1852", "source-scans", "plates")
TH = os.path.join(REF, "muse-drive", "review", "thumbs")
pairs = [
    ("plate_VIII", os.path.join(PL, "plate-008.jpg"), "CP010_base_insert_start", "Downes Plate VIII, column base / base plates (D16)"),
    ("glazing_waggon", os.path.join(MD, "commons", "Glazing_waggon.png"), "CP016_trolley_start", "Glazing waggon on the Paxton gutters (Muse 0174)"),
    ("sheer_legs", os.path.join(TH, "0336.jpg"), "CP012_bay_start", "Scaffold poles / sheer legs raising ironwork (Muse 0336, thumb)"),
    ("staging", os.path.join(TH, "0337.jpg"), "CP013_platform_start", "Workers on a long staging (Muse 0337, thumb)"),
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
