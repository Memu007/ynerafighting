"""Genera la hoja del personaje principal en pixel art estilo Sega Genesis.

El personaje se arma sobre un esqueleto (articulaciones) y cada parte del cuerpo
se dibuja como una "cápsula" sombreada con luz 3D, cuantizada a 4 tonos por
material y a la paleta de 9 bits del Genesis. Así, una pose nueva (piña, patada,
recibir golpe) es solo mover las articulaciones.

Uso:  python3 tools/art/personaje.py
Salida: assets/personajes/protagonista_hoja.png y un PNG por pose
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 84, 100
OUT = Path(__file__).resolve().parents[2] / "assets" / "personajes"
NIVELES = [0, 36, 73, 109, 146, 182, 219, 255]
LUZ = (0.55, -0.62, 0.56)  # desde arriba, adelante (el personaje mira a la derecha)
_n = math.sqrt(sum(v * v for v in LUZ))
LUZ = tuple(v / _n for v in LUZ)


def g(r, gg, b):
    q = lambda v: min(NIVELES, key=lambda n: abs(n - v))
    return (q(r), q(gg), q(b), 255)


# Rampas de 4 tonos: [brillo, base, sombra, sombra profunda]
PIEL = [g(236, 170, 120), g(200, 130, 90), g(150, 80, 50), g(100, 45, 35)]
PELO = [g(80, 70, 110), g(40, 35, 70), g(15, 10, 40), g(0, 0, 20)]
SHORT = [g(80, 80, 120), g(40, 40, 80), g(20, 20, 50), g(0, 0, 30)]
CELESTE = [g(200, 240, 255), g(110, 190, 255), g(70, 130, 220), g(40, 80, 160)]
BLANCO = [g(255, 255, 255), g(225, 225, 230), g(160, 160, 200), g(110, 110, 150)]
GUANTE = [g(200, 240, 255), g(90, 170, 240), g(50, 110, 200), g(20, 60, 140)]
JOGGING = [g(190, 190, 200), g(145, 145, 155), g(105, 105, 115), g(70, 70, 85)]
ZAPA = [g(255, 255, 255), g(220, 220, 220), g(150, 150, 170), g(100, 100, 120)]
ROJO = [g(255, 110, 90), g(220, 40, 40), g(150, 20, 30), g(90, 0, 20)]


def tono(dot):
    if dot > 0.78:
        return 0
    if dot > 0.42:
        return 1
    if dot > 0.08:
        return 2
    return 3


class Lienzo:
    def __init__(self):
        # cada píxel: None o (color, rampa)
        self.px = [[None] * W for _ in range(H)]

    def pintar(self, x, y, color, rampa):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = (color, rampa)

    def capsula(self, a, b, r1, r2, rampa, lejos=0, borde=True):
        """Cápsula sombreada de a a b. `rampa` puede ser una función (x, y) -> rampa."""
        ax, ay = a
        bx, by = b
        vx, vy = bx - ax, by - ay
        ll = vx * vx + vy * vy or 1e-6
        rmax = max(r1, r2)
        for y in range(int(min(ay, by) - rmax - 1), int(max(ay, by) + rmax + 2)):
            for x in range(int(min(ax, bx) - rmax - 1), int(max(ax, bx) + rmax + 2)):
                px, py = x + 0.5, y + 0.5
                t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / ll))
                cx, cy = ax + t * vx, ay + t * vy
                r = r1 + (r2 - r1) * t
                dx, dy = px - cx, py - cy
                d = math.hypot(dx, dy)
                if d > r:
                    continue
                nx, ny = dx / r, dy / r
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                dot = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
                ramp = rampa(x, y) if callable(rampa) else rampa
                i = min(3, tono(dot) + lejos)
                # contorno interno: donde esta parte tapa a otra
                if borde and d > r - 1 and 0 <= y < H and 0 <= x < W:
                    debajo = self.px[y][x]
                    if debajo is not None and debajo[1] is not ramp:
                        i = 3
                self.pintar(x, y, ramp[i], ramp)

    def elipse(self, c, rx, ry, rampa, lejos=0):
        cx, cy = c
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                nx, ny = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if nx * nx + ny * ny > 1:
                    continue
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                dot = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
                ramp = rampa(x, y) if callable(rampa) else rampa
                self.pintar(x, y, ramp[min(3, tono(dot) + lejos)], ramp)

    def contorno(self):
        """Contorno exterior de 1 px, oscurecido según el material vecino."""
        nuevos = []
        for y in range(H):
            for x in range(W):
                if self.px[y][x] is not None:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and self.px[ny][nx] is not None:
                        prof = self.px[ny][nx][1][3]
                        col = g(prof[0] * 0.45, prof[1] * 0.4, prof[2] * 0.5 + 10)
                        nuevos.append((x, y, col))
                        break
        for x, y, col in nuevos:
            self.px[y][x] = (col, None)

    def imagen(self):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = img.load()
        for y in range(H):
            for x in range(W):
                if self.px[y][x] is not None:
                    p[x, y] = self.px[y][x][0]
        return img


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ---------------------------------------------------------------- poses
# Proporciones heroicas de arcade: hombros anchos, brazos y piernas gruesos,
# guardia alta y postura abierta. Piso en y=96.
GUARDIA = dict(
    cabeza=(41, 14), cuello=(40, 23), pecho=(38, 33), cintura=(37, 50),
    hombro_f=(46, 29), codo_f=(52, 43), muneca_f=(56, 33), puno_f=(58, 25),
    hombro_b=(30, 30), codo_b=(32, 45), muneca_b=(42, 39), puno_b=(47, 33),
    cadera_f=(43, 57), rodilla_f=(53, 73), tobillo_f=(56, 91), punta_f=(62, 94),
    cadera_b=(32, 57), rodilla_b=(26, 74), tobillo_b=(21, 91), punta_b=(27, 94),
)
PINA = dict(GUARDIA,
    cabeza=(45, 15), cuello=(43, 24), pecho=(40, 33),
    hombro_f=(49, 29), codo_f=(60, 28), muneca_f=(69, 27), puno_f=(75, 27),
    hombro_b=(32, 30), codo_b=(36, 44), muneca_b=(45, 35), puno_b=(48, 27),
    rodilla_f=(55, 72), tobillo_f=(59, 91), punta_f=(65, 94),
    rodilla_b=(24, 74), tobillo_b=(15, 91), punta_b=(21, 94),
)


# ---------------------------------------------------------------- looks
def vincha(L, hx, hy):
    """Vincha albiceleste con tiras al viento."""
    def franjas(x, y):
        return BLANCO if int(y - (hy - 5)) % 3 == 1 else CELESTE
    for tira in (((hx - 6, hy - 4), (hx - 13, hy - 5), (hx - 18, hy - 2)),
                 ((hx - 6, hy - 3), (hx - 12, hy + 1), (hx - 16, hy + 5))):
        L.capsula(tira[0], tira[1], 1.8, 1.5, franjas, lejos=1, borde=False)
        L.capsula(tira[1], tira[2], 1.5, 1.0, franjas, lejos=1, borde=False)
    for y in range(int(hy - 5), int(hy - 2)):
        for x in range(int(hx - 7), int(hx + 7)):
            c = L.px[y][x]
            if c is not None and c[1] in (PIEL, PELO):
                ramp = franjas(x, y)
                L.pintar(x, y, ramp[1] if x > hx - 2 else ramp[2], ramp)


def dibujar(pose, look):
    L = Lienzo()
    P = pose
    peleador = look != "calle"
    pierna = PIEL if peleador else JOGGING
    pie = PIEL if peleador else ZAPA
    torso = PIEL if peleador else BLANCO  # de calle: musculosa blanca

    # --- brazo de atrás (hombro y brazo, detrás del cuerpo)
    L.capsula(P["hombro_b"], P["codo_b"], 4.8, 4.0, PIEL, lejos=1)

    # --- piernas
    for lado, lejos in (("b", 1), ("f", 0)):
        cad, rod, tob, pun = (P[f"cadera_{lado}"], P[f"rodilla_{lado}"],
                              P[f"tobillo_{lado}"], P[f"punta_{lado}"])
        L.capsula(cad, rod, 7.2, 5.2, pierna, lejos)
        L.capsula(rod, lerp(rod, tob, 0.35), 5.2, 5.0, pierna, lejos)  # gemelo
        L.capsula(lerp(rod, tob, 0.35), tob, 5.0, 3.4, pierna, lejos)
        L.capsula(tob, pun, 3.0 if not peleador else 2.6, 2.2, pie, lejos)
        if not peleador:
            L.capsula(lerp(rod, tob, 0.85), tob, 4.0, 3.8, pierna, lejos)  # puño del jogging
            ax, ay = lerp(tob, pun, 0.35)
            for k in range(3):  # detalle celeste en la zapa
                L.pintar(int(ax) + k, int(ay), CELESTE[1 + lejos], CELESTE)
        else:
            L.capsula(cad, lerp(cad, rod, 0.5), 8.0, 7.4, SHORT, lejos)
            a0, a1 = lerp(cad, rod, 0.1), lerp(cad, rod, 0.5)
            L.capsula(a0, a1, 1.1, 1.1, CELESTE, lejos, borde=False)  # franja lateral
    cad_c = lerp(P["cadera_b"], P["cadera_f"], 0.5)
    L.capsula(P["cadera_b"], P["cadera_f"], 8.2 if peleador else 7.6,
              8.2 if peleador else 7.6, SHORT if peleador else JOGGING)
    if peleador:  # sol de mayo en el short
        sx, sy = int(P["cadera_f"][0]) + 3, int(P["cadera_f"][1]) + 5
        amarillo = [g(255, 255, 150), g(255, 219, 36), g(219, 146, 0), g(146, 73, 0)]
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (2, 1), (0, -1), (1, 2)):
            L.pintar(sx + dx, sy + dy, amarillo[1 if (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)) else 2], amarillo)

    # --- torso ancho (en V)
    L.capsula(P["pecho"], P["cintura"], 11.0, 7.6, torso)
    L.capsula(P["cuello"], P["pecho"], 4.0, 4.6, PIEL, borde=False)
    L.elipse(P["hombro_b"], 5.4, 5.0, PIEL, lejos=1)  # deltoides
    cx, cy = int(P["pecho"][0]), int(P["pecho"][1])
    if peleador:
        s2, s3 = PIEL[2], PIEL[3]
        for x in range(cx - 7, cx + 9):  # borde inferior de pectorales
            curva = 0 if abs(x - cx) < 2 else (1 if abs(x - cx) < 6 else 0)
            L.pintar(x, cy + 6 + curva, s3 if abs(x - cx) > 1 else s2, PIEL)
        for y in range(cy - 1, cy + 7):  # esternón
            L.pintar(cx, y, s2, PIEL)
        for fila in (cy + 10, cy + 13, cy + 16):  # abdominales (6 pack)
            for x in (cx - 3, cx - 2, cx + 2, cx + 3):
                L.pintar(x, fila, s2, PIEL)
        for y in range(cy + 8, cy + 18):  # línea alba
            L.pintar(cx, y, s2, PIEL)
        for y in range(cy + 9, cy + 18):  # oblicuos
            L.pintar(cx - 6, y, s3, PIEL)
        L.capsula((cad_c[0] - 8, cad_c[1] - 6), (cad_c[0] + 8, cad_c[1] - 6), 1.6, 1.6, SHORT)
    else:
        # musculosa: brazos y hombros al aire, escote
        for x in range(cx - 3, cx + 4):
            L.pintar(x, cy - 5 + abs(x - cx) // 2, PIEL[2], PIEL)
        L.capsula((cad_c[0] - 8, cad_c[1] - 6), (cad_c[0] + 8, cad_c[1] - 6), 1.6, 1.6, JOGGING)
    L.elipse(P["hombro_f"], 5.8, 5.2, PIEL)  # deltoides de adelante

    # --- cabeza
    hx, hy = P["cabeza"]
    L.elipse((hx, hy), 6.0, 7.4, PIEL)
    L.capsula((hx - 1, hy + 4), (hx + 3.5, hy + 5.5), 3.4, 3.0, PIEL, borde=False)  # mandíbula
    L.capsula((hx - 4.5, hy - 3.5), (hx + 3, hy - 6), 3.6, 3.0, PELO, borde=False)
    for (dx, dy) in ((-5, -8), (-3, -10), (-1, -11), (1, -11), (3, -10), (5, -8), (-7, -6)):
        L.pintar(int(hx + dx), int(hy + dy), PELO[1], PELO)
        L.pintar(int(hx + dx), int(hy + dy) + 1, PELO[1], PELO)
    hx, hy = int(hx), int(hy)
    L.pintar(hx - 3, hy + 1, PIEL[2], PIEL)  # oreja
    L.pintar(hx - 3, hy + 2, PIEL[3], PIEL)
    L.pintar(hx - 2, hy + 1, PIEL[3], PIEL)
    for x in range(hx + 1, hx + 6):  # ceja gruesa, fruncida
        L.pintar(x, hy - 1 + (1 if x == hx + 5 else 0), PELO[2], PIEL)
    L.pintar(hx + 3, hy + 1, g(255, 255, 255), PIEL)  # ojo
    L.pintar(hx + 4, hy + 1, g(20, 10, 30), PIEL)
    L.pintar(hx + 7, hy + 2, PIEL[1], PIEL)  # nariz
    L.pintar(hx + 7, hy + 3, PIEL[2], PIEL)
    L.pintar(hx + 6, hy + 4, PIEL[3], PIEL)
    for x in (hx + 4, hx + 5, hx + 6):  # boca seria
        L.pintar(x, hy + 6, PIEL[3], PIEL)
    for (x, y) in ((hx + 1, hy + 7), (hx + 3, hy + 8), (hx + 5, hy + 8), (hx + 2, hy + 6)):
        L.pintar(x, y, PIEL[2], PIEL)  # barba de pocos días
    if peleador:
        vincha(L, hx, hy)

    # --- brazos (adelante): antebrazos y puños en guardia
    for lado, lejos in (("b", 1), ("f", 0)):
        hom, cod, mun, pun = (P[f"hombro_{lado}"], P[f"codo_{lado}"],
                              P[f"muneca_{lado}"], P[f"puno_{lado}"])
        if lado == "f":
            L.capsula(hom, cod, 5.0, 4.2, PIEL, lejos)  # bíceps
        L.capsula(cod, mun, 4.4, 3.4, PIEL, lejos)  # antebrazo
        if peleador:
            L.capsula(lerp(cod, mun, 0.55), mun, 3.8, 3.5, BLANCO, lejos)  # vendas
            L.capsula(mun, pun, 4.6, 5.4, GUANTE, lejos)
            px_, py_ = lerp(mun, pun, 0.5)
            L.pintar(int(px_), int(py_), BLANCO[1 + lejos], BLANCO)  # velcro
            L.pintar(int(px_), int(py_) + 1, BLANCO[1 + lejos], BLANCO)
        else:
            L.capsula(mun, pun, 3.6, 4.4, PIEL, lejos)

    L.contorno()
    return L.imagen()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frames = [
        ("CALLE", dibujar(GUARDIA, "calle")),
        ("GUARDIA", dibujar(GUARDIA, "peleador")),
        ("PINA", dibujar(PINA, "peleador")),
    ]
    for nombre, img in frames:
        img.save(OUT / f"protagonista_{nombre.lower()}.png")

    esc, margen = 5, 8
    fondo = [g(40, 20, 70), g(60, 30, 90)]
    ancho = len(frames) * (W * esc + margen) + margen
    alto = H * esc + margen * 2 + 24
    hoja = Image.new("RGBA", (ancho, alto), fondo[0])
    d = ImageDraw.Draw(hoja)
    fuente = ImageFont.load_default(size=16)
    for i, (nombre, img) in enumerate(frames):
        x = margen + i * (W * esc + margen)
        d.rectangle((x, margen, x + W * esc - 1, margen + H * esc - 1), fill=fondo[1])
        piso = margen + 96 * esc
        d.ellipse((x + 14 * esc, piso - 2 * esc, x + 70 * esc, piso + 2 * esc), fill=fondo[0])
        hoja.alpha_composite(img.resize((W * esc, H * esc), Image.NEAREST), (x, margen))
        d.text((x + 4, margen + H * esc + 4), nombre, font=fuente, fill=(255, 255, 255))
    hoja.convert("RGB").save(OUT / "protagonista_hoja.png")
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
