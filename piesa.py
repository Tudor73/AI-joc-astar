from tkinter import E
import pygame 
import os

class Piesa:
    def __init__(self, culoare, x, y):
        self.culoar = culoare
        self.x= x
        self.y = y
    
    def deseneaza_piesa(self, ecran):
        image = pygame.image.load(os.path.join('images', 'black.png'))    

        image_rect = image.get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        ecran.blit(image, image_rect)
        pygame.display.update()

    def __repr__(self):
        sir = f"{self.culoare}, ({self.x}, {self.y})"
        return sir