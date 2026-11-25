#!/usr/bin/env python3
"""Front page of Wednesday 25 November 2026, drawn from scratch.

main.py renders one 1024x1024 PNG summing up the world's news of
Wednesday 25 November 2026. It carries its own 5x7 pixel font, its own
filled-shape drawing helpers and its own PNG encoder, all standard
library, no network, no clock, no randomness. Every story below was
first reported, or happened, on Wednesday 25 November 2026:

  * MARKETS -- Asian shares tumble as fresh US tariff threats loom
    and the AI rebound stumbles; Kospi -5.3%, Taiwan -5.1%
    (Reuters, 25 Nov)
  * SPACE -- China's Shenzhou-24 launches with the first Pakistani
    astronaut bound for the Tiangong station (Reuters, 25 Nov)
  * PACIFIC -- Australia and Solomon Islands sign a security pact
    making Canberra the islands' defence partner (Reuters, 25 Nov)
  * UKRAINE -- a Russian strike kills two in the Odesa region and
    drones hit Kyiv, injuring two (Reuters, 25 Nov)
  * ECUADOR -- the Trump administration pauses joint military
    operations with Ecuador during a probe (Reuters, 25 Nov)
  * CHINA -- Shanghai party chief Chen Jining is put under
    investigation, the fourth Politburo member probed since 2025
    (Reuters, 25 Nov)
  * CRICKET -- Vaibhav Sooryavanshi, 15, smashes 204 off 53 balls,
    the fastest List A century and double century (BBC, 25 Nov;
    match played Tue in Doha)
  * AUSTRALIA -- inflation jumps to 4.9% as the cost-of-living
    crisis intensifies (The Guardian, 25 Nov)

Run it twice and the two files are byte-identical: the picture is a
pure function of the constants in this file.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 232)
NAVY = (20, 33, 61)
NAVY2 = (40, 56, 90)
INK = (26, 26, 23)
RED = (176, 36, 28)
GOLD = (198, 160, 38)
TEAL = (13, 106, 106)
GREY = (76, 76, 70)
WHITE = (254, 252, 247)
EDGE = (188, 180, 162)
SKY = (172, 204, 223)
LEAF = (46, 110, 52)
AMBER = (255, 153, 51)
PINK = (214, 120, 130)

# ------------------------------------------------------------------- font
# Pixel font, five cells wide and seven tall. "#" is a filled cell.
FONT = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "# # #", "#  ##", "#  ##", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", "#   #", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "0": (" ### ", "#  ##", "# # #", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "# #  ", "  #  ", "  #  ", "  #  ", "#####"),
    "2": (" ### ", "#   #", "    #", "  ## ", " #   ", "#    ", "#####"),
    "3": ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ",": ("     ", "     ", "     ", "     ", "     ", " ##  ", " #   "),
    "'": ("  #  ", "  #  ", "     ", "     ", "     ", "     ", "     "),
    "-": ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "(": ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    "/": ("    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "),
    "%": ("##  #", "## # ", "  #  ", " #   ", "#  ##", "#  ##", "     "),
    "&": (" ##  ", "#  # ", "#  # ", " #   ", "# # #", "#  # ", " ## #"),
    "+": ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    "=": ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    '"': (" # # ", " # # ", "     ", "     ", "     ", "     ", "     "),
    "*": ("     ", " # # ", "  #  ", "#####", "  #  ", " # # ", "     "),
}

EMPTY = ("     ", "     ", "     ", "     ", "     ", "     ", "     ")


def glyph_for(ch):
    return FONT.get(ch, EMPTY)


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap_text(text, max_chars):
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, w * h * 3, 3):
            self.buf[i] = r
            self.buf[i + 1] = g
            self.buf[i + 2] = b

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.buf[i] = r
                self.buf[i + 1] = g
                self.buf[i + 2] = b

    def frame(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x0, x1, y, color, t=1):
        for yy in range(y, y + t):
            for xx in range(x0, x1 + 1):
                self.px(xx, yy, color)

    def vline(self, x, y0, y1, color, t=1):
        for xx in range(x, x + t):
            for yy in range(y0, y1 + 1):
                self.px(xx, yy, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(t):
                for b in range(t):
                    self.px(x + a, y + b, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            span = int((r * r - dy * dy) ** 0.5) if r * r >= dy * dy else 0
            self.rect(cx - span, yy, 2 * span + 1, 1, color)

    def ring(self, cx, cy, r, color, t=3):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            if r * r < dy * dy:
                continue
            span = int((r * r - dy * dy) ** 0.5)
            inner = int(((r - t) * (r - t) - dy * dy) ** 0.5) if (r - t) * (r - t) >= dy * dy else 0
            self.rect(cx - span, yy, span - inner + 1, 1, color)
            self.rect(cx + inner, yy, span - inner + 1, 1, color)

    def triangle(self, ax, ay, bx, by, cx, cy, color):
        # Filled triangle by scanline interpolation.
        pts = sorted(((ax, ay), (bx, by), (cx, cy)), key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        if y0 == y2:
            return
        for yy in range(y0, y2 + 1):
            xs = []
            for (px0, py0), (px1, py1) in (((x0, y0), (x1, y1)),
                                           ((x1, y1), (x2, y2)),
                                           ((x0, y0), (x2, y2))):
                if py0 == py1:
                    continue
                if min(py0, py1) <= yy <= max(py0, py1):
                    xs.append(px0 + (px1 - px0) * (yy - py0) / (py1 - py0))
            if len(xs) >= 2:
                self.rect(int(min(xs)), yy, int(max(xs)) - int(min(xs)) + 1, 1, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s.upper():
            glyph = glyph_for(ch)
            for row in range(7):
                line = glyph[row]
                for col in range(5):
                    if line[col] == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)


# --------------------------------------------------------------------- PNG
def _chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(path, canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.buf[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ------------------------------------------------------------------ icons
def icon_warning(c, x, y, s):
    c.triangle(x + s // 2, y + 2, x + 2, y + s - 2, x + s - 2, y + s - 2, AMBER)
    c.triangle(x + s // 2, y + 10, x + 9, y + s - 8, x + s - 9, y + s - 8, NAVY)
    c.text(x + s // 2 - 6, y + s // 2 - 4, "!", 2, WHITE)


def icon_city(c, x, y, s):
    base = y + s - 8
    c.disc(x + 10, y + 12, 6, GREY)
    c.disc(x + 22, y + 8, 5, GREY)
    c.rect(x + 4, base - 22, 14, 22, NAVY2)
    c.rect(x + 22, base - 34, 14, 34, NAVY)
    c.rect(x + 40, base - 16, 12, 16, GREY)
    c.rect(x, base, s, 3, INK)


def icon_ball(c, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    c.disc(cx, cy, r, LEAF)
    c.line(cx - r + 4, cy - r + 12, cx - 4, cy, WHITE, 3)
    c.line(cx - 4, cy, cx - r + 4, cy + r - 12, WHITE, 3)
    c.line(cx + r - 4, cy - r + 12, cx + 4, cy, WHITE, 3)
    c.line(cx + 4, cy, cx + r - 4, cy + r - 12, WHITE, 3)


def icon_chip(c, x, y, s):
    m = s // 5
    c.rect(x + m, y + m, s - 2 * m, s - 2 * m, NAVY)
    c.rect(x + 2 * m, y + 2 * m, s - 4 * m, s - 4 * m, GOLD)
    c.rect(x + 2 * m + 4, y + 2 * m + 4, s - 4 * m - 8, s - 4 * m - 8, NAVY2)
    for i in range(3):
        yy = y + m + 4 + i * (s - 2 * m - 8) // 2
        c.rect(x, yy, m, 3, NAVY)
        c.rect(x + s - m, yy, m, 3, NAVY)


def icon_clip(c, x, y, s):
    c.rect(x + 6, y + 4, s - 12, s - 8, WHITE)
    c.frame(x + 6, y + 4, s - 12, s - 8, NAVY, 3)
    c.rect(x + s // 2 - 8, y, 16, 8, RED)
    c.line(x + 12, y + 18, x + 18, y + 26, TEAL, 3)
    c.line(x + 18, y + 26, x + 30, y + 12, TEAL, 3)
    c.rect(x + 12, y + 34, s - 24, 4, EDGE)
    c.rect(x + 12, y + 44, s - 30, 4, EDGE)


def icon_rocket(c, x, y, s):
    cx = x + s // 2
    c.triangle(cx, y + 2, cx - 12, y + 30, cx + 12, y + 30, NAVY)
    c.rect(cx - 12, y + 28, 24, 22, NAVY2)
    c.triangle(cx - 12, y + 34, cx - 24, y + 52, cx - 12, y + 48, RED)
    c.triangle(cx + 12, y + 34, cx + 24, y + 52, cx + 12, y + 48, RED)
    c.disc(cx, y + 38, 6, GOLD)
    c.triangle(cx, y + 58, cx - 7, y + 50, cx + 7, y + 50, AMBER)
    c.rect(cx - 2, y + 50, 4, 8, RED)


def icon_shield(c, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    c.triangle(cx, cy + 24, cx - 22, cy - 16, cx + 22, cy - 16, NAVY)
    c.rect(cx - 22, cy - 16, 44, 22, NAVY)
    c.triangle(cx, cy + 24, cx - 22, cy + 6, cx + 22, cy + 6, NAVY2)
    c.line(cx - 10, cy - 2, cx - 2, cy + 8, WHITE, 4)
    c.line(cx - 2, cy + 8, cx + 12, cy - 10, WHITE, 4)


def icon_tower(c, x, y, s):
    base = y + s - 8
    c.rect(x + 14, base - 44, 16, 44, NAVY)
    c.rect(x + 34, base - 30, 12, 30, NAVY2)
    c.rect(x + 6, base - 18, 10, 18, GREY)
    c.rect(x, base, s, 3, INK)
    c.disc(x + 22, base - 52, 5, RED)
    for yy in (base - 38, base - 28, base - 18):
        c.rect(x + 18, yy, 8, 4, GOLD)
        c.rect(x + 37, yy + 4, 6, 4, GOLD)


def icon_cricket(c, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    c.disc(cx, cy, r, RED)
    c.line(cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8, WHITE, 3)
    c.line(cx + r - 8, cy - r + 8, cx - r + 8, cy + r - 8, WHITE, 3)
    c.disc(cx, cy, 5, WHITE)


def icon_uparrow(c, x, y, s):
    bx, base = x + 4, y + s - 10
    heights = (14, 24, 34)
    for i, hh in enumerate(heights):
        c.rect(bx + i * 18, base - hh, 12, hh, TEAL)
    c.line(bx + 2, base - 40, bx + 52, base - 62, RED, 4)
    c.triangle(bx + 52, base - 62, bx + 36, base - 62, bx + 52, base - 46, RED)


# ------------------------------------------------------------------- boxes
def box(c, x, y, w, h, kicker, head_lines, sub, head_scale=3, icon=None,
        icon_size=56):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, EDGE, 2)
    pad = 16
    c.rect(x + pad, y + 14, 8, 14, RED)
    c.text(x + pad + 14, y + 14, kicker, 2, RED)
    if icon is not None:
        icon(c, x + w - pad - icon_size, y + 10, icon_size)
    hy = y + 44
    lh = 7 * head_scale + 6
    for line in head_lines:
        c.text(x + pad, hy, line, head_scale, INK)
        hy += lh
    chars = (w - 2 * pad) // 12
    sy = hy + 8
    for line in wrap_text(sub, chars):
        c.text(x + pad, sy, line, 2, GREY)
        sy += 18


def lead(c):
    x, y, w, h = 28, 132, 968, 256
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, NAVY, 3)
    c.rect(x + 20, y + 18, 8, 14, RED)
    c.text(x + 34, y + 18, "MARKETS", 2, RED)
    c.text(x + 20, y + 48, "ASIAN SHARES TUMBLE", 4, INK)
    c.text(x + 20, y + 86, "AS TARIFFS LOOM", 4, INK)
    sub = ("Fresh US tariff threats hit sentiment and the AI rebound "
           "stumbles: Kospi, Taiwan and the Nikkei all fall sharply.")
    sy = y + 136
    for line in wrap_text(sub, 51):
        c.text(x + 20, sy, line, 2, GREY)
        sy += 18
    c.text(x + 20, y + 210, "THE AI RALLY FADES", 2, TEAL)
    # Falling bars and arrow on the right.
    bx, base = 720, y + 232
    heights = (172, 136, 96, 56)
    cols = (RED, GOLD, NAVY2, TEAL)
    for i, (hh, col) in enumerate(zip(heights, cols)):
        c.rect(bx + i * 62, base - hh, 44, hh, col)
    c.line(bx - 8, base - 188, bx + 232, base - 40, RED, 4)
    c.triangle(bx + 232, base - 40, bx + 212, base - 40, bx + 232, base - 60, RED)
    c.rect(bx - 8, base, 252, 3, INK)
    labels = ("-5.3%", "-5.1%", "-2.9%", "-2.3%")
    for i, lab in enumerate(labels):
        c.text(bx + i * 62 + 4, base + 8, lab, 1, GREY)
    c.text(bx - 8, y + 18, "KOSPI  TAIWAN  NIKKEI  MSCI ASIA", 1, GREY)


# -------------------------------------------------------------------- page
def render():
    c = Canvas(W, H, PAPER)
    # Masthead.
    c.rect(0, 0, W, 116, NAVY)
    c.text_center(512, 22, "THE WORLD TODAY", 5, WHITE)
    c.text_center(512, 72, "WEDNESDAY 25 NOVEMBER 2026", 2, GOLD)
    c.rect(0, 116, W, 4, RED)
    c.text_center(512, 122, "THE DAY IN EIGHT STORIES", 1, GREY)

    lead(c)

    # Row two: Shenzhou and the Solomons pact.
    box(c, 28, 404, 474, 232, "SPACE",
        ["CHINA LAUNCHES", "SHENZHOU-24 CREW"],
        "First Pakistani astronaut heads to the Tiangong station. "
        "Three-man crew lifts off on Wednesday morning.",
        icon=icon_rocket)
    box(c, 522, 404, 474, 232, "PACIFIC",
        ["CANBERRA SEALS", "SOLOMONS PACT"],
        "Australia signs a security pact making it the islands' "
        "defence partner of choice, a shift from China.",
        icon=icon_shield)

    # Row three: Ukraine, Ecuador, Shanghai.
    box(c, 28, 652, 312, 172, "UKRAINE",
        ["ODESA STRIKE", "KILLS TWO"],
        "Russian strike hits Odesa region. Kyiv drones injure two.",
        icon=icon_city, icon_size=40)
    box(c, 356, 652, 312, 172, "ECUADOR",
        ["US PAUSES OPS", "WITH ECUADOR"],
        "Joint military ops paused during probe of a lethal raid.",
        icon=icon_warning, icon_size=40)
    box(c, 684, 652, 312, 172, "CHINA",
        ["SHANGHAI CHIEF", "UNDER PROBE"],
        "Chen Jining probed. Fourth Politburo member investigated since 2025.",
        icon=icon_tower, icon_size=40)

    # Row four: cricket and Australian inflation.
    box(c, 28, 840, 474, 148, "CRICKET",
        ["15-YEAR-OLD SMASHES", "204 OFF 53 BALLS"],
        "Fastest List A century and double century. 28 sixes in Doha.",
        icon=icon_cricket, icon_size=52)
    box(c, 522, 840, 474, 148, "AUSTRALIA",
        ["INFLATION JUMPS", "TO 4.9 PCT"],
        "Prices up more than expected in October. RBA under pressure.",
        icon=icon_uparrow, icon_size=52)

    c.text_center(512, 998, "SOURCES: REUTERS / BBC / THE GUARDIAN",
                  1, GREY)
    return c


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(path, render())
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
