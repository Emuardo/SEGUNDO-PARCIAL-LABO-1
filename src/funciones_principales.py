import pygame
from configuraciones import *

def mostrar_texto(superficie ,texto,tamaño_fuente, coordenadas, color_fuente = (255,255,255), color_fondo = None):
    fuente = pygame.font.SysFont("Harry P", tamaño_fuente) 
    sup_texto = fuente.render(texto , True, color_fuente, color_fondo)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenadas
    superficie.blit(sup_texto, rect_texto)
