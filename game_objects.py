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
