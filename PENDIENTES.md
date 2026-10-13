# Estado y pendientes — Conurbano Fighter

Actualizado: 2026-10-13.

## Cómo retomar
Leer este archivo y el código antes de trabajar. No confundir propuestas con funciones terminadas.
Eliminar un pendiente únicamente después de implementarlo y verificarlo. Actualizar fecha y siguiente paso en el mismo cambio. Git conserva el historial.
Este archivo es la referencia actual; docs/GDD.md y docs/ROADMAP.md son antecedentes cuando entren en conflicto.

## Estado comprobado de esta sesión
El juego base ya está publicado en index.html, con retratos y tools/check-game.cjs.
Pruebas de lógica pasan para guardado/continuación, secuencias de entrenamiento, compras, resultados y transiciones.
Se añadió guía inicial que se cierra y recuerda su lectura; panel grande de vida, fatiga y dinero; tienda con precio, fatiga/vida previstas y saldo restante. Diseño adaptable a celular.
Verificación visual en navegador pendiente: Playwright está instalado pero su ejecutable Chromium no está disponible. No afirmar que se probó visualmente ni que el balance está resuelto.

## Pendientes, en orden

### 1. Cerrar la base jugable
- [ ] Verificar guardado y continuación, estilos de rivales y pistas de Osvaldo, y ejercicios distintos.
- [ ] Comprobar balance jugando: hubo ajustes demasiado difíciles y demasiado fáciles. Las pruebas de lógica no prueban diversión.
- [ ] Completar el panel grande con estadísticas de fuerza, velocidad, aguante y técnica; vida, fatiga y dinero ya están ampliados.
- [ ] Conservar el sábado con solo preparación (comida/masaje) o empezar pelea, sin ejercicios.
- [ ] Mostrar explicaciones iniciales una sola vez y permitir saltar transiciones repetidas. Mantener consejos específicos de cada próximo rival.

### 2. Progresión y economía
- [ ] Incorporar fama que desbloquee sponsors, mejores bolsas y productos.
- [ ] Ajustar ingresos y recuperación para que perder no produzca una espiral sin salida; conservar descanso gratis.
- [ ] Comprar equipamiento permanente que mejore un ejercicio concreto: mayor ganancia y mayor fatiga, sin volver inútiles las alternativas.
- [ ] Añadir compras de progreso personal, incluido auto; reflejarlas visualmente, sin dar fuerza por comprar bienes.
- [ ] Validar primero tres peleas completas, un sponsor y una compra importante antes de extender la campaña.

### 3. Campaña
- [ ] Seis peleas argentinas: dos barriales, dos regionales, semifinal y campeonato.
- [ ] Rivales que cambien las decisiones: presión con agotamiento, contragolpe y alcance, entre otros; no solo más vida.
- [ ] Alternar novedades entre peleas: ejercicio, sponsor, mejora o escena breve del barrio.
- [ ] Revancha breve y contundente con Brian como cierre del barrio y demostración del progreso.
- [ ] Oferta de representante y salto a liga internacional ficticia; Osvaldo sigue en la esquina.
- [ ] Cuatro peleas internacionales hasta el título y final del juego.
- [ ] Mantener coherencia entre reglas de combate y liga; no presentar boxeo como UFC ni ampliar a suelo/derribos sin una decisión nueva.

### 4. Encuentro opcional de riesgo
- [ ] Tras las primeras dos victorias, una oferta de la mafia con aceptar/rechazar y riesgos explícitos.
- [ ] Aceptar abre pelea opcional, pago y fatiga, y suma sospecha.
- [ ] Definir consecuencias de ser descubierto: perder sponsor o suspensión; comunicar el riesgo antes de elegir.
- [ ] Rechazar conserva la ruta deportiva y abre una oportunidad legal menos lucrativa.
- [ ] Probar un solo encuentro; no abrir una campaña criminal completa todavía.
- [ ] Evitar un 50–50 arbitrario como única mecánica y evitar que aceptar sea siempre la mejor opción.

## Siguiente paso
Verificar visualmente panel y tienda en escritorio/celular; completar estadísticas grandes y continuar progresión económica. Mantener el balance como pendiente hasta probar jugabilidad.
