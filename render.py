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
        "n": "1", "tag": "REPORTED", "colour": RED,
        "headline": "TWO TANKERS HIT MINES AND CATCH FIRE IN HORMUZ",
        "summary": "Iran's Guards say two tankers hit mines.",
        "source": "Reuters", "art": "tanker",
    },
    {
        "n": "2", "tag": "CLAIM", "colour": GOLD,
        "headline": "HOUTHIS CLAIM STRIKE ON RAS TANURA REFINERY",
        "summary": "Houthis say they hit Saudi's top refinery.",
        "source": "Reuters", "art": "refinery",
    },
    {
        "n": "3", "tag": "OFFICIAL", "colour": NAVY,
        "headline": "US PROPOSES NEW TARIFFS ON 14 PARTNERS",
        "summary": "US proposes tariffs on 14 partners.",
        "source": "Reuters", "art": "tariffs",
    },
]

MEDIUM = [
    ("4", "UK ENERGY CAP TO JUMP 26% TO £2,166",
     "Ofgem: typical cap rises from £1,723.",
     "Ofgem", "OFFICIAL", "£"),
    ("5", "CAIRO TANKER FIRE KILLS AT LEAST 31",
     "Tanker burns on Cairo's Ring Road; 21 hurt.",
     "CNN", "REPORTED", "EG"),
    ("6", "CHINA LAUNCHES SHENZHOU-24, PAKISTAN'S FIRST ASTRONAUT",
     "Shenzhou-24 lifts off from Jiuquan.",
     "AP", "OFFICIAL", "CN"),
    ("7", "KOSPI PLUNGES 6.2% AS AI SHARES TUMBLE",
     "Kospi falls to 4,697.51; Samsung -9.9%.",
     "AP", "OFFICIAL", "KR"),
    ("8", "US ECONOMY GREW 4.3% IN Q3, FASTEST IN 3 YEARS",
     "Q3 growth revised up from 3.4%.",
     "Reuters", "OFFICIAL", "US"),
    ("9", "SOLOMON ISLANDS SIGNS SECURITY TREATY WITH AUSTRALIA",
     "Australia named primary security partner.",
     "NYT", "OFFICIAL", "AU"),
    ("10", "JUDGES URGE DROP OF KEY NETANYAHU BRIBERY CASE",
     "Court says conviction in Case 4000 unlikely.",
     "Reuters", "REPORTED", "IL"),
    ("11", "AT LEAST 490,334 RUSSIAN SOLDIERS DEAD, BBC FINDS",
     "Leaked records put the toll since Feb 2022.",
     "BBC", "REPORTED", "RU"),
    ("12", "BANGLADESH RAISES GARMENT WAGE 36% AFTER PROTESTS",
     "Entry wage rises to 17,000 taka a month.",
     "Daily Brief", "REPORTED", "BD"),
]

MORE = [
    ("13", "Poland to set no-fly zone on Ukraine border", "Poland", "REPORTED"),
    ("14", "RSF drone strikes kill 19 in Sudan's Blue Nile", "Sudan", "REPORTED"),
    ("15", "26 miners trapped in flooded West Java gold mine", "Indonesia", "REPORTED"),
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
]

TIMELINE = [
    ("00:18 UTC", "Shenzhou-24 launches"),
    ("Morning", "Kospi falls 6.2%"),
    ("Midday", "UK cap rise announced"),
    ("Afternoon", "US tariffs proposed"),
    ("16:08 UTC", "Cairo tanker fire"),
]

PINS = [  # (number, lon, lat, label)
    ("1", 56.5, 26.5, "Hormuz"), ("2", 50.2, 26.6, "Ras Tanura"),
    ("5", 31.2, 30.0, "Cairo"), ("4", -0.1, 51.5, "London"),
    ("6", 100.3, 41.0, "Jiuquan"), ("7", 127.0, 37.5, "Seoul"),
    ("9", 149.1, -35.3, "Canberra"), ("15", 106.8, -6.6, "Bogor"),
    ("3", -77.0, 38.9, "Washington"),
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
    JITTER = {"1": (16, -12), "2": (-16, 10), "5": (0, 12), "4": (0, -10)}
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
    stats = ["38 STORIES", "9 REGIONS", "3 TOP STORIES", "SOURCES: REUTERS • AP • BBC"]
    x = 24
    widths = [170, 150, 210, 446]
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
    d.rectangle([24, 446, W - 24, 470], fill=NAVY)
    d.text((36, 458), "THE DAY IN BRIEF  —  9 MORE STORIES", font=font(SANS_B, 17),
           fill=(255, 255, 255), anchor="lm")

    # Medium 9: 3 cols x 3 rows (headline max 2 lines, summary 1 line)
    mcol_w, mrow_h = 312, 56
    for i, (num, head, summ, src, tag, code) in enumerate(MEDIUM):
        col, row = i % 3, i // 3
        x0 = 24 + col * (mcol_w + gap)
        y0 = 478 + row * mrow_h
        d.rectangle([x0, y0, x0 + 44, y0 + 44], fill=TEAL if i % 2 == 0 else NAVY)
        d.text((x0 + 22, y0 + 22), code, font=font(SANS_B, 14), fill=(255, 255, 255), anchor="mm")
        tx = x0 + 52
        hf = font(SANS_B, 13)
        for ln in wrap(d, head, hf, mcol_w - 52)[:2]:
            d.text((tx, y0), ln, font=hf, fill=INK)
            y0 += 15
        sf = font(SANS, 11)
        sline = summ
        while d.textlength(sline, font=sf) > mcol_w - 52 and len(sline) > 4:
            sline = sline[:-4].rstrip() + "…"
        d.text((tx, y0), sline, font=sf, fill=(70, 70, 70))
        d.text((tx, 478 + row * mrow_h + 48), f"{src} • {tag}", font=font(SANS_B, 9), fill=GREY)

    # Map + timeline
    map_x, map_y, map_w, map_h = 24, 654, 600, 96
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
            d.line([tl_x + 17, ty + 13, tl_x + 17, ty + 22], fill=RED, width=2)
        d.text((tl_x + 30, ty), when, font=font(SANS_B, 12), fill=RED)
        d.text((tl_x + 118, ty), what, font=font(SANS, 12), fill=INK)
        ty += 19

    # More list
    d.rectangle([24, 774, W - 24, 798], fill=NAVY)
    d.text((36, 786), "MORE ON 25 NOVEMBER  —  26 MORE STORIES", font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="lm")
    for i, (num, head, src, tag) in enumerate(MORE):
        col, row = i % 2, i // 2
        x0 = 24 + col * 500
        y0 = 806 + row * 11
        d.text((x0, y0), f"{num}.", font=font(SANS_B, 11), fill=RED)
        d.text((x0 + 28, y0), head, font=font(SANS, 11), fill=INK)
        # source right-aligned in its column
        d.text((x0 + 488, y0), src, font=font(SANS_B, 10), fill=GREY, anchor="ra")

    # Footer: Date Check + labels + exclusions (date-checked both ways)
    fy = 956
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
