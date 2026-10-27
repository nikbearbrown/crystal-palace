#!/usr/bin/env python3
"""Draw the two faces of the 1851 Great Exhibition medal as heightmaps.

Relief is INTERPRETED from the two reference photographs (see ../refs/):
masses and lettering follow the photographs; the pictorial relief is an
impressionistic reading of them, not a tracing. Lettering text is the
exact transcription read off the photographs (verified at 2x zoom).

Canvas: 1024x1024, disc radius 500 px = 19.5 mm  -> 25.641 px/mm.
Image space: centre (512,512); +x right, image-up = medal-up.
Outputs: height_obverse.png, height_reverse.png (sharp, for bump) and
height_*_soft.png (slightly blurred, for mesh displacement sampling).
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 500.0 / 19.5            # px per mm
CX = CY = 512.0
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
COND = 0.80                 # die lettering is narrower than the font

def X(x_mm):  return CX + x_mm * S
def Y(z_mm):  return CY - z_mm * S   # z up -> image y down

def font(px):
    return ImageFont.truetype(SERIF, int(px))

def arc_text(img, s, r_mm, fpx, fill):
    """Draw s along the top arc, letters upright, tops pointing outward,
    centred on straight-up. Advances use condensed letter widths."""
    d = ImageDraw.Draw(img)
    f = font(fpx)
    widths = []
    for ch in s:
        b = d.textbbox((0, 0), ch, font=f)
        widths.append((b[2] - b[0]) * COND)
    r_px = r_mm * S
    total_ang = sum(widths) / r_px
    a = -total_ang / 2.0
    cap = fpx * 0.72
    for ch, w in zip(s, widths):
        a_mid = a + (w / r_px) / 2.0
        rr = r_px + cap / 2.0
        px = CX + rr * math.sin(a_mid)
        py = CY - rr * math.cos(a_mid)
        tile = Image.new("L", (int(fpx * 1.3) + 20, int(fpx) + 24), 0)
        td = ImageDraw.Draw(tile)
        td.text((10, 8), ch, font=f, fill=fill)
        tw = tile.size[0]
        tile = tile.resize((max(1, int(tw * COND)), tile.size[1]), Image.BICUBIC)
        rot = tile.rotate(-math.degrees(a_mid), expand=True, resample=Image.BICUBIC)
        img.paste(Image.new("L", rot.size, fill),
                  (int(px - rot.size[0] / 2), int(py - rot.size[1] / 2)), rot)
        a += w / r_px

def straight_line(img, s, z_mm, fpx, fill, max_w_mm=None):
    d = ImageDraw.Draw(img)
    f = font(fpx)
    if max_w_mm:
        while fpx > 10:
            b = d.textbbox((0, 0), s, font=f, anchor="ms")
            if (b[2] - b[0]) * COND <= max_w_mm * S:
                break
            fpx -= 1
            f = font(fpx)
    b = d.textbbox((0, 0), s, font=f, anchor="ms")
    w = int(b[2] - b[0]) + 8
    h = int(fpx * 1.6)
    by = int(fpx * 1.12)              # baseline row inside the tile
    tile = Image.new("L", (w, h), 0)
    td = ImageDraw.Draw(tile)
    td.text((w / 2, by), s, font=f, fill=fill, anchor="ms")
    tile = tile.resize((max(1, int(w * COND)), h), Image.BICUBIC)
    img.paste(Image.new("L", tile.size, fill),
              (int(CX - tile.size[0] / 2), int(Y(z_mm) - by)), tile)

# ---------------------------------------------------------------- obverse
def obverse():
    img = Image.new("L", (1024, 1024), 0)
    d = ImageDraw.Draw(img)
    V = 235

    # --- curved legend (nested arcs, clear radial gap)
    arc_text(img, "THE BUILDING AT LONDON, FOR THE", 15.30, 46, V)
    arc_text(img, "INTERNATIONAL EXHIBITION", 12.90, 50, V)
    straight_line(img, "1851", 9.85, 58, V)

    d = ImageDraw.Draw(img)
    # --- the building: tiers, light touch
    d.polygon([(X(-17.6), Y(-3.85)), (X(12.4), Y(-3.85)), (X(12.4), Y(4.55)),
               (X(-17.6), Y(3.35))], fill=140)
    # brighter clerestory (top) tier
    d.polygon([(X(-17.6), Y(1.55)), (X(12.4), Y(2.35)), (X(12.4), Y(4.55)),
               (X(-17.6), Y(3.35))], fill=154)
    # west-end front panel, slightly proud
    d.polygon([(X(-17.6), Y(-3.85)), (X(-16.2), Y(-3.85)), (X(-16.2), Y(3.42)),
               (X(-17.6), Y(3.35))], fill=150)
    # horizontal floor bands
    for z0, z1 in ((1.55, 2.35), (-0.75, -0.35), (-2.6, -2.25)):
        zz0 = z0 + (-17.6 + 17.6) * 0  # base heights at left
        d.line([(X(-17.6), Y(z0)), (X(12.4), Y(z1))], fill=90, width=3)
    # fine vertical glazing divisions (subtle)
    x = -16.1
    while x < 12.3:
        top = 3.35 + (x + 17.6) * (1.2 / 30.0)
        d.line([(X(x), Y(-3.85)), (X(x), Y(top))], fill=118, width=1)
        x += 0.85
    # roof line + small finial ticks
    d.line([(X(-17.6), Y(3.35)), (X(12.4), Y(4.55))], fill=200, width=3)
    x = -17.0
    while x < 12.2:
        top = 3.35 + (x + 17.6) * (1.2 / 30.0)
        d.line([(X(x), Y(top)), (X(x), Y(top + 0.42))], fill=200, width=2)
        x += 1.9
    # --- transept: barrel vault, same glazing language, slightly prouder
    pts = []
    for i in range(25):
        t = i / 24.0
        xx = 1.2 + t * 7.3
        zz = 4.5 + math.sin(t * math.pi) * 1.9
        pts.append((X(xx), Y(zz)))
    pts += [(X(8.5), Y(-3.85)), (X(1.2), Y(-3.85))]
    d.polygon(pts, fill=154)
    for z in (1.9, -0.55, -2.4):
        d.line([(X(1.2), Y(z)), (X(8.5), Y(z))], fill=104, width=3)
    for xx in (2.42, 3.64, 4.85, 6.06, 7.27):
        zz = 4.5 + math.sin(((xx - 1.2) / 7.3) * math.pi) * 1.9
        d.line([(X(xx), Y(-3.85)), (X(xx), Y(zz))], fill=112, width=2)
    d.line([(X(4.85), Y(6.4)), (X(4.85), Y(7.05))], fill=205, width=3)
    d.polygon([(X(4.85), Y(7.05)), (X(5.75), Y(6.8)), (X(4.85), Y(6.55))], fill=205)

    # --- ground strip: light, scattered crowd
    d.rectangle([X(-17.6), Y(-3.85), X(16.6), Y(-5.4)], fill=104)
    rnd = random.Random(1851)
    for _ in range(120):
        gx = rnd.uniform(-17.2, 16.2); gz = rnd.uniform(-5.3, -4.0)
        r = rnd.choice((1, 1, 2))
        d.ellipse([X(gx) - r, Y(gz) - r, X(gx) + r, Y(gz) + r], fill=rnd.randint(135, 175))
    for gx in (-11.0, -4.5, 3.0, 9.5):
        d.line([(X(gx), Y(-5.2)), (X(gx), Y(-4.45))], fill=165, width=3)
        d.ellipse([X(gx) - 2, Y(-4.35) - 2, X(gx) + 2, Y(-4.35) + 2], fill=170)

    # --- tree at right: dense, darker canopy overhanging the nave end
    d.polygon([(X(14.0), Y(-3.85)), (X(15.1), Y(-3.85)), (X(14.9), Y(1.2)),
               (X(14.3), Y(1.2))], fill=158)
    d.line([(X(14.55), Y(0.9)), (X(12.7), Y(2.6))], fill=146, width=5)
    d.line([(X(14.6), Y(1.1)), (X(16.8), Y(2.9))], fill=146, width=5)
    rnd2 = random.Random(42)
    for _ in range(30):
        cx = 15.3 + rnd2.uniform(-3.5, 3.5); cz = 3.4 + rnd2.uniform(-2.4, 2.4)
        rx = rnd2.uniform(0.7, 1.45); rz = rx * rnd2.uniform(0.65, 0.9)
        d.ellipse([X(cx - rx), Y(cz + rz), X(cx + rx), Y(cz - rz)],
                  fill=rnd2.randint(128, 178))
    for _ in range(70):
        cx = 15.3 + rnd2.uniform(-4.3, 4.3); cz = 3.4 + rnd2.uniform(-3.3, 3.3)
        d.ellipse([X(cx) - 2, Y(cz) - 2, X(cx) + 2, Y(cz) + 2], fill=92)

    # --- exergue band + signatures
    d.rectangle([X(-16.9), Y(-5.4), X(16.9), Y(-6.7)], fill=42)
    d.line([(X(-17.4), Y(-5.4)), (X(17.4), Y(-5.4))], fill=215, width=3)
    d.line([(X(-17.2), Y(-6.7)), (X(17.2), Y(-6.7))], fill=215, width=3)
    fsmall = font(17)
    d.text((X(-16.3), Y(-6.02)), "J. PAXTON ESQ. ARCHT.", font=fsmall, fill=190, anchor="ls")
    d.text((X(16.3), Y(-6.02)), "ALLEN & MOORE F.", font=fsmall, fill=190, anchor="rs")

    # --- crown above the medallion
    crown = [(-2.3, -9.5), (2.3, -9.5), (2.15, -7.75), (1.15, -8.7),
             (0.55, -7.3), (0.0, -8.65), (-0.55, -7.3), (-1.15, -8.7),
             (-2.15, -7.75)]
    d.polygon([(X(x), Y(z)) for x, z in crown], fill=205)
    for tx in (-2.15, 0.0, 2.15):
        d.ellipse([X(tx) - 3, Y(-7.5) - 3, X(tx) + 3, Y(-7.5) + 3], fill=215)

    # --- floral bouquet between left putto and crown
    rnd3 = random.Random(7)
    for _ in range(9):
        cx = -4.7 + rnd3.uniform(-0.85, 0.85); cz = -9.1 + rnd3.uniform(-0.6, 0.6)
        r = rnd3.uniform(0.28, 0.48)
        d.ellipse([X(cx - r), Y(cz + r), X(cx + r), Y(cz - r)], fill=rnd3.randint(150, 182))

    # --- central oval medallion with conjoined busts
    ocx, ocz, orx, orz = 0.0, -12.85, 2.55, 3.2
    d.ellipse([X(ocx - orx), Y(ocz + orz), X(ocx + orx), Y(ocz - orz)], fill=42)
    d.ellipse([X(ocx - orx), Y(ocz + orz), X(ocx + orx), Y(ocz - orz)], outline=218, width=6)
    d.ellipse([X(-1.5), Y(-11.1), X(0.1), Y(-13.2)], fill=100)   # rear bust mass
    prof = [(0.45, -10.95), (0.95, -11.3), (1.3, -12.0), (1.02, -12.4),
            (1.14, -12.68), (0.85, -13.0), (0.75, -13.55), (1.05, -14.5),
            (0.35, -14.6), (0.25, -13.7), (-0.2, -13.25), (-0.42, -12.2),
            (-0.2, -11.25)]
    d.polygon([(X(x), Y(z)) for x, z in prof], fill=140)
    d.ellipse([X(-0.55), Y(-10.75), X(0.3), Y(-11.6)], fill=146)  # back hair/bun

    # --- putti drawn on their own layer, blurred and max-composited back
    #     so the figure masses read as rounded relief, not cut paper.
    #     Base outline for the LEFT putto, absolute mm, read off the
    #     photograph: wing tip up-left, head, torso, arm reaching to the
    #     medallion, two trailing legs, scalloped wing trailing edge.
    fig = Image.new("L", (1024, 1024), 0)
    fd = ImageDraw.Draw(fig)
    LEFT = [(-14.9, -8.3), (-12.4, -9.3), (-10.1, -9.9), (-9.6, -10.6),
            (-7.5, -10.4), (-7.15, -11.6), (-7.3, -12.6), (-4.6, -13.15),
            (-4.8, -13.9), (-7.5, -13.6), (-7.7, -14.4), (-6.1, -16.25),
            (-7.0, -16.6), (-8.6, -15.3), (-10.3, -15.9), (-11.5, -16.3),
            (-11.0, -14.6), (-11.2, -13.7), (-12.8, -13.1), (-12.1, -11.8),
            (-13.6, -11.1), (-13.2, -9.9)]
    def putto(pts, m, dx):
        poly = [(dx + m * x, z) for x, z in pts]
        fd.polygon([(X(x), Y(z)) for x, z in poly], fill=168)
    putto(LEFT, +1, 0.0)          # left putto as drawn
    putto(LEFT, -1, -1.2)         # right: mirrored, recentred on x=+8.1

    for (hx, hz, m) in ((-8.55, -9.35, -1), (7.35, -9.35, 1)):
        # head: bright disc; hair: darker cap behind/above
        fd.ellipse([X(hx - 1.32), Y(hz + 1.32), X(hx + 1.32), Y(hz - 1.32)], fill=150)
        fd.ellipse([X(hx - 1.14), Y(hz + 1.05), X(hx + 1.14), Y(hz - 1.23)], fill=192)
        # wing feather separations
        sx, sz = hx + m * 1.6, hz - 1.3
        fd.line([(X(sx), Y(sz)), (X(sx + m * 3.4), Y(sz + 2.2))], fill=124, width=2)
        fd.line([(X(sx + m * 0.2), Y(sz - 1.1)), (X(sx + m * 3.2), Y(sz + 0.5))], fill=124, width=2)
        # drape fold across the hips
        fd.line([(X(hx - m * 1.1), Y(hz - 4.3)), (X(hx + m * 1.5), Y(hz - 5.2))], fill=122, width=3)

    # left putto's palm frond: a fan of leaves from the lower-left hand
    for ang, ln in ((-160, 3.6), (-138, 4.4), (-115, 4.6), (-92, 4.2), (-70, 3.4)):
        a = math.radians(ang)
        x0, z0 = -11.2, -13.5
        fd.line([(X(x0), Y(z0)), (X(x0 + ln * math.cos(a)), Y(z0 + ln * math.sin(a)))],
                fill=164, width=3)
    # right putto's caduceus: staff against the outer arm, small winged top
    fd.line([(X(8.9), Y(-10.8)), (X(11.7), Y(-10.4))], fill=172, width=7)
    fd.line([(X(11.8), Y(-8.2)), (X(11.8), Y(-14.1))], fill=182, width=4)
    fd.polygon([(X(11.8), Y(-8.25)), (X(11.05), Y(-7.8)), (X(11.75), Y(-8.9))], fill=182)
    fd.polygon([(X(11.8), Y(-8.25)), (X(12.55), Y(-7.8)), (X(11.85), Y(-8.9))], fill=182)
    fd.arc([X(11.2), Y(-9.4), X(12.4), Y(-10.7)], 90, 300, fill=140, width=2)

    from PIL import ImageChops
    fig = fig.filter(ImageFilter.GaussianBlur(2.1))
    img = ImageChops.lighter(img, fig)
    return img

# ---------------------------------------------------------------- reverse
def reverse():
    img = Image.new("L", (1024, 1024), 0)
    V = 238
    arc_text(img, "THE MATERIALS ARE", 15.35, 50, V)
    arc_text(img, "IRON AND GLASS,", 13.15, 56, V)
    lines = [
        "IN SHAPE",
        "A PARALLELOGRAM,",
        "1848 FT LONG BY 408 FT BROAD,",
        "AND 66 FT HIGH;",
        "IT IS CROSSED MIDWAY BY",
        "A TRANSEPT 108 FT HIGH,",
        "ON THE NORTH SIDE IS AN",
        "ADDITIONAL 936 FT IN LENGTH",
        "BY 48 FT IN BREADTH;",
        "TOTAL AREA OF SPACE",
        "855,560 CUBIC FT;",
        "OR NEARLY 21 ACRES;",
        "ESTIMATED VALUE",
        "\u00a3150,000.",
    ]
    z0, pitch = 7.35, 1.665
    for i, s in enumerate(lines):
        z = z0 - i * pitch
        half_chord = math.sqrt(max(16.6 ** 2 - z ** 2, 25.0))
        straight_line(img, s, z, 47, V, max_w_mm=2 * half_chord * 0.985)
    return img

def masked(a, r_mm, r0, r1):
    import numpy as np
    m = np.clip((r1 - r_mm) / (r1 - r0), 0.0, 1.0)
    m = m * m * (3 - 2 * m)
    return (a * m).astype(np.uint8)

if __name__ == "__main__":
    import os
    import numpy as np
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work")
    os.makedirs(out, exist_ok=True)
    yy, xx = np.mgrid[0:1024, 0:1024]
    r_mm = np.hypot(xx - CX, yy - CY) / S
    for name, fn in (("obverse", obverse), ("reverse", reverse)):
        a = np.asarray(fn()).astype(np.float32)
        # sharp (bump) copy: gentle fade only very close to the rim;
        # soft (displacement) copy: stronger fade + blur
        Image.fromarray(masked(a, r_mm, 17.55, 18.55)).save(
            os.path.join(out, f"height_{name}.png"))
        soft = Image.fromarray(masked(a, r_mm, 16.95, 18.1))
        soft.filter(ImageFilter.GaussianBlur(1.1)).save(
            os.path.join(out, f"height_{name}_soft.png"))
        print(name, "saved")
