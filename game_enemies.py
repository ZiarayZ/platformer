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
