#space invaders game
import pygame
import os
import time
import random

pygame.init()


#print(pygame.__version__)

#load fighters
bee = pygame.image.load("resources/Bee.png")
fly = pygame.image.load("resources/Fly.png")
plane = pygame.image.load("resources/BluePlane.png")

#load shooters
bee_shooter = pygame.image.load("resources/shooter-blue.png")
fly_shooter = pygame.image.load("resources/shooter-red.png")
plane_shooter = pygame.image.load("resources/shooter-green.png")
sprite_shooter = pygame.image.load("resources/shooter-sprite.png")

#load sprite (main player)
sprite = pygame.image.load("resources/Neha_Sprite.png")

#create the screen and configure the screen size and caption
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
screen.fill("#87CEEB")
pygame.display.set_caption("SpartanDash")
pygame.display.flip()

#load and scale background
DEFAULT_SIZE = (350, 245)
background = pygame.image.load("resources/tower_lawn.png")
original_width, original_height = background.get_size()
new_height = int((screen_info.current_w / original_width) * original_height)
background = pygame.transform.scale(background, (screen_info.current_w, new_height))

font = pygame.font.Font("resources/Grand9KPixel.ttf", 25)

#main loop
def run():
    running = True
    timer = pygame.time.Clock()
    FPS = 60 #frames per second for speed
    level = 1
    lives = 5

    while running:
        timer.tick(FPS)
        set_background(level, lives)

        for event in pygame.event.get():
            #exit the loop and close the screen in player quits
            if event.type == pygame.QUIT:
                running = False

def set_background(level, lives):
    #draw background to screen
    screen.blit(background, (0,0)) 
    pygame.display.update()

    levels_text = font.render(f"Level: {level}", True, "#ebfbfc")
    lives_text = font.render(f"Lives: {lives}", True, "#ebfbfc")

    screen.blit(levels_text, (10, 10))
    screen.blit(lives_text, (10, 50))

run()     
