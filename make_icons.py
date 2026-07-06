from PIL import Image, ImageDraw

BEIHILFE = (178, 107, 24)   # Bernstein
PKV      = (14, 124, 124)   # Petrol
BRAND    = (14, 92, 85)

def make(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(size * (0.14 if maskable else 0.0))
    box = size - 2 * pad
    r = int(box * 0.22)

    # abgerundetes Quadrat mit diagonaler Zweiteilung (Beihilfe | PKV)
    tile = Image.new("RGBA", (box, box), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, box - 1, box - 1], radius=r, fill=BEIHILFE)
    # untere Dreieckshälfte = PKV
    td.polygon([(0, box), (box, box), (box, 0)], fill=PKV)
    # abgerundete Maske erneut anwenden
    mask = Image.new("L", (box, box), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, box - 1, box - 1], radius=r, fill=255)
    img.paste(tile, (pad, pad), mask)

    # feiner Trennstrich + Häkchen-Motiv (Erstattung erledigt)
    d = ImageDraw.Draw(img)
    cx = pad + box * 0.5
    cy = pad + box * 0.5
    lw = max(2, int(size * 0.045))
    d.line([(pad + box * 0.30, cy + box * 0.02),
            (pad + box * 0.45, cy + box * 0.17),
            (pad + box * 0.72, cy - box * 0.20)],
           fill=(255, 255, 255, 235), width=lw, joint="curve")
    return img

for s in (192, 512):
    make(s).save(f"icon-{s}.png")
make(512, maskable=True).save("icon-512-maskable.png")
print("Icons erstellt: icon-192.png, icon-512.png, icon-512-maskable.png")
