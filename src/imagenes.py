import pygame
from configuraciones import *

try:
    icono_juego = pygame.image.load(r"./src\resources\img\icono_juego.png")

    fondo_menus = pygame.image.load(r"./src\resources\img\fondo_menu_principal.jpg")
    fondo_menus = pygame.transform.scale(fondo_menus, RESOLUCION_DE_PANTALLA)
    
    ravenclaw = pygame.image.load(r"./src\resources\img\Ravenclaw.jpg")
    ravenclaw = pygame.transform.scale(ravenclaw, (250,250))
    
    gryffindor = pygame.image.load(r"./src\resources\img\Gryffindor.png")
    gryffindor = pygame.transform.scale(gryffindor, (260,250))
    
    hufflepuff = pygame.image.load(r"./src\resources\img\Hufflepuff.jpg")
    hufflepuff = pygame.transform.scale(hufflepuff, (250,250))
    
    slytherin = pygame.image.load(r"./src\resources\img\Slytherin.jpg")
    slytherin = pygame.transform.scale(slytherin, (250,250))
    
            
except:
    print("Error al cargar los recursos (imagenes)")