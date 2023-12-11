import pygame
from pygame.locals import *
from configuraciones import *
from hoja_de_sprite import HojaDeSprites


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, grupos, hoja_sprite: HojaDeSprites, x, y, distancia_cambio_direccion_derecha,distancia_cambio_direccion_izquierda):
        super().__init__(grupos)
        self.animaciones = hoja_sprite.obtener_diccionario_de_animaciones(1)
        self.movimiento_actual = 0
        self.direccion = "derecha"
        self.image = self.animaciones[self.direccion][self.movimiento_actual]
        self.rect = self.image.get_rect(center=(x, y))
        self.mascara = pygame.mask.from_surface(self.image)
        self.velocidad_x = 5
        self.velocidad_y = 0
        self.ultima_actualizacion = pygame.time.get_ticks()
        self.tiempo_de_animacion = 100
        self.contador_pasos = 0
        self.contador_colision = 0
        self.tiempo_disparo = 0
        self.distancia_cambio_direccion_derecha = distancia_cambio_direccion_derecha
        self.distancia_cambio_direccion_izquierda = distancia_cambio_direccion_izquierda
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        self.contador_pasos += 1
        
        if tiempo_actual - self.ultima_actualizacion >= self.tiempo_de_animacion:
            self.movimiento_actual += 1
        
            if self.movimiento_actual == 3:
                self.movimiento_actual = 0
                
            if self.contador_pasos < self.distancia_cambio_direccion_derecha:
                self.rect.x += self.velocidad_x
                self.direccion = "derecha"
            elif self.contador_pasos >= self.distancia_cambio_direccion_derecha and self.contador_pasos < self.distancia_cambio_direccion_izquierda:
                self.rect.x -= self.velocidad_x
                self.direccion = "izquierda"
            elif self.contador_pasos >= self.distancia_cambio_direccion_izquierda:
                self.contador_pasos = 0
            
            self.image = self.animaciones[self.direccion][self.movimiento_actual]
            self.ultima_actualizacion = tiempo_actual
            
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
                    self.en_suelo = True
            
            if self.rect.bottom > plataforma.rect.top and self.rect.top < plataforma.rect.top:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = 0
                    self.en_suelo = True
            elif self.rect.top < plataforma.rect.bottom and self.rect.bottom > plataforma.rect.bottom:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidad_y = 0
                    self.en_suelo = False
    
    def verificar_colision_hechizos(self, hechizos, jugador):
        colisiones = pygame.sprite.spritecollide(self, hechizos, False)
        for hechizo in colisiones:
                if hechizo.rect.colliderect(self.rect):  
                    self.contador_colision += 1
                    hechizo.kill()
                    hechizo.rect.x = -1000
                    hechizo.rect.y = -1000
                    
                    if self.contador_colision == 3:
                        self.kill()
                        self.rect.x = -1000
                        self.rect.y = -1000
                        jugador.puntaje += 500

