import pygame

pygame.init()

dimension_ventana = pygame.display.Info()
ancho , largo = dimension_ventana.current_w , dimension_ventana.current_h

ANCHO_JUGADOR = 32
LARGO_JUGADOR = 48

resolucion_de_pantalla = (ancho,largo)

FPS = 40

### PALETA DE COLORES ###

color_dorado = (255, 223, 0)
color_negro = (0,0,0)
color_blanco = (255,255,255)
color_plateado = (192,192,192)
color_rojo = (208,0,0)
color_bordo = (118,11,9)
color_celeste = (7,129,163)
color_celeste_oscuro = (5,84,120)
color_amarillo = (216,171,13)
color_amarillo_oscuro = (161,120,20)
color_gris = (205,205,205)
color_verde = (28,123,27)
color_verde_oscuro = (17,72,15)


