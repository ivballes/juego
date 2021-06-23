



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

    

    if vidas <= 0:
        juego_terminado()


