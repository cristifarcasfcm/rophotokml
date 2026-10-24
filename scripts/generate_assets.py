#!/usr/bin/env python3
"""Generează TOATE resursele grafice (iconițe, splash, grafice magazine) pentru Android și iOS.
Rulare (din rădăcina proiectului):  python3 scripts/generate_assets.py
Necesită Pillow:  pip install pillow
Rezultatele se scriu direct în android/ , ios/ și store/ (se comit în git).
"""
import glob, os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BG = (13, 26, 13)
GREEN = (34, 197, 94)
SS = 4  # supersampling


def art(side):
    """Desenul (parcelă KML + lentilă foto + pin GPS) pe fundal transparent, pătrat `side`."""
    s = side * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    poly = [(.15, .35), (.40, .15), (.85, .25), (.80, .75), (.35, .85), (.15, .65)]
    d.polygon([(x * s, y * s) for x, y in poly], fill=(34, 197, 94, 60), outline=(34, 197, 94, 235), width=max(2, int(s * .03)))
    cx, cy = s * .5, s * .52
    for r, fill, outline, w in [
        (.26, (24, 95, 165, 255), (255, 255, 255, 245), .035),
        (.18, (15, 40, 70, 255), (250, 199, 117, 220), .015),
        (.10, (60, 140, 220, 255), None, 0),
    ]:
        rr = s * r
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=fill, outline=outline, width=max(1, int(s * w)))
    hl, off = s * .04, s * .04
    d.ellipse([cx - off - hl, cy - off - hl, cx - off + hl, cy - off + hl], fill=(255, 255, 255, 235))
    px, py, pr = s * .72, s * .30, s * .09
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=max(1, int(s * .02)))
    dr = s * .03
    d.ellipse([px - dr, py - dr, px + dr, py + dr], fill=(255, 255, 255, 255))
    return img.resize((side, side), Image.LANCZOS)


def paste_center(base, layer, cx=0.5, cy=0.5):
    x = int(base.width * cx - layer.width / 2)
    y = int(base.height * cy - layer.height / 2)
    base.alpha_composite(layer, (x, y))


def legacy_icon(size, round_=False):
    img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size * SS
    w = max(2, int(s * .04))
    if round_:
        d.ellipse([0, 0, s - 1, s - 1], fill=BG + (255,), outline=GREEN + (255,), width=w)
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * .22), fill=BG + (255,), outline=GREEN + (255,), width=w)
    img = img.resize((size, size), Image.LANCZOS)
    paste_center(img, art(int(size * (.78 if round_ else .9))))
    return img


def foreground(size):
    """Strat adaptiv Android: conținut în zona sigură (66/108 din lățime)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    paste_center(img, art(int(size * 66 / 108)))
    return img


def full_bleed(size):
    """Pătrat opac fără colțuri rotunjite și fără alpha (cerință Apple + Google Play)."""
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    m = int(size * .035)
    d.rectangle([m, m, size - m - 1, size - m - 1], outline=GREEN + (255,), width=max(2, int(size * .008)))
    paste_center(img, art(int(size * .82)))
    return img.convert("RGB")


def font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf",
              "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", "DejaVuSansMono-Bold.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def splash(w, h):
    img = Image.new("RGBA", (w, h), BG + (255,))
    side = int(min(w, h) * .28)
    paste_center(img, art(side), .5, .46)
    return img.convert("RGB")


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "PNG")
    print("  ", os.path.relpath(path, ROOT))


def main():
    res = os.path.join(ROOT, "android/app/src/main/res")
    print("Android iconițe:")
    for dens, legacy, fg in [("mdpi", 48, 108), ("hdpi", 72, 162), ("xhdpi", 96, 216), ("xxhdpi", 144, 324), ("xxxhdpi", 192, 432)]:
        save(legacy_icon(legacy), f"{res}/mipmap-{dens}/ic_launcher.png")
        save(legacy_icon(legacy, True), f"{res}/mipmap-{dens}/ic_launcher_round.png")
        save(foreground(fg), f"{res}/mipmap-{dens}/ic_launcher_foreground.png")
    with open(f"{res}/values/ic_launcher_background.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0D1A0D</color>\n</resources>\n')
    print("Android splash:")
    for p in glob.glob(f"{res}/drawable*/splash.png"):
        w, h = Image.open(p).size
        save(splash(w, h), p)
    print("iOS:")
    save(full_bleed(1024), os.path.join(ROOT, "ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png"))
    for p in glob.glob(os.path.join(ROOT, "ios/App/App/Assets.xcassets/Splash.imageset/*.png")):
        w, h = Image.open(p).size
        save(splash(w, h), p)
    print("Grafice magazine:")
    save(full_bleed(512), os.path.join(ROOT, "store/android/icon-512.png"))
    save(full_bleed(1024), os.path.join(ROOT, "store/ios/icon-1024.png"))
    fg = Image.new("RGB", (1024, 500), BG)
    d = ImageDraw.Draw(fg)
    d.rectangle([0, 488, 1024, 500], fill=GREEN)
    fga = fg.convert("RGBA")
    paste_center(fga, art(300), .2, .5)
    d = ImageDraw.Draw(fga)
    d.text((400, 170), "ROPhotoKml", font=font(78), fill=(250, 199, 117, 255))
    d.text((402, 275), "GPS · KML · fotografii georeferențiate", font=font(24), fill=(232, 245, 232, 255))
    save(fga.convert("RGB"), os.path.join(ROOT, "store/android/feature-graphic-1024x500.png"))


if __name__ == "__main__":
    main()
