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
