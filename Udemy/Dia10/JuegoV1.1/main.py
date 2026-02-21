import math
import pygame
import random
from pygame import mixer
import io



# -------------------------
# Inicialización (audio + pygame)
# -------------------------
pygame.mixer.pre_init(44100, -16, 2, 512)  # mejora estabilidad/latencia del audio
pygame.init()
mixer.set_num_channels(16)  # más canales para varios sonidos simultáneos

# -------------------------
# Pantalla
# -------------------------
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Invasion espacial')

# Icono y fondo
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# -------------------------
# Música de fondo
# -------------------------
mixer.music.load("musica_fondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# -------------------------
# Sonidos (cargar UNA sola vez)
# -------------------------
sonido_bala = mixer.Sound("disparo.mp3")
sonido_bala.set_volume(0.5)

sonido_colision = mixer.Sound("explosion.mp3")
sonido_colision.set_volume(0.7)

# Canales dedicados (evita que se pisen)
canal_bala = mixer.Channel(0)
canal_explosion = mixer.Channel(1)

# -------------------------
# Jugador
# -------------------------
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# -------------------------
# Enemigos (listas)
# -------------------------
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("ovni_enemy.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# -------------------------
# Balas
# -------------------------
balas = []
img_bala = pygame.image.load("bala.png")

# (estas variables ya no se usan directamente, pero las dejo para no “obviar” nada)
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 0.1
bala_visible = False

def fuente_bytes(fuente):
    #abre el archivo TT en modo lectura binaria
    with open(fuente, 'rb') as f:
        #lee todos los butes del archivo y los almacena en una variable
        ttf_bytes = f.read()
    #crea un objeto BytesIO a parir de los bytes del archivo TIF
    return io.BytesIO(ttf_bytes)


# -------------------------
# Puntaje
# -------------------------
puntaje = 0
fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10

# Texto final
fuente_final = pygame.font.Font(fuente_como_bytes, 40)

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))



def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (225, 225, 225))
    pantalla.blit(mi_fuente_final, (60, 200))

def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

def disparar_bala(x, y):
    # Esta función queda por compatibilidad con tu código original,
    # pero en esta versión estamos usando la lista "balas".
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    return distancia < 27

# -------------------------
# Loop del juego
# -------------------------
se_ejecuta = True
while se_ejecuta:

    # Fondo
    pantalla.blit(fondo, (0, 0))

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                # reproducir sonido de disparo sin recargar archivo
                canal_bala.play(sonido_bala)

                # crear bala nueva
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Movimiento jugador
    jugador_x += jugador_x_cambio

    # Bordes jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Enemigos
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        # Movimiento enemigo
        enemigo_x[e] += enemigo_x_cambio[e]

        # Bordes enemigo (CORREGIDO)
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.1
            enemigo_y[e] += enemigo_y_cambio[e]   # <-- FIX (antes estaba mal)
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.1
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colisiones bala-enemigo
        for bala in balas[:]:  # <-- iterar sobre copia para poder remover seguro
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                canal_explosion.play(sonido_colision)

                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento balas (CORREGIDO)
    for bala in balas[:]:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))

        if bala["y"] < 0:
            balas.remove(bala)

    # Dibujar jugador
    jugador(jugador_x, jugador_y)

    # Puntaje
    mostrar_puntaje(texto_x, texto_y)

    # Actualizar pantalla
    pygame.display.update()

pygame.quit()