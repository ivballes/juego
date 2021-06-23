

import sys    # para usar exit()
import time   # para usar sleep()
import pygame

ANCHO = 640 # Ancho de la pantalla.
ALTO = 480  # Alto de la pantalla.


# Inicializando pantalla.
pantalla = pygame.display.set_mode((ANCHO, ALTO))

pygame.display.set_caption('Barco Hundido')


while True:
  
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # cerrar el videojuego.
            sys.exit()
       
            