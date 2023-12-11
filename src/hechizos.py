import pygame
from configuraciones import *

class Hechizos(pygame.sprite.Sprite):
    def __init__(self, grupos, color, velocidad, posicion_inicial, ancho, largo, direccion = None):
        super().__init__(grupos)
        self.ancho = ancho
        self.largo = largo
        self.image = pygame.Surface((self.ancho, self.largo))
        self.image.fill(color)
        self.direccion = direccion
        self.velocidad = velocidad
        self.duracion = 75
        # Determina la posición inicial según la dirección
        if direccion == "izquierda":
            self.rect = self.image.get_rect(midright=posicion_inicial)
            
        elif direccion == "derecha":
            self.rect = self.image.get_rect(midleft=posicion_inicial)

    def update(self):
        self.duracion -= 1
        if self.duracion <= 0:
            self.kill()
        
        if self.direccion == "izquierda":
            self.rect.x -= self.velocidad
            
        elif self.direccion == "derecha":
            self.rect.x += self.velocidad

        if self.rect.right < 0 or self.rect.left > dimension_ventana.current_w:
            self.rect.x = -1000
            self.rect.y = -1000

   
                
                
            