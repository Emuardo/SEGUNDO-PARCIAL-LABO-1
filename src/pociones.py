import pygame

class PocionesMagicas(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    