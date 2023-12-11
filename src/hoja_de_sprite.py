import pygame
from configuraciones import *

class HojaDeSprites:
    def __init__(self, hoja_sprite:pygame.Surface, filas:int, columnas:int, ancho:int, largo:int, claves = None) -> None:
        self.hoja_sprite = hoja_sprite
        self.ancho = self.hoja_sprite.get_width()
        self.largo = self.hoja_sprite.get_height()
        self.filas = filas
        self.columnas = columnas
        self.ancho_sprite = ancho
        self.largo_sprite = largo
        self.claves = claves
        
    def obtener_lista_de_animaciones(self, escala = 1)-> list:
        self.ancho = escala * self.ancho
        self.largo = escala * self.largo
        self.ancho_sprite = escala * self.ancho_sprite
        self.largo_sprite = escala * self.largo_sprite
        
        self.hoja_sprite = pygame.transform.scale(self.hoja_sprite, (self.ancho, self.largo))
        contador_columnas = 0
        lista_de_animaciones = []

        for fila in range(self.filas):
            animacion_filas = []
            for _ in range(self.columnas):
                animacion_filas.append(self.hoja_sprite.subsurface((contador_columnas * self.ancho_sprite,fila * self.largo_sprite, self.ancho_sprite, self.largo_sprite)))
                contador_columnas += 1
            contador_columnas = 0
            
            lista_de_animaciones.append(animacion_filas)
            
        return lista_de_animaciones

    def obtener_diccionario_de_animaciones(self, escala = 1)-> dict:
        self.ancho = escala * self.ancho
        self.largo = escala * self.largo
        self.ancho_sprite = escala * self.ancho_sprite
        self.largo_sprite = escala * self.largo_sprite
        
        self.hoja_sprite = pygame.transform.scale(self.hoja_sprite, (self.ancho, self.largo))
        contador_columnas = 0
        diccionario_de_animaciones = {}

        for fila in range(self.filas):
            animacion_filas = []
            for _ in range(self.columnas):
                animacion_filas.append(self.hoja_sprite.subsurface((contador_columnas * self.ancho_sprite,fila * self.largo_sprite, self.ancho_sprite, self.largo_sprite)))
                contador_columnas += 1
            diccionario_de_animaciones[self.claves[fila]] = animacion_filas
            contador_columnas = 0
        
        return diccionario_de_animaciones

