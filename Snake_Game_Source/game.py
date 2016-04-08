# -*- coding: utf-8 -*-

import pygame
import random
import os
import sys

#Initialize pygame
pygame.init()

#Colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (0, 255, 255)
snake_Head_image = pygame.image.load(os.path.join('Content/Sprites', 'SnakeHead.png'))
snake_Body_image = pygame.image.load(os.path.join('Content/Sprites', 'SnakeBody.png'))
apple_image = pygame.image.load(os.path.join('Content/Sprites', 'Apple.png'))
icon_image = pygame.image.load(os.path.join('Content/Sprites', 'Icon.png'))

#Music:
bg_music = pygame.mixer.music.load(os.path.join('Content/Music', 'bitjam_159.ogg'))
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)

#Sounds:
eat_sound = pygame.mixer.Sound(os.path.join('Content/Sounds', 'Eating_Sound.wav'))
eat_sound.set_volume(1.0)

#Variables:
block_size = 10
clock = pygame.time.Clock()
direction = "right"
if os.name == 'nt':
    default_font = "Comic Sans MS"
else:
    default_font = "Ubuntu"
smallfont = pygame.font.SysFont(default_font, 25)
mediumfont = pygame.font.SysFont(default_font, 40)
bigfont = pygame.font.SysFont(default_font, 55)

#Set Display Parameters
infoObject = pygame.display.Info()
global display_width
global display_height
wd_display_width = 800
wd_display_height = 600
fs_display_width = infoObject.current_w
fs_display_height = infoObject.current_h
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white)
pygame.display.set_caption('Snake')
pygame.display.set_icon(icon_image)
FPS = 15
global is_fullscreen
is_fullscreen = False

#Defining Fuctions:
def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def game_intro():
    global is_fullscreen
    f = open(os.path.join('Content', "score.txt"), "r")
    highscore = f.read()
    highscore = int(highscore)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if is_fullscreen == False:
                            pygame.display.set_mode((fs_display_width, fs_display_height), pygame.FULLSCREEN)
                            display_width = fs_display_width
                            display_height = fs_display_height
                            pygame.mouse.set_visible(False)
                            is_fullscreen = True
                    else:
                            pygame.display.set_mode((wd_display_width, wd_display_height))
                            display_width = wd_display_width
                            display_height = wd_display_height
                            pygame.mouse.set_visible(True)
                            is_fullscreen = False
                if event.key == pygame.K_o:
                    volume = pygame.mixer.music.get_volume()
                    volume += 0.1
                    pygame.mixer.music.set_volume (volume)
                if event.key == pygame.K_l:
                    volume = pygame.mixer.music.get_volume()
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to this Snake-Game!", green, -150, "big")
        message_to_screen("The objective of the Game is to eat the red apples", black, -30, "small")
        message_to_screen("The more Apples you eat, the longer you get", black, 10, "small")
        message_to_screen("If you run into yourself, or the edges, you die!", black, 50, "small")
        message_to_screen("Press 'C' to play and 'Q' to quit", blue, 90, "small")
        message_to_screen("High Score: " + str(highscore), black, 130, "small")
        message_to_screen("Good Luck!", red, 180, "medium")
        pygame.display.update()
        clock.tick(15)

def snake(snakelist):
    if direction == "right":
        head = pygame.transform.rotate(snake_Head_image, 180)
    if direction == "left":
        head = pygame.transform.rotate(snake_Head_image, 0)
    if direction == "up":
        head = pygame.transform.rotate(snake_Head_image, 270)
    if direction == "down":
        head = pygame.transform.rotate(snake_Head_image, 90)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        gameDisplay.blit(snake_Body_image, [XnY[0], XnY[1]])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = mediumfont.render(text, True, color)
    if size == "big":
        textSurface = bigfont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    #Defining Variables:
    global display_width
    global display_height
    blocksize = 10
    AppleThickness = 10
    lead_x = (display_width/2)
    lead_y = (display_height/2)
    lead_x_change = blocksize
    lead_y_change = 0
    gameExit = False
    gameOver = False
    randAppleX = round(random.randrange(0, display_width-AppleThickness))
    randAppleY = round(random.randrange(0, display_height-AppleThickness))
    snakeList = []
    snakeLength = 1
    global direction
    direction = 'right'
    saved = False
    win = False
    global is_fullscreen

    #Actual Game
    while not gameExit:

        while gameOver == True:
            if not saved:
                f = open(os.path.join('Content', 'score.txt'), 'r')
                lastscore = f.read()
                lastscore = int(lastscore)
                f.close
                if lastscore < (snakeLength-1):
                    f = open(os.path.join('Content', 'score.txt'), 'w')
                    f.write(str(snakeLength-1))
                    f.close()
                    win = True
                    lastscore = str(snakeLength-1)
                    saved = True
                else:
                    win = False
                    saved = True
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -100, "big")
            if win == True:
                message_to_screen("New Highscore: " + str(snakeLength-1), black, -50, "medium")
            else:
                message_to_screen("No new Highscore, try again!", black, -50, "medium")
            message_to_screen("Press 'C' to play again or 'Q' to quit", red, 50, "small")
            message_to_screen("High Score :" + str(snakeLength-1) + "/" + str(lastscore), black, 90, "small")
            pygame.display.update()

            for event in pygame.event.get():
                #Quit Event
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                #Key Events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_F11:
                        if is_fullscreen == False:
                            pygame.display.set_mode((fs_display_width, fs_display_height), pygame.FULLSCREEN)
                            display_width = fs_display_width
                            display_height = fs_display_height
                            pygame.mouse.set_visible(False)
                            is_fullscreen = True
                        else:
                            pygame.display.set_mode((wd_display_width, wd_display_height))
                            display_width = wd_display_width
                            display_height = wd_display_height
                            pygame.mouse.set_visible(True)
                            is_fullscreen = False
                    if event.key == pygame.K_o:
                        volume = pygame.mixer.music.get_volume()
                        volume += 0.1
                        pygame.mixer.music.set_volume (volume)
                    if event.key == pygame.K_l:
                        volume = pygame.mixer.music.get_volume()
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)

        #Event Handling
        for event in pygame.event.get():
            #Quit Event
            if event.type == pygame.QUIT:
                gameExit = True
            #Key Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameOver = True
                if event.key == pygame.K_LEFT:
                    lead_x_change = -blocksize
                    lead_y_change = 0
                    direction = "left"
                if event.key == pygame.K_RIGHT:
                    lead_x_change = blocksize
                    lead_y_change = 0
                    direction = "right"
                if event.key == pygame.K_UP:
                    lead_y_change = -blocksize
                    lead_x_change = 0
                    direction = "up"
                if event.key == pygame.K_DOWN:
                    lead_y_change = blocksize
                    lead_x_change = 0
                    direction = "down"
                if event.key == pygame.K_o:
                    volume = pygame.mixer.music.get_volume()
                    volume += 0.1
                    pygame.mixer.music.set_volume (volume)
                if event.key == pygame.K_l:
                    volume = pygame.mixer.music.get_volume()
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)

        #Game Logic:
        #Movement Logic
        lead_x += lead_x_change
        lead_y += lead_y_change
        #Defining Borders
        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
            gameOver = True
        #Graphics Management
        gameDisplay.fill(white)
        gameDisplay.blit(apple_image, [randAppleX, randAppleY])
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        snake(snakeList)
        score(snakeLength-1)
        pygame.display.update()
        clock.tick(FPS)
        #Apple Eat:
        if lead_x >= randAppleX  and lead_x <= randAppleX + AppleThickness or lead_x + block_size >= randAppleX and lead_x + block_size <= randAppleX + AppleThickness:
            if lead_y >= randAppleY  and lead_y <= randAppleY + AppleThickness or lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + AppleThickness:
                eat_sound.play()
                randAppleX = round(random.randrange(0, display_width - AppleThickness))
                randAppleY = round(random.randrange(0, display_height - AppleThickness))
                snakeLength += 1

    #Quit Game
    pygame.quit()
    sys.exit()
game_intro()
gameLoop()
pygame.mixer.music.stop()
