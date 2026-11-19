#!/usr/bin/env python3
"""Draw THE WORLD — Wednesday 18 November 2026, a one-page newspaper
front page summing up that day's real world news. Deterministic:
same input always writes identical bytes to entry.png.
All stories are real events reported on Wednesday 18 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
MUTED = (90, 84, 74)
RED = (163, 22, 33)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
RULE = (60, 56, 50)
SKY = (219, 231, 243)
SAND = (239, 227, 200)
GREY = (229, 229, 224)
GREEN = (220, 234, 217)
ROSE = (243, 217, 215)
SEA = (200, 222, 235)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
        "DejaVuSerif.ttf" if serif else \
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def tw(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text, size=11):
    draw.text((x, y), text, font=font(size, bold=True), fill=RED)
    return y + size + 4


def headline(draw, x, y, text, fnt, max_w, lh, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    return draw_lines(draw, x, y, lines, fnt, fill, lh), len(lines)


def deck(draw, x, y, text, size, max_w, lh, fill=(50, 48, 44)):
    fnt = font(size)
    lines = wrap(draw, text, fnt, max_w)
    return draw_lines(draw, x, y, lines, fnt, fill, lh)


def rule(draw, x, y, w, h=1, fill=RULE):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill)


def panel(draw, x, y, w, h, fill):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill)
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=RULE, width=1)


# ---------------------------------------------------------------- illustrations
def ill_skyline(d, x, y, w, h):
    """Shenzhen skyline at dusk: sky, sun, towers, three flags."""
    panel(d, x, y, w, h, SKY)
    d.ellipse([x + w - 70, y + 6, x + w - 34, y + 42], fill=(240, 190, 90))
    towers = [(0.02, 0.10, 0.55), (0.13, 0.08, 0.75), (0.22, 0.12, 0.45),
              (0.35, 0.07, 0.85), (0.43, 0.11, 0.60), (0.55, 0.08, 0.70),
              (0.64, 0.12, 0.50), (0.77, 0.09, 0.65), (0.87, 0.11, 0.42)]
    for fx, fw, fh in towers:
        bx, bw = x + int(w * fx), int(w * fw)
        bh = int(h * fh)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(38, 48, 66))
        for wy in range(y + h - bh + 6, y + h - 4, 12):
            for wx in range(bx + 4, bx + bw - 3, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 220, 130))
    # three small flags on the tallest tower, kept inside the panel
    tower_top = y + h - int(h * 0.85)
    fx = x + int(w * 0.35) + 6
    pole_top = max(y + 2, tower_top - 12)
    d.line([fx, pole_top, fx, tower_top], fill=INK, width=2)
    d.rectangle([fx, pole_top, fx + 16, pole_top + 8], fill=RED)
    d.rectangle([fx + 18, pole_top, fx + 34, pole_top + 8], fill=BLUE)
    d.rectangle([fx + 36, pole_top, fx + 52, pole_top + 8],
                fill=(240, 240, 240))


def ill_gulf(d, x, y, w, h):
    """Strait of Hormuz: sea, tanker, drone dots, smoke."""
    panel(d, x, y, w, h, SEA)
    d.polygon([(x + 8, y + h - 14), (x + 8, y + h - 26), (x + 46, y + h - 26),
               (x + 46, y + h - 14)], fill=(120, 60, 40))
    d.rectangle([x + 20, y + h - 34, x + 30, y + h - 26], fill=(120, 60, 40))
    d.line([x + 24, y + h - 34, x + 24, y + h - 42], fill=INK, width=2)
    for wx in (x + 60, x + 120, x + 180, x + 240, x + 300):
        d.line([wx, y + h - 8, wx + 26, y + h - 8], fill=(255, 255, 255), width=2)
    for dx, dy in [(0.55, 0.25), (0.68, 0.45), (0.82, 0.2)]:
        cx, cy = x + int(w * dx), y + int(h * dy)
        d.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=INK)
        d.line([cx - 8, cy, cx + 8, cy], fill=INK, width=1)
    d.ellipse([x + int(w * 0.55) - 12, y + 4, x + int(w * 0.55) + 4, y + 16],
              fill=(150, 150, 150))


def ill_bridge(d, x, y, w, h):
    """Kerch Bridge: two arches, one span broken, water below."""
    panel(d, x, y, w, h, SKY)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 160, 190))
    mid = x + w // 2
    d.arc([x + 10, y + 8, mid - 6, y + h - 10], 180, 360, fill=INK, width=4)
    d.arc([mid + 6, y + 8, x + w - 10, y + h - 10], 180, 360, fill=INK, width=4)
    d.line([x + 8, y + h - 26, mid - 30, y + h - 26], fill=INK, width=4)
    d.line([mid - 30, y + h - 26, mid - 18, y + h - 12], fill=INK, width=4)
    d.line([mid + 30, y + h - 26, x + w - 8, y + h - 26], fill=INK, width=4)
    d.ellipse([mid - 4, y + 6, mid + 12, y + 18], fill=(150, 150, 150))
    for sx in (x + 30, x + 90, mid + 60, x + w - 40):
        d.line([sx, y + h - 26, sx, y + h - 20], fill=INK, width=3)


def ill_ballot(d, x, y, w, h):
    panel(d, x, y, w, h, SAND)
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 26, cy - 22, cx + 26, cy + 22], fill=GOLD)
    d.polygon([(cx, cy - 14), (cx + 4, cy - 4), (cx + 15, cy - 4),
               (cx + 6, cy + 3), (cx + 9, cy + 14), (cx, cy + 7),
               (cx - 9, cy + 14), (cx - 6, cy + 3), (cx - 15, cy - 4),
               (cx - 4, cy - 4)], fill=(255, 255, 255))


def ill_chip(d, x, y, w, h):
    panel(d, x, y, w, h, (222, 226, 238))
    cx, cy = x + w // 2, y + h // 2
    for px in (cx - 34, cx - 12, cx + 12):
        d.line([px, cy - 22, px, cy - 32], fill=INK, width=2)
        d.line([px, cy + 22, px, cy + 32], fill=INK, width=2)
    for py in (cy - 16, cy + 16):
        d.line([cx - 40, py, cx - 50, py], fill=INK, width=2)
        d.line([cx + 40, py, cx + 50, py], fill=INK, width=2)
    d.rectangle([cx - 34, cy - 22, cx + 34, cy + 22], fill=(30, 60, 40))
    d.rectangle([cx - 16, cy - 10, cx + 16, cy + 10], fill=(90, 200, 120))
    d.text((cx - 9, cy - 7), "AI", font=font(11, bold=True), fill=INK)


def ill_tent(d, x, y, w, h):
    panel(d, x, y, w, h, SAND)
    cx, cy = x + w // 2, y + h // 2 + 4
    d.polygon([(cx - 40, cy + 16), (cx, cy - 18), (cx + 40, cy + 16)],
              fill=(200, 170, 120))
    d.polygon([(cx - 8, cy + 16), (cx, cy - 2), (cx + 8, cy + 16)],
              fill=(90, 70, 50))
    for rx, ry in [(0.2, 0.2), (0.35, 0.12), (0.65, 0.25), (0.8, 0.15)]:
        d.line([x + int(w * rx), y + int(h * ry), x + int(w * rx) - 4,
                y + int(h * ry) + 8], fill=BLUE, width=2)


def ill_virus(d, x, y, w, h):
    panel(d, x, y, w, h, ROSE)
    cx, cy = x + w // 2, y + h // 2
    for ang in range(0, 360, 45):
        import math
        x1 = cx + int(16 * math.cos(math.radians(ang)))
        y1 = cy + int(16 * math.sin(math.radians(ang)))
        x2 = cx + int(24 * math.cos(math.radians(ang)))
        y2 = cy + int(24 * math.sin(math.radians(ang)))
        d.line([x1, y1, x2, y2], fill=RED, width=2)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=RED)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=RED)
    d.ellipse([cx - 6, cy - 6, cx + 2, cy + 2], fill=(255, 255, 255))
    for px, py in [(0.2, 0.7), (0.8, 0.65), (0.75, 0.25)]:
        d.ellipse([x + int(w * px) - 5, y + int(h * py) - 5,
                   x + int(w * px) + 5, y + int(h * py) + 5], fill=RED)


def ill_shield(d, x, y, w, h):
    panel(d, x, y, w, h, (222, 234, 220))
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx - 22, cy - 18), (cx + 22, cy - 18), (cx + 22, cy + 2),
               (cx, cy + 24), (cx - 22, cy + 2)], fill=TEAL)
    d.rectangle([cx - 3, cy - 10, cx + 3, cy + 8], fill=(255, 255, 255))
    d.rectangle([cx - 10, cy - 3, cx + 10, cy + 3], fill=(255, 255, 255))


def ill_nodes(d, x, y, w, h):
    panel(d, x, y, w, h, (222, 226, 238))
    pts = [(0.2, 0.3), (0.45, 0.65), (0.7, 0.25), (0.85, 0.7), (0.5, 0.35)]
    xy = [(x + int(w * px), y + int(h * py)) for px, py in pts]
    for i in range(len(xy)):
        for j in range(i + 1, len(xy)):
            d.line([xy[i], xy[j]], fill=(120, 130, 160), width=1)
    for cx, cy in xy:
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=BLUE)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def ill_chart(d, x, y, w, h):
    panel(d, x, y, w, h, (232, 228, 220))
    base = y + h - 10
    candles = [(0.1, 0.5, 0.7), (0.25, 0.35, 0.6), (0.4, 0.55, 0.75),
               (0.55, 0.3, 0.5), (0.7, 0.45, 0.65), (0.85, 0.2, 0.4)]
    for fx, flo, fhi in candles:
        cx = x + int(w * fx)
        top = y + int(h * (1 - fhi))
        bot = y + int(h * (1 - flo))
        d.line([cx, top - 6, cx, bot + 6], fill=INK, width=1)
        d.rectangle([cx - 6, top, cx + 6, bot], fill=RED)
    d.line([x + 8, base, x + w - 8, base], fill=INK, width=2)
    d.line([x + 10, y + 8, x + w - 30, y + h - 22], fill=BLUE, width=2)


def ill_globe(d, x, y, w, h):
    panel(d, x, y, w, h, GREEN)
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=TEAL)
    d.arc([cx - 20, cy - 20, cx + 20, cy + 20], 200, 340, fill=(255, 255, 255),
          width=2)
    d.line([cx - 20, cy, cx + 20, cy], fill=(255, 255, 255), width=2)
    d.ellipse([cx - 20, cy - 20, cx - 6, cy - 6], fill=(120, 200, 140))
    d.ellipse([cx + 4, cy + 6, cx + 18, cy + 18], fill=(120, 200, 140))
    d.polygon([(cx + 26, cy + 8), (cx + 34, cy - 4), (cx + 30, cy + 12)],
              fill=(40, 140, 60))


# ------------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28                      # side margin
    CW = W - 2 * M              # 968 content width

    # ---- masthead ------------------------------------------------------
    rule(d, M, 10, CW, 2)
    name = "THE WORLD"
    nf = font(58, bold=True, serif=True)
    d.text(((W - tw(d, name, nf)) / 2, 16), name, font=nf, fill=INK)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    df = font(19, bold=True)
    d.text(((W - tw(d, date, df)) / 2, 82), date, font=df, fill=INK)
    sf = font(11)
    d.text((M, 106), "Vol. I — No. 1", font=sf, fill=MUTED)
    right = "WEDNESDAY EDITION"
    d.text((W - M - tw(d, right, sf), 106), right, font=sf, fill=MUTED)
    rule(d, M, 122, CW, 3)
    rule(d, M, 127, CW, 1)

    # ---- lead row: y 136..336 ------------------------------------------
    y0 = 136
    LX, LW = M, 616
    RX, RW = M + 632, 336
    y = kicker(d, LX, y0, "THE SUMMIT — SHENZHEN, CHINA", 12)
    y, _ = headline(d, LX, y, "Trump, Xi and Putin to hold first "
                    "three-way summit in Shenzhen",
                    font(31, bold=True, serif=True), LW, 37)
    y = deck(d, LX, y + 4,
             "Xi Jinping and Vladimir Putin met in Shenzhen on Wednesday, a day "
             "before their planned trilateral with Donald Trump on the sidelines "
             "of the APEC summit — the first meeting of all three leaders.",
             13, LW, 17)
    d.text((LX, y + 2), "By THE WORLD STAFF — SHENZHEN",
           font=font(10, bold=True), fill=MUTED)
    ill_skyline(d, LX, 296, LW, 40)

    # right column: Gulf, then Kerch
    y = kicker(d, RX, y0, "THE GULF — KUWAIT CITY", 11)
    y, _ = headline(d, RX, y, "Iran strikes Kuwait and Bahrain",
                    font(18, bold=True, serif=True), RW, 22)
    y = deck(d, RX, y + 2,
             "Iran fired drones at a US base in Kuwait and sites in Bahrain "
             "after US jets hit Qeshm Island.",
             11, RW, 14)
    ill_gulf(d, RX, y + 4, RW, 30)
    y = kicker(d, RX, 241, "UKRAINE — KERCH", 11)
    y, _ = headline(d, RX, y, "Kerch Bridge hit again",
                    font(18, bold=True, serif=True), RW, 22)
    y = deck(d, RX, y + 2,
             "Ukraine struck the bridge to Crimea for a second day; part of "
             "the road span collapsed into the strait.",
             11, RW, 14)
    ill_bridge(d, RX, y + 4, RW, 24)
    rule(d, M, 340, CW, 1)

    # ---- rows of four --------------------------------------------------
    def four_row(y_top, items):
        col_w = (CW - 3 * 14) // 4
        for i, (kick, head, text, ill) in enumerate(items):
            cx = M + i * (col_w + 14)
            ill(d, cx, y_top, col_w, 48)
            yy = kicker(d, cx, y_top + 52, kick, 10)
            yy, _ = headline(d, cx, yy, head, font(15, bold=True, serif=True),
                             col_w, 19)
            deck(d, cx, yy + 2, text, 11, col_w, 14)
        return y_top + 136

    y = four_row(348, [
        ("WASHINGTON — ALASKA", "Democrats take the Senate, 56–44",
         "Mary Peltola defeats Dan Sullivan in Alaska, flipping the chamber.",
         ill_ballot),
        ("TECH — SANTA CLARA", "Nvidia revenue doubles to $115.8B",
         "Board rules out bringing back Jensen Huang; Colette Kress stays "
         "interim chief.", ill_chip),
        ("GAZA — GAZA CITY", "Israel opens new ground operation",
         "Troops push into Hamas-held central Gaza in the first broad "
         "offensive in a year.", ill_tent),
        ("HEALTH — DR CONGO", "Ebola passes 11,000 cases",
         "Three in four children under five infected do not survive, health "
         "officials say.", ill_virus),
    ])
    rule(d, M, y + 2, CW, 1)
    y = four_row(y + 10, [
        ("HEALTH — WASHINGTON", "US loses measles-free status",
         "Elimination status held for 26 years ends after 5,400 cases and "
         "10 deaths.", ill_shield),
        ("TECH — SAN FRANCISCO", "Anthropic raises $81.3B in record IPO",
         "The largest stock offering on record prices as AI demand stays "
         "hot.", ill_nodes),
        ("MARKETS — NEW YORK", "Fed minutes sink stocks; gold dives",
         "Dow falls 1.1% for a third day; S&P 500 slips below its 200-day "
         "average.", ill_chart),
        ("CLIMATE — ANTALYA", "Climate talks deadlocked at COP31",
         "75 nations back Türkiye’s electrification target as finance splits "
         "the room.", ill_globe),
    ])
    # ---- EU loan band + pull-quote --------------------------------------
    rule(d, M, y + 2, CW, 1)
    yy = 640
    kicker(d, M, yy, "EUROPE — BRUSSELS", 10)
    yy, _ = headline(d, M, yy + 15, "EU proposes €45B loan to Ukraine for 2027",
                     font(17, bold=True, serif=True), 600, 21)
    deck(d, M, yy + 2,
         "The loan would be repaid after Russia pays reparations, the "
         "Commission says.", 12, 600, 15)
    qx, qw = M + 632, 336
    d.rectangle([qx, 640, qx + qw - 1, 688], outline=RULE, width=1)
    d.rectangle([qx, 640, qx + 4, 688], fill=RED)
    d.text((qx + 14, 648), "“An unprecedented operation.”",
           font=font(14, serif=True), fill=INK)
    d.text((qx + 14, 670), "— Volodymyr Zelenskyy, on the Kerch Bridge strike",
           font=font(10), fill=MUTED)

    # ---- flashpoints ------------------------------------------------------
    d.text((M, 698), "FLASHPOINTS — WEDNESDAY 18 NOVEMBER 2026",
           font=font(12, bold=True), fill=RED)
    rule(d, M, 714, CW, 1)
    flash = [
        ("SHENZHEN", "Three-way summit set"),
        ("MANILA", "Quad meets at leader level"),
        ("HORMUZ", "Tanker hit by projectile"),
        ("KUWAIT", "Drones target US base"),
        ("BAHRAIN", "Attacks intercepted"),
        ("QESHM", "US hit missile site"),
        ("KERCH", "Bridge span collapses"),
        ("KYIV", "141 drones; 126 downed"),
        ("GAZA", "Ground operation opens"),
        ("ANTALYA", "COP31 deadlocked"),
        ("ALASKA", "Senate flips 56–44"),
        ("SIBERIA", "Military plane crash, 19 dead"),
    ]
    chip_w = (CW - 5 * 10) // 6
    for i, (place, line) in enumerate(flash):
        cx = M + (i % 6) * (chip_w + 10)
        cy = 720 + (i // 6) * 40
        d.rectangle([cx, cy, cx + chip_w - 1, cy + 35], fill=(255, 255, 255),
                    outline=RULE, width=1)
        d.ellipse([cx + 8, cy + 9, cx + 15, cy + 16], fill=RED)
        d.text((cx + 20, cy + 5), place, font=font(11, bold=True), fill=INK)
        d.text((cx + 8, cy + 20), line, font=font(9), fill=MUTED)

    # ---- by the numbers ---------------------------------------------------
    d.rectangle([M, 800, M + CW - 1, 844], fill=INK)
    stats = [
        ("3", "leaders at the Shenzhen table"),
        ("141", "drones over Ukraine; 126 downed"),
        ("56–44", "Democrats take the Senate"),
        ("11,000", "Ebola cases in DR Congo"),
        ("$115.8B", "Nvidia quarterly revenue"),
    ]
    stat_w = CW // 5
    for i, (num, label) in enumerate(stats):
        sx = M + i * stat_w + 10
        d.text((sx, 806), num, font=font(20, bold=True, serif=True),
               fill=(247, 242, 231))
        d.text((sx, 830), label, font=font(10), fill=(200, 194, 182))

    # ---- in brief ---------------------------------------------------------
    d.text((M, 852), "IN BRIEF", font=font(12, bold=True), fill=RED)
    rule(d, M, 868, CW, 1)
    brief = [
        "Canada, China cut tariffs after Carney–Xi talks",
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
        "Iraq–Türkiye pipeline oil flows again",
        "China retail +0.4%, output +4.8%; both miss",
        "UnitedHealth −10.2%; Humana −13.0% on rules",
        "India arrests 38 in multi-state cyber crackdown",
        "Odesa strikes kill 4, injure 13 in Ukraine",
        "Germany accuses Russia of banned chemicals",
        "OpenAI launches GPT-6.2 Astra and Sol",
        "Voyager 1 reaches ‘light-day’ milestone",
        "Word of the year: ‘human’, says Cambridge",
        "Brent $91.95; gold $3,741.90 after sell-off",
    ]
    col_w = (CW - 2 * 16) // 3
    bf = font(11)
    for i, item in enumerate(brief):
        bx = M + (i % 3) * (col_w + 16)
        by = 874 + (i // 3) * 17
        d.text((bx, by), "▪ " + item, font=bf, fill=INK)

    # ---- footer -----------------------------------------------------------
    foot = ("THE WORLD — Wednesday 18 November 2026 • Every story verified "
            "against reporting published on 18 November 2026.")
    ff = font(9)
    d.text(((W - tw(d, foot, ff)) / 2, 1012), foot, font=ff, fill=MUTED)
    return img, d, y


def main():
    img, d, y = build()
    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
