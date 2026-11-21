#!/usr/bin/env python3
"""Draw the front page: THE WORLD IN ONE DAY - Saturday 21 November 2026.

Renders entry.png (1024x1024) deterministically with Pillow only.
Run:  python3 draw.py [output-path]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
INK = (26, 24, 20)
RED = (172, 28, 36)
DARKRED = (140, 20, 28)
GREY = (96, 90, 78)
RULE = (60, 55, 45)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FD}/DejaVuSerif-Bold.ttf"
SERIF = f"{FD}/DejaVuSerif.ttf"
SANS = f"{FD}/DejaVuSans.ttf"
SANS_B = f"{FD}/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, fnt):
    return d.textlength(text, font=fnt)


def fit(d, text, path, size, max_w, min_size=8):
    """Largest font size <= size that fits text in max_w."""
    while size > min_size:
        f = font(path, size)
        if tw(d, text, f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, num, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = font(SANS_B, 12 if num < 10 else 10)
    t = str(num)
    d.text((x - tw(d, t, f) / 2, y - 7 if num < 10 else y - 6), t, font=f,
           fill=WHITE)


def banner(d, x, y, w, label, h=24, fsize=13):
    d.rectangle([x, y, x + w, y + h], fill=RED)
    f = fit(d, label, SANS_B, fsize, w - 10)
    d.text((x + 6, y + (h - fsize) / 2 - 1), label, font=f, fill=WHITE)


def source_tag(d, x, y, w, text, anchor_right=True):
    f = font(SANS_B, 9)
    twd = tw(d, text, f)
    bw = twd + 10
    bx = x + w - bw if anchor_right else x
    d.rectangle([bx, y - 14, bx + bw, y], fill=(20, 20, 20))
    d.text((bx + 5, y - 12), text, font=f, fill=WHITE)


# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    # sky bands
    d.rectangle([x, y, x + w, y + h], fill=(198, 224, 232))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(240, 200, 120))
    # sun
    d.ellipse([x + w - 52, y + 10, x + w - 16, y + 46], fill=(246, 178, 60))
    # globe
    gx, gy, gr = x + 78, y + h // 2 + 8, 52
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 132, 196))
    blob = (88, 168, 92)
    d.polygon([(gx - 34, gy - 26), (gx - 12, gy - 34), (gx - 6, gy - 16),
               (gx - 18, gy - 4), (gx - 34, gy - 8)], fill=blob)
    d.polygon([(gx + 2, gy - 30), (gx + 26, gy - 26), (gx + 30, gy - 8),
               (gx + 12, gy - 10), (gx + 4, gy - 18)], fill=blob)
    d.polygon([(gx - 10, gy + 8), (gx + 8, gy + 6), (gx + 14, gy + 22),
               (gx + 2, gy + 34), (gx - 8, gy + 22)], fill=blob)
    d.polygon([(gx + 22, gy + 14), (gx + 36, gy + 18), (gx + 30, gy + 30),
               (gx + 20, gy + 24)], fill=blob)
    # thermometer
    tx = x + w - 108
    d.rounded_rectangle([tx, y + 18, tx + 16, y + h - 26], 8, fill=WHITE,
                        outline=INK, width=2)
    d.rectangle([tx + 5, y + 52, tx + 11, y + h - 30], fill=RED)
    d.ellipse([tx - 6, y + h - 44, tx + 22, y + h - 16], fill=RED)
    for i in range(4):
        ly = y + 28 + i * 18
        d.line([tx + 18, ly, tx + 26, ly], fill=INK, width=2)
    # clock (overtime)
    cx, cy, cr = x + 178, y + 40, 24
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE, outline=INK,
              width=3)
    d.line([cx, cy, cx, cy - 15], fill=INK, width=3)
    d.line([cx, cy, cx + 11, cy + 6], fill=RED, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=INK)
    # delegate tables with little flags
    d.rectangle([x + 8, y + h - 20, x + 130, y + h - 8], fill=(120, 84, 50))
    d.rectangle([x + 150, y + h - 20, x + 240, y + h - 8], fill=(120, 84, 50))
    for i, fcol in enumerate([(200, 40, 50), (40, 90, 170), (240, 190, 60),
                            (60, 150, 80), (150, 60, 140), (230, 120, 40)]):
        fx = x + 20 + i * 36
        d.line([fx, y + h - 34, fx, y + h - 20], fill=INK, width=1)
        d.rectangle([fx, y + h - 34, fx + 11, y + h - 27], fill=fcol)


def scene_saudi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    # stars
    for i, (sx, sy) in enumerate([(30, 18), (70, 34), (120, 14), (170, 40),
                                  (230, 20), (268, 44), (52, 52), (150, 30)]):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(230, 230, 210))
    # moon
    d.ellipse([x + w - 46, y + 8, x + w - 18, y + 36], fill=(238, 232, 200))
    d.ellipse([x + w - 56, y + 6, x + w - 30, y + 34], fill=(16, 22, 48))
    # missile trails (arcs) and bursts
    def burst(bx, by, col=(255, 190, 80)):
        for a in range(0, 360, 30):
            r1, r2 = 4, 15
            d.line([bx + r1 * math.cos(math.radians(a)),
                    by + r1 * math.sin(math.radians(a)),
                    bx + r2 * math.cos(math.radians(a)),
                    by + r2 * math.sin(math.radians(a))], fill=col, width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 240, 190))
    trails = [((x + 26, y + h - 34), (x + 96, y + 40)),
              ((x + 70, y + h - 34), (x + 168, y + 30)),
              ((x + 130, y + h - 34), (x + 238, y + 46))]
    for (x0, y0), (x1, y1) in trails:
        pts = []
        for t in range(21):
            tt = t / 20
            px = x0 + (x1 - x0) * tt
            py = y0 + (y1 - y0) * tt - math.sin(tt * math.pi) * 26
            pts.append((px, py))
        d.line(pts, fill=(255, 160, 70), width=2)
        burst(x1, y1)
    # skyline
    base = y + h
    heights = [44, 66, 38, 78, 52, 88, 46, 70, 40, 60, 34]
    bx = x + 4
    for i, bh in enumerate(heights):
        bw = 22 + (i % 3) * 4
        d.rectangle([bx, base - bh, bx + bw, base], fill=(8, 10, 22))
        for wy in range(int(base - bh) + 6, int(base) - 6, 10):
            for wx in range(int(bx) + 4, int(bx + bw) - 4, 8):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 214, 120))
        bx += bw + 3


def scene_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    # sun and clouds in the sky left of the seismograph
    d.ellipse([x + w - 34, y + 6, x + w - 12, y + 28], fill=(246, 178, 60))
    for cx, cy, s in [(30, 16, 1.0), (58, 30, 0.7)]:
        d.ellipse([x + cx - 16 * s, y + cy - 6 * s, x + cx + 16 * s,
                   y + cy + 6 * s], fill=(248, 246, 240))
        d.ellipse([x + cx - 8 * s, y + cy - 10 * s, x + cx + 9 * s,
                   y + cy + 2 * s], fill=(248, 246, 240))
    # mountains
    d.polygon([(x, y + 58), (x + 60, y + 22), (x + 110, y + 52),
               (x + 160, y + 18), (x + 220, y + 50), (x + w, y + 26),
               (x + w, y + 70), (x, y + 70)], fill=(150, 138, 116))
    # ridge + houses
    gy = y + h - 34
    d.rectangle([x, gy, x + w, y + h], fill=(176, 150, 104))
    for hx, hw, hh in [(18, 34, 22), (66, 28, 18), (238, 36, 24),
                       (196, 26, 17), (150, 24, 15), (282, 26, 18)]:
        d.rectangle([x + hx, gy - hh, x + hx + hw, gy], fill=(240, 236, 220),
                    outline=INK, width=1)
        d.polygon([(x + hx - 3, gy - hh), (x + hx + hw / 2, gy - hh - 10),
                   (x + hx + hw + 3, gy - hh)], fill=RED)
    # ground crack
    crack = [(x + 96, gy), (x + 118, gy + 8), (x + 110, gy + 14),
             (x + 138, gy + 22), (x + 132, gy + 30)]
    d.line(crack, fill=(60, 40, 20), width=3)
    # seismograph drum + trace
    sx, sy, sw, sh = x + 96, y + 12, 130, 52
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE, outline=INK, width=2)
    for gx_ in range(sx + 10, sx + sw, 12):
        d.line([gx_, sy + 2, gx_, sy + sh - 2], fill=(220, 220, 220), width=1)
    pts, mid = [], sy + sh / 2
    pattern = [0, 1, -1, 2, -3, 8, -12, 14, -9, 4, -2, 10, -13, 7, -3, 1, 0]
    for i, v in enumerate(pattern):
        pts.append((sx + 6 + i * (sw - 12) / (len(pattern) - 1), mid - v * 1.6))
    d.line(pts, fill=RED, width=2)


def mini_scene(kind, d, x, y, w, h):
    """Small scene for briefs; each kind draws a recognisable vignette."""
    if kind == "bridge":  # Kyiv warning
        d.rectangle([x, y, x + w, y + h], fill=(30, 42, 74))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(24, 60, 96))
        for px in (x + 26, x + w - 30):
            d.rectangle([px, y + 12, px + 5, y + h - 12], fill=(200, 200, 205))
        d.line([x + 4, y + 20, x + w - 4, y + 20], fill=(220, 220, 225), width=3)
        for i in range(5):
            lx = x + 12 + i * (w - 24) / 4
            d.line([lx, y + 20, lx + 8, y + h - 14], fill=(150, 150, 160),
                   width=1)
        # warning triangle
        cx, cy = x + w // 2, y + 16
        d.polygon([(cx, cy - 9), (cx - 10, cy + 8), (cx + 10, cy + 8)],
                  fill=(250, 200, 60), outline=INK)
        d.text((cx - 2, cy - 4), "!", font=font(SANS_B, 11), fill=INK)
    elif kind == "drone":  # Hormuz
        d.rectangle([x, y, x + w, y + h], fill=(40, 90, 130))
        d.polygon([(x, y), (x + 52, y), (x + 30, y + h), (x, y + h)],
                  fill=(196, 172, 120))
        d.polygon([(x + w, y), (x + w - 46, y), (x + w - 26, y + h),
                   (x + w, y + h)], fill=(196, 172, 120))
        cx, cy = x + w // 2, y + h // 2 - 2
        d.polygon([(cx - 26, cy), (cx + 20, cy - 3), (cx + 28, cy),
                   (cx + 20, cy + 3), (cx - 26, cy)], fill=(60, 60, 66))
        d.line([cx + 6, cy - 3, cx - 8, cy - 13], fill=(60, 60, 66), width=3)
        d.line([cx + 6, cy + 3, cx - 8, cy + 11], fill=(60, 60, 66), width=3)
        for r in (8, 14):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=2)
    elif kind == "centrifuge":  # Tehran uranium
        d.rectangle([x, y, x + w, y + h], fill=(52, 56, 64))
        for i in range(4):
            cx = x + 22 + i * 34
            d.rectangle([cx, y + 10, cx + 18, y + h - 8], fill=(170, 178, 190),
                        outline=INK)
            d.rectangle([cx + 3, y + 16, cx + 15, y + h - 14],
                        fill=(120, 200, 150))
        cx, cy = x + w - 26, y + 18
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(250, 220, 90))
        for a in range(0, 360, 60):
            ex = cx + 11 * math.cos(math.radians(a))
            ey = cy + 11 * math.sin(math.radians(a))
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], outline=(250, 220, 90),
                      width=2)
    elif kind == "servers":  # Trump AI tax
        d.rectangle([x, y, x + w, y + h], fill=(36, 44, 58))
        for i in range(3):
            rx = x + 14 + i * 40
            d.rectangle([rx, y + 8, rx + 30, y + h - 6], fill=(88, 100, 118),
                        outline=INK)
            for j in range(3):
                d.ellipse([rx + 5, y + 13 + j * 11, rx + 9, y + 17 + j * 11],
                          fill=(110, 230, 140))
        d.polygon([(x + w - 40, y + 8), (x + w - 12, y + 8), (x + w - 12,
                    y + 30), (x + w - 26, y + 38), (x + w - 40, y + 30)],
                  fill=RED)
        f = font(SANS_B, 15)
        d.text((x + w - 33, y + 12), "$", font=f, fill=WHITE)
    elif kind == "flags":  # China-Japan
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
        d.line([x + 40, y + 6, x + 40, y + h - 4], fill=INK, width=2)
        d.rectangle([x + 40, y + 6, x + 88, y + 30], fill=(222, 41, 47))
        for sx, sy in [(46, 10), (56, 8), (58, 14), (56, 20)]:
            d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4],
                      fill=(255, 222, 60))
        d.line([x + w - 40, y + 6, x + w - 40, y + h - 4], fill=INK, width=2)
        d.rectangle([x + w - 88, y + 6, x + w - 40, y + 30], fill=WHITE,
                    outline=INK)
        d.ellipse([x + w - 72, y + 12, x + w - 56, y + 28], fill=(200, 30, 40))
    elif kind == "jet":  # Davao
        d.rectangle([x, y, x + w, y + h], fill=(24, 34, 62))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 90, 96))
        for i in range(10):
            d.line([x + 8 + i * 18, y + h - 4, x + 16 + i * 18, y + h - 4],
                   fill=(250, 220, 90), width=2)
        cy = y + 20
        d.polygon([(x + 22, cy), (x + 96, cy - 6), (x + 128, cy + 2),
                   (x + 96, cy + 7), (x + 26, cy + 6)], fill=(225, 228, 232))
        d.polygon([(x + 26, cy - 2), (x + 40, cy - 13), (x + 50, cy - 12),
                   (x + 44, cy)], fill=(200, 30, 40))
        d.polygon([(x + 84, cy + 4), (x + 104, cy + 13), (x + 94, cy + 13),
                   (x + 76, cy + 6)], fill=(200, 205, 212))
        for fx in range(3):
            d.polygon([(x + 108 + fx * 5, cy - 2), (x + 122 + fx * 6, cy - 6),
                       (x + 118 + fx * 5, cy + 3)], fill=(250, 140, 40))
    elif kind == "parliament":  # Canberra AI
        d.rectangle([x, y, x + w, y + h], fill=(206, 224, 240))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 170, 100))
        bx, bw = x + w // 2 - 44, 88
        d.rectangle([bx, y + 24, bx + bw, y + h - 8], fill=(238, 238, 240),
                    outline=INK)
        d.polygon([(bx - 6, y + 24), (bx + bw // 2, y + 6), (bx + bw + 6,
                    y + 24)], fill=(150, 60, 50))
        d.line([x + w // 2, y + 6, x + w // 2, y - 2 + 8], fill=INK, width=2)
        d.polygon([(x + w // 2, y + 2), (x + w // 2 + 12, y + 5),
                   (x + w // 2, y + 8)], fill=(40, 80, 160))
        for i in range(4):
            d.rectangle([bx + 10 + i * 19, y + 30, bx + 17 + i * 19,
                         y + h - 12], fill=(90, 120, 160))
        f = font(SANS_B, 12)
        d.text((x + 10, y + 12), "AI", font=f, fill=(30, 90, 160))
    elif kind == "bitcoin":  # Markets
        d.rectangle([x, y, x + w, y + h], fill=(26, 28, 36))
        pts = [(x + 8, y + 10), (x + 44, y + 16), (x + 74, y + 12),
               (x + 104, y + 24), (x + 134, y + 30), (x + w - 10, y + 40)]
        d.line(pts, fill=(240, 90, 80), width=3)
        d.polygon([(x + w - 10, y + 40), (x + w - 22, y + 38),
                   (x + w - 14, y + 28)], fill=(240, 90, 80))
        cx, cy, r = x + 40, y + h - 22, 15
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26))
        f = font(SANS_B, 17)
        d.text((cx - 6, cy - 11), "B", font=f, fill=WHITE)
    elif kind == "f1":  # Las Vegas
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 40))
        pts = [(x + 10, y + 30), (x + 44, y + 12), (x + 84, y + 26),
               (x + 110, y + 10), (x + 140, y + 30), (x + w - 12, y + 16)]
        d.line(pts, fill=(230, 230, 235), width=4)
        for i in range(4):
            for j in range(2):
                col = (240, 240, 240) if (i + j) % 2 == 0 else (20, 20, 20)
                d.rectangle([x + w - 34 + i * 7, y + 6 + j * 7,
                             x + w - 27 + i * 7, y + 13 + j * 7], fill=col)
        d.polygon([(x + 58, y + 34), (x + 84, y + 30), (x + 92, y + 36),
                   (x + 84, y + 41), (x + 60, y + 40)], fill=(200, 30, 40))
        d.rectangle([x + 70, y + 24, x + 78, y + 32], fill=(200, 30, 40))
    elif kind == "cricket":  # Wellington
        d.rectangle([x, y, x + w, y + h], fill=(104, 168, 92))
        d.rectangle([x + 62, y + 4, x + 118, y + h - 4], fill=(216, 198, 150))
        for sx in (x + 132, x + 139, x + 146):
            d.rectangle([sx, y + 12, sx + 3, y + 34], fill=(240, 230, 190),
                        outline=INK)
        d.line([x + 130, y + 12, x + 148, y + 12], fill=(240, 230, 190),
               width=3)
        d.line([x + 30, y + 34, x + 58, y + 12], fill=(150, 100, 50), width=5)
        d.ellipse([x + 96, y + 8, x + 106, y + 18], fill=(178, 30, 40))


# ---------------------------------------------------------------- map
LAND = [
    # (lon0, lon1, lat0, lat1) coarse land boxes for a dot-grid world map
    (-168, -52, 52, 72), (-140, -120, 32, 50), (-125, -66, 25, 49),
    (-102, -86, 14, 24), (-92, -77, 7, 19), (-80, -72, -4, 11),
    (-79, -35, -33, 5), (-73, -55, -54, -33), (-70, -55, -38, -22),
    (-58, -35, -10, -34), (-18, -12, 65, 67), (-25, -12, 64, 66),
    (-11, 2, 50, 59), (-6, -2, 43, 49), (-9, 3, 36, 44),
    (3, 19, 42, 51), (5, 31, 45, 55), (12, 45, 48, 60),
    (18, 32, 54, 70), (28, 48, 41, 52), (45, 180, 50, 68),
    (60, 140, 42, 55), (100, 142, 20, 42), (78, 98, 8, 28),
    (92, 110, 5, 22), (112, 122, 20, 32), (122, 130, 28, 38),
    (126, 142, 34, 46), (129, 142, 43, 51), (140, 146, 36, 45),
    (-17, 35, 15, 32), (-10, 32, 30, 36), (10, 30, 30, 33),
    (32, 52, 12, 32), (12, 42, -34, 12), (42, 52, -12, 12),
    (44, 50, -16, -12), (113, 154, -39, -11), (166, 178, -47, -34),
    (95, 105, 5, 20), (100, 110, -6, 2), (109, 119, -3, 7),
    (119, 126, 0, 2), (120, 127, 6, 19), (131, 141, -4, -1),
    (141, 150, -6, -3), (40, 44, 36, 42), (44, 60, 24, 30),
    (48, 60, 12, 26), (34, 44, 28, 38), (54, 78, 6, 20),
    (68, 90, 20, 36), (90, 98, 20, 28),
]


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 234),
                outline=RULE, width=1)
    cols, rows = 100, 34
    cw, ch = w / cols, h / rows
    for r in range(rows):
        lat = 80 - r * (140 / rows)
        for c in range(cols):
            lon = -180 + c * (360 / cols)
            for (a, b, la, lb) in LAND:
                if a <= lon <= b and la <= lat <= lb:
                    cx = x + c * cw + cw / 2
                    cy = y + r * ch + ch / 2
                    d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                              fill=(116, 156, 96))
                    break
    for num, lon, lat, dx, dy in pins:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (80 - lat) / 140 * h + dy
        r = 7.5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE,
                  width=1)
        f = font(SANS_B, 8 if num < 10 else 7)
        t = str(num)
        d.text((px - tw(d, t, f) / 2, py - 4.5), t, font=f, fill=WHITE)


# ---------------------------------------------------------------- page
def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    CW = W - 2 * M

    # kicker
    f = font(SANS_B, 21)
    d.text((M, 14), "THE WORLD IN ONE DAY", font=f, fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    fr = fit(d, right, SANS_B, 16, 640)
    d.text((W - M - tw(d, right, fr), 18), right, font=fr, fill=RED)
    d.line([M, 46, W - M, 46], fill=RULE, width=2)

    # masthead
    fm = fit(d, "Saturday 21 November 2026", SERIF_B, 84, CW)
    d.text((M, 52), "Saturday 21 November 2026", font=fm, fill=INK)
    deck = ("Summit runs past its deadline \u00b7 missiles downed over "
            "Saudi Arabia \u00b7 deep quake shakes Peru")
    fd = fit(d, deck, SERIF, 20, CW)
    d.text(((W - tw(d, deck, fd)) / 2, 138), deck, font=fd, fill=(70, 60, 40))
    d.line([M, 168, W - M, 168], fill=RULE, width=1)

    # stat strip
    stats = [
        ("Day 13", "of COP31, a summit planned to close on day 12"),
        ("5", "Houthi missiles shot down over Riyadh and Jizan"),
        ("6.7", "magnitude of the earthquake in Jun\u00edn, Peru"),
        ("146", "people safe after a jet's emergency landing"),
        ("$58,983", "bitcoin early Saturday, down 3.9% in a day"),
        ("124*", "K. L. Rahul's score at tea in Wellington"),
    ]
    sy, sh = 176, 66
    cell = CW / 6
    for i, (num, cap) in enumerate(stats):
        cx = M + i * cell
        if i:
            d.line([cx, sy + 4, cx, sy + sh - 4], fill=RULE, width=1)
        fn_ = fit(d, num, SERIF_B, 33, cell - 12)
        d.text((cx + (cell - tw(d, num, fn_)) / 2, sy), num, font=fn_, fill=RED)
        fc = font(SANS, 10)
        for j, ln in enumerate(wrap(d, cap, fc, cell - 12)):
            d.text((cx + (cell - tw(d, ln, fc)) / 2, sy + 38 + j * 12), ln,
                   font=fc, fill=GREY)
    d.line([M, sy + sh + 4, W - M, sy + sh + 4], fill=RULE, width=1)

    # region bar
    regions = [("EUROPE", 4, (84, 110, 168)), ("ASIA", 10, (196, 84, 60)),
               ("MIDDLE EAST", 5, (222, 164, 60)), ("AFRICA", 1, (96, 150, 90)),
               ("AMERICAS", 11, (70, 130, 150)), ("OCEANIA", 3, (140, 100, 160)),
               ("GLOBAL", 1, (110, 110, 110))]
    ry, rh = 252, 24
    total = sum(c for _, c, _ in regions)
    rx = M
    widths, acc = [], 0
    for i, (_, c, _) in enumerate(regions):
        wseg = round(CW * c / total) if i < len(regions) - 1 else CW - acc
        widths.append(wseg)
        acc += wseg
    for (name, c, col), wseg in zip(regions, widths):
        d.rectangle([rx, ry, rx + wseg, ry + rh], fill=col)
        label = f"{name} {c}"
        if wseg >= 44:
            fl = fit(d, label, SANS_B, 12, wseg - 6, min_size=7)
            d.text((rx + (wseg - tw(d, label, fl)) / 2, ry + 5), label,
                   font=fl, fill=WHITE)
        else:
            # thin segment: stack name over count so the label stays
            # inside its own segment
            fl = font(SANS_B, 8)
            d.text((rx + (wseg - tw(d, name, fl)) / 2, ry + 2), name,
                   font=fl, fill=WHITE)
            cs = str(c)
            d.text((rx + (wseg - tw(d, cs, fl)) / 2, ry + 12), cs,
                   font=fl, fill=WHITE)
        rx += wseg

    # heroes
    heroes = [
        dict(banner="COP31: OVERTIME", scene=scene_cop31, tag="AFP \u00b7 Al Jazeera",
             place="ANTALYA, T\u00dcRK\u0130YE \u00b7 CLIMATE",
             head="Climate Summit Runs Past Its Deadline, Still No Deal",
             body="Into day 13 after missing Friday's planned close, the "
                  "summit stayed split over a draft that never mentions "
                  "fossil fuels; a third text was promised. (AFP, Al Jazeera)"),
        dict(banner="SAUDI: MISSILES", scene=scene_saudi, tag="AFP \u00b7 Reuters",
             place="RIYADH \u00b7 JIZAN \u00b7 WAR",
             head="Five Houthi Missiles Shot Down Over Saudi Arabia",
             body="Three ballistic missiles were destroyed over Riyadh "
                  "before dawn and two over Jizan late on Friday, a day "
                  "after it bombed Hodeidah port. (AFP, Reuters)"),
        dict(banner="PERU: QUAKE 6.7", scene=scene_peru, tag="USGS \u00b7 IGP",
             place="JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
             head="Deep Quake of 6.7 Shakes Central Peru",
             body="The quake struck at 00:09 UTC near Carhuamayo, 108 km "
                  "down, and was felt in Lima and along the coast. Peru's "
                  "IGP reported no deaths and no tsunami risk. (USGS, IGP)"),
    ]
    hy, hh = 288, 252
    hgap = 16
    hw = (CW - 2 * hgap) // 3
    for i, hro in enumerate(heroes):
        hx = M + i * (hw + hgap)
        sh_h = 128
        hro["scene"](d, hx, hy, hw, sh_h)
        banner(d, hx, hy, hw, hro["banner"], h=24, fsize=13)
        source_tag(d, hx, hy + sh_h, hw, hro["tag"])
        badge(d, hx + 12, hy + sh_h + 16, i + 1)
        fp = font(SANS_B, 11)
        d.text((hx + 28, hy + sh_h + 10), hro["place"], font=fp, fill=RED)
        fh = font(SERIF_B, 19)
        lines = wrap(d, hro["head"], fh, hw - 2)
        ly = hy + sh_h + 30
        for ln in lines[:2]:
            d.text((hx, ly), ln, font=fh, fill=INK)
            ly += 23
        fb = font(SANS, 11)
        for ln in wrap(d, hro["body"], fb, hw - 2)[:5]:
            d.text((hx, ly + 2), ln, font=fb, fill=(50, 46, 38))
            ly += 14

    # briefs
    briefs = [
        ("bridge", "KYIV: WARNING", "NBC", "Zelensky: Crimea Bridge \u2018Will Not Stay\u2019",
         "He warns Putin as Russia steps up double-tap strikes. (NBC)"),
        ("drone", "HORMUZ: DRONE", "IRIB", "Iran Says It Shot Down a US Drone",
         "Tehran claims a 58th MQ-9; Washington has not confirmed. (IRIB)"),
        ("centrifuge", "TEHRAN: URANIUM", "Tol", "Iran: Uranium Stock Stays in Iran",
         "The minister still sees a \u2018fair solution\u2019. (Tol)"),
        ("servers", "WASHINGTON: AI TAX", "ABC", "Trump Vows a Tax on Data Centres Abroad",
         "A \u2018tremendous\u2019 penalty; no details yet. (ABC)"),
        ("flags", "BEIJING: TAIWAN", "AFP", "China Tells Japan to Correct Its Taiwan Words",
         "Tokyo says its stance is unchanged. (AFP)"),
        ("jet", "DAVAO: 146 SAFE", "AP", "Jet Lands Safely After an Engine Fire Alert",
         "Air Niugini diverts after midnight; all 146 safe. (AP)"),
        ("parliament", "CANBERRA: AI TALKS", "ABC", "Australia and China Agree to AI Talks",
         "Albanese ends an 11-day trip. (ABC)"),
        ("bitcoin", "BITCOIN: $58,983", "CoinGecko", "Bitcoin Trades Below $59,000",
         "Ether falls 6.1% to $1,625 in the sell-off. (CoinGecko)"),
        ("f1", "VEGAS: RUSSELL P1", "Formula 1", "Russell Fastest in Final Vegas Practice",
         "1:34.041 on a slippery track, well clear. (Formula 1)"),
        ("cricket", "WELLINGTON: 124*", "AFP", "Rahul Hits a Century Against New Zealand",
         "124 not out at tea; India 344 for 2. (AFP)"),
    ]
    by = 552
    bgap = 12
    bw = (CW - 4 * bgap) // 5
    brow_h = 102
    for idx, (kind, blab, stag, head, text) in enumerate(briefs):
        r, c = divmod(idx, 5)
        bx = M + c * (bw + bgap)
        yy = by + r * (brow_h + 4)
        sc_h = 46
        mini_scene(kind, d, bx, yy, bw, sc_h)
        banner(d, bx, yy, bw, blab, h=14, fsize=9)
        source_tag(d, bx, yy + sc_h, bw, stag)
        badge(d, bx + 9, yy + sc_h + 11, idx + 4, r=8)
        fh = fit(d, head, SANS_B, 12, bw - 2, min_size=9)
        # first headline line is indented past the badge
        first = wrap(d, head, fh, bw - 22)[0]
        rest = head[len(first):].strip()
        ly = yy + sc_h + 5
        d.text((bx + 21, ly), first, font=fh, fill=INK)
        ly += 13
        if rest:
            for ln in wrap(d, rest, fh, bw - 2)[:1]:
                d.text((bx, ly), ln, font=fh, fill=INK)
                ly += 13
        ft = font(SANS, 9)
        for ln in wrap(d, text, ft, bw - 2)[:2]:
            d.text((bx, ly + 1), ln, font=ft, fill=(50, 46, 38))
            ly += 10

    # bottom: map + index
    bot_y = 776
    map_w = 428
    fh2 = font(SANS_B, 13)
    d.text((M, bot_y), "WHERE IT HAPPENED", font=fh2, fill=INK)
    pins = [
        (1, 30.7, 36.9, 0, 0), (2, 46.7, 24.6, 0, 0), (3, -75.5, -11.2, 0, 0),
        (4, 30.5, 50.4, -4, -4), (5, 56.5, 26.5, 6, 2), (6, 51.4, 35.7, 0, -6),
        (7, -77.0, 38.9, -8, -4), (8, 116.4, 39.9, 4, -4),
        (9, 125.6, 7.1, 0, 0), (10, 149.1, -35.3, 0, 0),
        (11, -30.0, 22.0, 0, 0), (12, -115.1, 36.2, -6, -4),
        (13, 174.8, -41.3, 0, 0), (14, 33.4, 47.9, 8, 6),
        (15, 12.6, 55.7, 0, 0), (16, 30.7, 36.9, 11, 6),
        (17, -79.5, 9.0, 0, 4), (18, 106.8, -6.2, 0, 0),
        (19, 43.3, 14.8, -6, 4), (20, -77.0, 38.9, 9, 4),
        (21, -77.0, 38.9, 0, 10), (22, -99.0, 31.5, 0, 0),
        (23, -118.2, 34.1, -10, 6), (24, -92.5, 38.4, 6, -6),
        (25, -123.1, 49.3, 0, 0), (26, 125.8, 39.0, -6, -6),
        (27, 127.3, 36.5, 8, 4), (28, 121.6, 25.0, 6, 6),
        (29, 100.5, 13.8, -4, 4), (30, 77.2, 28.6, -6, 0),
        (31, 85.1, 20.3, 6, 6), (32, 96.2, 19.0, 8, -4),
        (33, 57.5, -20.2, 0, 0), (34, 145.0, -37.8, -8, 4),
        (35, -115.1, 36.2, 8, 6),
    ]
    draw_map(d, M, bot_y + 18, map_w, 128, pins)

    ix = M + map_w + 18
    iw = W - M - ix
    d.text((ix, bot_y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=fit(d, "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
                    SANS_B, 13, iw), fill=INK)
    index = [
        "14 Kryvyi Rih \u2014 double strike kills 2, injures 42 (Kyiv Independent)",
        "15 Copenhagen \u2014 Russian attach\u00e9 expelled over a plot (Al Jazeera)",
        "16 Antalya \u2014 EU warns of a no-\u2018fossil summit\u2019 (AFP)",
        "17 Antalya \u2014 Panama threatens to block the text (Al Jazeera)",
        "18 Antalya \u2014 PLN signs six clean-power deals (Antara)",
        "19 Yemen \u2014 Houthis threaten Jeddah, Red Sea ports (Al Jazeera)",
        "20 Washington \u2014 Vance: Iran strikes were Trump's call (Reuters)",
        "21 Washington \u2014 lawmaker threatens SpaceX funding (CNN)",
        "22 Texas \u2014 execution of a man of 67 takes 63 minutes (ABC)",
        "23 Los Angeles \u2014 jury convicts Palisades fire starter (ABC)",
        "24 Missouri \u2014 judge OKs $7.25bn Roundup settlement (AFP)",
        "25 Vancouver \u2014 Canada rests defence in youth climate trial (AFP)",
        "26 Pyongyang \u2014 Kim tours factories, no Trump meeting (AFP)",
        "27 Sejong \u2014 freight train derails; no one hurt (Korea Herald)",
        "28 Taipei \u2014 budget and a cash payout are passed (Taipei Times)",
        "29 Bangkok \u2014 six-point plan on arsenic in two rivers (The Nation)",
        "30 New Delhi \u2014 Pakistani minister at SCO forum in India (Dawn)",
        "31 Eastern India \u2014 rain alerts as Akvan remnants move in (ETV)",
        "32 Myanmar \u2014 groups urge sanctions after court ruling (AP)",
        "33 Port Louis \u2014 African rating agency talks to 15 states (UN)",
        "34 Melbourne \u2014 Cummins keeps the Australian captaincy (ABC)",
        "35 Las Vegas \u2014 Verstappen sent to the stewards (Autosport)",
    ]
    fi = font(SANS, 10)
    col_w = (iw - 14) / 2
    for i, line in enumerate(index):
        cx = ix + (i // 11) * (col_w + 14)
        ly = bot_y + 22 + (i % 11) * 12
        fline = fit(d, line, SANS, 10, col_w, min_size=7)
        d.text((cx, ly), line, font=fline, fill=(40, 37, 30))

    # date check strip
    dy = 932
    d.rectangle([M, dy, W - M, dy + 62], outline=RED, width=2)
    fdc = font(SANS_B, 11)
    d.text((M + 8, dy + 5), "DATE CHECK \u2014 left out, with their real dates:",
           font=fdc, fill=RED)
    left = [
        "\u2715 Fri 20 Nov \u2014 Wall Street's fall into a correction",
        "\u2715 Fri 20 Nov \u2014 the barrage that hit Kyiv's bridges",
        "\u2715 Fri 20 Nov \u2014 the missile that landed in Poland",
        "\u2715 Fri 20 Nov \u2014 the UK\u2013EU reset deal",
    ]
    right = [
        "\u2715 Fri 20 Nov \u2014 Cyclone Akvan's landfall in India",
        "\u2715 Wed 18 Nov \u2014 Voyager 1 reaches one light-day",
        "? Not confirmed \u2014 BepiColombo's Mercury orbit entry",
        "? Not confirmed \u2014 any final COP31 text",
    ]
    fdi = font(SANS, 9)
    for j in range(4):
        yy = dy + 20 + j * 10
        d.text((M + 8, yy), left[j], font=fdi, fill=(40, 37, 30))
        d.text((M + 500, yy), right[j], font=fdi, fill=(40, 37, 30))

    # footer
    foot = ("Every story on this page happened, or was first reported, on "
            "Saturday 21 November 2026. Officials' counts and claims are "
            "attributed; sources are named beside each story; all "
            "illustrations are original drawings.")
    ff = fit(d, foot, SANS, 9, CW)
    d.text((M, 1002), foot, font=ff, fill=GREY)

    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
