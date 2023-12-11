import pygame
from configuraciones import *

try:
    fondo_menus = pygame.image.load(r"./src\resources\img\fondo_menu_principal.jpg")
    fondo_menus = pygame.transform.scale(fondo_menus, resolucion_de_pantalla)
    
    fondo_menu_perdiste = pygame.image.load(r"./src\resources\img\imagen_fondo_perdiste.jpg")
    fondo_menu_perdiste = pygame.transform.scale(fondo_menu_perdiste, resolucion_de_pantalla)
    
    ravenclaw = pygame.image.load(r"./src\resources\img\Ravenclaw.jpg")
    ravenclaw = pygame.transform.scale(ravenclaw, (250,250))
    
    gryffindor = pygame.image.load(r"./src\resources\img\Gryffindor.png")
    gryffindor = pygame.transform.scale(gryffindor, (260,250))
    
    hufflepuff = pygame.image.load(r"./src\resources\img\Hufflepuff.jpg")
    hufflepuff = pygame.transform.scale(hufflepuff, (250,250))
    
    slytherin = pygame.image.load(r"./src\resources\img\Slytherin.jpg")
    slytherin = pygame.transform.scale(slytherin, (250,250))        
    
    fondo_niveles = pygame.image.load(r"src\resources\img\fondo_niveles.png")
    fondo_niveles = pygame.transform.scale(fondo_niveles, resolucion_de_pantalla)
    
except:
    print("Error al cargar los recursos (imagenes)")
    
try: 
    pygame.mixer.music.load(r"./src\resources\sounds\sonido_menus.mp3")
    
    sonidos_niveles = pygame.mixer.Sound(r"./src\resources\sounds\sonido_niveles.mp3")
    
    sonido_jefe_final = pygame.mixer.Sound(r"./src\resources\sounds\sonido_pelea_final.mp3")
except:
    print("Error al cargar los recursos (sonidos)")