#!/usr/bin/env python3
"""THE WORLD — Wednesday 18 November 2026. Front page, drawn fresh with PIL.
Revision focus: realistic buildings — a believable Shenzhen dusk skyline
(Ping An Finance Centre, KingKey 100, China Resources Tower) with real
window grids, facade shading and haze, plus a detailed US Capitol dome.
Deterministic: fixed seed, no network, no time input."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24
CW = W - 2 * M

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (110, 105, 95)
RULE = (30, 30, 30)

DJ = "/usr/share/fonts/truetype/dejavu/"
SERIF = DJ + "DejaVuSerif.ttf"
SERIF_B = DJ + "DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = DJ + "DejaVuSans.ttf"
SANS_B = DJ + "DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def lerp(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def vgrad(d, x0, y0, x1, y1, c_top, c_bot):
    """Vertical gradient filled box."""
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(c_top, c_bot, (y - y0) / h))


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, font, fill, maxw, leading):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color):
    """Colour-coded section kicker with a small square bullet."""
    f = F(SANS_B, 11)
    d.rectangle([x, y + 1, x + 8, y + 9], fill=color)
    d.text((x + 12, y), text, font=f, fill=color)
    return y + 14


# ---------------------------------------------------------------- skyline
def tower_windows(d, cx, y_top, y_bot, w_top, w_bot, rows, cols, rng,
                  lit_prob, lit_col, dark_col, curve=1.0, ww=3, wh=4):
    """Window grid on a tapered tower. Width interpolates top->bottom.
    curve>1 makes the taper bulge outward near the base (bamboo shoot)."""
    h = max(1, y_bot - y_top)
    for r in range(rows):
        y = y_top + int((r + 0.5) * h / rows)
        t = (y - y_top) / h
        w = w_top + (w_bot - w_top) * (t ** curve)
        left = cx - w / 2
        for c in range(cols):
            x = left + (c + 0.5) * w / cols
            col = lit_col if rng.random() < lit_prob else dark_col
            d.rectangle([x - ww / 2, y - wh / 2, x + ww / 2, y + wh / 2],
                        fill=col)


def tapered_body(d, cx, y_top, y_bot, w_top, w_bot, c_top, c_bot, curve=1.0):
    """Tower body as horizontal slices -> smooth vertical gradient + taper."""
    h = max(1, y_bot - y_top)
    for y in range(y_top, y_bot):
        t = (y - y_top) / h
        w = w_top + (w_bot - w_top) * (t ** curve)
        d.line([(cx - w / 2, y), (cx + w / 2, y)],
               fill=lerp(c_top, c_bot, t))


def draw_skyline(d, x0, y0, x1, y1):
    """Shenzhen at dusk. Far hazy layer, mid layer, near landmarks, sun,
    ground band with reflections, and the summit table in front."""
    rng = random.Random(20261118)
    # --- sky: deep dusk purple -> orange horizon
    vgrad(d, x0, y0, x1, y1, (36, 22, 64), (232, 134, 58))
    # --- sun glow, low on the right (kept inside the hero box)
    sx, sy = x1 - 150, y1 - 26
    for r, col in [(44, (232, 150, 80)), (34, (244, 178, 96)),
                   (22, (252, 205, 130)), (12, (255, 226, 160))]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    # --- far hazy towers (pale, low contrast; heights fit inside the box)
    far = [(70, 66, 30), (150, 60, 26), (420, 64, 28), (500, 58, 24),
           (660, 62, 26), (800, 60, 30), (905, 64, 26), (950, 58, 20)]
    for fx, fh, fw in far:
        d.rectangle([fx, y1 - fh, fx + fw, y1], fill=(148, 122, 170))
        for wy in range(y1 - fh + 6, y1 - 4, 8):
            for wx in range(fx + 4, fx + fw - 3, 7):
                if rng.random() < 0.35:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(168, 146, 186))
    # --- mid layer blocks with real window grids (tops inside the box)
    mid = [(110, 76, 46, 0.42), (210, 70, 40, 0.38), (455, 80, 44, 0.45),
           (770, 74, 42, 0.40), (860, 68, 38, 0.36)]
    for mx, mh, mw, lit in mid:
        d.rectangle([mx, y1 - mh, mx + mw, y1], fill=(58, 42, 88))
        for wy in range(y1 - mh + 7, y1 - 5, 9):
            for wx in range(mx + 5, mx + mw - 4, 8):
                col = (255, 208, 120) if rng.random() < lit else (46, 54, 96)
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=col)
    # --- Ping An Finance Centre: tallest, tapered, spire + antenna
    # (all inside the hero box: body top 134, spire tip 112)
    cx, yb = 330, y1
    tapered_body(d, cx, 134, yb, 30, 64, (74, 53, 104), (28, 18, 51))
    tower_windows(d, cx, 136, yb - 4, 28, 60, 13, 7, rng, 0.48,
                  (255, 210, 122), (40, 50, 92))
    d.polygon([(cx - 13, 134), (cx + 13, 134), (cx + 3, 118), (cx - 3, 118)],
              fill=(58, 42, 88))
    d.line([(cx, 118), (cx, 112)], fill=(200, 190, 220), width=2)
    d.ellipse([cx - 2, 110, cx + 2, 114], fill=(255, 220, 140))
    # --- KingKey 100: sloped top, slight taper
    cx2 = 590
    d.polygon([(cx2 - 26, yb), (cx2 - 24, 140), (cx2 + 24, 148),
               (cx2 + 26, yb)], fill=(66, 47, 96))
    tower_windows(d, cx2, 144, yb - 4, 44, 50, 12, 6, rng, 0.44,
                  (255, 208, 120), (38, 48, 90))
    d.line([(cx2 - 24, 140), (cx2 + 24, 148)], fill=(120, 100, 150), width=2)
    # --- China Resources Tower: bamboo shoot, curved taper + rings + ribs
    cx3 = 735
    tapered_body(d, cx3, 136, yb, 18, 60, (80, 58, 110), (30, 20, 54),
                 curve=1.6)
    tower_windows(d, cx3, 140, yb - 4, 16, 56, 13, 6, rng, 0.46,
                  (255, 212, 124), (42, 52, 94), curve=1.6)
    for ry in range(148, yb - 6, 12):
        t = (ry - 136) / (yb - 136)
        w = 18 + (60 - 18) * (t ** 1.6)
        d.line([(cx3 - w / 2, ry), (cx3 + w / 2, ry)], fill=(128, 108, 158))
    for f in (-0.32, 0.0, 0.32):
        xs = []
        for yy in range(136, yb, 8):
            t = (yy - 136) / (yb - 136)
            w = 18 + (60 - 18) * (t ** 1.6)
            xs.append((cx3 + f * w, yy))
        d.line(xs, fill=(110, 92, 142), width=1)
    # --- near dark base band + faint window reflections
    d.rectangle([x0, y1 - 8, x1, y1], fill=(20, 16, 42))
    for rx in range(x0 + 30, x1 - 20, 46):
        if rng.random() < 0.6:
            d.line([(rx, y1 - 8), (rx, y1 - 2)], fill=(150, 100, 50), width=2)
    # --- summit table in front: three figures, three flags
    tx0, tx1, ty0, ty1 = 452, 572, y1 - 22, y1 - 2
    d.ellipse([tx0, ty0 - 4, tx1, ty1 + 6], fill=(14, 10, 30))
    for fx, fc in [(478, (178, 34, 52)), (512, (222, 0, 0)),
                   (546, (255, 255, 255))]:
        d.line([(fx, ty0 - 26), (fx, ty0 - 6)], fill=(220, 210, 190), width=1)
        if fc == (178, 34, 52):
            d.rectangle([fx, ty0 - 26, fx + 15, ty0 - 16], fill=(178, 34, 52))
            d.rectangle([fx, ty0 - 26, fx + 15, ty0 - 23], fill=(255, 255, 255))
            d.rectangle([fx, ty0 - 26, fx + 15, ty0 - 20], fill=(0, 82, 165))
        elif fc == (222, 0, 0):
            d.rectangle([fx, ty0 - 26, fx + 15, ty0 - 16], fill=(222, 0, 0))
            d.ellipse([fx + 2, ty0 - 25, fx + 6, ty0 - 21], fill=(255, 222, 0))
        else:
            d.rectangle([fx, ty0 - 26, fx + 15, ty0 - 16], fill=(255, 255, 255))
            d.rectangle([fx, ty0 - 23, fx + 15, ty0 - 20], fill=(0, 57, 166))
            d.rectangle([fx, ty0 - 20, fx + 15, ty0 - 16], fill=(213, 0, 50))
    for hx in (470, 512, 554):
        d.ellipse([hx - 6, ty0 - 14, hx + 6, ty0 - 2], fill=(24, 18, 44))
        d.polygon([(hx - 9, ty0 - 2), (hx + 9, ty0 - 2), (hx + 5, ty0 + 8),
                   (hx - 5, ty0 + 8)], fill=(24, 18, 44))


# ---------------------------------------------------------------- capitol
def draw_capitol(d, x0, y0, x1, y1):
    """US Capitol dome, detailed: ribbed dome, lantern, colonnade, steps.
    Scaled to fit exactly inside (x0, y0, x1, y1)."""
    rng = random.Random(77)
    vgrad(d, x0, y0, x1, y1, (22, 38, 77), (48, 74, 130))
    for _ in range(26):
        sx = rng.randint(x0 + 3, x1 - 3)
        sy = rng.randint(y0 + 2, y0 + 12)
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(220, 225, 240))
    cx = (x0 + x1) // 2
    base = y1 - 1
    white = (242, 237, 226)
    shade = (198, 192, 178)
    rib = (170, 164, 150)
    # steps
    d.rectangle([cx - 46, base - 4, cx + 46, base - 2], fill=white)
    d.rectangle([cx - 52, base - 2, cx + 52, base], fill=shade)
    # main block with colonnade
    d.rectangle([cx - 44, base - 13, cx + 44, base - 4], fill=white)
    for colx in range(cx - 38, cx + 39, 8):
        d.line([(colx, base - 12), (colx, base - 5)], fill=rib)
    d.rectangle([cx - 44, base - 14, cx + 44, base - 13], fill=shade)
    # drum
    d.rectangle([cx - 20, base - 18, cx + 20, base - 14], fill=white)
    for colx in range(cx - 16, cx + 17, 5):
        d.line([(colx, base - 17), (colx, base - 15)], fill=rib)
    # dome: half-ellipse, apex at y0+3, base at base-18
    dy0, dy1 = y0 + 3, base - 18
    dx0, dx1 = cx - 28, cx + 28
    d.pieslice([dx0, dy0, dx1, dy1 + 8], 180, 360, fill=white)
    d.pieslice([cx, dy0, dx1, dy1 + 8], 180, 360, fill=shade)
    # ribs: fan lines from the apex down to the base arc
    ecx, ecy = cx, (dy0 + dy1 + 8) // 2
    erx, ery = 28, (dy1 + 8 - dy0) // 2
    for ang in range(205, 336, 19):
        a = math.radians(ang)
        ex = ecx + erx * math.cos(a)
        ey = ecy + ery * math.sin(a)
        d.line([(cx, dy0 + 1), (ex, ey)], fill=rib)
    # lantern + finial (inside the box)
    d.rectangle([cx - 4, dy0 - 3, cx + 4, dy0], fill=white)
    d.line([(cx, dy0 - 3), (cx, y0)], fill=white, width=1)
    d.ellipse([cx - 1, y0, cx + 1, y0 + 2], fill=(255, 220, 140))


# ------------------------------------------------------- small panel art
def art_gulf(d, x0, y0, x1, y1):
    vgrad(d, x0, y0, x1, y1, (24, 44, 96), (52, 92, 150))
    rng = random.Random(5)
    for _ in range(8):
        sx = rng.randint(x0 + 4, x1 - 8)
        sy = y0 + rng.randint(2, 8)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 235))
    for ex, ey, er in [(x1 - 46, y0 + 16, 12), (x1 - 30, y0 + 22, 8)]:
        for r, c in [(er, (232, 120, 40)), (er * 2 // 3, (244, 170, 80)),
                     (er // 3, (255, 220, 140))]:
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    d.line([(x0 + 20, y1 - 8), (x1 - 90, y1 - 8)], fill=(180, 200, 230), width=2)
    for dx in (x0 + 60, x0 + 120, x0 + 190):
        d.ellipse([dx, y0 + 26, dx + 8, y0 + 30], fill=(20, 26, 50))
        d.line([(dx + 8, y0 + 28), (dx + 16, y0 + 28)], fill=(20, 26, 50))


def art_kerch(d, x0, y0, x1, y1):
    vgrad(d, x0, y0, x1, y1, (70, 110, 160), (30, 60, 110))
    d.line([(x0, y0 + 12), (x1, y0 + 12)], fill=(40, 40, 46), width=5)
    d.line([(x0 + 90, y0 + 12), (x0 + 150, y0 + 30)], fill=(40, 40, 46),
           width=5)
    for px in range(x0 + 6, x1 - 6, 18):
        d.line([(px, y0 + 14), (px, y0 + 22)], fill=(30, 30, 38), width=2)
    for sx in (x0 + 120, x0 + 160):
        for r, c in [(9, (120, 120, 125)), (6, (150, 150, 155)),
                     (3, (190, 190, 195))]:
            d.ellipse([sx - r, y0 + 14 - r, sx + r, y0 + 14 + r], fill=c)
    for wy in range(y0 + 26, y1 - 3, 5):
        d.line([(x0 + 8, wy), (x1 - 8, wy)], fill=(90, 130, 175), width=1)


def art_chip(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 60, 40))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 26, cy - 13, cx + 26, cy + 13], fill=(24, 110, 74),
                outline=(140, 220, 170))
    for px in range(cx - 20, cx + 21, 8):
        d.line([(px, cy - 19), (px, cy - 13)], fill=(140, 220, 170), width=2)
        d.line([(px, cy + 13), (px, cy + 19)], fill=(140, 220, 170), width=2)
    d.text((cx - 10, cy - 8), "AI", font=F(SANS_B, 13), fill=(220, 255, 230))


def art_dunes(d, x0, y0, x1, y1):
    vgrad(d, x0, y0, x1, y1, (238, 200, 130), (196, 150, 84))
    d.ellipse([x1 - 40, y0 - 8, x1 - 8, y0 + 24], fill=(255, 226, 150))
    d.arc([x0 - 40, y0 + 6, x1 + 20, y1 + 26], 200, 340, fill=(160, 110, 52),
          width=3)
    d.arc([x0 - 60, y0 + 18, x1, y1 + 30], 200, 340, fill=(140, 96, 44),
          width=3)


def art_virus(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(248, 220, 225))
    rng = random.Random(9)
    for vx, vy, vr in [(x0 + 50, y0 + 20, 11), (x1 - 60, y0 + 18, 9),
                       ((x0 + x1) // 2 + 30, y0 + 22, 7)]:
        for a in range(0, 360, 30):
            ar = math.radians(a)
            d.line([(vx + int(vr * math.cos(ar)), vy + int(vr * math.sin(ar))),
                    (vx + int((vr + 5) * math.cos(ar)),
                     vy + int((vr + 5) * math.sin(ar)))],
                   fill=(200, 40, 60), width=2)
        d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(214, 48, 68))
        d.ellipse([vx - vr // 2, vy - vr // 2, vx + vr // 2, vy + vr // 2],
                  fill=(160, 20, 40))


def art_shield(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(222, 240, 222))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 16, cy - 12), (cx + 16, cy - 12), (cx + 16, cy + 2),
               (cx, cy + 16), (cx - 16, cy + 2)], fill=(255, 255, 255),
              outline=(46, 125, 50))
    d.rectangle([cx - 2, cy - 8, cx + 2, cy + 8], fill=(46, 125, 50))
    d.rectangle([cx - 8, cy - 2, cx + 8, cy + 2], fill=(46, 125, 50))


def art_network(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 230, 244))
    rng = random.Random(11)
    pts = [(x0 + rng.randint(10, (x1 - x0) - 10),
            y0 + rng.randint(6, (y1 - y0) - 6)) for _ in range(7)]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if rng.random() < 0.5:
                d.line([pts[i], pts[j]], fill=(90, 130, 180), width=1)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(31, 78, 121))


def art_candles(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(250, 248, 244))
    rng = random.Random(13)
    x = x0 + 14
    prev = y0 + 12
    while x < x1 - 12:
        h = rng.randint(8, 18)
        top = prev + rng.randint(-6, 6)
        top = max(y0 + 4, min(top, y1 - 6 - h))  # stay inside the strip
        col = (198, 57, 47) if rng.random() < 0.6 else (39, 120, 74)
        d.line([(x + 3, top - 4), (x + 3, top + h + 4)], fill=col, width=1)
        d.rectangle([x, top, x + 6, top + h], fill=col)
        prev = top + h // 2
        x += 16
    d.line([(x0 + 8, y1 - 6), (x1 - 8, y0 + 8)], fill=(163, 22, 33), width=2)


def art_globe(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(206, 232, 226))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 124))
    for k in (-1, 0, 1):
        d.arc([cx - r + k * 6, cy - r, cx + r + k * 6, cy + r], 270, 90,
              fill=(206, 232, 226), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(206, 232, 226), width=1)
    d.ellipse([cx + 6, cy - 6, cx + 12, cy], fill=(120, 200, 110))


# ---------------------------------------------------------------- content
LEAD = {
    "kicker": ("THE SUMMIT — SHENZHEN, CHINA", RED),
    "headline": "Trump, Xi and Putin to hold first three-way summit in Shenzhen",
    "deck": ("Xi Jinping and Vladimir Putin met in Shenzhen on Wednesday, a day "
             "before their planned trilateral with Donald Trump on the sidelines "
             "of the APEC summit — the first meeting of all three leaders."),
    "byline": "By THE WORLD STAFF — SHENZHEN",
}

ROW2 = [
    {"art": art_gulf, "kicker": ("THE GULF — KUWAIT CITY", RED),
     "headline": "Iran strikes Kuwait and Bahrain",
     "deck": ("Iran fired drones at a US base in Kuwait and sites in Bahrain "
              "after US jets hit Qeshm Island.")},
    {"art": art_kerch, "kicker": ("UKRAINE — KERCH", RED),
     "headline": "Kerch Bridge hit again",
     "deck": ("Ukraine struck the bridge to Crimea for a second day; part of "
              "the road span collapsed into the strait.")},
]

GRID = [
    {"art": draw_capitol, "kicker": ("WASHINGTON — ALASKA", RED),
     "headline": "Democrats take the Senate, 56–44",
     "deck": "Mary Peltola defeats Dan Sullivan in Alaska, flipping the chamber."},
    {"art": art_chip, "kicker": ("TECH — SANTA CLARA", (31, 78, 121)),
     "headline": "Nvidia revenue doubles to $115.8B",
     "deck": "Board rules out bringing back Jensen Huang; Colette Kress stays interim chief."},
    {"art": art_dunes, "kicker": ("GAZA — GAZA CITY", RED),
     "headline": "Israel opens new ground operation",
     "deck": "Troops push into Hamas-held central Gaza in the first broad offensive in a year."},
    {"art": art_virus, "kicker": ("HEALTH — DR CONGO", (46, 125, 50)),
     "headline": "Ebola passes 11,000 cases",
     "deck": "Three in four children under five infected do not survive, health officials say."},
    {"art": art_shield, "kicker": ("HEALTH — WASHINGTON", (46, 125, 50)),
     "headline": "US loses measles-free status",
     "deck": "Elimination status held for 26 years ends after 5,400 cases and 10 deaths."},
    {"art": art_network, "kicker": ("TECH — SAN FRANCISCO", (31, 78, 121)),
     "headline": "Anthropic raises $81.3B in record IPO",
     "deck": "The largest stock offering on record prices as AI demand stays hot."},
    {"art": art_candles, "kicker": ("MARKETS — NEW YORK", (194, 87, 27)),
     "headline": "Fed minutes sink stocks; gold dives",
     "deck": "Dow falls 1.1% for a third day; S&P 500 slips below its 200-day average."},
    {"art": art_globe, "kicker": ("CLIMATE — ANTALYA", (15, 118, 110)),
     "headline": "Climate talks deadlocked at COP31",
     "deck": "75 nations back Türkiye's electrification target as finance splits the room."},
]

EU = {
    "kicker": ("EUROPE — BRUSSELS", (30, 58, 95)),
    "headline": "EU proposes €45B loan to Ukraine for 2027",
    "deck": "The loan would be repaid by Russian reparations, the Commission says.",
}
QUOTE = ("An unprecedented operation.",
         "— Volodymyr Zelenskyy, on the Kerch Bridge strike")

FLASH = [
    ("SHENZHEN", "Three-way summit set"),
    ("MANILA", "Quad summit at leader level"),
    ("HORMUZ", "Tanker hit by projectile"),
    ("KUWAIT", "Drones target US base"),
    ("BAHRAIN", "Attacks intercepted"),
    ("QESHIM", "US hit missile site"),
    ("KERCH", "Bridge span collapses"),
    ("KYIV", "141 drones; 126 downed"),
    ("GAZA", "Ground operation opens"),
    ("ANTALYA", "COP31 deadlocked"),
    ("ALASKA", "Senate flips 56–44"),
    ("SIBERIA", "Military plane crash, 19 dead"),
]

NUMBERS = [
    ("3", "leaders at the Shenzhen table"),
    ("141", "drones over Ukraine, 126 downed"),
    ("56–44", "Democrats take the Senate"),
    ("11,000", "Ebola cases in DR Congo"),
    ("$115.8B", "Nvidia quarterly revenue"),
]

BRIEF = [
    "Canada, China cut tariffs after Carney–Xi talks",
    "UK sanctions 8 firms over West Bank settlements",
    "Saudi coalition hits 60 Houthi military sites",
    "950,000 displaced Gazans on flood-prone ground",
    "Russian jets buzz Taiwan; Japan airspace",
    "EU clears signature of Indonesia trade deal",
    "UK inflation at 1-year high, price cap +26% in Jan",
    "Ghana beats USA; Amputee World Cup quarterfinal",
    "Lookman out for rest of 2026 with knee injury",
    "Khel.ai launches cloud-based cricket DRS",
    "Max Tang, 16, takes bronze at Oceanman final",
    "Modi meets Prince and Princess of Wales",
    "Knesset elects Matan Kahana speaker",
    "Sudan strikes displace about 3,000 people",
    "Iraq–Türkiye pipeline oil flows again",
    "China retail +0.4%, output +4.8%, both miss",
    "UnitedHealth −10.2%; Humana −13.0% on rules",
    "India arrests 38 in multi-state cyber crackdown",
    "Odesa strikes kill 4, injure 13 in Ukraine",
    "Germany accuses Russia of banned chemicals",
    "OpenAI launches GPT-6.2 Astra and Sol",
    "Voyager 1 reaches 'light-day' milestone",
    "Word of the year: 'human', Cambridge",
    "Brent $91.95; gold $3,741.90 after sell-off",
]


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead
    d.text((W // 2, 6), "THE WORLD", font=F(SERIF_B, 58), fill=INK,
           anchor="ma")
    d.text((W // 2, 66), "WEDNESDAY, 18 NOVEMBER 2026", font=F(SANS_B, 19),
           fill=RED, anchor="ma")
    d.line([(M, 90), (W - M, 90)], fill=RULE, width=2)
    d.line([(M, 94), (W - M, 94)], fill=RULE, width=1)
    d.text((M, 98), "Vol. I — No. 1", font=F(SANS, 10), fill=GREY)
    d.text((W - M, 98), "WEDNESDAY EDITION", font=F(SANS, 10), fill=GREY,
           anchor="ra")

    # --- hero skyline
    draw_skyline(d, M, 110, W - M, 198)

    # --- lead story
    y = 206
    y = kicker(d, M, y, LEAD["kicker"][0], LEAD["kicker"][1])
    y = draw_wrapped(d, M, y, LEAD["headline"], F(SERIF_B, 34), INK, CW, 37)
    y = draw_wrapped(d, M, y + 4, LEAD["deck"], F(SANS, 14), (40, 40, 40),
                     CW, 17)
    d.text((M, y + 4), LEAD["byline"], font=F(SANS_B, 11), fill=INK)
    y = y + 4 + 13
    d.line([(M, y + 6), (W - M, y + 6)], fill=RULE, width=1)

    # --- row 2: Gulf + Kerch
    y = y + 14
    colw = (CW - 12) // 2
    for i, st in enumerate(ROW2):
        x = M + i * (colw + 12)
        st["art"](d, x, y, x + colw, y + 40)
        yy = kicker(d, x, y + 46, st["kicker"][0], st["kicker"][1])
        yy = draw_wrapped(d, x, yy, st["headline"], F(SERIF_B, 20), INK,
                          colw, 22)
        draw_wrapped(d, x, yy + 2, st["deck"], F(SANS, 12), (40, 40, 40),
                     colw, 14)
    y = y + 40 + 14 + 44 + 30
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)

    # --- 8-panel grid
    y = y + 8
    pw = (CW - 3 * 8) // 4
    for r in range(2):
        for c in range(4):
            st = GRID[r * 4 + c]
            x = M + c * (pw + 8)
            yy = y + r * 116
            st["art"](d, x, yy, x + pw, yy + 34)
            yy2 = kicker(d, x, yy + 38, st["kicker"][0], st["kicker"][1])
            yy2 = draw_wrapped(d, x, yy2, st["headline"], F(SERIF_B, 15),
                               INK, pw, 18)
            draw_wrapped(d, x, yy2 + 1, st["deck"], F(SANS, 10), (40, 40, 40),
                         pw, 12)
    y = y + 2 * 116
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)

    # --- EU + pull-quote
    y = y + 8
    euw = 640
    yy = kicker(d, M, y, EU["kicker"][0], EU["kicker"][1])
    yy = draw_wrapped(d, M, yy, EU["headline"], F(SERIF_B, 19), INK, euw, 22)
    draw_wrapped(d, M, yy + 2, EU["deck"], F(SANS, 12), (40, 40, 40), euw, 14)
    qx = M + euw + 16
    d.text((qx, y - 6), "“", font=F(SERIF_B, 44), fill=RED)
    draw_wrapped(d, qx + 34, y + 4, QUOTE[0], F(SERIF_I, 16), INK,
                 W - M - qx - 34, 19)
    d.text((qx + 34, y + 26), QUOTE[1], font=F(SANS, 10), fill=GREY)
    y = y + 52
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)

    # --- flashpoints
    y = y + 6
    d.text((M, y), "FLASHPOINTS — WEDNESDAY 18 NOVEMBER 2026",
           font=F(SANS_B, 11), fill=RED)
    y = y + 16
    fw = CW // 6
    for i, (name, desc) in enumerate(FLASH):
        fx = M + (i % 6) * fw
        fy = y + (i // 6) * 20
        d.ellipse([fx, fy + 2, fx + 6, fy + 8], fill=RED)
        d.text((fx + 10, fy), name, font=F(SANS_B, 10), fill=INK)
        d.text((fx + 10, fy + 11), desc, font=F(SANS, 9), fill=(60, 60, 60))
    y = y + 42

    # --- By the Numbers (black band)
    d.rectangle([M, y, W - M, y + 40], fill=(12, 12, 12))
    nw = CW // 5
    for i, (num, label) in enumerate(NUMBERS):
        nx = M + i * nw
        d.text((nx + nw // 2, y + 3), num, font=F(SANS_B, 22),
               fill=(255, 255, 255), anchor="ma")
        d.text((nx + nw // 2, y + 27), label, font=F(SANS, 9),
               fill=(200, 200, 200), anchor="ma")
    y = y + 48

    # --- In Brief
    d.text((M, y), "IN BRIEF", font=F(SANS_B, 11), fill=INK)
    y = y + 14
    bw = CW // 3
    for i, item in enumerate(BRIEF):
        bx = M + (i % 3) * bw
        by = y + (i // 3) * 11
        d.rectangle([bx, by + 2, bx + 5, by + 7], fill=RED)
        d.text((bx + 9, by), item, font=F(SANS, 10), fill=(30, 30, 30))
    y = y + 8 * 11 + 6

    # --- footer
    d.text((W // 2, y), "THE WORLD — Wednesday 18 November 2026 • "
           "Every story verified against reporting published on 18 November 2026.",
           font=F(SANS, 9), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)
