#!/usr/bin/env python3
"""Script to generate placeholder dress PNG images using PIL"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_dress_image(filename, dress_name, body_color, accent_color, category, style="kurta"):
    """Create a simple dress illustration as PNG"""
    img = Image.new("RGBA", (400, 600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bc = body_color
    ac = accent_color

    if style == "kurta":
        # Body / kameez
        draw.polygon([
            (140,80),(260,80),(280,300),(120,300)
        ], fill=bc)
        # Neckline
        draw.ellipse([170,75,230,105], fill=(bc[0]-20,bc[1]-20,bc[2]-20,255))
        # Left sleeve
        draw.polygon([(140,80),(80,180),(100,200),(150,130)], fill=bc)
        # Right sleeve
        draw.polygon([(260,80),(320,180),(300,200),(250,130)], fill=bc)
        # Shalwar
        draw.polygon([(120,300),(280,300),(260,580),(140,580)], fill=(bc[0],bc[1],bc[2],200))
        # Border decoration
        draw.line([(120,300),(280,300)], fill=ac, width=4)
        draw.line([(140,580),(260,580)], fill=ac, width=4)
        # Embroidery dots on neckline
        for x in range(160, 245, 12):
            draw.ellipse([x,88,x+6,94], fill=ac)
        # Bottom border dots
        for x in range(125, 280, 15):
            draw.ellipse([x,295,x+8,303], fill=ac)

    elif style == "lehenga":
        # Choli (top)
        draw.polygon([(155,80),(245,80),(255,180),(145,180)], fill=bc)
        # Neckline
        draw.ellipse([175,75,225,100], fill=(bc[0]-20,bc[1]-20,bc[2]-20,255))
        # Short sleeves
        draw.polygon([(155,80),(110,140),(125,155),(158,110)], fill=bc)
        draw.polygon([(245,80),(290,140),(275,155),(242,110)], fill=bc)
        # Lehenga skirt (flared)
        draw.polygon([(145,180),(255,180),(310,580),(90,580)], fill=bc)
        # Dupatta
        draw.polygon([(100,70),(300,70),(290,120),(110,120)], fill=(bc[0],bc[1],bc[2],160))
        # Gold border on skirt
        draw.line([(145,180),(255,180)], fill=ac, width=5)
        draw.line([(90,580),(310,580)], fill=ac, width=6)
        # Embroidery on skirt
        for i, x in enumerate(range(100, 310, 25)):
            y = 300 + i*8
            if y < 560:
                draw.ellipse([x,y,x+10,y+10], fill=ac)

    elif style == "saree":
        # Blouse
        draw.polygon([(155,80),(245,80),(250,175),(150,175)], fill=bc)
        draw.ellipse([178,75,222,100], fill=(bc[0]-20,bc[1]-20,bc[2]-20,255))
        # Short blouse sleeves
        draw.polygon([(155,85),(115,145),(128,158),(158,112)], fill=bc)
        draw.polygon([(245,85),(285,145),(272,158),(242,112)], fill=bc)
        # Saree drape (petticoat)
        draw.polygon([(150,175),(250,175),(255,580),(145,580)], fill=(bc[0],bc[1],bc[2],200))
        # Pallu (over shoulder)
        draw.polygon([(155,80),(290,60),(295,130),(245,130),(200,100)], fill=(bc[0],bc[1],bc[2],180))
        # Gold border
        draw.line([(145,580),(255,580)], fill=ac, width=7)
        draw.polygon([(280,60),(295,60),(298,580),(283,580)], fill=ac)
        # Zari work
        for y in range(200, 570, 30):
            draw.ellipse([148,y,158,y+10], fill=ac)

    elif style == "anarkali":
        # Top
        draw.polygon([(145,80),(255,80),(270,220),(130,220)], fill=bc)
        draw.ellipse([173,74,227,102], fill=(bc[0]-20,bc[1]-20,bc[2]-20,255))
        # Long sleeves
        draw.polygon([(145,85),(90,200),(108,210),(150,115)], fill=bc)
        draw.polygon([(255,85),(310,200),(292,210),(250,115)], fill=bc)
        # Flared anarkali skirt
        draw.polygon([(130,220),(270,220),(320,580),(80,580)], fill=bc)
        # Dupatta
        draw.polygon([(95,72),(305,72),(298,125),(102,125)], fill=(bc[0],bc[1],bc[2],150))
        # Stone work border
        for x in range(90, 320, 18):
            draw.ellipse([x,570,x+10,580], fill=ac)
        for x in range(130, 270, 15):
            draw.ellipse([x,215,x+8,223], fill=ac)

    # Dress name label at bottom
    draw.rectangle([60,520,340,555], fill=(0,0,0,120))
    # Simple text (no font needed)
    draw.text((200,535), dress_name, fill=(255,215,0,255), anchor="mm")

    return img


# ── CASUAL DRESSES ────────────────────────────────────────────
casual_dresses = [
    ("casual_pink_kurta.png",    "Pink Lawn Kurta",     (232,160,190,255), (255,215,0,255),  "kurta"),
    ("casual_teal_kurta.png",    "Teal Chikankari",     (38,166,154,255),  (255,193,7,255),  "kurta"),
    ("casual_yellow_kurta.png",  "Yellow Printed Kurta",(255,193,7,255),   (233,30,99,255),  "kurta"),
    ("casual_green_kurta.png",   "Mehendi Green Kurta", (76,175,80,255),   (255,235,59,255), "kurta"),
]

# ── FORMAL DRESSES ────────────────────────────────────────────
formal_dresses = [
    ("formal_emerald_anarkali.png", "Emerald Anarkali",  (27,94,32,255),   (255,215,0,255),  "anarkali"),
    ("formal_burgundy_anarkali.png","Burgundy Anarkali", (109,27,45,255),  (244,143,177,255),"anarkali"),
    ("formal_navy_anarkali.png",    "Navy Blue Formal",  (26,35,126,255),  (192,160,96,255), "anarkali"),
    ("formal_purple_anarkali.png",  "Purple Cape Dress", (106,27,154,255), (225,190,231,255),"anarkali"),
]

# ── BRIDAL DRESSES ────────────────────────────────────────────
bridal_dresses = [
    ("bridal_red_lehenga.png",    "Red Bridal Lehenga", (198,40,40,255),  (255,215,0,255),  "lehenga"),
    ("bridal_pink_lehenga.png",   "Pink Bridal Lehenga",(233,30,99,255),  (255,215,0,255),  "lehenga"),
    ("bridal_gold_lehenga.png",   "Gold Tissue Lehenga",(184,134,11,255), (255,249,196,255),"lehenga"),
    ("bridal_red_saree.png",      "Red Banarasi Saree", (198,40,40,255),  (255,215,0,255),  "saree"),
]

os.makedirs("dresses/casual", exist_ok=True)
os.makedirs("dresses/formal", exist_ok=True)
os.makedirs("dresses/bridal", exist_ok=True)

print("Generating dress images...")
for fname, name, bc, ac, style in casual_dresses:
    img = create_dress_image(fname, name, bc, ac, "casual", style)
    img.save(f"dresses/casual/{fname}")
    print(f"  ✓ {fname}")

for fname, name, bc, ac, style in formal_dresses:
    img = create_dress_image(fname, name, bc, ac, "formal", style)
    img.save(f"dresses/formal/{fname}")
    print(f"  ✓ {fname}")

for fname, name, bc, ac, style in bridal_dresses:
    img = create_dress_image(fname, name, bc, ac, "bridal", style)
    img.save(f"dresses/bridal/{fname}")
    print(f"  ✓ {fname}")

print("\n✅ All dress images generated!")
print("Now run: streamlit run app.py")
