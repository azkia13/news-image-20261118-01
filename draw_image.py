#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (1024x1024 PNG).

Deterministic: no network, no randomness, fixed fonts (DejaVu, shipped with
most Linux distros). Run: python3 draw_image.py  -> writes entry.png next to
this file. The entry program (main.ts) only copies entry.png to the output
dir, exactly like the kit starter, so the grader needs no extra dependency.

Stories (all reported on / dated 18 Nov 2026, cross-checked in several
outlets incl. Reuters):
  1. US-Iran: US sinks five Iranian tankers; Iran hits back at ships and a
     US base in Jordan; Bahrain intercepts Iranian drones.
  2. Kerch Bridge: Ukraine strikes the Crimea bridge a 2nd night; its road
     arch collapses into the Kerch Strait; Russia hits two Kyiv bridges.
  3. North Korea fires a ballistic missile into the Sea of Japan.
  4. Gaza: UN warns of deaths from cold; 1.7m displaced; Australia, Canada,
     Italy and the UK urge Israel to let aid in.
  5. COP31 in Antalya enters its decisive phase; draft deal splits nations
     over a fossil-fuel phase-out and a $120bn adaptation fund.
  6. Israel: President Herzog asks ex-army chief Gadi Eisenkot to form a
     government, bypassing caretaker PM Netanyahu.
  Also: Russian military plane crashes in Siberia (19 dead); 146,000 protest
  in France over living costs; Trump arrives in Manila for Quad talks.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def panel(draw, box, fill="#FFFFFF", outline="#0A2540", width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def kicker(draw, x, y, s, color="#FFFFFF", bg="#C0392B"):
    f = font(13, True)
    w = int(draw.textlength(s, font=f)) + 16
    draw.rounded_rectangle([x, y, x + w, y + 22], radius=4, fill=bg)
    text(draw, (x + 8, y + 4), s, f, color)


def headline_block(draw, box, kick, kick_bg, head, sub, head_size=23, sub_size=15):
    x0, y0, x1, y1 = box
    kicker(draw, x0 + 12, y0 + 10, kick, bg=kick_bg)
    lines = wrap(draw, head, font(head_size, True), x1 - x0 - 24)
    y = y0 + 40
    for ln in lines:
        text(draw, (x0 + 12, y), ln, font(head_size, True), "#0A2540")
        y += head_size + 4
    for ln in wrap(draw, sub, font(sub_size), x1 - x0 - 24):
        text(draw, (x0 + 12, y + 2), ln, font(sub_size), "#333333")
        y += sub_size + 4


# ---------------------------------------------------------------- scenes
def scene_gulf(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (255, 176, 102), (178, 52, 44))
    draw.ellipse([x1 - 120, y0 + 18, x1 - 40, y0 + 98], fill="#FFD76E")
    # sea
    draw.rectangle([x0, y0 + 130, x1, y1], fill="#123A5C")
    for yy in (y0 + 148, y0 + 168, y0 + 188):
        draw.line([(x0 + 10, yy), (x1 - 10, yy)], fill="#2E6B9E", width=3)
    # tanker 1 (left, burning)
    draw.rectangle([x0 + 30, y0 + 88, x0 + 300, y0 + 132], fill="#5B2C2C")
    for cx in range(x0 + 45, x0 + 290, 42):
        draw.rectangle([cx, y0 + 66, cx + 30, y0 + 88], fill="#E67E22")
    draw.rectangle([x0 + 250, y0 + 48, x0 + 272, y0 + 88], fill="#3D3D3D")
    # flames
    for (fx, fy, r, c) in [(x0 + 90, y0 + 52, 26, "#FF8C1A"),
                          (x0 + 130, y0 + 40, 32, "#FFC93C"),
                          (x0 + 170, y0 + 54, 22, "#FF6B1A")]:
        draw.polygon([(fx - r, fy + r), (fx, fy - r), (fx + r, fy + r)], fill=c)
    draw.ellipse([x0 + 100, y0 + 8, x0 + 150, y0 + 48], fill="#5A5A5A")
    draw.ellipse([x0 + 140, y0 - 6, x0 + 200, y0 + 38], fill="#777777")
    # warship (right)
    draw.polygon([(x1 - 260, y0 + 132), (x1 - 30, y0 + 132), (x1 - 60, y0 + 104),
                  (x1 - 230, y0 + 104)], fill="#4A5A6A")
    draw.rectangle([x1 - 200, y0 + 82, x1 - 150, y0 + 104], fill="#4A5A6A")
    draw.line([(x1 - 175, y0 + 82), (x1 - 175, y0 + 58)], fill="#4A5A6A", width=4)


def scene_kerch(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (168, 208, 236), (120, 170, 210))
    draw.rectangle([x0, y0 + 118, x1, y1], fill="#1F5C8A")
    for yy in (y0 + 138, y0 + 160):
        draw.line([(x0 + 8, yy), (x1 - 8, yy)], fill="#7FB3D5", width=3)
    # bridge deck left + right, middle span collapsed
    draw.rectangle([x0 + 8, y0 + 78, x0 + 130, y0 + 92], fill="#E8E8E8")
    draw.rectangle([x0 + 210, y0 + 78, x1 - 8, y0 + 92], fill="#E8E8E8")
    draw.arc([x0 + 20, y0 + 30, x0 + 120, y0 + 92], 180, 360, fill="#FFFFFF", width=5)
    draw.arc([x0 + 222, y0 + 30, x1 - 20, y0 + 92], 180, 360, fill="#FFFFFF", width=5)
    # collapsed span tilted into water
    draw.polygon([(x0 + 130, y0 + 92), (x0 + 205, y0 + 150), (x0 + 185, y0 + 162),
                  (x0 + 118, y0 + 104)], fill="#CFCFCF")
    draw.polygon([(x0 + 140, y0 + 150), (x0 + 170, y0 + 138), (x0 + 200, y0 + 152),
                  (x0 + 168, y0 + 168)], fill="#FFFFFF")
    # drones
    for (dx, dy) in [(x0 + 60, y0 + 22), (x0 + 260, y0 + 14)]:
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill="#222222")


def scene_missile(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (10, 18, 48), (38, 64, 110))
    for (sx, sy) in [(x0 + 30, y0 + 20), (x0 + 90, y0 + 48), (x0 + 200, y0 + 16),
                     (x0 + 260, y0 + 60), (x0 + 150, y0 + 34)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill="#FFFFFF")
    draw.rectangle([x0, y0 + 118, x1, y1], fill="#0E2A4A")
    # missile diagonal up-right with flame trail
    draw.line([(x0 + 60, y0 + 108), (x0 + 210, y0 + 30)], fill="#FF9E2C", width=7)
    draw.line([(x0 + 60, y0 + 108), (x0 + 210, y0 + 30)], fill="#FFD76E", width=3)
    mx, my = x0 + 210, y0 + 30
    draw.polygon([(mx, my - 16), (mx + 34, my + 4), (mx + 6, my + 14)], fill="#E8E8E8")
    draw.polygon([(mx + 34, my + 4), (mx + 44, my + 2), (mx + 36, my + 10)], fill="#C0392B")
    # coastline
    draw.polygon([(x0, y1), (x0, y0 + 128), (x0 + 90, y0 + 118), (x0 + 70, y1)],
                 fill="#1B3A2A")


def scene_gaza(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (150, 160, 175), (110, 125, 145))
    draw.rectangle([x0, y0 + 118, x1, y1], fill="#5A7A96")
    # rain
    for rx in range(x0 + 12, x1 - 10, 26):
        draw.line([(rx, y0 + 8), (rx - 8, y0 + 34)], fill="#EAF2F8", width=2)
    # tents
    for tx in (x0 + 22, x0 + 108, x0 + 194):
        draw.polygon([(tx, y0 + 118), (tx + 34, y0 + 82), (tx + 68, y0 + 118)],
                     fill="#E8DCC3", outline="#8A7A5A")
        draw.polygon([(tx + 28, y0 + 118), (tx + 34, y0 + 102), (tx + 40, y0 + 118)],
                     fill="#5A4A33")
    # aid truck
    draw.rectangle([x0 + 210, y0 + 92, x0 + 296, y0 + 118], fill="#FFFFFF",
                   outline="#0A2540")
    draw.rectangle([x0 + 296, y0 + 100, x1 - 14, y0 + 118], fill="#DCE6EE",
                   outline="#0A2540")
    draw.ellipse([x0 + 222, y0 + 114, x0 + 238, y0 + 130], fill="#222222")
    draw.ellipse([x0 + 268, y0 + 114, x0 + 284, y0 + 130], fill="#222222")
    # red cross on the truck box
    cx, cy = x0 + 253, y0 + 105
    draw.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill="#C0392B")
    draw.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill="#C0392B")


def scene_cop31(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (18, 120, 110), (12, 84, 96))
    # sun
    draw.ellipse([x1 - 78, y0 + 12, x1 - 28, y0 + 62], fill="#FFD76E")
    # globe
    cx, cy, r = x0 + 88, y0 + 78, 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#2E86C1", outline="#FFFFFF",
                 width=3)
    draw.ellipse([cx - 34, cy - 30, cx - 2, cy - 2], fill="#27AE60")
    draw.ellipse([cx + 2, cy + 6, cx + 34, cy + 34], fill="#27AE60")
    draw.ellipse([cx + 8, cy - 38, cx + 30, cy - 14], fill="#229954")
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill="#AED6F1", width=3)
    # leaf
    lx, ly = x1 - 92, y0 + 108
    draw.ellipse([lx, ly, lx + 52, ly + 26], fill="#58D68D")
    draw.line([(lx, ly + 26), (lx + 52, ly)], fill="#1E8449", width=3)
    # COP31 badge
    draw.rounded_rectangle([x0 + 12, y0 + 100, x0 + 108, y0 + 130], radius=6,
                           fill="#FFFFFF")
    text(draw, (x0 + 22, y0 + 106), "COP31", font(16, True), "#0E6B62")


def scene_israel(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (190, 215, 235), (140, 175, 205))
    gy = y0 + 62  # ground line
    draw.rectangle([x0, gy, x1, y1], fill="#7A9A5A")
    # Knesset-like building
    draw.rectangle([x0 + 60, y0 + 18, x0 + 250, gy], fill="#EFE6CE",
                   outline="#8A7A5A")
    draw.polygon([(x0 + 50, y0 + 18), (x0 + 155, y0 + 2), (x0 + 260, y0 + 18)],
                 fill="#D9CBA8", outline="#8A7A5A")
    for px in range(x0 + 76, x0 + 244, 30):
        draw.rectangle([px, y0 + 26, px + 12, gy], fill="#C9B98F")
    # Israeli flag on a pole
    draw.line([(x1 - 40, y0 + 4), (x1 - 40, gy)], fill="#333333", width=3)
    draw.rectangle([x1 - 40, y0 + 4, x1 - 12, y0 + 30], fill="#FFFFFF",
                   outline="#2E6B9E")
    draw.line([(x1 - 40, y0 + 8), (x1 - 12, y0 + 8)], fill="#2E6B9E", width=3)
    draw.line([(x1 - 40, y0 + 26), (x1 - 12, y0 + 26)], fill="#2E6B9E", width=3)


def main():
    img = Image.new("RGB", (W, H), "#F6F1E7")
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 116], fill="#0A2540")
    d.rectangle([0, 116, W, 120], fill="#C0392B")
    text(d, (16, 14), "THE WORLD IN ONE IMAGE", font(15, True), "#FFD76E")
    text(d, (1008, 14), "WORLD NEWS", font(15, True), "#9FB6CC", anchor="ra")
    text(d, (16, 36), "WEDNESDAY 18 NOVEMBER 2026", font(44, True), "#FFFFFF")
    text(d, (16, 88), "Six stories that defined the day  \u2014  from the Gulf to Gaza, Kyiv to Antalya",
         font(16), "#D6E4F0")

    # ---- lead: US-Iran ----
    panel(d, [16, 128, 664, 464])
    scene_gulf(d, [18, 130, 662, 278])
    headline_block(d, [16, 278, 664, 464], "LEAD  \u00b7  THE GULF", "#C0392B",
                   "US SINKS FIVE IRANIAN TANKERS",
                   "Iran hits back at ships and a US base in Jordan; Bahrain "
                   "intercepts Iranian drones aimed at US radar sites.",
                   head_size=30, sub_size=16)

    # ---- Kerch ----
    panel(d, [676, 128, 1008, 464])
    scene_kerch(d, [678, 130, 1006, 278])
    headline_block(d, [676, 278, 1008, 464], "UKRAINE", "#1A5276",
                   "KERCH BRIDGE FALLS",
                   "Ukraine hits the Crimea bridge a 2nd night; its road arch "
                   "collapses into the strait. Russia strikes two Kyiv bridges.",
                   head_size=24, sub_size=15)

    # ---- row 2 ----
    panel(d, [16, 476, 336, 744])
    scene_missile(d, [18, 478, 334, 606])
    headline_block(d, [16, 606, 336, 744], "ASIA", "#6C3483",
                   "NORTH KOREA FIRES MISSILE",
                   "Missile lands in the Sea of Japan after joint drills.",
                   head_size=22, sub_size=15)

    panel(d, [352, 476, 672, 744])
    scene_gaza(d, [354, 478, 670, 606])
    headline_block(d, [352, 606, 672, 744], "GAZA", "#7D6608",
                   "AID CALL AS WINTER BITES",
                   "UN warns of cold deaths; 1.7m displaced. Four nations "
                   "urge aid in.",
                   head_size=22, sub_size=15)

    panel(d, [688, 476, 1008, 744])
    scene_cop31(d, [690, 478, 1006, 606])
    headline_block(d, [688, 606, 1008, 744], "CLIMATE  \u00b7  COP31", "#0E6B62",
                   "CLIMATE DEAL DEADLOCK",
                   "Antalya talks in decisive phase; draft splits nations "
                   "on fossil fuels.",
                   head_size=22, sub_size=15)

    # ---- bottom row ----
    panel(d, [16, 756, 512, 932])
    scene_israel(d, [18, 758, 510, 828])
    headline_block(d, [16, 828, 512, 932], "ISRAEL", "#2E6B9E",
                   "EISENKOT TAPPED TO LEAD",
                   "President Herzog asks ex-army chief Gadi Eisenkot to form "
                   "a government, bypassing Netanyahu.",
                   head_size=22, sub_size=14)

    panel(d, [524, 756, 1008, 932], fill="#FFF8E6")
    text(d, (540, 768), "ALSO TODAY", font(15, True), "#C0392B")
    items = [
        ("Russian military plane crashes in Siberia \u2014 19 dead.",
         "A transport aircraft goes down in the Kemerovo region."),
        ("146,000 march in France over living costs.",
         "Unions strike as protests enter a fourth weekend."),
        ("Trump arrives in Manila for Quad talks.",
         "The US president heads on to a summit with Xi in China."),
    ]
    y = 794
    for head, sub in items:
        d.ellipse([540, y + 5, 550, y + 15], fill="#C0392B")
        text(d, (560, y), head, font(15, True), "#0A2540")
        text(d, (560, y + 20), sub, font(13), "#555555")
        y += 46

    # ---- footer ----
    d.rectangle([0, 944, W, H], fill="#0A2540")
    text(d, (16, 962), "18 NOVEMBER 2026", font(20, True), "#FFD76E")
    text(d, (16, 988), "The day's world news in one image. Stories as reported on 18 November 2026.",
         font(14), "#D6E4F0")
    text(d, (1008, 968), "make.fun", font(20, True), "#FFFFFF", anchor="ra")

    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
