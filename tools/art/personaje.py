"""Genera el personaje principal en pixel art estilo arcade de los 90 (tipo WrestleFest).

Cómo funciona:
- El cuerpo se modela con volúmenes (elipses y cápsulas) que representan cada
  músculo: trapecios, deltoides, pectorales, abdominales, bíceps, cuádriceps, gemelos.
- Cada volumen se sombrea con una luz 3D y se reduce a 6 tonos por material, con
  cambio de color en las sombras (piel → rojo/violeta) como en el pixel art de arcade.
- Entre músculos se marca una línea interna suave; afuera, un contorno oscuro.

Uso:  python3 tools/art/personaje.py
Salida: assets/personajes/protagonista_*.png y la hoja protagonista_hoja.png
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 104, 132
PISO = 127
OUT = Path(__file__).resolve().parents[2] / "assets" / "personajes"
LUZ = (0.42, -0.62, 0.66)
_n = math.sqrt(sum(v * v for v in LUZ))
LUZ = tuple(v / _n for v in LUZ)
CONTORNO = (28, 10, 22, 255)


def c(h):
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


# Rampas de 6 tonos (brillo → sombra profunda), con cambio de tono en las sombras
PIEL = [c("ffe7b8"), c("f6c58a"), c("e19a62"), c("c0713f"), c("8f4630"), c("5c2527")]
PELO = [c("6a6fa8"), c("3b3f78"), c("24255a"), c("15143d"), c("0c0a28"), c("06041a")]
SHORT = [c("5a5f8e"), c("34386a"), c("22254f"), c("15173a"), c("0d0e29"), c("07071a")]
CELESTE = [c("e8faff"), c("a8e4ff"), c("6cc3f5"), c("3f93d6"), c("2a64a8"), c("1a3f78")]
BLANCO = [c("ffffff"), c("f1f1f6"), c("d4d6e6"), c("a9adc9"), c("7c7fa3"), c("535678")]
AMARILLO = [c("fffbd0"), c("ffe766"), c("f5bf2a"), c("d08a12"), c("995a0c"), c("5e3208")]
OJO = c("1a0d1e")
UMBRALES = (0.88, 0.72, 0.52, 0.30, 0.08)


def tono(dot):
    for i, u in enumerate(UMBRALES):
        if dot > u:
            return i
    return 5


class Lienzo:
    def __init__(self):
        self.px = [[None] * W for _ in range(H)]

    def pintar(self, x, y, color, rampa=None):
        if 0 <= x < W and 0 <= y < H:
            self.px[int(y)][int(x)] = (color, rampa)

    def _poner(self, x, y, nx, ny, dist_borde, rampa, lejos, linea):
        nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
        dot = nx * LUZ[0] + ny * LUZ[1] + nz * LUZ[2]
        ramp = rampa(x, y) if callable(rampa) else rampa
        i = min(5, tono(dot) + lejos)
        if linea is not None and dist_borde < 1.0 and self.px[y][x] is not None:
            i = max(i, linea)
        self.px[y][x] = (ramp[i], ramp)

    def elipse(self, cen, rx, ry, rampa, ang=0.0, lejos=0, linea=3):
        """Volumen elíptico (músculo). `ang` en grados. `linea`: tono del borde interno."""
        cx, cy = cen
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        rr = max(rx, ry) + 1
        for y in range(max(0, int(cy - rr)), min(H, int(cy + rr + 1))):
            for x in range(max(0, int(cx - rr)), min(W, int(cx + rr + 1))):
                dx, dy = x + 0.5 - cx, y + 0.5 - cy
                lx, ly = dx * ca + dy * sa, -dx * sa + dy * ca
                ux, uy = lx / rx, ly / ry
                q = ux * ux + uy * uy
                if q > 1:
                    continue
                nx, ny = ux * ca - uy * sa, ux * sa + uy * ca
                borde = (1 - math.sqrt(q)) * min(rx, ry)
                self._poner(x, y, nx, ny, borde, rampa, lejos, linea)

    def capsula(self, a, b, r1, r2, rampa, lejos=0, linea=3):
        ax, ay = a
        bx, by = b
        vx, vy = bx - ax, by - ay
        ll = vx * vx + vy * vy or 1e-6
        rm = max(r1, r2) + 1
        for y in range(max(0, int(min(ay, by) - rm)), min(H, int(max(ay, by) + rm + 1))):
            for x in range(max(0, int(min(ax, bx) - rm)), min(W, int(max(ax, bx) + rm + 1))):
                px, py = x + 0.5, y + 0.5
                t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / ll))
                cx, cy = ax + t * vx, ay + t * vy
                r = r1 + (r2 - r1) * t
                dx, dy = px - cx, py - cy
                d = math.hypot(dx, dy)
                if d > r:
                    continue
                self._poner(x, y, dx / r, dy / r, r - d, rampa, lejos, linea)

    def contorno(self):
        nuevos = []
        for y in range(H):
            for x in range(W):
                if self.px[y][x] is not None:
                    continue
                if any(0 <= x + dx < W and 0 <= y + dy < H and self.px[y + dy][x + dx] is not None
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    nuevos.append((x, y))
        for x, y in nuevos:
            self.px[y][x] = (CONTORNO, None)

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


def angulo(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


# ---------------------------------------------------------------- poses
# Vista 3/4 mirando a la derecha. "f" = lado de adelante (cerca de la cámara).
GUARDIA = dict(
    cabeza=(55, 17), torso_arriba=(50, 43), torso_abajo=(49, 68),
    hombro_b=(34, 40), codo_b=(29, 60), muneca_b=(41, 52), puno_b=(47, 44),
    hombro_f=(65, 40), codo_f=(74, 60), muneca_f=(79, 46), puno_f=(81, 36),
    cadera_b=(41, 80), rodilla_b=(32, 102), tobillo_b=(27, 123), punta_b=(34, 126),
    cadera_f=(58, 80), rodilla_f=(69, 101), tobillo_f=(74, 122), punta_f=(82, 125),
)
PINA = dict(GUARDIA,
    cabeza=(59, 18), torso_arriba=(53, 43), torso_abajo=(50, 68),
    hombro_b=(37, 40), codo_b=(34, 60), muneca_b=(45, 51), puno_b=(51, 42),
    hombro_f=(68, 40), codo_f=(81, 39), muneca_f=(91, 38), puno_f=(97, 38),
    rodilla_f=(72, 100), tobillo_f=(78, 122), punta_f=(86, 125),
    rodilla_b=(30, 102), tobillo_b=(21, 123), punta_b=(28, 126),
)


# ---------------------------------------------------------------- dibujo
def brazo_superior(L, hom, cod, lejos):
    L.capsula(hom, cod, 6.5, 5.0, PIEL, lejos)
    L.elipse(lerp(hom, cod, 0.5), 8.5, 5.6, PIEL, angulo(hom, cod), lejos)  # bíceps


def antebrazo_y_puno(L, cod, mun, pun, lejos):
    L.elipse(lerp(cod, mun, 0.35), 7.0, 5.2, PIEL, angulo(cod, mun), lejos)
    L.capsula(cod, mun, 5.0, 3.8, PIEL, lejos)
    L.capsula(lerp(cod, mun, 0.6), mun, 4.4, 4.2, BLANCO, lejos)  # vendas
    for k in (0.68, 0.82):
        a = lerp(cod, mun, k)
        L.pintar(a[0], a[1], BLANCO[3 + lejos], BLANCO)
    L.capsula(mun, pun, 5.4, 6.6, CELESTE, lejos)  # guante
    L.elipse(lerp(mun, pun, 0.8), 6.4, 5.2, CELESTE, angulo(mun, pun), lejos)
    v = lerp(mun, pun, 0.3)
    L.capsula((v[0] - 3, v[1]), (v[0] + 3, v[1]), 1.2, 1.2, BLANCO, lejos, linea=None)  # velcro


def pierna(L, cad, rod, tob, pun, lejos):
    L.capsula(cad, rod, 9.0, 6.0, PIEL, lejos)
    L.elipse(lerp(cad, rod, 0.5), 12.0, 7.6, PIEL, angulo(cad, rod), lejos)  # cuádriceps
    L.elipse(lerp(rod, tob, 0.3), 8.0, 5.8, PIEL, angulo(rod, tob), lejos)  # gemelo
    L.capsula(rod, tob, 6.0, 3.8, PIEL, lejos, linea=None)
    L.elipse(rod, 5.0, 4.4, PIEL, 0, lejos)  # rodilla
    L.capsula(tob, pun, 4.0, 3.0, PIEL, lejos)  # pie descalzo


def short(L, P):
    for lado, lejos in (("b", 1), ("f", 0)):
        cad, rod = P[f"cadera_{lado}"], P[f"rodilla_{lado}"]
        L.capsula(cad, lerp(cad, rod, 0.4), 10.5, 9.6, SHORT, lejos)
        a, b = lerp(cad, rod, 0.05), lerp(cad, rod, 0.4)
        off = 7 if lado == "f" else -7
        L.capsula((a[0] + off, a[1]), (b[0] + off, b[1]), 1.4, 1.4, CELESTE, lejos, linea=None)
    L.capsula(P["cadera_b"], P["cadera_f"], 11.5, 11.5, SHORT)
    cx = (P["cadera_b"][0] + P["cadera_f"][0]) / 2
    cy = P["cadera_b"][1] - 9
    L.capsula((cx - 13, cy), (cx + 13, cy), 2.2, 2.2, SHORT, linea=4)  # elástico
    # sol de mayo en la pierna de adelante
    sx, sy = P["cadera_f"][0] + 2, P["cadera_f"][1] + 4
    for ang in range(0, 360, 45):
        r = math.radians(ang)
        L.pintar(sx + round(4 * math.cos(r)), sy + round(4 * math.sin(r)), AMARILLO[2], AMARILLO)
    L.elipse((sx + 0.5, sy + 0.5), 2.6, 2.6, AMARILLO, linea=None)


def torso(L, P):
    ta, tb = P["torso_arriba"], P["torso_abajo"]
    L.capsula(ta, tb, 17.0, 10.5, PIEL, linea=None)  # dorsales / volumen base
    # trapecios y cuello
    L.elipse((ta[0] - 8, ta[1] - 7), 9, 5, PIEL, -20, lejos=1)
    L.elipse((ta[0] + 9, ta[1] - 7), 9, 5, PIEL, 20)
    L.capsula((P["cabeza"][0] - 3, P["cabeza"][1] + 8), (ta[0], ta[1] - 8), 6.5, 7.5, PIEL, linea=None)
    L.elipse((ta[0] + 1, ta[1] - 6), 3.5, 3, PIEL, 0, linea=None)  # nuez / clavícula
    # pectorales
    L.elipse((ta[0] - 8, ta[1] + 6), 11, 8.5, PIEL, 8, lejos=1)
    L.elipse((ta[0] + 8, ta[1] + 6), 11.5, 8.8, PIEL, -8)
    # abdominales (6 pack) y oblicuos
    for fila in range(3):
        y = ta[1] + 18 + fila * 6.2
        x = ta[0] + (tb[0] - ta[0]) * (fila / 3)
        L.elipse((x - 3.5, y), 3.4, 2.9, PIEL, 0, lejos=1)
        L.elipse((x + 3.7, y), 3.6, 2.9, PIEL, 0)
    L.elipse((tb[0] - 9, tb[1] - 8), 3.2, 8, PIEL, 12, lejos=1)
    L.elipse((tb[0] + 9, tb[1] - 8), 3.2, 8, PIEL, -12)
    L.pintar(tb[0], tb[1] + 1, PIEL[4], PIEL)  # ombligo


def cabeza(L, P, vincha=True):
    hx, hy = P["cabeza"]
    L.elipse((hx, hy), 9.5, 11.5, PIEL, 0, linea=None)
    L.elipse((hx + 3, hy + 7), 7.5, 5.8, PIEL, 10, linea=None)  # mandíbula cuadrada
    L.elipse((hx - 6.5, hy + 1.5), 2.2, 3.4, PIEL, 0, lejos=1)  # oreja
    # pelo: volumen con puntas hacia atrás
    L.elipse((hx - 1.5, hy - 6.5), 9.2, 6.2, PELO, -12, linea=None)
    for (dx, dy, r) in ((-9, -6, 3.2), (-7, -11, 3.0), (-2, -13, 3.2), (3, -12.5, 3.0), (7, -9, 2.6)):
        L.elipse((hx + dx, hy + dy), r, r * 0.8, PELO, 0, linea=4)
    for y in range(int(hy - 3), int(hy + 6)):  # degradé rapado atrás
        for x in range(int(hx - 9), int(hx - 4)):
            p = L.px[y][x]
            if p is not None and p[1] is PIEL and (x + y) % 2 == 0:
                L.pintar(x, y, PELO[3], PIEL)
    hx, hy = int(hx), int(hy)
    # cara (mirando a la derecha en 3/4)
    for x in range(hx, hx + 8):  # cejas gruesas, fruncidas
        L.pintar(x, hy - 2 + (1 if x >= hx + 6 else 0), PELO[3], PIEL)
        L.pintar(x, hy - 1 + (1 if x >= hx + 6 else 0), PELO[2] if x % 2 else PELO[3], PIEL)
    for x, y, col in ((hx + 2, hy + 1, BLANCO[1]), (hx + 3, hy + 1, OJO), (hx + 2, hy + 2, PIEL[3]),
                      (hx + 3, hy + 2, PIEL[3]), (hx + 6, hy + 1, BLANCO[2]), (hx + 7, hy + 1, OJO)):
        L.pintar(x, y, col, PIEL)
    for x, y, i in ((hx + 8, hy + 2, 1), (hx + 9, hy + 3, 1), (hx + 9, hy + 4, 2),  # nariz
                    (hx + 8, hy + 5, 4), (hx + 7, hy + 5, 3), (hx + 4, hy + 3, 3)):
        L.pintar(x, y, PIEL[i], PIEL)
    for x in range(hx + 4, hx + 9):  # boca apretada
        L.pintar(x, hy + 8, PIEL[5] if x < hx + 8 else PIEL[4], PIEL)
    L.pintar(hx + 5, hy + 9, PIEL[3], PIEL)
    for (x, y) in ((hx, hy + 9), (hx + 2, hy + 10), (hx + 4, hy + 11), (hx + 6, hy + 11),
                   (hx + 1, hy + 7), (hx + 3, hy + 12), (hx + 8, hy + 10), (hx - 1, hy + 11)):
        L.pintar(x, y, PIEL[4], PIEL)  # barba de pocos días
    if vincha:
        hx, hy = P["cabeza"]
        def franjas(x, y):
            return BLANCO if int(y - (hy - 7)) % 4 in (1, 2) else CELESTE
        for fin in (((hx - 16, hy - 8), (hx - 25, hy - 3)), ((hx - 15, hy - 2), (hx - 22, hy + 6))):
            L.capsula((hx - 8, hy - 5), fin[0], 2.4, 2.0, franjas, lejos=1, linea=4)
            L.capsula(fin[0], fin[1], 2.0, 1.2, franjas, lejos=1, linea=4)
        L.elipse((hx - 8.5, hy - 5), 2.6, 2.8, franjas, 0, lejos=1)  # nudo
        for y in range(int(hy - 7), int(hy - 3)):
            for x in range(int(hx - 10), int(hx + 10)):
                p = L.px[y][x]
                if p is not None and p[1] in (PIEL, PELO):
                    ramp = franjas(x, y)
                    L.pintar(x, y, ramp[1 if x > hx else 2], ramp)


def dibujar(P):
    L = Lienzo()
    # atrás hacia adelante
    brazo_superior(L, P["hombro_b"], P["codo_b"], 1)
    pierna(L, P["cadera_b"], P["rodilla_b"], P["tobillo_b"], P["punta_b"], 1)
    pierna(L, P["cadera_f"], P["rodilla_f"], P["tobillo_f"], P["punta_f"], 0)
    short(L, P)
    L.elipse(P["hombro_b"], 8, 8.5, PIEL, 0, lejos=1)  # deltoides atrás
    torso(L, P)
    cabeza(L, P)
    antebrazo_y_puno(L, P["codo_b"], P["muneca_b"], P["puno_b"], 1)
    brazo_superior(L, P["hombro_f"], P["codo_f"], 0)
    L.elipse(P["hombro_f"], 8.8, 9, PIEL, 0)  # deltoides adelante
    antebrazo_y_puno(L, P["codo_f"], P["muneca_f"], P["puno_f"], 0)
    L.contorno()
    return L.imagen()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("protagonista_*.png"):
        f.unlink()
    frames = [("GUARDIA", dibujar(GUARDIA)), ("PINA", dibujar(PINA))]
    for nombre, img in frames:
        img.save(OUT / f"protagonista_{nombre.lower()}.png")

    esc, margen = 4, 10
    ancho = len(frames) * (W * esc + margen) + margen
    alto = H * esc + margen * 2 + 20
    hoja = Image.new("RGBA", (ancho, alto), c("1c1233"))
    d = ImageDraw.Draw(hoja)
    fuente = ImageFont.load_default(size=16)
    for i, (nombre, img) in enumerate(frames):
        x = margen + i * (W * esc + margen)
        d.rectangle((x, margen, x + W * esc - 1, margen + H * esc - 1), fill=c("3b5aa8"))
        piso = margen + PISO * esc
        d.rectangle((x, piso - 4, x + W * esc - 1, margen + H * esc - 1), fill=c("2a4180"))
        d.ellipse((x + 18 * esc, piso - 3 * esc, x + 90 * esc, piso + 2 * esc), fill=c("1d2e63"))
        hoja.alpha_composite(img.resize((W * esc, H * esc), Image.NEAREST), (x, margen))
        d.text((x + 4, margen + H * esc + 2), nombre, font=fuente, fill=(255, 255, 255))
    hoja.convert("RGB").save(OUT / "protagonista_hoja.png")
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
