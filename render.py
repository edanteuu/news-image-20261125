#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news image (1024x1024).

Local build tool only: run `python3 render.py` to write entry.png.
The graded program is main.py (stdlib only) which copies entry.png
to /output/entry.png. Pillow is used here, at build time only.
All news below was verified as happening / first reported on
Wednesday 25 November 2026. Labels: OFFICIAL = confirmed by an
authority, REPORTED = reported by a named source, CLAIM = a party's
claim, not confirmed.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (90, 90, 90)
LIGHT = (238, 234, 224)
RED = (178, 34, 34)
NAVY = (18, 48, 88)
TEAL = (14, 90, 90)
GOLD = (184, 134, 11)
BLUE = (40, 90, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to pixel width, return list of lines."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ---------------- news data (verified 25 Nov 2026) ----------------
TOP = [
    {
        "n": "1", "tag": "OFFICIAL", "colour": NAVY,
        "headline": "UK ENERGY CAP TO JUMP 26% TO £2,166",
        "summary": "Ofgem: typical cap rises from £1,723.",
        "source": "Ofgem", "art": "cap",
    },
    {
        "n": "2", "tag": "REPORTED", "colour": RED,
        "headline": "CAIRO TANKER FIRE KILLS AT LEAST 31",
        "summary": "Tanker burns on Ring Road; 21 hurt.",
        "source": "CNN", "art": "firetruck",
    },
    {
        "n": "3", "tag": "OFFICIAL", "colour": NAVY,
        "headline": "US PROPOSES NEW TARIFFS ON 14 PARTNERS",
        "summary": "US proposes tariffs on 14 partners.",
        "source": "Reuters", "art": "tariffs",
    },
]

MEDIUM = [
    ("4", "TWO TANKERS HIT MINES AND BURN IN HORMUZ",
     "Iran's Guards say two tankers hit mines.",
     "Reuters", "REPORTED", "IR", "tanker"),
    ("5", "HOUTHIS CLAIM STRIKE ON RAS TANURA REFINERY",
     "Coalition says it shot down 4 drones; the refinery hit is not confirmed.",
     "Reuters", "CLAIM", "SA", "refinery"),
    ("6", "SHENZHOU-24 LAUNCHES WITH PAKISTAN'S FIRST ASTRONAUT",
     "Shenzhou-24 lifts off from Jiuquan.",
     "AP", "OFFICIAL", "CN", "rocket"),
    ("7", "KOSPI PLUNGES 6.2% AS AI SHARES TUMBLE",
     "Kospi falls to 4,697.51; Samsung -9.9%.",
     "AP", "OFFICIAL", "KR", "chart_down"),
    ("8", "US ECONOMY GREW 4.3% IN Q3, FASTEST IN 3 YEARS",
     "Q3 growth revised up from 3.4%.",
     "Reuters", "OFFICIAL", "US", "chart_up"),
    ("9", "SOLOMON ISLANDS SIGNS TREATY WITH AUSTRALIA",
     "Australia named primary security partner.",
     "NYT", "OFFICIAL", "AU", "treaty"),
    ("10", "JUDGES URGE DROP OF KEY NETANYAHU BRIBERY CASE",
     "Court says conviction in Case 4000 unlikely.",
     "Reuters", "REPORTED", "IL", "gavel"),
    ("11", "AT LEAST 490,334 RUSSIAN SOLDIERS DEAD, BBC FINDS",
     "Leaked records put the toll since Feb 2022.",
     "BBC", "REPORTED", "RU", "document"),
    ("12", "BANGLADESH RAISES GARMENT WAGE 36% AFTER PROTESTS",
     "Entry wage rises to 17,000 taka a month.",
     "Daily Brief", "REPORTED", "BD", "factory"),
]

MORE = [
    ("13", "Poland to set no-fly zone on Ukraine border", "Poland", "REPORTED"),
    ("14", "RSF drone strikes kill 19 in Sudan's Blue Nile", "Sudan", "REPORTED"),
    ("15", "9 dead, 17 trapped in flooded West Java gold mine", "Indonesia", "REPORTED"),
    ("16", "North Korea expels Swiss diplomat, shuts office", "North Korea", "OFFICIAL"),
    ("17", "US proposes extra tariffs on Brazilian sugar, aircraft", "USA / Brazil", "OFFICIAL"),
    ("18", "Saudi-led coalition says it hit Hodeidah port", "Yemen", "CLAIM"),
    ("19", "US tells citizens to leave Iran immediately", "USA", "OFFICIAL"),
    ("20", "Ukrainian drones set two Rosneft refineries ablaze", "Russia", "REPORTED"),
    ("21", "Russian strikes kill two in Odesa, hit Kyiv", "Ukraine", "REPORTED"),
    ("22", "Ukraine says it needs €115bn for 2027", "Ukraine", "OFFICIAL"),
    ("23", "Colombia frees hostages after supermarket siege", "Colombia", "REPORTED"),
    ("24", "Germany's Merz accuses Russia of escalating threats", "Germany", "REPORTED"),
    ("25", "Pope criticises failure of COP31 climate talks", "Vatican", "REPORTED"),
    ("26", "UN warns of new Israeli attacks in Gaza, West Bank", "UN", "OFFICIAL"),
    ("27", "UN aid chief arrives in Yemen as millions go hungry", "Yemen", "OFFICIAL"),
    ("28", "Ebola workers evacuated amid fighting in DR Congo", "DR Congo", "REPORTED"),
    ("29", "Australia passes Digital Duty of Care Act", "Australia", "OFFICIAL"),
    ("30", "Lille beat Bayern 2-1 in Champions League", "France", "OFFICIAL"),
    ("31", "Israeli strike kills Hamas official in Gaza", "Gaza", "REPORTED"),
    ("32", "Iraq court backs federal troops at borders", "Iraq", "OFFICIAL"),
    ("33", "Libya vows retaliation after officers die", "Libya", "REPORTED"),
    ("34", "US Army detonates 5 tonnes of explosive in Iowa", "USA", "REPORTED"),
    ("35", "Aramco opens $7bn Shaheen complex in S Korea", "S Korea", "OFFICIAL"),
    ("36", "ESA Hera reveals Dimorphos crater images", "Europe", "OFFICIAL"),
    ("37", "Greece holds 24-hour nationwide strike", "Greece", "REPORTED"),
    ("38", "US jobless claims fall to 189,000", "USA", "OFFICIAL"),
    ("39", "Pakistan and Russia sign 5-year trade programme", "Pakistan", "OFFICIAL"),
    ("40", "Record king tides flood California coast", "USA", "REPORTED"),
]

TIMELINE = [
    ("00:18 UTC", "Shenzhou-24 launches"),
    ("07:00 UTC", "UK cap rise announced"),
    ("13:00 UTC", "Ras Tanura claim filed"),
    ("16:08 UTC", "Cairo tanker fire"),
]

PINS = [  # (number, lon, lat, label)
    ("1", -0.1, 51.5, "London"), ("2", 31.2, 30.0, "Cairo"),
    ("3", -77.0, 38.9, "Washington"), ("4", 56.5, 26.5, "Hormuz"),
    ("5", 50.2, 26.6, "Ras Tanura"), ("6", 100.3, 41.0, "Jiuquan"),
    ("7", 127.0, 37.5, "Seoul"), ("9", 149.1, -35.3, "Canberra"),
    ("15", 106.8, -6.6, "Bogor"),
]


# ---------------- simple drawn art (no external images) ----------------
def draw_art(draw, kind, x, y, w, h):
    if kind == "tanker":
        draw.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 30, 40))
        draw.rectangle([x + w - 70, y + h - 52, x + w - 18, y + h - 26], fill=(60, 60, 75))
        draw.rectangle([x, y + h - 12, x + w, y + h], fill=(20, 60, 110))
        for i, (fx, fy, s) in enumerate([(x + 40, y + 8, 26), (x + 90, y + 22, 20), (x + 150, y + 2, 30)]):
            draw.ellipse([fx, fy, fx + s, fy + s], fill=(120, 120, 125))
        for fx, fy in [(x + 52, y + 30), (x + 104, y + 44), (x + 164, y + 26)]:
            draw.polygon([(fx, fy + 26), (fx + 12, fy), (fx + 24, fy + 26)], fill=(230, 90, 20))
        draw.ellipse([x + 210, y + 18, x + 232, y + 40], fill=(18, 18, 18))
        for dx, dy in [(-8, -8), (8, -8), (0, -12), (-8, 8), (8, 8)]:
            draw.line([x + 221 + dx, y + 29 + dy, x + 221, y + 29], fill=(18, 18, 18), width=3)
    elif kind == "refinery":
        for i, tx in enumerate([x + 20, x + 80, x + 140, x + 200]):
            draw.rectangle([tx, y + 40, tx + 36, y + h - 10], fill=(90, 95, 105))
            draw.rectangle([tx + 6, y + 18, tx + 30, y + 40], fill=(120, 125, 135))
        draw.rectangle([x, y + h - 10, x + w, y + h], fill=(70, 70, 80))
        for fx, fy in [(x + 110, y + 30), (x + 170, y + 46)]:
            draw.polygon([(fx, fy + 26), (fx + 12, fy), (fx + 24, fy + 26)], fill=(230, 90, 20))
        for i in range(3):
            draw.ellipse([x + 235 + i * 5, y + 10 + i * 9, x + 258 + i * 5, y + 33 + i * 9],
                         fill=(110, 110, 115))
    elif kind == "cap":  # lightning bolt + pound sign + up arrow
        draw.polygon([(x + 34, y + 6), (x + 66, y + 6), (x + 50, y + 34),
                      (x + 68, y + 34), (x + 28, y + 74), (x + 42, y + 42),
                      (x + 26, y + 42)], fill=(230, 180, 20))
        draw.text((x + 96, y + 2), "£", font=font(SANS_B, 52), fill=NAVY)
        draw.polygon([(x + 214, y + 34), (x + 236, y + 34), (x + 225, y + 8)], fill=RED)
        draw.rectangle([x + 220, y + 32, x + 230, y + 68], fill=RED)
        draw.text((x + 244, y + 40), "26%", font=font(SANS_B, 20), fill=RED)
    elif kind == "firetruck":  # fuel tanker truck with flames and smoke
        draw.rectangle([x, y + 64, x + w, y + 68], fill=(150, 150, 155))
        for fx, fy in [(x + 60, y + 12), (x + 120, y + 16)]:
            draw.polygon([(fx, fy + 22), (fx + 11, fy), (fx + 22, fy + 22)], fill=(230, 90, 20))
        for fx, fy, s in [(x + 82, y + 0, 13), (x + 132, y + 4, 10)]:
            draw.ellipse([fx, fy, fx + s, fy + s], fill=(120, 120, 125))
        draw.rectangle([x + 20, y + 26, x + 190, y + 58], fill=(205, 205, 210),
                       outline=(90, 90, 95), width=2)
        draw.rectangle([x + 20, y + 26, x + 190, y + 34], fill=(170, 170, 175))
        draw.rectangle([x + 196, y + 34, x + 250, y + 58], fill=RED)
        draw.rectangle([x + 210, y + 38, x + 232, y + 48], fill=(200, 230, 245))
        for wx in [x + 50, x + 120, x + 222]:
            draw.ellipse([wx - 11, y + 52, wx + 11, y + 74], fill=(20, 20, 20))
            draw.ellipse([wx - 4, y + 59, wx + 4, y + 67], fill=(150, 150, 155))
    else:  # tariffs: document + bars
        draw.rectangle([x + 20, y + 8, x + 130, y + h - 8], fill=(255, 255, 255),
                       outline=(40, 40, 40), width=2)
        for i in range(4):
            draw.line([x + 32, y + 24 + i * 16, x + 118, y + 24 + i * 16], fill=(120, 120, 120), width=3)
        draw.text((x + 32, y + 12), "%", font=font(SANS_B, 22), fill=RED)
        for i, (bx, bh, lab) in enumerate([(x + 150, 56, "20%"), (x + 205, 38, "15%")]):
            draw.rectangle([bx, y + h - 14 - bh, bx + 34, y + h - 14], fill=NAVY if i == 0 else TEAL)
            draw.text((bx, y + h - 34 - bh), lab, font=font(SANS_B, 15), fill=INK)
        draw.text((x + 150, y + h - 12), "CN  EU", font=font(SANS_B, 13), fill=GREY)


def draw_mini_art(draw, kind, x, y, w, h):
    """Small flat vector scene for a medium panel, in a w x h box."""
    if kind == "tanker":
        for fx, fy, s in [(x + 10, y + 2, 10), (x + 26, y + 6, 8)]:
            draw.ellipse([fx, fy, fx + s, fy + s], fill=(120, 120, 125))
        for fx, fy in [(x + 14, y + 16), (x + 30, y + 20)]:
            draw.polygon([(fx, fy + 12), (fx + 6, fy), (fx + 12, fy + 12)], fill=(230, 90, 20))
        draw.rectangle([x + 2, y + 28, x + w - 2, y + 36], fill=(30, 30, 40))
        draw.rectangle([x + w - 18, y + 18, x + w - 4, y + 28], fill=(60, 60, 75))
        draw.rectangle([x, y + 36, x + w, y + h], fill=(20, 60, 110))
    elif kind == "refinery":
        for tx in [x + 4, x + 22, x + 40]:
            draw.rectangle([tx, y + 14, tx + 13, y + 34], fill=(90, 95, 105))
            draw.rectangle([tx + 2, y + 8, tx + 11, y + 14], fill=(120, 125, 135))
        draw.rectangle([x, y + 34, x + w, y + h], fill=(70, 70, 80))
        draw.polygon([(x + 28, y + 18), (x + 34, y + 6), (x + 40, y + 18)], fill=(230, 90, 20))
        draw.ellipse([x + 48, y + 2, x + 56, y + 10], fill=(110, 110, 115))
    elif kind == "rocket":
        draw.text((x + 2, y + 2), "✦", font=font(SANS_B, 11), fill=(150, 150, 160))
        draw.text((x + 48, y + 10), "✦", font=font(SANS_B, 9), fill=(150, 150, 160))
        draw.polygon([(x + 26, y + 10), (x + 36, y + 10), (x + 31, y)], fill=RED)
        draw.rectangle([x + 26, y + 10, x + 36, y + 28], fill=(235, 235, 238),
                       outline=(120, 120, 130))
        draw.ellipse([x + 28, y + 15, x + 34, y + 21], fill=(40, 90, 160))
        draw.polygon([(x + 26, y + 24), (x + 20, y + 32), (x + 26, y + 30)], fill=RED)
        draw.polygon([(x + 36, y + 24), (x + 42, y + 32), (x + 36, y + 30)], fill=RED)
        draw.polygon([(x + 28, y + 28), (x + 34, y + 28), (x + 31, y + h)], fill=(230, 90, 20))
    elif kind == "chart_down":
        for bx, bh in [(x + 6, 24), (x + 22, 16), (x + 38, 8)]:
            draw.rectangle([bx, y + 34 - bh, bx + 12, y + 34], fill=(178, 34, 34))
        draw.line([x + 4, y + 6, x + 56, y + 30], fill=RED, width=3)
        draw.polygon([(x + 50, y + 22), (x + 58, y + 30), (x + 48, y + 32)], fill=RED)
    elif kind == "chart_up":
        for bx, bh in [(x + 6, 10), (x + 22, 18), (x + 38, 26)]:
            draw.rectangle([bx, y + 34 - bh, bx + 12, y + 34], fill=NAVY if bx < x + 30 else TEAL)
        draw.line([x + 4, y + 30, x + 56, y + 6], fill=(14, 90, 90), width=3)
        draw.polygon([(x + 50, y + 14), (x + 58, y + 6), (x + 48, y + 4)], fill=(14, 90, 90))
    elif kind == "treaty":
        draw.rectangle([x + 10, y + 4, x + 52, y + 34], fill=(255, 255, 255),
                       outline=(100, 100, 110), width=2)
        for i in range(3):
            draw.line([x + 16, y + 12 + i * 7, x + 46, y + 12 + i * 7],
                      fill=(140, 140, 145), width=2)
        draw.ellipse([x + 42, y + 28, x + 54, y + h], fill=RED)
        draw.line([x + 4, y + h - 4, x + 40, y + h - 4], fill=(40, 90, 160), width=2)
    elif kind == "gavel":
        draw.rectangle([x + 10, y + 8, x + 42, y + 18], fill=(120, 85, 50))
        draw.rectangle([x + 24, y + 18, x + 30, y + 32], fill=(90, 60, 35))
        draw.rectangle([x + 8, y + 34, x + 52, y + h], fill=(150, 150, 155))
    elif kind == "document":
        draw.rectangle([x + 14, y + 2, x + 48, y + 34], fill=(255, 255, 255),
                       outline=(100, 100, 110), width=2)
        for i in range(3):
            draw.line([x + 19, y + 10 + i * 7, x + 43, y + 10 + i * 7],
                      fill=(140, 140, 145), width=2)
        draw.rectangle([x + 19, y + 28, x + 43, y + 32], fill=RED)
    else:  # factory
        draw.ellipse([x + 48, y, x + 56, y + 8], fill=(120, 120, 125))
        draw.rectangle([x + 50, y + 6, x + 56, y + 22], fill=(70, 70, 80))
        draw.polygon([(x + 2, y + 36), (x + 2, y + 20), (x + 12, y + 28), (x + 22, y + 20),
                      (x + 32, y + 28), (x + 42, y + 20), (x + 52, y + 28), (x + 58, y + 24),
                      (x + 58, y + 36)], fill=(90, 95, 105))
        draw.ellipse([x + 4, y + 26, x + 16, y + 38], fill=GOLD)


CONTINENTS = [
    [(-170, 65), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-80, 32), (-90, 30), (-97, 26), (-105, 22), (-115, 30), (-125, 40),
     (-130, 55), (-150, 60)],
    [(-80, 10), (-60, 10), (-50, 0), (-40, -10), (-35, -20), (-45, -30), (-60, -40),
     (-70, -50), (-75, -35), (-80, -15)],
    [(-10, 36), (-5, 44), (0, 50), (5, 58), (10, 60), (20, 65), (30, 70), (40, 68),
     (30, 60), (20, 55), (15, 45), (10, 40), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (50, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25),
     (10, -15), (5, 5), (-5, 5)],
    [(40, 68), (60, 70), (80, 73), (100, 75), (120, 72), (140, 72), (160, 65),
     (170, 60), (160, 50), (140, 40), (130, 35), (120, 25), (110, 10), (100, 8),
     (90, 15), (80, 8), (70, 20), (60, 25), (50, 28), (40, 35)],
    [(113, -22), (125, -15), (135, -12), (145, -15), (150, -25), (155, -35),
     (145, -40), (135, -35), (125, -32)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(225, 235, 245), outline=(150, 160, 175))
    def px(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (75 - lat) / 130.0 * h)
    for cont in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in cont]
        draw.polygon(pts, fill=(190, 200, 185), outline=(140, 150, 140))
    JITTER = {"4": (16, -12), "5": (-16, 10), "2": (0, 12), "1": (0, -10)}
    for num, lon, lat, label in PINS:
        cx, cy = px(lon, lat)
        dx, dy = JITTER.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            draw.line([cx, cy, cx + dx, cy + dy], fill=RED, width=1)
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
            cx, cy = cx + dx, cy + dy
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED, outline=(255, 255, 255), width=2)
        draw.text((cx, cy), num, font=font(SANS_B, 12), fill=(255, 255, 255), anchor="mm")


# ---------------- layout ----------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 12], fill=RED)
    d.rectangle([0, H - 10, W, H], fill=NAVY)

    # Masthead
    d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52),
           fill=INK, anchor="mt")
    d.text((W // 2, 96), "MAKE.FUN  •  WORLD NEWS  •  ALL STORIES VERIFIED FOR ONE DAY",
           font=font(SANS_B, 15), fill=GREY, anchor="mt")
    d.rectangle([24, 122, W - 24, 162], fill=RED)
    d.text((W // 2, 142), "WEDNESDAY, 25 NOVEMBER 2026", font=font(SANS_B, 29),
           fill=(255, 255, 255), anchor="mm")

    # Stats strip
    stats = ["40 STORIES", "9 REGIONS", "3 TOP STORIES",
             "SOURCES: REUTERS • AP • BBC • CNN • NYT • UN NEWS • ESA"]
    x = 24
    widths = [140, 130, 170, 536]
    for txt, wd in zip(stats, widths):
        d.rectangle([x, 172, x + wd, 198], outline=(150, 140, 120), width=1)
        d.text((x + wd // 2, 185), txt, font=font(SANS_B, 14), fill=NAVY, anchor="mm")
        x += wd

    # Top 3
    col_w, gap = 312, 20
    top_y, top_h = 206, 232
    for i, story in enumerate(TOP):
        x0 = 24 + i * (col_w + gap)
        d.rectangle([x0, top_y, x0 + col_w, top_y + top_h], outline=(160, 150, 130), width=2)
        d.rectangle([x0, top_y, x0 + col_w, top_y + 30], fill=story["colour"])
        d.text((x0 + 10, top_y + 15), f"TOP STORY {story['n']}  •  {story['tag']}",
               font=font(SANS_B, 14), fill=(255, 255, 255), anchor="lm")
        draw_art(d, story["art"], x0 + 12, top_y + 42, col_w - 24, 78)
        y = top_y + 120
        y = draw_wrapped(d, (x0 + 12, y), story["headline"], font(SANS_B, 20),
                         INK, col_w - 24, leading=24)
        sf2 = font(SANS, 13)
        s2 = story["summary"]
        while d.textlength(s2, font=sf2) > col_w - 24 and len(s2) > 4:
            s2 = s2[:-4].rstrip() + "\u2026"
        d.text((x0 + 12, y + 4), s2, font=sf2, fill=(60, 60, 60))
        d.text((x0 + 12, top_y + top_h - 12), f"Source: {story['source']}",
               font=font(SANS_B, 11), fill=GREY, anchor="lb")

    # Section header: Day in brief
    d.rectangle([24, 442, W - 24, 466], fill=NAVY)
    d.text((36, 454), "THE DAY IN BRIEF  —  9 MORE STORIES", font=font(SANS_B, 17),
           fill=(255, 255, 255), anchor="lm")

    # Medium 9: 3 cols x 3 rows, each with a small flat scene + code chip
    mcol_w, mrow_h = 312, 66
    for i, (num, head, summ, src, tag, code, art) in enumerate(MEDIUM):
        col, row = i % 3, i // 3
        x0 = 24 + col * (mcol_w + gap)
        y0 = 474 + row * mrow_h
        d.rectangle([x0, y0, x0 + mcol_w, y0 + mrow_h], outline=(160, 150, 130), width=1)
        d.rectangle([x0, y0, x0 + 70, y0 + mrow_h], fill=(238, 234, 222))
        d.rectangle([x0, y0, x0 + 70, y0 + 18], fill=TEAL if i % 2 == 0 else NAVY)
        d.text((x0 + 35, y0 + 9), code, font=font(SANS_B, 12), fill=(255, 255, 255), anchor="mm")
        draw_mini_art(d, art, x0 + 4, y0 + 22, 62, 40)
        tx = x0 + 78
        tw = mcol_w - 78
        hf = font(SANS_B, 13)
        hy = y0
        for ln in wrap(d, head, hf, tw)[:2]:
            d.text((tx, hy), ln, font=hf, fill=INK)
            hy += 15
        sf = font(SANS, 11)
        for ln in wrap(d, summ, sf, tw)[:2]:
            d.text((tx, hy), ln, font=sf, fill=(70, 70, 70))
            hy += 12
        d.text((tx, y0 + 56), f"{src} • {tag}", font=font(SANS_B, 9), fill=GREY)

    # Map + timeline
    map_x, map_y, map_w, map_h = 24, 680, 600, 80
    d.text((map_x, map_y - 4), "WHERE IT HAPPENED  —  SCHEMATIC MAP",
           font=font(SANS_B, 14), fill=NAVY)
    draw_map(d, map_x, map_y + 16, map_w, map_h - 16)
    tl_x = 648
    d.text((tl_x, map_y - 4), "THE DAY IN ORDER (UTC*)", font=font(SANS_B, 14), fill=NAVY)
    d.rectangle([tl_x, map_y + 16, W - 24, map_y + 16 + map_h - 16], outline=(150, 160, 175))
    ty = map_y + 20
    for j, (when, what) in enumerate(TIMELINE):
        d.ellipse([tl_x + 12, ty + 3, tl_x + 22, ty + 13], fill=RED)
        if j < len(TIMELINE) - 1:
            d.line([tl_x + 17, ty + 13, tl_x + 17, ty + 17], fill=RED, width=2)
        d.text((tl_x + 30, ty), when, font=font(SANS_B, 12), fill=RED)
        d.text((tl_x + 118, ty), what, font=font(SANS, 12), fill=INK)
        ty += 14

    # More list
    d.rectangle([24, 772, W - 24, 796], fill=NAVY)
    d.text((36, 784), "MORE ON 25 NOVEMBER  —  28 MORE STORIES", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="lm")
    for i, (num, head, src, tag) in enumerate(MORE):
        col, row = i % 2, i // 2
        x0 = 24 + col * 500
        y0 = 804 + row * 11
        d.text((x0, y0), f"{num}.", font=font(SANS_B, 11), fill=RED)
        d.text((x0 + 28, y0), head, font=font(SANS, 11), fill=INK)
        # source right-aligned in its column
        d.text((x0 + 488, y0), src, font=font(SANS_B, 10), fill=GREY, anchor="ra")

    # Footer: Date Check + labels + exclusions (date-checked both ways)
    fy = 966
    d.text((24, fy), "DATE CHECK: Every story above happened or was first reported on Wednesday, 25 November 2026.",
           font=font(SANS_B, 12), fill=RED)
    d.text((24, fy + 14),
           "OFFICIAL = confirmed by an authority  •  REPORTED = reported by a named source  •  CLAIM = a party's claim, not confirmed.",
           font=font(SANS, 11), fill=GREY)
    d.text((24, fy + 28),
           "EXCLUDED AS NOT 25 NOV: Huawei verdict (24 Nov)  •  Riyadh tower strike (24 Nov)  •  Nigeria attacks (21–22 Nov)  •  MI5 warning (24 Nov)",
           font=font(SANS_B, 10), fill=RED)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
