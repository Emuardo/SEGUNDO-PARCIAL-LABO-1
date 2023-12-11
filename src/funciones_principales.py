import pygame
from configuraciones import *

def mostrar_texto(superficie, texto, tamaño_fuente, coordenadas, color_fuente = (255,255,255), color_fondo = None):
    try:
        fuente = pygame.font.SysFont("Harry P", tamaño_fuente) 
        sup_texto = fuente.render(texto , True, color_fuente, color_fondo)
        rect_texto = sup_texto.get_rect()
        rect_texto.center = coordenadas
        superficie.blit(sup_texto, rect_texto)
    except:
        print("Error al dibujar el texto en la pantalla")

def dibujar_boton(superficie, posicion_x, posicion_y, ancho_boton, largo_boton, texto_boton, tamaño_de_texto_boton, color_texto_boton, color_boton):
    try:
        font = pygame.font.SysFont("Harry P", tamaño_de_texto_boton)
        boton = pygame.Rect(posicion_x, posicion_y, ancho_boton, largo_boton)
        pygame.draw.rect(superficie, color_boton, boton, border_radius = 25)
        text_surface = font.render(texto_boton, True, color_texto_boton)
        text_rect = text_surface.get_rect(center=boton.center)  
        superficie.blit(text_surface, text_rect)
        
        return boton
    except:
        print("Error al dibujar el botón en la pantalla")
        

        
        
