#!/usr/bin/env python3
"""
Generate Persian motivational quote images for Telegram channels.
Usage:  python3 scripts/generate-post.py [--quote "..." --palette deep_purple --output posts/post.png]

Dependencies: pip3 install Pillow arabic-reshaper python-bidi
Fonts: Vazirmatn Bold/Black/Medium TTF files in fonts/ directory
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(SKILL_DIR, "..", "..", "..", "..", "workspace", "fonts")
OUTPUT_DIR = os.path.join(SKILL_DIR, "..", "..", "..", "..", "workspace", "posts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1080, 1080

PALETTES = {
    "deep_purple": {"bg_top": (25,10,60),"bg_bottom": (60,20,100),"accent": (200,150,255),"text": (255,255,255),"subtext": (200,180,230),"quote_mark": (180,120,255)},
    "warm_gold":   {"bg_top": (50,30,10),"bg_bottom": (80,50,15),"accent": (255,200,80),"text": (255,255,255),"subtext": (230,200,160),"quote_mark": (255,180,50)},
    "ocean_blue":  {"bg_top": (10,30,80),"bg_bottom": (20,60,120),"accent": (100,200,255),"text": (255,255,255),"subtext": (170,210,240),"quote_mark": (80,180,255)},
    "midnight":    {"bg_top": (15,15,30),"bg_bottom": (25,25,50),"accent": (255,215,0),"text": (255,255,255),"subtext": (200,200,220),"quote_mark": (255,200,50)},
}

def reshape(text): return get_display(arabic_reshaper.reshape(text))

def wrap(text, max_chars=22):
    words, lines, cur, cur_len = text.split(), [], [], 0
    for w in words:
        if cur_len + len(w) + 1 > max_chars and cur:
            lines.append(" ".join(cur)); cur, cur_len = [w], len(w)
        else: cur.append(w); cur_len += len(w) + 1
    if cur: lines.append(" ".join(cur))
    return lines

def generate(quote, author="سید حسین عباسمنش", sub_text="", palette="deep_purple", out="post.png"):
    p = PALETTES.get(palette, PALETTES["deep_purple"])
    img = Image.new("RGB", (WIDTH, HEIGHT), p["bg_top"])
    draw = ImageDraw.Draw(img)

    # gradient
    for y in range(HEIGHT):
        r = p["bg_top"][0] + (p["bg_bottom"][0]-p["bg_top"][0])*y//HEIGHT
        g = p["bg_top"][1] + (p["bg_bottom"][1]-p["bg_top"][1])*y//HEIGHT
        b = p["bg_top"][2] + (p["bg_bottom"][2]-p["bg_top"][2])*y//HEIGHT
        draw.line([(0,y),(WIDTH,y)], fill=(r,g,b))

    try:
        fb = ImageFont.truetype(os.path.join(FONT_DIR,"Vazirmatn-Bold.ttf"), 36)
        fq = ImageFont.truetype(os.path.join(FONT_DIR,"Vazirmatn-Black.ttf"), 48)
        fm = ImageFont.truetype(os.path.join(FONT_DIR,"Vazirmatn-Medium.ttf"), 28)
    except: fb = fq = fm = ImageFont.load_default()

    y = 140
    # accent line
    draw.rounded_rectangle([(WIDTH//2-100, y), (WIDTH//2+100, y+3)], radius=2, fill=p["accent"]); y += 40
    # opening quote
    qm = reshape("«")
    bb = draw.textbbox((0,0), qm, font=fq)
    draw.text(((WIDTH-(bb[2]-bb[0]))//2, y), qm, font=fq, fill=p["quote_mark"]); y += 100
    # quote text
    for line in wrap(quote, 20 if len(quote)>60 else 24):
        rl = reshape(line)
        bb = draw.textbbox((0,0), rl, font=fq)
        draw.text(((WIDTH-(bb[2]-bb[0]))//2, y), rl, font=fq, fill=p["text"]); y += 76
    y += 20
    # closing quote
    cm = reshape("»")
    bb = draw.textbbox((0,0), cm, font=fq)
    draw.text(((WIDTH-(bb[2]-bb[0]))//2, y), cm, font=fq, fill=p["quote_mark"]); y += 80
    # line
    draw.rounded_rectangle([(WIDTH//2-100, y), (WIDTH//2+100, y+2)], radius=1, fill=p["accent"]); y += 30
    # sub text
    if sub_text:
        for line in wrap(sub_text, 30):
            rl = reshape(line)
            bb = draw.textbbox((0,0), rl, font=fm)
            draw.text(((WIDTH-(bb[2]-bb[0]))//2, y), rl, font=fm, fill=p["subtext"]); y += 44
        y += 20
    # author
    at = reshape(author)
    bb = draw.textbbox((0,0), at, font=fb)
    draw.text(((WIDTH-(bb[2]-bb[0]))//2, y), at, font=fb, fill=p["accent"]); y += 50
    # bottom accent
    draw.rounded_rectangle([(WIDTH//2-100, y), (WIDTH//2+100, y+2)], radius=1, fill=p["accent"])

    path = os.path.join(OUTPUT_DIR, out)
    img.save(path, "PNG", quality=95)
    print(json.dumps({"status":"ok","path":path,"palette":palette}))
    return path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--quote", default="تو همان چیزی هستی که باور داری")
    parser.add_argument("--author", default="سید حسین عباسمنش")
    parser.add_argument("--sub-text", default="")
    parser.add_argument("--palette", default="deep_purple", choices=list(PALETTES.keys()))
    parser.add_argument("--output", default="post.png")
    args = parser.parse_args()
    generate(args.quote, args.author, args.sub_text, args.palette, args.output)
