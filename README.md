# Conurbano Fighter

Juego de pelea y entrenamiento en Villa Madero, hecho con HTML y JavaScript sin dependencias para jugar.

## Abrir

Abrí `conurbano-fighter.html`: incluye todos los retratos y no necesita una carpeta de imágenes ni cargar fuentes de internet.

Para jugar desde un origen estable y continuar en el mismo navegador:

```bash
python3 -m http.server 8000
```

Entrá a http://localhost:8000. `index.html` es la fuente con assets separados. LocalStorage no comparte la partida entre dispositivos, archivos u orígenes; algunos modos privados y vistas previas no permiten guardar. El panel avisa si falla.

## Juego

- Flechas: moverse. Z: piña. X: patada. C: guardia. V: especial.
- Espacio: avanzar. N en portada: nueva partida. Botones táctiles y controles grandes para preparación.
- Lunes, miércoles y viernes: elegí entrenamiento o descanso. El sábado: prepararse o pelear.
- Seis peleas argentinas, cierre de la historia con Braian y cuatro fechas internacionales de kickboxing ficticio.
- Fama desbloquea equipo, sponsors y auto. El equipo avanzado da más ganancia y fatiga; se puede desactivar. Los bienes no dan fuerza.
- Una oferta clandestina permite elegir dinero extra con riesgo contra una ruta deportiva y sponsor legal.

El guardado conserva preparación, compras, decisiones, premios pendientes y el final. Si cerrás durante la pelea, se reinicia desde su preparación. Los premios cobrados no se duplican al continuar. Se migran los guardados de la versión anterior.

## Desarrollo y comprobaciones

```bash
node tools/check-game.cjs
node tools/simulate-combat.cjs
node tools/package-game.cjs
```

Las pruebas de lógica y las simulaciones no certifican que el juego sea divertido. El balance necesita una prueba humana. Para inspeccionar imágenes del canvas, `tools/render-game.cjs` requiere opcionalmente `@napi-rs/canvas`, pero el juego no lo necesita.

Ver [PENDIENTES.md](PENDIENTES.md) para las verificaciones que faltan. Los documentos de `docs/` son antecedentes de diseño.
