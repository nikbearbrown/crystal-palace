"""Make the reference-beside-render comparison images and the web JPEG copies for the course repo.

  python3 -I make_compare.py STAGE_DIR

Reads from STAGE_DIR/renders: section.png (lit), stairsec_flat.png (unlit), section_vs_plateVI.png and stairsec_vs_plateXV.png
(written by compare_plate_vi.py / compare_plate_xv.py: the plate crop on top, the flat render below, both at the render's
camera window), and the two *_overlay_*.png files. Writes STAGE_DIR/compare/*.jpg (+ web/ copies) and
STAGE_DIR/renders/web/*.jpg. The plate crops are the plates as registered by those scripts (scale bar and ground line);
nothing is redrawn.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
stage = Path(sys.argv[1])
R, C = stage / "renders", stage / "compare"
for d in (C, C / "web", R / "web"):
    d.mkdir(parents=True, exist_ok=True)


def font(size):
    for p in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def save_jpg(img, path, width=None, q=85):
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.convert("RGB").save(path, quality=q, optimize=True)


def side_by_side(ref, ren, left_cap, right_cap, out_name, box=None):
    """Reference on the left, render on the right, one caption bar above each."""
    if box:
        ref, ren = ref.crop(box), ren.crop(box)
    w, h = ref.size
    bar, gap = max(44, w // 40), 12
    f = font(bar - 16)
    sheet = Image.new("RGB", (2 * w + gap, h + bar), (250, 248, 242))
    sheet.paste(ref, (0, bar))
    sheet.paste(ren, (w + gap, bar))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), left_cap, fill=(30, 30, 30), font=f)
    d.text((w + gap + 10, 8), right_cap, fill=(30, 30, 30), font=f)
    save_jpg(sheet, C / out_name)
    save_jpg(sheet, C / "web" / out_name, width=1600)
    print("compare", out_name, sheet.size)


# Plate VI: transverse section on line A-B. Both images are 3000 x 800 at the same window; the left half of the width is
# shown side by side (the section is symmetric about the nave), the full width is shown in the overlay below.
sec_stack = Image.open(R / "section_vs_plateVI.png").convert("RGB")
W, H = 3000, 800
ref6 = sec_stack.crop((0, 0, W, H))
ren6 = Image.open(R / "section.png").convert("RGB")
assert ren6.size == (W, H), ren6.size
side_by_side(ref6, ren6, "Reference: Downes 1852, Plate VI, transverse section (left half)",
             "Render: this model, same window, lit (left half)", "section_left_half_vs_plateVI.jpg", box=(0, 0, 1500, 800))

# Plate XV: section through the staircases. Both images are 2800 x 1500 at the same window.
st_stack = Image.open(R / "stairsec_vs_plateXV.png").convert("RGB")
W2, H2 = 2800, 1500
ref15 = st_stack.crop((0, 0, W2, H2))
ren15 = Image.open(R / "stairsec_flat.png").convert("RGB")
assert ren15.size == (W2, H2), ren15.size
side_by_side(ref15, ren15, "Reference: Downes 1852, Plate XV, section through the staircases",
             "Render: this model, same window, unlit (white on black)", "stair_section_vs_plateXV.jpg")

# full-width Plate VI: the plate on top, the lit render below (the registration is the same as the overlay)
both = Image.new("RGB", (W, 2 * H + 20 + 2 * 60), (250, 248, 242))
d, f = ImageDraw.Draw(both), font(40)
d.text((10, 8), "Reference: Downes 1852, Plate VI, transverse section on line A-B (full width)", fill=(30, 30, 30), font=f)
both.paste(ref6, (0, 60))
d.text((10, H + 60 + 8), "Render: this model, the same window (orthographic, 440 ft across), lit", fill=(30, 30, 30), font=f)
both.paste(ren6, (0, H + 120))
save_jpg(both, C / "section_full_stacked_vs_plateVI.jpg")
save_jpg(both, C / "web" / "section_full_stacked_vs_plateVI.jpg", width=1600)

# overlays: the model's flat render in red over the plate (made by the project's scripts)
for src, dst, cap in (("section_overlay_plateVI.png", "section_overlay_plateVI.jpg",
                       "Overlay: this model (red) on Plate VI, full width. A consistency check, not independent evidence."),
                      ("stairsec_overlay_plateXV.png", "stair_section_overlay_plateXV.jpg",
                       "Overlay: this model (red) on Plate XV. A consistency check, not independent evidence.")):
    im = Image.open(R / src).convert("RGB")
    bar = 60 if im.width > 2900 else 52
    out = Image.new("RGB", (im.width, im.height + bar), (250, 248, 242))
    ImageDraw.Draw(out).text((10, 8), cap, fill=(30, 30, 30), font=font(bar - 20))
    out.paste(im, (0, bar))
    save_jpg(out, C / dst)
    save_jpg(out, C / "web" / dst, width=1600)
    print("overlay", dst, out.size)

# web copies of the lit renders (1400 px wide)
for p in sorted(R.glob("*.png")):
    if any(s in p.name for s in ("_overlay_", "_vs_plate")) or ("_flat" in p.name and p.stem != "stairsec_flat"):
        continue
    save_jpg(Image.open(p), R / "web" / (p.stem + ".jpg"), width=1400)
    print("web", p.stem)
