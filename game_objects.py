from random import randint,choice
import pygame

class Player(object):

    def __init__(self,walls,surfaces,jumps,runs,doors,x,y):
        self.walls = walls
        self.surfaces = surfaces
        self.jumps = jumps
        self.runs = runs
        self.doors = doors
        self.rect = pygame.Rect(x,y,20,20) #Location and size
        self.onGround=True #Defining player variables
        self.onWall=True
        self.onJump=False
        self.onRun=False

    def move(self,dx,dy,l,g):
        if dx != 0:
            self.move_single_axis(dx,0,l,g)

        if dy != 0:
            self.move_single_axis(0,dy,l,g)

    def move_single_axis(self,dx,dy,l,g):
        self.l = l
        self.g = g
        self.rect.x += dx
        self.rect.y += dy

        for surface in self.surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dx > 0:
                    self.rect.right = surface.rect.left
                if dx < 0:
                    self.rect.left = surface.rect.right
                if dy > 0:
                    self.rect.bottom = surface.rect.top
                    self.onGround=True #So that player can jump again
                    self.l = 0#Helps stop glitches from falling from great heights
                if dy < 0:
                    self.rect.top = surface.rect.bottom
                    self.g = 0

        for door in self.doors:
            if self.rect.colliderect(door.rect):#Collide with Surfaces
                if dx > 0:
                    self.rect.right = door.rect.left
                if dx < 0:
                    self.rect.left = door.rect.right
                if dy > 0:
                    self.rect.bottom = door.rect.top
                    self.onGround=True #So that player can jump again
                    self.l = 0#Helps stop glitches from falling from great heights
                if dy < 0:
                    self.rect.top = door.rect.bottom
                    self.g = 0

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):#Checking if player is touching a wall
                self.onWall=True

        for jump in self.jumps:
            if self.rect.colliderect(jump.rect):#Checking if on jump pad
                self.onJump=True

        for run in self.runs:
            if self.rect.colliderect(run.rect):
                self.onRun=True

class EnemyH(object):

    def __init__(self,wx,wy,surfaces,doors):
        self.surfaces = surfaces
        self.doors = doors
        self.rect = pygame.Rect(wx,wy,10,10) #Location and size
        self.direction = choice(["left","right"])
        self.speed = randint(3,7)

    def move(self,dx,dy):
        if dx != 0:
            self.move_single_axis(dx,0)

    def move_single_axis(self,dx,dy):
        self.rect.x += dx
        
        for surface in self.surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dx > 0:
                    self.direction = "right"
                if dx < 0:
                    self.direction = "left"
        for door in self.doors:
            if self.rect.colliderect(door.rect):#Collide with Doors
                if dx > 0:
                    self.direction = "right"
                if dx < 0:
                    self.direction = "left"

class EnemyV(object):

    def __init__(self,wx,wy,surfaces,doors):
        self.surfaces = surfaces
        self.doors = doors
        self.rect = pygame.Rect(wx,wy,10,10) #Location and size
        self.direction = choice(["up","down"])
        self.speed = randint(3,5)

    def move(self,dx,dy):
        if dy != 0:
            self.move_single_axis(0,dy)

    def move_single_axis(self,dx,dy):
        self.rect.y += dy
        
        for surface in self.surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dy > 0:
                    self.direction = "down"
                if dy < 0:
                    self.direction = "up"
        for door in self.doors:
            if self.rect.colliderect(door.rect):#Collide with Doors
                if dy > 0:
                    self.direction = "down"
                if dy < 0:
                    self.direction = "up"

class Wall(object):
    def __init__(self,wx,wy): #Background,Climbable
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(130,150),randint(60,80),randint(10,30))

    def reset_wall(self):
        self.active = False

class Surface(object):
    def __init__(self,wx,wy): #Foreground,Collidable
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(0,20),randint(90,110),randint(0,20))

    def reset_surface(self):
        self.active = False

class Door(object):
    def __init__(self,wx,wy): #Foreground,Collidable
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(120,130),randint(120,130),randint(120,130))

    def reset_door(self):
        self.active = False

class Jump(object):
    def __init__(self,wx,wy):
        self.rect = pygame.Rect(wx,wy+8,10,2)
        self.colour = (100,128,255)

    def reset_jump(self):
        self.active = False

class Run(object):
    def __init__(self,wx,wy):
        self.rect = pygame.Rect(wx,wy+16,10,2)
        self.colour = (255,128,100)

    def reset_run(self):
        self.active = False
