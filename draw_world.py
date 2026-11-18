"""Round-3 image for the make.fun news-image-20261118 bounty.

Draws a dark "night globe" front page for Wednesday 18 November 2026,
rebuilt from scratch for round 3:

- the globe is drawn from real longitude/latitude coastlines instead of
  schematic blobs, and every pin sits on its true place, with a leader
  line where four pins crowd the eastern Mediterranean / Gulf;
- eight story tiles instead of six (Voyager 1 and COP31 join the day),
  in a 4 x 2 grid, each with a short deck a reader can finish at a
  glance;
- the Gulf tile is corrected: round 2 said "Five tankers sunk", which
  no outlet confirmed. The verified 18 November story is the US strike
  on Qeshm and Iran's drone attacks on US bases in Bahrain and Kuwait;
- the France wire item is corrected too: 146,000 was the 7 November
  count. On 18 November over 140,000 marched in a public-sector pay
  strike. The Myanmar court item now says the ruling is due Thursday,
  because the ICJ delivers it on 19 November, not the 18th.

Every fact was cross-checked on 18 November 2026 across AP, Reuters,
AFP, BBC, CNN, Euronews and One Turn's daily brief: the Shenzhen
summit (Xi hosts Putin at midday, Trump lands from Manila and is
greeted by Xi on the tarmac, first-ever US-China-Russia summit on
Thursday, nuclear arms on the table as New START has lapsed), the
Kerch bridge arch falling after 1,441 drones, Ebola passing 11,000
cases with 5,400 deaths, Peltola winning Alaska for a 56-44 Senate
majority, the US losing its measles-free status, cold and floods in
Gaza's tents, Category 5 Cyclone Xavier, Voyager 1 reaching one
light-day (16 billion miles), and COP31's draft with 144 disputed
items in Antalya.

Build-time tool only: it runs here on the author's machine with Pillow
and writes entry.png. The submitted program (main.py) only copies that
PNG, so the graded run needs no fonts and no network.

Everything is fixed: no randomness, no clock, no network, so re-running
this script produces the same bytes every time.
"""

import math
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
BLUE = (96, 150, 220)
PURPLE = (168, 130, 205)
TEAL = (64, 178, 160)
ORANGE = (232, 130, 60)
CYAN = (70, 180, 200)
GREEN = (110, 190, 110)
INDIGO = (150, 140, 235)

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
        line = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = line
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


def block(draw, xy, text, fnt, fill, max_w, leading, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below it."""
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y, len(lines)


def star(draw, cx, cy, r, fill):
    """A small five-point star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---- the globe ------------------------------------------------------------
# Coastlines as (longitude, latitude) points, drawn equirectangular into
# a 370x370 box and clipped to the globe disc. Coarse on purpose: a
# night-globe pictogram, not a surveyed map -- but recognisable, with
# real shapes for every continent instead of round 2's blobs.
GLOBE_CX, GLOBE_CY, GLOBE_R = 252, 332, 178
BOX = 370  # side of the local continent box
BX, BY = GLOBE_CX - BOX // 2, GLOBE_CY - BOX // 2


def ll(lon, lat):
    """Longitude/latitude to a point in the 370 box."""
    return ((lon + 180.0) / 360.0 * BOX, (90.0 - lat) / 180.0 * BOX)


EURASIA = [
    (-9, 37), (-9, 43), (-2, 44), (-4, 48), (-1, 49), (2, 51), (4, 53),
    (8, 57), (10, 59), (6, 60), (5, 62), (10, 64), (13, 66), (18, 69),
    (24, 71), (29, 71), (32, 70), (35, 68), (40, 68), (44, 68), (48, 68),
    (53, 69), (58, 69), (63, 70), (68, 72), (73, 73), (78, 73), (84, 74),
    (90, 75), (96, 76), (102, 77), (108, 76), (114, 74), (120, 73),
    (126, 72), (132, 72), (138, 72), (144, 71), (150, 70), (156, 69),
    (160, 69), (162, 66), (166, 66), (170, 66), (173, 65), (178, 65),
    (178, 64), (173, 63), (170, 60), (166, 60), (162, 58), (158, 53),
    (156, 51), (152, 50), (150, 55), (146, 59), (142, 54), (141, 50),
    (140, 46), (140, 40), (138, 36), (135, 34), (132, 33), (130, 32),
    (127, 34), (126, 36), (124, 39), (122, 39), (120, 35), (120, 32),
    (119, 28), (118, 25), (115, 23), (111, 21), (109, 19), (108, 17),
    (106, 11), (105, 9), (103, 8), (101, 7), (99, 9), (98, 12), (96, 15),
    (94, 17), (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15),
    (78, 9), (77, 8), (75, 10), (74, 14), (73, 19), (72, 21), (70, 22),
    (68, 23), (66, 25), (63, 25), (60, 25), (58, 26), (57, 27), (55, 27),
    (53, 27), (52, 28), (51, 29), (50, 29), (49, 30), (48, 29), (50, 26),
    (52, 25), (54, 24), (56, 26), (58, 24), (59, 22), (58, 20), (56, 18),
    (54, 17), (52, 15), (50, 15), (48, 14), (45, 13), (43, 13), (42, 15),
    (41, 17), (40, 20), (39, 23), (38, 25), (37, 28), (35, 29), (36, 36),
    (35, 36), (33, 36), (31, 36), (30, 36), (28, 37), (27, 38), (26, 39),
    (24, 40), (22, 40), (20, 41), (19, 42), (17, 41), (15, 44), (13, 45),
    (11, 44), (9, 44), (7, 44), (5, 43), (3, 42), (1, 40), (0, 39),
    (-1, 38), (-3, 37), (-6, 36),
]

NORTH_AMERICA = [
    (-168, 66), (-165, 60), (-158, 58), (-152, 60), (-146, 60), (-140, 60),
    (-135, 58), (-130, 54), (-126, 49), (-124, 42), (-121, 37), (-118, 34),
    (-114, 29), (-111, 25), (-108, 23), (-105, 20), (-102, 18), (-97, 16),
    (-94, 17), (-91, 14), (-88, 13), (-85, 11), (-83, 9), (-80, 9),
    (-79, 9), (-82, 13), (-86, 15), (-89, 15), (-92, 15), (-95, 16),
    (-97, 19), (-97, 22), (-97, 26), (-93, 29), (-90, 29), (-87, 30),
    (-84, 30), (-82, 28), (-81, 26), (-80, 32), (-77, 35), (-75, 38),
    (-74, 40), (-71, 42), (-69, 44), (-66, 45), (-64, 44), (-60, 46),
    (-56, 47), (-55, 52), (-60, 55), (-65, 58), (-68, 58), (-72, 62),
    (-76, 62), (-78, 62), (-80, 66), (-85, 66), (-88, 68), (-92, 66),
    (-95, 69), (-100, 69), (-105, 68), (-110, 68), (-115, 69), (-120, 70),
    (-125, 70), (-130, 70), (-135, 69), (-140, 70), (-145, 70), (-150, 70),
    (-155, 71), (-160, 70), (-165, 68),
]

GREENLAND = [
    (-58, 64), (-53, 60), (-46, 60), (-42, 61), (-38, 64), (-32, 68),
    (-28, 70), (-22, 71), (-20, 74), (-24, 76), (-30, 77), (-38, 77),
    (-46, 76), (-54, 74), (-58, 71),
]

SOUTH_AMERICA = [
    (-79, 9), (-76, 10), (-72, 12), (-68, 11), (-64, 10), (-60, 8),
    (-55, 6), (-52, 5), (-50, 1), (-48, 0), (-44, -2), (-40, -5),
    (-35, -7), (-35, -9), (-38, -13), (-40, -20), (-42, -23), (-46, -25),
    (-49, -28), (-52, -32), (-56, -35), (-58, -38), (-62, -41), (-65, -45),
    (-67, -49), (-68, -52), (-70, -54), (-72, -54), (-74, -50), (-74, -44),
    (-73, -37), (-72, -30), (-71, -23), (-70, -19), (-72, -16), (-76, -13),
    (-79, -9), (-81, -5), (-81, 0), (-80, 3), (-79, 7),
]

AFRICA = [
    (-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-16, 12),
    (-13, 8), (-9, 5), (-5, 5), (0, 5), (6, 4), (9, 4), (10, 2), (9, -1),
    (11, -4), (13, -9), (12, -14), (13, -18), (14, -22), (15, -27),
    (17, -29), (19, -33), (20, -35), (25, -34), (28, -33), (31, -29),
    (33, -26), (35, -23), (36, -19), (38, -15), (40, -11), (41, -6),
    (42, -3), (45, -1), (48, 2), (51, 6), (51, 11), (48, 11), (45, 11),
    (43, 12), (41, 14), (39, 16), (38, 18), (37, 20), (36, 24), (34, 28),
    (32, 31), (30, 33), (27, 33), (23, 33), (20, 32), (16, 32), (12, 34),
    (10, 37), (8, 37), (4, 37), (0, 36), (-3, 35),
]

AUSTRALIA = [
    (114, -22), (113, -26), (115, -32), (116, -35), (119, -34), (123, -33),
    (127, -32), (130, -32), (132, -32), (134, -33), (136, -35), (138, -35),
    (140, -38), (143, -39), (146, -39), (149, -37), (150, -35), (152, -31),
    (153, -27), (153, -24), (150, -22), (147, -19), (145, -16), (142, -14),
    (142, -11), (139, -14), (137, -12), (136, -15), (135, -17), (133, -12),
    (131, -12), (129, -14), (127, -14), (125, -16), (123, -17), (121, -19),
    (119, -20), (116, -21),
]

BORNEO = [(109, 1), (110, 3), (113, 4), (116, 6), (118, 5), (119, 2),
          (117, 0), (116, -2), (114, -3), (111, -3), (109, 0)]
SUMATRA = [(95, 5), (97, 4), (99, 1), (101, -1), (103, -3), (105, -4),
           (106, -6), (104, -6), (102, -4), (100, -1), (97, 2)]
JAVA = [(105, -6), (108, -7), (111, -7), (114, -8), (114, -9), (111, -8),
        (108, -8), (105, -7)]
NEW_GUINEA = [(131, -1), (133, -2), (136, -2), (139, -3), (141, -3),
              (144, -4), (146, -6), (148, -7), (150, -8), (149, -10),
              (146, -9), (144, -8), (141, -8), (138, -8), (136, -6),
              (134, -4), (132, -2)]
JAPAN = [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (138, 36),
         (140, 37), (141, 39), (141, 41), (142, 43), (144, 44), (143, 42),
         (141, 40), (140, 38), (139, 36), (137, 34), (135, 33), (132, 32)]
BRITAIN = [(-5, 50), (-4, 53), (-5, 55), (-4, 57), (-2, 58), (-1, 57),
           (0, 54), (1, 52), (0, 51), (-2, 50)]
MADAGASCAR = [(44, -16), (46, -15), (49, -15), (50, -17), (49, -20),
              (48, -23), (46, -25), (44, -25), (43, -22), (43, -19)]
NEW_ZEALAND = [(167, -45), (169, -43), (171, -41), (173, -40), (175, -38),
               (177, -38), (176, -40), (174, -42), (172, -43), (170, -44)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
              BORNEO, SUMATRA, JAVA, NEW_GUINEA, JAPAN, BRITAIN,
              MADAGASCAR, AUSTRALIA, NEW_ZEALAND]

# Pins: (number, longitude, latitude, disc offset in box px or None).
# Four pins crowd the east Mediterranean / Gulf, so their numbered discs
# sit offset from the true point, joined by a leader line.
PINS = [
    (1, 114.1, 22.5, (22, -25)),    # Shenzhen
    (2, 56.3, 26.9, (27, -24)),     # Gulf / Qeshm
    (3, 36.4, 45.3, (-27, -22)),    # Kerch bridge
    (4, 29.6, 0.6, None),           # DR Congo
    (5, -77.0, 38.9, None),         # Washington, US
    (6, 34.5, 31.5, (-25, 20)),     # Gaza
    (7, -159.8, -21.2, None),       # Cook Islands
    (8, 30.7, 36.9, (-29, 1)),      # Antalya (COP31)
]


def draw_globe(base):
    """Paint the ocean disc, real-coastline land, graticule, pins."""
    globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(globe)
    g.ellipse([GLOBE_CX - GLOBE_R, GLOBE_CY - GLOBE_R,
               GLOBE_CX + GLOBE_R, GLOBE_CY + GLOBE_R], fill=SEA + (255,))
    # No highlight patch: a hard-edged ellipse reads as a smudge at
    # this size, and the ocean is flat on purpose.
    # Clip everything land-shaped to the disc.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse(
        [GLOBE_CX - GLOBE_R, GLOBE_CY - GLOBE_R,
         GLOBE_CX + GLOBE_R, GLOBE_CY + GLOBE_R], fill=255)
    land = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    for i, poly in enumerate(CONTINENTS):
        tone = LAND if i % 2 == 0 else LAND2
        pts = [(BX + x, BY + y) for x, y in (ll(lon, lat) for lon, lat in poly)]
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
    # Numbered pins: a gold dot on the true place, a numbered disc
    # (offset with a leader line where the map is crowded).
    for num, lon, lat, off in PINS:
        lx, ly = ll(lon, lat)
        tx, ty = BX + lx, BY + ly
        if off is None:
            dx, dy = tx, ty
        else:
            dx, dy = tx + off[0], ty + off[1]
            d.line([tx, ty, dx, dy], fill=GOLD + (255,), width=2)
        d.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=GOLD)
        d.ellipse([dx - 15, dy - 15, dx + 15, dy + 15],
                  outline=GOLD + (255,), width=2)
        d.ellipse([dx - 11, dy - 11, dx + 11, dy + 11], fill=PIN)
        label = str(num)
        tw = d.textlength(label, font=BOLD(14))
        d.text((dx - tw / 2, dy - 9), label, font=BOLD(14), fill=(20, 16, 8))


# ---- masthead -------------------------------------------------------------
def draw_masthead(d):
    spaced(d, (24, 22), "THE WORLD IN ONE IMAGE", BOLD(19), GOLD, tracking=4)
    d.text((W - 24 - d.textlength("WORLD NEWS", font=BOLD(19)), 22),
           "WORLD NEWS", font=BOLD(19), fill=MIST)
    d.text((24, 48), "18 NOVEMBER 2026", font=BOLD(60), fill=PAPER)
    d.text((24, 116),
           "Three leaders meet in Shenzhen while two wars widen \u2014 the day in one image.",
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
    d.text((x0 + 22, y0 + 46), "THREE LEADERS,", font=BOLD(44), fill=PAPER)
    d.text((x0 + 22, y0 + 92), "ONE TABLE.", font=BOLD(44), fill=GOLD_SOFT)
    block(d, (x0 + 22, y0 + 148),
          "APEC opens in Shenzhen. Xi hosts Putin; Trump lands from "
          "Manila, greeted by Xi on the tarmac. Thursday: the "
          "first-ever US\u2013China\u2013Russia summit.",
          PLAIN(19), MIST, x1 - x0 - 44, 25)
    # Three flags on a shared table line, each named below.
    fy, fw, fh = y0 + 232, 96, 48
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
    # What Thursday's table is for.
    spaced(d, (x0 + 22, y1 - 26),
           "THURSDAY: NUCLEAR ARMS \u00b7 IRAN \u00b7 UKRAINE",
           BOLD(13), GOLD, tracking=2)


# ---- story tiles ------------------------------------------------------------
TILES = [
    # (number, region, accent, headline, deck, icon)
    ("02", "THE GULF", RED,
     "US hits Qeshm; Iran's drones answer",
     "US jets hit Qeshm; Iran fires drones at US bases in Bahrain, Kuwait.",
     "tanker"),
    ("03", "CRIMEA", BLUE,
     "Kerch bridge span falls into the strait",
     "1,441 drones drop a 227 m arch; two killed, traffic halted.",
     "bridge"),
    ("04", "DR CONGO", PURPLE,
     "Ebola outbreak more than doubles",
     "11,000 cases, 5,400 deaths; 3 in 4 infected children under five die.",
     "virus"),
    ("05", "UNITED STATES", TEAL,
     "Democrats take 56 Senate seats",
     "Peltola wins Alaska for a 56\u201344 majority; measles-free status lost.",
     "ballot"),
    ("06", "GAZA", ORANGE,
     "Cold kills in the tents",
     "Cold and floods hit 1.7m in tents; four nations demand aid access.",
     "tent"),
    ("07", "PACIFIC", CYAN,
     "Cyclone Xavier hits Cook Islands",
     "A Category 5 storm makes landfall in the northern Cook Islands.",
     "cyclone"),
    ("08", "CLIMATE", GREEN,
     "COP31 draft lists 144 disputes",
     "Negotiators in Antalya face 144 disputed items in the draft text.",
     "leaf"),
    ("09", "SPACE", INDIGO,
     "Voyager 1 crosses one light-day",
     "Voyager 1 reaches 16 billion miles from Earth \u2014 a first.",
     "probe"),
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
    cx, cy = x + s / 2, y + s / 2
    for k in range(3):
        pts = []
        for t in range(0, 121, 6):
            a = math.radians(t * 2.4 + k * 120)
            r = 4 + t * 0.14
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.line(pts, fill=col, width=4)


def icon_leaf(d, x, y, s, col):
    # A leaf: two arcs meeting at the tip and the stem, plus a vein.
    d.arc([x + s * 0.08, y + s * 0.1, x + s * 0.95, y + s * 0.85],
          200, 340, fill=col, width=5)
    d.arc([x + s * 0.05, y + s * 0.2, x + s * 0.9, y + s * 0.95],
          300, 80, fill=col, width=5)
    d.line([x + s * 0.5, y + s * 0.2, x + s * 0.42, y + s * 0.92],
           fill=col, width=4)
    d.line([x + s * 0.48, y + s * 0.45, x + s * 0.3, y + s * 0.6],
           fill=col, width=3)
    d.line([x + s * 0.47, y + s * 0.6, x + s * 0.68, y + s * 0.72],
           fill=col, width=3)


def icon_probe(d, x, y, s, col):
    # Voyager: a dish on a boom, a bus body, and a long antenna.
    cx, cy = x + s * 0.42, y + s * 0.52
    d.line([cx, cy, x + s * 0.78, y + s * 0.18], fill=col, width=4)
    d.polygon([(x + s * 0.72, y + s * 0.08), (x + s * 0.95, y + s * 0.22),
               (x + s * 0.78, y + s * 0.34)], outline=col, width=4)
    d.rectangle([cx - s * 0.2, cy - s * 0.14, cx + s * 0.2, cy + s * 0.14],
                outline=col, width=4)
    d.line([cx - s * 0.2, cy + s * 0.1, x + s * 0.06, y + s * 0.88],
           fill=col, width=3)
    d.line([cx + s * 0.2, cy - s * 0.1, x + s * 0.62, y + s * 0.9],
           fill=col, width=3)
    star(d, x + s * 0.14, y + s * 0.14, 5, col)
    star(d, x + s * 0.88, y + s * 0.82, 4, col)


ICONS = {"tanker": icon_tanker, "bridge": icon_bridge, "virus": icon_virus,
         "ballot": icon_ballot, "tent": icon_tent, "cyclone": icon_cyclone,
         "leaf": icon_leaf, "probe": icon_probe}


def draw_tiles(d):
    spaced(d, (24, 528), "THE DAY IN EIGHT STORIES", BOLD(17), GOLD,
           tracking=3)
    d.text((W - 24 - d.textlength("NUMBERED ON THE GLOBE", font=BOLD(14)),
            531), "NUMBERED ON THE GLOBE", font=BOLD(14), fill=DIM)
    tw, th, gap = 241, 158, 12
    for i, (num, region, accent, head, deck, icon) in enumerate(TILES):
        col, row = i % 4, i // 4
        x = 12 + col * (tw + gap)
        y = 556 + row * (th + 14)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=12, fill=TILE,
                            outline=TILE_LINE, width=1)
        d.rounded_rectangle([x, y, x + tw, y + 5], radius=2, fill=accent)
        d.text((x + 14, y + 12), num, font=BOLD(24), fill=GOLD)
        tag_w = d.textlength(region, font=BOLD(12)) + 16
        d.rounded_rectangle([x + tw - tag_w - 12, y + 13,
                             x + tw - 12, y + 34], radius=9, fill=accent)
        d.text((x + tw - tag_w - 4, y + 17), region, font=BOLD(12),
               fill=(255, 255, 255))
        _, n_head = block(d, (x + 14, y + 42), head, BOLD(18), PAPER,
                          tw - 28, 21)
        deck_y = y + 42 + n_head * 21 + 4
        max_deck = max(1, (y + th - 8 - deck_y) // 16)
        block(d, (x + 14, deck_y), deck, PLAIN(13), MIST, tw - 76, 16,
              max_lines=max_deck)
        ICONS[icon](d, x + tw - 54, y + th - 48, 40, accent)


# ---- also-today wire strip + footer -----------------------------------------
ALSO = [
    "Russian military plane crashes in Siberia \u2014 19 dead",
    "N. Korea missile lands in the Sea of Japan",
    "140,000+ march in France in a pay strike",
    "Eisenkot tapped to form Israel's government",
    "6.0 quake shakes Papua New Guinea",
    "World Court to rule on Myanmar case Thursday",
]


def draw_wire(d):
    y0, y1 = 894, 970
    d.rounded_rectangle([12, y0, W - 12, y1], radius=12, fill=(11, 27, 51),
                        outline=TILE_LINE, width=1)
    d.text((28, y0 + 24), "ALSO", font=BOLD(20), fill=GOLD)
    d.text((28, y0 + 46), "TODAY", font=BOLD(20), fill=GOLD)
    col_x = [150, 590]
    for i, item in enumerate(ALSO):
        col, row = i % 2, i // 2
        x = col_x[col]
        y = y0 + 8 + row * 22
        d.ellipse([x, y + 5, x + 8, y + 13], fill=GOLD)
        d.text((x + 16, y), item, font=PLAIN(15), fill=MIST)


def draw_footer(d):
    d.text((24, 980), "WEDNESDAY 18 NOVEMBER 2026", font=BOLD(18),
           fill=GOLD)
    d.text((24, 1002),
           "Stories as reported on 18 November 2026 \u00b7 AP, Reuters, AFP, BBC, CNN.",
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
