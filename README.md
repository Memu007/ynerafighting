# Conurbano Fighter

Prototipo jugable de pelea y entrenamiento en Villa Madero. HTML y JavaScript sin dependencias de ejecución.

## Jugar

Abrí `index.html` en un navegador. Para un origen estable y guardar la partida:

```bash
python3 -m http.server 8000
```

Entrá a http://localhost:8000. El guardado usa localStorage del navegador: no se comparte entre dispositivos ni orígenes y puede no estar disponible en algunas vistas previas o modos privados. Conservá el mismo origen para retomar.

- Flechas: moverse. Z: piña. X: patada. C: guardia. V: especial.
- Espacio o toque: avanzar escenas. N en portada: nueva partida.
- En celular: botones en pantalla. Boxeo usa PIÑA y PATADA.

## Implementado

Portada, robo, reflexión en la habitación, entrada al gimnasio, charla de los lunes con pizarrón, tres actividades semanales, descanso, fatiga, premios, comida y masaje, peleas progresivas, resultados y especial Furia de Madero.

Ejercicios: pesas con precisión, cuerda con saltos por vuelta, bolsa con límite de tiempo y secuencias de boxeo. Los rivales tienen estilos simple, presión, defensa o contragolpe; Osvaldo da pistas acordes.

El guardado conserva el último punto de preparación completado; si cerrás durante una pelea, se retoma su preparación. Completar la campaña borra ese guardado.

## Validación

```bash
node tools/check-game.cjs
```

Pruebas de lógica con simulación de canvas y navegador: escenas, entrenamiento, compras, especial, resultado, guardado y continuación. No reemplazan la prueba de jugabilidad en un navegador real. Dificultad y precios siguen en calibración.

La documentación previa en `docs/` y el mockup se conservan como antecedentes; parte del diseño describe ideas aún no implementadas.
