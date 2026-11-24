"""Render the meme: 'MY AI AGENT BUILT MY GAME IN 3 MINUTES / THE FINAL BOSS IS A 404 ERROR'.

1024x1024 PNG, under 1 MiB. Drawn with PIL only.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, size, max_w, draw, s, stroke=6):
    """Largest font size <= `size` whose text fits within max_w."""
    while size > 10:
        fnt = ImageFont.truetype(path, size)
        bbox = draw.textbbox((0, 0), s, font=fnt, stroke_width=stroke)
        if bbox[2] - bbox[0] <= max_w:
            return fnt
        size -= 2
    return ImageFont.truetype(path, 10)


def text_center(draw, y, s, fnt, fill, stroke=6, stroke_fill=(0, 0, 0)):
    bbox = draw.textbbox((0, 0), s, font=fnt, stroke_width=stroke)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2 - bbox[0], y), s, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return bbox[3] - bbox[1]


def main():
    img = Image.new("RGB", (W, H), (13, 17, 23))
    d = ImageDraw.Draw(img, "RGBA")

    # subtle vertical gradient + dot grid
    for y in range(H):
        t = y / H
        r = int(13 + 18 * t)
        g = int(17 + 24 * t)
        b = int(23 + 38 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    for gy in range(40, H, 64):
        for gx in range(40, W, 64):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(255, 255, 255, 18))

    # stars
    import random
    rnd = random.Random(7)
    for _ in range(60):
        x, y = rnd.randint(20, W - 20), rnd.randint(20, H - 20)
        r = rnd.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randint(60, 160)))

    # ---- top setup lines ----
    y = 56
    y += text_center(d, y, "MY AI AGENT BUILT", fit_font(BOLD, 84, 940, d, "MY AI AGENT BUILT"), (255, 255, 255))
    y += 6
    y += text_center(d, y, "MY GAME IN 3 MINUTES", fit_font(BOLD, 84, 940, d, "MY GAME IN 3 MINUTES"), (255, 214, 64))
    y += 6

    # ---- center scene: rocket + controller ----
    cx = W // 2
    # launch pad ground line
    d.line([(140, 640), (884, 640)], fill=(255, 255, 255, 90), width=4)

    # rocket body (centered ~cx, nose at y=300, base at y=560)
    # flame
    d.polygon([(cx - 26, 560), (cx + 26, 560), (cx, 640)], fill=(255, 140, 0))
    d.polygon([(cx - 14, 560), (cx + 14, 560), (cx, 610)], fill=(255, 214, 64))
    # fins
    d.polygon([(cx - 52, 470), (cx - 52, 560), (cx - 96, 590)], fill=(214, 48, 49))
    d.polygon([(cx + 52, 470), (cx + 52, 560), (cx + 96, 590)], fill=(214, 48, 49))
    # body
    d.rounded_rectangle([cx - 52, 330, cx + 52, 560], radius=52, fill=(240, 240, 240))
    # nose cone
    d.polygon([(cx - 52, 360), (cx + 52, 360), (cx, 290)], fill=(214, 48, 49))
    # window
    d.ellipse([cx - 26, 400, cx + 26, 452], fill=(56, 130, 246))
    d.ellipse([cx - 26, 400, cx + 26, 452], outline=(13, 17, 23), width=4)
    d.ellipse([cx - 12, 410, cx + 4, 426], fill=(255, 255, 255))
    # "v1.0" badge on body
    d.rounded_rectangle([cx - 40, 490, cx + 40, 528], radius=10, fill=(13, 17, 23))
    d.text((cx, 509), "v1.0", font=font(MONO, 26), fill=(255, 214, 64), anchor="mm")

    # smoke puffs
    for (sx, sy, sr) in [(cx - 120, 620, 26), (cx + 120, 620, 26),
                         (cx - 80, 636, 20), (cx + 80, 636, 20), (cx, 642, 24)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200, 90))

    # floating code symbols
    d.text((120, 330), "{ }", font=font(MONO, 64), fill=(86, 156, 214), anchor="lm")
    d.text((W - 120, 330), "</>", font=font(MONO, 64), fill=(86, 156, 214), anchor="rm")
    d.text((120, 520), "0101", font=font(MONO, 44), fill=(120, 200, 120), anchor="lm")
    d.text((W - 120, 520), "SHIP", font=font(MONO, 44), fill=(255, 214, 64), anchor="rm")

    # game controller, bottom-left of the scene
    cbox = (120, 560, 330, 620)
    d.rounded_rectangle(cbox, radius=26, fill=(30, 41, 59), outline=(255, 255, 255), width=3)
    d.rectangle([168, 580, 196, 600], fill=(255, 255, 255))  # d-pad h
    d.rectangle([176, 572, 188, 608], fill=(255, 255, 255))  # d-pad v
    for (bx, by, col) in [(280, 580, (214, 48, 49)), (300, 596, (255, 214, 64)),
                          (260, 596, (56, 130, 246)), (280, 612, (120, 200, 120))]:
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col)

    # divider
    d.line([(90, 690), (934, 690)], fill=(255, 214, 64), width=5)

    # ---- punchline ----
    y = 724
    y += text_center(d, y, "THE FINAL BOSS", fit_font(BOLD, 96, 940, d, "THE FINAL BOSS"), (255, 255, 255))
    y += 8
    y += text_center(d, y, "IS A 404 ERROR", fit_font(BOLD, 96, 940, d, "IS A 404 ERROR"), (255, 80, 80))

    # small footer tag
    d.text((W // 2, 972), "shipped by my AI agent  •  make.fun", font=font(MONO, 22),
           fill=(160, 160, 160), anchor="mm")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
