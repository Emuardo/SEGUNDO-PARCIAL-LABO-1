import pygame
from pygame.locals import *
from configuraciones import *
from hoja_de_sprite import HojaDeSprites

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, grupos, hoja_sprite: HojaDeSprites, x, y):
        super().__init__(grupos)

        self.animaciones = hoja_sprite.obtener_diccionario_de_animaciones(1)
        self.movimiento_actual = 0
        self.direccion = "derecha"
        self.image = self.animaciones[self.direccion][self.movimiento_actual]
        self.rect = self.image.get_rect(center=(x, y))
        self.mascara = pygame.mask.from_surface(self.image)
        self.velocidad_x = 5
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.tiempo_de_animacion = 100
        self.contador_pasos = 0
    
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        self.contador_pasos += 1
        print(self.contador_pasos)
        if tiempo_actual - self.ultima_actualizacion >= self.tiempo_de_animacion:
            self.movimiento_actual += 1
        
            if self.movimiento_actual == 3:
                self.movimiento_actual = 0
                
            if self.contador_pasos < 30:
                self.rect.x += self.velocidad_x
                self.direccion = "derecha"
            elif self.contador_pasos >= 30 and self.contador_pasos < 60:
                self.rect.x -= self.velocidad_x
                self.direccion = "izquierda"
            elif self.contador_pasos >= 60:
                self.contador_pasos = 0
            
            self.image = self.animaciones[self.direccion][self.movimiento_actual]
            self.ultima_actualizacion = tiempo_actual
            

        
        