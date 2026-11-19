#!/usr/bin/env python3
"""THE WORLD — Wednesday, 18 November 2026. Fresh front-page poster, v2.
Design-only revision: bigger hero art, bolder hierarchy, richer illustrations,
stronger contrast. Same 36 verified stories as v1. Deterministic output.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # margin
CW = W - 2 * M              # content width = 976
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (163, 18, 30)
DARKRED = (122, 10, 22)
NAVY = (24, 42, 84)
BLUE = (27, 79, 156)
GREEN = (30, 122, 52)
TEAL = (14, 122, 107)
ORANGE = (176, 92, 8)
GREY = (90, 86, 76)
LIGHTGREY = (210, 204, 188)
GOLD = (198, 148, 28)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS_O = FD + "DejaVuSans-Oblique.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, width, leading):
    """Draw wrapped paragraph; return y after last line."""
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color, size=12):
    """Colour-coded section label: small square + bold caps text."""
    f = F(SANS_B, size)
    d.rectangle([x, y + 2, x + 9, y + 11], fill=color)
    d.text((x + 14, y), text, font=f, fill=color)
    return y + size + 2


def rule(d, x0, x1, y, fill=INK, w=1):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)


def centre(d, cx, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


# ---------------- art helpers ----------------

def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def skyline(d, box, base_y, colour, seed):
    """Deterministic building silhouettes with lit windows."""
    x0, y0, x1, y1 = box
    rng = random.Random(seed)
    x = x0
    while x < x1:
        bw = rng.randint(26, 54)
        bh = rng.randint(28, int((y1 - y0) * 0.85))
        d.rectangle([x, base_y - bh, min(x + bw, x1), base_y], fill=colour)
        for wy in range(base_y - bh + 6, base_y - 4, 9):
            for wx in range(x + 4, min(x + bw, x1) - 4, 9):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        x += bw + 3


def hero_art(d, box):
    """Dramatic Shenzhen dusk: gradient sky, skyline, summit table, 3 flags."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (58, 32, 86), (232, 106, 44))
    # low sun + glow
    cx, cy = x0 + int((x1 - x0) * 0.72), y0 + 52
    for r, c in ((46, (255, 170, 80)), (34, (255, 196, 110)), (22, (255, 224, 150))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    skyline(d, (x0, y0 + 34, x1, y1 - 26), y1 - 26, (30, 24, 54), 7)
    # ground + table glow
    d.rectangle([x0, y1 - 26, x1, y1], fill=(24, 18, 44))
    d.ellipse([x0 + 300, y1 - 44, x1 - 300, y1 - 6], fill=(255, 190, 90))
    # summit table
    tx0, tx1, ty = x0 + 380, x1 - 380, y1 - 34
    d.rectangle([tx0, ty, tx1, ty + 12], fill=(16, 12, 30))
    d.rectangle([tx0 + 8, ty + 12, tx1 - 8, y1 - 2], fill=(16, 12, 30))
    # three seated figures
    for fx in (tx0 + 52, (tx0 + tx1) // 2, tx1 - 52):
        d.ellipse([fx - 9, ty - 26, fx + 9, ty - 8], fill=(12, 10, 24))
        d.polygon([(fx - 16, ty - 8), (fx + 16, ty - 8), (fx + 11, ty + 2),
                   (fx - 11, ty + 2)], fill=(12, 10, 24))
    # three flags on poles above the table
    flags = [("us", tx0 + 30), ("cn", (tx0 + tx1) // 2), ("ru", tx1 - 30)]
    for kind, fx in flags:
        d.rectangle([fx, y0 + 44, fx + 2, ty - 26], fill=(220, 220, 210))
        fy = y0 + 44
        if kind == "us":
            for i in range(7):
                c = (178, 34, 52) if i % 2 == 0 else (240, 240, 235)
                d.rectangle([fx + 2, fy + i * 3, fx + 30, fy + i * 3 + 3], fill=c)
            d.rectangle([fx + 2, fy, fx + 14, fy + 9], fill=(30, 50, 110))
        elif kind == "cn":
            d.rectangle([fx + 2, fy, fx + 30, fy + 21], fill=(206, 32, 40))
            d.text((fx + 6, fy + 4), "*", font=F(SANS_B, 13), fill=(255, 222, 80))
        else:
            for i, c in enumerate(((240, 240, 235), (0, 90, 180), (200, 30, 40))):
                d.rectangle([fx + 2, fy + i * 7, fx + 30, fy + i * 7 + 7], fill=c)
    d.rectangle([x0, y0, x1, y0], fill=INK)


def sea_art(d, box):
    """Gulf: dusk sea, drone dots, explosion burst."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (64, 84, 130), (150, 180, 210))
    d.rectangle([x0, y0 + int((y1 - y0) * 0.55), x1, y1], fill=(36, 64, 110))
    for i, wx in enumerate(range(x0 + 14, x1 - 14, 34)):
        wy = y0 + int((y1 - y0) * 0.55) + (i % 3) * 4
        d.line([(wx, wy), (wx + 18, wy)], fill=(190, 215, 235), width=2)
    # explosion burst right
    bx, by = x1 - 52, y0 + 16
    for r, c in ((15, (255, 140, 40)), (10, (255, 190, 80)), (5, (255, 240, 160))):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=c)
    for dx, dy in ((-26, 6), (-18, -8), (8, -14)):
        d.ellipse([bx + dx - 3, by + dy - 3, bx + dx + 3, by + dy + 3], fill=(40, 40, 40))


def bridge_art(d, box):
    """Kerch: strait water, bridge with collapsed span, smoke."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (150, 175, 205), (210, 225, 235))
    d.rectangle([x0, y0 + 26, x1, y1], fill=(52, 96, 140))
    d.rectangle([x0, y0 + 14, x1, y0 + 20], fill=(30, 30, 34))
    d.rectangle([x0, y0 + 14, (x0 + x1) // 2 - 26, y0 + 20], fill=(30, 30, 34))
    d.polygon([((x0 + x1) // 2 - 26, y0 + 20), ((x0 + x1) // 2 + 4, y0 + 38),
               ((x0 + x1) // 2 + 18, y0 + 20)], fill=(30, 30, 34))
    for px in range(x0 + 8, x1 - 8, 16):
        d.rectangle([px, y0 + 8, px + 3, y0 + 14], fill=(30, 30, 34))
    for sx, sy, sr in (((x0 + x1) // 2 + 6, y0 + 8, 7), ((x0 + x1) // 2 + 18, y0 + 2, 5)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))


def capitol_art(d, box):
    """Senate: deep blue, capitol dome silhouette, stars."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(28, 48, 96))
    mx = (x0 + x1) // 2
    d.rectangle([mx - 46, y1 - 14, mx + 46, y1 - 6], fill=(245, 245, 240))
    d.rectangle([mx - 30, y1 - 26, mx + 30, y1 - 14], fill=(245, 245, 240))
    d.pieslice([mx - 18, y1 - 44, mx + 18, y1 - 12], 180, 360, fill=(245, 245, 240))
    d.rectangle([mx - 2, y1 - 52, mx + 2, y1 - 42], fill=(245, 245, 240))
    for sx, sy in ((x0 + 18, y0 + 8), (x1 - 26, y0 + 12), (x0 + 40, y0 + 20)):
        d.text((sx, sy), "*", font=F(SANS_B, 12), fill=(255, 214, 120))


def chip_art(d, box):
    """Nvidia: dark green, chip with AI label, circuit traces."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(12, 60, 38))
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    for ex, ey in ((x0 + 8, my - 12), (x0 + 8, my + 12), (x1 - 8, my - 12), (x1 - 8, my + 12)):
        d.line([(ex, ey), (mx - 16 if ex < mx else mx + 16, ey)], fill=(90, 200, 140), width=2)
    d.rectangle([mx - 16, my - 14, mx + 16, my + 14], fill=(8, 40, 26),
                outline=(120, 220, 160), width=2)
    d.text((mx - 9, my - 9), "AI", font=F(SANS_B, 13), fill=(140, 230, 170))


def desert_art(d, box):
    """Gaza: warm dunes + sun."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (250, 214, 150), (232, 176, 96))
    d.ellipse([x1 - 34, y0 + 4, x1 - 10, y0 + 28], fill=(255, 236, 170))
    d.polygon([(x0, y1), (x0, y1 - 18), (x0 + 90, y1 - 26), (x1, y1 - 8), (x1, y1)],
              fill=(206, 150, 74))
    d.polygon([(x0, y1), (x0, y1 - 8), (x0 + 120, y1 - 14), (x1, y1 - 2), (x1, y1)],
              fill=(188, 132, 60))


def virus_art(d, box):
    """Ebola: pink field, red spiky virus circles."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(246, 214, 214))
    for vx, vy, vr in (((x0 + x1) // 2, (y0 + y1) // 2, 12), (x0 + 26, y0 + 12, 7),
                       (x1 - 26, y1 - 12, 7)):
        for a in range(0, 360, 45):
            import math
            ex = vx + int(vr * 1.5 * math.cos(math.radians(a)))
            ey = vy + int(vr * 1.5 * math.sin(math.radians(a)))
            d.line([(vx, vy), (ex, ey)], fill=(190, 30, 40), width=2)
        d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(190, 30, 40))
        d.ellipse([vx - 4, vy - 4, vx + 4, vy + 4], fill=(120, 10, 20))


def shield_art(d, box):
    """Measles: pale green, shield + white cross."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 236, 214))
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(mx - 14, my - 14), (mx + 14, my - 14), (mx + 14, my + 2),
               (mx, my + 16), (mx - 14, my + 2)], fill=(24, 130, 60))
    d.rectangle([mx - 2, my - 8, mx + 2, my + 8], fill=(255, 255, 255))
    d.rectangle([mx - 7, my - 3, mx + 7, my + 1], fill=(255, 255, 255))


def network_art(d, box):
    """Anthropic: light blue, network nodes."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 246))
    pts = [(x0 + 16, y0 + 10), (x0 + 60, y0 + 26), (x1 - 40, y0 + 8),
           (x0 + 30, y1 - 12), (x1 - 18, y1 - 10), ((x0 + x1) // 2, (y0 + y1) // 2)]
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            d.line([p, q], fill=(120, 150, 200), width=1)
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(27, 79, 156))


def chart_art(d, box):
    """Fed/markets: white, red candlesticks falling."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 255, 255))
    d.line([(x0 + 4, y1 - 8), (x1 - 4, y1 - 8)], fill=(150, 150, 150), width=1)
    xs = [x0 + 12 + i * 20 for i in range(8)]
    tops = [y0 + 8, y0 + 12, y0 + 14, y0 + 18, y0 + 20, y0 + 24, y0 + 26, y0 + 30]
    for x, t in zip(xs, tops):
        d.line([(x + 5, t - 4), (x + 5, t + 16)], fill=(190, 30, 40), width=1)
        d.rectangle([x, t, x + 10, t + 12], fill=(190, 30, 40))
    d.line([(x0 + 8, y0 + 6), (x1 - 8, y0 + 34)], fill=(30, 30, 30), width=2)


def globe_art(d, box):
    """COP31: teal, globe + leaf."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(206, 232, 224))
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([mx - 15, my - 15, mx + 15, my + 15], fill=(46, 140, 90))
    d.ellipse([mx - 15, my - 15, mx + 2, my + 2], fill=(120, 200, 140))
    d.ellipse([mx + 4, my + 6, mx + 14, my + 14], fill=(120, 200, 140))
    d.polygon([(x1 - 24, y0 + 6), (x1 - 8, y0 + 6), (x1 - 8, y0 + 18)],
              fill=(30, 122, 52))


# ---------------- page assembly ----------------

def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    centre(d, W // 2, 6, "THE WORLD", F(SERIF_B, 52), INK)
    centre(d, W // 2, 66, "WEDNESDAY, 18 NOVEMBER 2026", F(SANS_B, 20), DARKRED)
    rule(d, M, W - M, 90, INK, 3)
    rule(d, M, W - M, 95, INK, 1)
    d.text((M, 99), "Vol. I \u2014 No. 1", font=F(SANS, 10), fill=GREY)
    vr = "WEDNESDAY EDITION"
    d.text((W - M - d.textlength(vr, font=F(SANS, 10)), 99), vr,
           font=F(SANS, 10), fill=GREY)

    # ---- hero art + lead story ----
    hero_art(d, (M, 112, W - M, 216))
    kicker(d, M, 222, "THE SUMMIT \u2014 SHENZHEN, CHINA", RED, 13)
    para(d, M, 240, "Trump, Xi and Putin to hold first three-way summit in Shenzhen",
         F(SERIF_B, 36), INK, CW, 37)
    para(d, M, 314, "Xi Jinping and Vladimir Putin met in Shenzhen on Wednesday, a day "
         "before their planned trilateral with Donald Trump on the sidelines of the "
         "APEC summit \u2014 the first meeting of all three leaders.",
         F(SANS, 14), (40, 40, 40), CW, 16)
    d.text((M, 348), "By THE WORLD STAFF \u2014 SHENZHEN", font=F(SANS_B, 11), fill=GREY)
    rule(d, M, W - M, 362, INK, 2)

    # ---- second row: Gulf + Kerch ----
    colw = (CW - 16) // 2
    row2 = [
        ("THE GULF \u2014 KUWAIT CITY", RED, "Iran strikes Kuwait and Bahrain",
         "Iran fired drones at a US base in Kuwait and sites in Bahrain after "
         "US jets hit Qeshm Island.", sea_art),
        ("UKRAINE \u2014 KERCH", RED, "Kerch Bridge hit again",
         "Ukraine struck the bridge to Crimea for a second day; part of the road "
         "span collapsed into the strait.", bridge_art),
    ]
    for i, (kick, col, head, deck, art) in enumerate(row2):
        x = M + i * (colw + 16)
        art(d, (x, 368, x + colw, 412))
        kicker(d, x, 418, kick, col, 12)
        para(d, x, 436, head, F(SERIF_B, 19), INK, colw, 20)
        para(d, x, 462, deck, F(SANS, 12), (40, 40, 40), colw, 13)
    rule(d, M, W - M, 506, INK, 1)
    return img, d


def draw_grid(d):
    """8 illustrated stories, 4 columns x 2 rows, colour-coded kickers."""
    gw = (CW - 3 * 10) // 4   # 236
    stories = [
        ("WASHINGTON \u2014 ALASKA", RED, "Democrats take the Senate, 56\u201344",
         "Mary Peltola defeats Dan Sullivan in Alaska, flipping the chamber.",
         capitol_art),
        ("TECH \u2014 SANTA CLARA", BLUE, "Nvidia revenue doubles to $115.8B",
         "Board rules out bringing back Jensen Huang; Colette Kress stays interim chief.",
         chip_art),
        ("GAZA \u2014 GAZA CITY", DARKRED, "Israel opens new ground operation",
         "Troops push into Hamas-held central Gaza in the first broad offensive in a year.",
         desert_art),
        ("HEALTH \u2014 DR CONGO", GREEN, "Ebola passes 11,000 cases",
         "Three in four children under five infected do not survive, health officials say.",
         virus_art),
        ("HEALTH \u2014 WASHINGTON", GREEN, "US loses measles-free status",
         "Elimination status held for 26 years ends after 5,400 cases and 10 deaths.",
         shield_art),
        ("TECH \u2014 SAN FRANCISCO", BLUE, "Anthropic raises $81.3B in record IPO",
         "The largest stock offering on record prices as AI demand stays hot.",
         network_art),
        ("MARKETS \u2014 NEW YORK", ORANGE, "Fed minutes sink stocks; gold dives",
         "Dow falls 1.1% for a third day; S&P 500 slips below its 200-day average.",
         chart_art),
        ("CLIMATE \u2014 ANTALYA", TEAL, "Climate talks deadlocked at COP31",
         "75 nations back T\u00fcrkiye\u2019s electrification target as finance splits the room.",
         globe_art),
    ]
    for idx, (kick, col, head, deck, art) in enumerate(stories):
        r, c = divmod(idx, 4)
        x = M + c * (gw + 10)
        y = 516 + r * 113
        art(d, (x, y, x + gw, y + 32))
        kicker(d, x, y + 36, kick, col, 11)
        para(d, x, y + 49, head, F(SERIF_B, 15), INK, gw, 16)
        para(d, x, y + 83, deck, F(SANS, 11), (40, 40, 40), gw, 12)


def draw_eu_quote(d):
    """EU loan band (left) + big pull-quote treatment (right)."""
    y = 742
    kicker(d, M, y, "EUROPE \u2014 BRUSSELS", NAVY, 12)
    d.text((M, y + 16), "EU proposes \u20ac45B loan to Ukraine for 2027",
           font=F(SERIF_B, 17), fill=INK)
    d.text((M, y + 38), "The loan would be repaid after Russia pays reparations, "
           "the Commission says.", font=F(SANS, 11), fill=(40, 40, 40))
    d.rectangle([632, y, 633, y + 42], fill=LIGHTGREY)  # vertical divider
    d.text((648, y - 6), "\u201c", font=F(SERIF_B, 44), fill=RED)
    d.text((686, y + 6), "An unprecedented operation.",
           font=F(SERIF, 17), fill=INK)
    d.text((686, y + 28), "\u2014 Volodymyr Zelenskyy, on the Kerch Bridge strike",
           font=F(SANS, 10), fill=GREY)


def draw_flashpoints(d):
    d.text((M, 792), "FLASHPOINTS \u2014 WEDNESDAY 18 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=RED)
    cells = [
        ("SHENZHEN", "Three-way summit set"), ("MANILA", "Quad summit at leader level"),
        ("HORMUZ", "Tanker hit by projectile"), ("KUWAIT", "Drones target US base"),
        ("BAHRAIN", "Attacks intercepted"), ("QESHM", "US hit missile site"),
        ("KERCH", "Bridge span collapses"), ("KYIV", "141 drones; 126 downed"),
        ("GAZA", "Ground operation opens"), ("ANTALYA", "COP31 deadlocked"),
        ("ALASKA", "Senate flips 56\u201344"), ("SIBERIA", "Military plane crash, 19 dead"),
    ]
    cw = (CW - 5 * 8) // 6
    for i, (name, note) in enumerate(cells):
        r, c = divmod(i, 6)
        x = M + c * (cw + 8)
        y = 807 + r * 22
        d.ellipse([x, y + 2, x + 7, y + 9], fill=RED)
        d.text((x + 11, y), name, font=F(SANS_B, 11), fill=INK)
        d.text((x + 11, y + 12), note, font=F(SANS, 9), fill=GREY)


def draw_numbers(d):
    d.rectangle([M, 855, W - M, 891], fill=(12, 12, 12))
    stats = [
        ("3", "leaders at the Shenzhen table"),
        ("141", "drones over Ukraine; 126 downed"),
        ("56\u201344", "Democrats take the Senate"),
        ("11,000", "Ebola cases in DR Congo"),
        ("$115.8B", "Nvidia quarterly revenue"),
    ]
    cw = CW // 5
    for i, (num, label) in enumerate(stats):
        cx = M + i * cw + cw // 2
        centre(d, cx, 858, num, F(SERIF_B, 20), (255, 255, 255))
        centre(d, cx, 880, label, F(SANS, 9), (200, 200, 195))


def draw_brief(d):
    d.text((M, 897), "IN BRIEF", font=F(SANS_B, 12), fill=INK)
    rule(d, M, W - M, 909, INK, 1)
    items = [
        "Canada, China cut tariffs after Carney\u2013Xi talks",
        "UK sanctions 8 firms over West Bank settlements",
        "Saudi coalition hits 60 Houthi military sites",
        "950,000 displaced Gazans on flood-prone ground",
        "Russian jets buzz Taiwan; enter Japan airspace",
        "EU clears signature of Indonesia trade deal",
        "UK inflation at 1-year high; price cap +26% in Jan",
        "Ghana beats USA; Amputee World Cup quarterfinal",
        "Lookman out for rest of 2026 with knee injury",
        "Khel.ai launches cloud-based cricket DRS",
        "Max Tang, 16, takes bronze at Oceanman final",
        "Modi meets Prince and Princess of Wales",
        "Knesset elects Matan Kahana as speaker",
        "Sudan strikes displace about 3,000 people",
        "Iraq\u2013T\u00fcrkiye pipeline oil flows again",
        "China retail +0.4%, output +4.8%; both miss",
        "UnitedHealth \u221210.2%; Humana \u221213.0% on rules",
        "India arrests 38 in multi-state cyber crackdown",
        "Odesa strikes kill 4, injure 13 in Ukraine",
        "Germany accuses Russia of banned chemicals",
        "OpenAI launches GPT-6.2 Astra and Sol",
        "Voyager 1 reaches \u2018light-day\u2019 milestone",
        "Word of the year: \u2018human\u2019, Cambridge",
        "Brent $91.95; gold $3,741.90 after sell-off",
    ]
    colw = (CW - 20) // 3
    f = F(SANS, 11)
    for i, item in enumerate(items):
        c, r = divmod(i, 8)
        x = M + c * (colw + 10)
        y = 913 + r * 12
        d.rectangle([x, y + 3, x + 5, y + 8], fill=RED)
        d.text((x + 10, y), item, font=f, fill=(30, 30, 30))
    foot = ("THE WORLD \u2014 Wednesday 18 November 2026 \u2022 Every story verified "
            "against reporting published on 18 November 2026.")
    centre(d, W // 2, 1013, foot, F(SANS, 9), GREY)


def main():
    img, d = draw_page()
    draw_grid(d)
    draw_eu_quote(d)
    draw_flashpoints(d)
    draw_numbers(d)
    draw_brief(d)
    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
