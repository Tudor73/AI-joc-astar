from tkinter import E
import pygame 
import os

class Piesa:

    razaPiesa=20
    def __init__(self, x, y):
        self.x= x
        self.y = y
    
    def deseneaza_piesa(self, ecran, piesa):

        image_rect = piesa.get_rect()
        image_rect.x = self.x - self.__class__.razaPiesa
        image_rect.y = self.y - self.__class__.razaPiesa
        ecran.blit(piesa, image_rect)
        pygame.display.update()

    def __repr__(self):
        sir = f"({self.x}, {self.y})"
        return sir
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y