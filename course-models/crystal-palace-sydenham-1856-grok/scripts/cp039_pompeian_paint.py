"""CP039 CANDIDATE (2026-11-17): procedural Fourth-Style wall paintings, ambulatory ceiling and mosaic floor textures
for the Pompeian Court peristyle (Digby Wyatt / Abbate, opened 10 Jun 1854). System python + Pillow, deterministic
(fixed seeds) -> refs/cp039_pompeian_paint/*.png, packed into the candidate blend by scripts/candidate_cp039_pompeian.py.

Source: G. Scharf, 'The Pompeian Court in the Crystal Palace' (1854 handbook, Crystal Palace Library; archive.org
pompeiancourtinc00scha), 'Description of the Pompeian House' Nos. 18-26 (peristyle):
  18 ambulatory: 'roof ... panelled and decorated according to the prevailing style of the lighter coloured ceilings
     at Pompeii. The devices are formed of very thin lines of the brightest colours upon white' -> ceiling tile (R type,
     pattern I); 'the wall behind [the lararium] is a rich Pompeian red, with a yellow ornament, forming a panel' (R).
  23 end wall of the peristyle: 'The general colour is white. Dado red and yellow. The three central compartments ...
     beneath a high canopy, supported by thin and gracefully ornamented columns, stands a lovely female ... playing the
     lyre ... Upon the architrave of this porch is a yellow group of a Winged Victory in a biga ... The left-hand figure
     is a priestess ... lower dress is blue ... the companion picture ... a young man in purple drapery ... offer a green
     wreath ... In the dado ... large square stalls or recesses. In the centre one ... a girl holding a lyre' (R content;
     drawing I - simplified painted figures, not copies of the Abbate tracings).
  general rule p.31-32: 'if the dado be black, the rest will be red or yellow, and the ceiling white' (west wall I).
  atrium: 'The floor is an excellent imitation of ancient mosaic work, executed by Messrs. Minton' (atrium R; the
     ambulatory floor pattern here I).
Pixel scale 40 px/ft; walls run from z 0 ft (bottom of image) to 19.4 ft (under the 20 ft cornice).
usage: python3 scripts/cp039_pompeian_paint.py   (writes the PNGs + md5 list)
"""
import os, math, random, hashlib
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'refs', 'cp039_pompeian_paint')
PPF = 40
H = 19.4
C = dict(red=(168, 38, 26), red_d=(120, 22, 16), yel=(214, 158, 48), yel_d=(170, 112, 28), blk=(28, 24, 22),
         wht=(232, 222, 200), wht2=(240, 232, 214), blue=(46, 96, 166), blue_l=(110, 160, 205), purple=(98, 36, 66),
         grn=(58, 112, 72), grn_l=(120, 160, 96), skin=(214, 168, 128), hair=(60, 36, 24), cin=(150, 30, 34),
         gold=(196, 150, 60), sea=(70, 140, 130), pink=(214, 140, 140), brown=(110, 70, 40))

class Wall:
    def __init__(s, w_ft, h_ft=H, ground='wht', seed=0):
        s.w, s.h = w_ft, h_ft; s.im = Image.new('RGB', (int(round(w_ft * PPF)), int(round(h_ft * PPF))), C.get(ground, ground))
        s.d = ImageDraw.Draw(s.im); s.r = random.Random(seed)
    def X(s, u): return int(round(u * PPF))
    def Y(s, z): return int(round((s.h - z) * PPF))
    def rect(s, u0, u1, z0, z1, col):
        s.d.rectangle([s.X(min(u0, u1)), s.Y(max(z0, z1)), s.X(max(u0, u1)) - 1, s.Y(min(z0, z1)) - 1], fill=C.get(col, col))
    def frame(s, u0, u1, z0, z1, col, w=0.08):
        s.rect(u0, u1, z1 - w, z1, col); s.rect(u0, u1, z0, z0 + w, col); s.rect(u0, u0 + w, z0, z1, col); s.rect(u1 - w, u1, z0, z1, col)
    def line(s, u0, z0, u1, z1, col, w=0.05):
        s.d.line([(s.X(u0), s.Y(z0)), (s.X(u1), s.Y(z1))], fill=C.get(col, col), width=max(1, int(w * PPF)))
    def poly(s, pts, col):
        s.d.polygon([(s.X(u), s.Y(z)) for u, z in pts], fill=C.get(col, col))
    def ell(s, u, z, ru, rz, col):
        s.d.ellipse([s.X(u - ru), s.Y(z + rz), s.X(u + ru), s.Y(z - rz)], fill=C.get(col, col))
    # ------------------------------------------------------------ motifs
    def candelabrum(s, u, z0, z1, col='yel', w=0.06):
        s.line(u, z0, u, z1, col, w)
        n = int((z1 - z0) / 1.6)
        for i in range(1, n + 1):
            z = z0 + i * (z1 - z0) / (n + 1); r = 0.35 if i % 2 else 0.22
            s.ell(u, z, r, 0.06, col); s.line(u - r, z, u - r * 0.6, z - 0.25, col, 0.03); s.line(u + r, z, u + r * 0.6, z - 0.25, col, 0.03)
        s.ell(u, z1, 0.25, 0.12, col)
    def garland(s, u0, u1, z, sag=0.45, col='grn'):
        pts = [(u0 + (u1 - u0) * t / 16, z - sag * math.sin(math.pi * t / 16)) for t in range(17)]
        for (a, b), (c, d) in zip(pts, pts[1:]): s.line(a, b, c, d, col, 0.12)
        for a, b in pts[::3]: s.ell(a, b, 0.07, 0.07, 'red')
    def figure(s, u, z, ht, drape='blue', mantle=None, attr=None, face=1, float_=False):
        """stylised painted figure, feet at z, height ht (ft)"""
        hr = ht * 0.065; hz = z + ht - hr
        sw = ht * 0.13
        if float_:
            s.poly([(u - sw * 1.6, z + ht * 0.25), (u + sw * 1.4, z + ht * 0.1), (u + sw * 0.5, z + ht * 0.78), (u - sw * 0.5, z + ht * 0.8)], drape)
        else:
            s.poly([(u - sw * 1.15, z), (u + sw * 1.15, z), (u + sw * 0.6, z + ht * 0.62), (u + sw * 0.55, z + ht * 0.8),
                    (u - sw * 0.55, z + ht * 0.8), (u - sw * 0.6, z + ht * 0.62)], drape)
            for k in (-0.5, 0.0, 0.5):     # folds
                s.line(u + k * sw * 0.8, z + ht * 0.05, u + k * sw * 0.4, z + ht * 0.6, tuple(int(c * 0.7) for c in C[drape]), 0.03)
        if mantle:
            s.poly([(u - sw * 0.7, z + ht * 0.8), (u + sw * 0.75, z + ht * 0.78), (u + sw * 1.0 * face, z + ht * 0.35), (u - sw * 0.2, z + ht * 0.45)], mantle)
        s.ell(u, z + ht * 0.82, sw * 0.32, ht * 0.03, 'skin')                       # neck
        s.ell(u, hz, hr * 0.85, hr, 'skin'); s.ell(u - face * hr * 0.15, hz + hr * 0.35, hr * 0.9, hr * 0.6, 'hair')
        s.line(u + face * sw * 0.5, z + ht * 0.76, u + face * sw * 1.5, z + ht * 0.6, 'skin', ht * 0.02)   # arm
        if attr == 'lyre':
            a = u + face * sw * 1.6; b = z + ht * 0.55
            s.line(a - 0.2, b, a - 0.25, b + 0.6, 'gold', 0.05); s.line(a + 0.2, b, a + 0.25, b + 0.6, 'gold', 0.05); s.line(a - 0.25, b + 0.55, a + 0.25, b + 0.55, 'gold', 0.04)
            s.ell(a, b, 0.25, 0.1, 'gold')
        elif attr == 'wreath':
            a = u + face * sw * 1.7; b = z + ht * 0.62; s.d.ellipse([s.X(a - 0.22), s.Y(b + 0.22), s.X(a + 0.22), s.Y(b - 0.22)], outline=C['grn'], width=5)
        elif attr == 'pitcher':
            a = u + face * sw * 1.6; b = z + ht * 0.5; s.ell(a, b, 0.13, 0.18, 'gold')
    def vista(s, u0, u1, z0, z1, ground='wht2'):
        """painted architectural perspective (thin columns, coffered canopy) - Fourth Style 'architectural ranges'"""
        s.rect(u0, u1, z0, z1, ground); cu = (u0 + u1) / 2; vz = z0 + (z1 - z0) * 0.45
        for k in range(3):
            f = 0.15 + k * 0.17; a = u0 + (u1 - u0) * f; b = u1 - (u1 - u0) * f; zt = z1 - (z1 - z0) * (0.1 + k * 0.08)
            for uu in (a, b): s.line(uu, z0 + (z1 - z0) * 0.08 * k, uu, zt, 'yel_d', 0.07)
            s.line(a, zt, b, zt, 'red', 0.06)
            s.line(a, zt, cu, vz + (z1 - z0) * 0.3, 'blue', 0.03); s.line(b, zt, cu, vz + (z1 - z0) * 0.3, 'blue', 0.03)
    def dado(s, u0, u1, z0, z1, main='red', alt='yel', recess_at=()):
        n = max(1, int(round((u1 - u0) / 4.2))); w = (u1 - u0) / n
        for i in range(n):
            a = u0 + i * w; s.rect(a, a + w, z0, z1, main if i % 2 == 0 else alt)
            s.frame(a + 0.25, a + w - 0.25, z0 + 0.3, z1 - 0.3, 'blk' if main != 'blk' else 'yel', 0.05)
            # plant spray
            m = a + w / 2; s.line(m, z0 + 0.35, m, z0 + 1.6, 'grn', 0.05)
            for k in range(4): s.line(m, z0 + 0.5 + k * 0.3, m + (0.5 if k % 2 else -0.5), z0 + 0.8 + k * 0.3, 'grn', 0.04)
        s.rect(u0, u1, z1 - 0.12, z1, 'blk'); s.rect(u0, u1, z0, z0 + 0.25, 'blk')
    def frieze(s, u0, u1, z0, z1, ground='purple', motif='yel'):
        s.rect(u0, u1, z0, z1, ground); s.rect(u0, u1, z0, z0 + 0.12, 'blk'); s.rect(u0, u1, z1 - 0.15, z1, 'wht')
        k = 0; u = u0 + 0.8
        while u < u1 - 0.8:
            if k % 3 == 2: s.garland(u - 0.9, u + 0.9, z1 - 0.5, 0.35, 'grn_l')
            else:
                s.poly([(u - 0.45, z0 + 0.3), (u + 0.45, z0 + 0.3), (u + 0.2, z1 - 0.4), (u - 0.2, z1 - 0.4)], motif)  # siren/griffin silhouettes (I)
                s.ell(u, z1 - 0.4, 0.15, 0.15, motif)
            u += 1.8; k += 1
    def upper(s, u0, u1, z0, z1):
        """white upper zone with thin-line painted aediculae"""
        s.rect(u0, u1, z0, z1, 'wht2')
        n = max(1, int((u1 - u0) / 5.0)); w = (u1 - u0) / n
        for i in range(n):
            a = u0 + i * w + 0.6; b = a + w - 1.2; zt = z1 - 0.6
            for uu in (a, b): s.line(uu, z0 + 0.3, uu, zt, 'yel_d', 0.04)
            s.line(a - 0.2, zt, b + 0.2, zt, 'red', 0.05); s.line(a, zt, (a + b) / 2, zt + 0.45, 'red', 0.03); s.line(b, zt, (a + b) / 2, zt + 0.45, 'red', 0.03)
            s.garland(a, b, zt - 0.3, 0.3, 'grn_l')
    def age(s, amt=10, seed=0):
        a = np.asarray(s.im).astype(np.float32); rng = np.random.default_rng(seed)
        n = rng.normal(0, 1, a.shape[:2])
        big = np.asarray(Image.fromarray(((rng.normal(0, 1, (a.shape[0] // 40 + 1, a.shape[1] // 40 + 1)) * 40 + 128).clip(0, 255)).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.BILINEAR)).astype(np.float32) - 128
        a += (n * amt * 0.35 + big * amt / 90.0)[..., None]
        s.im = Image.fromarray(a.clip(0, 255).astype(np.uint8)); s.d = ImageDraw.Draw(s.im)

def red_panel_scheme(W, u0, u1, main='red', pics=True, seed=0):
    """Fourth Style tripartite: black dado / red(or yellow) main panels with black strips + candelabra / frieze / upper"""
    r = random.Random(seed)
    W.dado(u0, u1, 0.0, 3.2, 'blk', 'blk')
    W.rect(u0, u1, 3.2, 13.0, main)
    n = max(1, int(round((u1 - u0) / 7.5))); w = (u1 - u0) / n
    for i in range(n + 1):
        uc = u0 + i * w; sw = min(0.9, w * 0.11)
        W.rect(max(u0, uc - sw), min(u1, uc + sw), 3.2, 13.0, 'blk')
        if u0 < uc < u1: W.candelabrum(uc, 3.6, 12.4, 'yel', 0.05)
    for i in range(n):
        a = u0 + i * w + 1.3; b = u0 + (i + 1) * w - 1.3
        W.frame(a, b, 3.9, 12.3, 'yel', 0.1); W.frame(a + 0.25, b - 0.25, 4.15, 12.05, 'wht', 0.025)
        m = (a + b) / 2
        if pics and i % 2 == 1:
            W.rect(m - 1.4, m + 1.4, 6.6, 9.8, 'wht2'); W.frame(m - 1.4, m + 1.4, 6.6, 9.8, 'yel_d', 0.08)
            W.rect(m - 1.3, m + 1.3, 6.7, 8.2, 'grn_l'); W.rect(m - 1.3, m + 1.3, 8.2, 9.7, 'blue_l')        # landscape vignette
            W.poly([(m - 0.9, 8.2), (m - 0.2, 8.2), (m - 0.55, 9.1)], 'brown'); W.rect(m + 0.3, m + 0.9, 8.2, 8.9, 'wht')
        else:
            W.figure(m, 7.0, 2.6, r.choice(['blue', 'grn', 'purple', 'yel']), 'wht', None, 1 if i % 2 else -1, float_=True)
    W.frieze(u0, u1, 13.0, 15.6, 'purple', 'yel')
    W.upper(u0, u1, 15.6, H)

def end_wall():
    """No. 23: the end wall of the peristyle (PY1 face, x -561.4 .. -494.6, seen from the peristyle; image left = x -561.4)"""
    w = 66.8; W = Wall(w, seed=23); xc = 33.4
    W.dado(0, w, 0.0, 3.2, 'red', 'yel')                                   # 'Dado red and yellow'
    for k, u in enumerate((xc - 5.6, xc, xc + 5.6)):                       # 'large square stalls or recesses'
        W.rect(u - 1.25, u + 1.25, 0.5, 2.9, 'blk'); W.frame(u - 1.25, u + 1.25, 0.5, 2.9, 'yel', 0.08)
        if k == 1: W.figure(u, 0.9, 1.7, 'pink', 'wht', 'lyre', 1)          # girl holding a lyre
    W.rect(0, w, 3.2, 13.0, 'wht')                                         # 'The general colour is white'
    # side zones: white panels, thin red/yellow borders, floating figures, thin candelabra
    for side in (-1, 1):
        for j in range(3):
            a = xc + side * (9.2 + j * 7.6); b = a + side * 6.4
            u0, u1 = min(a, b), max(a, b)
            if u1 > w - 0.3 or u0 < 0.3: continue
            W.frame(u0, u1, 3.8, 12.4, 'red', 0.12); W.frame(u0 + 0.25, u1 - 0.25, 4.05, 12.15, 'yel', 0.04)
            W.figure((u0 + u1) / 2, 7.0, 2.4, ['grn', 'blue', 'purple'][j], 'yel', None, -side, float_=True)
            W.candelabrum(u1 + 0.6 if side > 0 else u0 - 0.6, 3.6, 12.6, 'red', 0.05)
    # the lararium wall (No. 18): rich Pompeian red panel with yellow ornament, far (west) end at u 6..14 (I)
    W.rect(5.0, 15.0, 3.2, 13.0, 'red'); W.frame(5.6, 14.4, 3.8, 12.4, 'yel', 0.14); W.frame(6.1, 13.9, 4.3, 11.9, 'yel', 0.04)
    for k in range(5): W.ell(10.0, 5.0 + k * 1.6, 0.5, 0.18, 'yel_d')
    # the three central compartments (Nos. 23): canopy + lyre-player, priestess left, youth right
    W.rect(xc - 8.8, xc + 8.8, 3.2, 13.0, 'wht2')
    W.vista(xc - 2.6, xc + 2.6, 3.4, 12.6, 'blue_l')
    for uu in (xc - 2.3, xc + 2.3):                                        # thin ornamented columns
        W.rect(uu - 0.09, uu + 0.09, 3.4, 11.6, 'gold')
        for k in range(8): W.ell(uu, 4.0 + k * 1.0, 0.16, 0.05, 'red')
    W.poly([(xc - 2.8, 11.6), (xc + 2.8, 11.6), (xc, 12.9)], 'yel'); W.rect(xc - 2.8, xc + 2.8, 11.3, 11.7, 'red_d')   # high canopy
    W.poly([(xc - 1.3, 11.75), (xc + 0.2, 11.75), (xc + 1.0, 12.2), (xc - 0.6, 12.25)], 'yel_d')                       # Victory in a biga (yellow)
    W.rect(xc - 1.1, xc + 1.1, 3.4, 3.8, 'wht')                                                                          # door step
    W.figure(xc, 3.8, 5.6, 'wht', 'cin', 'lyre', 1)                                                                     # the lyrist
    for side, (drape, mant, attr) in ((-1, ('blue', 'yel', 'pitcher')), (1, ('purple', None, 'wreath'))):
        a = xc + side * 5.6
        W.rect(a - 2.4, a + 2.4, 3.6, 12.2, 'red'); W.frame(a - 2.4, a + 2.4, 3.6, 12.2, 'yel', 0.12)
        W.vista(a - 1.9, a + 1.9, 8.8, 11.9, 'wht2')
        W.figure(a, 4.2, 4.6, drape, mant, attr, -side)
    W.frieze(0, w, 13.0, 15.6, 'purple', 'yel'); W.upper(0, w, 15.6, H)
    W.age(9, 23); return W.im

def west_wall():
    """PX0 face (y 118.5 .. 153.4; image left = y 118.5): black dado, red panels with yellow ornament (scheme rule, I)"""
    w = 34.9; W = Wall(w, seed=19); red_panel_scheme(W, 0, w, 'red', True, 19); W.age(9, 19); return W.im

def tablinum_wall():
    """TY1 face (x -494.6 .. -561.4; image left = x -494.6), tablinum opening u 25.4..41.4 below 15.5 ft (transparent)"""
    w = 66.8; W = Wall(w, seed=7)
    red_panel_scheme(W, 0, 25.4, 'red', True, 7); red_panel_scheme(W, 41.4, w, 'red', True, 8)
    W.frieze(0, w, 13.0, 15.6, 'purple', 'yel'); W.upper(0, w, 15.6, H); W.rect(25.4, 41.4, 0, 13.0, 'blk')
    W.age(9, 7); return W.im

def ceiling_tile():
    """8 x 8 ft ambulatory ceiling panel: very thin bright lines on white (No. 18)"""
    W = Wall(8.0, 8.0, 'wht2', 18)
    W.frame(0.0, 8.0, 0.0, 8.0, 'red', 0.12); W.frame(0.45, 7.55, 0.45, 7.55, 'blue', 0.04); W.frame(0.75, 7.25, 0.75, 7.25, 'yel', 0.03)
    W.d.ellipse([W.X(2.6), W.Y(5.4), W.X(5.4), W.Y(2.6)], outline=C['red'], width=3)
    W.d.ellipse([W.X(3.4), W.Y(4.6), W.X(4.6), W.Y(3.4)], outline=C['grn'], width=3)
    for (a, b) in ((0.75, 0.75), (7.25, 0.75), (0.75, 7.25), (7.25, 7.25)):
        W.line(a, b, 4 + (a - 4) * 0.42, 4 + (b - 4) * 0.42, 'grn', 0.03); W.ell(a, b, 0.25, 0.25, 'red')
    for k in range(4):
        t = k * math.pi / 2; W.ell(4 + 1.9 * math.cos(t), 4 + 1.9 * math.sin(t), 0.18, 0.18, 'blue')
    W.age(5, 18); return W.im

def floor_tile():
    """4 x 4 ft ambulatory pavement: red-brown signinum with a lozenge net of white tesserae and black crosslets (I)"""
    W = Wall(4.0, 4.0, (122, 52, 34), 5)
    rng = random.Random(5)
    for i in range(4000):
        u = rng.uniform(0, 4); z = rng.uniform(0, 4); c = rng.choice([(110, 46, 30), (136, 62, 40), (100, 40, 28)])
        W.rect(u, u + 0.06, z, z + 0.06, c)
    for k in range(-8, 9):
        for t in range(0, 40):
            a = t / 10.0
            for (u, z) in ((a, a + k * 0.5), (a, -a + k * 0.5 + 4)):
                if 0 <= z <= 4: W.rect(u, u + 0.05, z, z + 0.05, (235, 228, 210))
    for u in (0.0, 1.0, 2.0, 3.0):
        for z in (0.5, 1.5, 2.5, 3.5):
            W.rect(u + 0.45, u + 0.55, z - 0.15, z + 0.15, 'blk'); W.rect(u + 0.35, u + 0.65, z - 0.05, z + 0.05, 'blk')
    W.age(6, 5); return W.im

def border_strip():
    """2 x 8 ft black-and-white meander border along the stylobate (I)"""
    W = Wall(8.0, 2.0, (232, 226, 210), 6)
    W.rect(0, 8, 0.15, 0.3, 'blk'); W.rect(0, 8, 1.7, 1.85, 'blk')
    for k in range(8):
        a = k * 1.0 + 0.15
        W.rect(a, a + 0.12, 0.45, 1.55, 'blk'); W.rect(a, a + 0.7, 1.43, 1.55, 'blk'); W.rect(a + 0.58, a + 0.7, 0.75, 1.55, 'blk')
        W.rect(a + 0.3, a + 0.7, 0.75, 0.87, 'blk'); W.rect(a + 0.3, a + 0.42, 0.75, 1.2, 'blk'); W.rect(a, a + 1.0, 0.45, 0.57, 'blk')
    W.age(5, 6); return W.im

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    outs = {'cp039_end_wall_no23.png': end_wall(), 'cp039_west_wall.png': west_wall(), 'cp039_tablinum_wall.png': tablinum_wall(),
            'cp039_ceiling_tile.png': ceiling_tile(), 'cp039_floor_tile.png': floor_tile(), 'cp039_border_strip.png': border_strip()}
    lines = []
    for k, im in outs.items():
        p = os.path.join(OUT, k); im.save(p, optimize=False)
        lines.append('%s  %s  %dx%d' % (hashlib.md5(open(p, 'rb').read()).hexdigest(), k, *im.size))
    open(os.path.join(OUT, 'md5.txt'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
