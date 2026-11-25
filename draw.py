#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up 25 November 2026 world news.

All artwork is drawn with PIL primitives (rectangles, ellipses, polygons, lines);
no external images are used. Output is deterministic: fixed text, fixed colours,
fixed geometry, no timestamps or randomness.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 24, 24)
NAVY = (16, 32, 64)
BLUE = (28, 68, 140)
GREY = (90, 88, 80)
LIGHT = (232, 226, 210)
GOLD = (214, 164, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` pixels."""
    lines = []
    for para in text.split("\n"):
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


def para(draw, xy, text, fnt, fill, width, leading=None):
    """Draw wrapped paragraph, return y just below the last line."""
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_art(draw, x, y, w, h):
    """Dark panel: server racks, a cracked shield, warning triangle."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY, outline=INK, width=3)
    # server racks on the left
    for i in range(3):
        rx = x + 24 + i * 118
        draw.rectangle([rx, y + 24, rx + 96, y + 124], fill=(24, 48, 88),
                       outline=(90, 130, 190), width=2)
        for j in range(3):
            ly = y + 34 + j * 28
            draw.rectangle([rx + 12, ly, rx + 84, ly + 15], fill=(10, 20, 40))
            draw.ellipse([rx + 18, ly + 3, rx + 28, ly + 12],
                         fill=(60, 220, 120) if j % 2 == 0 else (220, 60, 60))
            draw.rectangle([rx + 38, ly + 6, rx + 76, ly + 10], fill=(120, 160, 210))
    # shield with a crack, right side
    cx, cy = x + w - 150, y + h // 2
    shield = [(cx, cy - 78), (cx + 74, cy - 58), (cx + 74, cy + 8),
              (cx, cy + 84), (cx - 74, cy + 8), (cx - 74, cy - 58)]
    draw.polygon(shield, fill=(210, 220, 240), outline=GOLD, width=4)
    draw.polygon([(cx, cy - 52), (cx + 48, cy - 38), (cx + 48, cy + 4),
                  (cx, cy + 56), (cx - 48, cy + 4), (cx - 48, cy - 38)],
                 fill=BLUE)
    crack = [(cx - 8, cy - 50), (cx + 10, cy - 18), (cx - 12, cy + 6),
             (cx + 8, cy + 30), (cx - 4, cy + 54)]
    draw.line(crack, fill=RED, width=6, joint="curve")
    # warning triangle bottom right
    tx, ty = x + w - 96, y + h - 92
    draw.polygon([(tx, ty), (tx + 72, ty), (tx + 36, ty - 62)],
                 fill=GOLD, outline=INK, width=3)
    draw.text((tx + 30, ty - 48), "!", font=font(SANS, 34), fill=INK)
    draw.text((x + 24, y + h - 44), "LANGLEY, VIRGINIA  —  THE BREACH HIT AN",
              font=font(SANS_REG, 13), fill=(170, 190, 220))
    draw.text((x + 24, y + h - 24), "UNCLASSIFIED OPEN-SOURCE SYSTEM.",
              font=font(SANS_REG, 13), fill=(170, 190, 220))


def draw_ship(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(198, 214, 232), outline=INK, width=2)
    # sea
    for i in range(4):
        yy = y + h - 18 + i * 5
        draw.arc([x + 8 + i * 30, yy - 7, x + 60 + i * 30, yy + 7], 0, 180,
                 fill=BLUE, width=3)
    # hull
    draw.polygon([(x + 30, y + h - 38), (x + w - 30, y + h - 38),
                  (x + w - 52, y + h - 14), (x + 52, y + h - 14)], fill=(120, 40, 30))
    draw.rectangle([x + 78, y + 34, x + w - 78, y + h - 38], fill=(60, 60, 70))
    draw.rectangle([x + 100, y + 18, x + w - 130, y + 34], fill=(90, 90, 100))
    # smoke
    for i, r in enumerate((13, 10, 8)):
        draw.ellipse([x + w - 158 + i * 16, y + 8 - i * 4,
                       x + w - 158 + i * 16 + r * 2, y + 8 - i * 4 + r * 2],
                      fill=(120, 120, 120))


def draw_cross(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 214), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 - 8
    draw.rectangle([cx - 16, cy - 44, cx + 16, cy + 44], fill=RED)
    draw.rectangle([cx - 44, cy - 16, cx + 44, cy + 16], fill=RED)


def draw_cap(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 220, 190), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2
    draw.polygon([(cx - 70, cy + 6), (cx, cy - 46), (cx + 70, cy + 6)],
                 fill=NAVY, outline=INK, width=2)
    draw.rectangle([cx - 88, cy + 6, cx + 88, cy + 18], fill=NAVY)
    draw.rectangle([cx - 8, cy - 58, cx + 8, cy - 44], fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIF, 62),
           fill=PAPER, anchor="ma")
    d.text((W // 2, 84), "WEDNESDAY 25 NOVEMBER 2026  •  ONE DAY, THE WHOLE WORLD",
           font=font(SANS, 17), fill=GOLD, anchor="ma")
    rule(d, m, 130, W - m, 3)
    d.text((m, 138), "Vol. I — No. 25", font=font(SANS_REG, 15), fill=GREY)
    d.text((W - m, 138), "PRICE: FREE TO READ", font=font(SANS_REG, 15),
           fill=GREY, anchor="ra")

    # ---- breaking banner ----
    d.rectangle([m, 164, W - m, 196], fill=RED)
    d.text((W // 2, 170), "★  BREAKING NEWS  ★", font=font(SANS, 20),
           fill=(255, 255, 255), anchor="ma")

    # ---- lead headline ----
    y = para(d, (m, 208),
             "CIA AND U.S. SPY CHIEF'S OFFICE HIT BY CYBERATTACK",
             font(SERIF, 52), INK, W - 2 * m, leading=58)
    y = para(d, (m, y + 6),
             "Hackers breach the unclassified open-source intelligence system used by "
             "the CIA and the Office of the Director of National Intelligence. Officials "
             "say no classified data was touched. Who did it is still unknown.",
             font(SERIF_REG, 21), (40, 40, 40), W - 2 * m, leading=27) + 8

    # ---- lead illustration ----
    art_h = 170
    draw_lead_art(d, m, y, W - 2 * m, art_h)
    y += art_h + 8
    d.text((m, y), "THE LATEST IN A STRING OF CYBER INCIDENTS TO HIT U.S. AGENCIES.",
           font=font(SANS, 14), fill=RED)
    y += 26
    rule(d, m, y, W - m, 3)
    y += 12

    # ---- three secondary stories ----
    col_w = (W - 2 * m - 2 * 20) // 3
    stories = [
        ("UKRAINE WAR AT SEA",
         "ZELENSKIY CONFIRMS UKRAINE HIT RUSSIAN SHIP IN GULF OF FINLAND",
         "President Zelenskiy says Ukraine's drone strike on the cargo ship "
         "Sparta II was legitimate. Norway urges caution.",
         draw_ship),
        ("EBOLA AND WAR IN CONGO",
         "WHO EVACUATES EBOLA STAFF AS FIGHTING RAGES IN CONGO",
         "Health workers sheltered three days in a hospital in Akwe, Ituri, "
         "before being evacuated as fierce fighting closed in.",
         draw_cross),
        ("SEOUL",
         "SOUTH KOREA EDUCATION MINISTER QUITS OVER EXAM-CHEATING SCANDAL",
         "Minister Choi Kyo-jin resigns after a cheating scandal that shocked "
         "the nation and shook Seoul's schools.",
         draw_cap),
    ]
    top = y
    for i, (kicker, head, body, art) in enumerate(stories):
        x = m + i * (col_w + 20)
        d.text((x, top), kicker, font=font(SANS, 15), fill=RED)
        art(d, x, top + 26, col_w, 92)
        yy = para(d, (x, top + 130), head, font(SERIF, 19), INK, col_w,
                  leading=23)
        para(d, (x, yy + 4), body, font(SERIF_REG, 14), (40, 40, 40), col_w,
             leading=18)
        if i < 2:
            d.line([(x + col_w + 10, top), (x + col_w + 10, top + 268)],
                   fill=LIGHT, width=2)
    y = top + 266
    rule(d, m, y, W - m, 3)
    y += 10

    # ---- also today strip ----
    d.text((m, y), "ALSO TODAY", font=font(SANS, 17), fill=RED)
    y += 22
    items = [
        "NEPAL — A 5.6-magnitude quake strikes Koshi Province near the Chinese border.",
        "CRICKET — England beat Australia by eight wickets in the second T20 to level the series.",
        "TECH — Virginia and Oregon sue SpaceX over Grok's 'spicy mode' deepfakes.",
    ]
    for item in items:
        d.text((m + 14, y), "•", font=font(SANS, 16), fill=INK)
        y = para(d, (m + 34, y), item, font(SERIF_REG, 16), INK,
                 W - 2 * m - 34, leading=19) + 1
    y += 2
    rule(d, m, y, W - m, 2)
    d.text((W // 2, y + 4),
           "The World Today  •  Wednesday 25 November 2026  •  Stories first "
           "reported on 25 November 2026",
           font=font(SANS_REG, 12), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
