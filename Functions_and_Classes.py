## Importing modules
import pygame as py
import random
import math
from Constants import *

## Class to handle keyboard inputs and to make it possible to have key rebinds
class Keyboard():
    def __init__(self,controls):
        temp = []
        for i in range(len(controls)):
            temp.append([controls[i],False])
        #Set of scancodes and bools of the states of the keys
        self.controls = temp 
    def update(self,event):
        for i in range(len(self.controls)):
            if event.type == py.KEYDOWN:
                if event.scancode == self.controls[i][0]+1:
                    self.controls[i][1] = True
            elif event.type == py.KEYUP:
                if event.scancode == self.controls[i][0]+1:
                    self.controls[i][1] = False
                    
## Class for handling the spawning and despawning of upgrades 
class Upgrade():
    def __init__(self,pos,u_type,sprite):
        
        ## Type of upgrade
        self.u_type = u_type
        
        ## Time left to pick up the upgrade in frames
        self.time = 150
        
        ## Position of the upgrade sprite
        self.x, self.y = pos
        
        ## Upgrade sprite
        self.sprite = sprite
        
    ## Method for updating the time and drawing the sprite    
    def update(self,screen):
        self.time -= 1
        screen.blit(self.sprite,[self.x,self.y])
    
## Function that returns a bool of whether or not an item is in a list
def list_check(x,y):
    if x.count(y) != 0:
        return True
    else:
        return False
    
## Updates the highscore in the text file
def UpdateScore(highscore,difficulty,lines):
    lines[-1] = ""
    for i in range(10):
        lines[-1] = lines[-1]+str(highscore[i])+" "                 
    with open('Resources/settings.txt','w') as x:
        x.writelines("%s\n" % l for l in lines)
        
## Class for handling music             
class Radio():
    def __init__(self):
        self.time = 0
        self.sound = None
    def play(self,sound):
        if self.sound != None:
            self.sound.stop()    
        self.time = 30*py.mixer.Sound.get_length(sound)
        self.sound = sound
        self.sound.play()
    def update(self):
        if self.time == 0:
            self.sound = None
        else:
            self.time -= 1
            
## Function involved in spawn rate
def spawn_rate(diff,x):
    return 50/(x+diff)

## Function to determine the enemy count each wave
def enemy_amount(diff,x):
    return int((diff/5)*x**2 + 5*x + 30)

## Function for easy font creation    
def font(size):
    font = py.font.SysFont('Calibri', size, True, False)
    return font

## Function for resizing variables for different screen sizes
def resize(x,width):
    return width*x/1280

## Function for creating a vector given two points and a magnitude
def target(pos1,pos2,speed):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    hyp = (dx**2+dy**2)**(1/2)
    ratio = speed/hyp
    x_speed = dx*ratio
    y_speed = dy*ratio
    return [x_speed,y_speed]

## Class for updating, creating, and deleting the player projectiles
class Projectile():
    def __init__(self,p_pos,speeds,sprite):
        
        ## Projectile position
        self.x, self.y = p_pos
        
        ## Splitting the given vector into two speed variables for x and y
        self.x_speed,self.y_speed = speeds
        
        ## Projectile sprite
        self.sprite = sprite
        
    ## Method for moving and drawing the projectiles
    def update(self,screen):
        width, height = screen.get_size()
        self.x += self.x_speed
        self.y += self.y_speed
        screen.blit(self.sprite,[self.x,self.y])
        
## Class for updating, spawning, and despawning enemies
class Enemy():
    def __init__(self,sprite,screen):
        width, height = screen.get_size()
        x = random.randrange(-width-height//16,2*width)
        
        ## Random spawn location
        if -height//32 < x < width:
            y = random.choice([random.randrange(-width-height//16,-height//16),random.randrange(height,height+width)])
        else:
            y = random.randrange(-width,height+width)
            
        ## Enemy position
        self.pos = [x,y]
        
        ## Enemy sprite
        self.sprite = sprite
        
        ## Enemy speed
        self.speed = resize(7,width)
        
    ## Updating stats and moving the enemy    
    def update(self,player,screen):
        if list_check(player.upgrades,2):
            n = 2/3
        else:
            n = 1
        width, height = screen.get_size()
        x, y = target(self.pos,[player.pos[0]+(height//12-height//16)//2,player.pos[1]+(height//12-height//16)//2],self.speed)
        self.pos[0] += n*x
        self.pos[1] += n*y
        screen.blit(self.sprite,[self.pos[0],self.pos[1]])
        
## Class creating and updating the stats of the player(s)    
class Player():
    def __init__(self,sprite,pos,proj_sprite,size,shield):
        
        ## Player position
        self.pos = pos
        
        ## List of player projectiles
        self.shots = []
        
        ## Sprite for the player
        self.sprite = sprite
        
        ## Sprite for the shield upgrade
        self.shield = shield
        
        ## Sprite for the projectile
        self.proj_sprite = proj_sprite
        
        ## Upgrades; 0 is increased fire rate, 1 is quad shot, 2 is slow enemies, 3 is shield, 4 is screen kill
        self.upgrades = []
        
        ## Time left on each upgrade; this is paired with the above list
        self.upgrade_times = []
        
        ## Player size
        self.size = size
        
    ## Updating stats, projectiles and a tonne of other things    
    def update(self,controls,screen):
        width, height = screen.get_size()
        x,y = 0,0
        
        ## If the ___ key is press...
        if controls[2][1]:
            y -= resize(20,width)
        if controls[3][1]:
            y += resize(20,width)
        if controls[4][1]:
            x -= resize(20,width)
        if controls[5][1]:
            x += resize(20,width)
            
        ## Adjusting the player speed if they are going diagonally (Otherwise they would be going faster)    
        if x == resize(20,width) and y == resize(20,width):
            x,y = target([0,0],[x,y],resize(20,width))

        ## Collision with the edge of the screen    
        if self.pos[0] + x > width - height//12:
            x = 0
            self.pos[0] = width - height//12
        elif self.pos[0] + x < 0:
            x = 0
            self.pos[0] = 0
        if self.pos[1] + y > height - height//12:
            y = 0
            self.pos[1] = height - height//12
        elif self.pos[1] + y < 0:
            y = 0
            self.pos[1] = 0
            
        ## Adding the speeds to the player position    
        self.pos[0] += x
        self.pos[1] += y
        
        ## Updating the player shots
        for shot in self.shots:
            shot.update(screen)
            
        ## If the projectile goes of the screen it is deleted to prevent lag
        temp = 0
        for i in range(len(self.shots)):
            pos1,pos2 = [self.shots[i-temp].x,self.shots[i-temp].y], [0,0]
            if not check_collision(pos1,pos2,[height//25,height//25],screen.get_size()):
                self.shots.pop(i-temp)
                temp+=1
                
        ## Drawing the player on the screen
        screen.blit(self.sprite,self.pos)
        
        ## If they have the shield upgrade draw the shield
        if list_check(self.upgrades,3):
            screen.blit(self.shield,[self.pos[0]+height//24-height//20,self.pos[1]+height//24-height//20])

        ## Upgrading the upgrade times and deleting them if they are out of time
        temp = 0
        for i in range(len(self.upgrade_times)):
            self.upgrade_times[i-temp] -= 1
            if self.upgrades[i-temp] == 4 and self.upgrade_times[i-temp] > 1:
                self.upgrade_times[i-temp] = 1
            if self.upgrade_times[i-temp] < 1:
                self.upgrades.pop(i-temp)
                self.upgrade_times.pop(i-temp)
                temp += 1
                
    ## Method for creating projectiles        
    def shoot(self,m_pos,screen):
        x_speed, y_speed = target(self.pos,[m_pos[0]-screen.get_size()[1]//50,m_pos[1]-screen.get_size()[1]//50],resize(20,screen.get_size()[0]))

        ## If you have the quad-shot upgrade you shoot three extra projectiles
        if list_check(self.upgrades,1):
            self.shots.append(Projectile([self.pos[0]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2,self.pos[1]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2],[-x_speed,-y_speed],self.proj_sprite))
            self.shots.append(Projectile([self.pos[0]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2,self.pos[1]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2],[y_speed,-x_speed],self.proj_sprite))
            self.shots.append(Projectile([self.pos[0]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2,self.pos[1]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2],[-y_speed,x_speed],self.proj_sprite))     
        self.shots.append(Projectile([self.pos[0]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2,self.pos[1]+(screen.get_size()[1]//12-screen.get_size()[1]//25)//2],[x_speed,y_speed],self.proj_sprite))

## Function for collision detection between two rectangles given their positions and demensions as sets of data
def check_collision(pos1,pos2,sizes1,sizes2):
    o1_x,o1_y = pos1
    o2_x,o2_y = pos2
    o1_w,o1_h = sizes1
    o2_w,o2_h = sizes2
    delta_x,delta_y = abs(o1_x-o2_x),abs(o1_y-o2_y)
    if (o1_x > o2_x and delta_x < o2_w) or (o1_x <= o2_x and delta_x < o1_w):
        if o1_y > o2_y and delta_y < o2_h:
            return True
        elif o1_y <= o2_x and delta_y < o1_h:
            return True
        else:
            return False                
    else:
        return False

