#!/usr/bin/env python3
import os, sys, subprocess

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError:
    print("Pillow (PIL) nu este instalat. Se instalează acum prin pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pillow"])
    except Exception as e:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages", "pillow"])
    from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fundal verde-grafit modern (colțuri rotunjite)
    radius = int(size * 0.22)
    bg_color = (13, 26, 13, 255)
    border_color = (34, 197, 94, 255)
    
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=bg_color, outline=border_color, width=max(2, int(size*0.04)))
    
    # Poligon KML verde emerald (simbol GIS parcelă)
    poly_points = [
        (size * 0.15, size * 0.35),
        (size * 0.40, size * 0.15),
        (size * 0.85, size * 0.25),
        (size * 0.80, size * 0.75),
        (size * 0.35, size * 0.85),
        (size * 0.15, size * 0.65)
    ]
    draw.polygon(poly_points, fill=(34, 197, 94, 45), outline=(34, 197, 94, 220), width=max(1, int(size*0.025)))
    
    # Obiectiv cameră foto în centru
    cx, cy = size * 0.5, size * 0.52
    r_outer = size * 0.26
    r_mid = size * 0.18
    r_inner = size * 0.10
    
    # Inel exterior lentilă
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(24, 95, 165, 230), outline=(255, 255, 255, 240), width=max(2, int(size*0.035)))
    # Inel intermediar
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], fill=(15, 40, 70, 255), outline=(250, 199, 117, 200), width=max(1, int(size*0.015)))
    # Interior lentilă
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=(60, 140, 220, 240))
    # Reflexie luminoasă albă
    hl_r = size * 0.04
    draw.ellipse([cx - r_inner*0.4 - hl_r, cy - r_inner*0.4 - hl_r, cx - r_inner*0.4 + hl_r, cy - r_inner*0.4 + hl_r], fill=(255, 255, 255, 230))
    
    # Pin GPS roșu în dreapta-sus
    px, py = size * 0.72, size * 0.30
    pr = size * 0.09
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=max(1, int(size*0.02)))
    # Punct alb în pinul GPS
    dr = size * 0.03
    draw.ellipse([px - dr, py - dr, px + dr, py + dr], fill=(255, 255, 255, 255))
    
    img.save(filename, "PNG")
    print(f"Generated {filename} ({size}x{size})")

def main():
    sizes = [
        (48, "icon-48.png"),
        (72, "icon-72.png"),
        (96, "icon-96.png"),
        (144, "icon-144.png"),
        (192, "icon-192.png"),
        (512, "icon-512.png")
    ]
    for s, fn in sizes:
        create_icon(s, fn)

if __name__ == "__main__":
    main()
