"""Round-2 image for the make.fun news-image-20261118 bounty.

Draws a dark "night globe" front page for Wednesday 18 November 2026:
a glowing world globe with numbered pins, a Shenzhen summit lead panel,
six numbered story tiles and an "also today" wire strip.

Build-time tool only: it runs here on the author's machine with Pillow and
writes entry.png. The submitted program (main.py) only copies that PNG,
so the graded run needs no fonts and no network.

Everything is fixed: no randomness, no clock, no network, so re-running
this script produces the same bytes every time.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

# ---- palette: a night newsroom, deep navy + warm amber -------------------
INK = (8, 20, 38)          # page background, top
INK2 = (13, 33, 64)        # page background, bottom
PANEL = (16, 35, 63)       # lead panel fill
TILE = (15, 32, 58)        # story tile fill
TILE_LINE = (36, 70, 110)  # tile border
GOLD = (232, 178, 74)      # accent / pins / rules
GOLD_SOFT = (246, 214, 140)
PAPER = (244, 246, 250)    # headline white
MIST = (185, 201, 220)     # body grey-blue
DIM = (140, 160, 184)      # small print
SEA = (22, 64, 107)        # globe ocean
LAND = (62, 142, 122)      # globe land, teal green
LAND2 = (86, 160, 120)     # second land tone
PIN = (240, 166, 52)       # map pin amber
RED = (198, 60, 52)
TEAL = (64, 178, 160)
BLUE = (96, 150, 220)
GREEN = (110, 190, 110)
PURPLE = (168, 130, 205)
ORANGE = (232, 130, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu face, falling back to Liberation Sans if needed."""
    for path in (
        os.path.join(FONT_DIR, name),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731
PLAIN = lambda s: font("DejaVuSans.ttf", s)          # noqa: E731


def vertical_gradient(size, top, bottom):
    """A plain top-to-bottom gradient canvas, no external assets."""
    img = Image.new("RGB", size, top)
    px = img.load()
    w, h = size
    for y in range(h):
        t = y / max(1, h - 1)
        px_line = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = px_line
    return img


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw caps text with manual letter tracking."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def block(draw, xy, text, fnt, fill, max_w, leading):
    """Draw a wrapped paragraph; returns the y just below it."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    """A small five-point star centred on (cx, cy)."""
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---- the globe ------------------------------------------------------------
# Continents as simple polygons inside a 370x370 box; the box is centred
# on the globe and clipped to the circle. Shapes are deliberately
# schematic: a night-globe pictogram, not a surveyed map.
GLOBE_CX, GLOBE_CY, GLOBE_R = 252, 332, 178
BOX = 370  # side of the local continent box
BX, BY = GLOBE_CX - BOX // 2, GLOBE_CY - BOX // 2

CONTINENTS = [
    # North America
    [(30, 78), (92, 52), (148, 60), (168, 92), (146, 128), (108, 152),
     (72, 138), (40, 112)],
    # Greenland
    [(168, 38), (192, 34), (198, 52), (180, 60), (166, 50)],
    # South America
    [(104, 186), (150, 180), (166, 214), (142, 266), (116, 250),
     (100, 212)],
    # Africa
    [(196, 150), (246, 140), (270, 170), (256, 226), (220, 242),
     (200, 202)],
    # Europe
    [(196, 94), (226, 84), (242, 104), (222, 126), (200, 116)],
    # Asia
    [(250, 70), (330, 54), (356, 90), (332, 130), (290, 136),
     (264, 106)],
    # South-East Asian islands
    [(298, 148), (316, 144), (320, 158), (302, 162)],
    [(322, 164), (336, 160), (340, 172), (324, 176)],
    # Australia
    [(298, 214), (344, 208), (352, 238), (312, 246), (296, 230)],
]

# Pins: (number, local x, local y) in the same 370 box.
PINS = [
    (1, 310, 112),   # Shenzhen
    (2, 268, 128),   # Gulf / Qeshm
    (3, 238, 92),    # Crimea
    (4, 228, 196),   # DR Congo
    (5, 92, 96),     # United States
    (6, 230, 140),   # Gaza
    (7, 344, 236),   # Cook Islands
]


def draw_globe(base):
    """Paint the ocean circle, land blobs, graticule and numbered pins."""
    globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(globe)
    # Ocean disc with a soft highlight in the upper left.
    g.ellipse([GLOBE_CX - GLOBE_R, GLOBE_CY - GLOBE_R,
               GLOBE_CX + GLOBE_R, GLOBE_CY + GLOBE_R], fill=SEA + (255,))
    # Clip everything land-shaped to the disc.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse(
        [GLOBE_CX - GLOBE_R, GLOBE_CY - GLOBE_R,
         GLOBE_CX + GLOBE_R, GLOBE_CY + GLOBE_R], fill=255)
    land = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    for i, poly in enumerate(CONTINENTS):
        tone = LAND if i % 2 == 0 else LAND2
        pts = [(BX + x, BY + y) for x, y in poly]
        ld.polygon(pts, fill=tone + (255,))
    # Graticule on the same layer, so the disc mask clips its arcs.
    for dx in (-90, 0, 90):
        ld.ellipse([GLOBE_CX - 60 + dx * 0.55, GLOBE_CY - GLOBE_R,
                    GLOBE_CX + 60 + dx * 0.55, GLOBE_CY + GLOBE_R],
                   outline=(255, 255, 255, 42), width=2)
    for dy in (-62, 62):
        ld.ellipse([GLOBE_CX - GLOBE_R, GLOBE_CY - 55 + dy,
                    GLOBE_CX + GLOBE_R, GLOBE_CY + 55 + dy],
                   outline=(255, 255, 255, 36), width=2)
    land.putalpha(Image.composite(land.split()[3], Image.new("L", (W, H), 0), mask))
    globe.alpha_composite(land)
    g = ImageDraw.Draw(globe)
    g.ellipse([GLOBE_CX - GLOBE_R, GLOBE_CY - GLOBE_R,
               GLOBE_CX + GLOBE_R, GLOBE_CY + GLOBE_R],
              outline=(120, 180, 220, 160), width=3)
    base.alpha_composite(globe)
    d = ImageDraw.Draw(base)
    # Numbered pins with a glow ring.
    for num, lx, ly in PINS:
        x, y = BX + lx, BY + ly
        d.ellipse([x - 19, y - 19, x + 19, y + 19],
                  outline=GOLD + (255,), width=2)
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=PIN)
        label = str(num)
        tw = d.textlength(label, font=BOLD(15))
        d.text((x - tw / 2, y - 10), label, font=BOLD(15), fill=(20, 16, 8))


# ---- masthead -------------------------------------------------------------
def draw_masthead(d):
    spaced(d, (24, 22), "THE WORLD IN ONE IMAGE", BOLD(19), GOLD, tracking=4)
    d.text((W - 24 - d.textlength("WORLD NEWS", font=BOLD(19)), 22),
           "WORLD NEWS", font=BOLD(19), fill=MIST)
    d.text((24, 48), "18 NOVEMBER 2026", font=BOLD(60), fill=PAPER)
    d.text((24, 116),
           "Shenzhen hosts the world while two wars widen \u2014 the day in one image.",
           font=PLAIN(21), fill=MIST)
    d.rectangle([24, 148, W - 24, 151], fill=GOLD)


# ---- lead panel: Shenzhen ---------------------------------------------------
def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + 11, y + 10, 7, (255, 222, 0))
    for sx, sy in ((28, 7), (34, 12), (32, 19), (25, 20)):
        star(d, x + sx, y + sy, 3, (255, 222, 0))


def flag_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(245, 245, 245))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 0))


def flag_usa(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (245, 245, 245))
    d.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.55)],
                fill=(40, 60, 130))
    for row in range(3):
        for col in range(4):
            d.ellipse([x + 4 + col * 8, y + 4 + row * 7,
                       x + 7 + col * 8, y + 7 + row * 7], fill=(255, 255, 255))


def draw_lead(d):
    x0, y0, x1, y1 = 472, 164, 1000, 512
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=PANEL,
                        outline=TILE_LINE, width=2)
    d.rectangle([x0, y0, x1, y0 + 5], fill=GOLD)
    spaced(d, (x0 + 22, y0 + 20), "LEAD  \u00b7  SHENZHEN, CHINA",
           BOLD(17), GOLD, tracking=3)
    d.text((x0 + 22, y0 + 48), "THREE LEADERS,", font=BOLD(46), fill=PAPER)
    d.text((x0 + 22, y0 + 96), "ONE TABLE.", font=BOLD(46), fill=GOLD_SOFT)
    block(d, (x0 + 22, y0 + 156),
          "APEC opens in Shenzhen. Xi hosts Putin; Trump flies in "
          "from Manila after the Quad. Thursday: the first-ever "
          "US\u2013China\u2013Russia summit.",
          PLAIN(20), MIST, x1 - x0 - 44, 27)
    # Three flags on a shared table line, each named below.
    fy, fw, fh = y0 + 252, 96, 52
    d.rounded_rectangle([x0 + 22, fy + fh + 8, x1 - 22, fy + fh + 14],
                        radius=3, fill=GOLD)
    seats = [("XI", flag_china), ("PUTIN", flag_russia), ("TRUMP", flag_usa)]
    step = (x1 - x0 - 44 - 3 * fw) // 2
    for i, (name, painter) in enumerate(seats):
        fx = x0 + 22 + i * (fw + step)
        d.rectangle([fx - 2, fy - 2, fx + fw + 2, fy + fh + 2],
                    outline=(120, 150, 190), width=1)
        painter(d, fx, fy, fw, fh)
        d.line([fx + fw // 2, fy + fh + 2, fx + fw // 2, fy + fh + 8],
               fill=(200, 200, 200), width=3)
        nw = d.textlength(name, font=BOLD(16))
        d.text((fx + fw / 2 - nw / 2, fy + fh + 20), name,
               font=BOLD(16), fill=PAPER)


# ---- story tiles ------------------------------------------------------------
TILES = [
    # (number, region, accent, headline, deck, icon)
    ("02", "THE GULF", RED,
     "Five tankers sunk as the sea war widens",
     "US jets hit Qeshm; drones hit US bases in Bahrain and Kuwait.",
     "tanker"),
    ("03", "CRIMEA", BLUE,
     "Kerch bridge span falls into the strait",
     "Span falls; two killed, traffic halted. Russia hits Kyiv bridges.",
     "bridge"),
    ("04", "DR CONGO", PURPLE,
     "Ebola outbreak more than doubles",
     "11,000 cases, 5,400 deaths; three in four infected children die.",
     "virus"),
    ("05", "UNITED STATES", TEAL,
     "Democrats take 56 Senate seats",
     "Peltola wins Alaska; the US also loses its measles-free status.",
     "ballot"),
    ("06", "GAZA", ORANGE,
     "Cold kills in the tents",
     "The UN warns of cold deaths as 1.7 million shelter in tents.",
     "tent"),
    ("07", "PACIFIC", GREEN,
     "Cyclone Xavier hits the Cook Islands",
     "A Category 5 storm makes landfall in the northern islands.",
     "cyclone"),
]


def icon_tanker(d, x, y, s, col):
    d.polygon([(x, y + s * 0.55), (x + s * 0.95, y + s * 0.55),
               (x + s * 0.85, y + s * 0.8), (x + s * 0.1, y + s * 0.8)],
              fill=col)
    d.rectangle([x + s * 0.6, y + s * 0.28, x + s * 0.72, y + s * 0.55],
                fill=col)
    d.ellipse([x + s * 0.62, y + s * 0.12, x + s * 0.72, y + s * 0.28],
              fill=col)
    for wx in (0.1, 0.42, 0.74):
        d.arc([x + s * wx, y + s * 0.86, x + s * (wx + 0.24),
               y + s * 1.02], 180, 360, fill=col, width=3)


def icon_bridge(d, x, y, s, col):
    d.line([x, y + s * 0.7, x + s, y + s * 0.7], fill=col, width=5)
    d.arc([x + s * 0.08, y + s * 0.18, x + s * 0.6, y + s * 0.72],
          180, 360, fill=col, width=5)
    d.arc([x + s * 0.62, y + s * 0.34, x + s * 0.92, y + s * 0.72],
          180, 300, fill=col, width=5)
    d.polygon([(x + s * 0.72, y + s * 0.62), (x + s * 0.86, y + s * 0.58),
               (x + s * 0.8, y + s * 0.86), (x + s * 0.66, y + s * 0.88)],
              fill=col)


def icon_virus(d, x, y, s, col):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([cx + r * math.cos(a), cy + r * math.sin(a),
                cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)],
               fill=col, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - r * 0.45, cy - r * 0.5, cx - r * 0.05, cy - r * 0.1],
              fill=SEA)
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.45, cy + r * 0.5],
              fill=SEA)


def icon_ballot(d, x, y, s, col):
    d.rectangle([x + s * 0.14, y + s * 0.42, x + s * 0.86, y + s * 0.9],
                outline=col, width=4)
    d.line([x + s * 0.14, y + s * 0.42, x + s * 0.5, y + s * 0.2,
            x + s * 0.86, y + s * 0.42], fill=col, width=4)
    d.line([x + s * 0.3, y + s * 0.66, x + s * 0.45, y + s * 0.8,
            x + s * 0.72, y + s * 0.5], fill=col, width=5)


def icon_tent(d, x, y, s, col):
    d.polygon([(x + s * 0.5, y + s * 0.14), (x + s * 0.9, y + s * 0.82),
               (x + s * 0.1, y + s * 0.82)], outline=col, width=4)
    d.polygon([(x + s * 0.5, y + s * 0.5), (x + s * 0.66, y + s * 0.82),
               (x + s * 0.34, y + s * 0.82)], fill=col)
    d.line([x + s * 0.08, y + s * 0.92, x + s, y + s * 0.92],
           fill=col, width=3)


def icon_cyclone(d, x, y, s, col):
    import math
    cx, cy = x + s / 2, y + s / 2
    for k in range(3):
        pts = []
        for t in range(0, 121, 6):
            a = math.radians(t * 2.4 + k * 120)
            r = 4 + t * 0.14
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.line(pts, fill=col, width=4)


ICONS = {"tanker": icon_tanker, "bridge": icon_bridge, "virus": icon_virus,
         "ballot": icon_ballot, "tent": icon_tent, "cyclone": icon_cyclone}


def draw_tiles(d):
    spaced(d, (24, 528), "THE DAY IN SIX STORIES", BOLD(17), GOLD,
           tracking=3)
    d.text((W - 24 - d.textlength("NUMBERED ON THE GLOBE", font=BOLD(14)),
            531), "NUMBERED ON THE GLOBE", font=BOLD(14), fill=DIM)
    tw, th, gap = 324, 152, 12
    for i, (num, region, accent, head, deck, icon) in enumerate(TILES):
        col, row = i % 3, i // 3
        x = 12 + col * (tw + gap)
        y = 556 + row * (th + 14)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=12, fill=TILE,
                            outline=TILE_LINE, width=1)
        d.rounded_rectangle([x, y, x + tw, y + 5], radius=2, fill=accent)
        d.text((x + 14, y + 12), num, font=BOLD(26), fill=GOLD)
        tag_w = d.textlength(region, font=BOLD(13)) + 16
        d.rounded_rectangle([x + tw - tag_w - 12, y + 14,
                             x + tw - 12, y + 36], radius=9, fill=accent)
        d.text((x + tw - tag_w - 4, y + 18), region, font=BOLD(13),
               fill=(255, 255, 255))
        block(d, (x + 14, y + 46), head, BOLD(20), PAPER, tw - 28, 24)
        block(d, (x + 14, y + 98), deck, PLAIN(14), MIST, tw - 76, 18)
        ICONS[icon](d, x + tw - 58, y + th - 52, 44, accent)


# ---- also-today wire strip + footer -----------------------------------------
ALSO = [
    "Russian military plane crashes in Siberia \u2014 19 dead",
    "COP31 draft lists 144 disputed items in Antalya",
    "N. Korea missile lands in the Sea of Japan",
    "146,000 march in France over living costs",
    "Eisenkot tapped to form Israel's government",
    "6.0 quake shakes Papua New Guinea",
]


def draw_wire(d):
    y0, y1 = 890, 968
    d.rounded_rectangle([12, y0, W - 12, y1], radius=12, fill=(11, 27, 51),
                        outline=TILE_LINE, width=1)
    d.text((28, y0 + 28), "ALSO", font=BOLD(20), fill=GOLD)
    d.text((28, y0 + 50), "TODAY", font=BOLD(20), fill=GOLD)
    col_x = [150, 590]
    for i, item in enumerate(ALSO):
        col, row = i % 2, i // 2
        x = col_x[col]
        y = y0 + 12 + row * 22
        d.ellipse([x, y + 5, x + 8, y + 13], fill=GOLD)
        d.text((x + 16, y), item, font=PLAIN(15), fill=MIST)


def draw_footer(d):
    d.text((24, 980), "WEDNESDAY 18 NOVEMBER 2026", font=BOLD(18),
           fill=GOLD)
    d.text((24, 1002),
           "Stories as reported on 18 November 2026.",
           font=PLAIN(14), fill=DIM)
    mark = "make.fun"
    d.text((W - 24 - d.textlength(mark, font=BOLD(22)), 982), mark,
           font=BOLD(22), fill=PAPER)


def build():
    """Compose the whole page and write entry.png next to this file."""
    page = vertical_gradient((W, H), INK, INK2).convert("RGBA")
    draw = ImageDraw.Draw(page)
    draw_masthead(draw)
    draw_globe(page)
    draw = ImageDraw.Draw(page)
    draw_lead(draw)
    draw_tiles(draw)
    draw_wire(draw)
    draw_footer(draw)
    page.convert("RGB").save(OUT_PATH, format="PNG", optimize=True)
    return OUT_PATH


if __name__ == "__main__":
    print(build())
