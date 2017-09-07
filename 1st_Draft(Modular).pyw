from game_objects import *
from random import randint,choice
from time import sleep
import pygame
import os

#Variables
walls = []
surfaces = []
jumps = []
runs = []
doors = []
enemiesH = []
enemiesV = []
player = Player(walls,surfaces,jumps,runs,doors,10,690) #Create a player object from class
player_colour = [(0,0,0)]
p_colour = player_colour[0]
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
                doors.append(Door(x,y))
            if col.upper() == "S":#S - Surface
                surfaces.append(Surface(x,y))
            if col.upper() == "X":#X - Exit
                Exit = pygame.Rect(x,y,10,10)
            if col.upper() == "E":#E - Start
                end_rect = pygame.Rect(x,y,10,10)
            if col.upper() == "K":#K - Key
                key = pygame.Rect(x,y+2,10,6)
            x += 10
        y += 10
        x = 0
    player = Player(walls,surfaces,jumps,runs,doors,player.rect.x,player.rect.y)
            
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
        player.move(0,-5,l,g) #Move up

    if user_input[pygame.K_DOWN]:
        player.onGround = True
        player.move(0,5,l,g) #Move down

    if user_input[pygame.K_LEFT]:
        player.move(-5,0,l,g) #Move left

    if user_input[pygame.K_RIGHT]:
        player.move(5,0,l,g) #Move right

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
levelTurn=1
y=x=0
with open("levels/level ("+str(levelTurn)+").txt","r") as f:
    for row in f:
        for col in row:
            if col.upper() == "W":#W - Wall
                walls.append(Wall(x,y))
            if col.upper() == "S":#S - Surface
                surfaces.append(Surface(x,y))
            if col.upper() == "E":#E - Escape
                end_rect = pygame.Rect(x,y,10,10)
            if col.upper() == "P":#P - Player
                player.rect.x = x
                player.rect.y = y
            if col.upper() == "C":#C - Coin/Currency
                coin = pygame.Rect(x+3,y+3,5,5)
            if col.upper() == "J":#J - Jump Pad
                jumps.append(Jump(x,y))
            if col.upper() == "R":#R - Speed Pad
                runs.append(Run(x,y))
            if col.upper() == "T":#T - Door
                doors.append(Door(x,y))
            if col.upper() == "K":#K - Key
                key = pygame.Rect(x,y+2,10,6)
            x+=10
        y+=10
        x=0
    player = Player(walls,surfaces,jumps,runs,doors,player.rect.x,player.rect.y)
y=x=0
with open("levels/level ("+str(levelTurn)+").txt","r") as f:
    for row in f:
        for col in row:
            if col.upper() == "H":#H - Horizontal Moving Enemy
                enemiesH.append(EnemyH(x,y,surfaces,doors))
            if col.upper() == "V":#V - Vertical Moving Enemy
                enemiesV.append(EnemyV(x,y,surfaces,doors))
            x+=10
        y+=10
        x=0

#Incase in the main menu the user closes the window
try:
    if secondRunning:
        pass
except NameError:
    secondRunning = False

#Loop game
while secondRunning:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            secondRunning = False

        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
            turns = len(player_colour)
            turn += 1
            if turn == turns:
                turn = 0
            p_colour = player_colour[turn]

    #AI movement
    for enemy in enemiesH:
        if enemy.rect.colliderect(player.rect):
            player.rect.x = 10
            player.rect.y = 690
        if enemy.direction == "left":
            enemy.move(enemy.speed,0)
        if enemy.direction == "right":
            enemy.move(-enemy.speed,0)

    for enemy in enemiesV:
        if enemy.rect.colliderect(player.rect):
            player.rect.x = 10
            player.rect.y = 690
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
        player.move(0,-g,l,g)

    elif player.onGround==False: #Being pulled back down
        player.move(0,-g,l,g)
        if player.g == 0:
            g = 0
        g -= 1

    else:
        l+= 1
        playerLOC=player.rect.y #Pulling player down when not on surface
        player.move(0,l,l,g)
        l = player.l

        if playerLOC==player.rect.y:#Checking to see if player is on a surface
            l=player.l=0

        else:
            player.onWall=False

    if player.rect.y > height:
        player.rect.y = 690
        l=player.l=0

    if user_input[pygame.K_LEFT]:
        if player.onRun and speed == 5:
            speed *= 2
            player.onRun=False
        elif speed > 5:
            speed -= 1
        player.move(-speed,0,l,g) #Move left

    if user_input[pygame.K_RIGHT]:
        if player.onRun and speed == 5:
            speed *= 2
            player.onRun=False
        elif speed > 5:
            speed -= 1
        player.move(speed,0,l,g) #Move right

    if user_input[pygame.K_BACKSPACE]:
        player.rect.y = 690
        player.rect.x = 10
        l=player.l=g=player.g=0

    if player.rect.colliderect(coin):
        atuple = (randint(0,255),randint(0,255),randint(0,255))
        player_colour.append(atuple)
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
                           walls.append(Wall(x,y))
                       if col.upper() == "S":#S - Surface
                           surfaces.append(Surface(x,y))
                       if col.upper() == "E":#E - Escape
                           end_rect = pygame.Rect(x,y,10,10)
                       if col.upper() == "P":#P - Player
                           player.rect.x = x
                           player.rect.y = y
                       if col.upper() == "C":#C - Coin/Currency
                           coin = pygame.Rect(x+3,y+3,5,5)
                       if col.upper() == "J":#J - Jump Pad
                           jumps.append(Jump(x,y))
                       if col.upper() == "R":#R - Speed Pad
                           runs.append(Run(x,y))
                       if col.upper() == "T":#T - Door
                           doors.append(Door(x,y))
                       if col.upper() == "K":#K - Key
                           key = pygame.Rect(x,y+2,10,6)
                       x+=10
                   y+=10
                   x=0
           y=x=0
           with open("levels/level ("+str(levelTurn)+").txt","r") as f:
               for row in f:
                   for col in row:
                       if col.upper() == "H":#H - Horizontal Moving Enemy
                           enemiesH.append(EnemyH(x,y,surfaces,doors))
                       if col.upper() == "V":#V - Vertical Moving Enemy
                           enemiesV.append(EnemyV(x,y,surfaces,doors))
                       x+=10
                   y+=10
                   x=0
               player = Player(walls,surfaces,jumps,runs,doors,player.rect.x,player.rect.y)

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
print("Thanks for Playing!")
sleep(5)
