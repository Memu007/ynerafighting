# Estado y pendientes — Conurbano Fighter

Actualizado: 2026-10-13.

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

## Pendientes
- [ ] Probar la campaña jugando en navegador real: especial, lectura de ataques y descanso frente a rutina avanzada. Ajustar sólo tras registrar rival, stats, fatiga y resultado.
- [ ] Revisar CSS, scroll, foco y controles táctiles en escritorio y teléfono reales. No hay Chromium/Firefox instalado en este entorno; las pruebas VM y los renders no reemplazan esa revisión.

## Siguiente paso
Jugar las primeras tres fechas con preparación equilibrada, probar el sponsor y una mejora, y contrastar con una ruta que descansa más. Si una pelea queda demasiado fácil/difícil, registrar sus números antes de tocar el balance.
