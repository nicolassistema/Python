# 🚀 Invasión Espacial -- Guía Completa del Código

Este documento explica la estructura completa del juego desarrollado en
**Python + Pygame**. Sirve como plantilla base para futuros proyectos.

------------------------------------------------------------------------

# 📦 1. Importaciones

``` python
import math
import pygame
import random
from pygame import mixer
```

## ¿Qué hace cada una?

-   **math** → Permite usar funciones matemáticas como `sqrt()` para
    calcular distancias.
-   **pygame** → Motor del juego (ventana, teclado, imágenes, sonido).
-   **random** → Genera posiciones aleatorias.
-   **mixer** → Sistema de sonido de pygame.

------------------------------------------------------------------------

# 🎛 2. Inicialización

``` python
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.set_num_channels(16)
```

-   Configura audio.
-   Inicializa todos los módulos.
-   Permite múltiples sonidos simultáneos.

------------------------------------------------------------------------

# 🖥 3. Pantalla

``` python
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Invasion espacial')
```

-   Crea ventana 800x600.
-   Define título.

------------------------------------------------------------------------

# 🖼 4. Recursos gráficos

``` python
icono = pygame.image.load("ovni.png")
fondo = pygame.image.load("fondo.jpg")
```

-   `load()` solo carga la imagen.
-   Para dibujar se usa `blit()`.

------------------------------------------------------------------------

# 🎵 5. Música

``` python
mixer.music.load("musica_fondo.mp3")
mixer.music.play(-1)
```

-   `play(-1)` = loop infinito.
-   Se usa para música larga.

------------------------------------------------------------------------

# 🔊 6. Sonidos

``` python
sonido_bala = mixer.Sound("disparo.mp3")
sonido_colision = mixer.Sound("explosion.mp3")
```

-   Se cargan una sola vez.
-   Se reproducen con `.play()`.
-   Se pueden usar canales separados.

------------------------------------------------------------------------

# 🚀 7. Jugador

``` python
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
```

Movimiento básico:

``` python
jugador_x += jugador_x_cambio
```

Posición + velocidad = movimiento.

------------------------------------------------------------------------

# 👾 8. Enemigos

Se usan listas para múltiples enemigos:

``` python
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
```

Cada enemigo tiene: - Posición - Velocidad - Imagen

------------------------------------------------------------------------

# 🔫 9. Balas

``` python
balas = []
```

Cada bala es un diccionario:

``` python
{
 "x": jugador_x,
 "y": jugador_y,
 "velocidad": -5
}
```

Velocidad negativa = sube.

------------------------------------------------------------------------

# 💥 10. Colisiones

``` python
distancia = sqrt((x1-x2)^2 + (y1-y2)^2)
```

Si la distancia es menor que un valor → hay colisión.

------------------------------------------------------------------------

# 🔁 11. Loop Principal

``` python
while se_ejecuta:
```

En cada frame:

1.  Dibujar fondo
2.  Leer eventos
3.  Actualizar posiciones
4.  Detectar colisiones
5.  Dibujar objetos
6.  Actualizar pantalla

------------------------------------------------------------------------

# 🧠 Arquitectura base de cualquier juego Pygame

1.  Importaciones\
2.  Inicialización\
3.  Carga de recursos\
4.  Variables\
5.  Funciones\
6.  Loop principal

------------------------------------------------------------------------

# 🎯 Nivel del Proyecto

✔ Múltiples enemigos\
✔ Múltiples balas\
✔ Sistema de puntaje\
✔ Sonido estable\
✔ Detección de colisiones

Nivel: **Intermedio**

------------------------------------------------------------------------

# 🚀 Cómo reutilizar esta estructura

Podés crear:

-   Juego de zombies
-   Juego de autos
-   Juego de plataformas
-   Juego tipo shooter vertical

Solo cambiando sprites y lógica.

------------------------------------------------------------------------

# 📌 Conclusión

Este proyecto es una base sólida para entender:

-   Ciclo de renderizado
-   Movimiento por velocidad
-   Manejo correcto de sonido
-   Colisiones matemáticas
-   Arquitectura básica de videojuegos
