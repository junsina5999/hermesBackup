#!/usr/bin/env python3
"""
Persian motivational image generator - Premium Glassmorphism Style
Location: /data/workspace/premium_generator.py
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "posts_premium")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1080, 1080

PALETTES = {
    "luxury_gold": {
        "bg": (15, 15, 20),
        "card": (40, 40, 50, 100),
        "accent": (255, 215, 0),
        "text": (255, 255, 255),
        "glow": (255, 215, 0, 30)
    },
    "emerald_night": {
        "bg": (10, 25, 20),
        "card": (30, 50, 45, 120),
        "accent": (0, 255, 180),
        "text": (255, 255, 255),
        "glow": (0, 255, 180, 20)
    },
    "royal_purple": {
        "bg": (20, 10, 35),
        "card": (50, 30, 70, 130),
        "accent": (190, 120, 255),
        "text": (255, 255, 255),
        "glow": (190, 120, 255, 25)
    }
}

def p(text):
    """Reshape Persian/Arabic text — NO bidi reversal."""
    return arabic_reshaper.reshape(str(text))

def add_noise(img, strength=5):
    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            noise = random.randint(-strength, strength)
            r, g, b = pixels[x, y]
            pixels[x, y] = (max(0, min(255, r + noise)),
                            max(0, min(255, g + noise)),
                            max(0, min(255, b + noise)))
    return img

def draw_glass_card(img, palette):
    card_w, card_h = 900, 750
    x, y = (WIDTH - card_w)//2, (HEIGHT - card_h)//2

    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.rounded_rectangle([x, y, x+card_w, y+card_h], radius=50, fill=255)

    blurred_bg = img.filter(ImageFilter.GaussianBlur(radius=20))
    img.paste(blurred_bg, mask=mask)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    d_overlay = ImageDraw.Draw(overlay)
    d_overlay.rounded_rectangle([x, y, x+card_w, y+card_h], radius=50,
                                fill=palette["card"], outline=(255,255,255,40), width=2)
    d_overlay.ellipse([x+100, y-100, x+card_w-100, y+50], fill=palette["glow"])

    return Image.alpha_composite(img.convert("RGBA"), overlay)

def generate_premium_post(main_text, sub_text, author="سید حسین عباسمنش",
                          palette_key="royal_purple", name="post"):
    palette = PALETTES.get(palette_key, PALETTES["royal_purple"])
    img = Image.new("RGB", (WIDTH, HEIGHT), palette["bg"])

    overlay_bg = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    d_bg = ImageDraw.Draw(overlay_bg)
    d_bg.ellipse([-200, -200, 400, 400], fill=palette["glow"])
    d_bg.ellipse([WIDTH-400, HEIGHT-400, WIDTH+200, HEIGHT+200], fill=palette["glow"])
    img = Image.alpha_composite(img.convert("RGBA"), overlay_bg).convert("RGB")

    img = add_noise(img, strength=5)
    img = draw_glass_card(img, palette)
    draw = ImageDraw.Draw(img)

    f_quote = ImageFont.truetype(os.path.join(FONT_DIR, "Vazirmatn-Black.ttf"), 54)
    f_sub = ImageFont.truetype(os.path.join(FONT_DIR, "Vazirmatn-Medium.ttf"), 34)
    f_author = ImageFont.truetype(os.path.join(FONT_DIR, "Vazirmatn-Bold.ttf"), 40)
    f_qm = ImageFont.truetype(os.path.join(FONT_DIR, "Vazirmatn-Black.ttf"), 80)
    f_wm = ImageFont.truetype(os.path.join(FONT_DIR, "Vazirmatn-Medium.ttf"), 24)

    y = 240

    qm = p("«")
    bbox = draw.textbbox((0, 0), qm, font=f_qm)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, y), qm, font=f_qm, fill=palette["accent"])
    y += 110

    def wrap(text, max_chars):
        words = text.split()
        lines, cur = [], []
        for w in words:
            trial = " ".join(cur + [w])
            # Measure reshaped text width
            bbox = draw.textbbox((0, 0), p(trial), font=f_quote if max_chars < 30 else f_sub)
            w_px = bbox[2] - bbox[0]
            limit = 850 if max_chars < 30 else 830
            if w_px > limit:
                if cur:
                    lines.append(" ".join(cur))
                cur = [w]
            else:
                cur.append(w)
        if cur:
            lines.append(" ".join(cur))
        return lines

    # Main text
    for line in wrap(main_text, 22):
        txt = p(line)
        bbox = draw.textbbox((0, 0), txt, font=f_quote)
        w = bbox[2] - bbox[0]
        # Shadow
        draw.text(((WIDTH - w) // 2 + 2, y + 2), txt, font=f_quote, fill=(0, 0, 0, 100))
        # Main
        draw.text(((WIDTH - w) // 2, y), txt, font=f_quote, fill=palette["text"])
        y += 85

    y += 20
    # Sub text
    for line in wrap(sub_text, 35):
        txt = p(line)
        bbox = draw.textbbox((0, 0), txt, font=f_sub)
        w = bbox[2] - bbox[0]
        draw.text(((WIDTH - w) // 2, y), txt, font=f_sub, fill=(200, 200, 200, 255))
        y += 50

    y += 60
    # Author
    txt = p(author)
    bbox = draw.textbbox((0, 0), txt, font=f_author)
    w = bbox[2] - bbox[0]
    draw.line([(WIDTH - w) // 2, y + 50, (WIDTH + w) // 2, y + 50],
              fill=palette["accent"], width=2)
    draw.text(((WIDTH - w) // 2, y), txt, font=f_author, fill=palette["accent"])

    # Watermark
    wm = p("@abasmanesh222")
    bbox = draw.textbbox((0, 0), wm, font=f_wm)
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, HEIGHT - 80), wm, font=f_wm, fill=(150, 150, 150, 255))

    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.convert("RGB").save(path, "PNG", quality=95)
    print(f"Generated: {path}")
    return path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--main", required=True)
    parser.add_argument("--sub", required=True)
    parser.add_argument("--palette", default="royal_purple")
    parser.add_argument("--name", default="post")
    args = parser.parse_args()
    generate_premium_post(args.main, args.sub, palette_key=args.palette, name=args.name)
