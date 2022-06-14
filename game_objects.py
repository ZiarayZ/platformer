from random import randint
import pygame

class Box(object):
    def __init__(self,wx,wy,version="Surface"):
        self.rect = pygame.Rect(wx,wy,10,10)
        if version == "Wall": #Background, Climbable
            self.colour = (randint(130,150),randint(60,80),randint(10,30))
        elif version == "Surface": #Foreground, Collidable
            self.colour = (randint(0,20),randint(90,110),randint(0,20))
        elif version == "Door": #Foreground, Collidable
            self.colour = (randint(120,130),randint(120,130),randint(120,130))

class Pad(object):
    def __init__(self,wx,wy,version="Jump"):
        if version == "Jump":
            editVal = 8
            self.colour = (100,128,255)
        elif version == "Run":
            editVal = 16
            self.colour = (255,128,100)
        self.rect = pygame.Rect(wx,wy+editVal,10,2)
