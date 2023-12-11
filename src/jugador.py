import pygame
from pygame.locals import *
from configuraciones import *
from hoja_de_sprite import HojaDeSprites

pygame.init()

class Jugador(pygame.sprite.Sprite):
    def __init__(self, grupos, hoja_sprite: HojaDeSprites):
        super().__init__(grupos)
        
        self.animaciones = hoja_sprite.obtener_diccionario_de_animaciones(1)
        self.movimiento_actual = 0
        self.image = self.animaciones["derecha"][self.movimiento_actual]
        self.rect = self.image.get_rect(center = (50,1000))
        self.mascara = pygame.mask.from_surface(self.image)
        self.velocidad_x = 20
        self.velocidad_y = 0
        self.ultima_actualizacion = pygame.time.get_ticks()    
        self.tiempo_de_animacion = 100
        self.en_suelo = True
        
    def update(self): 
        
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            if self.rect.right <= ancho:
                self.rect.x += self.velocidad_x
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.ultima_actualizacion >= self.tiempo_de_animacion:
                    self.movimiento_actual += 1
                    self.image = self.animaciones["derecha"][self.movimiento_actual]
                    if self.movimiento_actual == 3:
                        self.movimiento_actual = 0
                    self.ultima_actualizacion = tiempo_actual
        if keys[K_LEFT]:
            if self.rect.x >= 0:
                self.rect.x -= self.velocidad_x
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.ultima_actualizacion >= self.tiempo_de_animacion:
                    self.movimiento_actual += 1
                    self.image = self.animaciones["izquierda"][self.movimiento_actual]
                    if self.movimiento_actual == 3:
                        self.movimiento_actual = 0
                    self.ultima_actualizacion = tiempo_actual
        if keys[K_SPACE] and self.en_suelo:
                self.velocidad_y = -50
                self.en_suelo = False
        
        self.velocidad_y += 10
        
        self.rect.y += self.velocidad_y
        
        if self.rect.bottom > dimension_ventana.current_h:
            self.rect.bottom = dimension_ventana.current_h
            self.velocidad_y = 0
            self.en_suelo = True
       
    def verificar_colision(self, plataformas):
        colisiones = pygame.sprite.spritecollide(self, plataformas, False )
        for plataforma in colisiones:
            
            if self.velocidad_y >= 0:
                if self.rect.bottom > plataforma.rect.top and self.rect.top < plataforma.rect.top:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = 0
            elif self.velocidad_y < 0: 
                if self.rect.top < plataforma.rect.bottom and self.rect.bottom > plataforma.rect.bottom:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidad_y = 0
                   

            if self.velocidad_y > 0:   
                self.rect.bottom = plataforma.rect.top
                self.velocidad_y = 0    
                self.en_suelo = True
            elif self.velocidad_y < 0:   
                self.rect.top = plataforma.rect.bottom
                self.velocidad_y = 0
                self.en_suelo = False    
        
          
            if self.rect.bottom > plataforma.rect.top:
                self.velocidad_y = 0
                self.en_suelo = False
            else:
                self.en_suelo = True
                
