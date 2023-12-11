import pygame

class HechizosAvanzados(pygame.sprite.Sprite):
    def __init__(self, grupos, color, posicion_inicial, radio, duracion):
        super().__init__(grupos)
        self.radio = radio
        self.image = pygame.Surface((2 * radio, 2 * radio), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radio, radio), radio, 5)
        self.rect = self.image.get_rect(center=posicion_inicial)
        self.duracion = duracion
        self.colision = 0

    def update(self):
        # Lógica de actualización del hechizo de protección avanzado
        self.duracion -= 1
        if self.duracion <= 0:
            self.kill()
    
    def verificar_colision_entre_hechizos_avanzados(self, hechizos):
        colision = pygame.sprite.spritecollide(self, hechizos, False)
        for hechizo in colision:
            self.colision += 1
            hechizo.kill()
            if self.colision == 2:
                hechizo.kill()
                self.rect.x = -1000
                self.rect.y = -1000