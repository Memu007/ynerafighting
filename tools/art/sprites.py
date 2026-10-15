"""Genera las hojas de sprites de todos los peleadores a partir del modelo volumétrico de personaje.py.

Cada personaje se describe con rampas de color (piel, pelo, ropa) y opciones de vestimenta tomadas
de su retrato en assets/portraits. Cada hoja es una tira horizontal de celdas de 136×132 px con el
mismo orden de poses (ORDEN_POSES), que index.html replica para elegir el cuadro.

Uso:  python3 tools/art/sprites.py            # genera assets/sprites/*.png y la hoja de revisión
      python3 tools/art/sprites.py lautaro    # sólo un personaje
"""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import personaje as base  # noqa: E402

CW, CH = 136, 132          # celda de la hoja; el piso queda en y=127 y el torso centrado en x≈66
DX = 16                    # desplazamiento de las poses de personaje.py (pensadas para 104 px)
PISO = 127
OUT = Path(__file__).resolve().parents[2] / "assets" / "sprites"
base.W, base.H = CW, CH    # Lienzo usa las globales del módulo al dibujar

ORDEN_POSES = ["guardia", "paso1", "paso2", "pina", "patada", "bloqueo", "golpe", "ko", "especial", "sentado", "senala"]
# Poses de entrenamiento: sólo las tienen Lautaro (ring) y Osvaldo; van después de las comunes para no mover índices.
POSES_ENTRENAMIENTO = ["pesas_abajo", "pesas_arriba", "soga", "salto", "manoplas"]
CON_ENTRENAMIENTO = ("lautaro", "osvaldo")


# ---------------------------------------------------------------- color
def hexa(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rampa(h, sombra=(0.92, 0.72, 1.0)):
    """Seis tonos desde brillo a sombra profunda; las sombras viran al tono `sombra` (rojizo/violeta)."""
    r, g, b = hexa(h)
    tonos = []
    for f, mezcla in ((1.38, 0.0), (1.16, 0.0), (1.0, 0.0), (0.78, 0.25), (0.56, 0.45), (0.36, 0.6)):
        cr, cg, cb = (min(255, r * f), min(255, g * f), min(255, b * f))
        cr = cr * (1 - mezcla) + cr * sombra[0] * mezcla
        cg = cg * (1 - mezcla) + cg * sombra[1] * mezcla
        cb = cb * (1 - mezcla) + cb * sombra[2] * mezcla
        tonos.append((int(cr), int(cg), int(cb), 255))
    return tonos


BLANCO, CELESTE, AMARILLO, OJO = base.BLANCO, base.CELESTE, base.AMARILLO, base.OJO
ZAPATILLA = rampa("#e9e6dc")
SUELA = rampa("#3a3a44")


# ---------------------------------------------------------------- personajes
def spec(**k):
    d = dict(piel="#e19a62", pelo="#24255a", estilo="corto", top="nada", top_color="#34386a", short="#34386a",
             guantes="#6cc3f5", pantalon=None, cabeza=None, gorra_color="#2c4268", barba=False, bigote=False,
             toalla=False, mayor=False, musculo=1.0)
    d.update(k)
    return d


PERSONAJES = {
    # Lautaro en el ring: torso desnudo y vincha, como en la hoja aprobada.
    "lautaro": spec(piel="#e19a62", pelo="#24255a", estilo="corto", cabeza="vincha", short="#34386a", guantes="#6cc3f5"),
    # Lautaro en la calle: buzo gris con capucha, gorra azul, jean y zapatillas, como en el retrato.
    "lautaro_calle": spec(piel="#e19a62", pelo="#24255a", estilo="corto", cabeza="gorra", gorra_color="#2c4268",
                          top="buzo", top_color="#5a6068", pantalon="#2f4a78", guantes=None),
    "kevin": spec(piel="#d9813d", pelo="#1a120b", estilo="rapado", cabeza="gorra_atras", gorra_color="#d62424",
                  top="musculosa", top_color="#1647a4", pantalon="#20242e", guantes=None),
    "braian": spec(piel="#c96d3d", pelo="#1f1510", estilo="rapado", cabeza="gorra", gorra_color="#178a3d",
                   top="campera", top_color="#1f5f33", pantalon="#4a4f58", guantes=None, barba=True),
    "custodio": spec(piel="#a85b30", pelo="#251612", estilo="rapado", top="musculosa", top_color="#433f34",
                     pantalon="#2a2a30", guantes=None, barba=True, musculo=1.12),
    "tito": spec(piel="#e48845", pelo="#6b2c10", estilo="ondulado", top="musculosa", top_color="#f55c02", short="#2b2b33", guantes="#d32921"),
    "rulo": spec(piel="#cf6d32", pelo="#2d1611", estilo="rulos", top="musculosa", top_color="#632785", short="#1d1d2a", guantes="#f5bf2a"),
    "nico": spec(piel="#b7612a", pelo="#0d090b", estilo="corto", top="musculosa", top_color="#017279", short="#f1f1f6", guantes="#d32921"),
    "marcos": spec(piel="#bc6a37", pelo="#8a5a3a", estilo="pelado", top="musculosa", top_color="#17a0a8", short="#2b2b33", guantes="#1647a4"),
    "sergio": spec(piel="#c66b37", pelo="#552610", estilo="ondulado", top="musculosa", top_color="#102f52", short="#8f1d1d", guantes="#f1f1f6"),
    "puma": spec(piel="#ae5c2c", pelo="#7a5a40", estilo="canoso", top="musculosa", top_color="#fbaa07", short="#1d1d2a", guantes="#d32921", musculo=1.1),
    "silva": spec(piel="#964e29", pelo="#170d0b", estilo="rapado", top="musculosa", top_color="#1f8a3a", short="#f1f1f6", guantes="#f5bf2a"),
    "petrov": spec(piel="#dd8f5c", pelo="#32201c", estilo="corto", top="musculosa", top_color="#9b1513", short="#1d2a5a", guantes="#f1f1f6", musculo=1.08),
    "lee": spec(piel="#d9843c", pelo="#1c1c25", estilo="corto", top="musculosa", top_color="#049764", short="#1d1d2a", guantes="#1647a4"),
    "henderson": spec(piel="#ec9765", pelo="#e2b05a", estilo="corto", top="musculosa", top_color="#d32921", short="#1d2a5a", guantes="#f5bf2a", barba=True, musculo=1.15),
    "osvaldo": spec(piel="#bd7249", pelo="#b9bcc2", estilo="canoso", top="musculosa", top_color="#2a2a30", pantalon="#3a3f4a",
                    guantes=None, bigote=True, toalla=True, mayor=True, musculo=0.95),
}


# ---------------------------------------------------------------- poses (coordenadas de personaje.py, 104 px de ancho)
G = base.GUARDIA
POSES = {
    "guardia": G,
    "paso1": dict(G, rodilla_b=(38, 102), tobillo_b=(44, 123), punta_b=(52, 126), rodilla_f=(62, 102), tobillo_f=(60, 123), punta_f=(68, 126)),
    "paso2": dict(G, rodilla_b=(26, 102), tobillo_b=(18, 123), punta_b=(26, 126), rodilla_f=(74, 100), tobillo_f=(82, 122), punta_f=(90, 125)),
    "pina": base.PINA,
    "patada": dict(G, cabeza=(49, 20), torso_arriba=(46, 45), torso_abajo=(48, 70),
                   hombro_b=(31, 42), codo_b=(27, 62), muneca_b=(38, 54), puno_b=(44, 46),
                   hombro_f=(61, 42), codo_f=(68, 60), muneca_f=(74, 48), puno_f=(76, 40),
                   cadera_b=(42, 82), rodilla_b=(34, 104), tobillo_b=(30, 124), punta_b=(38, 127),
                   cadera_f=(56, 78), rodilla_f=(80, 70), tobillo_f=(102, 62), punta_f=(112, 60)),
    "bloqueo": dict(G, cabeza=(55, 20),
                    hombro_b=(34, 40), codo_b=(40, 58), muneca_b=(52, 40), puno_b=(56, 28),
                    hombro_f=(65, 40), codo_f=(76, 56), muneca_f=(74, 38), puno_f=(70, 26)),
    "golpe": dict(G, cabeza=(44, 19), torso_arriba=(47, 45), torso_abajo=(50, 69),
                  hombro_b=(32, 42), codo_b=(20, 56), muneca_b=(14, 44), puno_b=(10, 38),
                  hombro_f=(62, 42), codo_f=(76, 52), muneca_f=(88, 44), puno_f=(94, 40),
                  rodilla_b=(28, 104), tobillo_b=(22, 124), punta_b=(30, 127),
                  rodilla_f=(66, 102), tobillo_f=(66, 123), punta_f=(74, 126)),
    "especial": dict(G, cabeza=(64, 20), torso_arriba=(58, 44), torso_abajo=(52, 69),
                     hombro_b=(40, 42), codo_b=(30, 58), muneca_b=(26, 48), puno_b=(28, 40),
                     hombro_f=(72, 40), codo_f=(88, 38), muneca_f=(100, 36), puno_f=(108, 36),
                     cadera_b=(42, 80), rodilla_b=(26, 104), tobillo_b=(14, 124), punta_b=(22, 127),
                     cadera_f=(62, 80), rodilla_f=(80, 100), tobillo_f=(88, 122), punta_f=(96, 125)),
    # Tirado de espaldas, cabeza a la izquierda. Se dibuja en coordenadas de celda (ya con DX).
    "ko": dict(cabeza=(16, 104), torso_arriba=(42, 108), torso_abajo=(62, 110),
               hombro_b=(40, 96), codo_b=(26, 86), muneca_b=(12, 80), puno_b=(4, 76),
               hombro_f=(40, 118), codo_f=(54, 124), muneca_f=(66, 122), puno_f=(72, 120),
               cadera_b=(72, 102), rodilla_b=(92, 100), tobillo_b=(110, 104), punta_b=(114, 96),
               cadera_f=(74, 114), rodilla_f=(94, 116), tobillo_f=(112, 118), punta_f=(118, 110), tirado=True),
    "sentado": dict(cabeza=(50, 36), torso_arriba=(46, 62), torso_abajo=(43, 84),
                    hombro_b=(31, 59), codo_b=(30, 78), muneca_b=(42, 92), puno_b=(48, 96),
                    hombro_f=(61, 59), codo_f=(66, 78), muneca_f=(72, 92), puno_f=(76, 96),
                    cadera_b=(38, 96), rodilla_b=(60, 98), tobillo_b=(58, 122), punta_b=(66, 126),
                    cadera_f=(46, 96), rodilla_f=(70, 96), tobillo_f=(68, 122), punta_f=(76, 126)),
    "senala": dict(G, hombro_b=(34, 40), codo_b=(30, 62), muneca_b=(32, 80), puno_b=(34, 88),
                   hombro_f=(65, 40), codo_f=(80, 30), muneca_f=(92, 22), puno_f=(98, 18),
                   rodilla_b=(36, 102), tobillo_b=(34, 123), punta_b=(42, 126), rodilla_f=(64, 102), tobillo_f=(66, 123), punta_f=(74, 126)),
    # Entrenamiento. `equipo` agrega la barra, las manijas de la soga o las manoplas en las manos; `sin_guantes` quita los guantes.
    "pesas_abajo": dict(G, hombro_b=(34, 42), codo_b=(26, 60), muneca_b=(30, 46), puno_b=(32, 40),
                        hombro_f=(65, 42), codo_f=(76, 60), muneca_f=(74, 46), puno_f=(72, 40),
                        rodilla_b=(34, 100), tobillo_b=(30, 123), punta_b=(38, 126), rodilla_f=(68, 100), tobillo_f=(72, 123), punta_f=(80, 126),
                        equipo="barra", sin_guantes=True),
    "pesas_arriba": dict(G, cabeza=(55, 20), hombro_b=(34, 40), codo_b=(30, 24), muneca_b=(32, 14), puno_b=(32, 10),
                         hombro_f=(65, 40), codo_f=(70, 24), muneca_f=(72, 14), puno_f=(72, 10),
                         rodilla_b=(32, 102), tobillo_b=(27, 123), punta_b=(34, 126), rodilla_f=(70, 101), tobillo_f=(75, 122), punta_f=(83, 125),
                         equipo="barra", sin_guantes=True),
    "soga": dict(G, hombro_b=(34, 40), codo_b=(26, 60), muneca_b=(24, 76), puno_b=(24, 84),
                 hombro_f=(65, 40), codo_f=(74, 60), muneca_f=(78, 76), puno_f=(78, 84),
                 rodilla_b=(38, 102), tobillo_b=(36, 123), punta_b=(44, 126), rodilla_f=(62, 102), tobillo_f=(64, 123), punta_f=(72, 126),
                 equipo="soga", sin_guantes=True),
    "salto": dict(cabeza=(55, 8), torso_arriba=(50, 34), torso_abajo=(49, 58),
                  hombro_b=(34, 31), codo_b=(26, 50), muneca_b=(24, 66), puno_b=(24, 74),
                  hombro_f=(65, 31), codo_f=(74, 50), muneca_f=(78, 66), puno_f=(78, 74),
                  cadera_b=(41, 70), rodilla_b=(36, 90), tobillo_b=(30, 110), punta_b=(38, 115),
                  cadera_f=(58, 70), rodilla_f=(66, 88), tobillo_f=(70, 108), punta_f=(78, 113),
                  equipo="soga", sin_guantes=True),
    "manoplas": dict(G, hombro_b=(34, 40), codo_b=(42, 54), muneca_b=(56, 42), puno_b=(62, 36),
                     hombro_f=(65, 40), codo_f=(78, 52), muneca_f=(90, 40), puno_f=(96, 34),
                     rodilla_b=(36, 102), tobillo_b=(34, 123), punta_b=(42, 126), rodilla_f=(64, 102), tobillo_f=(66, 123), punta_f=(74, 126),
                     equipo="manoplas"),
}
BARRA, DISCO, MANOPLA, MANIJA = rampa("#b8bcc4"), rampa("#3a3a44"), rampa("#c23a3a"), rampa("#2b2b33")


def equipo(L, P):
    """Objetos sostenidos: se dibujan después del cuerpo, en las coordenadas de los puños."""
    pb, pf = P["puno_b"], P["puno_f"]
    if P.get("equipo") == "barra":
        y = (pb[1] + pf[1]) / 2 - 2
        L.capsula((pb[0] - 26, y), (pf[0] + 26, y), 2.2, 2.2, BARRA, linea=4)
        for x in (pb[0] - 24, pf[0] + 24):
            L.elipse((x, y), 3.4, 9.5, DISCO, 0, linea=4)
            L.elipse((x, y), 1.6, 5.5, DISCO, 0, lejos=1, linea=None)
    elif P.get("equipo") == "soga":
        for p in (pb, pf):
            L.capsula((p[0], p[1] - 4), (p[0], p[1] + 8), 2.4, 2.0, MANIJA, linea=4)
    elif P.get("equipo") == "manoplas":
        for p, lejos in ((pb, 1), (pf, 0)):
            L.elipse((p[0] + 2, p[1] - 1), 6.5, 8.5, MANOPLA, -25, lejos=lejos)
            L.elipse((p[0] + 3, p[1] - 2), 3.5, 5.0, rampa("#f1f1f6"), -25, lejos=lejos, linea=None)
# Osvaldo y la pose de "guardia" de un no-peleador: brazos bajos.
RELAJADO = dict(G, hombro_b=(34, 40), codo_b=(30, 62), muneca_b=(32, 80), puno_b=(34, 88),
                hombro_f=(65, 40), codo_f=(70, 62), muneca_f=(70, 80), puno_f=(70, 88),
                rodilla_b=(36, 102), tobillo_b=(34, 123), punta_b=(42, 126), rodilla_f=(64, 102), tobillo_f=(66, 123), punta_f=(74, 126))


def desplazar(P):
    if P.get("tirado"):
        return P
    return {k: ((v[0] + DX, v[1]) if isinstance(v, tuple) else v) for k, v in P.items()}


lerp, angulo = base.lerp, base.angulo


# ---------------------------------------------------------------- partes del cuerpo
class Cuerpo:
    def __init__(self, s):
        self.s = s
        self.PIEL = rampa(s["piel"])
        self.PELO = rampa(s["pelo"], (0.9, 0.8, 1.1))
        self.TOP = rampa(s["top_color"])
        self.SHORT = rampa(s["short"])
        self.PANT = rampa(s["pantalon"]) if s["pantalon"] else None
        self.GUANTE = rampa(s["guantes"]) if s["guantes"] else None
        self.GORRA = rampa(s["gorra_color"])
        self.m = s["musculo"]
        self.manga = self.TOP if s["top"] in ("buzo", "campera") else None

    def brazo_superior(self, L, hom, cod, lejos):
        r = self.manga or self.PIEL
        L.capsula(hom, cod, 6.5 * self.m, 5.0 * self.m, r, lejos)
        L.elipse(lerp(hom, cod, 0.5), 8.5 * self.m, 5.6 * self.m, r, angulo(hom, cod), lejos)

    def antebrazo_y_puno(self, L, cod, mun, pun, lejos, abierta=False):
        r = self.manga or self.PIEL
        L.elipse(lerp(cod, mun, 0.35), 7.0 * self.m, 5.2 * self.m, r, angulo(cod, mun), lejos)
        L.capsula(cod, mun, 5.0, 3.8, r, lejos)
        if self.manga:  # puño de la manga
            L.capsula(lerp(cod, mun, 0.8), mun, 4.2, 4.0, [rampa(self.s["top_color"])[i] for i in (2, 3, 4, 5, 5, 5)], lejos, linea=None)
        if self.GUANTE and not abierta:
            L.capsula(lerp(cod, mun, 0.6), mun, 4.4, 4.2, BLANCO, lejos)  # vendas
            L.capsula(mun, pun, 5.4, 6.6, self.GUANTE, lejos)
            L.elipse(lerp(mun, pun, 0.8), 6.4, 5.2, self.GUANTE, angulo(mun, pun), lejos)
            v = lerp(mun, pun, 0.3)
            L.capsula((v[0] - 3, v[1]), (v[0] + 3, v[1]), 1.2, 1.2, BLANCO, lejos, linea=None)
        elif abierta:
            L.capsula(mun, pun, 3.6, 2.6, self.PIEL, lejos)
            d = lerp(mun, pun, 1.5)
            L.capsula(pun, d, 1.6, 1.3, self.PIEL, lejos, linea=None)  # índice
        else:
            L.capsula(mun, pun, 4.2, 4.6, self.PIEL, lejos)  # puño desnudo
            L.elipse(lerp(mun, pun, 0.75), 4.8, 4.0, self.PIEL, angulo(mun, pun), lejos, linea=4)

    def pierna(self, L, cad, rod, tob, pun, lejos):
        r = self.PANT or self.PIEL
        L.capsula(cad, rod, 9.0 * self.m, 6.0, r, lejos)
        L.elipse(lerp(cad, rod, 0.5), 12.0 * self.m, 7.6 * self.m, r, angulo(cad, rod), lejos)
        L.elipse(lerp(rod, tob, 0.3), 8.0 * self.m, 5.8, r, angulo(rod, tob), lejos)
        L.capsula(rod, tob, 6.0, 3.8 if not self.PANT else 5.0, r, lejos, linea=None)
        L.elipse(rod, 5.0, 4.4, r, 0, lejos)
        if self.PANT:
            L.capsula(tob, pun, 4.6, 3.6, ZAPATILLA, lejos)
            L.capsula((tob[0], tob[1] + 2), (pun[0], pun[1] + 1), 2.0, 1.6, SUELA, lejos, linea=None)
        else:
            L.capsula(tob, pun, 4.0, 3.0, self.PIEL, lejos)

    def short(self, L, P):
        if self.PANT:
            L.capsula(P["cadera_b"], P["cadera_f"], 11.5, 11.5, self.PANT)
            cx, cy = (P["cadera_b"][0] + P["cadera_f"][0]) / 2, P["cadera_b"][1] - 9
            L.capsula((cx - 12, cy), (cx + 12, cy), 2.0, 2.0, rampa("#3a2a1e"), linea=4)  # cinto
            return
        for lado, lejos in (("b", 1), ("f", 0)):
            cad, rod = P[f"cadera_{lado}"], P[f"rodilla_{lado}"]
            L.capsula(cad, lerp(cad, rod, 0.4), 10.5, 9.6, self.SHORT, lejos)
            a, b = lerp(cad, rod, 0.05), lerp(cad, rod, 0.4)
            off = 7 if lado == "f" else -7
            L.capsula((a[0] + off, a[1]), (b[0] + off, b[1]), 1.4, 1.4, BLANCO, lejos, linea=None)
        L.capsula(P["cadera_b"], P["cadera_f"], 11.5, 11.5, self.SHORT)
        cx, cy = (P["cadera_b"][0] + P["cadera_f"][0]) / 2, P["cadera_b"][1] - 9
        L.capsula((cx - 13, cy), (cx + 13, cy), 2.2, 2.2, self.SHORT, linea=4)
        if self.s["cabeza"] == "vincha":  # sol de mayo sólo en el short de Lautaro
            sx, sy = P["cadera_f"][0] + 2, P["cadera_f"][1] + 4
            for ang in range(0, 360, 45):
                r = math.radians(ang)
                L.pintar(sx + round(4 * math.cos(r)), sy + round(4 * math.sin(r)), AMARILLO[2], AMARILLO)
            L.elipse((sx + 0.5, sy + 0.5), 2.6, 2.6, AMARILLO, linea=None)

    def torso(self, L, P):
        ta, tb, m = P["torso_arriba"], P["torso_abajo"], self.m
        PIEL = self.PIEL
        L.capsula(ta, tb, 17.0 * m, 10.5 * m, PIEL, linea=None)
        L.elipse((ta[0] - 8, ta[1] - 7), 9, 5, PIEL, -20, lejos=1)
        L.elipse((ta[0] + 9, ta[1] - 7), 9, 5, PIEL, 20)
        L.capsula((P["cabeza"][0] - 3, P["cabeza"][1] + 8), (ta[0], ta[1] - 8), 6.5, 7.5, PIEL, linea=None)
        if self.s["top"] == "nada":
            L.elipse((ta[0] + 1, ta[1] - 6), 3.5, 3, PIEL, 0, linea=None)
            L.elipse((ta[0] - 8, ta[1] + 6), 11, 8.5, PIEL, 8, lejos=1)
            L.elipse((ta[0] + 8, ta[1] + 6), 11.5, 8.8, PIEL, -8)
            for fila in range(3):
                y = ta[1] + 18 + fila * 6.2
                x = ta[0] + (tb[0] - ta[0]) * (fila / 3)
                L.elipse((x - 3.5, y), 3.4, 2.9, PIEL, 0, lejos=1)
                L.elipse((x + 3.7, y), 3.6, 2.9, PIEL, 0)
            L.elipse((tb[0] - 9, tb[1] - 8), 3.2, 8, PIEL, 12, lejos=1)
            L.elipse((tb[0] + 9, tb[1] - 8), 3.2, 8, PIEL, -12)
            L.pintar(tb[0], tb[1] + 1, PIEL[4], PIEL)
            return
        if self.s["top"] == "musculosa":
            L.capsula((ta[0], ta[1] + 3), (tb[0], tb[1] + 2), 15.5 * m, 11 * m, self.TOP, linea=None)
            L.elipse((ta[0] - 8, ta[1] + 6), 11, 8.5, self.TOP, 8, lejos=1, linea=None)
            L.elipse((ta[0] + 8, ta[1] + 6), 11.5, 8.8, self.TOP, -8, linea=None)
            for dx, lejos in ((-9, 1), (10, 0)):
                L.capsula((ta[0] + dx, ta[1] - 8), (ta[0] + dx * 0.8, ta[1] + 4), 2.6, 3.2, self.TOP, lejos, linea=4)
        else:  # buzo o campera: cuerpo cerrado y capucha
            L.capsula((ta[0], ta[1] - 2), (tb[0], tb[1] + 4), 18.5 * m, 13 * m, self.TOP, linea=None)
            L.elipse((ta[0] - 8, ta[1] + 7), 11, 8, self.TOP, 8, lejos=1, linea=None)
            L.elipse((ta[0] + 8, ta[1] + 7), 11.5, 8.5, self.TOP, -8, linea=None)
            if self.s["top"] == "buzo":
                L.elipse((P["cabeza"][0] - 5, P["cabeza"][1] + 13), 11, 4.5, self.TOP, -8, lejos=1)  # capucha caída sobre la nuca
                L.elipse((P["cabeza"][0] - 12, P["cabeza"][1] + 9), 4.5, 6, self.TOP, 20, lejos=1, linea=4)
                for k in range(0, 18, 2):  # cordones
                    L.pintar(ta[0] + 2, ta[1] + k, BLANCO[2], BLANCO)
                    L.pintar(ta[0] + 7, ta[1] + k, BLANCO[2], BLANCO)
                L.capsula((ta[0] - 2, tb[1] + 6), (tb[0] + 10, tb[1] + 6), 1.2, 1.2, self.TOP, linea=4)  # bolsillo
            else:  # campera deportiva con tiras blancas
                for dx in (-5, 11):
                    L.capsula((ta[0] + dx, ta[1] - 6), (tb[0] + dx * 0.7, tb[1] + 8), 1.4, 1.4, BLANCO, linea=None)
                L.capsula((ta[0] + 3, ta[1] - 6), (tb[0] + 3, tb[1] + 10), 0.9, 0.9, rampa("#c8c8d0"), linea=None)  # cierre
        if self.s["toalla"]:
            for dx, lejos in ((-11, 1), (9, 0)):
                L.capsula((ta[0] + dx, ta[1] - 8), (ta[0] + dx + (2 if dx > 0 else -2), tb[1] - 2), 4.6, 4.2, rampa("#e6e2d6"), lejos, linea=4)

    def cabeza(self, L, P, ko=False):
        s, PIEL, PELO = self.s, self.PIEL, self.PELO
        hx, hy = P["cabeza"]
        L.elipse((hx, hy), 9.5, 11.5, PIEL, 0, linea=None)
        L.elipse((hx + 3, hy + 7), 7.5, 5.8, PIEL, 10, linea=None)
        L.elipse((hx - 6.5, hy + 1.5), 2.2, 3.4, PIEL, 0, lejos=1)
        estilo = s["estilo"]
        if estilo in ("corto", "ondulado", "canoso"):
            L.elipse((hx - 1.5, hy - 6.5), 9.2, 6.2, PELO, -12, linea=None)
            puntas = ((-9, -6, 3.2), (-7, -11, 3.0), (-2, -13, 3.2), (3, -12.5, 3.0), (7, -9, 2.6)) if estilo == "corto" else \
                     ((-10, -5, 3.6), (-9, -10, 3.4), (-3, -13, 3.6), (4, -12, 3.2), (8, -8, 2.8), (-11, 0, 3.0)) if estilo == "ondulado" else \
                     ((-9, -7, 2.8), (-5, -11, 2.8), (0, -12, 2.8), (5, -11, 2.6), (8, -8, 2.4))
            for (dx, dy, r) in puntas:
                L.elipse((hx + dx, hy + dy), r, r * 0.8, PELO, 0, linea=4)
        elif estilo == "rulos":
            for (dx, dy, r) in ((-10, -6, 4.5), (-6, -12, 4.5), (0, -14, 4.5), (6, -12, 4.2), (10, -7, 3.8), (-12, 2, 4.2), (-11, 10, 4.0), (-8, 17, 3.6), (12, 0, 3.0)):
                L.elipse((hx + dx, hy + dy), r, r * 0.9, PELO, 0, linea=4)
            L.elipse((hx - 1, hy - 6), 9.5, 7, PELO, -8, linea=None)
        elif estilo == "rapado":
            L.elipse((hx - 1.5, hy - 6.5), 9.2, 6.0, PELO, -12, linea=None, lejos=1)
        else:  # pelado
            L.pintar(hx + 2, hy - 8, PIEL[0], PIEL)
            L.pintar(hx + 3, hy - 8, PIEL[0], PIEL)
        if estilo != "pelado":
            for y in range(int(hy - 3), int(hy + 6)):
                for x in range(int(hx - 9), int(hx - 4)):
                    p = L.px[y][x]
                    if p is not None and p[1] is PIEL and (x + y) % 2 == 0:
                        L.pintar(x, y, PELO[3], PIEL)
        hx, hy = int(hx), int(hy)
        for x in range(hx, hx + 8):
            L.pintar(x, hy - 2 + (1 if x >= hx + 6 else 0), PELO[3] if estilo != "pelado" else PIEL[4], PIEL)
            L.pintar(x, hy - 1 + (1 if x >= hx + 6 else 0), PELO[2] if x % 2 else PELO[3], PIEL)
        if ko:
            for x, y in ((hx + 2, hy + 1), (hx + 3, hy + 2), (hx + 6, hy + 1), (hx + 7, hy + 2), (hx + 3, hy + 1), (hx + 7, hy + 1)):
                L.pintar(x, y, OJO, PIEL)
        else:
            for x, y, col in ((hx + 2, hy + 1, BLANCO[1]), (hx + 3, hy + 1, OJO), (hx + 2, hy + 2, PIEL[3]),
                              (hx + 3, hy + 2, PIEL[3]), (hx + 6, hy + 1, BLANCO[2]), (hx + 7, hy + 1, OJO)):
                L.pintar(x, y, col, PIEL)
        for x, y, i in ((hx + 8, hy + 2, 1), (hx + 9, hy + 3, 1), (hx + 9, hy + 4, 2), (hx + 8, hy + 5, 4), (hx + 7, hy + 5, 3), (hx + 4, hy + 3, 3)):
            L.pintar(x, y, PIEL[i], PIEL)
        for x in range(hx + 4, hx + 9):
            L.pintar(x, hy + 8 + (1 if ko else 0), PIEL[5] if x < hx + 8 else PIEL[4], PIEL)
        if s["mayor"]:
            for x, y in ((hx + 1, hy + 4), (hx + 2, hy + 5), (hx + 8, hy + 7), (hx + 1, hy - 4), (hx + 4, hy - 5)):
                L.pintar(x, y, PIEL[4], PIEL)
        if s["bigote"]:
            L.capsula((hx + 3, hy + 7), (hx + 10, hy + 7), 1.8, 1.4, PELO, linea=None)
        if s["barba"]:
            L.elipse((hx + 4, hy + 10), 7, 3.6, [PELO[2], PELO[3], PELO[3], PELO[4], PELO[4], PELO[5]], 0, linea=None)
        elif not s["mayor"]:
            for (x, y) in ((hx, hy + 9), (hx + 2, hy + 10), (hx + 4, hy + 11), (hx + 6, hy + 11), (hx + 1, hy + 7), (hx + 3, hy + 12), (hx + 8, hy + 10), (hx - 1, hy + 11)):
                L.pintar(x, y, PIEL[4], PIEL)
        cab = s["cabeza"]
        if cab == "vincha":
            def franjas(x, y):
                return BLANCO if int(y - (hy - 7)) % 4 in (1, 2) else CELESTE
            for fin in () if ko else (((hx - 16, hy - 8), (hx - 25, hy - 3)), ((hx - 15, hy - 2), (hx - 22, hy + 6))):  # sin colas en el KO
                L.capsula((hx - 8, hy - 5), fin[0], 2.4, 2.0, franjas, lejos=1, linea=4)
                L.capsula(fin[0], fin[1], 2.0, 1.2, franjas, lejos=1, linea=4)
            L.elipse((hx - 8.5, hy - 5), 2.6, 2.8, franjas, 0, lejos=1)
            for y in range(hy - 7, hy - 3):
                for x in range(hx - 10, hx + 10):
                    p = L.px[y][x]
                    if p is not None and p[1] in (PIEL, PELO):
                        ramp = franjas(x, y)
                        L.pintar(x, y, ramp[1 if x > hx else 2], ramp)
        elif cab in ("gorra", "gorra_atras"):
            L.elipse((hx - 1, hy - 7), 10.5, 7, self.GORRA, -8, linea=None)
            L.capsula((hx - 10, hy - 4), (hx + 10, hy - 4), 1.6, 1.6, self.GORRA, linea=4)
            if cab == "gorra":
                L.capsula((hx + 6, hy - 4), (hx + 20, hy - 2), 1.8, 1.4, self.GORRA, linea=4)  # visera adelante
            else:
                L.capsula((hx - 8, hy - 3), (hx - 20, hy + 1), 1.8, 1.4, self.GORRA, linea=4)  # visera atrás


def dibujar(s, nombre):
    P = desplazar(POSES.get(nombre, G))
    c = Cuerpo(s)
    if P.get("sin_guantes"):
        c.GUANTE = None
    if nombre in ("guardia", "paso1", "paso2") and s["guantes"] is None and s["top"] == "musculosa" and s["toalla"]:
        P = desplazar(RELAJADO)
    L = base.Lienzo()
    abierta = nombre == "senala" or (s["toalla"] and nombre != "ko")
    c.brazo_superior(L, P["hombro_b"], P["codo_b"], 1)
    c.pierna(L, P["cadera_b"], P["rodilla_b"], P["tobillo_b"], P["punta_b"], 1)
    c.pierna(L, P["cadera_f"], P["rodilla_f"], P["tobillo_f"], P["punta_f"], 0)
    c.short(L, P)
    L.elipse(P["hombro_b"], 8, 8.5, c.manga or c.PIEL, 0, lejos=1)
    c.torso(L, P)
    if P.get("tirado"):
        cabeza_tirada(c, L, P)
    else:
        c.cabeza(L, P)
    c.antebrazo_y_puno(L, P["codo_b"], P["muneca_b"], P["puno_b"], 1, abierta and nombre != "senala")
    c.brazo_superior(L, P["hombro_f"], P["codo_f"], 0)
    L.elipse(P["hombro_f"], 8.8, 9, c.manga or c.PIEL, 0)
    c.antebrazo_y_puno(L, P["codo_f"], P["muneca_f"], P["puno_f"], 0, abierta)
    equipo(L, P)
    L.contorno()
    return L.imagen()


def cabeza_tirada(c, L, P):
    """Dibuja la cabeza de pie en un lienzo aparte y la gira 90° para que mire hacia arriba."""
    aux = base.Lienzo()
    hx, hy = P["cabeza"]
    c.cabeza(aux, dict(P, cabeza=(60, 60)), ko=True)
    for y in range(CH):
        for x in range(CW):
            p = aux.px[y][x]
            if p is None:
                continue
            dx, dy = x - 60, y - 60
            L.pintar(hx + dy, hy - dx, p[0], p[1])


def hoja(s, poses):
    tira = Image.new("RGBA", (CW * len(poses), CH), (0, 0, 0, 0))
    for i, nombre in enumerate(poses):
        tira.alpha_composite(dibujar(s, nombre), (i * CW, 0))
    return tira


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ids = [a for a in sys.argv[1:] if a in PERSONAJES] or list(PERSONAJES)
    tiras = {}
    for pid in ids:
        tiras[pid] = hoja(PERSONAJES[pid], ORDEN_POSES + (POSES_ENTRENAMIENTO if pid in CON_ENTRENAMIENTO else []))
        tiras[pid].save(OUT / f"{pid}.png", optimize=True)
        print("OK", pid)
    if len(ids) == len(PERSONAJES):
        esc = 2
        rev = Image.new("RGB", (CW * (len(ORDEN_POSES) + len(POSES_ENTRENAMIENTO)) * esc, (CH + 14) * len(ids) * esc), (28, 18, 51))
        d = ImageDraw.Draw(rev)
        f = ImageFont.load_default(size=14)
        for r, pid in enumerate(ids):
            y = r * (CH + 14) * esc
            rev.paste(tiras[pid].resize((tiras[pid].width * esc, CH * esc), Image.NEAREST), (0, y), tiras[pid].resize((tiras[pid].width * esc, CH * esc), Image.NEAREST))
            d.text((4, y + CH * esc), pid, font=f, fill=(255, 255, 255))
        rev.save(OUT / "revision.png")
        print("Hoja de revisión ->", OUT / "revision.png")


if __name__ == "__main__":
    main()
