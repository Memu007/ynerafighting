"""Genera un mockup de pelea (escena 'Estación') en pixel art estilo Sega Genesis.

Todo se dibuja por código a la resolución nativa (320x224) y se escala x3.
Los colores se cuantizan a la paleta de 9 bits del Genesis (8 niveles por canal).

Uso:  python3 tools/art/mockup_estacion.py
Salida: assets/mockups/escena_estacion.png y assets/mockups/protagonista.png
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 320, 224
ESCALA = 3
OUT = Path(__file__).resolve().parents[2] / "assets" / "mockups"

NIVELES = [0, 36, 73, 109, 146, 182, 219, 255]


def g(r, gg, b):
    """Cuantiza un color a la paleta de 9 bits del Genesis."""
    q = lambda v: min(NIVELES, key=lambda n: abs(n - v))
    return (q(r), q(gg), q(b), 255)


def oscurecer(c, f=0.65):
    return g(int(c[0] * f), int(c[1] * f), int(c[2] * f))


CONTORNO = g(20, 12, 30)


# ---------------------------------------------------------------- peleadores
def peleador(piel, piel_s, pelo, remera, pantalon, zapas, capucha=False):
    """Peleador en guardia mirando a la derecha. Devuelve imagen RGBA 40x64."""
    img = Image.new("RGBA", (40, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = d.rectangle
    remera_s, pant_s = oscurecer(remera), oscurecer(pantalon)

    # piernas (pierna de atrás más oscura)
    r((11, 40, 15, 58), fill=pant_s)
    r((10, 58, 16, 60), fill=oscurecer(zapas))
    r((20, 40, 24, 50), fill=pantalon)
    r((22, 50, 26, 58), fill=pantalon)
    r((22, 58, 29, 60), fill=zapas)
    r((11, 38, 24, 42), fill=pantalon)  # cadera
    # brazo de atrás
    r((12, 20, 15, 28), fill=remera_s if capucha else piel_s)
    r((15, 25, 22, 28), fill=piel_s)
    r((21, 18, 25, 22), fill=piel_s)  # puño atrás
    # torso
    r((12, 18, 23, 38), fill=remera)
    r((12, 18, 14, 38), fill=remera_s)
    if capucha:
        r((13, 30, 22, 33), fill=remera_s)  # bolsillo canguro
    # cabeza
    r((16, 15, 20, 18), fill=piel_s)  # cuello
    r((14, 5, 24, 15), fill=piel)
    r((14, 5, 16, 15), fill=piel_s)
    r((22, 9, 22, 10), fill=CONTORNO)  # ojo
    r((22, 13, 24, 13), fill=piel_s)  # boca
    if capucha:
        r((12, 3, 21, 8), fill=remera)
        r((12, 3, 15, 16), fill=remera_s)
    else:
        r((13, 3, 24, 6), fill=pelo)
        r((13, 3, 15, 10), fill=pelo)
    # brazo de adelante (guardia)
    r((20, 20, 23, 27), fill=remera if capucha else piel)
    r((23, 24, 29, 27), fill=piel)
    r((27, 17, 31, 22), fill=piel)  # puño adelante
    r((27, 17, 31, 17), fill=g(255, 255, 255))  # brillo del puño

    # contorno de 1 px alrededor de todo lo opaco
    px = img.load()
    borde = []
    for y in range(64):
        for x in range(40):
            if px[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 40 and 0 <= ny < 64 and px[nx, ny][3] and px[nx, ny] != CONTORNO:
                        borde.append((x, y))
                        break
    for p in borde:
        px[p] = CONTORNO
    return img


# ---------------------------------------------------------------- escenario
def cielo(d):
    bandas = [g(40, 20, 80), g(90, 30, 110), g(160, 50, 110), g(220, 90, 90),
              g(250, 150, 70), g(255, 210, 110)]
    alto = 16
    for i, c in enumerate(bandas):
        y0 = i * alto
        d.rectangle((0, y0, W, y0 + alto), fill=c)
        if i + 1 < len(bandas):  # dithering entre bandas
            for y in range(y0 + alto - 3, y0 + alto + 1):
                for x in range((y % 2), W, 2):
                    d.point((x, y), fill=bandas[i + 1])
    d.ellipse((230, 70, 262, 102), fill=g(255, 240, 180))  # sol


def monoblocks(d, rng):
    base = g(60, 30, 80)
    x = -10
    while x < W:
        w, h = rng.randint(28, 44), rng.randint(40, 70)
        d.rectangle((x, 118 - h, x + w, 118), fill=base)
        for wy in range(118 - h + 4, 116, 6):
            for wx in range(x + 3, x + w - 2, 5):
                if rng.random() < 0.35:
                    d.rectangle((wx, wy, wx + 1, wy + 2), fill=g(255, 220, 110))
        x += w + rng.randint(2, 10)


def casas(d, rng):
    ladrillo, ladrillo_s = g(180, 80, 50), g(130, 55, 40)
    revoque = g(200, 190, 170)
    x = 0
    while x < W:
        w, h = rng.randint(36, 56), rng.randint(26, 40)
        top = 126 - h
        color = ladrillo if rng.random() < 0.6 else revoque
        d.rectangle((x, top, x + w, 126), fill=color)
        if color == ladrillo:
            for y in range(top + 2, 126, 3):
                off = 0 if (y // 3) % 2 else 2
                for bx in range(x + off, x + w, 4):
                    d.point((bx, y), fill=ladrillo_s)
        # hierros del segundo piso sin terminar
        for hx in range(x + 3, x + w - 1, 6):
            d.line((hx, top - 5, hx, top), fill=g(110, 70, 60))
        # tanque de agua
        if rng.random() < 0.7:
            tx = x + rng.randint(4, max(5, w - 14))
            d.rectangle((tx, top - 10, tx + 9, top - 1), fill=g(30, 40, 60))
            d.rectangle((tx + 1, top - 12, tx + 8, top - 10), fill=g(50, 60, 90))
        # ventana con reja
        wx = x + w // 2 - 4
        d.rectangle((wx, top + 8, wx + 8, top + 16), fill=g(40, 40, 70))
        for rx in range(wx + 2, wx + 8, 2):
            d.line((rx, top + 8, rx, top + 16), fill=g(20, 20, 20))
        x += w + 1


def tren_y_anden(d):
    # andén
    d.rectangle((0, 126, W, 150), fill=g(110, 110, 120))
    d.rectangle((0, 126, W, 127), fill=g(255, 220, 60))  # línea amarilla
    # vagón (detrás del andén, se ve la parte de arriba)
    d.rectangle((20, 98, 300, 128), fill=g(180, 185, 190))
    d.rectangle((20, 118, 300, 121), fill=g(40, 90, 180))
    for vx in range(30, 290, 22):
        d.rectangle((vx, 103, vx + 14, 113), fill=g(50, 60, 80))
        d.rectangle((vx + 1, 104, vx + 4, 106), fill=g(180, 200, 230))
    d.rectangle((20, 98, 300, 99), fill=g(110, 115, 120))
    # techo del andén
    d.rectangle((0, 84, W, 88), fill=g(70, 40, 40))
    for cx in range(8, W, 64):
        d.rectangle((cx, 88, cx + 2, 126), fill=g(60, 50, 50))


def vereda(d):
    d.rectangle((0, 150, W, H), fill=g(146, 146, 146))
    for y in range(150, H, 12):
        d.line((0, y, W, y), fill=g(109, 109, 109))
        off = 0 if (y // 12) % 2 else 12
        for x in range(off, W, 24):
            d.line((x, y, x, y + 11), fill=g(109, 109, 109))
    d.line((40, 170, 52, 176), fill=g(80, 80, 80))  # rajadura
    d.line((52, 176, 56, 184), fill=g(80, 80, 80))


def cartel(d, fuente):
    d.rectangle((268, 120, 269, 166), fill=g(80, 80, 80))
    d.rectangle((238, 110, 300, 128), fill=g(0, 110, 60))
    d.rectangle((239, 111, 299, 127), outline=g(255, 255, 255))
    d.text((242, 112), "V. CELINA", font=fuente, fill=g(255, 255, 255))


# ---------------------------------------------------------------- interfaz
def hud(d, fuente):
    for x0, lado in ((8, 1), (184, -1)):
        d.rectangle((x0, 8, x0 + 128, 16), fill=CONTORNO)
        d.rectangle((x0 + 1, 9, x0 + 127, 15), fill=g(180, 30, 30))
        vida = 104 if lado == 1 else 72
        if lado == 1:
            d.rectangle((x0 + 1, 9, x0 + vida, 15), fill=g(255, 220, 0))
        else:
            d.rectangle((x0 + 127 - vida, 9, x0 + 127, 15), fill=g(255, 220, 0))
        d.rectangle((x0, 19, x0 + 60, 22) if lado == 1 else (x0 + 68, 19, x0 + 128, 22),
                    fill=g(0, 180, 220))
    d.text((8, 24), "NAHUEL", font=fuente, fill=g(255, 255, 255))
    d.text((276, 24), "CHORRO", font=fuente, fill=g(255, 255, 255))
    d.rectangle((148, 5, 172, 21), fill=CONTORNO)
    d.text((153, 7), "60", font=fuente, fill=g(255, 220, 0))
    d.text((126, 196), "ROUND 1", font=fuente, fill=g(255, 255, 255))


def main():
    rng = random.Random(7)
    img = Image.new("RGBA", (W, H), g(0, 0, 0))
    d = ImageDraw.Draw(img)
    fuente = ImageFont.load_default()
    cielo(d)
    monoblocks(d, rng)
    casas(d, rng)
    tren_y_anden(d)
    vereda(d)
    cartel(d, fuente)

    nahuel = peleador(piel=g(219, 146, 109), piel_s=g(182, 109, 73), pelo=g(30, 20, 20), remera=g(255, 255, 255),
                      pantalon=g(40, 60, 140), zapas=g(230, 230, 230))
    chorro = peleador(piel=g(182, 109, 73), piel_s=g(146, 73, 36), pelo=g(20, 20, 20), remera=g(60, 60, 70),
                      pantalon=g(30, 30, 40), zapas=g(255, 255, 255), capucha=True)
    chorro = chorro.transpose(Image.FLIP_LEFT_RIGHT)
    for spr, x in ((nahuel, 96), (chorro, 184)):
        sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).ellipse((x + 6, 186, x + 34, 191), fill=(0, 0, 0, 110))
        img.alpha_composite(sombra)
        img.alpha_composite(spr, (x, 128))
    hud(d, fuente)

    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").resize((W * ESCALA, H * ESCALA), Image.NEAREST).save(OUT / "escena_estacion.png")

    hoja = Image.new("RGBA", (84, 68), g(60, 30, 80))
    hoja.alpha_composite(nahuel, (2, 2))
    hoja.alpha_composite(chorro, (42, 2))
    hoja.convert("RGB").resize((84 * 6, 68 * 6), Image.NEAREST).save(OUT / "protagonista.png")
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
