## Code Written by Daniel Dallaire
## Version 1.1
## Last Edit: January 4th, 2016

        ## --- Patch Notes --- ##
# -- Added a instructions tab to the options menu 
# -- Credits screen was redone
# -- Pause screen was redone
# -- Gameover screen was redone
# -- Titlescreen was redone
# -- Main text colour was changed from a black
#    to a blue to fit the backgrounds better
# -- Game settings were moved to their
#    own screen from the titlescreen
# -- Highscores were moved to their own
#    screen from the titlescreen
# -- A power up system was added
#    in which when enemies are killed
#    there is a chance to drop power
#    ups for the player to pick up,
#    currently there is 5 different
#    power ups
# -- Added random animations for the titlescreen


## Importing modules
import pygame as py
from Functions_and_Classes import *
from Constants import *
import random
import os

## Starting the pygame engine
py.init()

## Defining the screen size 
size = (600, 400)

## Creating the option screen
options_screen = py.display.set_mode(size)

## Setting the window text for the option screen 
py.display.set_caption("MYFOESIS Options")

## Setting the window icon for the option screen and main screen
icon = os.getcwd() + '\\Resources\\Sprites\\player_blue.png'
icon = py.image.load(icon)
py.display.set_icon(icon)

## Reading from the text file of saved options
x = open('Resources/settings.txt','r')                                      
text = x.readlines()
x.close()

## Setting the screen res
screen_res = resolutions[int(text[0])]

## Setting the volume levels
volumes = [int(text[1]),int(text[2])]

## Importing the click sound
click_sound = py.mixer.Sound("Resources/Sound/click_sound.ogg")
click_sound.set_volume(volumes[1]/100)

## Importing the background for the options
background = py.image.load("Resources/Images/options_background.jpg")
background = py.transform.scale(background,size)

## Setting the control scancodes in a list from the text file
controls = []
for i in range(6):
    controls.append(int(text[3+i]))

## Setting the highscores from the text file
highscore = []
for i in range(10):
    highscore.append("")
temp = text[9].strip()
temp2 = 0
for i in range(len(temp)):
    if temp[i] == " ":
        temp2+=1
    else:
        highscore[temp2]+=temp[i]
for i in range(10):
    highscore[i] = int(highscore[i])
    
## Variable to process rebinds in the controls part of the options
rebind = []
for i in range(6):
    rebind.append(False)
rebind.append(True)

## Variable set to False until the options window needs to be closed
done = False

## The current option tab
c_opt = "v"

## Variable that stores a bool for the mouse click
click = False

## Sets the clock for the window
clock = py.time.Clock()

## Variable for mouse click cooldown
m_cool = 0

## Bool to ensure that nothing opens if the user closes the options menu
end = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in py.event.get():
        
        ## Allows the window to close
        if event.type == py.QUIT:
            done = True
            end = True
            
        ## Stores the last key as a scancode in a variable for rebindability
        elif event.type == py.KEYDOWN:
            last_key = event.scancode
        else:
            last_key = None
            
    ## Sets the mouse position                
    m_pos = py.mouse.get_pos()
    
    ## Changes the mouse click bool
    if py.mouse.get_pressed()[0]:
        click = True
        if m_cool < 1:
            click_sound.play()
        m_cool = 5  
    else:
        click = False
        m_cool-=1
        
    ## Fills the screen with the background image    
    options_screen.blit(background,[0,0])
    
    ## Main vertical line
    py.draw.line(options_screen, Black, [200, 10], [200, 390], 1)
    
    ## Base lines and drawings for the options window
    for i in range(5):
        
        ## Dashes next to each option text/button
        py.draw.line(options_screen, Black, [180, (i+1)*400//6], [195, (i+1)*400//6], 1)
        
        ## If the option tab is currently open the text is greeb instead of black
        if option_strings[i][0].lower() == c_opt:
            temp = Green
        else:
            temp = Black

        ## Printing the option tab name to the screen
        text = font(30).render(option_strings[i],True,temp)
        options_screen.blit(text, [170-text.get_width(),(i+1)*400//6-text.get_height()//2])

        ## If you click a button go to that tab
        if click and 50 <= m_pos[0] <= 180 and (i+1)*400//6-text.get_height()//2 <= m_pos[1] <= (i+1)*400//6+text.get_height()//2:
           c_opt = option_strings[i][0].lower()
           if c_opt == "l":
               done = True
               
    ## Controls tab code        
    if c_opt == "c":

        ## For loop for each of the 6 controls
        for i in range(6):

            ## Printing the key name
            text = font(30).render(control_strings[i],True,Black)
            options_screen.blit(text, [240, (i+1)*size[1]//7-30//2])

            ## Drawing the rectangle around the key name
            py.draw.rect(options_screen,Black,([350,(i+1)*size[1]//7-25],[200,50]),2)

            ## If you clicked a key, the program now listens for a key press to rebind the control
            if rebind[i]:
                text = font(30).render("[Enter Key]",True,Black)
                options_screen.blit(text, [450-text.get_width()//2,(i+1)*size[1]//7-30//2])
                if last_key != None:
                    controls[i] = last_key-1
                    rebind[i] = False
            else:
                if controls.count(controls[i]) > 1:
                    colour = Red
                else:
                    colour = Black
                text = font(30).render(scancode_strings[controls[i]],True,colour)
                options_screen.blit(text, [450-text.get_width()//2,(i+1)*size[1]//7-30//2])

            ## If you clicked a key name and nothing else is currently being rebinded...    
            if click and rebind.count(True) < 2:
                if 350 <= m_pos[0] <= 550 and (i+1)*size[1]//7-25 <= m_pos[1] <= (i+1)*size[1]//7+25:
                    rebind[i] = True
                    
    ## Audio tab code            
    elif c_opt == "a":

        ## Setting the click sound volume
        click_sound.set_volume(volumes[1]/100)

        ## Printing "Music Volume" to the screen
        text = font(30).render("Music Volume",True,Black)
        options_screen.blit(text, [240,50])

        ## Printing "SFX Volume" to the screen
        text = font(30).render("SFX Volume",True,Black)
        options_screen.blit(text, [240,150])

        ## For loop for the two volume sliders
        for i in range(2):

            ## Different lines that make up the slider
            py.draw.line(options_screen, Black, [240, 105+i*100], [240, 125+i*100], 2)
            py.draw.line(options_screen, Black, [240, 115+i*100], [440, 115+i*100], 2)
            py.draw.line(options_screen, Black, [440, 105+i*100], [440, 125+i*100], 2)
            py.draw.line(options_screen, Black, [240+2*volumes[i], 105+i*100], [240+2*volumes[i], 125+i*100], 3)

            ## Printing the volumes to the screen
            text = font(20).render(str(volumes[i]),True,Black)
            options_screen.blit(text, [450,105+i*100])
            
        ## Code for changing the volume
        if click and 230 <= m_pos[0] <= 450:
            temp = (m_pos[0]-240)//2
            if temp < 0:
                temp = 0
            elif temp > 100:
                temp = 100
                
            if 100 <= m_pos[1] <= 130:
                volumes[0] = temp
            elif 200 <= m_pos[1] <= 230:
                volumes[1] = temp
    
    ## Video tab code
    elif c_opt == "v":
        text = font(30).render("Resolutions:",True,Black)
        options_screen.blit(text, [240,50])
        
        ## Small box to show which option the resolution is set at
        py.draw.rect(options_screen,Black,([243,103+50*resolutions.index(screen_res)],[14,14]))
        
        ## 3 bigger boxs and text info on the resolutions
        for i in range(3):
            py.draw.rect(options_screen,Black,([240,100+50*i],[20,20]),1)
            text = font(20).render(resolutions[i][1]+" "+str(resolutions[i][0]),True,Black)
            options_screen.blit(text, [280,100+50*i])
            ## If click an unchecked box
            if click and 240 <= m_pos[0] <= 260 and 100+50*i <= m_pos[1] <= 100+50*i+20:
                screen_res = resolutions[i]

    ## Instructions tab code
    elif c_opt == "i":
        text = font(30).render("Welcome to MYFOESIS",True,Black)
        options_screen.blit(text, [220,30])
        ## Goes through a list of lines to blit
        for i in range(len(instruction_strings)):
            text = font(25).render(instruction_strings[i],True,Black)
            options_screen.blit(text, [220,25+45*(i+1)])
    
    ## Flips the screen      
    py.display.flip()
    
    ## Sets the fps
    clock.tick(30)
    
## Allows you to quit
py.quit()


## Sets the lines to be wrote to the text file
lines = [str(resolutions.index(screen_res)),str(volumes[0]),str(volumes[1])]
for i in controls:
    lines.append(str(i))
temp = ""
for i in highscore:
    temp += str(i)+" "

lines.append(temp)
    
## Writes the lines variable to the text file    
with open('Resources/settings.txt','w') as x:
    x.writelines("%s\n" % l for l in lines)
x.close()

screen_res_o = screen_res

## Creating the volume variables
music_volume = volumes[0]
sfx_volume = volumes[1]


if not end:
    ## Starting the pygame engine
    py.init()

    ## Sets the screen resolution
    screen_res = screen_res[0]
    
    ## Creates the main screen
    screen = py.display.set_mode(screen_res)
    
    ## Sets the main window title
    py.display.set_caption("MYFOESIS")
    
    ## Variable set to False until the main window needs to be closed
    done = False
    
    ## Loading and resizing images and sprites
    player_size = screen_res[1]//12
    p_blue = py.image.load("Resources/Sprites/player_blue.png")
    p_blue = py.transform.scale(p_blue,[player_size,player_size])
    p_green = py.image.load("Resources/Sprites/player_green.png")
    p_green = py.transform.scale(p_green,[player_size,player_size])
    p_orange = py.image.load("Resources/Sprites/player_orange.png")
    p_orange = py.transform.scale(p_orange,[player_size,player_size])
    p_pink = py.image.load("Resources/Sprites/player_pink.png")
    p_pink = py.transform.scale(p_pink,[player_size,player_size])
    p_purple = py.image.load("Resources/Sprites/player_purple.png")
    p_purple = py.transform.scale(p_purple,[player_size,player_size])
    p_red = py.image.load("Resources/Sprites/player_red.png")
    p_red = py.transform.scale(p_red,[player_size,player_size])
    p_white = py.image.load("Resources/Sprites/player_white.png")
    p_white = py.transform.scale(p_white,[player_size,player_size])
    p_yellow = py.image.load("Resources/Sprites/player_yellow.png")
    p_yellow = py.transform.scale(p_yellow,[player_size,player_size])
    player_sprites = [[p_blue,"Blue"],[p_green,"Green"],[p_orange,"Orange"],[p_pink,"Pink"],[p_purple,"Purple"],[p_red,"Red"],[p_white,"White"],[p_yellow,"Yellow"]]
    player_colour = 0

    ## enemy sprites
    enemy_sprite = py.image.load("Resources/Sprites/enemy.png")
    enemy_sprite = py.transform.scale(enemy_sprite,[screen_res[1]//16,screen_res[1]//16])

    ## Projectile Sprites
    projectile = py.image.load("Resources/Sprites/projectile.png")
    projectile = py.transform.scale(projectile,[screen_res[1]//25,screen_res[1]//25])

    ## Shield Sprite
    shield = py.image.load("Resources/Sprites/shield.png")
    shield = py.transform.scale(shield,[screen_res[1]//10,screen_res[1]//10])
    
    ## Importing power up icons
    upgrade_sprites = []
    for i in range(5):
        temp = py.image.load("Resources/Sprites/pup"+str(i)+".png")
        temp = py.transform.scale(temp,[screen_res[1]//16,screen_res[1]//16])
        upgrade_sprites.append(temp)
    
    ## Loading background images
    backgrounds = []
    background = 0
    for i in range(3):      
        temp = py.image.load("Resources/Images/background"+str(i)+".jpg")
        temp = py.transform.scale(temp,screen_res)
        backgrounds.append(temp)
     
    ## Loading sound files and setting their volumes
    game_music = py.mixer.Sound("Resources/Sound/game_music.ogg")
    game_music.set_volume(music_volume/100)
    title_music = py.mixer.Sound("Resources/Sound/title_music.ogg")
    title_music.set_volume(music_volume/100)
    click_sound.set_volume(sfx_volume/100)
    click_sound.set_volume(volumes[1]/100)
    hit_sounds = []
    for i in range(4):
        temp = py.mixer.Sound("Resources/Sound/hit_"+str(i)+".ogg")
        temp.set_volume(sfx_volume/100)
        hit_sounds.append(temp)
    shot_sounds = []
    for i in range(4):
        temp = py.mixer.Sound("Resources/Sound/shoot_"+str(i)+".ogg")
        temp.set_volume(sfx_volume/100)
        shot_sounds.append(temp)

    ## A variable which stores which screen is being displays
    current_screen = "t"

    ## Creating the main keyboard and radio
    radio = Radio()
    key = Keyboard(controls)
    
    ## A variable for mouse click cooldown
    m_cool = 0
    
    ## A variable for the esc key cooldown
    esc_cool = 0
    
    ## A variable for the reset key cooldown
    r_cool = 0
    
    ## Creating the enemy list
    enemy_list = []
    
    ## Variable for enemy spawn delay
    enemy_delay = 0
    
    ## Setting the wave
    wave = 1
    
    ## Variable that stores the amount enemies in killed in the current wave
    wv_enemy_count = 0
    
    ## Variable that stores the game difficulty
    difficulty = 1
    
    ## Variable that stores the total enemies killed across all waves
    total_killed = 0
    
    ## List of upgrade drops
    upgrade_list = []
    
    ## Variables for the settings in the titlescreen
    left = False
    right = False
    
    ## List of positions for enemy sprites in the settings
    enemy_pos_set = []
    for i in range(10):
        enemy_pos_set.append([random.randrange(2*screen_res[0]//5,screen_res[0]-screen_res[1]//16),random.randrange(0,screen_res[1]-screen_res[1]//16)])

    ## List of position and directions for enemy sprites on the titlescreen
    title_enemies = []

## Main loop
while not done:
    # --- Main event loop
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True
            
        ## Updating keyboard key bools
        key.update(event)
        
    ## If reset key is pressed  
    if current_screen == "r":
        current_screen = "g"
        
        ## Update the highscore if the player beat it
        if highscore[difficulty-1] < total_killed:
            highscore[difficulty-1] = total_killed
            UpdateScore(highscore,difficulty,lines)
            
        ## Reset all variables to start the game again
        upgrade_list = []
        wave = 1
        total_killed = 0
        del player
        player_sprite = player_sprites[player_colour]
        player = Player(player_sprite[0],[screen_res[0]//2-player_size//2,screen_res[1]//2-player_size//2],projectile,player_size,shield)
        enemy_list = []
        r_cool = 10
        wv_enemy_count = 0
        
    ## Update the radia if no sound is playing    
    if current_screen == "g" or current_screen == "t":
        if radio.sound != None:
            radio.update()
      
    ## Setting the mouse position
    m_pos = py.mouse.get_pos()
    
    ## Changes the mouse click bool
    if py.mouse.get_pressed()[0] and m_cool <= 0 :
        click = True
        
        ## Play a sound if the player clicks the mouse
        if current_screen != "g":
            m_cool = 5
            click_sound.play()
    else:
        click = False
        
        ## If the player does not click continue decreasing the mouse cooldown variable
        m_cool -= 1
        
    ## Drawing the background to the screen
    screen.blit(backgrounds[background],[0,0])
    
    ## Code for the titlescreen
    if current_screen == "t":
        
        ## 1/50 chance of a enemy sprite to spawn on the titlescreen per frame
        if random.randrange(50) == 0:
            x = random.choice([-screen_res[1]//16,screen_res[0]])
            if x == -screen_res[1]//16:
                y = 1
            else:
                y = -1
            title_enemies.append([x,random.randrange(0,15*screen_res[1]//16),y,resize(random.randrange(6,9)
                                                                                      ,screen_res[0]),screen_res[0]])
        ## Drawing the titlescreen enemy sprites and deleting them if they are off screen
        temp = 0   
        for i in range(len(title_enemies)):
            screen.blit(enemy_sprite,[title_enemies[i-temp][0],title_enemies[i-temp][1]])
            title_enemies[i-temp][0] += title_enemies[i-temp][2] * title_enemies[i-temp][3]
            if not check_collision([-screen_res[0]//4,-screen_res[1]//4],[title_enemies[i-temp][0],title_enemies[i-temp][1]],[1.5*screen_res[0],1.5*screen_res[1]],[screen_res[1]//16,screen_res[1]//16]):
                title_enemies.pop(i-temp)    
                temp += 1

        ## Playing the titlescreen music if it is not already    
        if radio.time < 1 or radio.sound != title_music:
            radio.play(title_music)
            
        ## For loop for main title options; Play, Highscores, Credits, and Quit
        for i in range(len(title_strings)):
            
            ## Text and buttons
            text = font(int(resize(70,screen_res[0]))).render(title_strings[i],True,Blue)
            if screen_res[0]//20 <= m_pos[0] <= screen_res[0]//20 + text.get_width() and screen_res[1]//20 + i*screen_res[1]//8 <= m_pos[1] <= screen_res[1]//20 + i*screen_res[1]//8 + text.get_height():
                text = font(int(resize(70,screen_res[0]))).render(title_strings[i],True,Green)
                if click:
                    
                    ## If play start the game
                    if i == 0:
                        current_screen = "g"
                        total_killed = 0
                        player_sprite = player_sprites[player_colour]
                        player = Player(player_sprite[0],[screen_res[0]//2-player_size//2,screen_res[1]//2-player_size//2],projectile,player_size,shield)
                    else:
                        current_screen = title_strings[i][0].lower() 
            screen.blit(text,[screen_res[0]//20,screen_res[1]//20+i*screen_res[1]//8])
            
        ## If the current screen has changed delete the titlescreen enemies
        if current_screen != "t":
            title_enemies = []
            
    ## Code for highscores screen
    elif current_screen == "h":
        
        ## For loop to display the highscores for each of the 10 difficulties in a blue to red gradient
        for i in range(10):
            text = font(int(resize(35,screen_res[0]))).render("Difficulty "+str(i+1)+": "+str(highscore[i])+" Enemies",True,(22*i,0,100))
            screen.blit(text,[screen_res[0]//20,screen_res[1]//20+i*screen_res[1]//11])
            if key.controls[1][1]:
                current_screen = "t"
                        
    ## Code for credits screen          
    elif current_screen == "c":
        
        ## For loop to draw the credits screen text
        for i in range(len(credits_text)):
            if i%2 == 0:
                temp = Blue
            else:
                temp = Black
            text = font(int(resize(40,screen_res[0]))).render(credits_text[i],True,(temp))
            screen.blit(text,[screen_res[0]//20,screen_res[1]//20+i*screen_res[1]//9])
            
        ## If escape is press go back to the titlescreen
        if key.controls[1][1]:
            current_screen = "t"
            
    ## Code for settings
    elif current_screen == "s":
        
        ## Drawing enemy sprites in the settings according to the difficulty
        for i in range(difficulty):
            screen.blit(enemy_sprite,enemy_pos_set[i])
            
        ## Drawing the player sprite in the settings
        screen.blit(player_sprites[player_colour][0],[screen_res[0]//7,screen_res[1]//2])
        
        ## Settings buttons and text code
        for i in range(3):
            text1 = font(int(resize(70,screen_res[0]))).render("<",True,Black)
            if i == 1:
                x = str(difficulty)
            else:
                x = ""
            text2 = font(int(resize(50,screen_res[0]))).render(" "+setting_strings[i]+x+" ",True,((difficulty-1)*25,0,100))
            text3 = font(int(resize(70,screen_res[0]))).render(">",True,Black)
            
            ## If you hit the left arrow make left true
            if screen_res[0]//20 <= m_pos[0] <= screen_res[0]//20 + text1.get_width() and screen_res[1]//20 + i*screen_res[1]//8 <= m_pos[1] <= screen_res[1]//20 + i*screen_res[1]//8 + text1.get_height():
                text1 = font(int(resize(70,screen_res[0]))).render("<",True,Green)
                if click:
                    left = True
                    
            ## If you hit the left arrow make right true    
            elif screen_res[0]//20+text1.get_width()+text2.get_width() <= m_pos[0] <= screen_res[0]//20+text1.get_width()+text2.get_width()+text3.get_width() and screen_res[1]//20 + i*screen_res[1]//8 <= m_pos[1] <= screen_res[1]//20 + i*screen_res[1]//8 + text1.get_height():
                text3 = font(int(resize(70,screen_res[0]))).render(">",True,Green)
                if click:
                    right = True
                    
            ## Drawing button text
            screen.blit(text1,[screen_res[0]//20,screen_res[0]//24 + i*screen_res[1]//8])
            screen.blit(text2,[screen_res[0]//20+text1.get_width(),screen_res[0]//20 + i*screen_res[1]//8])
            screen.blit(text3,[screen_res[0]//20+text1.get_width()+text2.get_width(),screen_res[0]//24 + i*screen_res[1]//8])

            ## If left adjust variables accordingly
            if left:
                if i == 0:
                    if player_colour != 0:
                        player_colour -= 1
                    else:
                        player_colour = len(player_sprites)-1
                elif i == 1:
                    if difficulty != 1:
                        difficulty -= 1
                else:
                    if background != 0:
                        background -= 1
                    else:
                        background = len(backgrounds)-1
                left = False
                
            ## If right adjust variables accordingly
            if right:
                if i == 0:
                    if player_colour != len(player_sprites)-1:
                        player_colour += 1
                    else:
                        player_colour = 0
                elif i == 1:
                    if difficulty != 10:
                        difficulty += 1
                else:
                    if background != len(backgrounds)-1:
                        background += 1
                    else:
                        background = 0
                right = False
                
        ## If the escape key is pressed
        if key.controls[1][1]:
            current_screen = "t"
        
    ## Code for the gamescreen
    elif current_screen == "g":
        for i in range(len(upgrade_list)):
            if i == 0:
                temp = 0
                
            ## Updating the upgrades in the list
            upgrade_list[i-temp].update(screen)
            
            ## If upgrade is not picked up in 5 seconds it despawns
            if upgrade_list[i-temp].time < 1:
                upgrade_list.remove(upgrade_list[i-temp])
                temp += 1
                
            ## If the player touches the upgrade sprites, they pick them up and the upgrade is deleted
            elif check_collision(player.pos,[upgrade_list[i-temp].x,upgrade_list[i-temp].y],[screen_res[1]//12,screen_res[1]//12],[screen_res[1]//16,screen_res[1]//16]):
                player.upgrades.append(upgrade_list[i-temp].u_type)
                player.upgrade_times.append(300)
                upgrade_list.pop(i-temp)
                temp += 1
                
        ## Enemy spawning
        if enemy_delay%int(spawn_rate(difficulty,wave)) == 0:
            
            ## If all the enemies are killed start the next wave
            if int(enemy_amount(difficulty,wave)) <= wv_enemy_count:
                wave += 1
                wv_enemy_count = 0
                
            ## Else spawn another enemy
            elif wv_enemy_count + len(enemy_list) < int(enemy_amount(difficulty,wave)):
                enemy = Enemy(enemy_sprite,screen)
                enemy_list.append(enemy)
                
        ## Bomb power up kills everything on screen if you pick it up        
        if list_check(player.upgrades,4):
            i2 = 0
            for i in range(len(enemy_list)):
                if len(enemy_list) != 0:
                    if check_collision([0,0],enemy_list[i-i2].pos,[screen_res[0],screen_res[1]],[screen_res[1]//16,screen_res[1]//16]):
                        enemy_list.pop(i-i2)
                        wv_enemy_count +=1
                        i2+=1
                        random.choice(hit_sounds).play()
                        total_killed += 1
                        
        ## Increasing the enemy delay variable    
        enemy_delay+=1

        ## If the reset button is pressed reset the game
        if key.controls[0][1] and r_cool < 0:
            current_screen = "r"
            r_cool = 5
        else:
            r_cool -= 1
            
        ## If the game music isnt playing start playing the it
        if radio.time < 1 or radio.sound != game_music:
            radio.play(game_music)
            
        ## Update all the enemies
        for i in enemy_list:
            i.update(player,screen)
            
        ## Update the player
        player.update(key.controls,screen)
        
        ## If the player clicks shoot
        if click and m_cool < 1:
            
            ## If the player has the fire rate upgrade the cooldown is lower
            if list_check(player.upgrades,0):
                m_cool = 3
            else:
                m_cool = 6
                
            ## Player shoots 
            player.shoot(m_pos,screen)
            
            ## Play a shot sound
            random.choice(shot_sounds).play()
            
        ## For loop for collision between enemies and player projectiles
        i2 = 0
        for i in range(len(enemy_list)):
            j2 = 0
            for j in range(len(player.shots)):
                if len(enemy_list) != 0:
                    if check_collision([player.shots[j-j2].x,player.shots[j-j2].y],enemy_list[i-i2].pos,[screen_res[1]//25,screen_res[1]//25],[screen_res[1]//16,screen_res[1]//16]):
                        ## 20% chance to spawn an upgrade
                        if random.randrange(100) <= 20:
                            temp = random.randrange(5)
                            upgrade_list.append(Upgrade(enemy_list[i-i2].pos,temp,upgrade_sprites[temp]))
                        ## Deleting the shot
                        player.shots.pop(j-j2)
                        ## Deleting the enemy
                        enemy_list.pop(i-i2)
                        ## Increasing the enemy wave kill count
                        wv_enemy_count +=1
                        j2+=1
                        i2+=1
                        ## Play a hit sound
                        random.choice(hit_sounds).play()
                        ## Increasing the the total kill count
                        total_killed += 1
                        
        ## For loop between the player and enemies; this code is ignored if the player has the shield upgrade
        if not list_check(player.upgrades,3): 
            for i in range(len(enemy_list)):
                pos1 = [player.pos[0]+player_size//2,player.pos[1]+player_size//2]
                pos2 = enemy_list[i].pos
                if check_collision(pos1,pos2,[1,1],[screen_res[1]//16,screen_res[1]//16]):
                    current_screen = "go"
                    
        ## If escape is hit pause the game
        if key.controls[1][1] and esc_cool <= 0:
            current_screen = "p"
            esc_cool = 10
        esc_cool -=1

        ## Printing wave and score info to the screen
        text = font(int(resize(45,screen_res[0]))).render("Wave: "+str(wave),True,Blue)  
        screen.blit(text,[screen_res[1]//50,screen_res[1]//50])
        
        text = font(int(resize(45,screen_res[0]))).render("Enemies: "+str(int(enemy_amount(difficulty,wave))-wv_enemy_count),True,Blue)  
        screen.blit(text,[screen_res[1]//50,screen_res[1]//10])

        ## Showing the upgrades that the player currently has
        for i in range(len(set(player.upgrades))):
            screen.blit(upgrade_sprites[list(set(player.upgrades))[i]],[screen_res[1]//50,(9+i*4)*screen_res[1]//50])
                                  
    ## Code for the pause screen
    elif current_screen == "p":
        
        ## Paused text printingto the screen
        text = font(int(resize(50,screen_res[0]))).render("Paused",True,Blue)
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,screen_res[1]//5])
        
        ## Titlescreen text and button
        text = font(int(resize(50,screen_res[0]))).render("Titlescreen",True,Blue)
        if screen_res[0]//2-text.get_width()//2 < m_pos[0] < screen_res[0]//2+text.get_width()//2 and screen_res[1]//5 + screen_res[1]//10 < m_pos[1] < screen_res[1]//5 + screen_res[1]//10 + text.get_height():
            text = font(int(resize(50,screen_res[0]))).render("Titlescreen",True,Green)
            if click:
                if highscore[difficulty-1] < total_killed:
                    highscore[difficulty-1] = total_killed
                    UpdateScore(highscore,difficulty,lines)
                current_screen = "t"
                enemy_list = []
                enemy_delay = 0
                wave = 1
                wv_enemy_count = 0
                del player
                upgrade_list = []
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,screen_res[1]//5+screen_res[1]//10])

        ## Quit text and button
        text = font(int(resize(50,screen_res[0]))).render("Quit",True,Blue)
        if screen_res[0]//2-text.get_width()//2 < m_pos[0] < screen_res[0]//2+text.get_width()//2 and 2 * screen_res[1]//5 < m_pos[1] < 2 * screen_res[1]//5 + text.get_height():
            text = font(int(resize(50,screen_res[0]))).render("Quit",True,Green)
            if click:
                done = True
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,2*screen_res[1]//5])
        
        ## Code for the escape key
        if key.controls[1][1] and esc_cool <= 0:
            current_screen = "g"
            esc_cool = 5
            
        ## Reset code for the pause screen
        elif key.controls[0][1] and r_cool < 0:
            current_screen = "r"
            r_cool = 5
        else:
            r_cool -= 1
            esc_cool -=1

    ## Code for the gameover screen    
    elif current_screen == "go":
        ## Game over text on the gameover screen
        text = font(int(resize(50,screen_res[0]))).render("Game Over",True,(211,38,38))
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,screen_res[1]//5])

        ## Titlescreen button on the gameover screen
        text = font(int(resize(50,screen_res[0]))).render("Titlescreen",True,Black)
        if screen_res[0]//2-text.get_width()//2 < m_pos[0] < screen_res[0]//2+text.get_width()//2 and screen_res[1]//5+screen_res[1]//10 < m_pos[1] < screen_res[1]//5+screen_res[1]//10 + text.get_height():
            text = font(int(resize(50,screen_res[0]))).render("Titlescreen",True,Green)
            if click:
                if highscore[difficulty-1] < total_killed:
                    highscore[difficulty-1] = total_killed
                    UpdateScore(highscore,difficulty,lines)
                current_screen = "t"
                enemy_list = []
                enemy_delay = 0
                wave = 1
                wv_enemy_count = 0
                del player
                upgrade_list = []
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,screen_res[1]//5+screen_res[1]//10])

        ## Quit button text on the gameover screen
        text = font(int(resize(50,screen_res[0]))).render("Quit",True,Black)
        if screen_res[0]//2-text.get_width()//2 < m_pos[0] < screen_res[0]//2+text.get_width()//2 and 2 * screen_res[1]//5 < m_pos[1] < 2 * screen_res[1]//5 + text.get_height():
            text = font(int(resize(50,screen_res[0]))).render("Quit",True,Green)
            if click:
                current_screen = "q"
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,2*screen_res[1]//5])
        
        ## Stats text on the gameover screen
        text = font(int(resize(50,screen_res[0]))).render("You made it to wave: "+str(wave),True,Black)
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,screen_res[1]//5+3*screen_res[1]//10])
        text = font(int(resize(50,screen_res[0]))).render("and you killed "+str(total_killed)+" enemies.",True,Black)
        screen.blit(text,[screen_res[0]//2-text.get_width()//2,3*screen_res[1]//5])
        
        ## Reset code for the gameover screen
        if key.controls[0][1] and r_cool < 0:
            current_screen = "r"
            r_cool = 5
        else:
            r_cool -= 1
    elif current_screen == "q":
        done = True
        
    ## Flipping the screen
    py.display.flip()
    
    ## Setting the fps
    clock.tick(30)
    
## Allows you to quit
py.quit()        
    
## Sets the lines to be wrote to the text file
lines = [str(resolutions.index(screen_res_o)),str(volumes[0]),str(volumes[1])]
for i in controls:
    lines.append(str(i))
temp = ""
for i in highscore:
    temp += str(i)+" "

lines.append(temp)
    
## Writes the lines variable to the text file    
with open('Resources/settings.txt','w') as x:
    x.writelines("%s\n" % l for l in lines)
x.close()
