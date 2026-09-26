# GDD: Del Barrio al Octágono (título provisorio)

> Documento vivo. Lo marcado con **[SUPUESTO]** es una decisión provisoria que falta validar.

## 1. Visión

Un juego corto y rejugable de 1 a 2 horas que mezcla **gestión de entrenamiento** (elegís qué hacer cada semana) con **peleas arcade en 2D**, todo en pixel art de 16 bits. Es la historia de un pibe del conurbano que pasa de que lo afanen en la estación a pelear por el título de la liga más grande del mundo.

**Pilares:**
1. **Identidad local:** Villa Celina, Villa Madero, la General Paz, Crovara, el tren, los monoblocks, el gimnasio de chapa.
2. **Progreso que se siente:** cada semana de entreno cambia cómo pelea el personaje.
3. **Arcade sencillito:** pocos botones, fácil de agarrar, sin lucha en el piso.

## 2. Plataforma y público

- **Navegador** (desktop y celular). Se juega con un link, sin instalar nada.
- **Controles:** teclado, joystick (Gamepad API) y controles táctiles en celular.
- **Público:** fans de juegos retro, de MMA y de historias argentinas.
- **Todo gratis:** motor, herramientas y hosting (ver §11).

## 3. Historia

**Protagonista:** **el nombre lo elige cada jugador** al empezar. En los mockups y el código de prueba usamos "Nahuel" como nombre por defecto. Tiene 19 años y llega al barrio a vivir con su tía (motivo a definir).

**Acto 1: La llegada**
- Intro tipo historieta: se baja del tren en la zona de Villa Celina / Villa Madero.
- Dos chorros lo encaran, le roban la mochila y el celular y le pegan.
- **Pelea tutorial imposible de ganar:** enseña los controles y termina en derrota.
- Lo levanta **"el Tano"**, dueño de un gimnasio del barrio: "Si querés que no te pase más, vení mañana."

**Acto 2: El barrio (peleas locales)**
- Entrena, consigue un laburo para pagar la cuota y hace amigos y rivales en el gimnasio.
- Pelea en la canchita, en un club de Villa Madero y en un torneo del conurbano.
- Revancha contra el chorro que lo robó.

**Acto 3: El continente (circuito de segunda línea)**
- Firma con una promotora chica y pelea afuera: Brasil, Chile, México.
- Gana un título continental de una liga "de segunda" y eso le abre la puerta a la grande.

**Acto 4: La liga grande**
- Debuta en la **UCF** (liga ficticia, ver §10).
- Sube en el ranking hasta la pelea por el título.

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
| Bolsa | +Fuerza, +Técnica | Energía media |
| Soga / Correr por el barrio | +Resistencia, +Velocidad | Energía media |
| Pesas | +Fuerza grande | Energía alta |
| Sparring | +Técnica, +Defensa, chance de aprender una especial | Energía alta, riesgo de lesión |
| Laburar | +Plata | Energía media |
| Descansar / Comer con la tía | +Energía, +Moral | Nada |

### 4.2 Stats

| Stat | Qué afecta en la pelea |
|---|---|
| **Fuerza** | Daño de golpes |
| **Velocidad** | Velocidad de movimiento y de ataque, ventana de esquive |
| **Resistencia** | Estamina máxima y recuperación |
| **Técnica** | Combos disponibles, precisión, chance de crítico |
| **Defensa** | Daño bloqueado, recuperación tras recibir un golpe |

Escala **1–100**. El protagonista arranca con 10 en todo.

### 4.3 Eventos del barrio
Tarjetas entre semanas con decisiones cortas. Ejemplos:
- "Te invitan a un asado el viernes" → +Moral, −Energía.
- "Te ofrecen una changa pesada" → +Plata, riesgo de lesión.
- "Se corta la luz en el gimnasio" → se pierde un turno o se entrena en la calle.

## 5. Sistema de pelea

**Arcade sencillito**, estilo Street Fighter II / Streets of Rage, ambientado en MMA. **No hay derribos ni lucha en el piso**: todo es de pie.

### 5.1 Controles
| Botón | Acción |
|---|---|
| ← → | Moverse / retroceder |
| ↓ | Agacharse / esquivar bajo |
| A | Piña (rápida) |
| B | Patada (lenta, más daño) |
| A+B | Especial equipada (gasta la barra de **Aguante**) |
| Mantener ← | Guardia |

### 5.2 Barras
- **Vida:** llega a 0 y hay KO.
- **Estamina:** cada ataque la gasta. Sin estamina los golpes son lentos y débiles.
- **Aguante:** se llena pegando y recibiendo golpes, y se usa para las especiales.

### 5.3 Reglas
- **3 rounds** de 60 segundos de juego.
- Se gana por KO o por decisión (puntos por golpes conectados).

## 6. Especiales ("podercitos" y piñitas)

Se desbloquean por historia, sparring o eventos. Solo se equipan **2 a la vez**.

| Nombre (provisorio) | Cómo se consigue | Efecto |
|---|---|---|
| **La del Tano** | Historia (acto 1) | Gancho cargado, gran daño si conecta |
| **Aguante del Conurbano** | Ganar una pelea con menos del 20% de vida | Pasiva: una vez por pelea, te levantás con 30% en vez de caer |
| **Tren de la Belgrano** | Correr 10 veces | Embestida en carrera que cruza la pantalla |
| **Voleo del Potrero** | Evento de fútbol en la canchita | Patada giratoria alta que rompe la guardia |
| **Mate Cocido** | Evento con la tía | Recupera estamina durante un round |
| **Mano de Piedra** | Fuerza 70+ | Los contragolpes hacen el doble |

## 7. Progresión / etapas

| # | Nivel | Etapa | Lugar | Rival (ejemplo) |
|---|---|---|---|---|
| 0 | Tutorial | La llegada | Calle frente a la estación | Los chorros (pelea perdida) |
| 1 | Local | Canchita | Potrero de Villa Celina | Pibe del barrio |
| 2 | Local | Club | Club de barrio en Villa Madero | Amateur del club rival |
| 3 | Local | Revancha | Calle, de noche | El chorro que lo robó |
| 4 | Local | Torneo del Conurbano | Polideportivo | Campeón del torneo |
| 5 | Continental | Liga de segunda | Río de Janeiro | Capoeirista brasileño |
| 6 | Continental | Liga de segunda | Santiago de Chile | Boxeador chileno |
| 7 | Continental | **Título continental** | Ciudad de México | Campeón mexicano |
| 8 | UCF | Debut | Octágono, Las Vegas | Contendiente del ranking |
| 9 | UCF | Semifinal | Octágono | Top 3 |
| 10 | UCF | **Título mundial** | Octágono, evento principal | El campeón |

Entre etapa y etapa pasan 2 a 4 semanas de entrenamiento. Cada nivel sube la dificultad de la IA y los stats de los rivales.

**Nombres de ligas (provisorios):**
- Continental / de segunda: **"Liga Continental de Combate (LCC)"**.
- Liga grande: **"UCF – Ultimate Combat Federation"**.

## 8. Dirección de arte

El arte lo genera Claude por código, con scripts en Python + Pillow en `tools/art/`. Cada escena o sprite se genera con un comando, se revisa y se ajusta.

- **Resolución interna:** 320×224 (resolución del Genesis), escalada con *pixel-perfect*.
- **Paleta:** los colores se ajustan a la paleta real del Genesis (9 bits, 8 niveles por canal).
- **Sprites de peleadores:** unos 40×64 px con contorno oscuro de 1 px. Animaciones clave: idle, caminar, piña, patada, recibir golpe, caer y victoria.
- **Escenarios con parallax:**
  - estación de tren con monoblocks y casas con tanque de agua;
  - Av. Crovara y pasillos del barrio;
  - gimnasio y club;
  - escenarios del exterior;
  - octágono.
- **Interfaz:** barras al estilo Street Fighter II, tipografía pixel y menús de entrenamiento tipo tablero de corcho.
- **Cinemáticas:** viñetas estáticas con texto, como las intros de Streets of Rage.

Primer mockup: [`assets/mockups/escena_estacion.png`](../assets/mockups/escena_estacion.png), generado con `python3 tools/art/mockup_estacion.py`.

## 9. Audio

- Chiptune estilo Genesis. Opciones gratis:
  - generarlo por código con Web Audio;
  - componerlo en Furnace Tracker.
- Temas: barrio (cumbia chiptune), gimnasio, peleas y final.
- SFX: golpes secos, campana, multitud.

## 10. Riesgos y consideraciones

- **Marca UFC:** no se usa el nombre ni el logo. Va la liga ficticia **UCF**, que se entiende igual.
- **Representación del barrio:** evitar el estereotipo de "villa = delito" y mostrar comunidad.
- **Alcance:** el sistema de pelea es lo más riesgoso. Por eso el prototipo arranca por ahí.

## 11. Herramientas (todas gratis)

| Para qué | Herramienta | ¿Hay que instalar algo? |
|---|---|---|
| Motor del juego | **Phaser 3** (JavaScript/TypeScript) | No: es una librería que corre en el navegador |
| Arte | **Python + Pillow** (scripts en `tools/art/`) | No para el usuario: lo corre Claude |
| Código | Este repo en GitHub | No |
| Publicar el juego | **GitHub Pages** | No: se juega desde un link |
| Música (opcional) | Furnace Tracker | Solo si alguien quiere componer a mano |

> **¿Por qué Phaser y no Godot?** Godot también es gratis y exporta a web, pero para editarlo hay que instalar su editor. Con Phaser todo es código y el juego se prueba en el navegador. Así el usuario no tiene que bajar nada: solo abre el link.

## 12. Preguntas abiertas

- [x] Plataforma: navegador.
- [x] Pelea: arcade, sin piso.
- [x] Arte: lo hace Claude por código.
- [x] Protagonista: el nombre lo elige el jugador.
- [ ] Título definitivo del juego.
- [ ] Nombres definitivos de las ligas (UCF / LCC).
- [ ] Trasfondo del protagonista (¿por qué llega al barrio?).
