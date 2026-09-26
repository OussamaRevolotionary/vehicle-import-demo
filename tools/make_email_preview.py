"""Build the clickable preview image used inside outreach emails (dashboard + title + play button).

    python tools/make_email_preview.py            # writes assets/email-preview-fr.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("C:/Windows/Fonts")

VARIANTS = {
    "fr": dict(
        out="email-preview-fr.jpg",
        title="Plateforme d'importation automobile",
        sub="Écrans réels  ·  vidéo de 13 s  ·  prête dès le jour 1",
        button="Voir la démo en direct",
    ),
}


def build(v):
    base = Image.open(ROOT / "assets" / "og-image.jpg").convert("RGB").resize((1200, 630))
    # dark gradient over the lower two thirds so the text reads on top of the screenshot
    shade = Image.new("L", (1, 630))
    for y in range(630):
        shade.putpixel((0, y), int(max(0, min(1, (y - 230) / 260)) * 235))
    overlay = Image.new("RGB", (1200, 630), (10, 13, 19))
    base = Image.composite(overlay, base, shade.resize((1200, 630)))

    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(str(FONTS / "segoeuib.ttf"), 50)
    sub_font = ImageFont.truetype(str(FONTS / "segoeui.ttf"), 27)
    btn_font = ImageFont.truetype(str(FONTS / "segoeuib.ttf"), 33)

    d.text((56, 418), v["title"], font=title_font, fill=(255, 255, 255))
    d.text((58, 478), v["sub"], font=sub_font, fill=(214, 220, 230))

    tw = d.textlength(v["button"], font=btn_font)
    x0, y0, h = 56, 526, 68
    x1 = x0 + 78 + tw + 34
    d.rounded_rectangle((x0, y0, x1, y0 + h), radius=h // 2, fill=(220, 38, 38))
    cx, cy = x0 + 44, y0 + h // 2
    d.polygon([(cx - 10, cy - 14), (cx - 10, cy + 14), (cx + 14, cy)], fill=(255, 255, 255))
    d.text((x0 + 78, y0 + 11), v["button"], font=btn_font, fill=(255, 255, 255))

    out = ROOT / "assets" / v["out"]
    base.save(out, "JPEG", quality=84, optimize=True, progressive=True)
    print(out.name, out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    for variant in VARIANTS.values():
        build(variant)
