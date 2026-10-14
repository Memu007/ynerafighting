# Estado y pendientes — Conurbano Fighter

Actualizado: 2026-10-14.

## Cómo retomar
Leer este archivo y el código. Eliminar una tarea sólo cuando esté implementada y verificada. Git conserva el historial. Este archivo manda sobre los antecedentes de docs/GDD.md y docs/ROADMAP.md.

## Estado comprobado
- Campaña: seis fechas argentinas, revancha breve con Braian, representante y cuatro fechas de una liga ficticia de kickboxing. Osvaldo sigue en tu esquina.
- Rivales con presión y pausas, guardia, contragolpe, alcance y patrón equilibrado. El pizarrón usa sus estadísticas reales y consejos ligados a su estilo.
- Ejercicios distintos; fatiga; descanso gratuito; comida y masaje. Sábado con sólo dos acciones principales: prepararse o pelear.
- Fama, sponsor, bolsas crecientes, equipo permanente y rutina avanzada opcional (+1 nivel, +5 fatiga). Auto como logro visible sin efecto en combate.
- Un encuentro clandestino opcional tras dos victorias, aceptar/rechazar explícitos, combate, premio, fatiga, sospecha, riesgo de perder sponsor y suspensión. No avanza el circuito.
- Guía inicial que recuerda su lectura, estadísticas grandes, compras con vista previa, retratos para todos los rivales y escenas que se pueden saltar.
- Guardado v2 por identidad de rival, migración v1, compras/decisiones/resultados pendientes y final persistentes. Reabrir un resultado no vuelve a pagar. Si se cierra durante el combate se retoma su preparación.
- Corregida victoria registrada como derrota. Golpes normales ya no cancelan todos los ataques del rival; sólo la especial interrumpe. Simulación a 60 pasos por segundo independientemente de la pantalla.

## Verificación realizada
`node tools/check-game.cjs`: 25 comprobaciones de lógica de campaña, economía, ejercicios, estilos, KO, guardado, migración, reinicio, controles de sábado y reloj.
`node tools/simulate-combat.cjs`: 22 combates deterministas, dos políticas. Con tres sesiones exitosas semanales y fatiga 20: primeras fechas ~13–18 segundos; final ~20 segundos. Braian ~4 segundos deliberadamente. No son mediciones de jugadores reales.
`node tools/render-game.cjs <carpeta>`: inspección visual de 10 estados de canvas con los retratos reales. La fuente monospace de esa herramienta es una aproximación local; no verifica CSS ni interacción del navegador.
`node tools/package-game.cjs`: genera conurbano-fighter.html con imágenes incluidas para abrir sin carpeta de assets.

## Verificación en navegador — 2026-10-14
`node tools/check-browser.cjs`: Chromium real, ventanas 1280×900, 360×800 y 800×360; teclado, foco, casilla de rutina avanzada, compras, preparación del sábado, continuación y eventos táctiles emulados. Sin errores JavaScript ni desbordamiento horizontal. En las dos pantallas móviles, arena y controles caben juntos durante el combate.
`GAME_PLAY_CAREER=1 node tools/check-browser.cjs`: recorrido automático por la introducción y las tres primeras semanas usando botones, teclas y el reloj real del navegador. Completó las tres peleas, eligió el sponsor legal y compró el banco de pesas. Tito: ~22 s, vida final 122/154; Rulo: ~21 s, 55/181; Nico: ~25 s, 31/201. Cinco, cinco y siete especiales respectivamente. Son resultados de un controlador automático, no de una persona.

Corregido: activación nativa con espacio/Enter, foco de la casilla de rutina, captura y cancelación del toque, desplazamiento automático a la arena y composición de combate horizontal. Condición del personaje visible antes de elegir actividad; catálogo permanente plegable para reducir el scroll.

## Mejoras visuales pendientes — orden de trabajo
- [ ] Rehacer los cuerpos de los peleadores: sprites más detallados y coherentes con los retratos aprobados. Conservar caminar, piña, patada, guardia, especial, recibir golpe y KO. El retoque geométrico actual es provisorio.
- [x] Habitación, interior del gimnasio y cuartito del pizarrón rehechos al nivel de la fachada (ventanas con luz, ring de fondo, estante de trofeos, pizarrón con tiza). Los fondos se dibujan una vez en un canvas auxiliar y se reutilizan. Pendiente: cuerpo de Osvaldo coherente con su retrato.
- [x] Estación Villa Madero rehecha: skyline iluminado, techo con tubos, tren con puertas, baldosas y niebla. Se usa en el prólogo y en la revancha con Braian.
- [ ] Mejorar las animaciones de pesas, cuerda, bolsa y técnica. Los objetos y el personaje aún tienen arte provisional aunque los ejercicios funcionan distinto.
- [x] Escenarios por circuito: Club Social (fechas 1–2), Polideportivo Municipal (3–4), estadio cubierto (5–6) y arena de Las Vegas (internacional). Multitudes estáticas por el caché de fondo; animarlas queda pendiente. Resultado y sábado usan el ring de esa pelea.
- [ ] Pulir portada, escenas breves entre fechas e impactos/especial. La portada y la especial ya existen; falta llevar su acabado al nivel de los retratos.

Los retratos detallados están integrados. Las correcciones de teclado, foco y pantalla móvil no completan estos pendientes de arte.

## Verificación pendiente con jugadores
- [ ] Evaluar diversión y dificultad con una persona jugando la campaña. Registrar rival, stats, fatiga y resultado antes de ajustar números.
- [ ] Comprobar respuesta y ergonomía en un teléfono físico. La emulación táctil y las capturas verifican geometría y eventos, pero no dedos, latencia y rendimiento del aparato.

## Siguiente paso
Empezar por los sprites de combate y revisar una pelea con los retratos actuales. Después seguir con escenarios y ejercicios. Mantener las pruebas de dificultad y teléfono físico como verificaciones separadas.
