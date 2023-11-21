import pygame
import sys
from configuraciones import *
from random import *



### INICIALIZAMOS TODOS LOS MODULOS DE PYGAME ###############################################################################

pygame.init()

def dibujar_boton(x, y, text):
    try:
        fuente = pygame.font.Font(None, 36)
        boton = pygame.Rect(x, y, 250, 50)
        pygame.draw.rect(ventana , (0,0,0), boton)
        text_surface = fuente.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=boton.center)
        ventana.blit(text_surface, text_rect)
        return boton
    except:
        print("Error al dibujar el boton")
        
        
def mostrar_texto(superficie ,texto, fuente, coordenadas, color_fuente = (255,255,255), color_fondo = (0,230,0)):
    sup_texto = fuente.render(texto , True, color_fuente, color_fondo)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenadas
    superficie.blit(sup_texto, rect_texto)

reloj = pygame.time.Clock()
sigue_jugando = True
en_menu_principal = True
en_menu_opciones = False
ganaste = False
perdiste = False
en_juego = False
FPS = 10

while en_menu_principal:
    
        

    reloj.tick(FPS)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_menu_principal = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if iniciar_boton.collidepoint(pygame.mouse.get_pos()):
                perdiste = False
                en_menu_principal = True
            elif opciones_boton.collidepoint(pygame.mouse.get_pos()):
                en_menu_opciones = True
            elif salir_boton.collidepoint(pygame.mouse.get_pos()):
                en_menu_principal = False
                
    while en_menu_opciones:
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_menu_opciones = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if jugar_con_musica_boton.collidepoint(pygame.mouse.get_pos()):
                    pass
                elif jugar_sin_musica_boton.collidepoint(pygame.mouse.get_pos()):
                    pass
                elif volver_boton.collidepoint(pygame.mouse.get_pos()):
                    en_menu_opciones = False
                    en_menu_principal = True
                    

       
        jugar_con_musica_boton = dibujar_boton(500, 500, "Jugar con Música")
        jugar_sin_musica_boton = dibujar_boton(275, 300, "Jugar sin Música")
        volver_boton = dibujar_boton(275, 400, "Volver al menu")
        pygame.display.flip()
    
    while en_juego:
        
        pygame.mixer.music.pause()
        
        reloj.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
        pygame.display.flip()
    
    iniciar_boton = dibujar_boton(275, 200, "Iniciar Juego")
    opciones_boton = dibujar_boton(275, 300, "Opciones")
    salir_boton = dibujar_boton(275, 400, "Salir")
    pygame.display.flip()
    
    

pygame.quit()
sys.exit()
