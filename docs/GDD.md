# GDD: Del Barrio al Octágono (título provisorio)

> Documento vivo. Lo marcado con **[SUPUESTO]** es una decisión provisoria del PM que falta validar.

## 1. Visión

Un juego corto y rejugable de 1 a 2 horas que mezcla **gestión de entrenamiento** (elegís qué hacer cada semana) con **peleas de acción en 2D**, todo en pixel art de 16 bits. Es la historia de un pibe del conurbano que pasa de que lo afanen en la estación a pelear por un título mundial.

**Pilares:**
1. **Identidad local:** Villa Celina, Villa Madero, la General Paz, Crovara, el tren, el gimnasio de chapa. Que un pibe de ahí diga "eso es mi barrio".
2. **Progreso que se siente:** cada semana de entreno cambia cómo pelea el personaje.
3. **Peleas simples de aprender y con profundidad:** pocos botones, mucho timing.

## 2. Plataforma y público

- **[SUPUESTO]** Navegador (desktop y celular) para el prototipo. Después se evalúa un build de escritorio con Electron o Tauri.
- **Controles:** teclado, joystick (Gamepad API) y controles táctiles en celular.
- **Público:** fans de juegos retro, de MMA y de historias argentinas.

## 3. Historia

**Protagonista:** **[SUPUESTO]** "Nahuel", 19 años, nombre provisorio. Llega al barrio a vivir con su tía después de que se le complica la situación en su casa (motivo a definir).

**Acto 1: La llegada**
- Intro tipo historieta: se baja del tren (**[SUPUESTO]** la estación exacta la define el equipo; puede ser ficticia e inspirada en la zona).
- Camina hacia lo de su tía. Dos chorros lo encaran, le roban la mochila y el celular y le pegan.
- **Pelea tutorial imposible de ganar:** enseña los controles básicos y termina en derrota.
- Lo levanta **"el Tano"**, dueño de un gimnasio de boxeo/MMA del barrio: "Si querés que no te pase más, vení mañana."

**Acto 2: El barrio**
- Entrena, consigue un laburo (delivery, gomería) para pagar la cuota y hace amigos y rivales en el gimnasio.
- Primeras peleas: torneo de barrio y peleas amateur en un club.
- Subtrama: vuelve a cruzarse con los que lo robaron (pelea de revancha opcional o de historia).

**Acto 3: El salto**
- Circuito regional y luego una pelea en el exterior (Brasil) como "prueba".
- Firma con la liga grande (**nombre ficticio, ver §10**).
- Pelea final por el título.

**Tono:** el barrio no es solo peligro. Hay personajes queribles: la tía, el Tano, la del kiosco, el sparring que se vuelve amigo.

## 4. Loop de juego

```
┌──────────────┐    ┌────────────────────┐    ┌──────────┐
│ Semana en el │ →  │ Evento del barrio  │ →  │ ¿Pelea?  │ → siguiente semana
│ gimnasio     │    │ (random/historia)  │    │ (etapa)  │
└──────────────┘    └────────────────────┘    └──────────┘
```

### 4.1 Semana de entrenamiento
- Cada semana tiene **3 turnos**. En cada turno elegís **1 actividad**.
- Recursos: **Energía** (0–100), **Plata** ($) y **Moral** (0–100).
- Si la energía está muy baja, aumenta el riesgo de **lesión**, que te hace perder turnos.

| Actividad | Efecto principal | Costo |
|---|---|---|
| Bolsa | +Fuerza, +Técnica (golpes) | Energía media |
| Soga / Correr por el barrio | +Resistencia, +Velocidad | Energía media |
| Pesas | +Fuerza grande | Energía alta |
| Sparring | +Técnica, +Defensa, chance de aprender una especial | Energía alta, riesgo de lesión |
| Lucha / Grappling | +Suelo (derribos, defensa de derribos) | Energía alta |
| Laburar | +Plata | Energía media |
| Descansar / Comer con la tía | +Energía, +Moral | Nada |

### 4.2 Stats

| Stat | Qué afecta en la pelea |
|---|---|
| **Fuerza** | Daño de golpes |
| **Velocidad** | Velocidad de movimiento y ataque, ventana de esquive |
| **Resistencia** | Estamina máxima y recuperación |
| **Técnica** | Combos disponibles, precisión, chance de crítico |
| **Defensa** | Daño bloqueado, recuperación tras recibir un golpe |
| **Suelo** | Éxito de derribos y de escapes en el piso |

Escala **1–100**. El protagonista arranca con 10 en todo.

### 4.3 Eventos del barrio
Tarjetas entre semanas con decisiones cortas. Ejemplos:
- "Te invitan a un asado el viernes" → +Moral, −Energía.
- "Te ofrecen una changa pesada" → +Plata, riesgo de lesión.
- "Se corta la luz en el gimnasio" → se pierde un turno o se entrena en la calle.

## 5. Sistema de pelea

**[SUPUESTO]** Estilo **arcade con sabor MMA**: base tipo Street Fighter II / Streets of Rage, con derribos y un minijuego de piso simple. No es un simulador.

### 5.1 Controles
| Botón | Acción |
|---|---|
| ← → | Moverse / retroceder |
| ↓ | Agacharse / esquivar bajo |
| A | Piña (rápida) |
| B | Patada (lenta, más daño) |
| C | Agarre / derribo |
| A+B | Especial equipada (gasta barra de **Aguante**) |
| Mantener ← | Guardia |

### 5.2 Barras
- **Vida:** llega a 0 y hay KO.
- **Estamina:** cada ataque la gasta. Sin estamina los golpes son lentos y débiles.
- **Aguante:** se llena pegando y recibiendo golpes, y se usa para las especiales.

### 5.3 Piso (minijuego)
Al conectar un derribo se pasa al suelo. Ahí hay un minijuego de timing: una barra con zona verde para **golpear desde arriba**, **someter** o **escapar**, y el stat Suelo agranda la zona.

### 5.4 Reglas
- **3 rounds** de 60 segundos de juego.
- Se gana por KO, sumisión o decisión (puntos por golpes conectados y control).

## 6. Especiales ("podercitos" y piñitas)

Se desbloquean por historia, sparring o eventos. Solo se equipan **2 a la vez**.

| Nombre (provisorio) | Cómo se consigue | Efecto |
|---|---|---|
| **La del Tano** | Historia (acto 1) | Gancho cargado, gran daño si conecta |
| **Aguante del Conurbano** | Ganar una pelea con menos del 20% de vida | Pasiva: una vez por pelea, te levantás con 30% en vez de caer |
| **Tren de la Belgrano** | Correr 10 veces | Embestida en carrera que cruza la pantalla |
| **Derribo de Club** | Grappling 8 veces | Derribo que no falla si el rival está sin estamina |
| **Mate Cocido** | Evento con la tía | Recupera estamina durante un round |
| **Mano de Piedra** | Fuerza 70+ | Los contragolpes hacen el doble |

## 7. Progresión / etapas

| # | Etapa | Lugar | Rivales |
|---|---|---|---|
| 0 | Tutorial | Calle frente a la estación | Los chorros (pelea perdida) |
| 1 | Barrio | Potrero / canchita | Pibes del barrio |
| 2 | Amateur | Club de barrio (Villa Madero) | Peleadores amateurs |
| 3 | Revancha | Calle, de noche | El chorro que lo robó |
| 4 | Regional | Estadio chico | Profesionales locales |
| 5 | Exterior | Evento en Brasil | Especialista en jiu-jitsu |
| 6 | La Liga | Octágono grande | Contendientes |
| 7 | Título | Octágono, evento principal | El campeón |

Entre etapa y etapa pasan 2 a 4 semanas de entrenamiento.

## 8. Dirección de arte

- **Resolución interna:** 320×224 (resolución del Genesis), escalada con *pixel-perfect*.
- **Paleta:** limitada, de 16 a 32 colores por escena. Estilo Genesis: contrastado y con tonos saturados.
- **Sprites de peleadores:** unos 64×96 px. Animaciones clave: idle, caminar, piña, patada, agarre, recibir golpe, caer y victoria.
- **Escenarios con parallax:** estación de tren, Av. Crovara, pasillos del barrio, gimnasio, club, octágono.
- **Interfaz:** barras al estilo Street Fighter II, tipografía pixel y menús de entrenamiento tipo tablero de corcho con fotos pegadas.
- **Cinemáticas:** viñetas estáticas con texto, como las intros de Streets of Rage.

## 9. Audio

- Chiptune estilo YM2612 (Furnace Tracker).
- Temas: barrio (cumbia chiptune), gimnasio (rock/funk), peleas (épico) y final (himno).
- SFX: golpes secos, campana, multitud.

## 10. Riesgos y consideraciones

- **Marca UFC:** no se puede usar el nombre ni el logo sin licencia. Hay que usar una liga ficticia (ej: "Liga Mundial de Octágono / LMO").
- **Representación del barrio:** evitar el estereotipo de "villa = delito" y mostrar comunidad. Idealmente, validarlo con gente de la zona.
- **Alcance:** el sistema de pelea es lo más riesgoso. Por eso el prototipo arranca por ahí.
- **Arte:** el pixel art animado lleva mucho tiempo. Se empieza con arte provisorio (placeholders).

## 11. Preguntas abiertas

- [ ] Plataforma final (¿web, PC, celular?).
- [ ] Profundidad de la pelea (¿arcade o más simulación?).
- [ ] ¿Quién hace el arte? ¿Hay presupuesto para un pixel artist?
- [ ] Nombre y trasfondo del protagonista.
- [ ] Título definitivo del juego.
