

import sys    # para usar exit()
import time   # para usar sleep()
import pygame

ANCHO = 640 # Ancho de la pantalla.
ALTO = 480  # Alto de la pantalla.
color_celeste = (0, 0, 64)  # Color celeste para el fondo.
color_negro = (255, 255, 255) # Color negro, para textos.

pygame.init()

class Proyectil(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagen/proyectil.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla.
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        # Establecer velocidad inicial.
        self.speed = [5, 5]

    def update(self):
        # Evitar que salga por debajo.
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que salga por la derecha.
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)

class Barco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagen/barco.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla en X.
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        # Establecer velocidad inicial.
        self.speed = [3, 3]

    def update(self, evento):
        # Buscar si se presionó flecha izquierda.
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        # Si se presionó flecha derecha.
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)

class Barquito(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagen/barquito.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial, provista externamente.
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadBarquitos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadBarquitos):
            barquito =  Barquito((pos_x, pos_y))
            self.add(barquito)

            pos_x += barquito.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += barquito.rect.height

# Función llamada tras dejar ir el proyectil.
def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 72)
    texto = fuente.render(' PERDIO.. FIN DEL JUEGO ', True, color_negro)
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Pausar por tres segundos
    time.sleep(3)
    # Salir.
    sys.exit()

def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, color_negro)
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0, 0]
    pantalla.blit(texto, texto_rect)

def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, color_negro)
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO, 0]
    pantalla.blit(texto, texto_rect)

# Inicializando pantalla.
pantalla = pygame.display.set_mode((ANCHO, ALTO))
# Configurar título de pantalla.
pygame.display.set_caption('Barco Hundido')
# Crear el reloj.
reloj = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada.
pygame.key.set_repeat(30)

proyectil = Proyectil()
jugador = Barco()
muro = Muro(50)
puntuacion = 0
vidas = 3
esperando_saque = True

while True:
    # Establecer FPS.
    reloj.tick(60)

    # Revisar todos los eventos.
    for evento in pygame.event.get():
        # Si se presiona de la barra de título,
        if evento.type == pygame.QUIT:
            # cerrar el videojuego.
            sys.exit()
        # Buscar eventos del teclado,
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)
            if esperando_saque == True and evento.key == pygame.K_SPACE:
                esperando_saque = False
                if proyectil.rect.centerx < ANCHO / 2:
                    proyectil.speed = [3, -3]
                else:
                    proyectil.speed = [-3, -3]

    # Actualizar posición.
    if esperando_saque == False:
        proyectil.update()
    else:
        proyectil.rect.midbottom = jugador.rect.midtop

    # Colisión.
    if pygame.sprite.collide_rect(proyectil, jugador):
        proyectil.speed[1] = -proyectil.speed[1]

    # Colisión de la proyectil con el muro.
    lista = pygame.sprite.spritecollide(proyectil, muro, False)
    if lista:
        barquito = lista[0]
        cx = proyectil.rect.centerx
        if cx < barquito.rect.left or cx > barquito.rect.right:
            proyectil.speed[0] = -proyectil.speed[0]
        else:
            proyectil.speed[1] = -proyectil.speed[1]
        muro.remove(barquito)
        puntuacion += 10

    # Revisar si proyectil sale de la pantalla.
    if proyectil.rect.top > ALTO:
        vidas -= 1
        esperando_saque = True

    # Rellenar la pantalla.
    pantalla.fill(color_celeste)
    # Mostrar puntuación
    mostrar_puntuacion()
    # Mostrar vidas.
    mostrar_vidas()
    # Dibujar bolita en pantalla.
    pantalla.blit(proyectil.image, proyectil.rect)
    # Dibujar jugador en pantalla.
    pantalla.blit(jugador.image, jugador.rect)
    # Dibujar los ladrillos.
    muro.draw(pantalla)
    # Actualizar los elementos en pantalla.
    pygame.display.flip()

    if vidas <= 0:
        juego_terminado()


