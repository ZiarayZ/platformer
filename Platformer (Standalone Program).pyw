from random import randint,choice
import pygame
import os

#Has to be referenced before some classes
l=0
g=0
deaths=0

class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(50,50,20,20) #Location and size
        self.onGround=True #Defining player variables
        self.onWall=True
        self.onJump=False
        self.onRun=False
        self.colour=[(0,0,0)]

    def move(self,dx,dy):
        if dx != 0:
            self.move_single_axis(dx,0)

        if dy != 0:
            self.move_single_axis(0,dy)

    def move_single_axis(self,dx,dy):
        global l
        global g
        self.rect.x += dx
        self.rect.y += dy

        for surface in surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dx > 0:
                    self.rect.right = surface.rect.left
                if dx < 0:
                    self.rect.left = surface.rect.right
                if dy > 0:
                    self.rect.bottom = surface.rect.top
                    self.onGround=True #So that player can jump again
                    l = 0#Helps stop glitches from falling from great heights
                if dy < 0:
                    self.rect.top = surface.rect.bottom
                    g = 0

        for door in doors:
            if self.rect.colliderect(door.rect):#Collide with Surfaces
                if dx > 0:
                    self.rect.right = door.rect.left
                if dx < 0:
                    self.rect.left = door.rect.right
                if dy > 0:
                    self.rect.bottom = door.rect.top
                    self.onGround=True #So that player can jump again
                    l = 0#Helps stop glitches from falling from great heights
                if dy < 0:
                    self.rect.top = door.rect.bottom
                    g = 0

        for wall in walls:
            if self.rect.colliderect(wall.rect):#Checking if player is touching a wall
                self.onWall=True

        for jump in jumps:
            if self.rect.colliderect(jump.rect):#Checking if on jump pad
                self.onJump=True

        for run in runs:
            if self.rect.colliderect(run.rect):
                self.onRun=True

class EnemyH(object):

    def __init__(self,wx,wy):
        enemiesH.append(self)
        self.rect = pygame.Rect(wx,wy,10,10) #Location and size
        self.direction = choice(["left","right"])
        self.speed = randint(3,7)

    def move(self,dx,dy):
        if dx != 0:
            self.move_single_axis(dx,0)

    def move_single_axis(self,dx,dy):
        global deaths
        global l
        self.rect.x += dx

        if self.rect.colliderect(player.rect):
            player.rect.x = 10
            player.rect.y = 690
            deaths += 1
            l = 0
        
        for surface in surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dx > 0:
                    self.direction = "right"
                if dx < 0:
                    self.direction = "left"
        for door in doors:
            if self.rect.colliderect(door.rect):#Collide with Doors
                if dx > 0:
                    self.direction = "right"
                if dx < 0:
                    self.direction = "left"

class EnemyV(object):

    def __init__(self,wx,wy):
        enemiesV.append(self)
        self.rect = pygame.Rect(wx,wy,10,10) #Location and size
        self.direction = choice(["up","down"])
        self.speed = randint(3,5)

    def move(self,dx,dy):
        if dy != 0:
            self.move_single_axis(0,dy)

    def move_single_axis(self,dx,dy):
        global l
        global deaths
        self.rect.y += dy

        if self.rect.colliderect(player.rect):
            player.rect.x = 10
            player.rect.y = 690
            deaths += 1
            l = 0
        
        for surface in surfaces:
            if self.rect.colliderect(surface.rect):#Collide with Surfaces
                if dy > 0:
                    self.direction = "down"
                if dy < 0:
                    self.direction = "up"
        for door in doors:
            if self.rect.colliderect(door.rect):#Collide with Doors
                if dy > 0:
                    self.direction = "down"
                if dy < 0:
                    self.direction = "up"

#Walls/Platforms and Spikes
class Wall(object):
    def __init__(self,wx,wy): #Background,Climbable
        walls.append(self)
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(130,150),randint(60,80),randint(10,30))

    def reset_wall(self):
        self.active = False

class Surface(object):
    def __init__(self,wx,wy): #Foreground,Collidable
        surfaces.append(self)
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(0,20),randint(90,110),randint(0,20))

    def reset_surface(self):
        self.active = False

class Door(object):
    def __init__(self,wx,wy): #Foreground,Collidable
        doors.append(self)
        self.rect = pygame.Rect(wx,wy,10,10)
        self.colour = (randint(120,130),randint(120,130),randint(120,130))

    def reset_door(self):
        self.active = False

class Jump(object):
    def __init__(self,wx,wy):
        jumps.append(self)
        self.rect = pygame.Rect(wx,wy+8,10,2)
        self.colour = (100,128,255)

    def reset_jump(self):
        self.active = False

class Run(object):
    def __init__(self,wx,wy):
        runs.append(self)
        self.rect = pygame.Rect(wx,wy+16,10,2)
        self.colour = (255,128,100)

    def reset_run(self):
        self.active = False

#Variables
walls = []
surfaces = []
jumps = []
runs = []
doors = []
enemiesH = []
enemiesV = []
player = Player() #Create a player object from class
p_colour = player.colour[0]
speed = 5
turn = 0
g=0 #Created 2 variables for gravity as it gets extremely complicated to use only one
l=0
width = 1080
height = 720
firstRunning = True

#Start pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#Set up Display
pygame.display.set_caption("Probably Some Great Platforming Game?")
screen = pygame.display.set_mode((width,height))

#Create ingame clock
clock = pygame.time.Clock()

x=y=0
#Generate Main Menu
with open("levels/1main_menu.txt","r") as f:
    for row in f:
        for col in row:
            if col.upper() == "P":#P - Player
                player.rect.x = x
                player.rect.y = y
            if col.upper() == "T":#T - Door
                Door(x,y)
            if col.upper() == "S":#S - Surface
                Surface(x,y)
            if col.upper() == "X":#X - Exit
                Exit = pygame.Rect(x,y,10,10)
            if col.upper() == "E":#E - Start
                end_rect = pygame.Rect(x,y,10,10)
            if col.upper() == "K":#K - Key
                key = pygame.Rect(x,y+2,10,6)
            x += 10
        y += 10
        x = 0
            
#Loop Main Menu
while firstRunning:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            firstRunning = False
    
    #Allow Player to move
    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_UP]:
        player.onGround = True
        player.move(0,-5) #Move up

    if user_input[pygame.K_DOWN]:
        player.onGround = True
        player.move(0,5) #Move down

    if user_input[pygame.K_LEFT]:
        player.move(-5,0) #Move left

    if user_input[pygame.K_RIGHT]:
        player.move(5,0) #Move right

    if player.rect.colliderect(key):
        del doors[:]
        key = pygame.Rect(1000,1002,10,6)

    if player.rect.colliderect(end_rect):
        firstRunning,secondRunning = False,True
        del surfaces[:] #End of a level, reconstruction
        del doors[:]

    if player.rect.colliderect(Exit):
        firstRunning,secondRunning = False,False

    #Draw everything
    screen.fill((204,255,255)) #Fill screen, light blue
    for surface in surfaces:
        pygame.draw.rect(screen,surface.colour,surface.rect)#Draw Foreground blocks onto screen

    for door in doors:
        pygame.draw.rect(screen,door.colour,door.rect)#Draw Doors

    pygame.draw.rect(screen,(0,255,255),end_rect)#Draw start
    pygame.draw.rect(screen,(255,0,0),Exit)#Draw exit
    pygame.draw.rect(screen,(0,0,0),key)#Draw Key
    pygame.draw.rect(screen,p_colour,player.rect)#Draw Player
    pygame.display.update()#Update screen
    pygame.display.flip()


#Generate Level
levelTurn=6
y=x=0
with open("levels/level ("+str(levelTurn)+").txt","r") as f:
    for row in f:
        for col in row:
            if col.upper() == "W":#W - Wall
                Wall(x,y)
            if col.upper() == "S":#S - Surface
                Surface(x,y)
            if col.upper() == "E":#E - Escape
                end_rect = pygame.Rect(x,y,10,10)
            if col.upper() == "P":#P - Player
                player.rect.x = x
                player.rect.y = y
            if col.upper() == "C":#C - Coin/Currency
                coin = pygame.Rect(x+3,y+3,5,5)
            if col.upper() == "J":#J - Jump Pad
                Jump(x,y)
            if col.upper() == "R":#R - Speed Pad
                Run(x,y)
            if col.upper() == "T":#T - Door
                Door(x,y)
            if col.upper() == "K":#K - Key
                key = pygame.Rect(x,y+2,10,6)
            if col.upper() == "H":#H - Horizontal Moving Enemy
                EnemyH(x,y)
            if col.upper() == "V":#V - Vertical Moving Enemy
                EnemyV(x,y)
            x+=10
        y+=10
        x=0

#Loop game
while secondRunning:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            secondRunning = False

        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
            turns = len(player.colour)
            turn += 1
            if turn == turns:
                turn = 0
            p_colour = player.colour[turn]

    #AI movement
    for enemy in enemiesH:
        if enemy.direction == "left":
            enemy.move(enemy.speed,0)
        if enemy.direction == "right":
            enemy.move(-enemy.speed,0)

    for enemy in enemiesV:
        if enemy.direction == "up":
            enemy.move(0,enemy.speed)
        if enemy.direction == "down":
            enemy.move(0,-enemy.speed)

    #Allow Player to move
    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_UP]and(player.onGround or player.onWall or player.onJump):#Allow it to jump
        player.onGround=False
        player.onWall=False
        if player.onJump:
            g=25
        else:
            g=15
        player.onJump = False
        player.move(0,-g)

    elif player.onGround==False: #Being pulled back down
        player.move(0,-g)
        g -= 1

    else:
        l+= 1
        playerLOC=player.rect.y #Pulling player down when not on surface
        player.move(0,l)

        if playerLOC==player.rect.y:#Checking to see if player is on a surface
            l=0

        else:
            player.onWall=False

    if player.rect.y > height:
        player.rect.y = 690
        l=0

    if user_input[pygame.K_LEFT]:
        if player.onRun and speed == 5:
            speed *= 2
            player.onRun=False
        elif speed > 5:
            speed -= 1
        player.move(-speed,0) #Move left

    if user_input[pygame.K_RIGHT]:
        if player.onRun and speed == 5:
            speed *= 2
            player.onRun=False
        elif speed > 5:
            speed -= 1
        player.move(speed,0) #Move right

    if user_input[pygame.K_BACKSPACE]:
        player.rect.y = 690
        player.rect.x = 10
        l = 0
        g = 0

    if player.rect.colliderect(coin):
        atuple = (randint(0,255),randint(0,255),randint(0,255))
        player.colour.append(atuple)
        coin = pygame.Rect(1000,1000,5,5)

    if player.rect.colliderect(key):
        del doors[:]
        key = pygame.Rect(1000,1002,10,6)

    if player.rect.colliderect(end_rect):
       del walls[:]
       del surfaces[:] #End of a level, reconstruction
       del jumps[:]
       del runs[:]
       del doors[:]
       del enemiesH[:]
       del enemiesV[:]
       
       levelTurn+=1

       y=x=0
       try:#When all levels are complete, throws error
           with open("levels/level ("+str(levelTurn)+").txt","r") as f:
               for row in f:
                   for col in row:
                       if col.upper() == "W":#W - Wall
                            Wall(x,y)
                       if col.upper() == "S":#S - Surface
                           Surface(x,y)
                       if col.upper() == "E":#E - Escape
                           end_rect = pygame.Rect(x,y,10,10)
                       if col.upper() == "P":#P - Player
                           player.rect.x = x
                           player.rect.y = y
                       if col.upper() == "C":#C - Coin/Currency
                           coin = pygame.Rect(x+3,y+3,4,4)
                       if col.upper() == "J":#J - Jump Pad
                           Jump(x,y)
                       if col.upper() == "R":#R - Speed Pad
                           Run(x,y)
                       if col.upper() == "T":#T - Door
                           Door(x,y)
                       if col.upper() == "K":#K - Key
                           key = pygame.Rect(x,y+2,10,4)
                       if col.upper() == "H":#H - Horizontal Moving Enemy
                           EnemyH(x,y)
                       if col.upper() == "V":#V - Vertical Moving Enemy
                           EnemyV(x,y)
                       x+=10
                   y+=10
                   x=0

       except IOError:
           secondRunning = False
           break

    #Recreating the screen
    screen.fill((204,255,255)) #Fill screen, light blue

    for wall in walls:
        pygame.draw.rect(screen,wall.colour,wall.rect)#Draw background blocks onto screen

    for surface in surfaces:
        pygame.draw.rect(screen,surface.colour,surface.rect)#Draw Foreground blocks onto screen

    for jump in jumps:
        pygame.draw.rect(screen,jump.colour,jump.rect)#Draw Jump Pads

    for run in runs:
        pygame.draw.rect(screen,run.colour,run.rect)#Draw Speed Pads

    for door in doors:
        pygame.draw.rect(screen,door.colour,door.rect)#Draw Doors

    for enemy in enemiesH:
        pygame.draw.rect(screen,(randint(0,255),randint(0,255),randint(0,255)),enemy.rect)#Draw horizontal moving enemies

    for enemy in enemiesV:
        pygame.draw.rect(screen,(randint(0,255),randint(0,255),randint(0,255)),enemy.rect)#Draw vertical moving enemies

    pygame.draw.rect(screen,(255,0,0),end_rect)#Draw exit
    pygame.draw.rect(screen,(255,255,0),coin)#Draw Coin/Currency
    pygame.draw.rect(screen,(0,0,0),key)#Draw Key
    pygame.draw.rect(screen,p_colour,player.rect)#Draw Player
    pygame.display.update()#Update screen
    pygame.display.flip()
    
pygame.quit()#Close the game
