# Roadmap

## Fase 0: Decisiones (pre-producción)
- [x] Crear el repo
- [x] Primer borrador del GDD
- [x] Validar los supuestos del GDD: navegador, arcade sin piso, arte por Claude y nombre elegido por el jugador
- [x] Primer mockup de arte: escena de la estación
- [ ] Definir el título y los nombres de las ligas

## Fase 1: Prototipo de pelea ← **próximo paso**
Objetivo: comprobar que **pelear es divertido** con arte provisorio.

- [ ] Setup del proyecto: Vite + TypeScript + Phaser 3, resolución 320×224 con escalado pixel-perfect
- [ ] Deploy automático (GitHub Pages o Railway) para jugarlo con un link
- [ ] Input: teclado + joystick (Gamepad API)
- [ ] Peleador controlable: moverse, guardia, esquivar, piña, patada (usando los sprites del mockup)
- [ ] Hitboxes/hurtboxes, daño, *hitstun*, *knockback*
- [ ] Barras de vida y estamina
- [ ] IA rival básica (acercarse, atacar, bloquear al azar)
- [ ] Rounds (3 × 60 s), KO, pantalla de victoria o derrota
- [ ] Stats conectados al combate (Fuerza → daño, Velocidad → velocidad, etc.) con un panel de debug para tocarlos en vivo

**Listo cuando:** se puede jugar una pelea completa contra la IA y cambiar stats cambia cómo se siente.

## Fase 2: Loop mínimo
- [ ] Pantalla para elegir el nombre del protagonista
- [ ] Intro con 3 viñetas y pelea tutorial (derrota)
- [ ] Pantalla de semana de entrenamiento (3 turnos, 5 actividades, energía y plata)
- [ ] 2 eventos del barrio
- [ ] 2 peleas locales (Canchita y Club)
- [ ] 1 especial: "La del Tano"
- [ ] Guardado en `localStorage`

## Fase 3: Contenido
- [ ] Las 11 etapas del GDD: locales, continentales y UCF
- [ ] Especiales completas
- [ ] Arte final: protagonista, rivales y escenarios
- [ ] Controles táctiles para celular

## Fase 4: Pulido
- [ ] Música y SFX chiptune
- [ ] Balance de stats y dificultad
- [ ] Menús, opciones y créditos
- [ ] Testing con jugadores del barrio
