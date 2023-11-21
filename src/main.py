import pygame
from imagenes import *
from funciones_principales import *
from configuraciones import *


pygame.init()
pygame.font.init()

ventana = pygame.display.set_mode(RESOLUCION_DE_PANTALLA)
pygame.display.set_caption("Harry Potter y La Batalla de Hogwarts")
pygame.display.set_icon(icono_juego)

### VARIABLES ###
jugando = True

while(jugando):
    
    for evento in pygame.event.get():
        if(evento.type == pygame.QUIT):
            jugando = False
    
    ventana.blit(fondo_menus, (0,0))
    mostrar_texto(ventana, "Harry Potter y La Batalla de Hogwarts", 100, (ANCHO // 2, 350), (212,175,100))
    mostrar_texto(ventana, "Harry Potter y La Batalla de Hogwarts", 99, (ANCHO// 2, 350), (255,0,0))
    ventana.blit(ravenclaw, (400, 5))
    ventana.blit(gryffindor, (700, 5))
    ventana.blit(hufflepuff, (1000, 5))
    ventana.blit(slytherin, (1300, 5))
    
    pygame.display.flip()
    
pygame.quit()
